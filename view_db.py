import oracledb


def main():
    conn = oracledb.connect(user="system",
                            password="YourPassword123",
                            dsn="localhost/XEPDB1")
    cursor = conn.cursor()

    # cursor.execute("""
    #     INSERT INTO Movie_Genre
    #     VALUES ('tt2582802', 'Horror')
    # """)
    # conn.commit()

    cursor.execute("SELECT * FROM Tv_Show")
    rows = cursor.fetchall()
    counter = 0
    for row in rows:
        print(row)
        counter += 1
    print(counter)

    cursor.close()
    conn.close()


main()
