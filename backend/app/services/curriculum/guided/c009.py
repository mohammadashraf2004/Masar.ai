"""COURSE-009 Enterprise RAG Engineering: guided implementation exercises."""
from . import Guided, check

EXERCISES = {
    "COURSE-009.M01.L02.EX09": Guided(
        goal=("Implement a fixed-length chunker with overlap and a sentence-aware chunker, and compare their boundaries.",
              "نفّذ مُقسِّمًا بطول ثابت مع تداخل، ومُقسِّمًا يراعي الجمل، وقارن حدود المقاطع في كلٍّ منهما."),
        steps=(
            ("Compute the step between fixed chunks from the size and overlap.", "احسب الخطوة بين المقاطع الثابتة من الحجم والتداخل."),
            ("End a sentence only when the word is not a known abbreviation.", "أنهِ الجملة فقط عندما لا تكون الكلمة اختصارًا معروفًا."),
            ("Compare with a naive split on \". \".", "قارن بالتقسيم الساذج على \". \"."),
        ),
        starter='''text = ("Dr. Smith joined Acme Inc. in 2019. She leads the RAG team. "
        "The team ships weekly, e.g. new retrievers. Results improved by 12.5% last year.")

# Step 1: chunks of `size` characters; each starts (size - overlap) characters after the previous one
def fixed_chunks(text, size=40, overlap=10):
    step = ___
    return [text[start:start + size] for start in range(0, len(text), step)]

ABBREVIATIONS = {"dr.", "mr.", "mrs.", "inc.", "e.g.", "i.e."}

# Step 2: close a sentence at ., ! or ? - unless the word is an abbreviation
def sentence_chunks(text):
    sentences, current = [], []
    for word in text.split():
        current.append(word)
        if word.endswith((".", "!", "?")) and ___:
            sentences.append(" ".join(current))
            current = []
    if current:
        sentences.append(" ".join(current))
    return sentences

fixed = fixed_chunks(text)
sentences = sentence_chunks(text)
# Step 3: the naive alternative - split wherever ". " appears
naive = ___

for chunk in fixed:
    print(repr(chunk))
print(sentences)
print(len(naive), "naive pieces:", naive)
''',
        answers=("size - overlap", "word.lower() not in ABBREVIATIONS", 'text.split(". ")'),
        checks=(
            check("[len(fixed), fixed[0][-10:] == fixed[1][:10]]", [5, True],
                  "Blank 1: the step is `size - overlap`, so the last 10 characters of one chunk start the next.",
                  "الفراغ 1: الخطوة هي `size - overlap`، فتبدأ آخر 10 أحرف من مقطع المقطعَ التالي."),
            check("sentences", ["Dr. Smith joined Acme Inc. in 2019.", "She leads the RAG team.",
                                "The team ships weekly, e.g. new retrievers.", "Results improved by 12.5% last year."],
                  "Blank 2: only end the sentence when `word.lower()` is not in `ABBREVIATIONS`.",
                  "الفراغ 2: لا تُنهِ الجملة إلا عندما لا تكون `word.lower()` ضمن `ABBREVIATIONS`."),
            check("len(naive)", 7, "Blank 3: use `text.split(\". \")` to see how abbreviations break the naive split.",
                  "الفراغ 3: استخدم `text.split(\". \")` لترى كيف تكسر الاختصاراتُ التقسيمَ الساذج."),
        ),
        hints=(
            ("If chunks are 40 long and share 10 characters, each new chunk starts 30 characters later.", "إذا كان طول المقاطع 40 وتشترك في 10 أحرف، فإن كل مقطع جديد يبدأ بعد 30 حرفًا."),
            ("Compare the lowercase word with the set: `word.lower() not in ABBREVIATIONS`.", "قارن الكلمة بالأحرف الصغيرة مع المجموعة: `word.lower() not in ABBREVIATIONS`."),
            ("`str.split(sep)` cuts at every occurrence of `sep`.", "يقطع `str.split(sep)` عند كل ظهور لـ `sep`."),
        ),
        success=("Correct! Fixed chunks cut through words and sentences, the naive split breaks after 'Dr.' and 'Inc.', and the sentence-aware chunker returns four clean sentences.",
                 "صحيح! تقطع المقاطع الثابتة الكلمات والجمل، ويكسر التقسيم الساذج النص بعد «Dr.» و«Inc.»، بينما يعيد المُقسِّم المراعي للجمل أربع جمل نظيفة."),
        expected=(
            "The lesson uses an NLP sentencizer such as spaCy; this abbreviation-aware splitter shows the same idea and runs in the sandbox.",
            "يستخدم الدرس أداة تقسيم جمل مثل spaCy؛ ويوضح هذا المُقسِّم المراعي للاختصارات الفكرة نفسها ويعمل داخل بيئة التدريب.",
        ),
    ),
    "COURSE-009.M01.L02.EX14": Guided(
        goal=("Filter report chunks by company and period before ranking them by vector similarity.",
              "رشّح مقاطع التقارير حسب الشركة والفترة قبل ترتيبها حسب التشابه المتجهي."),
        steps=(
            ("Keep only the chunks of the requested company.", "احتفظ فقط بمقاطع الشركة المطلوبة."),
            ("Keep only fiscal years 2021 to 2023.", "احتفظ فقط بالسنوات المالية من 2021 إلى 2023."),
            ("Rank by similarity, highest first.", "رتّب حسب التشابه، الأعلى أولًا."),
            ("Return the top 3 chunks.", "أعد أفضل 3 مقاطع."),
        ),
        starter='''-- report_chunks(chunk_id, company, fiscal_year, e0, e1, e2)
-- e0..e2 is a tiny embedding; the query embedding is (0.9, 0.1, 0.4)
SELECT chunk_id,
       ROUND(e0 * 0.9 + e1 * 0.1 + e2 * 0.4, 3) AS similarity
FROM report_chunks
WHERE company = ___
  AND fiscal_year ___
ORDER BY ___ DESC
LIMIT ___;
''',
        answers=("'Acme'", "BETWEEN 2021 AND 2023", "similarity", "3"),
        alternatives={
            2: (">= 2021 AND fiscal_year <= 2023", "IN (2021, 2022, 2023)"),
            3: ("ROUND(e0 * 0.9 + e1 * 0.1 + e2 * 0.4, 3)", "e0 * 0.9 + e1 * 0.1 + e2 * 0.4", "2"),
        },
        blanks=(
            ("compare `company` with the string `'Acme'`.", "قارن `company` بالنص `'Acme'`."),
            ("use `BETWEEN 2021 AND 2023` (both ends included).", "استخدم `BETWEEN 2021 AND 2023` (الطرفان مشمولان)."),
            ("order by the `similarity` alias.", "رتّب حسب الاسم المستعار `similarity`."),
            ("return three rows: `LIMIT 3`.", "أعد ثلاثة صفوف: `LIMIT 3`."),
        ),
        sql_setup='''CREATE TABLE report_chunks(chunk_id TEXT, company TEXT, fiscal_year INTEGER, e0 REAL, e1 REAL, e2 REAL);
INSERT INTO report_chunks VALUES
('acme-2019-1','Acme',2019,0.95,0.10,0.40),
('acme-2021-1','Acme',2021,0.80,0.20,0.30),
('acme-2022-1','Acme',2022,0.90,0.05,0.50),
('acme-2022-2','Acme',2022,0.10,0.90,0.10),
('acme-2023-1','Acme',2023,0.70,0.10,0.60),
('globex-2022-1','Globex',2022,0.99,0.10,0.45),
('globex-2023-1','Globex',2023,0.85,0.15,0.40);''',
        sql_columns=("chunk_id", "similarity"),
        sql_rows=(("acme-2022-1", 1.015), ("acme-2023-1", 0.88), ("acme-2021-1", 0.86)),
        hints=(
            ("Text values in SQL use single quotes.", "تُكتب القيم النصية في SQL بين علامتي اقتباس مفردتين."),
            ("`BETWEEN low AND high` includes both ends.", "يشمل `BETWEEN low AND high` الطرفين."),
            ("You can order by a column alias defined in SELECT.", "يمكنك الترتيب حسب اسم مستعار لعمود معرَّف في SELECT."),
        ),
        success=("Correct! Exact filters remove other companies and years first, so the similarity ranking only competes among the chunks that can actually answer the question - faster and more relevant.",
                 "صحيح! تحذف المرشحات الدقيقة الشركات والسنوات الأخرى أولًا، فلا يتنافس في ترتيب التشابه إلا المقاطع القادرة فعلًا على الإجابة - أسرع وأكثر صلة."),
        expected=(
            "SQLite has no vector type, so similarity is the dot product written out; in pgvector you would write `ORDER BY embedding <=> :query` after the same WHERE clause.",
            "لا يملك SQLite نوعًا للمتجهات، لذا يُكتب التشابه بوصفه ضربًا نقطيًا صريحًا؛ وفي pgvector تكتب `ORDER BY embedding <=> :query` بعد عبارة WHERE نفسها.",
        ),
        reflect=("Without the filter, why could a very similar chunk from the wrong company or year still reach the top 3?",
                 "لماذا قد يصل مقطع شديد التشابه من شركة أو سنة خاطئة إلى المراكز الثلاثة الأولى دون المرشح؟"),
        language="sql",
    ),
    "COURSE-009.M01.L09.EX04": Guided(
        goal=("Write a director-movie fact as triples and a SPARQL pattern that returns the director's name.",
              "اكتب حقيقة المخرج والفيلم بصيغة ثلاثيات، ونمط SPARQL يعيد اسم المخرج."),
        steps=(
            ("Complete the triple: Nolan directed Inception.", "أكمل الثلاثية: نولان أخرج Inception."),
            ("Select the variable `?name`.", "اختر المتغير `?name`."),
            ("Match a person who directed a movie.", "طابق شخصًا أخرج فيلمًا."),
            ("Bind that person's name to `?name`.", "اربط اسم ذلك الشخص بـ `?name`."),
        ),
        starter='''PREFIX ex: <http://example.org/>

# Data, as subject - predicate - object triples:
#   ex:nolan      ex:name      "Christopher Nolan" .
#   ex:inception  ex:title     "Inception" .
# Step 1: the triple "Nolan directed Inception"
#   ex:nolan      ex:directed  ___ .

# Step 2: return the director's name
SELECT ___ WHERE {
  # Step 3: a person who directed a movie
  ?person ___ ?movie .
  ?movie ex:title "Inception" .
  # Step 4: bind the person's name
  ?person ex:name ___ .
}
''',
        answers=("ex:inception", "?name", "ex:directed", "?name"),
        alternatives={2: ("$name",), 4: ("$name",)},
        blanks=(
            ("the object of the triple is the movie resource `ex:inception`.", "مفعول الثلاثية هو مورد الفيلم `ex:inception`."),
            ("select the output variable `?name`.", "اختر متغير الإخراج `?name`."),
            ("the predicate linking a person to a movie is `ex:directed`.", "المسند الذي يربط الشخص بالفيلم هو `ex:directed`."),
            ("bind the name to the same `?name` you selected.", "اربط الاسم بالمتغير `?name` نفسه الذي اخترته."),
        ),
        hints=(
            ("A triple is subject, predicate, object - Nolan, directed, the Inception resource.", "الثلاثية هي فاعل ومسند ومفعول - نولان، أخرج، مورد Inception."),
            ("Variables start with `?`; SELECT lists the ones you want back.", "تبدأ المتغيرات بـ `?`، ويسرد SELECT المتغيرات المطلوب إعادتها."),
            ("The same variable in two patterns joins them - that is how `?person` connects the movie to the name.", "المتغير نفسه في نمطين يربطهما - وهكذا يصل `?person` الفيلم بالاسم."),
        ),
        success=("Correct! `?movie` joins the title pattern to the directed pattern and `?person` joins it to the name, so the query returns \"Christopher Nolan\".",
                 "صحيح! يربط `?movie` نمط العنوان بنمط الإخراج، ويربطه `?person` بالاسم، فيعيد الاستعلام \"Christopher Nolan\"."),
        expected=(
            "SPARQL is checked by reading it: each completed line is compared with the expected pattern, ignoring extra spaces.",
            "يُفحص SPARQL بقراءته: يُقارن كل سطر مكتمل بالنمط المتوقع مع تجاهل المسافات الزائدة.",
        ),
        language="sparql",
    ),
}
