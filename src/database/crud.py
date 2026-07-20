from .database import get_connection

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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO products (name, brand, department, category, number_system, plu, price_type, unit_price, unit, notes, active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, brand, department, category, number_system, plu, price_type, unit_price, unit, notes, active))
    conn.commit()
    conn.close()

def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM products WHERE id = ?
    """, (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

def get_product_by_plu(plu):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM products WHERE plu = ?
    """, (plu,))
    product = cursor.fetchone()
    conn.close()
    return product

def search_products(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM products WHERE name LIKE ?
    """, (f"%{name}%",))
    products = cursor.fetchall()
    conn.close()
    return products

def list_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM products ORDER BY name
    """)
    products = cursor.fetchall()
    conn.close()
    return products

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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE products
    SET name = ?, brand = ?, department = ?, category = ?, number_system = ?, plu = ?, price_type = ?, unit_price = ?, unit = ?, notes = ?, active = ?, last_updated = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (name, brand, department, category, number_system, plu, price_type, unit_price, unit, notes, active, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM products WHERE id = ?
    """, (product_id,))
    conn.commit()
    conn.close()