"""COURSE-016 Machine Learning Systems and MLOps Engineering: guided exercises.

Service and function handlers run in the sandbox with stub cloud APIs;
Dockerfiles, Kubernetes manifests and the Click CLI are checked by reading them.
"""
from . import Guided, check

READ_NOTE = (
    "Configuration and CLI code is checked by reading it: each completed part is compared with the expected answer. Run it locally to see the result.",
    "يُفحص كود الإعداد وواجهة سطر الأوامر بقراءته: يُقارن كل جزء مكتمل بالإجابة المتوقعة. شغّله محليًا لترى النتيجة.",
)
STUB_NOTE = (
    "Stub functions stand in for the cloud services, so the handler's validation and responses run and are checked for real.",
    "تحل دوال بديلة محل الخدمات السحابية، فيعمل التحقق والاستجابات في المعالج ويُفحصان فعليًا.",
)

EXERCISES = {
    "COURSE-016.M04.L01.EX04": Guided(
        goal=("Evaluate a disease classifier on imbalanced data and see why 94% accuracy can hide a model that misses one sick patient in three.",
              "قيّم مصنّف أمراض على بيانات غير متوازنة، ولاحظ كيف تخفي دقة 94% نموذجًا يفوّت مريضًا من كل ثلاثة."),
        steps=(
            ("Compute precision.", "احسب الدقة النوعية (precision)."),
            ("Compute recall.", "احسب الاستدعاء (recall)."),
            ("Compute F1 from precision and recall.", "احسب F1 من precision وrecall."),
            ("Compute accuracy and compare it with recall.", "احسب accuracy وقارنها بـ recall."),
            ("Predict what a lower decision threshold does.", "توقّع أثر خفض عتبة القرار."),
        ),
        starter='''# Confusion matrix for 1,000 patients; only 120 actually have the disease.
tp, fp, fn, tn = 80, 20, 40, 860

# Step 1: of the patients flagged as sick, the share that really are
precision = ___
# Step 2: of the patients who really are sick, the share the model caught
recall = ___
# Step 3: the harmonic mean of precision and recall
f1 = ___
# Step 4: the share of all predictions that are right
accuracy = ___
print(f"precision={precision:.2f} recall={recall:.2f} f1={f1:.2f} accuracy={accuracy:.2f}")

# Step 5: a lower threshold flags more patients as sick, so more real cases are caught.
# Do false positives go "up" or "down"?
lower_threshold = {"recall": "up", "false_positives": ___}
''',
        answers=("tp / (tp + fp)", "tp / (tp + fn)", "2 * precision * recall / (precision + recall)",
                 "(tp + tn) / (tp + fp + fn + tn)", '"up"'),
        checks=(
            check("round(precision, 4)", 0.8, "Blank 1: `tp / (tp + fp)`.", "الفراغ 1: `tp / (tp + fp)`."),
            check("round(recall, 4)", 0.6667, "Blank 2: `tp / (tp + fn)`.", "الفراغ 2: `tp / (tp + fn)`."),
            check("round(f1, 4)", 0.7273, "Blank 3: `2 * precision * recall / (precision + recall)`.", "الفراغ 3: `2 * precision * recall / (precision + recall)`."),
            check("round(accuracy, 4)", 0.94, "Blank 4: correct predictions `(tp + tn)` over all four counts.", "الفراغ 4: التنبؤات الصحيحة `(tp + tn)` على مجموع العدادات الأربعة."),
            check("lower_threshold", {"recall": "up", "false_positives": "up"},
                  "Blank 5: flagging more patients also flags more healthy ones, so false positives go \"up\".",
                  "الفراغ 5: الإشارة إلى مرضى أكثر تشير أيضًا إلى أصحاء أكثر، فترتفع الإيجابيات الخاطئة \"up\"."),
        ),
        hints=(
            ("Precision divides by everything the model flagged (tp + fp); recall divides by everything that was really positive (tp + fn).",
             "تقسم precision على كل ما أشار إليه النموذج (tp + fp)، ويقسم recall على كل ما كان إيجابيًا فعلًا (tp + fn)."),
            ("F1 is 2·P·R / (P + R).", "F1 تساوي 2·P·R / (P + R)."),
            ("Accuracy is high because 860 healthy patients are easy to get right.", "accuracy مرتفعة لأن 860 مريضًا سليمًا يسهل تصنيفهم صحيحًا."),
        ),
        success=("Correct! Accuracy is 0.94 while recall is only 0.67: on imbalanced data, report precision, recall and F1 for the class that matters.",
                 "صحيح! accuracy تساوي 0.94 بينما recall تساوي 0.67 فقط: في البيانات غير المتوازنة، أبلغ عن precision وrecall وF1 للفئة المهمة."),
        reflect=("For a disease screen, would you lower the threshold anyway? What does a false positive cost compared with a false negative?",
                 "في فحص مرضي، هل ستخفض العتبة رغم ذلك؟ وما كلفة الإيجابي الخاطئ مقارنة بالسلبي الخاطئ؟"),
    ),
    "COURSE-016.M12.L01.EX02": Guided(
        goal=("Replace brittle prints with logging that tells a remote operator which file was processed, how it went, and the full traceback when it fails.",
              "استبدل أوامر الطباعة الهشّة بتسجيل يخبر المشغّل البعيد بالملف الذي عولج، وكيف سارت المعالجة، وبالتتبع الكامل عند الفشل."),
        steps=(
            ("Show DEBUG messages too.", "اعرض رسائل DEBUG أيضًا."),
            ("Create the named application logger `csv_processor`.", "أنشئ مسجّل التطبيق المسمّى `csv_processor`."),
            ("Log the file being processed at DEBUG.", "سجّل الملف قيد المعالجة بمستوى DEBUG."),
            ("Log normal completion at INFO.", "سجّل الإكمال العادي بمستوى INFO."),
            ("Log failures with the traceback.", "سجّل حالات الفشل مع التتبع."),
        ),
        starter='''import logging
import pandas as pd

# One readable line per event: time, level, which component, what happened.
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
# Step 1: the lowest level to show - DEBUG includes everything
logging.basicConfig(level=___, format=LOG_FORMAT)
# Step 2: a named logger instead of the anonymous root logger
logger = ___

def process_csv(path):
    # Step 3: which file is being processed - detail for debugging
    ___("Processing CSV file: %s", path)
    try:
        rows = pd.read_csv(path)
        # Step 4: normal completion
        ___("Processed %s rows from %s", len(rows), path)
        return rows
    except Exception:
        # Step 5: an ERROR record that also keeps the traceback
        ___("Failed to process CSV file: %s", path)
        raise

# process_csv("orders.csv")   ->  2026-10-09 10:15:02,114 INFO csv_processor Processed 120 rows from orders.csv
''',
        answers=("logging.DEBUG", 'logging.getLogger("csv_processor")', "logger.debug", "logger.info", "logger.exception"),
        alternatives={1: ('"DEBUG"', "10")},
        blanks=(
            ("`logging.DEBUG`.", "`logging.DEBUG`."),
            ("`logging.getLogger(\"csv_processor\")`.", "`logging.getLogger(\"csv_processor\")`."),
            ("`logger.debug`.", "`logger.debug`."),
            ("`logger.info`.", "`logger.info`."),
            ("`logger.exception` - it logs at ERROR and keeps the traceback.", "`logger.exception` - يسجّل بمستوى ERROR ويحتفظ بالتتبع."),
        ),
        hints=(
            ("`logging.getLogger(name)` returns the same named logger everywhere in the program.", "تعيد `logging.getLogger(name)` المسجّل المسمّى نفسه في كل مكان من البرنامج."),
            ("Each blank in `process_csv` is a logger method: debug, info or exception.", "كل فراغ في `process_csv` تابع من توابع المسجّل: debug أو info أو exception."),
            ("`logger.exception` logs at ERROR and attaches the current traceback; `logger.error` alone does not.", "يسجّل `logger.exception` بمستوى ERROR ويرفق التتبع الحالي، أما `logger.error` وحده فلا."),
        ),
        success=("Correct! A remote operator now sees which file failed, when, in which component, and the full traceback - instead of a bare 'failed'.",
                 "صحيح! يرى المشغّل البعيد الآن الملف الذي فشل، ومتى، وفي أي مكوّن، والتتبع الكامل - بدل كلمة «فشل» المجرّدة."),
        expected=READ_NOTE,
        reflect=("Why is this better for a remote pipeline than `print('failed')`?", "لماذا هذا أفضل لخط بيانات بعيد من `print('failed')`؟"),
    ),
    "COURSE-016.M16.L01.EX02": Guided(
        goal=("Write the three checks of a CSV linter: empty columns, leftover `Unnamed` index columns, and fields broken by carriage returns.",
              "اكتب الفحوص الثلاثة لأداة فحص CSV: الأعمدة الفارغة، وأعمدة الفهرس المتبقية `Unnamed`، والحقول التي تكسرها أحرف الرجوع."),
        steps=(
            ("Return an empty list for a file without rows.", "أعد قائمة فارغة لملف بلا صفوف."),
            ("Keep the columns that are empty in every row.", "احتفظ بالأعمدة الفارغة في كل الصفوف."),
            ("Count the column names containing `Unnamed`.", "عُدّ أسماء الأعمدة التي تحتوي `Unnamed`."),
            ("Report the first carriage return with a short preview.", "أبلغ عن أول حرف رجوع مع معاينة قصيرة."),
        ),
        starter='''def zero_count_columns(rows):
    """Names of columns that have no value in any row."""
    # Step 1: no rows means nothing to report
    if not rows:
        return ___
    # Step 2: keep a column when every row's value for it is ""
    return [column for column in rows[0] if ___]

def count_unnamed_columns(fieldnames):
    """pandas writes its index as 'Unnamed: 0' when a CSV is saved and re-read."""
    # Step 3: True counts as 1 inside sum()
    return ___

def first_carriage_return(rows):
    for row in rows:
        for column, value in row.items():
            if isinstance(value, str) and "\\r" in value:
                # Step 4: where it is, plus the first 40 characters only - long fields flood the terminal
                return ___
    return None

WARNINGS = {
    "zero_count": "Column(s) {} are empty in every row - drop them or check the export.",
    "unnamed": "{} 'Unnamed' column(s) - the index was probably saved by mistake.",
    "carriage_return": "Carriage return in column '{}' - the field may break rows apart.",
}

rows = [
    {"id": "1", "notes": "", "comment": "fine"},
    {"id": "2", "notes": "", "comment": "first line\\r" + "rest of a very long pasted support ticket " * 3},
]
print(WARNINGS["zero_count"].format(zero_count_columns(rows)))
print(WARNINGS["unnamed"].format(count_unnamed_columns(["Unnamed: 0", "id", "Unnamed: 5"])))
print(first_carriage_return(rows))
''',
        answers=("[]", 'all(row.get(column, "") == "" for row in rows)', 'sum("Unnamed" in name for name in fieldnames)',
                 '{"column": column, "preview": value[:40]}'),
        checks=(
            check("zero_count_columns([])", [], "Blank 1: return `[]`.", "الفراغ 1: أعد `[]`."),
            check("zero_count_columns(rows)", ["notes"],
                  "Blank 2: `all(row.get(column, \"\") == \"\" for row in rows)`.", "الفراغ 2: `all(row.get(column, \"\") == \"\" for row in rows)`."),
            check("[count_unnamed_columns(['Unnamed: 0', 'id', 'Unnamed: 5']), count_unnamed_columns(['id'])]", [2, 0],
                  "Blank 3: `sum(\"Unnamed\" in name for name in fieldnames)`.", "الفراغ 3: `sum(\"Unnamed\" in name for name in fieldnames)`."),
            check("first_carriage_return(rows) == {'column': 'comment', 'preview': rows[1]['comment'][:40]}", True,
                  "Blank 4: return the column name and `value[:40]`.", "الفراغ 4: أعد اسم العمود و`value[:40]`."),
        ),
        hints=(
            ("`all(...)` is True only when the condition holds for every row.", "تكون `all(...)` صحيحة فقط إذا تحقق الشرط في كل الصفوف."),
            ("`sum(condition for item in items)` counts the items where the condition is True.", "تعدّ `sum(condition for item in items)` العناصر التي يتحقق فيها الشرط."),
            ("Slicing `value[:40]` keeps the warning one line long.", "يُبقي الاقتطاع `value[:40]` التحذير في سطر واحد."),
        ),
        success=("Correct! Each check returns data, not text, so the CLI can print a warning, fail a CI job or emit JSON from the same result.",
                 "صحيح! يعيد كل فحص بيانات لا نصًا، فتستطيع واجهة سطر الأوامر أن تطبع تحذيرًا أو تُفشل مهمة CI أو تُخرج JSON من النتيجة نفسها."),
        reflect=("Why should the carriage-return preview be truncated?", "لماذا يجب اقتطاع معاينة حرف الرجوع؟"),
    ),
    "COURSE-016.M11.L01.EX01": Guided(
        goal=("Package a prediction service so the container holds everything offline accuracy never tested: pinned dependencies, the model, the preprocessing code and a reachable server.",
              "اجمع خدمة التنبؤ في حاوية تحتوي كل ما لم تختبره دقة النموذج دون اتصال: التبعيات المثبّتة، والنموذج، وكود المعالجة المسبقة، وخادمًا يمكن الوصول إليه."),
        steps=(
            ("Copy the pinned requirements first.", "انسخ المتطلبات المثبّتة أولًا."),
            ("Copy the serialized model.", "انسخ النموذج المحفوظ."),
            ("Copy the preprocessing and app code.", "انسخ كود المعالجة المسبقة والتطبيق."),
            ("Bind the server to 0.0.0.0:8080.", "اربط الخادم على 0.0.0.0:8080."),
        ),
        starter='''FROM python:3.11-slim
WORKDIR /app
# Step 1: pinned versions, installed in their own cached layer
COPY ___
RUN pip install --no-cache-dir -r requirements.txt
# Step 2: the serialized model
COPY ___
# Step 3: the SAME preprocessing code used in training, plus the Flask app
COPY ___
EXPOSE 8080
# Step 4: reachable from outside the container
CMD ["gunicorn", "--bind", ___, "app:app"]
# docker build -t predict .  &&  docker run -p 8080:8080 predict
# curl -X POST localhost:8080/predict -H "Content-Type: application/json" -d '{"features": [[5.1, 3.5, 1.4, 0.2]]}'
''',
        answers=("requirements.txt .", "model.joblib .", "preprocessing.py app.py ./", '"0.0.0.0:8080"'),
        alternatives={1: ("requirements.txt ./",), 2: ("model.joblib ./",), 3: ("app.py preprocessing.py ./", "preprocessing.py app.py .")},
        blanks=(
            ("copy `requirements.txt .`.", "انسخ `requirements.txt .`."),
            ("copy `model.joblib .`.", "انسخ `model.joblib .`."),
            ("copy `preprocessing.py app.py ./`.", "انسخ `preprocessing.py app.py ./`."),
            ("bind to `\"0.0.0.0:8080\"`.", "اربط على `\"0.0.0.0:8080\"`."),
        ),
        hints=(
            ("Dependencies first, application files later - for the build cache.", "التبعيات أولًا وملفات التطبيق لاحقًا - من أجل ذاكرة البناء المؤقتة."),
            ("A model without its preprocessing code gives different predictions.", "النموذج دون كود معالجته المسبقة يعطي تنبؤات مختلفة."),
            ("127.0.0.1 inside the container is unreachable from the host.", "العنوان 127.0.0.1 داخل الحاوية لا يمكن الوصول إليه من المضيف."),
        ),
        success=("Correct! Test the app outside the container first, then again inside it: a missing file, an unpinned dependency or a wrong bind address only shows up in the second test.",
                 "صحيح! اختبر التطبيق خارج الحاوية أولًا ثم داخلها: الملف المفقود أو التبعية غير المثبّتة أو عنوان الربط الخاطئ لا يظهر إلا في الاختبار الثاني."),
        expected=READ_NOTE,
        reflect=("Name two packaging failures that offline model accuracy would never reveal.", "اذكر فشلين في التحزيم لا تكشفهما دقة النموذج دون اتصال أبدًا."),
        language="dockerfile",
    ),
    "COURSE-016.M14.L01.EX03": Guided(
        goal=("Build a scoring endpoint that tells HTTP-contract, authentication and input-schema errors apart from normal scoring.",
              "ابنِ نقطة تقييم تميّز أخطاء عقد HTTP والمصادقة ومخطط المدخلات عن التقييم العادي."),
        steps=(
            ("Reject anything but POST with 405.", "ارفض كل ما ليس POST بالرمز 405."),
            ("Reject a missing or wrong JSON content type with 415.", "ارفض نوع محتوى JSON المفقود أو الخاطئ بالرمز 415."),
            ("Reject a body without the `data` field with 422.", "ارفض الجسم الذي يخلو من الحقل `data` بالرمز 422."),
            ("Map each status code to its failure category.", "اربط كل رمز حالة بفئة الفشل الخاصة به."),
        ),
        starter='''import json

API_KEY = "secret-key"

def score(method, headers, body):
    # Step 1: the scoring route only accepts POST
    if method != "POST":
        return ___
    if headers.get("Authorization") != f"Bearer {API_KEY}":
        return 401, {"error": "invalid or missing credentials"}
    # Step 2: the body must be declared as JSON
    if ___:
        return 415, {"error": "send Content-Type: application/json"}
    payload = json.loads(body)
    # Step 3: the model needs its input field
    if ___:
        return 422, {"error": "missing field: data"}
    return 200, {"prediction": [sum(row) for row in payload["data"]]}       # stand-in model

# Step 4: which part of the system failed?
CATEGORY = ___

good = {"Authorization": "Bearer secret-key", "Content-Type": "application/json"}
cases = [
    ("GET", good, ""),
    ("POST", {"Authorization": "Bearer secret-key"}, '{"data": [[1, 2]]}'),
    ("POST", {"Authorization": "Token secret-key", "Content-Type": "application/json"}, '{"data": [[1, 2]]}'),
    ("POST", good, '{"rows": [[1, 2]]}'),
    ("POST", good, '{"data": [[1, 2], [3, 4]]}'),
]
for case in cases:
    status, response = score(*case)
    print(status, CATEGORY[status], response)
''',
        answers=('(405, {"error": "use POST"})', 'headers.get("Content-Type") != "application/json"', '"data" not in payload',
                 '{401: "authentication", 405: "HTTP contract", 415: "HTTP contract", 422: "input schema", 200: "normal scoring"}'),
        checks=(
            check("[score(*case)[0] for case in cases]", [405, 415, 401, 422, 200],
                  "Blanks 1-3: return 405 for the wrong method, 415 without the JSON content type, 422 without `data`.",
                  "الفراغات 1-3: أعد 405 للطريقة الخاطئة، و415 دون نوع محتوى JSON، و422 دون `data`."),
            check("score(*cases[-1])", [200, {"prediction": [3, 7]}], "A correct request returns a JSON prediction.", "يعيد الطلب الصحيح تنبؤًا بصيغة JSON."),
            check("[CATEGORY[s] for s in (405, 415, 401, 422, 200)]", ["HTTP contract", "HTTP contract", "authentication", "input schema", "normal scoring"],
                  "Blank 4: map 401 to authentication, 405/415 to HTTP contract, 422 to input schema, 200 to normal scoring.",
                  "الفراغ 4: اربط 401 بالمصادقة، و405/415 بعقد HTTP، و422 بمخطط المدخلات، و200 بالتقييم العادي."),
        ),
        hints=(
            ("Return a (status, body) tuple, like the other branches.", "أعد صفًّا (status, body) مثل الفروع الأخرى."),
            ("A missing header makes `headers.get(...)` return None, which is also wrong.", "يجعل غياب الترويسة `headers.get(...)` يعيد None، وهذا خطأ أيضًا."),
            ("Each status code points at one layer of the request.", "يشير كل رمز حالة إلى طبقة واحدة من الطلب."),
        ),
        success=("Correct! Each failure gets its own status code, so a client can tell 'fix your request' from 'fix your credentials' from 'the model ran' at a glance.",
                 "صحيح! لكل فشل رمز حالة خاص به، فيستطيع العميل أن يميّز بنظرة واحدة بين «أصلح طلبك» و«أصلح بيانات اعتمادك» و«عمل النموذج»."),
        expected=STUB_NOTE,
    ),
    "COURSE-016.M15.L01.EX03": Guided(
        goal=("Move a tested Flask container to Kubernetes: three replicas behind a load-balanced Service.",
              "انقل حاوية Flask مُختبَرة إلى Kubernetes: ثلاث نسخ خلف خدمة موزّعة الحمل."),
        steps=(
            ("Run three replicas.", "شغّل ثلاث نسخ."),
            ("Use the image you tested locally.", "استخدم الصورة التي اختبرتها محليًا."),
            ("Declare container port 8080.", "صرّح بمنفذ الحاوية 8080."),
            ("Forward Service port 80 to 8080.", "حوّل منفذ الخدمة 80 إلى 8080."),
            ("Make the Service a load balancer.", "اجعل الخدمة موزّع حمل."),
        ),
        starter='''apiVersion: apps/v1
kind: Deployment
metadata:
  name: predict
spec:
  # Step 1
  replicas: ___
  selector:
    matchLabels:
      app: predict
  template:
    metadata:
      labels:
        app: predict
    spec:
      containers:
        - name: predict
          # Step 2: the image you built, ran and curl-tested locally
          image: ___
          ports:
            # Step 3
            - containerPort: ___
---
apiVersion: v1
kind: Service
metadata:
  name: predict
spec:
  selector:
    app: predict
  ports:
    - port: 80
      # Step 4
      targetPort: ___
  # Step 5: an external IP that spreads traffic across the replicas (also on GKE)
  type: ___
''',
        answers=("3", "predict:1.0.0", "8080", "8080", "LoadBalancer"),
        alternatives={2: (r"re:[a-z0-9./_-]*predict:[A-Za-z0-9._-]+",)},
        blanks=(
            ("`replicas: 3`.", "`replicas: 3`."),
            ("a tagged image such as `predict:1.0.0`.", "صورة موسومة مثل `predict:1.0.0`."),
            ("the container listens on `8080`.", "تستمع الحاوية على `8080`."),
            ("`targetPort: 8080`.", "`targetPort: 8080`."),
            ("`type: LoadBalancer`.", "`type: LoadBalancer`."),
        ),
        hints=(
            ("The Deployment keeps the replica count; the Service spreads traffic across them.", "يحافظ Deployment على عدد النسخ، وتوزّع الخدمة الحركة عليها."),
            ("Use a pinned tag, never `latest`.", "استخدم وسمًا مثبّتًا، ولا تستخدم `latest` أبدًا."),
            ("`port` is the Service's port, `targetPort` the container's.", "`port` هو منفذ الخدمة، و`targetPort` منفذ الحاوية."),
        ),
        success=("Correct! Each stage isolates a different failure: docker run tests the image, curl tests the API, `kubectl get pods` tests scheduling, and the Service tests networking.",
                 "صحيح! تعزل كل مرحلة فشلًا مختلفًا: يختبر docker run الصورة، ويختبر curl الواجهة، ويختبر `kubectl get pods` الجدولة، وتختبر الخدمة الشبكة."),
        expected=READ_NOTE,
        language="yaml",
    ),
    "COURSE-016.M15.L01.EX04": Guided(
        goal=("Write a serverless DataOps function that validates its JSON input, reads a document, calls a language API and returns a clear payload.",
              "اكتب دالة DataOps بلا خادم تتحقق من مدخل JSON، وتقرأ مستندًا، وتستدعي واجهة لغوية، وتعيد حمولة واضحة."),
        steps=(
            ("Require the `uri` field.", "اشترط الحقل `uri`."),
            ("Accept only gs:// URIs.", "اقبل فقط عناوين gs://."),
            ("Call the language API on the text.", "استدعِ الواجهة اللغوية على النص."),
            ("Return the result payload with status 200.", "أعد حمولة النتيجة مع الحالة 200."),
        ),
        starter='''def analyze_document(request_json, read_text, language_api):
    """Cloud Function body. read_text = Cloud Storage reader, language_api = Natural Language API (injected)."""
    # Step 1
    if not isinstance(request_json, dict) or ___:
        return {"error": "field 'uri' is required"}, 400
    # Step 2: only documents from our buckets
    if ___:
        return {"error": "only gs:// URIs are allowed"}, 400
    text = read_text(request_json["uri"])
    # Step 3
    sentiment = ___
    # Step 4
    return ___

storage = {"gs://reports/q3.txt": "Revenue grew strongly this quarter."}
fake_language_api = lambda text: {"score": 0.8 if "grew" in text else -0.2}
print(analyze_document({"uri": "gs://reports/q3.txt"}, storage.get, fake_language_api))
# gcloud functions call analyze-document --data '{"uri": "gs://reports/q3.txt"}'
''',
        answers=('"uri" not in request_json', 'not request_json["uri"].startswith("gs://")', "language_api(text)",
                 '{"uri": request_json["uri"], "characters": len(text), "sentiment": sentiment}, 200'),
        checks=(
            check("[analyze_document({}, storage.get, fake_language_api)[1], analyze_document('oops', storage.get, fake_language_api)[1]]", [400, 400],
                  "Blank 1: reject requests where `\"uri\" not in request_json`.", "الفراغ 1: ارفض الطلبات التي يكون فيها `\"uri\" not in request_json`."),
            check("analyze_document({'uri': 'https://evil.example/x'}, storage.get, fake_language_api)", [{"error": "only gs:// URIs are allowed"}, 400],
                  "Blank 2: `not request_json[\"uri\"].startswith(\"gs://\")`.", "الفراغ 2: `not request_json[\"uri\"].startswith(\"gs://\")`."),
            check("analyze_document({'uri': 'gs://reports/q3.txt'}, storage.get, fake_language_api)", [{"uri": "gs://reports/q3.txt", "characters": 35, "sentiment": {"score": 0.8}}, 200],
                  "Blanks 3-4: call `language_api(text)` and return the uri, the text length and the sentiment with 200.",
                  "الفراغان 3 و4: استدعِ `language_api(text)` وأعد العنوان وطول النص والمشاعر مع 200."),
        ),
        hints=(
            ("Validate before touching storage or paid APIs.", "تحقّق قبل لمس التخزين أو الواجهات المدفوعة."),
            ("`str.startswith(\"gs://\")` checks the scheme.", "يفحص `str.startswith(\"gs://\")` المخطط."),
            ("Return (payload, status) like the error branches.", "أعد (الحمولة، الحالة) مثل فروع الخطأ."),
        ),
        success=("Correct! Bad requests are rejected before any storage read or paid API call, and the success payload says exactly what was analysed.",
                 "صحيح! تُرفض الطلبات الخاطئة قبل أي قراءة من التخزين أو استدعاء واجهة مدفوعة، وتقول حمولة النجاح بالضبط ما الذي حُلّل."),
        expected=STUB_NOTE,
        reflect=("When would you replace this single function with a larger data pipeline?", "متى ستستبدل هذه الدالة المفردة بخط بيانات أكبر؟"),
    ),
    "COURSE-016.M16.L01.EX04": Guided(
        goal=("Write an HTTP-triggered ML function that only accepts authenticated POST requests with a valid JSON body.",
              "اكتب دالة تعلّم آلي تُطلق عبر HTTP ولا تقبل إلا طلبات POST مصادقًا عليها بجسم JSON صالح."),
        steps=(
            ("Accept only POST.", "اقبل POST فقط."),
            ("Reject unknown tokens with 401.", "ارفض الرموز المجهولة بالرمز 401."),
            ("Require a non-empty `text` string.", "اشترط نصًا غير فارغ في الحقل `text`."),
            ("Return the entities from the language service.", "أعد الكيانات من الخدمة اللغوية."),
        ),
        starter='''TOKENS = {"team-token-123"}

def analyze(method, headers, body, language_api):
    # Step 1
    if method != ___:
        return {"error": "method not allowed"}, 405
    token = headers.get("Authorization", "").removeprefix("Bearer ")
    # Step 2: an open endpoint lets anyone spend your API quota
    if ___:
        return {"error": "unauthorized"}, 401
    text = body.get("text") if isinstance(body, dict) else None
    # Step 3
    if ___:
        return {"error": "'text' must be a non-empty string"}, 400
    # Step 4
    return ___

fake_entities = lambda text: [word for word in text.split() if word.istitle()]
print(analyze("POST", {"Authorization": "Bearer team-token-123"}, {"text": "Masar opened in Cairo"}, fake_entities))
''',
        answers=('"POST"', "token not in TOKENS", "not isinstance(text, str) or not text.strip()",
                 '{"text": text, "entities": language_api(text)}, 200'),
        checks=(
            check("analyze('GET', {}, {}, fake_entities)[1]", 405, "Blank 1: compare with `\"POST\"`.", "الفراغ 1: قارن بـ `\"POST\"`."),
            check("[analyze('POST', {}, {'text': 'x'}, fake_entities)[1], analyze('POST', {'Authorization': 'Bearer nope'}, {'text': 'x'}, fake_entities)[1]]", [401, 401],
                  "Blank 2: `token not in TOKENS`.", "الفراغ 2: `token not in TOKENS`."),
            check("[analyze('POST', {'Authorization': 'Bearer team-token-123'}, b, fake_entities)[1] for b in ({}, {'text': '   '}, {'text': 5}, [1])]", [400, 400, 400, 400],
                  "Blank 3: reject non-strings and blank strings.", "الفراغ 3: ارفض غير النصوص والنصوص الفارغة."),
            check("analyze('POST', {'Authorization': 'Bearer team-token-123'}, {'text': 'Masar opened in Cairo'}, fake_entities)", [{"text": "Masar opened in Cairo", "entities": ["Masar", "Cairo"]}, 200],
                  "Blank 4: return the text and `language_api(text)` with status 200.", "الفراغ 4: أعد النص و`language_api(text)` مع الحالة 200."),
        ),
        hints=(
            ("Check the method, then the credentials, then the payload.", "افحص الطريقة، ثم بيانات الاعتماد، ثم الحمولة."),
            ("A missing header gives an empty token, which is not in TOKENS.", "الترويسة المفقودة تعطي رمزًا فارغًا ليس ضمن TOKENS."),
            ("`text.strip()` is empty for whitespace-only input.", "يكون `text.strip()` فارغًا للمدخل المكوّن من مسافات فقط."),
        ),
        success=("Correct! Unauthenticated callers never reach the paid language API, and malformed input is rejected with a message that says what to fix.",
                 "صحيح! لا يصل المستدعون غير المصادق عليهم أبدًا إلى الواجهة اللغوية المدفوعة، ويُرفض المدخل التالف برسالة تقول ما الذي يجب إصلاحه."),
        expected=STUB_NOTE,
        reflect=("Which cloud API must be enabled, which dependency goes into requirements.txt, and what is the function's entry point?",
                 "أي واجهة سحابية يجب تفعيلها؟ وأي تبعية تُضاف إلى requirements.txt؟ وما نقطة دخول الدالة؟"),
    ),
    "COURSE-016.M16.L01.EX06": Guided(
        goal=("Turn a repetitive scoring task into a small Click command-line tool with validated options and clear errors.",
              "حوّل مهمة تقييم متكررة إلى أداة سطر أوامر صغيرة بـ Click، بخيارات مُتحقَّق منها وأخطاء واضحة."),
        steps=(
            ("Declare the function as a Click command.", "صرّح بالدالة أمرًا من أوامر Click."),
            ("Validate the threshold to the range 0-1.", "تحقّق من أن العتبة في النطاق 0-1."),
            ("Fail with a readable error and a non-zero exit code.", "افشل برسالة خطأ مقروءة ورمز خروج غير صفري."),
            ("Run the command when the module is executed.", "شغّل الأمر عند تنفيذ الوحدة."),
        ),
        starter='''import click
import joblib
import pandas as pd

# Step 1
@___
@click.argument("csv_path", type=click.Path(exists=True, dir_okay=False))
@click.option("--model", "model_path", default="model.joblib", show_default=True, help="Serialized model to use.")
# Step 2: reject values outside 0-1 before any work starts
@click.option("--threshold", type=___, default=0.5, show_default=True, help="Probability above which a customer is flagged.")
def predict(csv_path, model_path, threshold):
    """Score a CSV of customers and print the ones likely to churn."""
    try:
        model = joblib.load(model_path)
    except FileNotFoundError as error:
        # Step 3: a clean message and exit code 1 instead of a traceback
        raise ___
    rows = pd.read_csv(csv_path)
    flagged = rows[model.predict_proba(rows)[:, 1] >= threshold]
    click.echo(f"{len(flagged)} of {len(rows)} customers flagged")

if __name__ == "__main__":
    # Step 4
    ___
''',
        answers=("click.command()", "click.FloatRange(0, 1)", "click.ClickException(str(error))", "predict()"),
        alternatives={2: ("click.FloatRange(0.0, 1.0)", "click.FloatRange(min=0, max=1)")},
        blanks=(
            ("`@click.command()`.", "`@click.command()`."),
            ("`click.FloatRange(0, 1)`.", "`click.FloatRange(0, 1)`."),
            ("`raise click.ClickException(str(error))`.", "`raise click.ClickException(str(error))`."),
            ("call `predict()`.", "استدعِ `predict()`."),
        ),
        hints=(
            ("Click's command decorator turns the function into a CLI entry point.", "يحوّل مزخرف الأوامر في Click الدالة إلى نقطة دخول لواجهة سطر الأوامر."),
            ("Click validates types like `FloatRange` before your code runs.", "يتحقق Click من أنواع مثل `FloatRange` قبل تشغيل كودك."),
            ("`ClickException` prints `Error: ...` and exits with code 1.", "يطبع `ClickException` الرسالة `Error: ...` ويخرج بالرمز 1."),
        ),
        success=("Correct! One documented command replaces a manual notebook routine: inputs are validated, errors are readable, and `--help` explains every option.",
                 "صحيح! يحل أمر واحد موثّق محل روتين يدوي في دفتر ملاحظات: المدخلات مُتحقَّق منها، والأخطاء مقروءة، ويشرح `--help` كل خيار."),
        expected=READ_NOTE,
        reflect=("How would you package and distribute this tool (PyPI or a container registry), and where would a microservice boundary appear later?",
                 "كيف ستحزم هذه الأداة وتوزّعها (PyPI أو سجل حاويات)؟ وأين ستظهر حدود خدمة مصغّرة لاحقًا؟"),
    ),
}
