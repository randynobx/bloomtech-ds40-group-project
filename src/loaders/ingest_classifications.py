'''ETL Pipeline for Classification CSVs -> Database'''

from pandas import read_csv
from .database_helpers import get_engine
from . import config

def run():
    '''Run ingestion script'''
    # Create database session
    engine = get_engine()

    # Load mechanics
    print('Loading mechanics into database...', end='')
    mechanic_path = f'{config.PROC_PATH}/{config.MECH_FILENAME}.csv'
    mechanic_df = read_csv(mechanic_path)
    mechanic_df.to_sql('mechanic', engine, if_exists='replace', index=None)
    print('Done')

    # Load categories
    print('Loading categories into database...', end='')
    category_path = f'{config.PROC_PATH}/{config.CAT_FILENAME}.csv'
    category_df = read_csv(category_path)
    category_df.to_sql('category', engine, if_exists='replace', index=None)
    print('Done')

