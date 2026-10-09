"""COURSE-004 Applied NLP with Transformers: guided implementation exercises."""
from . import Guided, check

EXERCISES = {
    "COURSE-004.M02.L01.EX01": Guided(
        goal=("Rebuild what a DistilBERT tokenizer returns - subword tokens, special tokens, input IDs, padding and the attention mask.",
              "أعد بناء ما يعيده مُقسِّم DistilBERT: الرموز الفرعية والرموز الخاصة ومعرّفات الإدخال والحشو وقناع الانتباه."),
        steps=(
            ("Wrap a sentence's tokens in `[CLS]` and `[SEP]`.", "أحِط رموز الجملة بـ `[CLS]` و`[SEP]`."),
            ("Pad every sequence with `[PAD]` to the longest length.", "احشُ كل تسلسل بـ `[PAD]` حتى أطول طول."),
            ("Build the attention mask: 1 for real tokens, 0 for padding.", "ابنِ قناع الانتباه: 1 للرموز الحقيقية و0 للحشو."),
            ("Convert the tokens to their IDs.", "حوّل الرموز إلى معرّفاتها."),
        ),
        starter='''# A tiny slice of the distilbert-base-uncased vocabulary
vocab = {"[PAD]": 0, "[UNK]": 100, "[CLS]": 101, "[SEP]": 102, "the": 1996, "movie": 3185,
         "was": 2001, "un": 4895, "##believ": 22042, "##able": 3085, "good": 2204}

def wordpiece(word):
    """Greedy longest-match WordPiece: pieces after the first start with ##."""
    pieces, start = [], 0
    while start < len(word):
        for end in range(len(word), start, -1):
            piece = word[start:end] if start == 0 else "##" + word[start:end]
            if piece in vocab:
                pieces.append(piece)
                start = end
                break
        else:
            return ["[UNK]"]
    return pieces

sentences = ["The movie was unbelievable", "Good"]

def tokenize(sentence):
    tokens = [piece for word in sentence.lower().split() for piece in wordpiece(word)]
    # Step 1: add the special tokens DistilBERT expects around every sequence
    return ___

batch_tokens = [tokenize(s) for s in sentences]
max_len = max(len(tokens) for tokens in batch_tokens)

# Step 2: pad every sequence to max_len with "[PAD]"   (tokenizer(..., padding=True))
padded = [___ for tokens in batch_tokens]

# Step 3: 1 for a real token, 0 for padding
attention_mask = [___ for tokens in padded]

# Step 4: token -> id                                      (tokenizer.convert_tokens_to_ids)
input_ids = [___ for tokens in padded]

for tokens, ids, mask in zip(padded, input_ids, attention_mask):
    print(tokens)
    print(ids, mask)
''',
        answers=(
            '["[CLS]"] + tokens + ["[SEP]"]',
            'tokens + ["[PAD]"] * (max_len - len(tokens))',
            '[0 if token == "[PAD]" else 1 for token in tokens]',
            "[vocab[token] for token in tokens]",
        ),
        checks=(
            check("batch_tokens[0]", ["[CLS]", "the", "movie", "was", "un", "##believ", "##able", "[SEP]"],
                  "Blank 1: return `[\"[CLS]\"] + tokens + [\"[SEP]\"]`.", "الفراغ 1: أعد `[\"[CLS]\"] + tokens + [\"[SEP]\"]`."),
            check("padded[1]", ["[CLS]", "good", "[SEP]", "[PAD]", "[PAD]", "[PAD]", "[PAD]", "[PAD]"],
                  "Blank 2: append `max_len - len(tokens)` copies of \"[PAD]\".",
                  "الفراغ 2: أضف `max_len - len(tokens)` نسخة من \"[PAD]\"."),
            check("attention_mask", [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 0, 0, 0, 0, 0]],
                  "Blank 3: the mask is 0 exactly where the token is \"[PAD]\", 1 elsewhere.",
                  "الفراغ 3: يكون القناع 0 تمامًا حيث يكون الرمز \"[PAD]\"، و1 في غير ذلك."),
            check("input_ids[1]", [101, 2204, 102, 0, 0, 0, 0, 0],
                  "Blank 4: look every token up in `vocab`.", "الفراغ 4: ابحث عن كل رمز في `vocab`."),
        ),
        hints=(
            ("DistilBERT sequences start with [CLS] and end with [SEP].", "تبدأ تسلسلات DistilBERT بـ [CLS] وتنتهي بـ [SEP]."),
            ("A list times a number repeats it: `[\"[PAD]\"] * 3`.", "ضرب القائمة في عدد يكرّرها: `[\"[PAD]\"] * 3`."),
            ("The attention mask tells the model which positions to ignore; padding carries no information.",
             "يخبر قناع الانتباه النموذج بالمواضع التي يتجاهلها؛ فالحشو لا يحمل أي معلومة."),
        ),
        success=("Correct! 'unbelievable' became `un`, `##believ`, `##able`, both sequences have the same length, and the mask hides the padding from attention.",
                 "صحيح! أصبحت «unbelievable» الرموز `un` و`##believ` و`##able`، وصار للتسلسلين الطول نفسه، ويخفي القناع الحشو عن الانتباه."),
        expected=(
            "`AutoTokenizer.from_pretrained(\"distilbert-base-uncased\")(sentences, padding=True)` returns these same `input_ids` and `attention_mask`; building them by hand shows what each part means.",
            "تعيد `AutoTokenizer.from_pretrained(\"distilbert-base-uncased\")(sentences, padding=True)` القيمتين `input_ids` و`attention_mask` نفسيهما؛ وبناؤهما يدويًا يوضح معنى كل جزء.",
        ),
        reflect=("Why would loading an unrelated tokenizer with this model be dangerous, even if it produced valid-looking IDs?",
                 "لماذا يكون تحميل مُقسِّم غير مرتبط بهذا النموذج خطيرًا، حتى لو أنتج معرّفات تبدو صالحة؟"),
    ),
    "COURSE-004.M01.L05.EX01": Guided(
        goal=("Build the lead-3 summarization baseline and measure what it keeps compared with a human summary.",
              "ابنِ خط الأساس للتلخيص المعتمد على الجمل الثلاث الأولى (lead-3)، وقِس ما يحتفظ به مقارنةً بملخص بشري."),
        steps=(
            ("Split the article into sentences.", "قسّم المقال إلى جمل."),
            ("Join the first three sentences into the baseline summary.", "اجمع الجمل الثلاث الأولى في ملخص خط الأساس."),
            ("List which key facts the baseline keeps.", "اذكر الحقائق الأساسية التي يحتفظ بها خط الأساس."),
            ("Compute ROUGE-1 recall: shared words ÷ reference words.", "احسب ROUGE-1 recall: الكلمات المشتركة ÷ كلمات الملخص المرجعي."),
        ),
        starter='''import re

article = ("Heavy rain flooded the river town of Elmsford on Tuesday. "
           "Emergency crews moved 300 families to two school shelters. "
           "The main bridge into town was closed after cracks appeared. "
           "Officials said the water should fall by Friday. "
           "Volunteers collected food and blankets at the town hall. "
           "The mayor thanked the crews for working through the night.")
human_summary = ("A flood in Elmsford forced 300 families into shelters and closed the main bridge. "
                 "Officials expect the water to fall by Friday.")

# Step 1: split after every ., ! or ? followed by whitespace
sentences = ___

# Step 2: the lead-3 baseline
baseline = ___

# Step 3: which key facts survive in the baseline?
key_facts = ["300 families", "shelters", "bridge", "Friday"]
kept_by_baseline = ___

# Step 4: ROUGE-1 recall = |shared words| / |reference words|
def rouge1_recall(candidate, reference):
    candidate_words = set(re.findall(r"[a-z0-9]+", candidate.lower()))
    reference_words = set(re.findall(r"[a-z0-9]+", reference.lower()))
    return ___

print(len(sentences), "sentences")
print("baseline:", baseline)
print("kept:", kept_by_baseline, "| ROUGE-1 recall:", round(rouge1_recall(baseline, human_summary), 3))
''',
        answers=(
            r're.split(r"(?<=[.!?])\s+", article.strip())',
            '" ".join(sentences[:3])',
            "[fact for fact in key_facts if fact in baseline]",
            "len(candidate_words & reference_words) / len(reference_words)",
        ),
        checks=(
            check("len(sentences) == 6 and sentences[3] == 'Officials said the water should fall by Friday.'", True,
                  "Blank 1: split with the regular expression `(?<=[.!?])\\s+` so each sentence keeps its full stop.",
                  "الفراغ 1: قسّم بالتعبير النمطي `(?<=[.!?])\\s+` لتحتفظ كل جملة بنقطتها."),
            check("baseline == ' '.join(sentences[:3])", True,
                  "Blank 2: join the first three sentences with spaces.", "الفراغ 2: اجمع الجمل الثلاث الأولى مع مسافات بينها."),
            check("kept_by_baseline", ["300 families", "shelters", "bridge"],
                  "Blank 3: keep each fact that appears in `baseline`, in the order of `key_facts`.",
                  "الفراغ 3: احتفظ بكل حقيقة تظهر في `baseline`، بترتيب `key_facts`."),
            check("[round(rouge1_recall('the cat sat', 'the cat ran'), 4), rouge1_recall('a b', 'a b')]", [0.6667, 1.0],
                  "Blank 4: divide the size of the shared word set by the size of the reference word set.",
                  "الفراغ 4: اقسم حجم مجموعة الكلمات المشتركة على حجم مجموعة كلمات المرجع."),
        ),
        hints=(
            ("A look-behind `(?<=[.!?])` splits after the punctuation without removing it.", "يقسم الاستباق الخلفي `(?<=[.!?])` بعد علامة الترقيم دون حذفها."),
            ("`sentences[:3]` are the first three sentences; `\" \".join(...)` glues them together.", "تمثّل `sentences[:3]` الجمل الثلاث الأولى، ويلصقها `\" \".join(...)` معًا."),
            ("`set_a & set_b` is the intersection of two sets.", "يعطي `set_a & set_b` تقاطع مجموعتين."),
        ),
        success=("Correct! Lead-3 keeps three of the four key facts but misses 'Friday', which only appears in sentence four - a cheap, strong baseline that still has blind spots.",
                 "صحيح! يحتفظ lead-3 بثلاث من الحقائق الأربع لكنه يفوّت «Friday» التي تظهر في الجملة الرابعة فقط - خط أساس رخيص وقوي، لكن له نقاط عمياء."),
        reflect=("Write your own two-sentence abstractive summary. When would the first-three-sentence baseline fail badly, and why keep it in evaluations anyway?",
                 "اكتب ملخصًا تجريديًا خاصًا بك من جملتين. متى يفشل خط الأساس المعتمد على الجمل الثلاث الأولى فشلًا كبيرًا؟ ولماذا نحتفظ به في التقييم مع ذلك؟"),
    ),
    "COURSE-004.M01.L07.EX01": Guided(
        goal=("Find the start and end token positions of an extractive answer and reject impossible spans.",
              "حدّد موضعي رمز البداية والنهاية لإجابة مستخرجة، وارفض المقاطع المستحيلة."),
        steps=(
            ("Find where the context begins in the `[CLS] question [SEP] context [SEP]` sequence.", "حدّد أين يبدأ السياق في التسلسل `[CLS] question [SEP] context [SEP]`."),
            ("Compute the answer's start token index.", "احسب فهرس رمز بداية الإجابة."),
            ("Compute the answer's end token index (inclusive).", "احسب فهرس رمز نهاية الإجابة (شاملًا)."),
            ("Write the rule that accepts only valid spans.", "اكتب القاعدة التي لا تقبل إلا المقاطع الصالحة."),
        ),
        starter='''question = "How long does the battery last?"
context = "The battery lasts around ten hours on one charge."
answer = "around ten hours"

q_tokens = question.lower().replace("?", "").split()
c_tokens = context.lower().replace(".", "").split()
tokens = ["[CLS]"] + q_tokens + ["[SEP]"] + c_tokens + ["[SEP]"]

# Step 1: index of the first context token inside `tokens`
context_start = ___

# Step 2: start index of the answer inside `tokens`
answer_words = answer.split()
start = ___
# Step 3: end index (inclusive)
end = ___

# Step 4: a valid span lies inside the context, has start <= end, and is not too long
def is_valid_span(start, end, max_answer_length=30):
    return ___

print(tokens)
print("span:", start, end, tokens[start:end + 1])
''',
        answers=(
            "len(q_tokens) + 2",
            "context_start + c_tokens.index(answer_words[0])",
            "start + len(answer_words) - 1",
            "context_start <= start <= end < len(tokens) - 1 and end - start + 1 <= max_answer_length",
        ),
        checks=(
            check("context_start", 8, "Blank 1: skip [CLS], the 6 question tokens and the first [SEP].",
                  "الفراغ 1: تجاوز [CLS] ورموز السؤال الستة و[SEP] الأول."),
            check("[start, end, tokens[start:end + 1]]", [11, 13, ["around", "ten", "hours"]],
                  "Blanks 2-3: offset the answer's position in `c_tokens` by `context_start`; the end is start + length - 1.",
                  "الفراغان 2 و3: أزِح موضع الإجابة داخل `c_tokens` بمقدار `context_start`؛ والنهاية = البداية + الطول − 1."),
            check("[is_valid_span(11, 13), is_valid_span(2, 3), is_valid_span(13, 11), is_valid_span(16, 17), is_valid_span(8, 16, max_answer_length=3)]",
                  [True, False, False, False, False],
                  "Blank 4: start must be at or after `context_start`, start <= end, end before the final [SEP], and length within the limit.",
                  "الفراغ 4: يجب أن تكون البداية عند `context_start` أو بعده، والبداية <= النهاية، والنهاية قبل [SEP] الأخير، والطول ضمن الحد."),
        ),
        hints=(
            ("Count the tokens before the context: one [CLS], the question tokens, one [SEP].", "عُدّ الرموز قبل السياق: [CLS] واحد، ورموز السؤال، و[SEP] واحد."),
            ("`c_tokens.index(word)` gives the word's position inside the context only.", "تعطي `c_tokens.index(word)` موضع الكلمة داخل السياق فقط."),
            ("Python allows chained comparisons such as `a <= b <= c < d`.", "تسمح Python بالمقارنات المتسلسلة مثل `a <= b <= c < d`."),
        ),
        success=("Correct! The answer is tokens 11-13, and the postprocessor rejects spans in the question, reversed spans, spans on special tokens and over-long spans.",
                 "صحيح! الإجابة هي الرموز 11 إلى 13، وترفض المعالجة اللاحقة المقاطع الواقعة في السؤال والمقاطع المعكوسة والمقاطع على الرموز الخاصة والمقاطع الطويلة جدًا."),
        reflect=("Why would an answer span selected from the question itself be invalid, even if its words look right?",
                 "لماذا يُعدّ مقطع الإجابة المختار من السؤال نفسه غير صالح، حتى لو بدت كلماته صحيحة؟"),
    ),
}
