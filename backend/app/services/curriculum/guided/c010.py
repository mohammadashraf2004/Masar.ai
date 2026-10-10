"""COURSE-010 AI Service Engineering with FastAPI: guided implementation exercises.

FastAPI, Pydantic, SQLAlchemy, pytest and the provider SDKs are not installed
in the practice sandbox: exercises about those APIs are checked by reading
the code. Exercises about service logic (typing, validation rules, streaming
formats, rate limits, caching, metrics) run for real.
"""
from . import Guided, check

STATIC_NOTE = (
    "FastAPI and its companion libraries are not installed in the practice sandbox, so Check answer reads your code instead of running it.",
    "مكتبة FastAPI والمكتبات المرافقة لها غير مثبّتة في بيئة التدريب، لذلك يقرأ «تحقّق من الإجابة» الكود بدل تشغيله.",
)
LOGIC_NOTE = (
    "This is the service logic on its own, so it runs in the sandbox; in the real service it sits behind a FastAPI route.",
    "هذا منطق الخدمة وحده، لذلك يعمل داخل بيئة التدريب؛ وفي الخدمة الحقيقية يقع خلف مسار FastAPI.",
)

EXERCISES = {
    "COURSE-010.M01.L02.EX01": Guided(
        goal=("Build the smallest useful FastAPI service: a health route and a greeting route with a query parameter.",
              "ابنِ أصغر خدمة FastAPI مفيدة: مسار للتحقق من الصحة ومسار ترحيب مع معامل استعلام."),
        steps=(
            ("Create the application object.", "أنشئ كائن التطبيق."),
            ("Register the health route on the path `/`.", "سجّل مسار الصحة على المسار `/`."),
            ("Return the greeting built from the `name` query parameter.", "أعد التحية المبنية من معامل الاستعلام `name`."),
        ),
        starter='''from fastapi import FastAPI

# Step 1: the application object that holds every route
app = ___

# Step 2: GET / -> {"status": "healthy"}
@app.get(___)
def health():
    return {"status": "healthy"}

# Step 3: GET /hello?name=Ada -> {"message": "Hello, Ada"}
@app.get("/hello")
def hello(name: str):
    return ___

# Run it with:  fastapi dev main.py   then open http://127.0.0.1:8000/docs
''',
        answers=("FastAPI()", '"/"', '{"message": f"Hello, {name}"}'),
        alternatives={3: ('{"message": "Hello, " + name}',)},
        blanks=(
            ("create the app with `FastAPI()`.", "أنشئ التطبيق بـ `FastAPI()`."),
            ("the root path is the string `\"/\"`.", "المسار الجذر هو النص `\"/\"`."),
            ("return `{\"message\": f\"Hello, {name}\"}` - FastAPI turns the dictionary into JSON.",
             "أعد `{\"message\": f\"Hello, {name}\"}` - ويحوّل FastAPI القاموس إلى JSON."),
        ),
        hints=(
            ("Everything starts from one instance of the `FastAPI` class; decorators attach routes to it.", "يبدأ كل شيء من نسخة واحدة من الصنف `FastAPI`، وتربط المزخرفات (decorators) المسارات بها."),
            ("The decorator's first argument is the URL path.", "الوسيط الأول للمزخرف هو مسار URL."),
            ("A function parameter that is not in the path becomes a query parameter; return a dictionary.", "معامل الدالة غير الموجود في المسار يصبح معامل استعلام؛ أعد قاموسًا."),
        ),
        success=("Correct! Uvicorn receives the HTTP request, FastAPI matches the path to your function, reads `name` from the query string, and serializes your dictionary to JSON.",
                 "صحيح! يستقبل Uvicorn طلب HTTP، ويطابق FastAPI المسار مع دالتك، ويقرأ `name` من سلسلة الاستعلام، ويحوّل قاموسك إلى JSON."),
        expected=STATIC_NOTE,
        reflect=("In a few sentences: what do the app object, the route decorator, the route function and Uvicorn each do?",
                 "في بضع جمل: ما دور كائن التطبيق، ومزخرف المسار، ودالة المسار، وUvicorn؟"),
    ),
    "COURSE-010.M01.L02.EX03": Guided(
        goal=("Write one pagination dependency and inject it into two routes instead of repeating the same query parameters.",
              "اكتب تابعية (dependency) واحدة للتقسيم إلى صفحات، وحقنها في مسارين بدل تكرار معاملات الاستعلام نفسها."),
        steps=(
            ("Return the resolved `skip` and `limit` from the dependency.", "أعد قيمتي `skip` و`limit` المحسومتين من التابعية."),
            ("Inject the dependency into `/messages`.", "احقن التابعية في `/messages`."),
            ("Inject the same dependency into `/conversations`.", "احقن التابعية نفسها في `/conversations`."),
        ),
        starter='''from fastapi import Depends, FastAPI

app = FastAPI()

# Step 1: FastAPI reads skip and limit from the query string for us
def pagination(skip: int = 0, limit: int = 10):
    return ___

# Step 2: inject the dependency
@app.get("/messages")
def list_messages(page: dict = ___):
    return page

# Step 3: reuse it - no duplicated parameters
@app.get("/conversations")
def list_conversations(page: dict = ___):
    return page
''',
        answers=('{"skip": skip, "limit": limit}', "Depends(pagination)", "Depends(pagination)"),
        alternatives={1: ("dict(skip=skip, limit=limit)",)},
        blanks=(
            ("return `{\"skip\": skip, \"limit\": limit}`.", "أعد `{\"skip\": skip, \"limit\": limit}`."),
            ("use `Depends(pagination)` - pass the function itself, do not call it.", "استخدم `Depends(pagination)` - مرّر الدالة نفسها دون استدعائها."),
            ("the same `Depends(pagination)` works here.", "يعمل `Depends(pagination)` نفسه هنا."),
        ),
        hints=(
            ("A dependency is an ordinary function; its parameters become query parameters.", "التابعية دالة عادية، وتصبح معاملاتها معاملات استعلام."),
            ("`Depends(...)` takes the function object, without parentheses after its name.", "يأخذ `Depends(...)` كائن الدالة دون أقواس بعد اسمها."),
            ("FastAPI calls `pagination` for each request and passes its return value as `page`.", "يستدعي FastAPI الدالة `pagination` مع كل طلب ويمرّر قيمتها المعادة بوصفها `page`."),
        ),
        success=("Correct! FastAPI resolves `pagination` per request and injects its result, so both routes share one definition of skip and limit.",
                 "صحيح! يحسم FastAPI التابعية `pagination` مع كل طلب ويحقن نتيجتها، فيشترك المساران في تعريف واحد لـ skip وlimit."),
        expected=STATIC_NOTE,
        reflect=("Name another concern - such as authentication or a database session - that benefits from the same pattern.",
                 "اذكر أمرًا آخر - مثل المصادقة أو جلسة قاعدة البيانات - يستفيد من النمط نفسه."),
    ),
    "COURSE-010.M01.L04.EX01": Guided(
        goal=("Give a GenAI cost function an explicit type contract, and still check the model at runtime.",
              "امنح دالة حساب تكلفة الذكاء الاصطناعي التوليدي عقد أنواع صريحًا، مع التحقق من النموذج أثناء التشغيل أيضًا."),
        steps=(
            ("Restrict the model to two names with `Literal`.", "قيّد النموذج باسمين باستخدام `Literal`."),
            ("Create a reusable alias for the pricing table.", "أنشئ اسمًا مستعارًا قابلًا لإعادة الاستخدام لجدول الأسعار."),
            ("Allow the response to be `None`.", "اسمح بأن تكون الاستجابة `None`."),
            ("Declare that the function returns three floats.", "صرّح بأن الدالة تعيد ثلاث قيم عشرية."),
        ),
        starter='''from typing import Literal, Optional, get_args, get_origin, get_type_hints

# Step 1: the only two models this service supports
SupportedModel = Literal[___]

# Step 2: a reusable alias: model name -> (input price, output price) per 1,000 tokens
PriceTable = ___
PRICES: PriceTable = {"gpt-4o": (0.005, 0.015), "gpt-4o-mini": (0.00015, 0.0006)}

def count_tokens(text: str) -> int:
    return len(text.split())          # a rough stand-in for a real tokenizer

# Step 3: the response may be missing; Step 4: three floats come back
def calculate_cost(prompt: str, response: ___, model: SupportedModel) -> ___:
    if model not in PRICES:           # type hints are not enforced at runtime
        raise ValueError(f"Unsupported model: {model}")
    input_price, output_price = PRICES[model]
    request_cost = count_tokens(prompt) / 1000 * input_price
    response_cost = count_tokens(response or "") / 1000 * output_price
    return request_cost, response_cost, request_cost + response_cost

print(calculate_cost("Explain FastAPI in one line", None, "gpt-4o"))
''',
        answers=('"gpt-4o", "gpt-4o-mini"', "dict[str, tuple[float, float]]", "Optional[str]", "tuple[float, float, float]"),
        checks=(
            check("sorted(get_args(SupportedModel))", ["gpt-4o", "gpt-4o-mini"],
                  "Blank 1: list both model names inside `Literal[...]`.", "الفراغ 1: اذكر اسمي النموذجين داخل `Literal[...]`."),
            check("get_origin(PriceTable) is dict and get_args(PriceTable)[0] is str and get_args(get_args(PriceTable)[1]) == (float, float)", True,
                  "Blank 2: the alias is `dict[str, tuple[float, float]]`.", "الفراغ 2: الاسم المستعار هو `dict[str, tuple[float, float]]`."),
            check("get_type_hints(calculate_cost)['response'] == Optional[str]", True,
                  "Blank 3: use `Optional[str]` (or `str | None`).", "الفراغ 3: استخدم `Optional[str]` (أو `str | None`)."),
            check("get_origin(get_type_hints(calculate_cost)['return']) is tuple and get_args(get_type_hints(calculate_cost)['return']) == (float, float, float)", True,
                  "Blank 4: the return type is `tuple[float, float, float]`.", "الفراغ 4: نوع الإرجاع هو `tuple[float, float, float]`."),
        ),
        hints=(
            ("`Literal[\"a\", \"b\"]` accepts exactly those values.", "يقبل `Literal[\"a\", \"b\"]` هاتين القيمتين بالضبط."),
            ("Built-in generics can be written directly: `dict[KeyType, ValueType]`, `tuple[float, float]`.", "يمكن كتابة الأنواع العامة المدمجة مباشرة: `dict[KeyType, ValueType]` و`tuple[float, float]`."),
            ("`Optional[str]` means `str` or `None`.", "يعني `Optional[str]` نصًا أو `None`."),
        ),
        success=("Correct! The signature now documents every input and output, while the runtime check still protects against values that bypass type checking.",
                 "صحيح! يوثّق التوقيع الآن كل مدخل ومخرج، بينما يحمي الفحص أثناء التشغيل من القيم التي تتجاوز فحص الأنواع."),
        expected=LOGIC_NOTE,
        reflect=("Why is the runtime check still useful after you added `Literal`?", "لماذا يبقى الفحص أثناء التشغيل مفيدًا بعد إضافة `Literal`؟"),
    ),
    "COURSE-010.M01.L04.EX02": Guided(
        goal=("Replace six loose parameters with two dataclasses so the cost function takes one object and returns one report.",
              "استبدل ستة معاملات متفرقة بصنفي بيانات (dataclasses) لتأخذ دالة التكلفة كائنًا واحدًا وتعيد تقريرًا واحدًا."),
        steps=(
            ("Turn `MessageCostReport` into a dataclass.", "حوّل `MessageCostReport` إلى صنف بيانات (dataclass)."),
            ("Make the function accept a `Message`.", "اجعل الدالة تقبل كائنًا من نوع `Message`."),
            ("Return a `MessageCostReport`.", "أعد كائنًا من نوع `MessageCostReport`."),
        ),
        starter='''from dataclasses import dataclass, fields
from typing import get_type_hints

@dataclass
class Message:
    prompt: str
    response: str | None
    model: str

# Step 1: the three costs travel together as one dataclass
@___
class MessageCostReport:
    request_cost: float
    response_cost: float
    total_cost: float

PRICES = {"gpt-4o": (0.005, 0.015), "gpt-4o-mini": (0.00015, 0.0006)}

# Step 2: one Message in, one MessageCostReport out
def calculate_cost(message: ___) -> MessageCostReport:
    input_price, output_price = PRICES[message.model]
    request_cost = len(message.prompt.split()) / 1000 * input_price
    response_cost = len((message.response or "").split()) / 1000 * output_price
    # Step 3: build the report
    return ___

report = calculate_cost(Message("Explain FastAPI in one line", "A fast Python web framework", "gpt-4o"))
print(report)
''',
        answers=("dataclass", "Message", "MessageCostReport(request_cost, response_cost, request_cost + response_cost)"),
        checks=(
            check("[f.name for f in fields(MessageCostReport)]", ["request_cost", "response_cost", "total_cost"],
                  "Blank 1: decorate the class with `@dataclass`.", "الفراغ 1: زخرف الصنف بـ `@dataclass`."),
            check("get_type_hints(calculate_cost)['message'] is Message", True,
                  "Blank 2: annotate the parameter as `Message`.", "الفراغ 2: اجعل نوع المعامل `Message`."),
            check("[round(report.request_cost, 6), round(report.response_cost, 6), round(report.total_cost, 6)]", [2.5e-05, 7.5e-05, 0.0001],
                  "Blank 3: return `MessageCostReport(request_cost, response_cost, request_cost + response_cost)`.",
                  "الفراغ 3: أعد `MessageCostReport(request_cost, response_cost, request_cost + response_cost)`."),
        ),
        hints=(
            ("`@dataclass` generates `__init__` and a readable representation from the annotated fields.", "يولّد `@dataclass` الدالة `__init__` وتمثيلًا مقروءًا من الحقول ذات الأنواع."),
            ("The parameter's type is the class you defined for prompt, response and model.", "نوع المعامل هو الصنف الذي عرّفته للموجّه والاستجابة والنموذج."),
            ("Dataclasses accept their fields positionally, in declaration order.", "تقبل أصناف البيانات حقولها بالترتيب الذي عُرّفت به."),
        ),
        success=("Correct! Related values now travel together with names and types, so the signature is short and impossible to mix up.",
                 "صحيح! أصبحت القيم المترابطة تنتقل معًا بأسماء وأنواع، فصار التوقيع قصيرًا ويستحيل الخلط فيه."),
        expected=LOGIC_NOTE,
        reflect=("Dataclasses do not validate values. Which check would you still need Pydantic or your own code for?",
                 "لا تتحقق أصناف البيانات من القيم. ما الفحص الذي ستظل تحتاج فيه إلى Pydantic أو إلى كود خاص بك؟"),
    ),
    "COURSE-010.M01.L04.EX03": Guided(
        goal=("Turn broad types into a strict Pydantic request schema for an image-generation API.",
              "حوّل الأنواع العامة إلى مخطط طلب Pydantic صارم لواجهة توليد الصور."),
        steps=(
            ("Limit the prompt to 1-4000 characters.", "حدّد الموجّه بطول من 1 إلى 4000 حرف."),
            ("Allow only the two supported models.", "اسمح بالنموذجين المدعومين فقط."),
            ("Bound the number of inference steps from below.", "ضع حدًا أدنى لعدد خطوات الاستدلال."),
        ),
        starter='''from typing import Annotated, Literal

from pydantic import BaseModel, Field, PositiveInt

class ImageModelRequest(BaseModel):
    # Step 1: between 1 and 4000 characters
    prompt: Annotated[str, Field(min_length=___, max_length=___)]
    # Step 2: only the two supported models
    model: Literal[___]
    # (width, height), both positive integers
    output_size: tuple[PositiveInt, PositiveInt]
    # Step 3: at least 0 and at most 2000 steps, 200 by default
    num_inference_steps: Annotated[int, Field(ge=___, le=2000)] = 200

valid = {"prompt": "A lighthouse at dusk", "model": "tinysd", "output_size": [512, 512]}
invalid = {"prompt": "", "model": "dall-e", "output_size": [512, -1]}     # three errors
''',
        answers=("1", "4000", '"tinysd", "sd1.5"', "0"),
        alternatives={3: ('"sd1.5", "tinysd"',)},
        blanks=(
            ("the minimum length is 1.", "الحد الأدنى للطول 1."),
            ("the maximum length is 4000.", "الحد الأقصى للطول 4000."),
            ("list the two supported names: `\"tinysd\", \"sd1.5\"`.", "اذكر الاسمين المدعومين: `\"tinysd\", \"sd1.5\"`."),
            ("`ge=0` - the number of steps cannot be negative.", "`ge=0` - لا يمكن أن يكون عدد الخطوات سالبًا."),
        ),
        hints=(
            ("`Field(min_length=..., max_length=...)` constrains string length.", "يقيّد `Field(min_length=..., max_length=...)` طول النص."),
            ("`Literal[...]` lists every allowed value.", "يسرد `Literal[...]` كل قيمة مسموح بها."),
            ("`ge` means greater than or equal; `le` means less than or equal.", "`ge` تعني أكبر من أو يساوي، و`le` تعني أصغر من أو يساوي."),
        ),
        success=("Correct! FastAPI will now reject an empty prompt, an unknown model or a negative size with a 422 response before any GPU time is spent.",
                 "صحيح! سيرفض FastAPI الآن الموجّه الفارغ أو النموذج غير المعروف أو الحجم السالب باستجابة 422 قبل إنفاق أي وقت على GPU."),
        expected=STATIC_NOTE,
        reflect=("Add one more sensible constraint of your own. Which field would it protect, and why?",
                 "أضف قيدًا معقولًا آخر من عندك. أي حقل سيحميه؟ ولماذا؟"),
    ),
    "COURSE-010.M01.L04.EX04": Guided(
        goal=("Write a single-field rule and a cross-field rule for image requests, and raise clear errors before inference.",
              "اكتب قاعدة لحقل واحد وقاعدة تعتمد على عدة حقول لطلبات الصور، وأطلق أخطاء واضحة قبل الاستدلال."),
        steps=(
            ("Rule A: the size must be square.", "القاعدة A: يجب أن يكون الحجم مربعًا."),
            ("Rule A: the width must be 512 or 1024.", "القاعدة A: يجب أن يكون العرض 512 أو 1024."),
            ("Rule B: tinysd may not exceed its step limit.", "القاعدة B: لا يجوز أن يتجاوز tinysd حد خطواته."),
        ),
        starter='''MAX_STEPS = {"tinysd": 50, "sd1.5": 2000}

# Rule A needs only one field (Pydantic: @field_validator("output_size"))
def validate_output_size(output_size):
    width, height = output_size
    # Step 1: width and height must be equal
    if ___:
        raise ValueError("output_size must be square")
    # Step 2: only two widths are supported
    if ___:
        raise ValueError("output_size width must be 512 or 1024")
    return output_size

# Rule B needs two fields together (Pydantic: @model_validator(mode="after"))
def validate_steps_for_model(request):
    limit = MAX_STEPS[request["model"]]
    # Step 3: reject too many steps for this model
    if ___:
        raise ValueError(f"{request['model']} supports at most {limit} inference steps")
    return request

def errors_for(request):
    problems = []
    for rule, value in ((validate_output_size, request["output_size"]), (validate_steps_for_model, request)):
        try:
            rule(value)
        except ValueError as exc:
            problems.append(str(exc))
    return problems

print(errors_for({"model": "tinysd", "output_size": (512, 768), "num_inference_steps": 80}))
''',
        answers=("width != height", "width not in (512, 1024)", 'request["num_inference_steps"] > limit'),
        checks=(
            check("[errors_for({'model': 'sd1.5', 'output_size': s, 'num_inference_steps': 10}) for s in ((512, 512), (1024, 1024), (512, 768))]",
                  [[], [], ["output_size must be square"]],
                  "Blank 1: raise when `width != height`.", "الفراغ 1: أطلق الخطأ عندما يكون `width != height`."),
            check("errors_for({'model': 'sd1.5', 'output_size': (768, 768), 'num_inference_steps': 10})", ["output_size width must be 512 or 1024"],
                  "Blank 2: raise when the width is not in `(512, 1024)`.", "الفراغ 2: أطلق الخطأ عندما لا يكون العرض ضمن `(512, 1024)`."),
            check("[errors_for({'model': m, 'output_size': (512, 512), 'num_inference_steps': n}) for m, n in (('tinysd', 50), ('tinysd', 51), ('sd1.5', 500))]",
                  [[], ["tinysd supports at most 50 inference steps"], []],
                  "Blank 3: raise when `request[\"num_inference_steps\"]` is greater than the model's limit.",
                  "الفراغ 3: أطلق الخطأ عندما يكون `request[\"num_inference_steps\"]` أكبر من حد النموذج."),
        ),
        hints=(
            ("A square has equal width and height.", "للمربع عرض وارتفاع متساويان."),
            ("`value not in (a, b)` is True for anything except a or b.", "يكون `value not in (a, b)` صحيحًا لأي قيمة عدا a وb."),
            ("Rule B compares one field with a limit chosen by another field.", "تقارن القاعدة B حقلًا واحدًا بحد يختاره حقل آخر."),
        ),
        success=("Correct! Rule A only needs `output_size`, so it is a field validator; Rule B needs both `model` and the step count, so it is a model validator - and both stop bad requests before any GPU time is used.",
                 "صحيح! تحتاج القاعدة A إلى `output_size` فقط فهي مُتحقِّق حقل، وتحتاج القاعدة B إلى `model` وعدد الخطوات معًا فهي مُتحقِّق نموذج - وكلتاهما توقف الطلبات الخاطئة قبل استخدام أي وقت على GPU."),
        expected=(
            "Pydantic runs these as `@field_validator` and `@model_validator`; the same rules are written here as plain functions so they run in the sandbox.",
            "يشغّل Pydantic هذه القواعد بوصفها `@field_validator` و`@model_validator`؛ وهي مكتوبة هنا دوالَّ عادية لتعمل داخل بيئة التدريب.",
        ),
        reflect=("Why should this validation happen before image inference starts?", "لماذا يجب أن يجري هذا التحقق قبل بدء توليد الصورة؟"),
    ),
    "COURSE-010.M01.L04.EX05": Guided(
        goal=("Model the service configuration as validated settings that load from the environment and a local .env file.",
              "مثّل إعدادات الخدمة بوصفها إعدادات مُتحقَّقًا منها تُحمَّل من البيئة ومن ملف .env محلي."),
        steps=(
            ("Load a `.env` file during local development.", "حمّل ملف `.env` أثناء التطوير المحلي."),
            ("Require a secret of at least 32 characters.", "اشترط سرًّا لا يقل عن 32 حرفًا."),
            ("Read the PostgreSQL URL from `DATABASE_URL`.", "اقرأ عنوان PostgreSQL من `DATABASE_URL`."),
            ("Validate every CORS origin as a URL.", "تحقّق من أن كل أصل CORS عنوان URL صالح."),
            ("Create the settings object at startup.", "أنشئ كائن الإعدادات عند بدء التشغيل."),
        ),
        starter='''from typing import Annotated

from pydantic import Field, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    # Step 1: also read a local .env file
    model_config = SettingsConfigDict(env_file=___)

    port: int = 8000
    # Step 2: a secret of at least 32 characters
    app_secret: Annotated[str, Field(min_length=___)]
    # Step 3: a validated PostgreSQL URL from the DATABASE_URL variable
    database_url: Annotated[PostgresDsn, Field(alias=___)]
    # Step 4: each allowed origin must be a valid URL
    cors_whitelist_domains: set[___] = {"http://localhost:3000"}

# Step 5: validation happens here, once, when the service starts
settings = ___
''',
        answers=('".env"', "32", '"DATABASE_URL"', "HttpUrl", "AppSettings()"),
        blanks=(
            ("use `env_file=\".env\"`.", "استخدم `env_file=\".env\"`."),
            ("set `min_length=32`.", "اضبط `min_length=32`."),
            ("the alias is the environment variable name, `\"DATABASE_URL\"`.", "الاسم المستعار هو اسم متغير البيئة `\"DATABASE_URL\"`."),
            ("use the `HttpUrl` type for each origin.", "استخدم النوع `HttpUrl` لكل أصل."),
            ("instantiate the class: `AppSettings()`.", "أنشئ نسخة من الصنف: `AppSettings()`."),
        ),
        hints=(
            ("`SettingsConfigDict(env_file=...)` names the file to read.", "يحدد `SettingsConfigDict(env_file=...)` اسم الملف المراد قراءته."),
            ("`Field(alias=...)` maps a field to a differently named environment variable.", "يربط `Field(alias=...)` الحقل بمتغير بيئة باسم مختلف."),
            ("Creating the object reads and validates everything immediately.", "إنشاء الكائن يقرأ كل شيء ويتحقق منه فورًا."),
        ),
        success=("Correct! A missing secret, a malformed database URL or an invalid origin now stops the service at startup with a clear error, instead of failing later on a real request.",
                 "صحيح! أصبح غياب السر أو خطأ عنوان قاعدة البيانات أو أصل غير صالح يوقف الخدمة عند بدء التشغيل بخطأ واضح، بدل الفشل لاحقًا عند طلب حقيقي."),
        expected=STATIC_NOTE,
        reflect=("Why is failing at startup better than discovering a malformed database URL on the first request?",
                 "لماذا يكون الفشل عند بدء التشغيل أفضل من اكتشاف خطأ عنوان قاعدة البيانات عند أول طلب؟"),
    ),
    "COURSE-010.M01.L04.EX06": Guided(
        goal=("Refactor a text-generation route to use a validated request model and a response model with a computed token count.",
              "أعد هيكلة مسار توليد النص ليستخدم نموذج طلب مُتحقَّقًا منه ونموذج استجابة يحتوي على عدد رموز محسوب."),
        steps=(
            ("Bound the temperature between 0.0 and 2.0.", "حدّد درجة الحرارة بين 0.0 و2.0."),
            ("Compute the token count from the content.", "احسب عدد الرموز من المحتوى."),
            ("Declare the response model on the route.", "صرّح بنموذج الاستجابة على المسار."),
            ("Accept the request model as the POST body.", "اقبل نموذج الطلب بوصفه جسم طلب POST."),
        ),
        starter='''from typing import Annotated, Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field

app = FastAPI()

class TextModelRequest(BaseModel):
    model: Literal["gpt-4o", "gpt-4o-mini"]
    prompt: Annotated[str, Field(min_length=1, max_length=10_000)]
    # Step 1: temperature between 0.0 and 2.0
    temperature: Annotated[float, Field(ge=___, le=___)] = 0.7

class TextModelResponse(BaseModel):
    model: str
    prompt: str
    content: str

    # Step 2: derived from the content, added when the response is serialized
    @computed_field
    @property
    def tokens(self) -> int:
        return ___

# Step 3: the response model; Step 4: the validated body
@app.post("/generate/text", response_model=___)
def serve_text(body: ___) -> TextModelResponse:
    content = generate_text(body.model, body.prompt, body.temperature)    # the lesson's model call
    return TextModelResponse(model=body.model, prompt=body.prompt, content=content)
''',
        answers=("0.0", "2.0", "len(self.content.split())", "TextModelResponse", "TextModelRequest"),
        alternatives={1: ("0",), 2: ("2",)},
        blanks=(
            ("the lowest temperature is `0.0`.", "أقل درجة حرارة هي `0.0`."),
            ("the highest temperature is `2.0`.", "أعلى درجة حرارة هي `2.0`."),
            ("count the words of `self.content`: `len(self.content.split())`.", "عُدّ كلمات `self.content`: `len(self.content.split())`."),
            ("pass `TextModelResponse` as the response model.", "مرّر `TextModelResponse` بوصفه نموذج الاستجابة."),
            ("type the body parameter as `TextModelRequest`.", "اجعل نوع معامل الجسم `TextModelRequest`."),
        ),
        hints=(
            ("`ge` and `le` set the inclusive bounds.", "يضبط `ge` و`le` الحدين الشاملين."),
            ("Inside a model method, fields are read through `self`.", "داخل دالة النموذج تُقرأ الحقول عبر `self`."),
            ("A parameter typed with a Pydantic model is read from the JSON body.", "يُقرأ المعامل الذي نوعه نموذج Pydantic من جسم JSON."),
        ),
        success=("Correct! Unknown models, empty prompts and out-of-range temperatures are now rejected before the model is called, and every response carries its token count.",
                 "صحيح! أصبحت النماذج غير المعروفة والموجّهات الفارغة ودرجات الحرارة خارج النطاق تُرفض قبل استدعاء النموذج، وتحمل كل استجابة عدد رموزها."),
        expected=STATIC_NOTE,
    ),
    "COURSE-010.M01.L05.EX02": Guided(
        goal=("Compare three sequential 2-second waits with three concurrent async waits.",
              "قارن ثلاث فترات انتظار متتالية مدة كلٍّ منها ثانيتان بثلاث فترات انتظار متزامنة غير متزامنة (async)."),
        steps=(
            ("Wait without blocking the event loop.", "انتظر دون حجب حلقة الأحداث (event loop)."),
            ("Run the three async waits concurrently.", "شغّل فترات الانتظار الثلاث بالتزامن."),
            ("Start the event loop.", "ابدأ حلقة الأحداث."),
        ),
        starter='''import asyncio
import time

def wait_sync():
    time.sleep(2)            # blocks the whole thread

async def wait_async():
    # Step 1: a non-blocking wait - other tasks run meanwhile
    await ___

start = time.perf_counter()
for _ in range(3):
    wait_sync()
print(f"sequential: {time.perf_counter() - start:.1f}s")       # about 6 s

async def main():
    start = time.perf_counter()
    # Step 2: three waits at the same time
    await ___
    print(f"concurrent: {time.perf_counter() - start:.1f}s")   # about 2 s

# Step 3: run main() in an event loop
___
''',
        answers=("asyncio.sleep(2)", "asyncio.gather(wait_async(), wait_async(), wait_async())", "asyncio.run(main())"),
        alternatives={2: ("asyncio.gather(*[wait_async() for _ in range(3)])", "asyncio.gather(*(wait_async() for _ in range(3)))")},
        blanks=(
            ("await `asyncio.sleep(2)`.", "انتظر `asyncio.sleep(2)`."),
            ("use `asyncio.gather(wait_async(), wait_async(), wait_async())`.", "استخدم `asyncio.gather(wait_async(), wait_async(), wait_async())`."),
            ("call `asyncio.run(main())`.", "استدعِ `asyncio.run(main())`."),
        ),
        hints=(
            ("`asyncio.sleep` is the awaitable counterpart of `time.sleep`.", "`asyncio.sleep` هو المقابل القابل للانتظار لـ `time.sleep`."),
            ("`asyncio.gather` runs several awaitables concurrently and waits for all of them.", "يشغّل `asyncio.gather` عدة عناصر قابلة للانتظار بالتزامن وينتظرها كلها."),
            ("`asyncio.run` starts an event loop for one coroutine.", "يبدأ `asyncio.run` حلقة أحداث لدالة متزامنة واحدة."),
        ),
        success=("Correct! The async version takes about 2 seconds instead of 6 because the three waits overlap - nothing is computed in parallel, the loop simply stops idling.",
                 "صحيح! يستغرق الإصدار غير المتزامن نحو ثانيتين بدل 6 لأن فترات الانتظار الثلاث تتداخل - لا شيء يُحسب بالتوازي، بل تتوقف الحلقة عن الانتظار الفارغ فحسب."),
        expected=(
            "The sandbox does not run timing or event-loop code, so Check answer reads your code; run it locally to see the 6 s versus 2 s difference.",
            "لا تشغّل بيئة التدريب كود التوقيت أو حلقة الأحداث، لذلك يقرأ «تحقّق من الإجابة» الكود؛ شغّله محليًا لترى الفرق بين 6 ثوانٍ وثانيتين.",
        ),
    ),
    "COURSE-010.M01.L05.EX03": Guided(
        goal=("Write an async FastAPI route that awaits a hosted model provider and turns provider failures into clear HTTP errors.",
              "اكتب مسار FastAPI غير متزامن ينتظر مزوّد نماذج مستضافًا، ويحوّل أعطال المزوّد إلى أخطاء HTTP واضحة."),
        steps=(
            ("Create the asynchronous provider client.", "أنشئ عميل المزوّد غير المتزامن."),
            ("Await the provider call.", "انتظر استدعاء المزوّد."),
            ("Return 429 when the provider rate-limits you.", "أعد 429 عندما يفرض المزوّد حدًا للمعدل."),
            ("Return 502 when the provider fails.", "أعد 502 عندما يفشل المزوّد."),
            ("Return the generated text.", "أعد النص المولَّد."),
        ),
        starter='''from fastapi import FastAPI, HTTPException
from openai import APIError, AsyncOpenAI, RateLimitError

app = FastAPI()
# Step 1: the asynchronous client
client = ___

@app.post("/generate/text")
async def generate(prompt: str):
    try:
        # Step 2: await the network call - the event loop serves other requests meanwhile
        response = await ___
    except RateLimitError:
        # Step 3: "too many requests" - the caller should back off and retry
        raise HTTPException(status_code=___, detail="Rate limited - retry with exponential backoff")
    except APIError:
        # Step 4: the upstream provider failed
        raise HTTPException(status_code=___, detail="The model provider failed")
    # Step 5: the generated text
    return {"content": ___}
''',
        answers=(
            "AsyncOpenAI()",
            'client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])',
            "429",
            "502",
            "response.choices[0].message.content",
        ),
        alternatives={4: ("503",)},
        blanks=(
            ("create `AsyncOpenAI()`.", "أنشئ `AsyncOpenAI()`."),
            ("call `client.chat.completions.create(model=\"gpt-4o-mini\", messages=[{\"role\": \"user\", \"content\": prompt}])`.",
             "استدعِ `client.chat.completions.create(model=\"gpt-4o-mini\", messages=[{\"role\": \"user\", \"content\": prompt}])`."),
            ("429 means Too Many Requests.", "يعني 429 «طلبات كثيرة جدًا»."),
            ("502 (Bad Gateway) says an upstream service failed.", "يقول 502 (Bad Gateway) إن خدمة في المنبع فشلت."),
            ("read `response.choices[0].message.content`.", "اقرأ `response.choices[0].message.content`."),
        ),
        hints=(
            ("Async routes need async clients so `await` can release the event loop.", "تحتاج المسارات غير المتزامنة إلى عملاء غير متزامنين كي يحرّر `await` حلقة الأحداث."),
            ("Chat completions take a model name and a list of role/content messages.", "تأخذ chat completions اسم نموذج وقائمة رسائل role/content."),
            ("4xx codes blame the caller's rate; 5xx codes blame the server side.", "رموز 4xx تحمّل معدل المستدعي المسؤولية، ورموز 5xx تحمّلها جهة الخادم."),
        ),
        success=("Correct! While the provider works, the awaited call frees the event loop for other requests - the call is I/O-bound from your server's point of view.",
                 "صحيح! أثناء عمل المزوّد يحرّر الاستدعاء المنتظَر حلقة الأحداث لطلبات أخرى - فالاستدعاء مقيَّد بالإدخال والإخراج من منظور خادمك."),
        expected=STATIC_NOTE,
        reflect=("What would go wrong if you used a synchronous client inside this async route?",
                 "ما الذي سيفسد لو استخدمت عميلًا متزامنًا داخل هذا المسار غير المتزامن؟"),
    ),
    "COURSE-010.M01.L05.EX04": Guided(
        goal=("Fix a route that blocks the event loop, in three valid ways.",
              "أصلح مسارًا يحجب حلقة الأحداث بثلاث طرق صحيحة."),
        steps=(
            ("Await an async client inside the async route.", "انتظر عميلًا غير متزامن داخل المسار غير المتزامن."),
            ("Call the sync client from a plain `def` route.", "استدعِ العميل المتزامن من مسار `def` عادي."),
            ("Move the blocking call to a worker thread.", "انقل الاستدعاء الحاجب إلى خيط عامل (worker thread)."),
        ),
        starter='''from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool

app = FastAPI()

# The bug: sync_client.generate() blocks inside an async route and freezes every other request.

# Fix 1: an async client, awaited
@app.get("/chat")
async def chat():
    result = await ___
    return result

# Fix 2: a plain def route - FastAPI runs it in a worker thread for you
@app.get("/chat-sync")
def chat_sync():
    result = ___
    return result

# Fix 3: keep the async route, but run the blocking call in the thread pool
@app.get("/chat-threaded")
async def chat_threaded():
    result = await ___
    return result
''',
        answers=('async_client.generate("hello")', 'sync_client.generate("hello")', 'run_in_threadpool(sync_client.generate, "hello")'),
        blanks=(
            ("await `async_client.generate(\"hello\")`.", "انتظر `async_client.generate(\"hello\")`."),
            ("a plain route may call `sync_client.generate(\"hello\")` directly.", "يمكن للمسار العادي استدعاء `sync_client.generate(\"hello\")` مباشرة."),
            ("pass the function and its argument: `run_in_threadpool(sync_client.generate, \"hello\")`.", "مرّر الدالة ووسيطها: `run_in_threadpool(sync_client.generate, \"hello\")`."),
        ),
        hints=(
            ("Only awaitable calls belong after `await`.", "لا يُكتب بعد `await` إلا الاستدعاءات القابلة للانتظار."),
            ("FastAPI runs `def` routes in a thread pool, so blocking there is fine.", "يشغّل FastAPI مسارات `def` في مجمّع خيوط، لذا لا بأس بالحجب هناك."),
            ("`run_in_threadpool(func, *args)` calls `func` in another thread and returns an awaitable.", "يستدعي `run_in_threadpool(func, *args)` الدالة في خيط آخر ويعيد عنصرًا قابلًا للانتظار."),
        ),
        success=("Correct! All three versions keep the event loop free; when an async SDK exists, Fix 1 is usually the best choice.",
                 "صحيح! تُبقي النسخ الثلاث حلقة الأحداث حرة؛ وعند توفر SDK غير متزامن يكون الإصلاح 1 عادةً الخيار الأفضل."),
        expected=STATIC_NOTE,
    ),
    "COURSE-010.M01.L05.EX06": Guided(
        goal=("Implement a vector repository `search` that scores, filters by a threshold, ranks and limits results.",
              "نفّذ الدالة `search` لمستودع متجهات، بحيث تحسب الدرجات وترشّح بعتبة وترتّب وتحدّ النتائج."),
        steps=(
            ("Score every stored point and keep its text and source.", "احسب درجة كل نقطة مخزّنة واحتفظ بنصها ومصدرها."),
            ("Drop results below the similarity threshold.", "احذف النتائج التي تقل عن عتبة التشابه."),
            ("Sort best first and keep at most `retrieval_limit`.", "رتّب من الأفضل واحتفظ بما لا يزيد على `retrieval_limit`."),
        ),
        starter='''import numpy as np

COLLECTIONS = {"docs": [
    {"vector": [0.9, 0.1, 0.0], "text": "FastAPI supports async routes.", "source": "fastapi.md"},
    {"vector": [0.8, 0.3, 0.1], "text": "Use async clients for model providers.", "source": "providers.md"},
    {"vector": [0.1, 0.9, 0.2], "text": "Qdrant stores vectors in collections.", "source": "qdrant.md"},
    {"vector": [0.0, 0.2, 0.9], "text": "Docker images package services.", "source": "docker.md"},
]}

def cosine(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

def search(collection_name, query_vector, retrieval_limit=3, score_threshold=0.5):
    points = COLLECTIONS[collection_name]
    # Step 1: one result per point: rounded score, original text, source metadata
    scored = [___ for point in points]
    # Step 2: keep results at or above the threshold
    scored = [result for result in scored if ___]
    # Step 3: best first, at most retrieval_limit results
    return ___

for result in search("docs", [1.0, 0.2, 0.0]):
    print(result)
''',
        answers=(
            '{"score": round(cosine(query_vector, point["vector"]), 3), "text": point["text"], "source": point["source"]}',
            'result["score"] >= score_threshold',
            'sorted(scored, key=lambda result: result["score"], reverse=True)[:retrieval_limit]',
        ),
        checks=(
            check("sorted(search('docs', [1.0, 0.2, 0.0])[0]) == ['score', 'source', 'text'] and search('docs', [1.0, 0.2, 0.0])[0]['text'] == 'FastAPI supports async routes.'", True,
                  "Blank 1: each result is a dictionary with `score`, `text` and `source`.", "الفراغ 1: كل نتيجة قاموس يحتوي على `score` و`text` و`source`."),
            check("[r['source'] for r in search('docs', [1.0, 0.2, 0.0])]", ["fastapi.md", "providers.md"],
                  "Blank 2: keep a result only when its score is at least `score_threshold`.",
                  "الفراغ 2: احتفظ بالنتيجة فقط عندما تكون درجتها `score_threshold` على الأقل."),
            check("[[r['source'] for r in search('docs', [0.0, 1.0, 0.3], retrieval_limit=k, score_threshold=0.0)] for k in (1, 2)]",
                  [["qdrant.md"], ["qdrant.md", "docker.md"]],
                  "Blank 3: sort by score from high to low, then slice to `retrieval_limit`.",
                  "الفراغ 3: رتّب حسب الدرجة تنازليًا، ثم اقطع إلى `retrieval_limit`."),
        ),
        hints=(
            ("Build the dictionary inside the list comprehension from `point` and `cosine(...)`.", "ابنِ القاموس داخل الـ list comprehension من `point` و`cosine(...)`."),
            ("The threshold removes weak matches before ranking.", "تحذف العتبة المطابقات الضعيفة قبل الترتيب."),
            ("`sorted(..., key=..., reverse=True)[:n]` gives the n best.", "يعطي `sorted(..., key=..., reverse=True)[:n]` أفضل n عناصر."),
        ),
        success=("Correct! The contract is explicit: vectors and settings in; scored text with its source out, filtered and ranked.",
                 "صحيح! أصبح العقد صريحًا: المتجهات والإعدادات تدخل، ويخرج النص المُقيَّم مع مصدره، مرشَّحًا ومرتّبًا."),
        expected=LOGIC_NOTE,
        reflect=("What goes wrong when the limit is too high, the threshold too low, or the threshold too high?",
                 "ما الذي يفسد عندما يكون الحد مرتفعًا جدًا، أو العتبة منخفضة جدًا، أو العتبة مرتفعة جدًا؟"),
    ),
    "COURSE-010.M01.L06.EX02": Guided(
        goal=("Produce a correctly formatted Server-Sent Events stream, word by word, ending with [DONE].",
              "أنتج تدفق Server-Sent Events بتنسيق صحيح، كلمة بكلمة، وينتهي بـ [DONE]."),
        steps=(
            ("Format one SSE message.", "نسّق رسالة SSE واحدة."),
            ("Yield one event per word.", "أعد (yield) حدثًا لكل كلمة."),
            ("Yield the final `[DONE]` event.", "أعد حدث `[DONE]` الأخير."),
        ),
        starter='''def sse_event(data):
    # Step 1: "data: <payload>" followed by a blank line
    return ___

def stream_words(text):
    """FastAPI streams this with StreamingResponse(stream_words(...), media_type="text/event-stream")."""
    for word in text.split():
        # Step 2: send each word as soon as it is ready
        ___
    # Step 3: tell the client the stream is over
    ___

events = list(stream_words("Hello from FastAPI"))
print(events)
''',
        answers=('f"data: {data}\\n\\n"', "yield sse_event(word)", 'yield sse_event("[DONE]")'),
        checks=(
            check("sse_event('x')", "data: x\n\n", "Blank 1: return `f\"data: {data}\\n\\n\"` - the blank line ends the event.",
                  "الفراغ 1: أعد `f\"data: {data}\\n\\n\"` - فالسطر الفارغ ينهي الحدث."),
            check("events[:3]", ["data: Hello\n\n", "data: from\n\n", "data: FastAPI\n\n"],
                  "Blank 2: `yield sse_event(word)` inside the loop.", "الفراغ 2: `yield sse_event(word)` داخل الحلقة."),
            check("events[-1] == 'data: [DONE]\\n\\n' and len(events) == 4", True,
                  "Blank 3: after the loop, `yield sse_event(\"[DONE]\")`.", "الفراغ 3: بعد الحلقة، `yield sse_event(\"[DONE]\")`."),
        ),
        hints=(
            ("An SSE message is `data: ...` plus two newline characters.", "رسالة SSE هي `data: ...` يليها حرفا سطر جديد."),
            ("`yield` hands one value to the client and pauses until the next is requested.", "يسلّم `yield` قيمة واحدة إلى العميل ويتوقف حتى تُطلب التالية."),
            ("The `[DONE]` marker goes after the loop, exactly once.", "توضع علامة `[DONE]` بعد الحلقة مرة واحدة فقط."),
        ),
        success=("Correct! Each word leaves as soon as it is ready, so the browser can render text while generation continues.",
                 "صحيح! تغادر كل كلمة فور جاهزيتها، فيستطيع المتصفح عرض النص بينما يستمر التوليد."),
        expected=(
            "In the service this becomes an `async def` generator with `await asyncio.sleep(...)` between words; the SSE format is exactly the same.",
            "في الخدمة يصبح هذا مولّدًا `async def` مع `await asyncio.sleep(...)` بين الكلمات؛ وتنسيق SSE هو نفسه تمامًا.",
        ),
        reflect=("Why is `yield` a better fit here than returning one final string?", "لماذا يناسب `yield` هنا أكثر من إعادة نص نهائي واحد؟"),
    ),
    "COURSE-010.M01.L06.EX03": Guided(
        goal=("Convert a provider's token stream into SSE events, skipping empty chunks and batching tiny ones.",
              "حوّل تدفق رموز المزوّد إلى أحداث SSE، مع تخطي المقاطع الفارغة وتجميع المقاطع الصغيرة جدًا."),
        steps=(
            ("Skip empty or missing chunks.", "تخطَّ المقاطع الفارغة أو المفقودة."),
            ("Emit once at least `min_chars` characters have accumulated.", "أرسل بمجرد تجمّع `min_chars` حرفًا على الأقل."),
            ("Flush the remainder.", "أرسل ما تبقى."),
            ("End with `[DONE]`.", "اختم بـ `[DONE]`."),
        ),
        starter='''provider_chunks = [{"content": "Fast"}, {"content": ""}, {"content": "API "}, {"content": None},
                   {"content": "streams "}, {"content": "tokens."}]

def provider_stream(prompt):
    """Stand-in for: async for chunk in await client.chat.completions.create(..., stream=True)"""
    yield from provider_chunks

def chat_stream(prompt, min_chars=8):
    buffer = ""
    for chunk in provider_stream(prompt):
        content = chunk["content"]
        # Step 1: providers send empty and None chunks - skip them
        if ___:
            continue
        buffer += content
        # Step 2: throttle - only emit once enough text has accumulated
        if ___:
            yield f"data: {buffer}\\n\\n"
            buffer = ""
    # Step 3: flush whatever is left
    if buffer:
        yield ___
    # Step 4: end the stream
    yield ___

print(list(chat_stream("hi")))
''',
        answers=("not content", "len(buffer) >= min_chars", 'f"data: {buffer}\\n\\n"', '"data: [DONE]\\n\\n"'),
        checks=(
            check("list(chat_stream('hi', min_chars=1))", ["data: Fast\n\n", "data: API \n\n", "data: streams \n\n", "data: tokens.\n\n", "data: [DONE]\n\n"],
                  "Blank 1: skip the chunk when `not content` (that covers both \"\" and None).",
                  "الفراغ 1: تخطَّ المقطع عندما يكون `not content` (وهذا يشمل \"\" وNone)."),
            check("list(chat_stream('hi'))[:2]", ["data: FastAPI \n\n", "data: streams \n\n"],
                  "Blank 2: emit when `len(buffer) >= min_chars`.", "الفراغ 2: أرسل عندما يكون `len(buffer) >= min_chars`."),
            check("list(chat_stream('hi'))[2:]", ["data: tokens.\n\n", "data: [DONE]\n\n"],
                  "Blanks 3-4: flush the buffer as an SSE event, then send `data: [DONE]`.",
                  "الفراغان 3 و4: أرسل محتوى المخزن حدثَ SSE، ثم أرسل `data: [DONE]`."),
        ),
        hints=(
            ("An empty string and None are both falsy, so one `not` check covers both.", "النص الفارغ وNone كلاهما يُعدّ خطأً منطقيًا، لذا يغطيهما فحص واحد بـ `not`."),
            ("Throttling here means fewer, larger events.", "التنظيم هنا يعني أحداثًا أقل عددًا وأكبر حجمًا."),
            ("Every event uses the same `data: ...\\n\\n` format, including the last ones.", "يستخدم كل حدث التنسيق نفسه `data: ...\\n\\n`، بما في ذلك الأخيرة."),
        ),
        success=("Correct! Empty chunks never reach the browser, tiny chunks are batched, and the stream always ends cleanly with [DONE].",
                 "صحيح! لا تصل المقاطع الفارغة إلى المتصفح أبدًا، وتُجمَّع المقاطع الصغيرة، وينتهي التدفق دائمًا بشكل نظيف بـ [DONE]."),
        expected=LOGIC_NOTE,
        reflect=("What happens to this function if the provider returns the whole answer at once instead of a stream?",
                 "ماذا يحدث لهذه الدالة إذا أعاد المزوّد الإجابة كاملة دفعة واحدة بدل التدفق؟"),
    ),
    "COURSE-010.M01.L06.EX05": Guided(
        goal=("Centralize the WebSocket connection lifecycle in a connection manager: connect, disconnect, send and broadcast.",
              "اجمع دورة حياة اتصالات WebSocket في مدير اتصالات: الاتصال وقطعه والإرسال والبث."),
        steps=(
            ("Remember a connection when it connects.", "احفظ الاتصال عند اتصاله."),
            ("Forget it on disconnect by keeping every other connection (safe even if called twice).", "انسَه عند قطع الاتصال بالاحتفاظ بكل الاتصالات الأخرى (وهذا آمن حتى لو استُدعي مرتين)."),
            ("Send a broadcast to every active connection.", "أرسل البث إلى كل اتصال نشط."),
        ),
        starter='''class FakeWebSocket:
    """Records what a fastapi.WebSocket would send (in FastAPI these methods are awaited)."""
    def __init__(self, name):
        self.name, self.accepted, self.sent = name, False, []

    def accept(self):
        self.accepted = True

    def send_text(self, text):
        self.sent.append(text)

class WSConnectionManager:
    def __init__(self):
        self.active_connections = []

    def connect(self, websocket):
        websocket.accept()
        # Step 1: remember the connection
        ___

    def disconnect(self, websocket):
        # Step 2: forget it - keep every connection except this one
        self.active_connections = ___

    def send(self, message, websocket):
        websocket.send_text(message)

    def broadcast(self, message):
        # Step 3: every active connection receives the message
        for connection in ___:
            self.send(message, connection)

manager = WSConnectionManager()
ada, ben = FakeWebSocket("ada"), FakeWebSocket("ben")
manager.connect(ada)
manager.connect(ben)
manager.broadcast("server restarting soon")
manager.disconnect(ada)
manager.disconnect(ada)          # a second disconnect must be harmless
manager.broadcast("back online")
print(ada.sent, ben.sent)
''',
        answers=("self.active_connections.append(websocket)", "[c for c in self.active_connections if c is not websocket]", "self.active_connections"),
        checks=(
            check("[ada.accepted, ben.sent]", [True, ["server restarting soon", "back online"]],
                  "Blanks 1 and 3: append the socket on connect and loop over `self.active_connections` to broadcast.",
                  "الفراغان 1 و3: أضف المقبس عند الاتصال، وكرّر على `self.active_connections` للبث."),
            check("[ada.sent, len(manager.active_connections)]", [["server restarting soon"], 1],
                  "Blank 2: rebuild the list without this socket, e.g. `[c for c in self.active_connections if c is not websocket]`, so it stops receiving broadcasts.",
                  "الفراغ 2: أعد بناء القائمة دون هذا المقبس، مثل `[c for c in self.active_connections if c is not websocket]`، كي يتوقف عن استقبال البث."),
        ),
        hints=(
            ("Use `append` to add; to drop one item, build a new list that keeps every other item (the sandbox blocks `.remove`).", "استخدم `append` للإضافة؛ ولحذف عنصر ابنِ قائمة جديدة تحتفظ بكل العناصر الأخرى (تمنع بيئة التدريب `.remove`)."),
            ("Filtering with `is not websocket` is naturally safe when the socket is already gone.", "الترشيح بـ `is not websocket` آمن تلقائيًا عندما يكون المقبس قد أُزيل مسبقًا."),
            ("Broadcast loops over the manager's own list.", "يكرّر البث على قائمة المدير نفسها."),
        ),
        success=("Correct! The manager owns the list of live sockets, so connecting, leaving and broadcasting all happen in one place.",
                 "صحيح! يملك المدير قائمة المقابس الحية، فيتم الاتصال والمغادرة والبث كلها في مكان واحد."),
        expected=LOGIC_NOTE,
        reflect=("Why is an in-memory list enough for a single-process demo but not for several server instances?",
                 "لماذا تكفي قائمة في الذاكرة لعرض توضيحي بعملية واحدة، لكنها لا تكفي لعدة نسخ من الخادم؟"),
    ),
    "COURSE-010.M01.L06.EX06": Guided(
        goal=("Write a WebSocket endpoint that answers prompt after prompt over one connection and always cleans up.",
              "اكتب نقطة نهاية WebSocket تجيب عن موجّه تلو الآخر عبر اتصال واحد، وتنظّف دائمًا ما خلّفته."),
        steps=(
            ("Keep the connection open in a loop.", "أبقِ الاتصال مفتوحًا داخل حلقة."),
            ("Stream each generated chunk back to the same socket.", "أرسل كل مقطع مولَّد إلى المقبس نفسه فور توليده."),
            ("Catch the client's disconnect.", "التقط قطع العميل للاتصال."),
            ("Always remove the connection.", "احذف الاتصال دائمًا."),
        ),
        starter='''from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
manager = WSConnectionManager()          # the async connection manager from the previous exercise

@app.websocket("/ws/chat")
async def chat(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Step 1: one connection, many prompts
        while ___:
            prompt = await manager.receive(websocket)
            # Step 2: forward every generated chunk as soon as it arrives
            async for chunk in ___:
                await manager.send(chunk, websocket)
    # Step 3: the client closed the tab or lost its network
    except ___:
        pass
    finally:
        # Step 4: cleanup runs whatever happened
        ___
''',
        answers=("True", "llm_client.stream(prompt)", "WebSocketDisconnect", "await manager.disconnect(websocket)"),
        alternatives={4: ("manager.disconnect(websocket)",)},
        blanks=(
            ("loop forever with `while True:`; the disconnect ends it.", "كرّر بلا نهاية بـ `while True:`؛ وقطع الاتصال ينهيها."),
            ("iterate over `llm_client.stream(prompt)`.", "كرّر على `llm_client.stream(prompt)`."),
            ("catch `WebSocketDisconnect`.", "التقط `WebSocketDisconnect`."),
            ("call `await manager.disconnect(websocket)`.", "استدعِ `await manager.disconnect(websocket)`."),
        ),
        hints=(
            ("The receive call inside the loop waits for the next prompt without reopening anything.", "ينتظر استدعاء الاستقبال داخل الحلقة الموجّه التالي دون إعادة فتح أي شيء."),
            ("`async for` consumes an asynchronous stream of chunks.", "يستهلك `async for` تدفقًا غير متزامن من المقاطع."),
            ("Code in `finally` runs after a normal exit, an error or a disconnect.", "يعمل الكود في `finally` بعد الخروج العادي أو الخطأ أو قطع الاتصال."),
        ),
        success=("Correct! Two prompts flow over the same socket - prompt, chunks, prompt, chunks - and the connection is removed however the session ends.",
                 "صحيح! يتدفق موجّهان عبر المقبس نفسه - موجّه ثم مقاطع ثم موجّه ثم مقاطع - ويُحذف الاتصال مهما كانت طريقة انتهاء الجلسة."),
        expected=STATIC_NOTE,
    ),
    "COURSE-010.M01.L07.EX03": Guided(
        goal=("Define the Conversation and Message tables with a one-to-many relationship and a useful index.",
              "عرّف جدولي Conversation وMessage بعلاقة واحد إلى متعدد وفهرس مفيد."),
        steps=(
            ("Mark the conversation's primary key.", "حدّد المفتاح الأساسي للمحادثة."),
            ("Link a conversation to its messages.", "اربط المحادثة برسائلها."),
            ("Point each message at its conversation with a foreign key.", "اجعل كل رسالة تشير إلى محادثتها بمفتاح أجنبي."),
            ("Index that foreign key.", "أنشئ فهرسًا لذلك المفتاح الأجنبي."),
            ("Link a message back to its conversation.", "اربط الرسالة بمحادثتها في الاتجاه المعاكس."),
        ),
        starter='''from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Conversation(Base):
    __tablename__ = "conversations"
    # Step 1: the primary key
    id: Mapped[int] = mapped_column(primary_key=___)
    title: Mapped[str] = mapped_column(String(200))
    model_type: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    # Step 2: one conversation has many messages
    messages: Mapped[list["Message"]] = relationship(back_populates=___)

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    # Steps 3-4: every message belongs to one conversation; we always look messages up by it
    conversation_id: Mapped[int] = mapped_column(ForeignKey(___), index=___)
    prompt: Mapped[str]
    response: Mapped[str | None]
    prompt_tokens: Mapped[int | None]
    response_tokens: Mapped[int | None]
    is_success: Mapped[bool] = mapped_column(default=True)
    status_code: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    # Step 5: the other side of the relationship
    conversation: Mapped["Conversation"] = relationship(back_populates=___)
''',
        answers=("True", '"conversation"', '"conversations.id"', "True", '"messages"'),
        blanks=(
            ("set `primary_key=True`.", "اضبط `primary_key=True`."),
            ("`back_populates` names the attribute on the other class: `\"conversation\"`.", "يسمّي `back_populates` الخاصية في الصنف الآخر: `\"conversation\"`."),
            ("reference `\"conversations.id\"` - table name, dot, column.", "أشِر إلى `\"conversations.id\"` - اسم الجدول ثم نقطة ثم العمود."),
            ("`index=True` speeds up loading a conversation's messages.", "يسرّع `index=True` تحميل رسائل المحادثة."),
            ("back-populate the `\"messages\"` attribute.", "اربط الخاصية `\"messages\"` في الاتجاه المعاكس."),
        ),
        hints=(
            ("Both sides of a relationship name each other with `back_populates`.", "يسمّي كل طرف من طرفي العلاقة الطرف الآخر عبر `back_populates`."),
            ("`ForeignKey` takes \"table.column\", not the class name.", "يأخذ `ForeignKey` الصيغة \"table.column\" لا اسم الصنف."),
            ("Columns you filter or join on often deserve an index.", "الأعمدة التي ترشّح أو تربط عليها كثيرًا تستحق فهرسًا."),
        ),
        success=("Correct! Messages point at their conversation, both sides of the relationship are wired, and the indexed foreign key keeps chat-history queries fast.",
                 "صحيح! تشير الرسائل إلى محادثتها، وطرفا العلاقة موصولان، ويحافظ المفتاح الأجنبي المفهرس على سرعة استعلامات سجل المحادثة."),
        expected=STATIC_NOTE,
    ),
    "COURSE-010.M01.L07.EX04": Guided(
        goal=("Write a FastAPI dependency that yields an async database session, rolls back on errors and always closes it.",
              "اكتب تابعية FastAPI تعطي (yield) جلسة قاعدة بيانات غير متزامنة، وتتراجع عند الأخطاء، وتغلقها دائمًا."),
        steps=(
            ("Create a session.", "أنشئ جلسة."),
            ("Yield it to the route.", "أعطها (yield) للمسار."),
            ("Roll back if the route raised an error.", "تراجع إذا أطلق المسار خطأً."),
            ("Close the session in every case.", "أغلق الجلسة في كل الحالات."),
        ),
        starter='''from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db_session():
    # Step 1: a new session for this request
    session = ___
    try:
        # Step 2: the route runs while we are paused here
        yield ___
    except Exception:
        # Step 3: undo the request's unfinished work
        await ___
        raise                      # let FastAPI turn the error into a response
    finally:
        # Step 4: always give the connection back to the pool
        await ___
''',
        answers=("async_session()", "session", "session.rollback()", "session.close()"),
        blanks=(
            ("call the factory: `async_session()`.", "استدعِ المصنع: `async_session()`."),
            ("yield the `session` itself.", "أعطِ `session` نفسها."),
            ("await `session.rollback()`.", "انتظر `session.rollback()`."),
            ("await `session.close()`.", "انتظر `session.close()`."),
        ),
        hints=(
            ("`async_sessionmaker` returns a factory; calling it gives a session.", "يعيد `async_sessionmaker` مصنعًا، واستدعاؤه يعطي جلسة."),
            ("A `yield` dependency pauses while the route uses the yielded value.", "تتوقف تابعية `yield` مؤقتًا بينما يستخدم المسار القيمة المُعطاة."),
            ("Rollback belongs to the error path; close belongs in `finally`.", "ينتمي التراجع إلى مسار الخطأ، وينتمي الإغلاق إلى `finally`."),
        ),
        success=("Correct! Every request gets its own session, a failure never leaves half-written data behind, and the connection always returns to the pool.",
                 "صحيح! يحصل كل طلب على جلسته الخاصة، ولا يترك الفشل بيانات مكتوبة جزئيًا أبدًا، ويعود الاتصال دائمًا إلى المجمّع."),
        expected=STATIC_NOTE,
        reflect=("Why is explicit commit/rollback control useful when one workflow performs several database operations?",
                 "لماذا يفيد التحكم الصريح في commit/rollback عندما ينفّذ سير عمل واحد عدة عمليات على قاعدة البيانات؟"),
    ),
    "COURSE-010.M01.L07.EX05": Guided(
        goal=("Complete the conversation CRUD routes: a 404 dependency, pagination, commits and the right status codes.",
              "أكمل مسارات CRUD للمحادثات: تابعية 404، والتقسيم إلى صفحات، والحفظ (commit)، ورموز الحالة الصحيحة."),
        steps=(
            ("Raise 404 when a conversation does not exist.", "أطلق 404 عندما لا توجد المحادثة."),
            ("Limit the list to `take` rows.", "حدّد القائمة بعدد `take` من الصفوف."),
            ("Return 201 when a conversation is created.", "أعد 201 عند إنشاء محادثة."),
            ("Commit the new row.", "احفظ الصف الجديد (commit)."),
            ("Return 204 after a delete.", "أعد 204 بعد الحذف."),
        ),
        starter='''from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

router = APIRouter(prefix="/conversations")
# SessionDep, Conversation and the Create/Update/Out schemas come from the lesson

async def get_conversation(conversation_id: int, session: SessionDep) -> Conversation:
    conversation = await session.get(Conversation, conversation_id)
    if conversation is None:
        # Step 1: one reusable "not found"
        raise HTTPException(status_code=___, detail="Conversation not found")
    return conversation

GetConversationDep = Annotated[Conversation, Depends(get_conversation)]

@router.get("")
async def list_conversations(session: SessionDep, skip: int = 0, take: int = 20) -> list[ConversationOut]:
    # Step 2: paginate
    result = await session.execute(select(Conversation).offset(skip).limit(___))
    return [ConversationOut.model_validate(c) for c in result.scalars()]

@router.get("/{conversation_id}")
async def read_conversation(conversation: GetConversationDep) -> ConversationOut:
    return ConversationOut.model_validate(conversation)

# Step 3: "Created"
@router.post("", status_code=___)
async def create_conversation(body: ConversationCreate, session: SessionDep) -> ConversationOut:
    conversation = Conversation(**body.model_dump())
    session.add(conversation)
    # Step 4: make it permanent
    await ___
    await session.refresh(conversation)
    return ConversationOut.model_validate(conversation)

@router.put("/{conversation_id}")
async def update_conversation(body: ConversationUpdate, conversation: GetConversationDep, session: SessionDep) -> ConversationOut:
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(conversation, key, value)
    await session.commit()
    return ConversationOut.model_validate(conversation)

# Step 5: "No Content"
@router.delete("/{conversation_id}", status_code=___)
async def delete_conversation(conversation: GetConversationDep, session: SessionDep) -> None:
    await session.delete(conversation)
    await session.commit()
''',
        answers=("404", "take", "201", "session.commit()", "204"),
        blanks=(
            ("404 means Not Found.", "يعني 404 «غير موجود»."),
            ("limit the query with the `take` parameter.", "حدّد الاستعلام بالمعامل `take`."),
            ("201 means Created.", "يعني 201 «تم الإنشاء»."),
            ("await `session.commit()`.", "انتظر `session.commit()`."),
            ("204 means No Content.", "يعني 204 «لا محتوى»."),
        ),
        hints=(
            ("One dependency raising 404 is reused by read, update and delete.", "تُعاد تابعية واحدة تطلق 404 في القراءة والتحديث والحذف."),
            ("`offset(skip).limit(take)` is classic pagination.", "`offset(skip).limit(take)` هو التقسيم إلى صفحات المعتاد."),
            ("Creating returns 201; deleting with no body returns 204.", "يعيد الإنشاء 201، ويعيد الحذف دون جسم 204."),
        ),
        success=("Correct! Every route shares the same 404 rule, lists are paginated, mutations are committed, and the status codes say exactly what happened.",
                 "صحيح! تشترك كل المسارات في قاعدة 404 نفسها، والقوائم مقسّمة إلى صفحات، والتعديلات محفوظة، ورموز الحالة تقول بالضبط ما حدث."),
        expected=STATIC_NOTE,
    ),
    "COURSE-010.M01.L07.EX06": Guided(
        goal=("Split `delete_conversation_for_user` into repository, service and controller responsibilities.",
              "قسّم `delete_conversation_for_user` إلى مسؤوليات المستودع والخدمة والمتحكّم."),
        steps=(
            ("In the service, raise NotFound for a missing conversation.", "في الخدمة، أطلق NotFound عند غياب المحادثة."),
            ("In the service, raise Forbidden when the user is not the owner.", "في الخدمة، أطلق Forbidden عندما لا يكون المستخدم هو المالك."),
            ("In the service, record an audit event.", "في الخدمة، سجّل حدث تدقيق."),
            ("In the controller, map NotFound to 404.", "في المتحكّم، حوّل NotFound إلى 404."),
        ),
        starter='''class NotFound(Exception):
    pass

class Forbidden(Exception):
    pass

class ConversationRepository:
    """Persistence only - no business rules."""
    def __init__(self, rows):
        self.rows = rows

    def get(self, conversation_id):
        return self.rows.get(conversation_id)

    def delete(self, conversation_id):
        self.rows.pop(conversation_id, None)

class ConversationService:
    """The business workflow: ownership and auditing."""
    def __init__(self, repository, audit_events):
        self.repository, self.audit_events = repository, audit_events

    def delete_conversation_for_user(self, conversation_id, user_id):
        conversation = self.repository.get(conversation_id)
        # Step 1
        if ___:
            raise NotFound(conversation_id)
        # Step 2: only the owner may delete it
        if ___:
            raise Forbidden(conversation_id)
        self.repository.delete(conversation_id)
        # Step 3: record who deleted what
        ___

def delete_endpoint(service, conversation_id, user_id):
    """The controller: turns the outcome into an HTTP status code."""
    try:
        service.delete_conversation_for_user(conversation_id, user_id)
        return 204
    except NotFound:
        # Step 4
        return ___
    except Forbidden:
        return 403

audit = []
service = ConversationService(ConversationRepository({1: {"owner_id": 7}, 2: {"owner_id": 8}}), audit)
print(delete_endpoint(service, 1, 7), delete_endpoint(service, 2, 7), delete_endpoint(service, 99, 7), audit)
''',
        answers=(
            "conversation is None",
            'conversation["owner_id"] != user_id',
            'self.audit_events.append({"action": "conversation_deleted", "conversation_id": conversation_id, "user_id": user_id})',
            "404",
        ),
        checks=(
            check("(lambda s: [delete_endpoint(s, 3, 1), delete_endpoint(s, 3, 2)])(ConversationService(ConversationRepository({3: {'owner_id': 2}}), []))", [403, 204],
                  "Blank 2: raise Forbidden when `conversation[\"owner_id\"]` differs from `user_id`.",
                  "الفراغ 2: أطلق Forbidden عندما يختلف `conversation[\"owner_id\"]` عن `user_id`."),
            check("delete_endpoint(ConversationService(ConversationRepository({}), []), 5, 1)", 404,
                  "Blanks 1 and 4: raise NotFound when the repository returns None, and map it to 404.",
                  "الفراغان 1 و4: أطلق NotFound عندما يعيد المستودع None، وحوّله إلى 404."),
            check("[e['action'] for e in audit] == ['conversation_deleted'] and audit[0]['conversation_id'] == 1 and audit[0]['user_id'] == 7", True,
                  "Blank 3: append an event with `action`, `conversation_id` and `user_id` to `self.audit_events`.",
                  "الفراغ 3: أضف إلى `self.audit_events` حدثًا يحتوي على `action` و`conversation_id` و`user_id`."),
        ),
        hints=(
            ("The repository returns None for a missing row.", "يعيد المستودع None للصف المفقود."),
            ("Ownership compares the stored owner with the requesting user.", "تقارن الملكية المالك المخزَّن بالمستخدم الطالب."),
            ("The audit event is a dictionary with the action, the conversation and the user.", "حدث التدقيق قاموس يحتوي على الإجراء والمحادثة والمستخدم."),
        ),
        success=("Correct! The repository only stores and loads, the service owns the ownership rule and the audit trail, and the controller only translates outcomes into HTTP codes.",
                 "صحيح! يقتصر المستودع على التخزين والتحميل، وتملك الخدمة قاعدة الملكية وسجل التدقيق، ويقتصر المتحكّم على تحويل النتائج إلى رموز HTTP."),
        expected=LOGIC_NOTE,
        reflect=("Why should the ownership check not be buried in a generic repository method?",
                 "لماذا يجب ألا يُدفن فحص الملكية داخل دالة عامة في المستودع؟"),
    ),
    "COURSE-010.M01.L07.EX08": Guided(
        goal=("Stream LLM chunks to the client immediately and persist the complete answer afterwards, without letting a database failure break the stream.",
              "أرسل مقاطع النموذج إلى العميل فورًا واحفظ الإجابة الكاملة بعد ذلك، دون أن يكسر فشلُ قاعدة البيانات التدفق."),
        steps=(
            ("Refuse unknown conversations before streaming anything.", "ارفض المحادثات غير المعروفة قبل إرسال أي شيء."),
            ("Keep a copy of every chunk you stream.", "احتفظ بنسخة من كل مقطع ترسله."),
            ("Save the prompt with the complete response.", "احفظ الموجّه مع الاستجابة الكاملة."),
            ("If saving fails, log it instead of raising.", "إذا فشل الحفظ فسجّله بدل إطلاق خطأ."),
        ),
        starter='''def stream_and_persist(conversation_id, prompt, conversations, llm_chunks, save_message, log):
    # Step 1: validate before the first byte is sent
    if ___:
        raise KeyError("conversation not found")
    collected = []
    for chunk in llm_chunks:
        # Step 2: copy the chunk for persistence, then send it right away
        ___
        yield f"data: {chunk}\\n\\n"
    yield "data: [DONE]\\n\\n"
    # Step 3: the client has everything - now persist prompt + complete response
    try:
        save_message({"conversation_id": conversation_id, "prompt": prompt, "response": ___})
    except Exception as exc:
        # Step 4: the stream is already delivered - record the failure, do not raise
        ___

saved, log = [], []
events = list(stream_and_persist(1, "Hi", {1, 2}, ["Hel", "lo!"], saved.append, log))

def broken_database(record):
    raise RuntimeError("database is down")

events_when_db_fails = list(stream_and_persist(2, "Hi", {1, 2}, ["Ok"], broken_database, log))

try:
    list(stream_and_persist(99, "Hi", {1, 2}, ["x"], saved.append, log))
    unknown_rejected = False
except KeyError:
    unknown_rejected = True
print(events, saved, events_when_db_fails, log, unknown_rejected)
''',
        answers=("conversation_id not in conversations", "collected.append(chunk)", '"".join(collected)', 'log.append(f"persist failed: {exc}")'),
        checks=(
            check("unknown_rejected", True,
                  "Blank 1: raise before streaming when `conversation_id not in conversations`.",
                  "الفراغ 1: أطلق الخطأ قبل الإرسال عندما يكون `conversation_id not in conversations`."),
            check("events", ["data: Hel\n\n", "data: lo!\n\n", "data: [DONE]\n\n"],
                  "Blank 2: append each chunk to `collected` before yielding it.", "الفراغ 2: أضف كل مقطع إلى `collected` قبل إرساله."),
            check("saved", [{"conversation_id": 1, "prompt": "Hi", "response": "Hello!"}],
                  "Blank 3: save the full response: `\"\".join(collected)`.", "الفراغ 3: احفظ الاستجابة كاملة: `\"\".join(collected)`."),
            check("[events_when_db_fails, log]", [["data: Ok\n\n", "data: [DONE]\n\n"], ["persist failed: database is down"]],
                  "Blank 4: append a message to `log` - the already-delivered stream must stay intact.",
                  "الفراغ 4: أضف رسالة إلى `log` - يجب أن يبقى التدفق المُسلَّم سليمًا."),
        ),
        hints=(
            ("Validation must happen before the generator yields anything.", "يجب أن يجري التحقق قبل أن يعطي المولّد أي شيء."),
            ("`\"\".join(list_of_strings)` rebuilds the full text.", "يعيد `\"\".join(list_of_strings)` بناء النص الكامل."),
            ("Inside `except`, append a message to `log` and let the function end normally.", "داخل `except` أضف رسالة إلى `log` ودع الدالة تنتهي بشكل طبيعي."),
        ),
        success=("Correct! The client path (stream) and the persistence path (save after [DONE]) are separate, so a database outage is logged instead of corrupting a response the user already has.",
                 "صحيح! مسار العميل (التدفق) ومسار الحفظ (الحفظ بعد [DONE]) منفصلان، فيُسجَّل تعطل قاعدة البيانات بدل إفساد استجابة وصلت إلى المستخدم بالفعل."),
        expected=LOGIC_NOTE,
    ),
    "COURSE-010.M01.L08.EX06": Guided(
        goal=("Encode a role-permission table and a reusable guard that returns 403 for roles that are not allowed.",
              "رمّز جدول صلاحيات الأدوار وحارسًا قابلًا لإعادة الاستخدام يعيد 403 للأدوار غير المسموح لها."),
        steps=(
            ("Allow the premium text model for moderators and admins.", "اسمح بنموذج النص المميز للمشرفين والمديرين."),
            ("Allow user administration for admins only.", "اسمح بإدارة المستخدمين للمديرين فقط."),
            ("Reject a user whose role is not in the allowed set.", "ارفض المستخدم الذي لا يقع دوره ضمن المجموعة المسموح بها."),
            ("Build the guard from the permission table.", "ابنِ الحارس من جدول الصلاحيات."),
        ),
        starter='''PERMISSIONS = {
    "generate_text": {"USER", "MODERATOR", "ADMIN"},
    # Step 1: the expensive premium model
    "premium_text_model": ___,
    "generate_image": {"MODERATOR", "ADMIN"},
    "view_other_conversations": {"MODERATOR", "ADMIN"},
    # Step 2: managing accounts
    "administer_users": ___,
}

class HTTPError(Exception):
    def __init__(self, status_code):
        self.status_code = status_code

def require_roles(allowed_roles):
    """Like a FastAPI dependency factory: returns a guard that runs before the route."""
    def guard(current_user):
        # Step 3: the role must be one of the allowed roles
        if ___:
            raise HTTPError(403)
        return current_user
    return guard

def call(permission, user):
    # Step 4: the guard for this permission
    guard = require_roles(___)
    try:
        guard(user)
        return 200
    except HTTPError as error:
        return error.status_code

for role in ("USER", "MODERATOR", "ADMIN"):
    print(role, {name: call(name, {"role": role}) for name in PERMISSIONS})
''',
        answers=('{"MODERATOR", "ADMIN"}', '{"ADMIN"}', 'current_user["role"] not in allowed_roles', "PERMISSIONS[permission]"),
        checks=(
            check("[call('premium_text_model', {'role': r}) for r in ('USER', 'MODERATOR', 'ADMIN')]", [403, 200, 200],
                  "Blank 1: the premium model is for `{\"MODERATOR\", \"ADMIN\"}`.", "الفراغ 1: النموذج المميز للدورين `{\"MODERATOR\", \"ADMIN\"}`."),
            check("[call('administer_users', {'role': r}) for r in ('USER', 'MODERATOR', 'ADMIN')]", [403, 403, 200],
                  "Blank 2: only `{\"ADMIN\"}` may administer users.", "الفراغ 2: لا يدير المستخدمين إلا `{\"ADMIN\"}`."),
            check("[call('generate_text', {'role': 'USER'}), call('generate_image', {'role': 'USER'}), call('generate_image', {'role': 'GUEST'})]", [200, 403, 403],
                  "Blanks 3-4: raise 403 when `current_user[\"role\"]` is not in the set from `PERMISSIONS[permission]`.",
                  "الفراغان 3 و4: أطلق 403 عندما لا يكون `current_user[\"role\"]` ضمن المجموعة الآتية من `PERMISSIONS[permission]`."),
        ),
        hints=(
            ("A set literal looks like `{\"A\", \"B\"}`.", "يُكتب حرفي المجموعة هكذا: `{\"A\", \"B\"}`."),
            ("`role not in allowed_roles` is True for every role outside the set - including unknown ones.", "يكون `role not in allowed_roles` صحيحًا لكل دور خارج المجموعة - بما في ذلك الأدوار غير المعروفة."),
            ("Look the allowed roles up in `PERMISSIONS` by the permission name.", "ابحث عن الأدوار المسموح بها في `PERMISSIONS` باسم الصلاحية."),
        ),
        success=("Correct! Access is decided by code before the route runs: unknown and insufficient roles get 403, whatever a prompt might say.",
                 "صحيح! يُحسم الوصول بالكود قبل تشغيل المسار: تحصل الأدوار غير المعروفة وغير الكافية على 403، مهما قال أي موجّه."),
        expected=LOGIC_NOTE,
        reflect=("Why must this rule never live only in an LLM system prompt?", "لماذا يجب ألا تعيش هذه القاعدة في موجّه نظام النموذج اللغوي وحده أبدًا؟"),
    ),
    "COURSE-010.M01.L09.EX02": Guided(
        goal=("Make a topical guardrail's output safe for control flow: accept exactly `allowed` or `disallowed`, and fail closed otherwise.",
              "اجعل مخرج حاجز المواضيع آمنًا لتدفق التحكم: اقبل `allowed` أو `disallowed` بالضبط، وأغلق الطريق في غير ذلك."),
        steps=(
            ("Normalize harmless whitespace and letter case.", "وحّد المسافات غير الضارة وحالة الأحرف."),
            ("Reject every other output.", "ارفض أي مخرج آخر."),
            ("Block the request when the verdict cannot be read.", "احجب الطلب عندما يتعذر قراءة الحكم."),
        ),
        starter='''ALLOWED_TOPICS = ("FastAPI", "API design", "GenAI service engineering")
SYSTEM_PROMPT = (f"You classify questions. Allowed topics: {', '.join(ALLOWED_TOPICS)}. "
                 "Reply with exactly one word: allowed or disallowed.")

class GuardrailError(ValueError):
    pass

def parse_verdict(raw):
    # Step 1: ignore surrounding whitespace and letter case
    verdict = ___
    # Step 2: anything except the two exact labels is an error
    if ___:
        raise GuardrailError(f"unexpected evaluator output: {raw!r}")
    return verdict

def handle(user_query, evaluator):
    try:
        verdict = parse_verdict(evaluator(user_query))
    except GuardrailError:
        # Step 3: fail closed
        return ___
    return "answer" if verdict == "allowed" else "blocked"

print(handle("How do I add a dependency in FastAPI?", lambda q: "allowed"))
print(handle("Write me a poem about cats", lambda q: "disallowed"))

try:
    parse_verdict("Sure, that's allowed!")
    free_text_rejected = False
except GuardrailError:
    free_text_rejected = True
print("free text rejected:", free_text_rejected)
''',
        answers=("raw.strip().lower()", 'verdict not in {"allowed", "disallowed"}', '"blocked"'),
        checks=(
            check("[parse_verdict('  Allowed\\n'), parse_verdict('DISALLOWED')]", ["allowed", "disallowed"],
                  "Blank 1: `raw.strip().lower()` removes whitespace and case differences.", "الفراغ 1: يزيل `raw.strip().lower()` فروق المسافات وحالة الأحرف."),
            check("free_text_rejected", True,
                  "Blank 2: raise GuardrailError for anything that is not exactly `allowed` or `disallowed`.",
                  "الفراغ 2: أطلق GuardrailError لأي شيء ليس `allowed` أو `disallowed` بالضبط."),
            check("[handle('q', lambda q: 'allowed'), handle('q', lambda q: 'disallowed')]", ["answer", "blocked"],
                  "Blank 2: only the exact labels `allowed` and `disallowed` pass.", "الفراغ 2: لا يمر إلا الوسمان `allowed` و`disallowed` بالضبط."),
            check("[handle('q', lambda q: 'Sure! This is allowed.'), handle('q', lambda q: '')]", ["blocked", "blocked"],
                  "Blanks 2-3: free text must raise GuardrailError, and the handler must then return \"blocked\".",
                  "الفراغان 2 و3: يجب أن يطلق النص الحر GuardrailError، ثم يجب أن يعيد المعالج \"blocked\"."),
        ),
        hints=(
            ("String methods can be chained: `.strip().lower()`.", "يمكن تسلسل دوال النصوص: `.strip().lower()`."),
            ("Membership in a two-element set is the whole rule.", "العضوية في مجموعة من عنصرين هي القاعدة كلها."),
            ("When in doubt, a guardrail blocks.", "عند الشك، يحجب الحاجز."),
        ),
        success=("Correct! The application only ever branches on one of two known values; chatty or empty evaluator output blocks the request instead of slipping through.",
                 "صحيح! لا يتفرع التطبيق إلا على إحدى قيمتين معروفتين؛ ويحجب مخرج المقيِّم الثرثار أو الفارغ الطلبَ بدل أن يمرّ."),
        expected=LOGIC_NOTE,
        reflect=("Why should free-form evaluator text never drive application logic directly?", "لماذا يجب ألا يقود نص المقيِّم الحر منطق التطبيق مباشرة أبدًا؟"),
    ),
    "COURSE-010.M01.L09.EX03": Guided(
        goal=("Run the guardrail and the generation concurrently, cancel generation on a disallowed verdict, and never release output early.",
              "شغّل الحاجز والتوليد بالتزامن، وألغِ التوليد عند حكم بالرفض، ولا تُخرج أي نتيجة قبل الأوان."),
        steps=(
            ("Start the guardrail task.", "ابدأ مهمة الحاجز."),
            ("Wake up as soon as either task finishes.", "استيقظ فور انتهاء أي من المهمتين."),
            ("Cancel generation when the request is disallowed.", "ألغِ التوليد عندما يُرفض الطلب."),
            ("Otherwise wait for and return the generation.", "وإلا فانتظر التوليد وأعده."),
        ),
        starter='''import asyncio

REFUSAL = "Sorry, I can only help with FastAPI and GenAI services."

async def guarded_generate(user_query):
    # Step 1: start both tasks at once
    guardrail_task = asyncio.create_task(___)
    generation_task = asyncio.create_task(generate_text(user_query))
    # Step 2: wake up when the first of them finishes
    done, _ = await asyncio.wait({guardrail_task, generation_task}, return_when=___)

    if guardrail_task in done:
        if not guardrail_task.result():
            # Step 3: stop paying for an answer we will never show
            ___
            return REFUSAL
        # Step 4: allowed - only now wait for the model's answer
        return await ___

    # generation finished first: hold its output until the guardrail decides
    if not await guardrail_task:
        return REFUSAL
    return generation_task.result()
''',
        answers=("is_topic_allowed(user_query)", "asyncio.FIRST_COMPLETED", "generation_task.cancel()", "generation_task"),
        blanks=(
            ("pass the coroutine `is_topic_allowed(user_query)`.", "مرّر الدالة المتزامنة `is_topic_allowed(user_query)`."),
            ("use `asyncio.FIRST_COMPLETED`.", "استخدم `asyncio.FIRST_COMPLETED`."),
            ("call `generation_task.cancel()`.", "استدعِ `generation_task.cancel()`."),
            ("await `generation_task`.", "انتظر `generation_task`."),
        ),
        hints=(
            ("`asyncio.create_task(coro)` starts a coroutine without waiting for it.", "يبدأ `asyncio.create_task(coro)` دالة متزامنة دون انتظارها."),
            ("`asyncio.wait(..., return_when=asyncio.FIRST_COMPLETED)` returns as soon as one task is done.", "يعود `asyncio.wait(..., return_when=asyncio.FIRST_COMPLETED)` فور انتهاء مهمة واحدة."),
            ("A task is awaitable, and `.cancel()` stops it.", "المهمة قابلة للانتظار، و`.cancel()` يوقفها."),
        ),
        success=("Correct! Both calls overlap to cut latency, but nothing reaches the user until the guardrail says yes - and a 'no' cancels the generation.",
                 "صحيح! يتداخل الاستدعاءان لتقليل زمن الانتظار، لكن لا يصل شيء إلى المستخدم قبل أن يوافق الحاجز - والرفض يلغي التوليد."),
        expected=STATIC_NOTE,
        reflect=("What is the provider rate-limit downside of starting generation before the guardrail decides?",
                 "ما عيب حدود معدل المزوّد في بدء التوليد قبل أن يحسم الحاجز قراره؟"),
    ),
    "COURSE-010.M01.L09.EX07": Guided(
        goal=("Rate-limit WebSocket prompts per authenticated user with a fixed window, and send a clear rejection when the limit is reached.",
              "حدّد معدل موجّهات WebSocket لكل مستخدم مُصادَق عليه بنافذة ثابتة، وأرسل رفضًا واضحًا عند بلوغ الحد."),
        steps=(
            ("Compute which time window `now` falls into.", "احسب النافذة الزمنية التي يقع فيها `now`."),
            ("Refuse once the user has used up the window.", "ارفض بمجرد أن يستنفد المستخدم النافذة."),
            ("Key the limit by the user ID.", "اربط الحد بمعرّف المستخدم."),
        ),
        starter='''class FixedWindowLimiter:
    def __init__(self, limit, window_seconds):
        self.limit, self.window = limit, window_seconds
        self.counts = {}                    # (user_id, window index) -> prompts used

    def allow(self, user_id, now):
        # Step 1: e.g. with 60 s windows, seconds 0-59 are window 0, 60-119 window 1
        window_index = ___
        key = (user_id, window_index)
        # Step 2: refuse once this user has used every prompt in the window
        if ___:
            return False
        self.counts[key] = self.counts.get(key, 0) + 1
        return True

limiter = FixedWindowLimiter(limit=3, window_seconds=60)

def on_prompt(user, prompt, now, sent):
    # Step 3: limit the authenticated user, not the socket or the IP address
    if not limiter.allow(___, now):
        sent.append("Rate limit reached - try again in a minute.")
        return
    for chunk in ("Fast", "API"):
        sent.append(chunk)      # endpoint: await websocket.send_text(chunk); await asyncio.sleep(0.05)

sent = []
for second in (1, 5, 10, 20, 61):
    on_prompt({"id": "u1"}, "hi", second, sent)
print(sent)
''',
        answers=("int(now // self.window)", "self.counts.get(key, 0) >= self.limit", 'user["id"]'),
        checks=(
            check("(lambda l: [l.allow('a', t) for t in (0, 1, 2, 3)])(FixedWindowLimiter(3, 60))", [True, True, True, False],
                  "Blanks 1-2: within one window, the fourth prompt must be refused.", "الفراغان 1 و2: داخل النافذة الواحدة يجب رفض الموجّه الرابع."),
            check("(lambda l: [l.allow('a', 1), l.allow('a', 2), l.allow('a', 61)])(FixedWindowLimiter(2, 60))", [True, True, True],
                  "Blank 1: a new window starts at 60 s: `int(now // self.window)`.", "الفراغ 1: تبدأ نافذة جديدة عند 60 ثانية: `int(now // self.window)`."),
            check("sent", ["Fast", "API", "Fast", "API", "Fast", "API", "Rate limit reached - try again in a minute.", "Fast", "API"],
                  "Blank 3: pass the authenticated `user[\"id\"]` to the limiter.", "الفراغ 3: مرّر `user[\"id\"]` الخاص بالمستخدم المُصادَق عليه إلى المحدِّد."),
            check("(lambda s: [on_prompt({'id': 'x'}, 'p', 1, s) for _ in range(4)] and on_prompt({'id': 'y'}, 'p', 1, s) or s[-2:])([])", ["Fast", "API"],
                  "Blank 3: each user has their own budget - another user must not be blocked.", "الفراغ 3: لكل مستخدم رصيده الخاص - يجب ألا يُحجب مستخدم آخر."),
        ),
        hints=(
            ("Integer division `now // window` numbers the windows 0, 1, 2, ...", "يرقّم القسم الصحيح `now // window` النوافذ 0، 1، 2، ..."),
            ("`dict.get(key, 0)` treats an unseen key as zero prompts used.", "يعامل `dict.get(key, 0)` المفتاح غير المرئي بوصفه صفر موجّهات مستخدمة."),
            ("The user's identity is in `user[\"id\"]`.", "هوية المستخدم موجودة في `user[\"id\"]`."),
        ),
        success=("Correct! The rate limit caps how many prompts each user may send; the separate stream throttle only paces the chunks of an accepted answer.",
                 "صحيح! يحدّ معدل الطلبات عدد الموجّهات التي يرسلها كل مستخدم، بينما ينظّم تنظيم التدفق المنفصل سرعة مقاطع الإجابة المقبولة فقط."),
        expected=LOGIC_NOTE,
        reflect=("Why do the rate limit and the stream throttle solve different problems?", "لماذا يحل تحديد المعدل وتنظيم التدفق مشكلتين مختلفتين؟"),
    ),
    "COURSE-010.M01.L10.EX02": Guided(
        goal=("Prepare an overnight batch job: one JSONL request per product with a `custom_id`, then match results back by that id.",
              "جهّز مهمة دفعية ليلية: طلب JSONL لكل منتج مع `custom_id`، ثم طابق النتائج بذلك المعرّف."),
        steps=(
            ("Give every request a unique `custom_id`.", "امنح كل طلب `custom_id` فريدًا."),
            ("Write the requests as JSON Lines.", "اكتب الطلبات بصيغة JSON Lines."),
            ("Find each result's product through its `custom_id`.", "جد منتج كل نتيجة عبر `custom_id` الخاص بها."),
        ),
        starter='''import json

products = [
    {"sku": "A-1", "description": "Wireless earbuds with a charging case"},
    {"sku": "B-7", "description": "Stainless steel chef's knife"},
    {"sku": "C-3", "description": "Organic green tea, 50 bags"},
]

def build_request(product):
    return {
        # Step 1: lets us match the result to this product later
        "custom_id": ___,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o-mini",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": 'Return JSON: {"category": "electronics" | "kitchen" | "grocery"}'},
                {"role": "user", "content": product["description"]},
            ],
        },
    }

# Step 2: JSON Lines - one request per line, ready to upload
batch_file = ___

# What the provider returns later: results in ANY order, each carrying its custom_id
def provider_result(custom_id, category):
    content = json.dumps({"category": category})
    return {"custom_id": custom_id, "response": {"body": {"choices": [{"message": {"content": content}}]}}}
results_jsonl = "\\n".join(json.dumps(r) for r in [
    provider_result("product-C-3", "grocery"), provider_result("product-A-1", "electronics"),
    provider_result("product-B-7", "kitchen"),
])

by_id = {build_request(p)["custom_id"]: p for p in products}
categories = {}
for line in results_jsonl.splitlines():
    result = json.loads(line)
    # Step 3: the original record for this result
    product = ___
    categories[product["sku"]] = json.loads(result["response"]["body"]["choices"][0]["message"]["content"])["category"]
print(categories)
''',
        answers=('f"product-{product[\'sku\']}"', '"\\n".join(json.dumps(build_request(p)) for p in products)', 'by_id[result["custom_id"]]'),
        checks=(
            check("[build_request(p)['custom_id'] for p in products]", ["product-A-1", "product-B-7", "product-C-3"],
                  "Blank 1: build the id from the SKU: `f\"product-{product['sku']}\"`.", "الفراغ 1: ابنِ المعرّف من رمز المنتج: `f\"product-{product['sku']}\"`."),
            check("[json.loads(line)['custom_id'] for line in batch_file.splitlines()]", ["product-A-1", "product-B-7", "product-C-3"],
                  "Blank 2: join one `json.dumps(build_request(p))` per line with `\"\\n\"`.", "الفراغ 2: اجمع `json.dumps(build_request(p))` لكل منتج في سطر مستقل باستخدام `\"\\n\"`."),
            check("categories", {"A-1": "electronics", "B-7": "kitchen", "C-3": "grocery"},
                  "Blank 3: look the product up with `by_id[result[\"custom_id\"]]` - never rely on the order of results.",
                  "الفراغ 3: ابحث عن المنتج بـ `by_id[result[\"custom_id\"]]` - ولا تعتمد أبدًا على ترتيب النتائج."),
        ),
        hints=(
            ("The SKU is already unique, so it makes a good basis for the id.", "رمز المنتج فريد بالفعل، لذا يصلح أساسًا للمعرّف."),
            ("`json.dumps` turns one request into one line of text.", "يحوّل `json.dumps` طلبًا واحدًا إلى سطر نصي واحد."),
            ("Results come back in any order; the id is the only reliable link.", "تعود النتائج بأي ترتيب؛ والمعرّف هو الرابط الموثوق الوحيد."),
        ),
        success=("Correct! Every request carries an id, the whole job travels as one JSONL file, and results are matched by id even though they came back shuffled.",
                 "صحيح! يحمل كل طلب معرّفًا، وتنتقل المهمة كلها ملفَّ JSONL واحدًا، وتُطابق النتائج بالمعرّف رغم عودتها بترتيب مختلط."),
        expected=LOGIC_NOTE,
        reflect=("Why is a batch job better than keeping 20,000 interactive requests open overnight?",
                 "لماذا تكون المهمة الدفعية أفضل من إبقاء 20,000 طلب تفاعلي مفتوحة طوال الليل؟"),
    ),
    "COURSE-010.M01.L10.EX03": Guided(
        goal=("Add a guard to a semantic cache so a similar-sounding prompt with different parameters is never answered from cache.",
              "أضف حارسًا إلى ذاكرة التخزين المؤقت الدلالية كي لا يُجاب أبدًا من الذاكرة عن موجّه متشابه الصياغة لكنه مختلف المعاملات."),
        steps=(
            ("Extract every number from a prompt.", "استخرج كل رقم من الموجّه."),
            ("Treat prompts as similar when the score reaches the threshold.", "اعتبر الموجّهين متشابهين عندما تبلغ الدرجة العتبة."),
            ("Require the numbers to match too.", "اشترط تطابق الأرقام أيضًا."),
            ("Reuse only when both conditions hold.", "أعد الاستخدام فقط عندما يتحقق الشرطان."),
        ),
        starter='''import re

# (cached prompt, new prompt, embedding similarity from the cache's model)
pairs = {
    "A": ("How do I build a FastAPI GenAI service?",
          "What is the process for building GenAI services with FastAPI?", 0.93),
    "B": ("Summarize this article in 100 words.", "Summarize this article in 50 words.", 0.97),
    "C": ("Show orders from the last 7 days.", "Show orders from the last 30 days.", 0.95),
}

# Step 1: all numbers in a prompt, in order
def numbers(text):
    return ___

def safe_to_reuse(cached_prompt, new_prompt, score, threshold=0.9):
    # Step 2: similar enough?
    similar = ___
    # Step 3: same parameters (word limits, date ranges, quantities)?
    same_parameters = ___
    # Step 4: reuse only if both hold
    return ___

print({name: safe_to_reuse(*pair) for name, pair in pairs.items()})
''',
        answers=(r're.findall(r"\d+", text)', "score >= threshold", "numbers(cached_prompt) == numbers(new_prompt)", "similar and same_parameters"),
        checks=(
            check("[numbers('last 7 days'), numbers('in 100 or 50 words'), numbers('no digits')]", [["7"], ["100", "50"], []],
                  "Blank 1: `re.findall(r\"\\d+\", text)` returns every run of digits.", "الفراغ 1: تعيد `re.findall(r\"\\d+\", text)` كل سلسلة أرقام."),
            check("{name: safe_to_reuse(*pair) for name, pair in pairs.items()}", {"A": True, "B": False, "C": False},
                  "Blanks 2-4: pair A is safe; B and C are similar but their numbers differ, so they must not reuse the cached answer.",
                  "الفراغات 2-4: الزوج A آمن؛ أما B وC فمتشابهان لكن أرقامهما مختلفة، لذا يجب ألا يعيدا استخدام الإجابة المخزّنة."),
            check("[safe_to_reuse('hi there', 'hello there', 0.5), safe_to_reuse('top 3', 'top 3', 0.95)]", [False, True],
                  "Blanks 2 and 4: a low score must never be reused, even with matching numbers.",
                  "الفراغان 2 و4: يجب ألا تُعاد أبدًا الدرجة المنخفضة، حتى مع تطابق الأرقام."),
        ),
        hints=(
            ("`\\d+` matches one or more digits.", "يطابق `\\d+` رقمًا واحدًا أو أكثر."),
            ("Compare the score with the threshold using `>=`.", "قارن الدرجة بالعتبة باستخدام `>=`."),
            ("Lists compare element by element with `==`.", "تُقارن القوائم عنصرًا بعنصر باستخدام `==`."),
        ),
        success=("Correct! High similarity alone would have served a 100-word summary for a 50-word request and last week's orders for a 30-day query; the parameter check prevents both.",
                 "صحيح! كان التشابه العالي وحده سيقدّم ملخصًا من 100 كلمة لطلب 50 كلمة، وطلبات الأسبوع الماضي لاستعلام عن 30 يومًا؛ ويمنع فحص المعاملات الحالتين."),
        expected=LOGIC_NOTE,
        reflect=("For pairs B and C, would caching the retrieved context instead of the final answer be safer? Why?",
                 "في الزوجين B وC، هل يكون تخزين السياق المسترجَع بدل الإجابة النهائية أكثر أمانًا؟ ولماذا؟"),
    ),
    "COURSE-010.M01.L10.EX04": Guided(
        goal=("Measure hit rate and false-hit rate for three cache thresholds, then implement LRU eviction.",
              "قِس معدل الإصابة ومعدل الإصابة الخاطئة لثلاث عتبات في ذاكرة التخزين المؤقت، ثم نفّذ الإخلاء وفق LRU."),
        steps=(
            ("Count a hit when the distance is within the threshold.", "احسب إصابة عندما تقع المسافة ضمن العتبة."),
            ("Compute the share of hits that served a wrong answer.", "احسب نسبة الإصابات التي قدّمت إجابة خاطئة."),
            ("On a hit, mark the entry as most recently used.", "عند الإصابة، علّم العنصر بوصفه الأحدث استخدامًا."),
            ("When full, evict the least recently used entry.", "عند الامتلاء، أخلِ العنصر الأقدم استخدامًا."),
        ),
        starter='''from collections import OrderedDict

# (Euclidean distance to the nearest cached query, was reusing its answer actually correct?)
observations = [(0.05, True), (0.12, True), (0.18, True), (0.22, False),
                (0.30, True), (0.35, False), (0.45, False), (0.60, False)]

def evaluate(threshold):
    # Step 1: smaller distance = closer match, so a hit is distance <= threshold
    hits = [correct for distance, correct in observations if ___]
    hit_rate = len(hits) / len(observations)
    # Step 2: share of hits that served a wrong answer (0.0 when there are no hits)
    false_hit_rate = ___
    return round(hit_rate, 3), round(false_hit_rate, 3)

results = {name: evaluate(t) for name, t in (("strict", 0.15), ("medium", 0.25), ("permissive", 0.40))}
print(results)

class LRUCache:
    def __init__(self, capacity):
        self.capacity, self.items = capacity, OrderedDict()

    def get(self, key):
        if key not in self.items:
            return None
        # Step 3: a hit makes this entry the most recently used
        ___
        return self.items[key]

    def put(self, key, value):
        self.items[key] = value
        self.items.move_to_end(key)
        if len(self.items) > self.capacity:
            # Step 4: drop the least recently used entry (the first one)
            ___

cache = LRUCache(2)
cache.put("q1", "a1")
cache.put("q2", "a2")
cache.get("q1")
cache.put("q3", "a3")          # evicts q2, the least recently used
print(list(cache.items))
''',
        answers=("distance <= threshold", "hits.count(False) / len(hits) if hits else 0.0",
                 "self.items.move_to_end(key)", "self.items.popitem(last=False)"),
        checks=(
            check("results", {"strict": [0.25, 0.0], "medium": [0.5, 0.25], "permissive": [0.75, 0.333]},
                  "Blanks 1-2: count observations with `distance <= threshold`; the false-hit rate is wrong hits ÷ hits.",
                  "الفراغان 1 و2: عُدّ الملاحظات التي `distance <= threshold`؛ ومعدل الإصابة الخاطئة = الإصابات الخاطئة ÷ الإصابات."),
            check("evaluate(0.01)", [0.0, 0.0], "Blank 2: with no hits the false-hit rate is 0.0, not a division by zero.",
                  "الفراغ 2: عند غياب الإصابات يكون معدل الإصابة الخاطئة 0.0، لا قسمة على صفر."),
            check("list(cache.items)", ["q1", "q3"],
                  "Blanks 3-4: `move_to_end(key)` on a hit; `popitem(last=False)` removes the oldest entry.",
                  "الفراغان 3 و4: `move_to_end(key)` عند الإصابة، و`popitem(last=False)` يحذف أقدم عنصر."),
        ),
        hints=(
            ("With Euclidean distance, 0 means identical.", "مع المسافة الإقليدية، تعني 0 التطابق التام."),
            ("`list.count(False)` counts the wrong answers among the hits.", "يعدّ `list.count(False)` الإجابات الخاطئة بين الإصابات."),
            ("An OrderedDict keeps insertion order: its front is the oldest entry.", "يحافظ OrderedDict على ترتيب الإدراج: مقدمته هي أقدم عنصر."),
        ),
        success=("Correct! Looser thresholds raise the hit rate and the false-hit rate together, and the LRU cache keeps the questions people keep asking.",
                 "صحيح! ترفع العتبات الأكثر تساهلًا معدل الإصابة ومعدل الإصابة الخاطئة معًا، وتحتفظ ذاكرة LRU بالأسئلة التي يكررها الناس."),
        expected=LOGIC_NOTE,
        reflect=("Which threshold would you pick for an FAQ assistant, and which metrics would you track in production?",
                 "أي عتبة ستختار لمساعد أسئلة شائعة؟ وما المقاييس التي ستتابعها في بيئة الإنتاج؟"),
    ),
    "COURSE-010.M01.L10.EX06": Guided(
        goal=("Replace prompt-only JSON with a Pydantic schema passed to the provider as a structured-output format.",
              "استبدل JSON المعتمد على الموجّه فقط بمخطط Pydantic يُمرَّر إلى المزوّد بوصفه تنسيق مخرجات منظَّم."),
        steps=(
            ("Bound `confidence` between 0 and 1.", "حدّد `confidence` بين 0 و1."),
            ("Pass the model as the response format.", "مرّر النموذج بوصفه تنسيق الاستجابة."),
            ("Read the parsed, validated object.", "اقرأ الكائن المحلَّل والمُتحقَّق منه."),
            ("Without native support, validate the raw JSON yourself.", "دون دعم أصلي، تحقّق من JSON الخام بنفسك."),
        ),
        starter='''from typing import Annotated, Literal

from openai import OpenAI
from pydantic import BaseModel, Field

class DocumentClassification(BaseModel):
    category: Literal["invoice", "contract", "report", "other"]
    # Step 1: a probability between 0 and 1
    confidence: Annotated[float, Field(ge=___, le=___)]
    reason: str

client = OpenAI()
completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": "Classify the document."},
              {"role": "user", "content": document_text}],
    # Step 2: the Pydantic model becomes the output schema
    response_format=___,
)
# Step 3: already an instance of DocumentClassification
result = ___

# Step 4: a provider without schema support - ask for JSON, then validate it yourself
fallback = ___
''',
        answers=("0.0", "1.0", "DocumentClassification", "completion.choices[0].message.parsed",
                 "DocumentClassification.model_validate_json(raw_text)"),
        alternatives={1: ("0",), 2: ("1",)},
        blanks=(
            ("the lower bound is `0.0`.", "الحد الأدنى `0.0`."),
            ("the upper bound is `1.0`.", "الحد الأعلى `1.0`."),
            ("pass the class `DocumentClassification` itself.", "مرّر الصنف `DocumentClassification` نفسه."),
            ("read `completion.choices[0].message.parsed`.", "اقرأ `completion.choices[0].message.parsed`."),
            ("use `DocumentClassification.model_validate_json(raw_text)`.", "استخدم `DocumentClassification.model_validate_json(raw_text)`."),
        ),
        hints=(
            ("`ge` and `le` give inclusive bounds.", "يعطي `ge` و`le` حدودًا شاملة."),
            ("`response_format` takes the class, not an instance.", "يأخذ `response_format` الصنف لا نسخة منه."),
            ("Every Pydantic model can validate JSON text with `model_validate_json`.", "يستطيع كل نموذج Pydantic التحقق من نص JSON عبر `model_validate_json`."),
        ),
        success=("Correct! The schema constrains generation where the provider supports it and validates the result either way - far stronger than pulling fields out of prose with regular expressions.",
                 "صحيح! يقيّد المخطط التوليد حين يدعمه المزوّد، ويتحقق من النتيجة في كل الأحوال - وهذا أقوى بكثير من استخراج الحقول من النثر بالتعابير النمطية."),
        expected=STATIC_NOTE,
    ),
    "COURSE-010.M01.L11.EX03": Guided(
        goal=("Write two focused pytest unit tests for the chunker, in Given-When-Then form.",
              "اكتب اختبارَي وحدة مركّزين بـ pytest لدالة التقطيع، بصيغة Given-When-Then."),
        steps=(
            ("Call `chunk` with the given tokens and size 2.", "استدعِ `chunk` مع الرموز المعطاة والحجم 2."),
            ("Assert the complete expected value.", "تحقّق من القيمة المتوقعة كاملة."),
            ("Expect a ValueError for an invalid size.", "توقّع ValueError عند الحجم غير الصالح."),
            ("Pass the invalid size 0.", "مرّر الحجم غير الصالح 0."),
        ),
        starter='''import pytest

from rag.chunking import chunk

def test_chunk_splits_tokens_into_pairs():
    # Given
    tokens = [1, 2, 3, 4, 5]
    # When
    result = ___
    # Then: assert the whole value, not just its length
    assert result == ___

def test_chunk_rejects_a_zero_size():
    # Given / When / Then: an invalid size raises ValueError
    with ___:
        chunk([1, 2, 3], ___)
''',
        answers=("chunk(tokens, 2)", "[[1, 2], [3, 4], [5]]", "pytest.raises(ValueError)", "0"),
        alternatives={1: ("chunk(tokens, chunk_size=2)",), 3: ('pytest.raises(ValueError, match="greater than 0")',)},
        blanks=(
            ("call `chunk(tokens, 2)`.", "استدعِ `chunk(tokens, 2)`."),
            ("five tokens in pairs give `[[1, 2], [3, 4], [5]]`.", "خمسة رموز في أزواج تعطي `[[1, 2], [3, 4], [5]]`."),
            ("use `pytest.raises(ValueError)`.", "استخدم `pytest.raises(ValueError)`."),
            ("pass `0` as the chunk size.", "مرّر `0` حجمًا للمقطع."),
        ),
        hints=(
            ("The When step is a single call to the function under test.", "خطوة When استدعاء واحد للدالة قيد الاختبار."),
            ("The last chunk holds the remaining token.", "يحتوي المقطع الأخير على الرمز المتبقي."),
            ("`with pytest.raises(ErrorType):` passes only if the block raises that error.", "لا ينجح `with pytest.raises(ErrorType):` إلا إذا أطلقت الكتلة ذلك الخطأ."),
        ),
        success=("Correct! One test pins down the exact output and the other pins down the failure mode - both run in milliseconds and never call a model.",
                 "صحيح! يثبّت اختبارٌ المخرجَ الدقيق ويثبّت الآخر نمط الفشل - وكلاهما يعمل في أجزاء من الثانية دون استدعاء أي نموذج."),
        expected=("pytest is not installed in the practice sandbox, so Check answer reads your tests instead of running them.",
                  "مكتبة pytest غير مثبّتة في بيئة التدريب، لذلك يقرأ «تحقّق من الإجابة» اختباراتك بدل تشغيلها."),
    ),
    "COURSE-010.M01.L11.EX04": Guided(
        goal=("Turn the chunker tests into parametrized tests that cover valid sizes, edge cases and invalid sizes.",
              "حوّل اختبارات دالة التقطيع إلى اختبارات بمعاملات تغطي الأحجام الصالحة والحالات الحدّية والأحجام غير الصالحة."),
        steps=(
            ("Give the expected result when the size is larger than the list.", "اكتب النتيجة المتوقعة عندما يكون الحجم أكبر من القائمة."),
            ("Give the expected result for an empty list.", "اكتب النتيجة المتوقعة لقائمة فارغة."),
            ("List the invalid sizes 0 and -1.", "اذكر الحجمين غير الصالحين 0 و-1."),
            ("Expect a ValueError for them.", "توقّع ValueError لهما."),
        ),
        starter='''import pytest

from rag.chunking import chunk

@pytest.mark.parametrize(
    "tokens, chunk_size, expected",
    [
        ([1, 2, 3], 1, [[1], [2], [3]]),
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([1, 2, 3], 5, ___),                       # Step 1: size larger than the list
        ([], 2, ___),                              # Step 2: empty input
        (list(range(1000)), 5, [list(range(i, i + 5)) for i in range(0, 1000, 5)]),
    ],
)
def test_chunk_valid_sizes(tokens, chunk_size, expected):
    assert chunk(tokens, chunk_size) == expected

# Step 3: the invalid sizes
@pytest.mark.parametrize("chunk_size", ___)
def test_chunk_rejects_invalid_sizes(chunk_size):
    # Step 4
    with pytest.raises(___):
        chunk([1, 2, 3], chunk_size)
''',
        answers=("[[1, 2, 3]]", "[]", "[0, -1]", "ValueError"),
        alternatives={3: ("[-1, 0]", "(0, -1)", "(-1, 0)")},
        blanks=(
            ("one chunk holding everything: `[[1, 2, 3]]`.", "مقطع واحد يحتوي على كل شيء: `[[1, 2, 3]]`."),
            ("no tokens means no chunks: `[]`.", "لا رموز تعني لا مقاطع: `[]`."),
            ("list both invalid sizes: `[0, -1]`.", "اذكر الحجمين غير الصالحين: `[0, -1]`."),
            ("the chunker raises `ValueError`.", "تطلق دالة التقطيع `ValueError`."),
        ),
        hints=(
            ("If the size exceeds the list, the whole list is one chunk.", "إذا تجاوز الحجم القائمة فإن القائمة كلها مقطع واحد."),
            ("`range(0, 0, step)` is empty, so the comprehension returns an empty list.", "النطاق `range(0, 0, step)` فارغ، لذا يعيد الـ comprehension قائمة فارغة."),
            ("Every value in the parameter list becomes its own test case.", "تصبح كل قيمة في قائمة المعاملات حالة اختبار مستقلة."),
        ),
        success=("Correct! One test function now checks seven cases, and every failure names the exact input that broke.",
                 "صحيح! أصبحت دالة اختبار واحدة تفحص سبع حالات، وكل فشل يسمّي المدخل المحدد الذي أفسدها."),
        expected=("pytest is not installed in the practice sandbox, so Check answer reads your tests instead of running them.",
                  "مكتبة pytest غير مثبّتة في بيئة التدريب، لذلك يقرأ «تحقّق من الإجابة» اختباراتك بدل تشغيلها."),
    ),
    "COURSE-010.M01.L11.EX05": Guided(
        goal=("Fix the three sources of flakiness in an async test suite: shared state, un-awaited I/O and blocking sleeps.",
              "أصلح المصادر الثلاثة لعدم الاستقرار في مجموعة اختبارات غير متزامنة: الحالة المشتركة، والإدخال والإخراج غير المنتظَر، والانتظار الحاجب."),
        steps=(
            ("Give every test a fresh list.", "امنح كل اختبار قائمة جديدة."),
            ("Await the database save.", "انتظر حفظ قاعدة البيانات."),
            ("Await the database count in the assertion.", "انتظر عدّ قاعدة البيانات في التأكيد."),
            ("Replace the blocking sleep with an async one.", "استبدل الانتظار الحاجب بانتظار غير متزامن."),
        ),
        starter='''import asyncio

import pytest

# Step 1: function-scoped (the default): a NEW list for every test
@pytest.fixture
def records():
    return ___

@pytest.mark.asyncio
async def test_saves_one_record(records, db):
    records.append({"id": 1})
    # Step 2: without await, the test can finish before the save happens
    await ___
    # Step 3: the count is I/O too
    assert ___

@pytest.mark.asyncio
async def test_waits_without_blocking(service):
    service.start()
    # Step 4: time.sleep() would freeze the event loop the service needs
    await ___
    assert service.is_ready()
''',
        answers=("[]", "db.save(records[0])", "await db.count() == 1", "asyncio.sleep(0.1)"),
        alternatives={3: ("1 == await db.count()",)},
        blanks=(
            ("return a new empty list: `[]`.", "أعد قائمة فارغة جديدة: `[]`."),
            ("await `db.save(records[0])`.", "انتظر `db.save(records[0])`."),
            ("assert `await db.count() == 1`.", "تحقّق من `await db.count() == 1`."),
            ("await `asyncio.sleep(0.1)`.", "انتظر `asyncio.sleep(0.1)`."),
        ),
        hints=(
            ("A fixture's return value is created again for every test that uses it.", "تُنشأ القيمة المعادة من الـ fixture من جديد لكل اختبار يستخدمها."),
            ("Every coroutine call needs `await`, including the one inside `assert`.", "يحتاج كل استدعاء لدالة متزامنة إلى `await`، بما في ذلك الاستدعاء داخل `assert`."),
            ("`asyncio.sleep` yields to the event loop; `time.sleep` blocks it.", "`asyncio.sleep` يفسح المجال لحلقة الأحداث، و`time.sleep` يحجبها."),
        ),
        success=("Correct! Each test now starts from the same clean state and waits for its own I/O, so it gives the same result every run - it is idempotent.",
                 "صحيح! يبدأ كل اختبار الآن من الحالة النظيفة نفسها وينتظر عمليات الإدخال والإخراج الخاصة به، فيعطي النتيجة نفسها في كل تشغيل - أي أنه متساوي القوى (idempotent)."),
        expected=("pytest is not installed in the practice sandbox, so Check answer reads your tests instead of running them.",
                  "مكتبة pytest غير مثبّتة في بيئة التدريب، لذلك يقرأ «تحقّق من الإجابة» اختباراتك بدل تشغيلها."),
    ),
    "COURSE-010.M01.L11.EX07": Guided(
        goal=("Compute retrieval precision and recall for one query and read what each one tells you.",
              "احسب دقة الاسترجاع (Precision) والاستدعاء (Recall) لاستعلام واحد، واقرأ ما يخبرك به كلٌّ منهما."),
        steps=(
            ("Find the true-positive document IDs.", "حدّد معرّفات المستندات الإيجابية الصحيحة."),
            ("Compute recall.", "احسب Recall."),
            ("Compute precision.", "احسب Precision."),
        ),
        starter='''expected = [1, 2, 3, 4, 5]     # documents that should be retrieved
retrieved = [2, 3, 6, 7]       # documents the retriever returned

# Step 1: relevant documents that were actually retrieved (sorted)
true_positives = ___
# Step 2: share of the relevant documents that were found
recall = ___
# Step 3: share of the retrieved documents that are relevant
precision = ___
print(true_positives, "recall", recall, "precision", precision)
''',
        answers=("sorted(set(expected) & set(retrieved))", "len(true_positives) / len(expected)", "len(true_positives) / len(retrieved)"),
        checks=(
            check("list(true_positives)", [2, 3], "Blank 1: intersect the two sets and sort the result.", "الفراغ 1: خذ تقاطع المجموعتين ورتّب النتيجة."),
            check("recall", 0.4, "Blank 2: recall divides by the number of EXPECTED documents (5).", "الفراغ 2: يقسم Recall على عدد المستندات المتوقعة (5)."),
            check("precision", 0.5, "Blank 3: precision divides by the number of RETRIEVED documents (4).", "الفراغ 3: يقسم Precision على عدد المستندات المسترجَعة (4)."),
        ),
        hints=(
            ("`set(a) & set(b)` keeps the elements in both.", "يحتفظ `set(a) & set(b)` بالعناصر الموجودة في الاثنين."),
            ("Recall asks: of what we needed, how much did we find?", "يسأل Recall: مما كنا نحتاجه، كم وجدنا؟"),
            ("Precision asks: of what we returned, how much was useful?", "يسأل Precision: مما أعدناه، كم كان مفيدًا؟"),
        ),
        success=("Correct! Recall 0.4 says three relevant documents were missed; precision 0.5 says half of what was retrieved is noise.",
                 "صحيح! يقول Recall بقيمة 0.4 إن ثلاثة مستندات ذات صلة فاتت، ويقول Precision بقيمة 0.5 إن نصف ما استُرجع ضجيج."),
        reflect=("Name one retrieval change that would raise recall but probably lower precision.", "اذكر تغييرًا واحدًا في الاسترجاع يرفع Recall لكنه قد يخفض Precision."),
    ),
    "COURSE-010.M01.L11.EX08": Guided(
        goal=("Write three behavioral tests for an AI tutor: minimum functionality, invariance and directional expectation.",
              "اكتب ثلاثة اختبارات سلوكية لمعلّم ذكي: الحد الأدنى من الوظيفة، والثبات، والتوقع الاتجاهي."),
        steps=(
            ("MFT: a beginner answer keeps sentences short.", "اختبار الحد الأدنى: تبقى جمل الإجابة للمبتدئ قصيرة."),
            ("Invariance: case and small typos do not change the answer.", "الثبات: لا تغيّر حالة الأحرف والأخطاء الإملائية الصغيرة الإجابة."),
            ("Directional: asking for detail makes the answer longer.", "الاتجاهي: طلب التفاصيل يجعل الإجابة أطول."),
        ),
        starter='''def tutor(question):
    """Stand-in for the AI tutor under test."""
    sentences = ["An API lets two programs talk to each other.", "You send a request and get a response."]
    if "detail" in question.lower():
        sentences += ["Requests use methods such as GET and POST.", "Responses carry status codes like 200 or 404."]
    return " ".join(sentences)

def average_sentence_length(text):
    sentences = [s for s in text.split(".") if s.strip()]
    return sum(len(s.split()) for s in sentences) / len(sentences)

# Each test takes the model so it can be pointed at any version of the tutor.

# Step 1: MFT - beginner-friendly answers average at most 15 words per sentence
def test_minimum_functionality(model):
    return ___

# Step 2: INV - case and a small typo must not change the answer
def test_invariance(model):
    return ___

# Step 3: DIR - asking for more detail must produce a longer answer
def test_directional(model):
    return ___

print(test_minimum_functionality(tutor), test_invariance(tutor), test_directional(tutor))
''',
        answers=(
            'average_sentence_length(model("What is an API?")) <= 15',
            'model("What is an API?") == model("what is an APi?")',
            'len(model("Explain APIs in detail").split()) > len(model("Explain APIs").split())',
        ),
        checks=(
            check("[test_minimum_functionality(tutor), test_minimum_functionality(lambda q: 'This answer is one extremely long sentence that keeps going and going and going without ever stopping to let a beginner breathe.')]",
                  [True, False],
                  "Blank 1: compare `average_sentence_length(model(...))` with 15.", "الفراغ 1: قارن `average_sentence_length(model(...))` بالعدد 15."),
            check("[test_invariance(tutor), test_invariance(lambda q: q)]", [True, False],
                  "Blank 2: call the model on two spellings of the same question and compare the answers.",
                  "الفراغ 2: استدعِ النموذج على كتابتين للسؤال نفسه وقارن الإجابتين."),
            check("[test_directional(tutor), test_directional(lambda q: 'Same short answer.')]", [True, False],
                  "Blank 3: the detailed question must give more words than the plain one.", "الفراغ 3: يجب أن يعطي السؤال المفصّل كلمات أكثر من السؤال العادي."),
        ),
        hints=(
            ("Each test returns True when the property holds.", "يعيد كل اختبار True عندما تتحقق الخاصية."),
            ("Invariance compares two outputs for inputs that should mean the same thing.", "يقارن الثبات مخرجين لمدخلين يجب أن يحملا المعنى نفسه."),
            ("A directional test compares a measurement across two inputs.", "يقارن الاختبار الاتجاهي قياسًا بين مدخلين."),
        ),
        success=("Correct! Each test measures a behavior, passes for the tutor and fails for a model that breaks that behavior - no exact-string comparison needed.",
                 "صحيح! يقيس كل اختبار سلوكًا، وينجح مع المعلّم ويفشل مع نموذج يُخلّ بذلك السلوك - دون حاجة إلى مقارنة نصوص حرفية."),
        expected=LOGIC_NOTE,
    ),
    "COURSE-010.M01.L11.EX09": Guided(
        goal=("Write an auto-evaluation test: send a rude input to the support bot, grade the reply with an evaluator, and assert it is not toxic.",
              "اكتب اختبار تقييم تلقائي: أرسل مدخلًا فظًّا إلى بوت الدعم، وقيّم الرد بمقيِّم، وتحقّق من أنه غير مسيء."),
        steps=(
            ("Parse the evaluator's JSON output.", "حلّل مخرج JSON من المقيِّم."),
            ("Send a difficult, rude message to the bot.", "أرسل رسالة صعبة وفظّة إلى البوت."),
            ("Assert that the verdict is not toxic.", "تحقّق من أن الحكم غير مسيء."),
        ),
        starter='''import json

def support_bot(message):
    return "I'm sorry this has been frustrating. Let me check your order status right away."

def evaluator(response):
    """Stand-in for an evaluator model asked for JSON: {"is_toxic": bool, "reason": str}."""
    toxic = any(word in response.lower() for word in ("stupid", "idiot", "shut up"))
    return json.dumps({"is_toxic": toxic, "reason": "insulting language" if toxic else "polite and helpful"})

def parse_evaluation(raw):
    # Step 1: structured evaluator output
    data = ___
    if not (isinstance(data.get("is_toxic"), bool) and isinstance(data.get("reason"), str)):
        raise ValueError("the evaluator returned an invalid verdict")
    return data

def test_bot_stays_respectful(bot):
    # Step 2: a difficult, rude input
    response = bot(___)
    verdict = parse_evaluation(evaluator(response))
    # Step 3: fail the test when the reply is toxic, showing the evaluator's reason
    ___
    return verdict

print(test_bot_stays_respectful(support_bot))
try:
    test_bot_stays_respectful(lambda message: "Shut up, this is your fault.")
    rude_bot_caught = False
except AssertionError:
    rude_bot_caught = True
print("rude bot caught:", rude_bot_caught)
''',
        answers=("json.loads(raw)", '"This is useless, you lost my order again!"', 'assert verdict["is_toxic"] is False, verdict["reason"]'),
        checks=(
            check("parse_evaluation('{\"is_toxic\": false, \"reason\": \"ok\"}')", {"is_toxic": False, "reason": "ok"},
                  "Blank 1: parse with `json.loads(raw)`.", "الفراغ 1: حلّل بـ `json.loads(raw)`."),
            check("(lambda seen: test_bot_stays_respectful(lambda m: seen.append(m) or 'Happy to help.') is not None and isinstance(seen[0], str) and any(w in seen[0].lower() for w in ('useless', 'terrible', 'worst', 'stupid', 'idiot', 'angry', 'lost', 'never', '!')))([])", True,
                  "Blank 2: pass a difficult, rude message string to the bot - for example a complaint ending with '!'.",
                  "الفراغ 2: مرّر إلى البوت رسالة نصية صعبة وفظّة - مثل شكوى تنتهي بعلامة '!'."),
            check("test_bot_stays_respectful(support_bot)['is_toxic']", False,
                  "The polite support bot must pass the test.", "يجب أن ينجح بوت الدعم المهذّب في الاختبار."),
            check("rude_bot_caught", True,
                  "Blank 3: `assert verdict[\"is_toxic\"] is False, verdict[\"reason\"]` so a toxic reply fails the test.",
                  "الفراغ 3: `assert verdict[\"is_toxic\"] is False, verdict[\"reason\"]` كي يُفشل الرد المسيء الاختبار."),
        ),
        hints=(
            ("`json.loads` turns the evaluator's text into a dictionary.", "يحوّل `json.loads` نص المقيِّم إلى قاموس."),
            ("The input should be the kind of message that tempts a bad reply.", "يجب أن يكون المدخل من نوع الرسائل التي تغري بردٍّ سيئ."),
            ("`assert condition, message` fails with the message when the condition is False.", "يفشل `assert condition, message` مع الرسالة عندما يكون الشرط False."),
        ),
        success=("Correct! The test grades behavior through structured evaluator output instead of exact strings - and it really fails for a rude bot.",
                 "صحيح! يقيّم الاختبار السلوك عبر مخرجات مقيِّم منظَّمة بدل النصوص الحرفية - ويفشل فعلًا مع بوت فظ."),
        expected=LOGIC_NOTE,
        reflect=("Give one reason the evaluator itself may be wrong, and one reason this test should not run on every small change.",
                 "اذكر سببًا قد يجعل المقيِّم نفسه مخطئًا، وسببًا لعدم تشغيل هذا الاختبار مع كل تعديل صغير."),
    ),
    "COURSE-010.M01.L12.EX02": Guided(
        goal=("Write a minimal, cache-friendly Dockerfile for a FastAPI service.",
              "اكتب ملف Dockerfile بسيطًا لخدمة FastAPI يستفيد من التخزين المؤقت للطبقات."),
        steps=(
            ("Start from a slim Python image.", "ابدأ من صورة Python مصغّرة."),
            ("Work in `/code`.", "اعمل داخل `/code`."),
            ("Copy `requirements.txt` before the source.", "انسخ `requirements.txt` قبل الكود المصدري."),
            ("Copy the source.", "انسخ الكود المصدري."),
            ("Make Uvicorn listen on all interfaces.", "اجعل Uvicorn يستمع على كل الواجهات."),
        ),
        starter='''# Step 1: a small Python base image
FROM ___
# Step 2: the working directory
WORKDIR ___
# Step 3: dependencies first - this layer stays cached while only source code changes
COPY ___
RUN pip install --no-cache-dir -r requirements.txt
# Step 4: then the application source
COPY ___
EXPOSE 8000
# Step 5: listen on every interface inside the container
CMD ["uvicorn", "main:app", "--host", ___, "--port", "8000"]
''',
        answers=("python:3.12-slim", "/code", "requirements.txt .", ". .", '"0.0.0.0"'),
        alternatives={1: ("python:3.11-slim", "python:3.13-slim"), 3: ("requirements.txt ./", "./requirements.txt .", "requirements.txt /code/"), 4: ("./ ./", ". /code")},
        blanks=(
            ("use a slim image such as `python:3.12-slim`.", "استخدم صورة مصغّرة مثل `python:3.12-slim`."),
            ("set `WORKDIR /code`.", "اضبط `WORKDIR /code`."),
            ("copy only `requirements.txt .` here.", "انسخ `requirements.txt .` فقط هنا."),
            ("copy everything with `. .`.", "انسخ كل شيء بـ `. .`."),
            ("bind to `\"0.0.0.0\"` so traffic from outside the container arrives.", "اربط على `\"0.0.0.0\"` كي تصل الحركة من خارج الحاوية."),
        ),
        hints=(
            ("Slim images leave out compilers and docs you do not need at runtime.", "تستبعد الصور المصغّرة المترجمات والوثائق التي لا تحتاجها أثناء التشغيل."),
            ("Docker reuses a layer until something it copied changes.", "يعيد Docker استخدام الطبقة إلى أن يتغير شيء نسخته."),
            ("`127.0.0.1` inside a container is unreachable from the host.", "العنوان `127.0.0.1` داخل الحاوية لا يمكن الوصول إليه من المضيف."),
        ),
        success=("Correct! Because requirements are installed before the source is copied, editing code rebuilds only the last layers.",
                 "صحيح! لأن المتطلبات تُثبَّت قبل نسخ الكود المصدري، فإن تعديل الكود يعيد بناء الطبقات الأخيرة فقط."),
        expected=("Dockerfiles are checked by reading them: each completed line is compared with the expected instruction, ignoring extra spaces.",
                  "تُفحص ملفات Dockerfile بقراءتها: يُقارن كل سطر مكتمل بالتعليمة المتوقعة مع تجاهل المسافات الزائدة."),
        language="dockerfile",
    ),
    "COURSE-010.M01.L12.EX03": Guided(
        goal=("Stop a container from leaving root-owned files in a bind-mounted folder by running it as your own user with least privilege.",
              "امنع الحاوية من ترك ملفات يملكها root في مجلد مربوط، بتشغيلها بمستخدمك الخاص وبأقل قدر من الصلاحيات."),
        steps=(
            ("Run the service as your host user and group.", "شغّل الخدمة بمستخدم المضيف ومجموعته."),
            ("Bind-mount `./outputs` to `/app/outputs`.", "اربط `./outputs` بـ `/app/outputs`."),
            ("Forbid gaining new privileges.", "امنع اكتساب صلاحيات جديدة."),
        ),
        starter='''services:
  server:
    build: .
    # Step 1: run as your host user instead of root, so files in ./outputs stay yours
    user: ___
    volumes:
      # Step 2: the host folder, mounted into the container
      - ___
    # Step 3: the process may never gain more privileges than it starts with
    security_opt:
      - ___
''',
        answers=('"${UID}:${GID}"', "./outputs:/app/outputs", "no-new-privileges:true"),
        alternatives={1: ('"1000:1000"', "${UID}:${GID}", "1000:1000")},
        blanks=(
            ("use your user and group IDs: `\"${UID}:${GID}\"`.", "استخدم معرّفي المستخدم والمجموعة: `\"${UID}:${GID}\"`."),
            ("map `./outputs:/app/outputs`.", "اربط `./outputs:/app/outputs`."),
            ("add `no-new-privileges:true`.", "أضف `no-new-privileges:true`."),
        ),
        hints=(
            ("Files created in a bind mount belong to the user the process runs as.", "تعود ملكية الملفات المنشأة في المجلد المربوط إلى المستخدم الذي تعمل به العملية."),
            ("A bind mount is `host_path:container_path`.", "الربط بصيغة `host_path:container_path`."),
            ("`security_opt` takes Docker security options such as `no-new-privileges:true`.", "يأخذ `security_opt` خيارات أمان Docker مثل `no-new-privileges:true`."),
        ),
        success=("Correct! Files written to ./outputs now belong to you, and the process cannot escalate - no need for a blanket `chmod 777`.",
                 "صحيح! أصبحت الملفات المكتوبة في ./outputs ملكك، ولا تستطيع العملية رفع صلاحياتها - دون حاجة إلى `chmod 777` شامل."),
        expected=("Compose files are checked by reading them: each completed line is compared with the expected entry, ignoring extra spaces.",
                  "تُفحص ملفات Compose بقراءتها: يُقارن كل سطر مكتمل بالمدخل المتوقع مع تجاهل المسافات الزائدة."),
        reflect=("When would you still need `chown` or `chmod`, and why is making everything world-writable a bad fix?",
                 "متى ستظل تحتاج إلى `chown` أو `chmod`؟ ولماذا يُعدّ جعل كل شيء قابلًا للكتابة للجميع إصلاحًا سيئًا؟"),
        language="yaml",
    ),
    "COURSE-010.M01.L12.EX05": Guided(
        goal=("Describe a FastAPI + PostgreSQL stack in one Compose file with a named volume, a shared network and a secret.",
              "صِف حزمة FastAPI وPostgreSQL في ملف Compose واحد مع وحدة تخزين مسمّاة وشبكة مشتركة وسرّ."),
        steps=(
            ("Build the server from the local Dockerfile.", "ابنِ الخادم من ملف Dockerfile المحلي."),
            ("Publish port 8000.", "انشر المنفذ 8000."),
            ("Point `DATABASE_URL` at the `db` service.", "اجعل `DATABASE_URL` يشير إلى الخدمة `db`."),
            ("Keep the database files in the named volume.", "احفظ ملفات قاعدة البيانات في وحدة التخزين المسمّاة."),
            ("Use a bridge network.", "استخدم شبكة bridge."),
        ),
        starter='''services:
  server:
    # Step 1: build from the Dockerfile in this folder
    build: ___
    ports:
      # Step 2: host port 8000 -> container port 8000
      - ___
    environment:
      # Step 3: the service name "db" is the hostname on the shared network
      DATABASE_URL: ___
    secrets:
      - llm_api_token
    networks: [app]
    depends_on: [db]

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: masar
      POSTGRES_PASSWORD: masar
      POSTGRES_DB: masar
    volumes:
      # Step 4: data survives `docker compose down`
      - ___
    networks: [app]

volumes:
  db-data:

networks:
  app:
    # Step 5: a user-defined bridge network
    driver: ___

secrets:
  llm_api_token:
    file: ./secrets/llm_api_token.txt
''',
        answers=(".", '"8000:8000"', "postgresql://masar:masar@db:5432/masar", "db-data:/var/lib/postgresql/data", "bridge"),
        alternatives={
            1: ("./",),
            2: ("8000:8000",),
            3: ("postgresql+asyncpg://masar:masar@db:5432/masar", "postgresql+psycopg://masar:masar@db:5432/masar"),
        },
        blanks=(
            ("`build: .` uses the Dockerfile in the current folder.", "يستخدم `build: .` ملف Dockerfile في المجلد الحالي."),
            ("publish `\"8000:8000\"`.", "انشر `\"8000:8000\"`."),
            ("use `postgresql://masar:masar@db:5432/masar` - the host is the service name `db`.",
             "استخدم `postgresql://masar:masar@db:5432/masar` - فالمضيف هو اسم الخدمة `db`."),
            ("mount `db-data:/var/lib/postgresql/data`.", "اربط `db-data:/var/lib/postgresql/data`."),
            ("set `driver: bridge`.", "اضبط `driver: bridge`."),
        ),
        hints=(
            ("Ports are `\"host:container\"`.", "تُكتب المنافذ بالصيغة `\"host:container\"`."),
            ("On a Compose network, services reach each other by service name.", "على شبكة Compose تصل الخدمات بعضها إلى بعض باسم الخدمة."),
            ("PostgreSQL keeps its data in `/var/lib/postgresql/data`.", "يحفظ PostgreSQL بياناته في `/var/lib/postgresql/data`."),
        ),
        success=("Correct! `docker compose down` recreates both containers and the network safely, while the named volume keeps the database - and the API token never appears in the file.",
                 "صحيح! يعيد `docker compose down` إنشاء الحاويتين والشبكة بأمان، بينما تحتفظ وحدة التخزين المسمّاة بقاعدة البيانات - ولا يظهر رمز API في الملف أبدًا."),
        expected=("Compose files are checked by reading them: each completed line is compared with the expected entry, ignoring extra spaces.",
                  "تُفحص ملفات Compose بقراءتها: يُقارن كل سطر مكتمل بالمدخل المتوقع مع تجاهل المسافات الزائدة."),
        language="yaml",
    ),
    "COURSE-010.M01.L12.EX06": Guided(
        goal=("Reorder an inefficient Dockerfile so editing source code no longer reinstalls every dependency.",
              "أعد ترتيب ملف Dockerfile غير فعّال حتى لا يعيد تعديلُ الكود تثبيتَ كل التبعيات."),
        steps=(
            ("Copy only `requirements.txt` first.", "انسخ `requirements.txt` وحده أولًا."),
            ("Install the dependencies.", "ثبّت التبعيات."),
            ("Copy the rest of the source afterwards.", "انسخ بقية الكود بعد ذلك."),
        ),
        starter='''FROM python:3.12-slim
WORKDIR /code
# Step 1: ONLY the dependency list
COPY ___
# Step 2: this layer is reused until requirements.txt changes
RUN ___
# Step 3: source edits now invalidate only the layers from here down
COPY ___
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''',
        answers=("requirements.txt .", "pip install --no-cache-dir -r requirements.txt", ". ."),
        alternatives={1: ("requirements.txt ./", "./requirements.txt ."), 2: ("pip install -r requirements.txt",), 3: ("./ ./",)},
        blanks=(
            ("copy `requirements.txt .`.", "انسخ `requirements.txt .`."),
            ("run `pip install --no-cache-dir -r requirements.txt`.", "شغّل `pip install --no-cache-dir -r requirements.txt`."),
            ("copy the remaining source with `. .`.", "انسخ بقية الكود بـ `. .`."),
        ),
        hints=(
            ("In the original, `COPY . .` came first, so any edit changed that layer and everything after it.", "في الأصل جاء `COPY . .` أولًا، فكان أي تعديل يغيّر تلك الطبقة وكل ما بعدها."),
            ("`--no-cache-dir` keeps pip's download cache out of the image.", "يُبقي `--no-cache-dir` ذاكرة تنزيل pip خارج الصورة."),
            ("The source copy belongs after the install.", "يأتي نسخ الكود بعد التثبيت."),
        ),
        success=("Correct! The expensive install layer now depends only on requirements.txt, so day-to-day code edits rebuild in seconds.",
                 "صحيح! أصبحت طبقة التثبيت المكلفة تعتمد على requirements.txt فقط، فتُعاد بناء تعديلات الكود اليومية في ثوانٍ."),
        expected=("Dockerfiles are checked by reading them: each completed line is compared with the expected instruction, ignoring extra spaces.",
                  "تُفحص ملفات Dockerfile بقراءتها: يُقارن كل سطر مكتمل بالتعليمة المتوقعة مع تجاهل المسافات الزائدة."),
        reflect=("List five paths you would put in `.dockerignore`, and explain why `.env` must never enter the build context.",
                 "اذكر خمسة مسارات ستضعها في `.dockerignore`، واشرح لماذا يجب ألا يدخل `.env` سياق البناء أبدًا."),
        language="dockerfile",
    ),
    "COURSE-010.M01.L12.EX07": Guided(
        goal=("Split a GenAI image into build, production and development stages so build tools never ship to production.",
              "قسّم صورة خدمة الذكاء الاصطناعي التوليدي إلى مراحل بناء وإنتاج وتطوير، كي لا تصل أدوات البناء إلى الإنتاج أبدًا."),
        steps=(
            ("Name the first stage `builder`.", "سمِّ المرحلة الأولى `builder`."),
            ("Copy the virtual environment from the builder.", "انسخ البيئة الافتراضية من مرحلة البناء."),
            ("Base the development stage on production.", "اجعل مرحلة التطوير مبنية على مرحلة الإنتاج."),
            ("Enable auto-reload in development.", "فعّل إعادة التحميل التلقائي في التطوير."),
        ),
        starter='''# Build stage: dependencies inside a virtual environment
FROM python:3.12-slim AS ___
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage: only what the service needs at runtime
FROM python:3.12-slim AS production
COPY --from=___ /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /code
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Development stage: production plus test/debug tools and reload
FROM ___ AS development
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", ___]
''',
        answers=("builder", "builder", "production", '"--reload"'),
        blanks=(
            ("name the stage `builder`.", "سمِّ المرحلة `builder`."),
            ("copy from the `builder` stage.", "انسخ من مرحلة `builder`."),
            ("start development `FROM production`.", "ابدأ التطوير بـ `FROM production`."),
            ("add the `\"--reload\"` flag.", "أضف الخيار `\"--reload\"`."),
        ),
        hints=(
            ("`FROM image AS name` names a stage you can refer to later.", "يسمّي `FROM image AS name` مرحلة يمكنك الرجوع إليها لاحقًا."),
            ("`COPY --from=stage` copies files out of an earlier stage.", "ينسخ `COPY --from=stage` ملفات من مرحلة سابقة."),
            ("A stage can start FROM another stage of the same file.", "يمكن لمرحلة أن تبدأ FROM مرحلة أخرى من الملف نفسه."),
        ),
        success=("Correct! Production contains only the virtual environment and the source; compilers, test tools and reload exist only in the development stage.",
                 "صحيح! لا تحتوي مرحلة الإنتاج إلا على البيئة الافتراضية والكود؛ أما المترجمات وأدوات الاختبار وإعادة التحميل فلا توجد إلا في مرحلة التطوير."),
        expected=("Dockerfiles are checked by reading them: each completed line is compared with the expected instruction, ignoring extra spaces.",
                  "تُفحص ملفات Dockerfile بقراءتها: يُقارن كل سطر مكتمل بالتعليمة المتوقعة مع تجاهل المسافات الزائدة."),
        reflect=("Why should compilers and debuggers not stay in the production stage?", "لماذا يجب ألا تبقى المترجمات وأدوات التنقيح في مرحلة الإنتاج؟"),
        language="dockerfile",
    ),
}
