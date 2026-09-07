import pandas as pd


# File paths
INPUT_FILE = "data/raw/Online Retail.xlsx"
OUTPUT_FILE = "data/processed/online_retail_cleaned.csv"


# Load raw data
df = pd.read_excel(INPUT_FILE)

raw_rows = len(df)


# --------------------------------------------------
# 1. Remove exact duplicate rows
# --------------------------------------------------
duplicate_count = df.duplicated().sum()

df = df.drop_duplicates()


# --------------------------------------------------
# 2. Remove cancelled invoices
# --------------------------------------------------
cancelled_invoice = df["InvoiceNo"].astype(str).str.startswith("C")

cancelled_count = cancelled_invoice.sum()

df = df[~cancelled_invoice].copy()


# --------------------------------------------------
# 3. Remove transactions with non-positive prices
# --------------------------------------------------
invalid_price = df["UnitPrice"] <= 0

invalid_price_count = invalid_price.sum()

df = df[~invalid_price].copy()


# --------------------------------------------------
# 4. Handle missing product descriptions
# --------------------------------------------------
description_mapping = (
    df.dropna(subset=["Description"])
    .groupby("StockCode")["Description"]
    .first()
)

missing_description_before = df["Description"].isna().sum()

df["Description"] = df["Description"].fillna(
    df["StockCode"].map(description_mapping)
)

missing_description_after = df["Description"].isna().sum()


# --------------------------------------------------
# 5. Handle missing CustomerID
# --------------------------------------------------
missing_customer_count = df["CustomerID"].isna().sum()

# Missing CustomerID values are intentionally retained.
# They will be represented as "Unknown Customer"
# during the data warehouse loading stage.


# --------------------------------------------------
# 6. Create revenue column
# --------------------------------------------------
df["Revenue"] = df["Quantity"] * df["UnitPrice"]


# --------------------------------------------------
# 7. Save processed data
# --------------------------------------------------
df.to_csv(OUTPUT_FILE, index=False)


# --------------------------------------------------
# Cleaning summary
# --------------------------------------------------
print("\n===== CLEANING SUMMARY =====")

print(f"Raw rows: {raw_rows}")
print(f"Duplicate rows removed: {duplicate_count}")
print(f"Cancelled transaction rows removed: {cancelled_count}")
print(f"Non-positive price rows removed: {invalid_price_count}")

print(
    f"Missing descriptions before filling: "
    f"{missing_description_before}"
)

print(
    f"Missing descriptions after filling: "
    f"{missing_description_after}"
)

print(
    f"Rows with missing CustomerID retained: "
    f"{missing_customer_count}"
)

print(f"Final cleaned rows: {len(df)}")

print(f"\nProcessed file saved to: {OUTPUT_FILE}")