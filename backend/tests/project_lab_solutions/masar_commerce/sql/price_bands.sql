WITH o AS (SELECT DISTINCT * FROM orders),
     i AS (SELECT DISTINCT * FROM order_items),
     banded AS (
         SELECT product_id,
                CASE WHEN list_price < 500 THEN 'budget'
                     WHEN list_price < 1500 THEN 'mid'
                     ELSE 'premium' END AS price_band
         FROM products),
     sales_by_product AS (
         SELECT i.product_id, SUM(i.quantity) AS units_sold, SUM(i.quantity * i.unit_price) AS revenue
         FROM i JOIN o ON o.order_id = i.order_id
         WHERE o.status = 'completed'
         GROUP BY i.product_id)
SELECT b.price_band, COUNT(*) AS products,
       COALESCE(SUM(s.units_sold), 0) AS units_sold, COALESCE(SUM(s.revenue), 0) AS revenue
FROM banded AS b
LEFT JOIN sales_by_product AS s USING (product_id)
GROUP BY b.price_band;
