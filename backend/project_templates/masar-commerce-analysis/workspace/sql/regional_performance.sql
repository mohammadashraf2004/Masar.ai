-- Result: one row per region
--   region, customers, orders, revenue, aov

SELECT
    region,
    COUNT(*) AS registered_customers
FROM customers
GROUP BY region;
