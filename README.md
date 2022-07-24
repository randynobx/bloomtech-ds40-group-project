# Board Game Project

![Pytest](https://github.com/randynobx/boardgamegeek_loader/actions/workflows/python-app.yml/badge.svg?event=push)

ETL pipeline, analysis and prediction models of board game data from BoardGameGeek.com

## Contents
- [About](#about)
- [Usage](#usage)
- [Contributers](#contributers)

## About

"BGP" is a collaborative project between members of the DataScience40 cohort at Bloomtech.

It includes a fully formed ETL pipeline using BoardGameGeek.com's BGGXMLAPI2 to create a relational database for 
analysis and predictive modeling purposes.

## Usage

### Setup pipenv enviroment for scraping
Run `pipenv install --dev` to install all requrired packages

Then run `pipenv shell`
### Setup database
Update `config/db_config.yaml` to connect to a database of your choosing, or stick with the default for sqlite3.

Then run

```bash
python setup_db.py
```

## Contributers

This project is a collaboration between three members of the DS40 cohort in the Data Science program at Bloomtech.
Below is a brief summary of each of our contributions. For more detail, please see [CONTRIBUTIONS.md](CONTRIBUTIONS.md).

### Chris Burrows
- stuff

### Nikolay Glushetskiy
- stuff

### Randy Nance
- Data Engineering
    - Wrote loaders subpackage and tests
    - Designed database schema
