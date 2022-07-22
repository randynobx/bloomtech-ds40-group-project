"""Tests for loader.scraper_browse_id"""

from requests import Response
from loaders import scraper_browse_id

def test_fetch_browse_page():
    test_id = 1
    test_res = scraper_browse_id.fetch_browse_page(test_id)
    assert isinstance(test_res, Response), 'Did not return a Response object'


def test_fetch_browse_page_2():
    test_id = 1283
    test_res = scraper_browse_id.fetch_browse_page(test_id)
    assert isinstance(test_res, Response), 'Did not return a Response object'


def test_extract_ids():
    test_id = 1
    test_res = scraper_browse_id.fetch_browse_page(test_id)
    id_list = scraper_browse_id.extract_ids(test_res)
    assert isinstance(id_list, list), 'Did not return a list'
    for i in id_list:
        assert i.isdigit(), f'Invalid ID {i} returned in list'
