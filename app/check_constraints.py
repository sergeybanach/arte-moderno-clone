import sqlite3

# Otevření databáze (uprav název souboru podle své databáze)
conn = sqlite3.connect('app.db')  # Nahraď 'app.db' názvem své databáze
cursor = conn.cursor()

# Výpis cizích klíčů v tabulce cart_item
cursor.execute("PRAGMA foreign_key_list(cart_item);")
foreign_keys = cursor.fetchall()

for fk in foreign_keys:
    print(fk)

conn.close()
