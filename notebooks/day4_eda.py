
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create charts folder
os.makedirs("charts", exist_ok=True)

# Load cleaned dataset
df = pd.read_excel("data/clean_sales_data.xlsx")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

sns.set_theme(style="whitegrid")

print("=" * 50)
print("SMARTSALES ANALYTICS - EXPLORATORY DATA ANALYSIS")
print("=" * 50)

print("\nDataset Shape:", df.shape)
print("\nMissing Values:\n", df.isnull().sum())
print("\nDuplicate Rows:", df.duplicated().sum())

print("\nTotal Sales: ₹{:,.2f}".format(df["Sales"].sum()))
print("Total Profit: ₹{:,.2f}".format(df["Profit"].sum()))
print("Total Orders:", df["Order_ID"].nunique())

margin = df["Profit"].sum() / df["Sales"].sum() * 100
print("Overall Profit Margin: {:.2f}%".format(margin))

# 1. Sales Distribution
plt.figure(figsize=(9, 5))
sns.histplot(df["Sales"], bins=40, kde=True)
plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("charts/sales_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

# 2. Sales Outliers
plt.figure(figsize=(9, 5))
sns.boxplot(x=df["Sales"])
plt.title("Sales Outlier Analysis")
plt.tight_layout()
plt.savefig("charts/sales_outliers.png", dpi=300, bbox_inches="tight")
plt.close()

# 3. Top 10 Products by Sales
top_products = df.groupby("Product")["Sales"].sum().nlargest(10).sort_values()

plt.figure(figsize=(10, 6))
top_products.plot(kind="barh")
plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("charts/top_products.png", dpi=300, bbox_inches="tight")
plt.close()

# 4. Region Sales
region_sales = df.groupby("Region")["Sales"].sum().sort_values()

plt.figure(figsize=(8, 5))
region_sales.plot(kind="bar")
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/region_sales.png", dpi=300, bbox_inches="tight")
plt.close()

# 5. Category Sales
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
category_sales.plot(kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/category_sales.png", dpi=300, bbox_inches="tight")
plt.close()

# 6. Category Profit
category_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
category_profit.plot(kind="bar")
plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Total Profit")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/category_profit.png", dpi=300, bbox_inches="tight")
plt.close()

# 7. Monthly Sales
monthly_sales = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum()
monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(12, 5))
monthly_sales.plot(marker="o")
plt.title("Monthly Sales Trend - 2025")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_sales.png", dpi=300, bbox_inches="tight")
plt.close()

# 8. Monthly Profit
monthly_profit = df.groupby(df["Order_Date"].dt.to_period("M"))["Profit"].sum()
monthly_profit.index = monthly_profit.index.astype(str)

plt.figure(figsize=(12, 5))
monthly_profit.plot(marker="o")
plt.title("Monthly Profit Trend - 2025")
plt.xlabel("Month")
plt.ylabel("Total Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_profit.png", dpi=300, bbox_inches="tight")
plt.close()

# 9. Product Profit Margin
product_margin = (
    df.groupby("Product")["Profit"].sum()
    / df.groupby("Product")["Sales"].sum()
    * 100
).sort_values()

plt.figure(figsize=(10, 6))
product_margin.plot(kind="barh")
plt.title("Profit Margin by Product")
plt.xlabel("Profit Margin (%)")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("charts/product_profit_margin.png", dpi=300, bbox_inches="tight")
plt.close()

# Business Insights
print("\n" + "=" * 50)
print("BUSINESS INSIGHTS")
print("=" * 50)

print("Best-Selling Product:", df.groupby("Product")["Sales"].sum().idxmax())
print("Highest-Sales Region:", df.groupby("Region")["Sales"].sum().idxmax())
print("Highest-Profit Category:", df.groupby("Category")["Profit"].sum().idxmax())
print("Highest-Sales Month:", monthly_sales.idxmax())
print("Highest-Profit Month:", monthly_profit.idxmax())

print("\nAll 9 charts saved successfully in the charts folder.")
