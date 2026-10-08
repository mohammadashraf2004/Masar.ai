"""Masar Commerce — Business Performance Analysis (Data Analyst capstone).

The reference capstone for Masar tracks: one business investigation in ten
milestones, from the brief to the executive report. Guidance tapers on
purpose:

  M1–M2  guided      — steps spelled out; learn to read the brief and the data
  M3–M4  moderate    — the goal and the output are given; the method is yours
  M5–M7  reduced     — the business question and the output contract only
  M8–M9  independent — choose the approach, then interpret what you found
  M10    synthesis   — requirements only; the conclusions are the learner's

SQL answers the core business questions (M4, price bands in M7); Python does
inspection, cleaning, KPIs and the deeper analyses SQL would make awkward
(concentration, growth, per-customer value, charts). No metric is computed
twice as a task. A running findings.md log records what each part of the
analysis means; the executive report (M10) is synthesised from it.

Every data task is checked by a private validator in
app/services/project_lab/validators/masar_commerce.py against results
computed from the data — and again on a hidden variant of it; markdown tasks
by validators/common.py. `validator_config` is server-side only. Hints are
authored, static and free: hint 1 the concept, hint 2 the fields and
relationships, hint 3 the implementation direction — never a finished query
or script, never a number.

Task slugs are permanent: learner progress is keyed on them.
"""

PLAN = "analysis_plan.md"
FINDINGS = "findings.md"
REPORT = "report.md"
INSPECT = "analysis/inspect_data.py"
CLEAN = "analysis/clean_data.py"
KPIS = "analysis/kpis.py"
CUSTOMERS = "analysis/customers.py"
PRODUCTS = "analysis/products.py"
TRENDS = "analysis/trends.py"
VISUALIZE = "analysis/visualize.py"


def hints(*pairs: tuple[str, str]) -> list[dict[str, str]]:
    return [{"en": en, "ar": ar} for en, ar in pairs]


def skill(en: str, ar: str) -> dict[str, str]:
    return {"en": en, "ar": ar}


def insight(heading: str, heading_ar: str, *, min_words: int = 0, min_items: int = 0) -> dict:
    """A findings.md section the task also asks for (presence and length only)."""
    spec: dict = {"heading": heading, "aliases": [heading_ar]}
    if min_words:
        spec["min_words"] = min_words
    if min_items:
        spec["min_items"] = min_items
    return spec


# Validated skill areas (shown on completion; reused later by portfolio/certificates).
SQL_ANALYSIS = skill("SQL Business Analysis", "تحليل الأعمال باستخدام SQL")
CLEANING = skill("Data Cleaning", "تنظيف البيانات")
PANDAS = skill("Pandas", "Pandas")
KPI = skill("KPI Analysis", "تحليل مؤشرات الأداء (KPI)")
CUSTOMER = skill("Customer Analysis", "تحليل العملاء")
PRODUCT = skill("Product Analysis", "تحليل المنتجات")
TIME_SERIES = skill("Time-Series Analysis", "تحليل السلاسل الزمنية")
VISUAL = skill("Data Visualization", "التمثيل المرئي للبيانات")
REPORTING = skill("Business Reporting", "إعداد تقارير الأعمال")

REPORT_SECTIONS = [
    {"heading": "Executive Summary", "aliases": ["الملخص التنفيذي"], "min_words": 40},
    {"heading": "Business Performance", "aliases": ["أداء الأعمال"], "min_words": 30},
    {"heading": "Customer Insights", "aliases": ["رؤى العملاء"], "min_words": 30},
    {"heading": "Product Insights", "aliases": ["رؤى المنتجات"], "min_words": 30},
    {"heading": "Regional and Time Trends", "aliases": ["الاتجاهات الإقليمية والزمنية"], "min_words": 30},
    {"heading": "Key Risks", "aliases": ["المخاطر الرئيسية"], "min_words": 20, "min_items": 2},
    {"heading": "Recommendations", "aliases": ["التوصيات"], "min_words": 30, "min_items": 3},
]


# ─── M1 — Business Brief (guided) ────────────────────────────────────────────

M1 = {
    "slug": "business-brief",
    "title": "Business Brief",
    "title_ar": "موجز العمل",
    "summary": "Understand the company, who needs the analysis, and what exactly will be measured.",
    "summary_ar": "افهم الشركة، ومن يحتاج إلى التحليل، وما الذي سيُقاس بالضبط.",
    "skills": [REPORTING],
    "tasks": [
        {
            "slug": "frame-the-brief",
            "title": "Frame the brief",
            "title_ar": "صِغ موجز التحليل",
            "primary_file": PLAN,
            "instructions": (
                "**Business question:** what is this analysis for, and who will use it?\n\n"
                "You have just joined Masar Commerce as a junior Data Analyst. Before touching data, a good analyst "
                "makes sure they understand the request and the people behind it.\n\n"
                "1. Read **README.md**: the company, management's six questions, the data dictionary and the "
                "business rules.\n"
                "2. In **analysis_plan.md**, under **Objective**, write two or three sentences in your own words: "
                "what this analysis will find out, and which decisions it supports.\n"
                "3. Under **Stakeholders**, write one line for each person named in the README: who they are and "
                "what they need from your work. They do not all need the same thing.\n"
                "4. Save, then press **Check Step**.\n\n"
                "The check confirms both sections are written in your own words (template lines never count); it "
                "does not judge your wording."
            ),
            "instructions_ar": (
                "**سؤال العمل:** ما الغرض من هذا التحليل، ومن سيستخدمه؟\n\n"
                "انضممت للتو إلى مسار كوميرس بصفتك محلّل بيانات مبتدئًا. قبل أن يلمس المحلّل الجيد البيانات، يتأكد من "
                "فهمه للطلب وللأشخاص الذين يقفون خلفه.\n\n"
                "1. اقرأ **README.ar.md**: الشركة، وأسئلة الإدارة الستة، وقاموس البيانات، وقواعد العمل.\n"
                "2. في **analysis_plan.md**، تحت **Objective** («الهدف»)، اكتب جملتين أو ثلاثًا بكلماتك: ماذا "
                "سيكتشف هذا التحليل، وأي قرارات يدعمها.\n"
                "3. تحت **Stakeholders** («أصحاب المصلحة»)، اكتب سطرًا لكل شخص مذكور في الموجز: من هو وماذا يحتاج "
                "من عملك. لا يحتاجون جميعًا إلى الشيء نفسه.\n"
                "4. احفظ الملف ثم اضغط **تحقق من الخطوة**.\n\n"
                "يتأكد الفحص من أن القسمين مكتوبان بكلماتك (أسطر القالب لا تُحتسب)، ولا يحكم على صياغتك."
            ),
            "hints": hints(
                ("A brief answers two things: what decision the work supports, and for whom.",
                 "الموجز يجيب عن أمرين: أي قرار يدعمه العمل، ولمن."),
                ("Management's six questions and the three stakeholders are near the top of the README; each "
                 "stakeholder owns a different decision (strategy, sales targets, customer campaigns).",
                 "أسئلة الإدارة الستة وأصحاب المصلحة الثلاثة في أعلى الموجز؛ ويملك كل منهم قرارًا مختلفًا "
                 "(الاستراتيجية، أهداف المبيعات، حملات العملاء)."),
                ("Write the objective as “Explain … in 2025 so that management can decide …”, then give each "
                 "stakeholder a bullet in the form “- Role: needs … to decide …”.",
                 "اكتب الهدف بصيغة «شرح … في 2025 لكي تقرر الإدارة …»، ثم خصّص لكل صاحب مصلحة نقطة بصيغة "
                 "«- الدور: يحتاج … ليقرر …»."),
            ),
            "validator_key": "common.markdown_sections",
            "validator_config": {"file": PLAN, "sections": [
                {"heading": "Objective", "aliases": ["الهدف"], "min_words": 15},
                {"heading": "Stakeholders", "aliases": ["أصحاب المصلحة"], "min_words": 20, "min_items": 3},
            ]},
        },
        {
            "slug": "plan-questions-and-kpis",
            "title": "Plan the questions and KPIs",
            "title_ar": "خطّط الأسئلة ومؤشرات الأداء",
            "primary_file": PLAN,
            "instructions": (
                "**Business question:** what exactly will you measure?\n\n"
                "Teams argue about numbers when they define them differently. Write your definitions down before "
                "you calculate anything — the rest of the project holds you to them.\n\n"
                "1. Under **Business questions**, list at least four questions your analysis will answer, one per "
                "line starting with `-`.\n"
                "2. Under **KPI definitions**, define the KPIs you will report. Your definitions must say:\n"
                "   - which orders count as recognised revenue;\n"
                "   - how the revenue of one order line is calculated;\n"
                "   - what average order value (AOV) means.\n"
                "3. Save, then press **Check Step**."
            ),
            "instructions_ar": (
                "**سؤال العمل:** ماذا ستقيس بالضبط؟\n\n"
                "تختلف الفرق على الأرقام حين تعرّفها بطرق مختلفة. اكتب تعريفاتك قبل أن تحسب أي شيء — فبقية المشروع "
                "تلتزم بها.\n\n"
                "1. تحت **Business questions** («أسئلة العمل») اكتب أربعة أسئلة على الأقل سيجيب عنها تحليلك، كل "
                "سؤال في سطر يبدأ بـ `-`.\n"
                "2. تحت **KPI definitions** («تعريفات مؤشرات الأداء») عرّف مؤشرات الأداء التي ستعرضها، على أن "
                "توضح تعريفاتك:\n"
                "   - أي الطلبات تُحتسب إيرادات معترفًا بها؛\n"
                "   - كيف تُحسب إيرادات سطر الطلب الواحد؛\n"
                "   - ما معنى متوسط قيمة الطلب (AOV).\n"
                "3. احفظ الملف ثم اضغط **تحقق من الخطوة**."
            ),
            "hints": hints(
                ("Turn each of management's six questions into something you can measure.",
                 "حوّل كل سؤال من أسئلة الإدارة الستة إلى شيء يمكن قياسه."),
                ("The README's business rules say which order status brings in money, and order_items holds the "
                 "price actually charged.",
                 "تحدد قواعد العمل في الموجز أي حالة طلب تجلب المال، ويحمل order_items السعر المدفوع فعلًا."),
                ("Define recognised revenue from the completed status and the order-line price, then define AOV in "
                 "terms of recognised revenue and the number of completed orders.",
                 "عرّف الإيرادات المعترف بها انطلاقًا من الحالة completed وسعر سطر الطلب، ثم عرّف AOV بدلالة "
                 "الإيرادات المعترف بها وعدد الطلبات المكتملة."),
            ),
            "validator_key": "common.markdown_sections",
            "validator_config": {"file": PLAN, "sections": [
                {"heading": "Business questions", "aliases": ["أسئلة العمل"], "min_items": 4},
                {"heading": "KPI definitions", "aliases": ["تعريفات مؤشرات الأداء"], "min_words": 25, "terms": [
                    {"any": ["completed", "مكتمل"],
                     "label": {"en": "Which orders count as revenue", "ar": "أي الطلبات تُحتسب إيرادات"},
                     "message": {"en": "Say which orders count as recognised revenue (see the business rules in README.md).",
                                 "ar": "وضّح أي الطلبات تُحتسب إيرادات معترفًا بها (انظر قواعد العمل في README.ar.md)."}},
                    {"any": ["unit_price", "unit price", "quantity", "سعر الوحدة", "الكمية"],
                     "label": {"en": "How line revenue is calculated", "ar": "كيف تُحسب إيرادات السطر"},
                     "message": {"en": "Explain how the revenue of one order line is calculated from the data.",
                                 "ar": "اشرح كيف تُحسب إيرادات سطر الطلب الواحد من البيانات."}},
                    {"any": ["average order value", "aov", "متوسط قيمة الطلب"],
                     "label": {"en": "Average order value is defined", "ar": "تعريف متوسط قيمة الطلب"},
                     "message": {"en": "Define average order value (AOV).", "ar": "عرّف متوسط قيمة الطلب (AOV)."}},
                ]},
            ]},
        },
    ],
}


