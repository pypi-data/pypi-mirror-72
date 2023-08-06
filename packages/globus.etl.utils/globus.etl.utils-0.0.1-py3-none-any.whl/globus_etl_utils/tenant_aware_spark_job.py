import json
import os
import pymongo
import itertools

from pyspark.sql import *
from pyspark.sql.window import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.dbutils import DBUtils

from tenant_service import TenantService
from persistance_service import PersistanceService
from tenant_aware_job import TenantAwareJob
from spark import rec_ren

class TenantAwareSparkJob(TenantAwareJob):
    spark_config: dict
    spark: SparkSession

    def __init__(
        self,
        tenant_service: TenantService, 
        persistance_service: PersistanceService,
        spark_cfg: dict,
        job_name: str
    ):
        super().__init__(tenant_service, persistance_service)

        self.spark_cfg = spark_cfg

        SparkSession.builder.config("spark.app.id", job_name)
        SparkSession.builder.config("spark.databricks.service.address", self.spark_cfg["address"])
        SparkSession.builder.config("spark.databricks.service.token", self.spark_cfg["token"])
        SparkSession.builder.config("spark.databricks.service.clusterId", self.spark_cfg["clusterId"])
        SparkSession.builder.config("spark.databricks.service.orgId", self.spark_cfg["orgId"])
        SparkSession.builder.config("spark.databricks.service.port", self.spark_cfg["port"])
        self.spark = SparkSession.builder.getOrCreate()


    def _enforce_naming_notation(
        self,
        df: DataFrame
    ) -> DataFrame:
        return self.spark \
            .createDataFrame(
                df.rdd,
                rec_ren(df.schema, lambda x: x[:1].upper() + x[1:])
            )
    
    
    def _save_data(
        self,
        df: DataFrame,
        tenant: dict,
        collection: str,
        write_mode: str = "append"
    ):
        df \
            .repartition(3) \
            .write \
            .format("com.mongodb.spark.sql.DefaultSource") \
            .mode(write_mode) \
            .option("uri", self.tenant_service.get_conn_str()) \
            .option("database", tenant['Database']) \
            .option("collection", collection) \
            .option("replaceDocument", "true") \
            .save()
        

    def _collapse_to_single_file(
        self,
        old_file_path_prefix: str, 
        new_file_path_prefix: str
    ):
        dbutils = DBUtils(self.spark.sparkContext)
        
        old_file_paths = dbutils.fs.ls(f"{old_file_path_prefix}/")

        partition_path = filter(
            lambda f: f.name.startswith('part-'),
            old_file_paths
        )
        
        partition_path = next(partition_path)

        if not partition_path:
            raise Exception(f"The file path {old_file_path_prefix} does not contain any partitions")
        else:
            partition_path = partition_path.path
        
        dbutils.fs.cp(
            partition_path, 
            new_file_path_prefix
        )

        dbutils.fs.rm(
            old_file_path_prefix, 
            recurse = True
        )
    