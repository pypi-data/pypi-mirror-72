import os
import json
import requests
import pandas as pd
from typing import Union
from google.oauth2.service_account import Credentials

from siametrics.deepmap.dataset import DatasetDiscoveryService
from .util import default_key_path, get_service_account_request_headers


class DeepmapClient:
    __default_project_id = 'siametrics-deepmap-dp'

    def __init__(self, key_path: Union[str, None] = None, project_id: Union[str, None] = None):
        self.__key_path = key_path or default_key_path
        self.project_id = project_id or DeepmapClient.__default_project_id

        if not os.path.exists(self.__key_path):
            self.__key_path = None

        self.__g_cred = None
        if self.__key_path:
            self.__g_cred = Credentials.from_service_account_file(self.__key_path)

        self.__discovery = DatasetDiscoveryService(self, self.project_id)

    def get_dataset(self, name: str):
        return self.__discovery.get_dataset(name)

    def list_datasets(self):
        return self.__discovery.list_datasets()

    def make_request(self, url, data=None, method='post'):
        data = json.dumps(data or {})

        headers = get_service_account_request_headers(self.__g_cred, url) if self.__g_cred else None

        if method == 'post':
            resp = requests.post(url, headers=headers, json=data)
        else:
            raise NotImplementedError(f'method {method} is not implemented.')

        resp.raise_for_status()

        return resp

    def query(self, query):
        cred = self.__g_cred and self.__g_cred.with_scopes(['https://www.googleapis.com/auth/bigquery'])
        df = pd.read_gbq(query, project_id=self.project_id, credentials=cred)
        return df

    def get_credentials(self, scopes):
        cred = self.__g_cred and self.__g_cred.with_scopes(scopes)
        return cred
