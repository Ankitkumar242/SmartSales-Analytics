import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("sql/smartsales.db")

print("Database connected successfully!")

# Close connection
connection.close()

print("Database connection closed.")

import sqlite3
import pandas as pd

# Excel file load
df = pd.read_excel("data/clean_sales_data.xlsx")

print("Excel data loaded!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Connect to SQLite database
connection = sqlite3.connect("sql/smartsales.db")

# Send DataFrame to SQL table
df.to_sql(
    "sales",
    connection,
    if_exists="replace",
    index=False
)

print("Data imported into SQL successfully!")

# Close connection
connection.close()

print("Database connection closed.")