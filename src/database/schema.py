from .database import get_connection

def create_tables():
    conn = get_connection()
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
    conn.close()