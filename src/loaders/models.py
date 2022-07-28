"""SQLAlchemy Models for Database"""

import os
from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey, Unicode
from sqlalchemy.orm import declarative_base, relationship
from .database_helpers import get_engine

Base = declarative_base()

# Association tables for classifications
game_mechanic = Table('game_mechanic', Base.metadata,
                        Column('GameID', ForeignKey('game.ID'),
                                primary_key=True),
                        Column('MechanicID', ForeignKey('mechanic.ID'),
                                primary_key=True)
)

game_category = Table('game_category', Base.metadata,
                        Column('GameID', ForeignKey('game.ID'),
                                primary_key=True),
                        Column('CategoryID', ForeignKey('category.ID'),
                                primary_key=True)
)


class GameMechanic(Base):
    '''Game Mechanics'''
    __table__ = game_mechanic

class GameCategory(Base):
    '''Game Categories'''
    __table__ = game_category


class Game(Base):
    '''Game class'''
    __tablename__ = "game"

    id = Column('ID', Integer, primary_key=True)
    title = Column('Title', Unicode(30), nullable=False)
    release_year = Column('ReleaseYear', Integer, nullable=False)
    avg_rating = Column('AvgRating', Float)
    bayes_rating = Column('BayesRating', Float)
    total_ratings = Column('TotalRatings', Integer)
    std_rating = Column('StdRatings', Float)
    min_players = Column('MinPlayers', Integer)
    max_players = Column('MaxPlayers', Integer)
    min_playtime = Column('MinPlaytime', Integer)
    max_playtime = Column('MaxPlaytime', Integer)
    weight = Column('Weight', Float)
    owned_copies = Column('OwnedCopies', Integer)
    mechanics = relationship('Mechanic',
                                secondary=game_mechanic,
                                backref='games')
    categories = relationship('Category',
                                secondary=game_category,
                                backref='games')


    def __repr__(self) -> str:
        return f'<ID: {self.id}, Title: {self.title}>'


class Mechanic(Base):
    '''Types of mechanics'''
    __tablename__ = 'mechanic'

    id = Column('ID', Integer, primary_key=True, nullable=False)
    name = Column('Name', String, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'<ID: {self.id}, Name: {self.name}>'


class Category(Base):
    '''Types of categories'''
    __tablename__ = 'category'

    id = Column('ID', Integer, primary_key=True, nullable=False)
    name = Column('Name', String, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'<ID: {self.id}, Name: {self.name}>'


def init(config) -> None:
    '''Create database tables

    Args:
        base (Base): declarative_base()
        config (Config): config object
    '''
    print('Initializing database...', end='')
    # Ensure config.DB_PATH exists if using SQLite3
    if 'sqlite' in config.DB_URL and not os.path.exists(config.DB_PATH):
        os.mkdir(config.DB_PATH)

    engine = get_engine(config.DB_URL)
    
    Base.metadata.create_all(engine)
        
    print('Done')


# Dictionary of classification types and their models
# (<Name>, <Name in Game class>, <Class name>)
CLASS_LIST = [
    ('mechanic', 'mechanics', Mechanic),
    ('category', 'categories', Category)
]
