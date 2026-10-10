"""COURSE-006 Production AI Engineering: example answers (part a)."""

EXAMPLES = {
    "COURSE-006.M01.L01.EX01": (
        """1. Tokenization splits text into the units (words, subwords or characters) that a model reads and predicts, each mapped to an ID.
2. Masked LM hides words and predicts them from both sides ("The [MASK] barked loudly" -> "dog"); autoregressive LM predicts the next token from the left only ("The dog" -> "barked").
3. Training pairs from "AI helps people learn": "AI" -> "helps"; "AI helps" -> "people"; "AI helps people" -> "learn".
4. The labels come from the text itself - the next word is already in the sentence - so nobody has to annotate anything.
5. Because any text provides its own labels, models can be trained on the huge amount of text on the internet without human labelling cost. Data was no longer the bottleneck, so models could grow in size and training data together. That scale produced general capabilities, which is what turned language models into foundation models.""",
        """1. الـ tokenization يقسم النص إلى الوحدات (كلمات أو subwords أو أحرف) التي يقرؤها النموذج ويتنبأ بها، ولكل منها رقم ID.
2. الـ masked LM يخفي كلمات ويتنبأ بها من الجانبين ("The [MASK] barked loudly" -> "dog")؛ والـ autoregressive LM يتنبأ بالـ token التالي من اليسار فقط ("The dog" -> "barked").
3. أزواج تدريب من "AI helps people learn": ‏"AI" -> "helps"؛ "AI helps" -> "people"؛ "AI helps people" -> "learn".
4. التسميات تأتي من النص نفسه - فالكلمة التالية موجودة أصلًا في الجملة - فلا يحتاج أحد إلى وضع تسميات.
5. لأن أي نص يوفر تسمياته بنفسه، أمكن تدريب النماذج على كمية النصوص الهائلة على الإنترنت دون تكلفة تسمية بشرية. فلم تعد البيانات عنق الزجاجة، وأمكن تكبير حجم النماذج وبيانات تدريبها معًا. وهذا الحجم أنتج قدرات عامة، وهو ما حوّل النماذج اللغوية إلى foundation models.""",
    ),
    "COURSE-006.M01.L01.EX02": (
        """Application: customer-support assistant for an online shop.
1. Problem: agents spend most of their time answering repetitive questions (orders, returns, shipping); AI can draft accurate answers from policies and order data instantly.
2. Complementary: humans still handle the support; AI speeds them up.
3. Reactive: it answers when a customer or agent asks.
4. First release: AI drafts replies, a human agent reviews and sends them; fully automatic answers only later for simple FAQs.
5. Prompting + RAG over policies and order data: knowledge changes often and must be current; finetuning only later if the tone or format remains wrong.
6. Product metrics: share of tickets resolved without escalation, average handling time, customer satisfaction score.
7. Usefulness threshold: at least 90% of drafts accepted with minor or no edits; draft ready within 3 seconds; cost below $0.02 per ticket.
8. Defensibility: proprietary data flywheel - accepted and corrected drafts become evaluation and training data competitors do not have.
9. Maintenance risks: policy documents going stale in the index; model/provider updates changing behaviour silently.
10. Layers: application - support UI, prompts, RAG pipeline, guardrails, evaluation and feedback; model - the chosen LLM and embedding model (and any adaptation); infrastructure - vector database, serving/API gateway, monitoring, logging.""",
        """التطبيق: مساعد دعم عملاء لمتجر إلكتروني.
1. المشكلة: يقضي الموظفون معظم وقتهم في الرد على أسئلة متكررة (الطلبات والإرجاع والشحن)؛ ويستطيع الـ AI صياغة إجابات دقيقة من السياسات وبيانات الطلبات فورًا.
2. مكمّل: ما زال البشر يقدمون الدعم، والـ AI يسرّعهم.
3. تفاعلي (reactive): يجيب عندما يسأل العميل أو الموظف.
4. الإصدار الأول: يصوغ الـ AI الردود ويراجعها موظف ثم يرسلها؛ والإجابات الآلية الكاملة لاحقًا فقط للأسئلة الشائعة البسيطة.
5. الـ prompting مع RAG على السياسات وبيانات الطلبات: المعرفة تتغير كثيرًا ويجب أن تكون حديثة؛ والـ finetuning لاحقًا فقط إذا ظلت النبرة أو الصيغة خاطئة.
6. مقاييس المنتج: نسبة التذاكر المحلولة دون تصعيد، ومتوسط زمن المعالجة، ودرجة رضا العملاء.
7. حد الفائدة: قبول 90% على الأقل من المسودات بتعديل طفيف أو دون تعديل؛ وجاهزية المسودة خلال 3 ثوانٍ؛ وتكلفة أقل من 0.02 دولار لكل تذكرة.
8. الميزة الدفاعية: دورة بيانات خاصة - المسودات المقبولة والمصححة تصبح بيانات تقييم وتدريب لا يملكها المنافسون.
9. مخاطر الصيانة: تقادم مستندات السياسات في الفهرس؛ وتحديثات النموذج أو المزوّد التي تغير السلوك بصمت.
10. الطبقات: التطبيق - واجهة الدعم والـ prompts وpipeline الـ RAG والضوابط والتقييم والتغذية الراجعة؛ النموذج - الـ LLM المختار ونموذج الـ embedding (وأي تكييف)؛ البنية التحتية - قاعدة البيانات المتجهة وخدمة النموذج/API gateway والمراقبة والتسجيل.""",
    ),
    "COURSE-006.M02.L01.EX01": (
        """1. Needed information: each model's results on Arabic tasks from my domain; the share of Arabic and domain data in training; the number of training tokens; tokenizer efficiency on Arabic text; inference cost and latency on my hardware; context length and licence terms.
2. Parameter count says how big the model is, not what it learned. Quality depends on the data (languages, domains), the amount of training, and the training method; a smaller model trained on the right data can beat a bigger one.
3. A tokenizer built mostly for English splits Arabic words into many small tokens: the same Arabic text costs more tokens, so it is more expensive, slower, uses more of the context window, and the model has seen less Arabic to learn from.
4. Training tokens determine how well the parameters were actually trained; a large model trained on too few tokens is undertrained, while a smaller model trained on many tokens can be stronger for its size.
5. Model B saw much more Arabic and domain text and tokenizes Arabic efficiently, so it may understand the domain's terms and write better Arabic, at lower cost.
6. Model A's much larger size gives stronger general reasoning, which may matter for complex questions or if many users mix English and Arabic.
7. Build 100-200 real Arabic domain questions with reference answers; run both models with the same prompts; score correctness and Arabic fluency (human review plus an AI judge), and measure latency and cost per answer.""",
        """1. المعلومات المطلوبة: نتائج كل نموذج على مهام عربية من مجالي؛ ونسبة البيانات العربية وبيانات المجال في التدريب؛ وعدد tokens التدريب؛ وكفاءة الـ tokenizer مع النص العربي؛ وتكلفة الاستدلال وزمنه على عتادي؛ وطول السياق وشروط الترخيص.
2. عدد الـ parameters يوضح حجم النموذج لا ما تعلمه. الجودة تعتمد على البيانات (اللغات والمجالات) وكمية التدريب وطريقته؛ والنموذج الأصغر المدرَّب على البيانات الصحيحة قد يتفوق على الأكبر.
3. الـ tokenizer المبني أساسًا للإنجليزية يقسم الكلمات العربية إلى tokens صغيرة كثيرة: فيكلف النص العربي نفسه tokens أكثر، فيكون أغلى وأبطأ ويستهلك جزءًا أكبر من نافذة السياق، كما أن النموذج رأى نصوصًا عربية أقل ليتعلم منها.
4. tokens التدريب تحدد مدى تدريب الـ parameters فعلًا؛ فالنموذج الكبير المدرَّب على tokens قليلة يكون undertrained، بينما قد يكون النموذج الأصغر المدرَّب على tokens كثيرة أقوى بالنسبة لحجمه.
5. النموذج B رأى نصوصًا عربية ونصوص مجال أكثر بكثير ويقسّم العربية بكفاءة، فقد يفهم مصطلحات المجال ويكتب عربية أفضل بتكلفة أقل.
6. حجم النموذج A الأكبر بكثير يمنحه استدلالًا عامًا أقوى، وقد يهم ذلك في الأسئلة المعقدة أو إذا خلط مستخدمون كثيرون بين الإنجليزية والعربية.
7. أبني 100-200 سؤال عربي حقيقي من المجال مع إجابات مرجعية؛ وأشغّل النموذجين بالـ prompts نفسها؛ وأقيّم الصحة وطلاقة العربية (مراجعة بشرية مع AI judge)، وأقيس زمن الاستجابة والتكلفة لكل إجابة.""",
    ),
    "COURSE-006.M02.L01.EX02": (
        """1. Fields: invoice_number (string), invoice_date (YYYY-MM-DD), vendor_name, currency (ISO code), subtotal, tax, total (numbers), line_items (list of {description, quantity, unit_price}).
2. A prompt with instructions, the exact JSON schema, one or two worked examples, and "return only JSON, use null for missing fields".
3. Parse every output; on failure, retry once with the parser error included in the prompt; log the failures to find patterns (truncation, extra text).
4. Post-processing (strip extra text, repair small syntax errors) is simple and model-independent but cannot fix badly broken output; constrained sampling (JSON mode or grammar-constrained decoding) only lets the model produce tokens that keep the output valid, guaranteeing valid structure.
5. Finetune only if, even with valid structure, the model keeps making systematic extraction mistakes on our invoice layouts and prompting plus examples cannot fix them, and we have enough labelled invoices.
6. Temperature 0 (or very low): extraction has one correct answer, so we want the most likely, consistent output.
7. Mostly not: with temperature near 0 the top token is chosen anyway, so top-k/top-p have little effect.
8. Set max tokens with comfortable headroom for the largest invoices, and stop on the closing brace of the top-level object; if the output stops because of the token limit, treat it as a failure and retry.
9. Validate content: check total = subtotal + tax and line items add up, date and currency formats; on failure run a second extraction or a verification prompt (test-time compute) and send disagreements to human review.
10. Hallucination: inventing an invoice number that is not on the document. Inconsistency: the same invoice gives different dates on different runs (e.g. day/month order).""",
        """1. الحقول: invoice_number ‏(نص)، وinvoice_date ‏(YYYY-MM-DD)، وvendor_name، وcurrency ‏(رمز ISO)، وsubtotal وtax وtotal ‏(أرقام)، وline_items ‏(قائمة من {description, quantity, unit_price}).
2. prompt فيه التعليمات ومخطط الـ JSON الدقيق ومثال أو اثنان محلولان، مع "return only JSON, use null for missing fields".
3. أحلل كل مخرج؛ وعند الفشل أعيد المحاولة مرة مع إدراج خطأ المحلل في الـ prompt؛ وأسجل حالات الفشل لاكتشاف الأنماط (الانقطاع أو نص زائد).
4. المعالجة اللاحقة (حذف النص الزائد وإصلاح أخطاء صغيرة) بسيطة ومستقلة عن النموذج لكنها لا تصلح المخرج المعطوب بشدة؛ أما الـ constrained sampling ‏(JSON mode أو decoding مقيد بقواعد) فلا يسمح للنموذج إلا بـ tokens تبقي المخرج صالحًا، فيضمن بنية صحيحة.
5. أستخدم الـ finetuning فقط إذا استمر النموذج - رغم صحة البنية - في أخطاء استخراج منهجية مع أشكال فواتيرنا ولم يصلحها الـ prompting والأمثلة، وكان لدينا عدد كافٍ من الفواتير المصنفة.
6. temperature تساوي 0 (أو منخفضة جدًا): للاستخراج إجابة صحيحة واحدة، فنريد المخرج الأرجح والمتسق.
7. غالبًا لا: مع temperature قرب الصفر يُختار الـ token الأعلى على أي حال، فيكون أثر top-k/top-p ضئيلًا.
8. أضبط max tokens بهامش مريح لأكبر الفواتير، وأتوقف عند القوس الختامي للكائن الرئيسي؛ وإذا توقف المخرج بسبب حد الـ tokens أعتبره فشلًا وأعيد المحاولة.
9. التحقق من المحتوى: total = subtotal + tax ومجموع البنود صحيح، وصيغ التاريخ والعملة؛ وعند الفشل أشغّل استخراجًا ثانيًا أو prompt للتحقق (test-time compute) وأرسل حالات الاختلاف لمراجعة بشرية.
10. الهلوسة: اختراع رقم فاتورة غير موجود في المستند. عدم الاتساق: الفاتورة نفسها تعطي تواريخ مختلفة في تشغيلات مختلفة (مثل ترتيب اليوم والشهر).""",
    ),
    "COURSE-006.M03.L01.EX01": (
        """| Task | Method | Why | Limitation |
| 1. Python function | Functional correctness (unit tests) | It either works or not | Only as good as the tests; ignores readability/efficiency |
| 2. 13 + 29 | Exact match ("42") | One correct answer | Fails "forty-two" or "42." unless outputs are normalized |
| 3. Translation | Semantic similarity (with human/AI judgment for samples) | Many correct phrasings | Embeddings can miss subtle meaning or tone errors |
| 4. Policy summary | AI judge (faithfulness, coverage) plus semantic similarity to a reference | Meaning matters, not wording | Judges can be biased and inconsistent; need calibration |
| 5. Marketing slogan | Human (or AI) judgment | Quality is stylistic and subjective | Costly, varies between raters |
| 6. Semantic search | Semantic similarity (embedding retrieval) evaluated with relevance metrics | Matches meaning, not keywords | Requires labelled relevant passages to evaluate |

7. For translation, BLEU rewards word overlap with one reference: a correct translation using different words gets a low score, while a fluent one that changes the meaning by flipping a negation can score high.""",
        """| المهمة | الطريقة | السبب | القيد |
| 1. دالة Python | functional correctness ‏(unit tests) | إما أن تعمل أو لا | جودتها بقدر جودة الاختبارات؛ وتتجاهل القراءة والكفاءة |
| 2. ‏13 + 29 | exact match ‏("42") | إجابة صحيحة واحدة | تفشل مع "forty-two" أو "42." ما لم تُوحَّد المخرجات |
| 3. الترجمة | semantic similarity (مع حكم بشري أو AI على عينات) | صياغات صحيحة كثيرة | قد تفوت الـ embeddings أخطاء دقيقة في المعنى أو النبرة |
| 4. ملخص سياسة | AI judge ‏(الأمانة والتغطية) مع semantic similarity بمرجع | المعنى هو المهم لا الصياغة | الحكام قد يكونون منحازين وغير متسقين؛ يحتاجون معايرة |
| 5. شعار تسويقي | حكم بشري (أو AI) | الجودة أسلوبية وذاتية | مكلف ويختلف بين المقيّمين |
| 6. بحث دلالي | semantic similarity ‏(استرجاع بالـ embeddings) يُقيَّم بمقاييس الصلة | يطابق المعنى لا الكلمات | يحتاج مقاطع ذات صلة مصنفة للتقييم |

7. في الترجمة يكافئ BLEU تطابق الكلمات مع مرجع واحد: فترجمة صحيحة بكلمات مختلفة تحصل على درجة منخفضة، بينما قد تحصل ترجمة سلسة غيّرت المعنى بقلب نفي على درجة عالية.""",
    ),
    "COURSE-006.M03.L01.EX02": (
        """1. Failure modes: the right document is not retrieved; the answer is not supported by the retrieved text (hallucination); outdated or wrong-version documents used; the assistant answers when it should say it does not know (or leaks restricted documents).
2. Exact signal: does the cited document ID match the gold source document for each test question (retrieval hit rate / recall@5).
3. Semantic signal: embedding similarity between the generated answer and the reference answer.
4. Judge criterion - faithfulness: "Is every claim in the answer supported by the provided context?" scored 1 (major unsupported claims), 2 (minor unsupported detail), 3 (fully supported), with a short justification.
5. Version: judge model name and version, the full prompt text, scoring scale, temperature and sampling settings, and the date - so scores stay comparable.
6. Run each comparison twice with the answers swapped; if the winner changes with position, the judge is position-biased. For verbosity, compare pairs where the shorter answer is known to be better and see whether the judge still picks the longer one.
7. Humans are needed to build and check the gold set, calibrate the judge against human ratings, and review high-risk answers (legal, HR, security).
8. Leaderboards measure general chat preferences of public users, not our documents, our questions, our latency/cost limits or our failure modes.
9. How many comparisons and the confidence interval (is 55% statistically different from 50%?), which question types B wins and loses (it may be worse on critical ones), and the differences in cost and latency.
10. Threshold: at least 90% of answers judged fully faithful and correct on the internal test set, with fewer than 2% confident wrong answers on unanswerable questions.""",
        """1. أنماط الفشل: عدم استرجاع المستند الصحيح؛ إجابة غير مدعومة بالنص المسترجع (hallucination)؛ استخدام مستندات قديمة أو بإصدار خاطئ؛ إجابة المساعد حين يجب أن يقول لا أعرف (أو تسريب مستندات مقيدة).
2. إشارة دقيقة: هل يطابق رقم المستند المستشهد به المستند المصدر الصحيح لكل سؤال اختبار (hit rate للاسترجاع / recall@5).
3. إشارة دلالية: تشابه الـ embedding بين الإجابة المولدة والإجابة المرجعية.
4. معيار الحكم - الأمانة (faithfulness): "Is every claim in the answer supported by the provided context?" بدرجات 1 (ادعاءات رئيسية غير مدعومة)، 2 (تفصيل ثانوي غير مدعوم)، 3 (مدعومة بالكامل)، مع تعليل قصير.
5. ما يجب ضبط إصداره: اسم نموذج الحكم وإصداره، ونص الـ prompt كاملًا، ومقياس الدرجات، والـ temperature وإعدادات الـ sampling، والتاريخ - لتبقى الدرجات قابلة للمقارنة.
6. أشغّل كل مقارنة مرتين مع تبديل الإجابتين؛ فإذا تغير الفائز بتغير الموضع فالحكم منحاز للموضع. وللإطالة أقارن أزواجًا تُعرف فيها أفضلية الإجابة الأقصر وأرى هل يختار الحكم الأطول رغم ذلك.
7. يلزم البشر لبناء المجموعة الذهبية وفحصها، ومعايرة الحكم مقابل تقييمات البشر، ومراجعة الإجابات عالية الخطورة (القانونية والموارد البشرية والأمن).
8. لوحات الصدارة تقيس تفضيلات محادثة عامة لمستخدمين عموميين، لا مستنداتنا ولا أسئلتنا ولا حدود زمن الاستجابة والتكلفة لدينا ولا أنماط فشلنا.
9. عدد المقارنات وفترة الثقة (هل 55% مختلفة إحصائيًا عن 50%؟)، وأنواع الأسئلة التي يفوز فيها B ويخسر (قد يكون أسوأ في الحرجة منها)، وفروق التكلفة وزمن الاستجابة.
10. الحد: أن تُقيَّم 90% على الأقل من الإجابات كأمينة وصحيحة بالكامل على مجموعة الاختبار الداخلية، مع أقل من 2% إجابات خاطئة واثقة على الأسئلة التي لا إجابة لها.""",
    ),
    "COURSE-006.M04.L01.EX01": (
        """Application: customer-support RAG assistant.
| Criterion | Metric | Hard requirement | Ideal target |
| Domain: answer product questions | Correctness on 200 real tickets | >= 85% | >= 95% |
| Domain: Arabic and English support | Correctness per language | Both >= 85% | Equal quality |
| Quality: faithfulness to retrieved docs | AI-judge faithfulness score | >= 90% fully supported | >= 97% |
| Quality: clarity and tone | Human rubric 1-5 | >= 4 | >= 4.5 |
| Instruction: answer only from context, else say so | Correct refusal rate | >= 90% | >= 98% |
| Instruction: follow output format (steps + citation) | Format compliance | >= 98% | 100% |
| Latency | Time to first token | < 2 s (p95) | < 800 ms |
| Cost | Cost per resolved ticket | < $0.05 | < $0.01 |
Hard attributes: supports Arabic; can be deployed with our data-privacy terms (no training on our data / region); context window >= 32k tokens.
Soft attributes (improvable later): tone (prompting/finetuning), speed (caching, smaller model), cost (routing simple questions to a cheaper model).
Public benchmarks (multilingual, instruction-following, long-context scores, price/latency tables) only shortlist 3-4 candidates.
Final decision: a private evaluation with our 200 tickets, our RAG pipeline and the metrics above, run on every candidate.
Trade-offs: I accept slightly lower style scores for half the cost; I do not accept lower faithfulness or refusal accuracy to save money.""",
        """التطبيق: مساعد دعم عملاء قائم على RAG.
| المعيار | المقياس | الحد الإلزامي | الهدف المثالي |
| المجال: الإجابة عن أسئلة المنتجات | الصحة على 200 تذكرة حقيقية | 85% على الأقل | 95% على الأقل |
| المجال: دعم العربية والإنجليزية | الصحة لكل لغة | كلاهما 85% على الأقل | جودة متساوية |
| الجودة: الأمانة للمستندات المسترجعة | درجة الأمانة من AI judge | 90% مدعومة بالكامل على الأقل | 97% على الأقل |
| الجودة: الوضوح والنبرة | rubric بشري من 1 إلى 5 | 4 على الأقل | 4.5 على الأقل |
| التعليمات: الإجابة من السياق فقط وإلا التصريح بذلك | نسبة الرفض الصحيح | 90% على الأقل | 98% على الأقل |
| التعليمات: اتباع شكل المخرج (خطوات مع استشهاد) | الالتزام بالشكل | 98% على الأقل | 100% |
| زمن الاستجابة | الزمن حتى أول token | أقل من 2 ثانية (p95) | أقل من 800 ms |
| التكلفة | تكلفة التذكرة المحلولة | أقل من 0.05 دولار | أقل من 0.01 دولار |
سمات إلزامية: دعم العربية؛ إمكانية النشر وفق شروط خصوصية بياناتنا (عدم التدريب على بياناتنا والمنطقة الجغرافية)؛ نافذة سياق لا تقل عن 32k token.
سمات مرنة (يمكن تحسينها لاحقًا): النبرة (prompting أو finetuning)، والسرعة (caching أو نموذج أصغر)، والتكلفة (توجيه الأسئلة البسيطة إلى نموذج أرخص).
المعايير العامة (نتائج تعدد اللغات واتباع التعليمات والسياق الطويل وجداول السعر وزمن الاستجابة) للتصفية الأولية فقط لاختيار 3-4 مرشحين.
القرار النهائي: تقييم خاص بتذاكرنا المائتين وpipeline الـ RAG الخاص بنا والمقاييس أعلاه على كل مرشح.
المقايضات: أقبل درجات أسلوب أقل قليلًا مقابل نصف التكلفة؛ ولا أقبل أمانة أو دقة رفض أقل لتوفير المال.""",
    ),
    "COURSE-006.M04.L01.EX02": (
        """1. Components and metrics: query rewriter - rewrite accuracy (judge); retriever - recall@5 of the gold document; reranker - nDCG@5; generator - faithfulness score; guardrail - false block / false pass rate.
2. Turn-level: share of answers judged correct and faithful. Task-level: share of conversations where the customer's issue was resolved without a human.
3. Criteria (1-3 rubrics): correctness (wrong / partly correct / correct), faithfulness (unsupported claims / minor unsupported detail / fully supported), helpfulness (does not address the question / partly / gives clear next steps).
4. Absolute threshold: >= 85% of turns correct and fully faithful on the test set, and task resolution >= 60%.
5. Business mapping: task resolution rate -> fewer escalations -> lower support cost per ticket (and CSAT).
6. 100% of traffic: cheap automatic checks - latency, cost, refusal/escalation rate, guardrail triggers, format validity, user thumbs up/down. Sampled (e.g. 2%): AI-judge correctness/faithfulness and human review.
7. Slices: language (Arabic/English), topic (billing, shipping, returns, technical), customer tier (new/returning), query length or channel (web/mobile).
8. Difficult set: multi-step questions, conflicting documents, ambiguous queries. Out-of-scope set: questions about competitors, legal advice, unrelated chit-chat - the right behaviour is to decline or escalate.
9. Bootstrap: resample the evaluation set with replacement many times (e.g. 1,000), recompute the metric each time, and look at the spread; if the 95% interval is wider than the differences we care about, the set is too small or noisy.
10. Version: model and provider version, prompts, retriever/embedding model, index snapshot, reranker, judge model and judge prompt, scoring rubrics, evaluation dataset version, code commit and sampling parameters.
11. After deployment: weekly human review of sampled conversations and of every thumbs-down; feedback becomes new labelled cases in the evaluation set.
12. Check the judge against human labels (agreement), check that offline scores predict online outcomes (resolution, CSAT), and confirm that known-bad changes produce lower scores.""",
        """1. المكونات ومقاييسها: معيد صياغة الاستعلام - دقة إعادة الصياغة (حكم)؛ المسترجع - recall@5 للمستند الصحيح؛ الـ reranker - nDCG@5؛ المولّد - درجة الأمانة؛ الضوابط (guardrail) - نسبة الحجب الخاطئ والتمرير الخاطئ.
2. على مستوى الدور: نسبة الإجابات المقيّمة كصحيحة وأمينة. على مستوى المهمة: نسبة المحادثات التي حُلت فيها مشكلة العميل دون موظف.
3. المعايير (rubric من 1 إلى 3): الصحة (خاطئة / صحيحة جزئيًا / صحيحة)، والأمانة (ادعاءات غير مدعومة / تفصيل ثانوي غير مدعوم / مدعومة بالكامل)، والفائدة (لا تعالج السؤال / جزئيًا / تعطي خطوات تالية واضحة).
4. الحد المطلق: 85% على الأقل من الأدوار صحيحة وأمينة بالكامل على مجموعة الاختبار، ونسبة حل المهام 60% على الأقل.
5. الربط بالأعمال: نسبة حل المهام -> تصعيدات أقل -> تكلفة دعم أقل لكل تذكرة (ورضا العملاء CSAT).
6. على 100% من الحركة: فحوص آلية رخيصة - زمن الاستجابة والتكلفة ونسبة الرفض/التصعيد وتفعيل الضوابط وصحة الشكل وتقييم المستخدم بالإعجاب أو عدمه. على عينة (مثل 2%): صحة وأمانة بحكم AI ومراجعة بشرية.
7. الشرائح: اللغة (عربية/إنجليزية)، والموضوع (الفواتير والشحن والإرجاع والدعم الفني)، وفئة العميل (جديد/عائد)، وطول الاستعلام أو القناة (الويب/الجوال).
8. مجموعة صعبة: أسئلة متعددة الخطوات ومستندات متعارضة واستعلامات غامضة. مجموعة خارج النطاق: أسئلة عن المنافسين ونصائح قانونية ودردشة غير ذات صلة - والسلوك الصحيح هو الاعتذار أو التصعيد.
9. الـ bootstrap: إعادة سحب مجموعة التقييم مع الإرجاع مرات كثيرة (مثل 1,000)، وإعادة حساب المقياس كل مرة، والنظر في التشتت؛ فإذا كانت فترة الـ 95% أوسع من الفروق التي تهمنا فالمجموعة صغيرة أو مشوشة.
10. ما يجب ضبط إصداره: النموذج وإصدار المزوّد، والـ prompts، والمسترجع ونموذج الـ embedding، ولقطة الفهرس، والـ reranker، ونموذج الحكم وprompt الحكم، والـ rubrics، وإصدار مجموعة التقييم، وcommit الكود، ومعاملات الـ sampling.
11. بعد النشر: مراجعة بشرية أسبوعية لعينة من المحادثات ولكل تقييم سلبي؛ وتتحول التغذية الراجعة إلى حالات مصنفة جديدة في مجموعة التقييم.
12. أقارن الحكم بتسميات البشر (نسبة الاتفاق)، وأتحقق من أن الدرجات offline تتنبأ بالنتائج online ‏(الحل والرضا)، وأتأكد من أن التغييرات السيئة المعروفة تعطي درجات أقل.""",
    ),
    "COURSE-006.M06.L01.EX01": (
        """1. Chunks: one section of a manual (by heading), one ticket (problem + resolution), one troubleshooting note; ~300-500 tokens with ~10-15% overlap for long sections.
2. Metadata: document type, product and model, version/date, section title, language, source URL, access level.
3. Hybrid: product codes and error numbers need exact term matching (BM25), while natural-language descriptions of problems need embeddings.
4. Evaluate the embedding model on our own queries: recall@k against labelled relevant chunks, its handling of product codes and Arabic/English mixing, embedding dimension/latency.
5. ANN: with millions of chunk vectors exact k-NN is too slow per query; ANN gives a near-perfect recall at a fraction of the latency.
6. HNSW: excellent recall and low query latency, at the cost of higher memory use and slower index builds - acceptable for a support assistant where latency matters.
7. Reranking: take the top ~50 hybrid candidates, score each (query, chunk) pair with a cross-encoder, keep the top 5.
8. Query rewriting: "My printer shows E-23." ... "How do I fix it on the newer model?" -> "How to fix error E-23 on printer model X200".
9. Contextual retrieval: a chunk saying "Press and hold for 10 seconds" is meaningless alone; prepending "Manual X200 - Resetting the network settings:" makes it retrievable.
10. Context precision: share of retrieved chunks that are relevant. Context recall: share of the needed information that appears in the retrieved chunks. Ranking: MRR or nDCG@5.
11. Infrastructure: p95 query latency and index build time (plus index size).
12. End to end: a test set of real questions with reference answers; measure answer correctness and faithfulness (AI judge plus human samples), resolution rate, latency and cost - and analyse failures by stage.""",
        """1. الـ chunks: قسم واحد من دليل (حسب العنوان)، أو تذكرة واحدة (المشكلة والحل)، أو ملاحظة استكشاف أعطال؛ بطول ~300-500 token وتداخل ~10-15% للأقسام الطويلة.
2. الـ metadata: نوع المستند، والمنتج والطراز، والإصدار والتاريخ، وعنوان القسم، واللغة، ورابط المصدر، ومستوى الوصول.
3. هجين: رموز المنتجات وأرقام الأخطاء تحتاج مطابقة كلمات دقيقة (BM25)، بينما تحتاج أوصاف المشكلات باللغة الطبيعية إلى الـ embeddings.
4. أقيّم نموذج الـ embedding على استعلاماتنا: recall@k مقابل chunks ذات صلة مصنفة، وتعامله مع رموز المنتجات ومزج العربية بالإنجليزية، وبُعد الـ embedding وزمنه.
5. الـ ANN: مع ملايين متجهات الـ chunks يكون k-NN الدقيق بطيئًا لكل استعلام؛ بينما يعطي الـ ANN ‏recall شبه كامل بجزء من الزمن.
6. HNSW: recall ممتاز وزمن استعلام منخفض، مقابل استهلاك ذاكرة أعلى وبناء فهرس أبطأ - وهذا مقبول لمساعد دعم يهمه زمن الاستجابة.
7. الـ reranking: آخذ أعلى ~50 مرشحًا هجينًا، وأقيّم كل زوج (استعلام، chunk) بـ cross-encoder، وأحتفظ بأعلى 5.
8. إعادة الصياغة: "My printer shows E-23." ... "How do I fix it on the newer model?" -> "How to fix error E-23 on printer model X200".
9. الاسترجاع السياقي: chunk يقول "Press and hold for 10 seconds" بلا معنى وحده؛ وإضافة "Manual X200 - Resetting the network settings:" في أوله تجعله قابلًا للاسترجاع.
10. context precision: نسبة الـ chunks المسترجعة ذات الصلة. context recall: نسبة المعلومات المطلوبة الموجودة في الـ chunks المسترجعة. الترتيب: MRR أو nDCG@5.
11. البنية التحتية: زمن الاستعلام p95 وزمن بناء الفهرس (مع حجم الفهرس).
12. من البداية للنهاية: مجموعة اختبار من أسئلة حقيقية بإجابات مرجعية؛ أقيس صحة الإجابة وأمانتها (AI judge مع عينات بشرية) ونسبة الحل وزمن الاستجابة والتكلفة - وأحلل الأعطال حسب المرحلة.""",
    ),
    "COURSE-006.M06.L01.EX02": (
        """1. Environment: company sales database, a reporting/spreadsheet tool, email. Goal: an accurate weekly report (revenue, units, top products, change vs. last week) sent to the sales manager. Constraints: read-only access to sales data, only internal recipients, no sending without approval in the first release.
2-3. Tools: query_sales(start, end, group_by) - read-only; get_last_week_report() - read-only; create_chart(data) - read-only (creates a file); build_report(sections) - write (draft file); send_email(to, subject, body, attachment) - write.
4. Human approval: send_email always (until the agent has a proven track record).
5. Plan: fetch this week's sales -> fetch last week's figures -> compute changes and top products -> create charts -> assemble the report draft -> validate -> ask approval -> send.
6. Parallel: this week's and last week's queries, and the charts once data exists. Sequential: compute after both queries; build after charts; send last.
7. Plan validation: every tool exists and parameters are valid (dates are the right week), the recipient is on the allowed list, the plan contains no write action before validation.
8. Reflection: after query_sales - are the totals plausible (not zero, no missing days)?; after build_report - do the report figures match the queried data?
9. Tool failure: retry once with backoff; if data is incomplete (missing days), mark the report as partial and ask the human instead of sending.
10. Metrics: goal success rate (correct report sent), invalid tool calls (nonexistent tools), parameter errors, number of steps vs. the optimal plan, cost per run, end-to-end latency (plus accuracy of the reported figures).
11. Ablation: remove get_last_week_report and see whether the agent still produces the week-over-week comparison (and at what extra cost) - showing whether the tool is needed.
12. Short-term memory: this run's data, intermediate results, tool outputs. Long-term memory: the manager's email, report format preferences, previous reports.""",
        """1. البيئة: قاعدة بيانات المبيعات، وأداة تقارير أو جداول، والبريد الإلكتروني. الهدف: تقرير أسبوعي دقيق (الإيرادات والوحدات وأفضل المنتجات والتغير عن الأسبوع الماضي) يُرسل لمدير المبيعات. القيود: وصول للقراءة فقط لبيانات المبيعات، ومستلمون داخليون فقط، وعدم الإرسال دون موافقة في الإصدار الأول.
2-3. الأدوات: query_sales(start, end, group_by) - قراءة فقط؛ get_last_week_report() - قراءة فقط؛ create_chart(data) - قراءة فقط (ينشئ ملفًا)؛ build_report(sections) - كتابة (ملف مسودة)؛ send_email(to, subject, body, attachment) - كتابة.
4. الموافقة البشرية: send_email دائمًا (حتى يثبت الـ agent موثوقيته).
5. الخطة: جلب مبيعات هذا الأسبوع -> جلب أرقام الأسبوع الماضي -> حساب التغيرات وأفضل المنتجات -> إنشاء الرسوم -> تجميع مسودة التقرير -> التحقق -> طلب الموافقة -> الإرسال.
6. بالتوازي: استعلاما هذا الأسبوع والماضي، والرسوم بعد توفر البيانات. بالتتابع: الحساب بعد الاستعلامين؛ والبناء بعد الرسوم؛ والإرسال أخيرًا.
7. التحقق من الخطة: كل أداة موجودة والمعاملات صحيحة (التواريخ للأسبوع الصحيح)، والمستلم في القائمة المسموحة، ولا توجد عملية كتابة قبل التحقق.
8. الـ reflection: بعد query_sales - هل المجاميع معقولة (ليست صفرًا ولا أيام مفقودة)؟؛ وبعد build_report - هل تطابق أرقام التقرير البيانات المستعلمة؟
9. فشل الأداة: إعادة المحاولة مرة مع تأخير؛ وإذا كانت البيانات ناقصة (أيام مفقودة) يُعلَّم التقرير كجزئي ويُسأل الإنسان بدلًا من الإرسال.
10. المقاييس: نسبة نجاح الهدف (إرسال تقرير صحيح)، والاستدعاءات غير الصالحة (أدوات غير موجودة)، وأخطاء المعاملات، وعدد الخطوات مقارنة بالخطة المثلى، والتكلفة لكل تشغيل، وزمن التنفيذ الكلي (مع دقة الأرقام المذكورة).
11. تجربة ablation: إزالة get_last_week_report ورؤية هل ما زال الـ agent ينتج المقارنة الأسبوعية (وبأي تكلفة إضافية) - لمعرفة هل الأداة ضرورية.
12. الذاكرة قصيرة المدى: بيانات هذا التشغيل والنتائج الوسيطة ومخرجات الأدوات. الذاكرة طويلة المدى: بريد المدير وتفضيلات شكل التقرير والتقارير السابقة.""",
    ),
    "COURSE-006.M07.L01.EX01": (
        """1. Today's balance - information failure (the model cannot know live data) -> RAG/tools: an account-balance API call. Evaluation: correctness of balances on test accounts.
2. Prose instead of YAML - behaviour failure -> prompting first (explicit format, examples, structured output); finetuning if it persists. Evaluation: YAML parse success rate.
3. Private policies - information failure -> RAG over the policy documents. Evaluation: answer correctness and faithfulness on policy questions.
4. Vague specifications despite correct sources - behaviour failure -> prompting with a specification template and examples, then finetuning on good specifications if needed. Evaluation: engineer-rated specificity rubric / acceptance rate.
5. Rare company DSL - behaviour/skill failure the model cannot learn from a few examples -> finetuning on DSL examples (plus DSL docs in context). Evaluation: share of DSL snippets that parse and pass tests.
6. Stale facts every week - information failure -> RAG with an index updated weekly (finetuning would go stale immediately). Evaluation: correctness on questions about this week's facts.
7. Current facts + strict style - both -> RAG for the facts plus finetuning (or strong prompting) for the response style. Evaluation: factual correctness and style-compliance rate, measured separately.
8. The evaluation signal for each choice is given above; each is measured before and after the change on the same test set.""",
        """1. رصيد اليوم - فشل معلومات (لا يعرف النموذج البيانات الحية) -> RAG/أدوات: استدعاء API لرصيد الحساب. التقييم: صحة الأرصدة على حسابات اختبار.
2. نص بدلًا من YAML - فشل سلوك -> الـ prompting أولًا (شكل صريح وأمثلة وstructured output)؛ ثم الـ finetuning إذا استمر. التقييم: نسبة نجاح تحليل الـ YAML.
3. سياسات خاصة - فشل معلومات -> RAG على مستندات السياسات. التقييم: صحة الإجابات وأمانتها على أسئلة السياسات.
4. مواصفات مبهمة رغم صحة المصادر - فشل سلوك -> prompting بقالب مواصفات وأمثلة، ثم finetuning على مواصفات جيدة إن لزم. التقييم: rubric للتحديد يقيّمه المهندسون / نسبة القبول.
5. لغة DSL نادرة خاصة بالشركة - فشل سلوك/مهارة لا يتعلمها النموذج من أمثلة قليلة -> finetuning على أمثلة DSL (مع وثائقها في السياق). التقييم: نسبة مقاطع DSL التي تُحلَّل وتجتاز الاختبارات.
6. حقائق تتقادم كل أسبوع - فشل معلومات -> RAG بفهرس يُحدَّث أسبوعيًا (فالـ finetuning يتقادم فورًا). التقييم: الصحة على أسئلة عن حقائق هذا الأسبوع.
7. حقائق حالية مع أسلوب صارم - الاثنان -> RAG للحقائق مع finetuning (أو prompting قوي) لأسلوب الرد. التقييم: الصحة الواقعية ونسبة الالتزام بالأسلوب، كلٌّ على حدة.
8. إشارة التقييم لكل اختيار مذكورة أعلاه؛ وتُقاس قبل التغيير وبعده على مجموعة الاختبار نفسها.""",
    ),
}
