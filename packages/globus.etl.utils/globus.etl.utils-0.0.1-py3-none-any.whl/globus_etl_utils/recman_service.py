import json
import os
import pymongo
import itertools

import requests

class RecmanService(object):
    
    base_url: str = 'https://api.recman.no/v2'

    def __init__(
        self
    ):
        super().__init__()
   
   
    def get_data(
        self, 
        key: str, 
        scope: str, 
        data_key: str,
        fields: str = None, 
        page: int = None, 
        updated: str = None,
        **extra_params: dict
    ):
        print(extra_params)
        print(extra_params.items())

        url = f"{self.base_url}/get/?key={key}&scope={scope}" \
            + (f"&fields={fields}" if fields else '') \
            + (f"&page={page}" if page else '') \
            + (f"&updated={updated}" if updated else '') \
            + '&' + '&'.join([f"{name}={value}" for name, value in extra_params.items()])
        
        response = requests.request("GET", url)

        if (response.status_code == 200):
            data = response.json()
            if data.get('success', None):
                if (type(data[data_key]) is dict):
                    return (list(data[data_key].values()), data.get('nextPage', None))
                else:
                    return (data[data_key], data.get('nextPage', None))
            elif data.get('numRows', None) == 0 and not data.get('errors', None):
                return [], None
            else:
                raise Exception(f"An error occurred during getting the data from recman. \
                    SatusCode: {response.status_code} Reason: {response.reason} Url: {url} Data: {data}")

        raise Exception(f"An error occurred during getting the data from recman. \
            SatusCode: {response.status_code} Reason: {response.reason} Url: {url}")