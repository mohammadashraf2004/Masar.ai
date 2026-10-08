-- Result: one row per band (budget < 500 <= mid < 1500 <= premium, on list_price)
--   price_band, products, units_sold, revenue

SELECT
    product_id,
    list_price
FROM products
LIMIT 10;
