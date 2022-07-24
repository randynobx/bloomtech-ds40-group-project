'''Create board games database'''

import os
from sqlalchemy import MetaData, Table, Column, Integer, Float, String, ForeignKey
from .database_helpers import get_engine

def run(config):
    '''Create database tables'''
    # Ensure /data/final/ directory exists
    if 'sqlite' in config.DB_URL and not os.path.exists('data/final'):
        os.mkdir('data/final')

    engine = get_engine(config.DB_URL)
    meta = MetaData()

    game = Table('game', meta,
                Column('ID', Integer, primary_key=True),
                Column('Title', String(30)),
                Column('ReleaseYear', Integer),
                Column('AvgRating', Float),
                Column('BayesRating', Float),
                Column('TotalRatings', Integer),
                Column('StdRatings', Float),
                Column('MinPlayers', Integer),
                Column('MaxPlayers', Integer),
                Column('MinPlaytime', Integer),
                Column('MaxPlaytime', Integer),
                Column('Weight', Float),
                Column('OwnedCopies', Integer),
    )


    mechanic = Table('mechanic', meta,
                    Column('ID', Integer, primary_key=True),
                    Column('Name', String, unique=True)
    )


    category = Table('category', meta,
                    Column('ID', Integer, primary_key=True),
                    Column('Name', String, unique=True)
    )


    game_mechanic_map = Table('game_mechanic_map', meta,
                            Column('MapID', Integer, primary_key=True),
                            Column('GameID', ForeignKey('game.ID')),
                            Column('MechanicID', ForeignKey('mechanic.ID'))
    )

    game_category_map = Table('game_category_map', meta,
                            Column('MapID', Integer, primary_key=True),
                            Column('GameID', ForeignKey('game.ID')),
                            Column('CategoryID', ForeignKey('category.ID'))
    )

    meta.create_all(engine)
