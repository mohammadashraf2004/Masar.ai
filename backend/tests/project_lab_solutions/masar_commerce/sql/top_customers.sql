WITH o AS (SELECT DISTINCT * FROM orders),
     i AS (SELECT DISTINCT * FROM order_items)
SELECT o.customer_id, SUM(i.quantity * i.unit_price) AS revenue, COUNT(DISTINCT o.order_id) AS orders
FROM i JOIN o ON o.order_id = i.order_id
WHERE o.status = 'completed'
GROUP BY o.customer_id
ORDER BY revenue DESC
LIMIT 10;
