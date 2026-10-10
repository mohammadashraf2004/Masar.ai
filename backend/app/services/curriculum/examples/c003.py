"""COURSE-003 Applied Deep Learning: example answers for written exercises."""

EXAMPLES = {
    "COURSE-003.M01.L01.EX01": (
        """1. Manual feature engineering - a person decides that "number of loops" matters and computes it before the model sees the data.
2. Representation learning - the network starts from raw pixels and its filters are learned from the labelled examples.
3. Manual feature engineering - the ratios are designed by an engineer from domain knowledge, not learned.
4. Representation learning - the intermediate features change during training in response to the loss.
Deep learning does not make domain knowledge irrelevant: experts are still needed to frame the problem, choose and clean the data, define the labels and decide whether the model's behaviour makes sense.""",
        """1. هندسة features يدوية - شخص قرر أن "عدد الحلقات" مهم وحسبه قبل أن يرى النموذج البيانات.
2. تعلّم التمثيل (representation learning) - تبدأ الشبكة من الـ pixels الخام وتُتعلَّم الـ filters من الأمثلة المصنفة.
3. هندسة features يدوية - النسب صممها مهندس من معرفة المجال ولم تُتعلَّم.
4. تعلّم التمثيل - تتغير الـ features الوسيطة أثناء التدريب استجابةً للـ loss.
الـ deep learning لا يجعل معرفة المجال بلا قيمة: ما زلنا نحتاج الخبراء لصياغة المشكلة واختيار البيانات وتنظيفها وتحديد التسميات والحكم على منطقية سلوك النموذج.""",
    ),
    "COURSE-003.M01.L01.EX02": (
        """1. Order: raw data -> Dataset -> DataLoader -> untrained model -> loss function -> optimizer (training loop) -> trained model -> deployment.
2. The Dataset turns problem-specific samples (files, records) into PyTorch-ready examples: a tensor input and its label.
3. The DataLoader groups examples into shuffled batches (optionally loading them in parallel workers) for the training loop.
4. The loss function measures how far the model's outputs are from the targets: one number the training process tries to reduce.
5. Autograd computes the gradient of the loss with respect to every parameter; the optimizer uses those gradients to update the parameters.
6. Deployment has different requirements from training - latency, memory, hardware, a stable serving interface and monitoring - so the trained model usually has to be exported and integrated separately.""",
        """1. الترتيب: البيانات الخام -> Dataset -> DataLoader -> نموذج غير مدرَّب -> loss function -> optimizer (حلقة التدريب) -> نموذج مدرَّب -> deployment.
2. يحوّل الـ Dataset العينات الخاصة بالمشكلة (ملفات أو سجلات) إلى أمثلة جاهزة لـ PyTorch: مدخل tensor مع التسمية الخاصة به.
3. يجمع الـ DataLoader الأمثلة في دفعات مخلوطة (وقد يحمّلها عبر workers متوازية) لحلقة التدريب.
4. تقيس الـ loss function مدى بُعد مخرجات النموذج عن الـ targets: رقم واحد تحاول عملية التدريب تقليله.
5. يحسب autograd الـ gradient للـ loss بالنسبة لكل parameter؛ ويستخدم الـ optimizer هذه الـ gradients لتحديث الـ parameters.
6. للـ deployment متطلبات مختلفة عن التدريب - زمن الاستجابة والذاكرة والعتاد وواجهة تشغيل مستقرة والمراقبة - لذا يُصدَّر النموذج المدرَّب ويُدمج عادةً في مرحلة منفصلة.""",
    ),
    "COURSE-003.M02.L01.EX01": (
        """1. Open the JPEG -> convert to RGB -> resize and centre-crop to the model's input size (for example 224x224) -> convert to a tensor -> normalize with the training mean/std -> add a batch dimension -> model.eval() and run under torch.no_grad() -> take the output scores -> softmax -> pick the top index -> map it to the class name.
2. The model learned its weights on images prepared in exactly that way; different sizes or pixel statistics give it inputs unlike anything it saw, and accuracy drops.
3. Models process batches: they expect a tensor of shape (N, C, H, W), so a single image becomes N=1.
4. eval() switches layers such as dropout and batch normalization to inference behaviour; in training mode they behave randomly or use batch statistics, giving inconsistent predictions.
5. Raw outputs (logits) are unnormalized scores; softmax turns them into values between 0 and 1 that sum to 1; the label is the class name of the highest value.
6. Softmax always distributes 100% across the 1,000 known classes. If the subject is not one of them, the model still has to choose a class, and it can do so with high softmax confidence - confidence is not proof of correctness.""",
        """1. فتح الـ JPEG -> التحويل إلى RGB -> تغيير الحجم والقص من المركز إلى حجم مدخل النموذج (مثل 224×224) -> التحويل إلى tensor -> الـ normalization بمتوسط وانحراف بيانات التدريب -> إضافة بُعد الدفعة -> model.eval() والتشغيل داخل torch.no_grad() -> أخذ درجات المخرج -> softmax -> اختيار أعلى فهرس -> تحويله إلى اسم الفئة.
2. تعلّم النموذج الـ weights على صور مجهزة بهذه الطريقة بالضبط؛ والأحجام أو إحصاءات الـ pixels المختلفة تعطيه مدخلات لم يرَ مثلها، فتنخفض الدقة.
3. تعالج النماذج دفعات: تتوقع tensor بشكل (N, C, H, W)، فتصبح الصورة الواحدة N=1.
4. يحوّل eval() طبقات مثل dropout والـ batch normalization إلى سلوك الاستدلال؛ ففي وضع التدريب تتصرف عشوائيًا أو تستخدم إحصاءات الدفعة، فتأتي التنبؤات غير متسقة.
5. المخرجات الخام (logits) درجات غير مطبَّعة؛ ويحولها softmax إلى قيم بين 0 و1 مجموعها 1؛ والتسمية هي اسم الفئة صاحبة أعلى قيمة.
6. يوزّع softmax دائمًا 100% على الفئات الألف المعروفة. فإذا لم يكن موضوع الصورة واحدًا منها، يظل النموذج مضطرًا لاختيار فئة، وقد يفعل ذلك بقيمة softmax عالية - فالثقة ليست دليلًا على الصحة.""",
    ),
    "COURSE-003.M02.L01.EX02": (
        """| Workflow | Raw input | Preparation | Pretrained model | Raw output | Final result |
| Image classification | A photo | Resize, crop, normalize, batch | CNN classifier (e.g. ResNet) | 1,000 class scores (logits) | The top class name and its probability |
| Diffusion inpainting | An image, a mask of the region to replace, a text prompt | Resize/normalize image and mask, tokenize and encode the prompt | Text-conditioned diffusion model | Iteratively denoised latent / pixels for the masked area | The edited image with the region filled in |
| Image captioning | A photo | Resize/normalize for the vision encoder | Vision encoder + language decoder | A sequence of token IDs (generated step by step) | A readable sentence describing the photo |

Shared pattern: every workflow prepares its input into the exact numeric format the model was trained on, runs a pretrained learned computation, and then decodes or interprets the raw numeric output into something a person can use.""",
        """| المسار | المدخل الخام | التجهيز | النموذج المدرَّب مسبقًا | المخرج الخام | النتيجة النهائية |
| تصنيف الصور | صورة | تغيير الحجم، القص، normalization، دفعة | CNN classifier (مثل ResNet) | ألف درجة فئة (logits) | اسم أعلى فئة واحتمالها |
| diffusion inpainting | صورة، mask للمنطقة المراد استبدالها، prompt نصي | تجهيز الصورة والـ mask وترميز الـ prompt | نموذج diffusion مشروط بالنص | latent أو pixels للمنطقة المغطاة بعد إزالة الضوضاء تدريجيًا | الصورة المعدّلة مع ملء المنطقة |
| وصف الصور (captioning) | صورة | تجهيزها للـ vision encoder | vision encoder مع language decoder | تسلسل token IDs (يُولَّد خطوة بخطوة) | جملة مقروءة تصف الصورة |

النمط المشترك: كل مسار يجهز مدخله إلى الصيغة الرقمية التي تدرّب عليها النموذج بالضبط، ثم يشغّل حسابًا متعلَّمًا مسبقًا، ثم يفك المخرج الرقمي الخام أو يفسره إلى شيء يستطيع الإنسان استخدامه.""",
    ),
    "COURSE-003.M04.L01.EX04": (
        """1. 50,000 elements per word.
2. Exactly one nonzero value.
3. A 256-dimensional embedding uses 256 numbers, almost 200 times fewer, and every one of them carries information (dense, not sparse).
4. Every pair of one-hot vectors is equally far apart and orthogonal, so "cat" is as different from "kitten" as from "airplane". Embedding vectors are learned so that words used in similar ways end up close together, so similarity becomes measurable as distance or cosine similarity.
5. Product IDs in an online shop (or user IDs, or ZIP codes): an embedding per product lets a recommender learn that products bought by similar customers are similar.""",
        """1. ‏50,000 عنصر لكل كلمة.
2. قيمة واحدة فقط غير صفرية.
3. الـ embedding ذو 256 بُعدًا يستخدم 256 رقمًا، أي أقل بنحو 200 مرة، وكل رقم منها يحمل معلومة (كثيف لا متفرق).
4. كل زوج من متجهات one-hot متعامد وبالمسافة نفسها، فتختلف "cat" عن "kitten" بقدر اختلافها عن "airplane". أما متجهات الـ embedding فتُتعلَّم بحيث تقترب الكلمات المستخدمة بطرق متشابهة، فيصبح التشابه قابلًا للقياس كمسافة أو cosine similarity.
5. أرقام المنتجات في متجر إلكتروني (أو أرقام المستخدمين أو الرموز البريدية): يتيح embedding لكل منتج أن يتعلم نظام التوصية أن المنتجات التي يشتريها عملاء متشابهون متشابهة.""",
    ),
    "COURSE-003.M05.L01.EX03": (
        """1. Underfitting: the model cannot even fit the training data - it is too simple, the learning rate is wrong, or training stopped too early.
2. Overfitting: after an initial improvement the model starts memorizing training data, so training loss keeps falling while validation loss rises.
3. Healthy learning: both losses decrease and stay close, so what is learned generalizes.
4. Still healthy: a small gap where training loss is slightly lower is normal; both are still declining together, so training can continue.
Calling val_loss.backward() would compute gradients from validation data and let the optimizer fit the parameters to it; the validation set would then no longer be independent data, and its loss would stop measuring generalization.""",
        """1. underfitting: لا يستطيع النموذج حتى ملاءمة بيانات التدريب - فهو بسيط جدًا أو الـ learning rate غير مناسب أو توقف التدريب مبكرًا.
2. overfitting: بعد تحسن أولي يبدأ النموذج في حفظ بيانات التدريب، فتستمر الـ training loss في الانخفاض بينما ترتفع الـ validation loss.
3. تعلّم سليم: تنخفض الخسارتان وتبقيان متقاربتين، فما يُتعلَّم ينتقل إلى بيانات جديدة.
4. ما زال سليمًا: الفجوة الصغيرة التي تكون فيها الـ training loss أقل قليلًا أمر طبيعي؛ وما دامتا تنخفضان معًا يمكن متابعة التدريب.
استدعاء val_loss.backward() يحسب gradients من بيانات الـ validation ويسمح للـ optimizer بملاءمة الـ parameters لها؛ فلا تعود مجموعة الـ validation بيانات مستقلة، ويتوقف الـ loss الخاص بها عن قياس الـ generalization.""",
    ),
    "COURSE-003.M09.L01.EX05": (
        """| Task | Architecture | Causal mask | Positional information | Attention |
| 1. Continue a text prompt | Decoder-only (GPT-style) | Yes - each token may only see earlier tokens | Added to the token embeddings of the sequence | Masked self-attention |
| 2. Review sentiment | Encoder-only (BERT-style) | No - the whole review is read at once | Added to the token embeddings | Bidirectional self-attention, then a classification head |
| 3. Translation | Encoder-decoder | Only in the decoder | Both the source and target sequences | Self-attention in the encoder, masked self-attention plus cross-attention (decoder to encoder) in the decoder |
| 4. Image classification from patches | Vision Transformer (encoder) | No | Added to each patch embedding (patch position in the image) | Self-attention between patches, then a class token / pooled output to the classifier |""",
        """| المهمة | البنية | causal mask | المعلومات الموضعية | الانتباه |
| 1. استكمال prompt نصي | decoder فقط (مثل GPT) | نعم - كل token يرى السابق فقط | تُضاف إلى token embeddings للتسلسل | masked self-attention |
| 2. مشاعر مراجعة | encoder فقط (مثل BERT) | لا - تُقرأ المراجعة كاملة دفعة واحدة | تُضاف إلى token embeddings | self-attention ثنائي الاتجاه ثم رأس تصنيف |
| 3. الترجمة | encoder-decoder | في الـ decoder فقط | لتسلسلي المصدر والهدف | self-attention في الـ encoder، وmasked self-attention مع cross-attention (من الـ decoder إلى الـ encoder) في الـ decoder |
| 4. تصنيف صورة من patches | Vision Transformer (encoder) | لا | تُضاف لكل patch embedding (موضع الـ patch في الصورة) | self-attention بين الـ patches ثم class token أو مخرج مجمّع للمصنف |""",
    ),
    "COURSE-003.M10.L01.EX04": (
        """| Stage | Input | Output | Operation | Possible failure | Metric |
| 1. Data loading | Raw CT files + annotation CSVs | HU array (voxels), spacing/origin, candidate list in patient coordinates | Parse metadata, convert coordinates to voxel indices, clip HU | Wrong coordinate conversion, mismatched series IDs | Spot checks: annotated nodules appear at the right voxels |
| 2. Candidate localization / segmentation | CT slices | Mask of suspicious regions, grouped into candidate centres | Segmentation model (e.g. U-Net) + grouping | Missed small nodules, many false candidates | Recall of known nodules, candidates per scan |
| 3. Candidate classification | Small 3D crop around each candidate | Probability that the candidate is a nodule | 3D CNN classifier | Class imbalance - predicting "not nodule" everywhere | Recall, precision, F1 on validation |
| 4. Malignancy classification | Crops of predicted nodules | Malignancy probability | Second classifier (often fine-tuned) | Few malignant examples, overfitting | AUC, sensitivity at fixed specificity |
| 5. Aggregation | Per-nodule probabilities | Per-patient result / report | Combine nodule results, threshold | Threshold too strict or too loose | Patient-level sensitivity/specificity |

I would prototype stage 3 (candidate classification) first: the dataset already provides candidate centres, so it can be trained on small crops quickly, gives fast feedback on data loading and imbalance problems, and is needed by the full pipeline anyway.""",
        """| المرحلة | المدخل | المخرج | العملية | فشل محتمل | المقياس |
| 1. تحميل البيانات | ملفات CT الخام وملفات CSV للتعليقات | مصفوفة HU (voxels) مع spacing/origin وقائمة مرشحين بإحداثيات المريض | قراءة الـ metadata وتحويل الإحداثيات إلى voxel indices وقص HU | تحويل إحداثيات خاطئ أو series IDs غير متطابقة | فحص عينات: العقيدات المعلَّمة تظهر في الـ voxels الصحيحة |
| 2. تحديد/تقسيم المرشحين | شرائح CT | mask للمناطق المشبوهة مجمّعة في مراكز مرشحة | نموذج segmentation (مثل U-Net) مع تجميع | فقدان العقيدات الصغيرة أو كثرة المرشحين الخاطئين | recall للعقيدات المعروفة، عدد المرشحين لكل فحص |
| 3. تصنيف المرشحين | قصاصة ثلاثية الأبعاد صغيرة حول كل مرشح | احتمال أن يكون المرشح عقيدة | 3D CNN classifier | عدم توازن الفئات - التنبؤ بـ "ليس عقيدة" دائمًا | recall وprecision وF1 على الـ validation |
| 4. تصنيف الخباثة | قصاصات العقيدات المتوقعة | احتمال الخباثة | مصنف ثانٍ (غالبًا بالـ fine-tuning) | أمثلة خبيثة قليلة، overfitting | AUC، والحساسية عند specificity ثابتة |
| 5. التجميع | احتمالات كل عقيدة | نتيجة/تقرير لكل مريض | دمج نتائج العقيدات وتطبيق عتبة | عتبة صارمة أو متساهلة أكثر من اللازم | sensitivity/specificity على مستوى المريض |

سأبني النموذج الأولي للمرحلة 3 (تصنيف المرشحين) أولًا: البيانات توفر مراكز المرشحين أصلًا، فيمكن التدريب على قصاصات صغيرة بسرعة، ويعطي تغذية راجعة سريعة عن مشكلات التحميل وعدم التوازن، كما أن الـ pipeline الكامل يحتاجه على أي حال.""",
    ),
    "COURSE-003.M10.L01.EX05": (
        """Known facts (from the chapter):
1. One input is a 3D CT volume of Hounsfield-unit values, roughly hundreds of slices of 512x512 voxels per scan.
2. Labels come from the dataset's annotation and candidate CSV files (candidate centres with a nodule flag; annotated nodules with diameters), produced by radiologists.
3. Voxels are not cubes: spacing differs between axes and between scans, and annotations are in patient (millimetre) coordinates, so they must be converted using each scan's origin, spacing and direction.
4. Scans come from different scanners and protocols, so intensity, slice thickness and noise vary.
5. Candidates are overwhelmingly negative (hundreds of non-nodules per real nodule) and nodules are tiny relative to the whole volume.
Decisions still to make:
6. A split strategy that keeps all candidates of one scan/patient in the same set, and that preserves the positive rate.
7. Storage/cache: decompressed volumes are large, so crops should be cached on disk (and the cache invalidated when preprocessing changes).
8. Compute: a GPU for 3D convolutions; enough CPU and I/O to feed crops; training time per epoch must be measured.
9. Subsystem boundaries: loading/conversion, candidate classification, segmentation, malignancy and reporting as separately testable parts.
10. Before adding a new CT source, validate: same coordinate conventions, HU calibration, label definition and annotation quality, and scanner differences - and check model performance on that source separately.""",
        """حقائق معروفة (من الفصل):
1. المدخل الواحد حجم CT ثلاثي الأبعاد بقيم Hounsfield units، نحو مئات الشرائح بحجم 512×512 voxel لكل فحص.
2. التسميات تأتي من ملفات CSV للتعليقات والمرشحين في مجموعة البيانات (مراكز المرشحين مع علامة العقيدة، والعقيدات المعلَّمة مع أقطارها)، وقد أعدّها أطباء أشعة.
3. الـ voxels ليست مكعبات: الـ spacing يختلف بين المحاور وبين الفحوص، والتعليقات بإحداثيات المريض (بالملّيمتر)، فيجب تحويلها باستخدام origin وspacing وdirection لكل فحص.
4. تأتي الفحوص من أجهزة وبروتوكولات مختلفة، فتختلف الشدة وسماكة الشريحة والضوضاء.
5. المرشحون سلبيون بأغلبية ساحقة (مئات غير العقيدات لكل عقيدة حقيقية)، والعقيدات صغيرة جدًا مقارنة بالحجم الكلي.
قرارات لم تُتخذ بعد:
6. استراتيجية تقسيم تبقي كل مرشحي فحص/مريض واحد في المجموعة نفسها وتحافظ على نسبة الإيجابيات.
7. التخزين والـ cache: الأحجام بعد فك الضغط كبيرة، لذا يجب تخزين القصاصات مؤقتًا على القرص (مع إبطال الـ cache عند تغيير المعالجة).
8. الحوسبة: GPU للـ 3D convolutions، وCPU وإدخال/إخراج كافيان لتغذية القصاصات، مع قياس زمن كل epoch.
9. حدود الأنظمة الفرعية: التحميل/التحويل، وتصنيف المرشحين، والـ segmentation، والخباثة، والتقارير كأجزاء قابلة للاختبار منفصلة.
10. قبل إضافة مصدر CT جديد يجب التحقق من: اتفاق قواعد الإحداثيات، ومعايرة HU، وتعريف التسمية وجودة التعليقات، وفروق الأجهزة - وفحص أداء النموذج على ذلك المصدر منفصلًا.""",
    ),
    "COURSE-003.M11.L01.EX04": (
        """Example synthetic data: 10 patients, 6 candidates each (60 candidates, 6 positive nodules with diameters 4-22 mm).
Split A (every tenth candidate to validation): 54 train / 6 validation candidates; validation happens to contain 1 positive and 5 negatives; diameters in validation 0-9 mm; leakage check: 6 of the 10 patients appear in both sets.
Split B (grouped by patient, 8 patients train / 2 patients validation): 48 train / 12 validation candidates; validation contains 1-2 positives depending on the patients; diameters span the whole range only if the chosen patients do; leakage check: no patient appears in both sets.
Recommendation: split B. Candidates from the same patient share anatomy, scanner and acquisition settings and are strongly correlated; with split A the model is validated on patients it has effectively seen, so the validation score is optimistic. Grouping by patient measures performance on new patients - and the class counts and diameter ranges of each split should still be checked, choosing patients so both sets contain positives.""",
        """بيانات تجريبية مثال: 10 مرضى، لكل منهم 6 مرشحين (60 مرشحًا، منها 6 عقيدات إيجابية بأقطار 4-22 مم).
التقسيم A (كل مرشح عاشر إلى الـ validation): 54 للتدريب و6 للـ validation؛ تصادف أن الـ validation فيه إيجابي واحد و5 سلبيات؛ الأقطار في الـ validation من 0 إلى 9 مم؛ فحص التسرب: 6 من المرضى العشرة يظهرون في المجموعتين.
التقسيم B (حسب المريض، 8 مرضى للتدريب ومريضان للـ validation): 48 للتدريب و12 للـ validation؛ يحتوي الـ validation على إيجابي أو اثنين حسب المرضى؛ ولا تغطي الأقطار المدى كله إلا إذا غطاه المرضى المختارون؛ فحص التسرب: لا يظهر أي مريض في المجموعتين.
التوصية: التقسيم B. مرشحو المريض الواحد يتشاركون التشريح والجهاز وإعدادات التصوير فهم مترابطون بشدة؛ ومع التقسيم A يُتحقق من النموذج على مرضى رآهم فعليًا، فتكون نتيجة الـ validation متفائلة. أما التجميع حسب المريض فيقيس الأداء على مرضى جدد - مع ضرورة فحص عدد الفئات ومدى الأقطار في كل مجموعة واختيار المرضى بحيث تحتوي المجموعتان على إيجابيات.""",
    ),
    "COURSE-003.M11.L01.EX05": (
        """| # | Test | Input fixture | Expected behaviour | Training failure it prevents |
| 1 | Metadata parsing | A small .mhd header with known spacing/origin | Parsed values equal the header | Wrong physical scale for every crop |
| 2 | Series ID matching | CSV rows with known series UIDs | Each row maps to exactly one scan | Labels attached to the wrong scan |
| 3 | Candidate/annotation matching | Candidate inside and outside an annotated nodule | Inside gets the diameter, outside gets none | Wrong nodule sizes / labels |
| 4 | HU clipping | Array with values -3000 and +5000 | Clipped to the chosen range (e.g. -1000..1000) | Extreme values dominating normalization |
| 5 | Coordinate round trip | Known patient coordinate | patient -> voxel -> patient returns the same point (within tolerance) | Crops centred in the wrong place |
| 6 | Axis order | Synthetic volume with a marked voxel | Index order (index, row, col) vs. (x, y, z) handled correctly | Systematically shifted crops |
| 7 | Crop at boundary | Candidate near the volume edge | Crop is padded/shifted, shape stays fixed | Crashes or wrongly sized tensors |
| 8 | Output shape | Any candidate | Crop shape e.g. (1, 32, 48, 48) | Model input errors |
| 9 | Output dtype | Any candidate | float32 tensor and integer/one-hot label | Silent type promotion, wrong loss |
| 10 | Cache invalidation | Change crop size in config | Cached crops are rebuilt | Training on stale crops |
| 11 | Split overlap | Full candidate list | No series UID in both train and validation | Leakage and optimistic validation |
| 12 | Class balance report | Training split | Positive/negative counts logged | Unnoticed extreme imbalance |
| 13 | Visual spot check | Ten random positive crops | A nodule is visible at the centre | Systematic coordinate bugs no unit test caught |""",
        """| # | الاختبار | المدخل التجريبي | السلوك المتوقع | فشل التدريب الذي يمنعه |
| 1 | قراءة الـ metadata | ملف .mhd صغير بقيم spacing/origin معروفة | القيم المقروءة تساوي الـ header | مقياس فيزيائي خاطئ لكل قصاصة |
| 2 | مطابقة series ID | صفوف CSV بأرقام series UID معروفة | كل صف يرتبط بفحص واحد بالضبط | تسميات ملحقة بالفحص الخطأ |
| 3 | مطابقة المرشح بالتعليق | مرشح داخل عقيدة معلَّمة وآخر خارجها | الداخلي يأخذ القطر والخارجي لا شيء | أحجام أو تسميات عقيدات خاطئة |
| 4 | قص HU | مصفوفة بقيم -3000 و+5000 | تُقص إلى المدى المختار (مثل -1000..1000) | سيطرة القيم المتطرفة على الـ normalization |
| 5 | ذهاب وإياب الإحداثيات | إحداثية مريض معروفة | مريض -> voxel -> مريض تعيد النقطة نفسها (ضمن هامش) | قصاصات متمركزة في مكان خاطئ |
| 6 | ترتيب المحاور | حجم تجريبي به voxel معلَّم | التعامل الصحيح مع (index, row, col) مقابل (x, y, z) | قصاصات مزاحة بشكل منهجي |
| 7 | القص عند الحدود | مرشح قرب حافة الحجم | تُحشى القصاصة أو تُزاح ويبقى الشكل ثابتًا | انهيار أو tensors بأحجام خاطئة |
| 8 | شكل المخرج | أي مرشح | شكل القصاصة مثل (1, 32, 48, 48) | أخطاء في مدخل النموذج |
| 9 | نوع البيانات | أي مرشح | tensor من نوع float32 وتسمية صحيحة أو one-hot | ترقية نوع صامتة أو loss خاطئة |
| 10 | إبطال الـ cache | تغيير حجم القص في الإعدادات | إعادة بناء القصاصات المخزنة | التدريب على قصاصات قديمة |
| 11 | تداخل التقسيم | قائمة المرشحين كاملة | لا يظهر series UID في التدريب والـ validation معًا | التسرب وvalidation متفائل |
| 12 | تقرير توازن الفئات | مجموعة التدريب | تسجيل أعداد الإيجابي/السلبي | عدم توازن شديد لا يُلاحَظ |
| 13 | فحص بصري | عشر قصاصات إيجابية عشوائية | عقيدة مرئية في المركز | أخطاء إحداثيات منهجية لم يلتقطها أي unit test |""",
    ),
    "COURSE-003.M12.L01.EX05": (
        """| Metric | Collected in | Console / TensorBoard | Failure it reveals |
| Overall loss | Training and validation loops, per batch, averaged per epoch | Both | Divergence, no learning, overfitting (train vs. val) |
| Positive loss | Loss averaged over positive samples only | TensorBoard | The model ignoring the rare class |
| Negative loss | Loss averaged over negative samples only | TensorBoard | Over-predicting positives |
| Overall accuracy | Epoch-end metrics | Both | Misleading alone under imbalance |
| Positive accuracy (recall) | Epoch-end metrics on positives | Both | Rare class never detected |
| Negative accuracy | Epoch-end metrics on negatives | Both | Too many false alarms |
| Samples processed | Training loop counter | TensorBoard (x-axis) | Comparing runs fairly despite different epoch sizes |
| Iteration rate / ETA | Loop timing | Console | Data loading bottlenecks, stalled runs |
| Dataset sample counts | Dataset init | Console | Wrong split sizes, empty class, broken filtering |
| Run identifier | Start of run | Both (log line, TensorBoard run name) | Mixing up results of different experiments |

Positive accuracy (positive-class recall) would have exposed the 99.7%-accuracy failure fastest: overall accuracy was high only because almost every sample is negative, while positive accuracy was 0% - the model never found a single nodule.""",
        """| المقياس | مكان جمعه | Console أم TensorBoard | الفشل الذي يكشفه |
| الـ loss الكلي | حلقتا التدريب والـ validation لكل دفعة ومتوسط كل epoch | كلاهما | التباعد، عدم التعلم، الـ overfitting (تدريب مقابل validation) |
| loss الإيجابيات | متوسط الـ loss على العينات الإيجابية فقط | TensorBoard | تجاهل النموذج للفئة النادرة |
| loss السلبيات | متوسط الـ loss على العينات السلبية فقط | TensorBoard | الإفراط في التنبؤ بالإيجابي |
| الـ accuracy الكلية | مقاييس نهاية الـ epoch | كلاهما | مضللة وحدها مع عدم التوازن |
| accuracy الإيجابيات (recall) | مقاييس نهاية الـ epoch على الإيجابيات | كلاهما | عدم اكتشاف الفئة النادرة أبدًا |
| accuracy السلبيات | مقاييس نهاية الـ epoch على السلبيات | كلاهما | إنذارات خاطئة كثيرة |
| العينات المعالجة | عدّاد حلقة التدريب | TensorBoard (المحور الأفقي) | مقارنة التشغيلات بعدل رغم اختلاف حجم الـ epoch |
| معدل التكرار / الوقت المتبقي | توقيت الحلقة | Console | اختناقات تحميل البيانات أو توقف التشغيل |
| أعداد عينات البيانات | تهيئة الـ Dataset | Console | أحجام تقسيم خاطئة أو فئة فارغة أو ترشيح معطوب |
| معرّف التشغيل | بداية التشغيل | كلاهما (سطر log واسم التشغيل في TensorBoard) | الخلط بين نتائج تجارب مختلفة |

كانت accuracy الإيجابيات (recall للفئة الإيجابية) ستكشف فشل الـ 99.7% أسرع من غيرها: الـ accuracy الكلية كانت مرتفعة فقط لأن كل العينات تقريبًا سلبية، بينما كانت accuracy الإيجابيات 0% - لم يجد النموذج عقيدة واحدة.""",
    ),
    "COURSE-003.M13.L01.EX05": (
        """| Run | Hypothesis | Change (everything else fixed) | Watch on validation | Supports / rejects |
| 0. Baseline | Reference point | Current balance ratio 1:1, current augmentation | F1, F2, recall, precision, loss | - |
| 1. Balance 1:3 | Showing more negatives reduces false positives without losing much recall | Positive:negative sampling 1:3 | Precision, F1, recall | Supported if precision rises and F1 is higher at similar recall; rejected if recall drops sharply |
| 2. Stronger augmentation | More variation reduces overfitting on the few positives | Larger rotation/scale/noise ranges | Train-val gap, F1, F2 | Supported if the gap shrinks and validation F1 improves; rejected if training fails to fit or F1 falls |
| 3. Augmentation combination | Flip + offset together beat either alone | Enable flip and offset, nothing else | F1 vs. single-augmentation runs | Supported if F1 exceeds both single runs |
| Metrics | F1 balances precision and recall; F2 weights recall more, which matters when missing a nodule is costlier than a false alarm | Computed every epoch on the same validation set | Best-epoch values, not only the last | Decide only on validation, compare runs with the same number of samples processed |

No setting is assumed to win in advance; each run is judged against the baseline with its stated criterion.""",
        """| التشغيل | الفرضية | التغيير (مع تثبيت كل ما عداه) | ما نراقبه على الـ validation | دعم أو رفض |
| 0. الأساس | نقطة مرجعية | نسبة التوازن الحالية 1:1 والـ augmentation الحالي | F1 وF2 وrecall وprecision والـ loss | - |
| 1. توازن 1:3 | عرض سلبيات أكثر يقلل الإيجابيات الخاطئة دون خسارة كبيرة في recall | نسبة أخذ العينات إيجابي:سلبي 1:3 | precision وF1 وrecall | مدعومة إذا ارتفعت precision وتحسن F1 مع recall متقارب؛ مرفوضة إذا انخفض recall بشدة |
| 2. augmentation أقوى | التنوع الأكبر يقلل الـ overfitting على الإيجابيات القليلة | نطاقات أكبر للدوران والتكبير والضوضاء | فجوة التدريب/الـ validation وF1 وF2 | مدعومة إذا ضاقت الفجوة وتحسن F1؛ مرفوضة إذا فشل التدريب في الملاءمة أو انخفض F1 |
| 3. دمج augmentation | القلب مع الإزاحة معًا أفضل من كل منهما وحده | تفعيل flip وoffset فقط | F1 مقارنة بتشغيلات الـ augmentation المفرد | مدعومة إذا تجاوز F1 التشغيلين المفردين |
| المقاييس | يوازن F1 بين precision وrecall؛ ويعطي F2 وزنًا أكبر لـ recall، وهذا مهم عندما يكون فقدان عقيدة أخطر من إنذار كاذب | تُحسب كل epoch على مجموعة الـ validation نفسها | قيم أفضل epoch لا الأخيرة فقط | القرار على الـ validation فقط، ومقارنة التشغيلات بعدد العينات المعالجة نفسه |

لا يُفترض مسبقًا أن إعدادًا ما سيفوز؛ يُحكم على كل تشغيل مقارنةً بالأساس وفق معياره المحدد.""",
    ),
    "COURSE-003.M14.L01.EX01": (
        """| Scenario | Task | Output | Why not another task |
| CT slice: is any nodule present? | Image classification | One label per image | Location is not needed |
| Chest X-ray: draw boxes around each suspicious nodule | Object detection | List of boxes + class + score | Classification gives no location; masks are unnecessary |
| CT: mark every lung-tissue voxel | Semantic segmentation | Per-pixel class mask (same H x W) | Boxes cannot follow the organ's outline |
| Histology: separate each individual cell nucleus | Instance segmentation | One mask per object instance | Semantic masks merge touching nuclei into one region |
| Photo: is it a cat or a dog? | Image classification | One label | Nothing about position is asked |
| Traffic camera: locate and count cars | Object detection | Boxes per car | Counting needs individual objects |
| Satellite image: road vs. not road for every pixel | Semantic segmentation | Per-pixel mask | Detection boxes would cover huge background areas |
| Shop shelf: cut out each product separately | Instance segmentation | Mask per product | Semantic segmentation cannot tell neighbouring products apart |""",
        """| الحالة | المهمة | المخرج | لماذا لا تكفي مهمة أخرى |
| شريحة CT: هل توجد عقيدة؟ | image classification | تسمية واحدة لكل صورة | الموقع غير مطلوب |
| أشعة صدر: رسم صناديق حول كل عقيدة مشبوهة | object detection | قائمة صناديق مع الفئة والدرجة | التصنيف لا يعطي موقعًا والـ masks غير ضرورية |
| CT: تعليم كل voxel من نسيج الرئة | semantic segmentation | mask بفئة لكل pixel (بنفس H × W) | الصناديق لا تتبع حدود العضو |
| أنسجة: فصل كل نواة خلية على حدة | instance segmentation | mask لكل كائن | الـ semantic masks تدمج الأنوية المتلامسة في منطقة واحدة |
| صورة: قطة أم كلب؟ | image classification | تسمية واحدة | لا يُسأل عن الموضع |
| كاميرا مرور: تحديد السيارات وعدّها | object detection | صندوق لكل سيارة | العدّ يحتاج كائنات منفردة |
| صورة قمر صناعي: طريق أم لا لكل pixel | semantic segmentation | mask لكل pixel | صناديق الكشف تغطي مساحات خلفية ضخمة |
| رف متجر: قص كل منتج منفردًا | instance segmentation | mask لكل منتج | الـ semantic segmentation لا يميز المنتجات المتجاورة |""",
    ),
    "COURSE-003.M14.L01.EX02": (
        """1-2. Inputs: one RGB image (resized/padded to 1024x1024 and normalized) and a point prompt: its (x, y) coordinates plus a label (foreground = 1).
3. The image goes only to the image encoder (a large ViT), which runs once per image and produces a grid of image embeddings that can be reused for many prompts. The point coordinates and label go to the prompt encoder, which turns them into small prompt embeddings (positional encoding of the point plus a learned foreground/background embedding). The mask decoder receives both - the image embeddings and the prompt embeddings - and uses attention in both directions between them.
Outputs: several candidate masks (typically three) at low resolution, upscaled to the image size, plus a predicted IoU (quality) score for each mask.
4. A single point is ambiguous: a click on a shirt could mean the button, the shirt, or the whole person. SAM therefore returns several plausible masks at different levels of granularity with confidence scores, and the user or application chooses (or adds more prompts to disambiguate).""",
        """1-2. المدخلات: صورة RGB واحدة (تُغيَّر إلى 1024×1024 مع الحشو والـ normalization) وprompt نقطي: إحداثيات (x, y) مع label (المقدمة = 1).
3. تذهب الصورة إلى الـ image encoder فقط (ViT كبير)، ويعمل مرة واحدة لكل صورة وينتج شبكة من image embeddings يمكن إعادة استخدامها لعدة prompts. وتذهب إحداثيات النقطة وتسميتها إلى الـ prompt encoder الذي يحولها إلى prompt embeddings صغيرة (positional encoding للنقطة مع embedding متعلَّم للمقدمة/الخلفية). ويستقبل الـ mask decoder الاثنين - image embeddings وprompt embeddings - ويستخدم الانتباه في الاتجاهين بينهما.
المخرجات: عدة masks مرشحة (ثلاثة عادةً) بدقة منخفضة تُكبَّر إلى حجم الصورة، مع درجة IoU متوقعة (جودة) لكل mask.
4. النقطة الواحدة غامضة: النقر على قميص قد يعني الزر أو القميص أو الشخص كله. لذلك يعيد SAM عدة masks معقولة بمستويات تفصيل مختلفة مع درجات ثقة، ويختار المستخدم أو التطبيق (أو يضيف prompts أخرى لإزالة الغموض).""",
    ),
    "COURSE-003.M14.L01.EX05": (
        """| Boundary | Data passed | Coordinate conversion | Risks |
| 1. CT loader -> segmentation | Normalized 2D slices (with neighbouring slices as channels) and the scan's origin/spacing/direction | None yet (voxel index space) | Normalization different from training, wrong slice order |
| 2. Segmentation -> mask post-processing | Per-slice probability masks | Index space | Threshold choice changes how many regions survive |
| 3. Post-processing -> candidate list | Connected regions turned into candidate centres (centre of mass in index space) + region size | Index (row, col, slice) -> patient millimetre coordinates using spacing/origin/direction | Axis-order and spacing mistakes shift every candidate |
| 4. Candidate list -> classifier | Candidate centres converted back to voxel indices to cut 3D crops of the classifier's expected shape | Patient -> voxel for the crop | Crops at volume borders, centres off the true nodule |
| 5. Classifier -> results | Probability per candidate | Report in patient coordinates | - |

Duplicate regions across adjacent slices: one nodule usually appears in several consecutive slices; conceptually those 2D regions should be grouped into one 3D candidate (for example by connecting overlapping regions in neighbouring slices) before classification. The exact grouping rule and its distance threshold are unresolved design choices, not given by the chapter.
Failure modes segmentation introduces downstream: missed nodules (the classifier never sees them - recall is capped by segmentation), many false regions (more work and more false positives), split or merged regions giving off-centre crops, and coordinate bugs that silently misplace every candidate.
Unresolved: probability threshold, minimum region size, grouping rule across slices, and how candidates from segmentation and from the original candidate list are combined.""",
        """| الحد | البيانات المنقولة | تحويل الإحداثيات | المخاطر |
| 1. محمّل CT -> الـ segmentation | شرائح 2D بعد الـ normalization (مع الشرائح المجاورة كقنوات) وorigin/spacing/direction للفحص | لا شيء بعد (فضاء voxel index) | normalization مختلف عن التدريب، ترتيب شرائح خاطئ |
| 2. الـ segmentation -> معالجة الـ mask | masks احتمالية لكل شريحة | فضاء الفهارس | اختيار العتبة يغير عدد المناطق الباقية |
| 3. المعالجة -> قائمة المرشحين | تحويل المناطق المتصلة إلى مراكز مرشحين (مركز الكتلة في فضاء الفهارس) مع حجم المنطقة | من الفهرس (row, col, slice) إلى إحداثيات المريض بالملّيمتر باستخدام spacing/origin/direction | أخطاء ترتيب المحاور أو الـ spacing تزيح كل المرشحين |
| 4. قائمة المرشحين -> المصنف | تحويل المراكز مرة أخرى إلى voxel indices لقص قصاصات 3D بالشكل الذي يتوقعه المصنف | من المريض إلى voxel للقص | قصاصات عند حدود الحجم، ومراكز بعيدة عن العقيدة الحقيقية |
| 5. المصنف -> النتائج | احتمال لكل مرشح | تقرير بإحداثيات المريض | - |

المناطق المكررة في الشرائح المتجاورة: تظهر العقيدة الواحدة عادةً في عدة شرائح متتالية؛ ومفاهيميًا يجب تجميع هذه المناطق ثنائية الأبعاد في مرشح ثلاثي الأبعاد واحد (مثلًا بربط المناطق المتداخلة في الشرائح المتجاورة) قبل التصنيف. أما قاعدة التجميع الدقيقة وعتبة المسافة فقرارات تصميم لم تُحسم ولا يقدمها الفصل.
أعطال يُدخلها الـ segmentation لاحقًا: عقيدات مفقودة (لا يراها المصنف أبدًا - فالـ recall محدود بالـ segmentation)، ومناطق خاطئة كثيرة (عمل أكثر وإيجابيات خاطئة أكثر)، ومناطق منقسمة أو مدموجة تعطي قصاصات غير متمركزة، وأخطاء إحداثيات تضع كل المرشحين في أماكن خاطئة بصمت.
غير محسوم: عتبة الاحتمال، وأصغر حجم للمنطقة، وقاعدة التجميع عبر الشرائح، وطريقة دمج مرشحي الـ segmentation مع قائمة المرشحين الأصلية.""",
    ),
}
