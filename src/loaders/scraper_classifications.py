'''Classifications Scraper for BGG

Pulls classification index pages from BGG website and saves raw and processed copies
'''

import re
from pandas import DataFrame
from . import config
from .scraper_helpers import save_file, fetch_page

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
        page = fetch_page(url)
        
        # Save raw data as html
        raw_filename = f'bgg_{label}.html'
        print(f'Saving {config.RAW_PATH}/{raw_filename}...', end='')
        save_file(config.RAW_PATH, raw_filename, page.content) 
        print('Done')

        # Extract and Transform data
        print(f'Extracting {label}...', end='')
        extracted_data = extract_data(page, label)
        print('Done')
        
        # Save to csv
        proc_filename = f'{config.PROC_PATH}/bgg_{label}.csv'
        print(f'Saving {proc_filename}...', end='')
        extracted_data.to_csv(proc_filename, index=False)
        print('Done')
        
        print(f'{label} classifications successfully extracted and saved to {proc_filename}')
