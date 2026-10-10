"""COURSE-006 Production AI Engineering: example answers (part b)."""

EXAMPLES = {
    "COURSE-006.M07.L01.EX02": (
        """1. Weights: 7B x 2 bytes = 14 GB.
2. Inference: 14 GB x 1.2 = about 16.8 GB.
3. All 7B trainable: gradient + 2 Adam states = 3 values x 2 bytes x 7B = 42 GB, on top of the 14 GB of weights (about 56 GB before activations).
4. Only 100M trainable: 3 x 2 bytes x 100M = 0.6 GB, plus the frozen 14 GB of weights.
5. They ignore activations (which grow with batch size and sequence length), temporary buffers, framework/CUDA overhead and memory fragmentation; mixed-precision setups often keep a float32 master copy, which adds more.
6. Gradient checkpointing stores only some activations and recomputes the rest during backpropagation: much lower activation memory, at the cost of roughly 20-30% more compute time.
7. Quantizing the frozen base (for example to 4-bit, as in QLoRA) shrinks the 14 GB weight term to about 3.5 GB; the trainable adapter parameters and their optimizer states stay in higher precision.
8. Training needs memory that inference does not: gradients, optimizer states and the activations saved for the backward pass, which scale with batch and sequence length - so a model that fits for inference can run out of memory as soon as training starts.""",
        """1. الـ weights: ‏7B × 2 bytes = 14 GB.
2. الاستدلال: 14 GB × 1.2 = نحو 16.8 GB.
3. إذا كانت كل الـ 7B قابلة للتدريب: gradient مع حالتي Adam = 3 قيم × 2 bytes × 7B = 42 GB، فوق 14 GB للـ weights (نحو 56 GB قبل الـ activations).
4. إذا كان 100M فقط قابلًا للتدريب: 3 × 2 bytes × 100M = 0.6 GB، مع 14 GB للـ weights المجمدة.
5. تتجاهل الحسابات الـ activations (التي تكبر مع حجم الدفعة وطول التسلسل)، والمخازن المؤقتة، وعبء الإطار وCUDA، وتجزؤ الذاكرة؛ كما تحتفظ إعدادات الـ mixed precision غالبًا بنسخة float32 رئيسية تضيف أكثر.
6. يخزن الـ gradient checkpointing بعض الـ activations فقط ويعيد حساب الباقي أثناء الـ backpropagation: ذاكرة activations أقل بكثير مقابل نحو 20-30% وقت حساب إضافي.
7. تقليل دقة الـ base المجمد (مثل 4-bit كما في QLoRA) يصغّر حد الـ weights من 14 GB إلى نحو 3.5 GB؛ بينما تبقى parameters الـ adapter القابلة للتدريب وحالات الـ optimizer الخاصة بها بدقة أعلى.
8. التدريب يحتاج ذاكرة لا يحتاجها الاستدلال: الـ gradients وحالات الـ optimizer والـ activations المحفوظة للـ backward pass، وهي تكبر مع الدفعة وطول التسلسل - لذا قد ينفد النموذج الذي يتسع للاستدلال من الذاكرة بمجرد بدء التدريب.""",
    ),
    "COURSE-006.M07.L01.EX03": (
        """1. A 7B model needs ~14 GB just for 16-bit weights, and full finetuning adds gradients and Adam states (~42 GB) plus activations - far more than 24 GB.
2. QLoRA as the first experiment: the base model in 4-bit (~3.5-4 GB for 7B) leaves room for adapters, activations and a reasonable batch on one 24 GB GPU; plain LoRA is the comparison if memory allows.
3. Start with the attention projections q_proj and v_proj (the original LoRA choice); if quality is insufficient, add k_proj, o_proj and the MLP layers, since structured-output tasks often benefit from adapting more layers.
4. Rank 8-16 to start (try 4-64). A higher rank adds parameters and memory and can overfit a small dataset without improving quality; the rank only needs to capture the task-specific change.
5. alpha scales the LoRA update (the effective scale is alpha/rank); it controls how strongly the adapter changes the base model's outputs, and is often set to about 1-2 x rank so that changing rank does not require retuning the learning rate.
6. Monitor training and validation loss, learning rate, gradient norm, GPU memory, and periodically the task metric (valid structured output and field accuracy) on a validation set.
7. Overfitting: validation loss rises or the validation task metric drops while training loss keeps falling; outputs start copying training examples.
8. Keep adapters separate: one shared base model serves 20 small customer adapters loaded on demand (multi-LoRA serving), instead of 20 full merged copies. Merge only for a single high-traffic version to remove adapter overhead.
9. Quality: schema-valid output rate and field-level accuracy on a held-out set vs. the base model with prompting. Latency: p50/p95 per request with the adapter. Memory: GPU memory at the expected concurrency.
10. If LoRA plateaus clearly below the target quality, and we have a large, high-quality dataset and enough hardware, full finetuning may capture changes a low-rank update cannot.""",
        """1. يحتاج نموذج 7B نحو 14 GB لأوزان 16-bit وحدها، ويضيف full finetuning الـ gradients وحالات Adam ‏(~42 GB) والـ activations - أكثر بكثير من 24 GB.
2. QLoRA كأول تجربة: النموذج الأساسي بـ 4-bit ‏(~3.5-4 GB لـ 7B) يترك مساحة للـ adapters والـ activations ودفعة معقولة على GPU واحدة بـ 24 GB؛ وLoRA العادي للمقارنة إن سمحت الذاكرة.
3. أبدأ بإسقاطات الانتباه q_proj وv_proj (الاختيار الأصلي في LoRA)؛ وإذا لم تكفِ الجودة أضيف k_proj وo_proj وطبقات الـ MLP، فمهام المخرجات المنظمة تستفيد غالبًا من تكييف طبقات أكثر.
4. rank بين 8 و16 للبداية (مع تجربة 4-64). الـ rank الأعلى يضيف parameters وذاكرة وقد يسبب overfitting على بيانات قليلة دون تحسين الجودة؛ فالـ rank يكفي أن يلتقط التغيير الخاص بالمهمة.
5. يضخّم alpha تحديث LoRA (المقياس الفعلي alpha/rank)؛ فهو يتحكم في قوة تغيير الـ adapter لمخرجات النموذج الأساسي، ويُضبط غالبًا عند 1-2 × rank حتى لا يتطلب تغيير الـ rank إعادة ضبط الـ learning rate.
6. أراقب الـ loss في التدريب والـ validation والـ learning rate ومعيار الـ gradient وذاكرة الـ GPU، ودوريًا مقياس المهمة (صلاحية المخرج المنظم ودقة الحقول) على مجموعة validation.
7. الـ overfitting: ارتفاع الـ validation loss أو انخفاض مقياس المهمة على الـ validation مع استمرار انخفاض الـ training loss؛ وبدء المخرجات في نسخ أمثلة التدريب.
8. أبقي الـ adapters منفصلة: نموذج أساسي واحد مشترك يخدم 20 adapter صغيرًا للعملاء يُحمَّل عند الطلب (multi-LoRA serving)، بدلًا من 20 نسخة كاملة مدمجة. والدمج فقط لإصدار واحد عالي الحركة لإزالة عبء الـ adapter.
9. الجودة: نسبة المخرجات الصالحة للمخطط ودقة الحقول على مجموعة محجوزة مقارنة بالنموذج الأساسي مع الـ prompting. زمن الاستجابة: p50/p95 لكل طلب مع الـ adapter. الذاكرة: ذاكرة الـ GPU عند التزامن المتوقع.
10. إذا توقف LoRA بوضوح دون الجودة المطلوبة، وكانت لدينا بيانات كبيرة عالية الجودة وعتاد كافٍ، فقد يلتقط full finetuning تغييرات لا يستطيعها تحديث low-rank.""",
    ),
    "COURSE-006.M08.L01.EX01": (
        """1. Desired behaviours: answer order, shipping and return questions using the provided order data and policies; ask a clarifying question when information is missing; follow the store's tone (polite, concise); escalate to a human for refunds above a limit or angry customers; respond in the customer's language (Arabic or English).
2. Unwanted: promising refunds or discounts the policy does not allow; inventing order details or tracking numbers.
3. Both: single-turn for simple questions, multi-turn for clarifications and follow-ups (most real support is multi-turn).
4. Coverage slices: topic (orders, shipping, returns, payments, product questions); language (Arabic, English, mixed); input length (one line to long complaints); typo/slang rate; customer type (new, returning, angry); output format (short answer, step list, escalation message).
5. High quality: relevant (addresses the question), aligned with the task and policy, consistent (similar inputs get similar answers and annotators agree), correctly formatted, unique (no near-duplicates), and compliant (no personal data, no policy violations).
6. Pilot: about 500-1,000 carefully reviewed examples covering all slices.
7. Train the same model and setup on 25%, 50% and 100% of the pilot, evaluate each on the same held-out set, and plot the metric against data size; the slope estimates how much more data would help.
8. Diminishing returns: the curve flattens - going from 50% to 100% improves the metric by less than its run-to-run noise - and errors that remain are concentrated in slices that need different data, not more of the same.""",
        """1. السلوكيات المطلوبة: الإجابة عن أسئلة الطلبات والشحن والإرجاع باستخدام بيانات الطلب والسياسات المقدمة؛ وطرح سؤال توضيحي عند نقص المعلومات؛ واتباع نبرة المتجر (مهذبة وموجزة)؛ والتصعيد إلى موظف في الاستردادات فوق حد معين أو مع العملاء الغاضبين؛ والرد بلغة العميل (عربية أو إنجليزية).
2. غير المرغوب: الوعد باستردادات أو خصومات لا تسمح بها السياسة؛ واختراع تفاصيل طلبات أو أرقام تتبع.
3. الاثنان: حوار من دور واحد للأسئلة البسيطة، ومتعدد الأدوار للتوضيح والمتابعة (معظم الدعم الحقيقي متعدد الأدوار).
4. شرائح التغطية: الموضوع (الطلبات والشحن والإرجاع والدفع وأسئلة المنتجات)؛ واللغة (عربية وإنجليزية ومختلطة)؛ وطول المدخل (من سطر إلى شكاوى طويلة)؛ ونسبة الأخطاء الإملائية والعامية؛ ونوع العميل (جديد، عائد، غاضب)؛ وشكل المخرج (إجابة قصيرة، قائمة خطوات، رسالة تصعيد).
5. الجودة العالية: ذو صلة (يعالج السؤال)، ومتوافق مع المهمة والسياسة، ومتسق (مدخلات متشابهة تحصل على إجابات متشابهة ويتفق المصنفون)، ومنسق بشكل صحيح، وفريد (بلا شبه تكرارات)، وملتزم (بلا بيانات شخصية ولا مخالفات للسياسة).
6. التجربة الأولية: نحو 500-1,000 مثال مراجَع بعناية يغطي كل الشرائح.
7. أدرّب النموذج والإعداد نفسيهما على 25% و50% و100% من التجربة، وأقيّم كلًا منها على المجموعة المحجوزة نفسها، وأرسم المقياس مقابل حجم البيانات؛ ويقدّر الميل مقدار فائدة البيانات الإضافية.
8. تناقص العائد: يتسطح المنحنى - فالانتقال من 50% إلى 100% يحسّن المقياس بأقل من تذبذبه بين التشغيلات - والأخطاء المتبقية تتركز في شرائح تحتاج بيانات مختلفة لا المزيد من النوع نفسه.""",
    ),
    "COURSE-006.M08.L01.EX02": (
        """1. Coverage plan: schema complexity (1 table / 2-3 joined tables / 4+ tables with nesting) x query type (filter, aggregation + GROUP BY, JOIN, subquery, window function, ORDER/LIMIT, date logic), with target counts per cell.
2. Real seed: a few hundred real user questions with verified SQL and our real schemas. Synthetic: new questions and SQL generated from those seeds across more schemas and query types.
3. Instructions: give the LLM a schema, a target query type and a few seed examples; ask for varied natural-language questions (different phrasings, levels of detail, some with typos).
4. SQL: a strong model writes SQL for each question given the schema (optionally generating 2-3 candidates).
5. Deterministic checks: the SQL parses; every table and column exists in the schema; it executes without error on a test database with realistic data and returns a non-empty, plausible result; candidates that disagree are flagged.
6. Failed examples are discarded or sent to a correction loop (regenerate with the error message) at most once; repeated failures are logged to improve the generators.
7. Deduplication: exact duplicates by normalized text, near-duplicates by embedding similarity of questions and normalized SQL.
8. AI judge: does the SQL actually answer the question's intent (e.g. "last month" vs. "last 30 days", correct aggregation level)? Execution success cannot detect a valid query that answers the wrong question.
9. After filtering, count examples per cell of the coverage plan and per schema; regenerate for under-filled cells.
10. Contamination: remove any example whose question or SQL closely matches benchmark test sets (e.g. Spider) and our held-out evaluation set. Lineage: store for each example its seed, generator model and prompt version, checks passed, and date.
11. Train the model with and without the synthetic data and compare execution accuracy on a held-out set of real user questions (never synthetic) on unseen schemas.""",
        """1. خطة التغطية: تعقيد المخطط (جدول واحد / 2-3 جداول مربوطة / 4 جداول أو أكثر مع تداخل) × نوع الاستعلام (ترشيح، تجميع مع GROUP BY، JOIN، استعلام فرعي، window function، ORDER/LIMIT، منطق التواريخ)، مع أعداد مستهدفة لكل خلية.
2. بذور حقيقية: بضع مئات من أسئلة المستخدمين الحقيقية مع SQL مُتحقق منه ومخططاتنا الحقيقية. اصطناعي: أسئلة وSQL جديدة تُولَّد من تلك البذور عبر مخططات وأنواع استعلامات أكثر.
3. التعليمات: أعطي الـ LLM مخططًا ونوع استعلام مستهدفًا وأمثلة بذور قليلة؛ وأطلب أسئلة متنوعة بلغة طبيعية (صياغات مختلفة ومستويات تفصيل وبعضها بأخطاء إملائية).
4. الـ SQL: يكتب نموذج قوي SQL لكل سؤال بمعلومية المخطط (مع توليد 2-3 مرشحين اختياريًا).
5. فحوص حتمية: الـ SQL قابل للتحليل؛ وكل جدول وعمود موجود في المخطط؛ ويُنفَّذ دون خطأ على قاعدة بيانات اختبار ببيانات واقعية ويعيد نتيجة غير فارغة ومعقولة؛ وتُعلَّم المرشحات المتعارضة.
6. الأمثلة الفاشلة تُحذف أو تُرسل إلى حلقة تصحيح (إعادة التوليد مع رسالة الخطأ) مرة واحدة على الأكثر؛ وتُسجَّل حالات الفشل المتكررة لتحسين المولّدات.
7. إزالة التكرار: التكرارات الدقيقة بالنص الموحَّد، وشبه التكرارات بتشابه embedding الأسئلة والـ SQL الموحَّد.
8. AI judge: هل يجيب الـ SQL فعلًا عن قصد السؤال (مثل "الشهر الماضي" مقابل "آخر 30 يومًا"، ومستوى التجميع الصحيح)؟ فنجاح التنفيذ لا يكشف استعلامًا صالحًا يجيب عن سؤال آخر.
9. بعد الترشيح أعدّ الأمثلة في كل خلية من خطة التغطية ولكل مخطط؛ وأعيد التوليد للخلايا الناقصة.
10. التلوث: أحذف أي مثال يشبه سؤاله أو الـ SQL الخاص به مجموعات اختبار المعايير (مثل Spider) ومجموعة التقييم المحجوزة لدينا. سجل المصدر (lineage): أخزن لكل مثال بذرته ونموذج المولّد وإصدار الـ prompt والفحوص التي اجتازها والتاريخ.
11. أدرّب النموذج بالبيانات الاصطناعية وبدونها وأقارن execution accuracy على مجموعة محجوزة من أسئلة مستخدمين حقيقية (لا اصطناعية أبدًا) على مخططات لم يرها.""",
    ),
    "COURSE-006.M08.L01.EX03": (
        """1. Provenance: source (public dataset name/version, internal log, synthetic generator), licence, collection date, generator model and prompt version for synthetic rows, language, and a stable example ID.
2. First statistics: counts per source, language and topic; length distributions of instructions and responses; share of empty/very short responses; number of turns; token counts.
3. Manual inspection: about 200 random examples stratified by source, plus the shortest, longest and most frequent examples.
4. Exact duplicates by hashing normalized text; near-duplicates with MinHash/LSH on n-grams, or embedding similarity, within and across sources.
5. Filters: PII detection (emails, phone numbers, IDs) to remove or mask; drop sources with incompatible licences; toxicity classifier; remove content violating our policies or the model's intended use.
6. Quality heuristics: length bounds, language detection, broken formatting, refusals or boilerplate answers, instruction/response mismatch; then an AI judge scoring helpfulness and correctness on the remaining candidates (with human checks of the judge).
7. Order: cheap steps first - schema/format checks, exact dedup, heuristic and compliance filters, near-dedup - and the expensive AI verification last, on the much smaller remainder.
8. Have two annotators (or annotator and judge) label an overlapping sample; compute agreement (e.g. Cohen's kappa) per category; low agreement shows unclear guidelines or ambiguous data to fix or drop.
9. Selecting 150,000: rank by quality score, then sample to keep the coverage targets (topics, languages, task types) balanced, preferring diverse examples over many near-similar ones.
10. Convert every example to the target model's chat template (system/user/assistant roles and special tokens) with the tokenizer's apply_chat_template, and verify a few by decoding.
11. Keep the raw dataset read-only and versioned; scripts write to new output versions, so a bug can always be rerun from the untouched original.
12. Trial: run the full pipeline on ~1,000 examples and check counts removed at each step, inspect samples of kept and removed rows, verify output format and template, and measure run time to estimate the full job.""",
        """1. سجل المصدر: المصدر (اسم مجموعة البيانات العامة وإصدارها، أو سجل داخلي، أو مولّد اصطناعي)، والترخيص، وتاريخ الجمع، ونموذج المولّد وإصدار الـ prompt للصفوف الاصطناعية، واللغة، ومعرّف ثابت للمثال.
2. الإحصاءات الأولى: الأعداد لكل مصدر ولغة وموضوع؛ وتوزيعات أطوال التعليمات والإجابات؛ ونسبة الإجابات الفارغة أو القصيرة جدًا؛ وعدد الأدوار؛ وأعداد الـ tokens.
3. الفحص اليدوي: نحو 200 مثال عشوائي مقسمة حسب المصدر، مع الأقصر والأطول والأكثر تكرارًا.
4. التكرارات الدقيقة بتجزئة (hash) النص الموحَّد؛ وشبه التكرارات بـ MinHash/LSH على الـ n-grams أو بتشابه الـ embeddings، داخل المصادر وبينها.
5. المرشحات: كشف البيانات الشخصية (البريد والهواتف وأرقام الهوية) لحذفها أو إخفائها؛ واستبعاد المصادر ذات التراخيص غير المتوافقة؛ ومصنف للمحتوى المسيء؛ وحذف المحتوى المخالف لسياساتنا أو للاستخدام المقصود للنموذج.
6. قواعد الجودة: حدود الطول، وكشف اللغة، والتنسيق المكسور، والرفض أو الإجابات النمطية، وعدم تطابق التعليمة مع الإجابة؛ ثم AI judge يقيّم الفائدة والصحة على المرشحين المتبقين (مع فحص بشري للحكم).
7. الترتيب: الخطوات الرخيصة أولًا - فحوص المخطط والشكل، وإزالة التكرار الدقيق، والمرشحات القاعدية ومرشحات الالتزام، وإزالة شبه التكرار - ثم التحقق المكلف بالـ AI أخيرًا على البقية الأصغر بكثير.
8. يصنّف مصنّفان (أو مصنّف وحكم) عينة مشتركة؛ وأحسب الاتفاق (مثل Cohen's kappa) لكل فئة؛ والاتفاق المنخفض يكشف إرشادات غير واضحة أو بيانات غامضة يجب إصلاحها أو حذفها.
9. اختيار 150,000: أرتب حسب درجة الجودة ثم أسحب مع الحفاظ على توازن أهداف التغطية (المواضيع واللغات وأنواع المهام)، مفضّلًا الأمثلة المتنوعة على كثير من المتشابهة.
10. أحوّل كل مثال إلى chat template للنموذج المستهدف (أدوار system/user/assistant والـ tokens الخاصة) بـ apply_chat_template في الـ tokenizer، وأتحقق من بعضها بفك ترميزها.
11. أبقي البيانات الخام للقراءة فقط وبإصدارات؛ وتكتب السكربتات إلى إصدارات مخرجات جديدة، فيمكن دائمًا إعادة التشغيل من الأصل السليم عند وجود خطأ.
12. التجربة: أشغّل الـ pipeline كاملًا على ~1,000 مثال وأتحقق من أعداد المحذوف في كل خطوة، وأفحص عينات من المحتفظ به والمحذوف، وأتحقق من الشكل والقالب، وأقيس زمن التشغيل لتقدير المهمة الكاملة.""",
    ),
    "COURSE-006.M09.L01.EX01": (
        """1. Prefill is compute-bound: high MFU and TTFT growing with input length show the GPU's arithmetic is saturated processing the prompt.
2. Decode is memory-bandwidth-bound: low MFU but high MBU - each token reads all weights and the KV cache from memory while doing little computation.
3. "GPU activity near 100%" only says the GPU is busy, not whether its compute units or memory bandwidth are used efficiently; MFU and MBU show which resource is the limit.
4. Prefill: prompt caching for repeated prefixes (system prompts), chunked prefill, and faster attention kernels (FlashAttention); also separating prefill from decode on different machines.
5. Decode: continuous batching (more sequences share each weight read), KV-cache quantization or GQA models, and speculative decoding.
6. Weight (and KV-cache) quantization reduces the bytes read from memory per token, which is exactly the bottleneck in decode, so tokens per second rise.
7. SLO: TTFT p95 < 1 s for inputs up to 4k tokens, and TPOT p95 < 50 ms.
8. Goodput counts only requests that meet the SLO; raw throughput can rise by batching while many users get unacceptable latency, so goodput measures useful capacity.
9. TTFT, TPOT and end-to-end latency at p50, p95 and p99 (sliced by input length), plus goodput and tokens per second.
10. Replay realistic traffic at several batch-size limits; for each, measure throughput, TTFT/TPOT percentiles and goodput; choose the largest batch size whose p95/p99 still meets the SLO (where goodput peaks).""",
        """1. الـ prefill محدود بالحوسبة (compute-bound): ارتفاع الـ MFU ونمو الـ TTFT مع طول المدخل يوضحان أن حساب الـ GPU مشبَع بمعالجة الـ prompt.
2. الـ decode محدود بعرض نطاق الذاكرة (memory-bandwidth-bound): MFU منخفض لكن MBU مرتفع - فكل token يقرأ كل الـ weights والـ KV cache من الذاكرة مع حساب قليل.
3. "نشاط GPU قرب 100%" يعني فقط أن الـ GPU مشغولة، لا أن وحدات الحساب أو عرض نطاق الذاكرة مستخدمة بكفاءة؛ أما MFU وMBU فيوضحان أي مورد هو القيد.
4. الـ prefill: الـ prompt caching للبادئات المتكررة (system prompts)، والـ chunked prefill، وkernels انتباه أسرع (FlashAttention)؛ وكذلك فصل الـ prefill عن الـ decode على أجهزة مختلفة.
5. الـ decode: الـ continuous batching (تتشارك تسلسلات أكثر في كل قراءة للـ weights)، وتقليل دقة الـ KV cache أو نماذج GQA، والـ speculative decoding.
6. الـ quantization للـ weights (والـ KV cache) يقلل عدد الـ bytes المقروءة من الذاكرة لكل token، وهو عنق الزجاجة نفسه في الـ decode، فيرتفع عدد الـ tokens في الثانية.
7. الـ SLO: ‏TTFT p95 أقل من ثانية لمدخلات حتى 4k token، وTPOT p95 أقل من 50 ms.
8. الـ goodput يحسب فقط الطلبات التي تحقق الـ SLO؛ فقد يرتفع الـ throughput الخام بالتجميع بينما يحصل مستخدمون كثيرون على زمن غير مقبول، لذا يقيس الـ goodput السعة المفيدة.
9. الـ TTFT والـ TPOT وزمن الاستجابة الكلي عند p50 وp95 وp99 (مقسمة حسب طول المدخل)، مع الـ goodput وعدد الـ tokens في الثانية.
10. أعيد تشغيل حركة واقعية بعدة حدود لحجم الدفعة؛ ولكل منها أقيس الـ throughput ومئينات TTFT/TPOT والـ goodput؛ وأختار أكبر حجم دفعة ما زالت فيه p95/p99 تحقق الـ SLO (حيث يبلغ الـ goodput ذروته).""",
    ),
    "COURSE-006.M09.L01.EX02": (
        """1. 2 x 8 x 4096 x 32 x 4096 x 2 = 17,179,869,184 bytes.
2. About 17.2 GB (16 GiB).
3. S = 8192: about 34.4 GB - the cache grows linearly with sequence length.
4. M = 1 byte (e.g. 8-bit KV cache): about 8.6 GB.
5. Doubling B doubles the cache again (about 34.4 GB at S = 4096): every extra concurrent sequence needs its own keys and values.
6. In MQA/GQA, many query heads share fewer key/value heads, so the cache stores K and V for fewer heads - the H term effectively becomes num_kv_heads x head_dim, e.g. 8 KV heads instead of 32 gives a 4x smaller cache.
7. PagedAttention stores the cache in small fixed-size blocks allocated on demand instead of reserving the maximum sequence length for every request; it removes fragmentation and over-reservation, so far more of the theoretical memory holds real tokens and blocks can be shared between requests with the same prefix.
8. Experiment: same model, hardware and realistic prompt/output length distribution; increase the number of simultaneous users until the TTFT/TPOT SLO is violated or requests are rejected for lack of memory; record maximum concurrency and goodput before and after (e.g. 8-bit KV cache plus PagedAttention), and confirm answer quality on an evaluation set did not degrade.""",
        """1. ‏2 × 8 × 4096 × 32 × 4096 × 2 = 17,179,869,184 byte.
2. نحو 17.2 GB ‏(16 GiB).
3. عند S = 8192: نحو 34.4 GB - فالـ cache يكبر خطيًا مع طول التسلسل.
4. عند M = 1 byte (مثل KV cache بـ 8-bit): نحو 8.6 GB.
5. مضاعفة B تضاعف الـ cache مرة أخرى (نحو 34.4 GB عند S = 4096): كل تسلسل متزامن إضافي يحتاج keys وvalues خاصة به.
6. في MQA/GQA تتشارك heads الـ query الكثيرة عددًا أقل من heads الـ key/value، فيخزن الـ cache قيم K وV لعدد أقل من الـ heads - أي يصبح الحد H فعليًا num_kv_heads × head_dim، فمثلًا 8 KV heads بدل 32 تعطي cache أصغر بأربع مرات.
7. يخزن PagedAttention الـ cache في كتل صغيرة ثابتة الحجم تُخصَّص عند الحاجة بدلًا من حجز أقصى طول تسلسل لكل طلب؛ فيزيل التجزؤ والحجز الزائد، فيحمل جزء أكبر بكثير من الذاكرة النظرية tokens حقيقية، ويمكن مشاركة الكتل بين الطلبات ذات البادئة نفسها.
8. التجربة: النموذج والعتاد نفسهما مع توزيع واقعي لأطوال الـ prompts والمخرجات؛ أزيد عدد المستخدمين المتزامنين حتى يُخرق الـ SLO للـ TTFT/TPOT أو تُرفض طلبات لنقص الذاكرة؛ وأسجل أقصى تزامن والـ goodput قبل التحسين وبعده (مثل KV cache بـ 8-bit مع PagedAttention)، وأتأكد من عدم تراجع جودة الإجابات على مجموعة تقييم.""",
    ),
    "COURSE-006.M09.L01.EX03": (
        """1. Online path for interactive users (strict TTFT/TPOT SLOs); batch path for nightly jobs (offline batch inference on spare or cheaper capacity, maximizing throughput, no latency SLO).
2. Continuous batching online: requests join and leave the running batch at every decoding step, which suits variable lengths and keeps TTFT low.
3. Yes: prompt (prefix) caching stores the KV cache of the long, shared system prompt, so it is not recomputed for every request - lower TTFT and cost.
4. Yes, worth it here: long documents make prefill heavy and would stall the decode steps of other users; separate prefill and decode workers (each scaled and optimized for its bottleneck) protect TTFT/TPOT.
5. The model does not fit on one GPU: tensor parallelism within a node to split each layer (pipeline parallelism across nodes if needed), context/sequence parallelism for the very long documents, and replica parallelism of that whole setup to handle more users.
6. With static batching every request waits for the longest one (2,000 tokens) while short ones (20 tokens) finish early, wasting slots; continuous batching refills a slot as soon as a sequence finishes.
7. Targets: TTFT p95 < 1 s (< 3 s for long documents), TPOT p95 < 40 ms, end-to-end p99 < 30 s for the longest answers, throughput tracked in tokens/s, and goodput >= 95% of requests within SLO.
8. Weight quantization (e.g. 8-bit or 4-bit) reduces memory and the number of GPUs needed and speeds memory-bound decode; KV-cache quantization supports more concurrent long contexts.
9. Speculative decoding helps long, predictable outputs (for example reformatting a document or code) when a small draft model guesses many tokens correctly, so the large model verifies several tokens per step.
10. Run the same offline evaluation set (task accuracy, faithfulness, format validity) on the unoptimized and optimized service and compare; additionally A/B test a slice of live traffic and watch user feedback before full rollout.""",
        """1. مسار online للمستخدمين التفاعليين (SLOs صارمة للـ TTFT/TPOT)؛ ومسار batch للمهام الليلية (استدلال دفعي offline على سعة فائضة أو أرخص لتعظيم الـ throughput بلا SLO لزمن الاستجابة).
2. continuous batching للمسار المباشر: تنضم الطلبات وتغادر الدفعة الجارية في كل خطوة decoding، وهذا يناسب الأطوال المتغيرة ويبقي الـ TTFT منخفضًا.
3. نعم: الـ prompt (prefix) caching يخزن الـ KV cache الخاص بالـ system prompt الطويل المشترك، فلا يُعاد حسابه لكل طلب - TTFT وتكلفة أقل.
4. نعم، مفيد هنا: المستندات الطويلة تجعل الـ prefill ثقيلًا وقد تعطل خطوات الـ decode لمستخدمين آخرين؛ وفصل workers الـ prefill عن الـ decode (كلٌّ يُوسَّع ويُحسَّن لعنق زجاجته) يحمي الـ TTFT/TPOT.
5. النموذج لا يتسع لـ GPU واحدة: tensor parallelism داخل العقدة لتقسيم كل طبقة (وpipeline parallelism عبر العقد إن لزم)، وcontext/sequence parallelism للمستندات الطويلة جدًا، وreplica parallelism لهذا الإعداد كاملًا لخدمة مستخدمين أكثر.
6. مع الـ static batching ينتظر كل طلب الأطول (2,000 token) بينما تنتهي القصيرة (20 token) مبكرًا فتُهدر الأماكن؛ أما الـ continuous batching فيملأ المكان بمجرد انتهاء تسلسل.
7. الأهداف: TTFT p95 أقل من ثانية (أقل من 3 ثوانٍ للمستندات الطويلة)، وTPOT p95 أقل من 40 ms، وزمن كلي p99 أقل من 30 ثانية لأطول الإجابات، وthroughput يُتابع بالـ tokens في الثانية، وgoodput لا يقل عن 95% من الطلبات ضمن الـ SLO.
8. الـ weight quantization ‏(مثل 8-bit أو 4-bit) يقلل الذاكرة وعدد وحدات GPU المطلوبة ويسرّع الـ decode المحدود بالذاكرة؛ والـ KV-cache quantization يدعم سياقات طويلة متزامنة أكثر.
9. الـ speculative decoding يفيد المخرجات الطويلة المتوقعة (مثل إعادة تنسيق مستند أو كود) عندما يخمّن نموذج مسودة صغير tokens كثيرة صحيحة، فيتحقق النموذج الكبير من عدة tokens في كل خطوة.
10. أشغّل مجموعة التقييم offline نفسها (دقة المهمة والأمانة وصلاحية الشكل) على الخدمة قبل التحسين وبعده وأقارن؛ ثم اختبار A/B على شريحة من الحركة الحية مع مراقبة تغذية المستخدمين قبل التعميم.""",
    ),
    "COURSE-006.M10.L01.EX01": (
        """1. Context construction: retrieve relevant policy passages (RAG) and fetch the customer's records (orders, plan) through internal APIs, and insert them into the prompt with clear labels.
2. Input guardrails: block prompt-injection attempts and off-topic or abusive requests; mask PII. Output guardrails: block responses containing other customers' data or secrets; check the answer is supported by the retrieved policy (and has no forbidden promises such as unapproved refunds).
3. PII masking: detect emails, phone numbers, card and ID numbers in the user message and records, replace them with placeholders ([EMAIL_1]) before calling the external model, keep the mapping server-side, and restore values in the response only where needed.
4. Router intents: order status, returns/refunds, billing questions, technical product help, account/security issues (routed to a human), and out-of-scope chit-chat.
5. Model gateway: one interface to all model providers, with API keys, access control, rate limits, cost tracking, logging, retries and fallback between models.
6. Exact caching: only non-personalized questions with identical normalized text, such as "What is your return policy?"
7. Semantic caching only for generic FAQ-type questions; evaluate false hits by sampling cache hits and having reviewers (or a judge) check whether the cached answer truly answers the new query - require a very high threshold and a false-hit rate below e.g. 1%.
8. "Where is my order?" depends on the specific customer's data and must never be answered from a shared cache.
9. Fallback: on provider outage or timeout, the gateway switches to a secondary model/provider; after repeated bad responses (failed output checks), retry once, then answer with a safe template and escalate to a human.
10. Flow: query -> input guardrails (injection check, PII masking) -> router -> context construction (RAG + customer records) -> cache lookup (only for generic intents) -> model gateway -> LLM -> output guardrails -> PII restore -> response, with logging at every step. Each component exists to address a specific production risk: missing knowledge, unsafe inputs/outputs, cost and latency, wrong handling of intents, and provider failures.""",
        """1. بناء السياق: استرجاع مقاطع السياسات المناسبة (RAG) وجلب سجلات العميل (الطلبات والخطة) عبر APIs داخلية وإدراجها في الـ prompt بتسميات واضحة.
2. ضوابط المدخل: حجب محاولات prompt injection والطلبات الخارجة عن الموضوع أو المسيئة؛ وإخفاء البيانات الشخصية. ضوابط المخرج: حجب الردود التي تحتوي بيانات عملاء آخرين أو أسرارًا؛ والتحقق من أن الإجابة مدعومة بالسياسة المسترجعة (وبلا وعود محظورة مثل استرداد غير معتمد).
3. إخفاء البيانات الشخصية: كشف البريد والهواتف وأرقام البطاقات والهوية في رسالة المستخدم والسجلات، واستبدالها برموز ([EMAIL_1]) قبل استدعاء النموذج الخارجي، والاحتفاظ بالربط على الخادم، واستعادة القيم في الرد عند الحاجة فقط.
4. نوايا الموجّه: حالة الطلب، الإرجاع والاسترداد، أسئلة الفواتير، مساعدة فنية للمنتج، مشكلات الحساب والأمان (تُحال لموظف)، ودردشة خارج النطاق.
5. بوابة النماذج (model gateway): واجهة واحدة لكل مزودي النماذج مع مفاتيح الـ API والتحكم في الوصول وحدود المعدل وتتبع التكلفة والتسجيل وإعادة المحاولة والتحويل بين النماذج.
6. التخزين المؤقت الدقيق: فقط للأسئلة غير المخصصة ذات النص الموحَّد المتطابق، مثل "What is your return policy?"
7. الـ semantic caching فقط لأسئلة FAQ العامة؛ وأقيّم الإصابات الخاطئة بسحب عينة من الإصابات يراجعها مقيّمون (أو حكم) للتحقق من أن الإجابة المخزنة تجيب فعلًا عن الاستعلام الجديد - مع عتبة عالية جدًا ونسبة إصابات خاطئة أقل من 1% مثلًا.
8. "Where is my order?" يعتمد على بيانات العميل نفسه ولا يجب أبدًا إجابته من cache مشترك.
9. البديل: عند انقطاع المزود أو انتهاء المهلة تحوّل البوابة إلى نموذج أو مزود ثانٍ؛ وبعد ردود سيئة متكررة (فشل فحوص المخرج) أعيد المحاولة مرة ثم أجيب بقالب آمن وأصعّد إلى موظف.
10. التدفق: الاستعلام -> ضوابط المدخل (فحص الحقن وإخفاء البيانات) -> الموجّه -> بناء السياق (RAG وسجلات العميل) -> البحث في الـ cache (للنوايا العامة فقط) -> بوابة النماذج -> الـ LLM -> ضوابط المخرج -> استعادة البيانات -> الرد، مع التسجيل في كل خطوة. كل مكوّن موجود لمعالجة خطر إنتاجي محدد: نقص المعرفة، والمدخلات/المخرجات غير الآمنة، والتكلفة وزمن الاستجابة، وسوء التعامل مع النوايا، وأعطال المزودين.""",
    ),
    "COURSE-006.M10.L01.EX02": (
        """1-2. Failure modes and metrics: retrieval misses (recall@k on a labelled sample, share of queries with no relevant chunk); unsupported answers (faithfulness score from a judge on sampled answers); wrong or missing escalation (escalation precision/recall vs. reviewed labels); tool/search errors (tool error rate, timeouts); slow or costly responses (latency and cost per request above budget).
3. TTFT, TPOT, end-to-end latency and cost per request, sliced by model, route/intent, input length bucket, user segment and with/without tool calls.
4. Exhaustive (cheap): latency, cost, tool errors, empty retrievals, format validity, guardrail triggers, user feedback. Sampled (expensive): judge-based faithfulness/correctness and human review.
5. Log: model name and version, prompt template version, temperature and other parameters, retriever and embedding model versions, index snapshot ID, top-k, reranker, tool definitions/versions, and guardrail configuration.
6. Trace: request ID -> query rewrite (input/output, ms) -> retrieval (query, returned chunk IDs and scores, ms) -> rerank (order, ms) -> prompt assembly (token count) -> LLM call (model, tokens, TTFT, TPOT, cost) -> tool calls -> output guardrails -> escalation decision -> response.
7. Alerts: error or timeout rate above baseline, p95 latency above SLO, empty-retrieval rate jump, faithfulness score drop on the rolling sample, sudden rise in escalations or negative feedback, cost per hour above budget.
8. For MTTR: full trace of the failing request with prompt, retrieved chunks, model output and versions; the ability to replay a request against a given configuration; a recent-deploy/config change log.
9. Prompt drift: compare prompt template versions and the distribution of token counts. User-behavior drift: monitor query topics, languages and length distributions against the baseline (embedding clusters). Provider-model drift: run a fixed canary evaluation set daily against the provider and alert on score changes.
10. Every confirmed production failure (reviewed thumbs-down, escalation error) is anonymized, labelled with the correct behaviour and added to the evaluation set, so regressions are caught before the next release.
11. Parallel: retrieving from the document index and fetching the user's records; running output guardrail checks concurrently with formatting.
12. The orchestrator must expose each step's inputs, outputs, timings and errors (the full trace and prompts actually sent), not only the final answer.""",
        """1-2. أنماط الفشل ومقاييسها: إخفاق الاسترجاع (recall@k على عينة مصنفة، ونسبة الاستعلامات بلا chunk مناسب)؛ وإجابات غير مدعومة (درجة الأمانة من حكم على إجابات مسحوبة)؛ وتصعيد خاطئ أو مفقود (precision/recall للتصعيد مقابل تسميات مراجَعة)؛ وأخطاء الأدوات والبحث (نسبة أخطاء الأدوات وانتهاء المهلة)؛ وردود بطيئة أو مكلفة (زمن وتكلفة لكل طلب فوق الميزانية).
3. الـ TTFT والـ TPOT والزمن الكلي والتكلفة لكل طلب، مقسمة حسب النموذج، والمسار/النية، وفئة طول المدخل، وشريحة المستخدمين، ووجود استدعاءات أدوات.
4. شامل (رخيص): زمن الاستجابة والتكلفة وأخطاء الأدوات والاسترجاع الفارغ وصلاحية الشكل وتفعيل الضوابط وتقييمات المستخدمين. على عينة (مكلف): الأمانة والصحة بالحكم ومراجعة بشرية.
5. التسجيل: اسم النموذج وإصداره، وإصدار قالب الـ prompt، والـ temperature وغيرها، وإصدارات المسترجع ونموذج الـ embedding، ومعرّف لقطة الفهرس، وقيمة top-k، والـ reranker، وتعريفات الأدوات وإصداراتها، وإعدادات الضوابط.
6. التتبع: معرّف الطلب -> إعادة صياغة الاستعلام (المدخل والمخرج والزمن) -> الاسترجاع (الاستعلام ومعرّفات الـ chunks ودرجاتها والزمن) -> إعادة الترتيب (الترتيب والزمن) -> تجميع الـ prompt ‏(عدد الـ tokens) -> استدعاء الـ LLM ‏(النموذج والـ tokens وTTFT وTPOT والتكلفة) -> استدعاءات الأدوات -> ضوابط المخرج -> قرار التصعيد -> الرد.
7. التنبيهات: نسبة أخطاء أو انتهاء مهلة فوق الأساس، وp95 لزمن الاستجابة فوق الـ SLO، وقفزة في نسبة الاسترجاع الفارغ، وانخفاض درجة الأمانة على العينة المتجددة، وارتفاع مفاجئ في التصعيد أو التقييمات السلبية، وتكلفة الساعة فوق الميزانية.
8. لتقليل MTTR: تتبع كامل للطلب الفاشل مع الـ prompt والـ chunks المسترجعة ومخرج النموذج والإصدارات؛ وإمكانية إعادة تشغيل طلب على إعداد محدد؛ وسجل لأحدث عمليات النشر وتغييرات الإعدادات.
9. انجراف الـ prompt: مقارنة إصدارات القوالب وتوزيع أعداد الـ tokens. انجراف سلوك المستخدمين: مراقبة مواضيع الاستعلامات ولغاتها وأطوالها مقارنة بالأساس (مجموعات الـ embeddings). انجراف نموذج المزود: تشغيل مجموعة تقييم canary ثابتة يوميًا على المزود والتنبيه عند تغير النتائج.
10. كل فشل إنتاجي مؤكد (تقييم سلبي مراجَع أو خطأ تصعيد) تُزال منه البيانات الشخصية ويُصنَّف بالسلوك الصحيح ويُضاف إلى مجموعة التقييم، فتُكتشف التراجعات قبل الإصدار التالي.
11. بالتوازي: الاسترجاع من فهرس المستندات وجلب سجلات المستخدم؛ وتشغيل فحوص ضوابط المخرج بالتزامن مع التنسيق.
12. يجب أن يكشف الـ orchestrator مدخلات كل خطوة ومخرجاتها وتوقيتها وأخطاءها (التتبع الكامل والـ prompts المرسلة فعلًا)، لا الإجابة النهائية فقط.""",
    ),
    "COURSE-006.M10.L01.EX03": (
        """1. Explicit: thumbs up/down on each suggestion; a 1-5 rating with optional comment after a longer draft; side-by-side choice between two versions.
2-3. Implicit signals (and alternative interpretations): accepting a suggestion unchanged (good - or the user did not read it); heavy editing of accepted text (poor quality - or personal style); regenerating (bad answer - or wanting more options); copying the text (useful - or copying to compare elsewhere); abandoning the draft (unhelpful - or interrupted); asking "make it shorter" (too long - or a different audience this time).
4. Ask after meaningful moments (finishing a document, a regenerate after several tries), rarely and never mid-flow; stay silent during focused writing and do not ask the same user repeatedly.
5. The user's edited final text vs. the model's original: (prompt, chosen = edited version, rejected = original) - filtered to edits that change meaning or quality, not just typo fixes.
6. The user's request, the shown response, previous turns, any document context the model used, and which version was downvoted.
7. Ask explicit permission before storing the context with a downvote ("Share this conversation to help improve suggestions?"), explain what is kept and for how long, remove personal data, and allow opting out.
8. Show the same pair in both orders to different users (randomized positions) and compare the win rate of the first position; a difference shows position bias.
9. Leniency: users who rate nearly everything 5 stars or upvote everything - normalize per user or weight by variance. Random clicks: impossibly fast ratings, inconsistent answers on repeated comparisons (insert duplicate pairs to check consistency).
10. Do not train only on content users already liked from the model's own outputs; keep a fixed, human-written evaluation set and a share of exploration, and cap the influence of any single user or cohort.
11. Users tend to approve answers that agree with them; checking correctness separately against facts (references, judges for factual accuracy) prevents the model from learning to please instead of being right.
12. Evaluation: aggregated, debiased feedback becomes test cases and metrics. Personalization: one user's explicit preferences adapt that user's experience only. Training: only consented, filtered, high-quality preference pairs are used, after review.""",
        """1. صريحة: إعجاب/عدم إعجاب لكل اقتراح؛ وتقييم من 1 إلى 5 مع تعليق اختياري بعد مسودة أطول؛ واختيار بين نسختين جنبًا إلى جنب.
2-3. إشارات ضمنية (وتفسيرات بديلة): قبول الاقتراح دون تغيير (جيد - أو لم يقرأه المستخدم)؛ وتعديل كبير للنص المقبول (جودة ضعيفة - أو أسلوب شخصي)؛ وإعادة التوليد (إجابة سيئة - أو رغبة في خيارات أكثر)؛ ونسخ النص (مفيد - أو نسخه للمقارنة في مكان آخر)؛ وترك المسودة (غير مفيدة - أو انقطاع)؛ وطلب "make it shorter" (طويل جدًا - أو جمهور مختلف هذه المرة).
4. أسأل بعد لحظات ذات معنى (إنهاء مستند، أو إعادة توليد بعد عدة محاولات)، نادرًا ولا أقطع الكتابة أبدًا؛ وأصمت أثناء الكتابة المركزة ولا أكرر السؤال للمستخدم نفسه.
5. نص المستخدم النهائي المعدّل مقابل الأصل من النموذج: ‏(prompt، المختار = النسخة المعدلة، المرفوض = الأصل) - مع ترشيح التعديلات التي تغيّر المعنى أو الجودة لا تصحيح الأخطاء الإملائية فقط.
6. طلب المستخدم، والرد المعروض، والأدوار السابقة، وأي سياق مستند استخدمه النموذج، وأي نسخة نالت التقييم السلبي.
7. أطلب إذنًا صريحًا قبل حفظ السياق مع التقييم السلبي ("Share this conversation to help improve suggestions?")، وأوضح ما يُحفظ ومدته، وأزيل البيانات الشخصية، وأتيح إلغاء المشاركة.
8. أعرض الزوج نفسه بالترتيبين على مستخدمين مختلفين (مواضع عشوائية) وأقارن نسبة فوز الموضع الأول؛ والفرق يكشف انحياز الموضع.
9. التساهل: مستخدمون يقيّمون كل شيء تقريبًا 5 نجوم أو يعجبون بكل شيء - أطبّع لكل مستخدم أو أعطي وزنًا حسب التباين. النقرات العشوائية: تقييمات سريعة بشكل مستحيل، وإجابات غير متسقة في المقارنات المكررة (بإدراج أزواج مكررة للتحقق من الاتساق).
10. لا أدرّب فقط على محتوى أعجب المستخدمين من مخرجات النموذج نفسه؛ بل أحتفظ بمجموعة تقييم ثابتة مكتوبة بشريًا ونسبة من الاستكشاف، وأحد من تأثير أي مستخدم أو مجموعة منفردة.
11. يميل المستخدمون إلى استحسان الإجابات التي توافقهم؛ والتحقق المنفصل من الصحة مقابل الحقائق (مراجع وحكام للدقة الواقعية) يمنع النموذج من تعلم إرضاء المستخدم بدلًا من الصواب.
12. التقييم: التغذية الراجعة المجمعة بعد إزالة الانحياز تصبح حالات اختبار ومقاييس. التخصيص: تفضيلات المستخدم الصريحة تكيّف تجربته وحده. التدريب: تُستخدم فقط أزواج تفضيل مُوافَق عليها ومرشحة وعالية الجودة بعد المراجعة.""",
    ),
}
