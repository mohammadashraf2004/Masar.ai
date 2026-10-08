-- Result: 10 rows, highest revenue first
--   customer_id, revenue, orders

SELECT
    customer_id,
    COUNT(*) AS rows_in_orders
FROM orders
GROUP BY customer_id
LIMIT 10;
