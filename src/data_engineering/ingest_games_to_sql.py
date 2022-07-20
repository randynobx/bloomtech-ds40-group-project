'''ETL Pipeline for XML -> Database'''

from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Session
from sqlalchemy.orm import Session
from data_engineering.db_classes import Game, GameCategory, GameMechanic

'''
RAW FORMAT: XML
DATABASE: postgresql??

# Process
for item in file.items
    extract data
    transform data
    load to db
'''

DATA_DIR = 'data'
DB_URL = "sqlite+pysqlite:///:memory:"

def connect_db():
    return create_engine(DB_URL, echo=True)

def query_db(engine, query: str, commit: bool):
    with Session(engine) as session:
        result = session.execute(query)
        if commit:
            session.commit()
    return result


def ingest_game(game: BeautifulSoup) -> Game:
    '''Ingest individual game data

    Args:
        game (BeautifulSoup): <item> node from xml file
    '''
    game_id = game.attrs['id']
    title = game.find('name').attrs['value']
    release_year = game.yearpublished.attrs['value']
    avg_rating = game.find('average').attrs['value']
    bayes_rating = game.find('bayesaverage').attrs['value']
    num_of_ratings = game.find('usersrated').attrs['value']
    std_rating = game.find('sttdev').attrs['value']
    min_players = game.minplayers.attrs['value']
    max_players = game.maxplayers.attrs['value']
    min_playtime = game.minplaytime.attrs['value']
    max_playtime = game.maxplaytime.attrs['value']
    weight = game.find('averageweight').attrs['value']
    owned_copies = game.find('owned').attrs['value']
    
    game_node = Game(game_id, title, release_year, avg_rating, bayes_rating,
                     num_of_ratings, std_rating, min_players, max_players,
                     min_playtime, max_playtime, weight, owned_copies)


def ingest_game_mech_mapping(game: BeautifulSoup):
    '''Ingest mechanic mappings for individual game

    Args:
        game (BeautifulSoup): <item> node from xml file
    '''
    game_id = game.attrs['id']
    mechanics_ids = [line.attrs['id'] for line
                        in game.find_all('link', type='boardgamemechanic')]

    mechanics = []
    for mech_id in mechanics_ids:
        mechanics.append(GameMechanic(game_id=game_id, category_id=mech_id))


def ingest_game_cat_mapping(game: BeautifulSoup):
    '''Ingest category mappings for individual game

    Args:
        game (BeautifulSoup): <item> node from xml file
    '''
    game_id = game.attrs['id']
    category_ids = [line.attrs['id'] for line
                        in game.find_all('link', type='boardgamecategory')]

    categories = []
    for cat_id in category_ids:
        categories.append(GameCategory(game_id=game_id, category_id=cat_id))


if __name__ == '__main__':
    filepath = f'{DATA_DIR}/raw/bgg_game_pages/bgg_games_batch_0.xml'
    
    # Open batch file
    with open(filepath, 'rb') as file:
        batch = BeautifulSoup(file, features='xml')

    # Create list of individual game items
    batch_list = [item for item in batch.items.children if item != '\n']

    for game in batch_list:
        ingest_game(game)
        ingest_game_mech_mapping(game)
        ingest_game_cat_mapping(game)
