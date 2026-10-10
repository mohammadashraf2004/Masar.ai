"""COURSE-004 Applied NLP with Transformers: example answers for written exercises."""

EXAMPLES = {
    "COURSE-004.M01.L01.EX01": (
        """2. In a simple encoder-decoder, the final encoder state must squeeze in everything about the sentence - "camera" as the subject, that it was ordered last month, and that it arrived damaged - because it is the only thing the decoder ever sees.
3. When generating the translation of "camera", the attention weight should be largest on the encoder position of "camera" (with some weight on "The").
4. With attention, the decoder can look back at every encoder state at each step and weight the relevant ones, so information no longer has to survive in one fixed-size vector; long sentences lose far less detail.
5. Encoder-decoder attention connects two sequences - decoder positions attend to the encoder's states. Self-attention works within one sequence - every token attends to the other tokens of the same sentence.""",
        """2. في الـ encoder-decoder البسيط يجب أن تحشر الحالة الأخيرة للـ encoder كل شيء عن الجملة - "camera" كفاعل، وأنها طُلبت الشهر الماضي، وأنها وصلت تالفة - لأنها الشيء الوحيد الذي يراه الـ decoder.
3. عند توليد ترجمة "camera" يجب أن يكون أكبر وزن attention على موضع "camera" في الـ encoder (مع بعض الوزن على "The").
4. مع الـ attention يستطيع الـ decoder في كل خطوة الرجوع إلى كل حالات الـ encoder وإعطاء الوزن للمهم منها، فلا تضطر المعلومات للبقاء في متجه واحد ثابت الحجم؛ وتفقد الجمل الطويلة تفاصيل أقل بكثير.
5. attention بين الـ encoder والـ decoder يربط تسلسلين - مواضع الـ decoder تنتبه إلى حالات الـ encoder. أما الـ self-attention فيعمل داخل تسلسل واحد - كل token ينتبه إلى tokens الجملة نفسها.""",
    ),
    "COURSE-004.M01.L01.EX02": (
        """1. Review positive/negative - text classification.
2. Company and city names - NER.
3. "When will my order arrive?" from a policy paragraph - extractive question answering.
4. Long complaint to three sentences - summarization.
5. English to German - translation.
6. Continue a support reply - text generation.

from transformers import pipeline
classifier = pipeline("text-classification")
classifier("The delivery was fast and the product works perfectly.")
# -> a list like [{"label": "POSITIVE", "score": 0.99}]

reader = pipeline("question-answering")
reader(question="When will my order arrive?", context=policy_text)
# -> a dict with "answer" (a span copied from the paragraph), "score", "start" and "end" """,
        """1. مراجعة إيجابية/سلبية - text classification.
2. أسماء الشركات والمدن - NER.
3. "When will my order arrive?" من فقرة سياسة الشحن - extractive question answering.
4. شكوى طويلة إلى ثلاث جمل - summarization.
5. من الإنجليزية إلى الألمانية - translation.
6. استكمال رد خدمة العملاء - text generation.

from transformers import pipeline
classifier = pipeline("text-classification")
classifier("The delivery was fast and the product works perfectly.")
# -> قائمة مثل [{"label": "POSITIVE", "score": 0.99}]

reader = pipeline("question-answering")
reader(question="When will my order arrive?", context=policy_text)
# -> قاموس فيه "answer" (مقطع منسوخ من الفقرة) و"score" و"start" و"end" """,
    ),
    "COURSE-004.M02.L01.EX02": (
        """| | Feature extraction | Fine-tuning |
| Parameters updated | Only the separate classifier (e.g. logistic regression) on frozen hidden states | All DistilBERT weights plus the classification head |
| Trade-off | Cheap: hidden states computed once, runs on CPU; lower accuracy | Needs a GPU and more training time; much higher accuracy |
| Chapter result | About 63% validation accuracy | About 92% validation accuracy (F1 ~0.92) |

4. The dataset is imbalanced, so a model that always predicts the most frequent class already scores about 35%. Comparing 63% with that baseline shows the frozen features genuinely carry emotion information rather than just exploiting class frequencies.
5. The confusion matrix showed anger and fear most often confused with sadness, and love and surprise frequently mistaken for joy.
6. Among the highest-loss validation examples I would check for wrong or ambiguous labels, texts whose emotion is genuinely unclear, and systematic patterns (for example a confusion between two emotions); if the errors are mostly label noise, a larger model will not fix them and cleaning the data is the better next step.""",
        """| | feature extraction | fine-tuning |
| الـ parameters المحدَّثة | المصنف المنفصل فقط (مثل logistic regression) على hidden states مجمدة | كل weights الـ DistilBERT مع رأس التصنيف |
| المقايضة | رخيص: تُحسب الـ hidden states مرة واحدة ويعمل على CPU؛ دقة أقل | يحتاج GPU ووقت تدريب أطول؛ دقة أعلى بكثير |
| نتيجة الفصل | نحو 63% validation accuracy | نحو 92% validation accuracy (F1 قرابة 0.92) |

4. البيانات غير متوازنة، فالنموذج الذي يتنبأ دائمًا بالفئة الأكثر تكرارًا يحقق نحو 35%. ومقارنة 63% بهذا الأساس توضح أن الـ features المجمدة تحمل معلومات حقيقية عن المشاعر لا مجرد استغلال لتكرار الفئات.
5. أظهرت الـ confusion matrix أن anger وfear تُخلطان غالبًا بـ sadness، وأن love وsurprise كثيرًا ما تُخطأ إلى joy.
6. في أمثلة الـ validation الأعلى loss أبحث عن تسميات خاطئة أو غامضة، ونصوص مشاعرها غير واضحة فعلًا، وأنماط منهجية (مثل خلط بين شعورين)؛ فإذا كانت الأخطاء غالبًا ضوضاء في التسميات فلن يصلحها نموذج أكبر، وتنظيف البيانات هو الخطوة الأفضل.""",
    ),
    "COURSE-004.M01.L02.EX01": (
        """2. "time flies like an arrow": "time" and "arrow" - with them "flies" is a verb (time passes quickly). "fruit flies like a banana": "fruit" and "banana" - with them "flies" is a noun (insects) and "like" is a verb.
3. A fixed embedding gives "flies" the same vector in both sentences, so the model cannot tell the verb from the noun; the meaning depends on the context, which a static vector cannot see.
4. Self-attention updates the vector of "flies" as a weighted average of the other tokens' values, with weights from query-key similarity. In the first sentence the weights focus on "time" and "arrow", in the second on "fruit" and "banana", so the same input embedding becomes two different contextualized representations.""",
        """2. "time flies like an arrow": الكلمتان "time" و"arrow" - معهما تكون "flies" فعلًا (الوقت يمر سريعًا). "fruit flies like a banana": الكلمتان "fruit" و"banana" - معهما تكون "flies" اسمًا (حشرات) و"like" فعلًا.
3. الـ embedding الثابت يعطي "flies" المتجه نفسه في الجملتين، فلا يستطيع النموذج التمييز بين الفعل والاسم؛ فالمعنى يعتمد على السياق الذي لا يراه متجه ثابت.
4. يحدّث self-attention متجه "flies" كمتوسط موزون لقيم الـ tokens الأخرى، بأوزان من تشابه الـ query والـ key. في الجملة الأولى تتركز الأوزان على "time" و"arrow"، وفي الثانية على "fruit" و"banana"، فيصبح الـ embedding نفسه تمثيلين سياقيين مختلفين.""",
    ),
    "COURSE-004.M01.L02.EX02": (
        """| Step | Shape |
| Token embeddings | [2, 6, 768] |
| Head dimension | 768 / 12 = 64 |
| One head's attention scores | [2, 6, 6] (every token against every token) |
| One head's output | [2, 6, 64] |
| All heads concatenated (and projected) | [2, 6, 768] |

6. Positional embeddings have the same shape as the token embeddings ([2, 6, 768]) and are added element by element, so they change the values, not the shape.
7. The classification head takes one vector per sequence (for example the [CLS] position, shape [2, 768]) and its final linear layer maps the hidden dimension 768 to the number of labels: [2, num_labels].""",
        """| الخطوة | الشكل |
| token embeddings | [2, 6, 768] |
| بُعد الـ head | 768 ÷ 12 = 64 |
| درجات الانتباه لـ head واحد | [2, 6, 6] (كل token مقابل كل token) |
| مخرج head واحد | [2, 6, 64] |
| كل الـ heads بعد الضم (والإسقاط) | [2, 6, 768] |

6. للـ positional embeddings نفس شكل الـ token embeddings ‏([2, 6, 768]) وتُجمع عنصرًا بعنصر، فتغير القيم لا الشكل.
7. يأخذ رأس التصنيف متجهًا واحدًا لكل تسلسل (مثل موضع [CLS] بشكل [2, 768])، وتحوّل طبقته الخطية الأخيرة البُعد المخفي 768 إلى عدد التسميات: [2, num_labels].""",
    ),
    "COURSE-004.M01.L03.EX01": (
        """Source language: German (12,000 labels). Target language: French (100 labels).
2. A German-only model has never learned French vocabulary or names, so it performs poorly on French users, and the product must serve both.
3. A multilingual pretrained model (for example XLM-R) shares one representation across ~100 languages, so entity patterns learned from German labels partly transfer to French.
4. Fine-tune on German only, then evaluate directly on a held-out French test set (zero-shot); compare with fine-tuning on the 100 French sentences, and with German + French combined.
5. Entity-level F1 (seqeval), computed on the same French test set for every strategy.
6. If zero-shot and combined-training French F1 stay clearly below German F1, and adding French examples (for example 25 -> 50 -> 100) keeps improving French F1 noticeably, then more French labels are worth collecting.""",
        """لغة المصدر: الألمانية (12,000 تسمية). اللغة الهدف: الفرنسية (100 تسمية).
2. النموذج الألماني فقط لم يتعلم مفردات أو أسماء فرنسية، فيكون أداؤه ضعيفًا مع المستخدمين الفرنسيين، والمنتج يجب أن يخدم الاثنين.
3. النموذج متعدد اللغات المدرَّب مسبقًا (مثل XLM-R) يتشارك تمثيلًا واحدًا لنحو 100 لغة، فتنتقل أنماط الكيانات المتعلَّمة من التسميات الألمانية جزئيًا إلى الفرنسية.
4. أضبط النموذج على الألمانية فقط ثم أقيّمه مباشرة على مجموعة اختبار فرنسية محجوزة (zero-shot)؛ وأقارن ذلك بالضبط على الجمل الفرنسية المائة، وبالألمانية والفرنسية معًا.
5. entity-level F1 ‏(seqeval)، يُحسب على مجموعة الاختبار الفرنسية نفسها لكل استراتيجية.
6. إذا بقي F1 الفرنسي في zero-shot والتدريب المشترك أقل بوضوح من الألماني، واستمرت إضافة أمثلة فرنسية (مثل 25 ثم 50 ثم 100) في تحسين F1 الفرنسي بشكل ملحوظ، فإن جمع تسميات فرنسية أكثر يستحق.""",
    ),
    "COURSE-004.M01.L03.EX02": (
        """| Token | Word ID | Aligned label |
| <s> | None | -100 |
| ▁New | 0 | B-ORG |
| ▁York | 1 | I-ORG |
| ▁Univers | 2 | I-ORG |
| ity | 2 | -100 |
| </s> | None | -100 |

6. The lesson trains one prediction per word, taken from its first subword, and -100 makes the loss ignore every other position. Labelling both "▁Univers" and "ity" would make the model predict a label for subword pieces too, so longer words would count more in the loss and the training objective (and evaluation alignment) would no longer be word-level.""",
        """| الـ token | الـ word ID | التسمية بعد المحاذاة |
| <s> | None | -100 |
| ▁New | 0 | B-ORG |
| ▁York | 1 | I-ORG |
| ▁Univers | 2 | I-ORG |
| ity | 2 | -100 |
| </s> | None | -100 |

6. يدرّب الدرس تنبؤًا واحدًا لكل كلمة يؤخذ من أول subword لها، والقيمة -100 تجعل الـ loss يتجاهل كل موضع آخر. ووضع التسمية على "▁Univers" و"ity" معًا يجعل النموذج يتنبأ بتسميات لأجزاء الكلمات أيضًا، فتُحتسب الكلمات الأطول أكثر في الـ loss، ولا يعود هدف التدريب (ولا محاذاة التقييم) على مستوى الكلمة.""",
    ),
    "COURSE-004.M01.L04.EX01": (
        """Step 1: the distribution is help 0.50, be 0.30, learn 0.20; greedy decoding picks "help".
New input: "Machine learning can help".
Step 2: the distribution is solve 0.45, people 0.35, systems 0.20; greedy picks "solve" -> "Machine learning can help solve".
6. The model predicts the next token from the full current context. The second distribution is computed from "Machine learning can help"; had "be" been chosen, the context and therefore the probabilities would be different, so it cannot exist before the first token is selected and appended.""",
        """الخطوة 1: التوزيع help 0.50 وbe 0.30 وlearn 0.20؛ يختار الـ greedy decoding كلمة "help".
المدخل الجديد: "Machine learning can help".
الخطوة 2: التوزيع solve 0.45 وpeople 0.35 وsystems 0.20؛ يختار greedy كلمة "solve" -> "Machine learning can help solve".
6. يتنبأ النموذج بالـ token التالي من السياق الحالي كاملًا. التوزيع الثاني يُحسب من "Machine learning can help"؛ ولو اختيرت "be" لاختلف السياق ومعه الاحتمالات، فلا يمكن أن يوجد قبل اختيار الـ token الأول وإضافته.""",
    ),
    "COURSE-004.M01.L04.EX02": (
        """| Scenario | Starting strategy | Why |
| 1. Short, stable, deterministic output | Greedy or beam search | Always picks the most likely continuation, so results are repeatable |
| 2. Creative story | Sampling with temperature around 0.7-1.0 (with top-p) | Randomness gives varied, less predictable text |
| 3. Repeating phrases | Beam search or sampling with no_repeat_ngram_size (e.g. 3) | Forbids repeating the same n-gram, breaking loops |
| 4. Bizarre rare words while sampling | Top-k or top-p sampling | Cuts off the low-probability tail before sampling |

5. Top-k=50 always keeps exactly the 50 most likely tokens, while top-p=0.9 keeps the smallest set whose probabilities add up to 90%, so the number of candidates adapts to how confident the model is.""",
        """| الحالة | الاستراتيجية الأولية | السبب |
| 1. مخرج قصير ثابت حتمي | greedy أو beam search | يختار دائمًا الاستكمال الأرجح فتتكرر النتائج نفسها |
| 2. قصة إبداعية | sampling مع temperature بين 0.7 و1.0 تقريبًا (مع top-p) | العشوائية تعطي نصًا متنوعًا وأقل توقعًا |
| 3. تكرار العبارات | beam search أو sampling مع no_repeat_ngram_size (مثل 3) | يمنع تكرار الـ n-gram نفسه فيكسر الحلقات |
| 4. كلمات نادرة غريبة أثناء الـ sampling | top-k أو top-p sampling | يقطع ذيل الاحتمالات المنخفضة قبل الاختيار |

5. top-k=50 يحتفظ دائمًا بأرجح 50 token بالضبط، بينما يحتفظ top-p=0.9 بأصغر مجموعة مجموع احتمالاتها 90%، فيتكيف عدد المرشحين مع مدى ثقة النموذج.""",
    ),
    "COURSE-004.M01.L05.EX02": (
        """| Step | Decoder input so far | Target token |
| 1 | <s> | Alice |
| 2 | <s> Alice | called |
| 3 | <s> Alice called | Bob |
| 4 | <s> Alice called Bob | today |
| 5 | <s> Alice called Bob today | </s> |

4. The decoder learns to predict the next token, so its input is the gold summary shifted right by one (starting with <s>) and the labels are the unshifted tokens; at each position the input is the previous gold token - that is teacher forcing.
5. All positions are processed in parallel during training, so a causal mask must hide the future target tokens; otherwise the decoder would read the answer instead of predicting it, and it could never generate at inference time, where the future does not exist.
6. Padding positions get the label -100 so the loss ignores them; they carry no information and should not affect the gradients.""",
        """| الخطوة | مدخل الـ decoder حتى الآن | الـ token الهدف |
| 1 | <s> | Alice |
| 2 | <s> Alice | called |
| 3 | <s> Alice called | Bob |
| 4 | <s> Alice called Bob | today |
| 5 | <s> Alice called Bob today | </s> |

4. يتعلم الـ decoder التنبؤ بالـ token التالي، فمدخله هو الملخص الصحيح مزاحًا لليمين بموضع واحد (يبدأ بـ <s>)، والتسميات هي الـ tokens دون إزاحة؛ وفي كل موضع يكون المدخل هو الـ token الصحيح السابق - وهذا هو teacher forcing.
5. تُعالَج كل المواضع بالتوازي أثناء التدريب، فلا بد من causal mask يخفي الـ tokens الهدف المستقبلية؛ وإلا قرأ الـ decoder الإجابة بدلًا من التنبؤ بها، ولما استطاع التوليد وقت الاستدلال حيث لا يوجد المستقبل.
6. تأخذ مواضع الحشو التسمية -100 فيتجاهلها الـ loss؛ فهي لا تحمل معلومات ولا يجب أن تؤثر في الـ gradients.""",
    ),
    "COURSE-004.M01.L07.EX02": (
        """1. Recall measures whether the passage containing the answer is among the k retrieved ones; the more passages we keep, the more likely it is included.
2. The reader runs a full transformer over every retrieved passage, so its work - and the end-to-end latency - grows roughly linearly with k.
3. k=3 for a real-time shop: recall jumps from 0.72 to 0.94 at a reader cost of 105 ms; going to k=5 adds only 3 points of recall for 60 ms more, and k=10 more than triples the latency for 5 points. k=3 is the elbow (k=5 if the latency budget allows ~165 ms).
4. End-to-end exact match / F1 of the final answers on a labelled QA set at each k (since more passages can also distract the reader), together with the total end-to-end latency including retrieval, at p95 rather than average.""",
        """1. يقيس الـ recall ما إذا كان المقطع الذي يحتوي الإجابة ضمن المقاطع k المسترجعة؛ وكلما احتفظنا بمقاطع أكثر زاد احتمال وجوده.
2. يشغّل الـ reader نموذج transformer كاملًا على كل مقطع مسترجع، فيكبر عمله - وزمن الاستجابة الكلي - خطيًا تقريبًا مع k.
3. k=3 لمتجر لحظي: يقفز الـ recall من 0.72 إلى 0.94 بتكلفة 105 ms للـ reader؛ والانتقال إلى k=5 يضيف 3 نقاط recall فقط مقابل 60 ms إضافية، وk=10 يضاعف زمن الاستجابة أكثر من ثلاث مرات مقابل 5 نقاط. فـ k=3 هي نقطة الانعطاف (أو k=5 إذا سمحت الميزانية بنحو 165 ms).
4. exact match وF1 للإجابات النهائية على مجموعة أسئلة مصنفة عند كل k (فالمقاطع الإضافية قد تشتت الـ reader أيضًا)، مع زمن الاستجابة الكلي شاملًا الاسترجاع، بقيمة p95 لا المتوسط.""",
    ),
    "COURSE-004.M01.L06.EX01": (
        """Use case: intent classifier for a support chatbot.
2. Quality: accuracy (and macro F1) on a held-out labelled set of real user queries, including the out-of-scope class.
3. Latency: run each query alone (batch size 1, as in production) on the target hardware; do 10 warm-up runs first (caches, lazy initialization), then 100+ timed runs with time.perf_counter, and report the mean, standard deviation and p95.
4. Size: the size of the saved model file (MB) plus peak memory while serving.
5. Representative query: "I want to transfer money to another account but it keeps failing" - a typical length and a typical intent, so its timing reflects real traffic (tested alongside a long query as a worst case).
6. An optimized model is unacceptable if accuracy drops more than an agreed budget (for example more than 1 point), or if it gets worse on critical intents such as fraud reports, however fast it is.""",
        """حالة الاستخدام: مصنف نوايا (intent classifier) لروبوت دعم.
2. الجودة: accuracy (مع macro F1) على مجموعة محجوزة مصنفة من استفسارات مستخدمين حقيقية، تشمل فئة خارج النطاق.
3. زمن الاستجابة: تشغيل كل استفسار منفردًا (batch size 1 كما في الإنتاج) على العتاد المستهدف؛ مع 10 تشغيلات تسخين أولًا (للـ caches والتهيئة المتأخرة)، ثم 100 تشغيل أو أكثر مقيسة بـ time.perf_counter، مع ذكر المتوسط والانحراف المعياري وp95.
4. الحجم: حجم ملف النموذج المحفوظ (MB) مع أقصى استهلاك للذاكرة أثناء الخدمة.
5. استفسار ممثِّل: "I want to transfer money to another account but it keeps failing" - طول معتاد ونية معتادة، فيعكس توقيته الحركة الحقيقية (ويُختبر معه استفسار طويل كأسوأ حالة).
6. يُرفض النموذج المحسَّن إذا انخفضت الدقة أكثر من حد متفق عليه (مثل أكثر من نقطة واحدة)، أو ساء أداؤه في نوايا حرجة مثل بلاغات الاحتيال، مهما كان سريعًا.""",
    ),
    "COURSE-004.M01.L06.EX02": (
        """| Scenario | First optimization | Rationale |
| 1. Accurate but too slow and oversized | Knowledge distillation | Train a smaller student to mimic the teacher's outputs, keeping most of the accuracy with far fewer layers |
| 2. Already a student, CPU still slow | Dynamic quantization (int8) | Integer weights and arithmetic speed up CPU inference and shrink the model without retraining |
| 3. Standard graph + optimized CPU runtime | Export to ONNX and run with ONNX Runtime | A portable graph plus graph-level optimizations and fast CPU kernels (can be combined with quantization) |
| 4. Storage is the constraint, sparsity acceptable | Pruning (e.g. movement pruning) | Removes many weights so the model can be stored sparsely |

5. After every change, re-measure the same three benchmark quantities: model quality (accuracy/F1), latency, and model size / memory.""",
        """| الحالة | التحسين الأول | السبب |
| 1. دقيق لكنه بطيء وكبير جدًا | knowledge distillation | تدريب student أصغر يحاكي مخرجات الـ teacher فيحتفظ بمعظم الدقة بطبقات أقل بكثير |
| 2. student موجود والـ CPU ما زال بطيئًا | dynamic quantization ‏(int8) | الـ weights والحساب بأعداد صحيحة يسرّعان الاستدلال على الـ CPU ويصغّران النموذج دون إعادة تدريب |
| 3. graph قياسي وruntime محسّن للـ CPU | التصدير إلى ONNX والتشغيل بـ ONNX Runtime | graph قابل للنقل مع تحسينات على مستوى الـ graph وkernels سريعة للـ CPU (ويمكن دمجه مع الـ quantization) |
| 4. التخزين هو القيد والـ sparsity مقبولة | pruning (مثل movement pruning) | يزيل weights كثيرة فيمكن تخزين النموذج بشكل متفرق |

5. بعد كل تغيير أعيد قياس الكميات الثلاث نفسها: جودة النموذج (accuracy/F1)، وزمن الاستجابة، وحجم النموذج والذاكرة.""",
    ),
    "COURSE-004.M01.L08.EX01": (
        """| Scenario | Methods to test first | Why |
| 1. 0 labels, 50,000 unlabeled tickets | Zero-shot classification with an NLI model; embedding lookup with a few hand-written label descriptions | Both need no training labels |
| 2. 25 labels, no extra corpus | Embedding lookup (nearest labelled examples); data augmentation (back-translation, token perturbation) + vanilla fine-tuning | Too few labels for fine-tuning alone; augmentation multiplies them |
| 3. 100 labels + 200,000 unlabeled | Domain adaptation (MLM on the unlabeled tickets) then fine-tuning; UDA/UST semi-supervised training | The large unlabeled corpus is the main asset |
| 4. 20,000 clean labels | Vanilla fine-tuning of a pretrained transformer (optionally with domain adaptation) | Enough labels; few-label tricks add little |

5. For a multilabel, imbalanced task: micro F1 (overall performance, dominated by frequent labels) and macro F1 (average over labels, so rare labels count equally).""",
        """| الحالة | الطرق التي أختبرها أولًا | السبب |
| 1. صفر تسميات و50,000 تذكرة غير مصنفة | zero-shot classification بنموذج NLI؛ وembedding lookup مع أوصاف قليلة مكتوبة للتسميات | كلاهما لا يحتاج تسميات تدريب |
| 2. ‏25 تسمية بلا نصوص إضافية | embedding lookup (أقرب الأمثلة المصنفة)؛ وdata augmentation (back-translation وتغيير tokens) مع vanilla fine-tuning | التسميات قليلة جدًا على الـ fine-tuning وحده، والـ augmentation يضاعفها |
| 3. ‏100 تسمية و200,000 غير مصنفة | domain adaptation ‏(MLM على التذاكر غير المصنفة) ثم fine-tuning؛ وتدريب semi-supervised بـ UDA/UST | النصوص غير المصنفة الكثيرة هي الثروة الأساسية |
| 4. ‏20,000 تسمية نظيفة | vanilla fine-tuning لنموذج transformer مدرَّب مسبقًا (مع domain adaptation اختياريًا) | التسميات كافية، وحيل التسميات القليلة لا تضيف كثيرًا |

5. لمهمة multilabel غير متوازنة: micro F1 (أداء عام تسيطر عليه التسميات الشائعة) وmacro F1 (متوسط على التسميات، فتُحتسب النادرة بالقدر نفسه).""",
    ),
    "COURSE-004.M01.L08.EX02": (
        """Arm A (baseline): BERT-base -> add a multilabel classification head -> fine-tune on the 80 labelled tickets -> evaluate.
Arm B (domain adaptation): BERT-base -> continue masked-language-model training on the 100,000 unlabeled cybersecurity tickets -> add the same multilabel head -> fine-tune on the same 80 labels with the same hyperparameters -> evaluate.
Controls: identical validation and test splits, identical classifier, training budget and threshold choice; the only difference is the extra MLM stage. Run each arm with several random seeds because 80 labels give noisy results.
Metrics: micro F1 and macro F1 on the test set.
Domain adaptation is useful if arm B beats arm A on both micro and macro F1 consistently across seeds by more than the seed-to-seed variation - especially macro F1, which shows rare categories improved.""",
        """الذراع A (الأساس): BERT-base -> إضافة رأس تصنيف multilabel -> fine-tuning على 80 تذكرة مصنفة -> التقييم.
الذراع B ‏(domain adaptation): BERT-base -> متابعة تدريب masked-language-model على 100,000 تذكرة أمن سيبراني غير مصنفة -> إضافة رأس multilabel نفسه -> fine-tuning على التسميات الثمانين نفسها بالـ hyperparameters نفسها -> التقييم.
الضوابط: تقسيمات validation واختبار متطابقة، ومصنف وميزانية تدريب واختيار عتبة متطابقة؛ الفرق الوحيد هو مرحلة الـ MLM الإضافية. أشغّل كل ذراع بعدة random seeds لأن 80 تسمية تعطي نتائج مشوشة.
المقاييس: micro F1 وmacro F1 على مجموعة الاختبار.
يكون الـ domain adaptation مفيدًا إذا تفوقت الذراع B على A في micro وmacro F1 باستمرار عبر الـ seeds وبفارق أكبر من التذبذب بين الـ seeds - خاصة macro F1 الذي يوضح تحسن الفئات النادرة.""",
    ),
    "COURSE-004.M01.L10.EX01": (
        """1. The code-specific tokenizer: 950 tokens almost fit in a 1,024-token context, while 1,800 tokens would need about two contexts.
2. Self-attention compares every token with every other token, so its cost grows with the square of the sequence length: 950 tokens need roughly a quarter of the attention computation of 1,800 tokens.
3. Indentation (leading spaces/tabs, which carry meaning in Python) and newlines; also common keywords and operators such as "def", "return", "==" or "self." as single tokens.
4. Subword fertility (average tokens per word) and the proportion of continued words (words split into more than one token) - lower is better for both.
5. Compression alone does not guarantee a better model: what matters is whether a model trained with the tokenizer generates and understands code better, so the final comparison must be on downstream metrics such as loss/perplexity and code-generation tests.""",
        """1. الـ tokenizer الخاص بالكود: 950 token تتسع تقريبًا في سياق من 1,024، بينما تحتاج 1,800 token إلى سياقين تقريبًا.
2. يقارن الـ self-attention كل token بكل token آخر، فتكبر تكلفته مع مربع طول التسلسل: 950 token تحتاج نحو ربع حسابات الانتباه التي تحتاجها 1,800 token.
3. المسافات البادئة (indentation، ولها معنى في Python) والأسطر الجديدة؛ وكذلك الكلمات المحجوزة والعمليات الشائعة مثل "def" و"return" و"==" و"self." كـ tokens منفردة.
4. الـ subword fertility (متوسط الـ tokens لكل كلمة) ونسبة الكلمات المجزأة (الكلمات المقسمة إلى أكثر من token) - والأقل أفضل في الاثنين.
5. الضغط وحده لا يضمن نموذجًا أفضل: المهم هو هل يولّد النموذج المدرَّب بهذا الـ tokenizer الكود ويفهمه بشكل أفضل، لذا يجب أن تكون المقارنة النهائية بمقاييس لاحقة مثل الـ loss/perplexity واختبارات توليد الكود.""",
    ),
    "COURSE-004.M01.L10.EX02": (
        """1. Dry run: train a small model (for example ~100M parameters, GPT-2 small) on the same data pipeline across the same multi-GPU setup for a few thousand steps, and confirm the loss falls and the run resumes correctly from a checkpoint.
2. Verify: dataset - streaming works, shuffling, no duplicate shards across workers, filtered/deduplicated content; tokenizer - the trained code tokenizer is loaded and round-trips code; dataloader - fixed-length packed sequences, correct shapes, no worker starvation; optimizer - learning-rate warm-up and decay schedule behave as planned, weight decay applied, no NaNs; logging - loss, learning rate and throughput reach the dashboard from the main process only; checkpoints - saved regularly, include optimizer state, and resuming reproduces the loss curve.
3. Gradient accumulation: when the desired effective batch size does not fit in GPU memory - gradients from several small batches are summed before one optimizer step.
4. Gradient checkpointing: when activations of the large model do not fit in memory - it stores fewer activations and recomputes them in the backward pass, trading compute for memory.
5. Training and validation loss, perplexity, learning rate, gradient norm, tokens per second, and GPU memory.
6. A HumanEval-style test: generate functions from docstrings and run them against unit tests (pass@k), which checks that the code works rather than just looks plausible.""",
        """1. التشغيل التجريبي: تدريب نموذج صغير (مثل ~100M parameter بحجم GPT-2 small) على الـ data pipeline نفسه وعبر إعداد الـ GPUs المتعددة نفسه لبضعة آلاف من الخطوات، والتأكد من انخفاض الـ loss ومن صحة الاستئناف من checkpoint.
2. ما يجب التحقق منه: البيانات - الـ streaming يعمل، والخلط، وعدم تكرار الأجزاء بين الـ workers، ومحتوى مُرشَّح ومُزالة تكراراته؛ الـ tokenizer - تحميل tokenizer الكود المدرَّب وأنه يعيد الكود كما هو؛ الـ dataloader - تسلسلات مضغوطة بطول ثابت وأشكال صحيحة وبلا جوع للـ workers؛ الـ optimizer - جدول الـ warm-up والتناقص للـ learning rate كما خُطط وتطبيق الـ weight decay وعدم ظهور NaN؛ الـ logging - وصول الـ loss والـ learning rate والإنتاجية إلى لوحة المتابعة من العملية الرئيسية فقط؛ الـ checkpoints - تُحفظ بانتظام وتشمل حالة الـ optimizer والاستئناف يعيد منحنى الـ loss نفسه.
3. الـ gradient accumulation: عندما لا يتسع حجم الدفعة الفعلي المطلوب في ذاكرة الـ GPU - تُجمع gradients عدة دفعات صغيرة قبل خطوة optimizer واحدة.
4. الـ gradient checkpointing: عندما لا تتسع activations النموذج الكبير في الذاكرة - يخزن activations أقل ويعيد حسابها في الـ backward pass، مقايضًا الحساب بالذاكرة.
5. الـ loss في التدريب والـ validation، والـ perplexity، والـ learning rate، ومعيار الـ gradient، وعدد الـ tokens في الثانية، وذاكرة الـ GPU.
6. اختبار بأسلوب HumanEval: توليد دوال من docstrings وتشغيلها على unit tests ‏(pass@k)، فيُتحقق من أن الكود يعمل لا أنه يبدو معقولًا فقط.""",
    ),
    "COURSE-004.M01.L09.EX01": (
        """1. Experiment C - scaling laws show performance improves smoothly when model size, data and compute are increased together in the right proportions.
2. Each variable becomes the bottleneck when only another one grows: a bigger model without more data or compute is undertrained, and more data with a small model cannot be absorbed - so the gains flatten (diminishing returns).
3. Infrastructure and engineering (distributed training across many GPUs, failures, storage) and the cost of compute and energy; also curating, filtering and deduplicating enormous datasets.
4. Scaling trends are smooth and predictable, so small pilot runs let us check the pipeline and fit a curve that roughly extrapolates the loss of the big run before spending most of the budget.""",
        """1. التجربة C - توضح قوانين التوسع (scaling laws) أن الأداء يتحسن بسلاسة عند زيادة حجم النموذج والبيانات والحوسبة معًا بالنسب الصحيحة.
2. يصبح كل متغير عنق الزجاجة عندما يكبر غيره وحده: النموذج الأكبر بلا بيانات أو حوسبة إضافية لا يُدرَّب كفاية، والبيانات الأكثر مع نموذج صغير لا يمكن استيعابها - فتتسطح المكاسب (diminishing returns).
3. البنية التحتية والهندسة (التدريب الموزع على وحدات GPU كثيرة والأعطال والتخزين) وتكلفة الحوسبة والطاقة؛ وكذلك تنقية مجموعات بيانات هائلة وترشيحها وإزالة تكراراتها.
4. اتجاهات التوسع ناعمة ويمكن توقعها، فالتجارب الصغيرة تسمح بفحص الـ pipeline وملاءمة منحنى يستقرئ تقريبًا الـ loss للتشغيل الكبير قبل إنفاق معظم الميزانية.""",
    ),
    "COURSE-004.M01.L09.EX02": (
        """1. Image classification with text-defined classes - CLIP: images and texts are embedded into one shared space, so an image is assigned to the class description whose embedding is most similar.
2. Natural-language aggregation questions over a table - TAPAS: it encodes the flattened table with extra row/column embeddings and predicts which cells to select and which aggregation (sum, count, average) to apply.
3. Speech to text - wav2vec 2.0: it learns speech representations from raw audio with self-supervision and is fine-tuned with a CTC head to output text.
4. Scanned invoice - LayoutLM: it combines each token's text with its 2D position on the page (and visual features), so layout tells it which number is the total.
5. Very long documents - Longformer or BigBird: sparse attention (local windows plus a few global tokens) makes the cost grow linearly instead of quadratically with length.""",
        """1. تصنيف صور بفئات معرّفة بالنص - CLIP: تُوضع الصور والنصوص في فضاء embedding مشترك واحد، فتُنسب الصورة إلى وصف الفئة الأقرب لها.
2. أسئلة تجميعية بلغة طبيعية على جدول - TAPAS: يرمّز الجدول المسطَّح مع embeddings إضافية للصف والعمود ويتنبأ بالخلايا المطلوبة وبنوع التجميع (sum أو count أو average).
3. الكلام إلى نص - wav2vec 2.0: يتعلم تمثيلات الكلام من الصوت الخام بالتعلم الذاتي، ويُضبط برأس CTC لإخراج النص.
4. فاتورة ممسوحة - LayoutLM: يجمع نص كل token مع موضعه ثنائي الأبعاد في الصفحة (وfeatures مرئية)، فيدله التخطيط على الرقم الذي يمثل الإجمالي.
5. مستندات طويلة جدًا - Longformer أو BigBird: الـ sparse attention (نوافذ محلية مع بعض الـ tokens العامة) يجعل التكلفة تكبر خطيًا لا تربيعيًا مع الطول.""",
    ),
}