# ─── M2 — Understand the Data (guided) ───────────────────────────────────────

M2 = {
    "slug": "understand-the-data",
    "title": "Understand the Data",
    "title_ar": "افهم البيانات",
    "summary": "Profile the four raw exports and find what is wrong with them before trusting any number.",
    "summary_ar": "استكشف ملفات التصدير الأربعة الخام واكتشف ما فيها من مشكلات قبل أن تثق بأي رقم.",
    "skills": [PANDAS],
    "tasks": [
        {
            "slug": "profile-the-tables",
            "title": "Profile the tables",
            "title_ar": "استكشف الجداول",
            "primary_file": INSPECT,
            "instructions": (
                "**Business question:** what data do we actually have, and for which period?\n\n"
                "1. Open **analysis/inspect_data.py** and press **Run**. It prints each table's shape, column types "
                "and first rows. Compare them with the data dictionary and notice how the tables connect.\n"
                "2. Set `row_counts`: a dictionary with the number of rows in each raw file, keyed `customers`, "
                "`orders`, `order_items` and `products` — counted exactly as exported.\n"
                "3. Set `order_date_range`: a list `[first, last]` with the earliest and latest `order_date`, as "
                "`\"YYYY-MM-DD\"` text.\n"
                "4. Run again, then press **Check Step**.\n\n"
                "Compute both from the DataFrames: the check also runs your file on a changed copy of the data."
            ),
            "instructions_ar": (
                "**سؤال العمل:** ما البيانات التي لدينا فعلًا، وعن أي فترة؟\n\n"
                "1. افتح **analysis/inspect_data.py** واضغط **تشغيل**؛ يطبع أبعاد كل جدول وأنواع أعمدته وأول "
                "صفوفه. قارنها بقاموس البيانات ولاحظ كيف ترتبط الجداول.\n"
                "2. عيّن `row_counts`: قاموس بعدد صفوف كل ملف خام، مفاتيحه `customers` و`orders` و`order_items` "
                "و`products` — محسوبة كما صُدِّرت تمامًا.\n"
                "3. عيّن `order_date_range`: قائمة `[first, last]` بأقدم وأحدث `order_date` كنص بصيغة "
                "`\"YYYY-MM-DD\"`.\n"
                "4. شغّل مرة أخرى ثم اضغط **تحقق من الخطوة**.\n\n"
                "احسب القيمتين من جداول DataFrame: فالفحص يشغّل ملفك أيضًا على نسخة معدّلة من البيانات."
            ),
            "hints": hints(
                ("Every DataFrame knows how many rows it has.", "كل DataFrame يعرف عدد صفوفه."),
                ("order_date is text in YYYY-MM-DD form, so its smallest and largest values are the first and last "
                 "dates.",
                 "العمود order_date نص بصيغة YYYY-MM-DD، لذا أصغر قيمه وأكبرها هما أول تاريخ وآخره."),
                ("Use len() (or .shape) on each of the four DataFrames, and the column's min() and max() for the "
                 "date range.",
                 "استخدم len() (أو ‎.shape) على كل جدول من الأربعة، ودالتي min() وmax() على العمود لنطاق التواريخ."),
            ),
            "validator_key": "masar_commerce.profile_tables",
            "validator_config": {"file": INSPECT},
        },
        {
            "slug": "find-quality-issues",
            "title": "Find the data quality issues",
            "title_ar": "اكتشف مشكلات جودة البيانات",
            "primary_file": INSPECT,
            "instructions": (
                "**Business question:** can we trust these exports as they are?\n\n"
                "The data engineering team warned that the exports are not clean. Find the problems and measure "
                "them — still in **analysis/inspect_data.py**, still on the raw data:\n\n"
                "- `duplicate_rows` — `{\"orders\": …, \"order_items\": …}`: how many rows in each file exactly "
                "repeat an earlier row;\n"
                "- `missing_city` — how many customers have no city;\n"
                "- `inconsistent_countries` — how many customer rows have a country that differs from its clean "
                "form (stray spaces, wrong capitalisation).\n\n"
                "Print a few of the problem rows as well: you will fix them in the next milestone."
            ),
            "instructions_ar": (
                "**سؤال العمل:** هل يمكننا الوثوق بملفات التصدير كما هي؟\n\n"
                "حذّر فريق هندسة البيانات من أن ملفات التصدير ليست نظيفة. اكتشف المشكلات وقِسها — في "
                "**analysis/inspect_data.py** نفسه وعلى البيانات الخام:\n\n"
                "- `duplicate_rows` — `{\"orders\": …, \"order_items\": …}`: كم صفًا في كل ملف يكرر صفًا سابقًا "
                "تمامًا؛\n"
                "- `missing_city` — كم عميلًا بلا مدينة؛\n"
                "- `inconsistent_countries` — كم صف عميل يختلف فيه اسم الدولة عن صيغته النظيفة (مسافات زائدة، حالة "
                "أحرف خاطئة).\n\n"
                "اطبع بعض الصفوف المعيبة أيضًا: ستصلحها في المرحلة التالية."
            ),
            "hints": hints(
                ("A duplicate is a row identical to one seen earlier; the first copy is not a duplicate.",
                 "الصف المكرر هو صف مطابق لصف ظهر قبله؛ والنسخة الأولى ليست مكررة."),
                ("pandas can flag repeated rows and missing values. For countries, compare each value with a "
                 "stripped, title-cased version of itself.",
                 "يستطيع pandas تحديد الصفوف المكررة والقيم المفقودة. وللدول، قارن كل قيمة بنسخة منها بعد إزالة "
                 "المسافات وتوحيد حالة الأحرف."),
                ("Count the True values of duplicated() for each file and of isna() for city; for countries, count "
                 "the rows where the original value is not equal to its .str.strip().str.title() form.",
                 "اعدد قيم True في duplicated() لكل ملف وفي isna() للمدينة؛ وللدول اعدد الصفوف التي لا تساوي فيها "
                 "القيمة الأصلية صيغتها بعد ‎.str.strip().str.title()."),
            ),
            "validator_key": "masar_commerce.quality_issues",
            "validator_config": {"file": INSPECT},
        },
        {
            "slug": "understand-orders-and-customers",
            "title": "Understand orders and customers",
            "title_ar": "افهم الطلبات والعملاء",
            "primary_file": INSPECT,
            "instructions": (
                "**Business question:** what happens to orders, and do all registered customers buy?\n\n"
                "Not every order brings in money, and not every registered customer has ordered.\n\n"
                "1. Set `orders_by_status`: a dictionary from each `status` to its number of **distinct** orders.\n"
                "2. Set `customers_without_orders`: how many customers in customers.csv never placed any order.\n"
                "3. Open **findings.md** — your analysis log for the whole project. Under **Data quality**, note "
                "each problem you found in this milestone and how it would distort the numbers if nobody fixed it "
                "(at least 30 words).\n\n"
                "Your executive report in milestone 10 is written from this log, so keep it honest and specific."
            ),
            "instructions_ar": (
                "**سؤال العمل:** ماذا يحدث للطلبات، وهل يشتري كل العملاء المسجلين؟\n\n"
                "ليس كل طلب يجلب المال، وليس كل عميل مسجل قد طلب شيئًا.\n\n"
                "1. عيّن `orders_by_status`: قاموس من كل `status` إلى عدد طلباته **المختلفة**.\n"
                "2. عيّن `customers_without_orders`: كم عميلًا في customers.csv لم يقدّم أي طلب قط.\n"
                "3. افتح **findings.md** — سجل تحليلك طوال المشروع. تحت **Data quality** («جودة البيانات») دوّن كل "
                "مشكلة وجدتها في هذه المرحلة وكيف ستشوّه الأرقام لو لم يصلحها أحد (30 كلمة على الأقل).\n\n"
                "يُكتب تقريرك التنفيذي في المرحلة 10 من هذا السجل، فاجعله دقيقًا ومحددًا."
            ),
            "hints": hints(
                ("You found duplicated order rows a step ago — they would count some orders twice.",
                 "وجدت صفوف طلبات مكررة في الخطوة السابقة — وستحسب بعض الطلبات مرتين."),
                ("Customers who never ordered do not appear in orders.csv at all; compare customer_id across the "
                 "two tables.",
                 "العملاء الذين لم يطلبوا لا يظهرون في orders.csv إطلاقًا؛ قارن customer_id بين الجدولين."),
                ("Remove duplicate rows (or count unique order_id values) before counting by status; use isin() "
                 "to find customers whose id never appears in orders.",
                 "احذف الصفوف المكررة (أو اعدد قيم order_id الفريدة) قبل العدّ حسب الحالة؛ واستخدم isin() لإيجاد "
                 "العملاء الذين لا يظهر معرّفهم في الطلبات."),
            ),
            "validator_key": "masar_commerce.orders_and_customers",
            "validator_config": {"file": INSPECT, "insight": insight("Data quality", "جودة البيانات", min_words=30)},
        },
    ],
}


# ─── M3 — Prepare and Clean the Data (moderate) ──────────────────────────────

