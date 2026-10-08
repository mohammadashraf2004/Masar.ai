WITH o AS (SELECT DISTINCT * FROM orders),
     i AS (SELECT DISTINCT * FROM order_items),
     sales_by_product AS (
         SELECT i.product_id, SUM(i.quantity) AS units_sold, SUM(i.quantity * i.unit_price) AS revenue
         FROM i JOIN o ON o.order_id = i.order_id
         WHERE o.status = 'completed'
         GROUP BY i.product_id)
SELECT p.product_id, p.product_name, p.category,
       COALESCE(s.units_sold, 0) AS units_sold, COALESCE(s.revenue, 0) AS revenue
FROM products AS p
LEFT JOIN sales_by_product AS s USING (product_id);
