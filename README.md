# Online Retail Data Engineering

An end-to-end data engineering project built using the **Online Retail dataset** to transform raw retail transactions into clean, structured and analysis-ready data.

## 📌 Project Overview

The project follows a complete data pipeline:

**Raw Excel Data → Python Cleaning → PostgreSQL Data Warehouse → SQL Analysis → Power BI Dashboard**

The main goal was to understand how raw transactional data can be processed and converted into useful business insights.

## 🛠️ Technologies Used

- **Python** – Data inspection, cleaning, transformation and validation
- **Pandas & OpenPyXL** – Data processing and Excel handling
- **PostgreSQL** – Database and data warehouse
- **SQL** – Business analysis and KPI calculations
- **Power BI** – Interactive dashboard and visualization
- **Git & GitHub** – Version control and project management

## 🔄 Project Workflow

### 1. Data Inspection
The raw Excel dataset was first explored to understand its structure, missing values, duplicates, cancellations and invalid records.

### 2. Data Cleaning
Python was used to:
- Remove duplicate records
- Remove cancelled transactions
- Remove invalid/non-positive prices
- Handle missing product descriptions
- Retain missing customer IDs as **Unknown Customer**
- Calculate transaction-level revenue

The cleaned data was then saved as a processed CSV file.

### 3. Data Validation
The cleaned dataset was validated for duplicates, cancelled invoices, negative quantities, invalid prices, missing values and revenue consistency.

### 4. PostgreSQL Data Warehouse
The cleaned data was loaded into PostgreSQL using a simple **star schema**:

- `dim_customer`
- `dim_product`
- `dim_date`
- `fact_sales`

The `fact_sales` table stores transaction-level sales, while the dimension tables provide customer, product and date information.

### 5. SQL Analysis
SQL queries were created to analyze:

- Total Revenue
- Total Orders
- Total Customers
- Total Products
- Monthly Revenue
- Monthly Orders
- Top Products
- Revenue by Country
- Average Order Value
- Top Customers

### 6. Power BI Dashboard
The PostgreSQL warehouse was connected to Power BI to create an interactive sales dashboard with KPIs, filters and visualizations.

### 📊 Dashboard

![Online Retail Sales Dashboard](screenshots/powerbi_dashboard.png)

## 📁 Project Structure

```text
Online-Retail-Data-Engineering/
│
├── screenshots/
├── sql/
│   └── analysis.sql
├── src/
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── validate_data.py
│   └── load_data.py
├── tests/
├── .gitignore
├── Data-Engineering_Mini-Project-Dashboard.pbix
└── README.md
