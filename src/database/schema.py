import sqlite3
from .database import get_connection
from src.utils.logger import logger

def create_tables():
    conn = get_connection()
    if conn is None:
        logger.error("Failed to create tables: Database connection could not be established.")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT,
            department TEXT,
            category TEXT,
            number_system INTEGER NOT NULL,
            plu TEXT NOT NULL,
            price_type TEXT NOT NULL,
            unit_price REAL NOT NULL,
            unit TEXT NOT NULL,
            notes TEXT,
            active INTEGER DEFAULT 1,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        logger.info("Database tables verified.")
    except sqlite3.Error as e:
        logger.error(f"Error creating tables: {e}")
    finally:
        conn.close()

def create_indexes():
    conn = get_connection()
    if conn is None:
        logger.error("Failed to create indexes: Database connection could not be established.")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_products_plu ON products(plu)
        """)
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)
        """)
        conn.commit()
        logger.info("Database indexes verified.")
    except sqlite3.Error as e:
        logger.error(f"Index creation failed: {e}")
    finally:
        conn.close()