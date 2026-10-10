"""COURSE-005 Applied LLM Engineering: guided implementation exercises.

Hugging Face models cannot be downloaded in the practice sandbox. Exercises
about the Transformers API are checked by reading the code; exercises about
what you do with model outputs (classify, cluster, rank, evaluate) use small
stand-in arrays shaped exactly like those outputs and run for real.
"""
from . import Guided, check

HF_NOTE = (
    "Hugging Face models cannot be downloaded in the practice sandbox, so Check answer reads your code instead of running it.",
    "لا يمكن تنزيل نماذج Hugging Face في بيئة التدريب، لذلك يقرأ «تحقّق من الإجابة» الكود بدل تشغيله.",
)
STANDIN_NOTE = (
    "The embeddings here are small stand-ins with the same shape and meaning as a model's output, so the whole workflow runs in the sandbox.",
    "التضمينات هنا بدائل صغيرة لها أبعاد مخرجات النموذج ومعناها نفسيهما، لذلك يعمل سير العمل كله داخل بيئة التدريب.",
)

EXERCISES = {
    "COURSE-005.M01.L01.EX02": Guided(
        goal=("Complete the lesson's Phi-3 generation pipeline and control what it returns.",
              "أكمل خط توليد Phi-3 في الدرس وتحكّم فيما يعيده."),
        steps=(
            ("Load the tokenizer from the same checkpoint as the model.", "حمّل المُقسِّم من نقطة الحفظ نفسها التي حُمّل منها النموذج."),
            ("Return only the newly generated text, not the prompt.", "أعد النص المولَّد الجديد فقط، لا الموجّه (prompt)."),
            ("Use greedy decoding so the same prompt gives the same answer.", "استخدم الفك الجشع (greedy) كي يعطي الموجّه نفسه الإجابة نفسها."),
            ("Run the pipeline on the messages and print the generated text.", "شغّل الخط على الرسائل واطبع النص المولَّد."),
        ),
        starter='''from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct", device_map="cuda", torch_dtype="auto", trust_remote_code=False,
)
# Step 1: the tokenizer that belongs to this checkpoint
tokenizer = ___

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    return_full_text=___,      # Step 2: only the new text
    max_new_tokens=200,
    do_sample=___,             # Step 3: greedy decoding
)

messages = [{"role": "user", "content": "Explain in two sentences what a tokenizer does."}]
# Step 4: run the pipeline, then print the generated text
output = ___
print(___)
''',
        answers=('AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")', "False", "False",
                 "generator(messages)", 'output[0]["generated_text"]'),
        blanks=(
            ("load it with `AutoTokenizer.from_pretrained(\"microsoft/Phi-3-mini-4k-instruct\")`.",
             "حمّله بـ `AutoTokenizer.from_pretrained(\"microsoft/Phi-3-mini-4k-instruct\")`."),
            ("`return_full_text=False` drops the prompt from the output.", "يحذف `return_full_text=False` الموجّه من المخرج."),
            ("`do_sample=False` always picks the most likely next token.", "يختار `do_sample=False` دائمًا الرمز التالي الأرجح."),
            ("call the pipeline like a function: `generator(messages)`.", "استدعِ الخط كأنه دالة: `generator(messages)`."),
            ("the text is at `output[0][\"generated_text\"]`.", "النص موجود في `output[0][\"generated_text\"]`."),
        ),
        hints=(
            ("A model and its tokenizer must come from the same checkpoint name.", "يجب أن يأتي النموذج ومُقسِّمه من اسم نقطة الحفظ نفسه."),
            ("Both settings in Steps 2 and 3 are booleans.", "الإعدادان في الخطوتين 2 و3 قيم منطقية."),
            ("The pipeline returns a list with one dictionary per input.", "يعيد الخط قائمة فيها قاموس لكل مدخل."),
        ),
        success=("Correct! The tokenizer turns the prompt into IDs, the model predicts tokens one at a time, and the pipeline settings decide what comes back and how deterministic it is.",
                 "صحيح! يحوّل المُقسِّم الموجّه إلى معرّفات، ويتوقع النموذج الرموز واحدًا تلو الآخر، وتحدد إعدادات الخط ما يُعاد ومدى ثباته."),
        expected=HF_NOTE,
        reflect=("Name one practical concern from the lesson to check before using this model in a real application.",
                 "اذكر أمرًا عمليًا واحدًا من الدرس يجب التحقق منه قبل استخدام هذا النموذج في تطبيق حقيقي."),
    ),
    "COURSE-005.M02.L01.EX01": Guided(
        goal=("Tokenize the same mixed text with three tokenizers and compare their token IDs, token strings and counts.",
              "قسّم النص المختلط نفسه بثلاثة مُقسِّمات، وقارن معرّفات الرموز ونصوصها وأعدادها."),
        steps=(
            ("Load each tokenizer by name.", "حمّل كل مُقسِّم باسمه."),
            ("Get the token IDs for the text.", "احصل على معرّفات الرموز للنص."),
            ("Convert the IDs back to token strings.", "حوّل المعرّفات مرة أخرى إلى نصوص الرموز."),
            ("Print how many tokens each tokenizer produced.", "اطبع عدد الرموز التي أنتجها كل مُقسِّم."),
        ),
        starter='''from transformers import AutoTokenizer

text = """English and CAPITALIZATION
12.0*50=600
def add(a, b):
    return a + b"""

for name in ["bert-base-uncased", "bert-base-cased", "gpt2"]:
    # Step 1: load the tokenizer
    tokenizer = ___
    # Step 2: token IDs
    token_ids = ___
    # Step 3: one string per token
    tokens = ___
    # Step 4: how many tokens?
    print(f"{name}: {___} tokens")
    print(tokens)
''',
        answers=("AutoTokenizer.from_pretrained(name)", "tokenizer(text).input_ids",
                 "tokenizer.convert_ids_to_tokens(token_ids)", "len(token_ids)"),
        alternatives={
            2: ('tokenizer(text)["input_ids"]', "tokenizer.encode(text)"),
            3: ("[tokenizer.decode(token_id) for token_id in token_ids]", "[tokenizer.decode([token_id]) for token_id in token_ids]"),
            4: ("len(tokens)",),
        },
        blanks=(
            ("use `AutoTokenizer.from_pretrained(name)`.", "استخدم `AutoTokenizer.from_pretrained(name)`."),
            ("call the tokenizer on the text and take `.input_ids`.", "استدعِ المُقسِّم على النص وخذ `.input_ids`."),
            ("use `tokenizer.convert_ids_to_tokens(token_ids)`.", "استخدم `tokenizer.convert_ids_to_tokens(token_ids)`."),
            ("count the IDs with `len(token_ids)`.", "عُدّ المعرّفات بـ `len(token_ids)`."),
        ),
        hints=(
            ("The loop variable `name` holds the checkpoint name.", "يحمل متغير الحلقة `name` اسم نقطة الحفظ."),
            ("Calling a tokenizer returns a dictionary-like object with `input_ids`.", "استدعاء المُقسِّم يعيد كائنًا يشبه القاموس فيه `input_ids`."),
            ("`convert_ids_to_tokens` maps every ID back to its token string.", "تحوّل `convert_ids_to_tokens` كل معرّف إلى نص رمزه."),
        ),
        success=("Correct! Compare the outputs: the uncased BERT lowercases CAPITALIZATION, BERT drops the indentation, and GPT-2 keeps spaces inside its tokens - each choice changes what the model can see.",
                 "صحيح! قارن المخرجات: يحوّل BERT غير الحساس لحالة الأحرف الكلمة CAPITALIZATION إلى أحرف صغيرة، ويُسقط BERT المسافات البادئة، ويحتفظ GPT-2 بالمسافات داخل رموزه - وكل اختيار يغيّر ما يستطيع النموذج رؤيته."),
        expected=HF_NOTE,
        reflect=("Why is the choice of tokenizer part of model design rather than a neutral preprocessing step?",
                 "لماذا يُعدّ اختيار المُقسِّم جزءًا من تصميم النموذج لا خطوة معالجة مسبقة محايدة؟"),
    ),
    "COURSE-005.M03.L01.EX01": Guided(
        goal=("Run one forward pass by hand and turn the last position's scores into the next token.",
              "نفّذ تمريرًا أماميًا واحدًا يدويًا، وحوّل درجات الموضع الأخير إلى الرمز التالي."),
        steps=(
            ("Tokenize the prompt into a PyTorch tensor of IDs.", "قسّم الموجّه إلى موتر PyTorch من المعرّفات."),
            ("Run only the Transformer body to get hidden states.", "شغّل جسم الـ Transformer فقط للحصول على الحالات المخفية."),
            ("Project the hidden states with the LM head.", "أسقط الحالات المخفية عبر رأس النموذج اللغوي (LM head)."),
            ("Pick the highest-scoring token at the last position.", "اختر الرمز ذا الدرجة الأعلى في الموضع الأخير."),
        ),
        starter='''from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "microsoft/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="auto")
prompt = "The capital of France is"

# Step 1: token IDs as a tensor of shape (batch=1, sequence_length)
input_ids = ___
print(input_ids.shape)

# Step 2: the Transformer body only (no generate): (batch, sequence, hidden_size)
hidden = ___
print(hidden.shape)

# Step 3: scores for every vocabulary token: (batch, sequence, vocab_size)
logits = ___
print(logits.shape)

# Step 4: the most likely NEXT token comes from the LAST position
token_id = ___
print(tokenizer.decode(token_id))   # " Paris"
''',
        answers=('tokenizer(prompt, return_tensors="pt").input_ids', "model.model(input_ids)[0]",
                 "model.lm_head(hidden)", "logits[0, -1].argmax(-1)"),
        alternatives={
            1: ('tokenizer(prompt, return_tensors="pt")["input_ids"]',),
            2: ("model.model(input_ids).last_hidden_state",),
            4: ("logits[0, -1].argmax()", "logits[0, -1].argmax(dim=-1)", "logits[0, -1, :].argmax(-1)",
                "logits[0, -1, :].argmax()", "torch.argmax(logits[0, -1])"),
        },
        blanks=(
            ("pass `return_tensors=\"pt\"` and take `.input_ids`.", "مرّر `return_tensors=\"pt\"` وخذ `.input_ids`."),
            ("call `model.model(input_ids)` and take its first output.", "استدعِ `model.model(input_ids)` وخذ مخرجه الأول."),
            ("apply `model.lm_head` to the hidden states.", "طبّق `model.lm_head` على الحالات المخفية."),
            ("take batch 0, position -1, then `argmax(-1)` over the vocabulary.", "خذ الدفعة 0 والموضع -1 ثم `argmax(-1)` على المفردات."),
        ),
        hints=(
            ("`return_tensors=\"pt\"` makes the tokenizer return PyTorch tensors.", "يجعل `return_tensors=\"pt\"` المُقسِّم يعيد موترات PyTorch."),
            ("`model.model` is the stack of Transformer blocks; `model.lm_head` is the final linear layer.",
             "يمثّل `model.model` كتل الـ Transformer، ويمثّل `model.lm_head` الطبقة الخطية الأخيرة."),
            ("Index `[0, -1]` selects the first sequence and its last position.", "يختار الفهرس `[0, -1]` التسلسل الأول وموضعه الأخير."),
        ),
        success=("Correct! One forward pass produces a score for every vocabulary token at every position; the last position's best score is the next token.",
                 "صحيح! يُنتج تمرير أمامي واحد درجة لكل رمز في المفردات عند كل موضع، وأفضل درجة في الموضع الأخير هي الرمز التالي."),
        expected=HF_NOTE,
        reflect=("Why is this only one step of autoregressive generation and not a complete answer?",
                 "لماذا يُعدّ هذا خطوة واحدة فقط من التوليد الانحداري الذاتي وليس إجابة كاملة؟"),
    ),
    "COURSE-005.M04.L01.EX01": Guided(
        goal=("Train a logistic-regression classifier on frozen sentence embeddings and read its precision, recall and confusion matrix.",
              "درّب مصنّف انحدار لوجستي على تضمينات جمل مُجمّدة، واقرأ Precision وRecall ومصفوفة الالتباس."),
        steps=(
            ("Fit logistic regression on the training embeddings.", "درّب الانحدار اللوجستي على تضمينات التدريب."),
            ("Predict the test labels.", "تنبّأ بتسميات الاختبار."),
            ("Build the confusion matrix.", "ابنِ مصفوفة الالتباس."),
            ("Compute precision for the positive class.", "احسب Precision للفئة الإيجابية."),
        ),
        starter='''import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Stand-in for model.encode(texts): one row per review, 8 dimensions instead of 768
rng = np.random.default_rng(42)
centers = rng.normal(size=(2, 8))
y_train = np.array([0, 1] * 40)
y_test = np.array([0, 1] * 15)
X_train = centers[y_train] + rng.normal(scale=1.3, size=(80, 8))
X_test = centers[y_test] + rng.normal(scale=1.3, size=(30, 8))
print("embeddings:", X_train.shape, X_test.shape)    # (documents, dimensions)

# Step 1: train only a small classifier on top of the frozen embeddings
clf = ___

# Step 2: predicted labels for the test reviews
y_pred = ___
print(classification_report(y_test, y_pred, target_names=["negative", "positive"]))

# Step 3: rows = true class, columns = predicted class
cm = ___
tn, fp, fn, tp = cm.ravel()

# Step 4: precision of the positive class
precision_positive = ___
recall_positive = tp / (tp + fn)
print(cm)
print("positive precision", round(precision_positive, 3), "recall", round(recall_positive, 3))
''',
        answers=("LogisticRegression(random_state=42).fit(X_train, y_train)", "clf.predict(X_test)",
                 "confusion_matrix(y_test, y_pred)", "tp / (tp + fp)"),
        checks=(
            check("bool(np.allclose(LogisticRegression(**clf.get_params()).fit(X_train, y_train).coef_, clf.coef_))", True,
                  "Blank 1: fit `LogisticRegression` on `X_train` and `y_train` (training data only).",
                  "الفراغ 1: درّب `LogisticRegression` على `X_train` و`y_train` (بيانات التدريب فقط)."),
            check("np.asarray(y_pred).tolist() == clf.predict(X_test).tolist()", True,
                  "Blank 2: call `clf.predict(X_test)`.", "الفراغ 2: استدعِ `clf.predict(X_test)`."),
            check("np.asarray(cm).tolist() == confusion_matrix(y_test, clf.predict(X_test)).tolist()", True,
                  "Blank 3: pass the true labels first: `confusion_matrix(y_test, y_pred)`.",
                  "الفراغ 3: مرّر التسميات الصحيحة أولًا: `confusion_matrix(y_test, y_pred)`."),
            check("abs(float(precision_positive) - tp / (tp + fp)) < 1e-9", True,
                  "Blank 4: precision = TP / (TP + FP) - of everything predicted positive, how much was right?",
                  "الفراغ 4: Precision = TP / (TP + FP) - من بين كل ما تُنبّئ بأنه إيجابي، كم كان صحيحًا؟"),
        ),
        hints=(
            ("A scikit-learn model is created and fitted in one line: `Model(...).fit(X, y)`.", "يُنشأ نموذج scikit-learn ويُدرَّب في سطر واحد: `Model(...).fit(X, y)`."),
            ("`confusion_matrix(y_true, y_pred)` - the order of the arguments matters.", "في `confusion_matrix(y_true, y_pred)` يهم ترتيب الوسائط."),
            ("Precision divides true positives by all predicted positives.", "تقسم Precision الإيجابيات الصحيحة على كل التنبؤات الإيجابية."),
        ),
        success=("Correct! Only the small classifier was trained - the embedding model stayed frozen - and the report shows precision and recall separately for each class.",
                 "صحيح! دُرّب المصنّف الصغير فقط وبقي نموذج التضمين مُجمّدًا، ويعرض التقرير Precision وRecall لكل فئة على حدة."),
        expected=STANDIN_NOTE,
        reflect=("Which is more common here, false positives or false negatives? And why is this not fine-tuning the language model?",
                 "أيهما أكثر هنا: الإيجابيات الكاذبة أم السلبيات الكاذبة؟ ولماذا لا يُعدّ هذا ضبطًا دقيقًا للنموذج اللغوي؟"),
    ),
    "COURSE-005.M05.L01.EX01": Guided(
        goal=("Run the embeddings → dimensionality reduction → HDBSCAN pipeline and count clusters and outliers.",
              "نفّذ خط التضمينات ← تقليل الأبعاد ← HDBSCAN، وعُدّ العناقيد والقيم الشاذة."),
        steps=(
            ("Reduce the embeddings to 5 dimensions.", "قلّل التضمينات إلى 5 أبعاد."),
            ("Cluster the reduced embeddings with HDBSCAN.", "جمّع التضمينات المقلّصة في عناقيد باستخدام HDBSCAN."),
            ("Count the clusters, ignoring the outlier label -1.", "عُدّ العناقيد مع تجاهل تسمية القيم الشاذة -1."),
            ("Count the outlier documents.", "عُدّ المستندات الشاذة."),
            ("Project the original embeddings to 2D for a plot.", "أسقط التضمينات الأصلية إلى بُعدين للرسم."),
        ),
        starter='''import numpy as np
from sklearn.cluster import HDBSCAN
from sklearn.decomposition import PCA

# Stand-in for sentence-transformer embeddings of 120 abstracts: three topics plus 15 unrelated documents
rng = np.random.default_rng(0)
topic_centers = rng.normal(scale=4, size=(3, 32))
embeddings = np.vstack([topic_centers[i] + rng.normal(size=(35, 32)) for i in range(3)]
                       + [rng.normal(scale=6, size=(15, 32))])
print("embeddings:", embeddings.shape)          # (documents, embedding dimensions)

# Step 1: reduce to 5 dimensions (the lesson uses UMAP; PCA plays the same role here)
reduced = ___

# Step 2: density-based clustering; documents in no dense region get the label -1
labels = ___

# Step 3: number of real clusters (do not count -1)
n_clusters = ___
# Step 4: number of outlier documents
n_outliers = ___

# Step 5: a 2D projection of the ORIGINAL embeddings, only for plotting
points_2d = ___
print("clusters:", n_clusters, "| outliers:", n_outliers, "| plot points:", points_2d.shape)
''',
        answers=(
            "PCA(n_components=5, random_state=0).fit_transform(embeddings)",
            "HDBSCAN(min_cluster_size=10).fit_predict(reduced)",
            "len(set(labels.tolist()) - {-1})",
            "int((labels == -1).sum())",
            "PCA(n_components=2, random_state=0).fit_transform(embeddings)",
        ),
        checks=(
            check("list(reduced.shape)", [120, 5], "Blank 1: `PCA(n_components=5).fit_transform(embeddings)` gives (120, 5).",
                  "الفراغ 1: تعطي `PCA(n_components=5).fit_transform(embeddings)` الأبعاد (120, 5)."),
            check("len(labels) == 120 and np.asarray(labels).tolist() == HDBSCAN(min_cluster_size=10).fit_predict(reduced).tolist()", True,
                  "Blank 2: cluster the REDUCED embeddings with `HDBSCAN(min_cluster_size=10).fit_predict(reduced)`.",
                  "الفراغ 2: جمّع التضمينات المقلّصة بـ `HDBSCAN(min_cluster_size=10).fit_predict(reduced)`."),
            check("n_clusters == len(set(np.asarray(labels).tolist()) - {-1})", True,
                  "Blank 3: count the distinct labels after removing -1.", "الفراغ 3: عُدّ التسميات المميزة بعد حذف -1."),
            check("n_outliers == int((np.asarray(labels) == -1).sum())", True,
                  "Blank 4: count how many labels equal -1.", "الفراغ 4: عُدّ التسميات التي تساوي -1."),
            check("list(points_2d.shape)", [120, 2], "Blank 5: project the original embeddings to 2 components.",
                  "الفراغ 5: أسقط التضمينات الأصلية إلى مكوّنين."),
        ),
        hints=(
            ("Dimensionality reducers in scikit-learn use `fit_transform`.", "تستخدم أدوات تقليل الأبعاد في scikit-learn الدالة `fit_transform`."),
            ("`fit_predict` returns one cluster label per document; -1 means 'outlier'.", "تعيد `fit_predict` تسمية عنقود لكل مستند، و-1 تعني «قيمة شاذة»."),
            ("`set(labels.tolist()) - {-1}` removes the outlier label before counting.", "يحذف `set(labels.tolist()) - {-1}` تسمية القيم الشاذة قبل العدّ."),
        ),
        success=("Correct! Cluster IDs are only numbers - read a few documents from each cluster before you give it a theme.",
                 "صحيح! معرّفات العناقيد مجرد أرقام - اقرأ بعض المستندات من كل عنقود قبل أن تمنحه موضوعًا."),
        expected=(
            "The lesson uses UMAP, which is not installed in the sandbox; PCA reduces the dimensions in the same pipeline position. The embeddings are stand-ins shaped like a model's output.",
            "يستخدم الدرس UMAP غير المثبّتة في بيئة التدريب، لذلك تقلّل PCA الأبعاد في الموضع نفسه من الخط. والتضمينات بدائل لها أبعاد مخرجات النموذج.",
        ),
        reflect=("Why can the 2D plot not be trusted as an exact picture of the original 32-dimensional geometry?",
                 "لماذا لا يمكن الوثوق بالرسم ثنائي الأبعاد بوصفه صورة دقيقة للهندسة الأصلية ذات الأبعاد الـ32؟"),
    ),
    "COURSE-005.M05.L01.EX02": Guided(
        goal=("Compute c-TF-IDF by hand to find the keywords that describe each topic.",
              "احسب c-TF-IDF يدويًا لإيجاد الكلمات المفتاحية التي تصف كل موضوع."),
        steps=(
            ("Join the documents of each topic into one class document.", "اجمع مستندات كل موضوع في مستند فئة واحد."),
            ("Normalize each class's word counts into term frequencies.", "حوّل أعداد كلمات كل فئة إلى تكرارات نسبية."),
            ("Compute the class-based IDF: log(1 + A / f_t).", "احسب IDF المعتمد على الفئة: log(1 + A / f_t)."),
            ("Take the three highest-scoring words of each topic.", "خذ أعلى ثلاث كلمات درجةً في كل موضوع."),
        ),
        starter='''import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

docs = [
    "the striker scored a late goal in the match", "fans cheered the goal and the win",
    "the coach praised the defence after the match", "a penalty goal decided the derby",
    "the new phone has a brighter screen and battery", "battery life on the phone improved",
    "the laptop screen is sharp and the battery lasts", "phone makers raced to improve battery charging",
    "the recipe needs fresh basil and garlic", "simmer the garlic sauce before adding pasta",
    "bake the bread until the crust is golden", "fresh pasta with basil sauce for dinner",
]
topics = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]     # cluster labels from the previous step

# Step 1: one class document per topic
class_docs = ___

vectorizer = CountVectorizer(stop_words="english")
counts = vectorizer.fit_transform(class_docs).toarray()      # (topics, vocabulary)
words = vectorizer.get_feature_names_out()

# Step 2: term frequency within each class (each row sums to 1)
tf = ___
# Step 3: A = average number of words per class; f_t = how often each word appears in ALL classes
A = counts.sum() / counts.shape[0]
idf = ___
ctfidf = tf * idf

# Step 4: the three highest-scoring words per topic
top_keywords = ___
for topic, keywords in enumerate(top_keywords):
    print(topic, keywords)
''',
        answers=(
            '[" ".join(doc for doc, topic in zip(docs, topics) if topic == k) for k in sorted(set(topics))]',
            "counts / counts.sum(axis=1, keepdims=True)",
            "np.log(1 + A / counts.sum(axis=0))",
            "[words[np.argsort(row)[::-1][:3]].tolist() for row in ctfidf]",
        ),
        checks=(
            check("len(class_docs) == 3 and 'striker' in class_docs[0] and 'phone' in class_docs[1] and 'basil' in class_docs[2]", True,
                  "Blank 1: for each topic k, join the documents whose label is k.",
                  "الفراغ 1: لكل موضوع k اجمع المستندات التي تسميتها k."),
            check("bool(np.allclose(tf.sum(axis=1), 1)) and list(tf.shape) == list(counts.shape)", True,
                  "Blank 2: divide each row of `counts` by its own row sum (`keepdims=True`).",
                  "الفراغ 2: اقسم كل صف في `counts` على مجموع صفه (`keepdims=True`)."),
            check("bool(np.allclose(idf, np.log(1 + A / counts.sum(axis=0))))", True,
                  "Blank 3: f_t is the column sum of `counts`; idf = log(1 + A / f_t).",
                  "الفراغ 3: f_t هو مجموع عمود `counts`؛ وidf = log(1 + A / f_t)."),
            check("[sorted(k) for k in top_keywords] == [sorted(words[np.argsort(r)[::-1][:3]].tolist()) for r in ctfidf] and 'goal' in top_keywords[0] and 'battery' in top_keywords[1]", True,
                  "Blank 4: sort each row of `ctfidf` from high to low and take the first three words.",
                  "الفراغ 4: رتّب كل صف من `ctfidf` تنازليًا وخذ أول ثلاث كلمات."),
        ),
        hints=(
            ("Combine `zip(docs, topics)` with a condition `if topic == k`.", "اجمع `zip(docs, topics)` مع الشرط `if topic == k`."),
            ("`counts.sum(axis=1, keepdims=True)` keeps a column shape so the division broadcasts.", "يحافظ `counts.sum(axis=1, keepdims=True)` على شكل العمود فتُبثّ القسمة."),
            ("`np.argsort(row)[::-1]` lists indices from the highest score to the lowest.", "يسرد `np.argsort(row)[::-1]` الفهارس من الدرجة الأعلى إلى الأدنى."),
        ),
        success=("Correct! c-TF-IDF rewards words that are frequent inside one topic but rare across topics, which is why 'goal', 'battery' and 'basil' rise to the top.",
                 "صحيح! يكافئ c-TF-IDF الكلمات المتكررة داخل موضوع واحد والنادرة عبر المواضيع، ولهذا ترتفع «goal» و«battery» و«basil» إلى القمة."),
        reflect=("BERTopic can re-rank these keywords with KeyBERTInspired or diversify them with MMR. Why keep the raw c-TF-IDF keywords next to the re-ranked ones?",
                 "يستطيع BERTopic إعادة ترتيب هذه الكلمات بـ KeyBERTInspired أو تنويعها بـ MMR. لماذا نحتفظ بكلمات c-TF-IDF الخام إلى جانب الكلمات المعاد ترتيبها؟"),
    ),
    "COURSE-005.M06.L01.EX01": Guided(
        goal=("Build three prompt versions from reusable components and score each version on the same test set.",
              "ابنِ ثلاث نسخ من الموجّه من مكوّنات قابلة لإعادة الاستخدام، وقيّم كل نسخة على مجموعة الاختبار نفسها."),
        steps=(
            ("Add the output requirements when they are switched on.", "أضف متطلبات المخرج عند تفعيلها."),
            ("Add each few-shot example as a Review/Sentiment pair.", "أضف كل مثال توضيحي (few-shot) زوجًا من Review/Sentiment."),
            ("Write the format-compliance check.", "اكتب فحص الالتزام بالتنسيق."),
            ("Score each version: compliant and correct outputs ÷ all outputs.", "قيّم كل نسخة: المخرجات الملتزمة والصحيحة ÷ كل المخرجات."),
        ),
        starter='''INSTRUCTION = "Classify the sentiment of the product review."
REQUIREMENTS = "Answer with exactly one word: positive, negative or neutral."
EXAMPLES = [("The case cracked on day one.", "negative"), ("Works exactly as described.", "positive")]
ALLOWED = {"positive", "negative", "neutral"}

def build_prompt(review, requirements=False, examples=False):
    parts = [INSTRUCTION]
    # Step 1: the output requirements, only when switched on
    if requirements:
        parts.append(___)
    # Step 2: each example as "Review: <text>\\nSentiment: <label>"
    if examples:
        parts.extend(___ for text, label in EXAMPLES)
    parts.append(f"Review: {review}\\nSentiment:")
    return "\\n\\n".join(parts)

print(build_prompt("It arrived on time.", requirements=True, examples=True))

expected = ["negative", "positive", "neutral", "negative", "positive"]
# Model outputs recorded for the same five reviews with each prompt version
outputs = {
    "v1 zero-shot":      ["The sentiment is negative.", "Positive!", "neutral", "negative", "Mixed, mostly positive"],
    "v2 + requirements": ["negative", "positive", "neutral", "negative", "positive."],
    "v3 + examples":     ["negative", "positive", "neutral", "negative", "positive"],
}

# Step 3: compliant = the output is exactly one allowed label
def is_compliant(output):
    return ___

# Step 4: share of outputs that are compliant AND equal to the expected label
scores = {version: ___ for version, answers in outputs.items()}
print(scores)
''',
        answers=(
            "REQUIREMENTS",
            'f"Review: {text}\\nSentiment: {label}"',
            "output in ALLOWED",
            "sum(is_compliant(a) and a == e for a, e in zip(answers, expected)) / len(answers)",
        ),
        checks=(
            check("REQUIREMENTS in build_prompt('x', requirements=True) and REQUIREMENTS not in build_prompt('x')", True,
                  "Blank 1: append the `REQUIREMENTS` text.", "الفراغ 1: أضف نص `REQUIREMENTS`."),
            check("'Review: The case cracked on day one.\\nSentiment: negative' in build_prompt('x', examples=True)", True,
                  "Blank 2: format each example as `f\"Review: {text}\\nSentiment: {label}\"`.",
                  "الفراغ 2: نسّق كل مثال بالشكل `f\"Review: {text}\\nSentiment: {label}\"`."),
            check("[is_compliant('neutral'), is_compliant('positive.'), is_compliant('Positive!')]", [True, False, False],
                  "Blank 3: an output is compliant only if it is exactly one of `ALLOWED`.",
                  "الفراغ 3: يكون المخرج ملتزمًا فقط إذا كان واحدًا من `ALLOWED` تمامًا."),
            check("{k: round(v, 2) for k, v in scores.items()}", {"v1 zero-shot": 0.4, "v2 + requirements": 0.8, "v3 + examples": 1.0},
                  "Blank 4: count outputs that are compliant and equal to the expected label, then divide by the number of outputs.",
                  "الفراغ 4: عُدّ المخرجات الملتزمة والمساوية للتسمية المتوقعة، ثم اقسم على عدد المخرجات."),
        ),
        hints=(
            ("Steps 1 and 2 add text to `parts`; the constants at the top hold that text.", "تضيف الخطوتان 1 و2 نصًا إلى `parts`، والثوابت في الأعلى تحمل ذلك النص."),
            ("Use an f-string with a newline `\\n` between the review and the sentiment.", "استخدم f-string مع سطر جديد `\\n` بين المراجعة والمشاعر."),
            ("`sum(...)` over True/False values counts the True ones.", "يعدّ `sum(...)` على القيم True/False القيمَ True."),
        ),
        success=("Correct! Each component was added one at a time and measured: requirements fixed most format errors, and examples fixed the rest.",
                 "صحيح! أُضيف كل مكوّن على حدة وقيس أثره: أصلحت المتطلبات معظم أخطاء التنسيق، وأصلحت الأمثلة الباقي."),
        reflect=("Which component would you keep if every extra token cost money, and how would you decide?",
                 "أي مكوّن ستحتفظ به لو كان لكل رمز إضافي تكلفة؟ وكيف ستقرر؟"),
    ),
    "COURSE-005.M06.L01.EX02": Guided(
        goal=("Parse and validate LLM output for a support ticket, and decide what the application does when validation fails.",
              "حلّل مخرجات نموذج لغوي لتذكرة دعم وتحقّق منها، وحدّد ما يفعله التطبيق عند فشل التحقق."),
        steps=(
            ("Parse the raw text as JSON.", "حلّل النص الخام بصيغة JSON."),
            ("Reject records with missing keys.", "ارفض السجلات التي تنقصها مفاتيح."),
            ("Enforce the business rule: high priority needs a human.", "طبّق قاعدة العمل: الأولوية العالية تحتاج إلى إنسان."),
            ("Map each failure to an action.", "اربط كل فشل بإجراء."),
        ),
        starter='''import json

CATEGORIES = {"billing", "technical", "account"}
PRIORITIES = {"low", "medium", "high"}
REQUIRED = {"category", "priority", "summary", "needs_human"}

raw_outputs = [
    '{"category": "billing", "priority": "medium", "summary": "Charged twice for March", "needs_human": false}',
    '{"category": "technical", "priority": "low", "summary": "App crashes on start", "needs_human": false',
    '{"category": "shipping", "priority": "medium", "summary": "Parcel is late", "needs_human": false}',
    '{"category": "account", "priority": "high", "summary": "Locked out of account", "needs_human": false}',
]

def validate(raw):
    """Return (record, None) when valid, otherwise (None, reason)."""
    try:
        # Step 1: parse the model output
        record = ___
    except json.JSONDecodeError:
        return None, "invalid_json"
    # Step 2: every required key must be present
    if ___:
        return None, "missing_keys"
    if (record["category"] not in CATEGORIES or record["priority"] not in PRIORITIES
            or not isinstance(record["needs_human"], bool)):
        return None, "invalid_value"
    # Step 3: business rule - every high-priority ticket goes to a human
    if ___:
        return None, "rule_violation"
    return record, None

# Step 4: what the application does next (retry, repair, human_review or accept)
ACTIONS = {None: "accept", "invalid_json": "retry", "missing_keys": "retry", "invalid_value": "repair", "rule_violation": ___}

reasons = [validate(raw)[1] for raw in raw_outputs]
print(reasons)
print([ACTIONS[reason] for reason in reasons])
''',
        answers=("json.loads(raw)", "not REQUIRED <= record.keys()", 'record["priority"] == "high" and not record["needs_human"]', '"human_review"'),
        alternatives={},
        checks=(
            check("reasons", [None, "invalid_json", "invalid_value", "rule_violation"],
                  "Blanks 1 and 3: parse with `json.loads(raw)`; flag a high-priority ticket whose `needs_human` is false.",
                  "الفراغان 1 و3: حلّل بـ `json.loads(raw)`؛ وأشِر إلى أي تذكرة أولويتها عالية وقيمة `needs_human` فيها false."),
            check("validate('{\"category\": \"billing\"}')[1]", "missing_keys",
                  "Blank 2: return `missing_keys` when some of `REQUIRED` is not in the record.",
                  "الفراغ 2: أعد `missing_keys` عندما يغيب بعض `REQUIRED` عن السجل."),
            check("validate('{\"category\": \"account\", \"priority\": \"high\", \"summary\": \"x\", \"needs_human\": true}')[1] is None", True,
                  "Blank 3: a high-priority ticket that already needs a human is valid.",
                  "الفراغ 3: التذكرة عالية الأولوية التي تحتاج إلى إنسان أصلًا صالحة."),
            check("ACTIONS['rule_violation']", "human_review",
                  "Blank 4: a business-rule violation should go to `\"human_review\"`.", "الفراغ 4: يجب أن يذهب خرق قاعدة العمل إلى `\"human_review\"`."),
        ),
        hints=(
            ("`json.loads` turns a JSON string into a dictionary and raises `JSONDecodeError` on bad syntax.",
             "تحوّل `json.loads` نص JSON إلى قاموس، وتطلق `JSONDecodeError` عند خطأ الصياغة."),
            ("`set_a <= set_b` asks whether every element of `set_a` is in `set_b`.", "يسأل `set_a <= set_b` هل كل عناصر `set_a` موجودة في `set_b`."),
            ("A rule violation is a judgement call, so a person should review it.", "خرق القاعدة مسألة تقدير، لذا يجب أن يراجعه شخص."),
        ),
        success=("Correct! Each output is parsed, checked for structure, values and business rules, and every failure has a defined next step instead of crashing.",
                 "صحيح! يُحلَّل كل مخرج ويُتحقق من بنيته وقيمه وقواعد العمل، ولكل فشل خطوة تالية محددة بدل الانهيار."),
        reflect=("Grammar-constrained decoding would prevent the broken JSON. Which of the four failures would it still not prevent, and why?",
                 "يمنع الفك المقيَّد بقواعد (grammar-constrained decoding) ظهور JSON المكسور. أيٌّ من حالات الفشل الأربع لن يمنعها؟ ولماذا؟"),
    ),
    "COURSE-005.M07.L01.EX01": Guided(
        goal=("Compare full-buffer, windowed and summary memory by what each one still knows and how much text it sends.",
              "قارن ذاكرة المخزن الكامل والنافذة والملخص بما لا تزال كل منها تعرفه ومقدار النص الذي ترسله."),
        steps=(
            ("Full buffer: keep every turn.", "المخزن الكامل: احتفظ بكل الأدوار."),
            ("Window: keep only the last two interactions (four turns).", "النافذة: احتفظ بآخر تفاعلين فقط (أربعة أدوار)."),
            ("List the facts each memory can still answer.", "اذكر الحقائق التي ما زالت كل ذاكرة تستطيع الإجابة عنها."),
            ("Count the words each memory sends to the model.", "عُدّ الكلمات التي ترسلها كل ذاكرة إلى النموذج."),
        ),
        starter='''turns = [
    ("user", "Hi, I'm Lina and I'm building a recipe app."),
    ("assistant", "Nice to meet you, Lina! Which stack are you using?"),
    ("user", "React Native. My budget is 5000 dollars."),
    ("assistant", "Got it, that budget works for an MVP."),
    ("user", "The deadline is June 30."),
    ("assistant", "Noted, that gives us about two months."),
    ("user", "I prefer Supabase for the backend."),
    ("assistant", "Supabase works well with React Native."),
]
facts = {"name": "Lina", "app": "recipe", "budget": "5000", "deadline": "June 30", "backend": "Supabase"}

# Step 1: full-buffer memory sends every turn
full_buffer = ___
# Step 2: window memory keeps the last two interactions (user + assistant = one interaction)
window = ___
# A running summary written by the model during the conversation
summary = "Lina is building a recipe app in React Native on a budget of about 5k; the deadline is the end of June; she prefers Supabase."

def context_text(memory):
    return memory if isinstance(memory, str) else " ".join(text for _, text in memory)

# Step 3: which facts appear in the context a memory provides?
def answerable(memory):
    text = context_text(memory)
    return ___

results = {"full": answerable(full_buffer), "window": answerable(window), "summary": answerable(summary)}
# Step 4: context size in words
sizes = {name: ___ for name, memory in [("full", full_buffer), ("window", window), ("summary", summary)]}
print(results)
print(sizes)
''',
        answers=("turns", "turns[-4:]", "sorted(name for name, value in facts.items() if value in text)",
                 "len(context_text(memory).split())"),
        checks=(
            check("len(full_buffer)", 8, "Blank 1: the full buffer is every turn: `turns`.", "الفراغ 1: المخزن الكامل هو كل الأدوار: `turns`."),
            check("[list(t) for t in window] == [list(t) for t in turns[-4:]]", True,
                  "Blank 2: two interactions are the last four turns: `turns[-4:]`.", "الفراغ 2: التفاعلان هما آخر أربعة أدوار: `turns[-4:]`."),
            check("results", {"full": ["app", "backend", "budget", "deadline", "name"], "window": ["backend", "deadline"], "summary": ["app", "backend", "name"]},
                  "Blank 3: keep a fact's name when its exact value appears in the text, then sort the names.",
                  "الفراغ 3: احتفظ باسم الحقيقة عندما تظهر قيمتها نفسها في النص، ثم رتّب الأسماء."),
            check("[sizes['full'] > sizes['summary'], sizes['window'] < sizes['full'], sizes['summary'] == len(summary.split())]", [True, True, True],
                  "Blank 4: split the context text on whitespace and count the words.",
                  "الفراغ 4: قسّم نص السياق على المسافات وعُدّ الكلمات."),
        ),
        hints=(
            ("Slicing with a negative start keeps items from the end: `items[-2:]` keeps the last two.", "يحتفظ التقطيع ببداية سالبة بعناصر من النهاية: `items[-2:]` يحتفظ بآخر عنصرين."),
            ("`value in text` checks whether the exact fact text appears.", "يتحقق `value in text` من ظهور نص الحقيقة نفسه."),
            ("`text.split()` gives the words; `len` counts them.", "يعطي `text.split()` الكلمات، و`len` يعدّها."),
        ),
        success=("Correct! The full buffer knows everything but sends the most text, the window forgets early facts, and the summary is compact but blurred '5000 dollars' into 'about 5k' and 'June 30' into 'the end of June'.",
                 "صحيح! يعرف المخزن الكامل كل شيء لكنه يرسل أكبر قدر من النص، وتنسى النافذة الحقائق المبكرة، والملخص موجز لكنه حوّل «5000 dollars» إلى «about 5k» و«June 30» إلى «the end of June»."),
        reflect=("Which memory would you choose for a short support chat, a very long assistant conversation, and a legal workflow that must keep exact wording?",
                 "أي ذاكرة ستختار لمحادثة دعم قصيرة، ولمحادثة مساعد طويلة جدًا، ولسير عمل قانوني يجب أن يحتفظ بالصياغة الدقيقة؟"),
    ),
    "COURSE-005.M08.L01.EX01": Guided(
        goal=("Combine lexical and dense search results and evaluate them with precision@k, average precision and MAP.",
              "ادمج نتائج البحث المعجمي والبحث الكثيف، وقيّمها بمقاييس precision@k ومتوسط الدقة (AP) وMAP."),
        steps=(
            ("Build the hybrid candidate list from both rankings.", "ابنِ قائمة المرشحين الهجينة من الترتيبين."),
            ("Compute precision@k.", "احسب precision@k."),
            ("Compute average precision for one query.", "احسب متوسط الدقة لاستعلام واحد."),
            ("Average it over all queries (MAP).", "احسب متوسطه على كل الاستعلامات (MAP)."),
        ),
        starter='''relevant = {"q1": {"d3", "d7"}, "q2": {"d1"}, "q3": {"d2", "d5", "d9"}}
bm25_ranking = {"q1": ["d3", "d4", "d7", "d1", "d8"], "q2": ["d6", "d1", "d2", "d3", "d4"], "q3": ["d5", "d8", "d2", "d1", "d9"]}
dense_ranking = {"q1": ["d7", "d3", "d2", "d9", "d4"], "q2": ["d1", "d6", "d5", "d7", "d8"], "q3": ["d2", "d3", "d9", "d6", "d5"]}

# Step 1: hybrid candidates - dense results first, then BM25, without duplicates (first-seen order)
def hybrid(query):
    return ___

# Step 2: share of the top-k results that are relevant
def precision_at_k(ranking, relevant_docs, k):
    return ___

# Step 3: average of precision@k at every rank k that holds a relevant document
def average_precision(ranking, relevant_docs):
    hits = [precision_at_k(ranking, relevant_docs, k)
            for k, doc in enumerate(ranking, start=1) if doc in relevant_docs]
    return ___

# Step 4: mean of the average precisions over all queries
def mean_average_precision(rankings):
    return ___

print("hybrid q1:", hybrid("q1"))
print("MAP  bm25:", round(mean_average_precision(bm25_ranking), 4), " dense:", round(mean_average_precision(dense_ranking), 4))
''',
        answers=(
            "list(dict.fromkeys(dense_ranking[query] + bm25_ranking[query]))",
            "sum(doc in relevant_docs for doc in ranking[:k]) / k",
            "sum(hits) / len(relevant_docs)",
            "sum(average_precision(rankings[q], relevant[q]) for q in relevant) / len(relevant)",
        ),
        checks=(
            check("hybrid('q1')", ["d7", "d3", "d2", "d9", "d4", "d1", "d8"],
                  "Blank 1: concatenate dense then BM25 and drop repeats while keeping order, e.g. `list(dict.fromkeys(...))`.",
                  "الفراغ 1: ضع نتائج البحث الكثيف ثم BM25 واحذف التكرار مع الحفاظ على الترتيب، مثل `list(dict.fromkeys(...))`."),
            check("[precision_at_k(['a', 'b', 'c'], {'a', 'c'}, 1), round(precision_at_k(['a', 'b', 'c'], {'a', 'c'}, 3), 4)]", [1.0, 0.6667],
                  "Blank 2: count relevant documents in `ranking[:k]` and divide by k.",
                  "الفراغ 2: عُدّ المستندات ذات الصلة في `ranking[:k]` واقسم على k."),
            check("[round(average_precision(bm25_ranking[q], relevant[q]), 4) for q in ('q1', 'q2', 'q3')]", [0.8333, 0.5, 0.7556],
                  "Blank 3: divide the sum of the hit precisions by the number of relevant documents.",
                  "الفراغ 3: اقسم مجموع الدقة عند مواضع الإصابة على عدد المستندات ذات الصلة."),
            check("[round(mean_average_precision(bm25_ranking), 4), round(mean_average_precision(dense_ranking), 4)]", [0.6963, 0.9185],
                  "Blank 4: average `average_precision` over every query in `relevant`.",
                  "الفراغ 4: احسب متوسط `average_precision` على كل استعلام في `relevant`."),
        ),
        hints=(
            ("`dict.fromkeys(items)` keeps the first occurrence of every item, in order.", "يحتفظ `dict.fromkeys(items)` بأول ظهور لكل عنصر، بالترتيب."),
            ("Summing True/False values counts the relevant documents.", "جمع القيم True/False يعدّ المستندات ذات الصلة."),
            ("AP divides by ALL relevant documents, so a relevant document that never appears lowers the score.",
             "يقسم AP على كل المستندات ذات الصلة، لذا فإن المستند ذا الصلة الذي لا يظهر أبدًا يخفض الدرجة."),
        ),
        success=("Correct! MAP rewards finding relevant passages early: dense search scores 0.92 against 0.70 for BM25 on this mini test set, and the hybrid list gives a reranker both sets of candidates.",
                 "صحيح! يكافئ MAP العثور على المقاطع ذات الصلة مبكرًا: يحقق البحث الكثيف 0.92 مقابل 0.70 لـ BM25 في مجموعة الاختبار الصغيرة هذه، وتعطي القائمة الهجينة أداةَ إعادة الترتيب كلتا مجموعتي المرشحين."),
        reflect=("Which retrieval errors would still remain after a cross-encoder reranks the hybrid list?",
                 "ما أخطاء الاسترجاع التي ستبقى بعد أن تعيد أداة cross-encoder ترتيب القائمة الهجينة؟"),
    ),
    "COURSE-005.M09.L01.EX01": Guided(
        goal=("Compare images and captions in a shared CLIP-style embedding space and use it for zero-shot classification.",
              "قارن الصور والتسميات التوضيحية في فضاء تضمين مشترك بأسلوب CLIP، واستخدمه للتصنيف دون أمثلة (zero-shot)."),
        steps=(
            ("L2-normalize the image embeddings.", "طبّع تضمينات الصور بمعيار L2."),
            ("Compute the image × caption cosine-similarity matrix.", "احسب مصفوفة تشابه جيب التمام بين الصور والتسميات."),
            ("Rank the captions for every image.", "رتّب التسميات لكل صورة."),
            ("Predict the best caption for each image.", "تنبّأ بأفضل تسمية لكل صورة."),
        ),
        starter='''import numpy as np

captions = ["a photo of a cat", "a photo of a dog", "a city skyline at night", "a bowl of fruit"]
# Stand-ins for model.get_image_features(...) and model.get_text_features(...)
image_embeddings = np.array([
    [0.9, 0.1, 0.0, 0.1, 0.3, 0.0],     # image 0: a cat
    [0.2, 0.8, 0.1, 0.0, 0.3, 0.1],     # image 1: a dog
    [0.0, 0.1, 0.9, 0.2, 0.0, 0.3],     # image 2: a skyline
    [0.5, 0.4, 0.1, 0.2, 0.6, 0.1],     # image 3: a fox (no caption describes it)
])
text_embeddings = np.array([
    [1.0, 0.1, 0.0, 0.0, 0.2, 0.0],
    [0.1, 1.0, 0.0, 0.1, 0.2, 0.1],
    [0.0, 0.0, 1.0, 0.1, 0.0, 0.3],
    [0.1, 0.0, 0.1, 1.0, 0.1, 0.0],
])

# Step 1: unit-length rows (L2 normalization)
img = ___
txt = text_embeddings / np.linalg.norm(text_embeddings, axis=1, keepdims=True)

# Step 2: cosine similarity for every (image, caption) pair
similarity = ___

# Step 3: for each image, caption indices from most to least similar
rankings = ___

# Step 4: zero-shot classification - the best caption per image
predicted = ___

print(similarity.round(2))
print(predicted)
''',
        answers=(
            "image_embeddings / np.linalg.norm(image_embeddings, axis=1, keepdims=True)",
            "img @ txt.T",
            "np.argsort(-similarity, axis=1)",
            "[captions[i] for i in similarity.argmax(axis=1)]",
        ),
        checks=(
            check("bool(np.allclose(np.linalg.norm(img, axis=1), 1)) and bool(np.allclose(img[0] * np.linalg.norm(image_embeddings[0]), image_embeddings[0]))", True,
                  "Blank 1: divide each row by its own L2 norm (`axis=1, keepdims=True`).",
                  "الفراغ 1: اقسم كل صف على معياره L2 (`axis=1, keepdims=True`)."),
            check("list(similarity.shape) == [4, 4] and bool(np.allclose(similarity, img @ txt.T))", True,
                  "Blank 2: with unit vectors, cosine similarity is a matrix product: `img @ txt.T`.",
                  "الفراغ 2: مع المتجهات ذات الطول الواحد يصبح تشابه جيب التمام ضربًا مصفوفيًا: `img @ txt.T`."),
            check("np.asarray(rankings)[:, 0].tolist() == similarity.argmax(axis=1).tolist() and np.asarray(rankings)[:, -1].tolist() == similarity.argmin(axis=1).tolist()", True,
                  "Blank 3: sort each row in descending order, e.g. `np.argsort(-similarity, axis=1)`.",
                  "الفراغ 3: رتّب كل صف تنازليًا، مثل `np.argsort(-similarity, axis=1)`."),
            check("predicted[:3]", ["a photo of a cat", "a photo of a dog", "a city skyline at night"],
                  "Blank 4: pick the caption at `similarity.argmax(axis=1)` for every image.",
                  "الفراغ 4: اختر التسمية عند `similarity.argmax(axis=1)` لكل صورة."),
        ),
        hints=(
            ("`np.linalg.norm(x, axis=1, keepdims=True)` gives each row's length as a column.", "يعطي `np.linalg.norm(x, axis=1, keepdims=True)` طول كل صف على شكل عمود."),
            ("Images are rows and captions are columns: `img @ txt.T`.", "الصور صفوف والتسميات أعمدة: `img @ txt.T`."),
            ("`argsort` sorts ascending, so sort `-similarity` to get the most similar first.", "يرتّب `argsort` تصاعديًا، لذا رتّب `-similarity` للحصول على الأكثر تشابهًا أولًا."),
        ),
        success=("Correct! The cat, dog and skyline match their captions, while the fox is still forced onto one of the four captions - relative scores only rank the candidates you supply.",
                 "صحيح! تطابق القطة والكلب وخط الأفق تسمياتها، بينما يُجبَر الثعلب على إحدى التسميات الأربع - فالدرجات النسبية ترتّب المرشحين الذين تقدّمهم فقط."),
        expected=STANDIN_NOTE,
        reflect=("Why is a single similarity score hard to interpret on its own, and how would the same matrix support text-to-image retrieval?",
                 "لماذا يصعب تفسير درجة تشابه واحدة بمفردها؟ وكيف تدعم المصفوفة نفسها استرجاع الصور من النص؟"),
    ),
    "COURSE-005.M10.L01.EX01": Guided(
        goal=("Implement the Multiple Negatives Ranking loss and see why hard negatives teach an embedding model more than easy ones.",
              "نفّذ دالة الخسارة Multiple Negatives Ranking، وافهم لماذا تعلّم السلبيات الصعبة نموذج التضمين أكثر من السهلة."),
        steps=(
            ("Score every anchor against every positive in the batch.", "احسب درجة كل نقطة ارتكاز (anchor) مقابل كل إيجابي في الدفعة."),
            ("Write the MNR loss: cross-entropy where anchor i's correct match is positive i.", "اكتب خسارة MNR: cross-entropy حيث المطابق الصحيح لنقطة الارتكاز i هو الإيجابي i."),
            ("Write the cosine-similarity loss: MSE between scores and gold labels.", "اكتب خسارة تشابه جيب التمام: متوسط مربع الخطأ بين الدرجات والتسميات المرجعية."),
            ("Compare the loss with a hard negative against an easy negative.", "قارن الخسارة مع سلبي صعب مقابل سلبي سهل."),
        ),
        starter='''import numpy as np

def normalize(x):
    return x / np.linalg.norm(x, axis=-1, keepdims=True)

rng = np.random.default_rng(0)
anchors = normalize(rng.normal(size=(4, 16)))
positives = normalize(anchors + 0.3 * rng.normal(size=(4, 16)))   # paraphrases of each anchor

# Step 1: cosine similarity of every anchor with every positive (in-batch negatives)
scores = ___

# Step 2: MNR loss - for anchor i the correct "class" is column i
def mnr_loss(scores, scale=20.0):
    logits = scale * scores
    log_probs = logits - np.log(np.exp(logits).sum(axis=1, keepdims=True))
    return ___

# Step 3: cosine-similarity loss for labelled pairs
def cosine_loss(pair_scores, gold):
    return ___

# Step 4: one extra candidate for anchor 0 - an easy (unrelated) or a hard (close but wrong) negative
easy_negative = normalize(rng.normal(size=(1, 16)))
hard_negative = normalize(anchors[:1] + 0.5 * rng.normal(size=(1, 16)))
loss_easy = mnr_loss(np.hstack([scores, anchors @ easy_negative.T]))
loss_hard = mnr_loss(np.hstack([scores, anchors @ hard_negative.T]))
hard_negative_costs_more = ___

print("MNR loss:", round(mnr_loss(scores), 4), "| with easy negative:", round(loss_easy, 4), "| with hard negative:", round(loss_hard, 4))
''',
        answers=("anchors @ positives.T", "-np.mean(np.diag(log_probs))", "np.mean((pair_scores - gold) ** 2)", "bool(loss_hard > loss_easy)"),
        checks=(
            check("bool(np.allclose(scores, anchors @ positives.T))", True,
                  "Blank 1: with unit vectors, `anchors @ positives.T` gives every cosine similarity.",
                  "الفراغ 1: مع المتجهات ذات الطول الواحد يعطي `anchors @ positives.T` كل قيم تشابه جيب التمام."),
            check("abs(float(mnr_loss(np.eye(3) * 0.9)) - float(-np.mean(np.diag((lambda l: l - np.log(np.exp(l).sum(axis=1, keepdims=True)))(20.0 * np.eye(3) * 0.9))))) < 1e-9", True,
                  "Blank 2: average the negative log-probability on the diagonal: `-np.mean(np.diag(log_probs))`.",
                  "الفراغ 2: احسب متوسط سالب لوغاريتم الاحتمال على القطر: `-np.mean(np.diag(log_probs))`."),
            check("[round(float(cosine_loss(np.array([0.9, 0.2]), np.array([1.0, 0.0]))), 4), float(cosine_loss(np.array([0.5]), np.array([0.5])))]", [0.025, 0.0],
                  "Blank 3: mean squared error between predicted cosine scores and gold labels.",
                  "الفراغ 3: متوسط مربع الخطأ بين درجات جيب التمام المتوقعة والتسميات المرجعية."),
            check("hard_negative_costs_more == bool(loss_hard > loss_easy) and hard_negative_costs_more", True,
                  "Blank 4: compare the two losses: `bool(loss_hard > loss_easy)`.", "الفراغ 4: قارن الخسارتين: `bool(loss_hard > loss_easy)`."),
        ),
        hints=(
            ("Row i of `scores` holds anchor i's similarity to every positive; the diagonal holds the true pairs.",
             "يحمل الصف i من `scores` تشابه نقطة الارتكاز i مع كل إيجابي، ويحمل القطر الأزواج الصحيحة."),
            ("`np.diag(log_probs)` picks the log-probability of the correct column in every row.", "يختار `np.diag(log_probs)` لوغاريتم احتمال العمود الصحيح في كل صف."),
            ("A hard negative is similar to the anchor, so it steals probability from the true positive.", "السلبي الصعب يشبه نقطة الارتكاز، فيسرق جزءًا من احتمال الإيجابي الصحيح."),
        ),
        success=("Correct! MNR treats every other positive in the batch as a negative, and a hard negative raises the loss far more than an easy one - so it gives the model more to learn from.",
                 "صحيح! تعامل MNR كل إيجابي آخر في الدفعة بوصفه سلبيًا، ويرفع السلبي الصعب الخسارة أكثر بكثير من السلبي السهل - فيمنح النموذج ما يتعلمه أكثر."),
        reflect=("Write one anchor with an easy negative and a hard negative of your own. Why is the hard one difficult but still wrong?",
                 "اكتب نقطة ارتكاز واحدة مع سلبي سهل وسلبي صعب من عندك. لماذا يكون الصعب صعبًا لكنه يبقى خاطئًا؟"),
    ),
    "COURSE-005.M11.L01.EX01": Guided(
        goal=("Count the trainable parameters of full fine-tuning, head-only training and partial unfreezing of BERT.",
              "احسب المعاملات القابلة للتدريب في الضبط الكامل، وتدريب الرأس فقط، وفكّ التجميد الجزئي لنموذج BERT."),
        steps=(
            ("Full fine-tuning: every parameter trains.", "الضبط الكامل: يتدرّب كل معامل."),
            ("Head only: only the classifier trains.", "الرأس فقط: يتدرّب المصنّف وحده."),
            ("Partial: classifier, pooler and the last two encoder blocks.", "جزئي: المصنّف والـ pooler وآخر كتلتين في المُرمِّز."),
            ("Compute the share of parameters the partial setup trains.", "احسب نسبة المعاملات التي يدرّبها الإعداد الجزئي."),
        ),
        starter='''# Parameter counts of bert-base-uncased with a 2-class head, grouped by module
param_sizes = {
    "bert.embeddings": 23_837_184,
    **{f"bert.encoder.layer.{i}": 7_087_872 for i in range(12)},
    "bert.pooler": 590_592,
    "classifier": 1_538,
}

def trainable(is_trainable):
    """Sum the sizes of the modules for which is_trainable(name) is True
    (in PyTorch: param.requires_grad = is_trainable(name))."""
    return sum(size for name, size in param_sizes.items() if is_trainable(name))

# Step 1: full fine-tuning
full = ___
# Step 2: classification head only
head_only = ___
# Step 3: head + pooler + encoder blocks 10 and 11
partial = trainable(lambda name: name.startswith(___))
# Step 4: share of all parameters trained in the partial setup, rounded to 4 decimals
partial_share = ___

print(f"full {full:,} | head only {head_only:,} | partial {partial:,} ({partial_share:.1%})")
''',
        answers=(
            "trainable(lambda name: True)",
            'trainable(lambda name: name == "classifier")',
            '("classifier", "bert.pooler", "bert.encoder.layer.10", "bert.encoder.layer.11")',
            "round(partial / full, 4)",
        ),
        checks=(
            check("full", 109483778, "Blank 1: everything trains, so the rule returns True for every name.",
                  "الفراغ 1: يتدرّب كل شيء، لذا تعيد القاعدة True لكل اسم."),
            check("head_only", 1538, "Blank 2: only the `classifier` module trains.", "الفراغ 2: تتدرّب الوحدة `classifier` فقط."),
            check("partial", 14767874,
                  "Blank 3: pass a tuple of the four prefixes - `startswith` accepts a tuple.",
                  "الفراغ 3: مرّر صفًّا من البادئات الأربع - فالدالة `startswith` تقبل صفًّا."),
            check("partial_share", 0.1349, "Blank 4: divide `partial` by `full` and round to 4 decimals.",
                  "الفراغ 4: اقسم `partial` على `full` وقرّب إلى 4 منازل عشرية."),
        ),
        hints=(
            ("`lambda name: True` is a rule that accepts every module.", "القاعدة `lambda name: True` تقبل كل وحدة."),
            ("Compare the module name with \"classifier\" for the head-only rule.", "قارن اسم الوحدة بـ \"classifier\" في قاعدة الرأس فقط."),
            ("`name.startswith((\"a\", \"b\"))` is True if the name starts with any of them.", "تكون `name.startswith((\"a\", \"b\"))` صحيحة إذا بدأ الاسم بأيٍّ منها."),
        ),
        success=("Correct! Head-only training updates 0.001% of BERT, partial unfreezing about 13.5%, and full fine-tuning all 109 million parameters - compute grows with each step.",
                 "صحيح! يحدّث تدريب الرأس فقط 0.001% من BERT، ويحدّث فكّ التجميد الجزئي نحو 13.5%، ويحدّث الضبط الكامل كل المعاملات الـ109 ملايين - وتزداد الحوسبة مع كل خطوة."),
        reflect=("For a resource-constrained deployment, which setup would you choose, and what accuracy loss would you accept?",
                 "في نشر محدود الموارد، أي إعداد ستختار؟ وما خسارة الدقة التي ستقبلها؟"),
    ),
    "COURSE-005.M12.L01.EX01": Guided(
        goal=("Plan a QLoRA instruction-tuning run: format the data, compute the effective batch size, and count the LoRA parameters.",
              "خطّط لتجربة ضبط بالتعليمات باستخدام QLoRA: نسّق البيانات، واحسب حجم الدفعة الفعلي، وعُدّ معاملات LoRA."),
        steps=(
            ("Format one example with the TinyLlama chat template.", "نسّق مثالًا واحدًا بقالب المحادثة الخاص بـ TinyLlama."),
            ("Compute the effective batch size.", "احسب حجم الدفعة الفعلي."),
            ("Count the LoRA parameters for one weight matrix.", "عُدّ معاملات LoRA لمصفوفة أوزان واحدة."),
            ("Count the LoRA parameters for all target modules in all layers.", "عُدّ معاملات LoRA لكل الوحدات المستهدفة في كل الطبقات."),
        ),
        starter='''# Step 1: the chat template the base model will also see at inference time
def format_example(instruction, response):
    return ___

print(format_example("What is QLoRA?", "QLoRA fine-tunes LoRA adapters on top of a 4-bit base model."))

# Step 2: examples per optimizer step
per_device_batch_size, gradient_accumulation_steps, num_gpus = 2, 8, 1
effective_batch_size = ___

# Step 3: a LoRA adapter on a (d_in -> d_out) matrix adds A (d_in x r) and B (r x d_out)
def lora_params(d_in, d_out, r):
    return ___

# TinyLlama: 22 layers; attention projections (input, output) sizes
targets = {"q_proj": (2048, 2048), "k_proj": (2048, 256), "v_proj": (2048, 256), "o_proj": (2048, 2048)}
r, n_layers = 64, 22
# Step 4: adapters on every target module of every layer
total_lora = ___

base_params = 1.1e9
print("effective batch:", effective_batch_size)
print(f"LoRA parameters: {total_lora:,} ({total_lora / base_params:.2%} of the base model)")
print("4-bit base weights:", round(base_params * 0.5 / 1e9, 2), "GB")
''',
        answers=(
            'f"<|user|>\\n{instruction}</s>\\n<|assistant|>\\n{response}</s>"',
            "per_device_batch_size * gradient_accumulation_steps * num_gpus",
            "r * (d_in + d_out)",
            "n_layers * sum(lora_params(d_in, d_out, r) for d_in, d_out in targets.values())",
        ),
        checks=(
            check("format_example('Hi', 'Hello')", "<|user|>\nHi</s>\n<|assistant|>\nHello</s>",
                  "Blank 1: return `f\"<|user|>\\n{instruction}</s>\\n<|assistant|>\\n{response}</s>\"`.",
                  "الفراغ 1: أعد `f\"<|user|>\\n{instruction}</s>\\n<|assistant|>\\n{response}</s>\"`."),
            check("effective_batch_size", 16, "Blank 2: multiply the batch per device, the accumulation steps and the number of GPUs.",
                  "الفراغ 2: اضرب الدفعة لكل جهاز في خطوات التراكم في عدد وحدات GPU."),
            check("lora_params(2048, 256, 8)", 18432, "Blank 3: A has d_in × r values and B has r × d_out: r · (d_in + d_out).",
                  "الفراغ 3: للمصفوفة A d_in × r قيمة، وللمصفوفة B r × d_out: أي r · (d_in + d_out)."),
            check("total_lora", 18022400, "Blank 4: sum over the four target modules, then multiply by the 22 layers.",
                  "الفراغ 4: اجمع على الوحدات المستهدفة الأربع ثم اضرب في الطبقات الـ22."),
        ),
        hints=(
            ("The template wraps the user turn and the assistant turn in their role tags, each ending with </s>.",
             "يحيط القالب دور المستخدم ودور المساعد بوسوم أدوارهما، وينتهي كلٌّ منهما بـ </s>."),
            ("Gradient accumulation adds up several small batches before one optimizer step.", "يجمع تراكم التدرّجات عدة دفعات صغيرة قبل خطوة مُحسِّن واحدة."),
            ("LoRA replaces a d_in × d_out update by two thin matrices of rank r.", "يستبدل LoRA تحديثًا بحجم d_in × d_out بمصفوفتين رفيعتين من الرتبة r."),
        ),
        success=("Correct! About 18 million LoRA parameters - under 2% of the model - train on top of 4-bit base weights that need roughly 0.55 GB.",
                 "صحيح! نحو 18 مليون معامل LoRA - أقل من 2% من النموذج - تتدرّب فوق أوزان أساسية بدقة 4 بت تحتاج إلى نحو 0.55 GB."),
        reflect=("What does a larger LoRA rank buy you, what does it cost, and how could optimizing only for a benchmark mislead you?",
                 "ماذا تكسب من رتبة LoRA أكبر؟ وما تكلفتها؟ وكيف قد يضلّلك التحسين من أجل معيار قياسي واحد فقط؟"),
    ),
}
