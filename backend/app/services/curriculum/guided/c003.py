"""COURSE-003 Applied Deep Learning (PyTorch): guided implementation exercises.

The practice sandbox has NumPy but not PyTorch. Exercises about shapes and
maths run in NumPy, whose arrays follow the same shape, indexing and
broadcasting rules as tensors; each step names the PyTorch equivalent.
Exercises about the PyTorch API itself stay in PyTorch and are checked by
reading the code.
"""
from . import Guided, check

TORCH_NOTE = (
    "PyTorch is not installed in the practice sandbox, so Check answer reads your code instead of running it.",
    "مكتبة PyTorch غير مثبّتة في بيئة التدريب، لذلك يقرأ «تحقّق من الإجابة» الكود بدل تشغيله.",
)
NUMPY_NOTE = (
    "NumPy arrays follow the same shape, indexing and broadcasting rules as PyTorch tensors, so this exercise runs in NumPy; the comments name the PyTorch call.",
    "تتبع مصفوفات NumPy قواعد الأبعاد والفهرسة والبث نفسها في موترات PyTorch، لذلك يعمل هذا التمرين بـ NumPy، وتذكر التعليقات استدعاء PyTorch المقابل.",
)

ATTENTION_REFERENCE = (
    "(lambda s: (lambda e: e / e.sum(-1, keepdims=True))(np.exp(s - s.max(-1, keepdims=True))))"
    "(np.where(np.tril(np.ones((T, T), dtype=bool)), Q @ K.T / np.sqrt(d_k), -np.inf))"
)

