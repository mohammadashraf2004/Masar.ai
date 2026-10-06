"""M04.L01 — Evaluate AI Systems.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 4, "Evaluate AI Systems".
Instructor-authored curriculum adaptation based only on the supplied chapter.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M04.L01"

MODULE_ORDER = 4

MODULE_TITLE = "Evaluating AI Systems"

MODULE_DESCRIPTION = (
    "Learn how to define evaluation criteria, select models, reason about "
    "build-versus-buy decisions, navigate public benchmarks, detect benchmark "
    "contamination, and build a reliable evaluation pipeline for production AI "
    "applications."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Page range not provided in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Evaluate AI Systems",

    "slug": "ai-engineering-m04-l01-evaluate-ai-systems",

    "description": (
        "A practical lesson on evaluation-driven development, model-selection "
        "criteria, factuality and safety evaluation, instruction following, "
        "latency and cost, model APIs versus self-hosting, benchmark pitfalls, "
        "and end-to-end evaluation-pipeline design."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.5,

    "skill_tags": [
        "ai-evaluation",
        "evaluation-driven-development",
        "factual-consistency",
        "safety-evaluation",
        "instruction-following",
        "model-selection",
        "latency",
        "cost",
        "model-apis",
        "self-hosting",
        "benchmarks",
        "data-contamination",
        "evaluation-pipeline",
        "production-evaluation",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Evaluate AI Systems",

        "content": (
            "# Evaluate AI Systems\n"
            "\n"
            "> **Course:** AI Engineering Foundations  \n"
            "> **Lesson:** M04.L01  \n"
            "> **Module:** Evaluating AI Systems  \n"
            "> **Source alignment:** Chapter 4, *Evaluate AI Systems*. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Apply evaluation-driven development by defining success before "
            "building an AI application.\n"
            "- Organize model-selection criteria into domain capability, generation "
            "quality, instruction following, cost, latency, scale, and operational "
            "constraints.\n"
            "- Distinguish local factual consistency from global factual consistency.\n"
            "- Explain multiple approaches to factuality verification, including AI "
            "judges, self-verification, search-augmented checking, and textual entailment.\n"
            "- Design safety evaluations appropriate to an application's risks.\n"
            "- Evaluate instruction-following behavior using automatically verifiable "
            "constraints and subjective criteria.\n"
            "- Balance quality, latency, and cost using hard requirements and soft preferences.\n"
            "- Distinguish hard model attributes from soft attributes in model selection.\n"
            "- Compare model APIs and self-hosting across privacy, data lineage, "
            "performance, functionality, cost, control, and deployment constraints.\n"
            "- Evaluate whether a public benchmark is relevant and trustworthy for "
            "your application.\n"
            "- Explain benchmark saturation, correlation, aggregation, and contamination.\n"
            "- Design an end-to-end evaluation pipeline that evaluates components, "
            "turns, tasks, metrics, and production behavior.\n"
            "- Build scoring rubrics tied to business outcomes and usefulness thresholds.\n"
            "- Use data slices, bootstrap analysis, and experiment tracking to improve "
            "evaluation reliability.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Evaluation-driven development\n"
            "\n"
            "A model is useful only if it works for the purpose you care about. "
            "That means evaluation should be designed **before** the application "
            "is fully built, not added as an afterthought.\n"
            "\n"
            "The chapter calls this **evaluation-driven development**. The idea is "
            "inspired by test-driven development in software engineering:\n"
            "\n"
            "```text\n"
            "software engineering:\n"
            "tests -> implementation\n"
            "\n"
            "AI engineering:\n"
            "evaluation criteria -> application development\n"
            "```\n"
            "\n"
            "Before spending heavily on an application, ask:\n"
            "\n"
            "- What business or user value must this application create?\n"
            "- How will we know whether it creates that value?\n"
            "- What failures would make it unsafe or unusable?\n"
            "- What quality level is merely impressive, and what level is actually useful?\n"
            "\n"
            "Applications with clear measurable outcomes are easier to justify and "
            "improve. Recommendation systems can be linked to engagement or purchase "
            "behavior. Fraud systems can be linked to prevented losses. Generated "
            "code can often be tested through execution.\n"
            "\n"
            "This does not mean teams should build only easy-to-measure applications. "
            "It means difficult applications require more deliberate investment in "
            "evaluation infrastructure.\n"
            "\n"
            "[[IMAGE_NEEDED: Evaluation-driven development loop | A loop showing "
            "define criteria -> build prototype -> evaluate -> improve -> deploy -> "
            "collect production evidence -> refine criteria | Learner should notice "
            "that evaluation starts before implementation and continues throughout "
            "the application's lifecycle]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Start with application-specific evaluation criteria\n"
            "\n"
            "The chapter groups common criteria into four broad buckets:\n"
            "\n"
            "1. **Domain-specific capability** — can the model perform the kind of "
            "work your domain requires?\n"
            "2. **Generation capability** — are the generated outputs useful, "
            "faithful, safe, coherent, or otherwise high quality?\n"
            "3. **Instruction-following capability** — does the model actually "
            "follow the instructions and constraints you give it?\n"
            "4. **Cost and latency** — can you afford to run the system, and is it "
            "fast enough for the product experience?\n"
            "\n"
            "Imagine a legal-contract summarizer. You might ask:\n"
            "\n"
            "- Does the model understand legal content?\n"
            "- Is the summary factually consistent with the contract?\n"
            "- Does the summary follow the requested length and format?\n"
            "- How long does it take and how much does it cost?\n"
            "\n"
            "A single overall score cannot answer all of these questions.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Domain-specific capability\n"
            "\n"
            "A model must first possess the capabilities the application needs. A "
            "coding agent needs coding ability. A translation application needs "
            "the required languages. A scientific assistant needs relevant "
            "knowledge and reasoning ability.\n"
            "\n"
            "These capabilities are constrained by the model's training data, "
            "architecture, size, and training process.\n"
            "\n"
            "### Use exact evaluation when possible\n"
            "\n"
            "Coding tasks are a strong example. Generated code can be executed and "
            "checked for functional correctness. But correctness may not be enough.\n"
            "\n"
            "A generated SQL query can return the right rows yet be unusably slow. "
            "Therefore, evaluation might include:\n"
            "\n"
            "- Execution correctness.\n"
            "- Runtime.\n"
            "- Memory usage.\n"
            "- Readability or maintainability.\n"
            "\n"
            "The first three can often be measured exactly. Readability may require "
            "human or AI judgment.\n"
            "\n"
            "### Why multiple-choice benchmarks are popular\n"
            "\n"
            "Many domain benchmarks convert open-ended knowledge or reasoning into "
            "multiple-choice questions because the answers are easier to verify and "
            "results are easier to reproduce.\n"
            "\n"
            "For a four-option question with one correct answer, random guessing "
            "gives a 25% baseline. Classification is a related special case where "
            "the same answer categories are reused across examples.\n"
            "\n"
            "However, MCQs mainly test **recognition or selection**. They are not "
            "a complete measurement of open-ended generation ability.\n"
            "\n"
            "Small changes in prompt formatting or option presentation can also "
            "change model behavior, so benchmark design matters.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Generation capability\n"
            "\n"
            "Open-ended generation has long been studied in natural language "
            "generation (NLG). Traditional metrics included:\n"
            "\n"
            "- **Fluency:** is the text grammatically natural?\n"
            "- **Coherence:** does the text follow a logical structure?\n"
            "- **Faithfulness:** does generated content preserve the source meaning?\n"
            "- **Relevance:** does the output focus on what matters?\n"
            "\n"
            "Modern foundation models are often already highly fluent, so other "
            "failure modes become more important. Two major categories emphasized "
            "in the chapter are **factual consistency** and **safety**.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Factual consistency\n"
            "\n"
            "A fluent response can still contain unsupported or false information. "
            "For many applications, factual consistency is therefore a critical "
            "evaluation criterion.\n"
            "\n"
            "The chapter separates two settings.\n"
            "\n"
            "### Local factual consistency\n"
            "\n"
            "Evaluate the output against an explicit context.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- A summary should be supported by its source document.\n"
            "- A customer-support answer should match company policy.\n"
            "- A RAG answer should be supported by retrieved passages.\n"
            "\n"
            "If the context says one thing and the response says the opposite, the "
            "response is locally inconsistent even if the response happens to match "
            "some external fact.\n"
            "\n"
            "### Global factual consistency\n"
            "\n"
            "Evaluate the output against open-world knowledge. This is harder because "
            "the system must first determine which external sources are trustworthy.\n"
            "\n"
            "The difficult part is often not comparison—it is identifying what the "
            "facts actually are.\n"
            "\n"
            "[[IMAGE_NEEDED: Local versus global factual consistency | A split "
            "diagram where local factuality compares an answer directly against "
            "provided context, while global factuality first retrieves trusted "
            "external evidence and then verifies the answer | Learner should notice "
            "that global verification adds an evidence-discovery problem]]\n"
            "\n"
            "### Design factuality tests around known hallucination patterns\n"
            "\n"
            "The chapter recommends analyzing outputs to discover where your model "
            "hallucinates most often, then over-representing those failure patterns "
            "in evaluation.\n"
            "\n"
            "Examples from the chapter include questions about niche knowledge and "
            "questions that falsely assume something exists.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Methods for evaluating factual consistency\n"
            "\n"
            "### AI-as-a-judge\n"
            "\n"
            "Given a source context and a generated response, an AI judge can be "
            "asked whether every important claim is supported.\n"
            "\n"
            "### Self-verification\n"
            "\n"
            "A method such as SelfCheckGPT generates multiple responses and looks "
            "for disagreement. If repeated outputs conflict strongly, the original "
            "answer may be unreliable.\n"
            "\n"
            "The tradeoff is cost: generating many extra responses just to evaluate "
            "one answer can be expensive.\n"
            "\n"
            "### Knowledge-augmented verification\n"
            "\n"
            "The chapter describes a search-augmented approach with a sequence like:\n"
            "\n"
            "```text\n"
            "response\n"
            "  -> split into factual statements\n"
            "  -> rewrite statements to be self-contained\n"
            "  -> generate search queries\n"
            "  -> retrieve evidence\n"
            "  -> judge each statement against evidence\n"
            "```\n"
            "\n"
            "This converts global factuality into a set of evidence-backed local "
            "checks.\n"
            "\n"
            "### Textual entailment / natural language inference\n"
            "\n"
            "Given a **premise** (context) and **hypothesis** (claim), classify the "
            "relationship as:\n"
            "\n"
            "- **Entailment:** the claim follows from the context.\n"
            "- **Contradiction:** the claim conflicts with the context.\n"
            "- **Neutral:** the context neither supports nor contradicts the claim.\n"
            "\n"
            "This turns factual-consistency evaluation into a classification task "
            "that can be performed by specialized scorers.\n"
            "\n"
            "[[IMAGE_NEEDED: Search-augmented factuality evaluator | A four-stage "
            "pipeline showing response decomposition, self-contained claims, web or "
            "knowledge search, and claim verification | Learner should notice that "
            "long-form factuality can be reduced to verifying smaller atomic claims]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Safety evaluation\n"
            "\n"
            "Safety is an umbrella covering many types of harmful outputs. Depending "
            "on the application, evaluation may include categories such as:\n"
            "\n"
            "- Inappropriate or explicit language.\n"
            "- Harmful recommendations.\n"
            "- Hate or discriminatory content.\n"
            "- Threats or graphic violence.\n"
            "- Stereotypes.\n"
            "- Bias toward particular ideological or religious viewpoints when "
            "neutrality is required by the product.\n"
            "\n"
            "Possible evaluators include:\n"
            "\n"
            "- General-purpose AI judges.\n"
            "- Provider moderation systems.\n"
            "- Small specialized toxicity or hate-speech classifiers.\n"
            "- Human reviewers.\n"
            "\n"
            "Specialized safety models can be much smaller, faster, and cheaper than "
            "large general-purpose judges.\n"
            "\n"
            "The key principle is not to adopt a generic safety benchmark blindly. "
            "Define the harms that matter for your product and evaluate those risks.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Instruction-following capability\n"
            "\n"
            "A model can understand the domain yet still fail the application by "
            "ignoring instructions.\n"
            "\n"
            "Suppose the model correctly understands tweet sentiment but is told to "
            "output only:\n"
            "\n"
            "```text\n"
            "NEGATIVE\n"
            "POSITIVE\n"
            "NEUTRAL\n"
            "```\n"
            "\n"
            "If it outputs `HAPPY`, the problem is not necessarily sentiment "
            "understanding. It may be instruction following.\n"
            "\n"
            "Instruction following includes much more than JSON formatting. You may "
            "require:\n"
            "\n"
            "- Specific keywords.\n"
            "- Forbidden words.\n"
            "- A fixed language.\n"
            "- A word, sentence, or paragraph limit.\n"
            "- Exact bullet counts.\n"
            "- JSON/YAML or other formats.\n"
            "- Content constraints.\n"
            "- A specific tone or linguistic style.\n"
            "\n"
            "### Automatically verifiable instructions\n"
            "\n"
            "Some instructions can be checked with deterministic code. For example:\n"
            "\n"
            "- Does the output contain the required keyword?\n"
            "- Is it valid JSON?\n"
            "- Does it have exactly three bullet points?\n"
            "- Is it under 100 words?\n"
            "\n"
            "### Subjective instructions\n"
            "\n"
            "Other instructions such as 'write for a young audience' or 'use a "
            "respectful tone' require human or AI judgment.\n"
            "\n"
            "A useful approach is to decompose the instruction into explicit yes/no "
            "criteria, then score how many criteria are satisfied.\n"
            "\n"
            "### Model failure or prompt failure?\n"
            "\n"
            "Instruction-following evaluation has an important ambiguity: poor "
            "performance can be caused by the model or by bad instructions. Your "
            "evaluation process must control prompt quality carefully.\n"
            "\n"
            "The chapter's practical advice is to build your **own** instruction "
            "benchmark using the instructions your product actually needs.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Roleplaying as an instruction-following problem\n"
            "\n"
            "Roleplaying is common in games, companions, interactive stories, and "
            "prompt-engineering workflows.\n"
            "\n"
            "A roleplaying model can be evaluated along at least two dimensions:\n"
            "\n"
            "1. **Style:** does the output sound like the intended role?\n"
            "2. **Knowledge:** does the output stay within what the role would know?\n"
            "\n"
            "The second requirement includes **negative knowledge**: the model "
            "should not reveal knowledge the character is not supposed to have.\n"
            "\n"
            "Some role constraints can be checked heuristically, but AI judges or "
            "human evaluators are often needed for nuanced behavior.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Cost, latency, and scale are part of model quality\n"
            "\n"
            "A model that produces excellent answers but is too slow or too "
            "expensive may still be unusable.\n"
            "\n"
            "### Multi-objective optimization\n"
            "\n"
            "Model selection often involves multiple competing goals. A useful "
            "strategy is to identify **hard requirements** first.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "TTFT must be < 200 ms\n"
            "cost must be < target budget\n"
            "quality must exceed minimum threshold\n"
            "```\n"
            "\n"
            "Remove models that fail hard requirements. Then compare the remaining "
            "models on softer preferences.\n"
            "\n"
            "### Common latency metrics\n"
            "\n"
            "- Time to first token (TTFT).\n"
            "- Time per output token.\n"
            "- Time between tokens.\n"
            "- Total query latency.\n"
            "\n"
            "Latency depends on model behavior, prompt length, generated length, and "
            "sampling configuration.\n"
            "\n"
            "### Cost depends on deployment model\n"
            "\n"
            "For APIs, cost often scales with token usage. For self-hosted systems, "
            "cost is dominated by infrastructure plus engineering and operations.\n"
            "\n"
            "The cost per token of self-hosting can improve with utilization and "
            "scale, so the API-versus-host decision may change as traffic grows.\n"
            "\n"
            "[[IMAGE_NEEDED: Quality-cost-latency tradeoff | A three-axis conceptual "
            "diagram or Pareto frontier where some models are higher quality but "
            "slower/more expensive and others are cheaper/faster with lower quality | "
            "Learner should notice that model selection is a multi-objective problem]]\n"
            "\n"
            "{{exercise:M04.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 11. A practical model-selection workflow\n"
            "\n"
            "The goal is not to find the universally best model. It is to find the "
            "best model **for your application**.\n"
            "\n"
            "The chapter distinguishes **hard attributes** and **soft attributes**.\n"
            "\n"
            "### Hard attributes\n"
            "\n"
            "Attributes that are impossible or impractical for you to change, such as:\n"
            "\n"
            "- License restrictions.\n"
            "- Privacy constraints.\n"
            "- Model availability.\n"
            "- Deployment size constraints.\n"
            "- Provider restrictions.\n"
            "\n"
            "### Soft attributes\n"
            "\n"
            "Attributes you may be able to improve through prompting, retrieval, "
            "finetuning, optimization, or system design, such as:\n"
            "\n"
            "- Accuracy.\n"
            "- Factual consistency.\n"
            "- Toxicity.\n"
            "- Sometimes latency, if you control the model stack.\n"
            "\n"
            "Whether an attribute is hard or soft depends on your situation. If "
            "you control model serving, latency may be optimizable. If an external "
            "provider controls serving, latency may be effectively hard.\n"
            "\n"
            "### Four-step workflow\n"
            "\n"
            "1. Filter models that violate hard requirements.\n"
            "2. Use public information and benchmarks to narrow the field.\n"
            "3. Run your own evaluation pipeline on the most promising candidates.\n"
            "4. Monitor the selected model in production and keep collecting evidence.\n"
            "\n"
            "These steps are iterative. New evidence can cause you to revisit an "
            "earlier decision.\n"
            "\n"
            "[[IMAGE_NEEDED: Model-selection funnel | A four-stage funnel from all "
            "models -> hard-attribute filtering -> public benchmark shortlist -> "
            "private evaluation -> production monitoring | Learner should notice "
            "that public benchmarks narrow candidates but do not make the final choice]]\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Open source, open weight, and model licenses\n"
            "\n"
            "Model openness exists on a spectrum.\n"
            "\n"
            "- **Open weight:** model weights are available, but training data may "
            "not be public.\n"
            "- **Open model:** the chapter uses this idea for models where data is "
            "also available more openly.\n"
            "- **Commercial/proprietary model:** access is primarily controlled by "
            "the provider, often through an API.\n"
            "\n"
            "Model licenses are critical. Before adopting a model, check questions "
            "such as:\n"
            "\n"
            "- Is commercial use allowed?\n"
            "- Are there usage-scale restrictions?\n"
            "- Can outputs be used to train or improve other models?\n"
            "- Are redistribution, finetuning, or derivative models allowed?\n"
            "\n"
            "Do not assume 'weights available' means unrestricted use.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Model APIs versus self-hosting\n"
            "\n"
            "An inference service hosts a model, accepts requests, runs inference, "
            "and returns responses. A model API is the interface through which an "
            "application accesses that service.\n"
            "\n"
            "The same model can sometimes be available through multiple providers, "
            "with different pricing, features, optimization, and performance.\n"
            "\n"
            "The chapter proposes seven axes for deciding whether to use an API or "
            "host a model yourself:\n"
            "\n"
            "1. Data privacy.\n"
            "2. Data lineage and copyright.\n"
            "3. Performance.\n"
            "4. Functionality.\n"
            "5. Cost.\n"
            "6. Control/access/transparency.\n"
            "7. On-device deployment.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Privacy, data lineage, and legal constraints\n"
            "\n"
            "### Data privacy\n"
            "\n"
            "An external API requires sending data to an external service unless "
            "the service is deployed inside your controlled environment. For some "
            "organizations, that alone makes certain APIs unacceptable.\n"
            "\n"
            "Questions include:\n"
            "\n"
            "- Where is data processed?\n"
            "- Is data retained?\n"
            "- Can provider policy change?\n"
            "- Could sensitive data appear in future training?\n"
            "- Are there data-residency rules?\n"
            "\n"
            "### Data lineage and copyright\n"
            "\n"
            "Teams may also need to understand where a model's training data came "
            "from. This matters for auditing, IP risk, and regulatory requirements.\n"
            "\n"
            "Open data can improve inspectability, but enormous datasets are still "
            "hard to audit completely. Commercial contracts can sometimes shift or "
            "clarify parts of legal responsibility, but this is an organizational "
            "and legal decision, not only a technical one.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Functionality, control, and operational tradeoffs\n"
            "\n"
            "### Functionality\n"
            "\n"
            "An application may need more than raw text generation:\n"
            "\n"
            "- Scalable serving.\n"
            "- Function/tool calling.\n"
            "- Structured outputs.\n"
            "- Guardrails.\n"
            "- Log probabilities.\n"
            "- Finetuning support.\n"
            "\n"
            "API providers may give many capabilities out of the box, saving "
            "engineering time. But you are limited to what the provider exposes.\n"
            "\n"
            "Open models give more access to weights, logprobs, internals, "
            "finetuning, quantization, and serving choices, but your team becomes "
            "responsible for more of the engineering.\n"
            "\n"
            "### API cost versus engineering cost\n"
            "\n"
            "APIs can become expensive at scale. Self-hosting can reduce marginal "
            "usage cost but introduces engineering, operations, monitoring, "
            "optimization, and reliability costs.\n"
            "\n"
            "The cheapest token price is not necessarily the cheapest system.\n"
            "\n"
            "### Control and transparency\n"
            "\n"
            "External providers can impose rate limits, change models, change "
            "behavior, change terms, or discontinue support. With open/self-hosted "
            "models, you gain more control and can freeze versions, but you also "
            "own more operational responsibility.\n"
            "\n"
            "### On-device deployment\n"
            "\n"
            "If a model must run locally without external network access, a remote "
            "API is not sufficient. On-device deployment favors models that can be "
            "run and optimized locally.\n"
            "\n"
            "[[IMAGE_NEEDED: API versus self-hosted decision matrix | A two-column "
            "matrix comparing external APIs and self-hosted models across privacy, "
            "performance, functionality, cost, control, finetuning, and on-device "
            "deployment | Learner should notice that neither option is universally "
            "better; the right choice depends on application constraints]]\n"
            "\n"
            "---\n"
            "\n"

            "## 16. How to use public benchmarks correctly\n"
            "\n"
            "Thousands of benchmarks exist. Evaluation harnesses make it easier to "
            "run many of them, but the existence of a benchmark does not mean it is "
            "relevant to your application.\n"
            "\n"
            "Public benchmarks are most useful as a **filtering tool**. They help "
            "remove clearly weak candidates and identify models worth deeper testing.\n"
            "\n"
            "When reviewing a benchmark, ask:\n"
            "\n"
            "- What capability does it measure?\n"
            "- Does that capability matter to my product?\n"
            "- Is the benchmark saturated?\n"
            "- Is the benchmark reliable and well constructed?\n"
            "- Is the benchmark likely contaminated?\n"
            "- Does the task format resemble my application's actual tasks?\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Public leaderboards and benchmark aggregation\n"
            "\n"
            "A leaderboard combines several benchmark scores into a ranking. The "
            "hard part is deciding **which** benchmarks to include and **how** to "
            "combine them.\n"
            "\n"
            "### Coverage is always incomplete\n"
            "\n"
            "Running benchmarks costs compute, so leaderboards usually include "
            "only a subset of possible capabilities. A leaderboard may emphasize "
            "reasoning and knowledge while omitting coding, tool use, retrieval, "
            "summarization, safety, or another capability you need.\n"
            "\n"
            "### Benchmark correlation matters\n"
            "\n"
            "If two benchmarks measure nearly the same capability and are strongly "
            "correlated, including both can give that capability too much weight.\n"
            "\n"
            "### Aggregation changes the ranking\n"
            "\n"
            "A simple average gives every benchmark equal weight even when the "
            "benchmarks differ in importance, difficulty, scale, or units.\n"
            "\n"
            "Other leaderboards may aggregate using win rates or other methods. "
            "Different aggregation choices can produce different rankings.\n"
            "\n"
            "### Create a private leaderboard for your application\n"
            "\n"
            "For a real product, your model-selection process is effectively a "
            "private leaderboard whose criteria and weights reflect your own needs.\n"
            "\n"
            "Use public data to shortlist candidates, then test them using your own "
            "prompts, datasets, and metrics.\n"
            "\n"
            "[[IMAGE_NEEDED: Public versus private leaderboard | A diagram showing "
            "public benchmarks feeding a coarse shortlist, then application-specific "
            "benchmarks, weights, cost, and latency producing a private model ranking | "
            "Learner should notice that public rankings are only an early filter]]\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Benchmark contamination\n"
            "\n"
            "**Data contamination** occurs when evaluation data also appears in the "
            "training data. It is also described as leakage or training on the test set.\n"
            "\n"
            "A model can then score highly because it remembers benchmark examples "
            "rather than because it generalizes to the underlying capability.\n"
            "\n"
            "### How contamination happens\n"
            "\n"
            "- Public benchmark data can be scraped from the web into training data.\n"
            "- Training and evaluation data can originate from the same source.\n"
            "- Developers can intentionally train on benchmark data after model selection.\n"
            "\n"
            "### How contamination can be detected\n"
            "\n"
            "**N-gram overlap**  \n"
            "Look for long sequences shared between benchmark examples and training data.\n"
            "\n"
            "**Perplexity**  \n"
            "Unusually low perplexity on evaluation text can suggest the model has "
            "seen or memorized that text before.\n"
            "\n"
            "N-gram comparison is stronger when training data is available but can "
            "be expensive. Perplexity is cheaper but less definitive.\n"
            "\n"
            "A trustworthy benchmark should ideally keep a private holdout set or "
            "otherwise make contamination analysis possible.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Evaluation pipeline step 1: evaluate every component\n"
            "\n"
            "Real AI systems contain multiple stages. If you evaluate only the final "
            "answer, you may know that the system failed but not **where** it failed.\n"
            "\n"
            "Suppose a system extracts a current employer from a resume PDF:\n"
            "\n"
            "```text\n"
            "PDF\n"
            " -> text extraction\n"
            " -> employer extraction\n"
            " -> final answer\n"
            "```\n"
            "\n"
            "A wrong employer could be caused by bad PDF extraction or bad entity "
            "extraction. Evaluate each stage independently.\n"
            "\n"
            "### Turn-based versus task-based evaluation\n"
            "\n"
            "- **Turn-based evaluation:** assess each system response or interaction turn.\n"
            "- **Task-based evaluation:** assess whether the user ultimately accomplished "
            "the goal and how efficiently.\n"
            "\n"
            "Task-based evaluation is often closer to what users care about. A "
            "debugging assistant that solves a problem in two turns is meaningfully "
            "different from one that needs twenty turns.\n"
            "\n"
            "[[IMAGE_NEEDED: Component, turn, and task evaluation | A layered "
            "diagram showing intermediate component metrics at the bottom, turn-level "
            "quality in the middle, and end-to-end task success at the top | Learner "
            "should notice that a reliable pipeline measures both local failures and "
            "the final user outcome]]\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Evaluation pipeline step 2: create a clear guideline\n"
            "\n"
            "The chapter calls the evaluation guideline one of the most important "
            "parts of the pipeline. Ambiguous guidelines produce ambiguous scores.\n"
            "\n"
            "Define both:\n"
            "\n"
            "- What the application **should** do.\n"
            "- What the application **should not** do.\n"
            "\n"
            "For example, a support bot may need a policy for out-of-scope questions.\n"
            "\n"
            "### Define criteria\n"
            "\n"
            "A correct answer is not always a good answer. A response can be "
            "factually correct but rude, unhelpful, irrelevant, or unsafe.\n"
            "\n"
            "A customer-support system might use criteria such as:\n"
            "\n"
            "- Relevance.\n"
            "- Factual consistency.\n"
            "- Safety.\n"
            "\n"
            "### Create scoring rubrics with examples\n"
            "\n"
            "For each criterion, choose a scoring system and define what each score "
            "means. Examples help evaluators interpret the rubric consistently.\n"
            "\n"
            "Possible scales include:\n"
            "\n"
            "- Binary: 0/1.\n"
            "- Three-way: contradiction / neutral / entailment.\n"
            "- Discrete numerical: 1–5.\n"
            "\n"
            "Validate the rubric with humans. If people interpret it differently, "
            "the rubric needs refinement.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Tie evaluation metrics to business metrics\n"
            "\n"
            "A model metric matters only if it helps answer a product or business question.\n"
            "\n"
            "Instead of saying:\n"
            "\n"
            "```text\n"
            "Factual consistency = 90%\n"
            "```\n"
            "\n"
            "try to understand what that enables:\n"
            "\n"
            "```text\n"
            "90% factual consistency\n"
            " -> allows automation of X% of support requests\n"
            " -> reduces response time by Y\n"
            " -> changes cost/customer satisfaction by Z\n"
            "```\n"
            "\n"
            "This mapping helps decide whether improving a metric is worth the effort.\n"
            "\n"
            "### Usefulness threshold\n"
            "\n"
            "Define the minimum quality at which the system becomes useful. Below "
            "that threshold, the application should not be deployed for that use case.\n"
            "\n"
            "Be careful when choosing business metrics. Engagement or time-spent "
            "metrics can create incentives that are not always aligned with user "
            "well-being or product quality.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Evaluation pipeline step 3: choose methods and data\n"
            "\n"
            "Different criteria can use different evaluators.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "toxicity -> specialized classifier\n"
            "relevance -> semantic similarity\n"
            "factual consistency -> AI judge\n"
            "structured format -> deterministic validator\n"
            "task success -> end-to-end functional metric\n"
            "```\n"
            "\n"
            "You can also combine methods for the **same** criterion. A cheap model "
            "might evaluate 100% of traffic while an expensive judge or human expert "
            "evaluates a smaller sample.\n"
            "\n"
            "### Use logprobs when available\n"
            "\n"
            "For classification, log probabilities can show whether the model is "
            "confident or uncertain among allowed classes. They can also support "
            "perplexity-based measurements.\n"
            "\n"
            "### Keep humans in the loop when needed\n"
            "\n"
            "Automatic metrics are valuable, but open-ended tasks can still require "
            "expert review. Human evaluation can act as a North Star signal and be "
            "used on sampled production outputs.\n"
            "\n"
            "### Experimentation and production differ\n"
            "\n"
            "Offline experiments may have curated reference answers. Production may "
            "not. But production provides real user feedback and real traffic patterns.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Build representative evaluation datasets\n"
            "\n"
            "Use annotated examples to evaluate each component and criterion. Real "
            "production examples are especially valuable when available.\n"
            "\n"
            "### Slice your evaluation data\n"
            "\n"
            "Aggregate scores can hide serious failures. Slice data by meaningful "
            "attributes such as:\n"
            "\n"
            "- Free versus paid users.\n"
            "- Mobile versus web traffic.\n"
            "- Input length.\n"
            "- Topic or domain.\n"
            "- Known difficult cases.\n"
            "- Typos or noisy input.\n"
            "- Out-of-scope requests.\n"
            "\n"
            "Slicing helps uncover bias, debug failures, and identify areas for improvement.\n"
            "\n"
            "### Simpson's paradox\n"
            "\n"
            "Aggregated results can tell a different story from every subgroup. One "
            "model may appear better overall even while another model is better in "
            "each relevant slice because the models were evaluated on different slice "
            "distributions.\n"
            "\n"
            "[[IMAGE_NEEDED: Simpson's paradox in model evaluation | A two-group "
            "table where Model A performs better than Model B inside each subgroup "
            "but Model B has a higher aggregated score due to different group sizes | "
            "Learner should notice why aggregate metrics must be inspected alongside "
            "slice-level results]]\n"
            "\n"
            "A practical principle from the chapter is:\n"
            "\n"
            "> **If you care about something, put a test set on it.**\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Is your evaluation set large enough?\n"
            "\n"
            "An evaluation set must be large enough to produce stable conclusions "
            "but small enough to run affordably.\n"
            "\n"
            "### Bootstrap analysis\n"
            "\n"
            "One practical reliability check is bootstrapping:\n"
            "\n"
            "1. Sample from your evaluation set **with replacement**.\n"
            "2. Re-evaluate the system on this bootstrapped set.\n"
            "3. Repeat many times.\n"
            "4. Inspect how much the score changes.\n"
            "\n"
            "If scores swing wildly, the evaluation set may be too small or too noisy.\n"
            "\n"
            "### Detecting small improvements requires more samples\n"
            "\n"
            "Large score differences need fewer examples to detect reliably than "
            "small score differences. The chapter provides a rough heuristic showing "
            "that shrinking the effect size by about 3x may require roughly 10x more "
            "examples for similar confidence.\n"
            "\n"
            "The general lesson is more important than memorizing exact counts:\n"
            "\n"
            "**A 1% claimed improvement needs much stronger statistical evidence "
            "than a 30% improvement.**\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Evaluate your evaluation pipeline\n"
            "\n"
            "Your evaluation system can itself be wrong, noisy, expensive, or misleading.\n"
            "\n"
            "Ask:\n"
            "\n"
            "### Are the signals valid?\n"
            "\n"
            "- Do better responses actually receive better scores?\n"
            "- Do improved evaluation metrics lead to improved product outcomes?\n"
            "\n"
            "### Is the pipeline reliable?\n"
            "\n"
            "- Does running the same pipeline twice produce similar conclusions?\n"
            "- How much variance appears across different evaluation samples?\n"
            "\n"
            "For AI judges, keep configurations stable and reduce unnecessary "
            "sampling variation.\n"
            "\n"
            "### Are metrics redundant?\n"
            "\n"
            "If two metrics are nearly perfectly correlated, one may be redundant. "
            "If they are unexpectedly uncorrelated, that may reveal either an "
            "interesting model property or a flawed metric.\n"
            "\n"
            "### What does evaluation cost?\n"
            "\n"
            "Evaluation can add significant latency and monetary cost. That cost "
            "must be designed into the system rather than ignored.\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Iterate without losing comparability\n"
            "\n"
            "Evaluation criteria will evolve as the product and user behavior change. "
            "You may need to update datasets, rubrics, judges, or scoring methods.\n"
            "\n"
            "But if the evaluation process changes constantly without versioning, "
            "scores over time become impossible to compare.\n"
            "\n"
            "Track everything that can affect evaluation, including:\n"
            "\n"
            "- Evaluation dataset version.\n"
            "- Data slices.\n"
            "- Rubric version.\n"
            "- Judge model/version.\n"
            "- Judge prompt.\n"
            "- Judge sampling configuration.\n"
            "- Model under test.\n"
            "- Application prompt/version.\n"
            "- Retrieval or tool configuration when relevant.\n"
            "\n"
            "Evaluation should evolve—but in a controlled, observable way.\n"
            "\n"
            "{{exercise:M04.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> The model with the highest public leaderboard rank is automatically "
            "the best model for my application.\n"
            "\n"
            "**Why this is wrong:** public leaderboards represent their chosen "
            "benchmarks and aggregation rules, not your exact task, traffic, cost "
            "constraints, or failure modes.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Functional correctness is enough for every coding application.\n"
            "\n"
            "**Why this is wrong:** a solution can be correct yet too slow, too "
            "memory-intensive, insecure, or impossible to maintain.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> If an answer is globally true, it is locally faithful to the context.\n"
            "\n"
            "**Why this is wrong:** local factual consistency asks whether the "
            "provided context supports the answer, not whether the statement is true "
            "somewhere else.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> A model API is always cheaper than self-hosting.\n"
            "\n"
            "**Why this is wrong:** the tradeoff changes with scale, utilization, "
            "engineering cost, infrastructure, and operational requirements.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> Public benchmark results are trustworthy because benchmark answers "
            "are objective.\n"
            "\n"
            "**Why this is wrong:** benchmark design, saturation, relevance, "
            "aggregation, prompt sensitivity, and training-data contamination can "
            "all distort what a score means.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> If my overall metric improves, every user group benefits.\n"
            "\n"
            "**Why this is wrong:** aggregate metrics can hide slice-specific "
            "regressions and even Simpson's paradox.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Evaluation-driven development | Defining evaluation criteria before building the application. |\n"
            "| Domain-specific capability | Ability required for a particular field or task, such as coding or legal reasoning. |\n"
            "| Generation capability | Quality properties of open-ended outputs such as faithfulness or relevance. |\n"
            "| Local factual consistency | Whether an output is supported by explicitly provided context. |\n"
            "| Global factual consistency | Whether an output is supported by trustworthy open-world knowledge. |\n"
            "| Textual entailment | Classification of a claim as entailed, contradicted, or neutral relative to a premise. |\n"
            "| Instruction following | Ability to obey requested format, content, style, language, or behavioral constraints. |\n"
            "| Hard attribute | Model property that is impossible or impractical for your team to change. |\n"
            "| Soft attribute | Model property that may be improved through adaptation or optimization. |\n"
            "| TTFT | Time to first token. |\n"
            "| Pareto optimization | Multi-objective optimization where improving one objective may worsen another. |\n"
            "| Inference service | System that hosts a model, executes requests, and returns outputs. |\n"
            "| Open weight model | Model whose weights are available even if training data is not fully public. |\n"
            "| Model API | Interface for accessing an inference or other model service. |\n"
            "| Data lineage | Information about where model data originated and how it was processed. |\n"
            "| Evaluation harness | Tooling for running models against multiple benchmarks. |\n"
            "| Benchmark saturation | Condition where many models approach the benchmark's ceiling. |\n"
            "| Benchmark correlation | Degree to which two benchmark scores move together across models. |\n"
            "| Data contamination | Evaluation examples appearing in model training data. |\n"
            "| Turn-based evaluation | Evaluation of individual interaction turns. |\n"
            "| Task-based evaluation | Evaluation of whether the complete user goal is achieved. |\n"
            "| Scoring rubric | Explicit rules describing what each evaluation score means. |\n"
            "| Usefulness threshold | Minimum evaluation level required for an application to be useful. |\n"
            "| Data slicing | Evaluating performance separately on meaningful subsets of data. |\n"
            "| Simpson's paradox | Aggregate results reversing the pattern seen within subgroups. |\n"
            "| Bootstrap | Resampling with replacement to estimate score variability or reliability. |\n"
            "| Experiment tracking | Recording evaluation data, prompts, rubrics, models, and configurations so results remain reproducible. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What does evaluation-driven development mean?\n"
            "2. What four broad evaluation buckets does the chapter introduce?\n"
            "3. Why can a functionally correct SQL query still be unusable?\n"
            "4. Why are MCQs easy to evaluate but incomplete for generative capability?\n"
            "5. What is the difference between local and global factual consistency?\n"
            "6. How does search-augmented factuality verification work?\n"
            "7. What are entailment, contradiction, and neutral?\n"
            "8. Why should safety evaluation be application-specific?\n"
            "9. How can deterministic code evaluate instruction following?\n"
            "10. Why can poor instruction following be confused with poor domain capability?\n"
            "11. What role does negative knowledge play in roleplaying evaluation?\n"
            "12. What are TTFT and total query latency?\n"
            "13. What is the difference between a hard and soft model attribute?\n"
            "14. What are the four high-level stages of model selection?\n"
            "15. Why does a model license matter even if weights are downloadable?\n"
            "16. Name the seven axes for API versus self-hosting decisions.\n"
            "17. Why might self-hosting become more attractive at scale?\n"
            "18. Why might an API still be preferable despite higher token cost?\n"
            "19. Why should public benchmarks be treated as filters rather than final selectors?\n"
            "20. Why is benchmark correlation relevant when building a leaderboard?\n"
            "21. What is data contamination and why does it inflate benchmark scores?\n"
            "22. How can n-gram overlap and perplexity help detect contamination?\n"
            "23. Why should intermediate components be evaluated independently?\n"
            "24. What is the difference between turn-based and task-based evaluation?\n"
            "25. Why are scoring rubrics central to evaluation reliability?\n"
            "26. How should model metrics connect to business metrics?\n"
            "27. Why should you slice evaluation data?\n"
            "28. What does Simpson's paradox warn you about?\n"
            "29. How can bootstrapping reveal that an evaluation set is too small?\n"
            "30. Why must the evaluation pipeline itself be evaluated?\n"
            "31. Which variables should be versioned for reproducible AI-judge evaluation?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**The right model is not the one with the most impressive generic "
            "score. It is the model that meets your application's hard constraints "
            "and usefulness threshold when measured by an evaluation pipeline built "
            "around your real users, tasks, risks, cost, latency, and business goals.**\n"
        ),

        "estimated_minutes": 270,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "evaluation-driven-development", "title": "Evaluation-driven development", "order": 1},
            {"id": "evaluation-criteria", "title": "Application-specific evaluation criteria", "order": 2},
            {"id": "domain-capability", "title": "Domain-specific capability", "order": 3},
            {"id": "generation-capability", "title": "Generation capability", "order": 4},
            {"id": "factual-consistency", "title": "Factual consistency", "order": 5},
            {"id": "factuality-methods", "title": "Factuality evaluation methods", "order": 6},
            {"id": "safety", "title": "Safety evaluation", "order": 7},
            {"id": "instruction-following", "title": "Instruction-following capability", "order": 8},
            {"id": "roleplaying", "title": "Roleplaying evaluation", "order": 9},
            {"id": "cost-latency", "title": "Cost, latency, and scale", "order": 10},
            {"id": "model-selection-workflow", "title": "Model-selection workflow", "order": 11},
            {"id": "open-model-terminology", "title": "Open models and licenses", "order": 12},
            {"id": "api-vs-self-host", "title": "Model APIs versus self-hosting", "order": 13},
            {"id": "privacy-lineage", "title": "Privacy and data lineage", "order": 14},
            {"id": "functionality-control", "title": "Functionality and control", "order": 15},
            {"id": "public-benchmarks", "title": "Using public benchmarks", "order": 16},
            {"id": "leaderboards", "title": "Public leaderboards", "order": 17},
            {"id": "benchmark-contamination", "title": "Benchmark contamination", "order": 18},
            {"id": "pipeline-components", "title": "Evaluate every component", "order": 19},
            {"id": "evaluation-guideline", "title": "Create an evaluation guideline", "order": 20},
            {"id": "business-metrics", "title": "Tie evaluation to business metrics", "order": 21},
            {"id": "methods-and-data", "title": "Choose evaluation methods and data", "order": 22},
            {"id": "evaluation-data", "title": "Build representative evaluation datasets", "order": 23},
            {"id": "sample-size-reliability", "title": "Evaluation-set reliability", "order": 24},
            {"id": "evaluate-evaluation", "title": "Evaluate the evaluation pipeline", "order": 25},
            {"id": "iterate-track", "title": "Iterate and track changes", "order": 26},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M04.L01.EX01",

            "title": "Create a Model-Selection Scorecard",

            "lesson_code": "M04.L01",

            "section_id": "cost-latency",

            "placement": "after_section",

            "description": (
                "Practice turning product requirements into concrete model-selection "
                "criteria instead of selecting a model from benchmark reputation alone."
            ),

            "instructions": (
                "Choose one application: customer-support RAG assistant, coding agent, "
                "document summarizer, education tutor, or your own AI product.\n\n"
                "1. Define two required domain capabilities.\n"
                "2. Define two generation-quality criteria.\n"
                "3. Define two instruction-following constraints.\n"
                "4. Define one hard latency requirement and one ideal latency target.\n"
                "5. Define one hard cost requirement and one ideal cost target.\n"
                "6. Identify three hard model attributes.\n"
                "7. Identify three soft attributes you might improve later.\n"
                "8. State what public benchmark information you would use only for "
                "shortlisting.\n"
                "9. Define the private evaluation that would make the final decision.\n"
                "10. Explain one quality-versus-cost tradeoff you are willing to make "
                "and one you are not willing to make."
            ),

            "expected_output": (
                "A model-selection scorecard or table with criteria, metrics, hard "
                "requirements, ideal targets, and a short explanation of the final "
                "selection process."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "evaluation-criteria",
                "model-selection",
                "cost-latency-tradeoffs",
                "hard-soft-attributes",
                "decision-reasoning",
            ],
        },

        {
            "id": "M04.L01.EX02",

            "title": "Design a Production Evaluation Pipeline",

            "lesson_code": "M04.L01",

            "section_id": "iterate-track",

            "placement": "after_section",

            "description": (
                "Design an evaluation pipeline that can guide development and remain "
                "useful after the AI application reaches production."
            ),

            "instructions": (
                "Design an evaluation pipeline for a RAG customer-support assistant.\n\n"
                "1. Draw the system components and define one metric for each component.\n"
                "2. Define one turn-level metric and one task-level success metric.\n"
                "3. Define three response-quality criteria and a scoring rubric for each.\n"
                "4. Define an absolute usefulness threshold.\n"
                "5. Map at least one evaluation metric to a business outcome.\n"
                "6. Choose which metrics should run on 100% of traffic and which should "
                "run only on a sampled subset.\n"
                "7. Define at least four evaluation-data slices.\n"
                "8. Include one difficult-case set and one out-of-scope set.\n"
                "9. Describe how you would use bootstrap resampling to check whether "
                "your evaluation set is stable enough.\n"
                "10. List all experiment/evaluation variables you would version.\n"
                "11. Explain how human reviewers and user feedback would be included "
                "after deployment.\n"
                "12. State how you would tell whether the evaluation pipeline itself "
                "is producing trustworthy signals."
            ),

            "expected_output": (
                "A complete production-minded evaluation design including component, "
                "turn, task, quality, business, slice, statistical-reliability, human, "
                "and versioning considerations."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "evaluation-pipeline-design",
                "rag-evaluation",
                "rubric-design",
                "data-slicing",
                "bootstrap-reliability",
                "production-monitoring",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M04.L01.QZ01",

        "title": "Evaluate AI Systems — Knowledge Check",

        "lesson_code": "M04.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M04.L01.Q01",
                "section_id": "evaluation-driven-development",
                "question": "What is evaluation-driven development?",
                "options": [
                    "Choosing metrics only after deployment",
                    "Defining evaluation criteria before building the application",
                    "Using only public leaderboards",
                    "Training a model before identifying the use case",
                ],
                "correct": 1,
                "explanation": (
                    "Evaluation-driven development begins by defining what success "
                    "and failure mean before significant implementation."
                ),
            },
            {
                "id": "M04.L01.Q02",
                "section_id": "domain-capability",
                "question": (
                    "A generated SQL query returns the correct result but takes "
                    "100 times longer than an efficient solution. What does this show?"
                ),
                "options": [
                    "Functional correctness may be necessary but insufficient",
                    "The query is automatically unusable in every application",
                    "Latency never matters for model evaluation",
                    "Only lexical similarity should be measured",
                ],
                "correct": 0,
                "explanation": (
                    "The output can be correct yet fail efficiency requirements, so "
                    "runtime or resource usage may need separate evaluation."
                ),
            },
            {
                "id": "M04.L01.Q03",
                "section_id": "factual-consistency",
                "question": (
                    "What is local factual consistency?"
                ),
                "options": [
                    "Whether a statement is supported by the provided context",
                    "Whether a statement appears frequently on the internet",
                    "Whether the model agrees with itself",
                    "Whether the answer is fluent",
                ],
                "correct": 0,
                "explanation": (
                    "Local factuality is judged against explicit context supplied "
                    "to the system."
                ),
            },
            {
                "id": "M04.L01.Q04",
                "section_id": "factuality-methods",
                "question": (
                    "Which sequence best describes search-augmented factuality verification?"
                ),
                "options": [
                    "Split claims -> generate search queries -> retrieve evidence -> verify claims",
                    "Increase temperature -> sample once -> accept output",
                    "Translate output -> shorten output -> rank by length",
                    "Fine-tune tokenizer -> measure BLEU -> stop",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter describes decomposing long responses into claims, "
                    "retrieving evidence, and verifying each claim against that evidence."
                ),
            },
            {
                "id": "M04.L01.Q05",
                "section_id": "instruction-following",
                "question": (
                    "A sentiment model understands a tweet but outputs HAPPY when "
                    "the allowed labels are POSITIVE, NEGATIVE, or NEUTRAL. What "
                    "capability is most obviously failing?"
                ),
                "options": [
                    "Instruction-following capability",
                    "GPU memory",
                    "Domain knowledge of sentiment",
                    "Benchmark contamination",
                ],
                "correct": 0,
                "explanation": (
                    "The model appears to understand the sentiment but fails to obey "
                    "the required output-label constraint."
                ),
            },
            {
                "id": "M04.L01.Q06",
                "section_id": "cost-latency",
                "question": (
                    "What is a good first step when latency is a non-negotiable "
                    "product requirement?"
                ),
                "options": [
                    "Filter out models that fail the latency requirement",
                    "Ignore latency until after launch",
                    "Always choose the biggest model",
                    "Rank only by benchmark accuracy",
                ],
                "correct": 0,
                "explanation": (
                    "Hard constraints should remove infeasible models before softer "
                    "tradeoffs are considered."
                ),
            },
            {
                "id": "M04.L01.Q07",
                "section_id": "model-selection-workflow",
                "question": (
                    "Which is the best example of a hard model attribute?"
                ),
                "options": [
                    "A license that forbids your intended commercial use",
                    "A prompt that could perhaps be improved",
                    "A small factuality regression that might respond to RAG",
                    "A formatting error that can be fixed with validation",
                ],
                "correct": 0,
                "explanation": (
                    "A license restriction can make a model unusable regardless of "
                    "prompting or adaptation quality."
                ),
            },
            {
                "id": "M04.L01.Q08",
                "section_id": "api-vs-self-host",
                "question": (
                    "Why can the same API-versus-self-hosting decision change as "
                    "an application grows?"
                ),
                "options": [
                    "Traffic scale can change the relative importance of API cost, "
                    "utilization, and engineering cost",
                    "Models stop using tokens at high scale",
                    "Licenses disappear after deployment",
                    "Self-hosting has no fixed infrastructure cost",
                ],
                "correct": 0,
                "explanation": (
                    "The economic and operational tradeoff depends on usage, "
                    "utilization, staffing, and infrastructure."
                ),
            },
            {
                "id": "M04.L01.Q09",
                "section_id": "leaderboards",
                "question": (
                    "Why should strongly correlated benchmarks be treated carefully "
                    "when building a leaderboard?"
                ),
                "options": [
                    "They may overweight essentially the same capability",
                    "Correlation proves both benchmarks are invalid",
                    "Correlated benchmarks cannot be automated",
                    "Correlation always means data contamination",
                ],
                "correct": 0,
                "explanation": (
                    "If several benchmarks measure nearly the same thing, combining "
                    "them equally can unintentionally give that capability extra weight."
                ),
            },
            {
                "id": "M04.L01.Q10",
                "section_id": "benchmark-contamination",
                "question": "What is benchmark contamination?",
                "options": [
                    "Evaluation examples appearing in the model's training data",
                    "A benchmark containing too many questions",
                    "A benchmark using multiple-choice questions",
                    "A model producing unsafe text",
                ],
                "correct": 0,
                "explanation": (
                    "Training on evaluation examples can inflate benchmark scores "
                    "because the model may memorize the test data."
                ),
            },
            {
                "id": "M04.L01.Q11",
                "section_id": "pipeline-components",
                "question": (
                    "Why evaluate intermediate components separately?"
                ),
                "options": [
                    "To identify where an end-to-end failure originates",
                    "To avoid evaluating the final user outcome",
                    "Because final answers are never useful",
                    "To make every metric identical",
                ],
                "correct": 0,
                "explanation": (
                    "Component-level evaluation helps isolate which stage caused "
                    "an end-to-end failure."
                ),
            },
            {
                "id": "M04.L01.Q12",
                "section_id": "business-metrics",
                "question": "What is a usefulness threshold?",
                "options": [
                    "The minimum quality at which the application becomes useful",
                    "The maximum number of benchmarks a model can run",
                    "The minimum GPU memory for all AI systems",
                    "A public leaderboard rank",
                ],
                "correct": 0,
                "explanation": (
                    "A usefulness threshold converts an abstract evaluation score "
                    "into a deployment or product-readiness requirement."
                ),
            },
            {
                "id": "M04.L01.Q13",
                "section_id": "evaluation-data",
                "question": (
                    "Why should evaluation data be sliced into meaningful subgroups?"
                ),
                "options": [
                    "Aggregate scores can hide subgroup failures and biases",
                    "Slicing guarantees higher scores",
                    "Slicing removes the need for production data",
                    "Every slice must contain the same number of examples",
                ],
                "correct": 0,
                "explanation": (
                    "Slice-level analysis helps reveal failures that disappear in "
                    "overall averages."
                ),
            },
            {
                "id": "M04.L01.Q14",
                "section_id": "sample-size-reliability",
                "question": (
                    "If bootstrap evaluations of the same 100-example dataset vary "
                    "from 70% to 90%, what is the main concern?"
                ),
                "options": [
                    "The evaluation estimate is unstable and may need more or better data",
                    "The model is necessarily overfitting",
                    "Bootstrapping cannot be used for evaluation",
                    "The score should simply be averaged and ignored",
                ],
                "correct": 0,
                "explanation": (
                    "Large bootstrap variance suggests that the current sample does "
                    "not provide a stable estimate of performance."
                ),
            },
            {
                "id": "M04.L01.Q15",
                "section_id": "evaluate-evaluation",
                "question": (
                    "Which question best checks whether an evaluation metric is valid?"
                ),
                "options": [
                    "Do responses humans consider better actually receive higher scores?",
                    "Does the metric have a colorful dashboard?",
                    "Is the metric used by the largest company?",
                    "Can the metric be computed without data?",
                ],
                "correct": 0,
                "explanation": (
                    "A metric should produce signals that align with true quality "
                    "and ultimately with the product outcomes you care about."
                ),
            },
            {
                "id": "M04.L01.Q16",
                "section_id": "iterate-track",
                "type": "open",
                "question": (
                    "You replace the model, change the prompt, update the evaluation "
                    "rubric, and switch AI-judge models at the same time. The score "
                    "improves by 8%. Explain why this result is difficult to interpret "
                    "and describe how experiment tracking should be redesigned."
                ),
            },
        ],

        "passing_score": 70,
    },
}
