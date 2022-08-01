'''Helper fucntions for database'''

from requests import Session
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker

def get_engine(url: str) -> engine.Engine:
    '''Generate a SQL Alchemy engine

    Args:
        url (str): database connection string

    Returns:
        SQL Alchemy engine
    '''
    return create_engine(url)

def connect_to_db(url: str) -> Session:
    '''Generate a SQL Alchemy session

    Args:
        url (str): database connection string

    Returns:
        SQL Alchemy session
    '''
    engine = get_engine(url)
    Session = sessionmaker(bind=engine)
    return Session()
