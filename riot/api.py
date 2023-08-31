import requests
from utils.http_client import HttpClient

from .modules.consts import Region
from .modules import create_league_module

class API(HttpClient):
    _BASE_URL = 'https://{region}.api.riotgames.com'

    def __init__(self, region: Region, api_key: str, request_timeout_sec=10):
        super().__init__(request_timeout_sec)
        self._region = region
        self._api_key = api_key
        self._request_timeout_sec = request_timeout_sec
        
        # Modules
        self.league = create_league_module(self)

    @property
    def base_url(self):
        return self._BASE_URL.format(region=str(self._region.value.endpoint))
    
    def _request(self, name: str, url: str, *args, **kwargs) -> requests.Response:
        url = f'{self.base_url}/{url}'
        print(url)
        return super()._request(name, url, *args, **kwargs, headers={
            'X-Riot-Token': self._api_key
        })
