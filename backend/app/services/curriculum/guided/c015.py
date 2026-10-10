"""COURSE-015 Voice AI Engineering - Real-Time Voice Agents: guided exercises.

Tool-calling, routing and agent-to-agent logic runs in the sandbox with stub
functions standing in for model calls and remote services; MCP server wiring
is checked by reading the code.
"""
from . import Guided, check

STUB_NOTE = (
    "Stub functions stand in for the model and the remote services, so the host-side logic runs and is checked for real.",
    "تحل دوال بديلة محل النموذج والخدمات البعيدة، فيعمل منطق جهة المضيف ويُفحص فعليًا.",
)

EXERCISES = {
    "COURSE-015.M01.L01.EX01": Guided(
        goal=("Separate what the model sees (a function declaration) from what the host runs (a validated implementation).",
              "افصل ما يراه النموذج (تعريف الدالة) عما يشغّله المضيف (تنفيذ مُتحقَّق منه)."),
        steps=(
            ("Mark both arguments as required in the declaration.", "اجعل الوسيطين مطلوبين في التعريف."),
            ("Reject division by zero.", "ارفض القسمة على صفر."),
            ("Return the result in a structured form.", "أعد النتيجة بصيغة منظَّمة."),
            ("Execute the model's call on the host.", "نفّذ استدعاء النموذج على المضيف."),
        ),
        starter='''# What the MODEL sees: a declaration it can choose to call
divide_declaration = {
    "name": "divide",
    "description": "Divide a by b and return the quotient. Examples: divide(10, 4) -> 2.5; divide(9, 3) -> 3.0",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "The dividend"},
            "b": {"type": "number", "description": "The divisor; must not be zero"},
        },
        # Step 1
        "required": ___,
    },
}

# What the HOST runs: the real implementation, with its own validation
def divide(a, b):
    # Step 2: never trust the model to avoid zero
    if ___:
        return {"error": "b must not be zero"}
    # Step 3
    return ___

def execute(call):
    """The model only produces `call`; the host decides whether and how to run it."""
    if call["name"] != divide_declaration["name"]:
        return {"error": f"unknown tool {call['name']!r}"}
    # Step 4: run the implementation with the model's arguments
    return ___

print(execute({"name": "divide", "args": {"a": 10, "b": 4}}), execute({"name": "divide", "args": {"a": 1, "b": 0}}))
''',
        answers=('["a", "b"]', "b == 0", '{"result": a / b}', 'divide(**call["args"])'),
        checks=(
            check("sorted(divide_declaration['parameters']['required'])", ["a", "b"], "Blank 1: `[\"a\", \"b\"]`.", "الفراغ 1: `[\"a\", \"b\"]`."),
            check("[divide(1, 0), divide(0, 5)]", [{"error": "b must not be zero"}, {"result": 0.0}],
                  "Blank 2: check the divisor `b == 0`, not the dividend.", "الفراغ 2: افحص المقسوم عليه `b == 0` لا المقسوم."),
            check("divide(10, 4)", {"result": 2.5}, "Blank 3: `{\"result\": a / b}`.", "الفراغ 3: `{\"result\": a / b}`."),
            check("[execute({'name': 'divide', 'args': {'a': 9, 'b': 3}}), execute({'name': 'rm', 'args': {}})]", [{"result": 3.0}, {"error": "unknown tool 'rm'"}],
                  "Blank 4: `divide(**call[\"args\"])` unpacks the arguments.", "الفراغ 4: يفكّ `divide(**call[\"args\"])` الوسائط."),
        ),
        hints=(
            ("`required` lists the parameter names the model must always supply.", "يسرد `required` أسماء المعاملات التي يجب أن يوفرها النموذج دائمًا."),
            ("Return errors as data so the model can explain them to the user.", "أعد الأخطاء بوصفها بيانات كي يشرحها النموذج للمستخدم."),
            ("`f(**d)` calls f with the dictionary's keys as keyword arguments.", "يستدعي `f(**d)` الدالة f بمفاتيح القاموس وسائطَ مسمّاة."),
        ),
        success=("Correct! The model only ever sees the declaration and proposes a call; the host validates and executes it - so a bad argument becomes a readable error, not a crash.",
                 "صحيح! لا يرى النموذج إلا التعريف ويقترح استدعاءً؛ ويتحقق المضيف منه وينفّذه - فتصبح الوسيطة الخاطئة خطأً مقروءًا لا انهيارًا."),
        expected=STUB_NOTE,
    ),
    "COURSE-015.M01.L03.EX03": Guided(
        goal=("Build a safe tool-calling turn: validate currency codes, handle a timing-out API, and turn the tool result into the final answer.",
              "ابنِ دورة آمنة لاستدعاء الأدوات: تحقّق من رموز العملات، وتعامل مع واجهة تنتهي مهلتها، وحوّل نتيجة الأداة إلى الإجابة النهائية."),
        steps=(
            ("Reject codes that are not three uppercase letters.", "ارفض الرموز التي ليست ثلاثة أحرف كبيرة."),
            ("Turn a timeout into a structured error.", "حوّل انتهاء المهلة إلى خطأ منظَّم."),
            ("Execute the model's requested tool call.", "نفّذ استدعاء الأداة الذي طلبه النموذج."),
            ("Answer gracefully when the tool failed.", "أجب بلطف عندما تفشل الأداة."),
        ),
        starter='''import re

get_exchange_rate_declaration = {
    "name": "get_exchange_rate",
    "description": "Current exchange rate between two ISO 4217 currency codes, e.g. USD -> EUR.",
    "parameters": {"type": "object", "required": ["base_currency", "quote_currency"],
                   "properties": {"base_currency": {"type": "string"}, "quote_currency": {"type": "string"}}},
}
RATES = {("USD", "EUR"): 0.92, ("EUR", "EGP"): 52.1}

class Timeout(Exception):
    pass

def fetch_rate(base, quote):
    """Stand-in for the external rates API (called with a timeout)."""
    if base == "JPY":
        raise Timeout()
    return RATES[(base, quote)]

def get_exchange_rate(base_currency, quote_currency):
    for code in (base_currency, quote_currency):
        # Step 1: system instructions cannot guarantee valid input - code can
        if ___:
            return {"error": f"invalid currency code: {code!r}"}
    try:
        rate = fetch_rate(base_currency, quote_currency)
    except Timeout:
        # Step 2
        return ___
    except KeyError:
        return {"error": "currency pair not supported"}
    return {"base": base_currency, "quote": quote_currency, "rate": rate}

def run_turn(model_call):
    """model request -> backend execution -> tool result -> final answer"""
    # Step 3
    result = ___
    if "error" in result:
        # Step 4
        return ___
    return f"1 {result['base']} = {result['rate']} {result['quote']}"

print(run_turn({"name": "get_exchange_rate", "args": {"base_currency": "USD", "quote_currency": "EUR"}}))
''',
        answers=(
            r'not re.fullmatch(r"[A-Z]{3}", code)',
            '{"error": "rate service timed out, please try again later"}',
            'get_exchange_rate(**model_call["args"])',
            "f\"Sorry, I couldn't get that rate: {result['error']}.\"",
        ),
        checks=(
            check("[get_exchange_rate('usd', 'EUR'), get_exchange_rate('USD', 'EURO')]", [{"error": "invalid currency code: 'usd'"}, {"error": "invalid currency code: 'EURO'"}],
                  "Blank 1: `not re.fullmatch(r\"[A-Z]{3}\", code)`.", "الفراغ 1: `not re.fullmatch(r\"[A-Z]{3}\", code)`."),
            check("'error' in get_exchange_rate('JPY', 'USD') and 'timed out' in get_exchange_rate('JPY', 'USD')['error']", True,
                  "Blank 2: return an `error` dictionary that says the service timed out.", "الفراغ 2: أعد قاموس `error` يذكر انتهاء مهلة الخدمة."),
            check("run_turn({'name': 'get_exchange_rate', 'args': {'base_currency': 'EUR', 'quote_currency': 'EGP'}})", "1 EUR = 52.1 EGP",
                  "Blank 3: `get_exchange_rate(**model_call[\"args\"])`.", "الفراغ 3: `get_exchange_rate(**model_call[\"args\"])`."),
            check("run_turn({'name': 'get_exchange_rate', 'args': {'base_currency': 'usd', 'quote_currency': 'EUR'}})", "Sorry, I couldn't get that rate: invalid currency code: 'usd'.",
                  "Blank 4: build the apology from `result['error']`.", "الفراغ 4: ابنِ الاعتذار من `result['error']`."),
        ),
        hints=(
            ("`re.fullmatch` requires the whole string to match.", "يشترط `re.fullmatch` مطابقة النص كله."),
            ("Errors returned as data let the model explain the failure.", "الأخطاء المعادة بوصفها بيانات تتيح للنموذج شرح الفشل."),
            ("An f-string can include the error text.", "يمكن أن يتضمن f-string نص الخطأ."),
        ),
        success=("Correct! The host validates every argument and contains every API failure; the model's instructions can ask for valid codes, but only code can guarantee them.",
                 "صحيح! يتحقق المضيف من كل وسيطة ويحتوي كل فشل في الواجهة؛ يمكن لتعليمات النموذج أن تطلب رموزًا صالحة، لكن الكود وحده يضمنها."),
        expected=STUB_NOTE,
    ),
    "COURSE-015.M01.L04.EX03": Guided(
        goal=("Route a Researcher → Analyst → Writer workflow deterministically through shared state, with a loop back when the analysis finds gaps.",
              "وجّه سير عمل Researcher ← Analyst ← Writer توجيهًا حتميًا عبر حالة مشتركة، مع رجوع عندما يجد التحليل ثغرات."),
        steps=(
            ("Have the Researcher append a finding to the shared state.", "اجعل Researcher يضيف نتيجة إلى الحالة المشتركة."),
            ("Have the Analyst flag missing evidence.", "اجعل Analyst يشير إلى نقص الأدلة."),
            ("Loop back to the Researcher when more research is needed.", "ارجع إلى Researcher عند الحاجة إلى مزيد من البحث."),
            ("Otherwise follow the fixed route.", "وإلا فاتبع المسار الثابت."),
        ),
        starter='''def researcher(state):
    round_number = len(state["findings"]) + 1
    # Step 1: write the finding into the shared state
    ___

def analyst(state):
    # Step 2: at least two independent findings are needed
    state["needs_more_research"] = ___
    state["analysis"] = None if state["needs_more_research"] else f"{len(state['findings'])} sources agree prices are falling"

def writer(state):
    state["report"] = f"{state['goal']}: {state['analysis']}"        # the Writer needs only goal + analysis

AGENTS = {"researcher": researcher, "analyst": analyst, "writer": writer}
ROUTE = {"researcher": "analyst", "analyst": "writer", "writer": None}   # deterministic routing

def run(goal, max_steps=8):
    state = {"goal": goal, "findings": [], "analysis": None, "report": None, "trace": []}
    agent = "researcher"
    for _ in range(max_steps):
        if agent is None:
            break
        state["trace"].append(agent)
        AGENTS[agent](state)
        # Step 3: return to an earlier agent when the analysis found a gap
        if agent == "analyst" and ___:
            agent = "researcher"
        else:
            # Step 4
            agent = ___
    return state

final = run("Home battery prices")
print(final["trace"], final["report"])
''',
        answers=('state["findings"].append(f"source {round_number}: battery prices fell")', 'len(state["findings"]) < 2',
                 'state["needs_more_research"]', "ROUTE[agent]"),
        checks=(
            check("final['findings']", ["source 1: battery prices fell", "source 2: battery prices fell"],
                  "Blank 1: append a finding to `state[\"findings\"]`.", "الفراغ 1: أضف نتيجة إلى `state[\"findings\"]`."),
            check("final['trace']", ["researcher", "analyst", "researcher", "analyst", "writer"],
                  "Blanks 2-4: flag `len(state[\"findings\"]) < 2`, loop back on that flag, otherwise follow `ROUTE[agent]`.",
                  "الفراغات 2-4: أشِر إلى `len(state[\"findings\"]) < 2`، وارجع عند هذه الإشارة، وإلا فاتبع `ROUTE[agent]`."),
            check("final['report']", "Home battery prices: 2 sources agree prices are falling",
                  "The Writer runs once the Analyst is satisfied.", "يعمل Writer بمجرد رضا Analyst."),
        ),
        hints=(
            ("Shared state is a dictionary every agent reads and writes.", "الحالة المشتركة قاموس يقرأ منه كل وكيل ويكتب فيه."),
            ("The flag is a Boolean expression about the number of findings.", "الإشارة تعبير منطقي عن عدد النتائج."),
            ("`ROUTE[agent]` gives the next agent in the fixed order.", "يعطي `ROUTE[agent]` الوكيل التالي في الترتيب الثابت."),
        ),
        success=("Correct! Routing is predictable and testable: every agent communicates only through the shared state, and one explicit rule sends work back when evidence is missing.",
                 "صحيح! التوجيه متوقع وقابل للاختبار: يتواصل كل وكيل عبر الحالة المشتركة فقط، وتعيد قاعدة صريحة واحدة العمل عند نقص الأدلة."),
        expected=STUB_NOTE,
        reflect=("When would dynamic (LLM-chosen) routing be worth giving up this predictability?",
                 "متى يستحق التوجيه الديناميكي (الذي يختاره النموذج) التخلي عن هذه القابلية للتوقع؟"),
    ),
    "COURSE-015.M01.L06.EX08": Guided(
        goal=("Coordinate two remote A2A agents: call them through one helper, record task history, answer an input-required task with a DataPart, and collect a FilePart.",
              "نسّق وكيلين بعيدين عبر A2A: استدعهما من خلال دالة مساعدة واحدة، وسجّل تاريخ المهام، وأجب عن مهمة تطلب مدخلًا بجزء بيانات، واجمع جزء ملف."),
        steps=(
            ("Refuse agents without an Agent Card.", "ارفض الوكلاء الذين ليست لهم بطاقة وكيل."),
            ("Record every task in the history.", "سجّل كل مهمة في التاريخ."),
            ("Answer the input-required task with the missing data.", "أجب عن المهمة التي تطلب مدخلًا بالبيانات الناقصة."),
            ("Return the worker's file name.", "أعد اسم ملف العامل."),
        ),
        starter='''AGENT_CARDS = {
    "strategist": {"name": "Strategist", "url": "http://localhost:9001", "skills": ["plan_research"]},
    "worker": {"name": "Research Worker", "url": "http://localhost:9002", "skills": ["collect_sources"]},
}

def remote_strategist(message):                     # stand-in for an A2A server
    if "region" not in message:
        return {"state": "input-required", "parts": [{"kind": "data", "data": {"question": "Which region?"}}]}
    return {"state": "completed", "parts": [{"kind": "data", "data": {"plan": [f"prices in {message['region']}", "subsidies"]}}]}

def remote_worker(message):
    return {"state": "completed", "parts": [{"kind": "file", "file": {"name": "sources.csv", "mimeType": "text/csv"}}]}

SERVERS = {"strategist": remote_strategist, "worker": remote_worker}
history = []

def call_remote_agent(agent, message):
    """Contract: send one message to an advertised agent, record it, return its Task."""
    # Step 1
    if ___:
        raise ValueError(f"unknown agent {agent!r}")
    task = SERVERS[agent](message)
    # Step 2: what to inspect when something fails later
    ___
    return task

def coordinate(topic):
    task = call_remote_agent("strategist", {"topic": topic})
    if task["state"] == "input-required":
        # Step 3: supply the missing field and ask again
        task = call_remote_agent("strategist", ___)
    plan = task["parts"][0]["data"]["plan"]
    sources = call_remote_agent("worker", {"plan": plan})
    # Step 4: the artifact name from the FilePart
    return ___

print(coordinate("home batteries"), history)

try:
    call_remote_agent("rogue-agent", {"topic": "anything"})
    unknown_rejected = False
except ValueError:
    unknown_rejected = True
''',
        answers=("agent not in AGENT_CARDS", 'history.append({"agent": agent, "message": message, "state": task["state"]})',
                 '{"topic": topic, "region": "EU"}', 'sources["parts"][0]["file"]["name"]'),
        checks=(
            check("coordinate('home batteries')", "sources.csv", "Blanks 3-4: resend with a `region`, then read the FilePart's name.",
                  "الفراغان 3 و4: أعد الإرسال مع `region`، ثم اقرأ اسم جزء الملف."),
            check("[(h['agent'], h['state']) for h in history[:3]]", [["strategist", "input-required"], ["strategist", "completed"], ["worker", "completed"]],
                  "Blank 2: append agent, message and task state to `history`.", "الفراغ 2: أضف الوكيل والرسالة وحالة المهمة إلى `history`."),
            check("unknown_rejected", True, "Blank 1: raise when `agent not in AGENT_CARDS`.", "الفراغ 1: أطلق خطأً عندما يكون `agent not in AGENT_CARDS`."),
        ),
        hints=(
            ("Only agents that publish an Agent Card are known to the coordinator.", "لا يعرف المنسِّق إلا الوكلاء الذين ينشرون بطاقة وكيل."),
            ("Task history is what you read first when a multi-agent run fails.", "تاريخ المهام هو أول ما تقرؤه عندما يفشل تشغيل متعدد الوكلاء."),
            ("A FilePart carries `file` metadata such as `name` and `mimeType`.", "يحمل جزء الملف بيانات `file` الوصفية مثل `name` و`mimeType`."),
        ),
        success=("Correct! One helper enforces the contract for every remote call, the history shows the input-required round trip, and the final artifact comes back as a FilePart.",
                 "صحيح! تفرض دالة مساعدة واحدة العقد على كل استدعاء بعيد، ويُظهر التاريخ رحلة طلب المدخل ذهابًا وإيابًا، وتعود النتيجة النهائية جزءَ ملف."),
        expected=STUB_NOTE,
        reflect=("How would you test each server on its own before debugging the whole workflow?",
                 "كيف ستختبر كل خادم على حدة قبل تنقيح سير العمل كاملًا؟"),
    ),
    "COURSE-015.M01.L07.EX06": Guided(
        goal=("Write a reusable Project Management MCP server with tools, resources and a prompt that any MCP host can use.",
              "اكتب خادم MCP قابلًا لإعادة الاستخدام لإدارة المشاريع، بأدوات وموارد وموجّه يستطيع أي مضيف MCP استخدامها."),
        steps=(
            ("Expose a project summary as a URI-templated resource.", "اعرض ملخص المشروع موردًا بقالب URI."),
            ("Expose the team list as a resource.", "اعرض قائمة الفريق موردًا."),
            ("Register the weekly status prompt.", "سجّل موجّه الحالة الأسبوعية."),
            ("Serve over STDIO for local development.", "قدّم الخادم عبر STDIO للتطوير المحلي."),
        ),
        starter='''from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Project Management")

@mcp.tool()
def create_task(title: str, due_date: str) -> dict:
    """Create a task and return its id."""
    ...

@mcp.tool()
def update_status(task_id: str, status: str) -> dict:
    """Move a task to todo, doing or done."""
    ...

@mcp.tool()
def list_overdue() -> list[dict]:
    """Tasks past their due date."""
    ...

# Step 1: read-only data addressed by a URI template
@mcp.resource(___)
def project_summary(project_id: str) -> str:
    ...

# Step 2
@___
def team_members() -> list[str]:
    ...

# Step 3: a reusable prompt template hosts can offer to users
@___
def weekly_status(project_id: str) -> str:
    return f"Summarise this week's progress and risks for project {project_id}."

if __name__ == "__main__":
    # Step 4: local development transport (production would use streamable HTTP)
    mcp.run(transport=___)
''',
        answers=('"projects://{project_id}/summary"', 'mcp.resource("team://members")', "mcp.prompt()", '"stdio"'),
        blanks=(
            ("use the URI template `\"projects://{project_id}/summary\"`.", "استخدم قالب URI `\"projects://{project_id}/summary\"`."),
            ("`mcp.resource(\"team://members\")`.", "`mcp.resource(\"team://members\")`."),
            ("`mcp.prompt()`.", "`mcp.prompt()`."),
            ("`\"stdio\"`.", "`\"stdio\"`."),
        ),
        hints=(
            ("Tools act, resources provide data, prompts offer templates.", "الأدوات تنفّذ، والموارد توفر البيانات، والموجّهات تقدّم قوالب."),
            ("A `{placeholder}` in the URI becomes a function argument.", "يصبح `{placeholder}` في URI وسيطةً للدالة."),
            ("STDIO for local development; streamable HTTP when several hosts connect remotely.", "STDIO للتطوير المحلي، وstreamable HTTP عندما تتصل عدة مضيفات عن بُعد."),
        ),
        success=("Correct! Because the server speaks plain MCP, ADK, an IDE and any other host can discover the same tools, resources and prompt without changes.",
                 "صحيح! لأن الخادم يتحدث MCP خالصًا، تستطيع ADK وبيئة التطوير وأي مضيف آخر اكتشاف الأدوات والموارد والموجّه نفسها دون تغيير."),
        expected=("The MCP SDK is not installed in the practice sandbox, so Check answer reads your code instead of running it.",
                  "حزمة MCP SDK غير مثبّتة في بيئة التدريب، لذلك يقرأ «تحقّق من الإجابة» الكود بدل تشغيله."),
        reflect=("Name one Sampling use case and one Elicitation use case for this server.", "اذكر حالة استخدام واحدة للـ Sampling وأخرى للـ Elicitation لهذا الخادم."),
    ),
}