M3 = {
    "slug": "prepare-and-clean",
    "title": "Prepare and Clean the Data",
    "title_ar": "جهّز البيانات ونظّفها",
    "summary": "Fix the problems once, in one place, and build the analysis-ready sales table every later step uses.",
    "summary_ar": "أصلح المشكلات مرة واحدة في مكان واحد، وابنِ جدول المبيعات الجاهز للتحليل الذي تعتمد عليه كل الخطوات التالية.",
    "skills": [CLEANING, PANDAS],
    "tasks": [
        {
            "slug": "remove-duplicates",
            "title": "Remove duplicate records",
            "title_ar": "احذف السجلات المكررة",
            "primary_file": CLEAN,
            "instructions": (
                "**Business question:** what does each order really look like — once?\n\n"
                "**analysis/clean_data.py** is the single place where the data gets fixed: every later script "
                "imports `load_clean_data()` from it, so a mistake here flows into every number in your report.\n\n"
                "Make `clean_orders()` return one row per order and `clean_order_items()` one row per order line, "
                "without losing any real order or line. How you do it is up to you.\n\n"
                "Check Step reads `orders_clean` and `items_clean` from the block at the bottom of the file."
            ),
            "instructions_ar": (
                "**سؤال العمل:** كيف يبدو كل طلب حقًا — مرة واحدة؟\n\n"
                "**analysis/clean_data.py** هو المكان الوحيد الذي تُصلَح فيه البيانات: كل الملفات اللاحقة تستورد "
                "منه `load_clean_data()`، فأي خطأ هنا ينتقل إلى كل رقم في تقريرك.\n\n"
                "اجعل `clean_orders()` تعيد صفًا واحدًا لكل طلب، و`clean_order_items()` صفًا واحدًا لكل سطر طلب، "
                "دون أن تفقد أي طلب أو سطر حقيقي. الطريقة متروكة لك.\n\n"
                "يقرأ الفحص `orders_clean` و`items_clean` من الجزء السفلي في الملف."
            ),
            "hints": hints(
                ("The duplicates you measured in milestone 2 are exact copies; removing them must keep the first copy.",
                 "الصفوف المكررة التي قِستها في المرحلة 2 نسخ مطابقة؛ وحذفها يجب أن يُبقي النسخة الأولى."),
                ("order_id identifies an order and order_item_id an order line; after cleaning, each should appear "
                 "exactly once.",
                 "يحدد order_id الطلب ويحدد order_item_id سطر الطلب؛ وبعد التنظيف يجب أن يظهر كل منهما مرة واحدة."),
                ("Drop exact duplicate rows in each function and reset the index; converting order_date to a date "
                 "here will help in later milestones.",
                 "احذف الصفوف المكررة تمامًا في كل دالة وأعد ضبط الفهرس؛ وتحويل order_date إلى تاريخ هنا سيفيدك في "
                 "المراحل اللاحقة."),
            ),
            "validator_key": "masar_commerce.clean_duplicates",
            "validator_config": {"file": CLEAN},
        },
        {
            "slug": "standardise-customers",
            "title": "Standardise customer values",
            "title_ar": "وحّد قيم العملاء",
            "primary_file": CLEAN,
            "instructions": (
                "**Business question:** can we group customers reliably by where they live?\n\n"
                "Complete `clean_customers()` so that every country has a single spelling and no customer is left "
                "without a city. Keep **every** customer: a customer with a missing city is still a customer, and "
                "dropping them would silently remove their orders from every total.\n\n"
                "Check Step reads `customers_clean`."
            ),
            "instructions_ar": (
                "**سؤال العمل:** هل يمكننا تجميع العملاء بدقة حسب مكان سكنهم؟\n\n"
                "أكمل `clean_customers()` بحيث يصبح لكل دولة تهجئة واحدة ولا يبقى أي عميل بلا مدينة. احتفظ **بكل** "
                "العملاء: فالعميل الذي مدينته مفقودة ما زال عميلًا، وحذفه سيُسقط طلباته بصمت من كل إجمالي.\n\n"
                "يقرأ الفحص `customers_clean`."
            ),
            "hints": hints(
                ("Fixing a value is better than dropping the row it sits in.", "إصلاح القيمة أفضل من حذف الصف الذي يحتويها."),
                ("The country problems are extra spaces and capitalisation; a missing city can be filled with a "
                 "clear placeholder.",
                 "مشكلات الدولة هي المسافات الزائدة وحالة الأحرف؛ ويمكن ملء المدينة المفقودة بقيمة بديلة واضحة."),
                ("Work on a copy, standardise the country column with string methods, and fill missing cities with "
                 "a value such as \"Unknown\".",
                 "اعمل على نسخة، ووحّد عمود الدولة بدوال النصوص، واملأ المدن المفقودة بقيمة مثل \"Unknown\"."),
            ),
            "validator_key": "masar_commerce.clean_customers",
            "validator_config": {"file": CLEAN},
        },
        {
            "slug": "build-sales-table",
            "title": "Build the sales table",
            "title_ar": "ابنِ جدول المبيعات",
            "primary_file": CLEAN,
            "instructions": (
                "**Business question:** what did we actually sell?\n\n"
                "Complete `build_sales()`: one row per order line of a **completed** order, with the order, customer "
                "and product details joined in, and `line_revenue = quantity × unit_price`. The function's "
                "docstring lists the columns later milestones rely on.\n\n"
                "Joins are where analyses quietly go wrong: a join to a table that still has duplicates multiplies "
                "rows, and a join on the wrong key loses them. Check your row count after every join.\n\n"
                "Check Step reads `sales`."
            ),
            "instructions_ar": (
                "**سؤال العمل:** ماذا بعنا فعلًا؟\n\n"
                "أكمل `build_sales()`: صف واحد لكل سطر من طلب **مكتمل**، مع ربط تفاصيل الطلب والعميل والمنتج، "
                "و`line_revenue = quantity × unit_price`. يسرد التوثيق داخل الدالة الأعمدة التي تعتمد عليها المراحل "
                "اللاحقة.\n\n"
                "عمليات الربط (JOIN) هي حيث تفسد التحليلات بصمت: الربط مع جدول ما زال فيه تكرار يضاعف الصفوف، "
                "والربط على مفتاح خاطئ يُسقطها. تحقق من عدد الصفوف بعد كل ربط.\n\n"
                "يقرأ الفحص `sales`."
            ),
            "hints": hints(
                ("Only completed orders are recognised sales; every other status must stay out of this table.",
                 "الطلبات المكتملة وحدها مبيعات معترف بها؛ وكل حالة أخرى يجب أن تبقى خارج هذا الجدول."),
                ("order_items links to orders through order_id, orders to customers through customer_id, and "
                 "order_items to products through product_id. Use the cleaned tables.",
                 "يرتبط order_items بـ orders عبر order_id، وorders بـ customers عبر customer_id، وorder_items بـ "
                 "products عبر product_id. استخدم الجداول النظيفة."),
                ("Filter the cleaned orders to completed first, merge them with the order lines, then bring in the "
                 "customer and product columns, add line_revenue and keep the listed columns.",
                 "اختر الطلبات المكتملة من الطلبات النظيفة أولًا، وادمجها مع أسطر الطلبات، ثم أضف أعمدة العميل والمنتج، "
                 "واحسب line_revenue واحتفظ بالأعمدة المذكورة."),
            ),
            "validator_key": "masar_commerce.build_sales",
            "validator_config": {"file": CLEAN},
        },
    ],
}


# ─── M4 — SQL Business Analysis (moderate) ───────────────────────────────────

SQL_RAW_NOTE = (
    "SQL runs on the **raw** tables, so your query has to deal with the data issues itself. Once you have a "
    "CTE that returns clean, completed order lines, reuse it in your other queries — analysts keep building "
    "blocks like that rather than solving the same problem twice."
)
SQL_RAW_NOTE_AR = (
    "يعمل SQL على الجداول **الخام**، لذا يجب أن يعالج استعلامك مشكلات البيانات بنفسه. وحين يصبح لديك تعبير "
    "CTE يعيد أسطر الطلبات المكتملة النظيفة، أعد استخدامه في استعلاماتك الأخرى — فالمحللون يحتفظون بمثل هذه "
    "اللبنات بدل حل المشكلة نفسها مرتين."
)

