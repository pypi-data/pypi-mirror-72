import json
import os
import itertools

from pyspark.sql import *
from pyspark.sql.window import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.dbutils import DBUtils

from globus_etl_utils.persistance_service import PersistanceService
from globus_etl_utils.job import Job

class SparkJob(Job):

    spark_config: dict
    spark: SparkSession
    persistance_service: PersistanceService

    def __init__(
        self,
        persistance_service: PersistanceService,
        spark_cfg: dict,
        job_name: str
    ):
        super().__init__(persistance_service)

        self.spark_cfg = spark_cfg

        SparkSession.builder.config("spark.app.id", job_name)
        SparkSession.builder.config("spark.databricks.service.address", self.spark_cfg["address"])
        SparkSession.builder.config("spark.databricks.service.token", self.spark_cfg["token"])
        SparkSession.builder.config("spark.databricks.service.clusterId", self.spark_cfg["clusterId"])
        SparkSession.builder.config("spark.databricks.service.orgId", self.spark_cfg["orgId"])
        SparkSession.builder.config("spark.databricks.service.port", self.spark_cfg["port"])
        self.spark = SparkSession.builder.getOrCreate()

        
    def _save_table_to_csv(self, table_name: str, file_path: str):
        self.spark \
            .read \
            .table(table_name) \
            .repartition(1) \
            .write \
            .mode("overwrite") \
            .option("header", "true") \
            .csv(file_path)
    
    