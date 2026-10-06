"""M01.L07 — Building Robust Agents with Evaluation and Feedback.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
AI Agents in Action, Chapter 7, page range not supplied in the provided source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L07"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of AI Agents"

MODULE_DESCRIPTION = (
    "Learn how to make agent quality measurable and improvable using benchmarks, "
    "test-driven agent development, grounding and critic agents, rubrics, "
    "guardrails, bounded retries, human feedback, governance, tracing, Phoenix, "
    "experiments, and annotations."
)

SOURCE_CHAPTER = 7

SOURCE_PAGES = "Page range not supplied in the provided chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Building Robust Agents with Evaluation and Feedback",

    "slug": "ai-agents-m01-l07",

    "description": (
        "Build a disciplined evaluation layer around agent systems. Learn how to "
        "define benchmarks, test stochastic behavior, evaluate natural-language "
        "outputs, enforce grounding, use rubrics and critics, monitor multi-agent "
        "governance, and turn traces and human feedback into regression datasets."
    ),

    "order": 7,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.25,

    "skill_tags": [
        "agent-evaluation",
        "feedback",
        "tdad",
        "benchmarks",
        "grounding",
        "critic-agents",
        "evaluation-agents",
        "guardrails",
        "rubrics",
        "human-feedback",
        "red-teaming",
        "phoenix",
        "observability",
        "annotations",
        "governance",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
        "M01.L06",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Building Robust Agents with Evaluation and Feedback",

        "content": (
            "# Building Robust Agents with Evaluation and Feedback\n"
            "\n"
            "> **Course:** AI Agents  \n"
            "> **Lesson:** M01.L07  \n"
            "> **Module:** Foundations of AI Agents  \n"
            "> **Source alignment:** *AI Agents in Action*, Chapter 7. "
            "The supplied chapter did not include a page range. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain what evaluation and feedback contribute to agent robustness.\n"
            "- Distinguish deterministic tests, LLM evaluators, and human evaluation.\n"
            "- Explain red-team, benchmark, grounding, critic, and human-feedback roles.\n"
            "- Describe how evaluation fits into the agent's sense-plan-act-learn cycle.\n"
            "- Apply test-driven agent development (TDAD).\n"
            "- Design benchmarks with expected and known-bad outputs.\n"
            "- Explain why stochastic agents should be tested multiple times.\n"
            "- Refactor prompts and tools using the smallest effective change.\n"
            "- Detect when the evaluator—not the agent—is producing the wrong score.\n"
            "- Build a typed evaluation-agent contract.\n"
            "- Distinguish grounding agents, critic agents, and general evaluation agents.\n"
            "- Enforce grounding through output guardrails.\n"
            "- Design safe bounded retry and escalation behavior.\n"
            "- Build and validate rubrics for open-ended output.\n"
            "- Explain evaluator collusion and multi-agent governance risks.\n"
            "- Use traces, sessions, metadata, datasets, experiments, and annotations with Phoenix.\n"
            "- Turn production feedback into reusable regression tests.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Evaluation makes robustness measurable\n"
            "\n"
            "Evaluation does not automatically make an agent robust. A badly designed agent can still "
            "fail even when surrounded by dashboards and evaluators.\n"
            "\n"
            "What evaluation provides is something equally important: **visibility**.\n"
            "\n"
            "It lets us answer questions such as:\n"
            "\n"
            "- Does the agent solve the goal reliably?\n"
            "- Does it use the correct tool?\n"
            "- Is its answer grounded in evidence?\n"
            "- How often does it fail?\n"
            "- How variable are repeated runs?\n"
            "- How much does each successful run cost?\n"
            "- What should we change next?\n"
            "\n"
            "Feedback closes the loop by turning those observations into changes to prompts, tools, "
            "models, policies, or architecture.\n"
            "\n"
            "A useful engineering view is:\n"
            "\n"
            "```text\n"
            "Agent behavior\n"
            "    |\n"
            "    v\n"
            "Observe / evaluate\n"
            "    |\n"
            "    v\n"
            "Store feedback\n"
            "    |\n"
            "    v\n"
            "Improve system\n"
            "    |\n"
            "    +------> evaluate again\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Internal versus external evaluation\n"
            "\n"
            "Agents already contain an internal feedback concept in the **Learn** stage of the "
            "sense-plan-act-learn cycle. After an action, the agent observes what happened and decides "
            "what to do next.\n"
            "\n"
            "External evaluation adds independent mechanisms around the agent.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- deterministic tests,\n"
            "- benchmark suites,\n"
            "- red-team tests,\n"
            "- grounding checks,\n"
            "- critic agents,\n"
            "- human review,\n"
            "- feedback databases,\n"
            "- monitoring and alerting.\n"
            "\n"
            "External feedback can follow two broad paths.\n"
            "\n"
            "### In-loop feedback\n"
            "\n"
            "The result immediately affects the agent's next action.\n"
            "\n"
            "```text\n"
            "Agent -> Critic -> Feedback -> Agent retry\n"
            "```\n"
            "\n"
            "### Offline feedback\n"
            "\n"
            "The evaluation is stored for later analysis rather than changing the current response.\n"
            "\n"
            "```text\n"
            "Agent -> Evaluation store -> Dashboard / regression analysis / improvement work\n"
            "```\n"
            "\n"
            "Both are useful. In-loop evaluation controls current behavior; offline evaluation improves "
            "future versions of the system.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Three kinds of evaluation\n"
            "\n"
            "The chapter groups evaluation into three broad forms.\n"
            "\n"
            "### Deterministic evaluation\n"
            "\n"
            "Use ordinary code when correctness is exact.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- output matches a schema,\n"
            "- required field exists,\n"
            "- tool X was called,\n"
            "- a numerical value is in range,\n"
            "- a known label was returned.\n"
            "\n"
            "### LLM or agent evaluation\n"
            "\n"
            "Use a model when quality is fuzzy or semantic.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- Is the answer relevant?\n"
            "- Does this summary preserve the important facts?\n"
            "- Does the response satisfy a tone rubric?\n"
            "- Is the generated plan sufficiently complete?\n"
            "\n"
            "### Human evaluation\n"
            "\n"
            "Humans remain important for:\n"
            "\n"
            "- edge cases,\n"
            "- policy concerns,\n"
            "- tone and social appropriateness,\n"
            "- disputed evaluator outcomes,\n"
            "- real-world judgment.\n"
            "\n"
            "The most reliable systems combine these forms rather than forcing every quality question "
            "through a single evaluator type.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Red teams, benchmarks, humans, grounding, and critics\n"
            "\n"
            "The chapter identifies several concrete evaluation methods.\n"
            "\n"
            "### Red-team testing\n"
            "\n"
            "Attempts to find inputs or patterns that break the system.\n"
            "\n"
            "Use it to probe:\n"
            "\n"
            "- safety boundaries,\n"
            "- prompt injection,\n"
            "- unexpected tool usage,\n"
            "- policy failures,\n"
            "- adversarial inputs.\n"
            "\n"
            "### Benchmark testing\n"
            "\n"
            "Measures how well an agent reaches a known goal across a defined test set.\n"
            "\n"
            "### Human feedback\n"
            "\n"
            "Ratings, comments, expert reviews, and manual labels expose failures automated evaluators may miss.\n"
            "\n"
            "The chapter also warns that raw human feedback is noisy. Useful production practices include:\n"
            "\n"
            "- aggregation,\n"
            "- outlier detection,\n"
            "- expert-weighted or stratified review,\n"
            "- manual follow-up on flagged outputs.\n"
            "\n"
            "### Grounding evaluation\n"
            "\n"
            "Checks whether claims are supported by an authoritative source or retrieved context.\n"
            "\n"
            "### Critic/evaluation agents\n"
            "\n"
            "Review generated outputs, plans, or actions and provide structured feedback.\n"
            "\n"
            "The correct method depends on the type of failure you are trying to detect.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Evaluation agents also need governance\n"
            "\n"
            "A multi-agent system can create a dangerous illusion of independent verification.\n"
            "\n"
            "Suppose:\n"
            "\n"
            "- Agent A gives a wrong answer.\n"
            "- Evaluator B uses the same model family, assumptions, and context.\n"
            "- Evaluator B approves the wrong answer.\n"
            "\n"
            "Now the system looks validated even though both agents share the same blind spot.\n"
            "\n"
            "The chapter describes this as a **collusion risk**: multiple agents reinforce the same "
            "incorrect conclusion instead of providing independent checks.\n"
            "\n"
            "Useful governance practices include:\n"
            "\n"
            "- using different models/providers for evaluators when practical,\n"
            "- using adversarial evaluator prompts rather than confirmation-oriented prompts,\n"
            "- randomly sampling supposedly good outputs for human review,\n"
            "- defining which evaluator has final authority,\n"
            "- logging every agent-to-agent evaluation message,\n"
            "- escalating unresolved disagreement,\n"
            "- limiting each agent's authority to its role.\n"
            "\n"
            "An evaluation layer that produces false confidence can be worse than having no evaluator at all.\n"
            "\n"
            "[[IMAGE_NEEDED: Independent evaluation versus colluding evaluation | "
            "Left: generator and evaluator share the same blind spot and both approve a wrong answer. "
            "Right: generator is checked by a differently configured evaluator plus periodic human review | "
            "Learner should notice that multiple agents do not automatically equal independent evidence]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Test-Driven Agent Development (TDAD)\n"
            "\n"
            "Test-driven agent development adapts the discipline of test-driven development to stochastic agents.\n"
            "\n"
            "The core idea is:\n"
            "\n"
            "> Define what good behavior looks like **before** you start endlessly tuning the agent.\n"
            "\n"
            "A TDAD cycle looks like:\n"
            "\n"
            "```text\n"
            "Define goals and benchmarks\n"
            "        |\n"
            "        v\n"
            "Run tests and expect failures\n"
            "        |\n"
            "        v\n"
            "Make the minimum useful change\n"
            "        |\n"
            "        v\n"
            "Rerun all benchmarks\n"
            "        |\n"
            "        v\n"
            "Refactor and repeat\n"
            "```\n"
            "\n"
            "Unlike deterministic software tests, agent tests often need repeated runs because LLM outputs vary.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Design benchmarks around behavior, not only final text\n"
            "\n"
            "A simple benchmark contains:\n"
            "\n"
            "- an input question,\n"
            "- an expected answer,\n"
            "- optionally, known-bad answers.\n"
            "\n"
            "But a complete agent benchmark can evaluate much more:\n"
            "\n"
            "- final correctness,\n"
            "- tool choice,\n"
            "- tool arguments,\n"
            "- grounding,\n"
            "- number of steps,\n"
            "- latency,\n"
            "- token usage,\n"
            "- cost,\n"
            "- error recovery.\n"
            "\n"
            "An agent that reaches the right answer through five unnecessary wrong tool calls is not equivalent "
            "to an agent that reaches it through two appropriate calls.\n"
            "\n"
            "This is an important shift from traditional text-only evaluation:\n"
            "\n"
            "> Evaluate the **trajectory**, not only the final sentence.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. A minimal benchmarked RAG agent\n"
            "\n"
            "The chapter introduces TDAD with a small fictional knowledge database.\n"
            "\n"
            "A simplified structure is:\n"
            "\n"
            "```python\n"
            "_knowledge = [\n"
            "    \"Nebula Forge engine spins antimatter rings for gravity control.\",\n"
            "    \"Solaris Glacier releases luminescent icefire at dusk.\",\n"
            "]\n"
            "\n"
            "_benchmarks = [\n"
            "    {\"q\": \"Nebula Forge engine spins what?\", \"a\": \"antimatter\"},\n"
            "    {\"q\": \"Solaris Glacier releases luminescent what?\", \"a\": \"icefire\"},\n"
            "]\n"
            "\n"
            "@function_tool\n"
            "def search_knowledge(query: str) -> dict:\n"
            "    matches = [\n"
            "        doc for doc in _knowledge\n"
            "        if query.lower() in doc.lower()\n"
            "    ]\n"
            "    return {\"status\": \"ok\", \"context\": \"\\n\".join(matches)}\n"
            "```\n"
            "\n"
            "The first version is intentionally under-specified. Failure is useful because it gives us evidence about "
            "what the system actually needs.\n"
            "\n"
            "One passing run is not enough. The chapter recommends repeating benchmark runs to inspect consistency.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Refactor using the smallest effective change\n"
            "\n"
            "A common anti-pattern is prompt inflation: every failure causes another paragraph to be appended to "
            "the system prompt.\n"
            "\n"
            "The chapter recommends escalating changes gradually.\n"
            "\n"
            "A practical order is:\n"
            "\n"
            "1. Change one word for clarity or tone.\n"
            "2. Add a short clause.\n"
            "3. Add one sentence.\n"
            "4. Add a small prompt section.\n"
            "5. Add or modify a tool.\n"
            "6. Change model or generation settings.\n"
            "\n"
            "The purpose is not minimalism for its own sake. Lean changes make causality easier to understand and reduce "
            "the chance of introducing new contradictory instructions.\n"
            "\n"
            "Also remove prompt content that no longer earns its place.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Put tool guidance where it belongs\n"
            "\n"
            "Modern agent SDKs already expose tool names, descriptions, and parameter schemas to the model.\n"
            "\n"
            "Therefore, do not duplicate every tool detail inside the agent prompt unless the workflow requires special guidance.\n"
            "\n"
            "For example, instead of:\n"
            "\n"
            "```text\n"
            "Call function search_knowledge with one string argument...\n"
            "```\n"
            "\n"
            "prefer a well-designed tool:\n"
            "\n"
            "```python\n"
            "@function_tool\n"
            "def search_knowledge_by_keyword(query: str) -> dict:\n"
            "    \"\"\"Search the knowledge store using one concise keyword query.\"\"\"\n"
            "    ...\n"
            "```\n"
            "\n"
            "Then use prompt instructions only for behavior the tool metadata cannot express, such as:\n"
            "\n"
            "```text\n"
            "If retrieval is thin, rephrase the query and try again before concluding the answer is absent.\n"
            "```\n"
            "\n"
            "This separation makes tool behavior easier to maintain and reduces prompt clutter.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Sometimes the evaluator is wrong\n"
            "\n"
            "Suppose the expected answer is:\n"
            "\n"
            "```text\n"
            "photons\n"
            "```\n"
            "\n"
            "and the agent returns:\n"
            "\n"
            "```text\n"
            "Photons.\n"
            "```\n"
            "\n"
            "Strict equality marks the answer wrong even though the meaning is correct.\n"
            "\n"
            "Another example:\n"
            "\n"
            "```text\n"
            "Expected: currents\n"
            "Actual:   Water currents\n"
            "```\n"
            "\n"
            "Again, a brittle evaluator may report a false failure.\n"
            "\n"
            "At minimum, deterministic natural-language comparisons may need normalization:\n"
            "\n"
            "- lowercase,\n"
            "- trim whitespace,\n"
            "- remove harmless punctuation,\n"
            "- account for acceptable variants.\n"
            "\n"
            "For more open-ended answers, an LLM evaluator or rubric may be more appropriate.\n"
            "\n"
            "The broader lesson is crucial:\n"
            "\n"
            "> When a benchmark fails, diagnose whether the problem is in the agent, the retrieval system, the benchmark, or the evaluator.\n"
            "\n"
            "{{exercise:M01.L07.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Typed evaluation agents\n"
            "\n"
            "Free-form answers often cannot be evaluated by exact string matching.\n"
            "\n"
            "A separate evaluation agent can return a typed result:\n"
            "\n"
            "```python\n"
            "from pydantic import BaseModel\n"
            "\n"
            "class EvaluationOutput(BaseModel):\n"
            "    is_correct: bool\n"
            "    feedback: str\n"
            "\n"
            "evaluation_agent = Agent(\n"
            "    name=\"Evaluation Agent\",\n"
            "    instructions=(\n"
            "        \"Evaluate whether the answer satisfies the expected key requirement. \"\n"
            "        \"Return correctness plus concise feedback.\"\n"
            "    ),\n"
            "    output_type=EvaluationOutput,\n"
            ")\n"
            "```\n"
            "\n"
            "Typed evaluator output gives application code a stable contract:\n"
            "\n"
            "```text\n"
            "is_correct -> programmatic gate\n"
            "feedback   -> diagnosis / retry / reporting\n"
            "```\n"
            "\n"
            "The evaluator should itself be tested for false positives and false negatives.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Grounding, critic, and general evaluation agents\n"
            "\n"
            "These three evaluator roles overlap, but they answer different questions.\n"
            "\n"
            "### Grounding agent\n"
            "\n"
            "Question:\n"
            "\n"
            "```text\n"
            "Is this answer supported by the authoritative context?\n"
            "```\n"
            "\n"
            "Best fit:\n"
            "\n"
            "- RAG,\n"
            "- citation verification,\n"
            "- memory verification,\n"
            "- tool-result validation.\n"
            "\n"
            "### Critic agent\n"
            "\n"
            "Question:\n"
            "\n"
            "```text\n"
            "How well does this generated output satisfy the quality criteria?\n"
            "```\n"
            "\n"
            "Best fit:\n"
            "\n"
            "- plans,\n"
            "- reports,\n"
            "- images,\n"
            "- generated content,\n"
            "- iterative refinement.\n"
            "\n"
            "### General evaluation agent\n"
            "\n"
            "Question:\n"
            "\n"
            "```text\n"
            "Did this output satisfy the benchmark or task requirement?\n"
            "```\n"
            "\n"
            "Best fit:\n"
            "\n"
            "- test suites,\n"
            "- benchmark scoring,\n"
            "- complex pass/fail decisions.\n"
            "\n"
            "Choosing the narrowest evaluator that matches the requirement usually makes the result easier to understand.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Grounding agents verify evidence\n"
            "\n"
            "A grounding evaluator needs access to the same authoritative context used to generate the answer.\n"
            "\n"
            "The pattern is:\n"
            "\n"
            "```text\n"
            "Retrieved context -----------+\n"
            "                              |\n"
            "                              v\n"
            "Retrieved context -> RAG Agent -> Answer\n"
            "                              |\n"
            "                              v\n"
            "                       Grounding Agent\n"
            "                              |\n"
            "                         pass / fail\n"
            "```\n"
            "\n"
            "A typed grounding result might be:\n"
            "\n"
            "```python\n"
            "class GroundedAnswer(BaseModel):\n"
            "    is_answer_grounded: bool\n"
            "    feedback: str\n"
            "```\n"
            "\n"
            "The evaluator should answer a narrow question: are the response claims supported by the source context?\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Turn grounding into an output guardrail\n"
            "\n"
            "Evaluation becomes operationally useful when it can enforce behavior.\n"
            "\n"
            "A grounding check can run inside an output guardrail:\n"
            "\n"
            "```python\n"
            "@output_guardrail\n"
            "async def ground_answer(context, agent, output):\n"
            "    grounding = await Runner.run(\n"
            "        grounding_agent,\n"
            "        input=str({\n"
            "            \"question\": output.question,\n"
            "            \"answer\": output.answer,\n"
            "        }),\n"
            "    )\n"
            "\n"
            "    checked = grounding.final_output\n"
            "\n"
            "    return GuardrailFunctionOutput(\n"
            "        output_info={\n"
            "            \"answer_is_grounded\": checked.is_answer_grounded,\n"
            "            \"feedback\": checked.feedback,\n"
            "        },\n"
            "        tripwire_triggered=not checked.is_answer_grounded,\n"
            "    )\n"
            "```\n"
            "\n"
            "Then the calling code can choose a policy when the tripwire fires.\n"
            "\n"
            "Possible policies include:\n"
            "\n"
            "- block with a static safe response,\n"
            "- regenerate using evaluator feedback,\n"
            "- escalate to a human,\n"
            "- return a failure signal to an upstream system.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Retry ceilings and failure policy\n"
            "\n"
            "A critic loop must not retry forever.\n"
            "\n"
            "Suppose the evaluator rejects an answer three times. What happens next is an architectural decision.\n"
            "\n"
            "Useful options include:\n"
            "\n"
            "- safe static fallback,\n"
            "- explicit failure returned to an internal pipeline,\n"
            "- human escalation for high-stakes workflows,\n"
            "- best failed candidate with a confidence warning when appropriate.\n"
            "\n"
            "A bounded loop might look like:\n"
            "\n"
            "```python\n"
            "MAX_ATTEMPTS = 3\n"
            "\n"
            "for attempt in range(MAX_ATTEMPTS):\n"
            "    candidate = await generate()\n"
            "    evaluation = await evaluate(candidate)\n"
            "\n"
            "    if evaluation.passed:\n"
            "        return candidate\n"
            "\n"
            "    feedback = evaluation.feedback\n"
            "\n"
            "return safe_failure_response()\n"
            "```\n"
            "\n"
            "The retry ceiling prevents hidden token and latency runaways.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Use the right evaluation method for the output type\n"
            "\n"
            "Structured outputs often have objective metrics.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- classification accuracy,\n"
            "- precision,\n"
            "- recall,\n"
            "- F1,\n"
            "- exact schema validity,\n"
            "- numeric error.\n"
            "\n"
            "Open-ended outputs are different.\n"
            "\n"
            "A summary can be correct in many different phrasings. A plan can be good along some dimensions and weak along others.\n"
            "\n"
            "These cases benefit from:\n"
            "\n"
            "- rubrics,\n"
            "- LLM-as-judge,\n"
            "- human review.\n"
            "\n"
            "Do not use a complex rubric where an exact deterministic metric is enough. Do not use strict equality where quality is inherently multidimensional.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Building useful rubrics\n"
            "\n"
            "A rubric turns vague quality into explicit criteria and performance levels.\n"
            "\n"
            "A strong rubric-development process is:\n"
            "\n"
            "1. Define the purpose of the output.\n"
            "2. Define measurable criteria.\n"
            "3. Choose a rating scale.\n"
            "4. Describe what each score means.\n"
            "5. Apply the rubric to sample outputs.\n"
            "6. Combine or weight scores if appropriate.\n"
            "7. Check evaluator consistency.\n"
            "8. Revise the rubric over time.\n"
            "\n"
            "Possible agent-quality criteria include:\n"
            "\n"
            "- factual accuracy,\n"
            "- grounding,\n"
            "- completeness,\n"
            "- structural correctness,\n"
            "- tone,\n"
            "- tool usage correctness,\n"
            "- error recovery,\n"
            "- hallucination rate.\n"
            "\n"
            "The rubric itself must be validated against human judgment. A consistently wrong rubric is still wrong.\n"
            "\n"
            "[[IMAGE_NEEDED: Rubric evaluation matrix | "
            "A table-like visual with rows Accuracy, Grounding, Tool Use, Completeness, Error Handling and columns "
            "scores 1 through 5, with short descriptions for weak versus strong performance | "
            "Learner should notice that rubrics make multiple quality dimensions explicit]]\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Critic agents and rubric-guided refinement\n"
            "\n"
            "A critic agent scores generated output against the rubric and provides feedback.\n"
            "\n"
            "A typed critic response might be:\n"
            "\n"
            "```python\n"
            "class CritiqueResult(BaseModel):\n"
            "    output_pass: bool\n"
            "    score: int\n"
            "    feedback: str\n"
            "```\n"
            "\n"
            "Then generation and critique can form a bounded loop:\n"
            "\n"
            "```text\n"
            "Generate\n"
            "   |\n"
            "   v\n"
            "Critic scores output\n"
            "   |\n"
            "   +--> pass -> deliver\n"
            "   |\n"
            "   +--> fail -> feedback -> regenerate\n"
            "```\n"
            "\n"
            "The chapter demonstrates this with image-generation style guidelines, but the architecture applies equally to reports, plans, graphs, and other high-variance outputs.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Evaluation thresholds need calibration\n"
            "\n"
            "Suppose a rubric score ranges from 1 to 5.\n"
            "\n"
            "A low threshold may pass weak content. A high threshold may reject many acceptable outputs and exhaust retry budgets.\n"
            "\n"
            "Therefore, the pass threshold should be treated as a measurable decision.\n"
            "\n"
            "A practical process is:\n"
            "\n"
            "1. Collect a representative sample of outputs.\n"
            "2. Have humans label which should pass and fail.\n"
            "3. Score the same outputs with the rubric/evaluator.\n"
            "4. Compare agreement.\n"
            "5. Choose a threshold balancing false passes and false rejections.\n"
            "6. Revalidate when the rubric, model, or agent changes.\n"
            "\n"
            "This is evaluator calibration.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Why observability matters\n"
            "\n"
            "Once an agent uses multiple model calls, tools, handoffs, retries, and evaluators, the final output no longer tells you enough about what happened.\n"
            "\n"
            "Trace-level observability helps inspect:\n"
            "\n"
            "- model calls,\n"
            "- tool usage,\n"
            "- agent transitions,\n"
            "- token usage,\n"
            "- latency,\n"
            "- cost,\n"
            "- sessions,\n"
            "- evaluator decisions,\n"
            "- failure paths.\n"
            "\n"
            "The chapter uses **Arize Phoenix** as an open-source observability and evaluation platform.\n"
            "\n"
            "It also notes that alternatives exist; the important concept is the observability pattern, not dependence on one vendor.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Connecting agent traces to Phoenix\n"
            "\n"
            "The source demonstrates running Phoenix locally and sending traces to it.\n"
            "\n"
            "A simplified version is:\n"
            "\n"
            "```python\n"
            "import os\n"
            "\n"
            "os.environ[\"PHOENIX_COLLECTOR_ENDPOINT\"] = \"http://localhost:6006\"\n"
            "\n"
            "set_trace_processors([])\n"
            "\n"
            "tracer_provider = register(\n"
            "    project_name=\"agents\",\n"
            "    auto_instrument=True,\n"
            ")\n"
            "\n"
            "with trace(\"RAG Evaluation Workflow\"):\n"
            "    result = await Runner.run(agent, input_text)\n"
            "```\n"
            "\n"
            "The named trace creates an understandable unit of work inside the observability system.\n"
            "\n"
            "Phoenix can then expose operational information about the agent and the underlying LLM calls.\n\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Sessions and metadata make traces analyzable\n"
            "\n"
            "One trace is useful. Hundreds of traces become much more valuable when they can be grouped and filtered.\n"
            "\n"
            "The chapter attaches metadata such as:\n"
            "\n"
            "```python\n"
            "metadata = {\n"
            "    \"run_id\": \"abc123\",\n"
            "    \"env\": \"dev\",\n"
            "    \"customer_tier\": \"pro\",\n"
            "    \"model\": model,\n"
            "}\n"
            "\n"
            "with (\n"
            "    using_session(\"sess-42\"),\n"
            "    using_metadata(metadata),\n"
            "):\n"
            "    with trace(\"Agent Workflow\"):\n"
            "        result = await Runner.run(agent, input_text)\n"
            "```\n"
            "\n"
            "This enables questions such as:\n"
            "\n"
            "- Do failures happen more often in production than development?\n"
            "- Does one model version have higher latency?\n"
            "- Are premium-user sessions using more tools?\n"
            "- Did a prompt change improve one cohort but hurt another?\n"
            "\n"
            "Metadata turns raw traces into analyzable datasets.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Turn traces into datasets and experiments\n"
            "\n"
            "The outer loop of evaluation begins when real trace spans are collected into reusable datasets.\n"
            "\n"
            "A practical workflow is:\n"
            "\n"
            "```text\n"
            "Production/dev traces\n"
            "      |\n"
            "      v\n"
            "Select representative spans\n"
            "      |\n"
            "      v\n"
            "Create evaluation dataset\n"
            "      |\n"
            "      v\n"
            "Run experiment on new prompt/model/tool version\n"
            "      |\n"
            "      v\n"
            "Compare evaluator scores + operational metrics\n"
            "```\n"
            "\n"
            "This is much more powerful than judging a new prompt from a few hand-picked examples.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Annotations turn human judgment into structured data\n"
            "\n"
            "A developer may notice that the agent chose the wrong tool. A domain expert may notice a subtle policy error. A QA reviewer may mark an answer as excellent.\n"
            "\n"
            "If those observations remain in chat messages or meeting notes, they disappear from the evaluation system.\n"
            "\n"
            "Annotations make them reusable.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- `correctness=fail`,\n"
            "- `tool_selection=wrong`,\n"
            "- `needs_review=true`,\n"
            "- `grounding=good`,\n"
            "- `tone=poor`.\n"
            "\n"
            "Once stored with trace data, annotations can be filtered and analyzed against:\n"
            "\n"
            "- latency,\n"
            "- cost,\n"
            "- token usage,\n"
            "- tool choice,\n"
            "- model version,\n"
            "- prompt version.\n"
            "\n"
            "Over time, flagged examples become a natural regression suite.\n"
            "\n"
            "[[IMAGE_NEEDED: From trace annotation to regression dataset | "
            "Show Trace -> Reviewer annotation -> Stored labeled span -> Dataset -> New agent version -> Regression experiment | "
            "Learner should notice how one manual observation becomes reusable evaluation data]]\n"
            "\n"
            "{{exercise:M01.L07.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 26. A practical evaluation playbook\n"
            "\n"
            "Use this sequence when hardening an agent.\n"
            "\n"
            "### Step 1 — Define success before tuning\n"
            "\n"
            "Create benchmark cases, expected behavior, and important known-bad examples.\n"
            "\n"
            "### Step 2 — Test repeatedly\n"
            "\n"
            "Measure variability, not only one lucky run.\n"
            "\n"
            "### Step 3 — Diagnose the layer that failed\n"
            "\n"
            "Was the problem in retrieval, prompt, tool metadata, model, evaluator, or benchmark?\n"
            "\n"
            "### Step 4 — Make the smallest useful change\n"
            "\n"
            "Avoid uncontrolled prompt growth.\n"
            "\n"
            "### Step 5 — Rerun all prior benchmarks\n"
            "\n"
            "New fixes may create regressions elsewhere.\n"
            "\n"
            "### Step 6 — Use typed evaluator output\n"
            "\n"
            "Make pass/fail and feedback programmatically usable.\n"
            "\n"
            "### Step 7 — Ground authoritative answers\n"
            "\n"
            "Use source-aware validation when claims must be supported.\n"
            "\n"
            "### Step 8 — Add rubric critics for open-ended output\n"
            "\n"
            "Define criteria rather than asking a vague judge whether something is 'good.'\n"
            "\n"
            "### Step 9 — Bound retries and define escalation\n"
            "\n"
            "Evaluation loops need explicit stopping rules.\n"
            "\n"
            "### Step 10 — Trace everything important\n"
            "\n"
            "Include evaluator behavior, not only generator behavior.\n"
            "\n"
            "### Step 11 — Capture human feedback structurally\n"
            "\n"
            "Convert review into annotations and datasets.\n"
            "\n"
            "### Step 12 — Re-evaluate evaluators\n"
            "\n"
            "A monitoring layer can drift or share the same blind spots as the system it judges.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Evaluation makes a weak architecture robust\n"
            "\n"
            "> Evaluation reveals behavior and guides improvement; it cannot compensate for fundamentally bad system design.\n"
            "\n"
            "### Misconception 2: A passing benchmark run proves the agent is reliable\n"
            "\n"
            "> LLM behavior is variable, so repeated runs are needed to understand consistency.\n"
            "\n"
            "### Misconception 3: Every failed benchmark means the agent is wrong\n"
            "\n"
            "> The evaluator, expected answer, retrieval system, or benchmark may be the real problem.\n"
            "\n"
            "### Misconception 4: A second agent is automatically an independent judge\n"
            "\n"
            "> Shared models, training data, assumptions, and prompts can create shared blind spots.\n"
            "\n"
            "### Misconception 5: More prompt instructions are always the best fix\n"
            "\n"
            "> Tool metadata, typed outputs, model settings, retrieval, or architecture may be the better place to change behavior.\n"
            "\n"
            "### Misconception 6: Rubric score thresholds can be chosen arbitrarily\n"
            "\n"
            "> Thresholds should be calibrated against representative human-labeled outputs.\n"
            "\n"
            "### Misconception 7: Observability is only for debugging crashes\n"
            "\n"
            "> Traces are also datasets for evaluating quality, cost, latency, and model behavior.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Evaluation | Measuring whether agent behavior satisfies requirements |\n"
            "| Feedback | Information used to improve current or future behavior |\n"
            "| Benchmark | Defined test case or suite measuring agent performance |\n"
            "| Red-team test | Adversarial test designed to uncover failure modes |\n"
            "| TDAD | Test-driven agent development |\n"
            "| Grounding evaluator | Checker that verifies claims against authoritative context |\n"
            "| Critic agent | Evaluator that scores generated output against criteria/rubric |\n"
            "| Evaluation agent | General evaluator used to judge benchmark/task success |\n"
            "| Guardrail | Enforcing validation boundary capable of blocking or redirecting output |\n"
            "| Tripwire | Guardrail condition that signals failure |\n"
            "| Rubric | Explicit evaluation criteria plus performance scale |\n"
            "| Calibration | Aligning evaluator scores or thresholds with human judgment |\n"
            "| False positive | Evaluator incorrectly passes a bad result |\n"
            "| False negative | Evaluator incorrectly rejects an acceptable result |\n"
            "| Collusion risk | Multiple agents reinforcing the same wrong assumption or blind spot |\n"
            "| Trace | Recorded execution path across model/tool/agent calls |\n"
            "| Session | Grouping of related interactions in observability data |\n"
            "| Metadata | Structured labels attached to traces for filtering/analysis |\n"
            "| Annotation | Structured human or programmatic label attached to a trace/span |\n"
            "| Regression dataset | Set of previously problematic or representative cases rerun after changes |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What does evaluation provide that architecture alone does not?\n"
            "2. How is in-loop feedback different from offline evaluation?\n"
            "3. When should deterministic evaluation be preferred over an LLM judge?\n"
            "4. What does red-team testing measure?\n"
            "5. Why should agent benchmarks inspect intermediate behavior as well as final output?\n"
            "6. What is TDAD?\n"
            "7. Why should stochastic benchmarks be rerun multiple times?\n"
            "8. What is the recommended order for escalating prompt/tool/model changes?\n"
            "9. Why might strict string equality be a bad natural-language evaluator?\n"
            "10. How do grounding, critic, and evaluation agents differ?\n"
            "11. How does an output guardrail operationalize a grounding check?\n"
            "12. Why do critic loops need retry ceilings?\n"
            "13. When are rubrics more appropriate than accuracy?\n"
            "14. Why must rubrics and thresholds be validated against humans?\n"
            "15. What is evaluator collusion?\n"
            "16. Why should evaluator traces also be logged?\n"
            "17. What do sessions and metadata add to observability?\n"
            "18. How can annotations become regression tests?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Robust agent engineering is an empirical loop: define what good behavior means, test the "
            "agent repeatedly, observe the entire trajectory, change the smallest responsible part, and "
            "test again. Grounding agents, critics, rubrics, guardrails, traces, and human feedback are "
            "useful only when their own quality is measured and when their signals become actionable "
            "improvements rather than decorative dashboards.**\n"
        ),

        "estimated_minutes": 255,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "evaluation-purpose", "title": "Evaluation makes robustness measurable", "order": 1},
            {"id": "internal-external-feedback", "title": "Internal versus external evaluation", "order": 2},
            {"id": "evaluation-types", "title": "Three kinds of evaluation", "order": 3},
            {"id": "evaluation-methods", "title": "Red teams, benchmarks, humans, grounding, and critics", "order": 4},
            {"id": "governance", "title": "Evaluation agents also need governance", "order": 5},
            {"id": "tdad", "title": "Test-Driven Agent Development (TDAD)", "order": 6},
            {"id": "benchmark-design", "title": "Design benchmarks around behavior, not only final text", "order": 7},
            {"id": "baseline-rag", "title": "A minimal benchmarked RAG agent", "order": 8},
            {"id": "minimal-change", "title": "Refactor using the smallest effective change", "order": 9},
            {"id": "tool-prompt-separation", "title": "Put tool guidance where it belongs", "order": 10},
            {"id": "evaluator-bugs", "title": "Sometimes the evaluator is wrong", "order": 11},
            {"id": "evaluation-agent", "title": "Typed evaluation agents", "order": 12},
            {"id": "three-evaluator-agents", "title": "Grounding, critic, and general evaluation agents", "order": 13},
            {"id": "grounding-agent", "title": "Grounding agents verify evidence", "order": 14},
            {"id": "grounding-guardrail", "title": "Turn grounding into an output guardrail", "order": 15},
            {"id": "retry-policy", "title": "Retry ceilings and failure policy", "order": 16},
            {"id": "structured-vs-open-eval", "title": "Use the right evaluation method for the output type", "order": 17},
            {"id": "rubrics", "title": "Building useful rubrics", "order": 18},
            {"id": "critic-loop", "title": "Critic agents and rubric-guided refinement", "order": 19},
            {"id": "threshold-calibration", "title": "Evaluation thresholds need calibration", "order": 20},
            {"id": "phoenix-purpose", "title": "Why observability matters", "order": 21},
            {"id": "phoenix-connect", "title": "Connecting agent traces to Phoenix", "order": 22},
            {"id": "sessions-metadata", "title": "Sessions and metadata make traces analyzable", "order": 23},
            {"id": "datasets-experiments", "title": "Turn traces into datasets and experiments", "order": 24},
            {"id": "annotations", "title": "Annotations turn human judgment into structured data", "order": 25},
            {"id": "evaluation-playbook", "title": "A practical evaluation playbook", "order": 26},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L07.EX01",

            "title": "Use TDAD to Improve a RAG Agent—and Its Evaluator",

            "lesson_code": "M01.L07",

            "section_id": "evaluator-bugs",

            "placement": "after_section",

            "description": (
                "Practice benchmark-driven agent development while learning to distinguish "
                "agent failures from retrieval and evaluator failures."
            ),

            "instructions": (
                "Build the fictional RAG benchmark setup from this lesson.\n"
                "1. Create at least five benchmark questions with expected answers and one known-bad answer each.\n"
                "2. Run the baseline agent three times and record pass rate for every run.\n"
                "3. Inspect retrieval/tool traces for failed questions.\n"
                "4. Make the smallest change that addresses the most obvious failure.\n"
                "5. Improve the keyword tool name/docstring if tool usage is unclear.\n"
                "6. Rerun all benchmarks three times.\n"
                "7. Intentionally use strict string equality and identify at least one false failure caused by case, punctuation, or harmless wording.\n"
                "8. Fix the evaluator with normalization.\n"
                "9. Add a typed EvaluationOutput agent for answers that cannot be evaluated reliably with string rules.\n"
                "10. Compare the deterministic evaluator and LLM evaluator on the same benchmark set.\n"
                "11. Write which component caused each failure: generator, retrieval, tool selection, benchmark, or evaluator.\n"
                "12. Keep a short change log showing each modification and its measured effect."
            ),

            "expected_output": (
                "A small TDAD benchmark suite, three-run baseline and improved scores, "
                "an evaluator-bug example, a corrected deterministic evaluator, a typed "
                "LLM evaluator, and a failure-attribution table."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "tdad",
                "benchmarking",
                "evaluation",
                "tool-metadata",
                "regression-testing",
                "evaluator-validation",
                "failure-analysis",
            ],
        },

        {
            "id": "M01.L07.EX02",

            "title": "Build a Production Evaluation Loop with Grounding and Phoenix",

            "lesson_code": "M01.L07",

            "section_id": "annotations",

            "placement": "after_section",

            "description": (
                "Combine grounding, guardrails, bounded retries, tracing, metadata, "
                "annotations, and regression datasets into one evaluation architecture."
            ),

            "instructions": (
                "Scenario: You operate an internal RAG agent that answers policy questions.\n"
                "1. Create a typed answer object containing question, answer, and references.\n"
                "2. Add a grounding evaluator that receives the answer and the authoritative retrieved context.\n"
                "3. Wrap the grounding evaluator in an output guardrail.\n"
                "4. On grounding failure, allow at most two regeneration attempts using evaluator feedback.\n"
                "5. After retries are exhausted, return a static safe fallback.\n"
                "6. Define a rubric for relevance, completeness, grounding, and tool-use correctness.\n"
                "7. Add a critic agent that returns typed score, pass/fail, and feedback.\n"
                "8. Define a threshold and explain how you would calibrate it using human-labeled outputs.\n"
                "9. Trace the workflow in Phoenix (or equivalent observability tooling) with a session ID and metadata including model, environment, and run ID.\n"
                "10. Add at least three possible annotations such as correctness, wrong_tool, and needs_review.\n"
                "11. Explain how failed/annotated spans become a regression dataset for the next prompt or model version.\n"
                "12. Add one governance control to reduce evaluator-collusion risk."
            ),

            "expected_output": (
                "A complete evaluation architecture containing a grounding guardrail, "
                "bounded retry policy, rubric critic, calibrated threshold plan, observability "
                "metadata, annotations, regression workflow, and governance control."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "grounding",
                "guardrails",
                "bounded-retries",
                "rubrics",
                "critic-agents",
                "phoenix",
                "metadata",
                "annotations",
                "regression-datasets",
                "governance",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L07.QZ01",

        "title": "Building Robust Agents with Evaluation and Feedback — Knowledge Check",

        "lesson_code": "M01.L07",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L07.Q01",
                "section_id": "evaluation-purpose",
                "question": "What is the most accurate role of evaluation in agent robustness?",
                "options": [
                    "Evaluation automatically repairs bad architecture",
                    "Evaluation makes behavior measurable and provides evidence for improvement",
                    "Evaluation removes model variability",
                    "Evaluation replaces testing",
                ],
                "correct": 1,
                "explanation": (
                    "Evaluation exposes actual behavior and produces signals that can guide "
                    "changes, but it cannot repair a fundamentally poor design by itself."
                ),
            },

            {
                "id": "M01.L07.Q02",
                "section_id": "evaluation-types",
                "question": "Which case is best handled by a deterministic evaluator?",
                "options": [
                    "Whether a report feels persuasive",
                    "Whether an output object contains the required schema fields",
                    "Whether a poem is emotionally powerful",
                    "Whether a summary is elegantly written",
                ],
                "correct": 1,
                "explanation": (
                    "Schema validity has an exact check and does not require semantic judgment."
                ),
            },

            {
                "id": "M01.L07.Q03",
                "section_id": "governance",
                "question": "Why can using the same model for generator and evaluator be risky?",
                "options": [
                    "The evaluator cannot read text from the generator",
                    "They may share assumptions and blind spots, creating false confidence",
                    "The evaluator will always reject the answer",
                    "The model cannot produce typed output twice",
                ],
                "correct": 1,
                "explanation": (
                    "Shared training and failure modes can cause an evaluator to approve the "
                    "same hallucination or mistake."
                ),
            },

            {
                "id": "M01.L07.Q04",
                "section_id": "tdad",
                "question": "What comes first in TDAD?",
                "options": [
                    "Add many prompt rules",
                    "Define desired behavior and benchmarks",
                    "Deploy to production",
                    "Create an evaluator dashboard",
                ],
                "correct": 1,
                "explanation": (
                    "TDAD begins by deciding what good behavior should look like and expressing it through benchmarks."
                ),
            },

            {
                "id": "M01.L07.Q05",
                "section_id": "benchmark-design",
                "question": "Why should an agent benchmark inspect tool calls and intermediate behavior?",
                "options": [
                    "Because final outputs never matter",
                    "A correct final answer can still be reached through inefficient or unsafe behavior",
                    "Tool calls are deterministic in every agent",
                    "It removes the need for expected answers",
                ],
                "correct": 1,
                "explanation": (
                    "Trajectory quality matters: an agent can accidentally reach the right answer "
                    "while making poor decisions on the way."
                ),
            },

            {
                "id": "M01.L07.Q06",
                "section_id": "minimal-change",
                "question": "Why does the chapter recommend the smallest effective change first?",
                "options": [
                    "Because prompts can never be long",
                    "To preserve causal understanding and avoid unnecessary prompt complexity",
                    "Because tools cannot be changed",
                    "Because models should never be pinned",
                ],
                "correct": 1,
                "explanation": (
                    "Small changes make it easier to attribute improvements or regressions to a specific modification."
                ),
            },

            {
                "id": "M01.L07.Q07",
                "section_id": "evaluator-bugs",
                "question": "Expected answer is 'photons'; actual answer is 'Photons.'. What is the likely problem if the test fails?",
                "options": [
                    "The retrieval system must be wrong",
                    "The evaluator may be too brittle",
                    "The agent must use a different model",
                    "The benchmark should be deleted",
                ],
                "correct": 1,
                "explanation": (
                    "Case and punctuation differences should not necessarily make a semantically correct answer fail."
                ),
            },

            {
                "id": "M01.L07.Q08",
                "section_id": "three-evaluator-agents",
                "question": "Which evaluator asks whether a response is supported by authoritative source context?",
                "options": [
                    "Grounding agent",
                    "General critic only",
                    "Router agent",
                    "Planning agent",
                ],
                "correct": 0,
                "explanation": (
                    "Grounding evaluation specifically checks support against source/context evidence."
                ),
            },

            {
                "id": "M01.L07.Q09",
                "section_id": "grounding-guardrail",
                "question": "What changes when a grounding evaluator is placed inside an output guardrail?",
                "options": [
                    "It becomes capable of enforcing a block or recovery policy",
                    "It can no longer produce feedback",
                    "It disables retrieval",
                    "It removes the need for authoritative context",
                ],
                "correct": 0,
                "explanation": (
                    "The guardrail turns a diagnostic result into an enforceable runtime decision."
                ),
            },

            {
                "id": "M01.L07.Q10",
                "section_id": "retry-policy",
                "question": "Why must critic-driven retries have a hard ceiling?",
                "options": [
                    "Every retry is guaranteed to fail",
                    "Unbounded loops can consume unlimited cost and latency",
                    "Critics can only run once",
                    "Retries prevent tracing",
                ],
                "correct": 1,
                "explanation": (
                    "The retry policy needs a bounded failure path to avoid runaway execution."
                ),
            },

            {
                "id": "M01.L07.Q11",
                "section_id": "rubrics",
                "question": "Why is a rubric better than a vague 'is this good?' prompt for open-ended evaluation?",
                "options": [
                    "It eliminates all evaluator variability",
                    "It defines explicit quality dimensions and score meanings",
                    "It removes the need for human review",
                    "It makes every output binary",
                ],
                "correct": 1,
                "explanation": (
                    "Rubrics make evaluation criteria visible, structured, and diagnosable."
                ),
            },

            {
                "id": "M01.L07.Q12",
                "section_id": "threshold-calibration",
                "question": "How should a pass threshold ideally be selected?",
                "options": [
                    "Choose the highest number possible",
                    "Calibrate evaluator scores against representative human judgments",
                    "Always use 50%",
                    "Use a random threshold so the evaluator stays unbiased",
                ],
                "correct": 1,
                "explanation": (
                    "Threshold calibration balances false passes and false rejections against real human labels."
                ),
            },

            {
                "id": "M01.L07.Q13",
                "section_id": "annotations",
                "question": "What is a major long-term value of trace annotations?",
                "options": [
                    "They can turn human review into reusable labeled datasets and regression tests",
                    "They eliminate the need for metadata",
                    "They reduce context-window size automatically",
                    "They train the production model immediately",
                ],
                "correct": 0,
                "explanation": (
                    "Annotations convert ad hoc judgments into structured signals that can be filtered, analyzed, and replayed."
                ),
            },

            {
                "id": "M01.L07.Q14",
                "section_id": "evaluation-playbook",
                "type": "open",
                "question": (
                    "Design an evaluation system for a production RAG agent. Include benchmarks, repeated "
                    "runs, trajectory checks, grounding evaluation, one rubric critic, a bounded retry policy, "
                    "human review, tracing metadata, annotations, and one mechanism for checking evaluator quality."
                ),
            },
        ],

        "passing_score": 70,
    },
}