M4 = {
    "slug": "sql-business-analysis",
    "title": "SQL Business Analysis",
    "title_ar": "تحليل الأعمال باستخدام SQL",
    "summary": "Answer management's core questions directly in SQL — then say what the answers mean.",
    "summary_ar": "أجب عن أسئلة الإدارة الأساسية مباشرة بـ SQL — ثم وضّح ما تعنيه الإجابات.",
    "skills": [SQL_ANALYSIS],
    "tasks": [
        {
            "slug": "sql-revenue-by-category",
            "title": "Revenue by category",
            "title_ar": "الإيرادات حسب الفئة",
            "primary_file": "sql/revenue_by_category.sql",
            "instructions": (
                "**Business question:** which product categories bring in the most recognised revenue?\n\n"
                "The Head of Sales sets targets by category and needs to know where the money comes from. Write "
                "**sql/revenue_by_category.sql** so it returns one row per category with the columns `category` and "
                "`revenue`. The starter query runs, but it counts order lines of every status.\n\n"
                f"{SQL_RAW_NOTE} Row order does not matter for this check."
            ),
            "instructions_ar": (
                "**سؤال العمل:** أي فئات المنتجات تجلب أعلى إيرادات معترف بها؟\n\n"
                "يضع رئيس المبيعات أهدافه حسب الفئة ويحتاج إلى معرفة مصدر المال. اكتب **sql/revenue_by_category.sql** "
                "ليعيد صفًا لكل فئة بالعمودين `category` و`revenue`. الاستعلام المبدئي يعمل، لكنه يعدّ أسطر الطلبات "
                "بكل الحالات.\n\n"
                f"{SQL_RAW_NOTE_AR} ترتيب الصفوف لا يهم في هذا الفحص."
            ),
            "hints": hints(
                ("Recognised revenue needs three things: the price charged, the order status and the product's "
                 "category — and each order counted once.",
                 "تحتاج الإيرادات المعترف بها إلى ثلاثة أشياء: السعر المدفوع، وحالة الطلب، وفئة المنتج — مع حساب "
                 "كل طلب مرة واحدة."),
                ("quantity and unit_price are in order_items, status in orders, category in products; orders and "
                 "order_items both contain exact duplicate rows.",
                 "الكمية والسعر في order_items، والحالة في orders، والفئة في products؛ وفي orders وorder_items "
                 "صفوف مكررة تمامًا."),
                ("Deduplicate orders and order lines first (a CTE keeps it readable), join the three tables on their "
                 "keys, keep completed orders, then sum quantity × unit_price per category.",
                 "أزل التكرار من الطلبات والأسطر أولًا (تعبير CTE يجعل ذلك مقروءًا)، واربط الجداول الثلاثة على "
                 "مفاتيحها، واحتفظ بالطلبات المكتملة، ثم اجمع quantity × unit_price لكل فئة."),
            ),
            "validator_key": "masar_commerce.sql_revenue_by_category",
            "validator_config": {"file": "sql/revenue_by_category.sql"},
        },
        {
            "slug": "sql-monthly-revenue",
            "title": "Monthly revenue and orders",
            "title_ar": "الإيرادات والطلبات الشهرية",
            "primary_file": "sql/monthly_revenue.sql",
            "instructions": (
                "**Business question:** how did recognised revenue and completed orders move month by month?\n\n"
                "Management sees sales changing but cannot say when. Write **sql/monthly_revenue.sql**: one row per "
                "month, **in calendar order**, with the columns `month`, `revenue` and `orders` (distinct completed "
                "orders). `month` can be text like `2025-01` or the first day of the month.\n\n"
                "Order matters here — a trend read out of order is a wrong trend."
            ),
            "instructions_ar": (
                "**سؤال العمل:** كيف تحرّكت الإيرادات المعترف بها والطلبات المكتملة شهرًا بعد شهر؟\n\n"
                "ترى الإدارة أن المبيعات تتغير لكنها لا تعرف متى. اكتب **sql/monthly_revenue.sql**: صف لكل شهر "
                "**بالترتيب الزمني** بالأعمدة `month` و`revenue` و`orders` (الطلبات المكتملة المختلفة). يمكن أن "
                "يكون `month` نصًا مثل `2025-01` أو أول يوم في الشهر.\n\n"
                "الترتيب مهم هنا — الاتجاه الذي يُقرأ بلا ترتيب اتجاه خاطئ."
            ),
            "hints": hints(
                ("A monthly trend groups sales by the month the order was placed; an order has several lines but "
                 "counts once.",
                 "الاتجاه الشهري يجمّع المبيعات حسب شهر تقديم الطلب؛ وللطلب عدة أسطر لكنه يُحسب مرة واحدة."),
                ("order_date is a date column; DuckDB can format it as year-month or truncate it to the month.",
                 "العمود order_date تاريخ؛ ويستطيع DuckDB تنسيقه بصيغة السنة-الشهر أو اقتطاعه إلى الشهر."),
                ("Reuse your deduplicated, completed sales, group by a month expression built with strftime or "
                 "date_trunc, count distinct order ids, and order the result by month.",
                 "أعد استخدام مبيعاتك المكتملة بعد إزالة التكرار، وجمّع حسب تعبير للشهر مبني بـ strftime أو "
                 "date_trunc، واعدد معرّفات الطلبات المختلفة، ورتّب النتيجة حسب الشهر."),
            ),
            "validator_key": "masar_commerce.sql_monthly_revenue",
            "validator_config": {"file": "sql/monthly_revenue.sql"},
        },
        {
            "slug": "sql-top-customers",
            "title": "Top customers",
            "title_ar": "أفضل العملاء",
            "primary_file": "sql/top_customers.sql",
            "instructions": (
                "**Business question:** who are our ten most valuable customers?\n\n"
                "Marketing wants to treat its best customers differently, and \"best\" means the most recognised "
                "revenue — not the most orders. Write **sql/top_customers.sql** returning those 10 customers, "
                "highest first, with the columns `customer_id`, `revenue` and `orders` (their distinct completed "
                "orders).\n\n"
                "Ranking is the point of this query, so the order of the rows is checked."
            ),
            "instructions_ar": (
                "**سؤال العمل:** من هم أعلى عشرة عملاء قيمةً لدينا؟\n\n"
                "يريد التسويق معاملة أفضل عملائه بشكل مختلف، و«الأفضل» تعني الأعلى في الإيرادات المعترف بها — لا "
                "الأكثر طلبًا. اكتب **sql/top_customers.sql** ليعيد هؤلاء العشرة، الأعلى أولًا، بالأعمدة "
                "`customer_id` و`revenue` و`orders` (طلباتهم المكتملة المختلفة).\n\n"
                "الترتيب هو جوهر هذا الاستعلام، لذا يُفحص ترتيب الصفوف."
            ),
            "hints": hints(
                ("Aggregate per customer first; ranking comes after.", "اجمع لكل عميل أولًا؛ ثم يأتي الترتيب."),
                ("customer_id is in orders, the money in order_items; sort by revenue, not by the order count.",
                 "يوجد customer_id في orders والمال في order_items؛ رتّب حسب الإيرادات لا حسب عدد الطلبات."),
                ("Group completed, deduplicated sales by customer, compute revenue and a distinct order count, sort "
                 "by revenue descending and keep ten rows (LIMIT, or a ranking window function).",
                 "جمّع المبيعات المكتملة بعد إزالة التكرار حسب العميل، واحسب الإيرادات وعدد الطلبات المختلفة، ورتّب "
                 "تنازليًا حسب الإيرادات واحتفظ بعشرة صفوف (LIMIT أو دالة ترتيب نافذية)."),
            ),
            "validator_key": "masar_commerce.sql_top_customers",
            "validator_config": {"file": "sql/top_customers.sql"},
        },
        {
            "slug": "sql-product-performance",
            "title": "Performance of every product",
            "title_ar": "أداء كل منتج",
            "primary_file": "sql/product_performance.sql",
            "instructions": (
                "**Business question:** how does every product in the catalogue perform — including the ones that "
                "did not sell at all?\n\n"
                "Dead stock costs money too, so the Head of Sales needs to see it. Write "
                "**sql/product_performance.sql**: one row for **every** product in products.csv with the columns "
                "`product_id`, `product_name`, `category`, `units_sold` and `revenue`. Products with no completed "
                "sales must show `0`, not an empty value."
            ),
            "instructions_ar": (
                "**سؤال العمل:** كيف يؤدي كل منتج في الكتالوج — ومنها المنتجات التي لم تُبع إطلاقًا؟\n\n"
                "المخزون الراكد يكلّف المال أيضًا، لذا يحتاج رئيس المبيعات إلى رؤيته. اكتب "
                "**sql/product_performance.sql**: صف لكل منتج في products.csv **بلا استثناء** بالأعمدة `product_id` "
                "و`product_name` و`category` و`units_sold` و`revenue`. يجب أن تُظهر المنتجات التي ليس لها مبيعات "
                "مكتملة القيمة `0` لا قيمة فارغة."
            ),
            "hints": hints(
                ("A product that never sold has no order lines at all — an inner join drops it.",
                 "المنتج الذي لم يُبع ليس له أسطر طلبات إطلاقًا — والربط الداخلي يُسقطه."),
                ("Start from products and attach sales to it; a missing match produces NULL, which the business "
                 "reads as 0.",
                 "ابدأ من products وأضف إليها المبيعات؛ وعدم التطابق ينتج NULL، وهو ما تقرؤه الشركة صفرًا."),
                ("Compute completed sales per product in a CTE, LEFT JOIN it to products, and replace NULL totals "
                 "with 0 (COALESCE).",
                 "احسب المبيعات المكتملة لكل منتج في CTE، واربطها بـ products عبر LEFT JOIN، واستبدل الإجماليات "
                 "الفارغة بصفر (COALESCE)."),
            ),
            "validator_key": "masar_commerce.sql_product_performance",
            "validator_config": {"file": "sql/product_performance.sql"},
        },
        {
            "slug": "sql-regional-performance",
            "title": "Regional performance",
            "title_ar": "أداء المناطق",
            "primary_file": "sql/regional_performance.sql",
            "instructions": (
                "**Business question:** how do our four sales regions compare?\n\n"
                "Write **sql/regional_performance.sql**: one row per region with the columns `region`, `customers` "
                "(distinct customers with a completed order), `orders` (distinct completed orders), `revenue` and "
                "`aov` (revenue ÷ orders).\n\n"
                "Then look at all five of your SQL results together. In **findings.md**, under **SQL findings**, "
                "write what they tell management — where revenue concentrates, how it moved, what surprised you "
                "(at least 40 words). Interpret; do not paste tables."
            ),
            "instructions_ar": (
                "**سؤال العمل:** كيف تتقارن مناطق المبيعات الأربع؟\n\n"
                "اكتب **sql/regional_performance.sql**: صف لكل منطقة بالأعمدة `region` و`customers` (العملاء "
                "المختلفون الذين لديهم طلب مكتمل) و`orders` (الطلبات المكتملة المختلفة) و`revenue` و`aov` "
                "(الإيرادات ÷ الطلبات).\n\n"
                "ثم انظر إلى نتائج SQL الخمس معًا. في **findings.md** تحت **SQL findings** («نتائج SQL») اكتب ما "
                "تخبر به الإدارة — أين تتركز الإيرادات، وكيف تحركت، وما الذي فاجأك (40 كلمة على الأقل). فسّر ولا "
                "تلصق الجداول."
            ),
            "hints": hints(
                ("A region with many customers but a low AOV tells a different story from one with fewer, higher-"
                 "value customers.",
                 "المنطقة ذات العملاء الكثيرين ومتوسط طلب منخفض تروي قصة مختلفة عن منطقة ذات عملاء أقل وقيمة أعلى."),
                ("region is a customer attribute, reached through orders.customer_id; customers and orders are both "
                 "distinct counts.",
                 "المنطقة صفة للعميل تصل إليها عبر orders.customer_id؛ والعملاء والطلبات كلاهما عدد قيم مختلفة."),
                ("Join completed, deduplicated lines to orders and customers, group by region, count distinct "
                 "customers and orders, and divide revenue by orders for AOV. For the findings, compare your five "
                 "results rather than restating them.",
                 "اربط الأسطر المكتملة بعد إزالة التكرار مع orders وcustomers، وجمّع حسب المنطقة، واعدد العملاء "
                 "والطلبات المختلفة، واقسم الإيرادات على الطلبات لحساب AOV. وفي السجل قارن نتائجك الخمس بدل تكرارها."),
            ),
            "validator_key": "masar_commerce.sql_regional_performance",
            "validator_config": {"file": "sql/regional_performance.sql",
                                 "insight": insight("SQL findings", "نتائج SQL", min_words=40)},
        },
    ],
}


# ─── M5 — Core Business KPIs (reduced guidance) ──────────────────────────────

