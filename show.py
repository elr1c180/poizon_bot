import sqlite3


with sqlite3.connect('promo.db') as conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM promo')
    for promo in cur.fetchall():
        print(promo)