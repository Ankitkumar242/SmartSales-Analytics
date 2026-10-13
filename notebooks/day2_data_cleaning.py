import pandas as pd

# Excel file load
df = pd.read_excel("data/sales_data.xlsx")

print("Data loaded successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nFirst 5 rows:")
print(df.head())

print("\n--- DATA INFORMATION ---")
df.info()

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATE CHECK ---")

duplicates = df.duplicated().sum()

print("Duplicate rows:", duplicates)

print("\n--- NUMERICAL SUMMARY ---")
print(df.describe())

print("\n--- INVALID VALUES CHECK ---")

print("Quantity <= 0:", (df["Quantity"] <= 0).sum())
print("Unit Price <= 0:", (df["Unit_Price"] <= 0).sum())
print("Discount < 0:", (df["Discount"] < 0).sum())
print("Discount > 100:", (df["Discount"] > 100).sum())
print("Sales < 0:", (df["Sales"] < 0).sum())
print("Cost < 0:", (df["Cost"] < 0).sum())

# ---------------- CLEAN DATA ----------------

clean_df = df.copy()

# Remove duplicate rows
clean_df = clean_df.drop_duplicates()

# Remove rows with missing values
clean_df = clean_df.dropna()

# Convert date column to datetime
clean_df["Order_Date"] = pd.to_datetime(clean_df["Order_Date"])

print("\n--- CLEANING RESULT ---")
print("Original rows:", len(df))
print("Clean rows:", len(clean_df))
print("Rows removed:", len(df) - len(clean_df))

# Save cleaned dataset
clean_df.to_excel(
    "data/clean_sales_data.xlsx",
    index=False
)

print("\nClean dataset saved successfully!")

# ---------------- BUSINESS METRICS ----------------

clean_df["Profit_Margin"] = (
    clean_df["Profit"] / clean_df["Sales"] * 100
).round(2)

clean_df["Revenue_per_Unit"] = (
    clean_df["Sales"] / clean_df["Quantity"]
).round(2)

print("\n--- BUSINESS METRICS ---")
print(clean_df[[
    "Sales",
    "Cost",
    "Profit",
    "Profit_Margin",
    "Revenue_per_Unit"
]].head())

# Save final cleaned dataset
clean_df.to_excel(
    "data/clean_sales_data.xlsx",
    index=False
)

print("\nFinal cleaned dataset saved successfully!")
print("Final rows:", len(clean_df))
print("Final columns:", len(clean_df.columns))