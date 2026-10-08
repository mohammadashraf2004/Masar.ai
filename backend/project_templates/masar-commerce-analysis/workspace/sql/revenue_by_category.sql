-- Result: one row per category
--   category, revenue
-- Tables (raw exports): customers, orders, order_items, products

SELECT
    p.category,
    COUNT(*) AS order_lines
FROM order_items AS oi
JOIN products AS p ON p.product_id = oi.product_id
GROUP BY p.category;
