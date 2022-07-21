'''Scrape game information from BGG

Takes bgg game ids and generates batched xml files
'''

from math import ceil
from . import bggxmlapi2 as api
from . import config

def save_game_batch(content: str, id: int) -> None:
    '''Save game page to file

    Args:
        content (str): html of page to save
        id (int): id to identify file with
    '''
    filename = f'{config.DATA_PATH}/raw/bgg_games_batch_{str(id)}.xml'
    try:
        with open(filename, 'xb') as file:
            file.write(content)
    except FileExistsError:
        with open(filename, 'wb') as file:
            file.write(content)

def scrape_game_pages(game_ids_list: list, batch_size: int) -> None:
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
        batch_res = api.fetch_game(id_batch)
        save_game_batch(batch_res.content, batch_num)

def run():
    '''Run scraper'''
    game_ids_file = f'{config.DATA_PATH}/processed/game_ids.csv'
    
    print(f'Using ids from {game_ids_file}\nBatch size: {config.BATCH_SIZE}')
    
    # Load game ids
    print(f'Loading game ids from {game_ids_file}...', end='')
    with open(game_ids_file, 'r') as file:
        game_ids_list = file.read().split('\n')
    print('Done')
    
    print('Fetching game data...', end='')
    scrape_game_pages(game_ids_list, config.BATCH_SIZE)
    print('Done')
