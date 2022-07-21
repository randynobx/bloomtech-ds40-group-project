'''Helper fucntions for database'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import config

def get_engine():
    '''Generate a SQL Alchemy engine

    Returns:
        SQL Alchemy engine
    '''
    return create_engine(config.DB_URL)

def connect_to_db():
    '''Generate a SQL Alchemy session

    Returns:
        SQL Alchemy session
    '''
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()