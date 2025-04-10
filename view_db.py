import oracledb


def main():
    conn = oracledb.connect(user="system",
                            password="YourPassword123",
                            dsn="localhost/XEPDB1")
    cursor = conn.cursor()

    tables = [
        "Movie",
        "Director",
        "Movie_Review",
        "Directs_Movie",
        "Directs_TV_Show",
        "Movie_Genre",
        "Movie_Awards",
        "Movie_SServices",
        "Writes_Movie",
        "Writes_Show",
        "Writer_Media",
        "Writer",
        "Acts_Movie",
        "Acts_Show",
        "Actor_Media",
        "Actor",
        "Show_Streaming_Services",
        "Show_Media",
        "Show_Genre",
        "Show_Review",
        "Show_Award",
        "Tv_Show",
    ]

    for table in tables:
        try:
            print(f"\n--- {table} ---")
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except oracledb.DatabaseError as e:
            print(f"Error querying table {table}: {e}")

    cursor.close()
    conn.close()


main()
