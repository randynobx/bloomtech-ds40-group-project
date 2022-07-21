'''ETL Pipeline for game batch XML -> Database'''

from bs4 import BeautifulSoup
from sqlalchemy import MetaData
from .database_helpers import connect_to_db
from .boardgame_db_classes import Game, GameCategoryMap, GameMechanicMap
from . import config


def ingest_game(game: BeautifulSoup) -> Game:
    '''Ingest individual game data

    Args:
        game (BeautifulSoup): <item> node from xml file

    Returns:
        Game object
    '''
    return Game(
        id = game.attrs['id'],
        title = game.find('name').attrs['value'],
        release_year = game.yearpublished.attrs['value'],
        avg_rating = game.find('average').attrs['value'],
        bayes_rating = game.find('bayesaverage').attrs['value'],
        total_ratings = game.find('usersrated').attrs['value'],
        std_rating = game.find('stddev').attrs['value'],
        min_players = game.minplayers.attrs['value'],
        max_players = game.maxplayers.attrs['value'],
        min_playtime = game.minplaytime.attrs['value'],
        max_playtime = game.maxplaytime.attrs['value'],
        weight = game.find('averageweight').attrs['value'],
        owned_copies = game.find('owned').attrs['value']
    )


def ingest_game_mech_mapping(game: BeautifulSoup) -> list:
    '''Ingest mechanic mappings for individual game

    Args:
        game (BeautifulSoup): <item> node from xml file

    Returns:
        List of GameMechanismMap objects
    '''
    game_id = game.attrs['id']
    mechanics_ids = [line.attrs['id'] for line
                        in game.find_all('link', type='boardgamemechanic')]

    return [GameMechanicMap(game_id=game_id, mechanic_id=mech_id)
            for mech_id in mechanics_ids]


def ingest_game_cat_mapping(game: BeautifulSoup) -> list:
    '''Ingest category mappings for individual game

    Args:
        game (BeautifulSoup): <item> node from xml file

    Returns:
        List of GameCategoryMap objects
    '''
    game_id = game.attrs['id']
    category_ids = [line.attrs['id'] for line
                        in game.find_all('link', type='boardgamecategory')]

    return [GameCategoryMap(game_id=game_id, category_id=cat_id)
                  for cat_id in category_ids]


def run():
    '''Run ingestion script'''
    with connect_to_db() as session:
        # Run process for each batch
        total_batches = int(config.NUM_OF_PAGES * 100 / config.BATCH_SIZE)
        for batch_num in range(total_batches):
            print(f'Loading batch {batch_num}...', end='')
            filepath = f'{config.DATA_PATH}/raw/bgg_games_batch_{batch_num}.xml'
            
            # Open batch file
            with open(filepath, 'rb') as file:
                batch = BeautifulSoup(file, features='xml')

            # Create list of individual game items
            batch_list = [item for item in batch.items.children if item != '\n']

            # Iterate through games to extract data and add to database
            for game in batch_list:
                # Extract and transform data
                session.add(ingest_game(game))
                session.add_all(ingest_game_mech_mapping(game))
                session.add_all(ingest_game_cat_mapping(game))
                session.commit()
            print('Done')    
