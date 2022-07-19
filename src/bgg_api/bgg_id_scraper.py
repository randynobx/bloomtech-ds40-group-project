'''Scrape Top N games from BGG'''

import re
import requests
from bs4 import BeautifulSoup

# Path to data directory
DATA_PATH = 'data'

def save_browse_page(content: str, page: int) -> None:
    '''Save browse page to file

    Args:
        content (str): html of page to save
        page (int): page number to identify file with
    '''
    filename = f'{DATA_PATH}/raw/bgg_browse_pages/bgg_browse_page_{str(page)}.html'
    with open(filename, 'xb') as file:
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

if __name__ == '__main__':
    NUM_OF_PAGES = 10
    id_list = []
    print(f'Fetching first {NUM_OF_PAGES} pages ({NUM_OF_PAGES * 100} total games)')
    # Fetch, save, and extract each page
    for pagenum in range(1, NUM_OF_PAGES + 1):
        print(pagenum, end=' ')
        page = fetch_browse_page(pagenum)
        save_browse_page(page.content, pagenum)
        id_list.extend(extract_ids(page))
    
    # Save ids to file
    filepath = f'{DATA_PATH}/processed/Top_{NUM_OF_PAGES * 100}_game_ids.txt'
    with open(filepath, 'x') as file:
        for id in id_list:
            file.write(f'{str(id)}\n')
    print(f'Game IDs successfully extracted. Saved to {filepath[3:]}')
