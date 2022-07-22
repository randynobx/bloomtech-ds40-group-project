'''Tests for BoardGameGeek XMLAPI2 helper functions'''

import re
from requests import Response
from loaders import bggxmlapi2 as api


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


def test_build_query_batch():
    qtype = 'thing'
    test_params = {
        'id': '224517,160010,150',
        'stats': 1,
        'type': 'boardgames'
    }
    exp_url = 'https://boardgamegeek.com/xmlapi2/thing?id=224517,160010,150&stats=1&type=boardgames'
    test_query_url = api.build_query(qtype, test_params)
    assert isinstance(test_query_url, str), 'Did not return a string'
    assert test_query_url == exp_url
    

def test_fetch_game():
    test_id = 224517
    test_res = api.fetch_game(test_id)
    assert isinstance(test_res, Response), 'Did not return a Response object'
    ans_item = r'<item type="boardgame" id="224517">'
    pattern = re.compile(ans_item)
    test_item = re.search(pattern, str(test_res.content))[0]
    assert test_item == ans_item, f'Wrong item returned. Received {test_item}'


def test_fetch_game_batch():
    test_id = '224517,160010,150'
    test_res = api.fetch_game(test_id)
    assert isinstance(test_res, Response), 'Did not return a Response object'
    pattern =  re.compile(r'<item type="boardgame" id="\d+">')
    items_search = re.findall(pattern, str(test_res.content))
    assert len(items_search) == 3
    

def test_fetch_search_results():
    test_results = api.fetch_search_results('Brass')
    assert isinstance(test_results, Response), 'Did not return a Response object'
