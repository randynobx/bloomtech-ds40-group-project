"""Create and load boardgame database"""
from src.loaders import scraper_browse_id, scraper_classifications, create_db,\
                        scraper_games, ingest_classifications, ingest_games
from src.loaders.config import Config

# Create config object
config = Config('config')

# Run scraping modules
print('Scraping BGG...')
scraper_browse_id.run(config)
scraper_classifications.run(config)
scraper_games.run(config)
print('Scraping Done')

# Create database
print('Initializing Database...', end='')
create_db.run(config)
print('Done')

# Run ingestion modules
print('Transforming and loading data to database...')
ingest_classifications.run(config)
ingest_games.run(config)
print('ETL Done')
