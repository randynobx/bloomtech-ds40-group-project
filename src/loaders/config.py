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
        self.dialect = config['DIALECT']
        self.driver = config['DRIVER']
        self.username = config['USER']
        self.password = config['PASS']
        self.host = config['HOST']
        self.port = config['PORT']
        self.database = config['DB']
        if self.dialect == 'sqlite':
            self.DB_URL = f'{self.dialect}+{self.driver}:///{self.database}'
        else:
            self.DB_URL = f'{self.dialect}+{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
