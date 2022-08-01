'''ETL Pipeline for Classification CSVs -> Database'''

from pandas import read_csv
from .database_helpers import get_engine

def run(config) -> None:
    '''Run ingestion script'''
    # Create database engine
    engine = get_engine(config.DB_URL)

    # Load each classification table (Mechanic, Category, etc...)
    for label in config.CLASSIFICATIONS:
        print(f'Loading {label} into database...', end='')
        path = f'{config.PROC_PATH}/bgg_{label}.csv'
        df = read_csv(path)
        df.to_sql(label, engine, if_exists='replace', index=None)
        print('Done')
