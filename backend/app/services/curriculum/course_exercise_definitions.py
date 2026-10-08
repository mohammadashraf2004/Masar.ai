"""Authored deterministic definitions for implementation exercises in Courses 17 and 18.

The lesson files remain the source of titles, instructions, skills, placement,
and translations. This reviewed registry adds only executable starter/solution
code and hidden deterministic tests to exercises that have an objective result.
"""
from __future__ import annotations

from typing import Any

from .spec import CourseSpec


def _feedback(number: int, en: str, ar: str) -> dict[str, Any]:
    return {
        "id": f"blank_{number}", "type": "sql_blank", "blank": number,
        "accepted": [], "feedback": {"en": f"Blank {number}: {en}", "ar": f"الفراغ {number}: {ar}"},
    }


def _fill_sql(template: str, answers: list[str]) -> str:
    result = template
    for answer in answers:
        result = result.replace("___", answer, 1)
    return result


def _sql(
    template: str, answers: list[list[str]], setup: str, columns: list[str], rows: list[list[Any]],
    feedback: list[tuple[str, str]], *, ordered: bool = False,
) -> dict[str, Any]:
    canonical = [variants[0] for variants in answers]
    tests = []
    for index, (variants, messages) in enumerate(zip(answers, feedback), start=1):
        test = _feedback(index, messages[0], messages[1])
        test["accepted"] = variants
        tests.append(test)
    tests.append({
        "id": "query_result", "type": "sql_result", "setup_sql": setup,
        "expected_columns": columns, "expected_rows": rows, "ordered": ordered,
        "feedback": {
            "en": "The query runs, but its columns or rows do not match the required result.",
            "ar": "يعمل الاستعلام، لكن أعمدته أو صفوفه لا تطابق النتيجة المطلوبة.",
        },
    })
    return {
        "exercise_type": "code", "language": "sql", "starter_code": template,
        "solution_code": _fill_sql(template, canonical), "tests": tests,
        "hint": "Fill only the marked SQL fields; each field is checked before the query result.",
        "hint_ar": "أكمل حقول SQL المحددة فقط؛ يُفحص كل حقل قبل فحص نتيجة الاستعلام.",
        "success_message": "Correct! Your completed read-only query returns the expected result.",
        "success_message_ar": "صحيح! يعيد استعلامك المكتمل للقراءة فقط النتيجة المتوقعة.",
    }


