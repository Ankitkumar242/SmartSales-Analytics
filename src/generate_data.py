import pandas as pd
import numpy as np

# Reproducible random data
np.random.seed(42)

# Number of records
n = 10000

# Basic data
order_ids = np.arange(10001, 10001 + n)

dates = pd.date_range(
    start="2025-01-01",
    end="2025-12-31",
    periods=n
)

customers = [f"CUST{str(i).zfill(4)}" for i in range(1, 1001)]

customer_names = [
    f"Customer_{i}" for i in range(1, 1001)
]

products = [
    "Laptop",
    "Mobile",
    "Monitor",
    "Keyboard",
    "Mouse",
    "Headphones",
    "Printer",
    "Tablet",
    "Webcam",
    "Speaker"
]

categories = {
    "Laptop": "Electronics",
    "Mobile": "Electronics",
    "Monitor": "Electronics",
    "Keyboard": "Accessories",
    "Mouse": "Accessories",
    "Headphones": "Accessories",
    "Printer": "Office",
    "Tablet": "Electronics",
    "Webcam": "Accessories",
    "Speaker": "Electronics"
}

regions = [
    "North",
    "South",
    "East",
    "West"
]

# Generate random values
customer_ids = np.random.choice(customers, n)

customer_name_map = {
    customer: f"Customer_{int(customer[4:])}"
    for customer in customers
}

customer_name_values = [
    customer_name_map[c] for c in customer_ids
]

product_values = np.random.choice(products, n)

region_values = np.random.choice(regions, n)

quantity = np.random.randint(1, 10, n)

unit_price = np.random.choice(
    [500, 1000, 1500, 3000, 5000, 10000, 20000, 40000, 60000],
    n
)

discount = np.random.choice(
    [0, 5, 10, 15, 20],
    n
)

# Sales calculation
sales = quantity * unit_price

sales_after_discount = sales * (1 - discount / 100)

# Cost
cost = sales_after_discount * np.random.uniform(
    0.55, 0.85, n
)

profit = sales_after_discount - cost

# Create DataFrame
df = pd.DataFrame({
    "Order_ID": order_ids,
    "Order_Date": dates,
    "Customer_ID": customer_ids,
    "Customer_Name": customer_name_values,
    "Product": product_values,
    "Category": [categories[p] for p in product_values],
    "Region": region_values,
    "Quantity": quantity,
    "Unit_Price": unit_price,
    "Discount": discount,
    "Sales": sales_after_discount.round(2),
    "Cost": cost.round(2),
    "Profit": profit.round(2)
})

# Save Excel file
df.to_excel(
    "data/sales_data.xlsx",
    index=False
)

print("Dataset created successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("\nFirst 5 rows:")
print(df.head())