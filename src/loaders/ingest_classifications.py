'''ETL Pipeline for Classification CSVs -> Database'''

import pandas as pd
from yaml import safe_load
from .database_helpers import get_engine
from . import config

def run():
    '''Run ingestion script'''
    # Create database session
    engine = get_engine()

    # Load mechanics
    print('Loading mechanics into database...', end='')
    mechanic_path = f'{config.DATA_PATH}/processed/bgg_mechanic.csv'
    mechanic_df = pd.read_csv(mechanic_path)
    mechanic_df.to_sql('mechanic', engine, if_exists='replace', index=None)
    print('Done')

    # Load categories
    print('Loading categories into database...', end='')
    category_path = f'{config.DATA_PATH}/processed/bgg_category.csv'
    category_df = pd.read_csv(category_path)
    category_df.to_sql('category', engine, if_exists='replace', index=None)
    print('Done')

