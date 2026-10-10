"""COURSE-012 AI Agents Foundations: guided implementation exercises.

Wiring code for the OpenAI Agents SDK and FastMCP is checked by reading it
(neither is installed in the practice sandbox). The deterministic parts of an
agent system - flows, guardrails, bounded loops, routing and evaluation - run
for real, with small stub functions standing in for model calls.
"""
from . import Guided, check

SDK_NOTE = (
    "The Agents SDK and the MCP SDK are not installed in the practice sandbox, so Check answer reads your code instead of running it.",
    "حزمتا Agents SDK وMCP SDK غير مثبّتتين في بيئة التدريب، لذلك يقرأ «تحقّق من الإجابة» الكود بدل تشغيله.",
)
STUB_NOTE = (
    "Small stub functions stand in for the model calls, so the deterministic control logic runs and is checked for real.",
    "تحل دوال بديلة صغيرة محل استدعاءات النموذج، فيعمل منطق التحكم الحتمي ويُفحص فعليًا.",
)

EXERCISES = {
    "COURSE-012.M01.L02.EX02": Guided(
        goal=("Give the Research Planner two function tools, a typed output and a named trace.",
              "امنح مخطِّط البحث أداتين من الدوال، ومخرجًا محدد النوع، وتتبّعًا مسمّى."),
        steps=(
            ("Turn `get_research_sources` into a function tool.", "حوّل `get_research_sources` إلى أداة دالة."),
            ("Register both tools with the agent.", "سجّل الأداتين لدى الوكيل."),
            ("Make the agent return a `ResearchPlanModel`.", "اجعل الوكيل يعيد `ResearchPlanModel`."),
            ("Wrap the run in a trace named \"Research planning\".", "ضع التشغيل داخل تتبّع اسمه \"Research planning\"."),
            ("Read the validated plan from the result.", "اقرأ الخطة المُتحقَّق منها من النتيجة."),
        ),
        starter='''from typing import TypedDict

from agents import Agent, Runner, function_tool, trace
from pydantic import BaseModel

class ResearchTask(TypedDict):
    step: int
    research_source: str
    url: str
    description: str

class ResearchPlanModel(BaseModel):
    goal: str
    tasks: list[ResearchTask]

# Step 1: expose this function to the agent as a tool
@___
def get_research_sources() -> list[str]:
    """Return the research sources the planner may use."""
    return ["Wikipedia", "Google Scholar", "YouTube"]

@function_tool
def get_resource_url(source: str) -> str:
    """Return the base URL of one research source."""
    return {"Wikipedia": "https://wikipedia.org", "Google Scholar": "https://scholar.google.com",
            "YouTube": "https://youtube.com"}.get(source, "unknown")

planner = Agent(
    name="Research Planner",
    instructions=("Call get_research_sources first, then get_resource_url for each source you use. "
                  "Every task needs a step number, research source, URL and description."),
    tools=___,                 # Step 2: both tools
    output_type=___,           # Step 3: a validated, typed plan
)

async def main():
    # Step 4: one named trace for the whole run
    with ___:
        result = await Runner.run(planner, "Plan research on home solar batteries")
    # Step 5: an instance of ResearchPlanModel
    plan = ___
    print(plan.tasks)
''',
        answers=("function_tool", "[get_research_sources, get_resource_url]", "ResearchPlanModel",
                 'trace("Research planning")', "result.final_output"),
        alternatives={2: ("[get_resource_url, get_research_sources]",)},
        blanks=(
            ("decorate it with `@function_tool`.", "زخرفها بـ `@function_tool`."),
            ("pass `[get_research_sources, get_resource_url]`.", "مرّر `[get_research_sources, get_resource_url]`."),
            ("set `output_type=ResearchPlanModel`.", "اضبط `output_type=ResearchPlanModel`."),
            ("use `trace(\"Research planning\")`.", "استخدم `trace(\"Research planning\")`."),
            ("read `result.final_output`.", "اقرأ `result.final_output`."),
        ),
        hints=(
            ("The SDK's tool decorator builds the tool schema from the function's signature and docstring.", "يبني مزخرف الأدوات في الـ SDK مخطط الأداة من توقيع الدالة ووصفها."),
            ("`output_type` makes the SDK validate the final answer against your model.", "يجعل `output_type` الحزمةَ تتحقق من الإجابة النهائية مقابل نموذجك."),
            ("`trace(name)` is a context manager that groups every span of the run.", "`trace(name)` مدير سياق يجمع كل مقاطع التشغيل."),
        ),
        success=("Correct! The planner must fetch the sources before it can look up their URLs - those calls are sequential - and its answer arrives as a validated ResearchPlanModel inside one trace.",
                 "صحيح! يجب أن يجلب المخطِّط المصادر قبل أن يبحث عن عناوينها - فهذه الاستدعاءات متتالية - وتصل إجابته بوصفها ResearchPlanModel مُتحقَّقًا منه داخل تتبّع واحد."),
        expected=SDK_NOTE,
        reflect=("Which tool calls could run in parallel, and what safety or reliability check would you add before production?",
                 "أي استدعاءات الأدوات يمكن أن تعمل بالتوازي؟ وما فحص الأمان أو الموثوقية الذي ستضيفه قبل الإنتاج؟"),
    ),
    "COURSE-012.M01.L03.EX01": Guided(
        goal=("Build a one-tool FastMCP server whose name, signature and docstring tell an agent exactly what the tool does.",
              "ابنِ خادم FastMCP بأداة واحدة، يخبر اسمها وتوقيعها ووصفها الوكيلَ بما تفعله الأداة بالضبط."),
        steps=(
            ("Create the server named \"Research Tools\".", "أنشئ الخادم باسم \"Research Tools\"."),
            ("Register the function as an MCP tool.", "سجّل الدالة أداةَ MCP."),
            ("Declare its return type.", "صرّح بنوع الإرجاع."),
            ("Serve it over STDIO.", "قدّمها عبر STDIO."),
        ),
        starter='''from mcp.server.fastmcp import FastMCP

# Step 1: the server, as clients will see it
mcp = ___

# Step 2: register the function as a tool
@___
def get_research_sources() -> ___:          # Step 3: the return type becomes the output schema
    """Provide the list of research sources an agent may use."""
    return ["Wikipedia", "Google", "YouTube"]

if __name__ == "__main__":
    # Step 4: a local process the client starts and talks to over stdin/stdout
    mcp.run(transport=___)

# Inspect it with:  mcp dev research_server.py
''',
        answers=('FastMCP("Research Tools")', "mcp.tool()", "list[str]", '"stdio"'),
        blanks=(
            ("create `FastMCP(\"Research Tools\")`.", "أنشئ `FastMCP(\"Research Tools\")`."),
            ("use the decorator `@mcp.tool()`.", "استخدم المزخرف `@mcp.tool()`."),
            ("the function returns `list[str]`.", "تعيد الدالة `list[str]`."),
            ("use `transport=\"stdio\"`.", "استخدم `transport=\"stdio\"`."),
        ),
        hints=(
            ("The server's name is the first argument to `FastMCP`.", "اسم الخادم هو الوسيط الأول لـ `FastMCP`."),
            ("`@mcp.tool()` - note the parentheses: it is called to make the decorator.", "`@mcp.tool()` - لاحظ القوسين: إنه يُستدعى لإنشاء المزخرف."),
            ("STDIO is the simplest transport for a tool server that runs next to one client.", "يُعدّ STDIO أبسط ناقل لخادم أدوات يعمل بجوار عميل واحد."),
        ),
        success=("Correct! The Inspector will show the tool's name, the docstring as its description, an empty input schema and a list-of-strings result.",
                 "صحيح! سيعرض المفتش اسم الأداة، والوصف بوصفه شرحها، ومخطط إدخال فارغًا، ونتيجة من قائمة نصوص."),
        expected=SDK_NOTE,
        reflect=("Why does the docstring matter so much to an agent that has never seen your code?",
                 "لماذا يهم الوصف (docstring) كثيرًا لوكيل لم يرَ كودك من قبل؟"),
    ),
    "COURSE-012.M01.L03.EX02": Guided(
        goal=("Move two in-process tools into their own FastMCP server and let the agent use the server instead of the functions.",
              "انقل أداتين داخل العملية إلى خادم FastMCP مستقل، ودع الوكيل يستخدم الخادم بدل الدوال."),
        steps=(
            ("Return how many events the journal holds.", "أعد عدد الأحداث في السجل."),
            ("Register `load_journal` as a tool too.", "سجّل `load_journal` أداةً أيضًا."),
            ("Return a copy of the journal.", "أعد نسخة من السجل."),
            ("Register the server with the agent.", "سجّل الخادم لدى الوكيل."),
        ),
        starter='''# ---- journal_server.py: the tools now live behind an MCP server ----
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Time Travel Tracker")
_journal: list[str] = []

@mcp.tool()
def record_event(entry: str) -> dict:
    """Add a new travel event to the journal."""
    _journal.append(entry)
    # Step 1: report the new size of the journal
    return {"status": "recorded", "count": ___}

# Step 2: the second tool
@___
def load_journal() -> list[str]:
    """Return every recorded travel event, oldest first."""
    # Step 3: a copy, so callers cannot change the server's list
    return ___

if __name__ == "__main__":
    mcp.run()

# ---- agent.py: the agent registers the SERVER, not the functions ----
from agents import Agent, Runner
from agents.mcp import MCPServerStdio, MCPServerStdioParams

async def main():
    params = MCPServerStdioParams(command="mcp", args=["run", "journal_server.py"])
    async with MCPServerStdio(name="Time Travel Tracker", params=params) as journal_server:
        agent = Agent(
            name="Time Traveller",
            instructions="Record every trip, then summarize the journal.",
            mcp_servers=___,                  # Step 4
        )
        result = await Runner.run(agent, "We went from 2050 back to 2025, then forward to 2035.")
        print(result.final_output)
''',
        answers=("len(_journal)", "mcp.tool()", "list(_journal)", "[journal_server]"),
        alternatives={3: ("_journal.copy()", "_journal[:]")},
        blanks=(
            ("return `len(_journal)`.", "أعد `len(_journal)`."),
            ("use `@mcp.tool()`.", "استخدم `@mcp.tool()`."),
            ("return `list(_journal)`.", "أعد `list(_journal)`."),
            ("pass `[journal_server]`.", "مرّر `[journal_server]`."),
        ),
        hints=(
            ("`len()` counts the events.", "تعدّ `len()` الأحداث."),
            ("Every function the server exposes needs the same decorator.", "تحتاج كل دالة يعرضها الخادم إلى المزخرف نفسه."),
            ("`mcp_servers` takes a list of connected servers.", "يأخذ `mcp_servers` قائمة بالخوادم المتصلة."),
        ),
        success=("Correct! The agent no longer knows how the journal is stored - it only sees the server's tools, which any other agent can now reuse.",
                 "صحيح! لم يعد الوكيل يعرف كيف يُخزَّن السجل - إنه يرى أدوات الخادم فقط، والتي يمكن لأي وكيل آخر إعادة استخدامها الآن."),
        expected=SDK_NOTE,
        reflect=("What happens to the in-memory `_journal` when several agents share one long-running server, and what storage would you use instead?",
                 "ماذا يحدث لـ `_journal` المخزّن في الذاكرة عندما يتشارك عدة وكلاء خادمًا واحدًا طويل التشغيل؟ وما التخزين الذي ستستخدمه بدلًا منه؟"),
    ),
    "COURSE-012.M01.L04.EX01": Guided(
        goal=("Split one tool-heavy agent into three focused agents and let deterministic code decide whether planning runs.",
              "قسّم وكيلًا مثقلًا بالأدوات إلى ثلاثة وكلاء مركّزين، ودع كودًا حتميًا يقرر هل يعمل التخطيط."),
        steps=(
            ("Make the research agent return the typed model.", "اجعل وكيل البحث يعيد النموذج محدد النوع."),
            ("Skip planning when there are no sources.", "تخطَّ التخطيط عند غياب المصادر."),
            ("Give the planner only the goal and the sources.", "أعطِ المخطِّط الهدف والمصادر فقط."),
            ("Give the filesystem agent only the plan and destination.", "أعطِ وكيل الملفات الخطة والوجهة فقط."),
        ),
        starter='''from dataclasses import dataclass, field

@dataclass
class ResearchSourcesModel:
    research_sources: list[str] = field(default_factory=list)

calls = []          # which agents actually ran

def research_agent(goal):
    calls.append("research")
    known = {"home solar batteries": ["NREL reports", "IEEE papers"], "time travel": []}
    # Step 1: a typed result, not free text
    return ___

def planning_agent(goal, sources):
    calls.append("planning")
    return f"Plan for {goal}: " + "; ".join(f"review {source}" for source in sources)

def filesystem_agent(plan, destination):
    calls.append("filesystem")
    return {"path": destination, "content": plan}

def run_flow(goal, destination="plan.md"):
    sources = research_agent(goal)
    # Step 2: no sources -> no planning (a code decision, not an LLM decision)
    if ___:
        return {"status": "skipped", "reason": "no research sources found"}
    # Step 3: the planner receives only what it needs
    plan = ___
    # Step 4: so does the filesystem agent
    return ___

print(run_flow("home solar batteries"), calls)
''',
        answers=('ResearchSourcesModel(research_sources=known.get(goal, []))', "not sources.research_sources",
                 "planning_agent(goal, sources.research_sources)", "filesystem_agent(plan, destination)"),
        checks=(
            check("isinstance(research_agent('home solar batteries'), ResearchSourcesModel) and research_agent('time travel').research_sources == []", True,
                  "Blank 1: return `ResearchSourcesModel(research_sources=known.get(goal, []))`.", "الفراغ 1: أعد `ResearchSourcesModel(research_sources=known.get(goal, []))`."),
            check("(lambda: (calls.clear(), run_flow('time travel'), list(calls))[1:])()",
                  [{"status": "skipped", "reason": "no research sources found"}, ["research"]],
                  "Blank 2: when `sources.research_sources` is empty, stop before the planner runs.",
                  "الفراغ 2: عندما تكون `sources.research_sources` فارغة، توقّف قبل تشغيل المخطِّط."),
            check("(lambda: (calls.clear(), run_flow('home solar batteries', 'out.md'), list(calls))[1:])()",
                  [{"path": "out.md", "content": "Plan for home solar batteries: review NREL reports; review IEEE papers"}, ["research", "planning", "filesystem"]],
                  "Blanks 3-4: call `planning_agent(goal, sources.research_sources)`, then `filesystem_agent(plan, destination)`.",
                  "الفراغان 3 و4: استدعِ `planning_agent(goal, sources.research_sources)` ثم `filesystem_agent(plan, destination)`."),
        ),
        hints=(
            ("Construct the dataclass with the list of sources for the goal.", "أنشئ صنف البيانات مع قائمة المصادر الخاصة بالهدف."),
            ("An empty list is falsy, so `not sources.research_sources` detects it.", "القائمة الفارغة قيمتها المنطقية خاطئة، لذا يكشفها `not sources.research_sources`."),
            ("Each agent call passes only its own inputs.", "يمرّر كل استدعاء وكيل مدخلاته الخاصة فقط."),
        ),
        success=("Correct! Each agent has one job and only the context it needs, and a plain `if` - not a prompt - decides that an empty source list skips planning.",
                 "صحيح! لكل وكيل مهمة واحدة والسياق الذي يحتاجه فقط، ويقرر `if` بسيط - لا موجّه - أن قائمة المصادر الفارغة تتخطى التخطيط."),
        expected=STUB_NOTE,
        reflect=("Name one token-cost benefit, one reliability benefit, and one failure mode that this decomposition does not remove.",
                 "اذكر فائدة واحدة في تكلفة الرموز، وفائدة واحدة في الموثوقية، ونمط فشل واحد لا يزيله هذا التقسيم."),
    ),
    "COURSE-012.M01.L04.EX02": Guided(
        goal=("Guard an agent handoff: check the plan's type and quality, retry at most twice with feedback, then fail clearly.",
              "احمِ تسليم الوكيل: تحقّق من نوع الخطة وجودتها، وأعد المحاولة مرتين على الأكثر مع ملاحظات، ثم افشل بوضوح."),
        steps=(
            ("Reject plans that are not detailed or shorter than 40 characters.", "ارفض الخطط غير المفصّلة أو التي تقل عن 40 حرفًا."),
            ("Allow one attempt plus at most two retries.", "اسمح بمحاولة واحدة مع إعادتين على الأكثر."),
            ("Log the validated plan before the handoff.", "سجّل الخطة المُتحقَّق منها قبل التسليم."),
            ("Return a clear static failure after the last attempt.", "أعد فشلًا ثابتًا وواضحًا بعد المحاولة الأخيرة."),
        ),
        starter='''from dataclasses import dataclass

@dataclass
class ResearchPlanModel:
    research_plan: str
    is_detailed: bool

feedback_seen = []
handoff_log = []

def planning_agent(goal, feedback=None):
    """Stub: the first draft is weak; with feedback the next one is good."""
    feedback_seen.append(feedback)
    if feedback is None:
        return ResearchPlanModel("Read about it.", False)
    return ResearchPlanModel("1. Survey NREL reports. 2. Compare chemistries. 3. Summarize costs.", True)

def output_guardrail(plan):
    """Return (ok, feedback)."""
    if not isinstance(plan, ResearchPlanModel):            # deterministic type check first
        return False, "Return a ResearchPlanModel."
    # Step 1: the quality bar
    if ___:
        return False, "Too short: list at least three concrete research steps."
    return True, None

def plan_with_retries(goal, agent=planning_agent, max_retries=2):
    feedback = None
    # Step 2: the first attempt plus at most max_retries retries - never unbounded
    for attempt in range(___):
        plan = agent(goal, feedback)
        ok, feedback = output_guardrail(plan)
        if ok:
            # Step 3: observe the validated payload; never modify it
            ___
            return plan
    # Step 4: a clear, static failure
    return ___

print(plan_with_retries("home batteries"), feedback_seen, handoff_log)
''',
        answers=(
            "not plan.is_detailed or len(plan.research_plan) < 40",
            "max_retries + 1",
            "handoff_log.append(plan.research_plan)",
            'ResearchPlanModel("Planning failed: the plan did not meet the quality bar.", False)',
        ),
        checks=(
            check("[plan_with_retries('x').is_detailed, feedback_seen[:2]]", [True, [None, "Too short: list at least three concrete research steps."]],
                  "Blank 1: reject when `not plan.is_detailed or len(plan.research_plan) < 40`; the feedback then reaches the second attempt.",
                  "الفراغ 1: ارفض عندما يكون `not plan.is_detailed or len(plan.research_plan) < 40`؛ فتصل الملاحظات إلى المحاولة الثانية."),
            check("(lambda tries: [plan_with_retries('x', agent=lambda g, f: (tries.append(1), ResearchPlanModel('Read.', False))[1]).research_plan, len(tries)])([])",
                  ["Planning failed: the plan did not meet the quality bar.", 3],
                  "Blanks 2 and 4: three attempts in total, then the static failure plan.",
                  "الفراغان 2 و4: ثلاث محاولات إجمالًا، ثم خطة الفشل الثابتة."),
            check("handoff_log[:1]", ["1. Survey NREL reports. 2. Compare chemistries. 3. Summarize costs."],
                  "Blank 3: append the validated `plan.research_plan` to `handoff_log` before returning.",
                  "الفراغ 3: أضف `plan.research_plan` المُتحقَّق منه إلى `handoff_log` قبل الإرجاع."),
        ),
        hints=(
            ("Two conditions joined with `or`: not detailed, or too short.", "شرطان مرتبطان بـ `or`: غير مفصّلة، أو قصيرة جدًا."),
            ("`range(max_retries + 1)` gives the first attempt plus the retries.", "يعطي `range(max_retries + 1)` المحاولة الأولى مع الإعادات."),
            ("The callback only records; the guardrail is what enforces.", "يكتفي رد النداء بالتسجيل؛ أما الحاجز فهو الذي يفرض."),
        ),
        success=("Correct! Bad output is caught at the boundary, the retry budget is finite, feedback improves the next attempt, and the callback observes without changing anything.",
                 "صحيح! يُلتقط المخرج السيئ عند الحد، وميزانية الإعادة محدودة، وتحسّن الملاحظات المحاولة التالية، ويراقب رد النداء دون تغيير أي شيء."),
        expected=STUB_NOTE,
        reflect=("How would you defend against instructions injected inside the plan text before the FilesystemAgent acts on it?",
                 "كيف ستدافع ضد التعليمات المحقونة داخل نص الخطة قبل أن يعمل عليها FilesystemAgent؟"),
    ),
    "COURSE-012.M01.L05.EX01": Guided(
        goal=("Turn year arithmetic into a ReAct loop: act with a tool, observe the result, then decide the next step.",
              "حوّل حساب السنوات إلى حلقة ReAct: نفّذ بأداة، ولاحظ النتيجة، ثم قرر الخطوة التالية."),
        steps=(
            ("Call the chosen tool instead of computing in the prompt.", "استدعِ الأداة المختارة بدل الحساب داخل الموجّه."),
            ("Record each action and its observation in the trace.", "سجّل كل إجراء وملاحظته في التتبّع."),
            ("Make the observation the new state.", "اجعل الملاحظة هي الحالة الجديدة."),
        ),
        starter='''def travel_back(year, years):
    return year - years

def travel_forward(year, years):
    return year + years

TOOLS = {"travel_back": travel_back, "travel_forward": travel_forward}
# The agent's decisions, one per step: 25 back, 10 forward, 5 back
decisions = [("travel_back", 25), ("travel_forward", 10), ("travel_back", 5)]

def react(start_year, decisions):
    year, trace = start_year, []
    for action, years in decisions:
        # Step 1: act - the tool does the arithmetic
        observation = ___
        # Step 2: keep the action and what it returned
        trace.append(___)
        # Step 3: the observation is the state for the next decision
        year = ___
    return year, trace

final_year, trace = react(2050, decisions)
print(final_year)
for step in trace:
    print(step)
''',
        answers=("TOOLS[action](year, years)", '{"action": action, "years": years, "observation": observation}', "observation"),
        checks=(
            check("final_year", 2030, "Blanks 1 and 3: call `TOOLS[action](year, years)` and carry its result forward.",
                  "الفراغان 1 و3: استدعِ `TOOLS[action](year, years)` ومرّر نتيجتها إلى الخطوة التالية."),
            check("[(s['action'], s['observation']) for s in trace]", [["travel_back", 2025], ["travel_forward", 2035], ["travel_back", 2030]],
                  "Blank 2: append a dictionary with `action`, `years` and `observation`.", "الفراغ 2: أضف قاموسًا يحتوي على `action` و`years` و`observation`."),
        ),
        hints=(
            ("`TOOLS[action]` is the function; call it with the current year and the step.", "`TOOLS[action]` هي الدالة؛ استدعها مع السنة الحالية والخطوة."),
            ("A trace entry records what was done and what came back.", "يسجّل مدخل التتبّع ما فُعل وما عاد."),
            ("Without updating `year`, every step would start from 2050 again.", "دون تحديث `year` ستبدأ كل خطوة من 2050 مجددًا."),
        ),
        success=("Correct! Each action produces an observation that feeds the next decision - that act/observe loop is what makes it ReAct rather than one chain-of-thought pass.",
                 "صحيح! ينتج كل إجراء ملاحظة تغذّي القرار التالي - وحلقة التنفيذ/الملاحظة هذه هي ما يجعلها ReAct لا مرورًا واحدًا بسلسلة التفكير."),
        expected=STUB_NOTE,
    ),
    "COURSE-012.M01.L05.EX02": Guided(
        goal=("Bound a reasoning system: explore a limited number of migration plans and enforce the downtime rule in code.",
              "قيّد نظام استدلال: استكشف عددًا محدودًا من خطط الترحيل، وطبّق قاعدة التوقف عن الخدمة في الكود."),
        steps=(
            ("Write the downtime rule as a function.", "اكتب قاعدة التوقف عن الخدمة دالةً."),
            ("Explore at most `MAX_BRANCHES` alternatives.", "استكشف `MAX_BRANCHES` بديلًا على الأكثر."),
            ("Pick the lowest-risk plan that passes the rule.", "اختر الخطة الأقل خطرًا التي تجتاز القاعدة."),
        ),
        starter='''MAX_BRANCHES = 3
DOWNTIME_LIMIT_MINUTES = 15

# Alternative migration paths proposed by the planner (the Tree-of-Thoughts step)
branches = [
    {"name": "big-bang cutover", "downtime_minutes": 120, "risk": 0.20},
    {"name": "blue-green switch", "downtime_minutes": 5, "risk": 0.30},
    {"name": "strangler fig", "downtime_minutes": 0, "risk": 0.40},
    {"name": "dual-write migration", "downtime_minutes": 2, "risk": 0.25},
]

# Step 1: the hard rule lives in code, not only in a prompt
def meets_downtime(branch):
    return ___

# Step 2: a hard cap on exploration cost
explored = ___

valid = [branch for branch in explored if meets_downtime(branch)]
# Step 3: lowest risk among the valid plans (None if there is none)
chosen = ___
print([b["name"] for b in explored], "->", chosen)
''',
        answers=('branch["downtime_minutes"] <= DOWNTIME_LIMIT_MINUTES', "branches[:MAX_BRANCHES]",
                 'min(valid, key=lambda branch: branch["risk"]) if valid else None'),
        checks=(
            check("[meets_downtime({'downtime_minutes': m}) for m in (0, 15, 16)]", [True, True, False],
                  "Blank 1: allow downtime up to and including `DOWNTIME_LIMIT_MINUTES`.", "الفراغ 1: اسمح بالتوقف حتى `DOWNTIME_LIMIT_MINUTES` شاملًا."),
            check("[b['name'] for b in explored]", ["big-bang cutover", "blue-green switch", "strangler fig"],
                  "Blank 2: keep only the first `MAX_BRANCHES` branches.", "الفراغ 2: احتفظ بأول `MAX_BRANCHES` فرعًا فقط."),
            check("chosen['name']", "blue-green switch",
                  "Blank 3: the big-bang cutover is lowest risk but breaks the rule; choose the lowest risk among `valid`.",
                  "الفراغ 3: الانتقال الفوري أقل خطرًا لكنه يخالف القاعدة؛ اختر الأقل خطرًا من بين `valid`."),
        ),
        hints=(
            ("Compare the branch's downtime with the limit.", "قارن مدة توقف الفرع بالحد."),
            ("Slicing `[:n]` caps how many branches are explored.", "يحدّ التقطيع `[:n]` عدد الفروع المستكشفة."),
            ("`min(items, key=...)` picks the item with the smallest key.", "يختار `min(items, key=...)` العنصر ذا المفتاح الأصغر."),
        ),
        success=("Correct! The cheapest-risk plan was rejected by code because it breaks the downtime rule, and the exploration budget stayed fixed even though a fourth plan existed.",
                 "صحيح! رفض الكودُ الخطة الأقل خطرًا لأنها تخالف قاعدة التوقف، وبقيت ميزانية الاستكشاف ثابتة رغم وجود خطة رابعة."),
        reflect=("Decompose the migration goal into 4-6 subproblems. Where would a ReAct tool call, a ToT branch and a critic loop each add value - and which would you drop for cost?",
                 "قسّم هدف الترحيل إلى 4-6 مشكلات فرعية. أين يضيف كلٌّ من استدعاء أداة ReAct وفرع ToT وحلقة الناقد قيمة؟ وأيها ستحذفه بسبب التكلفة؟"),
    ),
    "COURSE-012.M01.L06.EX01": Guided(
        goal=("Rank documents with TF-IDF and with semantic embeddings, and see where each one wins.",
              "رتّب المستندات باستخدام TF-IDF وباستخدام التضمينات الدلالية، وتعرّف أين يتفوق كلٌّ منهما."),
        steps=(
            ("Fit TF-IDF vectors for the documents.", "درّب متجهات TF-IDF للمستندات."),
            ("Score a query against every document by cosine similarity.", "قيّم الاستعلام مقابل كل مستند بتشابه جيب التمام."),
            ("Compute Chroma-style cosine distances for the semantic vectors.", "احسب مسافات جيب التمام على طريقة Chroma للمتجهات الدلالية."),
        ),
        starter='''import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    "The cat sat on the mat.",
    "A kitten is resting on a rug.",
    "Stock prices fell sharply today.",
    "The market dropped after the report.",
    "Error code E42 means the disk is full.",
    "Our servers ran out of storage space.",
]

# Step 1: lexical vectors for every document
vectorizer = TfidfVectorizer()
doc_vectors = ___

def lexical_top3(query):
    # Step 2: similarity of the query to every document
    scores = ___
    return np.argsort(-scores)[:3].tolist()

# Stand-in semantic embeddings (pets, finance, storage), as a sentence-embedding model would place them
semantic_docs = np.array([[0.9, 0.1, 0.0], [0.85, 0.1, 0.05], [0.05, 0.95, 0.1],
                          [0.1, 0.9, 0.05], [0.0, 0.1, 0.95], [0.05, 0.05, 0.9]])
semantic_queries = {"error code E42": np.array([0.1, 0.1, 0.9]), "a small cat napping": np.array([0.95, 0.05, 0.0])}

def semantic_top3(query):
    q = semantic_queries[query]
    # Step 3: Chroma's cosine distance = 1 - cosine similarity (smaller means closer)
    distances = ___
    return np.argsort(distances)[:3].tolist()

for query in semantic_queries:
    print(query, "| lexical:", lexical_top3(query), "| semantic:", semantic_top3(query))
''',
        answers=(
            "vectorizer.fit_transform(documents)",
            "cosine_similarity(vectorizer.transform([query]), doc_vectors)[0]",
            "1 - (semantic_docs @ q) / (np.linalg.norm(semantic_docs, axis=1) * np.linalg.norm(q))",
        ),
        checks=(
            check("doc_vectors.shape[0] == 6 and len(vectorizer.vocabulary_) > 10", True,
                  "Blank 1: `vectorizer.fit_transform(documents)` learns the vocabulary and builds the vectors.",
                  "الفراغ 1: يتعلّم `vectorizer.fit_transform(documents)` المفردات ويبني المتجهات."),
            check("[lexical_top3('error code E42')[0], lexical_top3('cat on the mat')[0]]", [4, 0],
                  "Blank 2: transform the query with the same vectorizer, then compare it with `doc_vectors`.",
                  "الفراغ 2: حوّل الاستعلام بالـ vectorizer نفسه، ثم قارنه بـ `doc_vectors`."),
            check("[sorted(semantic_top3('a small cat napping')[:2]), semantic_top3('error code E42')[:2] == [4, 5] or semantic_top3('error code E42')[:2] == [5, 4]]", [[0, 1], True],
                  "Blank 3: distance = 1 - cosine similarity; sort ascending so the closest come first.",
                  "الفراغ 3: المسافة = 1 - تشابه جيب التمام؛ رتّب تصاعديًا ليأتي الأقرب أولًا."),
        ),
        hints=(
            ("`fit_transform` learns the vocabulary; `transform` reuses it for new text.", "يتعلّم `fit_transform` المفردات، ويعيد `transform` استخدامها للنص الجديد."),
            ("`cosine_similarity(A, B)` returns a matrix; take row `[0]` for one query.", "تعيد `cosine_similarity(A, B)` مصفوفة؛ خذ الصف `[0]` لاستعلام واحد."),
            ("Cosine similarity is the dot product divided by both lengths.", "تشابه جيب التمام هو الضرب النقطي مقسومًا على الطولين."),
        ),
        success=("Correct! TF-IDF wins on the exact token 'E42'; the semantic vectors find the kitten on the rug although the query never says 'kitten' - and in Chroma, the smaller distance is the better match.",
                 "صحيح! يتفوق TF-IDF في الرمز الدقيق 'E42'، بينما تجد المتجهات الدلالية القطة الصغيرة على السجادة رغم أن الاستعلام لم يذكر 'kitten' - وفي Chroma تكون المسافة الأصغر هي المطابقة الأفضل."),
        expected=(
            "ChromaDB and embedding models are not installed in the sandbox, so the semantic vectors are stand-ins and distances are computed the way Chroma's cosine space does.",
            "ChromaDB ونماذج التضمين غير مثبّتة في بيئة التدريب، لذا فالمتجهات الدلالية بدائل، وتُحسب المسافات كما يحسبها فضاء جيب التمام في Chroma.",
        ),
    ),
    "COURSE-012.M01.L07.EX01": Guided(
        goal=("Find the false failures a strict string evaluator creates, fix them with normalization, and measure the pass rate again.",
              "اكتشف حالات الفشل الكاذبة التي يُحدثها مقيِّم نصي صارم، وأصلحها بالتطبيع، ثم قِس معدل النجاح مجددًا."),
        steps=(
            ("Normalize case, punctuation and surrounding spaces.", "وحّد حالة الأحرف وعلامات الترقيم والمسافات المحيطة."),
            ("Compute a pass rate for any evaluator.", "احسب معدل النجاح لأي مقيِّم."),
            ("List the questions that only fail because of strict equality.", "اذكر الأسئلة التي تفشل فقط بسبب المساواة الصارمة."),
        ),
        starter='''import re

benchmark = [
    {"question": "What is the refund window?", "expected": "30 days", "answer": "30 days."},
    {"question": "Which plan includes SSO?", "expected": "Enterprise", "answer": "enterprise"},
    {"question": "Who approves travel?", "expected": "Your manager", "answer": "Your manager"},
    {"question": "What is the daily per-diem?", "expected": "50 USD", "answer": "40 USD"},
    {"question": "Where are receipts uploaded?", "expected": "the expenses portal", "answer": " The Expenses Portal!"},
]

def strict_pass(answer, expected):
    return answer == expected

# Step 1: lowercase, drop punctuation, trim spaces
def normalize(text):
    return ___

def normalized_pass(answer, expected):
    return normalize(answer) == normalize(expected)

# Step 2: share of benchmark rows an evaluator passes
def pass_rate(evaluator):
    return ___

# Step 3: questions that fail strictly but pass after normalization (evaluator failures, not agent failures)
false_failures = ___

print("strict", pass_rate(strict_pass), "| normalized", pass_rate(normalized_pass))
print("false failures:", false_failures)
''',
        answers=(
            r're.sub(r"[^\w\s]", "", text).strip().lower()',
            'sum(evaluator(row["answer"], row["expected"]) for row in benchmark) / len(benchmark)',
            '[row["question"] for row in benchmark if not strict_pass(row["answer"], row["expected"]) and normalized_pass(row["answer"], row["expected"])]',
        ),
        checks=(
            check("[normalize(' The Expenses Portal!'), normalize('30 days.')]", ["the expenses portal", "30 days"],
                  "Blank 1: remove punctuation (e.g. `re.sub(r\"[^\\w\\s]\", \"\", text)`), then `.strip().lower()`.",
                  "الفراغ 1: احذف علامات الترقيم (مثل `re.sub(r\"[^\\w\\s]\", \"\", text)`) ثم `.strip().lower()`."),
            check("[pass_rate(strict_pass), pass_rate(normalized_pass)]", [0.2, 0.8],
                  "Blank 2: sum the evaluator's True/False results and divide by the number of rows.",
                  "الفراغ 2: اجمع نتائج المقيِّم True/False واقسم على عدد الصفوف."),
            check("false_failures", ["What is the refund window?", "Which plan includes SSO?", "Where are receipts uploaded?"],
                  "Blank 3: keep rows where `strict_pass` is False but `normalized_pass` is True.",
                  "الفراغ 3: احتفظ بالصفوف التي يكون فيها `strict_pass` خاطئًا و`normalized_pass` صحيحًا."),
        ),
        hints=(
            ("`[^\\w\\s]` matches anything that is neither a word character nor whitespace.", "يطابق `[^\\w\\s]` أي شيء ليس حرفًا من كلمة ولا مسافة."),
            ("Summing booleans counts the True values.", "جمع القيم المنطقية يعدّ القيم True."),
            ("A false failure is the evaluator's mistake, not the agent's.", "الفشل الكاذب خطأ المقيِّم لا خطأ الوكيل."),
        ),
        success=("Correct! Three of the four 'failures' were the evaluator's fault; only the wrong per-diem is a real generator failure. Fix the measurement before you change the agent.",
                 "صحيح! كانت ثلاث من حالات «الفشل» الأربع خطأ المقيِّم؛ ولا يُعدّ فشلًا حقيقيًا للمولّد إلا البدل اليومي الخاطئ. أصلح القياس قبل أن تغيّر الوكيل."),
        reflect=("For which kinds of answers would you add a typed LLM evaluator instead of string rules?",
                 "لأي أنواع من الإجابات ستضيف مقيِّمًا لغويًا محدد النوع بدل قواعد النصوص؟"),
    ),
    "COURSE-012.M01.L07.EX02": Guided(
        goal=("Ground a policy answer in retrieved context, regenerate with feedback at most twice, then fall back safely - and score answers with a rubric.",
              "اربط إجابة السياسات بالسياق المسترجَع، وأعد التوليد مع الملاحظات مرتين على الأكثر، ثم ارجع إلى بديل آمن - وقيّم الإجابات بمعيار."),
        steps=(
            ("An answer is grounded when every claim appears in the context.", "تكون الإجابة مرتبطة بالمصدر عندما يظهر كل ادعاء فيها في السياق."),
            ("Pass the unsupported claims back as feedback.", "أعد الادعاءات غير المدعومة ملاحظاتٍ."),
            ("Return the static fallback after the last attempt.", "أعد البديل الثابت بعد المحاولة الأخيرة."),
            ("Pass an answer when its weighted rubric score reaches the threshold.", "أنجح الإجابة عندما تبلغ درجتها الموزونة العتبة."),
        ),
        starter='''CONTEXT = {"Employees may work remotely up to 3 days per week.", "Remote work requires manager approval."}
FALLBACK = "I can't answer that reliably. Please check the HR policy page."

def split_claims(answer):
    return [part.strip() + "." for part in answer.split(".") if part.strip()]

# Step 1: grounded = every claim is in the authoritative context
def is_grounded(answer):
    return ___

def answer_with_grounding(question, generator, max_retries=2):
    feedback = None
    for attempt in range(max_retries + 1):
        draft = generator(question, feedback)
        if is_grounded(draft):
            return {"question": question, "answer": draft, "references": sorted(set(split_claims(draft))), "attempts": attempt + 1}
        # Step 2: tell the next attempt exactly which claims were unsupported
        feedback = ___
    # Step 3: retries exhausted
    return ___

RUBRIC_WEIGHTS = {"relevance": 0.3, "completeness": 0.2, "grounding": 0.4, "tool_use": 0.1}

# Step 4: weighted score of the 0-1 rubric scores, compared with the threshold
def passes(scores, threshold=0.7):
    return ___

drafts = iter(["Employees may work remotely 5 days per week.",
               "Employees may work remotely up to 3 days per week. Remote work requires manager approval."])
print(answer_with_grounding("How many remote days?", lambda q, f: next(drafts)))
''',
        answers=(
            "all(claim in CONTEXT for claim in split_claims(answer))",
            "[claim for claim in split_claims(draft) if claim not in CONTEXT]",
            '{"question": question, "answer": FALLBACK, "references": [], "attempts": max_retries + 1}',
            "sum(RUBRIC_WEIGHTS[key] * scores[key] for key in RUBRIC_WEIGHTS) >= threshold",
        ),
        checks=(
            check("[is_grounded('Remote work requires manager approval.'), is_grounded('Remote work requires manager approval. Pets are allowed.')]", [True, False],
                  "Blank 1: use `all(...)` over `split_claims(answer)`.", "الفراغ 1: استخدم `all(...)` على `split_claims(answer)`."),
            check("(lambda seen: [answer_with_grounding('q', lambda q, f: (seen.append(f), 'Pets are allowed.')[1])['answer'], seen])([])",
                  ["I can't answer that reliably. Please check the HR policy page.", [None, ["Pets are allowed."], ["Pets are allowed."]]],
                  "Blanks 2-3: feed back the unsupported claims, and after three attempts return the FALLBACK answer.",
                  "الفراغان 2 و3: أعد الادعاءات غير المدعومة ملاحظاتٍ، وبعد ثلاث محاولات أعد إجابة FALLBACK."),
            check("answer_with_grounding('q', lambda q, f: 'Remote work requires manager approval.')['attempts']", 1,
                  "A grounded first draft is returned immediately.", "تُعاد المسودة الأولى المرتبطة بالمصدر فورًا."),
            check("[passes({'relevance': 1, 'completeness': 1, 'grounding': 1, 'tool_use': 0}), passes({'relevance': 1, 'completeness': 1, 'grounding': 0, 'tool_use': 1})]", [True, False],
                  "Blank 4: multiply each score by its weight, sum, and compare with the threshold.",
                  "الفراغ 4: اضرب كل درجة في وزنها، واجمع، ثم قارن بالعتبة."),
        ),
        hints=(
            ("`all(claim in CONTEXT for claim in ...)` is True only if every claim is supported.", "تكون `all(claim in CONTEXT for claim in ...)` صحيحة فقط إذا كان كل ادعاء مدعومًا."),
            ("The feedback is the list of claims that are not in the context.", "الملاحظات هي قائمة الادعاءات غير الموجودة في السياق."),
            ("A weighted score is `sum(weight * score)`.", "الدرجة الموزونة هي `sum(weight * score)`."),
        ),
        success=("Correct! Unsupported answers are regenerated with precise feedback, the loop always ends, and when grounding keeps failing the user gets a safe answer instead of a confident fabrication.",
                 "صحيح! تُعاد الإجابات غير المدعومة مع ملاحظات دقيقة، وتنتهي الحلقة دائمًا، وعندما يستمر فشل الربط بالمصدر يحصل المستخدم على إجابة آمنة بدل اختلاق واثق."),
        expected=STUB_NOTE,
        reflect=("How would you calibrate the 0.7 threshold with human-labelled answers, and how do annotated failures become a regression dataset?",
                 "كيف ستعاير العتبة 0.7 بإجابات صنّفها البشر؟ وكيف تصبح حالات الفشل الموسومة مجموعة بيانات للاختبارات التراجعية؟"),
    ),
    "COURSE-012.M01.L09.EX01": Guided(
        goal=("Run a research loop with explicit state, a hard iteration cap, a confidence stop, stagnation detection and a bounded context.",
              "شغّل حلقة بحث بحالة صريحة، وحد أقصى صارم للتكرارات، وتوقف عند الثقة، وكشف للركود، وسياق محدود."),
        steps=(
            ("Stop at the maximum number of iterations.", "توقّف عند الحد الأقصى للتكرارات."),
            ("Send only the last three findings as context.", "أرسل آخر ثلاث نتائج فقط سياقًا."),
            ("Stop when confidence reaches the target.", "توقّف عندما تبلغ الثقة الهدف."),
            ("Stop when an iteration adds nothing new.", "توقّف عندما لا يضيف التكرار شيئًا جديدًا."),
        ),
        starter='''def run_research(goal, research_step, max_iterations=5, confidence_target=0.9):
    state = {"goal": goal, "findings": [], "iteration": 0, "confidence": 0.0, "status": "running"}
    while True:
        # Step 1: the hard cap
        if ___:
            state["status"] = "max_iterations"
            break
        # Step 2: a bounded context - only the most recent three findings
        update = research_step(goal, ___)
        state["iteration"] += 1
        new_findings = [f for f in update["findings"] if f not in state["findings"]]
        state["findings"] += new_findings
        state["confidence"] = update["confidence"]
        # Step 3: goal satisfied
        if ___:
            state["status"] = "confident"
            break
        # Step 4: stagnation - this iteration found nothing new
        if ___:
            state["status"] = "stagnated"
            break
    return state

FACTS = ["LFP cells are cheaper", "NMC cells are denser", "Recycling recovers lithium", "Grid batteries smooth demand peaks"]

def steady_researcher(goal, context):
    known = len(context)
    return {"findings": FACTS[: known + 1], "confidence": 0.3 + 0.2 * known}

final = run_research("home battery trade-offs", steady_researcher)
print(final["status"], final["iteration"], final["findings"])
''',
        answers=('state["iteration"] >= max_iterations', 'state["findings"][-3:]', 'state["confidence"] >= confidence_target', "not new_findings"),
        checks=(
            check("[final['status'], final['iteration'], len(final['findings'])]", ["confident", 4, 4],
                  "Blanks 2-3: pass the last three findings, and stop once confidence reaches the target.",
                  "الفراغان 2 و3: مرّر آخر ثلاث نتائج، وتوقّف بمجرد بلوغ الثقة الهدف."),
            check("(lambda s: [s['status'], s['iteration']])(run_research('g', lambda goal, context: {'findings': ['same fact'], 'confidence': 0.2}))", ["stagnated", 2],
                  "Blank 4: stop as soon as an iteration adds no new finding.", "الفراغ 4: توقّف بمجرد ألا يضيف التكرار أي نتيجة جديدة."),
            check("(lambda s: [s['status'], s['iteration']])(run_research('g', lambda goal, context: {'findings': [f'fact {len(context)}-{n}' for n in range(2)], 'confidence': 0.1}, max_iterations=3))", ["max_iterations", 3],
                  "Blank 1: stop when `state[\"iteration\"]` reaches `max_iterations`.", "الفراغ 1: توقّف عندما يبلغ `state[\"iteration\"]` القيمة `max_iterations`."),
            check("(lambda seen: run_research('g', lambda goal, context: (seen.append(len(context)), {'findings': [f'f{len(seen)}a', f'f{len(seen)}b'], 'confidence': 0.0})[1], max_iterations=4) and seen)([])", [0, 2, 3, 3],
                  "Blank 2: the context is capped at the three most recent findings.", "الفراغ 2: يُحدّ السياق بأحدث ثلاث نتائج."),
        ),
        hints=(
            ("Every loop needs an exit that does not depend on the model.", "تحتاج كل حلقة إلى مخرج لا يعتمد على النموذج."),
            ("Negative slicing `[-3:]` keeps the last three items.", "يحتفظ التقطيع السالب `[-3:]` بآخر ثلاثة عناصر."),
            ("`new_findings` is empty when the iteration repeated what was already known.", "تكون `new_findings` فارغة عندما يكرر التكرار ما كان معروفًا."),
        ),
        success=("Correct! The loop ends for exactly one recorded reason - confident, stagnated or capped - and the model never sees more than three recent findings.",
                 "صحيح! تنتهي الحلقة لسبب واحد مسجّل بالضبط - ثقة أو ركود أو بلوغ الحد - ولا يرى النموذج أبدًا أكثر من ثلاث نتائج حديثة."),
        expected=STUB_NOTE,
        reflect=("Why should the final synthesis step never perform new research?", "لماذا يجب ألا تُجري خطوة التوليف النهائية بحثًا جديدًا أبدًا؟"),
    ),
    "COURSE-012.M01.L09.EX02": Guided(
        goal=("Implement an orchestrator loop and a round-robin collaboration loop for the same goal, and compare their model calls.",
              "نفّذ حلقة منسِّق وحلقة تعاون بالتناوب للهدف نفسه، وقارن عدد استدعاءات النموذج فيهما."),
        steps=(
            ("End the orchestration loop on `finalize`.", "أنهِ حلقة التنسيق عند `finalize`."),
            ("Run the worker the orchestrator chose.", "شغّل العامل الذي اختاره المنسِّق."),
            ("End collaboration when the critic's score reaches consensus.", "أنهِ التعاون عندما تبلغ درجة الناقد الإجماع."),
            ("Find the cheaper architecture.", "حدّد المعمارية الأقل تكلفة."),
        ),
        starter='''calls = {"orchestration": 0, "collaboration": 0}    # model calls made by each design

def orchestrator_decide(state):
    """Stub orchestrator: research until two findings, then analyze, then finalize."""
    calls["orchestration"] += 1
    if len(state["findings"]) < 2:
        return {"action": "delegate", "worker": "research"}
    if not state["analysis"]:
        return {"action": "delegate", "worker": "analysis"}
    return {"action": "finalize"}

def research_worker(state):
    calls["orchestration"] += 1
    state["findings"].append(f"finding {len(state['findings']) + 1}")

def analysis_worker(state):
    calls["orchestration"] += 1
    state["analysis"] = "costs fall as chemistry improves"

WORKERS = {"research": research_worker, "analysis": analysis_worker}

def orchestrate(max_iterations=6):
    state = {"findings": [], "analysis": None, "decisions": []}
    for _ in range(max_iterations):
        decision = orchestrator_decide(state)
        state["decisions"].append(decision["action"] + ":" + decision.get("worker", ""))
        # Step 1: the orchestrator decided the work is done
        if ___:
            break
        # Step 2: run the chosen worker on the shared state
        ___
    return state

def collaborate(rounds=3, consensus=0.7):
    state = {"notes": [], "scores": []}
    for round_number in range(rounds):
        for role in ("researcher", "critic", "synthesizer"):
            calls["collaboration"] += 1
            state["notes"].append(f"{role} round {round_number + 1}")
        score = round(0.5 + 0.2 * round_number, 2)      # the critic's agreement this round
        state["scores"].append(score)
        # Step 3: consensus reached
        if ___:
            break
    return state

orchestrated, collaborated = orchestrate(), collaborate()
# Step 4: the design that needed fewer model calls
cheaper = ___
print(orchestrated["decisions"], collaborated["scores"], calls, cheaper)
''',
        answers=('decision["action"] == "finalize"', 'WORKERS[decision["worker"]](state)', "score >= consensus", "min(calls, key=calls.get)"),
        checks=(
            check("orchestrated['decisions']", ["delegate:research", "delegate:research", "delegate:analysis", "finalize:"],
                  "Blanks 1-2: break on `finalize`, otherwise call `WORKERS[decision[\"worker\"]](state)`.",
                  "الفراغان 1 و2: اخرج عند `finalize`، وإلا فاستدعِ `WORKERS[decision[\"worker\"]](state)`."),
            check("[collaborated['scores'], calls['collaboration']]", [[0.5, 0.7], 6],
                  "Blank 3: stop when the round's score is at least `consensus`.", "الفراغ 3: توقّف عندما تكون درجة الجولة `consensus` على الأقل."),
            check("[calls['orchestration'], cheaper]", [7, "collaboration"],
                  "Blank 4: pick the key of `calls` with the smallest value: `min(calls, key=calls.get)`.",
                  "الفراغ 4: اختر مفتاح `calls` ذا القيمة الأصغر: `min(calls, key=calls.get)`."),
        ),
        hints=(
            ("Compare the decision's action with \"finalize\".", "قارن إجراء القرار بـ \"finalize\"."),
            ("`WORKERS[name]` is a function; call it with `state`.", "`WORKERS[name]` دالة؛ استدعها مع `state`."),
            ("`min(d, key=d.get)` returns the key with the smallest value.", "يعيد `min(d, key=d.get)` المفتاح ذا القيمة الأصغر."),
        ),
        success=("Correct! The orchestrator spent 7 calls with one decision-maker that is easy to trace; the collaboration reached consensus in two rounds, 6 calls across three peers - cheaper here, but harder to debug.",
                 "صحيح! أنفق المنسِّق 7 استدعاءات مع صانع قرار واحد يسهل تتبّعه، بينما وصل التعاون إلى الإجماع في جولتين بـ 6 استدعاءات بين ثلاثة أقران - أقل تكلفة هنا لكنه أصعب في التنقيح."),
        expected=STUB_NOTE,
        reflect=("Which design better fits a research goal you care about, judging by quality, debugging effort and coordination overhead?",
                 "أي التصميمين يناسب هدف بحث يهمك أكثر، من حيث الجودة وجهد التنقيح وتكلفة التنسيق؟"),
    ),
    "COURSE-012.M01.L10.EX01": Guided(
        goal=("Implement the cognitive workspace's evaluator and attention router: detect contradictions, react to stagnation and present when confident.",
              "نفّذ المقيِّم وموجّه الانتباه في مساحة العمل المعرفية: اكتشف التناقضات، وتفاعل مع الركود، واعرض النتيجة عند الثقة."),
        steps=(
            ("Find claims whose negation is also present.", "جد الادعاءات التي يوجد نفيها أيضًا."),
            ("On a contradiction, switch to hypothesis testing.", "عند التناقض، انتقل إلى اختبار الفرضيات."),
            ("On stagnation, record the failed strategy.", "عند الركود، سجّل الاستراتيجية الفاشلة."),
            ("Present when confidence is at least 0.8.", "اعرض النتيجة عندما تكون الثقة 0.8 على الأقل."),
        ),
        starter='''from dataclasses import dataclass, field
from enum import Enum

class StrategyType(Enum):
    DIRECT = "direct"
    DECOMPOSE = "decompose"
    HYPOTHESIS_TEST = "hypothesis_test"

class AttentionSignal(Enum):
    CONTINUE = "continue"
    REPLAN = "replan"
    META_PLAN = "meta_plan"
    PRESENT = "present"

@dataclass
class CognitiveWorkspace:
    task: str
    strategy: StrategyType = StrategyType.DIRECT
    findings: list = field(default_factory=list)        # claims as plain strings
    confidence: float = 0.0
    history: list = field(default_factory=list)         # confidence after each cycle
    failed_strategies: list = field(default_factory=list)

def evaluate(workspace):
    claims = set(workspace.findings)
    # Step 1: a contradiction is a claim whose negation "not <claim>" is also present
    contradictions = ___
    return {"contradictions": contradictions}

def route_attention(workspace, evaluation):
    if evaluation["contradictions"]:
        # Step 2: go back to planning and test the competing hypotheses
        workspace.strategy = ___
        return AttentionSignal.REPLAN
    if len(workspace.history) >= 2 and workspace.history[-1] == workspace.history[-2]:
        # Step 3: stagnation - remember what did not work before meta-planning
        ___
        return AttentionSignal.META_PLAN
    # Step 4: confident enough to answer
    if ___:
        return AttentionSignal.PRESENT
    return AttentionSignal.CONTINUE

ws = CognitiveWorkspace("Why is the API slow?", findings=["cache is enabled", "not cache is enabled"])
print(route_attention(ws, evaluate(ws)), ws.strategy)
''',
        answers=(
            'sorted(claim for claim in claims if f"not {claim}" in claims)',
            "StrategyType.HYPOTHESIS_TEST",
            "workspace.failed_strategies.append(workspace.strategy)",
            "workspace.confidence >= 0.8",
        ),
        checks=(
            check("evaluate(CognitiveWorkspace('t', findings=['db is up', 'not db is up', 'cpu is high']))['contradictions']", ["db is up"],
                  "Blank 1: keep each claim for which `f\"not {claim}\"` is also in `claims`.", "الفراغ 1: احتفظ بكل ادعاء يكون `f\"not {claim}\"` موجودًا أيضًا في `claims`."),
            check("(lambda w: [route_attention(w, evaluate(w)).value, w.strategy.value])(CognitiveWorkspace('t', findings=['a', 'not a']))", ["replan", "hypothesis_test"],
                  "Blank 2: set `workspace.strategy = StrategyType.HYPOTHESIS_TEST`.", "الفراغ 2: اضبط `workspace.strategy = StrategyType.HYPOTHESIS_TEST`."),
            check("(lambda w: [route_attention(w, evaluate(w)).value, [s.value for s in w.failed_strategies]])(CognitiveWorkspace('t', strategy=StrategyType.DECOMPOSE, confidence=0.5, history=[0.5, 0.5]))", ["meta_plan", ["decompose"]],
                  "Blank 3: append the current strategy to `workspace.failed_strategies`.", "الفراغ 3: أضف الاستراتيجية الحالية إلى `workspace.failed_strategies`."),
            check("[route_attention(CognitiveWorkspace('t', confidence=c, history=[0.1, c]), {'contradictions': []}).value for c in (0.85, 0.6)]", ["present", "continue"],
                  "Blank 4: present when `workspace.confidence >= 0.8`.", "الفراغ 4: اعرض النتيجة عندما يكون `workspace.confidence >= 0.8`."),
        ),
        hints=(
            ("Build the negated text with an f-string and test membership in the set.", "ابنِ النص المنفي بـ f-string واختبر وجوده في المجموعة."),
            ("Enum members are reached as `StrategyType.NAME`.", "يُوصل إلى عناصر Enum بالشكل `StrategyType.NAME`."),
            ("Order matters: contradictions first, stagnation second, confidence last.", "الترتيب مهم: التناقضات أولًا، ثم الركود، ثم الثقة أخيرًا."),
        ),
        success=("Correct! Unlike a fixed perceive-plan-execute-evaluate loop, the router changes course: contradictions trigger hypothesis testing and stagnation triggers meta-planning with the failed strategy recorded.",
                 "صحيح! على عكس حلقة ثابتة من الإدراك ثم التخطيط ثم التنفيذ ثم التقييم، يغيّر الموجّه مساره: تُطلق التناقضات اختبار الفرضيات، ويُطلق الركود التخطيط الفوقي مع تسجيل الاستراتيجية الفاشلة."),
        expected=STUB_NOTE,
    ),
    "COURSE-012.M01.L10.EX02": Guided(
        goal=("Gate a cognitive agent's output on confidence and knowledge boundaries, then measure calibration and boundary accuracy against a baseline.",
              "اجعل مخرجات الوكيل المعرفي مشروطة بالثقة وحدود المعرفة، ثم قِس المعايرة ودقة الحدود مقارنةً بخط أساس."),
        steps=(
            ("Present only above 0.75 confidence; otherwise gather more.", "اعرض النتيجة فقط فوق ثقة 0.75؛ وإلا فاجمع المزيد."),
            ("Decide whether a question is inside the knowledge boundary.", "قرر هل السؤال داخل حدود المعرفة."),
            ("Compute the calibration error.", "احسب خطأ المعايرة."),
            ("Compute the knowledge-boundary accuracy.", "احسب دقة حدود المعرفة."),
        ),
        starter='''def gate(confidence, inside_boundary):
    if not inside_boundary:
        return "SIGNAL_UNCERTAINTY"
    # Step 1
    return ___

# Step 2: inside the boundary only if retrieval, memory and confidence all clear their bars
def inside_boundary(retrieval_relevance, memory_coverage, confidence):
    return ___

# Results on the same 6 test questions (correct is 1 or 0)
baseline = [
    {"kind": "easy", "correct": 1, "confidence": 0.9, "steps": 2, "flagged_uncertain": False},
    {"kind": "multistep", "correct": 0, "confidence": 0.8, "steps": 5, "flagged_uncertain": False},
    {"kind": "contradictory", "correct": 0, "confidence": 0.7, "steps": 4, "flagged_uncertain": False},
    {"kind": "compositional", "correct": 1, "confidence": 0.6, "steps": 6, "flagged_uncertain": False},
    {"kind": "unsupported", "correct": 0, "confidence": 0.8, "steps": 3, "flagged_uncertain": False},
    {"kind": "unsupported", "correct": 0, "confidence": 0.7, "steps": 3, "flagged_uncertain": True},
]
cognitive = [
    {"kind": "easy", "correct": 1, "confidence": 0.9, "steps": 3, "flagged_uncertain": False},
    {"kind": "multistep", "correct": 1, "confidence": 0.8, "steps": 7, "flagged_uncertain": False},
    {"kind": "contradictory", "correct": 1, "confidence": 0.6, "steps": 8, "flagged_uncertain": False},
    {"kind": "compositional", "correct": 1, "confidence": 0.7, "steps": 8, "flagged_uncertain": False},
    {"kind": "unsupported", "correct": 0, "confidence": 0.2, "steps": 4, "flagged_uncertain": True},
    {"kind": "unsupported", "correct": 0, "confidence": 0.1, "steps": 4, "flagged_uncertain": True},
]

# Step 3: mean absolute gap between confidence and correctness (lower is better calibrated)
def calibration_error(rows):
    return ___

# Step 4: share of unsupported questions the agent flagged as uncertain
def boundary_accuracy(rows):
    unsupported = [row for row in rows if row["kind"] == "unsupported"]
    return ___

for name, rows in (("baseline", baseline), ("cognitive", cognitive)):
    print(name, round(calibration_error(rows), 3), boundary_accuracy(rows), sum(r["steps"] for r in rows), "steps")
''',
        answers=(
            '"PRESENT" if confidence >= 0.75 else "GATHER_MORE"',
            "retrieval_relevance >= 0.5 and memory_coverage >= 0.3 and confidence >= 0.4",
            'sum(abs(row["confidence"] - row["correct"]) for row in rows) / len(rows)',
            'sum(row["flagged_uncertain"] for row in unsupported) / len(unsupported)',
        ),
        checks=(
            check("[gate(0.8, True), gate(0.5, True), gate(0.95, False)]", ["PRESENT", "GATHER_MORE", "SIGNAL_UNCERTAINTY"],
                  "Blank 1: present at confidence 0.75 or more, otherwise gather more.", "الفراغ 1: اعرض عند ثقة 0.75 أو أكثر، وإلا فاجمع المزيد."),
            check("[inside_boundary(0.7, 0.4, 0.6), inside_boundary(0.2, 0.9, 0.9), inside_boundary(0.9, 0.9, 0.3)]", [True, False, False],
                  "Blank 2: all three conditions must hold (relevance ≥ 0.5, coverage ≥ 0.3, confidence ≥ 0.4).",
                  "الفراغ 2: يجب أن تتحقق الشروط الثلاثة (الصلة ≥ 0.5، والتغطية ≥ 0.3، والثقة ≥ 0.4)."),
            check("[round(calibration_error(baseline), 3), round(calibration_error(cognitive), 3)]", [0.583, 0.217],
                  "Blank 3: average `abs(confidence - correct)` over the rows.", "الفراغ 3: احسب متوسط `abs(confidence - correct)` على الصفوف."),
            check("[boundary_accuracy(baseline), boundary_accuracy(cognitive)]", [0.5, 1.0],
                  "Blank 4: count flagged unsupported rows and divide by the number of unsupported rows.",
                  "الفراغ 4: عُدّ الصفوف غير المدعومة الموسومة واقسم على عدد الصفوف غير المدعومة."),
        ),
        hints=(
            ("A conditional expression returns one of two labels.", "يعيد التعبير الشرطي أحد وسمين."),
            ("Join the three comparisons with `and`.", "اربط المقارنات الثلاث بـ `and`."),
            ("Booleans sum as 1 and 0.", "تُجمع القيم المنطقية بوصفها 1 و0."),
        ),
        success=("Correct! The cognitive agent is better calibrated and flags every unsupported question - at the price of more steps. Whether that cost is worth it is a measurement, not a feeling.",
                 "صحيح! الوكيل المعرفي أفضل معايرة ويشير إلى كل سؤال غير مدعوم - على حساب خطوات أكثر. وهل تستحق هذه التكلفة؟ هذا قياس لا شعور."),
        reflect=("On your own 10-question test set, which metric would convince you the added complexity is worth it?",
                 "في مجموعة اختبار من 10 أسئلة تعدّها بنفسك، ما المقياس الذي سيقنعك بأن التعقيد الإضافي يستحق؟"),
    ),
}
