
import sqlite3

database_path = "sql/smartsales.db"

try:
    connection = sqlite3.connect(database_path)

    query = "SELECT name FROM sqlite_master WHERE type = ?"
    tables = connection.execute(query, ("table",)).fetchall()

    print("Database connected successfully!")
    print("Tables found:")

    for table in tables:
        print("-", table[0])

    connection.close()

except sqlite3.Error as error:
    print("Database error:", error)