M5 = {
    "slug": "core-kpis",
    "title": "Core Business KPIs",
    "title_ar": "مؤشرات الأداء الأساسية",
    "summary": "Calculate the headline KPIs, and the value of orders that did not turn into revenue.",
    "summary_ar": "احسب مؤشرات الأداء الرئيسية، وقيمة الطلبات التي لم تتحول إلى إيرادات.",
    "skills": [KPI, PANDAS],
    "tasks": [
        {
            "slug": "headline-kpis",
            "title": "Headline KPIs",
            "title_ar": "المؤشرات الرئيسية",
            "primary_file": KPIS,
            "instructions": (
                "**Business question:** how did the business perform overall in 2025?\n\n"
                "These five numbers open the CEO's report, so they must match the definitions in your analysis "
                "plan. In **analysis/kpis.py**, fill the `kpis` dictionary from the cleaned data:\n\n"
                "| key | meaning |\n| --- | --- |\n"
                "| `revenue` | recognised revenue |\n"
                "| `completed_orders` | number of completed orders |\n"
                "| `aov` | average order value |\n"
                "| `unique_customers` | customers with at least one completed order |\n"
                "| `items_sold` | units sold in completed orders |\n\n"
                "Keep full precision; round only in the report."
            ),
            "instructions_ar": (
                "**سؤال العمل:** كيف كان أداء الشركة إجمالًا في 2025؟\n\n"
                "تفتتح هذه الأرقام الخمسة تقرير الرئيس التنفيذي، لذا يجب أن تطابق التعريفات في خطة تحليلك. في "
                "**analysis/kpis.py** املأ القاموس `kpis` من البيانات النظيفة:\n\n"
                "| المفتاح | المعنى |\n| --- | --- |\n"
                "| `revenue` | الإيرادات المعترف بها |\n"
                "| `completed_orders` | عدد الطلبات المكتملة |\n"
                "| `aov` | متوسط قيمة الطلب |\n"
                "| `unique_customers` | العملاء الذين لديهم طلب مكتمل واحد على الأقل |\n"
                "| `items_sold` | القطع المبيعة في الطلبات المكتملة |\n\n"
                "احتفظ بالدقة الكاملة؛ وقرّب في التقرير فقط."
            ),
            "hints": hints(
                ("Your sales table already contains only completed order lines.", "يحتوي جدول المبيعات أسطر الطلبات المكتملة فقط."),
                ("One order has several lines and one customer several orders — orders and customers are distinct "
                 "counts, revenue and units are sums.",
                 "للطلب عدة أسطر وللعميل عدة طلبات — فالطلبات والعملاء عدد قيم مختلفة، والإيرادات والقطع مجاميع."),
                ("Sum line_revenue and quantity, count unique order_id and customer_id, and derive AOV from revenue "
                 "and the completed-order count.",
                 "اجمع line_revenue وquantity، واعدد قيم order_id وcustomer_id الفريدة، واشتق AOV من الإيرادات وعدد "
                 "الطلبات المكتملة."),
            ),
            "validator_key": "masar_commerce.headline_kpis",
            "validator_config": {"file": KPIS},
        },
        {
            "slug": "revenue-at-risk",
            "title": "Revenue at risk",
            "title_ar": "الإيرادات المعرّضة للخطر",
            "primary_file": KPIS,
            "instructions": (
                "**Business question:** how much value did we lose, or not collect yet?\n\n"
                "Cancelled, returned and pending orders are not revenue — but they are a risk management needs to "
                "size. Still in **analysis/kpis.py**:\n\n"
                "- `status_value` — `{\"cancelled\": …, \"returned\": …, \"pending\": …}`: the order-line value of "
                "each of those statuses;\n"
                "- `cancellation_rate` — the share of all orders that were cancelled (0–1)."
            ),
            "instructions_ar": (
                "**سؤال العمل:** ما قيمة ما خسرناه أو لم نحصّله بعد؟\n\n"
                "الطلبات الملغاة والمرتجعة والمعلّقة ليست إيرادات — لكنها خطر تحتاج الإدارة إلى معرفة حجمه. في "
                "**analysis/kpis.py** نفسه:\n\n"
                "- `status_value` — `{\"cancelled\": …, \"returned\": …, \"pending\": …}`: قيمة أسطر الطلبات لكل حالة "
                "من هذه الحالات؛\n"
                "- `cancellation_rate` — نسبة الطلبات الملغاة من كل الطلبات (من 0 إلى 1)."
            ),
            "hints": hints(
                ("The sales table holds only completed orders, so this needs the other cleaned tables.",
                 "يحتوي جدول المبيعات الطلبات المكتملة فقط، لذا تحتاج الجداول النظيفة الأخرى."),
                ("status lives in orders and the value in order_items; the rate's denominator is every distinct "
                 "order, whatever its status.",
                 "الحالة في orders والقيمة في order_items؛ ومقام النسبة هو كل الطلبات المختلفة مهما كانت حالتها."),
                ("Join the cleaned order lines to the cleaned orders, compute each line's value, total it per "
                 "status and keep the three statuses; take the mean of a cancelled-or-not flag over orders for "
                 "the rate.",
                 "اربط أسطر الطلبات النظيفة بالطلبات النظيفة، واحسب قيمة كل سطر، واجمعها لكل حالة واحتفظ بالحالات "
                 "الثلاث؛ وللنسبة خذ متوسط مؤشر «ملغى أم لا» على الطلبات."),
            ),
            "validator_key": "masar_commerce.revenue_at_risk",
            "validator_config": {"file": KPIS},
        },
    ],
}


# ─── M6 — Customer Analysis (reduced guidance) ───────────────────────────────

M6 = {
    "slug": "customer-analysis",
    "title": "Customer Analysis",
    "title_ar": "تحليل العملاء",
    "summary": "How concentrated is customer value, how many customers come back, and how do segments differ?",
    "summary_ar": "ما مدى تركّز قيمة العملاء، وكم عميلًا يعود، وكيف تختلف شرائح العملاء؟",
    "skills": [CUSTOMER, PANDAS],
    "tasks": [
        {
            "slug": "customer-concentration",
            "title": "Customer concentration",
            "title_ar": "تركّز قيمة العملاء",
            "primary_file": CUSTOMERS,
            "instructions": (
                "**Business question:** does our revenue depend on a small group of customers?\n\n"
                "Your SQL query named the top ten. Marketing now needs the bigger picture: if the best tenth of "
                "customers left, how much revenue would go with them? In **analysis/customers.py** set:\n\n"
                "- `customer_revenue` — each purchasing customer's recognised revenue (a dictionary or Series);\n"
                "- `top_decile_share` — the share of recognised revenue from the top 10% of purchasing customers "
                "(round the number of customers down), as a fraction."
            ),
            "instructions_ar": (
                "**سؤال العمل:** هل تعتمد إيراداتنا على مجموعة صغيرة من العملاء؟\n\n"
                "سمّى استعلام SQL أعلى عشرة عملاء. ويحتاج التسويق الآن إلى الصورة الأوسع: لو غادر أفضل عُشر "
                "العملاء، فكم من الإيرادات سيذهب معهم؟ في **analysis/customers.py** عيّن:\n\n"
                "- `customer_revenue` — الإيرادات المعترف بها لكل عميل مشترٍ (قاموس أو Series)؛\n"
                "- `top_decile_share` — حصة أعلى 10% من العملاء المشترين من الإيرادات المعترف بها (قرّب عدد العملاء "
                "لأسفل)، ككسر."
            ),
            "hints": hints(
                ("Concentration compares a group's share of the total with its share of the people.",
                 "التركّز يقارن حصة مجموعة من الإجمالي بحصتها من الأشخاص."),
                ("Purchasing customers are the customer_id values in your sales table; 10% of them, rounded down, "
                 "is the size of the group.",
                 "العملاء المشترون هم قيم customer_id في جدول المبيعات؛ و10% منهم مقرّبة لأسفل هي حجم المجموعة."),
                ("Total line_revenue per customer, sort it descending, add up the first n = number of customers // 10 "
                 "values and divide by total revenue.",
                 "اجمع line_revenue لكل عميل، ورتّبها تنازليًا، واجمع أول n = عدد العملاء // 10 قيمة واقسمها على "
                 "إجمالي الإيرادات."),
            ),
            "validator_key": "masar_commerce.customer_concentration",
            "validator_config": {"file": CUSTOMERS},
        },
        {
            "slug": "repeat-purchase-behaviour",
            "title": "Repeat purchase behaviour",
            "title_ar": "سلوك الشراء المتكرر",
            "primary_file": CUSTOMERS,
            "instructions": (
                "**Business question:** do customers come back?\n\n"
                "Winning a customer is expensive; keeping one is cheaper. Measure how many customers buy again:\n\n"
                "- `repeat_customer_rate` — the share of purchasing customers with two or more completed orders (0–1);\n"
                "- `one_time_customers` — purchasing customers with exactly one completed order;\n"
                "- `avg_orders_per_customer` — the average number of completed orders per purchasing customer."
            ),
            "instructions_ar": (
                "**سؤال العمل:** هل يعود العملاء؟\n\n"
                "كسب عميل جديد مكلف، والاحتفاظ به أرخص. قِس كم عميلًا يشتري مرة أخرى:\n\n"
                "- `repeat_customer_rate` — نسبة العملاء المشترين الذين لديهم طلبان مكتملان أو أكثر (من 0 إلى 1)؛\n"
                "- `one_time_customers` — العملاء المشترون الذين لديهم طلب مكتمل واحد فقط؛\n"
                "- `avg_orders_per_customer` — متوسط عدد الطلبات المكتملة لكل عميل مشترٍ."
            ),
            "hints": hints(
                ("Repeat behaviour is about orders per customer, not order lines per customer.",
                 "سلوك التكرار يتعلق بالطلبات لكل عميل، لا بأسطر الطلبات لكل عميل."),
                ("Each row of the sales table is a line; an order with three lines is still one order.",
                 "كل صف في جدول المبيعات سطر؛ والطلب ذو الأسطر الثلاثة يبقى طلبًا واحدًا."),
                ("Count distinct order_id per customer, then derive all three answers from that one Series.",
                 "اعدد قيم order_id المختلفة لكل عميل، ثم اشتق الإجابات الثلاث من تلك السلسلة وحدها."),
            ),
            "validator_key": "masar_commerce.repeat_behaviour",
            "validator_config": {"file": CUSTOMERS},
        },
        {
            "slug": "customer-segments",
            "title": "Consumer and business customers",
            "title_ar": "عملاء الأفراد والشركات",
            "primary_file": CUSTOMERS,
            "instructions": (
                "**Business question:** do business customers behave differently from consumers?\n\n"
                "Every customer belongs to a `segment`. Set `segment_revenue` and `segment_aov`, each a dictionary "
                "keyed `consumer` and `business`.\n\n"
                "Then, in **findings.md** under **Customers**, write what milestone 6 tells Marketing: how "
                "concentrated value is, how loyal customers are, and what the segments suggest (at least 30 words)."
            ),
            "instructions_ar": (
                "**سؤال العمل:** هل يتصرف عملاء الشركات بشكل مختلف عن الأفراد؟\n\n"
                "ينتمي كل عميل إلى شريحة `segment`. عيّن `segment_revenue` و`segment_aov`، كل منهما قاموس مفتاحاه "
                "`consumer` و`business`.\n\n"
                "ثم اكتب في **findings.md** تحت **Customers** («العملاء») ما تخبر به المرحلة 6 فريق التسويق: مدى "
                "تركّز القيمة، ومدى ولاء العملاء، وما توحي به الشرائح (30 كلمة على الأقل)."
            ),
            "hints": hints(
                ("This is the same KPI logic as milestone 5, applied per segment.",
                 "هذا منطق المؤشرات نفسه من المرحلة 5، مطبّقًا على كل شريحة."),
                ("segment is in the sales table; a segment's AOV divides its revenue by its distinct orders.",
                 "الشريحة موجودة في جدول المبيعات؛ وAOV الشريحة يقسم إيراداتها على طلباتها المختلفة."),
                ("Group sales by segment, sum line_revenue and count unique orders, then divide. For the findings, "
                 "connect the three customer results instead of listing them.",
                 "جمّع المبيعات حسب الشريحة، واجمع line_revenue واعدد الطلبات الفريدة، ثم اقسم. وفي السجل اربط نتائج "
                 "العملاء الثلاث بدل سردها."),
            ),
            "validator_key": "masar_commerce.customer_segments",
            "validator_config": {"file": CUSTOMERS, "insight": insight("Customers", "العملاء", min_words=30)},
        },
    ],
}


