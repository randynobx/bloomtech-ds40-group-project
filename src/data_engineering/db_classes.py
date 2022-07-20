'''Classes for database loading'''


class Game:
    '''Game class'''
    def __init__(self, game_id: int, title: str, release_year: int,
                 avg_rating: float, bayes_rating: float, num_of_ratings: int,
                 std_rating: float, min_players: int, max_players: int,
                 min_playtime: int, max_playtime: int, weight: float,
                 owned_copies: int):
        self.id = game_id
        self.title = title
        self.release_year = release_year
        self.avg_rating = avg_rating
        self.bayes_rating = bayes_rating
        self.num_of_ratings = num_of_ratings
        self.std_rating = std_rating
        self.min_players = min_players
        self.max_players = max_players
        self.min_playtime = min_playtime
        self.max_playtime = max_playtime
        self.weight = weight
        self.owned_copies = owned_copies



class Mechanism:
    '''Types of mechanisms'''
    def __init__(self, mech_id: int, name: str, description: str):
        self.mech_id = mech_id
        self.name = name


class Category:
    '''Types of categories'''
    def __init__(self, cat_id: int, name: str, description: str):
        self.cat_id = cat_id
        self.name = name


class GameMechanic:
    '''Game mechanism mappings'''
    def __init__(self, game_id: int, mech_id: int):
        self.game_id = game_id
        self.mech_id = mech_id


class GameCategory:
    '''Game category mappings'''
    def __init__(self, game_id: int, category_id: int):
        self.game_id = game_id
        self.category_id = category_id
