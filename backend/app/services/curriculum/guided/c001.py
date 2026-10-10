"""COURSE-001 Machine Learning: guided implementation exercises."""
from . import Guided, check

EXERCISES = {
    "COURSE-001.M03.L01.EX01": Guided(
        goal=(
            "Scale two features that live on very different ranges, learning the scaling only from the training data.",
            "وحّد مقياس خاصيتين تختلف نطاقاتهما كثيرًا، مع تعلّم معاملات التوحيد من بيانات التدريب فقط.",
        ),
        steps=(
            ("Create a `StandardScaler` object.", "أنشئ كائن `StandardScaler`."),
            ("Fit it on `X_train` and transform `X_train` in one call with `fit_transform`.",
             "طبّقه على `X_train` وحوّل `X_train` في استدعاء واحد باستخدام `fit_transform`."),
            ("Transform `X_test` with the same fitted scaler. Do not fit it again.",
             "حوّل `X_test` بالكائن نفسه بعد تدريبه، ولا تعِد تدريبه على بيانات الاختبار."),
            ("Click Run to compare the printed ranges, then Check answer.",
             "اضغط «تشغيل» لمقارنة النطاقات المطبوعة، ثم «تحقّق من الإجابة»."),
        ),
        starter='''import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Two features on very different scales: age (years) and yearly income (dollars)
X = np.array([
    [25, 32000], [32, 45000], [47, 88000], [51, 62000], [62, 120000],
    [23, 28000], [36, 51000], [44, 75000], [58, 98000], [29, 39000],
], dtype=float)
y = np.array([0, 0, 1, 1, 1, 0, 0, 1, 1, 0])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Step 1: Create the scaler
scaler = ___

# Step 2: Learn the mean and standard deviation from the TRAINING data, then scale it
X_train_scaled = ___

# Step 3: Scale the test data with the SAME fitted scaler (transform only)
X_test_scaled = ___

print("Training ranges (min, max):", X_train.min(axis=0).tolist(), X_train.max(axis=0).tolist())
print("Scaled training means:", X_train_scaled.mean(axis=0).round(3))
print("Scaled training std:  ", X_train_scaled.std(axis=0).round(3))
''',
        answers=("StandardScaler()", "scaler.fit_transform(X_train)", "scaler.transform(X_test)"),
        checks=(
            check("hasattr(scaler, 'fit') and hasattr(scaler, 'transform')", True,
                  "Blank 1: create a scaler object, for example `StandardScaler()`.",
                  "الفراغ 1: أنشئ كائن توحيد، مثل `StandardScaler()`."),
            check("bool(np.allclose(X_train_scaled, type(scaler)().fit(X_train).transform(X_train)))", True,
                  "Blank 2: fit the scaler on `X_train` and transform `X_train` in one step with `fit_transform`.",
                  "الفراغ 2: درّب الكائن على `X_train` وحوّل `X_train` في خطوة واحدة باستخدام `fit_transform`."),
            check("bool(np.allclose(X_test_scaled, type(scaler)().fit(X_train).transform(X_test)))", True,
                  "Blank 3: use `transform` on `X_test` with the scaler fitted on training data. Fitting again on the test set would use statistics the model must never see.",
                  "الفراغ 3: استخدم `transform` على `X_test` بالكائن المدرَّب على بيانات التدريب. إعادة التدريب على بيانات الاختبار تستخدم إحصاءات يجب ألا يراها النموذج."),
        ),
        hints=(
            ("A scaler is created like any scikit-learn object: call its class with parentheses.",
             "يُنشأ كائن التوحيد مثل أي كائن في scikit-learn: استدعِ اسم الصنف مع قوسين."),
            ("`fit_transform` learns the statistics and applies them in one call; use it only on training data.",
             "يتعلّم `fit_transform` الإحصاءات ويطبّقها في استدعاء واحد؛ استخدمه على بيانات التدريب فقط."),
            ("For the test set, call `scaler.transform(X_test)` so it is scaled with the training mean and standard deviation.",
             "لبيانات الاختبار استدعِ `scaler.transform(X_test)` لتُوحَّد بمتوسط بيانات التدريب وانحرافها المعياري."),
        ),
        success=(
            "Well done! The scaler learned its statistics from the training data only and applied exactly the same transformation to the test data.",
            "أحسنت! تعلّم كائن التوحيد إحصاءاته من بيانات التدريب فقط، وطبّق التحويل نفسه تمامًا على بيانات الاختبار.",
        ),
        expected=(
            "Scaled training features with a mean close to 0 and a standard deviation close to 1, and test features scaled with the training statistics.",
            "خصائص تدريب موحَّدة متوسطها قريب من 0 وانحرافها المعياري قريب من 1، وخصائص اختبار موحَّدة بإحصاءات التدريب.",
        ),
        reflect=(
            "Why would fitting a second scaler on `X_test` make the evaluation inconsistent?",
            "لماذا يجعل تدريب كائن توحيد ثانٍ على `X_test` عملية التقييم غير متّسقة؟",
        ),
    ),
    "COURSE-001.M04.L01.EX02": Guided(
        goal=(
            "Turn a raw timestamp into features a linear model can use to predict bike rentals.",
            "حوّل طابعًا زمنيًا خامًا إلى خصائص يستطيع نموذج خطي استخدامها للتنبؤ بعدد الدراجات المستأجرة.",
        ),
        steps=(
            ("Extract the hour of the day from `timestamp` with the `.dt` accessor.",
             "استخرج ساعة اليوم من `timestamp` باستخدام الواصف `.dt`."),
            ("Extract the day of the week (Monday = 0, Sunday = 6).",
             "استخرج يوم الأسبوع (الاثنين = 0، الأحد = 6)."),
            ("Create `is_weekend`: 1 for Saturday or Sunday, 0 otherwise.",
             "أنشئ `is_weekend`: القيمة 1 ليومي السبت والأحد، و0 لغيرهما."),
            ("One-hot encode `day_of_week` with `pd.get_dummies` so the model treats it as a category.",
             "رمّز `day_of_week` بطريقة One-hot باستخدام `pd.get_dummies` ليعامله النموذج كفئة."),
        ),
        starter='''import pandas as pd

rentals = pd.DataFrame({
    "timestamp": pd.to_datetime([
        "2026-03-02 08:00", "2026-03-02 17:00", "2026-03-07 11:00",
        "2026-03-08 15:00", "2026-03-09 08:00", "2026-03-14 13:00",
    ]),
    "rentals": [310, 420, 180, 210, 295, 230],
})

# Step 1: Hour of the day (0-23)
rentals["hour"] = ___

# Step 2: Day of the week (Monday=0 ... Sunday=6)
rentals["day_of_week"] = ___

# Step 3: 1 on Saturday/Sunday (day_of_week 5 or 6), otherwise 0
rentals["is_weekend"] = ___

# Step 4: One-hot encode day_of_week so a linear model sees categories, not a ranking
features = ___

print(features.drop(columns=["timestamp"]))
''',
        answers=(
            'rentals["timestamp"].dt.hour',
            'rentals["timestamp"].dt.dayofweek',
            '(rentals["day_of_week"] >= 5).astype(int)',
            'pd.get_dummies(rentals, columns=["day_of_week"])',
        ),
        checks=(
            check("rentals['hour'].tolist()", [8, 17, 11, 15, 8, 13],
                  "Blank 1: take the hour from the timestamp column, e.g. `rentals[\"timestamp\"].dt.hour`.",
                  "الفراغ 1: خذ الساعة من عمود الطابع الزمني، مثل `rentals[\"timestamp\"].dt.hour`."),
            check("rentals['day_of_week'].tolist()", [0, 0, 5, 6, 0, 5],
                  "Blank 2: use `.dt.dayofweek`, which counts Monday as 0 and Sunday as 6.",
                  "الفراغ 2: استخدم `.dt.dayofweek` الذي يعدّ الاثنين 0 والأحد 6."),
            check("[int(value) for value in rentals['is_weekend']]", [0, 0, 1, 1, 0, 1],
                  "Blank 3: a day is a weekend when `day_of_week` is 5 or 6; convert the comparison to 0/1.",
                  "الفراغ 3: يكون اليوم عطلة نهاية أسبوع عندما يكون `day_of_week` يساوي 5 أو 6؛ حوّل نتيجة المقارنة إلى 0 أو 1."),
            check("sorted(str(c) for c in features.columns if str(c).startswith('day_of_week_'))",
                  ["day_of_week_0", "day_of_week_5", "day_of_week_6"],
                  "Blank 4: call `pd.get_dummies` with `columns=[\"day_of_week\"]` so each day becomes its own 0/1 column.",
                  "الفراغ 4: استدعِ `pd.get_dummies` مع `columns=[\"day_of_week\"]` ليصبح كل يوم عمودًا مستقلًا بقيم 0 أو 1."),
            check("len(features)", 6,
                  "Blank 4: keep all six rows; encoding adds columns, it never removes rows.",
                  "الفراغ 4: احتفظ بالصفوف الستة؛ الترميز يضيف أعمدة ولا يحذف صفوفًا."),
        ),
        hints=(
            ("A datetime column exposes its parts through `.dt`, for example `.dt.hour`.",
             "يكشف عمود التاريخ والوقت أجزاءه عبر `.dt`، مثل `.dt.hour`."),
            ("A comparison such as `rentals[\"day_of_week\"] >= 5` gives True/False; `.astype(int)` turns it into 1/0.",
             "تعطي مقارنة مثل `rentals[\"day_of_week\"] >= 5` القيم True/False، ويحوّلها `.astype(int)` إلى 1/0."),
            ("`pd.get_dummies(rentals, columns=[\"day_of_week\"])` replaces the column with one indicator column per day.",
             "يستبدل `pd.get_dummies(rentals, columns=[\"day_of_week\"])` العمود بعمود مؤشر لكل يوم."),
        ),
        success=(
            "Great work! The timestamp is now hour, weekday and weekend features, with the weekday one-hot encoded so the linear model can learn a separate effect for each day.",
            "عمل رائع! أصبح الطابع الزمني خصائص للساعة ويوم الأسبوع وعطلة نهاية الأسبوع، مع ترميز يوم الأسبوع بطريقة One-hot ليتعلّم النموذج الخطي أثرًا مستقلًا لكل يوم.",
        ),
        expected=(
            "A `features` table with `hour`, `is_weekend` and one `day_of_week_*` indicator column per weekday that appears in the data.",
            "جدول `features` يحتوي على `hour` و`is_weekend` وعمود مؤشر `day_of_week_*` لكل يوم أسبوع يظهر في البيانات.",
        ),
        reflect=(
            "Why do raw future timestamps confuse a tree model trained only on earlier dates, and which extra feature (such as weather or holidays) could explain unusual demand?",
            "لماذا تُربك الطوابع الزمنية المستقبلية الخام نموذج الشجرة المدرَّب على تواريخ سابقة فقط؟ وما الخاصية الإضافية (مثل الطقس أو العطلات) التي قد تفسّر طلبًا غير معتاد؟",
        ),
    ),
    "COURSE-001.M05.L01.EX01": Guided(
        goal=(
            "Tune an RBF SVC with five-fold GridSearchCV on the training data, then evaluate it once on the untouched test set.",
            "اضبط نموذج SVC بنواة RBF باستخدام GridSearchCV بخمسة أجزاء على بيانات التدريب، ثم قيّمه مرة واحدة على بيانات الاختبار التي لم تُمس.",
        ),
        steps=(
            ("Write a parameter grid with two values for `C` and two for `gamma`.",
             "اكتب شبكة معاملات فيها قيمتان لـ `C` وقيمتان لـ `gamma`."),
            ("Create a `GridSearchCV` around `SVC(kernel=\"rbf\")` with `cv=5`.",
             "أنشئ `GridSearchCV` حول `SVC(kernel=\"rbf\")` مع `cv=5`."),
            ("Fit the search on the training data only.", "درّب البحث على بيانات التدريب فقط."),
            ("Score the fitted search once on the test data.", "قيّم البحث المدرَّب مرة واحدة على بيانات الاختبار."),
        ),
        starter='''from sklearn.datasets import load_iris
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.svm import SVC

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Step 1: Two values for C and two for gamma (4 combinations)
param_grid = ___

# Step 2: A five-fold search over an RBF SVC
grid = ___

# Step 3: Search using the TRAINING data only
___

# Step 4: Evaluate the chosen model once on the untouched test set
test_score = ___

print("Best parameters:", grid.best_params_)
print("Best cross-validation score:", round(grid.best_score_, 3))
print("Test score:", round(test_score, 3))
''',
        answers=(
            '{"C": [0.1, 10], "gamma": [0.01, 1]}',
            'GridSearchCV(SVC(kernel="rbf"), param_grid, cv=5)',
            "grid.fit(X_train, y_train)",
            "grid.score(X_test, y_test)",
        ),
        checks=(
            check("isinstance(param_grid, dict) and len(param_grid.get('C', [])) >= 2 and len(param_grid.get('gamma', [])) >= 2", True,
                  "Blank 1: write a dictionary with keys \"C\" and \"gamma\", each holding a list of at least two values.",
                  "الفراغ 1: اكتب قاموسًا بالمفتاحين \"C\" و\"gamma\"، ولكل منهما قائمة من قيمتين على الأقل."),
            check("grid.estimator.kernel", "rbf",
                  "Blank 2: wrap `SVC(kernel=\"rbf\")` in `GridSearchCV` together with `param_grid`.",
                  "الفراغ 2: ضع `SVC(kernel=\"rbf\")` داخل `GridSearchCV` مع `param_grid`."),
            check("grid.n_splits_", 5,
                  "Blank 2/3: use `cv=5` and call `fit` so the five-fold search actually runs.",
                  "الفراغان 2 و3: استخدم `cv=5` واستدعِ `fit` حتى يُنفَّذ البحث بخمسة أجزاء فعلًا."),
            check("int(grid.best_estimator_.shape_fit_[0]) == len(X_train)", True,
                  "Blank 3: fit the search on `X_train` and `y_train` only. The test set must stay unseen.",
                  "الفراغ 3: درّب البحث على `X_train` و`y_train` فقط. يجب أن تبقى بيانات الاختبار غير مرئية."),
            check("abs(test_score - grid.score(X_test, y_test)) < 1e-9", True,
                  "Blank 4: score the fitted search on `X_test` and `y_test`.",
                  "الفراغ 4: قيّم البحث المدرَّب على `X_test` و`y_test`."),
        ),
        hints=(
            ("A parameter grid is a dictionary: parameter name → list of values to try.",
             "شبكة المعاملات قاموس: اسم المعامل ← قائمة القيم المراد تجربتها."),
            ("`GridSearchCV(estimator, param_grid, cv=5)` builds the search; nothing runs until you call `.fit(...)`.",
             "ينشئ `GridSearchCV(estimator, param_grid, cv=5)` البحث، ولا يُنفَّذ شيء حتى تستدعي `.fit(...)`."),
            ("After fitting, `grid.score(X_test, y_test)` uses the best model found during the search.",
             "بعد التدريب يستخدم `grid.score(X_test, y_test)` أفضل نموذج عُثر عليه أثناء البحث."),
        ),
        success=(
            "Correct! Model selection used only cross-validation on the training data, and the test set gave one independent final score.",
            "صحيح! اعتمد اختيار النموذج على التحقق المتقاطع داخل بيانات التدريب فقط، وأعطت بيانات الاختبار نتيجة نهائية مستقلة واحدة.",
        ),
        expected=(
            "The best parameters, the best cross-validation score and one final test score are printed.",
            "طباعة أفضل المعاملات وأفضل نتيجة للتحقق المتقاطع ونتيجة اختبار نهائية واحدة.",
        ),
        reflect=(
            "Why would repeatedly changing the parameter ranges after looking at the test score make that score unreliable?",
            "لماذا يصبح تقدير الاختبار غير موثوق إذا عدّلت نطاقات المعاملات مرارًا بعد النظر إليه؟",
        ),
    ),
    "COURSE-001.M06.L01.EX01": Guided(
        goal=(
            "Chain scaling and logistic regression in one Pipeline so the test data is scaled with training statistics automatically.",
            "اربط التوحيد والانحدار اللوجستي في Pipeline واحد كي تُوحَّد بيانات الاختبار تلقائيًا بإحصاءات التدريب.",
        ),
        steps=(
            ("Put a scaler that standardizes each feature (mean 0, standard deviation 1) as the first step of the pipeline.",
             "ضع أداة توحيد تجعل لكل feature متوسطًا 0 وانحرافًا معياريًا 1 خطوةً أولى في الـ Pipeline."),
            ("Fit the whole pipeline on the unscaled training data.",
             "درّب الـ Pipeline كاملًا على بيانات التدريب غير الموحَّدة."),
            ("Score the pipeline directly on the unscaled test data.",
             "قيّم الـ Pipeline مباشرة على بيانات الاختبار غير الموحَّدة."),
        ),
        starter='''from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Step 1: The scaler runs first, then the classifier
pipe = Pipeline([
    ("scaler", ___),
    ("model", LogisticRegression(max_iter=1000)),
])

# Step 2: Fit the whole pipeline on the UNSCALED training data
___

# Step 3: Score on the unscaled test data - the pipeline scales it for you
test_score = ___

print("Test accuracy:", round(test_score, 3))
''',
        answers=("StandardScaler()", "pipe.fit(X_train, y_train)", "pipe.score(X_test, y_test)"),
        checks=(
            check("hasattr(pipe.named_steps['scaler'], 'transform')", True,
                  "Blank 1: the first step must be a scaler object such as `StandardScaler()`.",
                  "الفراغ 1: يجب أن تكون الخطوة الأولى كائن توحيد مثل `StandardScaler()`."),
            check("int(pipe.named_steps['scaler'].n_samples_seen_) == len(X_train)", True,
                  "Blank 2: call `pipe.fit(X_train, y_train)` so the scaler learns from the training rows only.",
                  "الفراغ 2: استدعِ `pipe.fit(X_train, y_train)` ليتعلّم كائن التوحيد من صفوف التدريب فقط."),
            check("abs(test_score - pipe.score(X_test, y_test)) < 1e-9", True,
                  "Blank 3: call `pipe.score(X_test, y_test)` on the raw test data; do not scale it yourself.",
                  "الفراغ 3: استدعِ `pipe.score(X_test, y_test)` على بيانات الاختبار الخام؛ لا توحّدها بنفسك."),
        ),
        hints=(
            ("Each pipeline step is a `(name, object)` pair; the object here is scikit-learn's scaler that standardizes each feature.",
             "كل خطوة في الـ Pipeline زوج `(name, object)`؛ والكائن هنا هو أداة scikit-learn التي توحّد مقياس كل feature."),
            ("A pipeline is fitted like a model: `pipe.fit(X_train, y_train)`.",
             "يُدرَّب الـ Pipeline مثل النموذج: `pipe.fit(X_train, y_train)`."),
            ("`pipe.score` transforms `X_test` with the fitted scaler before predicting, so pass the raw test data.",
             "يحوّل `pipe.score` البيانات `X_test` بكائن التوحيد المدرَّب قبل التنبؤ، لذا مرّر بيانات الاختبار الخام."),
        ),
        success=(
            "Correct! The scaler learned only from the training data during `fit`, and `score` reused those statistics on the test data for you.",
            "صحيح! تعلّم كائن التوحيد من بيانات التدريب فقط أثناء `fit`، وأعاد `score` استخدام تلك الإحصاءات على بيانات الاختبار نيابةً عنك.",
        ),
        expected=(
            "A fitted pipeline and its test accuracy (about 0.96).",
            "Pipeline مدرَّب ودقته على بيانات الاختبار (نحو 0.96).",
        ),
        reflect=(
            "Which step learns the scaling parameters, and why should you not transform `X_test` yourself before `pipe.score`?",
            "أي خطوة تتعلّم معاملات التوحيد؟ ولماذا لا يجب أن تحوّل `X_test` بنفسك قبل `pipe.score`؟",
        ),
    ),
    "COURSE-001.M06.L01.EX02": Guided(
        goal=(
            "Fix a leaky workflow by moving feature selection inside a Pipeline, so it is re-fitted inside every cross-validation fold.",
            "أصلح سير عمل يسرّب المعلومات بنقل اختيار الخصائص إلى داخل Pipeline، كي يُعاد تدريبه داخل كل جزء من أجزاء التحقق المتقاطع.",
        ),
        steps=(
            ("Make `SelectPercentile` (scored with `f_regression`) the first pipeline step.",
             "اجعل `SelectPercentile` (مع دالة التقييم `f_regression`) الخطوة الأولى في الـ Pipeline."),
            ("Add the Ridge `alpha` to the grid. Pipeline parameters are named `<step>__<parameter>`.",
             "أضف المعامل `alpha` الخاص بـ Ridge إلى الشبكة. تُسمّى معاملات الـ Pipeline بالصيغة `<step>__<parameter>`."),
            ("Create a five-fold `GridSearchCV` over the whole pipeline.",
             "أنشئ `GridSearchCV` بخمسة أجزاء على الـ Pipeline كاملًا."),
        ),
        starter='''from sklearn.datasets import make_regression
from sklearn.feature_selection import SelectPercentile, f_regression
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline

X, y = make_regression(n_samples=200, n_features=50, n_informative=5, noise=10, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Step 1: Feature selection goes INSIDE the pipeline, before the model
pipe = Pipeline([
    ("select", ___),
    ("ridge", Ridge()),
])

# Step 2: Search both steps; names follow "<step name>__<parameter>"
param_grid = {
    "select__percentile": [10, 50],
    ___: [0.1, 10.0],
}

# Step 3: Cross-validate the WHOLE pipeline
grid = ___
grid.fit(X_train, y_train)

print("Best parameters:", grid.best_params_)
print("Test R^2:", round(grid.score(X_test, y_test), 3))
''',
        answers=(
            "SelectPercentile(score_func=f_regression)",
            '"ridge__alpha"',
            "GridSearchCV(pipe, param_grid, cv=5)",
        ),
        checks=(
            check("hasattr(pipe.named_steps['select'], 'get_support') and pipe.named_steps['select'].score_func is f_regression", True,
                  "Blank 1: use `SelectPercentile(score_func=f_regression)`; `f_regression` scores features for a numeric target.",
                  "الفراغ 1: استخدم `SelectPercentile(score_func=f_regression)`؛ فالدالة `f_regression` تقيّم الخصائص لهدف رقمي."),
            check("sorted(grid.param_grid) if isinstance(grid.param_grid, dict) else None", ["ridge__alpha", "select__percentile"],
                  "Blank 2: name the Ridge parameter `\"ridge__alpha\"` - the step name, two underscores, then the parameter.",
                  "الفراغ 2: سمِّ معامل Ridge بالاسم `\"ridge__alpha\"` - اسم الخطوة ثم شرطتان سفليتان ثم اسم المعامل."),
            check("grid.estimator is pipe and grid.n_splits_ == 5", True,
                  "Blank 3: search over `pipe` itself (not Ridge alone) with `cv=5`, so selection is re-fitted in every fold.",
                  "الفراغ 3: ابحث على `pipe` نفسه (لا على Ridge وحده) مع `cv=5`، كي يُعاد اختيار الخصائص في كل جزء."),
        ),
        hints=(
            ("`SelectPercentile` takes the scoring function as `score_func=`; for regression use `f_regression`.",
             "يأخذ `SelectPercentile` دالة التقييم عبر `score_func=`؛ وفي الانحدار استخدم `f_regression`."),
            ("The existing key `\"select__percentile\"` shows the pattern: step name + `__` + parameter.",
             "يوضّح المفتاح الموجود `\"select__percentile\"` النمط: اسم الخطوة + `__` + اسم المعامل."),
            ("Pass the pipeline, the grid and `cv=5` to `GridSearchCV`.",
             "مرّر الـ Pipeline والشبكة و`cv=5` إلى `GridSearchCV`."),
        ),
        success=(
            "Correct! Feature selection now happens inside every fold, so each validation score is computed on data the selector never saw.",
            "صحيح! أصبح اختيار الخصائص يحدث داخل كل جزء، فتُحسب كل نتيجة تحقق على بيانات لم يرها أداة الاختيار.",
        ),
        expected=(
            "The best `select__percentile` and `ridge__alpha` combination and the test R² of the refitted pipeline.",
            "أفضل تركيبة من `select__percentile` و`ridge__alpha`، وقيمة R² على بيانات الاختبار للـ Pipeline بعد إعادة تدريبه.",
        ),
        reflect=(
            "Where did the original workflow leak information, and why does the corrected search need more computation?",
            "أين كان سير العمل الأصلي يسرّب المعلومات؟ ولماذا يحتاج البحث المصحَّح إلى حسابات أكثر؟",
        ),
    ),
    "COURSE-001.M07.L01.EX01": Guided(
        goal=(
            "Build a TF-IDF + logistic regression text classifier, compare unigrams with bigrams, and read which words the model trusts most.",
            "ابنِ مصنّف نصوص من TF-IDF والانحدار اللوجستي، وقارن الكلمات المفردة بالثنائيات، واقرأ الكلمات التي يثق بها النموذج أكثر.",
        ),
        steps=(
            ("Put a vectorizer that turns texts into TF-IDF features before the classifier.", "ضع أداة تحوّل النصوص إلى features من نوع TF-IDF قبل المصنّف."),
            ("Give the grid two n-gram ranges: unigrams `(1, 1)` and unigrams + bigrams `(1, 2)`.",
             "أعطِ الشبكة نطاقين للـ n-gram: المفردات `(1, 1)` والمفردات مع الثنائيات `(1, 2)`."),
            ("Score the best pipeline on the held-out test texts.", "قيّم أفضل Pipeline على نصوص الاختبار المحجوزة."),
            ("Select the indices of the three largest positive weights.", "اختر فهارس أكبر ثلاثة أوزان موجبة."),
        ),
        starter='''from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline

train_texts = [
    "great battery and great screen", "love this phone", "works perfectly, highly recommend",
    "excellent value for money", "fast delivery and great quality", "really happy with it",
    "terrible battery life", "broke after one week", "not worth the money",
    "screen stopped working", "very poor quality", "would not recommend",
]
train_labels = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
test_texts = ["great quality, love it", "poor battery, not happy", "highly recommend this", "stopped working fast"]
test_labels = [1, 0, 1, 0]

# Step 1: Turn text into TF-IDF features, then classify
pipe = make_pipeline(___, LogisticRegression())

# Step 2: Compare unigrams with unigrams + bigrams
param_grid = {"tfidfvectorizer__ngram_range": ___}

grid = GridSearchCV(pipe, param_grid, cv=3)
grid.fit(train_texts, train_labels)
print("Best n-gram range:", grid.best_params_)

# Step 3: Evaluate once on the held-out test texts
test_accuracy = ___
print("Test accuracy:", test_accuracy)

# Step 4: Which features push a review most strongly towards "positive"?
vectorizer = grid.best_estimator_.named_steps["tfidfvectorizer"]
model = grid.best_estimator_.named_steps["logisticregression"]
vocabulary = vectorizer.get_feature_names_out()
order = model.coef_[0].argsort()  # feature indices, most negative weight first
top_negative = vocabulary[order[:3]].tolist()
top_positive = vocabulary[___].tolist()
print("Most negative:", top_negative)
print("Most positive:", top_positive)
''',
        answers=("TfidfVectorizer()", "[(1, 1), (1, 2)]", "grid.score(test_texts, test_labels)", "order[-3:]"),
        checks=(
            check("hasattr(grid.best_estimator_.named_steps.get('tfidfvectorizer'), 'vocabulary_')", True,
                  "Blank 1: the first step must be `TfidfVectorizer()` (its step name is then `tfidfvectorizer`).",
                  "الفراغ 1: يجب أن تكون الخطوة الأولى `TfidfVectorizer()` (فيصبح اسم خطوتها `tfidfvectorizer`)."),
            check("sorted(tuple(r) for r in grid.param_grid['tfidfvectorizer__ngram_range'])", [[1, 1], [1, 2]],
                  "Blank 2: give a list of two tuples, `[(1, 1), (1, 2)]`.",
                  "الفراغ 2: أعطِ قائمة من صفّين (tuples): `[(1, 1), (1, 2)]`."),
            check("abs(test_accuracy - grid.score(test_texts, test_labels)) < 1e-9", True,
                  "Blank 3: score the fitted search on `test_texts` and `test_labels`.",
                  "الفراغ 3: قيّم البحث المدرَّب على `test_texts` و`test_labels`."),
            check("sorted(top_positive) == sorted(vocabulary[model.coef_[0].argsort()[-3:]].tolist())", True,
                  "Blank 4: `order` runs from most negative to most positive, so take its last three indices: `order[-3:]`.",
                  "الفراغ 4: يبدأ `order` بالأكثر سلبية وينتهي بالأكثر إيجابية، لذا خذ آخر ثلاثة فهارس: `order[-3:]`."),
        ),
        hints=(
            ("`make_pipeline` names each step after its class in lowercase, which is why the grid key starts with `tfidfvectorizer__`.",
             "يسمّي `make_pipeline` كل خطوة باسم صنفها بأحرف صغيرة، ولهذا يبدأ مفتاح الشبكة بـ `tfidfvectorizer__`."),
            ("An n-gram range is a tuple `(min_n, max_n)`; the grid needs a list of the ranges to compare.",
             "نطاق الـ n-gram صفّ `(min_n, max_n)`؛ وتحتاج الشبكة قائمة بالنطاقات المراد مقارنتها."),
            ("`argsort` sorts ascending, so the most positive weights are at the end of `order`.",
             "يرتّب `argsort` تصاعديًا، لذا تقع الأوزان الأكثر إيجابية في نهاية `order`."),
        ),
        success=(
            "Well done! The whole text pipeline was tuned with cross-validation, tested once, and its largest weights show which words and phrases signal a positive review.",
            "أحسنت! ضُبط الـ Pipeline النصي كاملًا بالتحقق المتقاطع واختُبر مرة واحدة، وتكشف أكبر أوزانه الكلمات والعبارات التي تشير إلى مراجعة إيجابية.",
        ),
        expected=(
            "The best n-gram range, the test accuracy, and the three most negative and most positive features.",
            "أفضل نطاق n-gram، ودقة الاختبار، وأكثر ثلاث خصائص سلبية وأكثر ثلاث خصائص إيجابية.",
        ),
        reflect=(
            "Pick one phrase-level feature that is genuinely useful and one that could mislead the model on new reviews.",
            "اختر خاصية على مستوى العبارة مفيدة حقًا، وأخرى قد تضلّل النموذج عند مراجعات جديدة.",
        ),
    ),
}
