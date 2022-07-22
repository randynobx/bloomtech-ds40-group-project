'''Classes for board game database'''

from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Game(Base):
    '''Game class'''
    __tablename__ = "game"

    id = Column('ID', Integer, primary_key=True)
    title = Column('Title', String(30), nullable=False)
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
    mechanisms = relationship('GameMechanicMap')
    categories = relationship('GameCategoryMap')


class Mechanic(Base):
    '''Types of mechanics'''
    __tablename__ = 'mechanic'

    id = Column('ID', Integer, primary_key=True, nullable=False)
    name = Column('Name', String, unique=True, nullable=False)


class Category(Base):
    '''Types of categories'''
    __tablename__ = 'category'

    id = Column('ID', Integer, primary_key=True, nullable=False)
    name = Column('Name', String, unique=True, nullable=False)


class GameMechanicMap(Base):
    '''Game mechanics mappings'''
    __tablename__ = 'game_mechanic_map'

    id = Column('MapID', Integer, primary_key=True)
    game_id = Column('GameID', ForeignKey('game.ID'), nullable=False)
    mechanic_id = Column('MechanicID', ForeignKey('mechanic.ID'),
                         nullable=False)


class GameCategoryMap(Base):
    '''Game category mappings'''
    __tablename__ = 'game_category_map'

    id = Column('MapID', Integer, primary_key=True)
    game_id = Column('GameID', ForeignKey('game.ID'), nullable=False)
    category_id = Column('CategoryID', ForeignKey('category.ID'),
                         nullable=False)
