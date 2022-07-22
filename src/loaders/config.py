"""loader package config"""

from yaml import safe_load

try:
    with open('config/config.yaml', 'r') as file:
        config = safe_load(file)
except FileNotFoundError:
    print('Config not found. Using package defaults instead.')
    DATA_PATH = 'data'
    NUM_OF_PAGES = 10
    BATCH_SIZE = 1000
else:
    DATA_PATH = config['DATA_PATH']
    NUM_OF_PAGES = config['SCRAPING']['NUM_OF_PAGES']
    BATCH_SIZE = config['SCRAPING']['BATCH_SIZE']

try:
    with open('config/db_config.yaml', 'r') as file:
        config = safe_load(file)
except FileNotFoundError:
    print('No db config found. Defaulting to boardgames.sqlite3')
    DB_URL = 'sqlite+pysqlite:///boardgames.sqlite3'
else:
    dialect = config['DIALECT']
    driver = config['DRIVER']
    username = config['USER']
    password = config['PASS']
    host = config['HOST']
    port = config['PORT']
    database = config['DB']
    if dialect == 'sqlite':
        DB_URL = f'{dialect}+{driver}:///{database}'
    else:
        DB_URL = f'{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'
