'''ETL Pipeline for game batch XML -> Database'''

from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
from .database_helpers import connect_to_db
from .boardgame_db_classes import Game, GameCategoryMap, GameMechanicMap


def ingest_game(game: BeautifulSoup) -> Game:
    '''Ingest individual game data

    Args:
        game (BeautifulSoup): <item> node from xml file

    Returns:
        Game object
    '''
    return Game(
        id = int(game.attrs['id']),
        title = game.find('name').attrs['value'],
        release_year = int(game.yearpublished.attrs['value']),
        avg_rating = float(game.find('average').attrs['value']),
        bayes_rating = float(game.find('bayesaverage').attrs['value']),
        total_ratings = int(game.find('usersrated').attrs['value']),
        std_rating = float(game.find('stddev').attrs['value']),
        min_players = int(game.minplayers.attrs['value']),
        max_players = int(game.maxplayers.attrs['value']),
        min_playtime = int(game.minplaytime.attrs['value']),
        max_playtime = int(game.maxplaytime.attrs['value']),
        weight = float(game.find('averageweight').attrs['value']),
        owned_copies = int(game.find('owned').attrs['value'])
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


def upsert_game(session: Session, game: Game):
    '''Insert or update Game object to database'''
     # Check if game exists, insert on absense
    existing = session.query(Game).filter_by(id=game.id).scalar()
    if not existing:
        session.add(game)
    elif existing.id == game.id:
        pass # <IMPLEMENT UPDATE>


def insert_mech_map(session: Session, mech_map: GameMechanicMap):
    '''Insert GameMechanicMap to database if not already existing'''
    mech_map_exists = session.query(GameMechanicMap)\
        .filter_by(game_id=mech_map.game_id,
                    mechanic_id=mech_map.mechanic_id)
    if not mech_map_exists.first():
        session.add(mech_map)

def insert_cat_map(session: Session, cat_map: GameCategoryMap):
    '''Insert GameCategoryMap to database if not already existing'''
    cat_map_exists = session.query(GameCategoryMap)\
                        .filter_by(game_id=cat_map.game_id,
                                   category_id=cat_map.category_id)
    if not cat_map_exists.first():
        session.add(cat_map)

def run(config):
    '''Run ingestion script'''
    with connect_to_db(config.DB_URL) as session:
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
                # Game data
                upsert_game(session, ingest_game(game))
                # GameMechanicMaps
                mech_maps = ingest_game_mech_mapping(game)
                for mech_map in mech_maps:
                    insert_mech_map(session, mech_map)
                # GameCategoryMaps
                cat_maps = ingest_game_cat_mapping(game)
                for cat_map in cat_maps:
                    insert_cat_map(session, cat_map)
                session.commit()
            print('Done')    
