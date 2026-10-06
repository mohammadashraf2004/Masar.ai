"""M01.L01 — Building AI Applications with Foundation Models.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 1, "Introduction to Building AI Applications with Foundation Models".
Instructor-authored curriculum adaptation based only on the supplied chapter.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of AI Engineering"

MODULE_DESCRIPTION = (
    "Understand how language models evolved into foundation models, why AI "
    "engineering emerged, where foundation models are useful, how to plan an "
    "AI product, and how the modern AI engineering stack differs from "
    "traditional ML engineering."
)

SOURCE_CHAPTER = 1

SOURCE_PAGES = "Page range not provided in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Building AI Applications with Foundation Models",

    "slug": "ai-engineering-m01-l01-building-with-foundation-models",

    "description": (
        "A practical introduction to foundation models and AI engineering: "
        "language models, tokens, self-supervision, multimodality, adaptation "
        "techniques, use cases, product planning, evaluation, infrastructure, "
        "and the modern AI application stack."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.0,

    "skill_tags": [
        "ai-engineering",
        "foundation-models",
        "language-models",
        "self-supervision",
        "multimodal-ai",
        "prompt-engineering",
        "rag",
        "finetuning",
        "evaluation",
        "ai-product-design",
        "ai-stack",
        "ml-engineering",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Building AI Applications with Foundation Models",

        "content": (
            "# Building AI Applications with Foundation Models\n"
            "\n"
            "> **Course:** AI Engineering Foundations  \n"
            "> **Lesson:** M01.L01  \n"
            "> **Module:** Foundations of AI Engineering  \n"
            "> **Source alignment:** Chapter 1, *Introduction to Building AI "
            "Applications with Foundation Models*. This lesson is an "
            "instructor-authored curriculum adaptation rather than a "
            "reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why the scale of modern AI models helped create the field "
            "of AI engineering.\n"
            "- Explain what a language model does and how tokens, vocabulary, "
            "tokenization, and probabilistic completion fit together.\n"
            "- Distinguish masked language models from autoregressive language "
            "models.\n"
            "- Explain why self-supervision made it possible to train models on "
            "very large amounts of text.\n"
            "- Describe the transition from LLMs to multimodal foundation models.\n"
            "- Distinguish prompt engineering, RAG, and finetuning as ways to "
            "adapt a general-purpose model.\n"
            "- Recognize major foundation-model application patterns and their "
            "limits.\n"
            "- Evaluate an AI application idea before building it.\n"
            "- Reason about human involvement, automation level, product "
            "defensibility, success metrics, milestones, and maintenance.\n"
            "- Describe the application-development, model-development, and "
            "infrastructure layers of the AI engineering stack.\n"
            "- Explain the major differences between traditional ML engineering "
            "and AI engineering.\n"
            "- Distinguish pre-training, finetuning, post-training, prompt "
            "engineering, dataset engineering, inference optimization, and "
            "evaluation.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why AI engineering emerged\n"
            "\n"
            "A useful way to understand modern AI is to start with **scale**. "
            "Models became larger, were trained on far more data, and required "
            "far more computation than earlier systems. This increase in scale "
            "had two important consequences.\n"
            "\n"
            "First, larger general-purpose models became capable of handling a "
            "wider range of tasks. Instead of building a separate model for every "
            "problem, developers could reuse one powerful model for writing, "
            "summarization, classification, coding, question answering, and other "
            "tasks.\n"
            "\n"
            "Second, training these very large models became expensive. It "
            "requires large datasets, specialized hardware, infrastructure, and "
            "expertise. Only a relatively small number of organizations can "
            "comfortably train frontier-scale models from scratch.\n"
            "\n"
            "That created a new pattern: **model as a service**. A model provider "
            "trains and serves the model, while application developers access it "
            "through an API or another hosted interface.\n"
            "\n"
            "The result is a major shift in where engineering effort goes:\n"
            "\n"
            "```text\n"
            "Traditional path\n"
            "problem -> collect data -> train model -> deploy model -> build product\n"
            "\n"
            "Foundation-model path\n"
            "problem -> choose existing model -> adapt model behavior -> evaluate -> build product\n"
            "```\n"
            "\n"
            "**AI engineering** is the discipline of building useful applications "
            "on top of readily available foundation models. It does not eliminate "
            "machine learning engineering. Instead, it changes the center of "
            "gravity from training every model yourself toward adapting, "
            "evaluating, integrating, and operating powerful existing models.\n"
            "\n"
            "[[IMAGE_NEEDED: From traditional ML to AI engineering | "
            "A two-lane diagram comparing the traditional workflow of collecting "
            "data and training a task-specific model with the foundation-model "
            "workflow of selecting an existing model, adapting it, evaluating it, "
            "and integrating it into an application | Learner should notice that "
            "AI engineering shifts much of the effort from model creation toward "
            "model adaptation and product development]]\n"
            "\n"
            "### The key mental model\n"
            "\n"
            "Do not think of a foundation model as the finished product. Think of "
            "it as a powerful component inside a larger software system. The "
            "application still needs instructions, context, data access, "
            "evaluation, interfaces, monitoring, and business logic.\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Language models: tokens, probabilities, and completion\n"
            "\n"
            "A **language model** captures statistical information about language. "
            "Given some context, it estimates which token is likely to fit next or "
            "which token is missing.\n"
            "\n"
            "For example, after a context such as:\n"
            "\n"
            "```text\n"
            "My favorite color is ...\n"
            "```\n"
            "\n"
            "a model should assign more probability to a plausible color word "
            "than to an unrelated word. The important point is that the model is "
            "working with **probabilities**, not guaranteed truths.\n"
            "\n"
            "### Tokens and tokenization\n"
            "\n"
            "Language models usually do not process raw sentences as indivisible "
            "objects. They break text into smaller units called **tokens**. A "
            "token may be a full word, a part of a word, punctuation, or another "
            "text unit chosen by the tokenizer.\n"
            "\n"
            "The process of splitting text into tokens is called "
            "**tokenization**. The complete set of tokens a model knows is its "
            "**vocabulary**.\n"
            "\n"
            "Tokens are a useful compromise between characters and full words:\n"
            "\n"
            "- They can preserve meaningful word pieces.\n"
            "- They keep the vocabulary smaller than a vocabulary containing "
            "every possible word.\n"
            "- They let a model represent unfamiliar or newly created words by "
            "splitting them into known pieces.\n"
            "\n"
            "[[IMAGE_NEEDED: Tokenization example | A short English sentence "
            "visually split into several word and subword tokens, including at "
            "least one word divided into two tokens | Learner should notice that "
            "tokens are not always identical to words and that tokenization "
            "controls the units the model processes]]\n"
            "\n"
            "### Two important language-model families\n"
            "\n"
            "**Masked language model**  \n"
            "A masked model predicts a missing token using context from both "
            "sides of the missing position. This is useful for tasks that need a "
            "strong representation of the whole sequence.\n"
            "\n"
            "```text\n"
            "My favorite ___ is blue.\n"
            "```\n"
            "\n"
            "The model can inspect both the words before and after the blank.\n"
            "\n"
            "**Autoregressive language model**  \n"
            "An autoregressive model predicts the next token using the tokens "
            "that came before it. It can then append that token and repeat the "
            "process, generating a sequence one token at a time.\n"
            "\n"
            "```text\n"
            "My favorite color is ___\n"
            "```\n"
            "\n"
            "This next-token process makes autoregressive models especially "
            "natural for open-ended text generation.\n"
            "\n"
            "[[IMAGE_NEEDED: Masked versus autoregressive language models | "
            "A side-by-side diagram where the masked model fills a blank using "
            "context on both sides and the autoregressive model predicts the next "
            "token using only preceding tokens | Learner should notice the "
            "different information available to each model during prediction]]\n"
            "\n"
            "### A language model as a completion machine\n"
            "\n"
            "A helpful beginner mental model is to treat an autoregressive "
            "language model as a very powerful completion machine. Give it a "
            "prompt, and it predicts a continuation.\n"
            "\n"
            "Many tasks can be reframed as completion:\n"
            "\n"
            "- Translation: provide a sentence and ask for its translation.\n"
            "- Classification: provide a document and ask the model to complete "
            "an `Answer:` field with a label.\n"
            "- Summarization: provide content followed by a summary instruction.\n"
            "- Coding: provide a description, partial function, or code context "
            "and ask the model to continue.\n"
            "\n"
            "This flexibility explains why one model can support many tasks. But "
            "the output is still a prediction sampled from a probability "
            "distribution. A fluent answer is not automatically a correct answer.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Self-supervision: the scaling breakthrough\n"
            "\n"
            "Large models need large amounts of training data. The traditional "
            "supervised approach can become a bottleneck because humans must "
            "label examples.\n"
            "\n"
            "Imagine a fraud detector. In supervised learning, each historical "
            "transaction might need a label such as `fraud` or `not fraud`. Human "
            "labeling can be slow, expensive, and difficult to scale, especially "
            "for expert tasks.\n"
            "\n"
            "**Self-supervision** changes this. The training signal is derived "
            "from the data itself instead of requiring a human to manually attach "
            "a label to every example.\n"
            "\n"
            "For autoregressive language modeling, a text sequence naturally "
            "creates many training examples. Consider:\n"
            "\n"
            "```text\n"
            "I love street food.\n"
            "```\n"
            "\n"
            "It can be turned conceptually into examples such as:\n"
            "\n"
            "| Context | Target |\n"
            "|---|---|\n"
            "| beginning | I |\n"
            "| I | love |\n"
            "| I love | street |\n"
            "| I love street | food |\n"
            "| I love street food | . |\n"
            "\n"
            "The next token becomes the label automatically. This means large "
            "collections of ordinary text can become training material without "
            "manual labeling of every token.\n"
            "\n"
            "### Self-supervised is not the same as unsupervised\n"
            "\n"
            "- **Self-supervised learning:** labels or prediction targets are "
            "constructed from the input itself.\n"
            "- **Unsupervised learning:** the learning objective does not require "
            "labels in the same sense.\n"
            "\n"
            "That distinction matters because people often use the terms "
            "interchangeably even though they describe different training setups.\n"
            "\n"
            "### Why larger models generally need more data\n"
            "\n"
            "A larger model has more parameters and therefore more capacity. To "
            "use that capacity effectively, it usually needs more training data. "
            "Training a very large model on a tiny dataset can waste compute "
            "because a smaller model might achieve similar or better results more "
            "efficiently.\n"
            "\n"
            "{{exercise:M01.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 4. From LLMs to multimodal foundation models\n"
            "\n"
            "A text-only language model sees the world through text. Real-world "
            "applications often need more: images, audio, video, and other data "
            "types. A **modality** is a type of data or signal, such as text, "
            "vision, or audio.\n"
            "\n"
            "A model that can work with more than one modality is "
            "**multimodal**. For example, a multimodal model might accept text and "
            "an image together, reason over both, and then produce text.\n"
            "\n"
            "The term **foundation model** is useful because these models act as "
            "a general base that can be reused for many downstream applications. "
            "In the supplied chapter, the term covers large language models and "
            "large multimodal models.\n"
            "\n"
            "[[IMAGE_NEEDED: Multimodal foundation model | A diagram with text "
            "tokens and image tokens entering the same model and a generated "
            "output token leaving it | Learner should notice that the model can "
            "condition its output on multiple modalities rather than text alone]]\n"
            "\n"
            "### From task-specific to general-purpose models\n"
            "\n"
            "Earlier ML systems were commonly designed for one narrow task. A "
            "sentiment classifier classified sentiment; a translation model "
            "translated. Foundation models are different because the same model "
            "can often perform many tasks without being retrained from scratch for "
            "each one.\n"
            "\n"
            "General-purpose does **not** mean perfect for every task. A model may "
            "need adaptation to follow a company's tone, use private knowledge, "
            "meet strict output formats, or improve performance on a specialized "
            "domain.\n"
            "\n"
            "### Three common adaptation techniques\n"
            "\n"
            "**1. Prompt engineering**  \n"
            "Give the model better instructions, examples, formatting rules, and "
            "context without changing its weights.\n"
            "\n"
            "**2. Retrieval-augmented generation (RAG)**  \n"
            "Retrieve relevant information from an external knowledge source and "
            "place that information into the model's context so it can answer "
            "using up-to-date or domain-specific evidence.\n"
            "\n"
            "**3. Finetuning**  \n"
            "Continue training the model so its weights change and it becomes "
            "better adapted to a target behavior or task.\n"
            "\n"
            "A simple decision intuition is:\n"
            "\n"
            "```text\n"
            "Need clearer behavior or formatting? -> Start with prompting.\n"
            "Need private/current knowledge?       -> Consider retrieval/RAG.\n"
            "Need deeper behavioral adaptation?   -> Consider finetuning.\n"
            "```\n"
            "\n"
            "These methods are not mutually exclusive. A production system can "
            "combine all three.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Why AI engineering is growing so quickly\n"
            "\n"
            "The chapter identifies three forces that make AI engineering grow "
            "rapidly.\n"
            "\n"
            "### Factor 1: General-purpose capabilities\n"
            "\n"
            "A foundation model can support many different tasks. That broadens "
            "the number of possible products and the number of people who can "
            "benefit from them.\n"
            "\n"
            "### Factor 2: Increased investment\n"
            "\n"
            "As organizations see possible gains in productivity, product quality, "
            "and speed to market, they invest more heavily in AI applications.\n"
            "\n"
            "### Factor 3: A lower barrier to entry\n"
            "\n"
            "Hosted models and APIs let developers use powerful models without "
            "running the full training and serving infrastructure themselves. In "
            "addition, developers can often express desired behavior in natural "
            "language, which lowers the cost of experimentation.\n"
            "\n"
            "### Why call it AI engineering?\n"
            "\n"
            "The chapter uses **AI engineering** to emphasize engineering "
            "applications around foundation models rather than focusing only on "
            "training ML models or only on operations. The discipline still "
            "inherits much from ML engineering and software engineering.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. What foundation models are useful for\n"
            "\n"
            "Because foundation models are general-purpose, their applications "
            "span many categories. The important lesson is not to memorize every "
            "example. Learn the **patterns**.\n"
            "\n"
            "### 6.1 Coding\n"
            "\n"
            "AI can assist with code completion, code generation, translation "
            "between languages or frameworks, documentation, testing, structured "
            "data extraction, and other software tasks.\n"
            "\n"
            "The key boundary is complexity. AI can be highly useful for many "
            "routine or well-specified tasks, while difficult system design, "
            "ambiguous requirements, and complex debugging can still demand strong "
            "human engineering judgment.\n"
            "\n"
            "### 6.2 Image and video production\n"
            "\n"
            "Generative models can create or edit visual assets, generate "
            "variations, help brainstorm designs, and accelerate marketing and "
            "creative workflows.\n"
            "\n"
            "### 6.3 Writing\n"
            "\n"
            "Writing is a natural use case because language models are trained to "
            "predict and generate text. They can draft, rewrite, summarize, adjust "
            "tone, generate marketing copy, help with reports, and support many "
            "communication tasks.\n"
            "\n"
            "The same capability can also be abused, for example by mass-producing "
            "low-quality content. Ease of generation does not guarantee quality or "
            "value.\n"
            "\n"
            "### 6.4 Education\n"
            "\n"
            "AI can adapt explanations, generate practice questions, provide "
            "tutoring, support language practice, and offer multiple ways to "
            "explain the same idea. The strongest educational use is not simply "
            "doing the learner's work, but helping the learner understand and "
            "practice.\n"
            "\n"
            "### 6.5 Conversational bots\n"
            "\n"
            "Conversational systems can answer questions, explain concepts, "
            "brainstorm, support customers, or act as copilots inside products. "
            "The interface can be text, voice, or even embodied in games and "
            "interactive environments.\n"
            "\n"
            "### 6.6 Information aggregation\n"
            "\n"
            "Foundation models can summarize documents, combine information from "
            "multiple sources, support 'talk to your documents' systems, and turn "
            "large amounts of communication into facts, questions, and action "
            "items.\n"
            "\n"
            "### 6.7 Data organization\n"
            "\n"
            "AI can help extract structure from unstructured data such as images, "
            "documents, receipts, contracts, and reports. It can also generate "
            "descriptions and semantic representations that make information "
            "easier to search.\n"
            "\n"
            "### 6.8 Workflow automation\n"
            "\n"
            "AI applications can automate multi-step tasks such as data entry, "
            "lead management, form filling, reimbursements, or travel planning. "
            "When a model can plan and use external tools, the system starts to "
            "look like an **agent**.\n"
            "\n"
            "### A practical risk lesson\n"
            "\n"
            "Organizations often deploy lower-risk internal applications before "
            "high-risk external systems. Internal knowledge tools, for example, "
            "can help a company learn how to build with AI while reducing exposure "
            "to failures that directly affect customers.\n"
            "\n"
            "[[IMAGE_NEEDED: Foundation-model use-case map | A compact map or "
            "wheel showing coding, visual generation, writing, education, "
            "conversational bots, information aggregation, data organization, and "
            "workflow automation around a central foundation model | Learner "
            "should notice that one general-purpose model can support many "
            "application categories]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Planning an AI application before building it\n"
            "\n"
            "A demo can be easy to build. A reliable product is much harder. "
            "Before investing deeply, ask whether the application should exist, "
            "what role AI should play, how success will be measured, and how the "
            "system will be maintained.\n"
            "\n"
            "### 7.1 Evaluate the use case\n"
            "\n"
            "Start with the business or user reason. Possible motivations include:\n"
            "\n"
            "- Protecting the business from disruption.\n"
            "- Increasing productivity or reducing costs.\n"
            "- Improving acquisition, retention, support, or internal operations.\n"
            "- Exploring a strategic technology before competitors do.\n"
            "\n"
            "Then ask **build or buy?** If a strong product already solves the "
            "problem cheaply and reliably, buying may be better. If AI is central "
            "to your differentiation or strategic control, building in-house may "
            "be more attractive.\n"
            "\n"
            "### 7.2 Decide how critical AI is\n"
            "\n"
            "**Critical AI** means the product fundamentally depends on AI. "
            "**Complementary AI** improves an existing product but is not required "
            "for the product to function.\n"
            "\n"
            "The more critical AI is, the stronger the requirements for accuracy, "
            "reliability, testing, fallback behavior, and monitoring.\n"
            "\n"
            "### 7.3 Reactive versus proactive AI\n"
            "\n"
            "- **Reactive:** AI responds after a user request or event.\n"
            "- **Proactive:** AI acts or surfaces information without an explicit "
            "request at that moment.\n"
            "\n"
            "Proactive systems can feel intrusive if they are wrong or low "
            "quality. Therefore, proactive behavior often needs a higher quality "
            "bar.\n"
            "\n"
            "### 7.4 Dynamic versus static behavior\n"
            "\n"
            "- **Dynamic:** the experience changes continuously using user "
            "feedback, personalization, memory, or ongoing adaptation.\n"
            "- **Static:** updates happen only when the shared model or product is "
            "updated.\n"
            "\n"
            "### 7.5 Decide the role of humans\n"
            "\n"
            "AI can support humans at different automation levels:\n"
            "\n"
            "```text\n"
            "Low automation:    AI suggests -> human decides\n"
            "Medium automation: AI handles simple cases -> human handles hard cases\n"
            "High automation:   AI acts directly -> human monitors or handles exceptions\n"
            "```\n"
            "\n"
            "When humans participate in the decision process, the approach is "
            "called **human-in-the-loop**.\n"
            "\n"
            "A useful maturity pattern from the chapter is **Crawl -> Walk -> "
            "Run**:\n"
            "\n"
            "- **Crawl:** human involvement is mandatory.\n"
            "- **Walk:** AI can interact directly with internal users.\n"
            "- **Run:** automation expands and may include external users.\n"
            "\n"
            "[[IMAGE_NEEDED: Crawl-Walk-Run automation maturity | A three-stage "
            "diagram showing mandatory human review, internal direct AI use, and "
            "higher automation with possible external-user interaction | Learner "
            "should notice that automation can increase gradually as confidence "
            "and evidence improve]]\n"
            "\n"
            "### 7.6 Think about defensibility\n"
            "\n"
            "The low barrier to building AI applications is good for you and good "
            "for your competitors. If your product is only a thin layer over a "
            "general model, the model provider may eventually add the same feature.\n"
            "\n"
            "The chapter highlights three broad sources of advantage:\n"
            "\n"
            "- **Technology:** unique engineering or capability.\n"
            "- **Data:** proprietary or compounding data and usage insights.\n"
            "- **Distribution:** the ability to reach and retain users.\n"
            "\n"
            "A useful product question is: **What becomes stronger as more users "
            "use this application?** If the answer is 'nothing', the moat may be "
            "weak.\n"
            "\n"
            "### 7.7 Define success before deployment\n"
            "\n"
            "Business success should be measurable. For a support assistant, "
            "possible business metrics include automation rate, response time, "
            "throughput, labor saved, and customer satisfaction.\n"
            "\n"
            "You also need a **usefulness threshold**: the minimum quality at "
            "which the system becomes worth deploying.\n"
            "\n"
            "Important metric groups include:\n"
            "\n"
            "- **Quality:** is the output useful and correct enough?\n"
            "- **Latency:** how quickly does the system respond? The chapter "
            "mentions TTFT (time to first token), TPOT (time per output token), "
            "and total latency.\n"
            "- **Cost:** what does each inference or completed task cost?\n"
            "- **Other constraints:** interpretability, fairness, and any "
            "application-specific requirements.\n"
            "\n"
            "### 7.8 Plan milestones and respect the last-mile problem\n"
            "\n"
            "Start by evaluating existing models. If an off-the-shelf model is "
            "already close to your goal, the remaining work may be manageable. If "
            "it is far away, the project may require more data, adaptation, and "
            "engineering than expected.\n"
            "\n"
            "The most important warning is that early progress can be misleading. "
            "Going from a rough prototype to 'pretty good' can be fast. Going from "
            "'pretty good' to dependable production quality can be much slower. "
            "Edge cases, hallucinations, latency, cost, monitoring, and product "
            "details often dominate the final stretch.\n"
            "\n"
            "### 7.9 Plan maintenance from day one\n"
            "\n"
            "Foundation-model products live in a fast-changing ecosystem. Model "
            "quality, API behavior, context limits, inference cost, providers, and "
            "regulations can all change.\n"
            "\n"
            "Therefore, production systems benefit from:\n"
            "\n"
            "- Versioning models and prompts.\n"
            "- Repeatable evaluations.\n"
            "- The ability to compare or swap providers.\n"
            "- Monitoring cost and latency.\n"
            "- Tracking regulatory and data constraints.\n"
            "- Avoiding deep dependence on a single assumption that may soon be "
            "invalid.\n"
            "\n"
            "{{exercise:M01.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 8. The three layers of the AI engineering stack\n"
            "\n"
            "The chapter organizes the AI stack into three layers. When building "
            "an application, teams often start at the top and move downward only "
            "when they need more control.\n"
            "\n"
            "### Layer 1: Application development\n"
            "\n"
            "This is where you shape the product around the model. Important work "
            "includes:\n"
            "\n"
            "- Prompt engineering.\n"
            "- Context construction and retrieval.\n"
            "- Evaluation.\n"
            "- User interface and product behavior.\n"
            "- Tool integration and workflows.\n"
            "\n"
            "### Layer 2: Model development\n"
            "\n"
            "This layer covers work on the models and the data used to adapt them:\n"
            "\n"
            "- Modeling and training.\n"
            "- Finetuning and other weight-changing methods.\n"
            "- Dataset engineering.\n"
            "- Inference optimization.\n"
            "- Evaluation of the resulting models.\n"
            "\n"
            "### Layer 3: Infrastructure\n"
            "\n"
            "Infrastructure supports reliable operation:\n"
            "\n"
            "- Model serving.\n"
            "- Data and compute management.\n"
            "- GPU and cluster infrastructure when needed.\n"
            "- Monitoring and observability.\n"
            "\n"
            "[[IMAGE_NEEDED: Three-layer AI engineering stack | A vertical stack "
            "with Application Development on top, Model Development in the "
            "middle, and Infrastructure at the bottom, with two or three example "
            "responsibilities inside each layer | Learner should notice that most "
            "application builders can begin at the top and move down only when "
            "more control is necessary]]\n"
            "\n"
            "### What changed and what stayed the same\n"
            "\n"
            "Foundation models changed tools and workflows, but many engineering "
            "principles remain:\n"
            "\n"
            "- AI applications still need to solve real problems.\n"
            "- Business metrics still need to connect to model or system metrics.\n"
            "- Teams still need systematic experiments.\n"
            "- Production systems still need monitoring and feedback loops.\n"
            "- Faster and cheaper inference is still desirable.\n"
            "\n"
            "What changed is the experiment surface. Instead of tuning only model "
            "hyperparameters, AI engineers may compare models, prompts, retrieval "
            "methods, sampling settings, context strategies, and adaptation "
            "techniques.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. AI engineering versus traditional ML engineering\n"
            "\n"
            "The chapter highlights three major differences.\n"
            "\n"
            "### Difference 1: Build a model versus adapt a model\n"
            "\n"
            "Traditional ML projects often require training a model for the "
            "application. AI engineering often begins with a model already trained "
            "by another organization. The engineer's job shifts toward selecting "
            "and adapting that model.\n"
            "\n"
            "### Difference 2: Bigger models increase compute and latency pressure\n"
            "\n"
            "Foundation models can be expensive to run. That makes GPU "
            "infrastructure, serving efficiency, and inference optimization more "
            "important.\n"
            "\n"
            "### Difference 3: Open-ended outputs are harder to evaluate\n"
            "\n"
            "A binary classifier has a small set of possible answers. A chatbot "
            "can produce countless plausible responses. That makes evaluation "
            "substantially harder and more central to AI engineering.\n"
            "\n"
            "A compact comparison:\n"
            "\n"
            "| Area | Traditional ML emphasis | Foundation-model AI emphasis |\n"
            "|---|---|---|\n"
            "| Model creation | Often central | Often start from an existing model |\n"
            "| Adaptation | Task-specific training | Prompting, context, RAG, finetuning |\n"
            "| Data | Feature engineering and labels are often central | Unstructured data, retrieval, quality, adaptation data |\n"
            "| Evaluation | Important | Even more important for open-ended outputs |\n"
            "| Inference efficiency | Important | Often more urgent because models are larger |\n"
            "| Interface | Sometimes secondary to the model | Often a core part of the product |\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Model development vocabulary you must get right\n"
            "\n"
            "Several terms are frequently confused. Keeping them separate will "
            "save you a lot of confusion later.\n"
            "\n"
            "### Training\n"
            "\n"
            "Training changes model weights through an optimization process. "
            "However, not every numerical change to weights is training; for "
            "example, changing weight precision through quantization is an "
            "optimization transformation rather than a training phase.\n"
            "\n"
            "### Pre-training\n"
            "\n"
            "Pre-training starts from randomly initialized weights and trains the "
            "base model. For large foundation models, this is usually the most "
            "resource-intensive phase.\n"
            "\n"
            "### Finetuning\n"
            "\n"
            "Finetuning continues training from an already trained model. Because "
            "the model begins with useful capabilities, finetuning generally needs "
            "less data and compute than pre-training.\n"
            "\n"
            "### Post-training\n"
            "\n"
            "Post-training is training performed after pre-training. The chapter "
            "notes that post-training and finetuning are conceptually similar, "
            "though people sometimes use 'post-training' for work done by the base "
            "model developer and 'finetuning' for adaptation done by application "
            "developers.\n"
            "\n"
            "### Prompt engineering is not training\n"
            "\n"
            "If you teach a model what to do only by changing its input context, "
            "you are not changing its weights. That is prompt engineering, not "
            "training.\n"
            "\n"
            "### Dataset engineering\n"
            "\n"
            "Dataset engineering includes curating, generating, annotating, and "
            "cleaning data used to train or adapt models.\n"
            "\n"
            "With foundation models, dataset work often involves unstructured "
            "data and tasks such as:\n"
            "\n"
            "- Deduplication.\n"
            "- Tokenization.\n"
            "- Context retrieval.\n"
            "- Quality control.\n"
            "- Removing sensitive or harmful material when required.\n"
            "\n"
            "Open-ended outputs also make annotation harder. Labeling an email as "
            "spam/not-spam is much easier than writing or judging a high-quality "
            "long-form answer.\n"
            "\n"
            "### Inference optimization\n"
            "\n"
            "Inference optimization means making model execution faster and "
            "cheaper. It becomes especially important for autoregressive models "
            "because generation happens token by token, so long outputs can "
            "directly increase latency and cost.\n"
            "\n"
            "The chapter points to techniques such as quantization, distillation, "
            "and parallelism as important tools in this area.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Application development: evaluation, context, and interface\n"
            "\n"
            "When many teams can access the same base models, the quality of the "
            "application layer becomes a major source of differentiation.\n"
            "\n"
            "### Evaluation\n"
            "\n"
            "Evaluation is needed throughout the lifecycle:\n"
            "\n"
            "- Selecting a model.\n"
            "- Comparing prompts or adaptation methods.\n"
            "- Measuring progress.\n"
            "- Deciding whether the application is ready to ship.\n"
            "- Detecting regressions and new opportunities in production.\n"
            "\n"
            "Evaluation is harder for foundation models because there may be many "
            "acceptable answers to the same prompt. A system can also change "
            "dramatically when you change the prompt, examples, context, or "
            "retrieval strategy. Therefore, a benchmark result is meaningful only "
            "when you understand **how** the model was evaluated.\n"
            "\n"
            "### Prompt engineering and context construction\n"
            "\n"
            "Prompt engineering is not only wording a clever instruction. A strong "
            "application may need to provide:\n"
            "\n"
            "- Clear instructions.\n"
            "- Examples.\n"
            "- Relevant retrieved information.\n"
            "- Tool descriptions and permissions.\n"
            "- Conversation history.\n"
            "- Memory or a strategy for managing long context.\n"
            "\n"
            "This broader process of supplying the model with what it needs is "
            "often better understood as **context construction**.\n"
            "\n"
            "### AI interface\n"
            "\n"
            "The interface is how users interact with the AI system. Common forms "
            "include:\n"
            "\n"
            "- Standalone web, desktop, or mobile applications.\n"
            "- Browser extensions.\n"
            "- Chatbots inside communication platforms.\n"
            "- Plug-ins or add-ons inside existing products.\n"
            "- Voice interfaces.\n"
            "- Embodied or spatial interfaces.\n"
            "\n"
            "The interface is also part of the feedback system. Conversations can "
            "give you rich user feedback, but that feedback can be difficult to "
            "structure and analyze automatically.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Why AI engineering is moving closer to full-stack engineering\n"
            "\n"
            "Traditional ML workflows often started with data and model training, "
            "while product integration came later. Foundation models make a "
            "different workflow possible: build a product prototype quickly using "
            "an existing model, test whether users care, then invest more deeply "
            "in data and model adaptation if the product shows promise.\n"
            "\n"
            "This increases the value of engineers who can move across the stack: "
            "model APIs, backend services, frontend interfaces, evaluation, data, "
            "and product iteration.\n"
            "\n"
            "[[IMAGE_NEEDED: Product-first AI engineering workflow | A simple "
            "loop showing idea -> existing foundation model -> product prototype "
            "-> user feedback -> evaluation -> better data/model adaptation -> "
            "improved product | Learner should notice that modern AI teams can "
            "validate the product earlier instead of waiting for a custom model "
            "to be trained first]]\n"
            "\n"
            "The key advantage is iteration speed. Fast demos are not the finish "
            "line, but they can reveal whether an idea deserves deeper investment.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> A foundation model is already a complete AI product.\n"
            "\n"
            "**Why this is wrong:** the model is one component. A production "
            "application still needs context, evaluation, interfaces, tool access, "
            "business rules, security, monitoring, and maintenance.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Prompt engineering and finetuning are the same thing.\n"
            "\n"
            "**Why this is wrong:** prompting changes the input context; "
            "finetuning changes model weights through training.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> If a demo works, the product is almost finished.\n"
            "\n"
            "**Why this is wrong:** the last mile often contains the hardest work: "
            "edge cases, quality thresholds, hallucinations, latency, cost, "
            "monitoring, compliance, and user experience.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> A larger model is automatically the best choice.\n"
            "\n"
            "**Why this is wrong:** larger models can cost more and respond more "
            "slowly. The right choice depends on required quality, latency, cost, "
            "control, and the task.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Token | A basic text unit processed by a language model; it may be a word, subword, punctuation mark, or another unit. |\n"
            "| Tokenization | The process of splitting text into tokens. |\n"
            "| Vocabulary | The complete set of tokens a model can represent directly. |\n"
            "| Language model | A model that captures statistical patterns in language and predicts tokens from context. |\n"
            "| Masked language model | A model trained to predict missing tokens using context on both sides. |\n"
            "| Autoregressive model | A model that predicts the next token using preceding tokens and can generate sequentially. |\n"
            "| Self-supervision | Training in which prediction targets are derived from the input data itself. |\n"
            "| Parameter | A learned variable in a model. |\n"
            "| Modality | A type of data such as text, image, audio, or video. |\n"
            "| Multimodal model | A model that can work with more than one modality. |\n"
            "| Foundation model | A large general-purpose model that can serve as a base for many downstream applications. |\n"
            "| Prompt engineering | Adapting model behavior through instructions, examples, and context without updating weights. |\n"
            "| RAG | Retrieval-augmented generation; retrieving external information and adding it to model context. |\n"
            "| Finetuning | Continuing training from an existing model so its weights change. |\n"
            "| Pre-training | Training a base model from randomly initialized weights. |\n"
            "| Post-training | Training performed after the pre-training stage. |\n"
            "| Human-in-the-loop | A system design in which humans participate in review, decisions, or exception handling. |\n"
            "| Inference | Computing a model output from an input. |\n"
            "| Inference optimization | Techniques that make inference faster and/or cheaper. |\n"
            "| Evaluation | Systematic measurement used to select, improve, validate, and monitor models or applications. |\n"
            "| Context construction | Supplying the model with the instructions, information, history, tools, and other context needed for a task. |\n"
            "| Agent | An AI system that can plan and use tools to carry out tasks. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer these without looking "
            "back at the lesson:\n"
            "\n"
            "1. Why did model scale help create the conditions for AI engineering?\n"
            "2. What is the difference between a token and a word?\n"
            "3. How does a masked language model differ from an autoregressive one?\n"
            "4. Why does self-supervision make language-model training easier to scale?\n"
            "5. What makes a foundation model different from a narrow task-specific model?\n"
            "6. When would you consider prompting, RAG, or finetuning?\n"
            "7. What are the eight major use-case patterns discussed in this lesson?\n"
            "8. Why should the role of humans be decided before deployment?\n"
            "9. What is a usefulness threshold?\n"
            "10. Why is the final 10-20% of product quality often harder than the first prototype?\n"
            "11. What are the three layers of the AI engineering stack?\n"
            "12. Why is evaluation especially difficult for open-ended outputs?\n"
            "13. What is the technical difference between prompting and training?\n"
            "14. Why has interface/product engineering become more important in AI engineering?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**AI engineering is not simply calling an LLM API. It is the "
            "engineering discipline of turning a powerful general-purpose model "
            "into a useful, measurable, reliable, maintainable product through "
            "adaptation, context, evaluation, interfaces, data, and infrastructure.**\n"
        ),

        "estimated_minutes": 180,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "why-ai-engineering",
                "title": "Why AI engineering emerged",
                "order": 1,
            },
            {
                "id": "language-model-basics",
                "title": "Language models: tokens, probabilities, and completion",
                "order": 2,
            },
            {
                "id": "self-supervision",
                "title": "Self-supervision: the scaling breakthrough",
                "order": 3,
            },
            {
                "id": "foundation-models",
                "title": "From LLMs to multimodal foundation models",
                "order": 4,
            },
            {
                "id": "growth-of-ai-engineering",
                "title": "Why AI engineering is growing so quickly",
                "order": 5,
            },
            {
                "id": "foundation-model-use-cases",
                "title": "What foundation models are useful for",
                "order": 6,
            },
            {
                "id": "planning-ai-applications",
                "title": "Planning an AI application before building it",
                "order": 7,
            },
            {
                "id": "ai-engineering-stack",
                "title": "The three layers of the AI engineering stack",
                "order": 8,
            },
            {
                "id": "ai-vs-ml-engineering",
                "title": "AI engineering versus traditional ML engineering",
                "order": 9,
            },
            {
                "id": "training-and-model-development",
                "title": "Model development vocabulary you must get right",
                "order": 10,
            },
            {
                "id": "application-development",
                "title": "Application development: evaluation, context, and interface",
                "order": 11,
            },
            {
                "id": "full-stack-shift",
                "title": "Why AI engineering is moving closer to full-stack engineering",
                "order": 12,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Trace the Evolution from Text to Foundation Models",

            "lesson_code": "M01.L01",

            "section_id": "self-supervision",

            "placement": "after_section",

            "description": (
                "Practice the core language-model concepts that explain why "
                "foundation models could scale."
            ),

            "instructions": (
                "1. Write a one-sentence definition of tokenization.\n"
                "2. Explain the difference between masked and autoregressive "
                "language modeling using your own example.\n"
                "3. Convert the short sentence 'AI helps people learn' into at "
                "least three conceptual next-token training examples.\n"
                "4. Explain why these examples are self-supervised rather than "
                "manually supervised.\n"
                "5. In 3-5 sentences, connect self-supervision to the growth of "
                "large language models."
            ),

            "expected_output": (
                "A short written answer containing a tokenization definition, "
                "a masked-vs-autoregressive comparison, at least three "
                "next-token training pairs, and an explanation of why "
                "self-supervision supports scaling."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "tokenization",
                "language-model-types",
                "self-supervision",
                "conceptual-reasoning",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Design a Production-Minded AI Application",

            "lesson_code": "M01.L01",

            "section_id": "planning-ai-applications",

            "placement": "after_section",

            "description": (
                "Turn an AI idea into a reasoned product plan instead of stopping "
                "at a demo."
            ),

            "instructions": (
                "Choose one application: customer-support assistant, document "
                "research assistant, coding copilot, education tutor, or another "
                "foundation-model application.\n\n"
                "1. State the user problem and why AI is useful for it.\n"
                "2. Decide whether AI is critical or complementary.\n"
                "3. Decide whether the behavior is reactive or proactive.\n"
                "4. Define the human-in-the-loop design for the first release.\n"
                "5. Choose whether you would start with prompting, RAG, "
                "finetuning, or a combination, and explain why.\n"
                "6. Define three business/product success metrics.\n"
                "7. Define a usefulness threshold including at least one quality, "
                "one latency, and one cost requirement.\n"
                "8. Name one defensibility advantage you would try to build.\n"
                "9. List two maintenance risks you would monitor after launch.\n"
                "10. Sketch which parts belong to the application, model, and "
                "infrastructure layers."
            ),

            "expected_output": (
                "A compact AI product design document that connects the use case "
                "to automation level, adaptation approach, metrics, reliability, "
                "defensibility, maintenance, and the three-layer AI stack."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "ai-product-planning",
                "human-in-the-loop",
                "model-adaptation",
                "evaluation-design",
                "ai-stack",
                "product-reasoning",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "Building AI Applications with Foundation Models — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",

                "section_id": "why-ai-engineering",

                "question": (
                    "Which change most directly lowered the barrier to building "
                    "applications with powerful foundation models?"
                ),

                "options": [
                    "Every developer can now train a frontier model cheaply",
                    "Models are available through hosted services and APIs",
                    "AI applications no longer need evaluation",
                    "Foundation models removed the need for software engineering",
                ],

                "correct": 1,

                "explanation": (
                    "Hosted models and APIs let developers use powerful models "
                    "without first building the full training and serving stack."
                ),
            },

            {
                "id": "M01.L01.Q02",

                "section_id": "language-model-basics",

                "question": (
                    "What is the defining training behavior of an autoregressive "
                    "language model?"
                ),

                "options": [
                    "It predicts the next token from preceding tokens",
                    "It only classifies complete documents",
                    "It always sees future tokens before generating",
                    "It predicts image labels from pixels",
                ],

                "correct": 0,

                "explanation": (
                    "Autoregressive language models predict the next token using "
                    "the sequence that came before it, then continue token by token."
                ),
            },

            {
                "id": "M01.L01.Q03",

                "section_id": "self-supervision",

                "question": (
                    "Why is language modeling well suited to self-supervision?"
                ),

                "options": [
                    "Every sentence is manually labeled by an expert",
                    "The input sequence itself can provide prediction targets",
                    "The model does not require any learning objective",
                    "Self-supervision removes the need for training data",
                ],

                "correct": 1,

                "explanation": (
                    "The sequence itself supplies targets such as the next token, "
                    "so large text datasets can be used without manually labeling "
                    "every example."
                ),
            },

            {
                "id": "M01.L01.Q04",

                "section_id": "foundation-models",

                "question": (
                    "A company needs an LLM to answer questions using frequently "
                    "updated internal policy documents. Which adaptation technique "
                    "is the most directly suited to bringing those documents into "
                    "the model's answer context?"
                ),

                "options": [
                    "Random weight initialization",
                    "Retrieval-augmented generation",
                    "Removing the user interface",
                    "Pre-training from scratch",
                ],

                "correct": 1,

                "explanation": (
                    "RAG retrieves relevant external information and adds it to "
                    "the model context, which is well suited to private or changing "
                    "knowledge."
                ),
            },

            {
                "id": "M01.L01.Q05",

                "section_id": "foundation-model-use-cases",

                "question": (
                    "Which statement best reflects the chapter's view of "
                    "foundation-model use cases?"
                ),

                "options": [
                    "They are useful only for text generation",
                    "They support many application patterns, but not every idea "
                    "should automatically be built",
                    "They are only useful for consumer chatbots",
                    "They remove all risk from automation",
                ],

                "correct": 1,

                "explanation": (
                    "Foundation models support many categories, but product risk, "
                    "quality, business value, and operational constraints still "
                    "matter."
                ),
            },

            {
                "id": "M01.L01.Q06",

                "section_id": "planning-ai-applications",

                "question": (
                    "Why might a team begin with mandatory human review before "
                    "allowing an AI system to interact directly with external users?"
                ),

                "options": [
                    "To permanently prevent automation",
                    "To learn system behavior and reduce risk while quality is "
                    "still being validated",
                    "Because AI cannot produce any useful outputs",
                    "Because human-in-the-loop means the model is not used",
                ],

                "correct": 1,

                "explanation": (
                    "Human review is a way to manage uncertainty and gather "
                    "evidence before increasing automation."
                ),
            },

            {
                "id": "M01.L01.Q07",

                "section_id": "ai-engineering-stack",

                "question": (
                    "Which responsibility belongs most directly to the "
                    "infrastructure layer?"
                ),

                "options": [
                    "Writing the system prompt",
                    "Designing the chat interface",
                    "Managing serving, compute, and monitoring",
                    "Choosing the wording of an example in the prompt",
                ],

                "correct": 2,

                "explanation": (
                    "Infrastructure covers the systems that serve models, manage "
                    "data and compute, and monitor operation."
                ),
            },

            {
                "id": "M01.L01.Q08",

                "section_id": "ai-vs-ml-engineering",

                "question": (
                    "Why is evaluation often harder in AI engineering than in a "
                    "traditional binary classification task?"
                ),

                "options": [
                    "Foundation models never produce text",
                    "Open-ended tasks can have many valid responses rather than "
                    "one simple ground-truth label",
                    "Binary classifiers require no evaluation",
                    "Foundation models always return the same output",
                ],

                "correct": 1,

                "explanation": (
                    "Open-ended generation can have many acceptable outputs, so "
                    "evaluation cannot rely only on exact comparison with one "
                    "ground-truth answer."
                ),
            },

            {
                "id": "M01.L01.Q09",

                "section_id": "training-and-model-development",

                "question": (
                    "Which action changes the model's input but does not, by "
                    "itself, update model weights?"
                ),

                "options": [
                    "Pre-training",
                    "Finetuning",
                    "Prompt engineering",
                    "Post-training",
                ],

                "correct": 2,

                "explanation": (
                    "Prompt engineering changes instructions and context. "
                    "Pre-training, finetuning, and post-training involve training "
                    "processes that update weights."
                ),
            },

            {
                "id": "M01.L01.Q10",

                "section_id": "application-development",

                "question": (
                    "Which statement best describes context construction?"
                ),

                "options": [
                    "Only shortening the user's prompt",
                    "Supplying the model with the instructions, information, "
                    "history, tools, and other context needed for the task",
                    "Training a model from random weights",
                    "Replacing evaluation with a larger context window",
                ],

                "correct": 1,

                "explanation": (
                    "Context construction is broader than prompt wording. It "
                    "includes the information and capabilities placed around the "
                    "model so it can complete the task."
                ),
            },

            {
                "id": "M01.L01.Q11",

                "section_id": "full-stack-shift",

                "type": "open",

                "question": (
                    "You can build a useful prototype with an existing foundation "
                    "model in two days. Explain why this does not prove the "
                    "application is production-ready. Refer to at least four ideas "
                    "from the lesson."
                ),
            },
        ],

        "passing_score": 70,
    },
}