EXERCISES = {
    "COURSE-003.M03.L01.EX01": Guided(
        goal=("Create a small tensor of 2D points and read its shape and indices.",
              "أنشئ موترًا صغيرًا من نقاط ثنائية الأبعاد واقرأ أبعاده وفهارسه."),
        steps=(
            ("Store the points (4, 1), (5, 3) and (2, 1) with one point per row.",
             "خزّن النقاط (4, 1) و(5, 3) و(2, 1) بحيث تكون كل نقطة في صف."),
            ("Select the complete second point.", "اختر النقطة الثانية كاملة."),
            ("Select only the y-coordinate of the first point.", "اختر الإحداثي y للنقطة الأولى فقط."),
            ("Create zeros with shape (4, 3, 2).", "أنشئ أصفارًا بالأبعاد (4, 3, 2)."),
            ("Add a leading size-1 dimension to `points`.", "أضف بُعدًا أماميًا بحجم 1 إلى `points`."),
        ),
        starter='''import numpy as np

# Step 1: three 2D points, one per row (torch.tensor([[4.0, 1.0], ...]))
points = ___

# Step 2: the complete second point (row index 1)
second_point = ___

# Step 3: only the y-coordinate (column 1) of the first point
first_y = ___

# Step 4: zeros with shape (4, 3, 2) (torch.zeros(4, 3, 2))
zeros = ___

# Step 5: a leading size-1 dimension (torch: points.unsqueeze(0))
batched = ___

print("points:", points.shape, "second:", second_point, "first y:", first_y)
print("zeros:", zeros.ndim, "dimensions,", zeros.size, "values")
print("batched:", batched.shape)
''',
        answers=(
            "np.array([[4.0, 1.0], [5.0, 3.0], [2.0, 1.0]])",
            "points[1]",
            "points[0, 1]",
            "np.zeros((4, 3, 2))",
            "np.expand_dims(points, axis=0)",
        ),
        checks=(
            check("np.asarray(points).tolist()", [[4.0, 1.0], [5.0, 3.0], [2.0, 1.0]],
                  "Blank 1: write the three points as a nested list inside `np.array`, one `[x, y]` per row.",
                  "الفراغ 1: اكتب النقاط الثلاث قائمة متداخلة داخل `np.array`، كل `[x, y]` في صف."),
            check("np.asarray(second_point).tolist()", [5.0, 3.0],
                  "Blank 2: the second point is row index 1: `points[1]`.",
                  "الفراغ 2: النقطة الثانية هي الصف ذو الفهرس 1: `points[1]`."),
            check("float(first_y)", 1.0,
                  "Blank 3: index row 0, column 1: `points[0, 1]`.",
                  "الفراغ 3: افهرس الصف 0 والعمود 1: `points[0, 1]`."),
            check("list(zeros.shape)", [4, 3, 2],
                  "Blank 4: pass the shape as a tuple: `np.zeros((4, 3, 2))`.",
                  "الفراغ 4: مرّر الأبعاد صفًّا (tuple): `np.zeros((4, 3, 2))`."),
            check("list(batched.shape)", [1, 3, 2],
                  "Blank 5: add the new axis at position 0, giving shape (1, 3, 2).",
                  "الفراغ 5: أضف المحور الجديد في الموضع 0، فتصبح الأبعاد (1, 3, 2)."),
        ),
        hints=(
            ("A shape lists the size of every dimension from the outside in: 3 points × 2 coordinates is (3, 2).",
             "تسرد الأبعاد حجم كل بُعد من الخارج إلى الداخل: 3 نقاط × إحداثيان تساوي (3, 2)."),
            ("Indexing with one number selects a row; `[row, column]` selects one value.",
             "الفهرسة برقم واحد تختار صفًا، و`[row, column]` تختار قيمة واحدة."),
            ("`np.expand_dims(points, axis=0)` (or `points[None]`) is NumPy's version of `unsqueeze(0)`.",
             "الدالة `np.expand_dims(points, axis=0)` (أو `points[None]`) هي مقابل `unsqueeze(0)` في NumPy."),
        ),
        success=("Correct! You can now read what every dimension of a tensor means and pick out rows and single values.",
                 "صحيح! أصبحت قادرًا على قراءة معنى كل بُعد في الموتر واختيار الصفوف والقيم المفردة."),
        expected=NUMPY_NOTE,
        reflect=("How many scalar values does a (4, 3, 2) tensor hold, and why?",
                 "كم قيمة مفردة يحتوي موتر بالأبعاد (4, 3, 2)؟ ولماذا؟"),
    ),
    "COURSE-003.M03.L01.EX02": Guided(
        goal=("Predict broadcast result shapes by aligning shapes from the right, then verify one.",
              "توقّع أبعاد نتيجة البث (Broadcasting) بمحاذاة الأبعاد من اليمين، ثم تحقّق من إحداها."),
        steps=(
            ("For each case, write the result shape as a tuple.", "اكتب لكل حالة أبعاد النتيجة في صفّ (tuple)."),
            ("Write `None` when the shapes cannot be broadcast together.", "اكتب `None` عندما لا يمكن بث الأبعاد معًا."),
            ("Run the code to see one case verified.", "شغّل الكود لترى التحقق من إحدى الحالات."),
        ),
        starter='''import numpy as np

# Align shapes from the RIGHT. Two sizes are compatible when they are equal or one of them is 1.
# Write the result shape as a tuple, or None when broadcasting is impossible.

# Case 1: (3, 4) and (4,)
case_1 = ___
# Case 2: (3, 1) and (1, 5)
case_2 = ___
# Case 3: (2, 3, 5, 5) and (3, 1, 1)
case_3 = ___
# Case 4: (2, 4) and (3, 4)
case_4 = ___
# Case 5: (1, 3, 1) and (4, 1, 5)
case_5 = ___

# torch.ones(...) broadcasts exactly like np.ones(...)
print("case 2 really gives:", (np.ones((3, 1)) + np.ones((1, 5))).shape)
''',
        answers=("(3, 4)", "(3, 5)", "(2, 3, 5, 5)", "None", "(4, 3, 5)"),
        checks=(
            check("None if case_1 is None else list(case_1)", [3, 4],
                  "Case 1: (4,) lines up with the last axis of (3, 4), so the result is (3, 4).",
                  "الحالة 1: يتحاذى (4,) مع المحور الأخير من (3, 4)، فتكون النتيجة (3, 4)."),
            check("None if case_2 is None else list(case_2)", [3, 5],
                  "Case 2: each size-1 axis stretches to match the other shape: (3, 5).",
                  "الحالة 2: يتمدد كل محور حجمه 1 ليطابق الشكل الآخر: (3, 5)."),
            check("None if case_3 is None else list(case_3)", [2, 3, 5, 5],
                  "Case 3: (3, 1, 1) aligns with the last three axes of (2, 3, 5, 5); the result keeps (2, 3, 5, 5).",
                  "الحالة 3: يتحاذى (3, 1, 1) مع المحاور الثلاثة الأخيرة من (2, 3, 5, 5)، فتبقى النتيجة (2, 3, 5, 5)."),
            check("case_4 is None", True,
                  "Case 4: the first axes are 2 and 3 - different and neither is 1 - so write `None`.",
                  "الحالة 4: المحوران الأولان 2 و3 مختلفان وليس أيٌّ منهما 1، لذا اكتب `None`."),
            check("None if case_5 is None else list(case_5)", [4, 3, 5],
                  "Case 5: compare axis by axis - (1 vs 4), (3 vs 1), (1 vs 5) - and keep the larger size each time.",
                  "الحالة 5: قارن محورًا بمحور - (1 مقابل 4) و(3 مقابل 1) و(1 مقابل 5) - واحتفظ بالحجم الأكبر في كل مرة."),
        ),
        hints=(
            ("Write both shapes right-aligned, one above the other; a missing axis on the left counts as size 1.",
             "اكتب الشكلين محاذيين لليمين أحدهما فوق الآخر؛ والمحور الناقص من اليسار يُعدّ بحجم 1."),
            ("In each column the sizes must be equal or one of them must be 1; the result takes the larger size.",
             "في كل عمود يجب أن يتساوى الحجمان أو يكون أحدهما 1، وتأخذ النتيجة الحجم الأكبر."),
            ("If any column has two different sizes and neither is 1, broadcasting fails: the answer is `None`.",
             "إذا احتوى أي عمود على حجمين مختلفين ليس أيٌّ منهما 1 يفشل البث، والإجابة `None`."),
        ),
        success=("Correct! Aligning shapes from the right lets you predict any broadcast before running it.",
                 "صحيح! محاذاة الأبعاد من اليمين تتيح لك توقّع أي عملية بث قبل تشغيلها."),
        expected=NUMPY_NOTE,
    ),
    "COURSE-003.M03.L01.EX03": Guided(
        goal=("See the difference between a view, a copy and a transpose by watching what changes in the original data.",
              "تعرّف على الفرق بين العرض (view) والنسخة (copy) والمنقول (transpose) بمراقبة ما يتغير في البيانات الأصلية."),
        steps=(
            ("Take row 1 as a view and change it.", "خذ الصف 1 بوصفه عرضًا (view) وغيّره."),
            ("Take row 2 as an independent copy and change it.", "خذ الصف 2 نسخةً مستقلة وغيّرها."),
            ("Transpose `points` without moving any data.", "انقل `points` (transpose) دون نقل أي بيانات."),
            ("Make a contiguous copy of the transpose.", "أنشئ نسخة متجاورة (contiguous) من المنقول."),
        ),
        starter='''import numpy as np

points = np.array([[4.0, 1.0], [5.0, 3.0], [2.0, 1.0]])
print("shape", points.shape, "strides (bytes)", points.strides)

# Step 1: row 1 as a VIEW (basic indexing shares memory, like points[1] in PyTorch)
second_point = ___
second_point[0] = 10.0
view_changed_points = bool(points[1, 0] == 10.0)

# Step 2: row 2 as an independent COPY (torch: points[2].clone())
third_point = ___
third_point[0] = 99.0
copy_changed_points = bool(points[2, 0] == 99.0)

# Step 3: the transpose (torch: points.t()) - only the strides change
points_t = ___
print("transpose strides", points_t.strides, "contiguous?", points_t.flags["C_CONTIGUOUS"])

# Step 4: a contiguous copy of the transpose (torch: points_t.contiguous())
points_t_contiguous = ___
print("after", points_t_contiguous.strides, "contiguous?", points_t_contiguous.flags["C_CONTIGUOUS"])
print("view changed points:", view_changed_points, "| copy changed points:", copy_changed_points)
''',
        answers=("points[1]", "points[2].copy()", "points.T", "np.ascontiguousarray(points_t)"),
        checks=(
            check("view_changed_points", True,
                  "Blank 1: `points[1]` is a view, so writing through it must change `points`.",
                  "الفراغ 1: `points[1]` عرض (view)، لذا يجب أن يغيّر التعديلُ عبره المصفوفةَ `points`."),
            check("copy_changed_points", False,
                  "Blank 2: call `.copy()` on the row so changing it leaves `points` untouched.",
                  "الفراغ 2: استدعِ `.copy()` على الصف كي لا يتأثر `points` عند تعديله."),
            check("list(points_t.shape) == [2, 3] and bool(np.shares_memory(points, points_t))", True,
                  "Blank 3: `points.T` gives shape (2, 3) while still sharing memory with `points`.",
                  "الفراغ 3: يعطي `points.T` الأبعاد (2, 3) مع بقاء الذاكرة مشتركة مع `points`."),
            check("bool(points_t_contiguous.flags['C_CONTIGUOUS']) and not np.shares_memory(points_t_contiguous, points) and points_t_contiguous.tolist() == points_t.tolist()", True,
                  "Blank 4: `np.ascontiguousarray(points_t)` copies the values into a new row-major layout.",
                  "الفراغ 4: تنسخ `np.ascontiguousarray(points_t)` القيم إلى ترتيب جديد متجاور بحسب الصفوف."),
        ),
        hints=(
            ("Plain indexing such as `points[0]` returns a view on the same memory.",
             "الفهرسة البسيطة مثل `points[0]` تعيد عرضًا على الذاكرة نفسها."),
            ("`.copy()` (PyTorch: `.clone()`) allocates new memory, so later changes stay local.",
             "يحجز `.copy()` (في PyTorch: `.clone()`) ذاكرة جديدة، فتبقى التعديلات اللاحقة محلية."),
            ("A transpose only swaps the strides; `np.ascontiguousarray` (PyTorch: `.contiguous()`) rewrites the data in order.",
             "يبدّل المنقول الخطوات (strides) فقط، بينما يعيد `np.ascontiguousarray` (في PyTorch: `.contiguous()`) كتابة البيانات بالترتيب."),
        ),
        success=("Correct! Views share storage, copies do not, and a transpose is cheap because it only changes strides until you ask for a contiguous layout.",
                 "صحيح! يشارك العرضُ التخزينَ ولا تشاركه النسخة، والمنقول رخيص لأنه يغيّر الخطوات فقط إلى أن تطلب ترتيبًا متجاورًا."),
        expected=(
            "NumPy reports strides in bytes, PyTorch in elements; the behaviour you observe is the same in both.",
            "يعرض NumPy الخطوات (strides) بالبايت، بينما يعرضها PyTorch بعدد العناصر؛ والسلوك الذي تلاحظه واحد في الاثنين.",
        ),
        reflect=("Why can a transpose be almost free before you call `.contiguous()`?",
                 "لماذا يكاد يكون النقل (transpose) بلا تكلفة قبل استدعاء `.contiguous()`؟"),
    ),
    "COURSE-003.M04.L01.EX01": Guided(
        goal=("Turn an image array (height × width × channels, 0-255) into a batched, normalized channels-first tensor.",
              "حوّل مصفوفة صورة (ارتفاع × عرض × قنوات، بقيم 0-255) إلى موتر بترتيب القنوات أولًا، مُطبَّع وضمن دفعة."),
        steps=(
            ("Move the channel axis first: C × H × W.", "انقل محور القنوات إلى البداية: C × H × W."),
            ("Convert to float and scale pixels to [0, 1].", "حوّل القيم إلى أعداد عشرية وحجّم البكسلات إلى [0, 1]."),
            ("Add a leading batch dimension: 1 × C × H × W.", "أضف بُعد دفعة في البداية: 1 × C × H × W."),
        ),
        starter='''import numpy as np

# A tiny 4 x 6 RGB image, laid out the way image libraries return it: H x W x C, uint8
image = np.arange(4 * 6 * 3, dtype=np.uint8).reshape(4, 6, 3)
print("raw:", image.shape, image.dtype)

# Step 1: channels first, C x H x W (torch: torch.from_numpy(image).permute(2, 0, 1))
chw = ___

# Step 2: float values scaled from 0-255 to [0, 1] (torch: chw.float() / 255)
scaled = ___

# Step 3: a leading batch dimension, 1 x C x H x W (torch: scaled.unsqueeze(0))
batch = ___

print("channels first:", chw.shape)
print("scaled:", scaled.dtype, float(scaled.min()), float(scaled.max()))
print("batch:", batch.shape)
''',
        answers=("image.transpose(2, 0, 1)", "chw.astype(np.float32) / 255.0", "np.expand_dims(scaled, axis=0)"),
        checks=(
            check("list(chw.shape) == [3, 4, 6] and bool(np.array_equal(chw[0], image[:, :, 0]))", True,
                  "Blank 1: reorder the axes with `transpose(2, 0, 1)` - a reshape would scramble the pixels.",
                  "الفراغ 1: أعد ترتيب المحاور بـ `transpose(2, 0, 1)` - أما reshape فسيخلط البكسلات."),
            check("str(scaled.dtype).startswith('float') and abs(float(scaled.max()) - 71 / 255) < 1e-6", True,
                  "Blank 2: convert to float, then divide by 255 so values fall in [0, 1].",
                  "الفراغ 2: حوّل إلى أعداد عشرية ثم اقسم على 255 لتقع القيم في [0, 1]."),
            check("list(batch.shape)", [1, 3, 4, 6],
                  "Blank 3: add the batch axis at the front, giving (1, 3, 4, 6).",
                  "الفراغ 3: أضف محور الدفعة في البداية لتصبح الأبعاد (1, 3, 4, 6)."),
        ),
        hints=(
            ("The raw axes are (H=0, W=1, C=2); listing them as (2, 0, 1) puts channels first.",
             "المحاور الخام هي (H=0، W=1، C=2)؛ وكتابتها بالترتيب (2, 0, 1) تضع القنوات أولًا."),
            ("Integer pixels must become floats before dividing, otherwise you lose the fractions.",
             "يجب تحويل البكسلات الصحيحة إلى أعداد عشرية قبل القسمة، وإلا ضاعت الكسور."),
            ("`np.expand_dims(scaled, axis=0)` adds the batch dimension.",
             "تضيف `np.expand_dims(scaled, axis=0)` بُعد الدفعة."),
        ),
        success=("Correct! The image is now a float batch in the 1 × C × H × W layout that convolutional networks expect.",
                 "صحيح! أصبحت الصورة دفعة عشرية بالترتيب 1 × C × H × W الذي تتوقعه الشبكات الالتفافية."),
        expected=NUMPY_NOTE,
    ),
    "COURSE-003.M04.L01.EX02": Guided(
        goal=("Classify table columns as continuous, ordinal or categorical, then one-hot encode a categorical column.",
              "صنّف أعمدة الجدول إلى متصلة أو ترتيبية أو فئوية، ثم رمّز عمودًا فئويًا بطريقة One-hot."),
        steps=(
            ("Fill in the kind of each variable.", "أكمل نوع كل متغير."),
            ("Set a 1 in the column of each row's category.", "ضع القيمة 1 في عمود الفئة الخاصة بكل صف."),
        ),
        starter='''import numpy as np

# Step 1: "continuous", "ordinal" or "categorical"?
kinds = {
    "temperature_c": "continuous",
    "tshirt_size": ___,       # small / medium / large
    "country": ___,           # Egypt, Japan, Brazil, ...
    "star_rating": ___,       # 1 to 5 stars
    "weight_kg": "continuous",
}

# Step 2: product category IDs are labels, not quantities, so one-hot encode them
# (torch: torch.zeros(4, 4).scatter_(1, ids.unsqueeze(1), 1.0))
category_ids = np.array([2, 0, 3, 2])
one_hot = np.zeros((len(category_ids), 4))
one_hot[np.arange(len(category_ids)), ___] = 1.0

print(kinds)
print(one_hot)
''',
        answers=('"ordinal"', '"categorical"', '"ordinal"', "category_ids"),
        checks=(
            check("kinds['tshirt_size']", "ordinal",
                  "Blank 1: sizes have a natural order (small < medium < large) but no fixed distance: ordinal.",
                  "الفراغ 1: للمقاسات ترتيب طبيعي (صغير < متوسط < كبير) دون مسافة ثابتة بينها: ترتيبي (ordinal)."),
            check("kinds['country']", "categorical",
                  "Blank 2: countries are names with no order: categorical.",
                  "الفراغ 2: الدول أسماء بلا ترتيب: فئوي (categorical)."),
            check("kinds['star_rating']", "ordinal",
                  "Blank 3: 4 stars is better than 3, but the gap between ratings is not a measured amount: ordinal.",
                  "الفراغ 3: أربع نجوم أفضل من ثلاث، لكن الفرق بين التقييمات ليس كمية مقيسة: ترتيبي (ordinal)."),
            check("one_hot.tolist()", [[0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
                  "Blank 4: use `category_ids` as the column index, so row i gets a 1 in column `category_ids[i]`.",
                  "الفراغ 4: استخدم `category_ids` فهرسًا للأعمدة، فيحصل الصف i على 1 في العمود `category_ids[i]`."),
        ),
        hints=(
            ("Ask two questions: is there an order? is the distance between values meaningful?",
             "اطرح سؤالين: هل يوجد ترتيب؟ وهل للمسافة بين القيم معنى؟"),
            ("Ordered but uneven steps → ordinal; no order at all → categorical.",
             "ترتيب بخطوات غير متساوية ← ترتيبي؛ بلا ترتيب إطلاقًا ← فئوي."),
            ("Fancy indexing with a row array and a column array sets one cell per row: `one_hot[rows, category_ids]`.",
             "الفهرسة بمصفوفة صفوف ومصفوفة أعمدة تضبط خلية واحدة في كل صف: `one_hot[rows, category_ids]`."),
        ),
        success=("Correct! Each column now has a representation that keeps its real meaning, and the category IDs no longer pretend to be quantities.",
                 "صحيح! أصبح لكل عمود تمثيل يحافظ على معناه الحقيقي، ولم تعد معرّفات الفئات تتظاهر بأنها كميات."),
        expected=NUMPY_NOTE,
        reflect=("What false meaning would a network learn if you fed product category ID 3 as the number 3?",
                 "ما المعنى الخاطئ الذي ستتعلمه الشبكة لو أدخلت معرّف الفئة 3 بوصفه العدد 3؟"),
    ),
    "COURSE-003.M04.L01.EX03": Guided(
        goal=("Reshape 72 hourly rows into 3 daily sequences and standardize one channel.",
              "أعد تشكيل 72 صفًا بالساعة إلى 3 سلاسل يومية، ثم وحّد مقياس قناة واحدة."),
        steps=(
            ("Reshape (72, 5) into 3 days × 24 hours × 5 variables.", "أعد تشكيل (72, 5) إلى 3 أيام × 24 ساعة × 5 متغيرات."),
            ("Reorder to N × C × L = (3, 5, 24).", "أعد الترتيب إلى N × C × L = (3, 5, 24)."),
            ("Standardize channel 0 to mean 0 and standard deviation 1.", "وحّد القناة 0 لتصبح بمتوسط 0 وانحراف معياري 1."),
        ),
        starter='''import numpy as np

hourly = np.arange(72 * 5, dtype=float).reshape(72, 5)   # 72 hours x 5 variables

# Step 1: 3 days x 24 hours x 5 variables (torch: hourly.view(3, 24, 5))
daily = ___

# Step 2: N x C x L = (3, 5, 24) (torch: daily.transpose(1, 2))
ncl = ___

# Step 3: standardize channel 0 over all available data
temperature = ncl[:, 0, :]
temperature_std = ___

print(daily.shape, ncl.shape)
print("mean", round(float(temperature_std.mean()), 3), "std", round(float(temperature_std.std()), 3))
''',
        answers=("hourly.reshape(3, 24, 5)", "daily.transpose(0, 2, 1)",
                 "(temperature - temperature.mean()) / temperature.std()"),
        checks=(
            check("list(daily.shape) == [3, 24, 5] and daily[1, 0].tolist() == hourly[24].tolist()", True,
                  "Blank 1: reshape to (3, 24, 5); hour 24 must become the first hour of day 2.",
                  "الفراغ 1: أعد التشكيل إلى (3, 24, 5)؛ يجب أن تصبح الساعة 24 أول ساعة في اليوم الثاني."),
            check("list(ncl.shape) == [3, 5, 24] and bool(np.array_equal(ncl[2, 3], hourly[48:72, 3]))", True,
                  "Blank 2: swap the last two axes with `transpose(0, 2, 1)` - reshaping again would mix variables and hours.",
                  "الفراغ 2: بدّل المحورين الأخيرين بـ `transpose(0, 2, 1)` - فإعادة التشكيل مرة أخرى ستخلط المتغيرات بالساعات."),
            check("round(float(temperature_std.mean()), 6) == 0.0 and round(float(temperature_std.std()), 6) == 1.0 and list(temperature_std.shape) == [3, 24]", True,
                  "Blank 3: subtract the channel's mean and divide by its standard deviation.",
                  "الفراغ 3: اطرح متوسط القناة ثم اقسم على انحرافها المعياري."),
        ),
        hints=(
            ("A reshape keeps the values in order, so 72 rows fill 3 blocks of 24.",
             "تحافظ إعادة التشكيل على ترتيب القيم، فتملأ الصفوف الـ72 ثلاث كتل من 24."),
            ("To change which axis comes where, use `transpose` with the new axis order.",
             "لتغيير موضع كل محور استخدم `transpose` مع الترتيب الجديد للمحاور."),
            ("Standardizing is `(x - x.mean()) / x.std()`.", "التوحيد هو `(x - x.mean()) / x.std()`."),
        ),
        success=("Correct! The hourly rows are now day-long sequences in N × C × L layout, ready for a 1D convolution or a recurrent model.",
                 "صحيح! أصبحت الصفوف بالساعة سلاسل يومية بترتيب N × C × L، جاهزة لالتفاف أحادي البعد أو نموذج تكراري."),
        expected=NUMPY_NOTE,
        reflect=("If several hours were missing from the middle of the data, which assumption of this reshape would break?",
                 "إذا فُقدت عدة ساعات من منتصف البيانات، فأي افتراض في إعادة التشكيل هذه سينكسر؟"),
    ),
    "COURSE-003.M05.L01.EX01": Guided(
        goal=("Compute a linear model's predictions and mean squared error by hand for two parameter settings.",
              "احسب يدويًا تنبؤات نموذج خطي ومتوسط مربع الخطأ لإعدادين مختلفين من المعاملات."),
        steps=(
            ("Return the linear model's prediction from `model`: the weight times the input, plus the bias.", "أعد من الدالة `model` تنبؤ النموذج الخطي: الوزن مضروبًا في المُدخل، زائد الانحياز."),
            ("Square the prediction errors inside `loss_fn`.", "ربّع أخطاء التنبؤ داخل `loss_fn`."),
            ("Compute the loss for w = 1, b = 0.", "احسب الخسارة عند w = 1 وb = 0."),
        ),
        starter='''import numpy as np

t_u = np.array([1.0, 2.0, 3.0])   # inputs
t_c = np.array([3.0, 5.0, 7.0])   # targets

# Step 1: the linear model
def model(t_u, w, b):
    return ___

# Step 2: mean squared error
def loss_fn(t_p, t_c):
    squared_diffs = ___
    return squared_diffs.mean()

# Step 3: predictions and loss for w=1.0, b=0.0
t_p_first = model(t_u, 1.0, 0.0)
loss_first = ___

# Compare with w=2.0, b=1.0
t_p_second = model(t_u, 2.0, 1.0)
loss_second = loss_fn(t_p_second, t_c)
print("first:", t_p_first, "loss", loss_first)
print("second:", t_p_second, "loss", loss_second)
''',
        answers=("w * t_u + b", "(t_p - t_c) ** 2", "loss_fn(t_p_first, t_c)"),
        checks=(
            check("np.asarray(t_p_first).tolist()", [1.0, 2.0, 3.0],
                  "Blank 1: the model multiplies by `w` and adds `b`: `w * t_u + b`.",
                  "الفراغ 1: يضرب النموذج في `w` ويضيف `b`: `w * t_u + b`."),
            check("round(float(loss_second), 6) == 0.0 and round(float(loss_fn(np.array([1.0, 1.0]), np.array([3.0, -1.0]))), 6) == 4.0", True,
                  "Blank 2: square each difference: `(t_p - t_c) ** 2`.",
                  "الفراغ 2: ربّع كل فرق: `(t_p - t_c) ** 2`."),
            check("round(float(loss_first), 4)", 9.6667,
                  "Blank 3: call `loss_fn` with the first predictions and the targets.",
                  "الفراغ 3: استدعِ `loss_fn` مع التنبؤات الأولى والأهداف."),
        ),
        hints=(
            ("A linear model is a weight times the input plus a bias.", "النموذج الخطي هو وزن مضروب في المدخل زائد انحياز (bias)."),
            ("The error is prediction minus target; squaring makes every error positive.",
             "الخطأ هو التنبؤ ناقص الهدف، والتربيع يجعل كل خطأ موجبًا."),
            ("With w = 1, b = 0 the errors are -2, -3, -4, so the loss is (4 + 9 + 16) / 3.",
             "عند w = 1 وb = 0 تكون الأخطاء -2 و-3 و-4، فتكون الخسارة (4 + 9 + 16) / 3."),
        ),
        success=("Correct! The loss falls from about 9.67 to 0, so w = 2, b = 1 fits these points exactly.",
                 "صحيح! تنخفض الخسارة من نحو 9.67 إلى 0، أي أن w = 2 وb = 1 تطابق هذه النقاط تمامًا."),
        expected=NUMPY_NOTE,
        reflect=("What does a lower loss tell you about the parameters - and what does it not tell you?",
                 "ماذا تخبرك الخسارة الأقل عن المعاملات، وما الذي لا تخبرك به؟"),
    ),
    "COURSE-003.M05.L01.EX02": Guided(
        goal=("Let autograd compute a gradient, compare it with the analytical gradient, and clear it before the next step.",
              "دع autograd يحسب التدرّج، وقارنه بالتدرّج التحليلي، ثم صفّره قبل الخطوة التالية."),
        steps=(
            ("Ask PyTorch to track gradients for `params`.", "اطلب من PyTorch تتبّع التدرّجات للمعاملات `params`."),
            ("Run the backward pass.", "نفّذ الانتشار العكسي (backward)."),
            ("Complete the analytical gradient for the bias.", "أكمل التدرّج التحليلي للانحياز (bias)."),
            ("Zero the accumulated gradient.", "صفّر التدرّج المتراكم."),
        ),
        starter='''import torch

t_u = torch.tensor([1.0, 2.0, 3.0])
t_c = torch.tensor([3.0, 5.0, 7.0])

# Step 1: parameters [w, b] that autograd should track
params = torch.tensor([1.0, 0.0], requires_grad=___)
w, b = params
t_p = w * t_u + b
loss = ((t_p - t_c) ** 2).mean()

# Step 2: let autograd fill params.grad
___
autograd_grad = params.grad.clone()

# Step 3: the analytical gradient: dL/dw = mean(2 * err * t_u), dL/db = mean(2 * err)
dloss_dtp = 2 * (t_p - t_c) / t_p.size(0)
manual_grad = torch.stack([(dloss_dtp * t_u).sum(), ___])
print(autograd_grad, manual_grad.detach())

# Step 4: gradients ACCUMULATE across backward calls - clear them before the next step
___
''',
        answers=("True", "loss.backward()", "dloss_dtp.sum()", "params.grad.zero_()"),
        alternatives={
            4: ("params.grad.data.zero_()",),
        },
        blanks=(
            ("set `requires_grad=True` so PyTorch records operations on `params`.",
             "اضبط `requires_grad=True` كي يسجّل PyTorch العمليات على `params`."),
            ("call `loss.backward()`.", "استدعِ `loss.backward()`."),
            ("the bias gradient is the sum of `dloss_dtp` (the bias multiplies 1): `dloss_dtp.sum()`.",
             "تدرّج الانحياز هو مجموع `dloss_dtp` (لأن الانحياز يُضرب في 1): `dloss_dtp.sum()`."),
            ("reset the stored gradient in place with `params.grad.zero_()`.",
             "صفّر التدرّج المخزَّن في مكانه بـ `params.grad.zero_()`."),
        ),
        hints=(
            ("Autograd only tracks tensors created with `requires_grad=True`.",
             "لا يتتبّع autograd إلا الموترات المنشأة مع `requires_grad=True`."),
            ("`backward()` is called on the scalar loss and writes into each parameter's `.grad`.",
             "يُستدعى `backward()` على الخسارة العددية ويكتب في الخاصية `.grad` لكل معامل."),
            ("The bias gradient has no `t_u` factor, and in-place methods ending in `_` such as `zero_()` modify the tensor itself.",
             "تدرّج الانحياز لا يحتوي على العامل `t_u`، والدوال المنتهية بـ `_` مثل `zero_()` تعدّل الموتر نفسه."),
        ),
        success=("Correct! Autograd matches the hand-derived gradient, and zeroing it prevents the next backward pass from adding to stale values.",
                 "صحيح! يطابق autograd التدرّج المشتق يدويًا، وتصفيره يمنع الانتشار العكسي التالي من الإضافة إلى قيم قديمة."),
        expected=TORCH_NOTE,
        reflect=("What would happen to training if you never cleared `params.grad` between steps?",
                 "ماذا سيحدث للتدريب لو لم تصفّر `params.grad` أبدًا بين الخطوات؟"),
    ),
    "COURSE-003.M05.L01.EX04": Guided(
        goal=("Swap the linear model for a quadratic one and keep the rest of the training loop unchanged.",
              "استبدل النموذج الخطي بنموذج تربيعي، واترك بقية حلقة التدريب دون تغيير."),
        steps=(
            ("State how many learnable parameters the quadratic model needs.", "حدّد عدد المعاملات القابلة للتعلّم التي يحتاجها النموذج التربيعي."),
            ("Return the quadratic prediction: `w2` times the squared input, plus `w1` times the input, plus the bias.",
             "أعد التنبؤ التربيعي: `w2` مضروبًا في مربع المُدخل، زائد `w1` مضروبًا في المُدخل، زائد الانحياز."),
            ("Complete the two reusable optimizer lines: backward, then step.", "أكمل سطري المُحسِّن القابلين لإعادة الاستخدام: backward ثم step."),
        ),
        starter='''import torch
import torch.optim as optim

t_c = torch.tensor([0.5, 14.0, 15.0, 28.0, 11.0, 8.0, 3.0, -4.0, 6.0, 13.0, 21.0])
t_u = torch.tensor([35.7, 55.9, 58.2, 81.9, 56.3, 48.9, 33.9, 21.8, 48.4, 60.4, 68.4])
t_un = 0.1 * t_u

# Step 1: how many learnable parameters does w2 * t_u**2 + w1 * t_u + b have?
n_params = ___

# Step 2: the quadratic model - the only part of the pipeline that changes
def model(t_u, w2, w1, b):
    return ___

def loss_fn(t_p, t_c):                     # unchanged
    return ((t_p - t_c) ** 2).mean()

params = torch.zeros(n_params, requires_grad=True)
optimizer = optim.Adam([params], lr=1e-2)  # unchanged

for epoch in range(5000):
    t_p = model(t_un, *params)
    loss = loss_fn(t_p, t_c)
    optimizer.zero_grad()
    # Step 3: backpropagate, then update the parameters
    ___
    ___
print(loss.item(), params)
''',
        answers=("3", "w2 * t_u ** 2 + w1 * t_u + b", "loss.backward()", "optimizer.step()"),
        alternatives={
            2: ("b + w1 * t_u + w2 * t_u ** 2", "w2 * t_u * t_u + w1 * t_u + b", "w2 * (t_u ** 2) + w1 * t_u + b"),
        },
        blanks=(
            ("w2, w1 and b are three separate learnable values.", "w2 وw1 وb ثلاث قيم مستقلة قابلة للتعلّم."),
            ("return `w2 * t_u ** 2 + w1 * t_u + b`.", "أعد `w2 * t_u ** 2 + w1 * t_u + b`."),
            ("first call `loss.backward()` to compute the gradients.", "استدعِ أولًا `loss.backward()` لحساب التدرّجات."),
            ("then call `optimizer.step()` to update the parameters.", "ثم استدعِ `optimizer.step()` لتحديث المعاملات."),
        ),
        hints=(
            ("Count the symbols the model learns, not the inputs.", "عُدّ الرموز التي يتعلّمها النموذج، لا المدخلات."),
            ("Only `model` changes; the loss function and optimizer loop stay exactly as they were.",
             "تتغير الدالة `model` فقط، وتبقى دالة الخسارة وحلقة المُحسِّن كما هي تمامًا."),
            ("Every training step is: zero the gradients, `loss.backward()`, `optimizer.step()`.",
             "كل خطوة تدريب هي: تصفير التدرّجات، ثم `loss.backward()`، ثم `optimizer.step()`."),
        ),
        success=("Correct! Only the model function changed; the loss and the optimizer loop were reused as they were.",
                 "صحيح! تغيّرت دالة النموذج فقط، وأُعيد استخدام الخسارة وحلقة المُحسِّن كما هي."),
        expected=TORCH_NOTE,
        reflect=("Why does a lower training loss not prove that the quadratic model generalizes better than the linear one?",
                 "لماذا لا تثبت الخسارة الأقل في التدريب أن النموذج التربيعي يعمّم أفضل من النموذج الخطي؟"),
    ),
    "COURSE-003.M06.L01.EX01": Guided(
        goal=("Compute tanh, sigmoid and ReLU on the same inputs and find where tanh saturates.",
              "احسب tanh وsigmoid وReLU على المدخلات نفسها، وحدّد أين تتشبّع tanh."),
        steps=(
            ("Compute tanh of `x`.", "احسب tanh للمتغير `x`."),
            ("Compute the sigmoid 1 / (1 + e^-x).", "احسب sigmoid بالصيغة 1 / (1 + e^-x)."),
            ("Compute ReLU: 0 for negative inputs, x otherwise.", "احسب ReLU: صفر للمدخلات السالبة، وx لغيرها."),
            ("Select the inputs where |tanh(x)| > 0.99.", "اختر المدخلات التي يكون عندها |tanh(x)| > 0.99."),
        ),
        starter='''import numpy as np

x = np.linspace(-5, 5, 21)     # torch.linspace(-5, 5, 21)

# Step 1: torch.tanh(x)
tanh = ___
# Step 2: torch.sigmoid(x) = 1 / (1 + exp(-x))
sigmoid = ___
# Step 3: torch.relu(x)
relu = ___

for value, a, b, c in zip(x, tanh, sigmoid, relu):
    print(f"{value:5.1f}  tanh {a:6.3f}  sigmoid {b:5.3f}  relu {c:4.1f}")

# Step 4: inputs where tanh is saturated (|tanh| > 0.99)
saturated = x[___].tolist()
print("tanh saturates at:", saturated)
''',
        answers=("np.tanh(x)", "1 / (1 + np.exp(-x))", "np.maximum(x, 0)", "np.abs(tanh) > 0.99"),
        checks=(
            check("bool(np.allclose(tanh, np.tanh(x)))", True,
                  "Blank 1: use `np.tanh(x)`.", "الفراغ 1: استخدم `np.tanh(x)`."),
            check("bool(np.allclose(sigmoid, 1 / (1 + np.exp(-x))))", True,
                  "Blank 2: the sigmoid is `1 / (1 + np.exp(-x))`.", "الفراغ 2: دالة sigmoid هي `1 / (1 + np.exp(-x))`."),
            check("bool(np.allclose(relu, np.where(x > 0, x, 0)))", True,
                  "Blank 3: ReLU keeps positive values and turns negatives into 0, e.g. `np.maximum(x, 0)`.",
                  "الفراغ 3: تحتفظ ReLU بالقيم الموجبة وتحوّل السالبة إلى 0، مثل `np.maximum(x, 0)`."),
            check("saturated == x[np.abs(np.tanh(x)) > 0.99].tolist()", True,
                  "Blank 4: build a Boolean mask `np.abs(tanh) > 0.99` and use it to index `x`.",
                  "الفراغ 4: أنشئ قناعًا منطقيًا `np.abs(tanh) > 0.99` واستخدمه لفهرسة `x`."),
        ),
        hints=(
            ("NumPy has `np.tanh` and `np.exp`; the sigmoid is built from `np.exp`.",
             "يوفّر NumPy الدالتين `np.tanh` و`np.exp`، وتُبنى sigmoid من `np.exp`."),
            ("`np.maximum(x, 0)` compares element by element.", "تقارن `np.maximum(x, 0)` عنصرًا بعنصر."),
            ("A comparison on an array gives a Boolean mask you can put inside `x[...]`.",
             "المقارنة على مصفوفة تعطي قناعًا منطقيًا يمكنك وضعه داخل `x[...]`."),
        ),
        success=("Correct! tanh and sigmoid flatten out for large |x| (saturation), while ReLU stays linear for positive inputs and is zero for negative ones.",
                 "صحيح! تتسطّح tanh وsigmoid عند قيم |x| الكبيرة (التشبّع)، بينما تبقى ReLU خطية للمدخلات الموجبة وتساوي صفرًا للسالبة."),
        expected=NUMPY_NOTE,
        reflect=("Why would a network made only of linear layers, with no activation between them, collapse into a single linear layer?",
                 "لماذا تنهار شبكة مكوّنة من طبقات خطية فقط، دون دوال تنشيط بينها، إلى طبقة خطية واحدة؟"),
    ),
    "COURSE-003.M06.L01.EX02": Guided(
        goal=("Predict the input and output shapes of linear layers for batched data.",
              "توقّع أبعاد مدخلات الطبقات الخطية ومخرجاتها لبيانات مجمّعة في دفعات."),
        steps=(
            ("Shape 32 one-feature samples as a batch.", "شكّل 32 عينة ذات خاصية واحدة بوصفها دفعة."),
            ("Predict the output shape of `Linear(1, 1)` on that batch.", "توقّع أبعاد مخرج `Linear(1, 1)` على تلك الدفعة."),
            ("Predict the output shape of `Linear(5, 2)` on 64 samples.", "توقّع أبعاد مخرج `Linear(5, 2)` على 64 عينة."),
            ("Shape one 20-feature sample as a batch of one.", "شكّل عينة واحدة ذات 20 خاصية بوصفها دفعة من عنصر واحد."),
        ),
        starter='''import numpy as np

rng = np.random.default_rng(0)

def linear(x, in_features, out_features):
    """What nn.Linear(in_features, out_features) computes: x @ weight.T + bias."""
    weight = rng.normal(size=(out_features, in_features))
    bias = np.zeros(out_features)
    return x @ weight.T + bias

# Step 1: 32 samples with ONE feature each, as a batch
x1 = np.ones(___)
# Step 2: predicted output shape of linear(x1, 1, 1)
predicted_1 = ___

# Step 3: predicted output shape of linear(x2, 5, 2) for 64 samples with 5 features
x2 = np.ones((64, 5))
predicted_2 = ___

# Step 4: ONE sample with 20 features, still with a batch dimension
x3 = np.ones(___)

print(linear(x1, 1, 1).shape, predicted_1)
print(linear(x2, 5, 2).shape, predicted_2)
print(linear(x3, 20, 10).shape)
''',
        answers=("(32, 1)", "(32, 1)", "(64, 2)", "(1, 20)"),
        checks=(
            check("list(x1.shape)", [32, 1],
                  "Blank 1: a batch of 32 one-feature samples has shape (32, 1): batch first, features last.",
                  "الفراغ 1: دفعة من 32 عينة ذات خاصية واحدة أبعادها (32, 1): الدفعة أولًا والخصائص أخيرًا."),
            check("list(predicted_1)", [32, 1],
                  "Blank 2: the batch size stays 32 and the last axis becomes `out_features` = 1.",
                  "الفراغ 2: يبقى حجم الدفعة 32 ويصبح المحور الأخير `out_features` = 1."),
            check("list(predicted_2)", [64, 2],
                  "Blank 3: 64 samples in, 64 out, each with `out_features` = 2.",
                  "الفراغ 3: تدخل 64 عينة وتخرج 64، لكل منها `out_features` = 2."),
            check("list(x3.shape)", [1, 20],
                  "Blank 4: one sample keeps a batch axis of size 1: (1, 20).",
                  "الفراغ 4: تحتفظ العينة الواحدة بمحور دفعة حجمه 1: (1, 20)."),
        ),
        hints=(
            ("Linear layers expect (batch, features); only the last axis changes.",
             "تتوقع الطبقات الخطية الأبعاد (batch, features)؛ ولا يتغير إلا المحور الأخير."),
            ("The output's last axis equals `out_features`; the batch axis passes through unchanged.",
             "المحور الأخير في المخرج يساوي `out_features`، ويمر محور الدفعة دون تغيير."),
            ("Even a single sample is passed as a batch of one: shape (1, features).",
             "حتى العينة الواحدة تُمرَّر دفعةً من عنصر واحد: الأبعاد (1, features)."),
        ),
        success=("Correct! A linear layer maps (batch, in_features) to (batch, out_features), whatever the batch size.",
                 "صحيح! تحوّل الطبقة الخطية الأبعاد (batch, in_features) إلى (batch, out_features) مهما كان حجم الدفعة."),
        expected=NUMPY_NOTE,
        reflect=("Why is (32, 1) clearer than (32,) for 32 one-feature samples?",
                 "لماذا تكون الأبعاد (32, 1) أوضح من (32,) لـ 32 عينة ذات خاصية واحدة؟"),
    ),
    "COURSE-003.M06.L01.EX03": Guided(
        goal=("Write out the parameters of `nn.Sequential(nn.Linear(2, 4), nn.Tanh(), nn.Linear(4, 1))`, count them and run a forward pass.",
              "اكتب معاملات `nn.Sequential(nn.Linear(2, 4), nn.Tanh(), nn.Linear(4, 1))`، وعُدّها، ونفّذ تمريرًا أماميًا."),
        steps=(
            ("Give the second linear layer's weight and bias their shapes.", "أعطِ وزن الطبقة الخطية الثانية وانحيازها أبعادهما."),
            ("Count all trainable scalars.", "عُدّ كل القيم المفردة القابلة للتدريب."),
            ("Finish the forward pass for a batch of 8 samples.", "أكمل التمرير الأمامي لدفعة من 8 عينات."),
        ),
        starter='''import numpy as np

# The model's parameters as PyTorch names them: weight is (out_features, in_features)
rng = np.random.default_rng(0)
params = {
    "0.weight": rng.normal(size=(4, 2)),   # nn.Linear(2, 4)
    "0.bias": np.zeros(4),
    # (index 1 is nn.Tanh(), which has no parameters)
    "2.weight": rng.normal(size=___),      # nn.Linear(4, 1)
    "2.bias": np.zeros(___),
}

# Step 2: what sum(p.numel() for p in model.parameters()) returns
total_params = ___

# Step 3: forward pass for 8 samples with 2 features
x = rng.normal(size=(8, 2))
hidden = np.tanh(x @ params["0.weight"].T + params["0.bias"])
output = ___

for name, value in params.items():
    print(f"{name:9} {value.shape}")
print("total parameters:", total_params, "| output shape:", output.shape)
''',
        answers=("(1, 4)", "1", "sum(p.size for p in params.values())",
                 'hidden @ params["2.weight"].T + params["2.bias"]'),
        checks=(
            check("list(params['2.weight'].shape)", [1, 4],
                  "Blank 1: `Linear(4, 1)` has a weight of shape (out, in) = (1, 4).",
                  "الفراغ 1: لطبقة `Linear(4, 1)` وزن بالأبعاد (out, in) = (1, 4)."),
            check("list(params['2.bias'].shape)", [1],
                  "Blank 2: there is one bias per output unit: 1.",
                  "الفراغ 2: يوجد انحياز واحد لكل وحدة إخراج: 1."),
            check("int(total_params)", 17,
                  "Blank 3: add up the sizes of every parameter array: 8 + 4 + 4 + 1.",
                  "الفراغ 3: اجمع أحجام كل مصفوفات المعاملات: 8 + 4 + 4 + 1."),
            check("list(output.shape) == [8, 1] and bool(np.allclose(output, hidden @ params['2.weight'].T + params['2.bias']))", True,
                  "Blank 4: apply the second layer to `hidden`: `hidden @ W.T + b`.",
                  "الفراغ 4: طبّق الطبقة الثانية على `hidden`: `hidden @ W.T + b`."),
        ),
        hints=(
            ("A weight is (out_features, in_features); a bias has one value per output.",
             "الوزن بالأبعاد (out_features, in_features)، وللانحياز قيمة واحدة لكل مخرج."),
            ("`.size` gives the number of values in an array; sum it over `params.values()`.",
             "تعطي `.size` عدد القيم في المصفوفة؛ اجمعها عبر `params.values()`."),
            ("The second layer works exactly like the first, but on `hidden` and without tanh.",
             "تعمل الطبقة الثانية مثل الأولى تمامًا، لكن على `hidden` ودون tanh."),
        ),
        success=("Correct! The network has 17 trainable values; Tanh adds none because it is a fixed function.",
                 "صحيح! للشبكة 17 قيمة قابلة للتدريب، ولا تضيف Tanh أي قيمة لأنها دالة ثابتة."),
        expected=NUMPY_NOTE,
    ),
    "COURSE-003.M06.L01.EX04": Guided(
        goal=("Train models of growing capacity on the thermometer data and compare training and validation error.",
              "درّب نماذج بسعة متزايدة على بيانات مقياس الحرارة، وقارن خطأ التدريب بخطأ التحقق."),
        steps=(
            ("Give the small network 2 hidden units.", "أعطِ الشبكة الصغيرة وحدتين مخفيتين."),
            ("Fit every model on the training rows only.", "درّب كل نموذج على صفوف التدريب فقط."),
            ("Compute each model's validation error.", "احسب خطأ التحقق لكل نموذج."),
        ),
        starter='''import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor

t_c = np.array([0.5, 14.0, 15.0, 28.0, 11.0, 8.0, 3.0, -4.0, 6.0, 13.0, 21.0])
t_u = np.array([35.7, 55.9, 58.2, 81.9, 56.3, 48.9, 33.9, 21.8, 48.4, 60.4, 68.4])
X = (0.1 * t_u).reshape(-1, 1)
val_idx = np.array([2, 9])
train_idx = np.setdiff1d(np.arange(len(X)), val_idx)
X_train, y_train, X_val, y_val = X[train_idx], t_c[train_idx], X[val_idx], t_c[val_idx]

# MLPRegressor(hidden_layer_sizes=(n,), activation="tanh") is Linear(1, n) -> Tanh -> Linear(n, 1)
models = {
    "Linear(1, 1)": LinearRegression(),
    # Step 1: two hidden units
    "1 -> 2 -> 1": MLPRegressor(hidden_layer_sizes=(___,), activation="tanh", solver="lbfgs", max_iter=5000, random_state=0),
    "1 -> 32 -> 1": MLPRegressor(hidden_layer_sizes=(32,), activation="tanh", solver="lbfgs", max_iter=5000, random_state=0),
}

results = {}
for name, model in models.items():
    # Step 2: fit on the training rows only
    ___
    train_mse = mean_squared_error(y_train, model.predict(X_train))
    # Step 3: error on the validation rows
    val_mse = ___
    results[name] = (round(train_mse, 2), round(val_mse, 2))
    print(f"{name:13} train {train_mse:7.2f}   validation {val_mse:7.2f}")
''',
        answers=("2", "model.fit(X_train, y_train)", "mean_squared_error(y_val, model.predict(X_val))"),
        checks=(
            check("list(models['1 -> 2 -> 1'].hidden_layer_sizes)", [2],
                  "Blank 1: the small network has 2 hidden units: `hidden_layer_sizes=(2,)`.",
                  "الفراغ 1: للشبكة الصغيرة وحدتان مخفيتان: `hidden_layer_sizes=(2,)`."),
            check("all(bool(np.allclose(type(m)(**m.get_params()).fit(X_train, y_train).predict(X_val), m.predict(X_val))) for m in models.values())", True,
                  "Blank 2: call `model.fit(X_train, y_train)` - never include the validation rows in training.",
                  "الفراغ 2: استدعِ `model.fit(X_train, y_train)` - ولا تُدخل صفوف التحقق في التدريب أبدًا."),
            check("all(abs(results[n][1] - round(mean_squared_error(y_val, m.predict(X_val)), 2)) < 1e-9 for n, m in models.items())", True,
                  "Blank 3: compare `y_val` with the model's predictions on `X_val`.",
                  "الفراغ 3: قارن `y_val` بتنبؤات النموذج على `X_val`."),
        ),
        hints=(
            ("`hidden_layer_sizes=(2,)` is one hidden layer with 2 units.", "`hidden_layer_sizes=(2,)` تعني طبقة مخفية واحدة بوحدتين."),
            ("Every scikit-learn model is trained with `.fit(X, y)`.", "يُدرَّب كل نموذج في scikit-learn بالدالة `.fit(X, y)`."),
            ("Validation error uses the same metric as training error, but on `X_val` and `y_val`.",
             "يستخدم خطأ التحقق المقياس نفسه المستخدم في خطأ التدريب، لكن على `X_val` و`y_val`."),
        ),
        success=("Correct! Compare the two columns: more hidden units lower the training error, but the validation error shows whether that capacity actually helps.",
                 "صحيح! قارن العمودين: الوحدات المخفية الإضافية تخفض خطأ التدريب، لكن خطأ التحقق يبيّن هل تساعد تلك السعة فعلًا."),
        expected=(
            "scikit-learn's `MLPRegressor` builds the same Linear → Tanh → Linear network as the lesson's PyTorch models and runs in the sandbox.",
            "يبني `MLPRegressor` في scikit-learn شبكة Linear → Tanh → Linear نفسها التي في نماذج PyTorch في الدرس، ويعمل داخل بيئة التدريب.",
        ),
        reflect=("Did greater capacity improve validation error, or mainly make the fitted curve more wiggly?",
                 "هل حسّنت السعة الأكبر خطأ التحقق، أم جعلت المنحنى الملائم أكثر تعرّجًا فقط؟"),
    ),
    "COURSE-003.M07.L01.EX01": Guided(
        goal=("Reproduce `ToTensor` and `Normalize` on a batch of 32×32 colour images.",
              "أعد إنتاج `ToTensor` و`Normalize` على دفعة من صور ملوّنة بحجم 32×32."),
        steps=(
            ("Convert images to channels-first floats in [0, 1].", "حوّل الصور إلى أعداد عشرية بترتيب القنوات أولًا وفي النطاق [0, 1]."),
            ("Compute the per-channel mean over the whole training set.", "احسب متوسط كل قناة على مجموعة التدريب كلها."),
            ("Normalize every channel with its mean and standard deviation.", "طبّع كل قناة بمتوسطها وانحرافها المعياري."),
        ),
        starter='''import numpy as np

# 100 random 32x32 RGB images stand in for CIFAR-10 (downloads are not available here)
rng = np.random.default_rng(0)
images = rng.integers(0, 256, size=(100, 32, 32, 3), dtype=np.uint8)   # N x H x W x C

# Step 1: what transforms.ToTensor() does: N x C x H x W floats in [0, 1]
tensors = ___
print("ToTensor:", tensors.shape, tensors.dtype, float(tensors.min()), float(tensors.max()))

# Step 2: per-channel statistics over images, height and width (axes 0, 2, 3)
mean = ___
std = tensors.std(axis=(0, 2, 3))

# Step 3: transforms.Normalize(mean, std) - subtract and divide per channel
normalized = ___
print("normalized range:", round(float(normalized.min()), 2), "to", round(float(normalized.max()), 2))
''',
        answers=(
            "images.transpose(0, 3, 1, 2).astype(np.float32) / 255.0",
            "tensors.mean(axis=(0, 2, 3))",
            "(tensors - mean[:, None, None]) / std[:, None, None]",
        ),
        checks=(
            check("list(tensors.shape) == [100, 3, 32, 32] and float(tensors.max()) <= 1.0 and bool(np.allclose(tensors[5, 1], images[5, :, :, 1] / 255.0))", True,
                  "Blank 1: move channels to axis 1 with `transpose(0, 3, 1, 2)`, then scale to [0, 1].",
                  "الفراغ 1: انقل القنوات إلى المحور 1 بـ `transpose(0, 3, 1, 2)`، ثم حجّم إلى [0, 1]."),
            check("bool(np.allclose(mean, images.mean(axis=(0, 1, 2)) / 255.0, atol=1e-5))", True,
                  "Blank 2: average over every axis except the channel axis: `axis=(0, 2, 3)`.",
                  "الفراغ 2: احسب المتوسط على كل المحاور ما عدا محور القنوات: `axis=(0, 2, 3)`."),
            check("bool(np.allclose(normalized.mean(axis=(0, 2, 3)), 0, atol=1e-4) and np.allclose(normalized.std(axis=(0, 2, 3)), 1, atol=1e-3))", True,
                  "Blank 3: reshape mean and std to (3, 1, 1) so they broadcast over height and width.",
                  "الفراغ 3: أعد تشكيل المتوسط والانحراف إلى (3, 1, 1) ليُبثّا على الارتفاع والعرض."),
        ),
        hints=(
            ("The raw axes are (N, H, W, C); PyTorch wants (N, C, H, W).", "المحاور الخام (N, H, W, C)، ويريد PyTorch الترتيب (N, C, H, W)."),
            ("Statistics per channel means reducing over all axes except axis 1.",
             "الإحصاءات لكل قناة تعني الاختزال على كل المحاور ما عدا المحور 1."),
            ("`mean[:, None, None]` has shape (3, 1, 1), which broadcasts against (N, 3, 32, 32).",
             "للتعبير `mean[:, None, None]` الأبعاد (3, 1, 1)، وهي تُبثّ مع (N, 3, 32, 32)."),
        ),
        success=("Correct! Each channel now has mean 0 and standard deviation 1, which is why normalized values can be below 0 or above 1.",
                 "صحيح! أصبح لكل قناة متوسط 0 وانحراف معياري 1، ولهذا قد تقل القيم المطبَّعة عن 0 أو تزيد على 1."),
        expected=NUMPY_NOTE,
    ),
    "COURSE-003.M07.L01.EX02": Guided(
        goal=("Turn logits into probabilities, predictions and a cross-entropy loss, and confirm log-softmax + NLL gives the same loss.",
              "حوّل الـ logits إلى احتمالات وتنبؤات وخسارة cross-entropy، وتأكد أن log-softmax مع NLL يعطيان الخسارة نفسها."),
        steps=(
            ("Normalize the exponentials of each row (softmax).", "طبّع الأسس في كل صف (softmax)."),
            ("Take the most likely class per sample.", "خذ الفئة الأرجح لكل عينة."),
            ("Average −log(probability of the true class).", "احسب متوسط −log(احتمال الفئة الصحيحة)."),
            ("Compute the same loss from `log_softmax`.", "احسب الخسارة نفسها من `log_softmax`."),
        ),
        starter='''import numpy as np

logits = np.array([[2.0, 0.5], [-1.0, 2.5], [0.2, 0.1]])   # 3 samples, 2 classes
targets = np.array([0, 1, 1])
rows = np.arange(len(targets))

# Step 1: softmax along each row (dim=1)
exp = np.exp(logits)
probabilities = ___

# Step 2: predicted class per sample (argmax)
predictions = ___

# Step 3: nn.CrossEntropyLoss(): mean of -log(probability of the true class)
cross_entropy = ___

# Step 4: LogSoftmax(dim=1) followed by nn.NLLLoss()
log_softmax = logits - np.log(exp.sum(axis=1, keepdims=True))
nll = ___

print(probabilities.round(3), predictions)
print("cross-entropy", round(float(cross_entropy), 4), "| log-softmax + NLL", round(float(nll), 4))
''',
        answers=(
            "exp / exp.sum(axis=1, keepdims=True)",
            "probabilities.argmax(axis=1)",
            "-np.log(probabilities[rows, targets]).mean()",
            "-log_softmax[rows, targets].mean()",
        ),
        checks=(
            check("bool(np.allclose(probabilities, np.exp(logits) / np.exp(logits).sum(axis=1, keepdims=True)))", True,
                  "Blank 1: divide each row's exponentials by that row's sum (`keepdims=True` keeps the shapes aligned).",
                  "الفراغ 1: اقسم أسس كل صف على مجموع ذلك الصف (`keepdims=True` تُبقي الأبعاد متوافقة)."),
            check("np.asarray(predictions).tolist()", [0, 1, 0],
                  "Blank 2: take `argmax` along axis 1 to get one class per sample.",
                  "الفراغ 2: خذ `argmax` على المحور 1 للحصول على فئة واحدة لكل عينة."),
            check("round(float(cross_entropy), 4)", 0.3252,
                  "Blank 3: pick each row's true-class probability with `probabilities[rows, targets]`, take -log, then the mean.",
                  "الفراغ 3: اختر احتمال الفئة الصحيحة لكل صف بـ `probabilities[rows, targets]`، ثم خذ -log، ثم المتوسط."),
            check("abs(float(nll) - float(cross_entropy)) < 1e-9", True,
                  "Blank 4: NLL takes the negative log-probability of the true class from `log_softmax` and averages it.",
                  "الفراغ 4: تأخذ NLL سالب لوغاريتم احتمال الفئة الصحيحة من `log_softmax` ثم تحسب المتوسط."),
        ),
        hints=(
            ("Softmax is exp(x) divided by the sum of exp over the classes in the same row.",
             "دالة softmax هي exp(x) مقسومة على مجموع exp لفئات الصف نفسه."),
            ("`array[rows, targets]` picks one value per row - the column given by the target.",
             "يختار `array[rows, targets]` قيمة واحدة لكل صف - العمود الذي يحدده الهدف."),
            ("log-softmax already contains the log, so NLL is just its negative at the true class, averaged.",
             "تحتوي log-softmax على اللوغاريتم أصلًا، لذا فإن NLL هي سالبها عند الفئة الصحيحة، بمتوسطها."),
        ),
        success=("Correct! CrossEntropyLoss equals LogSoftmax + NLLLoss, which is why you pass raw logits to it and never add a Softmax layer first.",
                 "صحيح! تساوي CrossEntropyLoss مجموع LogSoftmax وNLLLoss، ولهذا تمرّر إليها الـ logits الخام ولا تضيف طبقة Softmax قبلها."),
        expected=NUMPY_NOTE,
        reflect=("What goes wrong if you insert a Softmax layer before `nn.CrossEntropyLoss`?",
                 "ما الذي يفسد إذا أضفت طبقة Softmax قبل `nn.CrossEntropyLoss`؟"),
    ),
    "COURSE-003.M07.L01.EX03": Guided(
        goal=("Write one complete minibatch optimization step for a fully connected image classifier.",
              "اكتب خطوة تحسين كاملة على دفعة صغيرة لمصنّف صور متصل بالكامل."),
        steps=(
            ("Flatten each image to 3072 values while keeping the batch dimension.", "سطّح كل صورة إلى 3072 قيمة مع الحفاظ على بُعد الدفعة."),
            ("Compute the cross-entropy loss.", "احسب خسارة cross-entropy."),
            ("Backpropagate, then update the weights.", "نفّذ الانتشار العكسي ثم حدّث الأوزان."),
        ),
        starter='''import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# cifar2 is the lesson's bird-vs-airplane dataset of (3 x 32 x 32 image, label) pairs
train_loader = DataLoader(cifar2, batch_size=64, shuffle=True)
model = nn.Sequential(nn.Linear(3072, 512), nn.Tanh(), nn.Linear(512, 2))
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-2)

imgs, labels = next(iter(train_loader))
print(imgs.shape, labels.shape)          # torch.Size([64, 3, 32, 32]) torch.Size([64])

# Step 1: B x 3 x 32 x 32  ->  B x 3072 (keep the batch dimension!)
flat = ___

# Step 2: forward pass and loss
outputs = model(flat)
loss = ___

# Step 3: clear old gradients, backpropagate, update
optimizer.zero_grad()
___
___
print(loss.item())
''',
        answers=("imgs.view(imgs.shape[0], -1)", "loss_fn(outputs, labels)", "loss.backward()", "optimizer.step()"),
        alternatives={
            1: (
                "imgs.view(imgs.size(0), -1)", "imgs.reshape(imgs.shape[0], -1)", "imgs.reshape(imgs.size(0), -1)",
                "imgs.view(-1, 3072)", "imgs.reshape(-1, 3072)", "imgs.flatten(1)", "imgs.flatten(start_dim=1)",
                "torch.flatten(imgs, 1)", "torch.flatten(imgs, start_dim=1)", "imgs.view(len(imgs), -1)",
            ),
        },
        blanks=(
            ("flatten everything except axis 0, e.g. `imgs.view(imgs.shape[0], -1)`.",
             "سطّح كل شيء ما عدا المحور 0، مثل `imgs.view(imgs.shape[0], -1)`."),
            ("call `loss_fn(outputs, labels)` with the raw outputs (logits).",
             "استدعِ `loss_fn(outputs, labels)` مع المخرجات الخام (logits)."),
            ("call `loss.backward()` to compute the gradients.", "استدعِ `loss.backward()` لحساب التدرّجات."),
            ("call `optimizer.step()` to apply the update.", "استدعِ `optimizer.step()` لتطبيق التحديث."),
        ),
        hints=(
            ("`-1` lets PyTorch infer one dimension; keep the first dimension equal to the batch size.",
             "تسمح `-1` لـ PyTorch باستنتاج بُعد واحد؛ أبقِ البُعد الأول مساويًا لحجم الدفعة."),
            ("The loss function takes the model outputs and the true labels.", "تأخذ دالة الخسارة مخرجات النموذج والتسميات الصحيحة."),
            ("After `zero_grad()` comes `backward()` on the loss, then `step()` on the optimizer.",
             "بعد `zero_grad()` يأتي `backward()` على الخسارة، ثم `step()` على المُحسِّن."),
        ),
        success=("Correct! That is one full optimization step: flatten, forward, loss, zero_grad, backward, step.",
                 "صحيح! هذه خطوة تحسين كاملة: التسطيح، ثم التمرير الأمامي، ثم الخسارة، ثم zero_grad، ثم backward، ثم step."),
        expected=TORCH_NOTE,
        reflect=("What would go wrong if you flattened the whole batch into a single vector?",
                 "ما الخطأ الذي سيحدث لو سطّحت الدفعة كلها في متجه واحد؟"),
    ),
    "COURSE-003.M07.L01.EX04": Guided(
        goal=("Count how many parameters dense layers need for images, and compare with a convolution.",
              "احسب عدد المعاملات التي تحتاجها الطبقات الكثيفة للصور، وقارنه بطبقة التفاف."),
        steps=(
            ("Count `nn.Linear(3072, 512)` (weights + biases).", "احسب معاملات `nn.Linear(3072, 512)` (الأوزان + الانحيازات)."),
            ("Count `nn.Linear(3072, 1024)`.", "احسب معاملات `nn.Linear(3072, 1024)`."),
            ("Count the weights connecting a 1024×1024 RGB image to 1024 hidden units.", "احسب الأوزان التي تربط صورة RGB بحجم 1024×1024 بـ 1024 وحدة مخفية."),
            ("Count a 3→16-channel 3×3 convolution (weights + biases).", "احسب معاملات التفاف 3×3 من 3 قنوات إلى 16 (الأوزان + الانحيازات)."),
        ),
        starter='''# A Linear(in, out) layer has in * out weights plus out biases.

# Step 1: nn.Linear(3072, 512)
linear_512 = ___

# Step 2: nn.Linear(3072, 1024)
linear_1024 = ___

# Step 3: a 1024 x 1024 RGB image connected to 1024 hidden units (weights only)
big_image_weights = ___

# Step 4: nn.Conv2d(3, 16, kernel_size=3): 16 filters of size 3 x 3 x 3, plus 16 biases,
# reused at every image position
conv_3x3 = ___

print(f"{linear_512:,} | {linear_1024:,} | {big_image_weights:,} | {conv_3x3:,}")
''',
        answers=("3072 * 512 + 512", "3072 * 1024 + 1024", "1024 * 1024 * 3 * 1024", "16 * 3 * 3 * 3 + 16"),
        checks=(
            check("linear_512", 1573376, "Blank 1: 3072 × 512 weights plus 512 biases.", "الفراغ 1: 3072 × 512 وزنًا زائد 512 انحيازًا."),
            check("linear_1024", 3146752, "Blank 2: 3072 × 1024 weights plus 1024 biases.", "الفراغ 2: 3072 × 1024 وزنًا زائد 1024 انحيازًا."),
            check("big_image_weights", 3221225472,
                  "Blank 3: the input has 1024 × 1024 × 3 values, each connected to 1024 units.",
                  "الفراغ 3: للمدخل 1024 × 1024 × 3 قيمة، كل منها متصلة بـ 1024 وحدة."),
            check("conv_3x3", 448,
                  "Blank 4: 16 filters × (3 channels × 3 × 3) weights, plus 16 biases.",
                  "الفراغ 4: 16 مرشحًا × (3 قنوات × 3 × 3) وزنًا، زائد 16 انحيازًا."),
        ),
        hints=(
            ("Weights = inputs × outputs; add one bias per output.", "الأوزان = المدخلات × المخرجات، ثم أضف انحيازًا واحدًا لكل مخرج."),
            ("A 1024 × 1024 RGB image flattens to 1024 · 1024 · 3 inputs.", "تتسطّح صورة RGB بحجم 1024 × 1024 إلى 1024 · 1024 · 3 مدخلًا."),
            ("A convolution's size depends only on channels and kernel size, not on the image size.",
             "يعتمد حجم الالتفاف على القنوات وحجم النواة فقط، لا على حجم الصورة."),
        ),
        success=("Correct! Dense layers grow with every pixel - over 3 billion weights for one large image - while the convolution needs 448 parameters at any image size.",
                 "صحيح! تكبر الطبقات الكثيفة مع كل بكسل - أكثر من 3 مليارات وزن لصورة كبيرة واحدة - بينما يحتاج الالتفاف 448 معاملًا مهما كان حجم الصورة."),
        reflect=("Why does shifting an object by a few pixels change which flattened inputs are active, and how do random crops help?",
                 "لماذا تؤدي إزاحة جسم ببضعة بكسلات إلى تغيير المدخلات المسطّحة النشطة؟ وكيف تساعد القصاصات العشوائية؟"),
    ),
    "COURSE-003.M08.L01.EX01": Guided(
        goal=("Predict a convolution's weight shape, parameter count and output size before building it.",
              "توقّع أبعاد أوزان الالتفاف وعدد معاملاته وحجم مخرجه قبل بنائه."),
        steps=(
            ("Write the output-size formula for one spatial dimension.", "اكتب صيغة حجم المخرج لبُعد مكاني واحد."),
            ("Write the weight shape of `nn.Conv2d(3, 16, kernel_size=3)`.", "اكتب أبعاد أوزان `nn.Conv2d(3, 16, kernel_size=3)`."),
            ("Count the trainable parameters.", "احسب المعاملات القابلة للتدريب."),
            ("Give the output shape with `padding=0`.", "اكتب أبعاد المخرج عند `padding=0`."),
        ),
        starter='''# nn.Conv2d(3, 16, kernel_size=3, padding=1) applied to a batch of shape (64, 3, 32, 32)
in_channels, out_channels, kernel_size = 3, 16, 3

# Step 1: output size along one spatial axis
def conv_output_size(size, kernel_size, padding, stride=1):
    return ___

# Step 2: weight shape (out_channels, in_channels, kernel_height, kernel_width)
weight_shape = ___
bias_shape = (out_channels,)

# Step 3: trainable parameters (weights + biases)
param_count = ___

output_shape_pad1 = (64, out_channels, conv_output_size(32, 3, 1), conv_output_size(32, 3, 1))
# Step 4: the same layer with padding=0
output_shape_pad0 = ___

print(weight_shape, bias_shape, param_count)
print(output_shape_pad1, output_shape_pad0)
print("nn.Linear(3072, 512) for comparison:", 3072 * 512 + 512)
''',
        answers=(
            "(size + 2 * padding - kernel_size) // stride + 1",
            "(out_channels, in_channels, kernel_size, kernel_size)",
            "out_channels * in_channels * kernel_size * kernel_size + out_channels",
            "(64, out_channels, conv_output_size(32, 3, 0), conv_output_size(32, 3, 0))",
        ),
        checks=(
            check("[conv_output_size(32, 3, 1), conv_output_size(32, 3, 0), conv_output_size(28, 5, 0, 2)]", [32, 30, 12],
                  "Blank 1: output = (size + 2·padding − kernel) // stride + 1.",
                  "الفراغ 1: المخرج = (الحجم + 2·الحشو − النواة) // الخطوة + 1."),
            check("list(weight_shape)", [16, 3, 3, 3],
                  "Blank 2: Conv2d weights are (out_channels, in_channels, k, k) = (16, 3, 3, 3).",
                  "الفراغ 2: أوزان Conv2d بالأبعاد (out_channels, in_channels, k, k) = (16, 3, 3, 3)."),
            check("param_count", 448,
                  "Blank 3: 16 × 3 × 3 × 3 weights plus 16 biases = 448.",
                  "الفراغ 3: 16 × 3 × 3 × 3 وزنًا زائد 16 انحيازًا = 448."),
            check("list(output_shape_pad0)", [64, 16, 30, 30],
                  "Blank 4: without padding a 3×3 kernel trims one pixel from each side: 32 → 30.",
                  "الفراغ 4: دون حشو تقتطع النواة 3×3 بكسلًا من كل جانب: 32 ← 30."),
        ),
        hints=(
            ("Padding adds pixels on both sides; the kernel then fits (size + 2·padding − kernel) // stride + 1 times.",
             "يضيف الحشو بكسلات على الجانبين، ثم تتسع النواة (الحجم + 2·الحشو − النواة) // الخطوة + 1 مرة."),
            ("Each of the 16 filters looks at all 3 input channels through a 3×3 window.",
             "ينظر كل مرشح من المرشحات الـ16 إلى القنوات الثلاث كلها عبر نافذة 3×3."),
            ("The output keeps the batch size and has `out_channels` channels.", "يحافظ المخرج على حجم الدفعة ويحتوي على `out_channels` قناة."),
        ),
        success=("Correct! The convolution needs 448 parameters, against about 1.57 million for `nn.Linear(3072, 512)`, because the same small filters are reused at every position.",
                 "صحيح! يحتاج الالتفاف إلى 448 معاملًا مقابل نحو 1.57 مليون لـ `nn.Linear(3072, 512)`، لأن المرشحات الصغيرة نفسها تُعاد في كل موضع."),
    ),
    "COURSE-003.M08.L01.EX02": Guided(
        goal=("Complete the lesson's baseline CNN and keep every tensor shape consistent through the forward pass.",
              "أكمل شبكة CNN الأساسية في الدرس، وحافظ على اتساق أبعاد كل موتر عبر التمرير الأمامي."),
        steps=(
            ("Give `fc1` the number of flattened features after two poolings.", "أعطِ `fc1` عدد الخصائص المسطّحة بعد عمليتي تجميع (pooling)."),
            ("Apply conv2, tanh and max-pooling.", "طبّق conv2 ثم tanh ثم max-pooling."),
            ("Flatten to B × 512.", "سطّح إلى B × 512."),
            ("Return the output of `fc2`.", "أعد مخرج `fc2`."),
        ),
        starter='''import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 8, kernel_size=3, padding=1)
        # Step 1: features after two 2x2 poolings of a 32x32 input: 8 channels x 8 x 8
        self.fc1 = nn.Linear(___, 32)
        self.fc2 = nn.Linear(32, 2)

    def forward(self, x):                                     # x: (B, 3, 32, 32)
        out = F.max_pool2d(torch.tanh(self.conv1(x)), 2)      # (B, 16, 16, 16)
        # Step 2: conv2 -> tanh -> 2x2 max-pool                # (B, 8, 8, 8)
        out = ___
        # Step 3: flatten, keeping the batch dimension         # (B, 512)
        out = ___
        out = torch.tanh(self.fc1(out))                       # (B, 32)
        # Step 4: the final layer                              # (B, 2)
        return ___

model = Net()
print(model(torch.ones(4, 3, 32, 32)).shape)   # torch.Size([4, 2])
''',
        answers=("8 * 8 * 8", "F.max_pool2d(torch.tanh(self.conv2(out)), 2)", "out.view(-1, 8 * 8 * 8)", "self.fc2(out)"),
        alternatives={
            1: ("512",),
            3: (
                "out.view(-1, 512)", "out.view(out.shape[0], -1)", "out.view(out.size(0), -1)",
                "out.reshape(-1, 512)", "out.reshape(-1, 8 * 8 * 8)", "out.reshape(out.shape[0], -1)",
                "out.flatten(1)", "torch.flatten(out, 1)", "out.flatten(start_dim=1)",
            ),
        },
        blanks=(
            ("after two poolings the 32×32 maps are 8×8, with 8 channels: 8 * 8 * 8 = 512.",
             "بعد عمليتي تجميع تصبح الخرائط 32×32 بحجم 8×8 مع 8 قنوات: 8 * 8 * 8 = 512."),
            ("mirror the conv1 line: `F.max_pool2d(torch.tanh(self.conv2(out)), 2)`.",
             "حاكِ سطر conv1: `F.max_pool2d(torch.tanh(self.conv2(out)), 2)`."),
            ("flatten everything except the batch axis, e.g. `out.view(-1, 8 * 8 * 8)`.",
             "سطّح كل شيء ما عدا محور الدفعة، مثل `out.view(-1, 8 * 8 * 8)`."),
            ("return `self.fc2(out)`.", "أعد `self.fc2(out)`."),
        ),
        hints=(
            ("Each 2×2 max-pool halves height and width: 32 → 16 → 8.", "كل max-pool بحجم 2×2 ينصّف الارتفاع والعرض: 32 ← 16 ← 8."),
            ("The second block repeats the first one with `self.conv2`.", "تكرّر الكتلة الثانية الأولى باستخدام `self.conv2`."),
            ("A linear layer needs (B, features); `view(-1, 512)` produces exactly that.", "تحتاج الطبقة الخطية الأبعاد (B, features)، ويُنتج `view(-1, 512)` ذلك تمامًا."),
        ),
        success=("Correct! The shapes flow (B,3,32,32) → (B,16,16,16) → (B,8,8,8) → (B,512) → (B,32) → (B,2).",
                 "صحيح! تتدفق الأبعاد (B,3,32,32) ← (B,16,16,16) ← (B,8,8,8) ← (B,512) ← (B,32) ← (B,2)."),
        expected=TORCH_NOTE,
        reflect=("What error would you get without the flattening step, and why does `fc1` need a B × 512 tensor?",
                 "ما الخطأ الذي ستحصل عليه دون خطوة التسطيح؟ ولماذا تحتاج `fc1` إلى موتر B × 512؟"),
    ),
    "COURSE-003.M08.L01.EX03": Guided(
        goal=("Switch a model between training and evaluation mode and run inference without recording gradients.",
              "بدّل النموذج بين وضع التدريب ووضع التقييم، ونفّذ الاستدلال دون تسجيل التدرّجات."),
        steps=(
            ("Put the model in training mode.", "ضع النموذج في وضع التدريب."),
            ("Put the model in evaluation mode.", "ضع النموذج في وضع التقييم."),
            ("Wrap inference in a context that disables autograd.", "ضع الاستدلال داخل سياق يعطّل autograd."),
        ),
        starter='''import torch
import torch.nn as nn

model = nn.Sequential(nn.Linear(4, 4), nn.BatchNorm1d(4), nn.Dropout(p=0.5))
x = torch.randn(8, 4)

# Step 1: training mode - dropout is random, batch norm updates its running statistics
___
before = model[1].running_mean.clone()
out_a, out_b = model(x), model(x)
print("train: same output twice?", torch.equal(out_a, out_b))
print("running mean changed?", not torch.equal(before, model[1].running_mean))

# Step 2: evaluation mode - dropout is off, batch norm uses the stored statistics
___

# Step 3: no computation graph is recorded during pure inference
with ___:
    out_c, out_d = model(x), model(x)
print("eval: same output twice?", torch.equal(out_c, out_d))
''',
        answers=("model.train()", "model.eval()", "torch.no_grad()"),
        alternatives={2: ("model.train(False)",), 3: ("torch.inference_mode()",)},
        blanks=(
            ("call `model.train()`.", "استدعِ `model.train()`."),
            ("call `model.eval()`.", "استدعِ `model.eval()`."),
            ("use `torch.no_grad()` so no gradients are tracked.", "استخدم `torch.no_grad()` كي لا تُتتبَّع التدرّجات."),
        ),
        hints=(
            ("The mode is a method on the model itself.", "الوضع دالة على النموذج نفسه."),
            ("`model.eval()` changes how Dropout and BatchNorm behave; it does not turn off autograd.",
             "يغيّر `model.eval()` سلوك Dropout وBatchNorm، لكنه لا يعطّل autograd."),
            ("Turning off gradient tracking is a separate tool: the `torch.no_grad()` context manager.",
             "تعطيل تتبّع التدرّجات أداة منفصلة: مدير السياق `torch.no_grad()`."),
        ),
        success=("Correct! `model.eval()` changes layer behaviour (no dropout, stored batch-norm statistics), while `torch.no_grad()` separately stops autograd from recording.",
                 "صحيح! يغيّر `model.eval()` سلوك الطبقات (لا Dropout، وإحصاءات BatchNorm المخزّنة)، بينما يوقف `torch.no_grad()` بشكل منفصل تسجيل autograd."),
        expected=TORCH_NOTE,
        reflect=("In one sentence each: what does `model.eval()` change, and what does `torch.no_grad()` change?",
                 "في جملة واحدة لكل منهما: ماذا يغيّر `model.eval()`؟ وماذا يغيّر `torch.no_grad()`؟"),
    ),
    "COURSE-003.M08.L01.EX04": Guided(
        goal=("Build a residual block whose output can be added to its input, stack five of them and confirm gradients reach the first block.",
              "ابنِ كتلة متبقية (residual) يمكن جمع مخرجها مع مدخلها، ثم كدّس خمسًا منها وتأكد أن التدرّجات تصل إلى الكتلة الأولى."),
        steps=(
            ("Give BatchNorm the number of channels.", "أعطِ BatchNorm عدد القنوات."),
            ("Return the block output plus the identity skip connection.", "أعد مخرج الكتلة مضافًا إليه وصلة التخطي (identity)."),
            ("Backpropagate a scalar loss through the stack.", "مرّر خسارة عددية عكسيًا عبر الكتل المكدّسة."),
        ),
        starter='''import torch
import torch.nn as nn

class ResBlock(nn.Module):
    def __init__(self, n_chans):
        super().__init__()
        self.conv = nn.Conv2d(n_chans, n_chans, kernel_size=3, padding=1, bias=False)
        # Step 1: one normalization per channel
        self.batch_norm = nn.BatchNorm2d(___)

    def forward(self, x):
        out = torch.relu(self.batch_norm(self.conv(x)))
        # Step 2: the identity skip connection - shapes must match for the addition
        return ___

x = torch.randn(8, 16, 20, 20)
print(ResBlock(16)(x).shape)                  # torch.Size([8, 16, 20, 20])

stack = nn.Sequential(*[ResBlock(16) for _ in range(5)])
loss = stack(x).sum()
# Step 3: backpropagate through all five blocks
___
print(stack[0].conv.weight.grad is not None)  # True: the first block receives gradients
''',
        answers=("n_chans", "out + x", "loss.backward()"),
        alternatives={2: ("x + out",)},
        blanks=(
            ("BatchNorm2d needs the channel count: `n_chans`.", "تحتاج BatchNorm2d إلى عدد القنوات: `n_chans`."),
            ("add the input back: `out + x`.", "أضف المدخل مرة أخرى: `out + x`."),
            ("call `loss.backward()`.", "استدعِ `loss.backward()`."),
        ),
        hints=(
            ("BatchNorm needs the number of channels it normalizes - the block keeps the same count it was built with.", "تحتاج BatchNorm إلى عدد القنوات التي تطبّعها، والكتلة تحافظ على العدد نفسه الذي بُنيت به."),
            ("A residual block returns its computed output plus its unchanged input.", "تعيد الكتلة المتبقية مخرجها المحسوب مضافًا إليه مدخلها دون تغيير."),
            ("Gradients are computed by calling `backward()` on the scalar loss.", "تُحسب التدرّجات باستدعاء `backward()` على الخسارة العددية."),
        ),
        success=("Correct! Padding 1 keeps the shape, so `out + x` is valid, and the skip path lets gradients reach the first block directly.",
                 "صحيح! يحافظ الحشو 1 على الأبعاد فيصبح `out + x` صالحًا، ويتيح مسار التخطي وصول التدرّجات إلى الكتلة الأولى مباشرة."),
        expected=TORCH_NOTE,
        reflect=("Why must the block's input and output have exactly the same shape?",
                 "لماذا يجب أن يتطابق مدخل الكتلة ومخرجها في الأبعاد تمامًا؟"),
    ),
    "COURSE-003.M08.L01.EX05": Guided(
        goal=("Compare 3×3 and 5×5 kernels by parameter count, and see why a confident softmax does not mean the input belongs to a known class.",
              "قارن النواتين 3×3 و5×5 بعدد المعاملات، وافهم لماذا لا تعني الثقة العالية في softmax أن المدخل ينتمي إلى فئة معروفة."),
        steps=(
            ("Count the parameters of the same two layers with 5×5 kernels.", "احسب معاملات الطبقتين نفسيهما بنواة 5×5."),
            ("Choose the padding that keeps 32×32 maps for a 5×5 kernel.", "اختر الحشو الذي يحافظ على خرائط 32×32 مع نواة 5×5."),
            ("Turn the out-of-distribution logits into probabilities.", "حوّل الـ logits لمدخل من خارج التوزيع إلى احتمالات."),
        ),
        starter='''import numpy as np

def conv_params(in_ch, out_ch, k):
    return in_ch * out_ch * k * k + out_ch

# Baseline: conv1 3 -> 16 and conv2 16 -> 8, both 3x3
params_3x3 = conv_params(3, 16, 3) + conv_params(16, 8, 3)

# Step 1: the same two layers with 5x5 kernels
params_5x5 = ___

# Step 2: padding that keeps a 32x32 map the same size for a 5x5 kernel (stride 1)
padding_5x5 = ___

# Step 3: a bird-vs-airplane model is shown a photo of a cat and outputs these logits
logits = np.array([3.1, -1.4])
probabilities = ___
confidence = float(probabilities.max())

print("parameters:", params_3x3, "->", params_5x5)
print("softmax on a cat photo:", probabilities.round(3), "confidence", round(confidence, 3))
''',
        answers=("conv_params(3, 16, 5) + conv_params(16, 8, 5)", "2", "np.exp(logits) / np.exp(logits).sum()"),
        checks=(
            check("params_5x5", 4424, "Blank 1: call `conv_params` for both layers with k=5 and add them.",
                  "الفراغ 1: استدعِ `conv_params` للطبقتين مع k=5 واجمع النتيجتين."),
            check("padding_5x5", 2, "Blank 2: (32 + 2·p − 5) + 1 = 32 when p = 2.", "الفراغ 2: (32 + 2·p − 5) + 1 = 32 عندما p = 2."),
            check("bool(np.allclose(probabilities, np.exp(logits) / np.exp(logits).sum()))", True,
                  "Blank 3: softmax is `np.exp(logits) / np.exp(logits).sum()`.",
                  "الفراغ 3: دالة softmax هي `np.exp(logits) / np.exp(logits).sum()`."),
        ),
        hints=(
            ("Reuse `conv_params` with the same channels and `k=5`.", "أعد استخدام `conv_params` بالقنوات نفسها مع `k=5`."),
            ("For stride 1, 'same' padding is (kernel − 1) / 2.", "مع خطوة 1، يكون الحشو المحافظ على الحجم (النواة − 1) / 2."),
            ("Softmax always sums to 1 over the known classes - even for a cat.", "مجموع softmax دائمًا 1 على الفئات المعروفة - حتى لصورة قطة."),
        ),
        success=("Correct! 5×5 kernels need almost three times the parameters, and the model is about 99% 'sure' a cat is a bird or an airplane because softmax must choose among the classes it knows.",
                 "صحيح! تحتاج النواة 5×5 إلى نحو ثلاثة أضعاف المعاملات، والنموذج «واثق» بنحو 99% أن القطة طائر أو طائرة لأن softmax مضطرة للاختيار بين الفئات التي تعرفها."),
        reflect=("Why does a high softmax probability not prove that an image belongs to one of the training classes?",
                 "لماذا لا يثبت الاحتمال العالي في softmax أن الصورة تنتمي إلى إحدى فئات التدريب؟"),
    ),
    "COURSE-003.M09.L01.EX01": Guided(
        goal=("Turn a list of names into padded next-character inputs and targets for self-supervised training.",
              "حوّل قائمة أسماء إلى مدخلات وأهداف للحرف التالي مع حشو، لتدريب ذاتي الإشراف."),
        steps=(
            ("Encode each name with a boundary id 0 at both ends.", "رمّز كل اسم مع المعرّف الحدّي 0 في طرفيه."),
            ("Shift by one to build the targets.", "أزِح بمقدار موضع واحد لبناء الأهداف."),
            ("Pad the targets with -1, the value the loss ignores.", "احشُ الأهداف بالقيمة -1 التي تتجاهلها دالة الخسارة."),
            ("Count the positions that contribute to the loss.", "عُدّ المواضع التي تساهم في الخسارة."),
        ),
        starter='''import numpy as np

names = ["ada", "mona", "ali"]
chars = sorted(set("".join(names)))
stoi = {ch: i + 1 for i, ch in enumerate(chars)}
stoi["."] = 0                       # boundary token: start, end and input padding

# Step 1: ".ada." -> [0, a, d, a, 0]
encoded = [___ for name in names]

# Step 2: the model reads ids[:-1] and must predict the NEXT id at every position
inputs = [ids[:-1] for ids in encoded]
targets = [___ for ids in encoded]

# Step 3: pad to the longest sequence: inputs with 0, targets with -1 (ignore_index=-1)
max_len = max(len(seq) for seq in inputs)
X = np.array([seq + [0] * (max_len - len(seq)) for seq in inputs])
Y = np.array([___ for seq in targets])

# Step 4: positions that count in cross_entropy(..., ignore_index=-1)
counted_positions = ___

print(X)
print(Y)
print("positions in the loss:", counted_positions)
''',
        answers=(
            "[0] + [stoi[ch] for ch in name] + [0]",
            "ids[1:]",
            "seq + [-1] * (max_len - len(seq))",
            "int((Y != -1).sum())",
        ),
        checks=(
            check("encoded", [[0, 1, 2, 1, 0], [0, 5, 7, 6, 1, 0], [0, 1, 4, 3, 0]],
                  "Blank 1: wrap the character ids in a 0 on each side: `[0] + [stoi[ch] for ch in name] + [0]`.",
                  "الفراغ 1: أحِط معرّفات الحروف بالصفر من الجانبين: `[0] + [stoi[ch] for ch in name] + [0]`."),
            check("[list(t) for t in targets]", [[1, 2, 1, 0], [5, 7, 6, 1, 0], [1, 4, 3, 0]],
                  "Blank 2: the target at each position is the next id: `ids[1:]`.",
                  "الفراغ 2: الهدف في كل موضع هو المعرّف التالي: `ids[1:]`."),
            check("Y.tolist()", [[1, 2, 1, 0, -1], [5, 7, 6, 1, 0], [1, 4, 3, 0, -1]],
                  "Blank 3: pad targets with -1, not 0 - 0 is a real token the model should learn to predict.",
                  "الفراغ 3: احشُ الأهداف بـ -1 لا بـ 0 - فالصفر رمز حقيقي يجب أن يتعلّم النموذج توقّعه."),
            check("int(counted_positions)", 13,
                  "Blank 4: count the target entries that are not -1.", "الفراغ 4: عُدّ عناصر الأهداف التي لا تساوي -1."),
        ),
        hints=(
            ("Build the id list from three parts: [0], the character ids, and [0].", "ابنِ قائمة المعرّفات من ثلاثة أجزاء: [0]، ومعرّفات الحروف، و[0]."),
            ("Inputs drop the last id and targets drop the first, so they line up one step apart.",
             "تحذف المدخلات المعرّف الأخير وتحذف الأهداف الأول، فيتحاذيان بفارق خطوة واحدة."),
            ("A Boolean comparison such as `Y != -1` can be summed to count the True values.",
             "يمكن جمع مقارنة منطقية مثل `Y != -1` لعدّ القيم True."),
        ),
        success=("Correct! The text supplies its own labels: every real next character is a target, and padded positions are ignored by the loss.",
                 "صحيح! يوفّر النص تسمياته بنفسه: كل حرف تالٍ حقيقي هدف، والمواضع المحشوة تتجاهلها دالة الخسارة."),
        reflect=("In PyTorch you would pass `ignore_index=-1` to `F.cross_entropy`. Why is padding the targets with 0 instead a bug?",
                 "في PyTorch تمرّر `ignore_index=-1` إلى `F.cross_entropy`. لماذا يُعدّ حشو الأهداف بالصفر بدلًا من ذلك خطأً؟"),
    ),
    "COURSE-003.M09.L01.EX02": Guided(
        goal=("Implement causal scaled dot-product self-attention by hand and check its properties.",
              "نفّذ الانتباه الذاتي السببي بالضرب النقطي المُحجَّم يدويًا وتحقّق من خصائصه."),
        steps=(
            ("Compute the scaled scores Q·Kᵀ / √d_k.", "احسب الدرجات المحجّمة Q·Kᵀ / √d_k."),
            ("Build the lower-triangular causal mask.", "ابنِ القناع السببي المثلثي السفلي."),
            ("Normalize each row with softmax.", "طبّع كل صف بـ softmax."),
            ("Multiply the weights by V.", "اضرب الأوزان في V."),
        ),
        starter='''import numpy as np

rng = np.random.default_rng(0)
T, d_k = 4, 8                                   # 4 tokens, 8 features
x = rng.normal(size=(T, d_k))
W_q, W_k, W_v = (rng.normal(size=(d_k, d_k)) for _ in range(3))
Q, K, V = x @ W_q, x @ W_k, x @ W_v

# Step 1: scaled scores (torch: Q @ K.transpose(-2, -1) / math.sqrt(d_k))
scores = ___

# Step 2: position t may attend only to positions <= t
mask = ___
scores = np.where(mask, scores, -np.inf)

# Step 3: softmax along the last axis (subtracting the max keeps exp stable)
weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
weights = ___

# Step 4: weighted sum of the values
output = ___

print(weights.round(2))
print("rows sum to 1:", np.allclose(weights.sum(axis=-1), 1), "| output", output.shape)
''',
        answers=("Q @ K.T / np.sqrt(d_k)", "np.tril(np.ones((T, T), dtype=bool))",
                 "weights / weights.sum(axis=-1, keepdims=True)", "weights @ V"),
        checks=(
            check("bool(np.allclose(np.triu(np.nan_to_num(weights), 1), 0))", True,
                  "Blank 2: the mask must be lower-triangular (`np.tril`) so no token sees the future.",
                  "الفراغ 2: يجب أن يكون القناع مثلثيًا سفليًا (`np.tril`) كي لا يرى أي رمز المستقبل."),
            check("bool(np.allclose(weights.sum(axis=-1), 1))", True,
                  "Blank 3: divide each row by its own sum (`keepdims=True`).",
                  "الفراغ 3: اقسم كل صف على مجموعه (`keepdims=True`)."),
            check("bool(np.allclose(weights, " + ATTENTION_REFERENCE + "))", True,
                  "Blank 1: scale the scores by `np.sqrt(d_k)`: `Q @ K.T / np.sqrt(d_k)`.",
                  "الفراغ 1: حجّم الدرجات بـ `np.sqrt(d_k)`: `Q @ K.T / np.sqrt(d_k)`."),
            check("bool(np.allclose(output, " + ATTENTION_REFERENCE + " @ V))", True,
                  "Blank 4: the output is the attention weights times the values: `weights @ V`.",
                  "الفراغ 4: المخرج هو أوزان الانتباه مضروبة في القيم: `weights @ V`."),
        ),
        hints=(
            ("For 2D arrays, `K.T` is the transpose; divide by the square root of the key size.",
             "في المصفوفات ثنائية الأبعاد يكون `K.T` هو المنقول؛ اقسم على الجذر التربيعي لحجم المفتاح."),
            ("`np.tril(np.ones((T, T), dtype=bool))` is True on and below the diagonal.",
             "تكون `np.tril(np.ones((T, T), dtype=bool))` صحيحة على القطر وأسفله."),
            ("After normalizing, each row is a probability distribution over the allowed positions; `@ V` mixes the values.",
             "بعد التطبيع يصبح كل صف توزيعًا احتماليًا على المواضع المسموح بها، ويمزج `@ V` القيم."),
        ),
        success=("Correct! Each row sums to 1, the upper triangle is zero, and your result matches what `F.scaled_dot_product_attention(..., is_causal=True)` computes.",
                 "صحيح! مجموع كل صف 1، والمثلث العلوي صفر، ونتيجتك تطابق ما تحسبه `F.scaled_dot_product_attention(..., is_causal=True)`."),
        expected=NUMPY_NOTE,
    ),
    "COURSE-003.M09.L01.EX03": Guided(
        goal=("Follow the tensor shapes through a multi-head attention block, from splitting heads to the residual LayerNorm.",
              "تتبّع أبعاد الموترات عبر كتلة انتباه متعدد الرؤوس، من تقسيم الرؤوس حتى LayerNorm مع الوصلة المتبقية."),
        steps=(
            ("Compute the size of each head.", "احسب حجم كل رأس."),
            ("Split (B, T, D) into (B, H, T, D_head).", "قسّم (B, T, D) إلى (B, H, T, D_head)."),
            ("Merge the heads back to (B, T, D).", "ادمج الرؤوس مرة أخرى إلى (B, T, D)."),
            ("Apply the residual addition and LayerNorm.", "طبّق الجمع المتبقي (residual) ثم LayerNorm."),
        ),
        starter='''import numpy as np

rng = np.random.default_rng(0)
B, T, D, H = 2, 6, 32, 4
x = rng.normal(size=(B, T, D))
q = x @ rng.normal(size=(D, D)) / np.sqrt(D)     # one projection is enough to follow the shapes

# Step 1: features per head
D_head = ___

# Step 2: (B, T, D) -> (B, T, H, D_head) -> (B, H, T, D_head)
q_heads = ___

# attention inside every head (keys and values reuse q to keep the example short)
scores = q_heads @ q_heads.transpose(0, 1, 3, 2) / np.sqrt(D_head)
scores = np.where(np.tril(np.ones((T, T), dtype=bool)), scores, -np.inf)
weights = np.exp(scores - scores.max(-1, keepdims=True))
weights = weights / weights.sum(-1, keepdims=True)
head_out = weights @ q_heads                          # (B, H, T, D_head)

# Step 3: merge the heads back to (B, T, D)
merged = ___

def layer_norm(z):
    return (z - z.mean(-1, keepdims=True)) / np.sqrt(z.var(-1, keepdims=True) + 1e-5)

# Step 4: residual connection, then LayerNorm
y = ___

print("D_head", D_head, "| heads", q_heads.shape, "| merged", merged.shape, "| out", y.shape)
''',
        answers=("D // H", "q.reshape(B, T, H, D_head).transpose(0, 2, 1, 3)",
                 "head_out.transpose(0, 2, 1, 3).reshape(B, T, D)", "layer_norm(x + merged)"),
        checks=(
            check("int(D_head)", 8, "Blank 1: split D = 32 evenly across H = 4 heads.", "الفراغ 1: قسّم D = 32 بالتساوي على H = 4 رؤوس."),
            check("list(q_heads.shape) == [2, 4, 6, 8] and bool(np.allclose(q_heads[1, 2, 3], q[1, 3, 16:24]))", True,
                  "Blank 2: reshape to (B, T, H, D_head) first, then move the head axis before T with `transpose(0, 2, 1, 3)`.",
                  "الفراغ 2: أعد التشكيل إلى (B, T, H, D_head) أولًا، ثم انقل محور الرؤوس قبل T بـ `transpose(0, 2, 1, 3)`."),
            check("list(merged.shape) == [2, 6, 32] and bool(np.allclose(merged[1, 3, 16:24], head_out[1, 2, 3]))", True,
                  "Blank 3: undo the split in reverse order: transpose back, then reshape to (B, T, D).",
                  "الفراغ 3: اعكس التقسيم بالترتيب المعاكس: انقل المحاور أولًا ثم أعد التشكيل إلى (B, T, D)."),
            check("bool(np.allclose(y, layer_norm(x + merged)))", True,
                  "Blank 4: add the block input back (`x + merged`), then normalize.",
                  "الفراغ 4: أضف مدخل الكتلة مرة أخرى (`x + merged`)، ثم طبّع."),
        ),
        hints=(
            ("Every head gets an equal slice of the embedding: D / H features.", "يحصل كل رأس على شريحة متساوية من التضمين: D / H خاصية."),
            ("Reshape splits the last axis into (H, D_head); transpose then swaps the T and H axes.",
             "تقسم إعادة التشكيل المحور الأخير إلى (H, D_head)، ثم يبدّل النقل المحورين T وH."),
            ("Merging is the exact reverse, and the residual adds tensors of the same shape (B, T, D).",
             "الدمج هو العكس تمامًا، والوصلة المتبقية تجمع موترين بالأبعاد نفسها (B, T, D)."),
        ),
        success=("Correct! Heads are just a reshape of D into H × D_head, and merging restores (B, T, D) so the residual addition lines up.",
                 "صحيح! الرؤوس ليست إلا إعادة تشكيل لـ D إلى H × D_head، والدمج يعيد (B, T, D) فيتوافق الجمع المتبقي."),
        expected=NUMPY_NOTE,
        reflect=("Why must the attention output and the MLP output both have dimension D?",
                 "لماذا يجب أن يكون لمخرج الانتباه ومخرج الـ MLP البُعد D كلاهما؟"),
    ),
    "COURSE-003.M09.L01.EX04": Guided(
        goal=("Tokenize one sentence at character and word level and compare vocabulary size, sequence length and unknown words.",
              "قسّم جملة واحدة إلى رموز على مستوى الحرف والكلمة، وقارن حجم المفردات وطول التسلسل والكلمات غير المعروفة."),
        steps=(
            ("Split the text into characters.", "قسّم النص إلى حروف."),
            ("Encode the words with an `[UNK]` fallback.", "رمّز الكلمات مع الرجوع إلى `[UNK]` للكلمات غير المعروفة."),
            ("Count the distinct characters.", "عُدّ الحروف المميزة."),
            ("Count the unknown words.", "عُدّ الكلمات غير المعروفة."),
        ),
        starter='''text = "The cat sat. Zorblax sat too!"

# Step 1: character-level tokens (every character, including spaces and punctuation)
char_tokens = ___

# Step 2: word-level ids with an [UNK] fallback for words missing from the vocabulary
vocab = {"[UNK]": 0, "the": 1, "cat": 2, "sat.": 3, "sat": 4, "too!": 5}
words = text.lower().split()
word_ids = ___

# Step 3: how many distinct characters does the character vocabulary need?
char_vocab_size = ___

# Step 4: how many words fell back to [UNK]?
unknown_count = ___

print(len(char_tokens), "character tokens, vocabulary", char_vocab_size)
print(len(word_ids), "word tokens:", word_ids, "| unknown:", unknown_count)
''',
        answers=("list(text)", '[vocab.get(word, vocab["[UNK]"]) for word in words]', "len(set(char_tokens))", "word_ids.count(0)"),
        checks=(
            check("char_tokens == list(text)", True, "Blank 1: `list(text)` splits a string into characters.",
                  "الفراغ 1: تقسم `list(text)` السلسلة النصية إلى حروف."),
            check("list(word_ids)", [1, 2, 3, 0, 4, 5],
                  "Blank 2: look each word up with `vocab.get(word, vocab[\"[UNK]\"])`.",
                  "الفراغ 2: ابحث عن كل كلمة بـ `vocab.get(word, vocab[\"[UNK]\"])`."),
            check("char_vocab_size", 16, "Blank 3: count distinct characters with `len(set(...))`.",
                  "الفراغ 3: عُدّ الحروف المميزة بـ `len(set(...))`."),
            check("unknown_count", 1, "Blank 4: count how many ids equal the `[UNK]` id 0.",
                  "الفراغ 4: عُدّ المعرّفات التي تساوي معرّف `[UNK]` وهو 0."),
        ),
        hints=(
            ("A string is a sequence, so `list()` turns it into its characters.", "السلسلة النصية تسلسل، لذا يحوّلها `list()` إلى حروفها."),
            ("`dict.get(key, default)` returns the default when the key is missing.", "تعيد `dict.get(key, default)` القيمة الافتراضية عند غياب المفتاح."),
            ("`set()` removes duplicates; `list.count(x)` counts occurrences.", "يزيل `set()` التكرار، وتعدّ `list.count(x)` مرات الظهور."),
        ),
        success=("Correct! Characters give long sequences from a tiny vocabulary; words give short sequences but lose 'Zorblax' to [UNK] - the gap subword tokenizers such as BPE fill.",
                 "صحيح! تعطي الحروف تسلسلات طويلة من مفردات صغيرة جدًا، وتعطي الكلمات تسلسلات قصيرة لكنها تُضيع «Zorblax» في [UNK] - وهي الفجوة التي تسدّها مقسِّمات الكلمات الفرعية مثل BPE."),
        reflect=("Notice that 'sat' and 'sat.' are different word tokens. How would a subword tokenizer handle them?",
                 "لاحظ أن «sat» و«sat.» رمزان مختلفان على مستوى الكلمة. كيف سيتعامل معهما مقسِّم الكلمات الفرعية؟"),
    ),
    "COURSE-003.M10.L01.EX01": Guided(
        goal=("Build the linear diffusion noise schedule and use the closed form to noise a few points at a chosen timestep.",
              "ابنِ جدول الضوضاء الخطي في نماذج الانتشار، واستخدم الصيغة المغلقة لإضافة الضوضاء إلى بضع نقاط عند خطوة زمنية محددة."),
        steps=(
            ("Create 1000 betas evenly spaced from 1e-4 to 0.02.", "أنشئ 1000 قيمة beta متباعدة بانتظام من 1e-4 إلى 0.02."),
            ("Compute `alphas = 1 - betas`.", "احسب `alphas = 1 - betas`."),
            ("Take the cumulative product of the alphas.", "خذ الضرب التراكمي لقيم alpha."),
            ("Noise the clean points at t = 500 with the closed form.", "أضف الضوضاء إلى النقاط النظيفة عند t = 500 بالصيغة المغلقة."),
        ),
        starter='''import numpy as np

T = 1000
# Step 1: linear beta schedule from 1e-4 to 0.02 (torch.linspace(1e-4, 0.02, T))
betas = ___
# Step 2: alphas
alphas = ___
# Step 3: cumulative product of the alphas (torch.cumprod(alphas, dim=0))
alphas_cumprod = ___

sqrt_ab = np.sqrt(alphas_cumprod)              # how much signal is kept
sqrt_1m_ab = np.sqrt(1.0 - alphas_cumprod)     # how much noise is mixed in
for t in (0, 250, 500, 750, 999):
    print(f"t={t:4d}  signal {sqrt_ab[t]:.3f}  noise {sqrt_1m_ab[t]:.3f}")

# Step 4: x_t = sqrt(alpha_bar_t) * x0 + sqrt(1 - alpha_bar_t) * noise
rng = np.random.default_rng(0)
x0 = np.array([[1.0, 2.0], [-1.0, 0.5]])
noise = rng.normal(size=x0.shape)
t = 500
x_t = ___
print(x_t)
''',
        answers=("np.linspace(1e-4, 0.02, T)", "1.0 - betas", "np.cumprod(alphas)",
                 "sqrt_ab[t] * x0 + sqrt_1m_ab[t] * noise"),
        checks=(
            check("len(betas) == 1000 and bool(np.isclose(betas[0], 1e-4)) and bool(np.isclose(betas[-1], 0.02))", True,
                  "Blank 1: `np.linspace(1e-4, 0.02, T)` gives 1000 evenly spaced betas.",
                  "الفراغ 1: تعطي `np.linspace(1e-4, 0.02, T)` ألف قيمة beta متباعدة بانتظام."),
            check("bool(np.allclose(alphas, 1 - np.linspace(1e-4, 0.02, 1000)))", True,
                  "Blank 2: every alpha is one minus its beta.", "الفراغ 2: كل alpha تساوي واحدًا ناقص beta المقابلة."),
            check("bool(np.allclose(alphas_cumprod, np.cumprod(1 - np.linspace(1e-4, 0.02, 1000))))", True,
                  "Blank 3: use `np.cumprod(alphas)` - alpha-bar at t is the product of all alphas up to t.",
                  "الفراغ 3: استخدم `np.cumprod(alphas)` - قيمة alpha-bar عند t هي حاصل ضرب كل قيم alpha حتى t."),
            check("bool(np.allclose(x_t, sqrt_ab[500] * x0 + sqrt_1m_ab[500] * noise))", True,
                  "Blank 4: scale `x0` by the signal coefficient and `noise` by the noise coefficient at `t`, then add.",
                  "الفراغ 4: اضرب `x0` في معامل الإشارة و`noise` في معامل الضوضاء عند `t`، ثم اجمعهما."),
        ),
        hints=(
            ("`np.linspace(start, stop, count)` includes both ends.", "تشمل `np.linspace(start, stop, count)` الطرفين."),
            ("alpha-bar at step t multiplies every alpha from step 0 to t: a cumulative product.",
             "قيمة alpha-bar عند الخطوة t تضرب كل قيم alpha من الخطوة 0 حتى t: أي ضرب تراكمي."),
            ("Index both coefficient arrays with `t` and combine them with `x0` and `noise`.",
             "افهرس مصفوفتي المعاملين بـ `t` واجمعهما مع `x0` و`noise`."),
        ),
        success=("Correct! As t grows the signal coefficient shrinks towards 0 and the noise coefficient grows towards 1, so late timesteps are almost pure noise.",
                 "صحيح! مع ازدياد t يتقلص معامل الإشارة نحو 0 ويكبر معامل الضوضاء نحو 1، فتصبح الخطوات المتأخرة ضوضاء شبه خالصة."),
        expected=NUMPY_NOTE,
    ),
    "COURSE-003.M10.L01.EX02": Guided(
        goal=("Write one clean diffusion training step: noise the data, predict the noise, and update the model.",
              "اكتب خطوة تدريب واحدة نظيفة لنموذج انتشار: أضف الضوضاء إلى البيانات، وتوقّع الضوضاء، وحدّث النموذج."),
        steps=(
            ("Put the model in training mode.", "ضع النموذج في وضع التدريب."),
            ("Predict the noise from the noisy points and their timesteps.", "توقّع الضوضاء من النقاط المشوّشة وخطواتها الزمنية."),
            ("Compute the MSE between predicted and true noise.", "احسب متوسط مربع الخطأ بين الضوضاء المتوقعة والحقيقية."),
            ("Backpropagate and take an optimizer step.", "نفّذ الانتشار العكسي ثم خطوة المُحسِّن."),
        ),
        starter='''import torch
import torch.nn.functional as F

# model, optimizer, x0 (clean 2D points), T and forward_diffusion(x0, t) come from the lesson
device = "cuda" if torch.cuda.is_available() else "cpu"
model, x0 = model.to(device), x0.to(device)

# Step 1: training mode
___

t = torch.randint(0, T, (x0.shape[0],), device=device)   # one random timestep per point
x_t, noise = forward_diffusion(x0, t)                     # closed-form corruption + the noise it used

# Step 2: the model predicts the noise; it needs t to know how noisy x_t is
noise_pred = ___

# Step 3: mean squared error against the real noise
loss = ___

optimizer.zero_grad(set_to_none=True)
# Step 4: backpropagate, then update
___
___
print(loss.item())
''',
        answers=("model.train()", "model(x_t, t)", "F.mse_loss(noise_pred, noise)", "loss.backward()", "optimizer.step()"),
        alternatives={
            3: ("F.mse_loss(noise, noise_pred)", "((noise_pred - noise) ** 2).mean()", "((noise - noise_pred) ** 2).mean()"),
        },
        blanks=(
            ("call `model.train()`.", "استدعِ `model.train()`."),
            ("pass both the noisy points and the timesteps: `model(x_t, t)`.", "مرّر النقاط المشوّشة والخطوات الزمنية معًا: `model(x_t, t)`."),
            ("compare the prediction with the true noise: `F.mse_loss(noise_pred, noise)`.",
             "قارن التنبؤ بالضوضاء الحقيقية: `F.mse_loss(noise_pred, noise)`."),
            ("call `loss.backward()`.", "استدعِ `loss.backward()`."),
            ("call `optimizer.step()`.", "استدعِ `optimizer.step()`."),
        ),
        hints=(
            ("Every training step starts in training mode.", "تبدأ كل خطوة تدريب في وضع التدريب."),
            ("The target is the noise that was added, not the clean points.", "الهدف هو الضوضاء التي أُضيفت، لا النقاط النظيفة."),
            ("After `zero_grad`, the order is always `backward()` then `step()`.", "بعد `zero_grad` يكون الترتيب دائمًا `backward()` ثم `step()`."),
        ),
        success=("Correct! The model learns to recognise the noise at every timestep, and the timestep input tells it how much noise to expect.",
                 "صحيح! يتعلّم النموذج التعرّف على الضوضاء في كل خطوة زمنية، ويخبره مُدخل الخطوة الزمنية بمقدار الضوضاء المتوقع."),
        expected=TORCH_NOTE,
        reflect=("Why does the model need the timestep as an input?", "لماذا يحتاج النموذج الخطوة الزمنية مدخلًا؟"),
    ),
    "COURSE-003.M10.L01.EX03": Guided(
        goal=("Complete the reverse-diffusion sampling loop that turns Gaussian noise into 1000 2D points.",
              "أكمل حلقة أخذ العينات بالانتشار العكسي التي تحوّل ضوضاء غاوسية إلى 1000 نقطة ثنائية الأبعاد."),
        steps=(
            ("Switch the model to evaluation mode.", "حوّل النموذج إلى وضع التقييم."),
            ("Disable gradient tracking for sampling.", "عطّل تتبّع التدرّجات أثناء أخذ العينات."),
            ("Loop over the timesteps from T − 1 down to 0.", "كرّر على الخطوات الزمنية من T − 1 نزولًا إلى 0."),
            ("Replace `x` by one denoising step.", "استبدل `x` بخطوة إزالة ضوضاء واحدة."),
        ),
        starter='''import torch

def sample(model, n_points=1000, T=1000, snapshot_steps=(999, 500, 100, 0)):
    # Step 1: evaluation mode
    ___
    x = torch.randn(n_points, 2)          # start from pure Gaussian noise
    snapshots = {}
    # Step 2: no gradients are needed while sampling
    with ___:
        # Step 3: walk backwards through every timestep, T-1 down to 0
        for step in ___:
            t = torch.full((n_points,), step, dtype=torch.long)
            # Step 4: remove a little noise (sample_timestep comes from the lesson)
            x = ___
            if step in snapshot_steps:
                snapshots[step] = x.clone()
    return x, snapshots
''',
        answers=("model.eval()", "torch.no_grad()", "range(T - 1, -1, -1)", "sample_timestep(model, x, t)"),
        alternatives={2: ("torch.inference_mode()",), 3: ("reversed(range(T))",)},
        blanks=(
            ("call `model.eval()`.", "استدعِ `model.eval()`."),
            ("use `torch.no_grad()`.", "استخدم `torch.no_grad()`."),
            ("count down with `range(T - 1, -1, -1)` (or `reversed(range(T))`).", "عُدّ تنازليًا بـ `range(T - 1, -1, -1)` (أو `reversed(range(T))`)."),
            ("call `sample_timestep(model, x, t)`.", "استدعِ `sample_timestep(model, x, t)`."),
        ),
        hints=(
            ("Sampling is inference: evaluation mode and no autograd.", "أخذ العينات استدلال: وضع التقييم ودون autograd."),
            ("`range(start, stop, step)` with a step of -1 counts down; the stop value is excluded.",
             "تعدّ `range(start, stop, step)` تنازليًا عندما تكون الخطوة -1، ولا تُشمل قيمة النهاية."),
            ("Each iteration feeds the current `x` and the timestep tensor back into `sample_timestep`.",
             "كل تكرار يمرّر `x` الحالي وموتر الخطوة الزمنية إلى `sample_timestep` مرة أخرى."),
        ),
        success=("Correct! Generation repeats one small denoising step 1000 times, starting from noise.",
                 "صحيح! يكرّر التوليد خطوة صغيرة لإزالة الضوضاء 1000 مرة، بدءًا من الضوضاء."),
        expected=TORCH_NOTE,
        reflect=("Training jumps straight to any timestep with a closed form. Why can sampling not jump straight back to clean data?",
                 "يقفز التدريب مباشرة إلى أي خطوة زمنية بصيغة مغلقة. لماذا لا يستطيع أخذ العينات القفز مباشرة إلى البيانات النظيفة؟"),
    ),
    "COURSE-003.M11.L01.EX01": Guided(
        goal=("Merge candidate and annotation tables whose coordinates differ slightly, using an axis-wise tolerance.",
              "ادمج جدولي المرشحين والتعليقات التوضيحية اللذين تختلف إحداثياتهما قليلًا، باستخدام تفاوت مسموح لكل محور."),
        steps=(
            ("Group the annotations by series UID.", "جمّع التعليقات التوضيحية حسب معرّف السلسلة (series UID)."),
            ("Write the match test: every axis must be within a quarter of the diameter.", "اكتب اختبار المطابقة: يجب أن يقع كل محور ضمن ربع القطر."),
            ("Use the test when looking for a candidate's annotation.", "استخدم الاختبار عند البحث عن التعليق المطابق للمرشح."),
        ),
        starter='''# (series_uid, center_xyz in mm, is_nodule)
candidates = [
    ("1.2.3", (10.0, 20.0, 30.0), True),
    ("1.2.3", (50.0, 50.0, 50.0), False),
    ("4.5.6", (-5.2, 8.1, 100.4), True),
    ("4.5.6", (70.0, 10.0, 10.0), True),
]
# (series_uid, center_xyz in mm, diameter_mm) - measured by a different tool, so centers differ slightly
annotations = [
    ("1.2.3", (10.4, 19.7, 30.2), 6.5),
    ("4.5.6", (-5.0, 8.0, 100.0), 4.2),
]

# Step 1: series_uid -> list of (center_xyz, diameter_mm)
annotations_by_uid = {}
for uid, xyz, diameter in annotations:
    ___

# Step 2: match when EVERY axis differs by less than a quarter of the diameter
def matches(candidate_xyz, annotation_xyz, diameter_mm):
    return ___

# Step 3: attach a diameter to each positive candidate that has a nearby annotation
records = []
for uid, xyz, is_nodule in candidates:
    diameter = 0.0
    if is_nodule:
        for annotation_xyz, annotation_diameter in annotations_by_uid.get(uid, []):
            if ___:
                diameter = annotation_diameter
                break
    records.append({"is_nodule": is_nodule, "diameter_mm": diameter, "series_uid": uid, "center_xyz": xyz})

for record in records:
    print(record)
''',
        answers=(
            "annotations_by_uid.setdefault(uid, []).append((xyz, diameter))",
            "all(abs(c - a) < diameter_mm / 4 for c, a in zip(candidate_xyz, annotation_xyz))",
            "matches(xyz, annotation_xyz, annotation_diameter)",
        ),
        checks=(
            check("sorted((k, len(v)) for k, v in annotations_by_uid.items())", [["1.2.3", 1], ["4.5.6", 1]],
                  "Blank 1: append `(xyz, diameter)` to the list stored under `uid`, creating it first if needed.",
                  "الفراغ 1: أضف `(xyz, diameter)` إلى القائمة المخزّنة تحت `uid`، وأنشئها أولًا عند الحاجة."),
            check("[matches((0, 0, 0), (1, 0, 0), 8.0), matches((0, 0, 0), (1, 0, 0), 2.0), matches((0, 0, 0), (0, 0, 3), 8.0)]", [True, False, False],
                  "Blank 2: every axis difference must be smaller than `diameter_mm / 4`.",
                  "الفراغ 2: يجب أن يكون فرق كل محور أصغر من `diameter_mm / 4`."),
            check("[r['diameter_mm'] for r in records]", [6.5, 0.0, 4.2, 0.0],
                  "Blank 3: call `matches(xyz, annotation_xyz, annotation_diameter)` for each annotation of the same series.",
                  "الفراغ 3: استدعِ `matches(xyz, annotation_xyz, annotation_diameter)` لكل تعليق في السلسلة نفسها."),
        ),
        hints=(
            ("`dict.setdefault(key, [])` returns the list for `key`, creating an empty one the first time.",
             "تعيد `dict.setdefault(key, [])` القائمة الخاصة بالمفتاح، وتنشئ قائمة فارغة في المرة الأولى."),
            ("`zip` pairs the x, y and z values; `all(...)` is True only if every axis is close enough.",
             "تقرن `zip` قيم x وy وz معًا، وتكون `all(...)` صحيحة فقط إذا كان كل محور قريبًا بما يكفي."),
            ("The loop already gives you `annotation_xyz` and `annotation_diameter` - pass them to `matches`.",
             "تعطيك الحلقة `annotation_xyz` و`annotation_diameter` بالفعل - مرّرهما إلى `matches`."),
        ),
        success=("Correct! Two nodules found their annotation despite small coordinate differences, and the unmatched positive keeps diameter 0.",
                 "صحيح! وجدت عقدتان تعليقهما رغم الفروق الصغيرة في الإحداثيات، واحتفظ المرشح الإيجابي غير المطابق بالقطر 0."),
        reflect=("What assumption does a quarter-of-the-diameter tolerance make, and when could it match the wrong nodule?",
                 "ما الافتراض الذي يقوم عليه التفاوت بربع القطر؟ ومتى قد يطابق عقدة خاطئة؟"),
    ),
    "COURSE-003.M11.L01.EX02": Guided(
        goal=("Implement the IRC ↔ XYZ conversions and prove they round-trip, including a flipped axis.",
              "نفّذ التحويل بين IRC وXYZ في الاتجاهين، وأثبت أن التحويل ذهابًا وإيابًا يعيد القيم نفسها، حتى مع محور مقلوب."),
        steps=(
            ("Convert array coordinates to millimetres.", "حوّل إحداثيات المصفوفة إلى مليمترات."),
            ("Convert millimetres back to continuous array coordinates.", "حوّل المليمترات مرة أخرى إلى إحداثيات مصفوفة متصلة."),
            ("Round and reorder to (index, row, column).", "قرّب وأعد الترتيب إلى (index, row, column)."),
        ),
        starter='''import numpy as np

origin = np.array([-200.0, -180.0, -350.0])     # mm position of voxel (0, 0, 0)
spacing = np.array([0.7, 0.7, 2.5])             # mm per voxel along x (column), y (row), z (index)
identity = np.eye(3)
flip_y = np.diag([1.0, -1.0, 1.0])

def irc2xyz(coord_irc, origin, spacing, direction):
    cri = np.array(coord_irc, dtype=float)[::-1]      # (index, row, col) -> (col, row, index)
    # Step 1: scale by voxel size, rotate by the direction matrix, shift by the origin
    return ___

def xyz2irc(coord_xyz, origin, spacing, direction):
    # Step 2: undo the shift, undo the rotation, divide by voxel size
    cri = ___
    # Step 3: round to the nearest voxel and reorder (col, row, index) -> (index, row, col)
    return ___

points = [(0, 0, 0), (10, 100, 200), (63, 255, 7)]
round_trip_identity = [xyz2irc(irc2xyz(p, origin, spacing, identity), origin, spacing, identity) for p in points]
round_trip_flipped = [xyz2irc(irc2xyz(p, origin, spacing, flip_y), origin, spacing, flip_y) for p in points]
print(irc2xyz((10, 100, 200), origin, spacing, identity))
print(round_trip_identity, round_trip_flipped)
''',
        answers=(
            "direction @ (cri * spacing) + origin",
            "((np.array(coord_xyz) - origin) @ np.linalg.inv(direction)) / spacing",
            "tuple(int(v) for v in np.round(cri)[::-1])",
        ),
        checks=(
            check("bool(np.allclose(irc2xyz((10, 100, 200), origin, spacing, identity), [-60.0, -110.0, -325.0]))", True,
                  "Blank 1: multiply (col, row, index) by the spacing, apply `direction @`, then add `origin`.",
                  "الفراغ 1: اضرب (col, row, index) في المسافات، ثم طبّق `direction @`، ثم أضف `origin`."),
            check("bool(np.allclose(irc2xyz((10, 100, 200), origin, spacing, flip_y), [-60.0, -250.0, -325.0]))", True,
                  "Blank 1: apply the direction matrix to the scaled coordinates before adding the origin.",
                  "الفراغ 1: طبّق مصفوفة الاتجاه على الإحداثيات المحجّمة قبل إضافة نقطة الأصل."),
            check("[list(p) for p in round_trip_identity] == [[0, 0, 0], [10, 100, 200], [63, 255, 7]]", True,
                  "Blanks 2-3: subtract the origin, multiply by the inverse direction, divide by the spacing, round, then reverse the order.",
                  "الفراغان 2 و3: اطرح نقطة الأصل، ثم اضرب في معكوس الاتجاه، ثم اقسم على المسافات، ثم قرّب واعكس الترتيب."),
            check("[list(p) for p in round_trip_flipped] == [[0, 0, 0], [10, 100, 200], [63, 255, 7]]", True,
                  "Blank 2: undo the direction with `np.linalg.inv(direction)` so a flipped axis round-trips too.",
                  "الفراغ 2: ألغِ أثر الاتجاه بـ `np.linalg.inv(direction)` كي يعود المحور المقلوب أيضًا."),
            check("all(isinstance(v, int) for v in xyz2irc((-60.0, -110.0, -325.0), origin, spacing, identity))", True,
                  "Blank 3: return plain integers, e.g. `tuple(int(v) for v in np.round(cri)[::-1])`.",
                  "الفراغ 3: أعد أعدادًا صحيحة عادية، مثل `tuple(int(v) for v in np.round(cri)[::-1])`."),
        ),
        hints=(
            ("Order matters: voxel units → millimetres (× spacing) → orientation (direction @) → position (+ origin).",
             "الترتيب مهم: وحدات الفوكسل ← المليمترات (× المسافات) ← الاتجاه (direction @) ← الموضع (+ نقطة الأصل)."),
            ("Going back reverses every step in the opposite order.", "العودة تعكس كل خطوة بالترتيب المعاكس."),
            ("`np.round` then `int(...)` gives voxel indices; `[::-1]` turns (col, row, index) into (index, row, col).",
             "تعطي `np.round` ثم `int(...)` فهارس الفوكسلات، ويحوّل `[::-1]` الترتيب (col, row, index) إلى (index, row, col)."),
        ),
        success=("Correct! Every point survives the round trip, with or without a flipped axis.",
                 "صحيح! تعود كل نقطة سليمة بعد التحويل ذهابًا وإيابًا، مع محور مقلوب أو دونه."),
        reflect=("Why might an exact round trip fail for a physical point that does not sit at a voxel centre?",
                 "لماذا قد يفشل التحويل ذهابًا وإيابًا بدقة لنقطة فعلية لا تقع في مركز فوكسل؟"),
    ),
    "COURSE-003.M11.L01.EX03": Guided(
        goal=("Measure how much a one-CT cache saves when candidates are read in order versus shuffled.",
              "قِس مقدار ما يوفّره تخزين مؤقت يتسع لصورة CT واحدة عند قراءة المرشحين بالترتيب مقارنةً بقراءتهم بترتيب عشوائي."),
        steps=(
            ("Limit the cache to one CT.", "حدّد التخزين المؤقت بصورة CT واحدة."),
            ("Read each candidate's CT through the cache.", "اقرأ صورة CT لكل مرشح عبر التخزين المؤقت."),
            ("Count the loads for the shuffled order.", "عُدّ مرات التحميل للترتيب العشوائي."),
        ),
        starter='''from functools import lru_cache

load_count = 0

def load_ct(series_uid):
    """Pretend this reads a whole CT scan from disk - the expensive part."""
    global load_count
    load_count += 1
    return f"ct-{series_uid}"

# Step 1: keep only the most recently used CT in memory
@lru_cache(maxsize=___)
def get_ct(series_uid):
    return load_ct(series_uid)

def count_loads(order):
    global load_count
    get_ct.cache_clear()        # cold cache
    load_count = 0
    for series_uid in order:
        # Step 2: fetch this candidate's CT through the cache
        ___
    return load_count

ordered = ["a"] * 4 + ["b"] * 4 + ["c"] * 4          # candidates grouped by CT
shuffled = ["a", "b", "c", "a", "c", "b", "b", "a", "c", "c", "a", "b"]
ordered_loads = count_loads(ordered)
# Step 3: the same 12 candidates in shuffled order
shuffled_loads = ___
print("ordered:", ordered_loads, "loads | shuffled:", shuffled_loads, "loads")
''',
        answers=("1", "get_ct(series_uid)", "count_loads(shuffled)"),
        checks=(
            check("get_ct.cache_info().maxsize", 1, "Blank 1: `maxsize=1` keeps exactly one CT.", "الفراغ 1: يحتفظ `maxsize=1` بصورة CT واحدة بالضبط."),
            check("ordered_loads", 3,
                  "Blank 2: call `get_ct(series_uid)` inside the loop; grouped candidates should load each CT once.",
                  "الفراغ 2: استدعِ `get_ct(series_uid)` داخل الحلقة؛ يجب أن يُحمِّل المرشحون المجمَّعون كل صورة CT مرة واحدة."),
            check("shuffled_loads", 10, "Blank 3: call `count_loads(shuffled)`.", "الفراغ 3: استدعِ `count_loads(shuffled)`."),
        ),
        hints=(
            ("`lru_cache(maxsize=n)` remembers the results of the last n different arguments.",
             "تتذكّر `lru_cache(maxsize=n)` نتائج آخر n وسيطًا مختلفًا."),
            ("Only calls that miss the cache reach `load_ct` and increase `load_count`.",
             "لا تصل إلى `load_ct` وتزيد `load_count` إلا الاستدعاءات التي لا تجد نتيجتها في التخزين المؤقت."),
            ("Reuse `count_loads` for the second order.", "أعد استخدام `count_loads` للترتيب الثاني."),
        ),
        success=("Correct! Grouped access loads each CT once (3 loads), but shuffled access reloads almost every time (10 loads) - a one-CT LRU cache depends entirely on access order.",
                 "صحيح! يحمّل الوصول المجمَّع كل صورة CT مرة واحدة (3 مرات تحميل)، بينما يعيد الوصول العشوائي التحميل كل مرة تقريبًا (10 مرات) - فالتخزين المؤقت LRU لصورة واحدة يعتمد كليًا على ترتيب الوصول."),
        expected=(
            "Counting expensive loads measures the same effect as timing them, without depending on how fast the machine is.",
            "عدّ مرات التحميل المكلفة يقيس الأثر نفسه الذي يقيسه التوقيت، دون الاعتماد على سرعة الجهاز.",
        ),
    ),
    "COURSE-003.M12.L01.EX01": Guided(
        goal=("Wrap a dataset of 3D CT crops in DataLoaders with different worker counts and inspect one batch.",
              "غلّف مجموعة بيانات من مقاطع CT ثلاثية الأبعاد في DataLoaders بأعداد عمّال مختلفة، وافحص دفعة واحدة."),
        steps=(
            ("Use a batch size of 32.", "استخدم حجم دفعة 32."),
            ("Pass the current worker count.", "مرّر عدد العمّال الحالي."),
            ("Pin memory only when CUDA is available.", "ثبّت الذاكرة (pin memory) فقط عند توفر CUDA."),
            ("Take the first batch from the loader.", "خذ الدفعة الأولى من الـ loader."),
        ),
        starter='''import time
import torch
from torch.utils.data import DataLoader, Dataset

class SyntheticLuna(Dataset):
    """Returns tensors shaped like LunaDataset: (channel, index, row, column) and a label."""
    def __len__(self):
        return 256

    def __getitem__(self, index):
        return torch.randn(1, 32, 48, 48), torch.tensor(index % 2)

for workers in (0, 1, 2):
    loader = DataLoader(
        SyntheticLuna(),
        batch_size=___,                    # Step 1
        num_workers=___,                   # Step 2
        pin_memory=___,                    # Step 3
    )
    # Step 4: the first batch
    batch, labels = ___
    start = time.perf_counter()
    for _ in zip(range(5), loader):
        pass
    print(workers, tuple(batch.shape), f"{time.perf_counter() - start:.2f}s")   # (32, 1, 32, 48, 48)
''',
        answers=("32", "workers", "torch.cuda.is_available()", "next(iter(loader))"),
        alternatives={},
        blanks=(
            ("use `batch_size=32`.", "استخدم `batch_size=32`."),
            ("use the loop variable: `num_workers=workers`.", "استخدم متغير الحلقة: `num_workers=workers`."),
            ("`pin_memory=torch.cuda.is_available()` only helps when batches go to a GPU.",
             "يفيد `pin_memory=torch.cuda.is_available()` فقط عندما تُنقل الدفعات إلى GPU."),
            ("`next(iter(loader))` returns the first (inputs, labels) batch.", "تعيد `next(iter(loader))` أول دفعة (inputs, labels)."),
        ),
        hints=(
            ("The loop variable takes the values 0, 1 and 2 - pass it on as the number of worker processes.", "يأخذ متغير الحلقة القيم 0 و1 و2، فمرّره بوصفه عدد العمليات العاملة."),
            ("`torch.cuda.is_available()` returns True or False.", "تعيد `torch.cuda.is_available()` القيمة True أو False."),
            ("A DataLoader is iterable; `iter` then `next` gives its first batch.", "الـ DataLoader قابل للتكرار؛ و`iter` ثم `next` يعطيان أول دفعة."),
        ),
        success=("Correct! Each batch stacks 32 samples into N × 1 × 32 × 48 × 48; more workers prepare batches in parallel, but only up to the limits of CPU cores and disk speed.",
                 "صحيح! تكدّس كل دفعة 32 عينة في N × 1 × 32 × 48 × 48؛ ويجهّز العمّال الإضافيون الدفعات بالتوازي، لكن في حدود أنوية المعالج وسرعة القرص فقط."),
        expected=TORCH_NOTE,
        reflect=("Why does adding more workers not keep speeding up loading forever?",
                 "لماذا لا تستمر زيادة عدد العمّال في تسريع التحميل إلى ما لا نهاية؟"),
    ),
    "COURSE-003.M12.L01.EX02": Guided(
        goal=("Trace the shapes through LunaModel's four 3D blocks and count its trainable parameters.",
              "تتبّع الأبعاد عبر الكتل الثلاثية الأبعاد الأربع في LunaModel، واحسب معاملاته القابلة للتدريب."),
        steps=(
            ("Count the parameters of one 3×3×3 convolution.", "احسب معاملات التفاف واحد بحجم 3×3×3."),
            ("Write the shape after one block (two padded convolutions, then 2× max-pooling).", "اكتب الأبعاد بعد كتلة واحدة (التفافان بحشو ثم max-pooling بمعامل 2)."),
            ("Compute the number of flattened features.", "احسب عدد الخصائص بعد التسطيح."),
            ("Add the head `Linear(flat_features, 2)`.", "أضف رأس التصنيف `Linear(flat_features, 2)`."),
        ),
        starter='''def conv3d_params(in_ch, out_ch, k=3):
    # Step 1: weights (out x in x k x k x k) plus one bias per output channel
    return ___

def block_params(in_ch, out_ch):
    return conv3d_params(in_ch, out_ch) + conv3d_params(out_ch, out_ch)

def block_output_shape(shape, out_ch):
    # Step 2: padding=1 convolutions keep the size; MaxPool3d(2) halves depth, height and width
    n, _, d, h, w = shape
    return ___

shape = (2, 1, 32, 48, 48)               # batch, channel, index, row, column
channels = [1, 8, 16, 32, 64]            # LunaModel with 8 base channels
total = 2                                # tail BatchNorm3d(1): one weight, one bias
for in_ch, out_ch in zip(channels[:-1], channels[1:]):
    shape = block_output_shape(shape, out_ch)
    total += block_params(in_ch, out_ch)
    print(shape)

# Step 3: features after flattening the backbone output
flat_features = ___
# Step 4: the head nn.Linear(flat_features, 2)
total += ___
print("flattened:", flat_features, "| trainable parameters:", total)
''',
        answers=("in_ch * out_ch * k ** 3 + out_ch", "(n, out_ch, d // 2, h // 2, w // 2)",
                 "shape[1] * shape[2] * shape[3] * shape[4]", "flat_features * 2 + 2"),
        checks=(
            check("[conv3d_params(1, 8), conv3d_params(64, 64)]", [224, 110656],
                  "Blank 1: in × out × 3 × 3 × 3 weights plus `out_ch` biases.",
                  "الفراغ 1: in × out × 3 × 3 × 3 وزنًا زائد `out_ch` انحيازًا."),
            check("list(shape)", [2, 64, 2, 3, 3],
                  "Blank 2: keep the batch size, use `out_ch` channels, and halve each spatial size with `// 2`.",
                  "الفراغ 2: أبقِ حجم الدفعة، واستخدم `out_ch` قناة، ونصّف كل حجم مكاني بـ `// 2`."),
            check("flat_features", 1152, "Blank 3: multiply channels × depth × height × width: 64 × 2 × 3 × 3.",
                  "الفراغ 3: اضرب القنوات × العمق × الارتفاع × العرض: 64 × 2 × 3 × 3."),
            check("total", 222220, "Blank 4: the head has `flat_features * 2` weights plus 2 biases.",
                  "الفراغ 4: لرأس التصنيف `flat_features * 2` وزنًا زائد انحيازين."),
        ),
        hints=(
            ("A 3D kernel has k × k × k weights for every (input, output) channel pair.", "للنواة الثلاثية الأبعاد k × k × k وزنًا لكل زوج من قنوات (الإدخال، الإخراج)."),
            ("Four poolings turn 32 × 48 × 48 into 2 × 3 × 3.", "تحوّل أربع عمليات تجميع الأبعاد 32 × 48 × 48 إلى 2 × 3 × 3."),
            ("Flattening multiplies every axis except the batch axis.", "يضرب التسطيح كل المحاور ما عدا محور الدفعة."),
        ),
        success=("Correct! The backbone ends at (2, 64, 2, 3, 3), flattens to 1152 features, and LunaModel has 222,220 trainable parameters.",
                 "صحيح! ينتهي العمود الفقري عند (2, 64, 2, 3, 3)، ويُسطَّح إلى 1152 خاصية، ولدى LunaModel 222,220 معاملًا قابلًا للتدريب."),
    ),
    "COURSE-003.M12.L01.EX03": Guided(
        goal=("Run validation without changing a single model parameter, and prove it.",
              "نفّذ التحقق دون تغيير أي معامل في النموذج، وأثبت ذلك."),
        steps=(
            ("Switch the model to evaluation mode.", "حوّل النموذج إلى وضع التقييم."),
            ("Disable autograd for the validation loop.", "عطّل autograd في حلقة التحقق."),
            ("Compare every parameter with its saved copy.", "قارن كل معامل بنسخته المحفوظة."),
        ),
        starter='''import torch

# model (with BatchNorm3d), val_loader and loss_fn come from the lesson
before = [p.detach().clone() for p in model.parameters()]

# Step 1: evaluation mode - BatchNorm uses its stored statistics
___

# Step 2: no computation graph during validation
with ___:
    for batch, labels in val_loader:
        loss = loss_fn(model(batch), labels)     # no backward(), no optimizer.step()

# Step 3: is every parameter exactly unchanged?
unchanged = all(___ for b, p in zip(before, model.parameters()))
print("parameters unchanged:", unchanged)
''',
        answers=("model.eval()", "torch.no_grad()", "torch.equal(b, p)"),
        alternatives={2: ("torch.inference_mode()",), 3: ("torch.equal(p, b)", "torch.allclose(b, p)", "torch.allclose(p, b)", "bool((b == p).all())", "(b == p).all()")},
        blanks=(
            ("call `model.eval()`.", "استدعِ `model.eval()`."),
            ("use `torch.no_grad()`.", "استخدم `torch.no_grad()`."),
            ("compare the two tensors exactly with `torch.equal(b, p)`.", "قارن الموترين بدقة باستخدام `torch.equal(b, p)`."),
        ),
        hints=(
            ("Validation is evaluation: the model's mode must change first.", "التحقق تقييم: يجب أن يتغيّر وضع النموذج أولًا."),
            ("`torch.no_grad()` is a context manager used with `with`.", "يُستخدم مدير السياق `torch.no_grad()` مع `with`."),
            ("`torch.equal(a, b)` is True only when shapes and every value match.", "تكون `torch.equal(a, b)` صحيحة فقط عند تطابق الأبعاد وكل القيم."),
        ),
        success=("Correct! Validation in eval mode, under no_grad and without an optimizer step, leaves every parameter exactly as it was.",
                 "صحيح! التحقق في وضع التقييم، تحت no_grad ودون خطوة مُحسِّن، يترك كل معامل كما كان تمامًا."),
        expected=TORCH_NOTE,
        reflect=("Which of the two lines would you lose if you forgot `model.eval()`: the unchanged weights or the unchanged BatchNorm statistics?",
                 "لو نسيت `model.eval()`، فأيهما ستفقد: ثبات الأوزان أم ثبات إحصاءات BatchNorm؟"),
    ),
    "COURSE-003.M12.L01.EX04": Guided(
        goal=("Show how a classifier that always says 'negative' scores 99.7% accuracy on very imbalanced data.",
              "بيّن كيف يحقق مصنّف يقول «سلبي» دائمًا دقة 99.7% على بيانات شديدة عدم التوازن."),
        steps=(
            ("Predict every sample as negative.", "تنبّأ بأن كل العينات سلبية."),
            ("Compute the overall accuracy.", "احسب الدقة الإجمالية."),
            ("Compute the accuracy on the positive samples only.", "احسب الدقة على العينات الإيجابية فقط."),
            ("Compute the positive-class loss as probabilities rise from 0.01 to 0.20.", "احسب خسارة الفئة الإيجابية مع ارتفاع الاحتمالات من 0.01 إلى 0.20."),
        ),
        starter='''import numpy as np

labels = np.array([0] * 9970 + [1] * 30)       # 30 positives in 10,000 samples

# Step 1: a "model" that predicts negative for everything
predictions = ___

# Step 2: overall accuracy
overall_accuracy = ___
negative_accuracy = float((predictions[labels == 0] == 0).mean())
# Step 3: accuracy on the positive samples only
positive_accuracy = ___

# Step 4: positive probabilities improve, but all stay below the 0.5 threshold
probabilities = [0.01, 0.05, 0.10, 0.20]
positive_losses = ___
print(overall_accuracy, negative_accuracy, positive_accuracy)
print("cross-entropy on a positive:", positive_losses)
''',
        answers=(
            "np.zeros_like(labels)",
            "float((predictions == labels).mean())",
            "float((predictions[labels == 1] == 1).mean())",
            "[round(float(-np.log(p)), 3) for p in probabilities]",
        ),
        checks=(
            check("int(np.asarray(predictions).sum()) == 0 and len(predictions) == 10000", True,
                  "Blank 1: create 10,000 zeros, e.g. `np.zeros_like(labels)`.", "الفراغ 1: أنشئ 10,000 صفر، مثل `np.zeros_like(labels)`."),
            check("round(float(overall_accuracy), 4)", 0.997, "Blank 2: the fraction of predictions equal to the labels.",
                  "الفراغ 2: نسبة التنبؤات المساوية للتسميات."),
            check("float(positive_accuracy)", 0.0, "Blank 3: select the positive rows with `labels == 1` before comparing.",
                  "الفراغ 3: اختر الصفوف الإيجابية بـ `labels == 1` قبل المقارنة."),
            check("list(positive_losses)", [4.605, 2.996, 2.303, 1.609],
                  "Blank 4: the loss on a positive sample is -log(p); round each to 3 decimals.",
                  "الفراغ 4: الخسارة على عينة إيجابية هي -log(p)؛ قرّب كلًّا منها إلى 3 منازل."),
        ),
        hints=(
            ("`np.zeros_like(x)` gives an array of zeros shaped like `x`.", "تعطي `np.zeros_like(x)` مصفوفة أصفار بشكل `x` نفسه."),
            ("The mean of a Boolean array is the fraction of True values.", "متوسط المصفوفة المنطقية هو نسبة القيم True."),
            ("Cross-entropy for a positive sample is `-np.log(p)`.", "خسارة cross-entropy لعينة إيجابية هي `-np.log(p)`."),
        ),
        success=("Correct! 99.7% accuracy with 0% of the positives found: and the loss keeps falling as probabilities rise, even though no thresholded prediction changes yet.",
                 "صحيح! دقة 99.7% مع اكتشاف 0% من الحالات الإيجابية؛ وتستمر الخسارة في الانخفاض مع ارتفاع الاحتمالات رغم أن أي تنبؤ بعد العتبة لم يتغير بعد."),
        reflect=("Why can the positive loss improve while thresholded positive accuracy stays at zero?",
                 "لماذا يمكن أن تتحسن خسارة الفئة الإيجابية بينما تبقى دقتها بعد العتبة صفرًا؟"),
    ),
    "COURSE-003.M13.L01.EX01": Guided(
        goal=("Compute TP, TN, FP and FN from probabilities and a threshold, then accuracy, precision, recall and F1 - safely.",
              "احسب TP وTN وFP وFN من الاحتمالات والعتبة، ثم الدقة وPrecision وRecall وF1 بأمان."),
        steps=(
            ("Turn probabilities into predictions with the threshold.", "حوّل الاحتمالات إلى تنبؤات باستخدام العتبة."),
            ("Count the false positives.", "عُدّ الإيجابيات الكاذبة (FP)."),
            ("Compute precision, returning 0.0 when nothing was predicted positive.", "احسب Precision، وأعد 0.0 عندما لا يُتنبّأ بأي حالة إيجابية."),
            ("Compute F1, also guarded against division by zero.", "احسب F1 مع الحماية من القسمة على صفر أيضًا."),
        ),
        starter='''import numpy as np

labels = np.array([1,0,1,1,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0], dtype=bool)
probs = np.array([0.9,0.2,0.65,0.4,0.55,0.1,0.8,0.3,0.45,0.05,0.6,0.95,0.15,0.35,0.7,0.25,0.3,0.4,0.2,0.1])

def confusion(labels, probs, threshold):
    # Step 1: predicted positive when the probability reaches the threshold
    predicted = ___
    tp = int((predicted & labels).sum())
    tn = int((~predicted & ~labels).sum())
    # Step 2: predicted positive, actually negative
    fp = ___
    fn = int((~predicted & labels).sum())
    return tp, tn, fp, fn

def metrics(tp, tn, fp, fn):
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    # Step 3: precision; 0.0 when there are no predicted positives
    precision = ___
    recall = tp / (tp + fn) if tp + fn else 0.0
    # Step 4: F1; 0.0 when precision + recall is 0
    f1 = ___
    return accuracy, precision, recall, f1

for threshold in (0.25, 0.5, 0.75):
    counts = confusion(labels, probs, threshold)
    print(threshold, counts, [round(m, 3) for m in metrics(*counts)])
''',
        answers=(
            "probs >= threshold",
            "int((predicted & ~labels).sum())",
            "tp / (tp + fp) if tp + fp else 0.0",
            "2 * precision * recall / (precision + recall) if precision + recall else 0.0",
        ),
        checks=(
            check("[list(confusion(labels, probs, t)) for t in (0.25, 0.5, 0.75)]", [[8, 6, 6, 0], [5, 10, 2, 3], [3, 12, 0, 5]],
                  "Blanks 1-2: predict positive with `probs >= threshold`; FP counts predicted-positive AND actually-negative.",
                  "الفراغان 1 و2: تنبّأ بالإيجابي بـ `probs >= threshold`؛ ويعدّ FP ما تُنبّئ بأنه إيجابي وهو سلبي فعلًا."),
            check("[round(m, 4) for m in metrics(5, 10, 2, 3)]", [0.75, 0.7143, 0.625, 0.6667],
                  "Blanks 3-4: precision = TP / (TP + FP); F1 = 2·P·R / (P + R).",
                  "الفراغان 3 و4: Precision = TP / (TP + FP)، وF1 = 2·P·R / (P + R)."),
            check("list(metrics(0, 15, 0, 5))", [0.75, 0.0, 0.0, 0.0],
                  "Blanks 3-4: with no predicted positives, return 0.0 instead of dividing by zero.",
                  "الفراغان 3 و4: عند غياب التنبؤات الإيجابية أعد 0.0 بدل القسمة على صفر."),
        ),
        hints=(
            ("A comparison on an array gives a Boolean prediction for every sample.", "المقارنة على مصفوفة تعطي تنبؤًا منطقيًا لكل عينة."),
            ("`~labels` flips True and False, so `predicted & ~labels` marks false positives.", "يقلب `~labels` القيم True وFalse، لذا يحدّد `predicted & ~labels` الإيجابيات الكاذبة."),
            ("Use a conditional expression: `value if denominator else 0.0`.", "استخدم تعبيرًا شرطيًا: `value if denominator else 0.0`."),
        ),
        success=("Correct! Lowering the threshold trades false negatives for false positives, and the guarded formulas never produce an unexplained NaN.",
                 "صحيح! خفض العتبة يستبدل السلبيات الكاذبة بإيجابيات كاذبة، والصيغ المحمية لا تنتج NaN غير مفسَّرة أبدًا."),
        expected=NUMPY_NOTE,
    ),
    "COURSE-003.M13.L01.EX02": Guided(
        goal=("Reproduce the lesson's ratio-based balanced sampling, including the modulo wraparound.",
              "أعد إنتاج أخذ العينات المتوازن بالنسبة كما في الدرس، بما في ذلك الالتفاف بباقي القسمة."),
        steps=(
            ("Decide whether index `ndx` is a negative slot.", "حدّد هل الفهرس `ndx` موضع لعينة سلبية."),
            ("Compute the negative index, wrapping around the list.", "احسب فهرس العينة السلبية مع الالتفاف حول القائمة."),
            ("Compute the positive index, wrapping around the list.", "احسب فهرس العينة الإيجابية مع الالتفاف حول القائمة."),
        ),
        starter='''negative_list = [("neg", i) for i in range(100)]
pos_list = [("pos", i) for i in range(5)]

def sample(ndx, ratio_int):
    """With ratio_int = 2 the pattern is: positive, negative, negative, positive, ..."""
    pos_ndx = ndx // (ratio_int + 1)
    # Step 1: every slot that is not a multiple of (ratio_int + 1) holds a negative
    if ___:
        # Step 2: negatives used so far, wrapped around the negative list
        neg_ndx = ___
        return negative_list[neg_ndx]
    # Step 3: wrap around the (much shorter) positive list
    return pos_list[___]

labels_ratio_1 = [sample(i, 1)[0] for i in range(18)]
labels_ratio_2 = [sample(i, 2)[0] for i in range(18)]
print(labels_ratio_1)
print(labels_ratio_2)
''',
        answers=("ndx % (ratio_int + 1)", "(ndx - 1 - pos_ndx) % len(negative_list)", "pos_ndx % len(pos_list)"),
        checks=(
            check("labels_ratio_1 == ['pos', 'neg'] * 9 and labels_ratio_2 == ['pos', 'neg', 'neg'] * 6", True,
                  "Blank 1: a slot holds a negative when `ndx % (ratio_int + 1)` is not 0.",
                  "الفراغ 1: يحتوي الموضع على عينة سلبية عندما لا يساوي `ndx % (ratio_int + 1)` صفرًا."),
            check("[list(sample(13, 1)), list(sample(251, 1))]", [["neg", 6], ["neg", 25]],
                  "Blank 2: subtract the positives already used (`pos_ndx`) and the slot itself, then wrap with `% len(negative_list)`.",
                  "الفراغ 2: اطرح العينات الإيجابية المستخدمة (`pos_ndx`) والموضع نفسه، ثم التفّ بـ `% len(negative_list)`."),
            check("[list(sample(12, 1)), list(sample(250, 1))]", [["pos", 1], ["pos", 0]],
                  "Blank 3: wrap the positive index with `pos_ndx % len(pos_list)` - there are only 5 positives.",
                  "الفراغ 3: لُفّ فهرس العينات الإيجابية بـ `pos_ndx % len(pos_list)` - فهناك 5 عينات إيجابية فقط."),
        ),
        hints=(
            ("A non-zero remainder is truthy: the remainder of `ndx` divided by one more than the ratio is 0 only on the positive slots.",
             "الباقي غير الصفري يُعدّ صحيحًا: باقي قسمة `ndx` على النسبة زائد واحد يساوي 0 في مواضع العينات الإيجابية فقط."),
            ("By slot `ndx`, `pos_ndx + 1` positives have been placed, so `ndx - 1 - pos_ndx` negatives came before.",
             "عند الموضع `ndx` يكون قد وُضع `pos_ndx + 1` عينات إيجابية، أي أن `ndx - 1 - pos_ndx` عينة سلبية سبقته."),
            ("`% len(...)` keeps any index inside the list by starting over.", "يبقي `% len(...)` أي فهرس داخل القائمة بالبدء من جديد."),
        ),
        success=("Correct! Positives now appear in a fixed ratio, repeating the 5 rare examples many times per epoch.",
                 "صحيح! تظهر العينات الإيجابية الآن بنسبة ثابتة، مع تكرار الأمثلة النادرة الخمسة مرات كثيرة في كل حقبة."),
        reflect=("Why should the validation set keep its natural class balance instead of using this sampler?",
                 "لماذا يجب أن تحتفظ مجموعة التحقق بتوازن فئاتها الطبيعي بدل استخدام أداة أخذ العينات هذه؟"),
    ),
    "COURSE-003.M13.L01.EX03": Guided(
        goal=("Implement flip, offset, in-plane rotation and noise augmentations for a 3D candidate without changing its shape.",
              "نفّذ عمليات التعزيز (augmentation) بالقلب والإزاحة والتدوير داخل المستوى والضوضاء لمرشح ثلاثي الأبعاد دون تغيير أبعاده."),
        steps=(
            ("Mirror the volume along one axis.", "اعكس الحجم على محور واحد."),
            ("Shift the volume by a few voxels along each axis.", "أزِح الحجم ببضعة فوكسلات على كل محور."),
            ("Rotate in the row/column plane only.", "دوّر في مستوى الصفوف والأعمدة فقط."),
            ("Add small Gaussian noise.", "أضف ضوضاء غاوسية صغيرة."),
        ),
        starter='''import numpy as np

candidate = np.zeros((8, 16, 16))          # (index, row, column)
candidate[3:5, 4:7, 2:10] = 1.0            # an asymmetric bright bar, so changes are visible

# Step 1: mirror along one axis
def flip(volume, axis):
    return ___

# Step 2: shift by (d_index, d_row, d_col) voxels, wrapping at the edges
def offset(volume, shift):
    return ___

# Step 3: rotate by k * 90 degrees in the row/column plane (never across CT slices)
def rotate_in_plane(volume, k):
    return ___

# Step 4: Gaussian noise with a small standard deviation
def add_noise(volume, rng, std=0.05):
    return ___

def augment(volume, rng):
    out = volume
    for axis in range(3):
        if rng.random() > 0.5:
            out = flip(out, axis)
    out = offset(out, tuple(int(s) for s in rng.integers(-2, 3, size=3)))
    out = rotate_in_plane(out, int(rng.integers(0, 4)))
    return add_noise(out, rng)

samples = [augment(candidate, np.random.default_rng(seed)) for seed in range(3)]
print([s.shape for s in samples])
''',
        answers=("np.flip(volume, axis=axis)", "np.roll(volume, shift=shift, axis=(0, 1, 2))",
                 "np.rot90(volume, k=k, axes=(1, 2))", "volume + rng.normal(0, std, size=volume.shape)"),
        checks=(
            check("bool(np.array_equal(flip(candidate, 2), candidate[:, :, ::-1]))", True,
                  "Blank 1: `np.flip(volume, axis=axis)` mirrors the chosen axis.", "الفراغ 1: تعكس `np.flip(volume, axis=axis)` المحور المختار."),
            check("bool(np.array_equal(offset(candidate, (1, 0, -2))[4, 4:7, 0:8], np.ones((3, 8))))", True,
                  "Blank 2: shift every axis with `np.roll(volume, shift=shift, axis=(0, 1, 2))`.",
                  "الفراغ 2: أزِح كل محور بـ `np.roll(volume, shift=shift, axis=(0, 1, 2))`."),
            check("bool(np.allclose(rotate_in_plane(candidate, 1).sum(axis=(1, 2)), candidate.sum(axis=(1, 2)))) and not np.array_equal(rotate_in_plane(candidate, 1), candidate)", True,
                  "Blank 3: rotate over `axes=(1, 2)` so each CT slice stays in place.",
                  "الفراغ 3: دوّر على المحاور `axes=(1, 2)` كي تبقى كل شريحة CT في مكانها."),
            check("(lambda n: list(n.shape) == [8, 16, 16] and 0 < float(np.abs(n - candidate).max()) < 0.5)(add_noise(candidate, np.random.default_rng(1)))", True,
                  "Blank 4: add `rng.normal(0, std, size=volume.shape)` to the volume.", "الفراغ 4: أضف `rng.normal(0, std, size=volume.shape)` إلى الحجم."),
            check("all(list(s.shape) == [8, 16, 16] for s in samples)", True,
                  "Every augmentation must keep the shape (8, 16, 16).", "يجب أن يحافظ كل تعزيز على الأبعاد (8, 16, 16)."),
        ),
        hints=(
            ("NumPy has `np.flip`, `np.roll` and `np.rot90` for these three geometric changes.", "يوفّر NumPy الدوال `np.flip` و`np.roll` و`np.rot90` لهذه التغييرات الهندسية الثلاثة."),
            ("`np.roll` accepts a tuple of shifts together with a tuple of axes.", "تقبل `np.roll` صفًّا من الإزاحات مع صفّ من المحاور."),
            ("`np.rot90(volume, k=k, axes=(1, 2))` rotates rows and columns only; noise is `rng.normal(0, std, size=...)`.",
             "تدوّر `np.rot90(volume, k=k, axes=(1, 2))` الصفوف والأعمدة فقط، والضوضاء هي `rng.normal(0, std, size=...)`."),
        ),
        success=("Correct! Every augmentation keeps the candidate's shape and its bright structure, giving the model new but still realistic views of the same nodule.",
                 "صحيح! تحافظ كل عملية تعزيز على أبعاد المرشح وبنيته الساطعة، فتعطي النموذج مناظر جديدة لكن واقعية للعقدة نفسها."),
        expected=(
            "The lesson builds these transforms with `affine_grid` and `grid_sample`; NumPy's flip, roll and rot90 give the same discrete versions and run in the sandbox.",
            "يبني الدرس هذه التحويلات بـ `affine_grid` و`grid_sample`؛ وتعطي flip وroll وrot90 في NumPy النسخ المتقطعة نفسها وتعمل داخل بيئة التدريب.",
        ),
        reflect=("Why is rotating within a CT slice class-preserving, while rotating across slices might not be?",
                 "لماذا يحافظ التدوير داخل شريحة CT على الفئة، بينما قد لا يحافظ عليها التدوير عبر الشرائح؟"),
    ),
    "COURSE-003.M13.L01.EX04": Guided(
        goal=("Read training and validation curves to find where overfitting starts and which epoch to keep.",
              "اقرأ منحنيات التدريب والتحقق لتحديد بداية فرط التخصيص (Overfitting) والحقبة التي يجب الاحتفاظ بها."),
        steps=(
            ("Find the epoch with the lowest validation loss.", "حدّد الحقبة ذات أقل خسارة تحقق."),
            ("Compute the generalization gap for every epoch.", "احسب فجوة التعميم لكل حقبة."),
            ("Pick the epoch with the best validation F1.", "اختر الحقبة ذات أفضل F1 في التحقق."),
            ("Find the best epoch of the run with stronger augmentation.", "حدّد أفضل حقبة في التجربة ذات التعزيز الأقوى."),
        ),
        starter='''train_loss = [0.90, 0.70, 0.55, 0.45, 0.38, 0.32, 0.27, 0.23, 0.20, 0.17,
              0.15, 0.13, 0.11, 0.10, 0.09, 0.08, 0.07, 0.06, 0.06, 0.05]
val_loss = [0.92, 0.75, 0.62, 0.55, 0.51, 0.50, 0.52, 0.56, 0.61, 0.66,
            0.72, 0.78, 0.83, 0.88, 0.93, 0.97, 1.01, 1.05, 1.08, 1.11]
val_f1 = [0.10, 0.25, 0.38, 0.47, 0.53, 0.58, 0.57, 0.55, 0.52, 0.50,
          0.47, 0.45, 0.43, 0.41, 0.40, 0.38, 0.37, 0.36, 0.35, 0.34]
aug_val_loss = [0.93, 0.78, 0.66, 0.58, 0.53, 0.50, 0.48, 0.46, 0.45, 0.44,
                0.44, 0.45, 0.47, 0.50, 0.53, 0.56, 0.60, 0.63, 0.67, 0.70]

# Step 1: epoch number (1-based) with the lowest validation loss
best_epoch = ___
# Step 2: validation minus training loss for every epoch, rounded to 2 decimals
gaps = ___
# Step 3: the epoch (1-based) you would save, judged by validation F1
save_epoch = ___
# Step 4: best epoch (1-based) of the run with stronger augmentation
aug_best_epoch = ___

print("best val loss at epoch", best_epoch, "| save epoch", save_epoch, "| with augmentation", aug_best_epoch)
print("gap:", gaps)
''',
        answers=(
            "val_loss.index(min(val_loss)) + 1",
            "[round(v - t, 2) for t, v in zip(train_loss, val_loss)]",
            "val_f1.index(max(val_f1)) + 1",
            "aug_val_loss.index(min(aug_val_loss)) + 1",
        ),
        checks=(
            check("best_epoch", 6, "Blank 1: find the index of the minimum validation loss and add 1 for a 1-based epoch.",
                  "الفراغ 1: جد فهرس أقل خسارة تحقق وأضف 1 للحصول على رقم الحقبة بدءًا من 1."),
            check("list(gaps)[:3] + list(gaps)[-2:]", [0.02, 0.05, 0.07, 1.02, 1.06],
                  "Blank 2: subtract training loss from validation loss, epoch by epoch.",
                  "الفراغ 2: اطرح خسارة التدريب من خسارة التحقق، حقبة بحقبة."),
            check("save_epoch", 6, "Blank 3: use the epoch with the highest validation F1.", "الفراغ 3: استخدم الحقبة ذات أعلى F1 في التحقق."),
            check("aug_best_epoch", 10,
                  "Blank 4: apply the same rule to `aug_val_loss`; when two epochs tie, `index` returns the first.",
                  "الفراغ 4: طبّق القاعدة نفسها على `aug_val_loss`؛ وعند التساوي تعيد `index` أول حقبة."),
        ),
        hints=(
            ("`list.index(min(list))` gives the position of the smallest value.", "يعطي `list.index(min(list))` موضع أصغر قيمة."),
            ("`zip(train_loss, val_loss)` pairs the two losses of each epoch.", "تقرن `zip(train_loss, val_loss)` خسارتي كل حقبة."),
            ("Positions start at 0 but epochs are numbered from 1.", "تبدأ المواضع من 0 بينما تُرقَّم الحقب من 1."),
        ),
        success=("Correct! Validation loss bottoms out at epoch 6 while training loss keeps falling - the start of overfitting - and stronger augmentation delays the minimum to epoch 10.",
                 "صحيح! تبلغ خسارة التحقق أدناها عند الحقبة 6 بينما تستمر خسارة التدريب في الانخفاض - وهذه بداية فرط التخصيص - ويؤخر التعزيز الأقوى الحد الأدنى إلى الحقبة 10."),
        reflect=("Which epoch would you save, and which metrics justify that choice?", "أي حقبة ستحفظ؟ وما المقاييس التي تبرر هذا الاختيار؟"),
    ),
    "COURSE-003.M14.L01.EX03": Guided(
        goal=("Build a tiny CT-slice-to-mask dataset with a metadata file, then load it back and verify every pair.",
              "ابنِ مجموعة بيانات صغيرة من شرائح CT وأقنعتها مع ملف بيانات وصفية، ثم حمّلها مرة أخرى وتحقّق من كل زوج."),
        steps=(
            ("Name each mask file after its series UID.", "سمِّ كل ملف قناع باسم معرّف السلسلة."),
            ("Write one metadata record per slice.", "اكتب سجل بيانات وصفية واحدًا لكل شريحة."),
            ("Parse the JSON Lines text back into records.", "حلّل نص JSON Lines مرة أخرى إلى سجلات."),
            ("Check that every CT/mask pair exists and has matching dimensions.", "تحقّق من وجود كل زوج CT/قناع ومن تطابق أبعاده."),
        ),
        starter='''import json
import numpy as np

rng = np.random.default_rng(0)
scans = [("1.3.6.1", (12, 30, 40)), ("1.3.6.2", (40, 64, 20)), ("1.3.6.3", (7, 50, 50))]   # (uid, center IRC)

storage = {}        # stands in for the output folder: relative path -> array
metadata = []
for uid, center_irc in scans:
    ct = rng.normal(size=(96, 96))                  # one 2D CT slice
    mask = np.zeros_like(ct, dtype=np.uint8)
    row, col = center_irc[1], center_irc[2]
    mask[row - 2:row + 3, col - 2:col + 3] = 1      # a 5x5 synthetic nodule mask
    ct_name = f"ct/{uid}.npy"
    # Step 1: the matching mask file name
    mask_name = ___
    storage[ct_name] = ct
    storage[mask_name] = mask
    # Step 2: one metadata record per slice
    metadata.append(___)

metadata_jsonl = "\\n".join(json.dumps(record) for record in metadata)

# Step 3: read the JSON Lines text back into a list of records
loaded = ___
# Step 4: every pair exists and the CT and mask have the same shape
pairs_ok = ___
print(len(loaded), "records | pairs ok:", pairs_ok)
''',
        answers=(
            'f"mask/{uid}.npy"',
            '{"series_uid": uid, "center_irc": list(center_irc), "ct_file": ct_name, "mask_file": mask_name}',
            "[json.loads(line) for line in metadata_jsonl.splitlines()]",
            'all(storage[r["ct_file"]].shape == storage[r["mask_file"]].shape for r in loaded)',
        ),
        checks=(
            check("sorted(k for k in storage if k.startswith('mask/'))", ["mask/1.3.6.1.npy", "mask/1.3.6.2.npy", "mask/1.3.6.3.npy"],
                  "Blank 1: mirror the CT name inside a `mask/` folder: `f\"mask/{uid}.npy\"`.",
                  "الفراغ 1: حاكِ اسم ملف CT داخل مجلد `mask/`: `f\"mask/{uid}.npy\"`."),
            check("sorted(metadata[0]) == ['center_irc', 'ct_file', 'mask_file', 'series_uid'] and metadata[1]['center_irc'] == [40, 64, 20]", True,
                  "Blank 2: each record needs `series_uid`, `center_irc`, `ct_file` and `mask_file`.",
                  "الفراغ 2: يحتاج كل سجل إلى `series_uid` و`center_irc` و`ct_file` و`mask_file`."),
            check("len(loaded) == 3 and loaded[2]['mask_file'] == 'mask/1.3.6.3.npy'", True,
                  "Blank 3: parse each line with `json.loads`.", "الفراغ 3: حلّل كل سطر بـ `json.loads`."),
            check("pairs_ok is True or pairs_ok == True", True,
                  "Blank 4: compare `storage[r[\"ct_file\"]].shape` with the mask's shape for every record.",
                  "الفراغ 4: قارن `storage[r[\"ct_file\"]].shape` بأبعاد القناع لكل سجل."),
        ),
        hints=(
            ("The CT file name is `f\"ct/{uid}.npy\"`; the mask follows the same pattern.", "اسم ملف CT هو `f\"ct/{uid}.npy\"`، ويتبع القناع النمط نفسه."),
            ("A metadata record is a dictionary; JSON Lines stores one record per line.", "سجل البيانات الوصفية قاموس، ويخزّن JSON Lines سجلًا في كل سطر."),
            ("`text.splitlines()` gives the lines; `all(...)` checks every record.", "تعطي `text.splitlines()` الأسطر، وتتحقق `all(...)` من كل سجل."),
        ),
        success=("Correct! The dataset is self-describing: every record points to a CT and a mask of the same size, so a training loader can trust it.",
                 "صحيح! أصبحت مجموعة البيانات تصف نفسها: كل سجل يشير إلى صورة CT وقناع بالحجم نفسه، فيمكن لأداة تحميل التدريب الوثوق بها."),
        expected=(
            "The practice sandbox cannot write files, so a dictionary stands in for the output folder; the metadata is real JSON Lines.",
            "لا تستطيع بيئة التدريب كتابة الملفات، لذلك يحل قاموس محل مجلد الإخراج؛ أما البيانات الوصفية فهي JSON Lines حقيقية.",
        ),
    ),
    "COURSE-003.M14.L01.EX04": Guided(
        goal=("Write a correct SegFormer training epoch and validation epoch, with the right mode and gradient handling in each.",
              "اكتب حقبة تدريب وحقبة تحقق صحيحتين لنموذج SegFormer، مع الوضع الصحيح ومعالجة التدرّجات المناسبة في كل منهما."),
        steps=(
            ("Start the training epoch in training mode.", "ابدأ حقبة التدريب في وضع التدريب."),
            ("Backpropagate `outputs.loss` and step AdamW.", "مرّر `outputs.loss` عكسيًا ثم نفّذ خطوة AdamW."),
            ("Start the validation epoch in evaluation mode.", "ابدأ حقبة التحقق في وضع التقييم."),
            ("Run validation without autograd.", "نفّذ التحقق دون autograd."),
        ),
        starter='''import torch

def train_epoch(model, loader, optimizer, device):
    # Step 1: training mode
    ___
    total = 0.0
    for batch in loader:
        pixel_values = batch["pixel_values"].to(device)
        labels = batch["labels"].to(device)
        optimizer.zero_grad(set_to_none=True)
        outputs = model(pixel_values=pixel_values, labels=labels)
        # Step 2: backpropagate the loss the model returns, then update with AdamW
        ___
        ___
        total += outputs.loss.item()
    return total / len(loader)

def validate_epoch(model, loader, device):
    # Step 3: evaluation mode
    ___
    total = 0.0
    # Step 4: no gradients, and never touch the optimizer
    with ___:
        for batch in loader:
            outputs = model(pixel_values=batch["pixel_values"].to(device), labels=batch["labels"].to(device))
            total += outputs.loss.item()
    return total / len(loader)
''',
        answers=("model.train()", "outputs.loss.backward()", "optimizer.step()", "model.eval()", "torch.no_grad()"),
        alternatives={2: ('outputs["loss"].backward()',), 5: ("torch.inference_mode()",)},
        blanks=(
            ("call `model.train()`.", "استدعِ `model.train()`."),
            ("call `outputs.loss.backward()`.", "استدعِ `outputs.loss.backward()`."),
            ("call `optimizer.step()`.", "استدعِ `optimizer.step()`."),
            ("call `model.eval()`.", "استدعِ `model.eval()`."),
            ("use `torch.no_grad()`.", "استخدم `torch.no_grad()`."),
        ),
        hints=(
            ("Hugging Face models return their loss as `outputs.loss` when you pass `labels`.", "تعيد نماذج Hugging Face الخسارة في `outputs.loss` عندما تمرّر `labels`."),
            ("The training step is: zero_grad, forward, backward, step.", "خطوة التدريب هي: zero_grad ثم التمرير الأمامي ثم backward ثم step."),
            ("Validation mirrors training without backward or step, inside `torch.no_grad()`.", "يحاكي التحقق التدريبَ دون backward أو step، داخل `torch.no_grad()`."),
        ),
        success=("Correct! Training updates weights in train mode; validation measures them in eval mode without gradients or optimizer steps.",
                 "صحيح! يحدّث التدريب الأوزان في وضع التدريب، ويقيسها التحقق في وضع التقييم دون تدرّجات أو خطوات مُحسِّن."),
        expected=TORCH_NOTE,
        reflect=("What would go wrong if `validate_epoch` forgot `model.eval()`?", "ما الخطأ الذي سيحدث لو نسيت `validate_epoch` استدعاء `model.eval()`؟"),
    ),
}
