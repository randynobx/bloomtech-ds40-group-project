'''Classifications Scraper for BGG

Pulls classification index pages from BGG website and saves raw and processed copies
'''

import re
import requests
from pandas import DataFrame

DATA_DIR = 'data'

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
              columns=[f'{label}_id', 'name'])

if __name__ == '__main__':
    for label, url in classifications.items():
        # Fetch page
        page = requests.get(url)
        
        # Save raw data as html
        filepath = f'{DATA_DIR}/raw/bgg_index_pages/bgg_{label}.html'
        with open(filepath, 'xb') as file:
            file.write(page.content)
            
        # Extract and Transform data
        extracted_data = extract_data(page, label)
        
        # Save to csv
        extracted_data.to_csv(f'{DATA_DIR}/processed/bgg_{label}.csv',
                              index=False)
