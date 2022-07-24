"""loader package config"""

from yaml import safe_load

try:
    with open('config/config.yaml', 'r') as file:
        config = safe_load(file)
except FileNotFoundError:
    print('ERROR: config.yaml file not found!')
    raise
else:
    DATA_PATH = config['DATA']['PATH']
    RAW_PATH = DATA_PATH + '/' + config['DATA']['RAW']
    PROC_PATH = DATA_PATH + '/' + config['DATA']['PROC']
    FINAL_PATH = DATA_PATH + '/' + config['DATA']['FINAL']
    NUM_OF_PAGES = config['SCRAPING']['NUM_OF_PAGES']
    BATCH_SIZE = config['SCRAPING']['BATCH_SIZE']
    GAME_IDS_FILENAME = config['SCRAPING']['GAME_IDS_FILENAME']
    BROWSE_FILENAME = config['SCRAPING']['BROWSE_FILENAME']
    BATCH_FILENAME = config['SCRAPING']['BATCH_FILENAME']

try:
    with open('config/db_config.yaml', 'r') as file:
        config = safe_load(file)
except FileNotFoundError:
    print('ERROR: No db config found!')
    raise
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
