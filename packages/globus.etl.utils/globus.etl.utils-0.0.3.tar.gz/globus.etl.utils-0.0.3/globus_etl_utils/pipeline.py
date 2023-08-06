import json
import os
import pymongo
import itertools

from globus_etl_utils.job import Job
from globus_etl_utils.tenant_service import TenantService
from globus_etl_utils.persistance_service import PersistanceService

class Pipeline(Job):
    
    pipeline: list

    def __init__(
        self,
        persistance_service: PersistanceService ,
        *args
    ):
        super().__init__(persistance_service)

        self.pipeline = args
   
   
    def run(self):
        for job in self.pipeline:
            job.run()
        
        pass