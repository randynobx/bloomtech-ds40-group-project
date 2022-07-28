'''ETL Pipeline for game batch XML -> Database'''

from sqlalchemy import update
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
from loaders.database_helpers import connect_to_db
from loaders.models import Game, CLASS_LIST


def transform_game_data(game_soup: BeautifulSoup) -> dict:
    '''Transform game data from XML fragment to dict

    Args:
        game_soup (BeautifulSoup): XML <item> node for game

    Returns:
        Game data in dictionary form
    '''
    return {
        'id': int(game_soup.find('item').attrs['id']),
        'title': game_soup.find('name').attrs['value'],
        'release_year': int(game_soup.yearpublished.attrs['value']),
        'avg_rating': float(game_soup.find('average').attrs['value']),
        'bayes_rating': float(game_soup.find('bayesaverage').attrs['value']),
        'total_ratings': int(game_soup.find('usersrated').attrs['value']),
        'std_rating': float(game_soup.find('stddev').attrs['value']),
        'min_players': int(game_soup.minplayers.attrs['value']),
        'max_players': int(game_soup.maxplayers.attrs['value']),
        'min_playtime': int(game_soup.minplaytime.attrs['value']),
        'max_playtime': int(game_soup.maxplaytime.attrs['value']),
        'weight': float(game_soup.find('averageweight').attrs['value']),
        'owned_copies': int(game_soup.find('owned').attrs['value']),
    }


def transform_game_class_ids(name: str, game_soup: BeautifulSoup) -> list:
    '''Transform given classification ids from game's XML fragment to list

    Args:
        name (str): Name of classification ['mechanic', 'category', ...]
        game_soup (BeautifulSoup): XML <item> node for game

    Returns:
        List of numeric ID's for given classification name
    '''
    return [int(line.attrs['id'])
            for line in game_soup.find_all('link', type=f'boardgame{name}')]


def load_game_classifications(session: Session, class_obj, id_list: list) -> list:
    '''Load given classification ids as objects from database

    Args:
        session (Session): SQL Alchemy session to use
        class_obj: The SQL Alchemy model for the wanted classification
                    ['mechanic', 'category', ...]

    Returns:
        List of (class_obj type) objects
    '''
    return [session.get(class_obj, id) for id in id_list]


def load_game(session: Session, game: dict) -> None:
    '''Load individual game data into database (INSERT/UPDATE)

    Args:
        session (Session): SQL Alchemy session to use
        game (BeautifulSoup): <item> node from xml file
    '''
    existing = session.get(Game, game['id'])
    if not existing:
        # Add new game
        session.add(Game(**game))
        session.commit()
    elif existing.id == game['id']:
        # Check for updates to existing game
        updates, existing_dict = {}, vars(existing)
        for key, value in game.items():
            if isinstance(value, list):
                # Check classifications
                if key == 'mechanic':
                    existing.mechanics = value
                elif key == 'category':
                    existing.categories = value
            elif value != existing_dict[key]:
                # Check game object
                updates[key] = value
        if updates:
            # Update existing game only if new data is present
            update_stmt = update(Game).where(Game.id == game['id'])\
                .values(**updates)\
                .execution_options(synchronize_session="fetch")
            session.execute(update_stmt)
            session.commit()
        

def process_game(session: Session, game_soup: BeautifulSoup, class_list: list) -> None:
    '''Run ETL pipeline for individual game

    Args:
        session (Session): SQL Alchemy session to use
        game_soup (BeautifulSoup): XML <item> node for game
        class_list (list): List of classifications tuples
                        ex. ('mechanic', 'mechanics', Mechanic)
    '''
    # Extract data from XML fragments
    game_dict = transform_game_data(game_soup)
    # Extract and attach game classifications as objects
    for name, group, model in class_list:
        id_list = transform_game_class_ids(name, game_soup)
        game_dict[group] = load_game_classifications(session
                                                    , model
                                                    , id_list)
    # Load data into database
    load_game(session, game_dict)


def run(config) -> None:
    '''Run ingestion script

    Args:
        config (Config): initialized loaders.config.Config object
    '''
    with connect_to_db(config.DB_URL) as session:
        # Estimate max batch count as 100*NUM_OF_PAGES/BATCH_SIZE
        total_batches = int(config.NUM_OF_PAGES * 100 / config.BATCH_SIZE)
        # Run process for each batch
        for batch_num in range(total_batches):
            filepath = f'{config.RAW_PATH}/{config.BATCH_FILENAME}_{batch_num}.xml'
            # Open batch file
            try:
                with open(filepath, 'rb') as file:
                    batch = BeautifulSoup(file, features='xml')
            except FileNotFoundError:
                break # No more xml batch files, break loop

            print(f'Loading batch {batch_num}...', end='')

            # Create a list of XML fragments for each game
            game_batch = [item for item in batch.items.children if item != '\n']

            # Iterate and process games individually
            for game_soup in game_batch:
                # Run ETL pipeline from XML nodes for each game
                process_game(session, game_soup, CLASS_LIST)
                
            print('Done')    
