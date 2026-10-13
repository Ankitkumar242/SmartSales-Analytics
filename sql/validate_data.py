
import sqlite3
import pandas as pd

DATABASE = "sql/smartsales.db"

def validate_sales_data():
    print("=" * 55)
    print("SMARTSALES ANALYTICS - DATA VALIDATION")
    print("=" * 55)

    with sqlite3.connect(DATABASE) as connection:
        # Load data from SQL
        df = pd.read_sql_query("SELECT * FROM sales", connection)

    print(f"\nTotal Rows: {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")

    # 1. Missing values
    missing = int(df.isnull().sum().sum())
    print(f"\nMissing Values: {missing}")

    # 2. Duplicate rows
    duplicates = int(df.duplicated().sum())
    print(f"Duplicate Rows: {duplicates}")

    # 3. Unique orders
    if "Order_ID" in df.columns:
        print(f"Unique Orders: {df['Order_ID'].nunique():,}")

    # 4. Sales and profit totals
    for column in ["Sales", "Profit"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
            print(f"Total {column}: {df[column].sum():,.2f}")
            print(f"Invalid {column} Values: {df[column].isna().sum()}")

    # 5. Negative sales or quantities
    if "Sales" in df.columns:
        print("Negative Sales Rows:", int((df["Sales"] < 0).sum()))

    if "Quantity" in df.columns:
        quantity = pd.to_numeric(df["Quantity"], errors="coerce")
        print("Non-positive Quantity Rows:", int((quantity <= 0).sum()))

    # 6. Final status
    print("\n" + "=" * 55)

    if missing == 0 and duplicates == 0:
        print("BASIC VALIDATION PASSED")
    else:
        print("REVIEW REQUIRED: Check missing values or duplicates")

    print("=" * 55)


if __name__ == "__main__":
    validate_sales_data()
