import sqlite3

conn = sqlite3.connect(
    "database/inventory.db"
)

cursor = conn.cursor()

cursor.execute("""
    SELECT
        id,
        product_name,
        quantity_total,
        quantity_available,
        quantity_sold
    FROM inventory
    ORDER BY id DESC
""")

for row in cursor.fetchall():
    print(row)

conn.close()