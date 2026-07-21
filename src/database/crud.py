import sqlite3
from .database import get_connection
from src.utils.logger import logger

def add_product (
        name,
        brand,
        department,
        category,
        number_system,
        plu,
        price_type,
        unit_price,
        unit,
        notes="",
        active=1
):
    if not name.strip():
        raise ValueError("Product name cannot be empty.")
    if not plu.isdigit() or len(plu) != 5:
        raise ValueError("PLU must be a 5-digit number.")
    if number_system < 0 or number_system > 9:
        raise ValueError("Number system must be between 0 and 9.")
    if unit_price < 0:
        raise ValueError("Unit price cannot be negative.")
    if unit not in ("lb", "oz", "kg", "g", "each"):
        raise ValueError("Invalid unit.")
    if price_type not in ("weight", "price"):
        raise ValueError("Invalid price type.")
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO products (name, brand, department, category, number_system, plu, price_type, unit_price, unit, notes, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, brand, department, category, number_system, plu, price_type, unit_price, unit, notes, active))
        conn.commit()
        if product_id := cursor.lastrowid:
            logger.info(f"Added product: {name}")
        else:
            logger.warning(f"Failed to add product: {name}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Failed to add product: {e}")
        return False
    finally:
        conn.close()

def get_product_by_id(product_id):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM products WHERE id = ?
        """, (product_id,))
        product = cursor.fetchone()
        if product:
            logger.info(f"Retrieved product by ID: {product_id}")
        else:
            logger.warning(f"No product found with ID: {product_id}")
        return product
    except sqlite3.Error as e:
        logger.error(f"Failed to retrieve product by id: {e}")
        return None
    finally:
        conn.close()

def get_product_by_plu(plu):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM products WHERE plu = ?
        """, (plu,))
        product = cursor.fetchone()
        if product:
            logger.info(f"Retrieved product by PLU: {plu}")
        else:
            logger.warning(f"No product found with PLU: {plu}")
        return product
    except sqlite3.Error as e:
        logger.error(f"Failed to retrieve product by PLU: {e}")
        return None
    finally:
        conn.close()

def get_product_by_barcode(barcode):
    number_system = int(barcode[0])
    plu = barcode[1:6]
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM products WHERE number_system = ? AND plu = ?
        """, (number_system, plu))
        product = cursor.fetchone()
        if product:
            logger.info(f"Retrieved product by barcode: {barcode}")
        else:
            logger.warning(f"No product found with barcode: {barcode}")
        return product
    except sqlite3.Error as e:
        logger.error(f"Failed to retrieve product by barcode: {e}")
        return None
    finally:
        conn.close()

def search_products(name):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM products WHERE name LIKE ?
        """, (f"%{name}%",))
        products = cursor.fetchall()
        if products:
            logger.info(f"Found {len(products)} products matching name: {name}")
        else:
            logger.warning(f"No products found matching name: {name}")
        return products
    except sqlite3.Error as e:
        logger.error(f"Failed to search products by name: {e}")
        return None
    finally:
        conn.close()

def list_products():
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM products ORDER BY name
        """)
        products = cursor.fetchall()
        if products:
            logger.info(f"Retrieved {len(products)} products.")
        else:
            logger.warning("No products found.")
        return products
    except sqlite3.Error as e:
        logger.error(f"Failed to list products: {e}")
        return None
    finally:
        conn.close()

def update_product(
        product_id,
        name,
        brand,
        department,
        category,
        number_system,
        plu,
        price_type,
        unit_price,
        unit,
        notes,
        active
):
    if not name.strip():
        raise ValueError("Product name cannot be empty.")
    if not plu.isdigit() or len(plu) != 5:
        raise ValueError("PLU must be a 5-digit number.")
    if number_system < 0 or number_system > 9:
        raise ValueError("Number system must be between 0 and 9.")
    if unit_price < 0:
        raise ValueError("Unit price cannot be negative.")
    if unit not in ("lb", "oz", "kg", "g", "each"):
        raise ValueError("Invalid unit.")
    if price_type not in ("weight", "price"):
        raise ValueError("Invalid price type.")
    conn = get_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE products
        SET name = ?, brand = ?, department = ?, category = ?, number_system = ?, plu = ?, price_type = ?, unit_price = ?, unit = ?, notes = ?, active = ?, last_updated = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (name, brand, department, category, number_system, plu, price_type, unit_price, unit, notes, active, product_id))
        conn.commit()
        if cursor.rowcount > 0:
            logger.info(f"Updated product with ID: {product_id}")
        else:
            logger.warning(f"No product found with ID: {product_id}")
    except sqlite3.Error as e:
        logger.error(f"Failed to update product: {e}")
    finally:
        conn.close()

def delete_product(product_id):
    conn = get_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM products WHERE id = ?
        """, (product_id,))
        conn.commit()
        if cursor.rowcount > 0:
            logger.info(f"Deleted product with ID: {product_id}")
        else:
            logger.warning(f"No product found with ID: {product_id}")
    except sqlite3.Error as e:
        logger.error(f"Failed to delete product: {e}")
    finally:
        conn.close()