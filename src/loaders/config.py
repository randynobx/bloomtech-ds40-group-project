"""loader package config"""

from yaml import safe_load

class Config:
    def __init__(self, path: str='config') -> None:
        # General config
        with open(f'{path}/config.yaml', 'r') as file:
            config = safe_load(file)
        self.DATA_PATH = config['DATA']['PATH']
        self.RAW_PATH = self.DATA_PATH + '/' + config['DATA']['RAW']
        self.PROC_PATH = self.DATA_PATH + '/' + config['DATA']['PROC']
        self.FINAL_PATH = self.DATA_PATH + '/' + config['DATA']['FINAL']
        self.NUM_OF_PAGES = config['SCRAPING']['NUM_OF_PAGES']
        self.BATCH_SIZE = config['SCRAPING']['BATCH_SIZE']
        self.GAME_IDS_FILENAME = config['SCRAPING']['GAME_IDS_FILENAME']
        self.BROWSE_FILENAME = config['SCRAPING']['BROWSE_FILENAME']
        self.BATCH_FILENAME = config['SCRAPING']['BATCH_FILENAME']
        self.CLASSIFICATIONS = config['CLASSIFICATIONS']

        # Database config
        with open(f'{path}/db_config.yaml', 'r') as file:
            config = safe_load(file)
        dialect = config['DIALECT']
        driver = config['DRIVER']
        username = config['USER']
        password = config['PASS']
        host = config['HOST']
        port = config['PORT']
        database = config['DB']
        if dialect == 'sqlite':
            self.DB_URL = f'{dialect}+{driver}:///{database}'
        else:
            self.DB_URL = f'{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'
