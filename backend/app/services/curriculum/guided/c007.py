"""COURSE-007 AI Agents with MCP: guided implementation exercises."""
from . import Guided, check

EXERCISES = {
    "COURSE-007.M03.L02.EX01": Guided(
        goal=("Write a completion handler for a prompt argument that filters, respects context, hides sensitive values and caps its results.",
              "اكتب معالج إكمال تلقائي لوسيط موجّه، يُرشّح القيم ويراعي السياق ويخفي القيم الحساسة ويحدّ عدد النتائج."),
        steps=(
            ("Keep only values that start with what the user typed.", "احتفظ فقط بالقيم التي تبدأ بما كتبه المستخدم."),
            ("If a service is already chosen, keep only its environments.", "إذا اختير خدمة مسبقًا، فاحتفظ ببيئاتها فقط."),
            ("Return at most 100 values.", "أعد 100 قيمة على الأكثر."),
            ("Report whether more values exist than were returned.", "أخبر هل توجد قيم أكثر مما أُعيد."),
        ),
        starter='''ENVIRONMENTS = ["development", "staging", "production", "preview", "qa", "sandbox"]
ENVIRONMENTS_BY_SERVICE = {
    "billing-api": {"development", "staging", "production"},
    "docs-site": {"development", "preview", "production"},
}
NEVER_SUGGEST = {"prod-db-admin", "break-glass"}     # internal names must not leak to clients
MAX_VALUES = 100                                     # the MCP limit for one completion response

def complete_environment(partial, service=None, candidates=ENVIRONMENTS):
    # Step 1: case-insensitive prefix match on what the user has typed so far
    matches = [value for value in candidates if ___]
    # Step 2: an already-selected service narrows the environments
    if service in ENVIRONMENTS_BY_SERVICE:
        matches = [value for value in matches if ___]
    matches = [value for value in matches if value not in NEVER_SUGGEST]
    return {
        "values": ___,                 # Step 3: never more than MAX_VALUES
        "total": len(matches),
        "hasMore": ___,                # Step 4: True when values were cut off
    }

print(complete_environment("pr"))
print(complete_environment("", service="billing-api"))
''',
        answers=(
            "value.lower().startswith(partial.lower())",
            "value in ENVIRONMENTS_BY_SERVICE[service]",
            "matches[:MAX_VALUES]",
            "len(matches) > MAX_VALUES",
        ),
        checks=(
            check("complete_environment('PR')['values']", ["production", "preview"],
                  "Blank 1: compare lowercase versions with `startswith` so 'PR' still finds 'production'.",
                  "الفراغ 1: قارن النسختين بالأحرف الصغيرة باستخدام `startswith` حتى تجد 'PR' القيمة 'production'."),
            check("complete_environment('', service='docs-site')['values']", ["development", "production", "preview"],
                  "Blank 2: keep a value only if it is in `ENVIRONMENTS_BY_SERVICE[service]`.",
                  "الفراغ 2: احتفظ بالقيمة فقط إذا كانت ضمن `ENVIRONMENTS_BY_SERVICE[service]`."),
            check("(lambda r: [len(r['values']), r['total']])(complete_environment('env', candidates=[f'env-{i}' for i in range(250)]))", [100, 250],
                  "Blank 3: slice the matches to the first `MAX_VALUES` items; `total` still counts all of them.",
                  "الفراغ 3: اقطع المطابقات إلى أول `MAX_VALUES` عنصر؛ ويبقى `total` عدّادًا لها كلها."),
            check("[complete_environment('env', candidates=[f'env-{i}' for i in range(250)])['hasMore'], complete_environment('pr')['hasMore']]", [True, False],
                  "Blank 4: `hasMore` is True only when there were more matches than `MAX_VALUES`.",
                  "الفراغ 4: تكون `hasMore` صحيحة فقط عندما تزيد المطابقات على `MAX_VALUES`."),
            check("complete_environment('', candidates=['prod-db-admin', 'production'])['values']", ["production"],
                  "Hidden values must never be suggested - keep the `NEVER_SUGGEST` filter.",
                  "يجب ألا تُقترح القيم المخفية أبدًا - أبقِ مرشّح `NEVER_SUGGEST`."),
        ),
        hints=(
            ("`text.lower().startswith(prefix.lower())` ignores case on both sides.", "يتجاهل `text.lower().startswith(prefix.lower())` حالة الأحرف في الطرفين."),
            ("A set supports fast membership checks with `in`.", "تدعم المجموعة (set) فحص العضوية السريع بـ `in`."),
            ("Slicing with `[:n]` never fails, even when the list is shorter than n.", "التقطيع بـ `[:n]` لا يفشل أبدًا، حتى لو كانت القائمة أقصر من n."),
        ),
        success=("Correct! Suggestions follow what the user typed and the chosen service, never leak internal names, and tell the client honestly when the list was cut.",
                 "صحيح! تتبع الاقتراحات ما كتبه المستخدم والخدمة المختارة، ولا تكشف أسماء داخلية أبدًا، وتخبر العميل بصدق عندما تُقطع القائمة."),
        reflect=("What rate-limiting rule would you add so a client typing quickly cannot flood your server with completion requests?",
                 "ما قاعدة تحديد المعدل التي ستضيفها كي لا يُغرق عميلٌ يكتب بسرعة الخادمَ بطلبات الإكمال؟"),
    ),
    "COURSE-007.M03.L02.EX02": Guided(
        goal=("Paginate a 2,400-entry resource list with an opaque cursor and page through it like a client.",
              "قسّم قائمة موارد من 2,400 عنصر إلى صفحات باستخدام مؤشر معتم (opaque cursor)، وتصفّحها كما يفعل العميل."),
        steps=(
            ("Find where the requested page starts.", "حدّد أين تبدأ الصفحة المطلوبة."),
            ("Add `nextCursor` only while resources remain.", "أضف `nextCursor` فقط ما دامت هناك موارد متبقية."),
            ("Encode the next page's position into the cursor.", "رمّز موضع الصفحة التالية داخل المؤشر."),
            ("In the client loop, follow `nextCursor` until it disappears.", "في حلقة العميل، اتبع `nextCursor` حتى يختفي."),
        ),
        starter='''RESOURCES = [{"uri": f"file:///reports/{i:04d}.md", "name": f"Report {i}"} for i in range(2400)]
PAGE_SIZE = 120

def encode_cursor(offset):
    return f"r{offset * 7 + 3}"          # the client must treat this string as opaque

def decode_cursor(cursor):
    return (int(cursor[1:]) - 3) // 7

def list_resources(cursor=None):
    # Step 1: the first page starts at 0; later pages start where the cursor says
    start = ___
    result = {"resources": RESOURCES[start:start + PAGE_SIZE]}
    # Step 2: only add nextCursor when more resources remain after this page
    if ___:
        # Step 3: the cursor for the next page
        result["nextCursor"] = ___
    return result

# Step 4: a client keeps asking until nextCursor is absent
pages, cursor = 0, None
while True:
    response = list_resources(cursor)
    pages += 1
    cursor = ___
    if cursor is None:
        break
print("pages:", pages)
''',
        answers=("0 if cursor is None else decode_cursor(cursor)", "start + PAGE_SIZE < len(RESOURCES)",
                 "encode_cursor(start + PAGE_SIZE)", 'response.get("nextCursor")'),
        checks=(
            check("[len(list_resources()['resources']), list_resources()['resources'][0]['name']]", [120, "Report 0"],
                  "Blank 1: with no cursor, start at 0.", "الفراغ 1: دون مؤشر ابدأ من 0."),
            check("list_resources(list_resources()['nextCursor'])['resources'][0]['name']", "Report 120",
                  "Blanks 1 and 3: the second page must start at offset 120 - encode `start + PAGE_SIZE`, decode it on the next call.",
                  "الفراغان 1 و3: يجب أن تبدأ الصفحة الثانية عند الإزاحة 120 - رمّز `start + PAGE_SIZE` وفكّ ترميزه في الاستدعاء التالي."),
            check("'nextCursor' in list_resources(encode_cursor(2280)) or len(list_resources(encode_cursor(2280))['resources']) != 120", False,
                  "Blank 2: the last page (offset 2280) must have 120 resources and no `nextCursor`.",
                  "الفراغ 2: يجب أن تحتوي الصفحة الأخيرة (الإزاحة 2280) على 120 موردًا ودون `nextCursor`."),
            check("pages", 20, "Blank 4: read `response.get(\"nextCursor\")` so the loop stops after the last page.",
                  "الفراغ 4: اقرأ `response.get(\"nextCursor\")` لتتوقف الحلقة بعد الصفحة الأخيرة."),
        ),
        hints=(
            ("Use a conditional expression for the start: a default for the first page, the decoded cursor otherwise.",
             "استخدم تعبيرًا شرطيًا للبداية: قيمة افتراضية للصفحة الأولى، والمؤشر بعد فك ترميزه في غير ذلك."),
            ("More resources remain when the next page's start is still inside the list.", "تبقى موارد إضافية عندما تقع بداية الصفحة التالية داخل القائمة."),
            ("`dict.get(key)` returns None when the key is missing - exactly what ends the loop.", "تعيد `dict.get(key)` القيمة None عند غياب المفتاح - وهذا بالضبط ما ينهي الحلقة."),
        ),
        success=("Correct! 2,400 resources arrive in 20 pages of 120, the client only ever passes the cursor back, and the final page ends the loop by omitting `nextCursor`.",
                 "صحيح! تصل الموارد الـ2,400 في 20 صفحة من 120، ولا يفعل العميل إلا إعادة المؤشر، وتُنهي الصفحة الأخيرة الحلقة بحذف `nextCursor`."),
        reflect=("Why must the client treat the cursor as opaque, and why should this pagination design not be copied into a `tools/call` result?",
                 "لماذا يجب أن يعامل العميل المؤشر بوصفه معتمًا؟ ولماذا لا ينبغي نسخ تصميم التقسيم هذا إلى نتيجة `tools/call`؟"),
    ),
    "COURSE-007.M03.L02.EX03": Guided(
        goal=("Design an elicitation request for booking a support call, validate the answers, and handle accept, decline and cancel explicitly.",
              "صمّم طلب استيضاح (elicitation) لحجز مكالمة دعم، وتحقّق من الإجابات، وتعامل صراحةً مع القبول والرفض والإلغاء."),
        steps=(
            ("Mark the required fields of the flat schema.", "حدّد الحقول المطلوبة في المخطط المسطّح."),
            ("Reject times outside business hours (09:00-16:59).", "ارفض الأوقات خارج ساعات العمل (09:00-16:59)."),
            ("On accept, return the errors or the booking.", "عند القبول، أعد الأخطاء أو الحجز."),
            ("On cancel, stop without booking.", "عند الإلغاء، توقّف دون حجز."),
        ),
        starter='''import re

# A flat object of primitive fields - the only shape elicitation supports
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "title": "Your name"},
        "preferred_time": {"type": "string", "title": "Preferred time (HH:MM, 24-hour)"},
        "email": {"type": "string", "title": "Contact email", "format": "email"},
        "notes": {"type": "string", "title": "Anything we should know?"},
    },
    # Step 1: name, time and email are required; notes are optional
    "required": ___,
}

def validate(content):
    """Semantic checks the JSON schema cannot express."""
    errors = []
    if not re.fullmatch(r"[^@\\s]+@[^@\\s]+\\.[a-z]{2,}", content.get("email", ""), re.IGNORECASE):
        errors.append("email")
    time = re.fullmatch(r"(\\d{2}):(\\d{2})", content.get("preferred_time", ""))
    # Step 2: reject a malformed time or one outside 09:00-16:59
    if ___:
        errors.append("preferred_time")
    return errors

def resolve(result):
    if result["action"] == "accept":
        errors = validate(result["content"])
        # Step 3: report invalid fields, otherwise confirm the booking
        return ___
    if result["action"] == "decline":
        return {"status": "declined"}          # the user said no: do not ask again
    # Step 4: "cancel" - the user dismissed the form
    return ___

print(resolve({"action": "accept", "content": {"name": "Omar", "preferred_time": "10:30", "email": "omar@example.com"}}))
''',
        answers=(
            '["name", "preferred_time", "email"]',
            "not time or not 9 <= int(time.group(1)) < 17",
            '{"status": "invalid", "fields": errors} if errors else {"status": "booked", "name": result["content"]["name"]}',
            '{"status": "cancelled"}',
        ),
        checks=(
            check("sorted(schema['required'])", ["email", "name", "preferred_time"],
                  "Blank 1: list the three required field names; `notes` stays optional.",
                  "الفراغ 1: اذكر أسماء الحقول الثلاثة المطلوبة؛ ويبقى `notes` اختياريًا."),
            check("[validate({'email': 'a@b.io', 'preferred_time': t}) for t in ('09:00', '16:59', '17:00', '8:30', 'noon')]",
                  [[], [], ["preferred_time"], ["preferred_time"], ["preferred_time"]],
                  "Blank 2: flag the time when it does not match HH:MM or its hour is not between 9 and 16.",
                  "الفراغ 2: أشِر إلى الوقت عندما لا يطابق HH:MM أو تكون ساعته خارج 9 إلى 16."),
            check("[resolve({'action': 'accept', 'content': {'name': 'Omar', 'preferred_time': '10:30', 'email': 'omar@example.com'}}), resolve({'action': 'accept', 'content': {'name': 'Omar', 'preferred_time': '20:00', 'email': 'bad'}})]",
                  [{"status": "booked", "name": "Omar"}, {"status": "invalid", "fields": ["email", "preferred_time"]}],
                  "Blank 3: return `{\"status\": \"invalid\", \"fields\": errors}` when there are errors, else the booking.",
                  "الفراغ 3: أعد `{\"status\": \"invalid\", \"fields\": errors}` عند وجود أخطاء، وإلا فأعد الحجز."),
            check("resolve({'action': 'cancel'})", {"status": "cancelled"},
                  "Blank 4: a cancelled form ends without booking: `{\"status\": \"cancelled\"}`.",
                  "الفراغ 4: ينتهي النموذج الملغى دون حجز: `{\"status\": \"cancelled\"}`."),
        ),
        hints=(
            ("`required` is a list of property names.", "يمثّل `required` قائمة بأسماء الخصائص."),
            ("`re.fullmatch` returns None when the text does not match; `time.group(1)` is the hour.",
             "تعيد `re.fullmatch` القيمة None عند عدم المطابقة، و`time.group(1)` هي الساعة."),
            ("Each of the three actions needs its own explicit result.", "يحتاج كل إجراء من الإجراءات الثلاثة إلى نتيجته الصريحة."),
        ),
        success=("Correct! The form only asks for primitive fields, validates meaning as well as structure, and treats accept, decline and cancel as three different outcomes.",
                 "صحيح! يطلب النموذج حقولًا أولية فقط، ويتحقق من المعنى إلى جانب البنية، ويعامل القبول والرفض والإلغاء بوصفها ثلاث نتائج مختلفة."),
        reflect=("Which piece of information should never be collected this way, and what should the tool do if the client does not support elicitation?",
                 "ما المعلومة التي يجب ألا تُجمع بهذه الطريقة أبدًا؟ وماذا يجب أن تفعل الأداة إذا لم يدعم العميل الاستيضاح؟"),
    ),
    "COURSE-007.M03.L02.EX04": Guided(
        goal=("Make a long-running file-processing tool report progress, clean up and never publish a partial report when cancelled.",
              "اجعل أداة معالجة الملفات طويلة التشغيل تبلّغ عن تقدمها، وتنظّف ما خلّفته، ولا تنشر تقريرًا جزئيًا أبدًا عند إلغائها."),
        steps=(
            ("Report progress every 1,000 files.", "أبلغ عن التقدم كل 1,000 ملف."),
            ("Publish the report only after every file is processed.", "انشر التقرير فقط بعد معالجة كل الملفات."),
            ("Re-raise the cancellation after logging it.", "أعد إطلاق الإلغاء بعد تسجيله."),
            ("Always clear the temporary workspace.", "امسح مساحة العمل المؤقتة دائمًا."),
        ),
        starter='''class Cancelled(Exception):
    """Stands in for the cancellation exception the MCP SDK raises inside a tool."""

workspace = []      # temporary results that must never outlive the call
log = []

def process_files(files, report_progress, cancel_at=None):
    try:
        for done, name in enumerate(files, start=1):
            if done == cancel_at:
                raise Cancelled()
            workspace.append(name.upper())
            # Step 1: progress every 1,000 files, not on every file
            if ___:
                report_progress(done, len(files))
        # Step 2: publish a copy only once everything is processed
        report = ___
        return report
    except Cancelled:
        log.append(f"cancelled after {len(workspace)} of {len(files)} files")
        # Step 3: let the cancellation continue to the caller
        ___
    finally:
        # Step 4: always clean up the temporary workspace
        ___

files = [f"file_{i}.txt" for i in range(10_000)]
progress = []
report = process_files(files, lambda done, total: progress.append(done))

try:
    process_files(files, lambda done, total: None, cancel_at=2_500)
    cancellation_propagated = False
except Cancelled:
    cancellation_propagated = True
print(len(report), "files in the report |", len(progress), "progress updates |", log)
''',
        answers=("done % 1000 == 0", "list(workspace)", "raise", "workspace.clear()"),
        checks=(
            check("progress", [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
                  "Blank 1: report when `done` is a multiple of 1,000.", "الفراغ 1: أبلغ عندما يكون `done` من مضاعفات 1,000."),
            check("len(report) == 10000 and report[0] == 'FILE_0.TXT'", True,
                  "Blank 2: return a copy of the workspace (`list(workspace)`) - the original is cleared in `finally`.",
                  "الفراغ 2: أعد نسخة من مساحة العمل (`list(workspace)`) - فالأصل يُمسح في `finally`."),
            check("cancellation_propagated", True,
                  "Blank 3: re-raise with a bare `raise` so the caller knows the call was cancelled.",
                  "الفراغ 3: أعد الإطلاق بـ `raise` وحدها كي يعرف المستدعي أن الاستدعاء أُلغي."),
            check("len(workspace) == 0 and log == ['cancelled after 2499 of 10000 files']", True,
                  "Blank 4: clear the workspace in `finally`, so both success and cancellation leave nothing behind.",
                  "الفراغ 4: امسح مساحة العمل في `finally` كي لا يترك النجاح ولا الإلغاء أي أثر."),
        ),
        hints=(
            ("The remainder operator `%` tells you when a counter reaches a multiple of a number.", "يخبرك عامل باقي القسمة `%` متى يصل العدّاد إلى مضاعف لعدد ما."),
            ("`list(workspace)` copies the list; clearing the original later does not affect the copy.", "ينسخ `list(workspace)` القائمة، ولا يؤثر مسح الأصل لاحقًا في النسخة."),
            ("A bare `raise` inside `except` re-raises the current exception; `finally` runs in every case.",
             "تعيد `raise` وحدها داخل `except` إطلاق الاستثناء الحالي، وتعمل `finally` في كل الحالات."),
        ),
        success=("Correct! Progress is reported at a sensible rate, a cancelled run cleans up and propagates the cancellation, and only a complete run publishes a report.",
                 "صحيح! يُبلَّغ عن التقدم بمعدل معقول، وينظّف التشغيل الملغى ما خلّفه وينقل الإلغاء، ولا ينشر تقريرًا إلا التشغيل المكتمل."),
        reflect=("Why must the cancellation be re-raised instead of swallowed, and how do stdio and Streamable HTTP signal cancellation differently?",
                 "لماذا يجب إعادة إطلاق الإلغاء بدل ابتلاعه؟ وكيف يختلف إرسال إشارة الإلغاء بين stdio وStreamable HTTP؟"),
    ),
    "COURSE-007.M04.L01.EX03": Guided(
        goal=("Complete a WebSocket client transport for the MCP Python SDK: two memory-stream pairs, a reader task, a writer task and cleanup.",
              "أكمل ناقل عميل WebSocket لحزمة MCP في Python: زوجان من تدفقات الذاكرة، ومهمة قراءة، ومهمة كتابة، والتنظيف."),
        steps=(
            ("Create the read stream pair.", "أنشئ زوج تدفق القراءة."),
            ("Parse each WebSocket text frame into a JSON-RPC message.", "حلّل كل إطار نصي من WebSocket إلى رسالة JSON-RPC."),
            ("Send parse errors to the session instead of crashing.", "أرسل أخطاء التحليل إلى الجلسة بدل الانهيار."),
            ("Write each outgoing message as one JSON text frame.", "اكتب كل رسالة صادرة إطارًا نصيًا واحدًا بصيغة JSON."),
            ("Yield the session's two stream ends.", "أعد (yield) طرفي التدفق الخاصين بالجلسة."),
        ),
        starter='''import json
from contextlib import asynccontextmanager

import anyio
from mcp import types
from mcp.shared.message import SessionMessage
from pydantic import ValidationError
from websockets.asyncio.client import connect

@asynccontextmanager
async def websocket_client(url):
    # Step 1: wire -> session (the session reads read_stream; our reader task writes into it)
    read_stream_writer, read_stream = ___
    # session -> wire (the session writes write_stream; our writer task reads from it)
    write_stream, write_stream_reader = anyio.create_memory_object_stream(0)

    async with connect(url, subprotocols=["mcp"]) as ws:
        async def ws_reader():
            async with read_stream_writer:
                async for raw_text in ws:
                    try:
                        # Step 2: one text frame = one JSON-RPC message
                        message = ___
                        await read_stream_writer.send(SessionMessage(message))
                    except ValidationError as exc:
                        # Step 3: surface the error to the session instead of crashing the transport
                        await ___

        async def ws_writer():
            async with write_stream_reader:
                async for session_message in write_stream_reader:
                    payload = session_message.message.model_dump(by_alias=True, mode="json", exclude_none=True)
                    # Step 4: send it as one JSON text frame
                    await ___

        async with anyio.create_task_group() as tg:
            tg.start_soon(ws_reader)
            tg.start_soon(ws_writer)
            try:
                # Step 5: hand the session its two ends
                yield ___
            finally:
                tg.cancel_scope.cancel()
''',
        answers=(
            "anyio.create_memory_object_stream(0)",
            "types.JSONRPCMessage.model_validate_json(raw_text)",
            "read_stream_writer.send(exc)",
            "ws.send(json.dumps(payload))",
            "(read_stream, write_stream)",
        ),
        alternatives={2: ("types.JSONRPCMessage.model_validate(json.loads(raw_text))",), 5: ("read_stream, write_stream",)},
        blanks=(
            ("create it like the write pair: `anyio.create_memory_object_stream(0)`.", "أنشئه مثل زوج الكتابة: `anyio.create_memory_object_stream(0)`."),
            ("use `types.JSONRPCMessage.model_validate_json(raw_text)`.", "استخدم `types.JSONRPCMessage.model_validate_json(raw_text)`."),
            ("send the exception itself into the read stream: `read_stream_writer.send(exc)`.", "أرسل الاستثناء نفسه إلى تدفق القراءة: `read_stream_writer.send(exc)`."),
            ("serialize with `json.dumps(payload)` and pass it to `ws.send`.", "حوّل إلى نص بـ `json.dumps(payload)` ومرّره إلى `ws.send`."),
            ("yield the tuple `(read_stream, write_stream)`.", "أعد الصفّ `(read_stream, write_stream)`."),
        ),
        hints=(
            ("anyio's memory object stream returns a (send end, receive end) pair; a buffer size of 0 makes each send wait for a receiver.", "يعيد تدفق الكائنات في الذاكرة في anyio زوجًا (طرف الإرسال، طرف الاستقبال)؛ وحجم مخزن 0 يجعل كل إرسال ينتظر مستقبِلًا."),
            ("Pydantic models parse JSON text with `model_validate_json`.", "تحلّل نماذج Pydantic نص JSON بـ `model_validate_json`."),
            ("The session receives messages OR exceptions on its read stream; the transport hands it the ends it uses.",
             "تستقبل الجلسة رسائل أو استثناءات على تدفق القراءة، ويعطيها الناقل الطرفين اللذين تستخدمهما."),
        ),
        success=("Correct! This is the transport contract: the session only sees two memory streams, while the reader and writer tasks translate between those streams and WebSocket frames and are cancelled on exit.",
                 "صحيح! هذا هو عقد الناقل: لا ترى الجلسة إلا تدفقي ذاكرة، بينما تترجم مهمتا القراءة والكتابة بين هذين التدفقين وإطارات WebSocket وتُلغيان عند الخروج."),
        expected=(
            "The MCP SDK and websockets are not installed in the practice sandbox, so Check answer reads your code instead of running it.",
            "حزمة MCP ومكتبة websockets غير مثبّتتين في بيئة التدريب، لذلك يقرأ «تحقّق من الإجابة» الكود بدل تشغيله.",
        ),
        reflect=("Name two security risks that matter for a WebSocket transport but not for stdio.",
                 "اذكر خطرين أمنيين مهمّين لناقل WebSocket لكنهما غير مهمّين لـ stdio."),
    ),
}
