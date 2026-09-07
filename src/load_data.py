import os
import pandas as pd
from sqlalchemy import create_engine, text

# File and database settings
INPUT_FILE = "data/processed/online_retail_cleaned.csv"

DB_USER = "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "online_retail_db"

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD environment variable is not set.")

# Connect to PostgreSQL
connection_string = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_string)

# Read cleaned data
df = pd.read_csv(INPUT_FILE)

# Convert date column
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print(f"Loaded {len(df):,} rows from cleaned CSV.")

# -------------------------------------------------
# Clear existing warehouse data
# This makes the script safe to run again.
# -------------------------------------------------

with engine.begin() as connection:
    connection.execute(
        text(
            """
            TRUNCATE TABLE
                fact_sales,
                dim_customer,
                dim_product,
                dim_date
            RESTART IDENTITY CASCADE;
            """
        )
    )

print("Existing warehouse data cleared.")

# -------------------------------------------------
# 1. Customer dimension
# -------------------------------------------------

customers = df[["CustomerID", "Country"]].copy()

customers = customers.rename(
    columns={
        "CustomerID": "customer_id",
        "Country": "country"
    }
)

customers["customer_id"] = customers["customer_id"].astype("Int64")

customers = customers.drop_duplicates(subset=["customer_id"])

customers.loc[
    customers["customer_id"].isna(),
    "country"
] = "Unknown"

customers.to_sql(
    "dim_customer",
    engine,
    if_exists="append",
    index=False
)

print(f"Customers loaded: {len(customers):,}")

# -------------------------------------------------
# 2. Product dimension
# -------------------------------------------------

products = df[["StockCode", "Description"]].copy()

products = products.rename(
    columns={
        "StockCode": "stock_code",
        "Description": "description"
    }
)

products = products.drop_duplicates(subset=["stock_code"])

products.to_sql(
    "dim_product",
    engine,
    if_exists="append",
    index=False
)

print(f"Products loaded: {len(products):,}")

# -------------------------------------------------
# 3. Date dimension
# -------------------------------------------------

dates = pd.DataFrame({
    "full_date": df["InvoiceDate"].dt.date.unique()
})

dates["full_date"] = pd.to_datetime(dates["full_date"])

dates["date_key"] = (
    dates["full_date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

dates["year"] = dates["full_date"].dt.year
dates["month"] = dates["full_date"].dt.month
dates["month_name"] = dates["full_date"].dt.month_name()
dates["quarter"] = dates["full_date"].dt.quarter

dates = dates[
    [
        "date_key",
        "full_date",
        "year",
        "month",
        "month_name",
        "quarter"
    ]
]

dates.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False
)

print(f"Dates loaded: {len(dates):,}")

# -------------------------------------------------
# 4. Sales fact table
# -------------------------------------------------

customer_lookup = pd.read_sql(
    "SELECT customer_key, customer_id FROM dim_customer",
    engine
)

product_lookup = pd.read_sql(
    "SELECT product_key, stock_code FROM dim_product",
    engine
)

sales = df.copy()

sales["CustomerID"] = sales["CustomerID"].astype("Int64")

# Match each sale with its customer key
sales = sales.merge(
    customer_lookup,
    left_on="CustomerID",
    right_on="customer_id",
    how="left"
)

# Find the Unknown Customer key
unknown_customer_key = customer_lookup.loc[
    customer_lookup["customer_id"].isna(),
    "customer_key"
].iloc[0]

# Assign Unknown Customer key to missing CustomerID records
sales["customer_key"] = sales["customer_key"].fillna(
    unknown_customer_key
)

# Match each sale with its product key
sales = sales.merge(
    product_lookup,
    left_on="StockCode",
    right_on="stock_code",
    how="left"
)

# Create date key
sales["date_key"] = (
    sales["InvoiceDate"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

# Rename columns for PostgreSQL
sales = sales.rename(
    columns={
        "InvoiceNo": "invoice_no",
        "Quantity": "quantity",
        "UnitPrice": "unit_price",
        "Revenue": "revenue"
    }
)

# Keep only fact table columns
sales = sales[
    [
        "invoice_no",
        "customer_key",
        "product_key",
        "date_key",
        "quantity",
        "unit_price",
        "revenue"
    ]
]

# Load sales transactions
sales.to_sql(
    "fact_sales",
    engine,
    if_exists="append",
    index=False
)

print(f"Sales transactions loaded: {len(sales):,}")

print("\nData loading completed successfully.")