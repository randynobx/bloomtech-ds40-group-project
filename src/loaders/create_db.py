'''Create board games database'''

from sqlalchemy import MetaData, create_engine, Table, Column, Integer, Float, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .database_helpers import get_engine

def run():
    '''Create database tables'''
    engine = get_engine()
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
