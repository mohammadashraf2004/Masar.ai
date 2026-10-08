-- Result: one row per month, in calendar order
--   month ('2025-01' or a date), revenue, orders

SELECT
    order_date,
    status
FROM orders
LIMIT 10;
