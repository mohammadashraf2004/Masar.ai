"""COURSE-001 Machine Learning Foundations: example answers for written exercises."""

EXAMPLES = {
    "COURSE-001.M01.L01.EX01": (
        """1. Rules: (a) the subject contains "FREE MONEY"; (b) the message has more than five links; (c) the sender's domain is not in the user's contacts.
2. Legitimate emails that break them: (a) a bank newsletter titled "Free money-management workshop"; (b) a university digest with ten links to course pages; (c) a first email from a new colleague at another company.
3. Limitation: every new spam trick needs a new hand-written rule, and the rules start to contradict each other, so the list grows without end and nobody can predict how they interact.
4. With machine learning we collect many emails labelled spam / not spam, turn each one into features (words, links, sender), and let an algorithm learn which combinations predict the label.
5. Rules are transparent but brittle and costly to maintain. A model learned from labelled examples adapts to patterns nobody wrote down and can be retrained as spam changes, but it needs good labelled data and its decisions are harder to explain.""",
        """1. القواعد: (أ) عنوان الرسالة يحتوي "FREE MONEY"؛ (ب) الرسالة تحتوي أكثر من خمسة روابط؛ (ج) نطاق المرسل غير موجود في جهات اتصال المستخدم.
2. رسائل سليمة تخالفها: (أ) نشرة من البنك بعنوان "Free money-management workshop"؛ (ب) نشرة جامعية بها عشرة روابط لصفحات المقررات؛ (ج) أول رسالة من زميل جديد في شركة أخرى.
3. القيد: كل حيلة spam جديدة تحتاج قاعدة جديدة مكتوبة يدويًا، وتبدأ القواعد في التعارض، فتكبر القائمة بلا نهاية ولا يستطيع أحد توقع تفاعلها.
4. في machine learning نجمع رسائل كثيرة مصنفة spam أو not spam، ونحوّل كل رسالة إلى features (الكلمات والروابط والمرسل)، ونترك الخوارزمية تتعلم أي التركيبات تتنبأ بالـ label.
5. القواعد واضحة لكنها هشة ومكلفة في الصيانة. أما النموذج المتعلَّم من أمثلة مصنفة فيلتقط أنماطًا لم يكتبها أحد ويمكن إعادة تدريبه كلما تغيّر الـ spam، لكنه يحتاج بيانات مصنفة جيدة وقراراته أصعب في التفسير.""",
    ),
    "COURSE-001.M01.L01.EX02": (
        """1. Problem: predict whether a telecom customer will cancel (churn) in the next 30 days.
2. One sample: one customer at the end of a billing month.
3. Features: months since joining, number of support calls last month, monthly bill, change in data usage versus the previous month, contract type.
4. Target: churned within the next 30 days (yes/no).
5. User: the retention team, who decide which customers receive an offer.
6. Evidence: support calls, falling usage and month-to-month contracts are known warning signs, so the features carry real signal, though not certainty.
7. Missing: why the customer is unhappy - for example a competitor's better offer or a move abroad - which the billing data does not show.""",
        """1. المشكلة: التنبؤ بما إذا كان عميل شركة الاتصالات سيلغي اشتراكه (churn) خلال الثلاثين يومًا القادمة.
2. العينة الواحدة: عميل واحد في نهاية شهر الفوترة.
3. الـ features: عدد الأشهر منذ الاشتراك، عدد مكالمات الدعم في الشهر الماضي، قيمة الفاتورة الشهرية، التغير في استهلاك البيانات مقارنة بالشهر السابق، نوع العقد.
4. الـ target: هل ألغى خلال الثلاثين يومًا القادمة (نعم/لا).
5. المستخدم: فريق الاحتفاظ بالعملاء الذي يقرر من يتلقى عرضًا.
6. جودة الأدلة: مكالمات الدعم وانخفاض الاستهلاك والعقود الشهرية علامات إنذار معروفة، فالـ features تحمل إشارة حقيقية وإن لم تكن يقينًا.
7. معلومة ناقصة: سبب استياء العميل، مثل عرض أفضل من منافس أو انتقاله لبلد آخر، وهو ما لا تُظهره بيانات الفوترة.""",
    ),
    "COURSE-001.M02.L01.EX01": (
        """1. Fraudulent transaction - classification: the target is a category (fraud / not fraud).
2. Tomorrow's temperature - regression: the target is a continuous number of degrees.
3. Language of a web page - classification: the target is one of a fixed set of languages.
4. Monthly rent - regression: the target is a continuous amount of money.
5. Customer will cancel - classification: the target is a yes/no category.""",
        """1. معاملة احتيالية - classification: الـ target فئة (احتيال / ليس احتيالًا).
2. درجة حرارة الغد - regression: الـ target قيمة عددية متصلة بالدرجات.
3. لغة صفحة الويب - classification: الـ target واحدة من مجموعة لغات محددة.
4. الإيجار الشهري - regression: الـ target مبلغ مالي متصل.
5. هل سيلغي العميل اشتراكه - classification: الـ target فئة نعم/لا.""",
    ),
    "COURSE-001.M02.L01.EX02": (
        """1. Model A suggests underfitting: it is weak even on the data it was trained on (62%), so it has not captured the pattern.
2. Model B generalizes best: high training accuracy (91%) and almost the same test accuracy (89%).
3. Model C suggests overfitting: it is perfect on training data (100%) but much worse on new data (68%).
4. Reasoning: low training and low test scores mean the model is too simple; high training with a small gap means it learned a pattern that transfers; a large gap between training and test means it memorized details of the training set that do not hold for new data.""",
        """1. النموذج A يشير إلى underfitting: ضعيف حتى على بيانات التدريب نفسها (62%)، فلم يلتقط النمط.
2. النموذج B هو الأفضل في generalization: دقة تدريب عالية (91%) ودقة اختبار قريبة جدًا منها (89%).
3. النموذج C يشير إلى overfitting: مثالي على بيانات التدريب (100%) لكنه أسوأ بكثير على بيانات جديدة (68%).
4. التعليل: انخفاض الدقة في التدريب والاختبار معًا يعني أن النموذج بسيط أكثر من اللازم؛ ودقة تدريب عالية مع فجوة صغيرة تعني أنه تعلّم نمطًا ينتقل إلى بيانات جديدة؛ أما الفجوة الكبيرة بين التدريب والاختبار فتعني أنه حفظ تفاصيل بيانات التدريب التي لا تنطبق على غيرها.""",
    ),
    "COURSE-001.M03.L01.EX02": (
        """1. 200 to 20 features before another model - PCA: it is a linear projection that can transform new data the same way, keeping most of the variance.
2. Visualize 64-dimensional digits - t-SNE: it preserves local neighbourhoods in 2D, which makes digit groups visible (it is for visualization only and cannot transform new points).
3. Exactly five segments with representative centers - k-means: you set k=5 and each cluster has a centroid that describes a typical customer.
4. Irregular geographic groups with isolated points left out - DBSCAN: it finds clusters of any shape by density and labels sparse points as noise.
5. Hierarchy shown as a dendrogram - agglomerative clustering: it merges clusters step by step, and the dendrogram shows every level of that hierarchy.""",
        """1. تقليل 200 feature إلى 20 قبل نموذج آخر - PCA: إسقاط خطي يمكن تطبيقه بالطريقة نفسها على بيانات جديدة ويحتفظ بمعظم الـ variance.
2. تصوير أرقام بـ 64 بُعدًا - t-SNE: يحافظ على الجوار المحلي في بُعدين فتظهر مجموعات الأرقام بوضوح (وهو للتصوير فقط ولا يحوّل نقاطًا جديدة).
3. خمس شرائح بالضبط بمراكز ممثِّلة - k-means: نحدد k=5 ولكل مجموعة centroid يصف عميلًا نموذجيًا.
4. مجموعات جغرافية غير منتظمة مع ترك النقاط المعزولة - DBSCAN: يجد مجموعات بأي شكل حسب الكثافة ويصنّف النقاط المتفرقة على أنها noise.
5. تسلسل هرمي يُعرض في dendrogram - agglomerative clustering: يدمج المجموعات خطوة بخطوة، ويُظهر الـ dendrogram كل مستوى من هذا التسلسل.""",
    ),
    "COURSE-001.M04.L01.EX01": (
        """1. Continuous: age, monthly_spend.
2. Categorical: city, membership_type, device_code.
3. device_code is a label, not a quantity: tablet (2) is not "twice" desktop (1). Treating it as continuous would invent an order and distances that do not exist, so it should be one-hot encoded.
4. Plan: ColumnTransformer([("num", StandardScaler(), ["age", "monthly_spend"]), ("cat", OneHotEncoder(handle_unknown="ignore"), ["city", "membership_type", "device_code"])]), placed in a Pipeline before the model.
5. churned is the answer we want to predict. Feeding it in as an input would let the model read the answer, giving perfect but meaningless scores that collapse in production, where the target is unknown.
6. The ColumnTransformer (scaler and encoder) is fitted on the training set only, then the same fitted object transforms the test set, so no test statistics leak into training.""",
        """1. features متصلة: age وmonthly_spend.
2. features فئوية: city وmembership_type وdevice_code.
3. device_code تسمية وليس كمية: الـ tablet (2) ليس "ضعف" الـ desktop (1). معاملته كقيمة متصلة يخترع ترتيبًا ومسافات غير موجودة، لذا يجب ترميزه بـ one-hot encoding.
4. الخطة: ColumnTransformer([("num", StandardScaler(), ["age", "monthly_spend"]), ("cat", OneHotEncoder(handle_unknown="ignore"), ["city", "membership_type", "device_code"])]) داخل Pipeline قبل النموذج.
5. churned هو الإجابة التي نريد التنبؤ بها. إدخاله كـ feature يجعل النموذج يقرأ الإجابة، فيعطي نتائج مثالية بلا معنى تنهار في الإنتاج حيث الـ target غير معروف.
6. يُدرَّب الـ ColumnTransformer (الـ scaler والـ encoder) على بيانات التدريب فقط، ثم يُستخدم الكائن نفسه لتحويل بيانات الاختبار، فلا تتسرب أي إحصاءات من الاختبار إلى التدريب.""",
    ),
    "COURSE-001.M05.L01.EX02": (
        """1. Rare costly disease - recall (with the confusion matrix): it measures how many real cases we catch, so it penalizes false negatives.
2. Expensive follow-up - precision: it measures how many alarms are real, so it penalizes false positives.
3. 99-to-1 imbalance, comparing ranking across thresholds - ROC-AUC: it is threshold-independent and not inflated by the majority class the way accuracy is (a model that always says "negative" already gets 99% accuracy).
4. Ten classes with typical confusions - the confusion matrix: it shows exactly which class is mistaken for which.
5. Pass the chosen metric to model selection with scoring, for example GridSearchCV(model, param_grid, scoring="recall") or cross_val_score(model, X, y, scoring="roc_auc").""",
        """1. مرض نادر مكلف - recall (مع confusion matrix): يقيس كم حالة حقيقية التقطنا، فيعاقب على الـ false negatives.
2. متابعة مكلفة - precision: يقيس كم إنذارًا كان حقيقيًا، فيعاقب على الـ false positives.
3. عدم توازن 99 إلى 1 مع مقارنة الترتيب عبر العتبات - ROC-AUC: لا يعتمد على threshold ولا تضخمه الفئة الغالبة كما يحدث مع accuracy (نموذج يقول "سلبي" دائمًا يحصل على 99% accuracy).
4. عشر فئات مع خلط معتاد بينها - confusion matrix: يوضح بالضبط أي فئة تُخلط بأي فئة.
5. نمرر المقياس المختار لاختيار النموذج عبر scoring، مثل GridSearchCV(model, param_grid, scoring="recall") أو cross_val_score(model, X, y, scoring="roc_auc").""",
    ),
    "COURSE-001.M07.L01.EX02": (
        """1. Target: the department that should handle a message (billing, technical, sales, other). Real-world success: share of messages resolved without being re-routed, and time to first useful reply.
2. Baseline representation: TF-IDF of words and word pairs (bag of words) feeding a linear classifier such as logistic regression.
3. Offline metric: macro-averaged F1, so small departments count as much as large ones.
4. Human review: messages whose top predicted probability is below about 0.6, or where the top two departments are close, go to a human router.
5. Online: an A/B test comparing re-routing rate and resolution time between automatic routing and the current manual process.
6. Production concerns: latency of the routing step, and monitoring drift (new products and new vocabulary), plus privacy of customer messages.
7. Custom transformer: when preprocessing needs domain logic, for example replacing order numbers and e-mail addresses with placeholders, inside the pipeline so training and serving match.
8. Too large for RAM: switch to HashingVectorizer plus an incremental model (SGDClassifier with partial_fit), streaming the data in batches.""",
        """1. الـ target: القسم الذي يجب أن يعالج الرسالة (الفواتير، الدعم الفني، المبيعات، أخرى). النجاح الفعلي: نسبة الرسائل التي تُحل دون إعادة توجيه، والوقت حتى أول رد مفيد.
2. التمثيل المبدئي: TF-IDF للكلمات وأزواج الكلمات (bag of words) يغذي مصنفًا خطيًا مثل logistic regression.
3. مقياس offline: macro-averaged F1 حتى تُحتسب الأقسام الصغيرة بقدر الكبيرة.
4. المراجعة البشرية: الرسائل التي تقل فيها أعلى probability متوقعة عن 0.6 تقريبًا، أو يتقارب فيها أعلى قسمين، تذهب إلى موظف توجيه.
5. Online: اختبار A/B يقارن نسبة إعادة التوجيه ووقت الحل بين التوجيه الآلي والطريقة اليدوية الحالية.
6. مخاوف الإنتاج: زمن الاستجابة (latency) لخطوة التوجيه، ومراقبة الـ drift (منتجات ومفردات جديدة)، إضافة إلى خصوصية رسائل العملاء.
7. Custom transformer: عندما تحتاج المعالجة منطقًا خاصًا بالمجال، مثل استبدال أرقام الطلبات وعناوين البريد برموز، داخل الـ pipeline ليتطابق التدريب مع التشغيل.
8. إذا لم تتسع الذاكرة: ننتقل إلى HashingVectorizer مع نموذج تدريجي (SGDClassifier مع partial_fit) ونمرر البيانات على دفعات.""",
    ),
}
