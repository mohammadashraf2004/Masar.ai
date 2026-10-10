"""COURSE-017 Applied SQL for Data Analysis: guided SQL exercises.

Queries run against a fresh in-memory SQLite fixture; the result decides,
the blanks only point at the field to fix.
"""
from . import Guided

EXERCISES = {
    "COURSE-017.M01.L02.EX02": Guided(
        goal=("Repair four kinds of messy data in one query - inconsistent labels, prices stored as text, a placeholder date and orders whose customer is missing - without inventing values.",
              "أصلح أربعة أنواع من البيانات الفوضوية في استعلام واحد - تسميات غير متسقة، وأسعار مخزّنة نصوصًا، وتاريخ بديل، وطلبات عميلها مفقود - دون اختلاق قيم."),
        steps=(
            ("Standardize the known gender variants and keep unknown values as they are.", "وحّد صيغ الجنس المعروفة واترك القيم غير المعروفة كما هي."),
            ("Convert the price text to a number.", "حوّل نص السعر إلى رقم."),
            ("Turn the placeholder date back into NULL.", "أعد التاريخ البديل إلى NULL."),
            ("Flag orders whose customer record is missing.", "أشِر إلى الطلبات التي سجل عميلها مفقود."),
            ("Keep those orders in the result.", "احتفظ بتلك الطلبات في النتيجة."),
        ),
        starter='''-- customers(customer_id, gender, signup_date)    orders(order_id, customer_id, price_text)
SELECT o.order_id,
       o.customer_id,
       -- Step 1: 'F', 'female' and 'femme' all mean F; anything else (including NULL) stays unchanged
       CASE WHEN LOWER(c.gender) IN (___) THEN 'F' ELSE c.gender END AS gender_clean,
       -- Step 2: prices look like '$19.99' - remove the character that stops the cast
       CAST(REPLACE(o.price_text, ___, '') AS REAL) AS price,
       -- Step 3: 1970-01-01 was loaded for "unknown", so it must not look like a real date
       NULLIF(c.signup_date, ___) AS signup_date,
       -- Step 4: no matching customer row means every customer column is NULL
       CASE WHEN ___ THEN 'missing customer' ELSE 'ok' END AS customer_check
FROM orders AS o
-- Step 5: keep every order, even without a matching customer
___ JOIN customers AS c ON c.customer_id = o.customer_id
ORDER BY o.order_id;
''',
        answers=("'f', 'female', 'femme'", "'$'", "'1970-01-01'", "c.customer_id IS NULL", "LEFT"),
        alternatives={
            1: ("'f','femme','female'", "'female', 'f', 'femme'", "'female', 'femme', 'f'", "'femme', 'f', 'female'", "'femme', 'female', 'f'"),
            5: ("LEFT OUTER",),
        },
        blanks=(
            ("list the lowercase variants `'f', 'female', 'femme'`.", "اذكر الصيغ بالأحرف الصغيرة `'f', 'female', 'femme'`."),
            ("remove `'$'`.", "احذف `'$'`."),
            ("the placeholder `'1970-01-01'`.", "القيمة البديلة `'1970-01-01'`."),
            ("`c.customer_id IS NULL`.", "`c.customer_id IS NULL`."),
            ("a `LEFT` join keeps unmatched orders.", "تحتفظ `LEFT` بالطلبات غير المطابقة."),
        ),
        sql_setup='''CREATE TABLE customers(customer_id INTEGER, gender TEXT, signup_date TEXT);
INSERT INTO customers VALUES
(1,'F','2025-03-01'),(2,'female','1970-01-01'),(3,'femme','2025-06-10'),(4,NULL,'2025-07-04'),(5,'M','2025-08-15');
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, price_text TEXT);
INSERT INTO orders VALUES
(101,1,'$19.99'),(102,2,'$5.00'),(103,3,'$120.50'),(104,4,'$7.25'),(105,5,'$40'),(106,9,'$12.00');''',
        sql_columns=("order_id", "customer_id", "gender_clean", "price", "signup_date", "customer_check"),
        sql_rows=(
            (101, 1, "F", 19.99, "2025-03-01", "ok"),
            (102, 2, "F", 5.0, None, "ok"),
            (103, 3, "F", 120.5, "2025-06-10", "ok"),
            (104, 4, None, 7.25, "2025-07-04", "ok"),
            (105, 5, "M", 40.0, "2025-08-15", "ok"),
            (106, 9, None, 12.0, None, "missing customer"),
        ),
        hints=(
            ("Compare `LOWER(gender)` so 'F' and 'f' are treated alike; the ELSE branch keeps unknown values.", "قارن `LOWER(gender)` لتُعامل 'F' و'f' بالطريقة نفسها؛ ويحتفظ فرع ELSE بالقيم غير المعروفة."),
            ("`NULLIF(value, placeholder)` returns NULL when the two are equal.", "تعيد `NULLIF(value, placeholder)` القيمة NULL عندما تتساوى القيمتان."),
            ("After a LEFT JOIN, an unmatched row has NULL in the joined table's key.", "بعد LEFT JOIN يحمل الصف غير المطابق NULL في مفتاح الجدول المضموم."),
        ),
        success=("Correct! Each fix is explicit and reversible: known variants are mapped, unknown values are kept, the placeholder is honest NULL, and the orphan order is flagged instead of dropped.",
                 "صحيح! كل إصلاح صريح وقابل للتراجع: رُبطت الصيغ المعروفة، وبقيت القيم غير المعروفة، وصار التاريخ البديل NULL صادقة، ووُسم الطلب اليتيم بدل حذفه."),
        reflect=("Label each issue as a type, value-standardization, placeholder or missing-related-record problem. Which ones should be fixed upstream?",
                 "صنّف كل مشكلة: مشكلة نوع، أو توحيد قيم، أو قيمة بديلة، أو سجل مرتبط مفقود. وأيها يجب إصلاحه من المصدر؟"),
        language="sql",
    ),
    "COURSE-017.M01.L05.EX01": Guided(
        goal=("Turn an overstuffed support field into four clean columns and flag the rows that are missing a label.",
              "حوّل حقل دعم محشوًّا بالمعلومات إلى أربعة أعمدة نظيفة، وأشِر إلى الصفوف التي ينقصها أحد العناوين."),
        steps=(
            ("Find where the Product field starts.", "حدّد أين يبدأ الحقل Product."),
            ("Convert the opened text to a date.", "حوّل نص الفتح إلى تاريخ."),
            ("Trim the spaces around the product.", "احذف المسافات حول اسم المنتج."),
            ("Standardize the priority's case.", "وحّد حالة الأحرف في الأولوية."),
            ("Flag rows without a Priority label.", "أشِر إلى الصفوف التي ليس فيها العنوان Priority."),
        ),
        starter='''-- tickets(ticket_id, details), e.g.
-- 'Opened: 2026-04-03 | Product: Mobile App | Issue: Login | Priority: High'
WITH fields AS (
    -- The text after each label. A missing label gives NULL, and ' |' is appended
    -- so the last field also ends with a delimiter.
    SELECT ticket_id,
           details,
           SUBSTR(details || ' |', NULLIF(INSTR(details, 'Opened:'), 0) + LENGTH('Opened:'))     AS opened_rest,
           -- Step 1: the label that starts the product field
           SUBSTR(details || ' |', NULLIF(INSTR(details, ___), 0) + LENGTH('Product:'))          AS product_rest,
           SUBSTR(details || ' |', NULLIF(INSTR(details, 'Issue:'), 0) + LENGTH('Issue:'))       AS issue_rest,
           SUBSTR(details || ' |', NULLIF(INSTR(details, 'Priority:'), 0) + LENGTH('Priority:')) AS priority_rest
    FROM tickets
)
SELECT ticket_id,
       -- Step 2: cut at the first '|', trim, and turn the text into a date
       ___(TRIM(SUBSTR(opened_rest, 1, INSTR(opened_rest, '|') - 1))) AS opened_date,
       -- Step 3: cut at the first '|' and remove the surrounding spaces
       ___(SUBSTR(product_rest, 1, INSTR(product_rest, '|') - 1)) AS product,
       TRIM(SUBSTR(issue_rest, 1, INSTR(issue_rest, '|') - 1)) AS issue,
       -- Step 4: 'High', 'HIGH' and 'high' must become one value
       ___(TRIM(SUBSTR(priority_rest, 1, INSTR(priority_rest, '|') - 1))) AS priority,
       -- Step 5: a label that is not found has position 0
       CASE WHEN INSTR(details, 'Opened:') = 0 OR INSTR(details, 'Product:') = 0
              OR INSTR(details, 'Issue:') = 0 OR ___
            THEN 'malformed' ELSE 'ok' END AS parse_check
FROM fields
ORDER BY ticket_id;
''',
        answers=("'Product:'", "DATE", "TRIM", "LOWER", "INSTR(details, 'Priority:') = 0"),
        alternatives={5: ("INSTR(details,'Priority:')=0", "priority_rest IS NULL")},
        blanks=(
            ("search for the label `'Product:'`.", "ابحث عن العنوان `'Product:'`."),
            ("wrap the text in `DATE(...)`.", "ضع النص داخل `DATE(...)`."),
            ("wrap the product in `TRIM(...)`.", "ضع المنتج داخل `TRIM(...)`."),
            ("wrap the priority in `LOWER(...)`.", "ضع الأولوية داخل `LOWER(...)`."),
            ("`INSTR(details, 'Priority:') = 0`.", "`INSTR(details, 'Priority:') = 0`."),
        ),
        sql_setup='''CREATE TABLE tickets(ticket_id INTEGER, details TEXT);
INSERT INTO tickets VALUES
(1,'Opened: 2026-04-03 | Product: Mobile App | Issue: Login | Priority: High'),
(2,'Opened: 2026-04-04 |Product:  Web Portal| Issue: Billing | Priority: LOW'),
(3,'Opened: 2026-04-05 | Product: Mobile App | Issue: Crash');''',
        sql_columns=("ticket_id", "opened_date", "product", "issue", "priority", "parse_check"),
        sql_rows=(
            (1, "2026-04-03", "Mobile App", "Login", "high", "ok"),
            (2, "2026-04-04", "Web Portal", "Billing", "low", "ok"),
            (3, "2026-04-05", "Mobile App", "Crash", None, "malformed"),
        ),
        hints=(
            ("Every field follows the same pattern: find the label, take the text after it, cut at the next '|'.", "يتبع كل حقل النمط نفسه: جد العنوان، وخذ النص بعده، واقطع عند أول '|' تالٍ."),
            ("`TRIM` removes spaces at both ends; `LOWER` gives one spelling per value.", "تحذف `TRIM` المسافات من الطرفين، وتعطي `LOWER` كتابة واحدة لكل قيمة."),
            ("`INSTR(text, label)` returns 0 when the label is absent.", "تعيد `INSTR(text, label)` القيمة 0 عندما يغيب العنوان."),
        ),
        success=("Correct! Inconsistent spacing and case no longer split one product or priority into several values, and the ticket without a priority is flagged rather than silently parsed as garbage.",
                 "صحيح! لم تعد المسافات وحالة الأحرف غير المتسقة تقسم المنتج أو الأولوية الواحدة إلى عدة قيم، ووُسمت التذكرة التي بلا أولوية بدل تحليلها بصمت إلى قيم عشوائية."),
        expected=("SQLite has no split_part; INSTR and SUBSTR do the same delimiter-based parsing. In PostgreSQL you would write `TRIM(split_part(details, '|', 2))`.",
                  "لا يملك SQLite الدالة split_part؛ وتؤدي INSTR وSUBSTR التحليل نفسه القائم على الفواصل. وفي PostgreSQL تكتب `TRIM(split_part(details, '|', 2))`."),
        reflect=("Why is splitting on a label safer than splitting on position when a field can be missing?",
                 "لماذا يكون التقسيم بالاعتماد على العنوان أكثر أمانًا من التقسيم حسب الموضع عندما قد يغيب حقل ما؟"),
        language="sql",
    ),
    "COURSE-017.M01.L08.EX01": Guided(
        goal=("Refactor a tangled customer query into named CTEs - one per metric - joined into one row per customer.",
              "أعد هيكلة استعلام عملاء متشابك إلى CTEs مسمّاة - واحد لكل مقياس - تُضم في صف واحد لكل عميل."),
        steps=(
            ("Compute each customer's first order date.", "احسب تاريخ أول طلب لكل عميل."),
            ("Compute lifetime revenue, net of refunds.", "احسب الإيراد مدى الحياة بعد خصم المبالغ المستردة."),
            ("Pick the plan with the latest start date.", "اختر الخطة ذات أحدث تاريخ بدء."),
            ("Keep customers who have no tracked activity.", "احتفظ بالعملاء الذين ليس لهم نشاط مسجّل."),
        ),
        starter='''-- orders(order_id, customer_id, order_date, amount)  events(customer_id, event_date)
-- subscriptions(customer_id, plan, started_on)
-- Final grain: one row per customer who has ordered.
WITH first_orders AS (
    -- Step 1: the earliest order per customer
    SELECT customer_id, ___ AS first_order_date
    FROM orders
    GROUP BY customer_id
),
revenue AS (
    -- Step 2: assumption - refunds are stored as negative amounts, so a plain total nets them out
    SELECT customer_id, ___ AS lifetime_revenue
    FROM orders
    GROUP BY customer_id
),
last_activity AS (
    SELECT customer_id, MAX(event_date) AS last_activity_date
    FROM events
    GROUP BY customer_id
),
current_plan AS (
    -- Step 3: assumption - the plan with the latest start date is the current one
    SELECT s.customer_id, s.plan AS current_plan
    FROM subscriptions AS s
    WHERE s.started_on = (SELECT ___ FROM subscriptions AS later WHERE later.customer_id = s.customer_id)
)
SELECT f.customer_id, f.first_order_date, r.lifetime_revenue, a.last_activity_date, p.current_plan
FROM first_orders AS f
JOIN revenue AS r ON r.customer_id = f.customer_id
-- Step 4: a customer without events must not disappear from the data set
___ JOIN last_activity AS a ON a.customer_id = f.customer_id
LEFT JOIN current_plan AS p ON p.customer_id = f.customer_id
ORDER BY f.customer_id;
''',
        answers=("MIN(order_date)", "SUM(amount)", "MAX(later.started_on)", "LEFT"),
        alternatives={3: ("MAX(started_on)",), 4: ("LEFT OUTER",)},
        blanks=(
            ("`MIN(order_date)`.", "`MIN(order_date)`."),
            ("`SUM(amount)`.", "`SUM(amount)`."),
            ("`MAX(later.started_on)`.", "`MAX(later.started_on)`."),
            ("a `LEFT` join keeps customers without events.", "تحتفظ `LEFT` بالعملاء الذين ليست لهم أحداث."),
        ),
        sql_setup='''CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
(1,1,'2026-01-05',50),(2,1,'2026-02-10',30),(3,1,'2026-03-01',-10),(4,2,'2026-02-20',80),(5,3,'2026-03-15',25);
CREATE TABLE events(customer_id INTEGER, event_date TEXT);
INSERT INTO events VALUES (1,'2026-03-20'),(1,'2026-04-02'),(2,'2026-03-01');
CREATE TABLE subscriptions(customer_id INTEGER, plan TEXT, started_on TEXT);
INSERT INTO subscriptions VALUES (1,'basic','2026-01-05'),(1,'pro','2026-03-01'),(2,'basic','2026-02-20');''',
        sql_columns=("customer_id", "first_order_date", "lifetime_revenue", "last_activity_date", "current_plan"),
        sql_rows=(
            (1, "2026-01-05", 70, "2026-04-02", "pro"),
            (2, "2026-02-20", 80, "2026-03-01", "basic"),
            (3, "2026-03-15", 25, None, None),
        ),
        hints=(
            ("Each CTE has the same grain: one row per customer, thanks to GROUP BY customer_id.", "لكل CTE مستوى التفصيل نفسه: صف واحد لكل عميل، بفضل GROUP BY customer_id."),
            ("ISO dates compare correctly as text, so MIN and MAX work on them.", "تُقارن تواريخ ISO بشكل صحيح بوصفها نصوصًا، لذا تعمل عليها MIN وMAX."),
            ("An inner JOIN drops a customer that has no row in last_activity.", "تحذف JOIN الداخلية العميل الذي ليس له صف في last_activity."),
        ),
        success=("Correct! Each metric lives in its own named, testable CTE at customer grain, the assumptions are written down, and LEFT JOINs keep customer 3 even without activity or a plan.",
                 "صحيح! يعيش كل مقياس في CTE مسمّى خاص به وقابل للاختبار على مستوى العميل، والافتراضات مكتوبة، وتحتفظ LEFT JOIN بالعميل 3 رغم غياب النشاط والخطة."),
        reflect=("When would you materialize these steps as a temp table or move them into ETL instead of keeping CTEs?",
                 "متى ستحفظ هذه الخطوات في جدول مؤقت أو تنقلها إلى ETL بدل إبقائها CTEs؟"),
        language="sql",
    ),
}
