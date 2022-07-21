/* Create boardgames database and tables */

CREATE DATABASE boardgames_db
    WITH OWNER = 'admin';

CREATE TABLE IF NOT EXISTS game (
    ID              PRIMARY KEY,
    Title           VARCHAR(30) NOT NULL,
    ReleaseYear     DATE NOT NULL,
    AvgRating       REAL NOT NULL,
    BayesRating     REAL NOT NULL,
    TotalRatings    INT NOT NULL,
    StdRatings      REAL NOT NULL,
    MinPlayers      INT NOT NULL,
    MaxPlayers      INT NOT NULL,
    MinPlaytime     INT NOT NULL,
    MaxPlaytime     INT NOT NULL,
    Weight          REAL NOT NULL,
    OwnedCopies     INT NOT NULL,
);

CREATE TABLE IF NOT EXISTS mechanic (
    ID     INT NOT NULL,
    Name   VARCHAR(20) NOT NULL,
);

CREATE TABLE IF NOT EXISTS category (
    ID      INT NOT NULL,
    Name    VARCHAR(20) NOT NULL,
);

CREATE TABLE IF NOT EXISTS game_mechanic_map (
    GameID      INT NOT NULL,
    MechanicID  INT NOT NULL
);

CREATE TABLE IF NOT EXISTS game_category_map (
    GameID     INT NOT NULL,
    CategoryID INT NOT NULL,
);