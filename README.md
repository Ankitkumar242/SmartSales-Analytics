# SmartSales Analytics

An end-to-end Sales Data Analytics project built using Python, SQL, Pandas, and Streamlit.

## Project Overview

SmartSales Analytics analyzes sales transaction data to identify sales trends, profitability, product performance, and regional business insights through an interactive dashboard.

## Technologies Used

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- SQL (SQLite)
- Streamlit
- Excel

## Key Features

- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- SQL-based business analysis
- Interactive dashboard with filters
- Sales, profit, and profit-margin KPIs
- Monthly sales and profit analysis
- Region, category, and product performance charts
- CSV report download
- Data quality validation

## Dataset

- 10,000 sales records
- 15 columns
- 10,000 unique orders
- No missing values in the validated dataset
- No duplicate rows in the validated dataset

## Business Metrics

- Total Sales: ₹719,677,400
- Total Profit: ₹214,871,580.72
- Overall Profit Margin: Approximately 29.86%

These figures are based on the current project dataset.

## Run the Dashboard

1. Install Python.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Start the dashboard:

   `python -m streamlit run app.py`

6. Open the local URL displayed in the terminal.

## Data Validation

The project includes a validation script:

`python sql/validate_data.py`

It checks missing values, duplicate rows, order counts, numeric values, negative sales, and non-positive quantities.

## Project Goal

To demonstrate practical data analytics skills, including data preparation, SQL querying, exploratory analysis, visualization, and dashboard development.
