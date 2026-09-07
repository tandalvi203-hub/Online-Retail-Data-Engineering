import pandas as pd


# Path to the raw dataset
file_path = "data/raw/Online Retail.xlsx"


# Read the Excel file
df = pd.read_excel(file_path)


print("\n===== DATASET OVERVIEW =====")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())


print("\n===== DATA TYPES =====")
print(df.dtypes)


print("\n===== MISSING VALUES =====")
print(df.isnull().sum())


print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())


print("\n===== FIRST 5 ROWS =====")
print(df.head())


print("\n===== UNIQUE CUSTOMERS =====")
print(df["CustomerID"].nunique())


print("\n===== UNIQUE PRODUCTS =====")
print(df["StockCode"].nunique())


print("\n===== DATE RANGE =====")
print(f"Start: {df['InvoiceDate'].min()}")
print(f"End: {df['InvoiceDate'].max()}")


print("\n===== QUANTITY RANGE =====")
print(f"Minimum: {df['Quantity'].min()}")
print(f"Maximum: {df['Quantity'].max()}")


print("\n===== UNIT PRICE RANGE =====")
print(f"Minimum: {df['UnitPrice'].min()}")
print(f"Maximum: {df['UnitPrice'].max()}")


print("\n===== CANCELLED INVOICES =====")
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
print(f"Cancelled transaction rows: {cancelled.sum()}")
print(f"Unique cancelled invoices: {df.loc[cancelled, 'InvoiceNo'].nunique()}")

print("\n===== NEGATIVE QUANTITY =====")
negative_quantity = df["Quantity"] < 0
print(f"Rows with negative quantity: {negative_quantity.sum()}")


print("\n===== NON-POSITIVE UNIT PRICE =====")
non_positive_price = df["UnitPrice"] <= 0
print(f"Rows with UnitPrice <= 0: {non_positive_price.sum()}")


print("\n===== INVOICE PREFIXES =====")
invoice_prefixes = df["InvoiceNo"].astype(str).str[0].value_counts()
print(invoice_prefixes)


print("\n===== COUNTRIES =====")
print(f"Number of countries: {df['Country'].nunique()}")
print(df["Country"].value_counts().head(15))


print("\n===== MISSING CUSTOMER ID =====")
missing_customer = df["CustomerID"].isna()
print(f"Rows with missing CustomerID: {missing_customer.sum()}")
print(
    f"Percentage: {(missing_customer.mean() * 100):.2f}%"
)


print("\n===== EXTREME NEGATIVE QUANTITY RECORDS =====")
print(
    df.loc[
        df["Quantity"] < 0,
        ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]
    ]
    .sort_values("Quantity")
    .head(10)
)


print("\n===== EXTREME UNIT PRICE RECORDS =====")
print(
    df.loc[
        df["UnitPrice"] <= 0,
        ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]
    ]
    .sort_values("UnitPrice")
    .head(10)
)


print("\n===== ZERO QUANTITY RECORDS =====")
print(f"Rows with Quantity = 0: {(df['Quantity'] == 0).sum()}")


print("\n===== ZERO UNIT PRICE RECORDS =====")
print(f"Rows with UnitPrice = 0: {(df['UnitPrice'] == 0).sum()}")

print("\n===== NEGATIVE QUANTITY vs CANCELLED INVOICE =====")

negative_quantity = df["Quantity"] < 0
cancelled_invoice = df["InvoiceNo"].astype(str).str.startswith("C")

print("Negative quantity + cancelled invoice:",
      (negative_quantity & cancelled_invoice).sum())

print("Negative quantity + normal invoice:",
      (negative_quantity & ~cancelled_invoice).sum())

print("Positive quantity + cancelled invoice:",
      ((df["Quantity"] > 0) & cancelled_invoice).sum())


print("\n===== NON-POSITIVE PRICE BY INVOICE TYPE =====")

print("Non-positive price + cancelled invoice:",
      (non_positive_price & cancelled_invoice).sum())

print("Non-positive price + normal invoice:",
      (non_positive_price & ~cancelled_invoice).sum())


print("\n===== MISSING CUSTOMER ID BY INVOICE TYPE =====")

print("Missing CustomerID + cancelled invoice:",
      (missing_customer & cancelled_invoice).sum())

print("Missing CustomerID + normal invoice:",
      (missing_customer & ~cancelled_invoice).sum())


print("\n===== INVOICE PREFIX + QUANTITY SUMMARY =====")

invoice_summary = df.groupby(
    df["InvoiceNo"].astype(str).str[0]
)["Quantity"].agg(["count", "min", "max", "sum"])

print(invoice_summary)


print("\n===== EXTREME POSITIVE QUANTITY RECORDS =====")

print(
    df.loc[
        df["Quantity"] > 10000,
        ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]
    ]
    .sort_values("Quantity", ascending=False)
    .head(10)
)


print("\n===== EXTREME POSITIVE PRICE RECORDS =====")

print(
    df.loc[
        df["UnitPrice"] > 1000,
        ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]
    ]
    .sort_values("UnitPrice", ascending=False)
    .head(10)
)

print("\n===== NEGATIVE QUANTITY ON NORMAL INVOICES =====")

negative_normal = negative_quantity & ~cancelled_invoice

print(
    df.loc[
        negative_normal,
        ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]
    ].head(20)
)

print("\nDescriptions in negative normal invoices:")
print(
    df.loc[negative_normal, "Description"]
    .value_counts(dropna=False)
    .head(20)
)


print("\n===== NON-POSITIVE PRICE DESCRIPTIONS =====")

print(
    df.loc[
        non_positive_price,
        ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]
    ]
    .sort_values("UnitPrice")
    .head(30)
)

print("\nMost common descriptions with non-positive price:")
print(
    df.loc[non_positive_price, "Description"]
    .value_counts(dropna=False)
    .head(20)
)


print("\n===== SPECIAL STOCK CODES =====")

special_codes = (
    df.loc[non_positive_price, "StockCode"]
    .value_counts()
    .head(20)
)

print(special_codes)

print("\n===== FINAL CLEANING CHECKS =====")

print(
    "Negative quantity + normal invoice + positive price:",
    (negative_normal & (df["UnitPrice"] > 0)).sum()
)

print(
    "Negative quantity + normal invoice + zero price:",
    (negative_normal & (df["UnitPrice"] == 0)).sum()
)

print(
    "Positive quantity + zero price:",
    ((df["Quantity"] > 0) & (df["UnitPrice"] == 0)).sum()
)

print(
    "Negative quantity + positive price:",
    ((df["Quantity"] < 0) & (df["UnitPrice"] > 0)).sum()
)