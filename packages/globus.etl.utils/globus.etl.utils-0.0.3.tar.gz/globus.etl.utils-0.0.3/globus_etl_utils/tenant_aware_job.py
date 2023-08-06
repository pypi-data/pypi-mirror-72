import json
import os
import pymongo
import itertools

from globus_etl_utils.tenant_service import TenantService
from globus_etl_utils.persistance_service import PersistanceService
from globus_etl_utils.job import Job

class TenantAwareJob(Job):
    
    tenant_service: TenantService

    def __init__(
        self, 
        tenant_service: TenantService, 
        persistance_service: PersistanceService
    ):
        super().__init__(persistance_service)

        self.tenant_service = tenant_service
    
    
    def run(self):
        tenants = self.tenant_service.list_tenants()
        
        for tenant in tenants:
            self._on_process_tenant(tenant)
        
        groups_of_tenants = itertools.groupby(
            sorted(tenants, key = self._get_tenant_group_key), 
            key = self._get_tenant_group_key
        )

        for group_key, group_of_tenants in groups_of_tenants:
            _group_of_tenants = list(group_of_tenants)
            self._on_process_group_of_tenants(group_key, _group_of_tenants)
        
        self._on_process_all_tenants(tenants)
        self._on_process_master_data(self.tenant_service.mongo_db_cfg['master_db'], 
                                     self.tenant_service.mongo_db_cfg['master_internal_name'])


    def _on_process_tenant(
        self, 
        tenant: dict
    ):
        pass

    
    def _get_tenant_group_key(
        self, 
        tenant: dict
    ) -> object:
        return tenant['InternalName']

    
    def _on_process_group_of_tenants(
        self, 
        tenant_group: object, 
        tenants: list
    ):
        pass


    def _on_process_all_tenants(
        self, 
        tenants: list
    ):
        pass


    def _on_process_master_data(
        self, 
        master_db: str,
        master_internal_name: str
    ):
        pass