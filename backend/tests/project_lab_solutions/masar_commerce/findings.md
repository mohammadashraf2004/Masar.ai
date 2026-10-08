# Analysis Findings

## Data quality

The exports repeat some orders and order lines exactly, which would double-count revenue after a join. Some
customers have no city and some country names have stray spaces or the wrong case, which would split one country
into several groups. Only completed orders are revenue, so the other statuses must be excluded.

## SQL findings

Electronics brings in far more revenue than any other category, and Books very little. Revenue climbed through the
year with a clear peak late in the year after a quiet start. The top customers each spend far more than the typical
buyer. Two products never sold at all. Egypt and the Gulf bring in most of the revenue, and Gulf orders are larger.

## Customers

Value is fairly concentrated: the best tenth of buyers bring in about a third of revenue. Just over half of buyers
ordered more than once, so retention is the biggest lever. Business customers place much larger orders than
consumers, although consumers bring in most of the money.

## Products

Electronics and Home & Kitchen carry the business; Fashion is sold with the deepest discounts. The five best-selling
products alone bring in almost half of revenue, which is a real stock risk. Premium products earn the most revenue
even though they are a small part of the catalogue.

## Trends and regions

The second half of the year grew strongly over the first, helped by a November peak. Egypt is the largest region by
revenue, but a Gulf customer is worth more than a customer anywhere else, so the Gulf deserves more marketing even
though it is not the biggest region today.

## Chart takeaways

- The monthly chart shows a slow start, a summer dip and a strong end of year.
- The category chart shows how much the business depends on Electronics.
- The regional chart shows that Egypt and the Gulf together bring in most of the revenue.
