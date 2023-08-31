from .consts import Queue, Product
from .module import Module, create_response

class League(Module):
    @property
    def product(self) -> Product:
        return Product.LeagueOfLegends

    @property
    def name(self) -> str:
        return 'league'

    @property
    def version(self) -> str:
        return '4'
    
    def _get_league(self, name: str, queue: Queue):
        return create_response(name, self._api.get(
            self.get_path(
            f'{name}/by-queue/{queue.value}')).json())        
    
    def get_challenger_league(self, queue: Queue):
        return self._get_league('challengerleagues', queue)
    
    def get_grand_master_league(self, queue: Queue):
        return self._get_league('grandmasterleagues', queue)
    
    def get_master_league(self, queue: Queue):
        return self._get_league('masterleagues', queue)