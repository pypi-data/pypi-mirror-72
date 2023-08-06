import json
import os
import pymongo
import itertools

from globus_etl_utils.tenant_service import TenantService
from globus_etl_utils.persistance_service import PersistanceService

class Job(object):
    
    persistance_service: PersistanceService

    def __init__(
        self, 
        persistance_service: PersistanceService
    ):
        super().__init__()

        self.persistance_service = persistance_service
   

    def run(self):
        pass


    def _get_save_point_file_name(
        self, 
        recman_key: str, 
        scope_name: str
    ) -> str:
        return 'savepoint.json'


    def _get_save_point(
        self, 
        recman_key: str, 
        scope_name: str, 
        default_value: dict
    ) -> dict:
        file_name = self._get_save_point_file_name(recman_key, scope_name)

        save_point = self.persistance_service.get_data_if_exists(file_name)
        save_point = save_point and json.loads(save_point) or default_value

        return save_point
    

    def _persist_save_point(
        self, 
        recman_key: str, 
        scope_name: str, 
        value: dict
    ):
        file_name = self._get_save_point_file_name(recman_key, scope_name)

        self.persistance_service.save_data(file_name, json.dumps(value))
