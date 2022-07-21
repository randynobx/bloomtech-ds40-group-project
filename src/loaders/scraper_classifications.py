'''Classifications Scraper for BGG

Pulls classification index pages from BGG website and saves raw and processed copies
'''

import re
import requests
from pandas import DataFrame
from . import config

classifications = {
    'category': 'https://boardgamegeek.com/browse/boardgamecategory',
    'mechanic': 'https://boardgamegeek.com/browse/boardgamemechanic'
}


def extract_data(res: str, label: str) -> DataFrame:
    '''Extract data from html

    Args:
        res (str): contents of html file to parse
        label (str): what to label data ['category', 'mechanics']
    
    Returns:
        DataFrame
    '''
    
    search_pattern = r'/boardgame{label}/(\d+)/([a-zA-Z-]+)'.format(label=label)
    return DataFrame(re.findall(search_pattern, str(res.content)),
              columns=['ID', 'Name'])

def run():
    '''Run scraper'''
    for label, url in classifications.items():
        # Fetch page
        page = requests.get(url)
        
        # Save raw data as html
        raw_file = f'{config.DATA_PATH}/raw/bgg_{label}.html'
        print(f'Saving {raw_file}...', end='')
        try:
            with open(raw_file, 'xb') as file:
                file.write(page.content)
        except FileExistsError:
            with open(raw_file, 'wb') as file:
                file.write(page.content)    
        print('Done')

        # Extract and Transform data
        print(f'Extracting {label}...', end='')
        extracted_data = extract_data(page, label)
        print('Done')
        
        # Save to csv
        proc_file = f'{config.DATA_PATH}/processed/bgg_{label}.csv'
        print(f'Saving {proc_file}...', end='')
        extracted_data.to_csv(proc_file, index=False)
        print('Done')
        
        print(f'{label} classifications successfully extracted and saved to {proc_file}')
