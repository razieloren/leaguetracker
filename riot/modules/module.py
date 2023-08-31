from collections import namedtuple

from .consts import Product
from utils.http_client import HttpClient

def create_response(name, kwargs):
    attribs = list(kwargs.keys())
    values = list(kwargs.values())
    tpl_cls = namedtuple(name, ' '.join(attribs))
    extended_values= []
    for i, val in enumerate(values):
        if isinstance(val, list):
            sub_val = []
            for e in val:
                sub_val.append(create_response(f'{name}_{attribs[i]}', e))
            extended_values.append(sub_val)
        elif isinstance(val, dict):
            extended_values.append(create_response(f'{name}_{attribs[i]}', val))
        else:
            extended_values.append(val)
    inst = tpl_cls(*extended_values)
    return inst

class Module:
    def __init__(self, api: HttpClient):
        self._api = api

    @property
    def product(self) -> Product:
        raise NotImplementedError('product')

    @property
    def name(self) -> str:
        raise NotImplementedError('name')

    @property
    def version(self) -> str:
        raise NotImplementedError('version')
    
    @property
    def endpoint(self) -> str:
        return f'{self.product.value}/{self.name}/v{self.version}'
    
    def get_path(self, path: str):
        return f'{self.endpoint}/{path}'