# ─── M7 — Product Analysis (reduced guidance) ────────────────────────────────

M7 = {
    "slug": "product-analysis",
    "title": "Product Analysis",
    "title_ar": "تحليل المنتجات",
    "summary": "How dependent are we on a few categories and products, where do discounts eat margin, and do premium products pay?",
    "summary_ar": "ما مدى اعتمادنا على فئات ومنتجات قليلة، وأين تأكل الخصومات هامش الربح، وهل تجدي المنتجات الفاخرة؟",
    "skills": [PRODUCT, PANDAS, SQL_ANALYSIS],
    "tasks": [
        {
            "slug": "category-mix",
            "title": "Category mix and discounting",
            "title_ar": "مزيج الفئات والخصومات",
            "primary_file": PRODUCTS,
            "instructions": (
                "**Business question:** how dependent are we on each category, and where are we giving margin away?\n\n"
                "Your SQL result showed revenue by category. Turn it into decisions: what share of the business "
                "each category is, and how far below list price each category actually sells. In "
                "**analysis/products.py** set:\n\n"
                "- `category_share` — each category's share of recognised revenue (fractions adding up to 1);\n"
                "- `discount_by_category` — for each category, 1 − (revenue ÷ the same units at list price)."
            ),
            "instructions_ar": (
                "**سؤال العمل:** ما مدى اعتمادنا على كل فئة، وأين نتخلى عن هامش الربح؟\n\n"
                "أظهرت نتيجة SQL الإيرادات حسب الفئة. حوّلها إلى قرارات: ما حصة كل فئة من الأعمال، وكم تُباع كل فئة "
                "فعلًا تحت سعر الكتالوج. في **analysis/products.py** عيّن:\n\n"
                "- `category_share` — حصة كل فئة من الإيرادات المعترف بها (كسور مجموعها 1)؛\n"
                "- `discount_by_category` — لكل فئة: 1 − (الإيرادات ÷ الوحدات نفسها بسعر الكتالوج)."
            ),
            "hints": hints(
                ("A share is a part over the whole; discount depth compares what customers paid with the catalogue "
                 "price.",
                 "الحصة جزء على الكل؛ وعمق الخصم يقارن ما دفعه العملاء بسعر الكتالوج."),
                ("unit_price is what was charged and list_price the catalogue price; both are in your sales table.",
                 "unit_price هو المدفوع وlist_price سعر الكتالوج؛ وكلاهما في جدول المبيعات."),
                ("Group sales by category: divide each category's revenue by the total for the share, and compare "
                 "its revenue with the sum of quantity × list_price for the discount.",
                 "جمّع المبيعات حسب الفئة: اقسم إيرادات كل فئة على الإجمالي للحصة، وقارن إيراداتها بمجموع quantity "
                 "× list_price للخصم."),
            ),
            "validator_key": "masar_commerce.category_mix",
            "validator_config": {"file": PRODUCTS},
        },
        {
            "slug": "product-concentration",
            "title": "Product concentration",
            "title_ar": "تركّز المنتجات",
            "primary_file": PRODUCTS,
            "instructions": (
                "**Business question:** how much of the business rests on a handful of products?\n\n"
                "If a best-seller goes out of stock, how exposed are we? Set `top5_share` and `top10_share`: the "
                "share of recognised revenue from the five and the ten highest-revenue products, as fractions."
            ),
            "instructions_ar": (
                "**سؤال العمل:** كم من الأعمال يقوم على حفنة من المنتجات؟\n\n"
                "لو نفد مخزون منتج من الأكثر مبيعًا، فما مدى تعرّضنا؟ عيّن `top5_share` و`top10_share`: حصة أعلى "
                "خمسة وأعلى عشرة منتجات إيرادًا من الإيرادات المعترف بها، ككسور."
            ),
            "hints": hints(
                ("This is the product version of customer concentration.", "هذه نسخة المنتجات من تركّز العملاء."),
                ("Rank products by recognised revenue; only the ranking's top values matter.",
                 "رتّب المنتجات حسب الإيرادات المعترف بها؛ ولا يهم إلا أعلى القيم في الترتيب."),
                ("Total revenue per product, take the largest five (and ten) values and divide their sums by total "
                 "revenue.",
                 "اجمع الإيرادات لكل منتج، وخذ أكبر خمس (وعشر) قيم واقسم مجموعها على إجمالي الإيرادات."),
            ),
            "validator_key": "masar_commerce.product_concentration",
            "validator_config": {"file": PRODUCTS},
        },
        {
            "slug": "sql-price-bands",
            "title": "Price bands",
            "title_ar": "شرائح الأسعار",
            "primary_file": "sql/price_bands.sql",
            "instructions": (
                "**Business question:** do our premium products drive revenue, or our cheaper ones?\n\n"
                "Pricing decisions need the catalogue grouped by price level — a job SQL does well. Write "
                "**sql/price_bands.sql** with one row per band: `budget` (list price below 500), `mid` (500 up to "
                "1,500) and `premium` (1,500 and above), and the columns `price_band`, `products` (catalogue "
                "products in the band, sold or not), `units_sold` and `revenue`.\n\n"
                "Then, in **findings.md** under **Products**, write what milestone 7 means for the Head of Sales "
                "(at least 30 words)."
            ),
            "instructions_ar": (
                "**سؤال العمل:** هل تحرّك منتجاتنا الفاخرة الإيرادات أم الأرخص منها؟\n\n"
                "تحتاج قرارات التسعير إلى تجميع الكتالوج حسب مستوى السعر — وهي مهمة يجيدها SQL. اكتب "
                "**sql/price_bands.sql** بصف لكل شريحة: `budget` (سعر الكتالوج أقل من 500)، و`mid` (من 500 حتى أقل "
                "من 1,500)، و`premium` (1,500 فأكثر)، بالأعمدة `price_band` و`products` (منتجات الكتالوج في الشريحة، "
                "بيعت أم لا) و`units_sold` و`revenue`.\n\n"
                "ثم اكتب في **findings.md** تحت **Products** («المنتجات») ما تعنيه المرحلة 7 لرئيس المبيعات (30 "
                "كلمة على الأقل)."
            ),
            "hints": hints(
                ("Band the products first; unsold products still belong to a band.",
                 "صنّف المنتجات أولًا؛ فالمنتجات غير المبيعة تنتمي إلى شريحة أيضًا."),
                ("A CASE expression on list_price assigns the band; sales attach to products, not the other way "
                 "round.",
                 "يحدد تعبير CASE على list_price الشريحة؛ والمبيعات تُضاف إلى المنتجات لا العكس."),
                ("Build a banded product list in one CTE and completed sales per product in another, LEFT JOIN them, "
                 "then group by band, counting products and summing units and revenue with zeros for no sales.",
                 "ابنِ قائمة المنتجات المصنّفة في CTE والمبيعات المكتملة لكل منتج في CTE آخر، واربطهما بـ LEFT JOIN، "
                 "ثم جمّع حسب الشريحة: اعدد المنتجات واجمع الوحدات والإيرادات بأصفار حيث لا مبيعات."),
            ),
            "validator_key": "masar_commerce.sql_price_bands",
            "validator_config": {"file": "sql/price_bands.sql", "insight": insight("Products", "المنتجات", min_words=30)},
        },
    ],
}


# ─── M8 — Time and Regional Analysis (independent) ───────────────────────────

