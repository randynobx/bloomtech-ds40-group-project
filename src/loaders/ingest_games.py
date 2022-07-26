'''ETL Pipeline for game batch XML -> Database'''

from sqlalchemy import update
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
from .database_helpers import connect_to_db
from .models import Game, Category, Mechanic


def ingest_game(session: Session, game_soup: BeautifulSoup) -> Game:
    '''Ingest and upsert individual game data

    Args:
        session (Session)
        game (BeautifulSoup): <item> node from xml file

    Returns:
        Game object
    '''
    game = {
        'id': int(game_soup.attrs['id']),
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
        'mechanics': ingest_game_mechanics(session, game_soup),
        'categories': ingest_game_categories(session, game_soup)
    }
    
    existing = session.get(Game, game['id'])
    if not existing:
        # Add new game
        session.add(Game(**game))
    elif existing.id == game['id']:
        # Check for updates to existing game
        updates, existing_dict = {}, vars(existing)
        for key, value in game.items():
            if isinstance(value, list):
                # Check classifications
                if key == 'mechanics':
                    existing.mechanics = value
                elif key == 'categories':
                    existing.categories = value
            elif value != existing_dict[key]:
                # Check game object
                updates[key] = value
        if updates:
            # Update existing game
            stmt = update(Game).where(Game.id == game['id'])\
                .values(**updates)\
                .execution_options(synchronize_session="fetch")
            session.execute(stmt)



def ingest_game_mechanics(session: Session, game: BeautifulSoup) -> list:
    '''Ingest mechanic mappings for individual game

    Args:
        session (Session)
        game (BeautifulSoup): <item> node from xml file

    Returns:
        List of mechanic ids
    '''
    mechanics = []
    for line in game.find_all('link', type='boardgamemechanic'):
        mechanics.append(session.get(Mechanic, line.attrs['id']))
    return mechanics


def ingest_game_categories(session: Session, game: BeautifulSoup) -> list:
    '''Ingest category mappings for individual game

    Args:
        session (Session)
        game (BeautifulSoup): <item> node from xml file

    Returns:
        List of category ids
    '''
    categories = []
    for line in game.find_all('link', type='boardgamecategory'):
        categories.append(session.get(Category, line.attrs['id']))
    return categories


def run(config):
    '''Run ingestion script

    Args:
        config (Config): initialized loaders.config.Config object
    '''
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
                # Insert/Update data to database
                ingest_game(session, game)
                session.commit()
            print('Done')    
