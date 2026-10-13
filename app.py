
import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SmartSales Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------- DESIGN ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
div[data-testid="stMetric"] {
    background-color: rgba(128, 128, 128, 0.08);
    border: 1px solid rgba(128, 128, 128, 0.2);
    padding: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA FROM SQL ----------------
@st.cache_data
def load_data():
    database_path = Path("sql/smartsales.db")

    if not database_path.exists():
        raise FileNotFoundError(
            f"Database not found: {database_path.resolve()}"
        )

    with sqlite3.connect(str(database_path)) as connection:
        data = pd.read_sql_query(
            "SELECT * FROM sales",
            connection,
            parse_dates=["Order_Date"]
        )

    required_columns = [
        "Order_ID", "Order_Date", "Product", "Category",
        "Region", "Quantity", "Sales", "Profit"
    ]

    missing_columns = [
        col for col in required_columns if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required database columns: {missing_columns}"
        )

    data["Order_Date"] = pd.to_datetime(
        data["Order_Date"], errors="coerce"
    )

    for col in ["Sales", "Profit", "Quantity", "Cost",
                "Unit_Price", "Discount"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=["Order_Date", "Sales", "Profit"])

    return data


try:
    df = load_data()
except Exception as error:
    st.error(f"Data load error: {error}")
    st.info(
        "Check karo ki sql/smartsales.db mein sales table hai "
        "aur app.py project ke main folder mein hai."
    )
    st.stop()


# ---------------- HEADER ----------------
st.title("📊 SmartSales Analytics")
st.caption(
    "Interactive Sales & Business Intelligence Dashboard"
)
st.success("Data source: SQLite Database — sales table")
st.divider()


# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("🔎 Dashboard Filters")

min_date = df["Order_Date"].min()
max_date = df["Order_Date"].max()

if pd.isna(min_date) or pd.isna(max_date):
    st.error("Database mein valid Order_Date values nahi hain.")
    st.stop()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date.date(), max_date.date()),
    min_value=min_date.date(),
    max_value=max_date.date()
)

regions = sorted(df["Region"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())
products = sorted(df["Product"].dropna().unique().tolist())

selected_regions = st.sidebar.multiselect(
    "Select Region", regions, default=regions
)

selected_categories = st.sidebar.multiselect(
    "Select Category", categories, default=categories
)

selected_products = st.sidebar.multiselect(
    "Select Product", products, default=products
)


# ---------------- APPLY FILTERS ----------------
if isinstance(selected_dates, (tuple, list)):
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
    elif len(selected_dates) == 1:
        start_date = end_date = selected_dates[0]
    else:
        start_date, end_date = min_date.date(), max_date.date()
else:
    start_date = end_date = selected_dates

filtered_df = df[
    (df["Order_Date"].dt.date >= start_date)
    & (df["Order_Date"].dt.date <= end_date)
    & (df["Region"].isin(selected_regions))
    & (df["Category"].isin(selected_categories))
    & (df["Product"].isin(selected_products))
].copy()


# ---------------- KPI CARDS ----------------
st.subheader("Business Overview")

if filtered_df.empty:
    st.warning("Selected filters ke liye data nahi mila.")
    st.stop()

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

k1, k2, k3, k4 = st.columns(4)

k1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
k2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
k3.metric("🧾 Total Orders", f"{total_orders:,}")
k4.metric("🎯 Profit Margin", f"{profit_margin:.2f}%")


# ---------------- MONTHLY PERFORMANCE ----------------
st.divider()
st.subheader("📅 Monthly Performance")

monthly = (
    filtered_df.assign(
        Month=filtered_df["Order_Date"].dt.to_period("M").astype(str)
    )
    .groupby("Month")[["Sales", "Profit"]]
    .sum()
    .sort_index()
)

left, right = st.columns(2)

with left:
    st.markdown("**Monthly Sales Trend**")
    st.line_chart(monthly[["Sales"]], height=320)

with right:
    st.markdown("**Monthly Profit Trend**")
    st.line_chart(monthly[["Profit"]], height=320)


# ---------------- REGION PERFORMANCE ----------------
st.divider()
st.subheader("🌍 Regional Performance")

region_data = (
    filtered_df.groupby("Region", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Sales", ascending=False)
)

left, right = st.columns(2)

with left:
    st.markdown("**Sales by Region**")
    st.bar_chart(region_data.set_index("Region")[["Sales"]])

with right:
    st.markdown("**Profit by Region**")
    st.bar_chart(region_data.set_index("Region")[["Profit"]])


# ---------------- CATEGORY PERFORMANCE ----------------
st.divider()
st.subheader("📦 Category Performance")

category_data = (
    filtered_df.groupby("Category", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Sales", ascending=False)
)

left, right = st.columns(2)

with left:
    st.markdown("**Sales by Category**")
    st.bar_chart(category_data.set_index("Category")[["Sales"]])

with right:
    st.markdown("**Profit by Category**")
    st.bar_chart(category_data.set_index("Category")[["Profit"]])


# ---------------- PRODUCT PERFORMANCE ----------------
st.divider()
st.subheader("🏆 Product Analysis")

product_data = (
    filtered_df.groupby("Product", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
)

product_data["Profit Margin (%)"] = (
    product_data["Profit"]
    .div(product_data["Sales"].replace(0, pd.NA))
    .mul(100)
    .fillna(0)
)

product_data = product_data.sort_values(
    "Sales", ascending=False
)

left, right = st.columns(2)

with left:
    st.markdown("**Top 10 Products by Sales**")
    top_products = (
        product_data.head(10)
        .sort_values("Sales")
        .set_index("Product")
    )
    st.bar_chart(top_products[["Sales"]])

with right:
    st.markdown("**Product Profit Margin**")
    margin_products = (
        product_data.sort_values("Profit Margin (%)")
        .set_index("Product")
    )
    st.bar_chart(margin_products[["Profit Margin (%)"]])


# ---------------- DETAIL TABLE ----------------
st.divider()
st.subheader("📋 Detailed Product Summary")

st.dataframe(
    product_data.style.format({
        "Sales": "₹{:,.2f}",
        "Profit": "₹{:,.2f}",
        "Profit Margin (%)": "{:.2f}%",
        "Quantity": "{:,.0f}"
    }),
    use_container_width=True,
    hide_index=True
)


# ---------------- DOWNLOAD CSV ----------------
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=csv_data,
    file_name="smartsales_filtered_data.csv",
    mime="text/csv"
)

st.caption(
    f"SmartSales Analytics | SQL rows loaded: {len(df):,}"
)
