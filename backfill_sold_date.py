import sqlite3

conn = sqlite3.connect("database/inventory.db")
c = conn.cursor()

c.execute("""
    UPDATE inventory
    SET sold_date = DATE('now')
    WHERE tenant_id = 1
      AND quantity_sold > 0
      AND (sold_date IS NULL OR sold_date = '')
""")
print("Rows backfilled:", c.rowcount)

conn.commit()
conn.close()