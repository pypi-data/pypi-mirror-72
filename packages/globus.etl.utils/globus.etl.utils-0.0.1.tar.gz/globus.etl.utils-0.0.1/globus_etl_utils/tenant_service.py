import json
import os
import pymongo
import itertools

class TenantService(object):
    
    mongo_db_cfg: dict

    mongo_client: pymongo.MongoClient
    mongo_master_db: pymongo.database.Database
    mongo_tenants_colection: pymongo.collection.Collection

    conn_str: str

    def __init__(
        self, 
        mongo_db_cfg: dict
    ):
        super().__init__()

        self.mongo_db_cfg = mongo_db_cfg

        self.conn_str = self.get_conn_str()

        self.mongo_client = pymongo.MongoClient(self.conn_str)
        self.mongo_master_db = self.mongo_client.get_database(self.mongo_db_cfg['master_db'])
        
        self.mongo_tenants_colection = self.mongo_master_db.get_collection('Tenants')    


    def get_conn_str(self):
        return \
            f"mongodb://" \
                + f"{self.mongo_db_cfg['user_name']}" + ':' \
                + f"{self.mongo_db_cfg['user_password']}" + '@' \
                + f"{self.mongo_db_cfg['dns_srv']}" + '/' \
                + "?authSource=admin&connectTimeoutMS=300000"
    
   
    def list_tenants(self) -> list:

        recman_key = os.environ.get("RECMAN_KEY")
        tenants = list(self.mongo_tenants_colection.find({}))
        for tenant in tenants:
            if tenant['RecmanService']['IsUsed'] == True:
                tenant['RecmanService']['ReadKey'] = recman_key

        return tenants