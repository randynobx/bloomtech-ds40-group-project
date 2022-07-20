/* Create boardgames database and tables */

CREATE DATABASE boardgames_db
    WITH OWNER = 'admin';

CREATE TABLE IF NOT EXISTS games (
    game_id         PRIMARY KEY,
    title           VARCHAR(20) NOT NULL,
    release_year    DATE NOT NULL,
    avg_rating      REAL NOT NULL,
    bayes_rating    REAL NOT NULL,
    num_of_ratings  INT NOT NULL,
    std_ratings     REAL NOT NULL,
    min_players     INT NOT NULL,
    max_players     INT NOT NULL,
    min_playtime    INT NOT NULL,
    max_playtime    INT NOT NULL,
    weight          REAL NOT NULL,
    owned_copies    INT NOT NULL,
);

CREATE TABLE IF NOT EXISTS mechanisms (
    mech_id     INT NOT NULL,
    name        VARCHAR(20) NOT NULL,
);

CREATE TABLE IF NOT EXISTS categories (
    cat_id      INT NOT NULL,
    name        VARCHAR(20) NOT NULL,
);

CREATE TABLE IF NOT EXISTS game_mechanics_map (
    game_id     INT NOT NULL,
    mech_id     INT NOT NULL
);

CREATE TABLE IF NOT EXISTS game_categories_map (
    game_id     INT NOT NULL,
    category_id INT NOT NULL,
);