"""COURSE-005 Applied LLM Engineering: example answers for written exercises."""

EXAMPLES = {
    "COURSE-005.M01.L01.EX01": (
        """| Stage | What it adds | Static / contextual |
| Bag-of-words | Represents text as word counts; simple and fast, ignores order and meaning | Static |
| word2vec | Dense learned word vectors where similar words are close | Static (one vector per word) |
| RNN encoder-decoder | Processes sequences in order and generates output sequences (e.g. translation) | Contextual, but squeezed into one final state |
| Attention | Lets the decoder look at every input position and weight the relevant ones | Contextual |
| Transformer | Replaces recurrence with self-attention; parallel training on long contexts | Contextual |
| BERT | Encoder-only Transformer pretrained with masked language modelling; used for representations (classification, embeddings) | Contextual |
| GPT | Decoder-only Transformer trained to predict the next token; used for generation | Contextual |

Attention removed the bottleneck of compressing a whole sentence into one vector: every output can draw directly on the relevant inputs. The Transformer built entirely on attention, which made training parallel instead of step by step, so models could be trained on far more text. That scale is what made pretrained models like BERT and GPT possible, and every modern LLM descends from that architecture.""",
        """| المرحلة | ما تضيفه | ثابت / سياقي |
| bag-of-words | يمثل النص بأعداد الكلمات؛ بسيط وسريع ويتجاهل الترتيب والمعنى | ثابت |
| word2vec | متجهات كلمات كثيفة متعلَّمة تتقارب فيها الكلمات المتشابهة | ثابت (متجه واحد لكل كلمة) |
| RNN encoder-decoder | يعالج التسلسلات بالترتيب ويولّد تسلسلات مخرجة (مثل الترجمة) | سياقي لكنه مضغوط في حالة أخيرة واحدة |
| attention | يسمح للـ decoder بالنظر إلى كل مواضع المدخل وإعطاء الوزن للمهم منها | سياقي |
| Transformer | يستبدل التكرار بـ self-attention؛ تدريب متوازٍ على سياقات طويلة | سياقي |
| BERT | Transformer من encoder فقط مدرَّب بـ masked language modelling؛ للتمثيلات (التصنيف والـ embeddings) | سياقي |
| GPT | Transformer من decoder فقط مدرَّب على التنبؤ بالـ token التالي؛ للتوليد | سياقي |

أزال الـ attention عنق الزجاجة الناتج عن ضغط جملة كاملة في متجه واحد: فكل مخرج يمكنه الاستعانة مباشرة بالمدخلات المهمة. وبُني الـ Transformer بالكامل على الـ attention، فصار التدريب متوازيًا لا خطوة بخطوة، وأمكن تدريب النماذج على نصوص أكثر بكثير. وهذا الحجم هو ما جعل النماذج المدرَّبة مسبقًا مثل BERT وGPT ممكنة، وكل LLM حديث ينحدر من هذه البنية.""",
    ),
    "COURSE-005.M02.L01.EX02": (
        """1. Token level: "I love llamas" -> tokens ["I", " love", " ll", "amas"] -> IDs like [40, 1842, 32660, 17485] (the exact IDs depend on the tokenizer). Rare words are split into subwords.
2. Context level: a DeBERTa/BERT encoder returns a tensor of shape [1, 6, 768] for this input (with special tokens): 1 = batch, 6 = tokens including [CLS]/[SEP], 768 = hidden size. Each token's vector depends on its neighbours.
3. Text level: a sentence-transformers model (e.g. all-mpnet-base-v2) returns one vector of shape [768] for the whole sentence. Instead of one vector per token, it pools them into a single representation of the meaning of the full text, used for similarity search.
4. Songs: treat each playlist as a "sentence" and each song as a "word". Songs that appear near each other in many playlists are trained (word2vec-style, with negative sampling) to have similar vectors. To recommend, take the vector of a song the user likes and return its nearest neighbours by cosine similarity.
Pipeline: raw text -> the tokenizer splits it into tokens -> tokens are mapped to vocabulary IDs -> the model looks up an embedding for each ID -> Transformer layers make the embeddings contextual -> optionally they are pooled into one text embedding.""",
        """1. مستوى الـ token: "I love llamas" -> الـ tokens ‏["I", " love", " ll", "amas"] -> أرقام مثل [40, 1842, 32660, 17485] (تعتمد الأرقام الدقيقة على الـ tokenizer). تُقسَّم الكلمات النادرة إلى subwords.
2. مستوى السياق: يعيد encoder مثل DeBERTa أو BERT ‏tensor بشكل [1, 6, 768] لهذا المدخل (مع الـ tokens الخاصة): 1 = الدفعة، 6 = عدد الـ tokens بما فيها [CLS]/[SEP]، 768 = الحجم المخفي. ومتجه كل token يعتمد على جيرانه.
3. مستوى النص: يعيد نموذج sentence-transformers (مثل all-mpnet-base-v2) متجهًا واحدًا بشكل [768] للجملة كلها. فبدلًا من متجه لكل token يجمعها في تمثيل واحد لمعنى النص كاملًا، يُستخدم في البحث بالتشابه.
4. الأغاني: نعامل كل playlist كـ "جملة" وكل أغنية كـ "كلمة". الأغاني التي تتجاور في playlists كثيرة تُدرَّب (بأسلوب word2vec مع negative sampling) لتحصل على متجهات متشابهة. وللتوصية نأخذ متجه أغنية يحبها المستخدم ونعيد أقرب جيرانها بـ cosine similarity.
الـ pipeline: نص خام -> يقسمه الـ tokenizer إلى tokens -> تُحوَّل الـ tokens إلى أرقام المفردات -> يبحث النموذج عن embedding لكل رقم -> تجعل طبقات الـ Transformer الـ embeddings سياقية -> ويمكن تجميعها في embedding واحد للنص.""",
    ),
    "COURSE-005.M03.L01.EX02": (
        """1. The last position, the token "it": its output is used to predict the next token.
2. Its query asks, in effect, "which earlier tokens help me know what 'it' refers to and what comes next?"
3. Each earlier token has a key; the dot product of the query with every key (scaled, then softmax) gives a relevance score per token.
4. Each token's value carries its information; the output is the relevance-weighted sum of the values.
5. Illustrative weights (not from a real model): Sarah 0.12, fed 0.08, the 0.05, cat 0.55, because 0.10, it 0.10 - sum 1.00, with most attention on "cat".
6. During generation the future does not exist yet, and in training the model must learn to predict each token without seeing it, so a causal mask blocks attention to later positions.
7. Without a KV cache, the next step would recompute keys and values for every previous token in every layer. The cache stores them, so only the new token's query, key and value are computed.
8. MHA: every head has its own keys and values. MQA: all query heads share one key/value head (smallest cache, some quality loss). GQA: groups of query heads share key/value heads - a middle ground.
9. RoPE rotates the query and key vectors according to their positions right before the query-key dot product, so the attention score encodes relative position.
10. Pipeline: (1) tokenize the prompt, (2) look up token embeddings, (3) in each layer apply normalization, (4) compute Q, K, V, (5) apply RoPE to Q and K, (6) masked attention scores and softmax, (7) weighted sum of values and output projection plus residual, (8) feed-forward network plus residual, (9) final norm, (10) language-model head produces logits for the last position, (11) choose a token (greedy or sampling), (12) append it and repeat using the KV cache.""",
        """1. الموضع الأخير، الـ token ‏"it": يُستخدم مخرجه للتنبؤ بالـ token التالي.
2. الـ query الخاص به يسأل عمليًا: "أي الـ tokens السابقة تساعدني على معرفة إلام يشير 'it' وما الذي يأتي بعده؟"
3. لكل token سابق key؛ وحاصل الضرب النقطي للـ query مع كل key (بعد التقييس ثم softmax) يعطي درجة صلة لكل token.
4. يحمل الـ value لكل token معلوماته؛ والمخرج هو مجموع الـ values الموزون بدرجات الصلة.
5. أوزان توضيحية (ليست من نموذج حقيقي): Sarah 0.12، fed 0.08، the 0.05، cat 0.55، because 0.10، it 0.10 - المجموع 1.00، ومعظم الانتباه على "cat".
6. أثناء التوليد لا يوجد المستقبل بعد، وفي التدريب يجب أن يتعلم النموذج التنبؤ بكل token دون رؤيته، لذا يحجب causal mask الانتباه إلى المواضع اللاحقة.
7. بدون KV cache تعيد الخطوة التالية حساب الـ keys والـ values لكل الـ tokens السابقة في كل طبقة. والـ cache يخزنها، فلا يُحسب إلا الـ query والـ key والـ value للـ token الجديد.
8. MHA: لكل head ‏keys وvalues خاصة. MQA: كل heads الـ query تتشارك head واحدًا للـ key/value (أصغر cache مع بعض الخسارة في الجودة). GQA: مجموعات من heads الـ query تتشارك heads للـ key/value - حل وسط.
9. يدوّر RoPE متجهات الـ query والـ key حسب مواضعها قبل الضرب النقطي بينهما مباشرة، فتعبّر درجة الانتباه عن الموضع النسبي.
10. الـ pipeline: (1) تقسيم الـ prompt إلى tokens، (2) جلب الـ embeddings، (3) في كل طبقة تطبيق الـ normalization، (4) حساب Q وK وV، (5) تطبيق RoPE على Q وK، (6) درجات انتباه مقنّعة ثم softmax، (7) مجموع الـ values الموزون والإسقاط مع residual، (8) شبكة feed-forward مع residual، (9) normalization أخيرة، (10) يُخرج رأس النموذج اللغوي logits لآخر موضع، (11) اختيار token ‏(greedy أو sampling)، (12) إضافته والتكرار باستخدام الـ KV cache.""",
    ),
    "COURSE-005.M04.L01.EX02": (
        """Task: movie-review sentiment, 12 reviews with known labels (positive/negative).
| Approach | Correct | Notes |
| 1. Task-specific classifier (a RoBERTa model fine-tuned on sentiment) | 11/12 | Missed a sarcastic review |
| 2. Embeddings + label descriptions, cosine similarity | 9/12 (v1), 10/12 (v2) | v1: "positive" / "negative"; v2: "a positive movie review" / "a negative movie review" - two predictions changed |
| 3. Generative model with a prompt | 11/12 | Prompt: "Classify the review as positive or negative. Answer with exactly one word: positive or negative." |
4. Disagreements: mixed reviews ("great acting, terrible plot") and sarcasm; approach 2 was most sensitive to wording.
6. Output contract for approach 3: the response must be exactly "positive" or "negative" in lowercase; anything else is rejected and retried once, then marked "unknown".
7. Trade-offs: (1) a small model, fast and cheap, very stable output, but only exists if someone trained it for this task/domain. (2) needs only an embedding model and label text, no labeled data, fast, but accuracy depends on label wording. (3) flexible for any labels and strong on nuance, but needs a large model (GPU or API cost), is slower, and its output must be validated.
8. No universal winner: (1) when a matching model exists and latency matters; (2) for many or changing labels with no training data; (3) when nuance matters more than cost or the labels need explanation.""",
        """المهمة: مشاعر مراجعات أفلام، 12 مراجعة بتسميات معروفة (positive/negative).
| الطريقة | الصحيح | ملاحظات |
| 1. مصنف مخصص للمهمة (RoBERTa مضبوط على المشاعر) | 11 من 12 | أخطأ مراجعة ساخرة |
| 2. embeddings مع أوصاف التسميات وcosine similarity | 9 من 12 (الإصدار 1)، 10 من 12 (الإصدار 2) | الإصدار 1: "positive"/"negative"؛ الإصدار 2: "a positive movie review"/"a negative movie review" - تغيّر تنبؤان |
| 3. نموذج توليدي مع prompt | 11 من 12 | الـ prompt: "Classify the review as positive or negative. Answer with exactly one word: positive or negative." |
4. الاختلافات: المراجعات المختلطة ("great acting, terrible plot") والسخرية؛ وكانت الطريقة 2 الأكثر حساسية للصياغة.
6. عقد المخرج للطريقة 3: يجب أن يكون الرد "positive" أو "negative" بالضبط وبأحرف صغيرة؛ وأي شيء آخر يُرفض ويُعاد مرة واحدة ثم يُسجَّل "unknown".
7. المقايضات: (1) نموذج صغير سريع ورخيص ومخرجه ثابت جدًا، لكنه يوجد فقط إذا درّبه أحد لهذه المهمة والمجال. (2) يحتاج نموذج embedding ونص التسميات فقط بلا بيانات مصنفة، وسريع، لكن دقته تعتمد على صياغة التسميات. (3) مرن مع أي تسميات وقوي في الفروق الدقيقة، لكنه يحتاج نموذجًا كبيرًا (GPU أو تكلفة API) وأبطأ ويجب التحقق من مخرجه.
8. لا فائز عام: (1) عند وجود نموذج مطابق وأهمية زمن الاستجابة؛ (2) للتسميات الكثيرة أو المتغيرة بلا بيانات تدريب؛ (3) عندما تكون الدقة في الفروق أهم من التكلفة أو تحتاج التسميات إلى تفسير.""",
    ),
    "COURSE-005.M07.L01.EX02": (
        """1. Memory: the user's budget (amount, currency, per night or total), preferred currency, and the destinations discussed - stored by the application, not only in the chat text.
2. search_hotel_price(destination, dates): "Searches the web for current hotel prices in a city. Input: city name and dates. Returns prices with currency, source URL and date. Use it only for hotel prices."
3. convert_currency(amount, from_currency, to_currency): deterministic calculation using a current exchange-rate API; returns the converted amount and the rate used.
4. Fixed chain: load budget from memory -> final comparison -> formatted answer. Agent decisions: whether a search is needed, which query to run, whether the result needs conversion.
5. Loop: Thought (need the current price for Lisbon) -> Action search_hotel_price("Lisbon", dates) -> Observation (EUR 120/night, booking site, today) -> Thought (user prefers EGP) -> Action convert_currency(120, "EUR", "EGP") -> Observation (6,300 EGP) -> compare with budget -> Final answer.
6. Source metadata: URL, site name, retrieval date, the price's currency and whether it is per night, and taxes included or not.
7. Checks: a price was actually found and is a positive number; currency codes are valid; conversion used the stated rate and arithmetic re-checks; the comparison uses the same unit (per night vs. total) as the budget; the answer cites its source and date.
8. Missing price: say no current price was found, show what was searched, and offer to try other dates or sources - never invent a price. Tool failure: retry once, otherwise give the original-currency price and explain the conversion could not be done.
9. Log: user request, tool calls with arguments, observations, the rate used, validation results and the final answer (without unnecessary personal data).
10. Human approval: any booking or payment action must be shown to the user (hotel, dates, total price, cancellation terms) and confirmed explicitly before the tool is called.""",
        """1. الذاكرة: ميزانية المستخدم (المبلغ والعملة ولليلة أم إجمالية)، والعملة المفضلة، والوجهات التي نوقشت - يخزنها التطبيق لا نص المحادثة فقط.
2. search_hotel_price(destination, dates): "Searches the web for current hotel prices in a city. Input: city name and dates. Returns prices with currency, source URL and date. Use it only for hotel prices."
3. convert_currency(amount, from_currency, to_currency): حساب حتمي باستخدام API حالي لأسعار الصرف؛ يعيد المبلغ المحوَّل والسعر المستخدم.
4. سلسلة ثابتة (chain): تحميل الميزانية من الذاكرة -> المقارنة النهائية -> صياغة الإجابة. قرارات الـ agent: هل يلزم بحث، وأي استعلام يُشغَّل، وهل تحتاج النتيجة إلى تحويل.
5. الحلقة: Thought (أحتاج السعر الحالي في لشبونة) -> Action search_hotel_price("Lisbon", dates) -> Observation (‏120 يورو لليلة، موقع حجز، اليوم) -> Thought (المستخدم يفضّل الجنيه) -> Action convert_currency(120, "EUR", "EGP") -> Observation (‏6,300 جنيه) -> المقارنة بالميزانية -> Final answer.
6. بيانات المصدر: الرابط واسم الموقع وتاريخ الاسترجاع وعملة السعر وهل هو لليلة، وهل يشمل الضرائب.
7. الفحوص: أن سعرًا وُجد فعلًا وهو رقم موجب؛ وأن رموز العملات صحيحة؛ وأن التحويل استخدم السعر المذكور مع إعادة فحص الحساب؛ وأن المقارنة بالوحدة نفسها (لليلة أم إجمالي) كالميزانية؛ وأن الإجابة تذكر المصدر والتاريخ.
8. سعر مفقود: أوضح أنه لم يُعثر على سعر حالي وأبيّن ما بُحث عنه وأعرض تجربة تواريخ أو مصادر أخرى - دون اختراع سعر أبدًا. فشل الأداة: أعيد المحاولة مرة، وإلا أعطي السعر بعملته الأصلية وأوضح تعذر التحويل.
9. التسجيل: طلب المستخدم، واستدعاءات الأدوات بمعاملاتها، والملاحظات، والسعر المستخدم، ونتائج الفحص، والإجابة النهائية (دون بيانات شخصية غير ضرورية).
10. الموافقة البشرية: أي حجز أو دفع يجب عرضه على المستخدم (الفندق والتواريخ والسعر الكلي وشروط الإلغاء) وتأكيده صراحةً قبل استدعاء الأداة.""",
    ),
    "COURSE-005.M08.L01.EX02": (
        """1. Unit: one section of a technical document. Chunks of ~300-500 tokens with ~15% overlap, split on headings/paragraphs; each chunk is prefixed with the document title and section heading and stores metadata (doc id, version, section, page).
2. Hybrid lexical (BM25) + dense retrieval: technical text contains exact identifiers (error codes, function names) that keyword search finds well, while dense retrieval handles paraphrased questions.
3. The vector index stores chunk embeddings plus metadata and returns nearest neighbours quickly, with metadata filters (product, version).
4. First stage: top 50 from each retriever, merged (e.g. reciprocal rank fusion); the top 30 go to a cross-encoder reranker.
5. The best 5 chunks go to the generator.
6. Prompt: "Answer the question using only the context below. Cite the chunk id for each claim, like [3]. If the context does not contain the answer, say: 'The documents do not answer this.' Context: {chunks} Question: {question}"
7. Query rewriting: an LLM turns "and what about version 2?" plus chat history into a standalone question before retrieval.
8. Multi-query: "Compare memory limits of the API and the CLI" - search each separately. Multi-hop: "Which config file controls the module that throws error E42?" - first find the module for E42, then its config.
9. Retrieval: recall@k of the gold chunk, MRR, reranker nDCG, share of queries with zero relevant chunks. Generation: faithfulness (every claim supported), answer correctness vs. reference, citation accuracy, correct refusal when context is insufficient.
10. Debug: not retrieved - check chunking, embeddings and BM25 for that query, add query rewriting; retrieved but ranked low - inspect reranker scores, tune candidate counts; evidence in context but unsupported answer - tighten the prompt, lower temperature, test a stronger model; citation on the wrong claim - verify citations claim by claim with an automated check.""",
        """1. الوحدة: قسم واحد من مستند تقني. chunks بطول ~300-500 token وتداخل ~15%، تُقسَّم عند العناوين والفقرات؛ ويُسبق كل chunk بعنوان المستند والقسم ويخزن metadata ‏(رقم المستند والإصدار والقسم والصفحة).
2. استرجاع هجين: lexical ‏(BM25) مع dense: النصوص التقنية فيها معرّفات دقيقة (رموز أخطاء وأسماء دوال) يجدها البحث بالكلمات جيدًا، بينما يتعامل الاسترجاع الكثيف مع الأسئلة المعاد صياغتها.
3. يخزن الـ vector index ‏embeddings الـ chunks مع الـ metadata ويعيد أقرب الجيران بسرعة مع مرشحات metadata ‏(المنتج والإصدار).
4. المرحلة الأولى: أعلى 50 من كل مسترجع تُدمج (مثل reciprocal rank fusion)؛ وتذهب أعلى 30 إلى cross-encoder reranker.
5. تذهب أفضل 5 chunks إلى المولّد.
6. الـ prompt: "Answer the question using only the context below. Cite the chunk id for each claim, like [3]. If the context does not contain the answer, say: 'The documents do not answer this.' Context: {chunks} Question: {question}"
7. إعادة صياغة الاستعلام: يحوّل LLM عبارة "وماذا عن الإصدار 2؟" مع سجل المحادثة إلى سؤال مستقل قبل الاسترجاع.
8. multi-query: "قارن حدود الذاكرة في الـ API والـ CLI" - ابحث عن كل منهما منفصلًا. multi-hop: "ما ملف الإعدادات الذي يتحكم في الوحدة التي تطلق الخطأ E42؟" - جد الوحدة أولًا ثم ملفها.
9. الاسترجاع: recall@k للـ chunk الصحيح، وMRR، وnDCG للـ reranker، ونسبة الاستعلامات بلا أي chunk مناسب. التوليد: الأمانة (كل ادعاء مدعوم)، وصحة الإجابة مقارنة بمرجع، ودقة الاستشهاد، والرفض الصحيح عندما لا يكفي السياق.
10. التشخيص: لم يُسترجع - افحص التقطيع والـ embeddings وBM25 لهذا الاستعلام وأضف إعادة الصياغة؛ استُرجع لكن رُتب متأخرًا - افحص درجات الـ reranker واضبط أعداد المرشحين؛ الدليل في السياق والإجابة غير مدعومة - شدّد الـ prompt وخفّض الـ temperature وجرّب نموذجًا أقوى؛ استشهاد على ادعاء خاطئ - تحقق من الاستشهادات ادعاءً بادعاء بفحص آلي.""",
    ),
    "COURSE-005.M09.L01.EX02": (
        """1. Accept JPEG, PNG and WebP up to 10 MB, at least 224 px on the short side; reject other formats with a clear message.
2. Preprocessing: decode -> fix EXIF orientation -> convert to RGB -> resize/crop to the encoder's size (e.g. 224 or 384) -> normalize. Risk: centre-cropping a wide photo can cut off the serial-number label at the edge, and downscaling makes small text unreadable.
3. The ViT splits the image into fixed-size patches (e.g. 16x16), embeds each patch as a vector, adds position embeddings, and runs Transformer layers so every patch representation includes context from the others.
4. BLIP-2's Q-Former uses a small set of learnable query tokens that attend to the frozen ViT features and extract the most text-relevant information; a projection layer maps these queries into the LLM's embedding space, where they act as soft visual prompts placed before the text tokens.
5. Captioning: "Describe the product in this photo." VQA: "Is the charging port on this device damaged?"
6. Memory: the application stores previous questions and answers and a reference to the image (or its cached visual embeddings), and rebuilds the prompt each turn; the model itself remembers nothing.
7. Failures: a tiny label made unreadable by resizing (preprocessing); the model describes a crack that is not there (hallucination); a blurry or dark photo; a question about something outside the frame; a misidentified product model.
8. Insufficient evidence: say what cannot be determined ("the label is not readable"), ask for a closer or better-lit photo, and do not guess.
9. CLIP-style: matching the photo to the right product category or catalog item, and retrieving similar known-defect images. BLIP-2-style: free-form descriptions and answers to specific questions about the image.
10. Architecture: upload -> validation -> preprocessing -> (CLIP: identify product, retrieve docs) -> ViT encoder -> Q-Former bridge -> LLM with prompt, conversation memory and retrieved docs -> answer -> output checks (uncertainty wording, no unsupported claims) -> user.""",
        """1. نقبل JPEG وPNG وWebP حتى 10 MB، وألا يقل الضلع القصير عن 224 pixel؛ ونرفض الصيغ الأخرى برسالة واضحة.
2. التجهيز: فك الصورة -> تصحيح الاتجاه من EXIF -> التحويل إلى RGB -> تغيير الحجم والقص لحجم الـ encoder (مثل 224 أو 384) -> الـ normalization. الخطر: القص من المركز لصورة عريضة قد يقطع ملصق الرقم التسلسلي عند الحافة، والتصغير يجعل النص الصغير غير مقروء.
3. يقسم الـ ViT الصورة إلى patches بحجم ثابت (مثل 16×16) ويحول كل patch إلى متجه ويضيف position embeddings ثم يمررها في طبقات Transformer فيحمل تمثيل كل patch سياقًا من غيره.
4. يستخدم الـ Q-Former في BLIP-2 مجموعة صغيرة من query tokens قابلة للتعلم تنتبه إلى features الـ ViT المجمد وتستخرج أهم المعلومات المرتبطة بالنص؛ ثم تسقطها طبقة إلى فضاء embedding الخاص بالـ LLM لتعمل كـ soft visual prompts قبل الـ tokens النصية.
5. الوصف (captioning): "Describe the product in this photo." والـ VQA: "Is the charging port on this device damaged?"
6. الذاكرة: يخزن التطبيق الأسئلة والإجابات السابقة ومرجعًا للصورة (أو visual embeddings المخزنة) ويعيد بناء الـ prompt في كل دور؛ فالنموذج نفسه لا يتذكر شيئًا.
7. الأعطال: ملصق صغير صار غير مقروء بعد تغيير الحجم (التجهيز)؛ النموذج يصف شرخًا غير موجود (hallucination)؛ صورة مشوشة أو مظلمة؛ سؤال عن شيء خارج الإطار؛ خطأ في تحديد طراز المنتج.
8. الأدلة غير الكافية: أوضح ما لا يمكن تحديده ("الملصق غير مقروء") وأطلب صورة أقرب أو بإضاءة أفضل ولا أخمّن.
9. أسلوب CLIP: مطابقة الصورة مع فئة المنتج أو عنصر الكتالوج الصحيح، واسترجاع صور لعيوب معروفة مشابهة. أسلوب BLIP-2: أوصاف حرة وإجابات عن أسئلة محددة حول الصورة.
10. البنية: الرفع -> التحقق -> التجهيز -> (CLIP: تحديد المنتج واسترجاع المستندات) -> ViT encoder -> جسر Q-Former -> LLM مع الـ prompt وذاكرة المحادثة والمستندات المسترجعة -> الإجابة -> فحوص المخرج (صياغة عدم اليقين وعدم وجود ادعاءات غير مدعومة) -> المستخدم.""",
    ),
    "COURSE-005.M10.L01.EX02": (
        """1. Relevance: a document is relevant if it answers or directly helps with the user's technical question - not just shares vocabulary.
2. Start from a pretrained sentence-embedding model (e.g. all-mpnet-base-v2): it was already trained contrastively for similarity, so it gives usable embeddings from day one; a raw BERT backbone produces poor sentence embeddings without that training.
3. Split the 3,000 gold pairs by query (no query in both sets): about 2,400 train / 600 evaluation.
4. Positives: the labelled query-document pairs. Hard negatives: documents ranked high by BM25 or the current model for that query but not labelled relevant (checking they are truly irrelevant).
5. Yes, worth trying: TSDAE on the 100,000 domain documents adapts the model to the domain vocabulary before supervised fine-tuning; keep it only if the evaluation improves over fine-tuning without it.
6. Augmented SBERT: fine-tune a cross-encoder on the gold train pairs (it reads query and document together, so it is accurate but slow), then use it to score many new query-document pairs, creating a silver dataset.
7. Candidate pairs: for each query, retrieve the top documents with BM25 and with the current bi-encoder (semantic search), plus some random pairs - so the silver set contains hard, informative pairs.
8. MultipleNegativesRankingLoss with in-batch negatives plus the mined hard negatives (CosineSimilarityLoss on the silver scores is an alternative).
9. General: an STS benchmark to make sure general similarity did not collapse. Domain: recall@10, MRR@10 and nDCG@10 on the held-out 600 pairs over the full document collection.
10. Final choice weighs retrieval quality against query latency, time to embed the 100,000 documents (re-indexing speed) and model size/memory; a smaller model with nearly equal nDCG may be the better deployment.""",
        """1. الصلة: يكون المستند ذا صلة إذا أجاب عن السؤال التقني أو ساعد فيه مباشرة - لا مجرد تشارك المفردات.
2. أبدأ من نموذج sentence embedding مدرَّب مسبقًا (مثل all-mpnet-base-v2): فقد دُرّب تباينيًا (contrastive) على التشابه، فيعطي embeddings صالحة من اليوم الأول؛ أما BERT الخام فينتج sentence embeddings ضعيفة بدون ذلك التدريب.
3. أقسم الأزواج الذهبية الثلاثة آلاف حسب الاستعلام (لا يظهر استعلام في المجموعتين): نحو 2,400 للتدريب و600 للتقييم.
4. الإيجابيات: أزواج الاستعلام والمستند المصنفة. الـ hard negatives: مستندات يرتبها BM25 أو النموذج الحالي عاليًا لذلك الاستعلام لكنها غير مصنفة كذات صلة (مع التأكد من أنها غير ذات صلة فعلًا).
5. نعم، يستحق التجربة: TSDAE على 100,000 مستند من المجال يكيّف النموذج مع مفردات المجال قبل الـ fine-tuning الموجّه؛ وأحتفظ به فقط إذا تحسن التقييم مقارنة بالضبط بدونه.
6. Augmented SBERT: أضبط cross-encoder على أزواج التدريب الذهبية (يقرأ الاستعلام والمستند معًا فيكون دقيقًا لكن بطيئًا)، ثم أستخدمه لتقييم أزواج جديدة كثيرة فتتكون مجموعة silver.
7. الأزواج المرشحة: لكل استعلام أسترجع أعلى المستندات بـ BM25 وبالـ bi-encoder الحالي (semantic search) مع بعض الأزواج العشوائية - فتحتوي مجموعة الـ silver على أزواج صعبة ومفيدة.
8. MultipleNegativesRankingLoss مع in-batch negatives والـ hard negatives المستخرجة (والبديل CosineSimilarityLoss على درجات الـ silver).
9. عام: معيار STS للتأكد من أن التشابه العام لم ينهَر. خاص بالمجال: recall@10 وMRR@10 وnDCG@10 على الأزواج الستمائة المحجوزة عبر مجموعة المستندات كاملة.
10. يوازن الاختيار النهائي جودة الاسترجاع مع زمن الاستعلام ووقت تحويل 100,000 مستند (سرعة إعادة الفهرسة) وحجم النموذج وذاكرته؛ وقد يكون نموذج أصغر بـ nDCG شبه متساوٍ هو الأفضل للنشر.""",
    ),
    "COURSE-005.M11.L01.EX02": (
        """A. 50,000 messages, 5 intents - model: a pretrained encoder (e.g. bert-base or a multilingual model if needed); strategy: full fine-tuning with a classification head; data: the labelled messages split train/validation/test; granularity: document; preprocessing: tokenization with truncation/padding and a stratified split; evaluation: accuracy and macro F1, confusion matrix; failure: overconfident predictions on off-topic messages (add an "other" class); low compute: freeze lower layers or use a distilled model (DistilBERT).
B. 12 examples per class + 200,000 unlabeled documents - model: a sentence-transformer checkpoint; strategy: SetFit (contrastive fine-tuning of the embedder on pairs generated from the 12 examples per class, then a classification head), optionally after continued MLM pretraining; data: unlabeled docs for MLM, the labelled examples for SetFit; granularity: document; preprocessing: build balanced positive/negative pairs; evaluation: macro F1 with repeated runs over different few-shot samples; failure: domain jargon unknown to the model, unstable results from tiny data; low compute: skip MLM, SetFit alone is cheap.
9. I would run continued MLM on the internal documents first if the vocabulary is highly specialized, and compare SetFit with and without it on the same evaluation set.
C. 15,000 sentences with spans - model: a pretrained encoder (e.g. bert-base-cased, since capitalization helps NER); strategy: token classification with full fine-tuning; data: the labelled sentences; granularity: token; preprocessing: align word labels to subwords; evaluation: entity-level precision/recall/F1 (seqeval) per entity type; failure: product names unseen in training, label inconsistency; low compute: smaller encoder or freezing lower layers.
10. Alignment: tokenize with is_split_into_words=True, use word_ids() to give the word's label (B-/I-) to its first subword, and -100 to the remaining subwords and special tokens so the loss ignores them.""",
        """A. ‏50,000 رسالة و5 نوايا - النموذج: encoder مدرَّب مسبقًا (مثل bert-base أو نموذج متعدد اللغات إذا لزم)؛ الاستراتيجية: full fine-tuning مع رأس تصنيف؛ البيانات: الرسائل المصنفة مقسمة إلى تدريب وvalidation واختبار؛ المستوى: المستند؛ التجهيز: tokenization مع القص والحشو وتقسيم stratified؛ التقييم: accuracy وmacro F1 وconfusion matrix؛ الفشل: تنبؤات مفرطة الثقة على رسائل خارج الموضوع (أضيف فئة "other")؛ مع حوسبة محدودة: تجميد الطبقات الدنيا أو نموذج مقطّر (DistilBERT).
B. ‏12 مثالًا لكل فئة و200,000 مستند غير مصنف - النموذج: checkpoint من sentence-transformers؛ الاستراتيجية: SetFit ‏(ضبط تبايني للـ embedder على أزواج مولدة من الأمثلة الاثني عشر لكل فئة ثم رأس تصنيف)، واختياريًا بعد continued MLM pretraining؛ البيانات: المستندات غير المصنفة للـ MLM والأمثلة المصنفة للـ SetFit؛ المستوى: المستند؛ التجهيز: بناء أزواج إيجابية وسلبية متوازنة؛ التقييم: macro F1 مع تشغيلات متكررة على عينات few-shot مختلفة؛ الفشل: مصطلحات المجال غير المعروفة للنموذج ونتائج غير مستقرة من بيانات ضئيلة؛ مع حوسبة محدودة: تخطّي الـ MLM، فالـ SetFit وحده رخيص.
9. أشغّل continued MLM على المستندات الداخلية أولًا إذا كانت المفردات متخصصة جدًا، وأقارن SetFit معه وبدونه على مجموعة التقييم نفسها.
C. ‏15,000 جملة بمقاطع معلَّمة - النموذج: encoder مدرَّب مسبقًا (مثل bert-base-cased، لأن حالة الأحرف تفيد NER)؛ الاستراتيجية: token classification مع full fine-tuning؛ البيانات: الجمل المصنفة؛ المستوى: الـ token؛ التجهيز: محاذاة تسميات الكلمات مع الـ subwords؛ التقييم: precision/recall/F1 على مستوى الكيان (seqeval) لكل نوع؛ الفشل: أسماء منتجات لم تظهر في التدريب وعدم اتساق التسميات؛ مع حوسبة محدودة: encoder أصغر أو تجميد الطبقات الدنيا.
10. المحاذاة: tokenization مع is_split_into_words=True واستخدام word_ids() لإعطاء تسمية الكلمة (B-/I-) لأول subword منها، و-100 لباقي الـ subwords والـ tokens الخاصة فيتجاهلها الـ loss.""",
    ),
    "COURSE-005.M12.L01.EX02": (
        """1. SFT schema: {"system": ..., "instruction": user message, "response": ideal answer}. Examples: "How do I reset my password?" -> step-by-step reset instructions with the settings path; "My order arrived broken." -> apologize, ask for the order number and a photo, explain the replacement process.
2. QLoRA: the base model is loaded in 4-bit and only small LoRA adapters are trained, so SFT fits on a single GPU with little quality loss; full fine-tuning needs far more memory for a small gain.
3. SFT should teach the chat format and role: follow instructions, answer support questions concisely in the company's tone, ask for missing information, and refuse out-of-policy requests.
4. Preference schema: {"prompt": ..., "chosen": better response, "rejected": worse response, "reason": policy tag}.
5. Pairs: (a) refund request - chosen explains the policy and next step; rejected promises a refund the agent cannot authorize. (b) Vague complaint - chosen asks one clarifying question; rejected guesses the problem. (c) Simple question - chosen answers in two sentences; rejected gives a correct but rambling paragraph.
6. RLHF/PPO: train a reward model to score chosen above rejected, then use PPO to update the policy to maximize that reward while a KL penalty keeps it close to the SFT model.
7. DPO: optimize the policy directly on the pairs with a classification-style loss that raises the probability of chosen relative to rejected, compared with the frozen SFT reference - no separate reward model or sampling loop.
8. Evaluation: task correctness (resolved-ticket accuracy on a held-out set), instruction following (format/length constraints met), safety and policy adherence (no unauthorized promises, correct refusals), style/tone (rubric or LLM-as-judge with human spot checks), latency and cost per answer.
9. Before DPO: remove duplicates and pairs where chosen equals rejected, check label agreement on a sample, check that chosen is not systematically longer (to avoid teaching verbosity), check prompt diversity, and remove personal data.
10. Monitor response length over training (verbosity drift), refusal rate on harmless questions (over-alignment), reward/preference accuracy rising while human ratings fall (reward hacking), and scores on general capability benchmarks against the SFT model (capability loss).""",
        """1. مخطط الـ SFT: {"system": ...، "instruction": رسالة المستخدم، "response": الإجابة المثالية}. أمثلة: "How do I reset my password?" -> تعليمات إعادة التعيين خطوة بخطوة مع مسار الإعدادات؛ "My order arrived broken." -> الاعتذار وطلب رقم الطلب وصورة وشرح خطوات الاستبدال.
2. QLoRA: يُحمَّل النموذج الأساسي بـ 4-bit وتُدرَّب adapters صغيرة فقط من LoRA، فيتسع الـ SFT على GPU واحدة بخسارة جودة قليلة؛ بينما يحتاج full fine-tuning ذاكرة أكبر بكثير مقابل مكسب صغير.
3. يجب أن يعلّم الـ SFT صيغة المحادثة والدور: اتباع التعليمات، والإجابة عن أسئلة الدعم بإيجاز وبنبرة الشركة، وطلب المعلومات الناقصة، ورفض الطلبات المخالفة للسياسة.
4. مخطط التفضيلات: {"prompt": ...، "chosen": الرد الأفضل، "rejected": الرد الأسوأ، "reason": وسم السياسة}.
5. الأزواج: (أ) طلب استرداد - المختار يشرح السياسة والخطوة التالية؛ والمرفوض يعِد باسترداد لا يملك الموظف صلاحيته. (ب) شكوى مبهمة - المختار يسأل سؤالًا توضيحيًا واحدًا؛ والمرفوض يخمّن المشكلة. (ج) سؤال بسيط - المختار يجيب في جملتين؛ والمرفوض يعطي فقرة صحيحة لكنها مطولة.
6. RLHF/PPO: ندرّب reward model ليعطي المختار درجة أعلى من المرفوض، ثم نستخدم PPO لتحديث السياسة لتعظيم تلك المكافأة مع عقوبة KL تبقيها قريبة من نموذج الـ SFT.
7. DPO: يحسّن السياسة مباشرة على الأزواج بـ loss شبيه بالتصنيف يرفع احتمال المختار نسبةً إلى المرفوض مقارنة بمرجع SFT مجمد - بلا reward model منفصل ولا حلقة sampling.
8. التقييم: صحة المهمة (دقة حل التذاكر على مجموعة محجوزة)، واتباع التعليمات (الالتزام بقيود الشكل والطول)، والأمان والالتزام بالسياسة (لا وعود غير مصرح بها ورفض صحيح)، والأسلوب والنبرة (rubric أو LLM-as-judge مع فحص بشري لعينات)، وزمن الاستجابة والتكلفة لكل إجابة.
9. قبل DPO: إزالة التكرارات والأزواج التي يتساوى فيها المختار والمرفوض، وفحص اتفاق التسميات على عينة، والتأكد من أن المختار ليس أطول بشكل منهجي (حتى لا نعلّم الإطالة)، وفحص تنوع الـ prompts، وإزالة البيانات الشخصية.
10. أراقب طول الردود أثناء التدريب (انجراف الإطالة)، ونسبة الرفض على الأسئلة غير الضارة (over-alignment)، وارتفاع دقة التفضيل أو المكافأة مع انخفاض تقييمات البشر (reward hacking)، ونتائج معايير القدرات العامة مقارنة بنموذج الـ SFT (فقدان القدرات).""",
    ),
}
