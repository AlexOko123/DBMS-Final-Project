import oracledb


def main():
    conn = oracledb.connect(user="system",
                            password="YourPassword123",
                            dsn="localhost/XEPDB1")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Movie_Genre
        VALUES ('tt2582802', 'Horror')
    """)
    conn.commit()

    cursor.execute("SELECT * FROM Movie_Genre")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    conn.close()


main()
