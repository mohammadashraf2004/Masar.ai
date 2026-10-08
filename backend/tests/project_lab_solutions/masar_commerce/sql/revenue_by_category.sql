WITH o AS (SELECT DISTINCT * FROM orders),
     i AS (SELECT DISTINCT * FROM order_items)
SELECT p.category, SUM(i.quantity * i.unit_price) AS revenue
FROM i
JOIN o ON o.order_id = i.order_id
JOIN products AS p ON p.product_id = i.product_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;
