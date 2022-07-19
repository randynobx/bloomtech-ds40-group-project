'''Tests for BoardGameGeek XMLAPI2 helper functions'''

from bs4 import BeautifulSoup
from ..src import bggxmlapi2 as api


def test_build_query():
    qtype = 'thing'
    test_params = {
        'id': 224517,
        'stats': 1,
        'type': 'boardgames'
    }
    exp_url = 'https://boardgamegeek.com/xmlapi2/thing?id=224517&stats=1&type=boardgames'
    test_query_url = api.build_query(qtype, test_params)
    assert isinstance(test_query_url, str), 'Did not return a string'
    assert test_query_url == exp_url


def test_fetch_game():
    test_id = 224517
    title = 'Brass: Birmingham'
    test_soup = api.fetch_game(test_id)
    assert isinstance(test_soup, BeautifulSoup)
    assert test_soup.find('name', attrs={'type':'primary'})['value'] == title


def test_fetch_search_results():
    test_results = api.fetch_search_results('Brass')
    assert isinstance(test_results, BeautifulSoup), 'Did not return a\
         BeautifulSoup object'
    


def test_extract_ids_from_list():
    list_soup = api.fetch_hotness()
    test_list = api.extract_ids_from_list(list_soup)
    assert isinstance(test_list, list), 'Not a list?!!'
    for entry in test_list:
        assert isinstance(entry, str), 'Returned a non-str in list'
        assert entry.isDigit(), 'Returned a non-number str in list'
