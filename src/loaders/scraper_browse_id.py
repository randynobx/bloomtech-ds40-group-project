'''Scrape top N games from BGG

N = config.NUM_OF_PAGES * 100
'''

import re
import requests
from . import config

def save_browse_page(content: str, page: int) -> None:
    '''Save browse page to file

    Args:
        content (str): html of page to save
        page (int): page number to identify file with
    '''
    filename = f'{config.DATA_PATH}/raw/bgg_browse_page_{str(page)}.html'
    try:
        with open(filename, 'xb') as file:
            file.write(content)
    except FileExistsError:
        with open(filename, 'wb') as file:
            file.write(content)

def fetch_browse_page(page: int) -> requests:
    '''Fetch specified Browse page

    Args:
        page (int): Page number to grab from BGG

    Returns:
        (requests)'''
    url = f'https://boardgamegeek.com/browse/boardgame/page/{str(page)}'
    return requests.get(url)

def extract_ids(res: requests) -> list:
    '''Extract game id's from browse page

    Args:
        res (requests): requests object to extract game ids from

    Returns:
        list of game id's
    '''
    search_pattern = r'/boardgame/(\d+)/'
    # Change to set to remove duplicates
    return list(set(re.findall(search_pattern, str(res.content))))

def run():
    '''Run scraper'''
    id_list = []
    print(f'Fetching first {config.NUM_OF_PAGES} pages ({config.NUM_OF_PAGES * 100} total games)')
    # Fetch, save, and extract each page
    for pagenum in range(config.NUM_OF_PAGES):
        print(pagenum, end=' ')
        page = fetch_browse_page(pagenum)
        save_browse_page(page.content, pagenum)
        id_list.extend(extract_ids(page))
    print('Done')
    
    # Save ids to file
    filepath = f'{config.DATA_PATH}/processed/game_ids.csv'
    print(f'Saving game ids to {filepath}...', end='')
    try:
        with open(filepath, 'x') as file:
            file.write('\n'.join(list(set(id_list))))
    except FileExistsError:
        with open(filepath, 'w') as file:
            file.write('\n'.join(list(set(id_list))))
    print('Done')
