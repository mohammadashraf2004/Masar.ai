WITH o AS (SELECT DISTINCT * FROM orders),
     i AS (SELECT DISTINCT * FROM order_items)
SELECT c.region,
       COUNT(DISTINCT o.customer_id) AS customers,
       COUNT(DISTINCT o.order_id) AS orders,
       SUM(i.quantity * i.unit_price) AS revenue,
       SUM(i.quantity * i.unit_price) / COUNT(DISTINCT o.order_id) AS aov
FROM i
JOIN o ON o.order_id = i.order_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.region;
