import sqlite3
from datetime import datetime

conn = sqlite3.connect("database/inventory.db")
c = conn.cursor()

# Safety: ensure the table exists
c.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inventory_id INTEGER NOT NULL,
        tenant_id INTEGER NOT NULL DEFAULT 1,
        product_name TEXT, brand TEXT, model TEXT, category TEXT,
        price REAL, sold_at TEXT NOT NULL, restored_at TEXT
    )
""")

# Skip rows that already have sales (idempotent)
c.execute("""
    SELECT id, tenant_id, product_name, brand, model, category, price,
           quantity_sold, sold_date
    FROM inventory
    WHERE quantity_sold > 0
      AND id NOT IN (SELECT DISTINCT inventory_id FROM sales WHERE restored_at IS NULL)
""")

total = 0
for row in c.fetchall():
    inv_id, tid, pn, brand, model, cat, price, sold_count, sold_date = row
    ts = (sold_date + " 00:00:00") if sold_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for _ in range(sold_count):
        c.execute("""
            INSERT INTO sales
                (inventory_id, tenant_id, product_name, brand, model, category, price, sold_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (inv_id, tid, pn, brand, model, cat, price, ts))
        total += 1

conn.commit()
conn.close()
print(f"Created {total} historical sale rows.")