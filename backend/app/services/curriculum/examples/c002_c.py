"""COURSE-002 Deep Learning Foundations: example answers (part c)."""

EXAMPLES = {
    "COURSE-002.M13.L01.EX02": (
        """1. Input shape: (96, 8).
2. An LSTM/GRU reads the timesteps in order and carries a state forward, so it keeps the temporal structure and can remember what happened earlier; flattening turns the sequence into an unordered list of 768 numbers.
3. inputs = Input((96, 8)); x = LSTM(32)(inputs); outputs = Dense(1)(x); loss="mse", metric "mae".
4. Sigmoid squeezes outputs into 0-1, so it could never predict values outside that range; an unrestricted target needs a linear output (no activation).
5. LSTM(32, recurrent_dropout=0.25): it drops connections inside the recurrence with the same mask at every timestep, regularizing the recurrent layer and reducing overfitting.
6. GRU(32, return_sequences=True) -> GRU(32) -> Dense(1). The first layer must return its output at every timestep, because the second recurrent layer needs a full sequence as input; the last one returns only its final state.
7. When a single layer already uses regularization, validation loss has stopped improving, and the model is not yet overfitting - that is, when it is capacity-limited.
8. Not really: a bidirectional RNN also reads the sequence from old to new in reverse, spending half its capacity on a direction that emphasizes the least predictive old timesteps; a forward-only model is usually as good and cheaper here.
9. A model can only use the information present in its inputs. If a key driver (for example a holiday calendar or a price change) is not in the data, no amount of extra layers can learn it - you must add that data.""",
        """1. شكل المدخل: (96, 8).
2. يقرأ LSTM/GRU الـ timesteps بالترتيب ويحمل state إلى الأمام، فيحافظ على البنية الزمنية ويتذكر ما حدث سابقًا؛ أما الـ flattening فيحوّل التسلسل إلى قائمة غير مرتبة من 768 رقمًا.
3. inputs = Input((96, 8)); x = LSTM(32)(inputs); outputs = Dense(1)(x)؛ مع loss="mse" ومقياس "mae".
4. الـ sigmoid يضغط المخرجات بين 0 و1، فلا يستطيع التنبؤ بقيم خارج هذا المدى؛ والـ target غير المقيد يحتاج مخرجًا خطيًا (بلا activation).
5. LSTM(32, recurrent_dropout=0.25): يُسقط اتصالات داخل التكرار بنفس الـ mask في كل timestep، فيعمل regularization للطبقة المتكررة ويقلل الـ overfitting.
6. GRU(32, return_sequences=True) -> GRU(32) -> Dense(1). الطبقة الأولى يجب أن تعيد مخرجها في كل timestep لأن الطبقة المتكررة الثانية تحتاج تسلسلًا كاملًا كمدخل؛ والأخيرة تعيد الـ state النهائية فقط.
7. عندما تستخدم الطبقة الواحدة regularization بالفعل، وتوقفت الـ validation loss عن التحسن، ولا يعاني النموذج بعد من overfitting - أي عندما تكون سعته هي القيد.
8. ليس فعلًا: الـ bidirectional RNN يقرأ التسلسل أيضًا بالعكس، فينفق نصف سعته على اتجاه يبرز الـ timesteps القديمة الأقل تنبؤًا؛ والنموذج الأمامي فقط عادةً بنفس الجودة وأرخص هنا.
9. النموذج يستخدم فقط المعلومات الموجودة في مدخلاته. إذا كان عامل مؤثر (مثل تقويم العطلات أو تغير الأسعار) غير موجود في البيانات، فلن تتعلمه أي طبقات إضافية - يجب إضافة تلك البيانات.""",
    ),
    "COURSE-002.M14.L01.EX01": (
        """1. Standardized: "the product is not bad but delivery was slow" (lowercase, punctuation removed).
2. Tokens: [the, product, is, not, bad, but, delivery, was, slow].
3. An out-of-vocabulary word is mapped to the [UNK] (out-of-vocabulary) index instead of being dropped silently or causing an error.
4. Bag of words: a vector with one position per vocabulary word, set to 1 (or its count) for each word present - order is ignored.
5. Bigrams: "the product", "product is", "is not", "not bad", "bad but", "but delivery", "delivery was", "was slow".
6. "not bad" is mildly positive, but "not" and "bad" separately both look negative to a bag-of-words model; the bigram keeps the local order, so the negation is captured.
7. Dense(1, activation="sigmoid").
8. binary_crossentropy.
9. It trains in seconds, is hard to beat on short reviews where word order matters only locally, and gives a reference score any heavier LSTM must clearly exceed to justify its cost.""",
        """1. النص بعد التوحيد (standardization): "the product is not bad but delivery was slow" (أحرف صغيرة وبلا علامات ترقيم).
2. الـ tokens: [the, product, is, not, bad, but, delivery, was, slow].
3. الكلمة غير الموجودة في المفردات تُربط بفهرس [UNK] (out-of-vocabulary) بدلًا من حذفها بصمت أو التسبب في خطأ.
4. الـ bag of words: متجه بموضع لكل كلمة في المفردات، قيمته 1 (أو عدد التكرار) لكل كلمة موجودة - مع تجاهل الترتيب.
5. الـ bigrams: "the product" و"product is" و"is not" و"not bad" و"bad but" و"but delivery" و"delivery was" و"was slow".
6. "not bad" تعني رأيًا إيجابيًا معتدلًا، لكن "not" و"bad" منفصلتين تبدوان سلبيتين لنموذج bag of words؛ أما الـ bigram فيحتفظ بالترتيب المحلي فيلتقط النفي.
7. Dense(1, activation="sigmoid").
8. binary_crossentropy.
9. يتدرب في ثوانٍ، ومن الصعب التفوق عليه في المراجعات القصيرة حيث يهم ترتيب الكلمات محليًا فقط، ويعطي نتيجة مرجعية يجب أن يتجاوزها أي LSTM أثقل بوضوح ليبرر تكلفته.""",
    ),
    "COURSE-002.M14.L01.EX02": (
        """1. Subword tokenization: it keeps a manageable vocabulary while still representing rare words, product names and typos as known pieces, which suits noisy support messages.
2. A batch is one tensor, so every sequence in it must have the same length.
3. Truncation cuts sequences longer than the chosen length (for example 200 tokens); [PAD] fills shorter ones up to that length.
4. One-hot vectors of 30,000 dimensions are huge, sparse and treat every pair of words as equally different; a learned embedding (for example 256 dimensions) is dense, cheap, and places related words close together.
5. mask_zero=True tells the layers after the embedding to ignore the padding positions (index 0), so [PAD] does not influence the LSTM's result.
6. Input(token ids) -> Embedding(vocab_size, 256, mask_zero=True) -> Bidirectional(LSTM(32)) -> Dropout(0.5) -> Dense(1, activation="sigmoid").
7. Train the embedding on the 200,000 unlabeled messages with a self-supervised word-prediction task (CBOW), which needs no labels.
8. CBOW: hide a word, give the model the surrounding words, and train it to predict the hidden word; words used in similar contexts end up with similar embeddings.
9. The embedding matrix (one vector per token) is transferred and used to initialize the classifier's Embedding layer, frozen at first and possibly fine-tuned later.
10. Because a simple bag-of-words or bigram model is often surprisingly strong on short texts; the complex pipeline is only worth it if it clearly beats that baseline.""",
        """1. الـ subword tokenization: يحافظ على مفردات بحجم معقول مع تمثيل الكلمات النادرة وأسماء المنتجات والأخطاء الإملائية كأجزاء معروفة، وهذا مناسب لرسائل الدعم غير المنظمة.
2. الدفعة tensor واحد، لذا يجب أن يكون لكل تسلسل فيها الطول نفسه.
3. الـ truncation يقص التسلسلات الأطول من الطول المختار (مثل 200 token)؛ والـ [PAD] يملأ القصيرة حتى ذلك الطول.
4. متجهات one-hot بثلاثين ألف بُعد ضخمة ومتفرقة وتعامل كل زوج كلمات على أنه مختلف بالقدر نفسه؛ أما الـ embedding المتعلَّم (مثل 256 بُعدًا) فكثيف ورخيص ويضع الكلمات المترابطة قريبة من بعضها.
5. mask_zero=True يخبر الطبقات بعد الـ embedding بتجاهل مواضع الحشو (الفهرس 0)، فلا يؤثر [PAD] في نتيجة الـ LSTM.
6. Input(token ids) -> Embedding(vocab_size, 256, mask_zero=True) -> Bidirectional(LSTM(32)) -> Dropout(0.5) -> Dense(1, activation="sigmoid").
7. أدرّب الـ embedding على 200,000 رسالة غير مصنفة بمهمة self-supervised للتنبؤ بالكلمات (CBOW)، لا تحتاج تسميات.
8. الـ CBOW: نخفي كلمة ونعطي النموذج الكلمات المحيطة بها ونطلب منه التنبؤ بالكلمة المخفية؛ فتحصل الكلمات المستخدمة في سياقات متشابهة على embeddings متشابهة.
9. تُنقل مصفوفة الـ embedding (متجه لكل token) لتهيئة طبقة Embedding في المصنف، مجمدة في البداية وربما تُضبط لاحقًا.
10. لأن نموذج bag of words أو bigram البسيط قوي غالبًا بشكل مفاجئ في النصوص القصيرة؛ والـ pipeline المعقد لا يستحق إلا إذا تفوق على هذا الـ baseline بوضوح.""",
    ),
    "COURSE-002.M15.L01.EX01": (
        """Vocabulary: {"powerful", "useful", "data", "fun"}.
Step 1 - prompt "machine learning is": powerful 0.45, useful 0.30, fun 0.15, data 0.10 -> choose "powerful".
Step 2 - "machine learning is powerful": fun 0.60, useful 0.20, data 0.15, powerful 0.05 -> choose "fun" ("machine learning is powerful fun").
Step 3 - "machine learning is powerful fun": data 0.40, useful 0.30, fun 0.20, powerful 0.10 -> choose "data".
5. During training the model predicts each token from the tokens before it; if it could look at later tokens it would simply copy the answer, and at generation time those future tokens do not exist yet - so a causal mask blocks them.
6. Each generated token becomes part of the input for the next step: if step 2 picks an odd word ("fun"), every later prediction is conditioned on it, and the sentence drifts further from a sensible continuation - errors accumulate.""",
        """المفردات: {"powerful", "useful", "data", "fun"}.
الخطوة 1 - الـ prompt "machine learning is": powerful 0.45، useful 0.30، fun 0.15، data 0.10 -> نختار "powerful".
الخطوة 2 - "machine learning is powerful": لنفترض التوزيع powerful 0.05، useful 0.20، data 0.15، fun 0.60 -> نختار "fun" ("machine learning is powerful fun").
الخطوة 3 - "machine learning is powerful fun": data 0.40، useful 0.30، fun 0.20، powerful 0.10 -> نختار "data".
5. أثناء التدريب يتنبأ النموذج بكل token من الـ tokens السابقة له؛ ولو استطاع رؤية الـ tokens اللاحقة لنسخ الإجابة ببساطة، كما أن الـ tokens المستقبلية غير موجودة أصلًا وقت التوليد - لذا يحجبها causal mask.
6. كل token مولَّد يصبح جزءًا من مدخل الخطوة التالية: إذا اختارت الخطوة 2 كلمة غريبة ("fun")، فإن كل تنبؤ لاحق يُبنى عليها، فتنحرف الجملة أكثر عن استكمال معقول - أي تتراكم الأخطاء.""",
    ),
    "COURSE-002.M15.L01.EX02": (
        """2. The source sentence is tokenized into IDs, each ID is looked up in a token embedding, and a positional embedding is added so the encoder knows the order of "I will see you tomorrow".
3. Encoder self-attention lets every source token look at all the other source tokens and update its representation with their context (for example "see" attends to "you" and "tomorrow").
4. During training the decoder receives the whole target sentence at once; the causal mask stops each position from attending to later Spanish tokens, so it learns to predict the next word only from the words before it, exactly as at generation time.
5. In cross-attention the decoder's queries attend to the encoder's outputs (keys and values), so each Spanish token being generated can look at the relevant English words ("mañana" attends to "tomorrow").
6. The final Dense-softmax layer outputs a probability distribution over the target vocabulary for the next Spanish token.
7. A seq2seq decoder generates text one token at a time and must be causal. A bidirectional pretrained encoder (such as BERT) for classification reads the whole input at once - every token sees left and right context - and produces one label, with no generation and no causal mask.""",
        """2. تُقسَّم الجملة المصدر إلى IDs، ويُبحث عن كل ID في token embedding، ثم يُضاف positional embedding ليعرف الـ encoder ترتيب "I will see you tomorrow".
3. يسمح self-attention في الـ encoder لكل token مصدر بالنظر إلى كل الـ tokens الأخرى وتحديث تمثيله بسياقها (مثلًا "see" ينتبه إلى "you" و"tomorrow").
4. أثناء التدريب يستقبل الـ decoder الجملة الهدف كاملة دفعة واحدة؛ فيمنع الـ causal mask كل موضع من الانتباه إلى الكلمات الإسبانية اللاحقة، فيتعلم التنبؤ بالكلمة التالية من الكلمات السابقة فقط، تمامًا كما وقت التوليد.
5. في cross-attention تنتبه queries الـ decoder إلى مخرجات الـ encoder (keys وvalues)، فيستطيع كل token إسباني يجري توليده أن ينظر إلى الكلمات الإنجليزية المناسبة ("mañana" ينتبه إلى "tomorrow").
6. تُخرج طبقة Dense-softmax الأخيرة توزيع probability على مفردات اللغة الهدف للـ token الإسباني التالي.
7. الـ seq2seq decoder يولّد النص token تلو الآخر ويجب أن يكون causal. أما الـ encoder ثنائي الاتجاه المدرَّب مسبقًا (مثل BERT) للتصنيف فيقرأ المدخل كله دفعة واحدة - كل token يرى السياق يمينًا ويسارًا - وينتج label واحدًا، بلا توليد وبلا causal mask.""",
    ),
    "COURSE-002.M16.L01.EX01": (
        """2. At the final prompt position ("helps") the model outputs logits - one score per vocabulary token - which softmax turns into a distribution for the next token.
3. Greedy decoding takes the token with the highest probability (for example "businesses"), appends it, and repeats.
4. Without a cache, generating each new token reruns the whole Transformer over every previous token, recomputing the same keys and values for the prompt again and again, although only the newest token has changed.
5. At every layer, the keys and values of all past tokens can be cached; each step then computes keys, values and the query only for the new token and attends to the cached ones.
6. Without a cache the work per step grows with the full sequence length, so total work grows roughly quadratically; with caching each step does a constant amount of new projection work, so the longer the generated text, the larger the savings.""",
        """2. في آخر موضع من الـ prompt ("helps") يُخرج النموذج logits - درجة لكل token في المفردات - يحولها softmax إلى توزيع للـ token التالي.
3. الـ greedy decoding يأخذ الـ token صاحب أعلى probability (مثل "businesses") ويضيفه ثم يكرر.
4. بدون cache يعيد توليد كل token جديد تشغيل الـ Transformer كاملًا على كل الـ tokens السابقة، فيحسب الـ keys والـ values نفسها للـ prompt مرارًا رغم أن الجديد هو آخر token فقط.
5. في كل طبقة يمكن تخزين keys وvalues كل الـ tokens السابقة؛ فتحسب كل خطوة الـ keys والـ values والـ query للـ token الجديد فقط وتنتبه إلى المخزَّن.
6. بدون cache يزداد العمل في كل خطوة مع طول التسلسل كله، فيكبر العمل الكلي تربيعيًا تقريبًا؛ ومع الـ caching تقوم كل خطوة بقدر ثابت من الحسابات الجديدة، فكلما طال النص المولَّد زاد التوفير.""",
    ),
    "COURSE-002.M16.L01.EX02": (
        """2. Existing pretrained LLMs already understand language and code; training one from scratch costs enormous compute and data, while the company's knowledge can be supplied at question time instead.
3. Instruction fine-tuning helps if the assistant must follow a company-specific answer format, tone or tool usage that prompting alone does not achieve. LoRA freezes the base weights and trains small low-rank matrices added to some layers, so only a tiny fraction of parameters (and their optimizer state) need memory.
4. RAG flow: split documents into chunks -> embed them and store in a vector index -> embed the user's question -> retrieve the top-k most similar chunks -> build a prompt with instructions, the retrieved chunks and the question -> the LLM answers citing the chunks.
5. The model can still ignore, misread or mix the retrieved text with its own memory, and if retrieval returns the wrong or no relevant documents, the model may answer anyway.
6. Build a test set of questions with known answers and source documents; check that answers are correct, that the cited chunks actually contain the claims, and that the assistant says "I don't know" when the answer is not in the documents.""",
        """2. نماذج LLM المدرَّبة مسبقًا تفهم اللغة والكود أصلًا؛ وتدريب نموذج من الصفر يكلف حوسبة وبيانات هائلة، بينما يمكن تقديم معرفة الشركة وقت السؤال بدلًا من ذلك.
3. يفيد instruction fine-tuning إذا كان على المساعد اتباع شكل إجابة أو نبرة أو استخدام أدوات خاص بالشركة لا يحققه الـ prompting وحده. ويجمّد LoRA الـ weights الأساسية ويدرّب مصفوفات صغيرة منخفضة الرتبة (low-rank) تُضاف لبعض الطبقات، فلا يحتاج الذاكرة إلا جزء ضئيل من الـ parameters (وحالة الـ optimizer الخاصة بها).
4. تدفق RAG: تقسيم المستندات إلى chunks -> تحويلها إلى embeddings وتخزينها في vector index -> تحويل سؤال المستخدم إلى embedding -> استرجاع أعلى k مقاطع تشابهًا -> بناء prompt بالتعليمات والمقاطع المسترجعة والسؤال -> يجيب الـ LLM مستشهدًا بالمقاطع.
5. ما زال النموذج قد يتجاهل النص المسترجَع أو يسيء فهمه أو يخلطه بذاكرته، وإذا أعاد الاسترجاع مستندات خاطئة أو غير ذات صلة فقد يجيب النموذج على أي حال.
6. أبني مجموعة اختبار من أسئلة لها إجابات ومستندات مصدر معروفة؛ وأتحقق من صحة الإجابات، ومن أن المقاطع المستشهد بها تحتوي فعلًا على الادعاءات، ومن أن المساعد يقول "لا أعرف" عندما لا تكون الإجابة في المستندات.""",
    ),
    "COURSE-002.M17.L01.EX01": (
        """1. Encoder (image -> latent distribution), sampling step (draw a latent point), decoder (latent point -> image).
2. Instead of one fixed vector, the encoder outputs the parameters of a distribution over latent space: a mean and a (log) variance for every latent dimension.
3. z_mean is the centre of that distribution, z_log_var its log-variance (its spread), and epsilon is random noise from a standard normal distribution used to draw a sample.
4. z = z_mean + exp(0.5 * z_log_var) * epsilon.
5. Reconstruction loss makes the decoded image match the input, so the latent point keeps the information needed to rebuild the image.
6. KL regularization pulls each encoded distribution toward a standard normal, so the latent space is continuous, centred and well filled, without isolated "holes".
7. Because the decoder was trained on random samples around each mean, nearby points correspond to similar images; the space is smooth, so small moves give small visual changes.
8. Sample a random vector z from a standard normal distribution of the latent size, discard the encoder, and pass z through the decoder to get a new 64x64 image.""",
        """1. الـ encoder (صورة -> توزيع في الـ latent space)، وخطوة الـ sampling (سحب نقطة latent)، والـ decoder (نقطة latent -> صورة).
2. بدلًا من متجه ثابت واحد يُخرج الـ encoder معاملات توزيع على الـ latent space: متوسطًا وتباينًا (لوغاريتميًا) لكل بُعد latent.
3. الـ z_mean هو مركز ذلك التوزيع، والـ z_log_var لوغاريتم التباين (أي انتشاره)، والـ epsilon ضوضاء عشوائية من توزيع طبيعي معياري تُستخدم لسحب عينة.
4. z = z_mean + exp(0.5 * z_log_var) * epsilon.
5. الـ reconstruction loss يجعل الصورة المفكوكة تطابق المدخل، فتحتفظ النقطة الـ latent بالمعلومات اللازمة لإعادة بناء الصورة.
6. الـ KL regularization يجذب كل توزيع مُرمَّز نحو التوزيع الطبيعي المعياري، فيصبح الـ latent space متصلًا ومتمركزًا وممتلئًا بلا "ثقوب" معزولة.
7. لأن الـ decoder تدرّب على عينات عشوائية حول كل متوسط، فإن النقاط المتجاورة تقابل صورًا متشابهة؛ فالفضاء ناعم، والتحركات الصغيرة تعطي تغييرات مرئية صغيرة.
8. أسحب متجهًا عشوائيًا z من توزيع طبيعي معياري بحجم الـ latent، وأستغني عن الـ encoder، وأمرر z عبر الـ decoder لأحصل على صورة جديدة 64×64.""",
    ),
    "COURSE-002.M17.L01.EX02": (
        """1. Take training images, add a random amount of Gaussian noise to each, and train a network to predict (and so remove) that noise.
2. The diffusion time sets how much noise is added - from a nearly clean image to almost pure noise - so the model learns denoising at every noise level.
3. The U-Net receives the noisy image and the noise level (diffusion time) and predicts the noise that was added (equivalently, the clean image).
4. Start from pure random noise and repeatedly apply the model, removing a little predicted noise at each of many steps until an image emerges.
5. A text encoder turns the prompt into embeddings that are fed to the U-Net (through cross-attention) at every denoising step, so the denoising is conditioned on the text.
6. At each step the prediction is computed with the prompt embedding, so every partial denoise pushes the image toward content matching "a red robot walking through a snowy forest".
7. The model's prediction for the negative prompt (for example "blurry, extra arms") is subtracted, as in classifier-free guidance: the trajectory is pushed toward the positive prompt and away from the negative one.
8. More steps give finer, higher-quality images but take proportionally longer; fewer steps are faster but rougher.
9. Interpolating between the embedding of Prompt A and Prompt B (for example 30% A, 70% B) and generating from the same starting noise gives intermediate concepts - a robot gradually turning into a blue dragon.
10. Learned embeddings often lie on a curved surface where their length matters; linear interpolation passes through points with smaller norm that the model rarely saw, while spherical interpolation (slerp) keeps the vectors on that surface, giving more natural in-between images.""",
        """1. نأخذ صور التدريب ونضيف لكل منها كمية عشوائية من Gaussian noise وندرّب شبكة على التنبؤ بهذه الضوضاء (ومن ثم إزالتها).
2. وقت الـ diffusion يحدد كمية الضوضاء المضافة - من صورة شبه نظيفة إلى ضوضاء شبه خالصة - فيتعلم النموذج إزالة الضوضاء في كل المستويات.
3. يستقبل الـ U-Net الصورة المشوشة ومستوى الضوضاء (وقت الـ diffusion) ويتنبأ بالضوضاء المضافة (أو بالصورة النظيفة بشكل مكافئ).
4. نبدأ من ضوضاء عشوائية خالصة ونطبق النموذج مرارًا، فنزيل قليلًا من الضوضاء المتوقعة في كل خطوة من خطوات كثيرة حتى تظهر صورة.
5. يحوّل text encoder الـ prompt إلى embeddings تُغذَّى إلى الـ U-Net (عبر cross-attention) في كل خطوة إزالة ضوضاء، فتصبح الإزالة مشروطة بالنص.
6. في كل خطوة يُحسب التنبؤ مع embedding الـ prompt، فتدفع كل إزالة جزئية الصورة نحو محتوى يطابق "a red robot walking through a snowy forest".
7. يُطرح تنبؤ النموذج للـ negative prompt (مثل "blurry, extra arms")، كما في classifier-free guidance: فيُدفع المسار نحو الـ prompt الإيجابي وبعيدًا عن السلبي.
8. خطوات أكثر تعطي صورًا أدق وأعلى جودة لكنها تستغرق وقتًا أطول بالتناسب؛ وخطوات أقل أسرع لكن أخشن.
9. الاستيفاء بين embedding الـ Prompt A والـ Prompt B (مثل 30% من A و70% من B) والتوليد من الضوضاء الابتدائية نفسها يعطي مفاهيم وسيطة - روبوت يتحول تدريجيًا إلى تنين أزرق.
10. تقع الـ embeddings المتعلَّمة غالبًا على سطح منحنٍ يهم فيه طول المتجه؛ والاستيفاء الخطي يمر بنقاط ذات طول أصغر نادرًا ما رآها النموذج، بينما يُبقي الاستيفاء الكروي (slerp) المتجهات على ذلك السطح فتأتي الصور الوسيطة أكثر طبيعية.""",
    ),
    "COURSE-002.M18.L01.EX01": (
        """1. 3 widths x 2 dropout values x 2 optimizers = 12 configurations.
2. The test set must stay untouched to give an unbiased final estimate; choosing hyperparameters by test accuracy would fit them to the test data and make that number optimistic.
3. EarlyStopping ends a trial as soon as validation performance stops improving, so bad or already-converged configurations do not waste full training runs.
4. Results vary with random initialization and data order; averaging two runs per configuration reduces that noise, so a configuration is not chosen just because of one lucky run.
5. If thousands of configurations are tried, some will score well on the validation set by chance; the chosen one is then tuned to the peculiarities of that particular validation data and does worse on new data.
6. Train the three best models, have each predict probabilities for the same inputs, and combine them - for example averaging the class probabilities - to produce the ensemble's prediction.
7. When the models differ clearly in quality: give larger weights to the stronger models (weights chosen on validation data) instead of letting a weaker model count equally.
8. Different architectures make different mistakes, so their errors partly cancel when averaged; copies of one architecture tend to make the same mistakes, so averaging them adds little.""",
        """1. 3 قيم للعرض (widths) × قيمتان للـ dropout × 2 optimizer = 12 إعدادًا.
2. يجب أن تبقى مجموعة الاختبار دون مساس لتعطي تقديرًا نهائيًا غير منحاز؛ واختيار الـ hyperparameters حسب test accuracy يكيّفها مع بيانات الاختبار ويجعل ذلك الرقم متفائلًا.
3. ينهي EarlyStopping التجربة بمجرد توقف أداء الـ validation عن التحسن، فلا تهدر الإعدادات السيئة أو المستقرة أصلًا دورات تدريب كاملة.
4. تختلف النتائج حسب التهيئة العشوائية وترتيب البيانات؛ ومتوسط تشغيلين لكل إعداد يقلل هذه الضوضاء، فلا يُختار إعداد لمجرد تشغيلة محظوظة.
5. إذا جُرِّبت آلاف الإعدادات فسيحقق بعضها نتائج جيدة على الـ validation بالصدفة؛ فيكون المختار مضبوطًا على خصوصيات تلك البيانات ويسوء على بيانات جديدة.
6. أدرّب أفضل ثلاثة نماذج، ويتنبأ كل منها بالـ probabilities للمدخلات نفسها، ثم أجمعها - مثلًا بمتوسط probabilities الفئات - لتكوين تنبؤ الـ ensemble.
7. عندما تختلف النماذج بوضوح في الجودة: أعطي أوزانًا أكبر للنماذج الأقوى (تُختار الأوزان على بيانات الـ validation) بدلًا من أن يُحتسب النموذج الأضعف بالقدر نفسه.
8. البنى المختلفة ترتكب أخطاء مختلفة، فتلغي أخطاؤها بعضها جزئيًا عند المتوسط؛ أما نسخ البنية الواحدة فتميل لارتكاب الأخطاء نفسها، فلا يضيف متوسطها كثيرًا.""",
    ),
    "COURSE-002.M18.L01.EX02": (
        """1. Scenario A - data parallelism: the model fits on one GPU, so replicate it on all four, give each a slice of every batch, and average the gradients.
2. 512 / 4 = a local batch of 128 per GPU.
3. Data parallelism still needs a full copy of the model on every GPU; if the model does not fit on one GPU, replicating it is impossible.
4. Model sharding splits the model's weights (by layers or within layers) across several GPUs, so each GPU holds and computes only part of the model.
5. Shard the model across, for example, 2 GPUs, and run 4 such shard groups in parallel on different data (4 data replicas x 2 model shards = 8 GPUs).
6. GPUs must exchange gradients or activations after each step, and that communication, plus waiting for the slowest device, adds overhead the single-GPU run did not have.
7. Prefetching prepares the next batches on the CPU while the GPUs work on the current one, so the accelerators do not sit idle waiting for data.
8. Mixed precision does much of the math in float16 (or bfloat16), which runs faster on modern GPUs and halves memory traffic.
9. Weights stay in float32 so that the many small updates are not rounded away; float16 is used for the computations and the results are applied to the float32 copy.
10. Small gradients can underflow to zero in float16; multiplying the loss by a scale factor keeps them representable, and the gradients are divided by the same factor before the update.
11. int8 quantization stores weights (and possibly activations) as 8-bit integers with a scale factor: about 4x less memory than float32 and faster integer arithmetic on supporting hardware.
12. Most weights are small fractions such as 0.013; casting directly to int8 would round almost all of them to 0 or -1. Each value must first be divided by a scale (based on the tensor's range) so the range maps onto -127..127, and the scale is kept to recover approximate values.""",
        """1. الحالة A - data parallelism: النموذج يتسع لوحدة GPU واحدة، فنكرره على الأربع ونعطي كلًا منها جزءًا من كل دفعة ونأخذ متوسط الـ gradients.
2. 512 ÷ 4 = دفعة محلية من 128 لكل GPU.
3. الـ data parallelism يتطلب نسخة كاملة من النموذج على كل GPU؛ فإذا لم يتسع النموذج لوحدة واحدة فلا يمكن تكراره.
4. الـ model sharding يقسّم weights النموذج (حسب الطبقات أو داخلها) على عدة وحدات GPU، فتحمل كل وحدة جزءًا من النموذج فقط وتحسبه.
5. نقسّم النموذج مثلًا على وحدتين، ونشغّل 4 مجموعات كهذه بالتوازي على بيانات مختلفة (4 نسخ بيانات × جزأين للنموذج = 8 وحدات GPU).
6. يجب أن تتبادل الوحدات الـ gradients أو الـ activations بعد كل خطوة، وهذا الاتصال، مع انتظار أبطأ وحدة، يضيف عبئًا لم يكن موجودًا في التشغيل على GPU واحدة.
7. يجهّز الـ prefetching الدفعات التالية على الـ CPU بينما تعمل وحدات الـ GPU على الحالية، فلا تبقى المسرّعات خاملة في انتظار البيانات.
8. الـ mixed precision ينفذ جزءًا كبيرًا من الحسابات بـ float16 (أو bfloat16)، وهو أسرع على وحدات GPU الحديثة ويقلل نقل البيانات للنصف.
9. تبقى الـ weights بـ float32 حتى لا تضيع التحديثات الصغيرة الكثيرة بالتقريب؛ ويُستخدم float16 في الحسابات ثم تُطبق النتائج على نسخة float32.
10. قد تصبح الـ gradients الصغيرة صفرًا في float16 (underflow)؛ وضرب الـ loss في معامل تكبير يبقيها قابلة للتمثيل، ثم تُقسَّم الـ gradients على المعامل نفسه قبل التحديث.
11. الـ int8 quantization يخزن الـ weights (وربما الـ activations) كأعداد صحيحة 8-bit مع معامل scale: ذاكرة أقل بنحو 4 مرات من float32 وحساب صحيح أسرع على العتاد الداعم.
12. معظم الـ weights كسور صغيرة مثل 0.013؛ والتحويل المباشر إلى int8 سيقرّب معظمها إلى 0 أو -1. يجب أولًا قسمة كل قيمة على scale (حسب مدى الـ tensor) ليُطابق المدى نطاق -127..127، مع حفظ الـ scale لاستعادة قيم تقريبية.""",
    ),
}
