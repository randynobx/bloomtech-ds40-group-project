'''Scrape game information from BGG

Takes bgg game ids and generates batched xml files
'''

from math import ceil
from requests import Response
from . import config
from .bggxmlapi2 import fetch_game
from .scraper_helpers import save_file

def scrape_game_pages(game_ids_list: list, batch_size: int) -> Response:
    '''Fetch, save, and extract data from game pages

    Args:
        game_ids_list (list): list of game ids to scrape
        batch_size (int): number of ids to bundle into each request
    '''
    total_batches = ceil(len(game_ids_list) // batch_size) + 1
    for batch_num in range(total_batches):
        begin = batch_num * batch_size
        end = min(begin + batch_size, len(game_ids_list))
        id_batch = ','.join(game_ids_list[begin:end])
        yield fetch_game(id_batch)

def run():
    '''Run scraper'''
    game_ids_file = f'{config.PROC_PATH}/{config.GAME_IDS_FILENAME}.csv'
    batch_filename = f'{config.BATCH_FILENAME}_{str(id)}.xml'
    
    print(f'Using ids from {game_ids_file}\nBatch size: {config.BATCH_SIZE}')
    
    # Load game ids
    print(f'Loading game ids from {game_ids_file}...', end='')
    with open(game_ids_file, 'r') as file:
        game_ids_list = file.read().split('\n')
    print('Done')
    
    # Scrape game data in batches
    print('Fetching game data...', end='')
    for page in scrape_game_pages(game_ids_list, config.BATCH_SIZE):
        batch_filename = f'bgg_games_batch_{str(id)}.xml'
        save_file(config.RAW_PATH, batch_filename, page.content)
    print('Done')