SQL_DEFINITIONS: dict[str, dict[str, Any]] = {
    "COURSE-017.M01.L02.EX01": _sql(
        """SELECT
    /* blank:1 */ ___ /* endblank */,
    /* blank:2 */ ___ /* endblank */ AS order_count
FROM orders
GROUP BY /* blank:3 */ ___ /* endblank */
ORDER BY customer_id;
""",
        [["customer_id"], ["COUNT(*)", "count(1)"], ["customer_id"]],
        """CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, order_amount REAL, order_status TEXT);
INSERT INTO orders VALUES
(1,1,20,'paid'),(2,1,15,'paid'),(3,2,8,'pending'),
(4,2,12,'paid'),(5,2,30,'paid'),(6,3,9,'refunded');""",
        ["customer_id", "order_count"], [[1, 2], [2, 3], [3, 1]],
        [("select the customer identifier.", "اختر معرّف العميل."),
         ("use a row-count aggregate.", "استخدم دالة تجميع لعد الصفوف."),
         ("group at customer grain.", "اجمع على مستوى العميل.")], ordered=True,
    ),
    "COURSE-017.M01.L03.EX01": _sql(
        """SELECT
    sales_year,
    SUM(CASE WHEN kind_of_business = 'Women' THEN /* blank:1 */ ___ /* endblank */ ELSE 0 END) AS womens_sales,
    SUM(CASE WHEN kind_of_business = 'Men' THEN /* blank:2 */ ___ /* endblank */ ELSE 0 END) AS mens_sales,
    ROUND(
        SUM(CASE WHEN kind_of_business = 'Women' THEN sales ELSE 0 END) * 1.0 /
        /* blank:3 */ ___ /* endblank */,
        2
    ) AS women_to_men_ratio
FROM retail_sales
GROUP BY /* blank:4 */ ___ /* endblank */
ORDER BY sales_year;
""",
        [["sales"], ["sales"], ["NULLIF(SUM(CASE WHEN kind_of_business = 'Men' THEN sales ELSE 0 END), 0)"], ["sales_year"]],
        """CREATE TABLE retail_sales(sales_year INTEGER, kind_of_business TEXT, sales REAL);
INSERT INTO retail_sales VALUES (2024,'Women',120),(2024,'Men',100),(2025,'Women',150),(2025,'Men',120);""",
        ["sales_year", "womens_sales", "mens_sales", "women_to_men_ratio"],
        [[2024, 120.0, 100.0, 1.2], [2025, 150.0, 120.0, 1.25]],
        [("sum the sales value for women’s stores.", "اجمع قيمة المبيعات لمتاجر النساء."),
         ("sum the sales value for men’s stores.", "اجمع قيمة المبيعات لمتاجر الرجال."),
         ("divide by the men’s total while protecting against zero.", "اقسم على إجمالي الرجال مع الحماية من الصفر."),
         ("group by year.", "اجمع حسب السنة.")], ordered=True,
    ),
    "COURSE-017.M01.L03.EX02": _sql(
        """SELECT
    c.month,
    /* blank:1 */ ___ /* endblank */ AS sales,
    SUM(COALESCE(s.sales, 0)) OVER (
        /* blank:2 */ ___ /* endblank */
        /* blank:3 */ ___ /* endblank */
    ) AS rolling_3_month_sales
FROM month_calendar AS c
/* blank:4 */ ___ /* endblank */ product_sales AS s ON s.month = c.month
ORDER BY c.month;
""",
        [["COALESCE(s.sales, 0)"], ["ORDER BY c.month"], ["ROWS BETWEEN 2 PRECEDING AND CURRENT ROW"], ["LEFT JOIN"]],
        """CREATE TABLE month_calendar(month TEXT); CREATE TABLE product_sales(month TEXT, sales REAL);
INSERT INTO month_calendar VALUES ('2026-01'),('2026-02'),('2026-03'),('2026-04');
INSERT INTO product_sales VALUES ('2026-01',10),('2026-03',30),('2026-04',20);""",
        ["month", "sales", "rolling_3_month_sales"],
        [["2026-01",10.0,10.0],["2026-02",0,10.0],["2026-03",30.0,40.0],["2026-04",20.0,50.0]],
        [("replace a missing month’s sales with zero.", "استبدل مبيعات الشهر المفقود بصفر."),
         ("order the window chronologically.", "رتب النافذة زمنيًا."),
         ("define a three-row window including the current month.", "حدد نافذة من ثلاثة صفوف تشمل الشهر الحالي."),
         ("preserve every calendar month.", "احتفظ بكل شهر في التقويم.")], ordered=True,
    ),
    "COURSE-017.M01.L04.EX01": _sql(
        """WITH cohort_activity AS (
    SELECT
        u.cohort_month,
        /* blank:1 */ ___ /* endblank */ AS period_number,
        /* blank:2 */ ___ /* endblank */ AS active_users
    FROM users AS u
    JOIN activity AS a ON /* blank:3 */ ___ /* endblank */
    GROUP BY u.cohort_month, period_number
), retention AS (
    SELECT *, MAX(CASE WHEN period_number = 0 THEN active_users END)
        OVER (PARTITION BY /* blank:4 */ ___ /* endblank */) AS cohort_size
    FROM cohort_activity
)
SELECT cohort_month, period_number, active_users,
       ROUND(active_users * 100.0 / /* blank:5 */ ___ /* endblank */, 1) AS retention_pct
FROM retention
ORDER BY cohort_month, period_number;
""",
        [["(CAST(strftime('%Y', a.activity_date) AS INTEGER) - CAST(substr(u.cohort_month,1,4) AS INTEGER)) * 12 + (CAST(strftime('%m', a.activity_date) AS INTEGER) - CAST(substr(u.cohort_month,6,2) AS INTEGER))"],
         ["COUNT(DISTINCT u.user_id)"], ["a.user_id = u.user_id"], ["cohort_month"], ["cohort_size"]],
        """CREATE TABLE users(user_id INTEGER, cohort_month TEXT); CREATE TABLE activity(user_id INTEGER, activity_date TEXT);
INSERT INTO users VALUES (1,'2026-01'),(2,'2026-01'),(3,'2026-02');
INSERT INTO activity VALUES (1,'2026-01-05'),(2,'2026-01-08'),(1,'2026-02-03'),(3,'2026-02-10'),(3,'2026-03-12');""",
        ["cohort_month","period_number","active_users","retention_pct"],
        [["2026-01",0,2,100.0],["2026-01",1,1,50.0],["2026-02",0,1,100.0],["2026-02",1,1,100.0]],
        [("calculate elapsed months from cohort month.", "احسب الأشهر المنقضية منذ شهر المجموعة."),
         ("count distinct active users.", "عد المستخدمين النشطين المميزين."),
         ("join activity to its user.", "اربط النشاط بالمستخدم الخاص به."),
         ("partition the baseline by cohort.", "قسّم خط الأساس حسب المجموعة."),
         ("use the cohort’s period-zero size as denominator.", "استخدم حجم الفترة صفر للمجموعة مقامًا.")], ordered=True,
    ),
    "COURSE-017.M01.L07.EX01": _sql(
        """SELECT
    a.variant,
    /* blank:1 */ ___ /* endblank */ AS assigned_users,
    /* blank:2 */ ___ /* endblank */ AS converted_users,
    ROUND(
        COUNT(DISTINCT CASE WHEN o.order_time >= a.assignment_time THEN a.user_id END) * 100.0 /
        /* blank:3 */ ___ /* endblank */,
        1
    ) AS conversion_rate
FROM experiment_assignment AS a
/* blank:4 */ ___ /* endblank */ orders AS o
  ON o.user_id = a.user_id AND /* blank:5 */ ___ /* endblank */
GROUP BY a.variant
ORDER BY a.variant;
""",
        [["COUNT(DISTINCT a.user_id)"], ["COUNT(DISTINCT CASE WHEN o.order_time >= a.assignment_time THEN a.user_id END)"],
         ["COUNT(DISTINCT a.user_id)"], ["LEFT JOIN"], ["o.order_time >= a.assignment_time"]],
        """CREATE TABLE experiment_assignment(user_id INTEGER, variant TEXT, assignment_time TEXT); CREATE TABLE orders(user_id INTEGER, order_time TEXT);
INSERT INTO experiment_assignment VALUES (1,'control','2026-01-01'),(2,'control','2026-01-01'),(3,'treatment','2026-01-01'),(4,'treatment','2026-01-01');
INSERT INTO orders VALUES (1,'2026-01-02'),(2,'2025-12-30'),(3,'2026-01-03');""",
        ["variant","assigned_users","converted_users","conversion_rate"],
        [["control",2,1,50.0],["treatment",2,1,50.0]],
        [("count every assigned user once.", "عد كل مستخدم مُعيَّن مرة واحدة."),
         ("count only users converting after assignment.", "عد فقط المستخدمين الذين حوّلوا بعد التعيين."),
         ("use all assigned users as denominator.", "استخدم جميع المستخدمين المعيّنين مقامًا."),
         ("keep non-converting assigned users.", "احتفظ بالمستخدمين المعيّنين غير المحوّلين."),
         ("enforce post-assignment orders in the join.", "اشترط أن يكون الطلب بعد التعيين في الربط.")], ordered=True,
    ),
    "COURSE-017.M01.L08.EX05": _sql(
        """SELECT
    a.course_id AS course_1,
    b.course_id AS course_2,
    /* blank:1 */ ___ /* endblank */ AS learners
FROM course_enrollments AS a
JOIN course_enrollments AS b
  ON /* blank:2 */ ___ /* endblank */
 AND /* blank:3 */ ___ /* endblank */
GROUP BY a.course_id, b.course_id
ORDER BY learners DESC, course_1, course_2;
""",
        [["COUNT(DISTINCT a.user_id)"], ["a.user_id = b.user_id"], ["b.course_id > a.course_id", "a.course_id < b.course_id"]],
        """CREATE TABLE course_enrollments(user_id INTEGER, course_id TEXT);
INSERT INTO course_enrollments VALUES (1,'SQL'),(1,'Stats'),(1,'BI'),(2,'SQL'),(2,'Stats'),(3,'SQL'),(3,'Python');""",
        ["course_1","course_2","learners"],
        [["SQL","Stats",2],["BI","SQL",1],["BI","Stats",1],["Python","SQL",1]],
        [("count distinct learners for each pair.", "عد المتعلمين المميزين لكل زوج."),
         ("join enrollments belonging to the same learner.", "اربط التسجيلات الخاصة بالمتعلم نفسه."),
         ("keep one ordering and exclude self-pairs.", "احتفظ بترتيب واحد واستبعد الأزواج الذاتية.")], ordered=True,
    ),
}


