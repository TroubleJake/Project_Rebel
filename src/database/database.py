import sqlite3
from pathlib import Path
from src.utils.logger import logger

DATABASE_PATH = Path("data/products.db")

def get_connection():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        logger.info("Database connection established.")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return None

def database_exist():
    try:
        exists = DATABASE_PATH.exists()
        if exists:
            logger.info(f"Database file found.")
        else:
            logger.warning(f"Database file not found.")
        return exists
    except OSError as e:
        logger.error(f"Error checking database existence: {e}")
        return False