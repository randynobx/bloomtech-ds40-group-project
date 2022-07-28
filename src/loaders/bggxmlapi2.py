'''Helper functions for using the BoardGameGeek XMLAPI2'''

import requests


def build_query(query_type: str, params: dict) -> str:
    '''Build XML query for board game

    Args:
        query_type (str): type of query: thing, user, search...
        params (dict): dict of params using str for both keys and values

    Returns:
        Query URL for given parameters
    '''
    url = f'https://boardgamegeek.com/xmlapi2/{query_type}?'
    for key, value in params.items():
        url += f'{key}={str(value)}&'
    return url.strip('&')


def fetch_game(game_id: int) -> requests.Response:
    '''Fetch game data from BGG

    Args:
        game_id (int): numerical id of game on BGG

    Returns:
        Game data encoded with XML
    '''
    params = {
        'stats': '1',
        'id': game_id
    }
    request_url = build_query('thing', params)
    return requests.get(url=request_url)


def fetch_search_results(query: str) -> requests.Reponse:
    '''Fetch board game search results for given query

    Args:
        query (str): search query

    Returns:
        Search results encoded with XML
    '''
    query = query.replace(' ', '+')
    url = f'https://boardgamegeek.com/xmlapi2/search?query={query}&type=boardgame'
    return requests.get(url)


def fetch_hotness() -> requests.Response:
    '''Fetch list of Hottest 50 Games on BGG

    Returns:
        XML list of 'Hottest 50 Games on BGG'
    '''
    hot_list_url = 'https://boardgamegeek.com/xmlapi2/hot?boardgames'
    return requests.get(hot_list_url)
