"""M01.L02 — Core Components: LLMs, Prompting, and Agents.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
AI Agents in Action, Chapter 2, page range not supplied in the provided source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L02"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of AI Agents"

MODULE_DESCRIPTION = (
    "Build the core mental and practical foundations for AI agents: how LLMs "
    "generate tokens, how prompts shape behavior, how the OpenAI Agents SDK "
    "packages models and instructions into runnable agents, and how typed "
    "outputs, tracing, and tools make agent workflows more reliable."
)

SOURCE_CHAPTER = 2

SOURCE_PAGES = "Page range not supplied in the provided chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Core Components: LLMs, Prompting, and Agents",

    "slug": "ai-agents-m01-l02",

    "description": (
        "Understand how probabilistic language models power agents, how prompt "
        "engineering shapes their behavior, and how to build reliable agent "
        "workflows with typed outputs, tracing, and tool integration."
    ),

    "order": 2,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.0,

    "skill_tags": [
        "large-language-models",
        "tokenization",
        "sampling",
        "prompt-engineering",
        "openai-agents-sdk",
        "typed-output",
        "tracing",
        "tool-use",
        "tool-chaining",
        "agent-foundations",
    ],

    "prerequisite_ids": [
        "M01.L01",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Core Components: LLMs, Prompting, and Agents",

        "content": (
            "# Core Components: LLMs, Prompting, and Agents\n"
            "\n"
            "> **Course:** AI Agents  \n"
            "> **Lesson:** M01.L02  \n"
            "> **Module:** Foundations of AI Agents  \n"
            "> **Source alignment:** *AI Agents in Action*, Chapter 2. "
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
            "- Explain how an LLM generates text one token at a time.\n"
            "- Distinguish model prediction from token sampling.\n"
            "- Explain why text length and token length are not the same thing.\n"
            "- Describe how temperature, top-p, max tokens, and penalties affect generation.\n"
            "- Apply core prompt-engineering techniques to agent instructions.\n"
            "- Recognize common prompt-design failures and correct them.\n"
            "- Build a minimal agent with the OpenAI Agents SDK.\n"
            "- Use explicit model settings to control consistency, output length, and cost.\n"
            "- Use typed outputs to reduce brittle parsing and workflow breakage.\n"
            "- Explain why tracing is important in agent development.\n"
            "- Add internal tools to an agent and describe how tool registration works.\n"
            "- Distinguish sequential tool chaining from independent parallel tool calls.\n"
            "- Explain why limiting tool access improves cost, reliability, and safety.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why LLMs are the brain of modern agents\n"
            "\n"
            "In the previous lesson, you learned that an agent needs to interpret a goal, "
            "make decisions, plan, and use tools. In modern LLM-based agents, the language "
            "model provides much of that flexible reasoning and language capability.\n"
            "\n"
            "But before building agents, it helps to understand what the LLM is actually doing.\n"
            "\n"
            "An LLM does not read a prompt and retrieve a finished sentence from a hidden "
            "database. Instead, it repeatedly predicts what token should come next.\n"
            "\n"
            "At a high level:\n"
            "\n"
            "```text\n"
            "Prompt\n"
            "  -> tokenize\n"
            "  -> model processes tokens\n"
            "  -> probability distribution over next token\n"
            "  -> sampling/decoding chooses one token\n"
            "  -> append token to context\n"
            "  -> repeat\n"
            "```\n"
            "\n"
            "This repeated process produces complete answers one token at a time.\n"
            "\n"
            "[[IMAGE_NEEDED: LLM training versus inference | "
            "A two-part diagram. Left: training text -> tokenization -> prediction -> loss -> "
            "backpropagation -> updated weights. Right: prompt -> tokenization -> model -> next-token "
            "probabilities -> sampling -> generated token -> repeated generation | "
            "Learner should notice that training changes model weights, while inference uses the "
            "already-trained weights to generate tokens]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. LLMs are probabilistic token predictors\n"
            "\n"
            "The model receives tokenized input and produces a probability distribution over "
            "its vocabulary. That distribution answers a question like:\n"
            "\n"
            "```text\n"
            "Given everything I have seen so far, how likely is each possible next token?\n"
            "```\n"
            "\n"
            "A separate decoding or sampling process then chooses the actual next token.\n"
            "\n"
            "That distinction is important:\n"
            "\n"
            "- the **model** computes token probabilities,\n"
            "- the **sampling strategy** chooses which token becomes output.\n"
            "\n"
            "For the same model state and input, the probability distribution can be the same "
            "while different sampling strategies produce different outputs.\n"
            "\n"
            "### What training changes\n"
            "\n"
            "During base training, the model repeatedly predicts a next token and compares the "
            "prediction with the expected token. The mismatch is represented by a loss value. "
            "Backpropagation uses that loss to adjust the model's internal weights.\n"
            "\n"
            "Over enormous training datasets and many iterations, those weights come to encode "
            "patterns about language, concepts, relationships, and task structure.\n"
            "\n"
            "A useful correction to a common beginner mental model is this:\n"
            "\n"
            "> The model does not store knowledge as a giant lookup table.\n"
            "\n"
            "Its behavior emerges from learned parameters inside transformer attention and "
            "feedforward layers. During inference, those learned weights transform the current "
            "context into the next-token probability distribution.\n"
            "\n"
            "### Alignment after base training\n"
            "\n"
            "The chapter also separates base training from alignment. Alignment methods such as "
            "reinforcement learning with human feedback (RLHF) are used to improve instruction "
            "following and helpful conversational behavior. The source stresses that this is "
            "different from techniques specifically intended to improve reasoning behavior.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. What is a token?\n"
            "\n"
            "LLMs do not consume raw characters or complete sentences directly. Text is first "
            "broken into **tokens**. A token may represent:\n"
            "\n"
            "- a complete word,\n"
            "- part of a word,\n"
            "- punctuation,\n"
            "- whitespace-related structure,\n"
            "- or another vocabulary fragment.\n"
            "\n"
            "Each token maps to a numeric index in the model's vocabulary.\n"
            "\n"
            "### Why token count is different from text length\n"
            "\n"
            "Two text blocks with similar visible length can have very different token counts.\n"
            "\n"
            "For example, structured formats such as JSON contain braces, quotation marks, keys, "
            "colons, and repeated field names. These structural elements can increase token usage "
            "even when the underlying information is simple.\n"
            "\n"
            "```json\n"
            "{\"name\": \"Ada\", \"role\": \"researcher\"}\n"
            "```\n"
            "\n"
            "may use more tokens than an equivalent sentence such as:\n"
            "\n"
            "```text\n"
            "Ada is a researcher.\n"
            "```\n"
            "\n"
            "The lesson is not \"never use JSON.\" JSON is extremely useful for structured agent "
            "workflows. The lesson is that **structure has a token cost**.\n"
            "\n"
            "### Why token counting matters in agents\n"
            "\n"
            "Token count affects:\n"
            "\n"
            "- API cost,\n"
            "- context-window usage,\n"
            "- latency,\n"
            "- how much room remains for tool descriptions and conversation history,\n"
            "- how much output the model can generate.\n"
            "\n"
            "This becomes especially important in agent systems that may call an LLM several "
            "times during one task.\n"
            "\n"
            "The chapter mentions token-counting utilities such as `tiktoken` and SDK telemetry "
            "as practical ways to measure input and output usage instead of guessing from text length.\n"
            "\n"
            "[[IMAGE_NEEDED: Plain text versus JSON tokenization | "
            "Show the same semantic information written once as simple prose and once as JSON, "
            "with token boundaries highlighted so the JSON representation visibly contains more "
            "token pieces | "
            "Learner should notice that formatting characters and field names also consume tokens]]\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Controlling generation with model parameters\n"
            "\n"
            "Prompt wording is not the only thing that affects model output. Generation parameters "
            "control how the model samples or limits tokens.\n"
            "\n"
            "| Parameter | Main effect | Typical reason to change it |\n"
            "|---|---|---|\n"
            "| Temperature | Changes randomness in token selection | Lower for consistency; higher for creative variation |\n"
            "| top-p | Restricts sampling to a probability mass of likely tokens | Tighten or broaden variation |\n"
            "| max tokens | Caps response length | Control output size and cost |\n"
            "| presence penalty | Penalizes tokens once they have appeared | Encourage introduction of new material |\n"
            "| frequency penalty | Penalizes tokens more as they repeat | Reduce repeated phrases or loops |\n"
            "\n"
            "### Temperature\n"
            "\n"
            "Temperature reshapes the probability distribution before sampling.\n"
            "\n"
            "- Lower temperature makes high-probability tokens dominate more strongly.\n"
            "- Higher temperature makes the distribution flatter, allowing more variation.\n"
            "\n"
            "For a coding or planning agent, lower temperature may be useful because consistency "
            "and predictable formatting matter. For creative writing, a higher temperature may "
            "encourage more variety.\n"
            "\n"
            "However, temperature is an **influence**, not an absolute guarantee. Even at a very "
            "low setting, outputs may still vary.\n"
            "\n"
            "### top-p\n"
            "\n"
            "Top-p, also called nucleus sampling, keeps a set of likely tokens whose combined "
            "probability reaches the configured threshold, then samples from that set.\n"
            "\n"
            "The chapter advises against aggressively tuning both temperature and top-p at the "
            "same time because their interaction can make behavior harder to predict.\n"
            "\n"
            "### max tokens\n"
            "\n"
            "`max_tokens` provides a hard ceiling on response length. In agent systems this is "
            "especially useful as a cost and verbosity guardrail.\n"
            "\n"
            "### Seed and repeatability\n"
            "\n"
            "The chapter also mentions a seed parameter as useful for debugging and evaluation. "
            "The goal is to reduce uncontrolled variation when comparing runs.\n"
            "\n"
            "### Reasoning effort\n"
            "\n"
            "The source also notes that some modern models expose a reasoning-effort or thinking "
            "parameter. The chapter's recommendation is to avoid spending maximum reasoning effort "
            "on every tiny agent step. Use greater deliberation selectively for difficult planning, "
            "complex tool selection, or debugging.\n"
            "\n"
            "{{exercise:M01.L02.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Prompt engineering is the agent's behavioral design layer\n"
            "\n"
            "In Chapter 1, persona was introduced as one of the core agent layers. Prompt "
            "engineering is the practical process of designing that persona and its operating instructions.\n"
            "\n"
            "Good prompts make an agent more predictable. They also reduce wasted retries, unnecessary "
            "tokens, and ambiguous behavior.\n"
            "\n"
            "### Core prompt techniques\n"
            "\n"
            "The chapter presents several techniques that remain useful across different models.\n"
            "\n"
            "#### 1. Assign a clear role\n"
            "\n"
            "Tell the model who it is supposed to act as and what kind of expertise or perspective it should use.\n"
            "\n"
            "```text\n"
            "You are a senior DevOps engineer.\n"
            "```\n"
            "\n"
            "The role can shape vocabulary, tone, assumptions, and depth.\n"
            "\n"
            "#### 2. Front-load instructions\n"
            "\n"
            "Put the task and important constraints early. Then clearly separate user-provided "
            "data from instructions.\n"
            "\n"
            "#### 3. Use delimiters\n"
            "\n"
            "Delimiters make it obvious which text is data and which text is instruction.\n"
            "\n"
            "```text\n"
            "Task: Summarize the following article.\n"
            "\n"
            "<<<ARTICLE\n"
            "<article text>\n"
            "ARTICLE>>>\n"
            "```\n"
            "\n"
            "#### 4. Be specific\n"
            "\n"
            "Vague instructions create space for unpredictable interpretation. Prefer concrete "
            "requirements such as audience, length, number of items, and objective.\n"
            "\n"
            "#### 5. Define structure when needed\n"
            "\n"
            "If the framework does not provide typed output, you can describe the desired JSON, "
            "Markdown, CSV, or other structure in the prompt.\n"
            "\n"
            "When the SDK already enforces a typed output schema, strict formatting instructions "
            "can often be reduced.\n"
            "\n"
            "#### 6. Use examples\n"
            "\n"
            "Few-shot examples demonstrate the pattern the model should follow. They are useful "
            "when labels, style, or decision behavior is difficult to express through rules alone.\n"
            "\n"
            "#### 7. Use positive instructions\n"
            "\n"
            "Tell the model what to do instead of filling the prompt with prohibitions.\n"
            "\n"
            "```text\n"
            "Prefer: Explain using high-school-level language.\n"
            "Instead of only: Do not use jargon.\n"
            "```\n"
            "\n"
            "#### 8. Remove ambiguity\n"
            "\n"
            "Replace fuzzy expressions such as \"brief\" or \"a few\" with measurable limits when they matter.\n"
            "\n"
            "#### 9. Pick the right model and settings\n"
            "\n"
            "Prompt design is connected to model capability, cost, latency, and generation parameters.\n"
            "\n"
            "#### 10. Iterate and refine\n"
            "\n"
            "Treat prompt development like engineering: run it, inspect failures, tighten the "
            "instructions, add examples where needed, and test again.\n"
            "\n"
            "### Prompt caching\n"
            "\n"
            "The chapter also highlights a production optimization: stable prompt content can often "
            "benefit from provider-side prompt caching. Structuring stable system instructions and "
            "tool definitions separately from frequently changing user content can reduce repeated processing.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Turning workflows into prompts\n"
            "\n"
            "A useful way to write agent instructions is to imagine onboarding a new employee who "
            "has skill but lacks context.\n"
            "\n"
            "You do not need to explain every fact in the world. But you should make the workflow "
            "clear enough that the person can act without guessing critical requirements.\n"
            "\n"
            "For example, imagine a search agent that can choose between an internal knowledge base "
            "and the public web.\n"
            "\n"
            "A structured prompt could specify:\n"
            "\n"
            "```text\n"
            "Role: Internal Knowledge Search Agent\n"
            "\n"
            "Task:\n"
            "- Choose source A or B.\n"
            "- Search the chosen source.\n"
            "- If nothing is found, try the other source once.\n"
            "- If still unsuccessful, escalate.\n"
            "\n"
            "Constraints:\n"
            "- One chosen source at a time.\n"
            "- Up to three findings.\n"
            "- Plain language.\n"
            "```\n"
            "\n"
            "The important idea is that prompts can encode **decision points**, not only one-step "
            "instructions.\n"
            "\n"
            "However, a prompt-described loop is still not the same as a durable agent runtime. "
            "The chapter notes that plain LLM prompting may stop loops early, while an agent system "
            "can be designed to keep executing until the goal is complete or judged unattainable.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Common prompt-engineering pitfalls\n"
            "\n"
            "More instructions do not automatically produce a better prompt.\n"
            "\n"
            "| Problem | Why it hurts | Better approach |\n"
            "|---|---|---|\n"
            "| Too complicated | More context, more conflicts, higher token cost | Split into focused steps or roles |\n"
            "| Contradictory | Model must guess which instruction wins | Remove or prioritize conflicting rules |\n"
            "| Too simple | Creates many unnecessary round-trips | Combine related micro-tasks where appropriate |\n"
            "| Inconsistent delimiters | Harder for model and parsers to interpret structure | Use one consistent delimiter style |\n"
            "| Overly explicit | Too many rules increase the chance some are ignored | Keep critical rules; validate with guardrails |\n"
            "| Variable output | Low temperature alone does not guarantee consistency | Improve instructions, structure, schemas, and constraints |\n"
            "\n"
            "### A practical rule\n"
            "\n"
            "If your prompt is becoming a giant operating manual, ask whether part of the logic "
            "belongs somewhere else:\n"
            "\n"
            "- typed schemas,\n"
            "- a workflow engine,\n"
            "- a validation step,\n"
            "- a separate specialized agent,\n"
            "- tool-level constraints.\n"
            "\n"
            "Prompt engineering is powerful, but it should not carry every responsibility in the system.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Building a minimal agent with the OpenAI Agents SDK\n"
            "\n"
            "Once you understand model behavior and prompting, you can combine them into a runnable agent.\n"
            "\n"
            "The chapter's first example builds a research-planning component.\n"
            "\n"
            "A minimal version looks like this:\n"
            "\n"
            "```python\n"
            "from agents import Agent, Runner\n"
            "from dotenv import load_dotenv\n"
            "\n"
            "load_dotenv()\n"
            "\n"
            "instructions = \"\"\"\n"
            "You are a research planning assistant.\n"
            "\n"
            "TASK\n"
            "- You will receive a research topic.\n"
            "- Return five concise research tasks.\n"
            "\"\"\"\n"
            "\n"
            "agent = Agent(\n"
            "    name=\"Research Planner\",\n"
            "    instructions=instructions,\n"
            ")\n"
            "\n"
            "result = Runner.run_sync(\n"
            "    agent,\n"
            "    input=\"learn about AI agents\",\n"
            ")\n"
            "\n"
            "print(result.final_output)\n"
            "```\n"
            "\n"
            "### What each part does\n"
            "\n"
            "1. `Agent` defines the agent's name and instructions.\n"
            "2. `Runner` executes the agent.\n"
            "3. `load_dotenv()` loads environment configuration such as API credentials.\n"
            "4. `instructions` define the persona/task behavior.\n"
            "5. `Runner.run_sync(...)` runs the agent synchronously.\n"
            "6. `result.final_output` provides the final model response.\n"
            "\n"
            "At this point, the system is still mostly a prompted model step. Later, tool access "
            "adds the decision-making power associated with stronger agency.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Setting the agent model and generation settings\n"
            "\n"
            "Different agent roles need different generation behavior. A planner may benefit from "
            "consistency; a brainstorming agent may benefit from more variety.\n"
            "\n"
            "The chapter shows explicit model configuration similar to:\n"
            "\n"
            "```python\n"
            "from agents import Agent, ModelSettings\n"
            "\n"
            "agent = Agent(\n"
            "    name=\"Research Planner\",\n"
            "    instructions=instructions,\n"
            "    model=\"gpt-4.1\",\n"
            "    model_settings=ModelSettings(\n"
            "        temperature=0.0,\n"
            "        max_tokens=150,\n"
            "        top_p=1.0,\n"
            "        frequency_penalty=0.5,\n"
            "        presence_penalty=0.5,\n"
            "    ),\n"
            ")\n"
            "```\n"
            "\n"
            "The exact model choice may change over time, but the architectural lesson stays the same: "
            "make model selection and important generation settings explicit when reproducibility matters.\n"
            "\n"
            "Even with temperature set low, do not assume outputs will be perfectly identical. "
            "Longer outputs generally create more opportunities for variation.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Typed outputs make workflows more reliable\n"
            "\n"
            "Suppose Agent A produces a research plan that Agent B will consume.\n"
            "\n"
            "If Agent A returns free-form text, its formatting may vary:\n"
            "\n"
            "```text\n"
            "Run 1: 1. Search papers ...\n"
            "Run 2: Here is your plan: ...\n"
            "Run 3: {\"steps\": ...}\n"
            "```\n"
            "\n"
            "That variability can break downstream code.\n"
            "\n"
            "Typed output solves this by telling the SDK the structure the model must produce.\n"
            "\n"
            "### Basic typed output\n"
            "\n"
            "```python\n"
            "from pydantic import BaseModel\n"
            "\n"
            "class ResearchPlanModel(BaseModel):\n"
            "    tasks: list[str]\n"
            "\n"
            "agent = Agent(\n"
            "    name=\"Research Planner\",\n"
            "    instructions=instructions,\n"
            "    output_type=ResearchPlanModel,\n"
            ")\n"
            "```\n"
            "\n"
            "Now downstream code receives a predictable `ResearchPlanModel` instead of parsing arbitrary prose.\n"
            "\n"
            "### Why strict schemas matter\n"
            "\n"
            "The source shows an example where a loose dictionary structure causes a strict JSON schema error. "
            "The preferred solution is to fix the data model rather than disabling strict validation.\n"
            "\n"
            "A stricter approach can define a task shape explicitly:\n"
            "\n"
            "```python\n"
            "from pydantic import BaseModel, ConfigDict\n"
            "from typing_extensions import TypedDict\n"
            "\n"
            "class Task(TypedDict):\n"
            "    id: int\n"
            "    description: str\n"
            "\n"
            "class ResearchPlanModel(BaseModel):\n"
            "    tasks: list[Task]\n"
            "    model_config = ConfigDict(extra=\"forbid\")\n"
            "```\n"
            "\n"
            "`extra=\"forbid\"` prevents unexpected fields from silently appearing.\n"
            "\n"
            "### Why this matters for agents\n"
            "\n"
            "Typed outputs:\n"
            "\n"
            "- reduce brittle text parsing,\n"
            "- make handoffs between agents safer,\n"
            "- separate format enforcement from prompt wording,\n"
            "- make validation failures visible,\n"
            "- support predictable workflows despite probabilistic generation.\n"
            "\n"
            '{{image:typed-agent-workflow}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 11. Tracing: see what your agent actually did\n"
            "\n"
            "As agents gain more steps and tools, debugging from the final answer alone becomes difficult.\n"
            "\n"
            "Tracing records execution details such as:\n"
            "\n"
            "- model calls,\n"
            "- instructions,\n"
            "- inputs,\n"
            "- outputs,\n"
            "- token usage,\n"
            "- tool calls,\n"
            "- call order,\n"
            "- timing.\n"
            "\n"
            "The chapter notes that the OpenAI Agents SDK can provide tracing when used with the "
            "OpenAI API, and also mentions external observability tools as alternatives for "
            "multi-provider or framework-agnostic setups.\n"
            "\n"
            "You can also name a workflow trace in code:\n"
            "\n"
            "```python\n"
            "from agents import trace\n"
            "\n"
            "with trace(\"Deep Research Workflow\"):\n"
            "    result = Runner.run_sync(\n"
            "        agent,\n"
            "        input=\"learn about AI agents\",\n"
            "    )\n"
            "```\n"
            "\n"
            "A trace becomes increasingly valuable once an agent begins making multiple model "
            "calls or choosing among tools.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Giving agents tools\n"
            "\n"
            "A model that only produces text has limited agency. Tools allow the system to retrieve "
            "information or perform actions beyond the model itself.\n"
            "\n"
            "The chapter distinguishes:\n"
            "\n"
            "- **Tools:** capabilities available to the agent.\n"
            "- **Actions:** what the agent actually does with those capabilities.\n"
            "\n"
            "A tool may be:\n"
            "\n"
            "- an internal Python function,\n"
            "- an external service exposed through MCP,\n"
            "- a handoff to another agent.\n"
            "\n"
            "### Exposing a Python function as a tool\n"
            "\n"
            "The source demonstrates a pattern like this:\n"
            "\n"
            "```python\n"
            "from agents import function_tool\n"
            "\n"
            "@function_tool\n"
            "def get_research_sources() -> list[str]:\n"
            "    \"\"\"Return available research sources.\"\"\"\n"
            "    return [\"Wikipedia\", \"Google\", \"YouTube\"]\n"
            "\n"
            "agent = Agent(\n"
            "    name=\"Research Planner\",\n"
            "    instructions=instructions,\n"
            "    output_type=ResearchPlanModel,\n"
            "    tools=[get_research_sources],\n"
            ")\n"
            "```\n"
            "\n"
            "The decorator exposes the function as a tool and generates the structured description "
            "needed by the agent runtime.\n"
            "\n"
            "### Prompting tool use explicitly\n"
            "\n"
            "It is often useful to tell the agent **when** a tool should be used.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Before creating the research plan:\n"
            "1. Call get_research_sources().\n"
            "2. Use only the returned sources in the plan.\n"
            "```\n"
            "\n"
            "This makes the tool part of the agent's reasoning and workflow rather than merely "
            "a capability sitting unused in the registry.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Why more tools are not always better\n"
            "\n"
            "Giving an agent dozens of tools may look powerful, but every tool has a cost.\n"
            "\n"
            "The chapter emphasizes four important effects.\n"
            "\n"
            "### 1. Tools create token overhead\n"
            "\n"
            "Tool descriptions are commonly sent with LLM calls so the model knows what capabilities "
            "are available. More tool schemas mean more input tokens.\n"
            "\n"
            "### 2. Tools increase decision complexity\n"
            "\n"
            "The model must decide which tool is appropriate. Similar or poorly described tools make "
            "selection harder.\n"
            "\n"
            "### 3. Tools create failure points\n"
            "\n"
            "Tools can time out, hit rate limits, return malformed data, or fail entirely.\n"
            "\n"
            "The chapter highlights common recovery patterns:\n"
            "\n"
            "- retries with backoff for transient failures,\n"
            "- structured errors the model can reason about,\n"
            "- fallback tools or alternate paths,\n"
            "- timeouts for hanging operations.\n"
            "\n"
            "### 4. Tools grant power\n"
            "\n"
            "A search tool is relatively low risk. A delete-files tool can create destructive outcomes.\n"
            "\n"
            "The design principle is simple:\n"
            "\n"
            "> Give the agent only the capabilities it genuinely needs, and design as though it may "
            "eventually use every capability you expose.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Tool chaining and parallel calls\n"
            "\n"
            "Agents often need more than one tool call.\n"
            "\n"
            "### Sequential tool chaining\n"
            "\n"
            "A chain exists when a later tool depends on output from an earlier tool.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "get_research_sources()\n"
            "        |\n"
            "        v\n"
            "[\"Wikipedia\", \"Google\", \"YouTube\"]\n"
            "        |\n"
            "        v\n"
            "get_resource_url(\"Wikipedia\")\n"
            "        |\n"
            "        v\n"
            "\"https://www.wikipedia.org\"\n"
            "```\n"
            "\n"
            "The second call cannot be fully determined until the first call returns.\n"
            "\n"
            "### Parallel tool calls\n"
            "\n"
            "When tool calls are independent, a capable agent may issue several in parallel.\n"
            "\n"
            "```text\n"
            "             -> search_web()\n"
            "Agent step  -> query_calendar()\n"
            "             -> lookup_knowledge_base()\n"
            "```\n"
            "\n"
            "Parallel calls can reduce latency, but only when the calls do not depend on one another.\n"
            "\n"
            "### Why traces matter here\n"
            "\n"
            "Once a workflow contains several model and tool calls, tracing lets you inspect:\n"
            "\n"
            "- the order in which calls happened,\n"
            "- which calls depended on earlier results,\n"
            "- how long each step took,\n"
            "- where failures or unnecessary calls occurred.\n"
            "\n"
            "[[IMAGE_NEEDED: Sequential tool chain versus parallel tool calls | "
            "Left: Tool A -> result -> Tool B -> result. Right: one agent step fans out to Tool A, "
            "Tool B, and Tool C simultaneously, then merges results | "
            "Learner should notice that dependency determines whether calls must be sequential or "
            "can safely run in parallel]]\n"
            "\n"
            "{{exercise:M01.L02.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Putting the chapter together\n"
            "\n"
            "The complete picture now looks like this:\n"
            "\n"
            "```text\n"
            "User goal\n"
            "   |\n"
            "   v\n"
            "Prompt / persona\n"
            "   |\n"
            "   v\n"
            "LLM\n"
            "   |\n"
            "   +--> generation settings\n"
            "   +--> typed output contract\n"
            "   +--> registered tools\n"
            "   |\n"
            "   v\n"
            "Agent runtime\n"
            "   |\n"
            "   +--> tool calls\n"
            "   +--> tool chains / parallel calls\n"
            "   +--> traces\n"
            "   |\n"
            "   v\n"
            "Validated result\n"
            "```\n"
            "\n"
            "Each layer solves a different problem:\n"
            "\n"
            "- **LLM:** provides probabilistic language generation and reasoning capability.\n"
            "- **Prompt:** defines the task, role, constraints, and workflow guidance.\n"
            "- **Model settings:** tune variability, length, and cost.\n"
            "- **Typed output:** creates stable data contracts.\n"
            "- **Tools:** let the agent retrieve information and act.\n"
            "- **Tracing:** makes execution observable and debuggable.\n"
            "\n"
            "This is the bridge from 'prompting a model' to engineering an actual agent system.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: An LLM stores facts like a database\n"
            "\n"
            "> The model does not simply look up a stored sentence.\n"
            "\n"
            "Its learned weights transform the current context and produce a probability "
            "distribution over the next token.\n"
            "\n"
            "### Misconception 2: Temperature 0 guarantees identical answers\n"
            "\n"
            "> Low temperature reduces variation but does not make the whole system mathematically identical across every run.\n"
            "\n"
            "Prompt clarity, model behavior, tool results, and other runtime factors still matter.\n"
            "\n"
            "### Misconception 3: More prompt rules always improve reliability\n"
            "\n"
            "> Excessive rules can create conflicts, increase token cost, and make priorities harder to follow.\n"
            "\n"
            "Use schemas, guardrails, workflows, and specialized steps where appropriate.\n"
            "\n"
            "### Misconception 4: A prompt step is automatically a full agent\n"
            "\n"
            "> A prompted model can be one step in an agent workflow, but stronger agency appears when the system can make decisions and use tools to pursue a goal.\n"
            "\n"
            "### Misconception 5: Give the agent every available tool\n"
            "\n"
            "> Each tool adds token overhead, complexity, failure modes, and authority.\n"
            "\n"
            "Curate the tool set around what the agent truly needs.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Token | A vocabulary unit consumed or generated by the model |\n"
            "| Tokenization | Converting text into token IDs the model can process |\n"
            "| Probability distribution | Scores representing how likely each next token is |\n"
            "| Sampling | Choosing an actual next token from the model's distribution |\n"
            "| Temperature | Parameter controlling randomness in token selection |\n"
            "| top-p | Nucleus-sampling threshold that limits the candidate probability mass |\n"
            "| max tokens | Maximum number of output tokens the model may generate |\n"
            "| Prompt engineering | Designing instructions that shape model or agent behavior |\n"
            "| Persona | The role, behavior, and operating instructions assigned to an agent |\n"
            "| Few-shot prompting | Providing examples that demonstrate desired behavior |\n"
            "| Typed output | A validated data structure used as the agent's response contract |\n"
            "| Strict schema | A schema that rejects unexpected or structurally invalid output |\n"
            "| Trace | Recorded execution information about model and tool calls |\n"
            "| Tool | A callable capability available to an agent |\n"
            "| Action | A concrete use of a tool or other capability |\n"
            "| Tool chaining | Feeding an earlier tool's result into a later tool call |\n"
            "| Parallel tool calls | Independent tool calls executed at the same stage to reduce latency |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What does an LLM predict at each generation step?\n"
            "2. What is the difference between model prediction and sampling?\n"
            "3. Why can JSON use more tokens than equivalent prose?\n"
            "4. What happens when temperature is raised or lowered?\n"
            "5. Why should max tokens be treated as a cost and verbosity guardrail?\n"
            "6. Name five prompt-engineering techniques from this lesson.\n"
            "7. Why can a giant prompt become less reliable rather than more reliable?\n"
            "8. What are the minimum moving parts in the chapter's first agent example?\n"
            "9. Why are typed outputs useful between workflow steps?\n"
            "10. Why is disabling strict schema validation usually a weaker fix than correcting the schema?\n"
            "11. What information can tracing reveal?\n"
            "12. What changes when a function is exposed as a tool?\n"
            "13. Why should an agent have a limited tool set?\n"
            "14. When should tools be chained sequentially?\n"
            "15. When can tools be called in parallel?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Reliable agents are built by combining several controls: understand the LLM's "
            "probabilistic token behavior, write clear prompts, tune generation deliberately, "
            "enforce structured outputs, expose only necessary tools, and trace what actually "
            "happens during execution.**\n"
        ),

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "llm-foundation",
                "title": "Why LLMs are the brain of modern agents",
                "order": 1,
            },
            {
                "id": "probabilistic-generation",
                "title": "LLMs are probabilistic token predictors",
                "order": 2,
            },
            {
                "id": "tokens",
                "title": "What is a token?",
                "order": 3,
            },
            {
                "id": "generation-settings",
                "title": "Controlling generation with model parameters",
                "order": 4,
            },
            {
                "id": "prompt-engineering",
                "title": "Prompt engineering is the agent's behavioral design layer",
                "order": 5,
            },
            {
                "id": "workflow-prompts",
                "title": "Turning workflows into prompts",
                "order": 6,
            },
            {
                "id": "prompt-pitfalls",
                "title": "Common prompt-engineering pitfalls",
                "order": 7,
            },
            {
                "id": "minimal-agent",
                "title": "Building a minimal agent with the OpenAI Agents SDK",
                "order": 8,
            },
            {
                "id": "agent-model-settings",
                "title": "Setting the agent model and generation settings",
                "order": 9,
            },
            {
                "id": "typed-output",
                "title": "Typed outputs make workflows more reliable",
                "order": 10,
            },
            {
                "id": "tracing",
                "title": "Tracing: see what your agent actually did",
                "order": 11,
            },
            {
                "id": "tools",
                "title": "Giving agents tools",
                "order": 12,
            },
            {
                "id": "tool-cost-safety",
                "title": "Why more tools are not always better",
                "order": 13,
            },
            {
                "id": "tool-chaining",
                "title": "Tool chaining and parallel calls",
                "order": 14,
            },
            {
                "id": "complete-architecture",
                "title": "Putting the chapter together",
                "order": 15,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L02.EX01",

            "title": "Tune and Refine a Research Planner",

            "lesson_code": "M01.L02",

            "section_id": "generation-settings",

            "placement": "after_section",

            "description": (
                "Practice how prompt wording and generation settings affect a "
                "simple research-planning agent."
            ),

            "instructions": (
                "Build or adapt the minimal Research Planner agent from this lesson.\n"
                "1. Use the topic `learn about AI agents`.\n"
                "2. Require exactly five concise research tasks.\n"
                "3. Run once with temperature=0.0 and max_tokens=150.\n"
                "4. Run again with the same settings and compare the outputs.\n"
                "5. Change temperature to 1.0 and run once more.\n"
                "6. Refine the prompt using at least four techniques from this lesson: "
                "clear persona, front-loaded task, delimiters, measurable length limits, "
                "positive wording, examples, or explicit constraints.\n"
                "7. Write a short note explaining which changes came from prompt design "
                "and which came from generation settings."
            ),

            "expected_output": (
                "Three captured outputs plus a refined prompt and a short comparison "
                "of consistency, formatting, and variation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "prompt-engineering",
                "temperature",
                "max-tokens",
                "output-consistency",
                "agent-configuration",
            ],
        },

        {
            "id": "M01.L02.EX02",

            "title": "Build a Typed Tool-Using Research Agent",

            "lesson_code": "M01.L02",

            "section_id": "tool-chaining",

            "placement": "after_section",

            "description": (
                "Combine typed output, tool registration, tool chaining, and tracing "
                "into one small agent workflow."
            ),

            "instructions": (
                "Extend the Research Planner from this lesson.\n"
                "1. Create a strict ResearchPlanModel using Pydantic and TypedDict.\n"
                "2. Define get_research_sources() as a function tool.\n"
                "3. Define get_resource_url(source) as a second function tool.\n"
                "4. Register both tools with the agent.\n"
                "5. Update the prompt so the agent gets available sources before building the plan.\n"
                "6. Require each task to include a step number, research source, URL, and description.\n"
                "7. Wrap the run in a named trace.\n"
                "8. Identify which tool calls must be sequential and explain why.\n"
                "9. Identify one hypothetical independent tool call that could run in parallel.\n"
                "10. Write one safety or reliability improvement you would add before production use."
            ),

            "expected_output": (
                "A working or carefully written code example, a strict typed schema, "
                "a traced tool chain, and a short explanation of sequential dependencies, "
                "possible parallelism, and one production safeguard."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "typed-output",
                "pydantic",
                "function-tools",
                "tool-chaining",
                "tracing",
                "parallel-tool-reasoning",
                "agent-safety",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L02.QZ01",

        "title": "Core Components: LLMs, Prompting, and Agents — Knowledge Check",

        "lesson_code": "M01.L02",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L02.Q01",

                "section_id": "probabilistic-generation",

                "question": "What does an LLM produce before a next token is selected?",

                "options": [
                    "A complete final answer",
                    "A probability distribution over possible next tokens",
                    "A database row containing the next sentence",
                    "A fixed list of tool calls",
                ],

                "correct": 1,

                "explanation": (
                    "The model produces probabilities for candidate next tokens. "
                    "A decoding or sampling strategy then selects the actual token."
                ),
            },

            {
                "id": "M01.L02.Q02",

                "section_id": "tokens",

                "question": "Why is visible text length a poor estimate of token count?",

                "options": [
                    "Every character is always one token",
                    "Tokenization splits text into vocabulary-dependent pieces, and formatting also consumes tokens",
                    "Only numbers are tokenized",
                    "Tokens are counted only after generation finishes",
                ],

                "correct": 1,

                "explanation": (
                    "Tokens may be words, word parts, punctuation, or structural fragments, "
                    "so visually similar texts can use different token counts."
                ),
            },

            {
                "id": "M01.L02.Q03",

                "section_id": "generation-settings",

                "question": "What is the main effect of lowering temperature?",

                "options": [
                    "It increases context-window size",
                    "It makes higher-probability token choices dominate more strongly",
                    "It automatically validates JSON output",
                    "It adds more tools to the agent",
                ],

                "correct": 1,

                "explanation": (
                    "Lower temperature sharpens token selection toward higher-probability "
                    "choices, generally reducing variation."
                ),
            },

            {
                "id": "M01.L02.Q04",

                "section_id": "prompt-engineering",

                "question": "Which prompt is more precise?",

                "options": [
                    "Write something short about AI",
                    "Explain AI agents clearly",
                    "Write 3 bullet points, each under 20 words, for beginner software developers",
                    "Do not make the answer bad",
                ],

                "correct": 2,

                "explanation": (
                    "It defines count, length, audience, and structure, reducing ambiguity."
                ),
            },

            {
                "id": "M01.L02.Q05",

                "section_id": "prompt-pitfalls",

                "question": (
                    "A prompt has 40 detailed rules, several contradictory constraints, "
                    "and three different delimiter styles. What is the best first response?"
                ),

                "options": [
                    "Increase the temperature",
                    "Add even more rules",
                    "Simplify the prompt, remove conflicts, and standardize structure",
                    "Disable output validation",
                ],

                "correct": 2,

                "explanation": (
                    "Over-engineered prompts can increase confusion and token cost. "
                    "Simplifying and removing conflicts is the stronger fix."
                ),
            },

            {
                "id": "M01.L02.Q06",

                "section_id": "minimal-agent",

                "question": "What is the main role of Runner.run_sync in the lesson's minimal example?",

                "options": [
                    "Train a new foundation model",
                    "Execute the configured agent synchronously",
                    "Create an MCP server",
                    "Validate a Pydantic schema without running the model",
                ],

                "correct": 1,

                "explanation": (
                    "The runner executes the agent with the supplied input and returns the result."
                ),
            },

            {
                "id": "M01.L02.Q07",

                "section_id": "typed-output",

                "question": "Why are typed outputs valuable in multi-step agent workflows?",

                "options": [
                    "They make the model non-probabilistic",
                    "They remove the need for any prompt",
                    "They provide a predictable validated structure for downstream consumers",
                    "They guarantee every tool call succeeds",
                ],

                "correct": 2,

                "explanation": (
                    "Typed outputs act as stable contracts between workflow steps, reducing "
                    "the risk that formatting variation breaks downstream logic."
                ),
            },

            {
                "id": "M01.L02.Q08",

                "section_id": "tracing",

                "question": "Which question is tracing especially useful for answering?",

                "options": [
                    "What font should the UI use?",
                    "Which model/tool calls happened, in what order, and how long did they take?",
                    "What is the user's favorite color?",
                    "How should a database table be indexed without any runtime data?",
                ],

                "correct": 1,

                "explanation": (
                    "Tracing provides execution visibility across model calls, tool calls, "
                    "inputs, outputs, timing, and often token usage."
                ),
            },

            {
                "id": "M01.L02.Q09",

                "section_id": "tool-cost-safety",

                "question": "Why should an agent's tool list usually be limited?",

                "options": [
                    "Agents can only understand one tool",
                    "Every additional tool adds schema overhead, choice complexity, failure risk, and authority",
                    "Tools prevent tracing",
                    "A model cannot call functions written in Python",
                ],

                "correct": 1,

                "explanation": (
                    "Tool descriptions consume tokens, more choices make selection harder, "
                    "tools can fail, and powerful tools increase the consequences of mistakes."
                ),
            },

            {
                "id": "M01.L02.Q10",

                "section_id": "tool-chaining",

                "question": (
                    "Tool B requires an ID returned by Tool A. How should these calls normally be executed?"
                ),

                "options": [
                    "In parallel",
                    "Sequentially, because Tool B depends on Tool A's output",
                    "Only through typed output",
                    "Without tracing",
                ],

                "correct": 1,

                "explanation": (
                    "A dependency creates a tool chain. Tool A must produce the value "
                    "before Tool B can receive it."
                ),
            },

            {
                "id": "M01.L02.Q11",

                "section_id": "complete-architecture",

                "type": "open",

                "question": (
                    "Design a small research agent using the concepts in this lesson. "
                    "Describe its persona, model settings, typed output schema, two tools, "
                    "one trace you would inspect, and one rule for deciding whether the "
                    "tools run sequentially or in parallel."
                ),
            },
        ],

        "passing_score": 70,
    },
}
