-- 1. Total Revenue
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_sales;

-- 2. Total Orders
SELECT
    COUNT(DISTINCT invoice_no) AS total_orders
FROM fact_sales;

-- 3. Total Customers
SELECT
    COUNT(DISTINCT customer_id) AS total_customers
FROM dim_customer
WHERE customer_id IS NOT NULL;

-- 4. Total Products
SELECT
    COUNT(DISTINCT stock_code) AS total_products
FROM dim_product;

-- 5. Monthly Revenue
SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.revenue), 2) AS monthly_revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;

    -- 6. Top 10 Products by Revenue
SELECT
    p.stock_code,
    p.description,
    ROUND(SUM(f.revenue), 2) AS total_revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.stock_code,
    p.description
ORDER BY
    total_revenue DESC
LIMIT 10;

-- 7. Revenue by Country
SELECT
    c.country,
    ROUND(SUM(f.revenue), 2) AS total_revenue
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY
    c.country
ORDER BY
    total_revenue DESC;

    -- 8. Average Order Value
SELECT
    ROUND(
        SUM(revenue) / COUNT(DISTINCT invoice_no),
        2
    ) AS average_order_value
FROM fact_sales;

-- 9. Top 10 Customers by Revenue
SELECT
    c.customer_id,
    c.country,
    ROUND(SUM(f.revenue), 2) AS total_revenue
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
WHERE c.customer_id IS NOT NULL
GROUP BY
    c.customer_id,
    c.country
ORDER BY
    total_revenue DESC
LIMIT 10;

-- 10. Monthly Orders
SELECT
    d.year,
    d.month,
    d.month_name,
    COUNT(DISTINCT f.invoice_no) AS total_orders
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;