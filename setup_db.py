"""Create and load boardgame database"""
from src.loaders import scraper_browse_id, scraper_classifications, create_db,\
                        scraper_games, ingest_classifications, ingest_games

# Run scraping modules
print('Scraping BGG...')
scraper_browse_id.run()
scraper_classifications.run()
scraper_games.run()
print('Scraping Done')

# Create database
print('Initializing Database...', end='')
create_db.run()
print('Done')

# Run ingestion modules
print('Transforming and loading data to database...')
ingest_classifications.run()
ingest_games.run()
print('ETL Done')
