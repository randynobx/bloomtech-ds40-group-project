"""Create and load boardgame database"""
import src.loaders as loaders

# Run scraping modules
print('Scraping BGG...')
loaders.scraper_browse_id.run()
loaders.scraper_classifications.run()
loaders.scraper_games.run()
print('Scraping Done')

# Create database
print('Initializing Database...', end='')
loaders.create_db.run()
print('Done')

# Run ingestion modules
print('Transforming and loading data to database...')
loaders.ingest_classifications.run()
loaders.ingest_games.run()
print('ETL Done')
