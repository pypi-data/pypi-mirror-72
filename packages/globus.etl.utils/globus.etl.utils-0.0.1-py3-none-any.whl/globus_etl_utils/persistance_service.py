import json
import os
import pymongo
import itertools
from azure.storage.blob import BlockBlobService

class PersistanceService(object):
    
    blob_storage_cfg: dict
    blob_service: BlockBlobService

    def __init__(
        self, 
        blob_storage_cfg: dict
    ):
        super().__init__()

        self.blob_storage_cfg = blob_storage_cfg
        
        self.blob_service = BlockBlobService(
            blob_storage_cfg['account_name'], 
            blob_storage_cfg['account_key']
        )   

    
    def save_data(
        self, 
        name: str, 
        data: str
    ):
        self.blob_service.create_blob_from_text(
            self.blob_storage_cfg['container_name'], 
            name, 
            data
        )


    def save_data_from_file(
        self, 
        name: str,
        file_path: str
    ):
        self.blob_service.create_blob_from_path(
            self.blob_storage_cfg['container_name'], 
            name,
            file_path
        )
        

    def get_data(
        self, 
        name: str
    ) -> str:

        blob = self.blob_service.get_blob_to_text(
            self.blob_storage_cfg['container_name'], 
            name
        )

        return blob.content

    
    def get_data_if_exists(
        self, 
        name: str
    ) -> str:

        container_name = self.blob_storage_cfg['container_name']

        if self.blob_service.exists(container_name, name):
            return self.get_data(name)
        else:
            return None


    def list_items(
        self, 
        prefix: str
    ) -> str:

        blobs = self.blob_service.list_blobs(
            self.blob_storage_cfg['container_name'],
            prefix = prefix
        )

        return [b.name for b in blobs]