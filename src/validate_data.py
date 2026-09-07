import pandas as pd


INPUT_FILE = "data/processed/online_retail_cleaned.csv"


df = pd.read_csv(INPUT_FILE)


print("\n===== CLEANED DATA VALIDATION =====")

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


print("\n===== DUPLICATES =====")
print(f"Duplicate rows: {df.duplicated().sum()}")


print("\n===== CANCELLED INVOICES =====")
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
print(f"Cancelled invoice rows: {cancelled.sum()}")


print("\n===== QUANTITY VALIDATION =====")
print(f"Negative quantity rows: {(df['Quantity'] < 0).sum()}")
print(f"Zero quantity rows: {(df['Quantity'] == 0).sum()}")


print("\n===== PRICE VALIDATION =====")
print(f"Non-positive price rows: {(df['UnitPrice'] <= 0).sum()}")


print("\n===== MISSING VALUES =====")
print(df.isnull().sum())


print("\n===== DATA TYPES =====")
print(df.dtypes)


print("\n===== REVENUE VALIDATION =====")
print(f"Minimum revenue: {df['Revenue'].min()}")
print(f"Maximum revenue: {df['Revenue'].max()}")


print("\n===== DATE RANGE =====")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
print(f"Start: {df['InvoiceDate'].min()}")
print(f"End: {df['InvoiceDate'].max()}")


print("\n===== VALIDATION STATUS =====")

checks = {
    "No duplicate rows": df.duplicated().sum() == 0,
    "No cancelled invoices": cancelled.sum() == 0,
    "No negative quantities": (df["Quantity"] < 0).sum() == 0,
    "No zero quantities": (df["Quantity"] == 0).sum() == 0,
    "No non-positive prices": (df["UnitPrice"] <= 0).sum() == 0,
}

for check, passed in checks.items():
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {check}")