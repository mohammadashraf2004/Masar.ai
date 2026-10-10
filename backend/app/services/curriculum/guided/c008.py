"""COURSE-008 Vision, Language and Multimodal AI Engineering: guided implementation exercises."""
from . import Guided, check

EXERCISES = {
    "COURSE-008.M01.L01.EX04": Guided(
        goal=("Build a text-to-image retrieval index that derives its dimension from a real embedding, normalizes vectors and returns the top 5 images.",
              "ابنِ فهرس استرجاع للصور من النص، يستنتج بُعده من تضمين حقيقي، ويطبّع المتجهات، ويعيد أفضل 5 صور."),
        steps=(
            ("Read the index dimension from one sample embedding.", "اقرأ بُعد الفهرس من تضمين عينة واحد."),
            ("L2-normalize all image embeddings.", "طبّع كل تضمينات الصور بمعيار L2."),
            ("L2-normalize the text query embedding.", "طبّع تضمين الاستعلام النصي بمعيار L2."),
            ("Return the 5 most similar images.", "أعد أكثر 5 صور تشابهًا."),
        ),
        starter='''import numpy as np

rng = np.random.default_rng(0)
IMAGE_FEATURES = rng.normal(size=(50, 12))                     # stand-in for SigLIP image features
QUERY_FEATURES = IMAGE_FEATURES[7] * 2 + rng.normal(scale=0.3, size=12)

def get_image_embedding(index):        # model.get_image_features(**processor(images=...))
    return IMAGE_FEATURES[index]

def get_text_embedding(text):          # model.get_text_features(**processor(text=...))
    return QUERY_FEATURES

# Step 1: embed ONE image first and take the index dimension from it (never hard-code it)
sample = get_image_embedding(0)
dim = ___

vectors = np.stack([get_image_embedding(i) for i in range(len(IMAGE_FEATURES))])
assert vectors.shape[1] == dim, "embedding size does not match the index dimension"
# Step 2: unit-length rows, so inner product = cosine similarity (faiss.IndexFlatIP)
vectors = ___

# Step 3: the query must be normalized the same way
query = get_text_embedding("a red bicycle")
query = ___

# Step 4: the 5 best images (what index.search(query, 5) returns)
scores = vectors @ query
top5 = ___
print("dimension", dim, "| top 5:", top5)
''',
        answers=("sample.shape[-1]", "vectors / np.linalg.norm(vectors, axis=1, keepdims=True)",
                 "query / np.linalg.norm(query)", "np.argsort(-scores)[:5].tolist()"),
        checks=(
            check("int(dim)", 12, "Blank 1: read the dimension from the sample: `sample.shape[-1]`.",
                  "الفراغ 1: اقرأ البُعد من العينة: `sample.shape[-1]`."),
            check("bool(np.allclose(np.linalg.norm(vectors, axis=1), 1)) and bool(np.allclose(vectors[3] * np.linalg.norm(IMAGE_FEATURES[3]), IMAGE_FEATURES[3]))", True,
                  "Blank 2: divide every row by its own L2 norm (`axis=1, keepdims=True`).",
                  "الفراغ 2: اقسم كل صف على معياره L2 (`axis=1, keepdims=True`)."),
            check("bool(np.isclose(np.linalg.norm(query), 1))", True, "Blank 3: divide the query by `np.linalg.norm(query)`.",
                  "الفراغ 3: اقسم الاستعلام على `np.linalg.norm(query)`."),
            check("list(top5) == np.argsort(-(vectors @ query))[:5].tolist() and list(top5)[0] == 7", True,
                  "Blank 4: sort the scores from high to low and keep the first five indices.",
                  "الفراغ 4: رتّب الدرجات تنازليًا واحتفظ بأول خمسة فهارس."),
        ),
        hints=(
            ("The last axis of an embedding is its dimension.", "المحور الأخير في التضمين هو بُعده."),
            ("`np.linalg.norm(x, axis=1, keepdims=True)` gives one length per row.", "يعطي `np.linalg.norm(x, axis=1, keepdims=True)` طولًا واحدًا لكل صف."),
            ("`np.argsort(-scores)` lists indices from the highest score down.", "يسرد `np.argsort(-scores)` الفهارس من أعلى درجة نزولًا."),
        ),
        success=("Correct! Image 7 comes first, and the dimension check stops a mismatched model from silently writing wrong-sized vectors into the index.",
                 "صحيح! تأتي الصورة 7 أولًا، ويمنع فحص البُعد نموذجًا غير مطابق من كتابة متجهات بحجم خاطئ في الفهرس بصمت."),
        expected=(
            "NumPy stands in for SigLIP and FAISS here: `vectors @ query` is exactly what `IndexFlatIP.search` computes on normalized vectors.",
            "يحل NumPy هنا محل SigLIP وFAISS: فما يحسبه `vectors @ query` هو بالضبط ما يحسبه `IndexFlatIP.search` على المتجهات المطبَّعة.",
        ),
        reflect=("What failure does the dimension check prevent when someone later swaps the embedding model?",
                 "ما الفشل الذي يمنعه فحص البُعد عندما يستبدل أحدهم نموذج التضمين لاحقًا؟"),
    ),
    "COURSE-008.M01.L03.EX02": Guided(
        goal=("Line up next-token labels with model positions when an input starts with image embeddings.",
              "حاذِ تسميات الرمز التالي مع مواضع النموذج عندما يبدأ المدخل بتضمينات صورة."),
        steps=(
            ("Build the labels: image positions and the last position get -100.", "ابنِ التسميات: مواضع الصورة والموضع الأخير تأخذ -100."),
            ("List the (position, target) pairs that train the model.", "اذكر أزواج (الموضع، الهدف) التي تدرّب النموذج."),
            ("List the excluded positions.", "اذكر المواضع المستبعدة."),
        ),
        starter='''IGNORE = -100
n_image = 3
text_ids = [10, 20, 30, 40]
# position:   0    1    2    3   4   5   6
# input:     img  img  img  10  20  30  40
# The logit at a position predicts the NEXT token.

# Step 1: label per position - the next text token, or IGNORE where there is none to learn
labels = [IGNORE] * n_image + ___

# Step 2: (position, target) pairs that contribute to the loss
pairs = ___

# Step 3: positions excluded from the loss
excluded = ___

print(labels)
print(pairs, excluded)
''',
        answers=("text_ids[1:] + [IGNORE]",
                 "[(position, label) for position, label in enumerate(labels) if label != IGNORE]",
                 "[position for position, label in enumerate(labels) if label == IGNORE]"),
        checks=(
            check("labels", [-100, -100, -100, 20, 30, 40, -100],
                  "Blank 1: text position i predicts text token i+1 (`text_ids[1:]`), and the last position has no next token.",
                  "الفراغ 1: يتنبأ الموضع النصي i بالرمز النصي i+1 (`text_ids[1:]`)، وليس للموضع الأخير رمز تالٍ."),
            check("[list(p) for p in pairs]", [[3, 20], [4, 30], [5, 40]],
                  "Blank 2: keep (position, label) for every label that is not IGNORE.",
                  "الفراغ 2: احتفظ بـ (الموضع، التسمية) لكل تسمية لا تساوي IGNORE."),
            check("excluded", [0, 1, 2, 6], "Blank 3: list the positions whose label is IGNORE.",
                  "الفراغ 3: اذكر المواضع التي تسميتها IGNORE."),
        ),
        hints=(
            ("Shifting by one means the label at text position i is the text token at i+1.", "الإزاحة بموضع واحد تعني أن تسمية الموضع النصي i هي الرمز النصي في i+1."),
            ("`enumerate(labels)` yields (position, label) pairs.", "تعطي `enumerate(labels)` أزواج (الموضع، التسمية)."),
            ("-100 is the ignore index of PyTorch's cross-entropy.", "القيمة -100 هي مؤشر التجاهل في cross-entropy في PyTorch."),
        ),
        success=("Correct! Only text positions 3-5 are trained to predict 20, 30 and 40; image positions are context, not targets, and the last logit has nothing left to predict.",
                 "صحيح! لا تُدرَّب إلا المواضع النصية 3-5 على توقّع 20 و30 و40؛ مواضع الصورة سياق لا أهداف، وآخر logit لم يبقَ له ما يتوقعه."),
        reflect=("If image positions are never targets, how do they still influence the text predictions?",
                 "إذا لم تكن مواضع الصورة أهدافًا أبدًا، فكيف تؤثر مع ذلك في تنبؤات النص؟"),
    ),
    "COURSE-008.M01.L05.EX01": Guided(
        goal=("Build the label mask for a multimodal SFT example so only the assistant's answer is learned.",
              "ابنِ قناع التسميات لمثال ضبط بالتعليمات متعدد الوسائط، بحيث لا يُتعلَّم إلا جواب المساعد."),
        steps=(
            ("Keep assistant tokens as labels and replace everything else with -100.", "أبقِ رموز المساعد تسمياتٍ واستبدل كل ما عداها بـ -100."),
            ("Count the positions that contribute to the loss.", "عُدّ المواضع التي تساهم في الخسارة."),
            ("Compute the share of ignored positions.", "احسب نسبة المواضع المتجاهَلة."),
        ),
        starter='''IGNORE = -100
segments = [
    ("system", [1, 2, 3]),             # "You are a helpful assistant."
    ("image", [900, 900, 900, 900]),   # image placeholder tokens
    ("user", [11, 12, 13]),            # "What is in the picture?"
    ("assistant", [21, 22, 23, 24]),   # "A cat on a sofa."
]
input_ids = [token for _, ids in segments for token in ids]

# Step 1: learn only the assistant's tokens; system, image and user are context
labels = [___ for role, ids in segments for token in ids]

# Step 2: positions that contribute to the next-token loss
n_trained = ___

# Step 3: share of positions ignored by the loss (3 decimals)
ignored_share = ___

print(input_ids)
print(labels)
print(n_trained, "trained positions |", ignored_share, "ignored")
''',
        answers=('token if role == "assistant" else IGNORE', "sum(label != IGNORE for label in labels)",
                 "round(1 - n_trained / len(labels), 3)"),
        checks=(
            check("labels", [-100] * 10 + [21, 22, 23, 24],
                  "Blank 1: use `token if role == \"assistant\" else IGNORE`.", "الفراغ 1: استخدم `token if role == \"assistant\" else IGNORE`."),
            check("n_trained", 4, "Blank 2: count the labels that are not IGNORE.", "الفراغ 2: عُدّ التسميات التي لا تساوي IGNORE."),
            check("ignored_share", 0.714, "Blank 3: one minus the trained share, rounded to 3 decimals.",
                  "الفراغ 3: واحد ناقص نسبة المواضع المدرَّبة، مقرّبًا إلى 3 منازل."),
        ),
        hints=(
            ("A conditional expression inside the comprehension decides each label.", "يحدد تعبير شرطي داخل الـ comprehension كل تسمية."),
            ("`sum` over True/False counts the True values.", "يعدّ `sum` على القيم True/False القيمَ True."),
            ("The ignored share is 1 − trained / total.", "نسبة المتجاهَل هي 1 − المدرَّب / الإجمالي."),
        ),
        success=("Correct! The model sees the system prompt, image and question as context, but is only trained to produce the assistant's answer.",
                 "صحيح! يرى النموذج موجّه النظام والصورة والسؤال سياقًا، لكنه لا يُدرَّب إلا على إنتاج جواب المساعد."),
        reflect=("What would the model learn if the user's question were also kept in the labels?",
                 "ماذا سيتعلم النموذج لو بقي سؤال المستخدم أيضًا ضمن التسميات؟"),
    ),
    "COURSE-008.M01.L09.EX04": Guided(
        goal=("Repair a video SFT collator so it trains on the answer only, with padding masked out.",
              "أصلح أداة تجميع (collator) لضبط الفيديو بالتعليمات كي تتدرّب على الجواب فقط مع إخفاء الحشو."),
        steps=(
            ("Mask prompt and video tokens, keep the answer, mask the padding.", "أخفِ رموز الموجّه والفيديو، وأبقِ الجواب، وأخفِ الحشو."),
            ("Build the attention mask.", "ابنِ قناع الانتباه."),
            ("Count how many positions the buggy `labels = input_ids` version trained on by mistake.", "عُدّ المواضع التي دُرّبت عليها النسخة الخاطئة `labels = input_ids` بالخطأ."),
        ),
        starter='''PAD_ID, IGNORE = 0, -100

def collate(examples):
    sequences = [ex["prompt_ids"] + ex["video_ids"] + ex["answer_ids"] for ex in examples]
    max_len = max(len(seq) for seq in sequences)
    batch = {"input_ids": [], "labels": [], "attention_mask": []}
    for ex, seq in zip(examples, sequences):
        pad = max_len - len(seq)
        batch["input_ids"].append(seq + [PAD_ID] * pad)
        context = len(ex["prompt_ids"]) + len(ex["video_ids"])
        # Step 1: [USER_PROMPT][VIDEO] -> IGNORE, [ANSWER] -> its ids, [PAD] -> IGNORE
        batch["labels"].append(___)
        # Step 2: 1 for real tokens, 0 for padding
        batch["attention_mask"].append(___)
    return batch

batch = collate([
    {"prompt_ids": [5, 6, 7], "video_ids": [800] * 6, "answer_ids": [31, 32, 33]},
    {"prompt_ids": [5, 9], "video_ids": [800] * 4, "answer_ids": [41]},
])

# Step 3: the old collator used labels = input_ids. How many positions did it train on that it should not have?
wrongly_trained = ___
print(batch["labels"])
print(batch["attention_mask"], "| wrongly trained:", wrongly_trained)
''',
        answers=(
            '[IGNORE] * context + ex["answer_ids"] + [IGNORE] * pad',
            "[1] * len(seq) + [0] * pad",
            'sum(label == IGNORE for row in batch["labels"] for label in row)',
        ),
        checks=(
            check("batch['labels']", [[-100] * 9 + [31, 32, 33], [-100] * 6 + [41] + [-100] * 5],
                  "Blank 1: `[IGNORE] * context` + the answer ids + `[IGNORE] * pad`.",
                  "الفراغ 1: `[IGNORE] * context` + معرّفات الجواب + `[IGNORE] * pad`."),
            check("batch['attention_mask']", [[1] * 12, [1] * 7 + [0] * 5],
                  "Blank 2: ones for the real sequence, zeros for the padding.", "الفراغ 2: آحاد للتسلسل الحقيقي وأصفار للحشو."),
            check("wrongly_trained", 20, "Blank 3: count every position the correct labels mark as IGNORE.",
                  "الفراغ 3: عُدّ كل موضع تضع عليه التسميات الصحيحة IGNORE."),
        ),
        hints=(
            ("List multiplication builds runs of the same value: `[IGNORE] * 3`.", "يبني ضرب القوائم سلاسل من القيمة نفسها: `[IGNORE] * 3`."),
            ("The attention mask and the labels both mark padding, but with different values.", "يشير قناع الانتباه والتسميات كلاهما إلى الحشو، لكن بقيم مختلفة."),
            ("Every IGNORE in the fixed labels was a real training target in the buggy version.", "كل IGNORE في التسميات المصحَّحة كان هدف تدريب حقيقيًا في النسخة الخاطئة."),
        ),
        success=("Correct! Only the 4 answer tokens are trained now; the buggy `labels = input_ids` also trained the model to reproduce 20 prompt, video and padding positions.",
                 "صحيح! أصبحت رموز الجواب الأربعة وحدها مُدرَّبة؛ أما `labels = input_ids` الخاطئة فدرّبت النموذج أيضًا على إعادة إنتاج 20 موضعًا من الموجّه والفيديو والحشو."),
        reflect=("Why does `labels = input_ids` conflict with an answer-only training objective?",
                 "لماذا يتعارض `labels = input_ids` مع هدف تدريب يقتصر على الجواب؟"),
    ),
}
