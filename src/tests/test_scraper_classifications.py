'''Tests for loader.scraper_classifications'''

import requests
from pandas import DataFrame
from loaders import scraper_classifications

classifications = {
    'category': 'https://boardgamegeek.com/browse/boardgamecategory',
    'mechanic': 'https://boardgamegeek.com/browse/boardgamemechanic'
}


def test_extract_data_category():
    res = requests.get(classifications['category'])
    df = scraper_classifications.extract_data(res, 'category')
    assert isinstance(df, DataFrame), 'Did not return DataFrame'
    assert df['ID'].str.isdigit().sum() == len(df), 'Invalid ID found'
    assert df['Name'].isnull().sum() == 0, 'Empty Name found'

def test_extract_data_mechanics():
    res = requests.get(classifications['mechanic'])
    df = scraper_classifications.extract_data(res, 'mechanic')
    assert isinstance(df, DataFrame), 'Did not return DataFrame'
    assert df['ID'].str.isdigit().sum() == len(df), 'Invalid ID found'
    assert df['Name'].isnull().sum() == 0, 'Empty Name found'
