'''Helper functions for using the BoardGameGeek XMLAPI2'''

import requests
from bs4 import BeautifulSoup


def build_query(query_type: str, params: dict) -> str:
    '''Build XML query for board game

    Args:
        query_type (str): type of query: thing, user, search...
        params (dict): dict of params using str for both keys and values

    Returns:
        str: query url
    '''
    url = f'https://boardgamegeek.com/xmlapi2/{query_type}?'
    for key, value in params.items():
        url += f'&{key}={str(value)}'
    return url


def fetch_game(game_id: int) -> BeautifulSoup:
    '''Fetch game data from BGG

    Args:
        game_id (int): numerical id of game on BGG

    Returns:
        (BeautifulSoup)
    '''
    params = {
        'stats': '1',
        'id': game_id
    }
    request_url = build_query('thing', params)
    return BeautifulSoup(requests.get(url=request_url).content, features='xml')


def fetch_search_results(query: str) -> BeautifulSoup:
    '''Fetch board game search results for given query

    Args:
        query (str): search query

    Returns:
        (BeautifulSoup)
    '''
    query = query.replace(' ', '+')
    url = f'https://boardgamegeek.com/xmlapi2/search?query={query}&type=boardgame'
    return BeautifulSoup(requests.get(url).content, features='xml')


def extract_ids_from_list(soup: BeautifulSoup) -> list:
    '''Extract IDs from listed results

    Args:
        soup (BeautifulSoup): List to extract ids from

    Returns:
        (list): list of all ids as str
    '''
    return [line.attrs['id'] for line in soup.find_all('item')]

def fetch_hotness() -> BeautifulSoup:
    '''Fetch list of Hottest 50 Games on BGG

    Returns:
        (BeautifulSoup)
    '''
    hot_list_url = 'https://boardgamegeek.com/xmlapi2/hot?boardgames'
    return BeautifulSoup(requests.get(hot_list_url).content, features='xml')
