from .league import League

def create_league_module(api) -> League:
    return League(api)