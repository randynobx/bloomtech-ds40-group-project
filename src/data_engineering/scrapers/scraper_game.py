'''Scrape game information from BGG

Takes bgg game ids and generates batched xml files
'''

from math import ceil
import bggxmlapi2 as api

# Path to data directory
DATA_PATH = 'data'

def save_game_batch(content: str, id: int) -> None:
    '''Save game page to file

    Args:
        content (str): html of page to save
        id (int): id to identify file with
    '''
    filename = f'{DATA_PATH}/raw/bgg_game_pages/bgg_games_batch_{str(id)}.xml'
    with open(filename, 'x') as file:
        file.write(content)

def scrape_game_pages(game_ids_list: list, batch_size: int) -> None:
    '''Fetch, save, and extract data from game pages

    Args:
        game_ids_list (list): list of game ids to scrape
        batch_size (int): number of ids to bundle into each request
    '''
    total_batches = ceil(len(game_ids_list) // batch_size)
    for batch_num in range(total_batches):
        begin = batch_num * batch_size
        end = min(begin + batch_size, len(game_ids_list))
        id_batch = ','.join(game_ids_list[begin:end])
        games_soup = api.fetch_game(id_batch)
        save_game_batch(games_soup.prettify(), batch_num)

if __name__ == '__main__':
    GAME_IDS_FILE = f'{DATA_PATH}/processed/Top_1000_game_ids.csv'
    '''Recommended max batch size is 1200
    See: https://boardgamegeek.com/thread/2388502/updated-api-rate-limit-recommendation
    '''
    BATCH_SIZE = 1000
    
    print(f'Using ids from {GAME_IDS_FILE}\nBatch size: {BATCH_SIZE}')
    
    # Load game ids
    with open(GAME_IDS_FILE, 'r') as file:
        game_ids_list = file.read().split(',')
    
    print('Fetching data...')
    scrape_game_pages(game_ids_list, BATCH_SIZE)
    print('Fetch complete.')