PYTHON_DEFINITIONS: dict[str, dict[str, Any]] = {
    "COURSE-018.M01.L03.EX01": {
        "starter_code": """true_positives = 180\nfalse_positives = 60\nfalse_negatives = 20\ntrue_negatives = 740\n\n# TODO: calculate each classification metric\nprecision = None\n# TODO\nrecall = None\n# TODO\naccuracy = None\n# TODO\nf1 = None\n""",
        "solution_code": """true_positives = 180\nfalse_positives = 60\nfalse_negatives = 20\ntrue_negatives = 740\n\nprecision = true_positives / (true_positives + false_positives)\nrecall = true_positives / (true_positives + false_negatives)\naccuracy = (true_positives + true_negatives) / (true_positives + false_positives + false_negatives + true_negatives)\nf1 = 2 * precision * recall / (precision + recall)\n""",
        "tests": [
            {"id":"precision","type":"value_approx","variable":"precision","expected":0.75,"feedback":{"en":"Recheck the precision denominator.","ar":"راجع مقام Precision."}},
            {"id":"recall","type":"value_approx","variable":"recall","expected":0.9,"feedback":{"en":"Recheck the recall denominator.","ar":"راجع مقام Recall."}},
            {"id":"accuracy","type":"value_approx","variable":"accuracy","expected":0.92,"feedback":{"en":"Accuracy uses all four confusion-matrix cells.","ar":"تستخدم Accuracy الخانات الأربع لمصفوفة الالتباس."}},
            {"id":"f1","type":"value_approx","variable":"f1","expected":0.8181818181818182,"feedback":{"en":"Compute the harmonic mean of precision and recall.","ar":"احسب المتوسط التوافقي لـ Precision وRecall."}},
        ],
    },
    "COURSE-018.M01.L05.EX01": {
        "starter_code": """class_counts = [8, 60, 12]\ntotal = sum(class_counts)\n# TODO: probability of each class\nprobabilities = None\n# TODO: index of the largest class count\npredicted_class = None\n# TODO: Gini impurity = 1 - sum(p^2)\ngini = None\n""",
        "solution_code": """class_counts = [8, 60, 12]\ntotal = sum(class_counts)\nprobabilities = [count / total for count in class_counts]\npredicted_class = max(range(len(class_counts)), key=lambda index: class_counts[index])\ngini = 1 - sum(probability ** 2 for probability in probabilities)\n""",
        "tests": [
            {"id":"probabilities","type":"value_equals","variable":"probabilities","expected":[0.1,0.75,0.15],"feedback":{"en":"Divide every class count by the leaf total.","ar":"اقسم عدد كل فئة على إجمالي الورقة."}},
            {"id":"prediction","type":"value_equals","variable":"predicted_class","expected":1,"feedback":{"en":"Predict the index with the largest count.","ar":"تنبأ بفهرس الفئة ذات العدد الأكبر."}},
            {"id":"gini","type":"value_approx","variable":"gini","expected":0.405,"feedback":{"en":"Use 1 minus the sum of squared probabilities.","ar":"استخدم 1 ناقص مجموع مربعات الاحتمالات."}},
        ],
    },
    "COURSE-018.M01.L05.EX02": {
        "starter_code": """from sklearn.datasets import make_moons\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.tree import DecisionTreeClassifier\n\n# TODO: create the requested noisy dataset\nX, y = None\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nunrestricted = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)\n# TODO: constrain depth and leaf size\nregularized = None\n# TODO: compare generalization on the held-out set\nregularized_generalizes_better = None\nregularized_limits_depth = regularized.get_depth() <= 5\nregularized_uses_leaf_floor = regularized.min_samples_leaf == 10\ntest_rows = len(X_test)\n""",
        "solution_code": """from sklearn.datasets import make_moons\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.tree import DecisionTreeClassifier\n\nX, y = make_moons(n_samples=1000, noise=0.3, random_state=42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nunrestricted = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)\nregularized = DecisionTreeClassifier(max_depth=5, min_samples_leaf=10, random_state=42).fit(X_train, y_train)\nregularized_generalizes_better = regularized.score(X_test, y_test) >= unrestricted.score(X_test, y_test)\nregularized_limits_depth = regularized.get_depth() <= 5\nregularized_uses_leaf_floor = regularized.min_samples_leaf == 10\ntest_rows = len(X_test)\n""",
        "tests": [
            {"id":"depth","type":"value_equals","variable":"regularized_limits_depth","expected":True,"feedback":{"en":"The regularized tree must limit max_depth to 5.","ar":"يجب أن تحد الشجرة المنتظمة max_depth إلى 5."}},
            {"id":"leaf","type":"value_equals","variable":"regularized_uses_leaf_floor","expected":True,"feedback":{"en":"Use min_samples_leaf=10.","ar":"استخدم min_samples_leaf=10."}},
            {"id":"split","type":"value_equals","variable":"test_rows","expected":200,"feedback":{"en":"Keep the requested 20% test split.","ar":"احتفظ بنسبة 20% المطلوبة لمجموعة الاختبار."}},
            {"id":"generalization","type":"value_equals","variable":"regularized_generalizes_better","expected":True,"feedback":{"en":"Compare held-out accuracy, not training accuracy.","ar":"قارن دقة مجموعة الاختبار لا دقة التدريب."}},
        ],
    },
    "COURSE-018.M01.L07.EX01": {
        "starter_code": """import numpy as np\nfrom sklearn.datasets import load_iris\nfrom sklearn.decomposition import PCA\nfrom sklearn.preprocessing import StandardScaler\n\nX = load_iris().data\nX_scaled = StandardScaler().fit_transform(X)\nprobe = PCA().fit(X_scaled)\n# TODO: cumulative explained variance\ncumulative_variance = None\n# TODO: smallest component count reaching 95%\ncomponents_95 = None\n# TODO: fit and transform with the selected count\nX_reduced = None\n# TODO: reconstruct the first five samples\nX_reconstructed = None\nreduced_shape = list(X_reduced.shape)\ncompression_ratio = X_reduced.shape[1] / X_scaled.shape[1]\nreconstruction_shape = list(X_reconstructed.shape)\n""",
        "solution_code": """import numpy as np\nfrom sklearn.datasets import load_iris\nfrom sklearn.decomposition import PCA\nfrom sklearn.preprocessing import StandardScaler\n\nX = load_iris().data\nX_scaled = StandardScaler().fit_transform(X)\nprobe = PCA().fit(X_scaled)\ncumulative_variance = np.cumsum(probe.explained_variance_ratio_)\ncomponents_95 = int(np.argmax(cumulative_variance >= 0.95) + 1)\npca = PCA(n_components=components_95).fit(X_scaled)\nX_reduced = pca.transform(X_scaled)\nX_reconstructed = pca.inverse_transform(X_reduced[:5])\nreduced_shape = list(X_reduced.shape)\ncompression_ratio = X_reduced.shape[1] / X_scaled.shape[1]\nreconstruction_shape = list(X_reconstructed.shape)\n""",
        "tests": [
            {"id":"components","type":"value_equals","variable":"components_95","expected":2,"feedback":{"en":"Choose the first cumulative-variance index reaching 0.95, then add one.","ar":"اختر أول فهرس للتباين التراكمي يبلغ 0.95 ثم أضف واحدًا."}},
            {"id":"shape","type":"value_equals","variable":"reduced_shape","expected":[150,2],"feedback":{"en":"Transform all 150 rows with the selected PCA model.","ar":"حوّل الصفوف الـ150 كلها باستخدام نموذج PCA المختار."}},
            {"id":"ratio","type":"value_approx","variable":"compression_ratio","expected":0.5,"feedback":{"en":"Compression ratio is reduced features divided by original features.","ar":"نسبة الضغط هي عدد الخصائص المختزلة مقسومًا على الأصلية."}},
            {"id":"inverse","type":"value_equals","variable":"reconstruction_shape","expected":[5,4],"feedback":{"en":"Inverse-transform the first five reduced samples.","ar":"نفّذ inverse_transform لأول خمس عينات مختزلة."}},
        ],
    },
}


def apply_deterministic_course_exercises(course: CourseSpec) -> None:
    definitions = {**SQL_DEFINITIONS, **PYTHON_DEFINITIONS}
    for lesson in course.lessons:
        for exercise in lesson.exercises:
            definition = definitions.get(exercise.exercise_id)
            if not definition:
                continue
            exercise.exercise_type = definition.get("exercise_type", "code")
            exercise.language = definition.get("language", "python")
            exercise.starter_code = definition["starter_code"]
            exercise.solution_code = definition["solution_code"]
            exercise.tests = list(definition["tests"])
            exercise.hint = definition.get("hint") or "Complete the missing expressions, then run the deterministic checks."
            exercise.hint_ar = definition.get("hint_ar") or "أكمل التعبيرات الناقصة ثم شغّل الفحوص الحتمية."
            exercise.success_message = definition.get("success_message") or "Correct! The completed code satisfies every deterministic check."
            exercise.success_message_ar = definition.get("success_message_ar") or "صحيح! يحقق الكود المكتمل كل الفحوص الحتمية."
