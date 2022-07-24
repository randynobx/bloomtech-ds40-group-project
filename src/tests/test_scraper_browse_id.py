"""Tests for loader.scraper_browse_id"""

from loaders import scraper_browse_id
from loaders.scraper_helpers import fetch_page

def test_extract_ids():
    test_res = fetch_page('https://boardgamegeek.com/browse/boardgame')
    id_list = scraper_browse_id.extract_ids(test_res)
    assert isinstance(id_list, list), 'Did not return a list'
    for i in id_list:
        assert i.isdigit(), f'Invalid ID {i} returned in list'
