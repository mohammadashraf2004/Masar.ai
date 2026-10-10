"""COURSE-002 Deep Learning Foundations: example answers (part b)."""

EXAMPLES = {
    "COURSE-002.M04.L01.EX02": (
        """| Scenario | Type | Output units | Final activation | Loss | Metric |
| A. Spam or not | Binary classification | 1 | sigmoid | binary_crossentropy | accuracy (plus precision/recall) |
| B. 25 news topics | Multiclass, single-label | 25 | softmax | categorical_crossentropy (sparse_ if labels are integers) | accuracy |
| C. House price | Scalar regression | 1 | none (linear) | mse | mae |

6. Normalization statistics (mean, standard deviation) must come from the training set only; computing them on validation or test data leaks information about data the model should not have seen and makes the evaluation optimistic.
7. With a few hundred samples one validation split is small, so the score depends heavily on which samples landed in it. K-fold trains and validates K times on different partitions and averages the scores, giving a more stable estimate.
8. MAE 0.27 on a target divided by 100,000 means 0.27 x 100,000 = about 27,000 units of average error in the original scale.""",
        """| الحالة | النوع | وحدات المخرج | الـ activation الأخيرة | الـ loss | المقياس |
| A. spam أم لا | binary classification | 1 | sigmoid | binary_crossentropy | accuracy (مع precision/recall) |
| B. 25 موضوعًا إخباريًا | multiclass بتسمية واحدة | 25 | softmax | categorical_crossentropy (أو sparse_ إذا كانت التسميات أرقامًا) | accuracy |
| C. سعر منزل | scalar regression | 1 | بلا activation (خطية) | mse | mae |

6. يجب أن تُحسب إحصاءات الـ normalization (المتوسط والانحراف المعياري) من مجموعة التدريب فقط؛ فحسابها على الـ validation أو الاختبار يسرّب معلومات عن بيانات لا يجب أن يراها النموذج ويجعل التقييم متفائلًا.
7. مع بضع مئات من العينات تكون مجموعة الـ validation الواحدة صغيرة، فتعتمد النتيجة كثيرًا على العينات التي وقعت فيها. أما K-fold فيدرّب ويتحقق K مرات على تقسيمات مختلفة ويأخذ المتوسط، فيعطي تقديرًا أكثر ثباتًا.
8. قيمة MAE تساوي 0.27 على target مقسوم على 100,000 تعني 0.27 × 100,000 = نحو 27,000 وحدة متوسط خطأ بالمقياس الأصلي.""",
    ),
    "COURSE-002.M05.L01.EX01": (
        """1-2. With 6,000 examples: about 4,000 for training (fit the weights), 1,000 for validation (choose architecture, hyperparameters and number of epochs) and 1,000 for test (one final, unbiased estimate).
3. Every decision made by looking at a score leaks a little information about that data into the model. If the test set is used while tuning, the model is gradually fitted to it and its test score no longer measures performance on truly new data.
4. K-fold validation is preferable when data is scarce or when the validation score varies a lot between random splits: each example is used for validation once and the K scores are averaged.
5. Time-series precaution: split by time, never randomly - train on the past, validate and test on later periods - otherwise the model sees the future and the evaluation is unrealistically good.""",
        """1-2. مع 6,000 مثال: نحو 4,000 للتدريب (ضبط الـ weights)، و1,000 للـ validation (اختيار البنية والـ hyperparameters وعدد الـ epochs)، و1,000 للاختبار (تقدير نهائي واحد غير منحاز).
3. كل قرار يُتخذ بالنظر إلى نتيجة ما يسرّب قليلًا من المعلومات عن تلك البيانات إلى النموذج. إذا استُخدمت مجموعة الاختبار أثناء الضبط فإن النموذج يتكيف معها تدريجيًا، فلا تعود نتيجتها تقيس الأداء على بيانات جديدة فعلًا.
4. يُفضَّل K-fold validation عندما تكون البيانات قليلة أو تتغير نتيجة الـ validation كثيرًا بين التقسيمات العشوائية: يُستخدم كل مثال للتحقق مرة واحدة ويؤخذ متوسط النتائج K.
5. احتياط السلاسل الزمنية: التقسيم حسب الزمن لا عشوائيًا - التدريب على الماضي والتحقق والاختبار على فترات لاحقة - وإلا رأى النموذج المستقبل وصار التقييم جيدًا بشكل غير واقعي.""",
    ),
    "COURSE-002.M05.L01.EX02": (
        """1-2. This is overfitting: after epoch 7 the model keeps fitting details specific to the training data that do not hold for new data. The goal is performance on unseen data, so the lowest training loss is not what we want - validation loss is the measure that matters.
3. Interventions: stop training around epoch 7 (early stopping, keeping the best validation checkpoint); make the model smaller (fewer layers or units); add L2 weight regularization; add dropout; get more training data or use augmentation.
4. Dropout randomly zeroes a fraction of a layer's outputs during training, so the network cannot rely on fragile co-adapted features and has to learn more robust patterns; L2 regularization instead limits capacity by penalizing large weights.
5. Change one thing at a time, train with the same data splits, and compare the minimum validation loss and the epoch where it occurs; keep the change only if validation performance improves, and check the final choice once on the test set.""",
        """1-2. هذا overfitting: بعد الـ epoch السابعة يستمر النموذج في التكيف مع تفاصيل خاصة ببيانات التدريب لا تنطبق على بيانات جديدة. الهدف هو الأداء على البيانات غير المرئية، فأقل training loss ليس ما نريده - الـ validation loss هو المقياس المهم.
3. التدخلات: إيقاف التدريب قرب الـ epoch السابعة (early stopping مع الاحتفاظ بأفضل checkpoint)؛ تصغير النموذج (طبقات أو وحدات أقل)؛ إضافة L2 weight regularization؛ إضافة dropout؛ زيادة بيانات التدريب أو استخدام augmentation.
4. يصفّر الـ dropout نسبة عشوائية من مخرجات الطبقة أثناء التدريب، فلا تستطيع الشبكة الاعتماد على features هشة متكاتفة وتضطر لتعلم أنماط أكثر متانة؛ أما L2 فيقيّد السعة بمعاقبة الـ weights الكبيرة.
5. أغيّر شيئًا واحدًا كل مرة وأدرّب بالتقسيمات نفسها، ثم أقارن أقل validation loss والـ epoch التي حدثت فيها؛ أحتفظ بالتغيير فقط إذا تحسن أداء الـ validation، ثم أتحقق من الاختيار النهائي مرة واحدة على مجموعة الاختبار.""",
    ),
    "COURSE-002.M06.L01.EX01": (
        """1. Inputs: amount, merchant category, time of day, country of card vs. merchant, device and IP information, the customer's recent transaction history.
2. Target: whether the transaction is fraudulent (confirmed later by chargeback or investigation).
3. Task: binary classification on highly imbalanced data.
4. Data: historical transactions with confirmed fraud labels, covering several months and all payment channels.
5. Sampling bias: if only transactions flagged by the old rule system were investigated, fraud the rules missed is labelled "legitimate".
6. Target leakage: a "chargeback_filed" or "account_frozen" field that is only known after the fraud was discovered.
7. Metrics: precision (how many alerts are real, since analysts' time is limited) and recall (how much fraud is caught); PR-AUC summarizes both under imbalance. Accuracy is useless because "never fraud" already scores above 99%.
8. Split by time: train on older months, validate on the next month, test on the most recent month, so evaluation mimics future use.
9. Baseline: the current rule system, or "flag every transaction above a fixed amount" - the model must beat it on precision/recall.
10. Train a larger model until training metrics keep improving while validation metrics stall or drop; once that happens the model has enough capacity to overfit.
11. Experiments: class weighting for the imbalance; dropout or L2, and tuning the decision threshold on validation data.
12. Only once, after all choices are frozen, to report the final expected performance.""",
        """1. المدخلات: المبلغ، فئة التاجر، وقت المعاملة، دولة البطاقة مقابل دولة التاجر، معلومات الجهاز والـ IP، سجل معاملات العميل الأخيرة.
2. الـ target: هل المعاملة احتيالية (يُؤكَّد لاحقًا عبر chargeback أو تحقيق).
3. المهمة: binary classification على بيانات شديدة عدم التوازن.
4. البيانات: معاملات تاريخية بتسميات احتيال مؤكدة تغطي عدة أشهر وكل قنوات الدفع.
5. انحياز العينة (sampling bias): إذا لم يُحقَّق إلا في المعاملات التي أشار إليها نظام القواعد القديم، فإن الاحتيال الذي فاتته القواعد يُسمّى "سليمًا".
6. تسرب الـ target: حقل مثل "chargeback_filed" أو "account_frozen" لا يُعرف إلا بعد اكتشاف الاحتيال.
7. المقاييس: precision (كم إنذارًا حقيقي، لأن وقت المحللين محدود) وrecall (كم من الاحتيال اكتُشف)؛ ويلخصهما PR-AUC مع عدم التوازن. أما accuracy فلا فائدة منها لأن "لا احتيال أبدًا" يحقق أكثر من 99%.
8. التقسيم حسب الزمن: التدريب على الأشهر الأقدم، والـ validation على الشهر التالي، والاختبار على أحدث شهر، ليحاكي التقييم الاستخدام المستقبلي.
9. الـ baseline: نظام القواعد الحالي، أو "علّم كل معاملة فوق مبلغ ثابت" - ويجب أن يتفوق النموذج عليه في precision/recall.
10. أدرّب نموذجًا أكبر حتى تستمر مقاييس التدريب في التحسن بينما تتوقف مقاييس الـ validation أو تنخفض؛ عندها تكون لدى النموذج سعة كافية للـ overfitting.
11. التجارب: class weighting لمعالجة عدم التوازن؛ وdropout أو L2 مع ضبط عتبة القرار على بيانات الـ validation.
12. مرة واحدة فقط، بعد تثبيت كل الاختيارات، لتقرير الأداء النهائي المتوقع.""",
    ),
    "COURSE-002.M06.L01.EX02": (
        """A. Spam detector for end-to-end encrypted messages - on-device: the server never sees plaintext, so the model must run where messages are decrypted; it needs low latency and must work offline on modest phone hardware. Quantization (and pruning) help fit a small, fast model on the phone. Monitor: share of messages flagged, user "not spam" reports. New examples: users' explicit spam reports, shared only with consent. Drift: spammers switch to new wording or link formats.
B. Streaming recommendations - server/API: catalog, viewing history and heavy models live in the cloud, connectivity is assumed, and a few hundred milliseconds of latency is acceptable. Optimization is optional (cost), not essential. Monitor: click-through and watch time per recommendation, plus serving latency. New examples: logged impressions, clicks and watch time. Drift: tastes shift when a popular new series is released.
C. Factory defect removal - on-device/edge next to the belt: decisions must be made in milliseconds and cannot depend on a network connection. Quantization or pruning help reach real-time speed on embedded hardware. Monitor: inference latency and rejection rate (plus spot checks of false rejects). New examples: images of rejected and sampled accepted items reviewed by inspectors. Drift: a new supplier changes the colour or texture of the products.
A/B test (B): show half of the users the new recommender and half the current one, and compare watch time and retention over several weeks before switching everyone.""",
        """A. كاشف spam لرسائل مشفرة end-to-end - على الجهاز (on-device): الخادم لا يرى النص الصريح، فيجب أن يعمل النموذج حيث تُفك الرسائل؛ ويحتاج latency منخفضًا ويجب أن يعمل دون اتصال على عتاد هاتف متواضع. يساعد الـ quantization (والـ pruning) على تشغيل نموذج صغير وسريع على الهاتف. المراقبة: نسبة الرسائل المعلَّمة، وبلاغات المستخدم "ليست spam". الأمثلة الجديدة: بلاغات spam الصريحة من المستخدمين، تُشارك فقط بموافقتهم. الـ drift: انتقال المرسلين إلى صياغات أو أشكال روابط جديدة.
B. توصيات منصة البث - خادم/API: الكتالوج وسجل المشاهدة والنماذج الثقيلة في السحابة، والاتصال متوفر، وبضع مئات من الملّي ثانية مقبولة. التحسين اختياري (للتكلفة) لا أساسي. المراقبة: click-through ووقت المشاهدة لكل توصية، وlatency الخدمة. الأمثلة الجديدة: سجلات العرض والنقرات ووقت المشاهدة. الـ drift: تتغير الأذواق عند صدور مسلسل جديد شهير.
C. إزالة العيوب في المصنع - على الجهاز/الحافة بجوار السير: يجب اتخاذ القرار في ملّي ثوانٍ ولا يمكن الاعتماد على الشبكة. يساعد الـ quantization أو الـ pruning على تحقيق السرعة اللحظية على عتاد مدمج. المراقبة: latency الاستدلال ونسبة الرفض (مع فحص عينات من حالات الرفض الخاطئ). الأمثلة الجديدة: صور القطع المرفوضة وعينة من المقبولة يراجعها المفتشون. الـ drift: مورّد جديد يغيّر لون المنتجات أو ملمسها.
اختبار A/B (للنظام B): يرى نصف المستخدمين نظام التوصية الجديد والنصف الآخر الحالي، ونقارن وقت المشاهدة والاحتفاظ بالمستخدمين لعدة أسابيع قبل التحويل للجميع.""",
    ),
    "COURSE-002.M08.L01.EX01": (
        """1. One image: (180, 180, 3).
2. Binary classification: healthy vs. diseased.
3. Final layer: Dense(1, activation="sigmoid").
4. Loss: binary_crossentropy.
5. Sketch: Input(180,180,3) -> Rescaling(1/255) -> Conv2D(32,3,relu) -> MaxPooling2D -> Conv2D(64,3,relu) -> MaxPooling2D -> Conv2D(128,3,relu) -> MaxPooling2D -> Conv2D(256,3,relu) -> Flatten -> Dropout(0.5) -> Dense(1, sigmoid).
6. Pooling and convolution shrink height and width, while deeper layers need more channels to represent more, and more abstract, patterns; trading spatial resolution for feature depth keeps computation manageable.
7. Augmentation: random horizontal flips, small random rotations, random zoom (or brightness changes) - leaves can appear in any of these variations.
8. Augmentation creates new training variations to reduce overfitting; evaluation must measure the model on the real images as they are, and random changes would make test results noisy and not reproducible.
9. Training accuracy keeps rising toward 100% while validation accuracy plateaus or falls (validation loss rises).
10. A ModelCheckpoint with save_best_only=True on val_loss keeps the weights from the epoch with the best validation performance, so later overfitting epochs do not overwrite the best model.""",
        """1. الصورة الواحدة: (180, 180, 3).
2. binary classification: سليمة أم مريضة.
3. الطبقة الأخيرة: Dense(1, activation="sigmoid").
4. الـ loss: binary_crossentropy.
5. المخطط: Input(180,180,3) -> Rescaling(1/255) -> Conv2D(32,3,relu) -> MaxPooling2D -> Conv2D(64,3,relu) -> MaxPooling2D -> Conv2D(128,3,relu) -> MaxPooling2D -> Conv2D(256,3,relu) -> Flatten -> Dropout(0.5) -> Dense(1, sigmoid).
6. يصغّر الـ pooling والـ convolution الارتفاع والعرض، بينما تحتاج الطبقات الأعمق قنوات أكثر لتمثيل أنماط أكثر وأكثر تجريدًا؛ ومبادلة الدقة المكانية بعمق الـ features تبقي الحساب ممكنًا.
7. الـ augmentation: قلب أفقي عشوائي، دوران صغير عشوائي، تكبير عشوائي (أو تغيير السطوع) - فالأوراق قد تظهر بأي من هذه الأشكال.
8. ينشئ الـ augmentation أشكالًا جديدة من صور التدريب لتقليل الـ overfitting؛ أما التقييم فيجب أن يقيس النموذج على الصور الحقيقية كما هي، والتغييرات العشوائية تجعل نتائج الاختبار مشوشة وغير قابلة للتكرار.
9. تستمر training accuracy في الارتفاع نحو 100% بينما تثبت validation accuracy أو تنخفض (وترتفع الـ validation loss).
10. يحتفظ ModelCheckpoint مع save_best_only=True على val_loss بـ weights الـ epoch صاحبة أفضل أداء validation، فلا تكتب الـ epochs اللاحقة المصابة بالـ overfitting فوق أفضل نموذج.""",
    ),
    "COURSE-002.M08.L01.EX02": (
        """1. Load a backbone pretrained on ImageNet (for example Xception or ResNet) with include_top=False and put a new small classifier on top of its features.
2. Remove the original classification head (its 1000-class Dense layers) and replace it with pooling plus a Dense layer sized for my classes.
3. Freeze the entire pretrained backbone at first.
4. Train only the new head until it converges; then unfreeze the top few layers of the backbone, recompile, and train again jointly.
5. A low learning rate makes small adjustments to features that are already good; large updates would destroy the pretrained representations, especially while the new head's errors are still large.
6. Residual block: x -> [Conv -> BN -> ReLU -> Conv -> BN] = main path; the shortcut carries x unchanged; output = ReLU(main + shortcut).
7. The shapes must match for the addition, so the shortcut needs a 1x1 Conv2D with 64 filters (and the same stride) to project x from 32 to 64 channels.
8. Conv2D (without bias/activation) -> BatchNormalization -> ReLU.
9. Depthwise separable convolution: first a depthwise convolution filters each input channel spatially on its own, then a 1x1 pointwise convolution mixes the channels.
10. It needs far fewer parameters than a regular convolution, so the model has less capacity to memorize a small dataset while keeping strong spatial features.
11. MHR: build models as a modular hierarchy of repeated blocks (modularity, hierarchy, reuse) - stacks of similar blocks whose feature depth grows as resolution shrinks, with residual connections - instead of hand-designing every layer.""",
        """1. أحمّل backbone مدرَّبًا مسبقًا على ImageNet (مثل Xception أو ResNet) مع include_top=False وأضع مصنفًا صغيرًا جديدًا فوق الـ features الخاصة به.
2. أزيل رأس التصنيف الأصلي (طبقات Dense ذات الألف فئة) وأستبدله بـ pooling ثم طبقة Dense بحجم فئاتي.
3. أجمّد الـ backbone المدرَّب مسبقًا بالكامل في البداية.
4. أدرّب الرأس الجديد فقط حتى يستقر؛ ثم أفك تجميد الطبقات العليا القليلة من الـ backbone وأعيد compile وأدرّب معًا.
5. الـ learning rate المنخفض يجري تعديلات صغيرة على features جيدة أصلًا؛ أما التحديثات الكبيرة فتدمر التمثيلات المدرَّبة مسبقًا، خاصة ما دامت أخطاء الرأس الجديد كبيرة.
6. الـ residual block: x -> [Conv -> BN -> ReLU -> Conv -> BN] = المسار الرئيسي؛ والـ shortcut ينقل x دون تغيير؛ والمخرج = ReLU(main + shortcut).
7. يجب أن تتطابق الأشكال للجمع، لذا يحتاج الـ shortcut إلى Conv2D بحجم 1x1 و64 filter (وبنفس الـ stride) لإسقاط x من 32 إلى 64 قناة.
8. Conv2D (بلا bias أو activation) -> BatchNormalization -> ReLU.
9. الـ depthwise separable convolution: أولًا depthwise convolution ترشّح كل قناة مدخل مكانيًا وحدها، ثم pointwise convolution بحجم 1x1 تمزج القنوات.
10. تحتاج parameters أقل بكثير من الـ convolution العادية، فتقل قدرة النموذج على حفظ مجموعة بيانات صغيرة مع الحفاظ على features مكانية قوية.
11. مبدأ MHR: بناء النماذج كتسلسل هرمي من كتل متكررة (modularity, hierarchy, reuse) - رصّات من كتل متشابهة يزداد عمق features فيها كلما صغرت الدقة المكانية، مع residual connections - بدلًا من تصميم كل طبقة يدويًا.""",
    ),
    "COURSE-002.M10.L01.EX01": (
        """3. The progression is expected: early layers act as generic detectors of edges, colours and textures, so the image is still recognizable in their activations; each deeper layer combines the previous ones into more abstract, class-related concepts ("ear", "eye"), which look less and less like the original image.
4. A blank channel means the pattern that filter detects is not present in this image - the filter simply did not fire here, not that it is broken.
5. Information distillation: as the image passes through the network, information irrelevant to the task (exact pixels, visual details) is progressively discarded while information about the class is refined and amplified. The deep, sparse activations are a compact summary of "what is in the image" rather than "what it looks like", much as a person remembers that they saw a cat without remembering its exact pixels.""",
        """3. هذا التدرج متوقع: الطبقات الأولى تعمل ككواشف عامة للحواف والألوان والقوام، فتظل الصورة معروفة في activations الخاصة بها؛ وكل طبقة أعمق تجمع ما قبلها في مفاهيم أكثر تجريدًا ومرتبطة بالفئة ("أذن"، "عين")، فتبدو أقل فأقل شبهًا بالصورة الأصلية.
4. القناة الفارغة تعني أن النمط الذي يكشفه ذلك الـ filter غير موجود في هذه الصورة - أي أن الـ filter لم ينشط هنا، لا أنه معطل.
5. تقطير المعلومات (information distillation): مع مرور الصورة عبر الشبكة تُستبعد تدريجيًا المعلومات غير المهمة للمهمة (الـ pixels الدقيقة والتفاصيل المرئية) بينما تُنقّى المعلومات المتعلقة بالفئة وتُضخَّم. فالـ activations العميقة المتفرقة ملخص مضغوط لـ "ما في الصورة" لا "كيف تبدو"، كما يتذكر الإنسان أنه رأى قطة دون أن يتذكر الـ pixels بدقة.""",
    ),
    "COURSE-002.M10.L01.EX02": (
        """3. The heatmap shows the decision depends on grass, not the dog: the model has probably learned a spurious correlation - in training, most dog photos were taken outdoors on grass - so "grass" became a shortcut for "dog". It will likely fail on dogs indoors and may call a lawn with no dog "dog".
4. Changes: (a) rebalance the data - add dogs on varied backgrounds (indoors, snow, beach) and non-dog images on grass; (b) augment with crops focused on the animal or background replacement so the background stops being predictive.
5. Verification: rerun Grad-CAM on the same and new images to confirm the heatmap now covers the dog, and evaluate on a held-out set built to break the shortcut (dogs without grass, grass without dogs), comparing accuracy before and after.""",
        """3. توضح الـ heatmap أن القرار يعتمد على العشب لا على الكلب: غالبًا تعلّم النموذج ارتباطًا زائفًا (spurious correlation) - ففي التدريب التُقطت معظم صور الكلاب في الخارج على العشب - فصار "العشب" اختصارًا لـ "كلب". والأرجح أنه سيفشل مع الكلاب داخل المنازل وقد يسمّي مرجًا بلا كلب "dog".
4. التغييرات: (أ) إعادة توازن البيانات - إضافة كلاب على خلفيات متنوعة (داخل المنزل، ثلج، شاطئ) وصور بلا كلاب على العشب؛ (ب) augmentation بقصّ يركز على الحيوان أو استبدال الخلفية حتى لا تعود الخلفية مؤشرًا.
5. التحقق: إعادة Grad-CAM على الصور نفسها وصور جديدة للتأكد من أن الـ heatmap تغطي الكلب الآن، والتقييم على مجموعة held-out مصممة لكسر الاختصار (كلاب بلا عشب، عشب بلا كلاب)، مع مقارنة الدقة قبل التغيير وبعده.""",
    ),
    "COURSE-002.M11.L01.EX01": (
        """2. Target mask: an image of the same height and width where each pixel holds a class - for example 1 = product, 0 = background (optionally 2 = uncertain border).
3. Encoder-decoder: Input -> Conv2D(64, 3, strides=2) -> Conv2D(128, 3, strides=2) -> Conv2D(256, 3, strides=2) [encoder, smaller and deeper] -> Conv2DTranspose(256, 3, strides=2) -> Conv2DTranspose(128, 3, strides=2) -> Conv2DTranspose(64, 3, strides=2) [decoder, back to full size] -> Conv2D(num_classes, 3, activation="softmax") giving a class per pixel.
4. Classification only needs to know what is in the image, so it can throw away location; segmentation must say exactly where every product pixel is, so spatial detail has to be preserved and restored in the output.
5. IoU = area of overlap between predicted and true product mask / area of their union, computed per image and averaged; masks above a threshold (for example 0.9) are accepted.
6. With SAM a labeller clicks a point or draws a box on each product and the model proposes the full mask; the labeller only corrects mistakes instead of tracing every outline by hand.""",
        """2. الـ mask الهدف: صورة بنفس الارتفاع والعرض يحمل كل pixel فيها فئة - مثل 1 = منتج و0 = خلفية (واختياريًا 2 = حد غير مؤكد).
3. الـ encoder-decoder: Input -> Conv2D(64, 3, strides=2) -> Conv2D(128, 3, strides=2) -> Conv2D(256, 3, strides=2) [الـ encoder: أصغر وأعمق] -> Conv2DTranspose(256, 3, strides=2) -> Conv2DTranspose(128, 3, strides=2) -> Conv2DTranspose(64, 3, strides=2) [الـ decoder: يعود للحجم الكامل] -> Conv2D(num_classes, 3, activation="softmax") يعطي فئة لكل pixel.
4. التصنيف يكفيه معرفة ما في الصورة فيستطيع إهمال الموقع؛ أما الـ segmentation فيجب أن يحدد بالضبط مكان كل pixel من المنتج، لذا يجب الحفاظ على التفاصيل المكانية واستعادتها في المخرج.
5. الـ IoU = مساحة التداخل بين mask المنتج المتوقع والحقيقي ÷ مساحة اتحادهما، يُحسب لكل صورة ويؤخذ المتوسط؛ وتُقبل الـ masks فوق عتبة (مثل 0.9).
6. مع SAM ينقر المصنِّف نقطة أو يرسم مربعًا على كل منتج فيقترح النموذج الـ mask كاملًا؛ ويكتفي المصنِّف بتصحيح الأخطاء بدلًا من رسم كل حد يدويًا.""",
    ),
    "COURSE-002.M11.L01.EX02": (
        """2. Object detection: counting requires finding each individual box and its location; classification only says "boxes are present", and segmentation gives pixel masks that are slower and more than counting needs.
3. Each grid cell predicts a few bounding boxes - centre x, y, width, height - each with a confidence (objectness) score, plus class probabilities (here: "box").
4. The cell that contains the centre of the object's ground-truth box is responsible for predicting that object.
5. During training the confidence target for the responsible predictor is set from the IoU between its predicted box and the true box, so confidence learns to mean "there is an object and my box fits it well"; predictors with no object get target 0.
6. A pretrained single-stage detector (one network pass, no separate proposal stage) is fast enough for real-time video, and pretraining on a large dataset means a small set of conveyor images is enough to fine-tune it, instead of the huge labelled dataset training from scratch would need.""",
        """2. الـ object detection: العدّ يتطلب العثور على كل صندوق على حدة وموقعه؛ أما الـ classification فيقول فقط "توجد صناديق"، والـ segmentation يعطي masks على مستوى الـ pixel أبطأ وأكثر مما يحتاجه العدّ.
3. تتنبأ كل خلية في الشبكة (grid) ببضعة bounding boxes - مركز x وy والعرض والارتفاع - لكل منها درجة confidence (objectness)، إضافة إلى probabilities الفئات (هنا: "box").
4. الخلية التي يقع فيها مركز الصندوق الحقيقي للكائن هي المسؤولة عن التنبؤ به.
5. أثناء التدريب يُضبط هدف الـ confidence للمتنبئ المسؤول من الـ IoU بين صندوقه المتوقع والصندوق الحقيقي، فيتعلم أن الـ confidence تعني "يوجد كائن وصندوقي يطابقه جيدًا"؛ والمتنبئات التي لا يوجد عندها كائن هدفها 0.
6. الكاشف أحادي المرحلة المدرَّب مسبقًا (مرور واحد عبر الشبكة بلا مرحلة مقترحات منفصلة) سريع بما يكفي للفيديو اللحظي، والتدريب المسبق على مجموعة كبيرة يعني أن عددًا قليلًا من صور السير يكفي لضبطه، بدلًا من البيانات المصنفة الضخمة التي يحتاجها التدريب من الصفر.""",
    ),
    "COURSE-002.M13.L01.EX01": (
        """1. Chronological split: the first ~50% of the period for training, the next ~25% for validation, the last ~25% for testing.
2. Random mixing would let the model train on hours that come after the hours it is tested on; it would "know the future" (for example the weather that week), so the evaluation would be optimistic and not reflect real forecasting.
3. 7 days x 24 hours = 168 timesteps.
4. One sample: (168, 10).
5. Baseline: predict that demand 24 hours from now equals demand at the same hour today (a persistence/seasonal-naive forecast).
6. If a learned model cannot beat this zero-effort rule, its extra complexity adds nothing; the baseline sets the minimum useful error.
7. Flattening destroys the order of time: the Dense layer sees 1,680 unrelated numbers and must relearn that neighbouring hours are related and that the most recent hours matter most.
8. Not automatically. Conv1D assumes the same local pattern means the same thing wherever it appears in the window (translation invariance); for forecasting, recent hours matter more than old ones, so that assumption should be checked - for example by comparing against the baseline and a recurrent model on validation data.""",
        """1. تقسيم زمني: أول ~50% من الفترة للتدريب، و~25% التالية للـ validation، وآخر ~25% للاختبار.
2. الخلط العشوائي يسمح للنموذج بالتدريب على ساعات تأتي بعد الساعات التي يُختبر عليها؛ فيكون "عالمًا بالمستقبل" (مثل طقس ذلك الأسبوع)، فيصبح التقييم متفائلًا ولا يعكس التنبؤ الحقيقي.
3. 7 أيام × 24 ساعة = 168 timestep.
4. العينة الواحدة: (168, 10).
5. الـ baseline: التنبؤ بأن الطلب بعد 24 ساعة يساوي الطلب في الساعة نفسها اليوم (persistence أو seasonal-naive).
6. إذا لم يتفوق النموذج المتعلَّم على هذه القاعدة التي لا تتطلب جهدًا، فإن تعقيده الإضافي لا يضيف شيئًا؛ فالـ baseline يحدد أقل خطأ مفيد.
7. الـ flattening يدمّر ترتيب الزمن: ترى طبقة Dense ‏1,680 رقمًا غير مترابط وعليها أن تتعلم من جديد أن الساعات المتجاورة مرتبطة وأن الساعات الأحدث أهم.
8. ليس تلقائيًا. يفترض Conv1D أن النمط المحلي نفسه يعني الشيء نفسه أينما ظهر في النافذة (translation invariance)؛ وفي التنبؤ تكون الساعات الأحدث أهم من القديمة، لذا يجب التحقق من هذا الافتراض - مثلًا بالمقارنة مع الـ baseline ومع نموذج recurrent على بيانات الـ validation.""",
    ),
}
