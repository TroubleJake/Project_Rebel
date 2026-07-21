from src.database.database import database_exist
from src.database.schema import create_indexes, create_tables
from src.utils.logger import logger

def main():
    logger.info("Starting Project Rebel.")
    try:
        if database_exist():
            logger.info("Database already exists.")
        else:
            logger.info("Database not found. Creating database...")
        create_tables()
        create_indexes()
        logger.info("Project Rebel initialized successfully.")
    except Exception as e:
        logger.critical(f"Startup failed: {e}")

if __name__ == "__main__":
    main()