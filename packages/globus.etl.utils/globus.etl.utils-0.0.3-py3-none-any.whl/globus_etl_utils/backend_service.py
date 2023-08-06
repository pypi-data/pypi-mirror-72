import json
import requests
import datetime
import pytz
import dateutil.parser

class AuthToken:
    token: str
    token_expiration_time: datetime.datetime
    auth_headers: str

    def __init__(self, token: str, token_expiration_time: datetime.datetime):
        self.token = token
        self.token_expiration_time = token_expiration_time
        self.auth_headers = {'Content-Type': "application/json",'Authorization': token}


class BackendService:

    base_url: str
    password: str
    auth_token_cache: dict

    def __init__(self, base_url: str, password: str):
        self.auth_token_cache = dict()
        self.base_url = base_url
        self.password = password

    def __get_auth_token__(self, tenant_id: str) -> AuthToken:
        url = self.base_url + "/api/Auth/AuthUser/"
        payload = json.dumps({ "name": tenant_id, "password": self.password})
        headers = { 'Content-Type': "application/json" }
        response = requests.request("POST", url, data = payload, headers = headers)
        
        if (not response.ok):
            raise Exception(f"Can not get an access token. \
                SatusCode: {response.status_code} Reason: {response.reason}")
        
        token = response.json()['_Token']
        token_expiration_time = dateutil.parser.parse(response.json()['expirationDate'])

        return AuthToken(token, token_expiration_time)
        
    def __get_auth_token_from_cache__(self, tenant_id: str):
        auth_token = self.auth_token_cache.get(tenant_id)
        if (auth_token is None):
            auth_token = self.__get_auth_token__(tenant_id)
        
        current_utc_time = datetime.datetime.now(tz=pytz.utc)
        corrected_expiration_time = auth_token.token_expiration_time - datetime.timedelta(minutes=15)
        if (current_utc_time > corrected_expiration_time):
            auth_token = self.__get_auth_token__(tenant_id)

        self.auth_token_cache[tenant_id] = auth_token

        return auth_token
    