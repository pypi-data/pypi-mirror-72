import json
import os
import pymongo
import itertools

from job import Job
from tenant_service import TenantService
from persistance_service import PersistanceService

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