import sqlite3
conn = sqlite3.connect("database/inventory.db")
c = conn.cursor()

# ID 19: literal 'nan' string → empty string
c.execute("""
    UPDATE inventory SET brand = ''
    WHERE id = 19 AND tenant_id = 1 AND brand = 'nan'
""")
print("ID 19 brand fixed:", c.rowcount)

# Any row where Total ≠ Available + Sold → recompute
c.execute("""
    UPDATE inventory
    SET quantity_total = quantity_available + quantity_sold
    WHERE tenant_id = 1
      AND quantity_total != quantity_available + quantity_sold
""")
print("Totals recomputed:", c.rowcount)

conn.commit()
conn.close()
print("Done.")