M8 = {
    "slug": "time-and-regional-analysis",
    "title": "Time and Regional Analysis",
    "title_ar": "التحليل الزمني والإقليمي",
    "summary": "Decide whether the business is growing, when it earns its money, and what a customer is worth in each region.",
    "summary_ar": "حدّد هل تنمو الشركة، ومتى تجني أموالها، وكم يساوي العميل في كل منطقة.",
    "skills": [TIME_SERIES, PANDAS],
    "tasks": [
        {
            "slug": "growth",
            "title": "Growth and seasonality",
            "title_ar": "النمو والموسمية",
            "primary_file": TRENDS,
            "instructions": (
                "**Business question:** is Masar Commerce growing, or just seasonal?\n\n"
                "Your SQL result gave monthly revenue. The CEO's question is harder: is the business growing, and "
                "which months matter most? Decide how to analyse it in **analysis/trends.py**, and set:\n\n"
                "- `mom_growth` — month-over-month growth for each month from February to December, as fractions;\n"
                "- `best_month` — the `\"YYYY-MM\"` month with the highest recognised revenue;\n"
                "- `h2_vs_h1_growth` — second-half revenue compared with first-half revenue, as a fraction."
            ),
            "instructions_ar": (
                "**سؤال العمل:** هل تنمو مسار كوميرس، أم أنها موسمية فقط؟\n\n"
                "أعطتك نتيجة SQL الإيرادات الشهرية. سؤال الرئيس التنفيذي أصعب: هل تنمو الشركة، وأي الأشهر هي الأهم؟ "
                "قرّر كيف تحلل ذلك في **analysis/trends.py**، وعيّن:\n\n"
                "- `mom_growth` — النمو الشهري لكل شهر من فبراير إلى ديسمبر، ككسور؛\n"
                "- `best_month` — الشهر بصيغة `\"YYYY-MM\"` صاحب أعلى إيرادات معترف بها؛\n"
                "- `h2_vs_h1_growth` — إيرادات النصف الثاني مقارنة بإيرادات النصف الأول، ككسر."
            ),
            "hints": hints(
                ("Month-to-month swings are noisy; comparing halves of the year is a steadier growth signal.",
                 "التقلبات الشهرية متذبذبة؛ ومقارنة نصفي العام إشارة نمو أثبت."),
                ("Everything here derives from recognised revenue per month of order_date, kept in calendar order.",
                 "كل شيء هنا مشتق من الإيرادات المعترف بها لكل شهر من order_date، مرتبة زمنيًا."),
                ("Build a month-indexed Series of revenue sorted by month; percentage change gives growth (drop "
                 "January), the label of the maximum gives the best month, and July–December over January–June minus "
                 "one gives the half-year growth.",
                 "ابنِ سلسلة Series للإيرادات مفهرسة بالشهر ومرتبة زمنيًا؛ التغير النسبي بين الأشهر يعطي النمو (أسقط "
                 "يناير)، وفهرس القيمة القصوى يعطي أفضل شهر، وقسمة إيرادات يوليو–ديسمبر على إيرادات يناير–يونيو "
                 "ثم طرح واحد تعطي نمو نصف العام."),
            ),
            "validator_key": "masar_commerce.growth",
            "validator_config": {"file": TRENDS},
        },
        {
            "slug": "regional-value",
            "title": "Regional value",
            "title_ar": "قيمة المناطق",
            "primary_file": TRENDS,
            "instructions": (
                "**Business question:** where should we invest — where revenue is, or where customers are worth "
                "most?\n\n"
                "Choose your approach and set:\n\n"
                "- `region_share` — each region's share of recognised revenue (fractions);\n"
                "- `revenue_per_customer` — each region's recognised revenue per purchasing customer.\n\n"
                "Then, in **findings.md** under **Trends and regions**, explain what milestone 8 says about growth, "
                "seasonality and the regions — and what you would tell the CEO first (at least 40 words)."
            ),
            "instructions_ar": (
                "**سؤال العمل:** أين يجب أن نستثمر — حيث الإيرادات، أم حيث يكون العميل أعلى قيمة؟\n\n"
                "اختر طريقتك وعيّن:\n\n"
                "- `region_share` — حصة كل منطقة من الإيرادات المعترف بها (ككسور)؛\n"
                "- `revenue_per_customer` — الإيرادات المعترف بها لكل عميل مشترٍ في كل منطقة.\n\n"
                "ثم اشرح في **findings.md** تحت **Trends and regions** («الاتجاهات والمناطق») ما تقوله المرحلة 8 عن "
                "النمو والموسمية والمناطق — وما الذي ستقوله للرئيس التنفيذي أولًا (40 كلمة على الأقل)."
            ),
            "hints": hints(
                ("A large region and a valuable region are not always the same region.",
                 "المنطقة الكبيرة والمنطقة القيّمة ليستا دائمًا المنطقة نفسها."),
                ("Revenue per customer divides by purchasing customers (distinct customer_id in sales), not by orders "
                 "or registered customers.",
                 "الإيراد لكل عميل يقسم على العملاء المشترين (قيم customer_id المختلفة في المبيعات)، لا على الطلبات "
                 "ولا على العملاء المسجلين."),
                ("Group sales by region: divide revenue by the overall total for the share, and by the number of "
                 "unique customers for the per-customer value.",
                 "جمّع المبيعات حسب المنطقة: اقسم الإيرادات على الإجمالي العام للحصة، وعلى عدد العملاء الفريدين للقيمة "
                 "لكل عميل."),
            ),
            "validator_key": "masar_commerce.regional_value",
            "validator_config": {"file": TRENDS,
                                 "insight": insight("Trends and regions", "الاتجاهات والمناطق", min_words=40)},
        },
    ],
}


# ─── M9 — Data Visualization (independent) ───────────────────────────────────

def chart_task(slug, title, title_ar, question, question_ar, decision, decision_ar, chart, data_var, expected,
               shape, shape_ar, hint2, hint2_ar, *, takeaways=False):
    task = {
        "slug": slug,
        "title": title,
        "title_ar": title_ar,
        "primary_file": VISUALIZE,
        "instructions": (
            f"**Business question:** {question}\n\n"
            f"**Decision it supports:** {decision}\n\n"
            f"In **analysis/visualize.py**, build `{data_var}` — {shape} — plot the chart you think answers the "
            f"question best, and save it as `{chart}`.\n\n"
            "Check Step confirms the image is a real PNG and that the numbers you plotted match the data. It does "
            "not grade style — your report's readers will."
        ),
        "instructions_ar": (
            f"**سؤال العمل:** {question_ar}\n\n"
            f"**القرار الذي يدعمه:** {decision_ar}\n\n"
            f"في **analysis/visualize.py** ابنِ `{data_var}` — {shape_ar} — وأنشئ الرسم الذي تراه أوضح إجابة عن "
            f"السؤال، واحفظه باسم `{chart}`.\n\n"
            "يتأكد الفحص من أن الصورة PNG حقيقية ومن تطابق الأرقام المرسومة مع البيانات، ولا يقيّم الأسلوب — فهذا "
            "لقرّاء تقريرك."
        ),
        "hints": hints(
            ("A decision-oriented chart has a title that states the question, labelled axes with units (EGP) and "
             "nothing decorative.",
             "الرسم الموجّه للقرار له عنوان يطرح السؤال، ومحاور معنونة بالوحدة (EGP)، ولا زخرفة فيه."),
            (hint2, hint2_ar),
            (f"Compute {data_var} as a plain dictionary first, plot exactly those values, then savefig() to the "
             "path and close() the figure so the next chart starts clean.",
             f"احسب {data_var} كقاموس عادي أولًا، وارسم تلك القيم بالضبط، ثم احفظ بـ savefig() في المسار وأغلق "
             "الرسم بـ close() كي يبدأ الرسم التالي نظيفًا."),
        ),
        "validator_key": "masar_commerce.chart",
        "validator_config": {"file": VISUALIZE, "chart": chart, "data_var": data_var, "expected": expected},
    }
    if takeaways:
        task["instructions"] += (
            "\n\nFinally, in **findings.md** under **Chart takeaways**, write one bullet per chart: what should a "
            "reader conclude from it?"
        )
        task["instructions_ar"] += (
            "\n\nوأخيرًا، اكتب في **findings.md** تحت **Chart takeaways** («خلاصات الرسوم») نقطة لكل رسم: ماذا يجب "
            "أن يستنتج القارئ منه؟"
        )
        task["validator_config"]["insight"] = insight("Chart takeaways", "خلاصات الرسوم", min_words=20, min_items=3)
    return task


M9 = {
    "slug": "data-visualization",
    "title": "Data Visualization",
    "title_ar": "التمثيل المرئي للبيانات",
    "summary": "Three charts, each answering one business question for the report.",
    "summary_ar": "ثلاثة رسوم، يجيب كل منها عن سؤال عمل واحد للتقرير.",
    "skills": [VISUAL],
    "tasks": [
        chart_task(
            "chart-monthly-revenue", "Monthly revenue trend", "اتجاه الإيرادات الشهرية",
            "when in the year does Masar Commerce earn its money?", "متى تجني مسار كوميرس أموالها خلال العام؟",
            "when to stock up and when to run campaigns.", "متى نزيد المخزون ومتى نطلق الحملات.",
            "charts/monthly_revenue.png", "monthly_chart_data", "monthly_revenue",
            "a dictionary from month (\"2025-01\" …) to recognised revenue",
            "قاموس من الشهر (\"2025-01\" …) إلى الإيرادات المعترف بها",
            "A trend over time reads best as a line, with months in calendar order on the x-axis.",
            "يتضح الاتجاه الزمني في رسم خطي، والأشهر على المحور الأفقي بترتيبها الزمني."),
        chart_task(
            "chart-revenue-by-category", "Category performance", "أداء الفئات",
            "which categories carry the business?", "أي الفئات تحمل الأعمال؟",
            "where Sales focuses its targets and stock.", "أين تركّز المبيعات أهدافها ومخزونها.",
            "charts/revenue_by_category.png", "category_chart_data", "category_revenue",
            "a dictionary from category to recognised revenue", "قاموس من الفئة إلى الإيرادات المعترف بها",
            "Comparing categories reads best as sorted bars, largest first.",
            "تتضح المقارنة بين الفئات في أعمدة مرتبة، الأكبر أولًا."),
        chart_task(
            "chart-regional-performance", "Regional performance", "أداء المناطق",
            "which regions bring in the revenue?", "أي المناطق تجلب الإيرادات؟",
            "where to expand marketing and delivery.", "أين نوسّع التسويق والتوصيل.",
            "charts/revenue_by_region.png", "region_chart_data", "region_revenue",
            "a dictionary from region to recognised revenue", "قاموس من المنطقة إلى الإيرادات المعترف بها",
            "Four regions compare well as horizontal bars, largest at the top.",
            "تتضح المقارنة بين المناطق الأربع في أعمدة أفقية، الأكبر في الأعلى.", takeaways=True),
    ],
}


# ─── M10 — Executive Report (synthesis) ──────────────────────────────────────

