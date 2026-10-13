import sqlite3
import pandas as pd

connection = sqlite3.connect("sql/smartsales.db")

query = """
SELECT
    Region,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC;
"""

result = pd.read_sql_query(query, connection)

print("Region-wise Sales and Profit:")
print(result)

connection.close()