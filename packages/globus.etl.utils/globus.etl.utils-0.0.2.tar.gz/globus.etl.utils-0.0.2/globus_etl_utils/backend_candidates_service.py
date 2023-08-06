import json
import os
import requests
from time import sleep
from backend_service import BackendService

class BackendCandidatesService(BackendService):

    def send(self, tenant_id: str, data: list) -> dict:
        auth_token = self.__get_auth_token_from_cache__(tenant_id)

        url = f"{self.base_url}/api/Candidates/UpsertCandidates"

        for i in range(3):
            response = requests.request("POST", url, json = data, headers = auth_token.auth_headers)
            
            print(response.status_code, response.content)
            
            if response.status_code != 200:
                sleep(i * 60)
                continue
            break

        if (not response.ok):
            raise Exception(f"An error occurred during posting candidates to the backend. \
                SatusCode: {response.status_code} Reason: {response.reason}")