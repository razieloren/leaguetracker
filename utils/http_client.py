import requests

class HttpClient:
    _UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

    def __init__(self, request_timeout_sec=10):
        self._request_timeout_sec = request_timeout_sec
    
    def _request(self, name: str, url: str, *args, **kwargs) -> requests.Response:
        func = getattr(requests, name)
        headers = {
            'User-Agent': self._UA,
        }
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        resp = func(url, *args, **kwargs, timeout=self._request_timeout_sec)
        resp.raise_for_status()
        return resp
    
    def get(self, url: str, *args, **kwargs) -> requests.Response:
        return self._request('get', url, *args, **kwargs)
    
    def post(self, url: str, *args, **kwargs) -> requests.Response:
        return self._request('post', url, *args, **kwargs)
