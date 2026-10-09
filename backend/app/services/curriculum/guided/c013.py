"""COURSE-013 Applied Data Analysis with Python: guided implementation exercises.

Analysis with pandas, NumPy, SciPy and scikit-learn runs in the practice
sandbox. Plotting, file and network I/O, and libraries the sandbox does not
install (statsmodels, XGBoost, Keras, Transformers) are checked by reading the
code.
"""
from . import Guided, check

READ_NOTE = (
    "This code draws charts, touches files or the network, or uses a library the sandbox does not install, so Check answer reads your code instead of running it. Run it locally to see the result.",
    "يرسم هذا الكود مخططات، أو يتعامل مع الملفات أو الشبكة، أو يستخدم مكتبة غير مثبّتة في بيئة التدريب، لذلك يقرأ «تحقّق من الإجابة» الكود بدل تشغيله. شغّله محليًا لترى النتيجة.",
)

EXERCISES = {
    "COURSE-013.M02.L01.EX01": Guided(
        goal=("Build one connected NumPy workflow: reshape an array, select rows and values from it, compute on it without loops, and inspect it.",
              "ابنِ سير عمل واحدًا مترابطًا في NumPy: أعد تشكيل مصفوفة، واختر منها صفوفًا وقيمًا، واحسب عليها دون حلقات، وافحصها."),
        steps=(
            ("Reshape the 24 integers into 6 rows and 4 columns.", "أعد تشكيل الأعداد الصحيحة الأربعة والعشرين في 6 صفوف و4 أعمدة."),
            ("Select the second and fourth rows with fancy indexing.", "اختر الصفين الثاني والرابع بالفهرسة المتقدمة."),
            ("Keep only the values greater than 15 with a Boolean mask.", "احتفظ فقط بالقيم الأكبر من 15 باستخدام قناع منطقي."),
            ("Multiply every value by 10 without a loop.", "اضرب كل قيمة في 10 دون حلقة."),
            ("Find the flat index of the largest value.", "أوجد الفهرس المسطّح لأكبر قيمة."),
        ),
        starter='''import numpy as np

numbers = np.arange(1, 25)          # the integers 1 through 24

# Step 1: structure - six rows, four columns
matrix = ___
print(matrix.shape, matrix.dtype)

# Step 2: selection - rows are counted from 0, so the second and fourth rows are 1 and 3
selected_rows = ___

# Step 3: selection - a Boolean mask keeps the values where the condition is True
values_gt_15 = ___

# Step 4: computation - arithmetic on an array applies to every element
scaled = ___

# Step 5: inspection - the position of the maximum in the flattened array
max_index = ___

print(selected_rows, values_gt_15, scaled[0], max_index, sep="\\n")
''',
        answers=("numbers.reshape(6, 4)", "matrix[[1, 3]]", "matrix[matrix > 15]", "matrix * 10", "int(np.argmax(matrix))"),
        checks=(
            check("matrix.tolist()", [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]],
                  "Blank 1: `numbers.reshape(6, 4)`.", "الفراغ 1: `numbers.reshape(6, 4)`."),
            check("selected_rows.tolist()", [[5, 6, 7, 8], [13, 14, 15, 16]],
                  "Blank 2: pass a list of row positions, `matrix[[1, 3]]`.", "الفراغ 2: مرّر قائمة بمواضع الصفوف، `matrix[[1, 3]]`."),
            check("values_gt_15.tolist()", [16, 17, 18, 19, 20, 21, 22, 23, 24],
                  "Blank 3: index with the mask, `matrix[matrix > 15]`.", "الفراغ 3: افهرس بالقناع، `matrix[matrix > 15]`."),
            check("scaled.tolist()", [[10, 20, 30, 40], [50, 60, 70, 80], [90, 100, 110, 120], [130, 140, 150, 160], [170, 180, 190, 200], [210, 220, 230, 240]],
                  "Blank 4: `matrix * 10`.", "الفراغ 4: `matrix * 10`."),
            check("int(max_index)", 23, "Blank 5: `np.argmax(matrix)` gives the flat index.", "الفراغ 5: يعطي `np.argmax(matrix)` الفهرس المسطّح."),
        ),
        hints=(
            ("`reshape(rows, columns)` keeps the values and changes only the shape.", "تحافظ `reshape(rows, columns)` على القيم وتغيّر الشكل فقط."),
            ("A list inside the brackets selects several rows at once; a condition inside them filters values.", "القائمة داخل الأقواس تختار عدة صفوف معًا، والشرط داخلها يرشّح القيم."),
            ("`np.argmax` returns one position counted across the flattened array.", "تعيد `np.argmax` موضعًا واحدًا محسوبًا عبر المصفوفة المسطّحة."),
        ),
        success=("Correct! reshape changed the structure, fancy and Boolean indexing selected data, and `* 10` computed on every element at once.",
                 "صحيح! غيّرت reshape البنية، واختارت الفهرسة المتقدمة والمنطقية البيانات، وحسبت `* 10` على كل العناصر دفعة واحدة."),
        reflect=("Which steps changed the structure, which selected data, and which performed a computation?",
                 "أي الخطوات غيّرت البنية، وأيها اختار البيانات، وأيها أجرى حسابًا؟"),
    ),
    "COURSE-013.M02.L01.EX02": Guided(
        goal=("Run a small, reproducible pandas workflow: parse dates, derive features, filter, group, merge, handle a missing value and pivot.",
              "نفّذ سير عمل صغيرًا قابلًا للتكرار في pandas: حلّل التواريخ، واشتق ميزات، ورشّح، وجمّع، وادمج، وعالج قيمة مفقودة، وأنشئ جدولًا محوريًا."),
        steps=(
            ("Convert `Date` to datetime.", "حوّل `Date` إلى نوع التاريخ والوقت."),
            ("Add `month_name` and `day_name` columns.", "أضف العمودين `month_name` و`day_name`."),
            ("Keep the rows whose Amount is above the overall mean.", "احتفظ بالصفوف التي تزيد فيها Amount على المتوسط العام."),
            ("Compute the mean Amount per Region.", "احسب متوسط Amount لكل Region."),
        ),
        starter='''import pandas as pd

sales = pd.DataFrame({
    "Customer": ["Ada", "Ben", "Chen", "Dina", "Eli", "Farah"],
    "Region": ["East", "West", "East", "West", "East", "West"],
    "Amount": [120.0, 250.0, 180.0, 320.0, 210.0, 140.0],
    "Product": ["Phone", "Laptop", "Laptop", "Phone", "Phone", "Laptop"],
    "Date": ["2026-01-03", "2026-01-08", "2026-02-10", "2026-02-14", "2026-03-02", "2026-03-09"],
})

# Step 1: text dates become real dates
sales["Date"] = ___
# Step 2: the .dt accessor exposes date parts
sales["month_name"] = ___
sales["day_name"] = ___

# Step 3: a Boolean mask compared with the column mean
above_average = ___
# Step 4: split by Region, then average Amount
region_mean = ___

categories = pd.DataFrame({"Product": ["Phone", "Laptop"], "Category": ["Mobile", "Computer"]})
merged = sales.merge(categories, on="Product", how="left")

messy_sales = sales.copy()
messy_sales.loc[4, "Amount"] = None
missing_amount_count = int(messy_sales["Amount"].isna().sum())
cleaned_sales = messy_sales.copy()
cleaned_sales["Amount"] = cleaned_sales["Amount"].fillna(cleaned_sales["Amount"].median())   # robust to outliers

pivot = cleaned_sales.pivot_table(index="Region", columns="Product", values="Amount", aggfunc="sum", fill_value=0)
print(above_average[["Customer", "Amount"]], region_mean, merged[["Product", "Category"]].head(2), missing_amount_count, pivot, sep="\\n\\n")
''',
        answers=('pd.to_datetime(sales["Date"])', 'sales["Date"].dt.month_name()', 'sales["Date"].dt.day_name()',
                 'sales[sales["Amount"] > sales["Amount"].mean()]', 'sales.groupby("Region")["Amount"].mean()'),
        checks=(
            check("str(sales['Date'].dtype).startswith('datetime64')", True,
                  "Blank 1: `pd.to_datetime(sales[\"Date\"])`.", "الفراغ 1: `pd.to_datetime(sales[\"Date\"])`."),
            check("sales['month_name'].tolist()", ["January", "January", "February", "February", "March", "March"],
                  "Blank 2: `sales[\"Date\"].dt.month_name()`.", "الفراغ 2: `sales[\"Date\"].dt.month_name()`."),
            check("sales['day_name'].tolist()", ["Saturday", "Thursday", "Tuesday", "Saturday", "Monday", "Monday"],
                  "Blank 3: `sales[\"Date\"].dt.day_name()`.", "الفراغ 3: `sales[\"Date\"].dt.day_name()`."),
            check("above_average['Customer'].tolist()", ["Ben", "Dina", "Eli"],
                  "Blank 4: filter with `sales[\"Amount\"] > sales[\"Amount\"].mean()`.", "الفراغ 4: رشّح بالشرط `sales[\"Amount\"] > sales[\"Amount\"].mean()`."),
            check("{region: round(float(value), 2) for region, value in dict(region_mean).items()}", {"East": 170.0, "West": 236.67},
                  "Blank 5: `sales.groupby(\"Region\")[\"Amount\"].mean()`.", "الفراغ 5: `sales.groupby(\"Region\")[\"Amount\"].mean()`."),
        ),
        hints=(
            ("`pd.to_datetime` converts a whole column at once.", "تحوّل `pd.to_datetime` عمودًا كاملًا دفعة واحدة."),
            ("After conversion, `.dt.month_name()` and `.dt.day_name()` work on the column.", "بعد التحويل تعمل `.dt.month_name()` و`.dt.day_name()` على العمود."),
            ("Filter with `df[condition]`; group with `df.groupby(key)[column].mean()`.", "رشّح بـ `df[condition]`، وجمّع بـ `df.groupby(key)[column].mean()`."),
        ),
        success=("Correct! Every intermediate table is reproducible, and the median fill keeps one extreme sale from distorting the cleaned Amount column.",
                 "صحيح! كل جدول وسيط قابل للتكرار، والملء بالوسيط يمنع عملية بيع متطرفة واحدة من تشويه عمود Amount بعد التنظيف."),
        reflect=("Why might the median be a safer fill value than the mean here, and what does the pivot table show that the grouped mean does not?",
                 "لماذا قد يكون الوسيط قيمة ملء أكثر أمانًا من المتوسط هنا؟ وماذا يُظهر الجدول المحوري ولا يُظهره المتوسط المجمّع؟"),
    ),
    "COURSE-013.M03.L01.EX01": Guided(
        goal=("Describe a small score dataset with central tendency and spread, then see how one extreme value moves the mean and the median.",
              "صِف مجموعة درجات صغيرة بمقاييس النزعة المركزية والتشتت، ثم لاحظ كيف تحرّك قيمةٌ متطرفة واحدة المتوسط والوسيط."),
        steps=(
            ("Compute the mean.", "احسب المتوسط."),
            ("Find the mode.", "جد المنوال."),
            ("Compute the interquartile range.", "احسب المدى الربيعي."),
            ("Append the extreme score 100.", "أضف الدرجة المتطرفة 100."),
        ),
        starter='''import pandas as pd

scores = pd.Series([40, 45, 23, 39, 39])

# Step 1: the average
mean = ___
median = scores.median()
# Step 2: the most frequent value (mode() returns a Series)
mode = ___

q1, q3 = scores.quantile(0.25), scores.quantile(0.75)
# Step 3: the spread of the middle half
iqr = ___
value_range = scores.max() - scores.min()
variance, std = scores.var(), scores.std()          # pandas uses the sample formula (ddof=1)

# Step 4: add one extreme score and recompute
with_outlier = ___
change = {"mean": round(with_outlier.mean() - mean, 2), "median": round(with_outlier.median() - median, 2)}
print(mean, median, mode, iqr, value_range, round(variance, 2), round(std, 2))
print("change after adding 100:", change)
''',
        answers=("scores.mean()", "scores.mode()[0]", "q3 - q1", "pd.concat([scores, pd.Series([100])], ignore_index=True)"),
        checks=(
            check("round(float(mean), 2)", 37.2, "Blank 1: use `scores.mean()`.", "الفراغ 1: استخدم `scores.mean()`."),
            check("int(mode)", 39, "Blank 2: `scores.mode()[0]` takes the first (here the only) mode.", "الفراغ 2: يأخذ `scores.mode()[0]` المنوال الأول (والوحيد هنا)."),
            check("float(iqr)", 1.0, "Blank 3: IQR = Q3 - Q1.", "الفراغ 3: المدى الربيعي = Q3 - Q1."),
            check("change", {"mean": 10.47, "median": 0.5},
                  "Blank 4: append 100 as a new value, e.g. `pd.concat([scores, pd.Series([100])], ignore_index=True)`.",
                  "الفراغ 4: أضف 100 قيمةً جديدة، مثل `pd.concat([scores, pd.Series([100])], ignore_index=True)`."),
        ),
        hints=(
            ("A pandas Series has `.mean()`, `.median()` and `.mode()`.", "تملك سلسلة pandas الدوال `.mean()` و`.median()` و`.mode()`."),
            ("The IQR uses the 75th and 25th percentiles computed for you.", "يستخدم المدى الربيعي المئين 75 والمئين 25 المحسوبين لك."),
            ("`pd.concat` joins Series; `ignore_index=True` renumbers the result.", "يجمع `pd.concat` السلاسل، ويعيد `ignore_index=True` ترقيم النتيجة."),
        ),
        success=("Correct! One extreme score moved the mean by more than 10 points but the median by only 0.5 - the median is robust to outliers.",
                 "صحيح! حرّكت درجة متطرفة واحدة المتوسط بأكثر من 10 نقاط، بينما حرّكت الوسيط 0.5 فقط - فالوسيط مقاوم للقيم الشاذة."),
    ),
    "COURSE-013.M04.L01.EX01": Guided(
        goal=("Compute a dot product, a norm, a matrix product and a transpose, and see why matrix multiplication is not element-wise.",
              "احسب الضرب النقطي والمعيار وضرب المصفوفات والمنقول، وافهم لماذا لا يكون ضرب المصفوفات عنصرًا بعنصر."),
        steps=(
            ("Compute the dot product of v1 and v2.", "احسب الضرب النقطي لـ v1 وv2."),
            ("Compute the length (norm) of v1.", "احسب طول (معيار) v1."),
            ("Multiply the matrices A and B.", "اضرب المصفوفتين A وB."),
            ("Transpose A.", "انقل المصفوفة A."),
        ),
        starter='''import numpy as np

v1, v2 = np.array([2, 3]), np.array([4, 5])
# Step 1: 2*4 + 3*5
dot = ___
# Step 2: sqrt(2^2 + 3^2)
norm_v1 = ___

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
# Step 3: rows of A times columns of B
product = ___
elementwise = A * B                 # for comparison: NOT matrix multiplication
# Step 4: rows become columns
A_T = ___

print(dot, round(float(norm_v1), 4))
print(product)
print(elementwise)
print(A_T)
''',
        answers=("v1 @ v2", "np.linalg.norm(v1)", "A @ B", "A.T"),
        checks=(
            check("int(dot)", 23, "Blank 1: `v1 @ v2` (or `np.dot(v1, v2)`).", "الفراغ 1: `v1 @ v2` (أو `np.dot(v1, v2)`)."),
            check("round(float(norm_v1), 4)", 3.6056, "Blank 2: `np.linalg.norm(v1)`.", "الفراغ 2: `np.linalg.norm(v1)`."),
            check("np.asarray(product).tolist()", [[19, 22], [43, 50]], "Blank 3: `A @ B` - not `A * B`.", "الفراغ 3: `A @ B` - لا `A * B`."),
            check("np.asarray(A_T).tolist()", [[1, 3], [2, 4]], "Blank 4: `A.T` swaps rows and columns.", "الفراغ 4: يبدّل `A.T` الصفوف والأعمدة."),
        ),
        hints=(
            ("`@` is matrix multiplication in NumPy; for vectors it is the dot product.", "يمثّل `@` ضرب المصفوفات في NumPy، وهو الضرب النقطي للمتجهات."),
            ("`np.linalg.norm` gives the Euclidean length.", "تعطي `np.linalg.norm` الطول الإقليدي."),
            ("`.T` is the transpose.", "`.T` هو المنقول."),
        ),
        success=("Correct! A @ B combines each row of A with each column of B (19 = 1·5 + 2·7), while A * B only multiplies matching positions.",
                 "صحيح! يجمع A @ B كل صف من A مع كل عمود من B (19 = 1·5 + 2·7)، بينما يضرب A * B المواضع المتقابلة فقط."),
    ),
    "COURSE-013.M04.L01.EX02": Guided(
        goal=("Analyse a 2×2 matrix: determinant, inverse, solving Ax = b, eigenvalues and SVD.",
              "حلّل مصفوفة 2×2: المحدِّد، والمعكوس، وحل Ax = b، والقيم الذاتية، وتحليل SVD."),
        steps=(
            ("Compute the determinant.", "احسب المحدِّد."),
            ("Compute the inverse.", "احسب المعكوس."),
            ("Solve Ax = b.", "حلّ Ax = b."),
            ("Compute eigenvalues and eigenvectors.", "احسب القيم والمتجهات الذاتية."),
            ("Perform the SVD.", "نفّذ تحليل SVD."),
        ),
        starter='''import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])
b = np.array([3.0, 3.0])

# Step 1: non-zero means A is invertible
determinant = ___
rank = np.linalg.matrix_rank(A)
# Step 2
A_inv = ___
is_identity = bool(np.allclose(A @ A_inv, np.eye(2)))
# Step 3: solve directly (better than A_inv @ b)
x = ___
# Step 4
eigenvalues, eigenvectors = ___
# Step 5: A = U @ diag(S) @ Vt
U, S, Vt = ___

print(round(float(determinant), 4), rank, is_identity, x, eigenvalues, S)
''',
        answers=("np.linalg.det(A)", "np.linalg.inv(A)", "np.linalg.solve(A, b)", "np.linalg.eig(A)", "np.linalg.svd(A)"),
        checks=(
            check("round(float(determinant), 6)", 3.0, "Blank 1: `np.linalg.det(A)`.", "الفراغ 1: `np.linalg.det(A)`."),
            check("is_identity and bool(np.allclose(A_inv, [[2 / 3, -1 / 3], [-1 / 3, 2 / 3]]))", True, "Blank 2: `np.linalg.inv(A)`.", "الفراغ 2: `np.linalg.inv(A)`."),
            check("bool(np.allclose(x, [1.0, 1.0]))", True, "Blank 3: `np.linalg.solve(A, b)`.", "الفراغ 3: `np.linalg.solve(A, b)`."),
            check("sorted(round(float(v), 6) for v in eigenvalues) == [1.0, 3.0] and bool(np.allclose(A @ eigenvectors, eigenvectors * eigenvalues))", True,
                  "Blank 4: `np.linalg.eig(A)` returns the values and the vectors.", "الفراغ 4: تعيد `np.linalg.eig(A)` القيم والمتجهات."),
            check("bool(np.allclose(S, [3.0, 1.0])) and bool(np.allclose(U @ np.diag(S) @ Vt, A))", True,
                  "Blank 5: `np.linalg.svd(A)` returns U, S and Vt.", "الفراغ 5: تعيد `np.linalg.svd(A)` المصفوفات U وS وVt."),
        ),
        hints=(
            ("All of these live in `np.linalg`.", "كل هذه الدوال موجودة في `np.linalg`."),
            ("`solve(A, b)` is more accurate than multiplying by the inverse.", "`solve(A, b)` أدق من الضرب في المعكوس."),
            ("`eig` and `svd` return several arrays - unpack them.", "تعيد `eig` و`svd` عدة مصفوفات - فكّها في متغيرات."),
        ),
        success=("Correct! det = 3 and full rank mean A is invertible, x = [1, 1], and the eigenvalues 3 and 1 equal the singular values because A is symmetric and positive.",
                 "صحيح! المحدِّد 3 والرتبة كاملة، أي أن A قابلة للعكس، وx = [1, 1]، والقيمتان الذاتيتان 3 و1 تساويان القيم المنفردة لأن A متماثلة وموجبة."),
    ),
    "COURSE-013.M04.L01.EX04": Guided(
        goal=("Test a generated sample for normality with three methods and check whether they agree.",
              "اختبر طبيعية عينة مولَّدة بثلاث طرق، وتحقّق هل تتفق."),
        steps=(
            ("Draw 200 values from a normal distribution.", "اسحب 200 قيمة من توزيع طبيعي."),
            ("Run Shapiro-Wilk.", "شغّل اختبار Shapiro-Wilk."),
            ("Compare Anderson-Darling with its 5% critical value.", "قارن Anderson-Darling بقيمته الحرجة عند 5%."),
            ("Run D'Agostino-Pearson.", "شغّل اختبار D'Agostino-Pearson."),
        ),
        starter='''import numpy as np
from scipy import stats

rng = np.random.default_rng(42)
# Step 1: 200 values, mean 50, standard deviation 10
sample = ___

alpha = 0.05
# Step 2: Shapiro-Wilk (H0: the data come from a normal distribution)
shapiro_p = ___
# Step 3: Anderson-Darling - normal when the statistic is below the 5% critical value
anderson = stats.anderson(sample, dist="norm")
five_percent = list(anderson.significance_level).index(5.0)
anderson_normal = ___
# Step 4: D'Agostino-Pearson (skewness + kurtosis)
dagostino_p = ___

verdicts = {"shapiro": bool(shapiro_p > alpha), "anderson": anderson_normal, "dagostino": bool(dagostino_p > alpha)}
all_agree = len(set(verdicts.values())) == 1
print(verdicts, "agree:", all_agree)
''',
        answers=(
            "rng.normal(loc=50, scale=10, size=200)",
            "stats.shapiro(sample).pvalue",
            "bool(anderson.statistic < anderson.critical_values[five_percent])",
            "stats.normaltest(sample).pvalue",
        ),
        checks=(
            check("len(sample) == 200 and abs(float(np.mean(sample)) - 50) < 3 and abs(float(np.std(sample)) - 10) < 2", True,
                  "Blank 1: `rng.normal(loc=50, scale=10, size=200)`.", "الفراغ 1: `rng.normal(loc=50, scale=10, size=200)`."),
            check("abs(float(shapiro_p) - float(stats.shapiro(sample).pvalue)) < 1e-12", True,
                  "Blank 2: take `.pvalue` from `stats.shapiro(sample)`.", "الفراغ 2: خذ `.pvalue` من `stats.shapiro(sample)`."),
            check("anderson_normal == bool(anderson.statistic < anderson.critical_values[five_percent])", True,
                  "Blank 3: compare `anderson.statistic` with `anderson.critical_values[five_percent]`.",
                  "الفراغ 3: قارن `anderson.statistic` بـ `anderson.critical_values[five_percent]`."),
            check("abs(float(dagostino_p) - float(stats.normaltest(sample).pvalue)) < 1e-12", True,
                  "Blank 4: `stats.normaltest(sample).pvalue` is the D'Agostino-Pearson test.", "الفراغ 4: `stats.normaltest(sample).pvalue` هو اختبار D'Agostino-Pearson."),
        ),
        hints=(
            ("`rng.normal(loc, scale, size)` draws normal values.", "يسحب `rng.normal(loc, scale, size)` قيمًا طبيعية."),
            ("SciPy tests return result objects with a `.pvalue`.", "تعيد اختبارات SciPy كائنات نتائج فيها `.pvalue`."),
            ("A p-value above alpha means: no evidence against normality.", "تعني القيمة الاحتمالية الأعلى من alpha عدم وجود دليل ضد الطبيعية."),
        ),
        success=("Correct! All three methods judge this sample consistent with a normal distribution - but 'not rejected' is not the same as 'proven normal'.",
                 "صحيح! تحكم الطرق الثلاث بأن هذه العينة متسقة مع التوزيع الطبيعي - لكن «عدم الرفض» لا يعني «إثبات الطبيعية»."),
        reflect=("Plot a histogram with a KDE locally. Why should a visual check accompany the tests, especially for very large samples?",
                 "ارسم مدرجًا تكراريًا مع KDE محليًا. لماذا يجب أن يرافق الفحصُ البصري الاختبارات، خصوصًا مع العينات الكبيرة جدًا؟"),
    ),
    "COURSE-013.M05.L01.EX01": Guided(
        goal=("Choose the right Matplotlib chart for four analytical questions.",
              "اختر مخطط Matplotlib المناسب لأربعة أسئلة تحليلية."),
        steps=(
            ("A trend over months → line chart.", "اتجاه عبر الأشهر ← مخطط خطي."),
            ("A relationship between two numbers → scatter chart.", "علاقة بين رقمين ← مخطط انتشار."),
            ("Totals per category → bar chart.", "إجماليات لكل فئة ← مخطط أعمدة."),
            ("A distribution → histogram.", "توزيع ← مدرج تكراري."),
        ),
        starter='''import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [120, 135, 128, 150, 162, 170]
hours, exam = [1, 2, 3, 4, 5, 6, 7], [52, 58, 61, 67, 70, 78, 84]
categories, category_sales = ["Laptops", "Phones", "Tablets"], [420, 610, 180]
ages = [23, 25, 27, 29, 31, 31, 33, 35, 38, 41, 45, 52]

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
# Step 1: how did sales change over time?
___(months, sales)
axes[0, 0].set(title="Monthly sales", xlabel="Month", ylabel="Sales")
# Step 2: do more study hours go with higher scores?
___(hours, exam)
axes[0, 1].set(title="Study hours vs exam score", xlabel="Hours", ylabel="Score")
# Step 3: which category sells most?
___(categories, category_sales)
axes[1, 0].set(title="Sales by category", xlabel="Category", ylabel="Sales")
# Step 4: how are employee ages distributed?
___(ages, bins=6)
axes[1, 1].set(title="Employee age", xlabel="Age", ylabel="Employees")
fig.tight_layout()
plt.show()
''',
        answers=("axes[0, 0].plot", "axes[0, 1].scatter", "axes[1, 0].bar", "axes[1, 1].hist"),
        blanks=(
            ("a trend over time is a line: `axes[0, 0].plot`.", "الاتجاه عبر الزمن خط: `axes[0, 0].plot`."),
            ("a relationship between two numbers is a scatter: `axes[0, 1].scatter`.", "العلاقة بين رقمين انتشار: `axes[0, 1].scatter`."),
            ("comparing categories uses bars: `axes[1, 0].bar`.", "مقارنة الفئات تستخدم الأعمدة: `axes[1, 0].bar`."),
            ("a distribution is a histogram: `axes[1, 1].hist`.", "التوزيع مدرج تكراري: `axes[1, 1].hist`."),
        ),
        hints=(
            ("Each blank is `axes[row, column]` followed by a plotting method; match each chart type to the subplot the steps name.", "كل فراغ هو `axes[row, column]` تليه دالة رسم؛ طابِق كل نوع مخطط مع المخطط الفرعي الذي تحدده الخطوات."),
            ("Order matters on the x-axis for a line; it does not for a scatter.", "الترتيب على المحور x مهم للخط، وليس مهمًا للانتشار."),
            ("A histogram counts how many values fall in each bin.", "يعدّ المدرج التكراري عدد القيم في كل فئة."),
        ),
        success=("Correct! Each chart type matches its question: line for change over time, scatter for relationships, bars for comparing categories and a histogram for a distribution.",
                 "صحيح! يطابق كل نوع مخطط سؤاله: الخط للتغير عبر الزمن، والانتشار للعلاقات، والأعمدة لمقارنة الفئات، والمدرج التكراري للتوزيع."),
        expected=READ_NOTE,
    ),
    "COURSE-013.M05.L01.EX02": Guided(
        goal=("Answer five exploratory questions with five Seaborn chart families.",
              "أجب عن خمسة أسئلة استكشافية بخمس عائلات من مخططات Seaborn."),
        steps=(
            ("Show the relationship with a fitted regression line.", "اعرض العلاقة مع خط انحدار ملائم."),
            ("Add a KDE curve to the histogram.", "أضف منحنى KDE إلى المدرج التكراري."),
            ("Compare score distributions per track.", "قارن توزيعات الدرجات لكل مسار."),
            ("Visualize the correlation matrix.", "اعرض مصفوفة الارتباط بصريًا."),
            ("Plot every pair of numeric variables.", "ارسم كل زوج من المتغيرات الرقمية."),
        ),
        starter='''import pandas as pd
import seaborn as sns

df = pd.DataFrame({
    "study_hours": [1, 2, 2, 3, 4, 4, 5, 6, 6, 7],
    "sleep_hours": [8, 7, 6, 7, 6, 8, 5, 6, 7, 6],
    "score": [55, 58, 60, 66, 70, 72, 74, 80, 83, 88],
    "track": ["data", "web", "data", "web", "data", "web", "data", "web", "data", "web"],
})

# Step 1: relationship + fitted line
___(data=df, x="study_hours", y="score")
# Step 2: distribution with a smooth density curve
sns.histplot(data=df, x="score", kde=___)
# Step 3: compare groups
___(data=df, x="track", y="score")
# Step 4: correlations between the numeric columns
sns.heatmap(___, annot=True, cmap="coolwarm")
# Step 5: every pair of numeric variables, coloured by track
___(df, hue="track")
''',
        answers=("sns.regplot", "True", "sns.boxplot", "df.corr(numeric_only=True)", "sns.pairplot"),
        alternatives={1: ("sns.lmplot",), 3: ("sns.violinplot",), 4: ('df[["study_hours", "sleep_hours", "score"]].corr()', 'df.select_dtypes("number").corr()')},
        blanks=(
            ("use `sns.regplot` (or `sns.lmplot`).", "استخدم `sns.regplot` (أو `sns.lmplot`)."),
            ("`kde=True` adds the density curve.", "يضيف `kde=True` منحنى الكثافة."),
            ("use `sns.boxplot` (or `sns.violinplot`).", "استخدم `sns.boxplot` (أو `sns.violinplot`)."),
            ("pass `df.corr(numeric_only=True)`.", "مرّر `df.corr(numeric_only=True)`."),
            ("use `sns.pairplot`.", "استخدم `sns.pairplot`."),
        ),
        hints=(
            ("Blanks 1, 3 and 5 are plotting functions from `sns`.", "الفراغات 1 و3 و5 دوال رسم من `sns`."),
            ("A heatmap needs a matrix - the correlation matrix of the numeric columns.", "تحتاج الخريطة الحرارية إلى مصفوفة - مصفوفة ارتباط الأعمدة الرقمية."),
            ("`numeric_only=True` skips the text column.", "يتخطى `numeric_only=True` العمود النصي."),
        ),
        success=("Correct! Each chart answers its own question: relationship, distribution, group comparison, correlation structure and all pairwise views.",
                 "صحيح! يجيب كل مخطط عن سؤاله: العلاقة، والتوزيع، ومقارنة المجموعات، وبنية الارتباط، وكل المناظر الثنائية."),
        expected=READ_NOTE,
        reflect=("Write one observation under each chart. Which chart told you the most about this dataset?",
                 "اكتب ملاحظة واحدة تحت كل مخطط. أي مخطط أخبرك بالأكثر عن هذه البيانات؟"),
    ),
    "COURSE-013.M05.L01.EX03": Guided(
        goal=("Build an interactive Plotly chart with one trace per product and a dropdown that switches the visible traces.",
              "ابنِ مخطط Plotly تفاعليًا بمسار لكل منتج وقائمة منسدلة تبدّل المسارات الظاهرة."),
        steps=(
            ("Add one bar trace per product.", "أضف مسار أعمدة لكل منتج."),
            ("Make each button show only its own product.", "اجعل كل زر يعرض منتجه فقط."),
            ("Attach the buttons as a dropdown menu.", "اربط الأزرار بوصفها قائمة منسدلة."),
        ),
        starter='''import plotly.graph_objects as go

years = [2022, 2023, 2024, 2025]
sales = {"Laptops": [120, 150, 170, 210], "Phones": [300, 320, 310, 360], "Tablets": [90, 80, 95, 100]}
products = list(sales)

fig = go.Figure()
for product in products:
    # Step 1: one trace per product
    fig.add_trace(___(x=years, y=sales[product], name=product))

buttons = [dict(label="All products", method="update", args=[{"visible": [True] * len(products)}])]
for product in products:
    # Step 2: True only for this product's trace
    visible = ___
    buttons.append(dict(label=product, method="update", args=[{"visible": visible}]))

# Step 3: the dropdown changes the figure's trace visibility
fig.update_layout(updatemenus=[dict(type="dropdown", buttons=___)], title="Sales by product")
fig.show()
''',
        answers=("go.Bar", "[p == product for p in products]", "buttons"),
        alternatives={1: ("go.Scatter",)},
        blanks=(
            ("use `go.Bar` (or `go.Scatter` for lines).", "استخدم `go.Bar` (أو `go.Scatter` للخطوط)."),
            ("build `[p == product for p in products]`.", "ابنِ `[p == product for p in products]`."),
            ("pass the `buttons` list.", "مرّر قائمة `buttons`."),
        ),
        hints=(
            ("Each product becomes one trace built from `plotly.graph_objects` - choose its bar-chart class.", "يصبح كل منتج مسارًا واحدًا يُبنى من `plotly.graph_objects`، فاختر صنف المخطط الشريطي فيه."),
            ("The visible list has one True/False per trace, in trace order.", "تحتوي قائمة الظهور على True/False لكل مسار بترتيب المسارات."),
            ("`updatemenus` takes menus; each menu holds `buttons`.", "يأخذ `updatemenus` قوائم، وتحمل كل قائمة `buttons`."),
        ),
        success=("Correct! Each button runs an `update` that changes only the traces' `visible` property - the data never changes, just what is shown.",
                 "صحيح! ينفّذ كل زر عملية `update` تغيّر خاصية `visible` للمسارات فقط - البيانات لا تتغير، بل ما يُعرض فقط."),
        expected=READ_NOTE,
        reflect=("How would a year slider differ from this dropdown in what part of the figure state it changes?",
                 "كيف يختلف شريط تمرير للسنوات عن هذه القائمة المنسدلة في الجزء الذي يغيّره من حالة المخطط؟"),
    ),
    "COURSE-013.M05.L01.EX04": Guided(
        goal=("Wire a small Dash dashboard: a dropdown, a graph in one tab, a data table in another, and a callback that filters by year.",
              "اربط لوحة Dash صغيرة: قائمة منسدلة، ومخطط في تبويب، وجدول بيانات في تبويب آخر، ودالة رد نداء ترشّح حسب السنة."),
        steps=(
            ("Create the Dash app.", "أنشئ تطبيق Dash."),
            ("Give the graph the id the callback writes to.", "امنح المخطط المعرّف الذي تكتب إليه دالة رد النداء."),
            ("Declare the dropdown value as the callback input.", "صرّح بقيمة القائمة المنسدلة مدخلًا لدالة رد النداء."),
            ("Filter the rows for the chosen year.", "رشّح الصفوف للسنة المختارة."),
            ("Return the figure.", "أعد المخطط."),
        ),
        starter='''import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dash_table, dcc, html

df = pd.DataFrame({"year": [2024, 2024, 2025, 2025], "product": ["A", "B", "A", "B"], "sales": [10, 14, 13, 18]})

# Step 1
app = ___
app.layout = html.Div([
    dcc.Dropdown(id="year", options=sorted(df["year"].unique()), value=2025),
    dcc.Tabs([
        dcc.Tab(label="Chart", children=[dcc.Graph(id=___)]),            # Step 2
        dcc.Tab(label="Table", children=[dash_table.DataTable(data=df.to_dict("records"))]),
    ]),
])

# Output: the graph's figure; Step 3: Input: the dropdown's value
@app.callback(Output("sales-chart", "figure"), ___)
def update_chart(year):
    # Step 4
    filtered = ___
    # Step 5
    return ___

if __name__ == "__main__":
    app.run(debug=True)
''',
        answers=("Dash(__name__)", '"sales-chart"', 'Input("year", "value")', 'df[df["year"] == year]',
                 'px.bar(filtered, x="product", y="sales")'),
        alternatives={4: ('df.query("year == @year")', 'df.loc[df["year"] == year]')},
        blanks=(
            ("create `Dash(__name__)`.", "أنشئ `Dash(__name__)`."),
            ("the id must match the Output: `\"sales-chart\"`.", "يجب أن يطابق المعرّف الـ Output: `\"sales-chart\"`."),
            ("`Input(\"year\", \"value\")` - component id, then property.", "`Input(\"year\", \"value\")` - معرّف المكوّن ثم الخاصية."),
            ("keep rows with `df[\"year\"] == year`.", "احتفظ بالصفوف التي `df[\"year\"] == year`."),
            ("return `px.bar(filtered, x=\"product\", y=\"sales\")`.", "أعد `px.bar(filtered, x=\"product\", y=\"sales\")`."),
        ),
        hints=(
            ("Component ids connect the layout to the callback.", "تربط معرّفات المكوّنات التخطيط بدالة رد النداء."),
            ("Input and Output both take (component id, property name).", "يأخذ Input وOutput كلاهما (معرّف المكوّن، اسم الخاصية)."),
            ("The callback's return value becomes the Output property - here a figure.", "تصبح قيمة الإرجاع خاصية الـ Output - وهي هنا مخطط."),
        ),
        success=("Correct! Changing the dropdown fires the callback with the new year, and the returned figure replaces the graph's `figure` property.",
                 "صحيح! يؤدي تغيير القائمة المنسدلة إلى تشغيل دالة رد النداء بالسنة الجديدة، ويحل المخطط المُعاد محل خاصية `figure` في المخطط."),
        expected=READ_NOTE,
    ),
    "COURSE-013.M06.L01.EX01": Guided(
        goal=("Move one DataFrame through CSV, Excel, JSON, Parquet and Pickle.",
              "انقل إطار بيانات واحدًا عبر صيغ CSV وExcel وJSON وParquet وPickle."),
        steps=(
            ("Reload the CSV file.", "أعد تحميل ملف CSV."),
            ("Reload the Excel file.", "أعد تحميل ملف Excel."),
            ("Save JSON as a list of records.", "احفظ JSON بوصفه قائمة سجلات."),
            ("Reload the Parquet file.", "أعد تحميل ملف Parquet."),
            ("Reload the Pickle file.", "أعد تحميل ملف Pickle."),
        ),
        starter='''import pandas as pd

df = pd.DataFrame({"eid": [1, 2, 3], "name": ["Ada", "Ben", "Chen"],
                   "department": ["Data", "Web", "Data"], "salary": [5200, 4800, 6100]})

df.to_csv("employees.csv", index=False)               # plain text, easy to open anywhere
csv_back = ___                                        # Step 1

df.to_excel("employees.xlsx", index=False)            # needs openpyxl
excel_back = ___                                      # Step 2

df.to_json("employees.json", orient=___)              # Step 3: [{"eid": 1, ...}, ...]

df.to_parquet("employees.parquet")                    # columnar, typed and compact
parquet_back = ___                                    # Step 4

df.to_pickle("employees.pkl")                         # Python objects - only load files you trust
pickle_back = ___                                     # Step 5
''',
        answers=('pd.read_csv("employees.csv")', 'pd.read_excel("employees.xlsx")', '"records"',
                 'pd.read_parquet("employees.parquet")', 'pd.read_pickle("employees.pkl")'),
        blanks=(
            ("`pd.read_csv(\"employees.csv\")`.", "`pd.read_csv(\"employees.csv\")`."),
            ("`pd.read_excel(\"employees.xlsx\")`.", "`pd.read_excel(\"employees.xlsx\")`."),
            ("`orient=\"records\"` writes one object per row.", "يكتب `orient=\"records\"` كائنًا لكل صف."),
            ("`pd.read_parquet(\"employees.parquet\")`.", "`pd.read_parquet(\"employees.parquet\")`."),
            ("`pd.read_pickle(\"employees.pkl\")`.", "`pd.read_pickle(\"employees.pkl\")`."),
        ),
        hints=(
            ("Every `to_<format>` has a matching `pd.read_<format>`.", "لكل `to_<format>` دالة مقابلة `pd.read_<format>`."),
            ("JSON's `orient` decides the layout; \"records\" is a list of row objects.", "يحدد `orient` في JSON البنية؛ و\"records\" قائمة بكائنات الصفوف."),
            ("Pickle can run code while loading, so never unpickle untrusted files.", "قد يشغّل Pickle كودًا أثناء التحميل، لذا لا تفكّ أبدًا ملفات غير موثوقة."),
        ),
        success=("Correct! CSV and JSON are easiest for humans to inspect; Parquet keeps types and suits analytics; Pickle preserves Python objects but is only safe for trusted files.",
                 "صحيح! أسهل الصيغ للفحص البشري CSV وJSON؛ وتحافظ Parquet على الأنواع وتناسب التحليلات؛ ويحفظ Pickle كائنات Python لكنه آمن للملفات الموثوقة فقط."),
        expected=READ_NOTE,
    ),
    "COURSE-013.M06.L01.EX02": Guided(
        goal=("Round-trip data through SQLite: create, insert, commit, read into pandas, derive a column and write it back.",
              "مرّر البيانات ذهابًا وإيابًا عبر SQLite: أنشئ، وأدرج، واحفظ، واقرأ إلى pandas، واشتق عمودًا، ثم اكتبه مرة أخرى."),
        steps=(
            ("Connect to the database file.", "اتصل بملف قاعدة البيانات."),
            ("Commit the inserts.", "احفظ عمليات الإدراج (commit)."),
            ("Read the table into a DataFrame.", "اقرأ الجدول إلى إطار بيانات."),
            ("Write the processed DataFrame to a new table.", "اكتب إطار البيانات المعالَج إلى جدول جديد."),
            ("Close the connection.", "أغلق الاتصال."),
        ),
        starter='''import sqlite3

import pandas as pd

# Step 1: a local database file (created if missing)
connection = ___
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS employees (eid INTEGER PRIMARY KEY, name TEXT, salary REAL)")
cursor.executemany("INSERT OR REPLACE INTO employees VALUES (?, ?, ?)",
                   [(1, "Ada", 5200), (2, "Ben", 4800), (3, "Chen", 6100)])
# Step 2: make the inserts permanent
___

# Step 3: SQL result -> DataFrame
df = ___
df["annual_salary"] = df["salary"] * 12

# Step 4: write the processed data to a second table
df.to_sql(___, connection, if_exists="replace", index=False)
# Step 5
___
''',
        answers=('sqlite3.connect("company.db")', "connection.commit()", 'pd.read_sql_query("SELECT * FROM employees", connection)',
                 '"employees_processed"', "connection.close()"),
        alternatives={3: ('pd.read_sql("SELECT * FROM employees", connection)',)},
        blanks=(
            ("`sqlite3.connect(\"company.db\")`.", "`sqlite3.connect(\"company.db\")`."),
            ("`connection.commit()`.", "`connection.commit()`."),
            ("`pd.read_sql_query(\"SELECT * FROM employees\", connection)`.", "`pd.read_sql_query(\"SELECT * FROM employees\", connection)`."),
            ("name the new table `\"employees_processed\"`.", "سمِّ الجدول الجديد `\"employees_processed\"`."),
            ("`connection.close()`.", "`connection.close()`."),
        ),
        hints=(
            ("Changes are invisible to other connections until you commit.", "لا تظهر التغييرات للاتصالات الأخرى حتى تحفظها."),
            ("pandas runs the query and builds the DataFrame for you.", "ينفّذ pandas الاستعلام ويبني إطار البيانات لك."),
            ("`to_sql(name, connection, ...)` takes the table name first.", "يأخذ `to_sql(name, connection, ...)` اسم الجدول أولًا."),
        ),
        success=("Correct! The commit made the rows durable, `read_sql_query` fetched them into pandas, and `to_sql` wrote the derived column back to its own table.",
                 "صحيح! جعل الحفظ الصفوف دائمة، وجلب `read_sql_query` البيانات إلى pandas، وكتب `to_sql` العمود المشتق إلى جدوله الخاص."),
        expected=READ_NOTE,
    ),
    "COURSE-013.M06.L01.EX04": Guided(
        goal=("Write the same upload/download workflow for Amazon S3 and Azure Blob Storage, and map their concepts.",
              "اكتب سير عمل الرفع والتنزيل نفسه لـ Amazon S3 وAzure Blob Storage، وطابق مفاهيمهما."),
        steps=(
            ("Create the S3 client.", "أنشئ عميل S3."),
            ("Download the object from S3.", "نزّل الكائن من S3."),
            ("Get a client for one Azure blob.", "احصل على عميل لكائن Azure واحد."),
            ("Upload the file to Azure.", "ارفع الملف إلى Azure."),
            ("Read the downloaded blob's bytes.", "اقرأ بايتات الكائن المنزَّل."),
        ),
        starter='''import boto3
from azure.storage.blob import BlobServiceClient

with open("report.csv", "w") as f:
    f.write("id,total\\n1,99\\n")

# ---- Amazon S3: bucket -> object (credentials come from the environment, never the code)
s3 = ___                                                              # Step 1
s3.upload_file("report.csv", "my-bucket", "reports/report.csv")
___                                                                   # Step 2: to report_from_s3.csv

# ---- Azure Blob Storage: container -> blob
service = BlobServiceClient.from_connection_string(connection_string)  # read from a secret
blob = ___                                                            # Step 3
with open("report.csv", "rb") as data:
    ___                                                               # Step 4
with open("report_from_azure.csv", "wb") as out:
    out.write(___)                                                    # Step 5
''',
        answers=(
            'boto3.client("s3")',
            's3.download_file("my-bucket", "reports/report.csv", "report_from_s3.csv")',
            'service.get_blob_client(container="reports", blob="report.csv")',
            "blob.upload_blob(data, overwrite=True)",
            "blob.download_blob().readall()",
        ),
        blanks=(
            ("`boto3.client(\"s3\")`.", "`boto3.client(\"s3\")`."),
            ("`s3.download_file(\"my-bucket\", \"reports/report.csv\", \"report_from_s3.csv\")`.", "`s3.download_file(\"my-bucket\", \"reports/report.csv\", \"report_from_s3.csv\")`."),
            ("`service.get_blob_client(container=\"reports\", blob=\"report.csv\")`.", "`service.get_blob_client(container=\"reports\", blob=\"report.csv\")`."),
            ("`blob.upload_blob(data, overwrite=True)`.", "`blob.upload_blob(data, overwrite=True)`."),
            ("`blob.download_blob().readall()`.", "`blob.download_blob().readall()`."),
        ),
        hints=(
            ("S3 download takes (bucket, key, local file name) - the reverse of upload.", "يأخذ التنزيل من S3 (الحاوية، المفتاح، اسم الملف المحلي) - عكس الرفع."),
            ("In Azure you first get a client for one blob, then upload or download through it.", "في Azure تحصل أولًا على عميل لكائن واحد، ثم ترفع أو تنزّل عبره."),
            ("`download_blob()` returns a stream; `.readall()` gives the bytes.", "تعيد `download_blob()` تدفقًا، ويعطي `.readall()` البايتات."),
        ),
        success=("Correct! Bucket ↔ container, object ↔ blob, and both providers follow the same create-client → upload → download → read flow.",
                 "صحيح! الحاوية (bucket) تقابل الحاوية (container)، والكائن (object) يقابل الكائن (blob)، ويتبع المزوّدان التدفق نفسه: إنشاء العميل ← الرفع ← التنزيل ← القراءة."),
        expected=READ_NOTE,
    ),
    "COURSE-013.M06.L01.EX05": Guided(
        goal=("Fetch JSON from a REST endpoint safely, and request exactly three fields with GraphQL.",
              "اجلب JSON من نقطة REST بأمان، واطلب ثلاثة حقول بالضبط باستخدام GraphQL."),
        steps=(
            ("Send the GET request with a timeout.", "أرسل طلب GET مع مهلة زمنية."),
            ("Stop on HTTP errors.", "توقّف عند أخطاء HTTP."),
            ("Parse the JSON body.", "حلّل جسم JSON."),
            ("POST the GraphQL query.", "أرسل استعلام GraphQL عبر POST."),
        ),
        starter='''import requests

# ---- REST: the URL decides what you get back
response = ___                                    # Step 1
___                                               # Step 2: raise for 4xx/5xx instead of parsing an error page
user = ___                                        # Step 3
print(user["name"], user["email"], user["address"]["city"])

# ---- GraphQL: one endpoint; the query decides which fields come back
query = """
{
  country(code: "EG") {
    name
    capital
    currency
  }
}
"""
result = ___                                      # Step 4
print(result.json()["data"]["country"])
''',
        answers=(
            'requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=10)',
            "response.raise_for_status()",
            "response.json()",
            'requests.post("https://countries.trevorblades.com/", json={"query": query}, timeout=10)',
        ),
        blanks=(
            ("`requests.get(\"https://jsonplaceholder.typicode.com/users/1\", timeout=10)`.", "`requests.get(\"https://jsonplaceholder.typicode.com/users/1\", timeout=10)`."),
            ("`response.raise_for_status()`.", "`response.raise_for_status()`."),
            ("`response.json()`.", "`response.json()`."),
            ("`requests.post(\"https://countries.trevorblades.com/\", json={\"query\": query}, timeout=10)`.", "`requests.post(\"https://countries.trevorblades.com/\", json={\"query\": query}, timeout=10)`."),
        ),
        hints=(
            ("Always pass a `timeout` so a slow server cannot hang your script.", "مرّر دائمًا `timeout` كي لا يعلّق خادمٌ بطيء البرنامج."),
            ("`raise_for_status()` turns 4xx/5xx responses into exceptions.", "يحوّل `raise_for_status()` استجابات 4xx/5xx إلى استثناءات."),
            ("GraphQL sends the query as JSON: `json={\"query\": query}`.", "يرسل GraphQL الاستعلام بصيغة JSON: `json={\"query\": query}`."),
        ),
        success=("Correct! REST returns whatever the endpoint defines; GraphQL returns exactly the three fields you selected from one endpoint.",
                 "صحيح! تعيد REST كل ما تحدده نقطة النهاية، بينما تعيد GraphQL الحقول الثلاثة التي اخترتها بالضبط من نقطة نهاية واحدة."),
        expected=READ_NOTE,
    ),
    "COURSE-013.M07.L01.EX01": Guided(
        goal=("Measure missing data, then compare deletion with median, mode and group-based imputation.",
              "قِس البيانات المفقودة، ثم قارن الحذف بالتعويض بالوسيط والمنوال والتعويض حسب المجموعة."),
        steps=(
            ("Compute the missing percentage per column.", "احسب نسبة القيم المفقودة لكل عمود."),
            ("Count the rows left after listwise deletion.", "عُدّ الصفوف المتبقية بعد الحذف الكامل للصفوف الناقصة."),
            ("Fill Age with its median.", "عوّض Age بوسيطه."),
            ("Fill Income with the mean of each segment.", "عوّض Income بمتوسط كل شريحة."),
        ),
        starter='''import numpy as np
import pandas as pd

customers = pd.DataFrame({
    "Age": [25, np.nan, 41, 33, np.nan, 52, 29, 38],
    "Income": [42000, 51000, np.nan, 61000, 39000, np.nan, 45000, 58000],
    "Country": ["EG", "EG", "SA", None, "SA", "EG", "AE", "AE"],
    "PreferredDevice": ["mobile", None, "desktop", "mobile", "mobile", None, "desktop", "mobile"],
    "CreditScore": [700, 650, np.nan, 720, 610, 690, np.nan, 705],
    "Segment": ["A", "A", "B", "B", "A", "B", "A", "B"],
})

print(customers.isnull().any())
# Step 1: percentage missing per column, rounded to 1 decimal
missing_pct = ___
# Step 2: rows that survive dropping every incomplete row
complete_rows = ___
thresholded_rows = len(customers.dropna(thresh=5))      # keep rows with at least 5 known values

filled = customers.copy()
# Step 3: numeric column -> median (robust to outliers)
filled["Age"] = ___
filled["PreferredDevice"] = filled["PreferredDevice"].fillna(filled["PreferredDevice"].mode()[0])
# Step 4: fill Income with the mean income of the customer's own segment
filled["Income"] = ___

print(missing_pct.to_dict(), complete_rows, thresholded_rows)
print(filled)
''',
        answers=(
            "(customers.isnull().mean() * 100).round(1)",
            "len(customers.dropna())",
            'filled["Age"].fillna(filled["Age"].median())',
            'filled.groupby("Segment")["Income"].transform(lambda s: s.fillna(s.mean()))',
        ),
        checks=(
            check("missing_pct.to_dict()", {"Age": 25.0, "Income": 25.0, "Country": 12.5, "PreferredDevice": 25.0, "CreditScore": 25.0, "Segment": 0.0},
                  "Blank 1: the mean of `isnull()` is the missing share; multiply by 100.", "الفراغ 1: متوسط `isnull()` هو نسبة القيم المفقودة؛ اضربه في 100."),
            check("int(complete_rows)", 2, "Blank 2: `len(customers.dropna())`.", "الفراغ 2: `len(customers.dropna())`."),
            check("[float(v) for v in filled['Age']]", [25.0, 35.5, 41.0, 33.0, 35.5, 52.0, 29.0, 38.0],
                  "Blank 3: `filled[\"Age\"].fillna(filled[\"Age\"].median())`.", "الفراغ 3: `filled[\"Age\"].fillna(filled[\"Age\"].median())`."),
            check("[float(v) for v in filled['Income']]", [42000.0, 51000.0, 59500.0, 61000.0, 39000.0, 59500.0, 45000.0, 58000.0],
                  "Blank 4: group by Segment and fill each group with its own mean using `transform`.",
                  "الفراغ 4: جمّع حسب Segment وعوّض كل مجموعة بمتوسطها باستخدام `transform`."),
        ),
        hints=(
            ("True counts as 1, so the mean of `isnull()` is a fraction.", "تُحسب True بوصفها 1، لذا فإن متوسط `isnull()` نسبة."),
            ("`dropna()` without arguments removes every row with any missing value.", "يحذف `dropna()` دون وسائط كل صف فيه أي قيمة مفقودة."),
            ("`groupby(...)[col].transform(f)` returns one value per original row.", "يعيد `groupby(...)[col].transform(f)` قيمة لكل صف أصلي."),
        ),
        success=("Correct! Listwise deletion would keep only 2 of 8 customers; imputation keeps them all, but the group means assume customers in a segment are alike.",
                 "صحيح! كان الحذف الكامل للصفوف الناقصة سيُبقي عميلين فقط من ثمانية؛ أما التعويض فيحتفظ بهم جميعًا، لكن متوسطات المجموعات تفترض تشابه عملاء الشريحة الواحدة."),
        reflect=("What information can each method lose or distort?", "ما المعلومات التي قد تفقدها أو تشوّهها كل طريقة؟"),
    ),
    "COURSE-013.M07.L01.EX02": Guided(
        goal=("Detect outliers with Z-scores and with IQR fences, compare them, and cap the extremes.",
              "اكتشف القيم الشاذة بالدرجات المعيارية (Z-score) وبحدود المدى الربيعي، وقارن بينهما، ثم اقصص القيم المتطرفة."),
        steps=(
            ("Compute Z-scores.", "احسب الدرجات المعيارية."),
            ("Compute the IQR fences.", "احسب حدود المدى الربيعي."),
            ("List the values both methods flag.", "اذكر القيم التي تكتشفها الطريقتان."),
            ("Cap the series at the fences.", "اقصص السلسلة عند الحدود."),
        ),
        starter='''import pandas as pd

# Monthly income in thousands, with two clearly extreme values
income = pd.Series(list(range(40, 80)) + [300, 320], dtype=float)

# Step 1: how many standard deviations each value is from the mean
z = ___
z_outliers = income[z.abs() > 3].tolist()

q1, q3 = income.quantile(0.25), income.quantile(0.75)
iqr = q3 - q1
# Step 2: the Tukey fences
lower, upper = ___
iqr_outliers = income[(income < lower) | (income > upper)].tolist()

# Step 3: values flagged by both methods
both = ___
# Step 4: cap (winsorize) at the fences instead of deleting rows
capped = ___

print(z_outliers, iqr_outliers, both)
print(capped.max(), round(lower, 2), round(upper, 2))
''',
        answers=("(income - income.mean()) / income.std()", "q1 - 1.5 * iqr, q3 + 1.5 * iqr",
                 "sorted(set(z_outliers) & set(iqr_outliers))", "income.clip(lower=lower, upper=upper)"),
        checks=(
            check("[round(float(v), 4) for v in z.iloc[[0, -1]]] == [round(float(v), 4) for v in ((income - income.mean()) / income.std()).iloc[[0, -1]]]", True,
                  "Blank 1: subtract the mean and divide by the standard deviation.", "الفراغ 1: اطرح المتوسط ثم اقسم على الانحراف المعياري."),
            check("[round(float(lower), 2), round(float(upper), 2)]", [19.5, 101.5],
                  "Blank 2: lower = Q1 - 1.5·IQR, upper = Q3 + 1.5·IQR.", "الفراغ 2: الحد الأدنى = Q1 - 1.5·IQR، والأعلى = Q3 + 1.5·IQR."),
            check("list(both)", [300.0, 320.0], "Blank 3: intersect the two lists and sort.", "الفراغ 3: خذ تقاطع القائمتين ورتّب."),
            check("float(capped.max()) == float(upper) and len(capped) == 42 and float(capped.min()) == 40.0", True,
                  "Blank 4: `income.clip(lower=lower, upper=upper)` caps without dropping rows.", "الفراغ 4: يقصّ `income.clip(lower=lower, upper=upper)` دون حذف صفوف."),
        ),
        hints=(
            ("Series support arithmetic with scalars like the mean.", "تدعم السلاسل العمليات الحسابية مع قيم مفردة مثل المتوسط."),
            ("Tukey's rule uses 1.5 times the IQR.", "تستخدم قاعدة Tukey 1.5 ضعف المدى الربيعي."),
            ("`Series.clip` limits values to a range.", "تحصر `Series.clip` القيم في نطاق."),
        ),
        success=("Correct! Both methods flag 300 and 320; capping keeps every row but limits their pull on the mean - suitable if they are real but rare, not data-entry errors.",
                 "صحيح! تكتشف الطريقتان 300 و320؛ ويحتفظ القصّ بكل الصفوف لكنه يحدّ من تأثيرهما في المتوسط - وهذا مناسب إن كانت قيمًا حقيقية نادرة لا أخطاء إدخال."),
        reflect=("If the extremes were typos, would capping still be the right treatment? What would you do instead?",
                 "لو كانت القيم المتطرفة أخطاء كتابية، فهل يبقى القصّ المعالجة الصحيحة؟ وماذا ستفعل بدلًا منه؟"),
    ),
    "COURSE-013.M07.L01.EX03": Guided(
        goal=("Engineer features five ways: one-hot, label encoding, log transform, binning and two kinds of scaling.",
              "اصنع الخصائص بخمس طرق: One-hot، والترميز بالتسمية، والتحويل اللوغاريتمي، والتقسيم إلى فئات، ونوعين من التحجيم."),
        steps=(
            ("One-hot encode Country.", "رمّز Country بطريقة One-hot."),
            ("Label-encode Plan.", "رمّز Plan بالتسمية."),
            ("Log-transform Income.", "حوّل Income لوغاريتميًا."),
            ("Bin Income into three groups.", "قسّم Income إلى ثلاث فئات."),
            ("Min-max scale Income to 0-1.", "حجّم Income بطريقة min-max إلى 0-1."),
        ),
        starter='''import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler

customers = pd.DataFrame({
    "Country": ["EG", "SA", "EG", "AE", "SA"],
    "Plan": ["basic", "premium", "standard", "basic", "premium"],
    "Income": [30000, 85000, 52000, 41000, 120000],
})

# Step 1: one 0/1 column per country
encoded = ___
# Step 2: integer codes (alphabetical: basic=0, premium=1, standard=2)
customers["Plan_code"] = ___
# Step 3: log(1 + x) compresses large incomes
customers["Income_log"] = ___
# Step 4: low (<40k), middle (40k-80k), high (>80k)
customers["Income_Group"] = ___
customers["Income_std"] = StandardScaler().fit_transform(customers[["Income"]]).ravel()
# Step 5: rescale to the 0-1 range
customers["Income_minmax"] = ___
print(encoded.columns.tolist())
print(customers)
''',
        answers=(
            'pd.get_dummies(customers, columns=["Country"], dtype=int)',
            'LabelEncoder().fit_transform(customers["Plan"])',
            'np.log1p(customers["Income"])',
            'pd.cut(customers["Income"], bins=[0, 40000, 80000, np.inf], labels=["low", "middle", "high"])',
            'MinMaxScaler().fit_transform(customers[["Income"]]).ravel()',
        ),
        checks=(
            check("sorted(c for c in encoded.columns if str(c).startswith('Country_'))", ["Country_AE", "Country_EG", "Country_SA"],
                  "Blank 1: `pd.get_dummies(customers, columns=[\"Country\"], dtype=int)`.", "الفراغ 1: `pd.get_dummies(customers, columns=[\"Country\"], dtype=int)`."),
            check("[int(v) for v in customers['Plan_code']]", [0, 1, 2, 0, 1],
                  "Blank 2: `LabelEncoder().fit_transform(customers[\"Plan\"])`.", "الفراغ 2: `LabelEncoder().fit_transform(customers[\"Plan\"])`."),
            check("bool(np.allclose(customers['Income_log'], np.log1p(customers['Income'])))", True,
                  "Blank 3: `np.log1p(customers[\"Income\"])`.", "الفراغ 3: `np.log1p(customers[\"Income\"])`."),
            check("customers['Income_Group'].astype(str).tolist()", ["low", "high", "middle", "middle", "high"],
                  "Blank 4: `pd.cut` with bins [0, 40000, 80000, inf] and the three labels.", "الفراغ 4: `pd.cut` مع الحدود [0, 40000, 80000, inf] والتسميات الثلاث."),
            check("[round(float(v), 4) for v in customers['Income_minmax']]", [0.0, 0.6111, 0.2444, 0.1222, 1.0],
                  "Blank 5: `MinMaxScaler().fit_transform(customers[[\"Income\"]]).ravel()`.", "الفراغ 5: `MinMaxScaler().fit_transform(customers[[\"Income\"]]).ravel()`."),
        ),
        hints=(
            ("`pd.get_dummies(df, columns=[...])` replaces the column with indicators.", "يستبدل `pd.get_dummies(df, columns=[...])` العمود بمؤشرات."),
            ("Scalers expect a 2-D input: `customers[[\"Income\"]]`, then `.ravel()` flattens the result.", "تتوقع أدوات التحجيم مدخلًا ثنائي الأبعاد: `customers[[\"Income\"]]`، ثم يسطّح `.ravel()` النتيجة."),
            ("`pd.cut(values, bins=[...], labels=[...])` - one label per interval.", "`pd.cut(values, bins=[...], labels=[...])` - تسمية لكل فترة."),
        ),
        success=("Correct! One-hot keeps categories separate, label codes imply an order that 'basic < premium < standard' does not really have, the log tames large incomes, bins simplify, and scaling changes only the units.",
                 "صحيح! يُبقي One-hot الفئات منفصلة، وتفترض رموز التسمية ترتيبًا غير حقيقي في «basic < premium < standard»، ويروّض اللوغاريتم الدخول الكبيرة، وتبسّط الفئات، ولا يغيّر التحجيم إلا الوحدات."),
    ),
    "COURSE-013.M08.L01.EX01": Guided(
        goal=("Make a daily revenue series time-aware, then add lags, autocorrelation, a moving average and monthly totals.",
              "اجعل سلسلة الإيرادات اليومية واعية بالزمن، ثم أضف الإزاحات (lags) والارتباط الذاتي والمتوسط المتحرك والإجماليات الشهرية."),
        steps=(
            ("Parse the Date column as dates.", "حلّل عمود Date بوصفه تواريخ."),
            ("Create the 7-day lag.", "أنشئ الإزاحة لسبعة أيام."),
            ("Compute the lag-1 autocorrelation.", "احسب الارتباط الذاتي عند الإزاحة 1."),
            ("Compute the 7-day simple moving average.", "احسب المتوسط المتحرك البسيط لسبعة أيام."),
            ("Resample to month-end totals.", "أعد التجميع إلى إجماليات نهاية الشهر."),
        ),
        starter='''import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
dates = pd.date_range("2026-01-01", periods=60, freq="D")
revenue = 1000 + np.arange(60) * 5 + np.where(dates.dayofweek >= 5, 150, 0) + rng.normal(0, 20, 60)
df = pd.DataFrame({"Date": dates.strftime("%Y-%m-%d"), "Revenue": revenue.round(1)})

# Step 1: text -> datetime, then use it as the index
df["Date"] = ___
df = df.set_index("Date")

df["lag_1"] = df["Revenue"].shift(1)
# Step 2: the same weekday last week
df["lag_7"] = ___
# Step 3: how strongly today follows yesterday
autocorr_1 = ___
# Step 4: smooth out the weekly pattern
df["sma_7"] = ___
# Step 5: total revenue per calendar month
monthly = ___

print(df.head(8))
print(round(autocorr_1, 3))
print(monthly)
''',
        answers=('pd.to_datetime(df["Date"])', 'df["Revenue"].shift(7)', 'df["Revenue"].autocorr(lag=1)',
                 'df["Revenue"].rolling(7).mean()', 'df["Revenue"].resample("ME").sum()'),
        alternatives={},
        checks=(
            check("str(df.index.dtype).startswith('datetime64')", True, "Blank 1: `pd.to_datetime(df[\"Date\"])`.", "الفراغ 1: `pd.to_datetime(df[\"Date\"])`."),
            check("float(df['lag_7'].iloc[7]) == float(df['Revenue'].iloc[0]) and bool(df['lag_7'].iloc[:7].isna().all())", True,
                  "Blank 2: `df[\"Revenue\"].shift(7)`.", "الفراغ 2: `df[\"Revenue\"].shift(7)`."),
            check("abs(float(autocorr_1) - float(df['Revenue'].autocorr(lag=1))) < 1e-12", True,
                  "Blank 3: `df[\"Revenue\"].autocorr(lag=1)`.", "الفراغ 3: `df[\"Revenue\"].autocorr(lag=1)`."),
            check("abs(float(df['sma_7'].iloc[6]) - float(df['Revenue'].iloc[:7].mean())) < 1e-9 and bool(df['sma_7'].iloc[:6].isna().all())", True,
                  "Blank 4: `df[\"Revenue\"].rolling(7).mean()`.", "الفراغ 4: `df[\"Revenue\"].rolling(7).mean()`."),
            check("len(monthly) == 3 and abs(float(monthly.iloc[0]) - float(df['Revenue'].iloc[:31].sum())) < 1e-6", True,
                  "Blank 5: `df[\"Revenue\"].resample(\"ME\").sum()` - revenue adds up within a month.",
                  "الفراغ 5: `df[\"Revenue\"].resample(\"ME\").sum()` - تُجمع الإيرادات داخل الشهر."),
        ),
        hints=(
            ("Resampling and rolling windows need a DatetimeIndex.", "تحتاج إعادة التجميع والنوافذ المتحركة إلى فهرس من نوع DatetimeIndex."),
            ("`shift(n)` moves values n rows later; the first n become NaN.", "ينقل `shift(n)` القيم n صفًا إلى الأمام، وتصبح أول n قيم NaN."),
            ("\"ME\" is month-end; revenue is aggregated with `.sum()`.", "\"ME\" تعني نهاية الشهر، وتُجمع الإيرادات بـ `.sum()`."),
        ),
        success=("Correct! The series is now time-aware: lags line up past values, the 7-day average removes the weekend spike, and monthly totals show the trend.",
                 "صحيح! أصبحت السلسلة واعية بالزمن: تحاذي الإزاحات القيم السابقة، ويزيل المتوسط لسبعة أيام قفزة عطلة نهاية الأسبوع، وتُظهر الإجماليات الشهرية الاتجاه."),
        reflect=("With statsmodels installed locally, run `seasonal_decompose(df['Revenue'], model='additive', period=7)`. What do the trend, seasonal and residual parts show?",
                 "مع تثبيت statsmodels محليًا، شغّل `seasonal_decompose(df['Revenue'], model='additive', period=7)`. ماذا تُظهر مكوّنات الاتجاه والموسمية والبواقي؟"),
    ),
    "COURSE-013.M08.L01.EX02": Guided(
        goal=("Test stationarity with ADF and KPSS, then difference the series and test again.",
              "اختبر الاستقرار (stationarity) باختباري ADF وKPSS، ثم طبّق الفروق على السلسلة واختبرها مجددًا."),
        steps=(
            ("Get the ADF p-value.", "احصل على القيمة الاحتمالية لاختبار ADF."),
            ("Get the KPSS p-value with a constant.", "احصل على القيمة الاحتمالية لاختبار KPSS مع ثابت."),
            ("Take the first difference.", "خذ الفرق الأول."),
            ("Take the weekly seasonal difference.", "خذ الفرق الموسمي الأسبوعي."),
            ("Re-run ADF on the differenced series.", "أعد تشغيل ADF على السلسلة بعد الفروق."),
        ),
        starter='''from statsmodels.tsa.stattools import adfuller, kpss

# series: a pandas Series with a DatetimeIndex (e.g. the revenue from the previous exercise)

# Step 1: ADF  - H0: the series has a unit root (NOT stationary)
adf_p = ___
# Step 2: KPSS - H0: the series IS stationary around a constant
kpss_p = ___

# Step 3: remove the trend
first_diff = ___
# Step 4: remove the weekly pattern
seasonal_diff = ___

# Step 5: test again after the transformation
adf_p_after = ___
print(f"ADF p {adf_p:.3f} -> {adf_p_after:.3f} | KPSS p {kpss_p:.3f}")
''',
        answers=("adfuller(series)[1]", 'kpss(series, regression="c")[1]', "series.diff().dropna()", "series.diff(7).dropna()", "adfuller(first_diff)[1]"),
        blanks=(
            ("the p-value is item `[1]` of `adfuller(series)`.", "القيمة الاحتمالية هي العنصر `[1]` من `adfuller(series)`."),
            ("`kpss(series, regression=\"c\")[1]`.", "`kpss(series, regression=\"c\")[1]`."),
            ("`series.diff().dropna()`.", "`series.diff().dropna()`."),
            ("`series.diff(7).dropna()`.", "`series.diff(7).dropna()`."),
            ("`adfuller(first_diff)[1]`.", "`adfuller(first_diff)[1]`."),
        ),
        hints=(
            ("The two tests have opposite null hypotheses - read their p-values in opposite directions.", "للاختبارين فرضيتان صفريتان متعاكستان - فاقرأ قيمتيهما الاحتماليتين في اتجاهين متعاكسين."),
            ("`diff()` subtracts the previous value; `diff(7)` the value a week earlier.", "يطرح `diff()` القيمة السابقة، ويطرح `diff(7)` القيمة قبل أسبوع."),
            ("Differencing leaves NaN at the start - drop it before testing.", "تترك الفروق قيم NaN في البداية - احذفها قبل الاختبار."),
        ),
        success=("Correct! A small ADF p-value (reject the unit root) together with a large KPSS p-value (do not reject stationarity) is the combination you want after differencing.",
                 "صحيح! القيمة الاحتمالية الصغيرة لـ ADF (رفض جذر الوحدة) مع القيمة الكبيرة لـ KPSS (عدم رفض الاستقرار) هي التركيبة المرغوبة بعد الفروق."),
        expected=READ_NOTE,
    ),
    "COURSE-013.M08.L01.EX04": Guided(
        goal=("Evaluate a 7-period forecast with MAE, RMSE and a zero-safe MAPE.",
              "قيّم تنبؤًا لسبع فترات بمقاييس MAE وRMSE وMAPE الآمن مع القيم الصفرية."),
        steps=(
            ("Compute MAE.", "احسب MAE."),
            ("Compute RMSE.", "احسب RMSE."),
            ("Compute MAPE, skipping zero actuals.", "احسب MAPE مع تخطي القيم الفعلية الصفرية."),
        ),
        starter='''import numpy as np

# The last seven periods, in time order - the test set is never shuffled
actual = np.array([120, 0, 135, 150, 160, 155, 170], dtype=float)
predicted = np.array([118, 5, 140, 145, 170, 150, 160], dtype=float)
errors = actual - predicted

# Step 1: average size of the errors
mae = ___
# Step 2: like MAE, but large errors weigh more
rmse = ___
# Step 3: average percentage error; a zero actual would divide by zero
nonzero = actual != 0
mape = ___

print(round(mae, 3), round(rmse, 3), f"{mape:.2f}%")
''',
        answers=("np.mean(np.abs(errors))", "np.sqrt(np.mean(errors ** 2))", "np.mean(np.abs(errors[nonzero] / actual[nonzero])) * 100"),
        checks=(
            check("round(float(mae), 4)", 6.0, "Blank 1: mean of the absolute errors.", "الفراغ 1: متوسط القيم المطلقة للأخطاء."),
            check("round(float(rmse), 4)", 6.59, "Blank 2: square root of the mean squared error.", "الفراغ 2: الجذر التربيعي لمتوسط مربعات الأخطاء."),
            check("round(float(mape), 3)", 4.01, "Blank 3: use only `nonzero` positions, then multiply by 100.",
                  "الفراغ 3: استخدم المواضع `nonzero` فقط، ثم اضرب في 100."),
        ),
        hints=(
            ("`np.abs` and `np.mean` are enough for MAE.", "يكفي `np.abs` و`np.mean` لحساب MAE."),
            ("RMSE = sqrt(mean(error²)).", "RMSE = الجذر التربيعي لمتوسط مربع الخطأ."),
            ("Boolean indexing `errors[nonzero]` keeps only the safe positions.", "تحتفظ الفهرسة المنطقية `errors[nonzero]` بالمواضع الآمنة فقط."),
        ),
        success=("Correct! RMSE (6.59) is above MAE (6.0) because the two 10-unit misses weigh more; MAPE says forecasts are off by about 4% on average.",
                 "صحيح! RMSE (6.59) أعلى من MAE (6.0) لأن الخطأين بمقدار 10 وحدات يزنان أكثر؛ ويقول MAPE إن التنبؤات تبتعد بنحو 4% في المتوسط."),
        reflect=("State one limitation of each metric, and what MAPE tells a business user that MAE does not.",
                 "اذكر قيدًا واحدًا لكل مقياس، وما الذي يخبر به MAPE المستخدمَ في قطاع الأعمال ولا يخبره به MAE."),
    ),
    "COURSE-013.M09.L01.EX01": Guided(
        goal=("Fit and diagnose a one-predictor regression, then compare polynomial degrees on held-out points.",
              "درّب انحدارًا بمتغير تنبؤي واحد وشخّصه، ثم قارن درجات كثيرات الحدود على نقاط محجوزة."),
        steps=(
            ("Fit the OLS line.", "درّب خط المربعات الصغرى (OLS)."),
            ("Compute the residuals.", "احسب البواقي."),
            ("Compute adjusted R².", "احسب R² المعدَّل."),
            ("Compute the Durbin-Watson statistic.", "احسب إحصاء Durbin-Watson."),
            ("Pick the polynomial degree with the lowest validation error.", "اختر درجة كثير الحدود ذات أقل خطأ تحقق."),
        ),
        starter='''import numpy as np
from scipy import stats

experience = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
salary = np.array([35, 38, 44, 47, 50, 56, 58, 63, 66, 72], dtype=float)

# Step 1: ordinary least squares with one predictor
fit = ___
fitted = fit.intercept + fit.slope * experience
# Step 2: what the line does not explain
residuals = ___
r2 = fit.rvalue ** 2
n, k = len(salary), 1
# Step 3: R² penalised for the number of predictors
adjusted_r2 = ___
shapiro_p = stats.shapiro(residuals).pvalue          # H0: residuals are normal
# Step 4: about 2 means no autocorrelation in the residuals
durbin_watson = ___

# Underfit vs good fit vs overfit on a curved dataset
rng = np.random.default_rng(0)
x = np.linspace(-3, 3, 30)
y = x ** 2 + rng.normal(0, 1, 30)
train, validation = np.arange(30) % 3 != 0, np.arange(30) % 3 == 0

def validation_error(degree):
    coefficients = np.polyfit(x[train], y[train], degree)
    return float(np.mean((np.polyval(coefficients, x[validation]) - y[validation]) ** 2))

errors = {degree: round(validation_error(degree), 2) for degree in (1, 2, 12)}
# Step 5: the degree that generalises best
best_degree = ___
print(round(fit.slope, 3), round(fit.stderr, 3), f"p={fit.pvalue:.2g}", round(r2, 3), round(adjusted_r2, 3), round(durbin_watson, 2))
print(errors, best_degree)
''',
        answers=("stats.linregress(experience, salary)", "salary - fitted", "1 - (1 - r2) * (n - 1) / (n - k - 1)",
                 "np.sum(np.diff(residuals) ** 2) / np.sum(residuals ** 2)", "min(errors, key=errors.get)"),
        checks=(
            check("round(float(fit.slope), 4) == round(float(stats.linregress(experience, salary).slope), 4)", True,
                  "Blank 1: `stats.linregress(experience, salary)`.", "الفراغ 1: `stats.linregress(experience, salary)`."),
            check("bool(np.allclose(residuals, salary - fitted)) and abs(float(np.sum(residuals))) < 1e-9", True,
                  "Blank 2: residual = actual - fitted.", "الفراغ 2: الباقي = الفعلي - الملائم."),
            check("round(float(adjusted_r2), 6) == round(1 - (1 - float(r2)) * 9 / 8, 6)", True,
                  "Blank 3: 1 - (1 - R²)(n - 1)/(n - k - 1).", "الفراغ 3: 1 - (1 - R²)(n - 1)/(n - k - 1)."),
            check("round(float(durbin_watson), 6) == round(float(np.sum(np.diff(residuals) ** 2) / np.sum(residuals ** 2)), 6)", True,
                  "Blank 4: sum of squared successive differences over the sum of squared residuals.", "الفراغ 4: مجموع مربعات الفروق المتتالية مقسومًا على مجموع مربعات البواقي."),
            check("best_degree", 2, "Blank 5: `min(errors, key=errors.get)` - degree 1 underfits, degree 12 overfits.",
                  "الفراغ 5: `min(errors, key=errors.get)` - الدرجة 1 تقصّر في الملاءمة، والدرجة 12 تفرط فيها."),
        ),
        hints=(
            ("`stats.linregress` returns slope, intercept, rvalue, pvalue and stderr.", "تعيد `stats.linregress` الميل والمقطع وrvalue وpvalue وstderr."),
            ("`np.diff(residuals)` gives successive differences.", "يعطي `np.diff(residuals)` الفروق المتتالية."),
            ("Validation error, not training error, reveals overfitting.", "يكشف خطأ التحقق، لا خطأ التدريب، فرطَ الملاءمة."),
        ),
        success=("Correct! The line fits tightly (R² ≈ 0.99), the residual checks look clean, and on the curved data degree 2 beats both the underfitting line and the overfitting degree-12 curve.",
                 "صحيح! يلائم الخط البيانات بإحكام (R² ≈ 0.99)، وتبدو فحوص البواقي سليمة، وفي البيانات المنحنية تتفوق الدرجة 2 على الخط المقصّر وعلى منحنى الدرجة 12 المفرط."),
    ),
    "COURSE-013.M09.L01.EX02": Guided(
        goal=("Build the preprocessing pipeline KNN needs for a churn dataset: scale numeric columns and one-hot encode categories.",
              "ابنِ خط المعالجة المسبقة الذي يحتاجه KNN لبيانات انسحاب العملاء: حجّم الأعمدة الرقمية ورمّز الفئات بطريقة One-hot."),
        steps=(
            ("Scale the numeric columns.", "حجّم الأعمدة الرقمية."),
            ("One-hot encode the contract type.", "رمّز نوع العقد بطريقة One-hot."),
            ("Chain preprocessing and KNN in one Pipeline.", "اربط المعالجة المسبقة وKNN في Pipeline واحد."),
            ("Predict for a new customer.", "تنبّأ لعميل جديد."),
        ),
        starter='''import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

churn = pd.DataFrame({
    "tenure_months": [2, 30, 5, 48, 1, 24, 60, 3, 36, 8, 12, 55],
    "monthly_charges": [80, 45, 95, 40, 99, 55, 35, 90, 50, 85, 70, 38],
    "contract": ["monthly", "yearly", "monthly", "two-year", "monthly", "yearly",
                 "two-year", "monthly", "yearly", "monthly", "monthly", "two-year"],
    "churned": [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
})
X, y = churn.drop(columns="churned"), churn["churned"]

preprocess = ColumnTransformer([
    # Step 1: KNN measures distances, so put numbers on the same scale
    ("numeric", ___, ["tenure_months", "monthly_charges"]),
    # Step 2: categories become 0/1 columns
    ("categorical", ___, ["contract"]),
])
# Step 3: preprocessing is fitted together with the model
knn_pipeline = ___
knn_pipeline.fit(X, y)

new_customer = pd.DataFrame({"tenure_months": [4], "monthly_charges": [92], "contract": ["monthly"]})
# Step 4
prediction = ___
print("churn" if prediction == 1 else "stays")
''',
        answers=("StandardScaler()", 'OneHotEncoder(handle_unknown="ignore")',
                 'Pipeline([("preprocess", preprocess), ("knn", KNeighborsClassifier(n_neighbors=3))])',
                 "int(knn_pipeline.predict(new_customer)[0])"),
        checks=(
            check("hasattr(knn_pipeline.named_steps['preprocess'].named_transformers_['numeric'], 'mean_')", True,
                  "Blank 1: use `StandardScaler()` for the numeric columns.", "الفراغ 1: استخدم `StandardScaler()` للأعمدة الرقمية."),
            check("sorted(str(c) for c in knn_pipeline.named_steps['preprocess'].named_transformers_['categorical'].categories_[0])", ["monthly", "two-year", "yearly"],
                  "Blank 2: use `OneHotEncoder(handle_unknown=\"ignore\")`.", "الفراغ 2: استخدم `OneHotEncoder(handle_unknown=\"ignore\")`."),
            check("isinstance(knn_pipeline.steps[-1][1], KNeighborsClassifier)", True,
                  "Blank 3: a `Pipeline` whose last step is `KNeighborsClassifier(n_neighbors=3)`.", "الفراغ 3: `Pipeline` خطوته الأخيرة `KNeighborsClassifier(n_neighbors=3)`."),
            check("prediction", 1, "Blank 4: `int(knn_pipeline.predict(new_customer)[0])`.", "الفراغ 4: `int(knn_pipeline.predict(new_customer)[0])`."),
        ),
        hints=(
            ("Unscaled, tenure (0-60) and charges (35-99) would dominate distances differently.", "دون تحجيم، تهيمن مدة الاشتراك (0-60) والرسوم (35-99) على المسافات بشكل مختلف."),
            ("`handle_unknown=\"ignore\"` keeps prediction working for unseen categories.", "يحافظ `handle_unknown=\"ignore\"` على عمل التنبؤ مع الفئات غير المرئية."),
            ("A Pipeline is a list of (name, step) pairs.", "الـ Pipeline قائمة من أزواج (الاسم، الخطوة)."),
        ),
        success=("Correct! A short-tenure, high-charge, monthly-contract customer is predicted to churn - and because preprocessing lives in the pipeline it is fitted on training data only.",
                 "صحيح! يُتنبّأ بأن العميل قصير الاشتراك مرتفع الرسوم ذا العقد الشهري سينسحب - ولأن المعالجة المسبقة داخل الـ Pipeline فإنها تُدرَّب على بيانات التدريب فقط."),
        reflect=("Compare Logistic Regression, KNN, Decision Tree and Gaussian Naive Bayes: which need scaling, which are parametric, and one caveat for each.",
                 "قارن Logistic Regression وKNN وDecision Tree وGaussian Naive Bayes: أيها يحتاج إلى تحجيم، وأيها معلمي، وتحفّظًا واحدًا لكلٍّ منها."),
    ),
    "COURSE-013.M09.L01.EX03": Guided(
        goal=("Evaluate a churn classifier honestly: stratified split, training-only fit, the confusion matrix, and cross-validation.",
              "قيّم مصنّف انسحاب العملاء بأمانة: تقسيم طبقي، وتدريب على بيانات التدريب فقط، ومصفوفة الالتباس، والتحقق المتقاطع."),
        steps=(
            ("Split 80/20, stratified, with random_state=42.", "قسّم 80/20 تقسيمًا طبقيًا مع random_state=42."),
            ("Fit the pipeline on the training data only.", "درّب الـ Pipeline على بيانات التدريب فقط."),
            ("Compute recall for the churn class.", "احسب Recall لفئة الانسحاب."),
            ("Run 5-fold cross-validation on the whole pipeline.", "نفّذ تحققًا متقاطعًا بخمسة أجزاء على الـ Pipeline كاملًا."),
        ),
        starter='''import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=400, n_features=6, weights=[0.75, 0.25], random_state=42)   # 1 = churned

# Step 1: keep the churn rate the same in both parts
X_train, X_test, y_train, y_test = ___
pipeline = make_pipeline(StandardScaler(), LogisticRegression())
# Step 2: the test set stays unseen
___
y_pred = pipeline.predict(X_test)
churn_probability = pipeline.predict_proba(X_test)[:, 1]

tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
accuracy, precision = accuracy_score(y_test, y_pred), precision_score(y_test, y_pred)
# Step 3: of the customers who really churned, how many did we catch?
recall = ___
f1 = f1_score(y_test, y_pred)

# Step 4: five fresh fits of the whole pipeline, scored with F1
cv_scores = ___
print(f"TP {tp} FP {fp} FN {fn} TN {tn} | acc {accuracy:.3f} P {precision:.3f} R {recall:.3f} F1 {f1:.3f}")
print("CV F1:", cv_scores.round(3), "mean", round(cv_scores.mean(), 3))
''',
        answers=(
            "train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)",
            "pipeline.fit(X_train, y_train)",
            "recall_score(y_test, y_pred)",
            'cross_val_score(pipeline, X, y, cv=5, scoring="f1")',
        ),
        checks=(
            check("len(y_test) == 80 and abs(float(y_test.mean()) - float(y.mean())) < 0.02", True,
                  "Blank 1: `train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)`.", "الفراغ 1: `train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)`."),
            check("bool(np.allclose(make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)[-1].coef_, pipeline[-1].coef_))", True,
                  "Blank 2: fit with `X_train` and `y_train` only.", "الفراغ 2: درّب باستخدام `X_train` و`y_train` فقط."),
            check("abs(float(recall) - tp / (tp + fn)) < 1e-12", True, "Blank 3: `recall_score(y_test, y_pred)` = TP / (TP + FN).",
                  "الفراغ 3: `recall_score(y_test, y_pred)` = TP / (TP + FN)."),
            check("len(cv_scores) == 5 and abs(float(cv_scores.mean()) - float(cross_val_score(make_pipeline(StandardScaler(), LogisticRegression()), X, y, cv=5, scoring='f1').mean())) < 1e-9", True,
                  "Blank 4: `cross_val_score(pipeline, X, y, cv=5, scoring=\"f1\")`.", "الفراغ 4: `cross_val_score(pipeline, X, y, cv=5, scoring=\"f1\")`."),
        ),
        hints=(
            ("`stratify=y` keeps the class balance in both splits.", "يحافظ `stratify=y` على توازن الفئات في القسمين."),
            ("Recall = TP / (TP + FN): the share of real churners you caught.", "Recall = TP / (TP + FN): نسبة المنسحبين الفعليين الذين اكتشفتهم."),
            ("Cross-validating the pipeline refits the scaler inside every fold.", "التحقق المتقاطع على الـ Pipeline يعيد تدريب أداة التحجيم داخل كل جزء."),
        ),
        success=("Correct! FP = a loyal customer you would spend retention money on; FN = a churner you missed. Compare the single test score with the CV mean to see how much one split can vary.",
                 "صحيح! الإيجابي الكاذب عميل وفيّ ستنفق عليه ميزانية الاحتفاظ، والسلبي الكاذب منسحب فاتك. قارن نتيجة الاختبار الواحد بمتوسط التحقق المتقاطع لترى مقدار تفاوت تقسيم واحد."),
        reflect=("For an expensive retention campaign, would you prioritise precision or recall? Why?", "في حملة احتفاظ مكلفة، هل ستعطي الأولوية لـ Precision أم لـ Recall؟ ولماذا؟"),
    ),
    "COURSE-013.M10.L01.EX01": Guided(
        goal=("Standardize customer-behaviour features, choose PCA components by explained variance, check the 2-D map's trustworthiness and read the loadings.",
              "وحّد مقياس خصائص سلوك العملاء، واختر مكوّنات PCA حسب التباين المفسَّر، وتحقّق من موثوقية الخريطة ثنائية الأبعاد، واقرأ الأوزان (loadings)."),
        steps=(
            ("Standardize all features.", "وحّد مقياس كل الخصائص."),
            ("Compute the cumulative explained variance.", "احسب التباين المفسَّر التراكمي."),
            ("Measure the trustworthiness of the 2-D projection.", "قِس موثوقية الإسقاط ثنائي الأبعاد."),
            ("Build the loading table for PC1 and PC2.", "ابنِ جدول الأوزان لـ PC1 وPC2."),
        ),
        starter='''import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import trustworthiness
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(0)
engagement, spending = rng.normal(size=200), rng.normal(size=200)
behaviour = pd.DataFrame({
    "visits": engagement * 3 + 20,
    "minutes": engagement * 30 + 120 + rng.normal(0, 5, 200),
    "purchases": spending * 2 + 5,
    "basket_value": spending * 40 + 80 + rng.normal(0, 5, 200),
    "returns": rng.normal(1, 0.5, 200),
})

# Step 1: mean 0 and standard deviation 1 for every column
X = ___
# Step 2: running total of the variance each component explains
cumulative = ___
components_95 = int(np.argmax(cumulative >= 0.95) + 1)

pca2 = PCA(n_components=2).fit(X)
X_2d = pca2.transform(X)
# Step 3: how well the 2-D map preserves each point's neighbours (1.0 = perfectly)
trust = ___
# Step 4: one row per original feature, one column per component
loadings = ___
print(cumulative.round(3), components_95, round(trust, 3))
print(loadings.round(2))
''',
        answers=(
            "StandardScaler().fit_transform(behaviour)",
            "np.cumsum(PCA().fit(X).explained_variance_ratio_)",
            "trustworthiness(X, X_2d, n_neighbors=5)",
            'pd.DataFrame(pca2.components_.T, index=behaviour.columns, columns=["PC1", "PC2"])',
        ),
        checks=(
            check("bool(np.allclose(np.asarray(X).mean(axis=0), 0, atol=1e-9)) and bool(np.allclose(np.asarray(X).std(axis=0), 1))", True,
                  "Blank 1: `StandardScaler().fit_transform(behaviour)`.", "الفراغ 1: `StandardScaler().fit_transform(behaviour)`."),
            check("len(cumulative) == 5 and abs(float(cumulative[-1]) - 1.0) < 1e-9 and bool(np.all(np.diff(cumulative) >= 0))", True,
                  "Blank 2: `np.cumsum(PCA().fit(X).explained_variance_ratio_)`.", "الفراغ 2: `np.cumsum(PCA().fit(X).explained_variance_ratio_)`."),
            check("abs(float(trust) - float(trustworthiness(X, X_2d, n_neighbors=5))) < 1e-12", True,
                  "Blank 3: `trustworthiness(X, X_2d, n_neighbors=5)`.", "الفراغ 3: `trustworthiness(X, X_2d, n_neighbors=5)`."),
            check("list(loadings.shape) == [5, 2] and list(loadings.columns) == ['PC1', 'PC2'] and list(loadings.index) == list(behaviour.columns)", True,
                  "Blank 4: transpose `pca2.components_` so features are rows.", "الفراغ 4: انقل `pca2.components_` لتصبح الخصائص صفوفًا."),
        ),
        hints=(
            ("PCA is scale-sensitive, so standardize first.", "تتأثر PCA بالمقياس، لذا وحّده أولًا."),
            ("`explained_variance_ratio_` lists each component's share; `np.cumsum` adds them up.", "يسرد `explained_variance_ratio_` حصة كل مكوّن، ويجمعها `np.cumsum`."),
            ("`components_` is (components × features); `.T` flips it.", "`components_` بالأبعاد (مكوّنات × خصائص)، و`.T` يقلبها."),
        ),
        success=("Correct! Two components capture the engagement and spending patterns, `returns` is mostly noise, and the trustworthiness score tells you how faithful the 2-D picture is.",
                 "صحيح! يلتقط مكوّنان نمطي التفاعل والإنفاق، و`returns` في معظمه ضجيج، وتخبرك درجة الموثوقية بمدى أمانة الصورة ثنائية الأبعاد."),
        reflect=("Which features load most on PC1 and PC2, and what information do you lose by keeping only two components?",
                 "أي الخصائص لها أكبر وزن في PC1 وPC2؟ وما المعلومات التي تخسرها بالاحتفاظ بمكوّنين فقط؟"),
    ),
    "COURSE-013.M10.L01.EX02": Guided(
        goal=("Compare K-Means, hierarchical clustering and DBSCAN on the same data with three internal metrics.",
              "قارن K-Means والتجميع الهرمي وDBSCAN على البيانات نفسها بثلاثة مقاييس داخلية."),
        steps=(
            ("Compute K-Means inertia for K = 1 to 8 (the elbow curve).", "احسب قصور K-Means لقيم K من 1 إلى 8 (منحنى المرفق)."),
            ("Fit the chosen K-Means with K = 4.", "درّب K-Means المختار مع K = 4."),
            ("Fit Ward hierarchical clustering with 4 clusters.", "درّب التجميع الهرمي بطريقة Ward بأربعة عناقيد."),
            ("Score clusterings with silhouette, Calinski-Harabasz and Davies-Bouldin.", "قيّم التجميعات بمقاييس silhouette وCalinski-Harabasz وDavies-Bouldin."),
        ),
        starter='''import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler

X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=42)
X = StandardScaler().fit_transform(X)

# Step 1: within-cluster sum of squares for K = 1..8
inertias = ___
# Step 2: the K at the elbow
kmeans_labels = ___
# Step 3: bottom-up merging with Ward linkage, cut at 4 clusters
hier_labels = ___
dbscan_labels = DBSCAN(eps=0.3, min_samples=5).fit_predict(X)      # -1 = noise

def scores(labels):
    keep = labels != -1                                             # ignore DBSCAN noise
    # Step 4: (silhouette, Calinski-Harabasz, Davies-Bouldin)
    return ___

results = {name: scores(labels) for name, labels in
           (("kmeans", kmeans_labels), ("ward", hier_labels), ("dbscan", dbscan_labels))
           if len(set(labels.tolist()) - {-1}) >= 2}
print([round(v) for v in inertias])
print(results)
''',
        answers=(
            "[KMeans(n_clusters=k, n_init=10, random_state=42).fit(X).inertia_ for k in range(1, 9)]",
            "KMeans(n_clusters=4, n_init=10, random_state=42).fit_predict(X)",
            'AgglomerativeClustering(n_clusters=4, linkage="ward").fit_predict(X)',
            "(round(silhouette_score(X[keep], labels[keep]), 3), round(calinski_harabasz_score(X[keep], labels[keep]), 1), round(davies_bouldin_score(X[keep], labels[keep]), 3))",
        ),
        checks=(
            check("len(inertias) == 8 and all(a >= b for a, b in zip(inertias, inertias[1:]))", True,
                  "Blank 1: one inertia per K from 1 to 8; it can only go down as K grows.", "الفراغ 1: قيمة قصور لكل K من 1 إلى 8؛ ولا يمكن إلا أن تنخفض مع ازدياد K."),
            check("len(set(np.asarray(kmeans_labels).tolist())) == 4", True,
                  "Blank 2: `KMeans(n_clusters=4, n_init=10, random_state=42).fit_predict(X)`.", "الفراغ 2: `KMeans(n_clusters=4, n_init=10, random_state=42).fit_predict(X)`."),
            check("len(set(np.asarray(hier_labels).tolist())) == 4", True,
                  "Blank 3: `AgglomerativeClustering(n_clusters=4, linkage=\"ward\").fit_predict(X)`.", "الفراغ 3: `AgglomerativeClustering(n_clusters=4, linkage=\"ward\").fit_predict(X)`."),
            check("list(results['kmeans']) == [round(silhouette_score(X, kmeans_labels), 3), round(calinski_harabasz_score(X, kmeans_labels), 1), round(davies_bouldin_score(X, kmeans_labels), 3)]", True,
                  "Blank 4: return the three rounded scores computed on the non-noise points.", "الفراغ 4: أعد الدرجات الثلاث المقرّبة المحسوبة على النقاط غير الضجيجية."),
        ),
        hints=(
            ("`KMeans(...).fit(X).inertia_` is the within-cluster sum of squares.", "`KMeans(...).fit(X).inertia_` هو مجموع المربعات داخل العناقيد."),
            ("`fit_predict` returns one label per point.", "تعيد `fit_predict` تسمية لكل نقطة."),
            ("Higher silhouette and Calinski-Harabasz are better; lower Davies-Bouldin is better.", "الأعلى أفضل في silhouette وCalinski-Harabasz، والأقل أفضل في Davies-Bouldin."),
        ),
        success=("Correct! On four compact blobs K-Means and Ward agree and score well; DBSCAN shines instead on irregular shapes with noise.",
                 "صحيح! مع أربع كتل متراصّة يتفق K-Means وWard ويحققان درجات جيدة، بينما يتألق DBSCAN مع الأشكال غير المنتظمة والضجيج."),
        reflect=("Draw the elbow curve and a dendrogram locally. Which algorithm best matches compact, hierarchical or irregular/noisy structure?",
                 "ارسم منحنى المرفق ومخططًا شجريًا محليًا. أي خوارزمية تناسب البنية المتراصّة أو الهرمية أو غير المنتظمة/الضجيجية؟"),
    ),
    "COURSE-013.M10.L01.EX03": Guided(
        goal=("Compare Isolation Forest and Local Outlier Factor on data with global and local anomalies.",
              "قارن Isolation Forest وLocal Outlier Factor على بيانات فيها قيم شاذة عامة ومحلية."),
        steps=(
            ("Turn Isolation Forest scores into 'higher = more anomalous'.", "حوّل درجات Isolation Forest إلى «الأعلى = أكثر شذوذًا»."),
            ("Do the same for LOF.", "افعل الشيء نفسه لـ LOF."),
            ("Take each model's top-10 anomalies.", "خذ أعلى 10 قيم شاذة لكل نموذج."),
            ("Count how many top-10 points the models share.", "عُدّ النقاط المشتركة بين قائمتي أعلى 10."),
        ),
        starter='''import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(1)
dense = rng.normal([50, 5], [3, 0.5], size=(150, 2))          # a tight segment: spend, visits
loose = rng.normal([100, 2], [15, 1.0], size=(60, 2))         # a broad, loose segment
global_anomalies = np.array([[250, 20], [260, 22], [240, 19]])  # rows 210-212: far from everyone
local_anomalies = np.array([[60, 3.0], [41, 7.0]])              # rows 213-214: odd only next to the tight segment
X = StandardScaler().fit_transform(np.vstack([dense, loose, global_anomalies, local_anomalies]))

# Step 1: sklearn's score_samples is higher for NORMAL points - flip the sign
iso_scores = ___
# Step 2: LOF stores the negated factor - flip it too
lof = LocalOutlierFactor(n_neighbors=20).fit(X)
lof_scores = ___
# Step 3: indices of the 10 most anomalous points
iso_top10 = ___
lof_top10 = set(np.argsort(-lof_scores)[:10].tolist())
# Step 4: how many points do both models put in their top 10?
agreement = ___

print(sorted(iso_top10), sorted(lof_top10), agreement)
''',
        answers=("-IsolationForest(random_state=0).fit(X).score_samples(X)", "-lof.negative_outlier_factor_",
                 "set(np.argsort(-iso_scores)[:10].tolist())", "len(iso_top10 & lof_top10)"),
        checks=(
            check("bool(np.allclose(iso_scores, -IsolationForest(random_state=0).fit(X).score_samples(X)))", True,
                  "Blank 1: `-IsolationForest(random_state=0).fit(X).score_samples(X)`.", "الفراغ 1: `-IsolationForest(random_state=0).fit(X).score_samples(X)`."),
            check("bool(np.allclose(lof_scores, -lof.negative_outlier_factor_)) and float(lof_scores.min()) > 0", True,
                  "Blank 2: `-lof.negative_outlier_factor_`.", "الفراغ 2: `-lof.negative_outlier_factor_`."),
            check("{210, 211, 212} <= iso_top10 and len(iso_top10) == 10", True,
                  "Blank 3: sort scores from high to low and keep the first ten indices as a set.", "الفراغ 3: رتّب الدرجات تنازليًا واحتفظ بأول عشرة فهارس في مجموعة."),
            check("agreement == len(iso_top10 & set(np.argsort(-lof_scores)[:10].tolist()))", True,
                  "Blank 4: the size of the intersection of the two sets.", "الفراغ 4: حجم تقاطع المجموعتين."),
        ),
        hints=(
            ("Both models report 'normality'; negate to rank anomalies first.", "يعبّر النموذجان عن «الطبيعية»؛ اعكس الإشارة لترتيب القيم الشاذة أولًا."),
            ("`np.argsort(-scores)[:10]` gives the ten largest.", "يعطي `np.argsort(-scores)[:10]` أكبر عشر قيم."),
            ("Set intersection: `a & b`.", "تقاطع المجموعات: `a & b`."),
        ),
        success=("Correct! Both models catch the far-away global anomalies, but they disagree near the dense segment: LOF judges density relative to neighbours, Isolation Forest judges how easily a point is isolated overall.",
                 "صحيح! يلتقط النموذجان القيم الشاذة العامة البعيدة، لكنهما يختلفان قرب الشريحة الكثيفة: يحكم LOF على الكثافة نسبةً إلى الجيران، ويحكم Isolation Forest على مدى سهولة عزل النقطة إجمالًا."),
        reflect=("Inspect rows 213 and 214 in both rankings. Why might the two algorithms disagree about them?",
                 "افحص الصفين 213 و214 في الترتيبين. لماذا قد تختلف الخوارزميتان بشأنهما؟"),
    ),
    "COURSE-013.M11.L01.EX01": Guided(
        goal=("Compare a bootstrapped Random Forest (with out-of-bag scoring) and Extra Trees on churn data.",
              "قارن Random Forest بالعينات المعادة (مع تقييم خارج الحقيبة OOB) وExtra Trees على بيانات انسحاب العملاء."),
        steps=(
            ("One-hot encode the plan column inside the pipeline.", "رمّز عمود الخطة بطريقة One-hot داخل الـ Pipeline."),
            ("Turn on bootstrapping and the out-of-bag score.", "فعّل أخذ العينات المعادة وتقييم OOB."),
            ("Fit Extra Trees with the same number of trees.", "درّب Extra Trees بعدد الأشجار نفسه."),
            ("Read the forest's most important feature.", "اقرأ الخاصية الأهم في الغابة."),
        ),
        starter='''import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

rng = np.random.default_rng(3)
n = 400
df = pd.DataFrame({
    "tenure": rng.integers(1, 60, n),
    "monthly_charges": rng.uniform(20, 110, n).round(1),
    "plan": rng.choice(["monthly", "yearly", "two-year"], n),
})
df["churned"] = ((df["plan"] == "monthly") & (df["tenure"] < 12) | (df["monthly_charges"] > 95)).astype(int)
X, y = df.drop(columns="churned"), df["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

# Step 1: encode the categorical column, pass the numbers through
preprocess = ColumnTransformer([("plan", ___, ["plan"])], remainder="passthrough")
# Step 2: each tree sees a bootstrap sample; the left-out rows give a free validation score
forest = make_pipeline(preprocess, RandomForestClassifier(n_estimators=100, bootstrap=___, oob_score=___, random_state=42))
forest.fit(X_train, y_train)
# Step 3: random split thresholds instead of the best ones
extra = make_pipeline(preprocess, ___)
extra.fit(X_train, y_train)

names = forest[0].get_feature_names_out()
# Step 4: the forest's most important feature
top_feature = ___
print("OOB", round(forest[-1].oob_score_, 3), "| RF test", round(forest.score(X_test, y_test), 3),
      "| ET test", round(extra.score(X_test, y_test), 3), "| top:", top_feature)
''',
        answers=('OneHotEncoder(handle_unknown="ignore")', "True", "True",
                 "ExtraTreesClassifier(n_estimators=100, random_state=42)", "names[int(np.argmax(forest[-1].feature_importances_))]"),
        checks=(
            check("any('plan_monthly' in str(n) for n in names)", True, "Blank 1: `OneHotEncoder(handle_unknown=\"ignore\")`.",
                  "الفراغ 1: `OneHotEncoder(handle_unknown=\"ignore\")`."),
            check("0.5 < float(forest[-1].oob_score_) <= 1.0", True, "Blanks 2-3: `bootstrap=True, oob_score=True`.",
                  "الفراغان 2 و3: `bootstrap=True, oob_score=True`."),
            check("isinstance(extra[-1], ExtraTreesClassifier) and extra[-1].n_estimators == 100 and hasattr(extra[-1], 'estimators_')", True,
                  "Blank 4: `ExtraTreesClassifier(n_estimators=100, random_state=42)`.", "الفراغ 4: `ExtraTreesClassifier(n_estimators=100, random_state=42)`."),
            check("top_feature == names[int(np.argmax(forest[-1].feature_importances_))]", True,
                  "Blank 5: pick the name at the index of the largest importance.", "الفراغ 5: اختر الاسم عند فهرس أكبر أهمية."),
        ),
        hints=(
            ("`remainder=\"passthrough\"` keeps the numeric columns unchanged.", "يُبقي `remainder=\"passthrough\"` الأعمدة الرقمية دون تغيير."),
            ("OOB scoring only works when bootstrapping is on.", "لا يعمل تقييم OOB إلا عند تفعيل أخذ العينات المعادة."),
            ("`feature_importances_` lines up with `get_feature_names_out()`.", "تتوافق `feature_importances_` مع `get_feature_names_out()`."),
        ),
        success=("Correct! The OOB score gives a validation estimate without a separate split; Random Forest randomizes rows (bootstrap) and features, while Extra Trees also randomizes the split thresholds.",
                 "صحيح! يعطي تقييم OOB تقديرًا للتحقق دون تقسيم منفصل؛ ويعشّي Random Forest الصفوف (bootstrap) والخصائص، بينما يعشّي Extra Trees أيضًا عتبات التقسيم."),
    ),
    "COURSE-013.M11.L01.EX02": Guided(
        goal=("Compare sequential boosting (AdaBoost, Gradient Boosting with early stopping) with a soft-voting ensemble.",
              "قارن التعزيز المتتابع (AdaBoost، وGradient Boosting مع الإيقاف المبكر) بمجموعة تصويت ناعم."),
        steps=(
            ("Give AdaBoost a decision stump as its base learner.", "امنح AdaBoost جذع قرار (stump) متعلّمًا أساسيًا."),
            ("Stop Gradient Boosting after 5 rounds without improvement.", "أوقف Gradient Boosting بعد 5 جولات دون تحسن."),
            ("Average the models' probabilities in the voting ensemble.", "احسب متوسط احتمالات النماذج في مجموعة التصويت."),
            ("Read how many trees Gradient Boosting actually built.", "اقرأ عدد الأشجار التي بناها Gradient Boosting فعليًا."),
        ),
        starter='''from sklearn.datasets import make_classification
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=500, n_features=8, n_informative=5, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Step 1: many weak learners, each focusing on the previous ones' mistakes
ada = AdaBoostClassifier(estimator=___, n_estimators=50, random_state=42)
# Step 2: hold out 20% internally and stop when 5 rounds bring no improvement
gb = GradientBoostingClassifier(learning_rate=0.1, n_estimators=300, validation_fraction=0.2,
                                n_iter_no_change=___, random_state=42)
# Step 3: scale-sensitive models get a scaler; the forest does not need one
voting = VotingClassifier([
    ("lr", make_pipeline(StandardScaler(), LogisticRegression())),
    ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier())),
    ("rf", RandomForestClassifier(n_estimators=50, random_state=42)),
], voting=___)

scores = {name: round(model.fit(X_train, y_train).score(X_test, y_test), 3)
          for name, model in (("adaboost", ada), ("gradient boosting", gb), ("soft voting", voting))}
# Step 4: trees actually built before early stopping
gb_trees = ___
print(scores, "| GB trees used:", gb_trees, "of 300")
''',
        answers=("DecisionTreeClassifier(max_depth=1)", "5", '"soft"', "gb.n_estimators_"),
        checks=(
            check("ada.estimator.max_depth", 1, "Blank 1: a stump is `DecisionTreeClassifier(max_depth=1)`.", "الفراغ 1: الجذع هو `DecisionTreeClassifier(max_depth=1)`."),
            check("gb.n_iter_no_change == 5 and gb.n_estimators_ < 300", True, "Blank 2: `n_iter_no_change=5` turns on early stopping.",
                  "الفراغ 2: يفعّل `n_iter_no_change=5` الإيقاف المبكر."),
            check("voting.voting", "soft", "Blank 3: `voting=\"soft\"` averages predicted probabilities.", "الفراغ 3: يحسب `voting=\"soft\"` متوسط الاحتمالات المتوقعة."),
            check("gb_trees == gb.n_estimators_", True, "Blank 4: read `gb.n_estimators_` after fitting.", "الفراغ 4: اقرأ `gb.n_estimators_` بعد التدريب."),
        ),
        hints=(
            ("A stump is a tree with one split.", "الجذع شجرة بتقسيم واحد."),
            ("Early stopping needs both `validation_fraction` and `n_iter_no_change`.", "يحتاج الإيقاف المبكر إلى `validation_fraction` و`n_iter_no_change` معًا."),
            ("Hard voting counts labels; soft voting averages probabilities.", "يعدّ التصويت الصارم التسميات، ويحسب التصويت الناعم متوسط الاحتمالات."),
        ),
        success=("Correct! Boosting builds models in sequence and early stopping kept Gradient Boosting from using all 300 trees; voting combines independent models with a fixed rule.",
                 "صحيح! يبني التعزيز النماذج بالتتابع، ومنع الإيقاف المبكر Gradient Boosting من استخدام الأشجار الـ300 كلها؛ أما التصويت فيجمع نماذج مستقلة بقاعدة ثابتة."),
        reflect=("For a multiclass problem, when would you use one-vs-rest and when one-vs-one?",
                 "في مشكلة متعددة الفئات، متى ستستخدم one-vs-rest ومتى one-vs-one؟"),
    ),
    "COURSE-013.M11.L01.EX03": Guided(
        goal=("Stack three diverse models with out-of-fold predictions and compare the stack with the best single model.",
              "كدّس ثلاثة نماذج متنوعة بتنبؤات خارج الأجزاء (out-of-fold)، وقارن المكدّس بأفضل نموذج منفرد."),
        steps=(
            ("Pass the three diverse base models.", "مرّر النماذج الأساسية الثلاثة المتنوعة."),
            ("Build the meta-features with 5-fold cross-validation.", "ابنِ الخصائص الفوقية بتحقق متقاطع من 5 أجزاء."),
            ("Fit the stack on the training data only.", "درّب المكدّس على بيانات التدريب فقط."),
            ("Find the best single model's test score.", "جد نتيجة الاختبار لأفضل نموذج منفرد."),
        ),
        starter='''from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = make_classification(n_samples=500, n_features=10, n_informative=6, random_state=7)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

base_models = [
    ("lr", make_pipeline(StandardScaler(), LogisticRegression())),
    ("svc", make_pipeline(StandardScaler(), SVC())),
    ("rf", RandomForestClassifier(n_estimators=100, random_state=42)),
]
stack = StackingClassifier(
    estimators=___,                       # Step 1: the three diverse base models
    final_estimator=LogisticRegression(), # the meta-model
    cv=___,                               # Step 2: out-of-fold predictions
)
# Step 3: training data only
___
stack_score = stack.score(X_test, y_test)

single_scores = {name: model.fit(X_train, y_train).score(X_test, y_test) for name, model in base_models}
# Step 4: the best single model's score
best_single = ___
print(round(stack_score, 3), {k: round(v, 3) for k, v in single_scores.items()}, round(best_single, 3))
''',
        answers=("base_models", "5", "stack.fit(X_train, y_train)", "max(single_scores.values())"),
        checks=(
            check("[name for name, _ in stack.estimators] == ['lr', 'svc', 'rf'] and stack.cv == 5", True,
                  "Blanks 1-2: `estimators=base_models`, `cv=5`.", "الفراغان 1 و2: `estimators=base_models` و`cv=5`."),
            check("len(stack.estimators_) == 3 and abs(float(stack_score) - float(stack.score(X_test, y_test))) < 1e-12", True,
                  "Blank 3: `stack.fit(X_train, y_train)`.", "الفراغ 3: `stack.fit(X_train, y_train)`."),
            check("best_single == max(single_scores.values())", True, "Blank 4: `max(single_scores.values())`.", "الفراغ 4: `max(single_scores.values())`."),
        ),
        hints=(
            ("The list you built above already holds the (name, model) pairs; the meta-model learns how much to trust each.", "تحمل القائمة التي بنيتها أعلاه أزواج (الاسم، النموذج) بالفعل، ويتعلّم النموذج الفوقي مقدار الثقة بكلٍّ منها."),
            ("`cv=5` trains the meta-model on predictions each base model made for rows it did not see.", "يدرّب `cv=5` النموذج الفوقي على تنبؤات كل نموذج أساسي لصفوف لم يرها."),
            ("`max(dict.values())` is the best score.", "`max(dict.values())` هي أفضل نتيجة."),
        ),
        success=("Correct! Out-of-fold predictions keep the meta-model from learning from base-model predictions on rows they already memorized - the leakage that makes naive stacking look better than it is.",
                 "صحيح! تمنع التنبؤات خارج الأجزاء النموذجَ الفوقي من التعلّم من تنبؤات النماذج الأساسية على صفوف حفظتها مسبقًا - وهو التسريب الذي يجعل التكديس الساذج يبدو أفضل مما هو."),
    ),
    "COURSE-013.M11.L01.EX04": Guided(
        goal=("Configure XGBoost's regularization parameters and know what each one makes more conservative.",
              "اضبط معاملات التنظيم في XGBoost، واعرف ما يجعله كلٌّ منها أكثر تحفظًا."),
        steps=(
            ("Set the L2 penalty `reg_lambda` to 1.0.", "اضبط عقوبة L2 `reg_lambda` على 1.0."),
            ("Set the L1 penalty `reg_alpha` to 0.1.", "اضبط عقوبة L1 `reg_alpha` على 0.1."),
            ("Set `min_child_weight` to 5.", "اضبط `min_child_weight` على 5."),
            ("Set the split threshold `gamma` to 0.5.", "اضبط عتبة التقسيم `gamma` على 0.5."),
            ("Use log loss as the evaluation metric.", "استخدم log loss مقياسًا للتقييم."),
        ),
        starter='''from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=4,
    reg_lambda=___,          # Step 1: L2 penalty on leaf weights - higher shrinks them
    reg_alpha=___,           # Step 2: L1 penalty - can push leaf weights to exactly zero
    min_child_weight=___,    # Step 3: minimum hessian sum per leaf - higher blocks tiny leaves
    gamma=___,               # Step 4: minimum loss reduction required to make a split
    tree_method="hist",      # fast histogram-based split finding
    eval_metric=___,         # Step 5: the metric reported on validation data
)
model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
''',
        answers=("1.0", "0.1", "5", "0.5", '"logloss"'),
        alternatives={1: ("1",)},
        blanks=(
            ("set `reg_lambda=1.0`.", "اضبط `reg_lambda=1.0`."),
            ("set `reg_alpha=0.1`.", "اضبط `reg_alpha=0.1`."),
            ("set `min_child_weight=5`.", "اضبط `min_child_weight=5`."),
            ("set `gamma=0.5`.", "اضبط `gamma=0.5`."),
            ("use `\"logloss\"` for binary classification.", "استخدم `\"logloss\"` للتصنيف الثنائي."),
        ),
        hints=(
            ("lambda (L2) and alpha (L1) penalize large leaf weights.", "تعاقب lambda (L2) وalpha (L1) أوزان الأوراق الكبيرة."),
            ("min_child_weight and gamma make splits harder to justify.", "يجعل min_child_weight وgamma تبرير التقسيم أصعب."),
            ("Log loss is the standard metric for binary probabilities.", "يُعدّ log loss المقياس المعتاد للاحتمالات الثنائية."),
        ),
        success=("Correct! Raising any of the four regularization parameters makes the trees more conservative, which is how XGBoost fights overfitting.",
                 "صحيح! رفع أي من معاملات التنظيم الأربعة يجعل الأشجار أكثر تحفظًا، وهكذا يحارب XGBoost فرط التخصيص."),
        expected=READ_NOTE,
        reflect=("Fill a table: for each of reg_lambda, reg_alpha, min_child_weight, gamma, tree_method and eval_metric, what does it control and which overfitting behaviour does it target?",
                 "املأ جدولًا: لكلٍّ من reg_lambda وreg_alpha وmin_child_weight وgamma وtree_method وeval_metric، ماذا يتحكم فيه؟ وأي سلوك لفرط التخصيص يستهدفه؟"),
    ),
    "COURSE-013.M12.L01.EX02": Guided(
        goal=("Complete a Keras churn MLP and a CIFAR-10 CNN, matching each output layer to its loss.",
              "أكمل شبكة MLP لانسحاب العملاء وشبكة CNN لـ CIFAR-10 في Keras، مع مطابقة كل طبقة إخراج مع دالة خسارتها."),
        steps=(
            ("End the MLP with one sigmoid unit.", "أنهِ شبكة MLP بوحدة sigmoid واحدة."),
            ("Use binary cross-entropy for the MLP.", "استخدم binary cross-entropy لشبكة MLP."),
            ("Add batch normalization after the convolution.", "أضف التطبيع بالدفعات بعد الالتفاف."),
            ("End the CNN with a 10-way softmax.", "أنهِ شبكة CNN بطبقة softmax من 10 فئات."),
            ("Use categorical cross-entropy for the CNN.", "استخدم categorical cross-entropy لشبكة CNN."),
        ),
        starter='''from tensorflow import keras

n_features = 12
mlp = keras.Sequential([
    keras.layers.Input(shape=(n_features,)),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(16, activation="relu"),
    ___,                                                     # Step 1: P(churn)
])
mlp.compile(optimizer="adam", loss=___, metrics=["accuracy"])   # Step 2

cnn = keras.Sequential([
    keras.layers.Input(shape=(32, 32, 3)),
    keras.layers.Conv2D(32, 3, padding="same", activation="relu"),
    ___,                                                     # Step 3: stabilise activations
    keras.layers.MaxPooling2D(),
    keras.layers.Dropout(0.25),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation="relu"),
    ___,                                                     # Step 4: one probability per class
])
cnn.compile(optimizer="adam", loss=___, metrics=["accuracy"])   # Step 5: one-hot labels
''',
        answers=('keras.layers.Dense(1, activation="sigmoid")', '"binary_crossentropy"', "keras.layers.BatchNormalization()",
                 'keras.layers.Dense(10, activation="softmax")', '"categorical_crossentropy"'),
        alternatives={5: ('"sparse_categorical_crossentropy"',)},
        blanks=(
            ("`keras.layers.Dense(1, activation=\"sigmoid\")`.", "`keras.layers.Dense(1, activation=\"sigmoid\")`."),
            ("`\"binary_crossentropy\"`.", "`\"binary_crossentropy\"`."),
            ("`keras.layers.BatchNormalization()`.", "`keras.layers.BatchNormalization()`."),
            ("`keras.layers.Dense(10, activation=\"softmax\")`.", "`keras.layers.Dense(10, activation=\"softmax\")`."),
            ("`\"categorical_crossentropy\"` for one-hot labels.", "`\"categorical_crossentropy\"` للتسميات بصيغة One-hot."),
        ),
        hints=(
            ("Binary output: 1 unit + sigmoid. Multiclass output: one unit per class + softmax.", "الإخراج الثنائي: وحدة واحدة + sigmoid. الإخراج متعدد الفئات: وحدة لكل فئة + softmax."),
            ("The loss must match the output layer.", "يجب أن تطابق دالة الخسارة طبقة الإخراج."),
            ("BatchNormalization usually follows a convolution.", "يأتي BatchNormalization عادةً بعد الالتفاف."),
        ),
        success=("Correct! A sigmoid + binary cross-entropy predicts one probability; softmax + categorical cross-entropy spreads probability across 10 classes. Dropout and batch normalization regularize and stabilize training.",
                 "صحيح! يتنبأ sigmoid مع binary cross-entropy باحتمال واحد، بينما يوزّع softmax مع categorical cross-entropy الاحتمال على 10 فئات. ويعمل Dropout والتطبيع بالدفعات على التنظيم وتثبيت التدريب."),
        expected=READ_NOTE,
    ),
    "COURSE-013.M12.L01.EX03": Guided(
        goal=("Prepare a time series for SimpleRNN/LSTM models without leaking the future: chronological split, train-only scaling and 100-step windows.",
              "جهّز سلسلة زمنية لنماذج SimpleRNN/LSTM دون تسريب المستقبل: تقسيم زمني، وتحجيم على بيانات التدريب فقط، ونوافذ من 100 خطوة."),
        steps=(
            ("Split 80/20 in time order.", "قسّم 80/20 بالترتيب الزمني."),
            ("Fit the scaler on training values only.", "درّب أداة التحجيم على قيم التدريب فقط."),
            ("Use the value right after each window as its target.", "استخدم القيمة التي تلي كل نافذة مباشرة هدفًا لها."),
            ("Reshape to (samples, timesteps, features).", "أعد التشكيل إلى (samples, timesteps, features)."),
            ("Compute RMSE in the original units.", "احسب RMSE بالوحدات الأصلية."),
        ),
        starter='''import numpy as np
from sklearn.preprocessing import MinMaxScaler

rng = np.random.default_rng(0)
series = np.sin(np.arange(600) * 0.05) * 50 + 100 + rng.normal(0, 2, 600)

# Step 1: the first 80% for training, the last 20% for testing - never shuffle time
split = int(len(series) * 0.8)
train, test = ___
# Step 2: learn min/max from the training values only
scaler = MinMaxScaler().fit(___)
train_scaled = scaler.transform(train.reshape(-1, 1)).ravel()
test_scaled = scaler.transform(test.reshape(-1, 1)).ravel()

def make_windows(values, window=100):
    X = np.array([values[i:i + window] for i in range(len(values) - window)])
    # Step 3: the target is the value right after each window
    y = ___
    return X, y

X_train, y_train = make_windows(train_scaled)
# Step 4: recurrent layers expect (samples, timesteps, features)
X_train = ___

# Step 5: errors must be reported in the original units, not the 0-1 scale
def rmse_original_units(pred_scaled, true_scaled):
    return ___

print(train.shape, test.shape, X_train.shape, y_train.shape)
''',
        answers=(
            "series[:split], series[split:]",
            "train.reshape(-1, 1)",
            "np.array([values[i + window] for i in range(len(values) - window)])",
            "X_train.reshape(X_train.shape[0], X_train.shape[1], 1)",
            "float(np.sqrt(np.mean((scaler.inverse_transform(pred_scaled.reshape(-1, 1)) - scaler.inverse_transform(true_scaled.reshape(-1, 1))) ** 2)))",
        ),
        checks=(
            check("[len(train), len(test), float(train[-1]) == float(series[479]), float(test[0]) == float(series[480])]", [480, 120, True, True],
                  "Blank 1: `series[:split], series[split:]`.", "الفراغ 1: `series[:split], series[split:]`."),
            check("abs(float(scaler.data_max_[0]) - float(train.max())) < 1e-12", True,
                  "Blank 2: fit on `train.reshape(-1, 1)` - fitting on the full series leaks test information.",
                  "الفراغ 2: درّب على `train.reshape(-1, 1)` - فالتدريب على السلسلة كاملة يسرّب معلومات الاختبار."),
            check("float(y_train[0]) == float(train_scaled[100]) and len(y_train) == 380", True,
                  "Blank 3: `values[i + window]` follows the window `values[i:i + window]`.", "الفراغ 3: يلي `values[i + window]` النافذة `values[i:i + window]`."),
            check("list(X_train.shape)", [380, 100, 1], "Blank 4: add a feature axis of size 1.", "الفراغ 4: أضف محور خصائص بحجم 1."),
            check("round(rmse_original_units(np.array([0.5, 0.5]), np.array([0.5, 0.6])), 6) == round(float(np.sqrt(np.mean([0, (0.1 * (scaler.data_max_[0] - scaler.data_min_[0])) ** 2]))), 6)", True,
                  "Blank 5: inverse-transform both arrays before computing the RMSE.", "الفراغ 5: اعكس تحويل المصفوفتين قبل حساب RMSE."),
        ),
        hints=(
            ("Slicing at `split` keeps time order.", "يحافظ التقطيع عند `split` على الترتيب الزمني."),
            ("Scalers need 2-D input: `.reshape(-1, 1)`.", "تحتاج أدوات التحجيم إلى مدخل ثنائي الأبعاد: `.reshape(-1, 1)`."),
            ("`scaler.inverse_transform` returns values to the original units.", "يعيد `scaler.inverse_transform` القيم إلى وحداتها الأصلية."),
        ),
        success=("Correct! The data are ready for `SimpleRNN`/`LSTM` layers: 380 windows of 100 steps × 1 feature, scaled with training statistics only.",
                 "صحيح! أصبحت البيانات جاهزة لطبقات `SimpleRNN`/`LSTM`: 380 نافذة من 100 خطوة × خاصية واحدة، محجّمة بإحصاءات التدريب فقط."),
        reflect=("Why does passing the final test set as `validation_data` weaken the purity of the holdout?",
                 "لماذا يُضعف تمرير مجموعة الاختبار النهائية بوصفها `validation_data` نقاءَ البيانات المحجوزة؟"),
    ),
    "COURSE-013.M12.L01.EX04": Guided(
        goal=("Build a convolutional autoencoder, train it to reconstruct images, then to denoise them.",
              "ابنِ مُرمِّزًا تلقائيًا التفافيًا، ودرّبه على إعادة بناء الصور، ثم على إزالة ضجيجها."),
        steps=(
            ("Scale pixels to 0-1.", "حجّم البكسلات إلى 0-1."),
            ("Downsample in the encoder.", "صغّر الأبعاد في المُرمِّز."),
            ("Upsample in the decoder.", "كبّر الأبعاد في فاكّ الترميز."),
            ("Add Gaussian noise and clip to 0-1.", "أضف ضجيجًا غاوسيًا واقصص إلى 0-1."),
            ("Train noisy → clean.", "درّب من المشوّش إلى النظيف."),
        ),
        starter='''import numpy as np
from tensorflow import keras

(x_train, _), _ = keras.datasets.mnist.load_data()
# Step 1: 0-255 integers -> 0-1 floats, with a channel axis
x_train = (x_train.astype("float32") / ___)[..., np.newaxis]

encoder = keras.Sequential([
    keras.layers.Input(shape=(28, 28, 1)),
    keras.layers.Conv2D(32, 3, activation="relu", padding="same"),
    ___,                                                                # Step 2: 28 -> 14
    keras.layers.Conv2D(16, 3, activation="relu", padding="same"),
    keras.layers.MaxPooling2D(2, padding="same"),                       # 14 -> 7
])
decoder = keras.Sequential([
    keras.layers.Conv2D(16, 3, activation="relu", padding="same"),
    ___,                                                                # Step 3: 7 -> 14
    keras.layers.Conv2D(32, 3, activation="relu", padding="same"),
    keras.layers.UpSampling2D(2),                                       # 14 -> 28
    keras.layers.Conv2D(1, 3, activation="sigmoid", padding="same"),
])
autoencoder = keras.Sequential([encoder, decoder])
autoencoder.compile(optimizer="adam", loss="binary_crossentropy")
autoencoder.fit(x_train, x_train, epochs=5, batch_size=128)             # clean -> clean

# Step 4: noisy inputs that stay valid pixel values
x_noisy = ___
# Step 5: denoising: noisy in, clean out
autoencoder.fit(___, x_train, epochs=5, batch_size=128)
''',
        answers=("255.0", "keras.layers.MaxPooling2D(2, padding=\"same\")", "keras.layers.UpSampling2D(2)",
                 "np.clip(x_train + 0.3 * np.random.normal(size=x_train.shape), 0.0, 1.0)", "x_noisy"),
        alternatives={1: ("255",), 2: ("keras.layers.MaxPooling2D(2)", "keras.layers.MaxPooling2D()")},
        blanks=(
            ("divide by `255.0`.", "اقسم على `255.0`."),
            ("`keras.layers.MaxPooling2D(2, padding=\"same\")`.", "`keras.layers.MaxPooling2D(2, padding=\"same\")`."),
            ("`keras.layers.UpSampling2D(2)`.", "`keras.layers.UpSampling2D(2)`."),
            ("`np.clip(x_train + 0.3 * np.random.normal(size=x_train.shape), 0.0, 1.0)`.", "`np.clip(x_train + 0.3 * np.random.normal(size=x_train.shape), 0.0, 1.0)`."),
            ("the input is `x_noisy`; the target stays `x_train`.", "المدخل `x_noisy` ويبقى الهدف `x_train`."),
        ),
        hints=(
            ("Pooling halves height and width; upsampling doubles them.", "يقسم التجميع الارتفاع والعرض على اثنين، ويضاعفهما التكبير."),
            ("`np.clip(values, 0.0, 1.0)` keeps pixels in range after adding noise.", "يُبقي `np.clip(values, 0.0, 1.0)` البكسلات ضمن النطاق بعد إضافة الضجيج."),
            ("For denoising, only the input changes - the target is still the clean image.", "في إزالة الضجيج يتغير المدخل فقط - ويبقى الهدف الصورة النظيفة."),
        ),
        success=("Correct! The bottleneck forces the network to keep only essential structure, which is why reconstructions look smoother than the originals - and why the same model can learn to drop noise.",
                 "صحيح! يُجبر عنق الزجاجة الشبكة على الاحتفاظ بالبنية الأساسية فقط، ولهذا تبدو الصور المعاد بناؤها أنعم من الأصلية - ولهذا يستطيع النموذج نفسه تعلّم إسقاط الضجيج."),
        expected=READ_NOTE,
    ),
    "COURSE-013.M13.L01.EX01": Guided(
        goal=("Clean review text and remove stopwords without throwing away the negations that carry sentiment.",
              "نظّف نصوص المراجعات واحذف كلمات التوقف دون التخلص من أدوات النفي التي تحمل المشاعر."),
        steps=(
            ("Remove URLs.", "احذف الروابط."),
            ("Lowercase and collapse whitespace.", "حوّل إلى أحرف صغيرة ووحّد المسافات."),
            ("Tokenize into words.", "قسّم إلى كلمات."),
            ("Drop stopwords but keep not, no and never.", "احذف كلمات التوقف مع الاحتفاظ بـ not وno وnever."),
        ),
        starter='''import re

reviews = [
    "Loved it!!! Not bad at all https://shop.example.com/p/1",
    "I would NEVER buy this again.",
    "  The   battery   is   great ",
    "No issues, works as described.",
    "Terrible support... see http://help.example.com",
]
# A typical English stopword list - it includes the negations, as NLTK's does
STOPWORDS = {"i", "it", "the", "is", "this", "as", "at", "all", "a", "an", "and", "would", "see",
             "again", "buy", "not", "no", "never"}
KEEP = {"not", "no", "never"}                 # they flip sentiment, so they stay

def clean(text):
    # Step 1: drop links
    text = ___
    # Step 2: one space between words, lowercase
    return ___

# Step 3: words = runs of letters
def tokenize(text):
    return ___

# Step 4: remove stopwords, except the negations
def remove_stopwords(tokens):
    return ___

processed = [remove_stopwords(tokenize(clean(review))) for review in reviews]
for tokens in processed:
    print(tokens)
''',
        answers=(r're.sub(r"https?://\S+", "", text)', r're.sub(r"\s+", " ", text).strip().lower()', r're.findall(r"[a-z]+", text)',
                 "[token for token in tokens if token not in STOPWORDS or token in KEEP]"),
        checks=(
            check("[clean(reviews[0]), clean(reviews[2])]", ["loved it!!! not bad at all", "the battery is great"],
                  "Blanks 1-2: remove `https?://\\S+`, then collapse spaces, strip and lowercase.",
                  "الفراغان 1 و2: احذف `https?://\\S+`، ثم وحّد المسافات وأزل الأطراف وحوّل إلى أحرف صغيرة."),
            check("tokenize('works as described.')", ["works", "as", "described"],
                  "Blank 3: `re.findall(r\"[a-z]+\", text)`.", "الفراغ 3: `re.findall(r\"[a-z]+\", text)`."),
            check("processed", [["loved", "not", "bad"], ["never"], ["battery", "great"], ["no", "issues", "works", "described"], ["terrible", "support"]],
                  "Blank 4: keep a token if it is not a stopword OR it is one of the negations.", "الفراغ 4: احتفظ بالرمز إن لم يكن كلمة توقف أو كان من أدوات النفي."),
        ),
        hints=(
            ("`\\S+` matches everything up to the next space.", "يطابق `\\S+` كل شيء حتى المسافة التالية."),
            ("`re.sub(r\"\\s+\", \" \", text)` collapses runs of whitespace.", "يوحّد `re.sub(r\"\\s+\", \" \", text)` سلاسل المسافات."),
            ("Removing 'not' would turn 'not bad' into 'bad'.", "حذف 'not' سيحوّل 'not bad' إلى 'bad'."),
        ),
        success=("Correct! 'not bad' and 'never' survive cleaning, so the sentiment of each review is still in the tokens.",
                 "صحيح! نجت 'not bad' و'never' من التنظيف، فبقيت مشاعر كل مراجعة داخل الرموز."),
        reflect=("With NLTK installed locally, compare Porter stems with WordNet lemmas (with and without POS tags). Which loses more meaning?",
                 "مع تثبيت NLTK محليًا، قارن جذوع Porter بلِمّات WordNet (مع وسوم أقسام الكلام ودونها). أيهما يخسر معنى أكثر؟"),
    ),
    "COURSE-013.M13.L01.EX02": Guided(
        goal=("Compare sparse text representations: unigram counts, filtered n-grams and TF-IDF - and see what they cannot capture.",
              "قارن تمثيلات النص المتناثرة: عدّ الكلمات المفردة، والـ n-grams المرشَّحة، وTF-IDF - وتعرّف على ما لا تستطيع التقاطه."),
        steps=(
            ("Build unigram + bigram counts kept in ≥ 2 documents and ≤ 90% of them.", "ابنِ عدّ المفردات والثنائيات التي تظهر في مستندين على الأقل وفي 90% منها على الأكثر."),
            ("Build TF-IDF features.", "ابنِ خصائص TF-IDF."),
            ("Compute the sparsity of the TF-IDF matrix.", "احسب تناثر مصفوفة TF-IDF."),
            ("Check whether unigram counts keep word order.", "تحقّق هل يحافظ عدّ المفردات على ترتيب الكلمات."),
        ),
        starter='''from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

corpus = [
    "the battery life is great",
    "battery life is not great",
    "great screen and great battery",
    "the screen is not bright",
    "not worth the price",
    "great price for the battery",
]
unigram = CountVectorizer().fit(corpus)

# Step 1: unigrams + bigrams; drop terms in fewer than 2 documents or in more than 90% of them
ngrams = ___
# Step 2: TF-IDF weights
tfidf = ___
# Step 3: share of zero entries in the TF-IDF matrix
sparsity = ___
# Step 4: do "not good" and "good not" get different unigram vectors?
order_kept = ___

print(len(unigram.vocabulary_), "unigrams |", len(ngrams.vocabulary_), "kept n-grams:", sorted(ngrams.vocabulary_))
print("sparsity", round(sparsity, 3), "| word order kept:", order_kept)
''',
        answers=(
            "CountVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.9).fit(corpus)",
            "TfidfVectorizer().fit_transform(corpus)",
            "1 - tfidf.nnz / (tfidf.shape[0] * tfidf.shape[1])",
            '(unigram.transform(["not good"]) != unigram.transform(["good not"])).nnz > 0',
        ),
        checks=(
            check("'battery life' in ngrams.vocabulary_ and 'and' not in ngrams.vocabulary_ and ngrams.ngram_range == (1, 2)", True,
                  "Blank 1: `CountVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.9).fit(corpus)`.", "الفراغ 1: `CountVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.9).fit(corpus)`."),
            check("list(tfidf.shape) == [6, len(unigram.vocabulary_)]", True, "Blank 2: `TfidfVectorizer().fit_transform(corpus)`.",
                  "الفراغ 2: `TfidfVectorizer().fit_transform(corpus)`."),
            check("abs(float(sparsity) - (1 - tfidf.nnz / (tfidf.shape[0] * tfidf.shape[1]))) < 1e-12 and float(sparsity) > 0.5", True,
                  "Blank 3: 1 - non-zero entries / all entries.", "الفراغ 3: 1 - العناصر غير الصفرية / كل العناصر."),
            check("order_kept", False, "Blank 4: compare the two transformed vectors; with unigrams they are identical.",
                  "الفراغ 4: قارن المتجهين المحوّلين؛ فهما متطابقان مع المفردات."),
        ),
        hints=(
            ("`min_df` and `max_df` remove rare and overly common terms.", "يحذف `min_df` و`max_df` المصطلحات النادرة والشائعة جدًا."),
            ("Sparse matrices expose `.nnz`, the number of stored non-zeros.", "تكشف المصفوفات المتناثرة عن `.nnz`، عدد القيم غير الصفرية المخزّنة."),
            ("A bag of words counts words; it forgets their order.", "تعدّ حقيبة الكلمات الكلمات وتنسى ترتيبها."),
        ),
        success=("Correct! The matrices are mostly zeros, and unigram counts cannot tell 'not good' from 'good not' - bigrams recover a little order, and dense embeddings add meaning and context.",
                 "صحيح! المصفوفات في معظمها أصفار، ولا يميّز عدّ المفردات بين 'not good' و'good not' - وتستعيد الثنائيات قليلًا من الترتيب، وتضيف التضمينات الكثيفة المعنى والسياق."),
        reflect=("Compare these with averaged Word2Vec vectors and DistilBERT token embeddings for an ambiguous word in two contexts.",
                 "قارن هذه التمثيلات بمتوسط متجهات Word2Vec وبتضمينات رموز DistilBERT لكلمة غامضة في سياقين."),
    ),
    "COURSE-013.M13.L01.EX03": Guided(
        goal=("Build a leakage-aware TF-IDF + Naive Bayes sentiment baseline with stratified cross-validation and inspect its top terms.",
              "ابنِ خط أساس للمشاعر من TF-IDF وNaive Bayes يتجنب التسريب، مع تحقق متقاطع طبقي، وافحص أهم مصطلحاته."),
        steps=(
            ("Vectorize unigrams and bigrams inside the pipeline.", "حوّل المفردات والثنائيات إلى متجهات داخل الـ Pipeline."),
            ("Cross-validate on the training data only.", "نفّذ التحقق المتقاطع على بيانات التدريب فقط."),
            ("Fit on the full training set.", "درّب على مجموعة التدريب كاملة."),
            ("Rank the most indicative positive terms.", "رتّب أكثر المصطلحات دلالةً على الإيجابية."),
        ),
        starter='''import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

positive = ["great battery life", "love the bright screen", "works perfectly, great value", "excellent sound quality",
            "fast delivery and great service", "very happy with this phone", "the camera is excellent",
            "great price and fast shipping", "screen is sharp and bright", "really love it", "perfect for travel", "excellent build quality"]
negative = ["battery died after a week", "screen cracked on day one", "terrible customer service", "very poor sound quality",
            "slow delivery and broken box", "not happy with this phone", "the camera is blurry", "waste of money",
            "stopped working quickly", "really disappointed", "poor build quality", "terrible value"]
texts, labels = positive + negative, ["positive"] * 12 + ["negative"] * 12

def clean(text):
    return re.sub(r"[^a-z\\s]", " ", text.lower())

X_train, X_test, y_train, y_test = train_test_split([clean(t) for t in texts], labels, test_size=0.2,
                                                    stratify=labels, random_state=42)
pipeline = Pipeline([
    ("tfidf", ___),                       # Step 1: unigrams + bigrams
    ("nb", MultinomialNB()),
])
# Step 2: 5-fold stratified CV on the TRAINING data only
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = ___
# Step 3: final fit on all training data
___
test_f1 = f1_score(y_test, pipeline.predict(X_test), pos_label="positive")

nb, vocabulary = pipeline.named_steps["nb"], pipeline.named_steps["tfidf"].get_feature_names_out()
positive_row = list(nb.classes_).index("positive")
# Step 4: the 10 terms with the highest log-probability for the positive class
top_positive = ___
print(cv_scores.round(2), round(test_f1, 3))
print(top_positive)
''',
        answers=(
            "TfidfVectorizer(ngram_range=(1, 2))",
            "cross_val_score(pipeline, X_train, y_train, cv=cv)",
            "pipeline.fit(X_train, y_train)",
            "vocabulary[np.argsort(nb.feature_log_prob_[positive_row])[::-1][:10]].tolist()",
        ),
        checks=(
            check("pipeline.named_steps['tfidf'].ngram_range == (1, 2)", True, "Blank 1: `TfidfVectorizer(ngram_range=(1, 2))`.",
                  "الفراغ 1: `TfidfVectorizer(ngram_range=(1, 2))`."),
            check("len(cv_scores) == 5 and bool(np.allclose(cv_scores, cross_val_score(Pipeline([('tfidf', TfidfVectorizer(ngram_range=(1, 2))), ('nb', MultinomialNB())]), X_train, y_train, cv=cv)))", True,
                  "Blank 2: `cross_val_score(pipeline, X_train, y_train, cv=cv)` - never on the test set.", "الفراغ 2: `cross_val_score(pipeline, X_train, y_train, cv=cv)` - وليس على مجموعة الاختبار أبدًا."),
            check("hasattr(nb, 'feature_log_prob_') and len(vocabulary) == len(TfidfVectorizer(ngram_range=(1, 2)).fit(X_train).vocabulary_)", True,
                  "Blank 3: `pipeline.fit(X_train, y_train)`.", "الفراغ 3: `pipeline.fit(X_train, y_train)`."),
            check("top_positive == vocabulary[np.argsort(nb.feature_log_prob_[positive_row])[::-1][:10]].tolist() and len(top_positive) == 10", True,
                  "Blank 4: sort the positive row of `feature_log_prob_` from high to low and take 10 terms.", "الفراغ 4: رتّب الصف الإيجابي في `feature_log_prob_` تنازليًا وخذ 10 مصطلحات."),
        ),
        hints=(
            ("The vectorizer lives inside the pipeline so CV refits it in every fold.", "تعيش أداة التحويل داخل الـ Pipeline، فيعيد التحقق المتقاطع تدريبها في كل جزء."),
            ("`cross_val_score(model, X, y, cv=...)` returns one score per fold.", "تعيد `cross_val_score(model, X, y, cv=...)` نتيجة لكل جزء."),
            ("`feature_log_prob_` has one row per class, one column per term.", "لـ `feature_log_prob_` صف لكل فئة وعمود لكل مصطلح."),
        ),
        success=("Correct! A cheap, transparent baseline: every decision can be traced to term weights like 'great' and 'excellent'.",
                 "صحيح! خط أساس رخيص وشفاف: يمكن تتبّع كل قرار إلى أوزان مصطلحات مثل 'great' و'excellent'."),
        reflect=("Find one test error and explain which terms pushed the model the wrong way.", "جد خطأً واحدًا في الاختبار، واشرح أي المصطلحات دفعت النموذج في الاتجاه الخاطئ."),
    ),
    "COURSE-013.M13.L01.EX04": Guided(
        goal=("Prepare a fair DistilBERT fine-tuning run: tokenization, model, training arguments and a separate validation split.",
              "جهّز تشغيل ضبط دقيق عادل لـ DistilBERT: التقسيم إلى رموز، والنموذج، ومعاملات التدريب، وقسم تحقق منفصل."),
        steps=(
            ("Load the matching tokenizer.", "حمّل المُقسِّم المطابق."),
            ("Truncate long reviews.", "اقطع المراجعات الطويلة."),
            ("Cap sequences at 128 tokens.", "حدّد التسلسلات بـ 128 رمزًا."),
            ("Load the classification model with 2 labels.", "حمّل نموذج التصنيف بتسميتين."),
            ("Evaluate during training on the validation split, not the test split.", "قيّم أثناء التدريب على قسم التحقق لا قسم الاختبار."),
        ),
        starter='''from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments

checkpoint = "distilbert-base-uncased"
tokenizer = ___                                                   # Step 1

def tokenize(batch):
    return tokenizer(batch["text"], truncation=___, padding="max_length", max_length=___)   # Steps 2-3

train_ds = train_ds.map(tokenize, batched=True)
validation_ds = validation_ds.map(tokenize, batched=True)
test_ds = test_ds.map(tokenize, batched=True)           # used ONCE, after training

model = ___                                                       # Step 4
args = TrainingArguments(output_dir="distilbert-sentiment", per_device_train_batch_size=8,
                         learning_rate=2e-5, weight_decay=0.01, num_train_epochs=2, eval_strategy="epoch")
# Step 5: model selection uses the validation split
trainer = Trainer(model=model, args=args, train_dataset=train_ds, eval_dataset=___)
trainer.train()
print(trainer.evaluate(test_ds))                        # the final, untouched test evaluation
''',
        answers=("AutoTokenizer.from_pretrained(checkpoint)", "True", "128",
                 "AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)", "validation_ds"),
        blanks=(
            ("`AutoTokenizer.from_pretrained(checkpoint)`.", "`AutoTokenizer.from_pretrained(checkpoint)`."),
            ("`truncation=True`.", "`truncation=True`."),
            ("`max_length=128`.", "`max_length=128`."),
            ("`AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)`.", "`AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)`."),
            ("pass `validation_ds`.", "مرّر `validation_ds`."),
        ),
        hints=(
            ("Tokenizer and model must come from the same checkpoint.", "يجب أن يأتي المُقسِّم والنموذج من نقطة الحفظ نفسها."),
            ("Truncation and max_length together bound the sequence length.", "يحدّ القطع وmax_length معًا طول التسلسل."),
            ("Evaluating on the test set during training turns it into a validation set.", "التقييم على مجموعة الاختبار أثناء التدريب يحوّلها إلى مجموعة تحقق."),
        ),
        success=("Correct! The test split is used once, after training, so its score is an honest estimate - unlike reusing one split for both model selection and reporting.",
                 "صحيح! تُستخدم مجموعة الاختبار مرة واحدة بعد التدريب، فتكون نتيجتها تقديرًا أمينًا - بخلاف إعادة استخدام قسم واحد لاختيار النموذج وللإبلاغ معًا."),
        expected=READ_NOTE,
        reflect=("Compare this with the TF-IDF baseline on compute cost, interpretability and sensitivity to context.",
                 "قارن هذا بخط أساس TF-IDF من حيث تكلفة الحوسبة وقابلية التفسير والحساسية للسياق."),
    ),
    "COURSE-013.M14.L01.EX01": Guided(
        goal=("Prepare an image the way a vision model needs it: channel order, value range, square resizing strategies and denoising.",
              "جهّز صورة كما يحتاجها نموذج رؤية: ترتيب القنوات، ونطاق القيم، واستراتيجيات تحويلها إلى مربع، وإزالة الضجيج."),
        steps=(
            ("Convert BGR to RGB.", "حوّل BGR إلى RGB."),
            ("Convert to float32 in [0, 1].", "حوّل إلى float32 في [0, 1]."),
            ("Center-crop to a square.", "اقصص من المركز إلى مربع."),
            ("Letterbox: pad the short side to a square.", "الإطار (Letterbox): احشُ الضلع الأقصر لتصبح مربعًا."),
            ("Apply a 3×3 median filter.", "طبّق مرشح الوسيط 3×3."),
        ),
        starter='''import numpy as np

rng = np.random.default_rng(0)
h, w = 120, 200
# What cv2.imread returns: height x width x BGR, uint8. A blue-to-red gradient with a green square.
image_bgr = np.zeros((h, w, 3), dtype=np.uint8)
image_bgr[:, :, 0] = np.linspace(255, 0, w).astype(np.uint8)    # blue channel
image_bgr[:, :, 2] = np.linspace(0, 255, w).astype(np.uint8)    # red channel
image_bgr[40:80, 80:120, 1] = 255                               # green square

# Step 1: OpenCV stores BGR; most libraries expect RGB
image_rgb = ___
# Step 2: float32 values in [0, 1]
image = ___
# Step 3: the central square (keeps scale, loses the edges)
side = min(h, w)
top, left = (h - side) // 2, (w - side) // 2
center_crop = ___
# Step 4: letterbox (keeps everything, adds black bars above and below)
pad_total = w - h
letterbox = ___

# Salt-and-pepper noise on the green channel, then a 3x3 median filter
noisy = image[:, :, 1].copy()
noise = rng.random(noisy.shape)
noisy[noise < 0.05], noisy[noise > 0.95] = 0.0, 1.0

def median3(x):
    padded = np.pad(x, 1, mode="edge")
    neighbours = np.stack([padded[i:i + x.shape[0], j:j + x.shape[1]] for i in range(3) for j in range(3)])
    # Step 5: the middle value of every 3x3 neighbourhood
    return ___

denoised = median3(noisy)
print(image.dtype, center_crop.shape, letterbox.shape)
print("wrong pixels before:", int((noisy != image[:, :, 1]).sum()), "after:", int((np.abs(denoised - image[:, :, 1]) > 0.5).sum()))
''',
        answers=(
            "image_bgr[:, :, ::-1]",
            "image_rgb.astype(np.float32) / 255.0",
            "image[top:top + side, left:left + side]",
            "np.pad(image, ((pad_total // 2, pad_total - pad_total // 2), (0, 0), (0, 0)))",
            "np.median(neighbours, axis=0)",
        ),
        checks=(
            check("int(image_rgb[0, 0, 2]) == 255 and int(image_rgb[0, -1, 0]) == 255", True,
                  "Blank 1: reverse the channel axis: `image_bgr[:, :, ::-1]`.", "الفراغ 1: اعكس محور القنوات: `image_bgr[:, :, ::-1]`."),
            check("str(image.dtype) == 'float32' and float(image.max()) == 1.0 and float(image.min()) == 0.0", True,
                  "Blank 2: `.astype(np.float32) / 255.0`.", "الفراغ 2: `.astype(np.float32) / 255.0`."),
            check("list(center_crop.shape) == [120, 120, 3] and bool(np.array_equal(center_crop, image[:, 40:160]))", True,
                  "Blank 3: slice `top:top + side` rows and `left:left + side` columns.", "الفراغ 3: اقطع الصفوف `top:top + side` والأعمدة `left:left + side`."),
            check("list(letterbox.shape) == [200, 200, 3] and float(letterbox[0].max()) == 0.0 and bool(np.array_equal(letterbox[40:160], image))", True,
                  "Blank 4: pad 40 rows above and 40 below with zeros, nothing on the sides.", "الفراغ 4: احشُ 40 صفًا في الأعلى و40 في الأسفل بأصفار، ولا شيء على الجانبين."),
            check("int((np.abs(denoised - image[:, :, 1]) > 0.5).sum()) < int((noisy != image[:, :, 1]).sum()) // 5", True,
                  "Blank 5: `np.median(neighbours, axis=0)`.", "الفراغ 5: `np.median(neighbours, axis=0)`."),
        ),
        hints=(
            ("`[..., ::-1]` reverses the last axis.", "يعكس `[..., ::-1]` المحور الأخير."),
            ("A crop is just slicing; a letterbox is `np.pad` with zeros.", "القص مجرد تقطيع، والإطار هو `np.pad` بأصفار."),
            ("A median ignores a few extreme values, which is why it removes salt-and-pepper noise.", "يتجاهل الوسيط بضع قيم متطرفة، ولهذا يزيل ضجيج الملح والفلفل."),
        ),
        success=("Correct! Cropping keeps detail but loses the sides, letterboxing keeps everything but adds bars, and the median filter removes almost all impulse noise without blurring the square's edges.",
                 "صحيح! يحافظ القص على التفاصيل لكنه يفقد الجوانب، ويحافظ الإطار على كل شيء لكنه يضيف أشرطة، ويزيل مرشح الوسيط معظم الضجيج النبضي دون تمويه حواف المربع."),
        expected=(
            "OpenCV is not installed in the sandbox, so these steps use NumPy; `cv2.cvtColor`, `cv2.resize` and `cv2.medianBlur` perform the same operations.",
            "مكتبة OpenCV غير مثبّتة في بيئة التدريب، لذلك تستخدم هذه الخطوات NumPy؛ وتنفّذ `cv2.cvtColor` و`cv2.resize` و`cv2.medianBlur` العمليات نفسها.",
        ),
    ),
    "COURSE-013.M14.L01.EX02": Guided(
        goal=("Measure an image: adjust contrast with clipping, find edges, and compute area, perimeter, circularity and a histogram.",
              "قِس صورة: اضبط التباين مع القص، وجد الحواف، واحسب المساحة والمحيط والاستدارة والمدرج التكراري."),
        steps=(
            ("Increase contrast and brightness, clipping to [0, 1].", "زِد التباين والسطوع مع القص إلى [0, 1]."),
            ("Compute the gradient magnitude.", "احسب مقدار التدرّج."),
            ("Compute the edge density.", "احسب كثافة الحواف."),
            ("Measure the object's area.", "قِس مساحة الجسم."),
            ("Compute an 8-bin histogram.", "احسب مدرجًا تكراريًا من 8 فئات."),
        ),
        starter='''import numpy as np

rng = np.random.default_rng(0)
img = np.full((64, 64), 0.2) + rng.normal(0, 0.02, (64, 64))   # grayscale background
img[16:48, 16:48] += 0.6                                         # a bright 32x32 square object
img = np.clip(img, 0, 1)

# Step 1: contrast x1.5, brightness +0.1, then keep values valid
adjusted = ___
clipped_share = float((adjusted >= 1.0).mean())                  # how much detail was lost to clipping

# Step 2: edge strength from the image gradient
gy, gx = np.gradient(img)
magnitude = ___
edges = magnitude > 0.2
# Step 3: share of pixels that are edges
edge_density = ___

mask = img > 0.5
# Step 4: object area in pixels
area = ___
padded = np.pad(mask, 1)
interior = padded[:-2, 1:-1] & padded[2:, 1:-1] & padded[1:-1, :-2] & padded[1:-1, 2:]
perimeter = int((mask & ~interior).sum())                        # object pixels touching the background
circularity = 4 * np.pi * area / perimeter ** 2

# Step 5: how many pixels fall into each of 8 brightness bins
histogram = ___
print(round(clipped_share, 3), round(edge_density, 3), area, perimeter, round(circularity, 3), histogram)
''',
        answers=("np.clip(1.5 * img + 0.1, 0, 1)", "np.hypot(gx, gy)", "float(edges.mean())", "int(mask.sum())",
                 "np.histogram(img, bins=8, range=(0, 1))[0].tolist()"),
        checks=(
            check("bool(np.allclose(adjusted, np.clip(1.5 * img + 0.1, 0, 1))) and float(adjusted.max()) <= 1.0", True,
                  "Blank 1: `np.clip(1.5 * img + 0.1, 0, 1)`.", "الفراغ 1: `np.clip(1.5 * img + 0.1, 0, 1)`."),
            check("bool(np.allclose(magnitude, np.sqrt(gx ** 2 + gy ** 2)))", True, "Blank 2: `np.hypot(gx, gy)` (or `np.sqrt(gx**2 + gy**2)`).",
                  "الفراغ 2: `np.hypot(gx, gy)` (أو `np.sqrt(gx**2 + gy**2)`)."),
            check("abs(float(edge_density) - float(edges.mean())) < 1e-12 and 0 < float(edge_density) < 0.2", True,
                  "Blank 3: the mean of the boolean edge map.", "الفراغ 3: متوسط خريطة الحواف المنطقية."),
            check("[int(area), int(perimeter)]", [1024, 124], "Blank 4: count the True pixels in `mask`.", "الفراغ 4: عُدّ البكسلات True في `mask`."),
            check("sum(histogram) == 4096 and len(histogram) == 8 and list(histogram) == np.histogram(img, bins=8, range=(0, 1))[0].tolist()", True,
                  "Blank 5: `np.histogram(img, bins=8, range=(0, 1))[0].tolist()`.", "الفراغ 5: `np.histogram(img, bins=8, range=(0, 1))[0].tolist()`."),
        ),
        hints=(
            ("Multiply for contrast, add for brightness, then `np.clip`.", "اضرب للتباين وأضف للسطوع، ثم `np.clip`."),
            ("Gradient magnitude is the length of (gx, gy).", "مقدار التدرّج هو طول (gx, gy)."),
            ("`np.histogram` returns (counts, bin edges).", "تعيد `np.histogram` (الأعداد، حدود الفئات)."),
        ),
        success=("Correct! The square has area 1024 and perimeter 124, so its circularity is well below 1 - exactly how contour metrics tell squares from circles.",
                 "صحيح! مساحة المربع 1024 ومحيطه 124، فاستدارته أقل بكثير من 1 - وهكذا تميّز مقاييس الحدود المربعات من الدوائر."),
        expected=(
            "OpenCV is not installed in the sandbox, so these measurements use NumPy; `cv2.Canny`, `cv2.findContours` and `cv2.contourArea` compute the same ideas.",
            "مكتبة OpenCV غير مثبّتة في بيئة التدريب، لذلك تستخدم هذه القياسات NumPy؛ وتحسب `cv2.Canny` و`cv2.findContours` و`cv2.contourArea` الأفكار نفسها.",
        ),
        reflect=("Locally, run Canny with two threshold pairs and the Haar face detector on a group photo. What do the thresholds trade off?",
                 "محليًا، شغّل Canny بزوجين من العتبات وكاشف الوجوه Haar على صورة جماعية. ما الذي تقايض بينه العتبات؟"),
    ),
    "COURSE-013.M15.L01.EX01": Guided(
        goal=("Implement scaled dot-product attention in NumPy and read what one row of the attention matrix means.",
              "نفّذ الانتباه بالضرب النقطي المُحجَّم في NumPy، واقرأ معنى صف واحد في مصفوفة الانتباه."),
        steps=(
            ("Compute the scaled similarity scores.", "احسب درجات التشابه المحجّمة."),
            ("Normalize each row with softmax.", "طبّع كل صف بـ softmax."),
            ("Return the weighted sum of the values.", "أعد المجموع الموزون للقيم."),
            ("Find which token token 0 attends to most.", "جد الرمز الذي ينتبه إليه الرمز 0 أكثر."),
        ),
        starter='''import numpy as np

def scaled_dot_product_attention(Q, K, V):
    d_k = Q.shape[-1]
    # Step 1: every query against every key, scaled by sqrt(d_k)
    scores = ___
    weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
    # Step 2: each row becomes a probability distribution
    weights = ___
    # Step 3: mix the values with those weights
    return ___, weights

Q = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]])
K = np.array([[0.0, 1.0, 0.0], [0.2, 0.0, 0.1], [1.0, 0.0, 1.0]])
V = np.array([[1.0, 0.0], [0.0, 1.0], [5.0, 5.0]])
output, weights = scaled_dot_product_attention(Q, K, V)

# Step 4: the key token that token 0 attends to most
most_attended = ___
print(weights.round(3))
print("rows sum to 1:", weights.sum(axis=1).round(6), "| token 0 attends most to token", most_attended)
''',
        answers=("Q @ K.T / np.sqrt(d_k)", "weights / weights.sum(axis=-1, keepdims=True)", "weights @ V", "int(weights[0].argmax())"),
        checks=(
            check("bool(np.allclose(weights.sum(axis=1), 1))", True, "Blank 2: divide each row by its own sum (`keepdims=True`).",
                  "الفراغ 2: اقسم كل صف على مجموعه (`keepdims=True`)."),
            check("bool(np.allclose(weights, (lambda s: np.exp(s - s.max(-1, keepdims=True)) / np.exp(s - s.max(-1, keepdims=True)).sum(-1, keepdims=True))(Q @ K.T / np.sqrt(3))))", True,
                  "Blank 1: `Q @ K.T / np.sqrt(d_k)`.", "الفراغ 1: `Q @ K.T / np.sqrt(d_k)`."),
            check("bool(np.allclose(output, weights @ V))", True, "Blank 3: `weights @ V`.", "الفراغ 3: `weights @ V`."),
            check("most_attended", 2, "Blank 4: the index of the largest weight in row 0.", "الفراغ 4: فهرس أكبر وزن في الصف 0."),
        ),
        hints=(
            ("Queries are rows of Q, keys are rows of K - so use `K.T`.", "الاستعلامات صفوف Q والمفاتيح صفوف K - لذا استخدم `K.T`."),
            ("Softmax: exponentiate, then divide by the row sum.", "softmax: خذ الأس ثم اقسم على مجموع الصف."),
            ("`argmax` on row 0 gives the most attended key.", "يعطي `argmax` على الصف 0 المفتاح الأكثر انتباهًا."),
        ),
        success=("Correct! Each row is a probability distribution over the keys: token 0 puts most of its weight on token 2, so its output is pulled toward V[2].",
                 "صحيح! كل صف توزيع احتمالي على المفاتيح: يضع الرمز 0 معظم وزنه على الرمز 2، فيُسحب مخرجه نحو V[2]."),
        reflect=("Build a decision table for prompting, full fine-tuning and LoRA: weight changes, data needs, GPU cost, artifact size and typical use.",
                 "ابنِ جدول قرار للتوجيه بالموجّهات، والضبط الدقيق الكامل، وLoRA: تغيّر الأوزان، والحاجة إلى البيانات، وتكلفة GPU، وحجم الناتج، والاستخدام المعتاد."),
    ),
    "COURSE-013.M15.L01.EX02": Guided(
        goal=("Build a retrieve-then-answer prototype: embed documents and a query, retrieve the top two, and extract an answer from the best context.",
              "ابنِ نموذجًا أوليًا يسترجع ثم يجيب: ضمّن المستندات والاستعلام، واسترجع أفضل اثنين، واستخرج إجابة من أفضل سياق."),
        steps=(
            ("Embed the query with the same model as the documents.", "ضمّن الاستعلام بالنموذج نفسه المستخدم للمستندات."),
            ("Compute cosine similarities.", "احسب تشابه جيب التمام."),
            ("Retrieve the two best documents.", "استرجع أفضل مستندين."),
            ("Extract the sentence that best answers the question.", "استخرج الجملة التي تجيب عن السؤال على أفضل وجه."),
        ),
        starter='''import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    "Retrieval-augmented generation grounds answers in retrieved documents. Grounding reduces hallucinations because the model quotes real sources.",
    "Convolutional networks learn image features with shared filters. Pooling makes them robust to small shifts.",
    "LoRA fine-tunes small adapter matrices. It keeps the base model frozen and saves memory.",
    "Tokenizers split text into subword units. Vocabulary size trades sequence length against coverage.",
    "Vector databases store embeddings for similarity search. They return the nearest documents for a query.",
]
# Stand-in for SentenceTransformer.encode: TF-IDF vectors (the retrieval workflow is identical)
vectorizer = TfidfVectorizer().fit(documents)
doc_vectors = vectorizer.transform(documents)
query = "How does grounding reduce hallucinations?"

# Step 1: the query in the same vector space
query_vector = ___
# Step 2: one similarity per document
similarities = ___
# Step 3: indices of the two most similar documents
top_two = ___
context = documents[top_two[0]]

# Step 4: an extractive answer - the context sentence sharing the most words with the question
def extract_answer(question, context):
    question_words = set(re.findall(r"[a-z]+", question.lower()))
    sentences = [s.strip() + "." for s in context.split(".") if s.strip()]
    return ___

answer = extract_answer(query, context)
print("retrieved:", top_two)
print("context:", context)
print("answer:", answer)
''',
        answers=(
            "vectorizer.transform([query])",
            "cosine_similarity(query_vector, doc_vectors)[0]",
            "np.argsort(-similarities)[:2].tolist()",
            'max(sentences, key=lambda s: len(question_words & set(re.findall(r"[a-z]+", s.lower()))))',
        ),
        checks=(
            check("query_vector.shape[1] == doc_vectors.shape[1]", True, "Blank 1: `vectorizer.transform([query])` - transform, never fit, the query.",
                  "الفراغ 1: `vectorizer.transform([query])` - حوّل الاستعلام ولا تدرّب عليه."),
            check("bool(np.allclose(similarities, cosine_similarity(vectorizer.transform([query]), doc_vectors)[0]))", True,
                  "Blank 2: `cosine_similarity(query_vector, doc_vectors)[0]`.", "الفراغ 2: `cosine_similarity(query_vector, doc_vectors)[0]`."),
            check("list(top_two)[0] == 0 and len(top_two) == 2 and list(top_two) == np.argsort(-similarities)[:2].tolist()", True,
                  "Blank 3: sort similarities from high to low and keep two indices.", "الفراغ 3: رتّب التشابهات تنازليًا واحتفظ بفهرسين."),
            check("answer", "Grounding reduces hallucinations because the model quotes real sources.",
                  "Blank 4: pick the sentence with the largest word overlap with the question.", "الفراغ 4: اختر الجملة ذات أكبر تداخل في الكلمات مع السؤال."),
        ),
        hints=(
            ("Use the fitted vectorizer's `transform` for new text.", "استخدم `transform` من أداة التحويل المدرَّبة للنص الجديد."),
            ("`cosine_similarity` returns a 1 × N matrix for one query.", "تعيد `cosine_similarity` مصفوفة 1 × N لاستعلام واحد."),
            ("`max(items, key=...)` returns the best-scoring item.", "تعيد `max(items, key=...)` العنصر ذا الدرجة الأفضل."),
        ),
        success=("Correct! Retrieval found the RAG document and the extractor quoted the sentence that answers the question - the answer comes from a real source instead of the model's memory.",
                 "صحيح! وجد الاسترجاع مستند RAG واقتبس المستخرج الجملة التي تجيب عن السؤال - فالإجابة تأتي من مصدر حقيقي لا من ذاكرة النموذج."),
        expected=(
            "SentenceTransformers and QA models cannot be downloaded in the sandbox; TF-IDF vectors and a word-overlap extractor stand in, and the retrieve-then-answer workflow is the same.",
            "لا يمكن تنزيل SentenceTransformers ونماذج الإجابة عن الأسئلة في بيئة التدريب؛ لذا تحل محلها متجهات TF-IDF ومستخرج يعتمد على تداخل الكلمات، ويبقى سير العمل «استرجع ثم أجب» هو نفسه.",
        ),
    ),
}