M10 = {
    "slug": "executive-report",
    "title": "Executive Report",
    "title_ar": "التقرير التنفيذي",
    "summary": "Turn your findings into conclusions and recommendations management can act on.",
    "summary_ar": "حوّل نتائجك إلى استنتاجات وتوصيات يمكن للإدارة العمل بها.",
    "skills": [REPORTING],
    "tasks": [
        {
            "slug": "write-the-report",
            "title": "Write the report",
            "title_ar": "اكتب التقرير",
            "primary_file": REPORT,
            "instructions": (
                "**Business question:** what should management know, and what should they do?\n\n"
                "Write **report.md** for the CEO, the Head of Sales and the Head of Marketing, from your notes in "
                "findings.md. Keep the seven sections; at least two **Key Risks** and three **Recommendations**, "
                "each as a list item that follows from a finding.\n\n"
                "The conclusions are yours. Lead with what matters most, back each claim with your numbers, and "
                "write for readers who will never see your code. **Preview** shows the report as they will read it."
            ),
            "instructions_ar": (
                "**سؤال العمل:** ماذا يجب أن تعرف الإدارة، وماذا يجب أن تفعل؟\n\n"
                "اكتب **report.md** للرئيس التنفيذي ورئيس المبيعات ورئيس التسويق، انطلاقًا من ملاحظاتك في "
                "findings.md. أبقِ الأقسام السبعة (يمكنك استخدام عناوينها العربية: «الملخص التنفيذي»، «أداء الأعمال»، "
                "«رؤى العملاء»، «رؤى المنتجات»، «الاتجاهات الإقليمية والزمنية»، «المخاطر الرئيسية»، «التوصيات»)، "
                "مع خطرين على الأقل وثلاث توصيات، كل منها نقطة في قائمة نابعة من نتيجة.\n\n"
                "الاستنتاجات لك. ابدأ بالأهم، وادعم كل ادعاء بأرقامك، واكتب لقرّاء لن يروا شيفرتك. وتعرض **المعاينة** "
                "التقرير كما سيقرؤونه."
            ),
            "hints": hints(
                ("An executive section leads with the conclusion, then the evidence, then what it means.",
                 "يبدأ القسم التنفيذي بالاستنتاج، ثم الدليل، ثم المعنى."),
                ("Your findings.md sections map onto the report sections; risks come from exposures you measured "
                 "(concentration, leakage, loyalty, discounting).",
                 "تقابل أقسام findings.md أقسام التقرير؛ والمخاطر تأتي من مواطن التعرّض التي قستها (التركّز، "
                 "التسرّب، الولاء، الخصومات)."),
                ("Draft each section from the matching findings, then write the Executive Summary last as the three "
                 "or four points a reader must remember; give each recommendation an owner and a reason.",
                 "صُغ كل قسم من النتائج المقابلة له، ثم اكتب الملخص التنفيذي أخيرًا بثلاث أو أربع نقاط يجب أن "
                 "يتذكرها القارئ؛ واجعل لكل توصية مسؤولًا وسببًا."),
            ),
            "validator_key": "common.markdown_sections",
            "validator_config": {"file": REPORT, "sections": REPORT_SECTIONS},
        },
        {
            "slug": "support-with-numbers",
            "title": "Support it with numbers",
            "title_ar": "ادعمه بالأرقام",
            "primary_file": REPORT,
            "instructions": (
                "**Business question:** can management trust your conclusions?\n\n"
                "An executive report stands on its numbers. Make sure yours states what you calculated:\n\n"
                "- **Business Performance**: recognised revenue, completed orders and average order value;\n"
                "- **Customer Insights**: the repeat customer rate;\n"
                "- **Product Insights**: the category that brings in the most revenue;\n"
                "- **Regional and Time Trends**: the region with the highest revenue, and the best month.\n\n"
                "Round for readers — write “3.8 million EGP” rather than 3812455.5, or “27%” rather than 0.2731 (these show the format, not your numbers); sensible rounding and Arabic digits "
                "are accepted."
            ),
            "instructions_ar": (
                "**سؤال العمل:** هل يمكن للإدارة الوثوق باستنتاجاتك؟\n\n"
                "يقوم التقرير التنفيذي على أرقامه. تأكد أن تقريرك يذكر ما حسبته:\n\n"
                "- **أداء الأعمال**: الإيرادات المعترف بها، والطلبات المكتملة، ومتوسط قيمة الطلب؛\n"
                "- **رؤى العملاء**: معدل العملاء المتكررين؛\n"
                "- **رؤى المنتجات**: الفئة صاحبة أعلى إيرادات؛\n"
                "- **الاتجاهات الإقليمية والزمنية**: المنطقة صاحبة أعلى إيرادات، وأفضل شهر.\n\n"
                "قرّب للقرّاء — اكتب «3.8 مليون جنيه» بدل 3812455.5، أو «27%» بدل 0.2731 (هذه أمثلة على الصيغة لا على أرقامك)؛ يُقبل التقريب المعقول والأرقام العربية."
            ),
            "hints": hints(
                ("Every figure here already exists in your analysis.", "كل رقم هنا موجود بالفعل في تحليلك."),
                ("kpis.py, customers.py, your SQL results and trends.py hold them; put each in the section that "
                 "argues with it.",
                 "تحملها kpis.py وcustomers.py ونتائج SQL وtrends.py؛ ضع كل رقم في القسم الذي يستند إليه."),
                ("Write the figures into sentences that say what they mean, rounded for a reader — not as raw "
                 "dictionaries or long decimals.",
                 "اكتب الأرقام في جمل توضح معناها، مقرّبة للقارئ — لا كقواميس خام أو كسور طويلة."),
            ),
            "validator_key": "masar_commerce.report_metrics",
            "validator_config": {},
        },
        {
            "slug": "embed-the-charts",
            "title": "Embed the charts",
            "title_ar": "ضمّن الرسوم",
            "primary_file": REPORT,
            "instructions": (
                "**Business question:** what should the reader see at a glance?\n\n"
                "Embed your three charts in the sections they support, using Markdown image syntax such as "
                "`![Monthly revenue in 2025](charts/monthly_revenue.png)`, with one sentence under each saying what "
                "to take from it. Your charts already exist from milestone 9; **Preview** shows them in place."
            ),
            "instructions_ar": (
                "**سؤال العمل:** ماذا يجب أن يرى القارئ من النظرة الأولى؟\n\n"
                "ضمّن رسومك الثلاثة في الأقسام التي تدعمها بصيغة صور Markdown مثل "
                "`![Monthly revenue in 2025](charts/monthly_revenue.png)`، مع جملة تحت كل رسم توضح ما يُستخلص منه. "
                "رسومك موجودة بالفعل من المرحلة 9، وتعرضها **المعاينة** في أماكنها."
            ),
            "hints": hints(
                ("Place a chart next to the argument it supports, not in a gallery at the end.",
                 "ضع الرسم بجوار الحجة التي يدعمها، لا في معرض في النهاية."),
                ("The image paths are the ones you saved in milestone 9; the Artifacts tab lists them.",
                 "مسارات الصور هي التي حفظتها في المرحلة 9؛ ويعرضها تبويب الملفات الناتجة."),
                ("Add an image line for each chart in its section and a one-sentence takeaway under it; if a chart "
                 "is reported as not generated, run analysis/visualize.py once more.",
                 "أضف سطر صورة لكل رسم في قسمه وجملة خلاصة تحته؛ وإن ظهر أن رسمًا لم يُولَّد فشغّل analysis/visualize.py "
                 "مرة أخرى."),
            ),
            "validator_key": "masar_commerce.report_charts",
            "validator_config": {"min_charts": 3, "required": [
                "charts/monthly_revenue.png", "charts/revenue_by_category.png", "charts/revenue_by_region.png",
            ]},
        },
    ],
}


PROJECT = {
    "slug": "masar-commerce-analysis",
    "track_slug": "data-analyst",
    "title": "Masar Commerce — Business Performance Analysis",
    "title_ar": "مسار كوميرس — تحليل أداء الأعمال",
    "summary": (
        "Your capstone as a junior Data Analyst: investigate a year of an online retailer's data — profile and "
        "clean it, answer the business questions in SQL and pandas, chart what matters, and deliver an executive "
        "report with recommendations."
    ),
    "summary_ar": (
        "مشروع التخرج لمحلّل البيانات المبتدئ: حقّق في بيانات عام كامل لمتجر إلكتروني — استكشفها ونظّفها، وأجب عن "
        "أسئلة العمل بـ SQL وpandas، وارسم ما يهم، وقدّم تقريرًا تنفيذيًا بالتوصيات."
    ),
    "difficulty": "intermediate",
    "estimated_hours": 15,
    "template_key": "masar-commerce-analysis",
    # Matches DATASET_VERSION in scripts/generate_masar_commerce_data.py.
    "template_version": "2026.10.2",
    "read_only_paths": ["README.md", "README.ar.md", "data/"],
    "position": 10,
    # Shown on the Project Overview before the learner starts, and reused by
    # the completion summary (later: portfolio and certificates).
    "overview": {
        "role": "Junior Data Analyst",
        "role_ar": "محلل بيانات مبتدئ",
        "scenario": (
            "You have just joined Masar Commerce, an online retailer selling across Egypt, the Gulf, the Levant and "
            "North Africa. Sales changed during 2025 and management cannot say why. The CEO, the Head of Sales and "
            "the Head of Marketing have asked you to investigate the company's real order data — messy exports "
            "included — and tell them what is happening and what to do next."
        ),
        "scenario_ar": (
            "انضممت للتو إلى مسار كوميرس، متجر إلكتروني يبيع في مصر والخليج والشام وشمال أفريقيا. تغيّرت المبيعات "
            "خلال 2025 ولا تعرف الإدارة السبب. وقد طلب منك الرئيس التنفيذي ورئيس المبيعات ورئيس التسويق التحقيق في "
            "بيانات الطلبات الحقيقية للشركة — بما فيها ملفات التصدير غير النظيفة — وإخبارهم بما يحدث وما يجب فعله."
        ),
        "duration_hours": [12, 18],
        "skills": [
            skill("SQL", "SQL"), skill("Pandas", "Pandas"), skill("Data Cleaning", "تنظيف البيانات"),
            skill("Business KPIs", "مؤشرات أداء الأعمال (KPI)"), skill("Customer Analysis", "تحليل العملاء"),
            skill("Product Analysis", "تحليل المنتجات"), skill("Time-Series Analysis", "تحليل السلاسل الزمنية"),
            skill("Data Visualization", "التمثيل المرئي للبيانات"), skill("Business Communication", "التواصل في الأعمال"),
        ],
        "deliverables": [
            skill("SQL analyses of categories, months, customers, products, regions and price bands",
                  "تحليلات SQL للفئات والأشهر والعملاء والمنتجات والمناطق وشرائح الأسعار"),
            skill("Python analyses: data profiling, cleaning and a reusable sales table",
                  "تحليلات Python: استكشاف البيانات وتنظيفها وجدول مبيعات قابل لإعادة الاستخدام"),
            skill("The core business KPIs and the value at risk", "مؤشرات الأداء الأساسية والقيمة المعرّضة للخطر"),
            skill("Customer insights: concentration, loyalty and segments", "رؤى العملاء: التركّز والولاء والشرائح"),
            skill("Product insights: category mix, discounting and concentration",
                  "رؤى المنتجات: مزيج الفئات والخصومات والتركّز"),
            skill("Three decision-focused charts", "ثلاثة رسوم موجّهة للقرار"),
            skill("A final executive report with risks and recommendations",
                  "تقرير تنفيذي نهائي بالمخاطر والتوصيات"),
        ],
    },
    "milestones": [M1, M2, M3, M4, M5, M6, M7, M8, M9, M10],
    # Retired slugs are deleted on sync (with any progress on them): the
    # foundation demo, and tasks merged away when repeated work was removed.
    "retired_milestone_slugs": ["introduction", "inspect-the-data", "basic-kpis"],
    "retired_task_slugs": [
        "state-the-objective", "define-the-objective", "identify-stakeholders", "customer-value",
        "category-performance", "best-and-worst-products", "discount-depth", "monthly-trend",
        "regional-performance",
    ],
}
