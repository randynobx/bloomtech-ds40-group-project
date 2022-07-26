'''Scrape top N games from BGG

N = config.NUM_OF_PAGES * 100
'''
import sys
import re
from requests import Response
from .scraper_helpers import save_file, fetch_page

def extract_ids(res: Response) -> list:
    '''Extract game id's from browse page

    Args:
        res (requests): requests object to extract game ids from

    Returns:
        list of game id's
    '''
    search_pattern = r'/boardgame/(\d+)/'
    # Change to set to remove duplicates
    return list(set(re.findall(search_pattern, str(res.content))))

def run(config):
    '''Run scraper'''
    print(f'Fetching first {config.NUM_OF_PAGES} pages ({config.NUM_OF_PAGES * 100} total games)')

    # Fetch, save, and extract each page
    id_list = [] # Running list
    for pagenum in range(config.NUM_OF_PAGES):
        print(pagenum, end=' ')
        sys.stdout.flush() # Print updates in real time

        # Set page variables
        filename = f'{config.BROWSE_FILENAME}_{str(pagenum)}.html'
        page_url = f'https://boardgamegeek.com/browse/boardgame/page/{str(pagenum + 1)}'

        # Scrape page
        page = fetch_page(page_url)
        if page.status_code != 200:
            break
        save_file(config.RAW_PATH, filename, page.content)
        id_list.extend(extract_ids(page))
    print('Done')

    # Save ids to csv file
    contents = '\n'.join(list(set(id_list)))
    csv_filename = f'{config.GAME_IDS_FILENAME}.csv'
    print(f'Saving game ids to {config.PROC_PATH}/{csv_filename}...', end='')
    save_file(config.PROC_PATH, csv_filename, contents.encode())
    print('Done')
