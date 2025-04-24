import oracledb

conn = oracledb.connect(user="system",
                        password="YourPassword123",
                        dsn="localhost/XEPDB1")
cursor = conn.cursor()

cursor.execute("""
    SELECT Title FROM MOVIE
    """)

rows = cursor.fetchall()
for row in rows:
    print(row)
