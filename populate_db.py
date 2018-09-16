import sqlite3

sqlite_file = 'my_db.sqlite'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS DATA (
        X REAL,
        Y REAL
)""")

conn.commit()
conn.close()

if __name__=="__main__":
    pass