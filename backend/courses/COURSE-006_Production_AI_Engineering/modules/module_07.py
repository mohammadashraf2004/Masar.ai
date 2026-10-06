"""M08.L01 — Dataset Engineering.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 8, "Dataset Engineering".
Instructor-authored curriculum adaptation based only on the supplied chapter.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M08.L01"

MODULE_ORDER = 8

MODULE_TITLE = "Dataset Engineering"

MODULE_DESCRIPTION = (
    "Learn how to design, acquire, synthesize, verify, process, and maintain "
    "training datasets for foundation-model applications, with emphasis on "
    "data quality, coverage, quantity, annotation, synthetic data, distillation, "
    "deduplication, filtering, formatting, privacy, and compliance."
)

SOURCE_CHAPTER = 8

SOURCE_PAGES = "Page range not provided in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Dataset Engineering",

    "slug": "ai-engineering-m08-l01-dataset-engineering",

    "description": (
        "A practical guide to dataset engineering for post-training foundation "
        "models: data-centric AI, curation, quality/coverage/quantity, annotation, "
        "synthetic data, instruction-data generation, data verification, model "
        "distillation, inspection, deduplication, filtering, and final formatting."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 5.5,

    "skill_tags": [
        "dataset-engineering",
        "data-centric-ai",
        "data-curation",
        "annotation",
        "data-quality",
        "data-coverage",
        "data-quantity",
        "synthetic-data",
        "instruction-data",
        "data-verification",
        "distillation",
        "deduplication",
        "data-cleaning",
        "data-formatting",
        "data-compliance",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Dataset Engineering",

        "content": (
            "# Dataset Engineering\n"
            "\n"
            "> **Course:** AI Engineering Foundations  \n"
            "> **Lesson:** M08.L01  \n"
            "> **Module:** Dataset Engineering  \n"
            "> **Source alignment:** Chapter 8, *Dataset Engineering*. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the difference between model-centric and data-centric AI.\n"
            "- Design a dataset around the behavior you want a model to learn.\n"
            "- Match data formats to self-supervised finetuning, instruction "
            "finetuning, preference finetuning, reward modeling, tool use, and "
            "multi-turn conversation.\n"
            "- Evaluate dataset quality using relevance, task alignment, consistency, "
            "format correctness, uniqueness, and compliance.\n"
            "- Design data coverage across user behavior, topics, languages, "
            "lengths, formats, and edge cases.\n"
            "- Estimate how data quantity interacts with task complexity, base-model "
            "strength, finetuning method, and budget.\n"
            "- Use small-data experiments and performance-gain curves to estimate "
            "whether more data is likely to help.\n"
            "- Build a data acquisition strategy using application data, public "
            "datasets, purchased data, annotation, and synthesis.\n"
            "- Explain why annotation guidelines are central to both training and evaluation.\n"
            "- Distinguish data augmentation from data synthesis.\n"
            "- Use rule-based generation, transformations, perturbations, and "
            "simulation to create additional training data.\n"
            "- Explain AI-powered data synthesis, self-play, paraphrasing, translation, "
            "back-translation, and code/data generation workflows.\n"
            "- Design synthetic instruction-data pipelines from topics, templates, "
            "seed examples, and reverse-instruction methods.\n"
            "- Verify generated data using functional checks, AI judges, heuristics, "
            "anomaly detection, and factuality checks.\n"
            "- Explain the main limitations of synthetic data: quality problems, "
            "superficial imitation, model collapse, bias feedback loops, and "
            "obscured lineage.\n"
            "- Explain knowledge distillation and distinguish it from general "
            "synthetic-data training.\n"
            "- Inspect raw data statistically and manually before training.\n"
            "- Detect and remove duplicates using similarity, hashing, and "
            "dimensionality-reduction/search techniques.\n"
            "- Clean and filter datasets for quality, safety, privacy, policy, and budget.\n"
            "- Format data correctly for a model's tokenizer and chat template.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. What dataset engineering is\n"
            "\n"
            "A model cannot learn a behavior that its training data fails to "
            "demonstrate clearly enough.\n"
            "\n"
            "Dataset engineering is the process of creating a dataset that allows "
            "a model to learn the behavior you want **within your available budget**.\n"
            "\n"
            "That includes much more than collecting files. You may need to:\n"
            "\n"
            "- Decide what behaviors should appear in the data.\n"
            "- Decide which behaviors should be removed.\n"
            "- Acquire or annotate examples.\n"
            "- Synthesize missing examples.\n"
            "- Verify quality.\n"
            "- Balance coverage.\n"
            "- Remove duplicates.\n"
            "- Clean unsafe or noncompliant data.\n"
            "- Convert everything into the exact format the model expects.\n"
            "\n"
            "The chapter emphasizes that curation, generation, and processing are "
            "not a one-way pipeline. You often move back and forth as experiments "
            "reveal new weaknesses.\n"
            "\n"
            '{{image:dataset-engineering-lifecycle}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 2. A data-centric view of AI\n"
            "\n"
            "There are two broad ways to improve AI systems.\n"
            "\n"
            "### Model-centric AI\n"
            "\n"
            "Improve the model itself:\n"
            "\n"
            "- New architecture.\n"
            "- Larger model.\n"
            "- Better optimizer/training technique.\n"
            "- Better post-training method.\n"
            "\n"
            "### Data-centric AI\n"
            "\n"
            "Keep the model more fixed and improve the data:\n"
            "\n"
            "- Correct bad labels.\n"
            "- Add missing edge cases.\n"
            "- Improve annotation quality.\n"
            "- Increase diversity.\n"
            "- Remove duplication/noise.\n"
            "- Build a better training-data mix.\n"
            "\n"
            "In practice, successful systems often improve both model and data. The "
            "useful mental shift is to treat data as an engineered system, not a "
            "passive input.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Different training stages need different data\n"
            "\n"
            "The dataset format should match what the model is being trained to do.\n"
            "\n"
            "### Self-supervised finetuning\n"
            "\n"
            "Needs sequences of domain-relevant text or other raw data.\n"
            "\n"
            "### Instruction finetuning\n"
            "\n"
            "Needs examples like:\n"
            "\n"
            "```text\n"
            "(instruction, response)\n"
            "```\n"
            "\n"
            "### Preference finetuning\n"
            "\n"
            "Needs comparative examples such as:\n"
            "\n"
            "```text\n"
            "(instruction, winning_response, losing_response)\n"
            "```\n"
            "\n"
            "### Reward-model training\n"
            "\n"
            "Can use preference pairs or scored examples such as:\n"
            "\n"
            "```text\n"
            "((instruction, response), score)\n"
            "```\n"
            "\n"
            "The high-level curation principles remain similar even when the "
            "required example structure changes.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Training data should demonstrate the desired behavior\n"
            "\n"
            "A dataset is not only information; it is also a demonstration of "
            "**how the model should behave**.\n"
            "\n"
            "If you want concise answers, the dataset should contain concise answers. "
            "If you want tool use, the dataset should contain correct tool-use "
            "trajectories. If you want step-by-step explanations, the dataset needs "
            "examples that demonstrate that behavior.\n"
            "\n"
            "This also works in reverse. If unwanted behavior is present repeatedly "
            "in training data, the model may learn it. Dataset engineering can "
            "therefore include removing examples that teach behaviors you no longer want.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Reasoning and step-by-step data\n"
            "\n"
            "If you want a model to produce step-by-step responses, training "
            "examples should demonstrate step-by-step responses.\n"
            "\n"
            "Creating this data is more expensive than collecting final answers "
            "because annotators must explain intermediate steps correctly and clearly.\n"
            "\n"
            "The chapter uses this as an example of a general principle:\n"
            "\n"
            "> The more complex the behavior you want, the more demanding the "
            "annotation process becomes.\n"
            "\n"
            "This is one reason specialized reasoning datasets are less abundant "
            "than ordinary instruction-response datasets.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Tool-use data\n"
            "\n"
            "To teach a model to use tools, collect examples that include the "
            "actions required to complete a task.\n"
            "\n"
            "Human experts can help create this data, but an important problem "
            "appears: **human-efficient workflows are not always AI-efficient workflows**.\n"
            "\n"
            "A human may:\n"
            "\n"
            "```text\n"
            "open browser -> paste query -> click result -> read page\n"
            "```\n"
            "\n"
            "An AI agent may be better served by:\n"
            "\n"
            "```text\n"
            "call search API -> process returned results directly\n"
            "```\n"
            "\n"
            "Therefore, observation of human work is useful, but simulations and "
            "synthetic tool trajectories can sometimes discover better AI-native actions.\n"
            "\n"
            "Tool-use data may also need richer message structures than ordinary "
            "chat because one model turn can contain messages destined for different "
            "tools or recipients.\n"
            "\n"
            "[[IMAGE_NEEDED: Human versus AI tool workflow | A side-by-side flow "
            "showing a human using browser UI steps and an AI making direct API/tool "
            "calls | Learner should notice that copying human actions exactly may "
            "produce inefficient agent training data]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Single-turn versus multi-turn data\n"
            "\n"
            "**Single-turn data** teaches responses to isolated instructions.\n"
            "\n"
            "**Multi-turn data** teaches interaction across a task:\n"
            "\n"
            "- Asking clarifying questions.\n"
            "- Accepting corrections.\n"
            "- Using new information provided later.\n"
            "- Maintaining goals and constraints across turns.\n"
            "\n"
            "Single-turn data is easier to obtain. Multi-turn data is often more "
            "realistic for applications that solve tasks through conversation.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. The golden trio: quality, coverage, quantity\n"
            "\n"
            "The chapter organizes data curation around three core criteria:\n"
            "\n"
            "1. **Quality** — are the examples good enough to learn from?\n"
            "2. **Coverage** — do examples represent the range of situations the "
            "model must handle?\n"
            "3. **Quantity** — are there enough examples for the desired learning?\n"
            "\n"
            "A cooking analogy is useful:\n"
            "\n"
            "- Quality = ingredients are not spoiled.\n"
            "- Coverage = you have the right mix of ingredients.\n"
            "- Quantity = you have enough ingredients.\n"
            "\n"
            "A massive dataset can still be poor if it has bad examples or narrow coverage.\n"
            "\n"
            "[[IMAGE_NEEDED: Quality coverage quantity triangle | A triangle with "
            "quality, coverage/diversity, and quantity at the corners, with strong "
            "training data in the center | Learner should notice that increasing "
            "only one dimension cannot compensate for failures in the others]]\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Data quality\n"
            "\n"
            "The chapter emphasizes that a small amount of carefully curated data "
            "can outperform a much larger noisy dataset.\n"
            "\n"
            "It proposes six useful quality characteristics.\n"
            "\n"
            "### Relevant\n"
            "\n"
            "Examples should be relevant to the actual task. Old or unrelated data "
            "can be technically valid but still useless for the target behavior.\n"
            "\n"
            "### Aligned with task requirements\n"
            "\n"
            "The annotation should exhibit exactly what the product needs. If the "
            "task needs factual answers, annotations should be factual. If the task "
            "needs concise answers, annotations should be concise.\n"
            "\n"
            "### Consistent\n"
            "\n"
            "Similar cases should receive similar labels/answers across examples "
            "and annotators. Inconsistency makes the learning signal ambiguous.\n"
            "\n"
            "### Correctly formatted\n"
            "\n"
            "Remove irrelevant HTML, inconsistent whitespace, casing errors, "
            "incorrect numeric formatting, and format tokens that the model should "
            "not learn.\n"
            "\n"
            "### Sufficiently unique\n"
            "\n"
            "Excessive duplication biases the learned distribution and wastes compute.\n"
            "\n"
            "### Compliant\n"
            "\n"
            "Training data must satisfy internal policies, laws, licensing rules, "
            "privacy rules, and other requirements relevant to the organization.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Data coverage and diversity\n"
            "\n"
            "Coverage asks whether the dataset represents the situations that real "
            "users will create.\n"
            "\n"
            "Potential diversity dimensions include:\n"
            "\n"
            "- Short versus detailed prompts.\n"
            "- Clean versus typo-heavy text.\n"
            "- Multiple programming languages.\n"
            "- Topic diversity.\n"
            "- Language and cultural diversity.\n"
            "- Input length and response length.\n"
            "- Single-turn and multi-turn interactions.\n"
            "- Open-ended and close-ended tasks.\n"
            "- Output formats such as prose, JSON, code, tables, or yes/no.\n"
            "\n"
            "The correct dimensions depend on the application.\n"
            "\n"
            "A French-to-English translator may not need many languages, but it may "
            "need diversity in topics, sentence lengths, and styles. A global product "
            "assistant may care greatly about linguistic and cultural diversity.\n"
            "\n"
            "The chapter also warns that heterogeneous data is not automatically "
            "better. Adding unrelated data can hurt. Coverage should reflect a "
            "deliberate data mix.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Designing the data mix\n"
            "\n"
            "A simple starting point is to make the dataset resemble real "
            "application usage.\n"
            "\n"
            "If 60% of real requests are support questions and 10% are account "
            "changes, blindly using a 50/50 training mix changes the learned "
            "importance of those behaviors.\n"
            "\n"
            "But copying production frequency is not always enough. Some capabilities "
            "deserve deliberate over-representation because they are difficult, "
            "high-risk, or useful for general reasoning.\n"
            "\n"
            "The chapter describes model-development teams experimenting with "
            "different data mixes on smaller models before selecting a mix for "
            "larger training runs.\n"
            "\n"
            "The key principle is that **data mixture is a hyperparameter** and "
            "should be evaluated empirically.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. How much data do you need?\n"
            "\n"
            "There is no universal answer.\n"
            "\n"
            "Data requirements depend on at least:\n"
            "\n"
            "- Data quality.\n"
            "- Data diversity.\n"
            "- Task complexity.\n"
            "- Base-model capability.\n"
            "- Finetuning method.\n"
            "- Budget for data and compute.\n"
            "\n"
            "### Finetuning method\n"
            "\n"
            "Full finetuning normally requires more data than PEFT methods such as LoRA.\n"
            "\n"
            "### Task complexity\n"
            "\n"
            "Binary sentiment classification may need much less data than complex "
            "financial question answering.\n"
            "\n"
            "### Base-model performance\n"
            "\n"
            "If the base model is already close to the desired behavior, fewer "
            "examples may be required.\n"
            "\n"
            "The chapter suggests starting small—often tens of carefully selected "
            "examples—to see whether finetuning moves the model in the right direction "
            "before investing in a large annotation effort.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Use scaling curves before buying more data\n"
            "\n"
            "Train on subsets of the same dataset, for example:\n"
            "\n"
            "```text\n"
            "25% of data -> score A\n"
            "50% of data -> score B\n"
            "100% of data -> score C\n"
            "```\n"
            "\n"
            "Plot performance against dataset size.\n"
            "\n"
            "- **Steep slope:** more data may still provide strong gains.\n"
            "- **Flat/plateauing slope:** doubling the dataset may produce little improvement.\n"
            "\n"
            "This helps estimate whether additional annotation is worth the cost.\n"
            "\n"
            "The chapter also highlights diminishing returns: early examples can "
            "provide large gains, while later examples often contribute smaller gains.\n"
            "\n"
            "Task diversity can have a similar curve: adding new task types can "
            "provide large gains initially, followed by a plateau.\n"
            "\n"
            "[[IMAGE_NEEDED: Dataset-size performance curve | A learning curve "
            "showing performance rising quickly with early examples and gradually "
            "flattening | Learner should notice diminishing returns and how the "
            "slope informs whether more annotation is worthwhile]]\n"
            "\n"
            "{{exercise:M08.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Use cheaper or less-perfect data before scarce premium data\n"
            "\n"
            "The chapter gives three staged strategies.\n"
            "\n"
            "### Self-supervised -> supervised\n"
            "\n"
            "Use abundant raw domain text first, then scarce labeled examples.\n"
            "\n"
            "### Less-relevant -> highly relevant\n"
            "\n"
            "Learn a related behavior from an abundant dataset, then adapt with the "
            "smaller target-domain dataset.\n"
            "\n"
            "### Synthetic -> real\n"
            "\n"
            "Use synthetic examples to build broad initial behavior, then refine "
            "with scarce real data.\n"
            "\n"
            "These strategies can reduce the amount of expensive human-annotated "
            "data required, but they add training complexity and must be evaluated carefully.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Data acquisition strategy\n"
            "\n"
            "Potential sources include:\n"
            "\n"
            "- Your own application data.\n"
            "- Public datasets.\n"
            "- Purchased/proprietary datasets.\n"
            "- Manual annotation.\n"
            "- Synthetic generation.\n"
            "\n"
            "The chapter treats **application data** as especially valuable because "
            "it naturally reflects the distribution you actually care about.\n"
            "\n"
            "User-generated content, usage traces, system events, and feedback can "
            "form a **data flywheel** when used responsibly to improve the product.\n"
            "\n"
            "Before creating data from scratch, search existing sources. But never "
            "assume a public dataset is correct, clean, legally usable, or relevant. "
            "Inspect its origin, processing, license, and quality.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Annotation guidelines are part of the dataset\n"
            "\n"
            "Good annotation is not just 'hire people and ask them to label things.'\n"
            "\n"
            "Annotators need a clear definition of quality:\n"
            "\n"
            "- What makes a response good?\n"
            "- Can an answer be correct but unhelpful?\n"
            "- What separates score 3 from score 4?\n"
            "- How should uncertainty be handled?\n"
            "- Which sources may be used for fact-checking?\n"
            "- What should happen with ambiguous examples?\n"
            "\n"
            "The chapter connects annotation and evaluation: the same careful "
            "guidelines used to judge outputs can often be reused to create training data.\n"
            "\n"
            "This is a major benefit of investing early in a strong evaluation system.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Data augmentation versus data synthesis\n"
            "\n"
            "**Data augmentation** creates new examples by transforming real examples.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "real cat image -> flip/crop/rotate -> augmented cat image\n"
            "```\n"
            "\n"
            "**Data synthesis** creates artificial examples intended to mimic useful "
            "properties of real data.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "simulation -> synthetic insurance claim\n"
            "```\n"
            "\n"
            "The terms sometimes overlap in practice because both automate data creation.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Why synthesize data?\n"
            "\n"
            "Synthetic data can help with several goals.\n"
            "\n"
            "### Increase quantity\n"
            "\n"
            "Generate examples when real events are rare or expensive to collect.\n"
            "\n"
            "### Increase coverage\n"
            "\n"
            "Target missing regions of the data distribution:\n"
            "\n"
            "- Rare classes.\n"
            "- Edge cases.\n"
            "- Long inputs.\n"
            "- Short inputs.\n"
            "- Adversarial cases.\n"
            "- Underrepresented behaviors.\n"
            "\n"
            "### Increase quality\n"
            "\n"
            "AI-generated examples can sometimes be more consistent or better "
            "suited to AI-native workflows than human-created examples.\n"
            "\n"
            "### Protect privacy\n"
            "\n"
            "Synthetic examples may be used where real records are sensitive or unavailable.\n"
            "\n"
            "### Distill models\n"
            "\n"
            "Use outputs from a strong teacher model to train a cheaper/faster student.\n"
            "\n"
            "[[IMAGE_NEEDED: Synthetic-data motivations | Five branches from "
            "synthetic data labeled quantity, coverage, quality, privacy, and "
            "distillation | Learner should notice that synthetic data is not only "
            "a way to make a dataset bigger]]\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Rule-based synthesis and templates\n"
            "\n"
            "The simplest synthetic-data system uses explicit rules or templates.\n"
            "\n"
            "A transaction template may contain fields such as:\n"
            "\n"
            "```text\n"
            "transaction_id\n"
            "date\n"
            "amount\n"
            "merchant\n"
            "location\n"
            "payment_method\n"
            "status\n"
            "```\n"
            "\n"
            "A generator fills these fields using controlled distributions.\n"
            "\n"
            "Templates work well for structured artifacts:\n"
            "\n"
            "- Invoices.\n"
            "- Resumes.\n"
            "- Tax forms.\n"
            "- Contracts.\n"
            "- Configuration files.\n"
            "- Mathematical expressions.\n"
            "\n"
            "The advantage is control and verifiability. The limitation is that "
            "templates can produce repetitive, unrealistic distributions if designed poorly.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Transformations and perturbations\n"
            "\n"
            "Real examples can be transformed to create new examples while "
            "preserving the intended label or behavior.\n"
            "\n"
            "For images:\n"
            "\n"
            "- Crop.\n"
            "- Rotate.\n"
            "- Scale.\n"
            "- Flip.\n"
            "- Change brightness.\n"
            "- Add noise.\n"
            "\n"
            "For text:\n"
            "\n"
            "- Replace words with semantically similar words.\n"
            "- Rephrase.\n"
            "- Translate.\n"
            "- Introduce realistic typos/noise.\n"
            "\n"
            "Transformations can also be designed to reduce bias, such as swapping "
            "gendered terms when the target label should remain unchanged.\n"
            "\n"
            "**Perturbation** deliberately adds small changes. Training on perturbed "
            "examples can improve robustness against naturally noisy inputs and attacks.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Simulation\n"
            "\n"
            "Some data is dangerous, expensive, or rare to collect in the real world.\n"
            "\n"
            "Simulation can create it safely and cheaply.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- Self-driving edge cases.\n"
            "- Robot manipulation trajectories.\n"
            "- Manufacturing defects.\n"
            "- Financial rare events.\n"
            "- Extreme weather scenarios.\n"
            "- Tool-use trajectories for AI agents.\n"
            "\n"
            "A simulated environment is always an approximation. This creates a "
            "**sim-to-real** challenge: a system that succeeds in simulation may "
            "still fail in reality.\n"
            "\n"
            "However, simulation is often extremely useful for exploring many "
            "possible action sequences and retaining only successful or efficient ones.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. AI-powered data synthesis\n"
            "\n"
            "Foundation models expand the range of data that can be generated "
            "programmatically.\n"
            "\n"
            "They can simulate:\n"
            "\n"
            "- API outputs.\n"
            "- Customer interactions.\n"
            "- Tool-use environments.\n"
            "- Games and self-play.\n"
            "- Natural-language instructions.\n"
            "- Explanations and documentation.\n"
            "- Code.\n"
            "- Images and other media.\n"
            "\n"
            "AI synthesis is especially attractive for post-training data because "
            "instruction and preference data is expensive for humans to create.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Self-play and simulated participants\n"
            "\n"
            "AI can generate both sides of an interaction.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- Chess or Go agents playing against themselves.\n"
            "- Negotiation agents using different strategies.\n"
            "- A simulated customer talking to a simulated support assistant.\n"
            "\n"
            "Self-play can generate far more interaction data than humans can "
            "produce manually, but success depends on the realism and diversity "
            "of the simulated participants.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Paraphrasing, translation, and back-translation\n"
            "\n"
            "A model can transform one good example into many surface forms.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "How to reset my password?\n"
            " -> I forgot my password.\n"
            " -> How can I change my password?\n"
            " -> What are the steps to reset a password?\n"
            "```\n"
            "\n"
            "Translation can transfer datasets from high-resource languages into "
            "low-resource languages.\n"
            "\n"
            "### Back-translation verification\n"
            "\n"
            "```text\n"
            "English X\n"
            " -> translate to Lao Y\n"
            " -> translate Y back to English X'\n"
            " -> compare X with X'\n"
            "```\n"
            "\n"
            "A large mismatch suggests the translation may be poor.\n"
            "\n"
            "The same idea can verify generated code explanations or documentation: "
            "generate text from code, regenerate code from the text, then compare or "
            "execute the regenerated code.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Synthesizing instruction data\n"
            "\n"
            "Instruction finetuning needs instructions and responses. AI can generate:\n"
            "\n"
            "- Instructions only.\n"
            "- Responses only.\n"
            "- Both.\n"
            "\n"
            "A structured workflow starts with a **coverage plan**:\n"
            "\n"
            "1. Define topics, keywords, task types, or templates.\n"
            "2. Generate instructions for each region.\n"
            "3. Generate one or more candidate responses.\n"
            "4. Verify and filter.\n"
            "5. Measure coverage and generate additional examples where gaps remain.\n"
            "\n"
            "Seed examples can anchor style and task diversity. The chapter discusses "
            "well-known instruction datasets created by expanding a small set of "
            "seed examples into tens of thousands of synthetic examples.\n"
            "\n"
            "[[IMAGE_NEEDED: Instruction-data synthesis pipeline | Seed tasks/topics "
            "feeding instruction generation, response generation, verification, "
            "filtering, and final SFT dataset | Learner should notice that generation "
            "must be followed by verification and coverage analysis]]\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Reverse instruction\n"
            "\n"
            "Generating long, factual responses from scratch increases the chance "
            "of hallucination.\n"
            "\n"
            "Reverse instruction flips the direction:\n"
            "\n"
            "```text\n"
            "existing high-quality content\n"
            " -> AI generates an instruction/question\n"
            " -> pair instruction with the trusted content as response\n"
            "```\n"
            "\n"
            "This can turn reliable long-form text—such as articles, stories, or "
            "documentation—into instruction data without asking AI to invent the "
            "long response itself.\n"
            "\n"
            "A model can even be bootstrapped iteratively:\n"
            "\n"
            "1. Train a weak model from a small seed set.\n"
            "2. Generate instructions for trusted content.\n"
            "3. Finetune on the new pairs.\n"
            "4. Repeat and verify improvement.\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Synthetic data for long-context behavior\n"
            "\n"
            "A useful long-context synthesis pattern is:\n"
            "\n"
            "1. Take a long document.\n"
            "2. Split it into short chunks the current model can process reliably.\n"
            "3. Generate question-answer pairs from each chunk.\n"
            "4. During training, provide the **full long document** as context for "
            "those questions.\n"
            "\n"
            "The model learns to find and use relevant evidence inside a much larger context.\n"
            "\n"
            "---\n"
            "\n"

            "## 28. A high-quality coding-data synthesis pipeline\n"
            "\n"
            "Coding is especially suitable for synthetic data because outputs can "
            "be executed and tested.\n"
            "\n"
            "The chapter describes a pipeline with ideas such as:\n"
            "\n"
            "1. Generate diverse programming problems.\n"
            "2. Generate candidate solutions.\n"
            "3. Parse/lint the code.\n"
            "4. Generate and run unit tests.\n"
            "5. Feed execution errors back to the model for correction.\n"
            "6. Keep only solutions that pass the checks.\n"
            "7. Translate correct code into other programming languages.\n"
            "8. Filter translations with execution tests.\n"
            "9. Generate explanations/documentation.\n"
            "10. Verify them through back-translation into code.\n"
            "\n"
            "This illustrates a major theme of dataset engineering:\n"
            "\n"
            "> Synthesis becomes far more valuable when paired with automatic verification.\n"
            "\n"
            "[[IMAGE_NEEDED: Verified coding-data synthesis | Program problem -> "
            "generated code -> parser/linter -> unit tests -> correction loop -> "
            "verified example, with optional translation/back-translation branches | "
            "Learner should notice that bad generated examples are rejected rather "
            "than blindly added to training]]\n"
            "\n"
            "---\n"
            "\n"

            "## 29. Verify synthetic and real training data\n"
            "\n"
            "Synthetic data should be evaluated before training, using many of the "
            "same methods used to evaluate model outputs.\n"
            "\n"
            "### Functional correctness\n"
            "\n"
            "Use when outputs can be executed or objectively checked.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- Code passes tests.\n"
            "- SQL returns expected rows.\n"
            "- Structured output passes validation.\n"
            "\n"
            "### AI verifiers / judges\n"
            "\n"
            "Ask a model to score or classify examples against explicit quality criteria.\n"
            "\n"
            "### Factuality checks\n"
            "\n"
            "Filter examples likely to contain unsupported claims or hallucinations.\n"
            "\n"
            "### Topic filters\n"
            "\n"
            "Remove examples outside the target domain.\n"
            "\n"
            "### Anomaly detection\n"
            "\n"
            "Identify unusual examples that may represent corruption or low quality.\n"
            "\n"
            "### Heuristics\n"
            "\n"
            "Remove examples that are:\n"
            "\n"
            "- Empty.\n"
            "- Too short/too long for the use case.\n"
            "- Repetitive.\n"
            "- Same instruction with conflicting responses.\n"
            "- Outputs that simply repeat the inputs.\n"
            "\n"
            "The ultimate verification remains empirical: does training on the "
            "dataset improve the target model on the target evaluation set?\n"
            "\n"
            "{{exercise:M08.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 30. Limitation 1: quality control\n"
            "\n"
            "Synthetic data can be wrong, shallow, repetitive, biased, or "
            "hallucinated. If you cannot verify generated examples, you should be "
            "cautious about using them as training truth.\n"
            "\n"
            "Synthetic generation reduces the cost of **creating candidates**. It "
            "does not eliminate the cost of deciding which candidates are trustworthy.\n"
            "\n"
            "---\n"
            "\n"

            "## 31. Limitation 2: superficial imitation\n"
            "\n"
            "A student can learn to imitate the **style** of a strong teacher "
            "without acquiring the teacher's underlying reasoning capability.\n"
            "\n"
            "This is dangerous because the student may learn to produce outputs "
            "that **look like correct solutions** even when it cannot actually solve "
            "the problem.\n"
            "\n"
            "The chapter therefore warns against interpreting imitation quality as "
            "proof of factual accuracy or general reasoning improvement.\n"
            "\n"
            "---\n"
            "\n"

            "## 32. Limitation 3: model collapse and feedback loops\n"
            "\n"
            "Repeatedly training models on recursively generated data can distort "
            "the data distribution.\n"
            "\n"
            "A model tends to generate common/high-probability events more often "
            "than rare events. If its outputs become the next generation's training "
            "data, rare patterns may shrink further. Repeating the process can cause "
            "the model to forget tails of the real distribution.\n"
            "\n"
            "This phenomenon is often called **model collapse**.\n"
            "\n"
            "Research discussed in the chapter suggests that keeping real data in "
            "the mix can reduce this risk, although no universal synthetic-to-real "
            "ratio is established.\n"
            "\n"
            "Feedback loops can also amplify existing biases.\n"
            "\n"
            "[[IMAGE_NEEDED: Synthetic-data feedback loop | Real distribution -> "
            "model -> synthetic dataset biased toward common cases -> next model -> "
            "even narrower distribution, with rare cases fading | Learner should "
            "notice how repeated synthetic-only training can erase the tails]]\n"
            "\n"
            "---\n"
            "\n"

            "## 33. Limitation 4: obscured data lineage\n"
            "\n"
            "When model X generates data, the generated example may indirectly "
            "reflect model X's unknown training data.\n"
            "\n"
            "This creates several risks:\n"
            "\n"
            "- Copyright or licensing problems can propagate indirectly.\n"
            "- A benchmark may contaminate your training data through the teacher model.\n"
            "- It becomes harder to audit where particular information originated.\n"
            "- Commercial viability may be difficult to assess without provenance.\n"
            "\n"
            "Data lineage therefore matters even when examples are synthetic.\n"
            "\n"
            "---\n"
            "\n"

            "## 34. Model distillation\n"
            "\n"
            "**Knowledge distillation** trains a smaller **student** model to imitate "
            "a larger or stronger **teacher** model.\n"
            "\n"
            "The goal is usually deployment efficiency:\n"
            "\n"
            "- Smaller model.\n"
            "- Faster inference.\n"
            "- Lower cost.\n"
            "- Similar task performance where possible.\n"
            "\n"
            "The student can be trained from scratch or finetuned from a pre-trained model.\n"
            "\n"
            "Not all synthetic-data training is distillation. It is distillation "
            "when the teacher's behavior is explicitly the target the student is "
            "expected to reproduce.\n"
            "\n"
            "The teacher does not always need fewer parameters than the student; "
            "synthetic data can also bootstrap a more capable student when the "
            "teacher's generated examples are carefully verified.\n"
            "\n"
            "Always check model licenses: some prohibit using outputs to train "
            "other or competing models.\n"
            "\n"
            "---\n"
            "\n"

            "## 35. Data-processing principles\n"
            "\n"
            "Large-scale data processing can take hours or days. Process in an "
            "order that saves compute.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- If deduplication is cheap, remove duplicates before expensive cleaning.\n"
            "- If low-quality filtering is cheap, remove bad data before expensive deduplication.\n"
            "\n"
            "Two practical rules from the chapter are especially important:\n"
            "\n"
            "### Trial-run processing scripts\n"
            "\n"
            "Run on a small sample before applying to the full dataset.\n"
            "\n"
            "### Avoid destructive in-place processing\n"
            "\n"
            "Keep the original data because:\n"
            "\n"
            "- Another use case may need different processing.\n"
            "- A buggy script can corrupt the transformed dataset.\n"
            "\n"
            "---\n"
            "\n"

            "## 36. Inspect the data before training\n"
            "\n"
            "Before building complex processing pipelines, understand what you have.\n"
            "\n"
            "Inspect metadata such as:\n"
            "\n"
            "- Source and provenance.\n"
            "- Previous processing.\n"
            "- Past uses.\n"
            "\n"
            "Plot distributions such as:\n"
            "\n"
            "- Token frequencies.\n"
            "- Input lengths.\n"
            "- Response lengths.\n"
            "- Topics.\n"
            "- Languages.\n"
            "- Scores.\n"
            "- Annotators.\n"
            "- Time periods.\n"
            "\n"
            "Look for outliers and unexpected clusters.\n"
            "\n"
            "### Inter-annotator disagreement\n"
            "\n"
            "If several annotators label the same example, measure disagreement and "
            "inspect conflicts. Large disagreement can reveal ambiguous guidelines "
            "or inconsistent annotators.\n"
            "\n"
            "### Manual inspection still matters\n"
            "\n"
            "Data dashboards are not substitutes for reading actual examples. "
            "Manually inspect queries, labels, responses, contradictions, duplicates, "
            "and factual claims. A few minutes of direct inspection can reveal "
            "problems that statistics hide.\n"
            "\n"
            "[[IMAGE_NEEDED: Dataset inspection dashboard | Histograms for input "
            "length, response length, language, topic, and annotator score alongside "
            "a manual-example viewer | Learner should notice that aggregate "
            "statistics and raw-example inspection complement each other]]\n"
            "\n"
            "---\n"
            "\n"

            "## 37. Deduplicate data\n"
            "\n"
            "Duplicates distort the training distribution, waste compute, and can "
            "cause train/test contamination.\n"
            "\n"
            "Duplicates can occur at multiple levels:\n"
            "\n"
            "- Whole-document duplicates.\n"
            "- Repeated paragraphs inside one document.\n"
            "- Shared passages across documents.\n"
            "- Near-duplicates with small edits.\n"
            "\n"
            "You must define what 'duplicate' means for your application:\n"
            "\n"
            "- Exact equality?\n"
            "- 80% overlap?\n"
            "- Same items in a different order?\n"
            "- Same semantic meaning with different wording?\n"
            "\n"
            "### Pairwise similarity\n"
            "\n"
            "Compare examples using exact match, n-gram overlap, fuzzy matching, "
            "or semantic similarity. Powerful but expensive at large scale.\n"
            "\n"
            "### Hashing\n"
            "\n"
            "Map likely-similar examples into buckets and compare within buckets. "
            "The chapter mentions techniques such as MinHash and Bloom filters.\n"
            "\n"
            "### Dimensionality reduction / vector-search ideas\n"
            "\n"
            "Reduce representation dimensionality or use approximate-neighbor "
            "methods to narrow candidate duplicate pairs before expensive comparison.\n"
            "\n"
            "[[IMAGE_NEEDED: Deduplication strategies | Three branches showing "
            "pairwise similarity, hashing/bucketing, and vector/dimensionality "
            "reduction candidate search | Learner should notice the tradeoff "
            "between exhaustive accuracy and scalable candidate filtering]]\n"
            "\n"
            "---\n"
            "\n"

            "## 38. Clean and filter data\n"
            "\n"
            "Cleaning should improve model quality, safety, and compliance.\n"
            "\n"
            "Common operations include:\n"
            "\n"
            "- Remove irrelevant HTML/Markdown artifacts.\n"
            "- Normalize whitespace and formatting.\n"
            "- Remove fields the model should not see.\n"
            "- Remove PII or sensitive data when policy requires it.\n"
            "- Remove unlicensed/copyright-problematic data when required.\n"
            "- Filter toxic or unsafe data based on application policy.\n"
            "- Remove low-quality examples using verification methods.\n"
            "\n"
            "Manual inspection can reveal useful filtering heuristics. The chapter "
            "also notes that annotation quality can change during long annotation "
            "sessions, illustrating why metadata such as annotator and time can be useful.\n"
            "\n"
            "If you have more data than your compute budget allows, techniques such "
            "as active learning, importance sampling, or data pruning can help "
            "select examples believed to be most useful.\n"
            "\n"
            "---\n"
            "\n"

            "## 39. Format data exactly as the model expects\n"
            "\n"
            "After cleaning and deduplication, convert examples into the tokenizer "
            "and chat template expected by the base model.\n"
            "\n"
            "Incorrect formatting can create subtle model bugs.\n"
            "\n"
            "For SFT, data may look conceptually like:\n"
            "\n"
            "```text\n"
            "(instruction, response)\n"
            "```\n"
            "\n"
            "A prompt used during few-shot prompting can often be decomposed into "
            "individual training examples. After finetuning, the inference prompt "
            "may become much shorter because examples no longer need to be repeated "
            "inside every request.\n"
            "\n"
            "The inference format should remain consistent with the format used "
            "during finetuning. Small changes in separators, prefixes, spaces, or "
            "special tokens can affect behavior.\n"
            "\n"
            "{{exercise:M08.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> More training data is always better.\n"
            "\n"
            "**Why this is wrong:** noisy, duplicated, irrelevant, or badly mixed "
            "data can make a model worse while increasing cost.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Data quality just means the answer is factually correct.\n"
            "\n"
            "**Why this is wrong:** quality also includes relevance, alignment with "
            "task requirements, consistency, formatting, uniqueness, and compliance.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> Human-generated data is always higher quality than synthetic data.\n"
            "\n"
            "**Why this is wrong:** humans can be inconsistent, tired, or poorly "
            "matched to AI-native workflows. Synthetic data can be strong when it "
            "is targeted and verifiable.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> Synthetic data eliminates the need for humans.\n"
            "\n"
            "**Why this is wrong:** humans are still needed to define desired "
            "behavior, guidelines, edge cases, policies, and validation criteria.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> If an AI-generated example looks realistic, it is good training data.\n"
            "\n"
            "**Why this is wrong:** style can be convincing while facts, reasoning, "
            "or generalization are wrong.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> Training only on self-generated data is a safe way to improve forever.\n"
            "\n"
            "**Why this is wrong:** recursive synthetic-data feedback can narrow "
            "the distribution and cause model collapse or bias amplification.\n"
            "\n"
            "### Misconception 7\n"
            "\n"
            "> Distillation means all synthetic-data training.\n"
            "\n"
            "**Why this is wrong:** distillation specifically treats a teacher "
            "model's behavior as the target for a student.\n"
            "\n"
            "### Misconception 8\n"
            "\n"
            "> Deduplication only means removing exact duplicate rows.\n"
            "\n"
            "**Why this is wrong:** duplication can occur at document, paragraph, "
            "sentence, n-gram, or semantic levels.\n"
            "\n"
            "### Misconception 9\n"
            "\n"
            "> Data processing can be safely applied directly to the only copy.\n"
            "\n"
            "**Why this is wrong:** processing bugs can corrupt data and different "
            "applications may need different transformations.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Dataset engineering | Designing and processing data so it teaches the desired model behavior. |\n"
            "| Data-centric AI | Improving AI performance by improving data rather than primarily changing the model. |\n"
            "| Data curation | Selecting, balancing, creating, and removing examples for a training objective. |\n"
            "| Data quality | Degree to which examples are useful, reliable, relevant, consistent, formatted, unique, and compliant. |\n"
            "| Data coverage | How well the dataset represents the range of situations the model must handle. |\n"
            "| Data quantity | Amount of training data, measured appropriately for the training stage. |\n"
            "| Data mix | Relative proportion of domains/tasks/example types in the dataset. |\n"
            "| Annotation guideline | Explicit criteria telling annotators how to produce consistent labels/responses. |\n"
            "| Data flywheel | Product loop where application data is used to improve the product and generate better future data. |\n"
            "| Data augmentation | Creating new examples by transforming real examples. |\n"
            "| Synthetic data | Artificially generated data intended to model useful properties of real data. |\n"
            "| Procedural generation | Rule/program-based automatic generation of data or environments. |\n"
            "| Perturbation | Introducing controlled noise or modifications to an example. |\n"
            "| Simulation | Generating data inside a modeled environment instead of the real world. |\n"
            "| Self-play | Agents/models generating interactions by playing against themselves or other agents. |\n"
            "| Back-translation | Translate/generated-transform an example forward and then back to check faithfulness. |\n"
            "| Reverse instruction | Generate an instruction that would elicit an existing high-quality response. |\n"
            "| AI verifier | Model used to score/filter generated training examples. |\n"
            "| Model collapse | Distribution degradation from recursive reliance on generated data. |\n"
            "| Data lineage | Record of where data originated and how it was transformed. |\n"
            "| Knowledge distillation | Training a student model to imitate a teacher model. |\n"
            "| Deduplication | Detecting/removing duplicate or near-duplicate examples. |\n"
            "| MinHash | Hashing method often used to estimate set similarity efficiently. |\n"
            "| Bloom filter | Probabilistic data structure useful for efficient membership/duplicate checks. |\n"
            "| Inter-annotator disagreement | Degree to which annotators differ on the same examples. |\n"
            "| Active learning | Selecting particularly informative examples for labeling/training. |\n"
            "| Importance sampling | Sampling examples according to estimated importance for the objective. |\n"
            "| Chat template | Exact formatting structure expected by a conversational model. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What is dataset engineering trying to optimize?\n"
            "2. How does data-centric AI differ from model-centric AI?\n"
            "3. What data format is typical for SFT?\n"
            "4. What data format is typical for preference finetuning?\n"
            "5. Why is complex reasoning data expensive to annotate?\n"
            "6. Why might human tool-use traces be inefficient training targets for AI agents?\n"
            "7. What does multi-turn data teach that single-turn data does not?\n"
            "8. What are the three core data-curation criteria?\n"
            "9. Name the six data-quality characteristics discussed in the lesson.\n"
            "10. Why can a factually correct annotation still be misaligned with the task?\n"
            "11. What dimensions of diversity matter for your own application?\n"
            "12. Why can adding heterogeneous data hurt performance?\n"
            "13. What is a data mix?\n"
            "14. Which factors determine how much finetuning data you need?\n"
            "15. Why might a stronger base model need fewer examples?\n"
            "16. How can a dataset-size performance curve guide annotation spending?\n"
            "17. What does a plateau in the curve suggest?\n"
            "18. Why might you use raw domain text before expensive labeled data?\n"
            "19. Why is application data particularly valuable?\n"
            "20. What is a data flywheel?\n"
            "21. Why should public dataset licenses and provenance be inspected?\n"
            "22. Why are annotation guidelines reusable for evaluation?\n"
            "23. Distinguish augmentation from synthesis.\n"
            "24. Give two reasons to synthesize data beyond simply increasing quantity.\n"
            "25. What is the strength and weakness of template-based generation?\n"
            "26. How can perturbation improve robustness?\n"
            "27. What is the sim-to-real problem?\n"
            "28. What is self-play useful for?\n"
            "29. How does back-translation help verify generated data?\n"
            "30. What should an instruction-data coverage plan contain?\n"
            "31. What problem does reverse instruction reduce?\n"
            "32. How can synthetic QA examples be used to teach long-context behavior?\n"
            "33. Why is code especially suitable for synthetic training data?\n"
            "34. Name four ways to verify generated data.\n"
            "35. Why is functional verification stronger than visual plausibility when available?\n"
            "36. What is superficial imitation?\n"
            "37. Explain model collapse intuitively.\n"
            "38. How can real-data mixing reduce recursive synthetic-data risk?\n"
            "39. Why does synthetic generation obscure lineage?\n"
            "40. What distinguishes distillation from ordinary synthetic-data training?\n"
            "41. Why should processing scripts be trial-run first?\n"
            "42. Why should raw data be preserved?\n"
            "43. Which distributions should you inspect before training?\n"
            "44. What can inter-annotator disagreement reveal?\n"
            "45. Why is manual inspection still important?\n"
            "46. How can duplicates contaminate train/test evaluation?\n"
            "47. Compare pairwise, hashing, and vector-based deduplication.\n"
            "48. What kinds of data might need to be removed for compliance?\n"
            "49. How can active learning/data pruning help when compute is limited?\n"
            "50. Why must inference prompts match the finetuning format closely?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A training dataset is a behavioral specification expressed through "
            "examples. Strong dataset engineering does not maximize row count; it "
            "deliberately chooses what the model should learn, covers the situations "
            "that matter, verifies every possible shortcut, preserves provenance "
            "and compliance, and measures whether each new batch of data actually "
            "improves the model.**\n"
        ),

        "estimated_minutes": 330,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "dataset-engineering", "title": "What dataset engineering is", "order": 1},
            {"id": "data-centric-ai", "title": "Data-centric AI", "order": 2},
            {"id": "data-by-training-stage", "title": "Data by training stage", "order": 3},
            {"id": "behavior-data", "title": "Behavior in training data", "order": 4},
            {"id": "cot-data", "title": "Reasoning data", "order": 5},
            {"id": "tool-use-data", "title": "Tool-use data", "order": 6},
            {"id": "single-multi-turn", "title": "Single-turn and multi-turn data", "order": 7},
            {"id": "golden-trio", "title": "Quality, coverage, quantity", "order": 8},
            {"id": "data-quality", "title": "Data quality", "order": 9},
            {"id": "data-coverage", "title": "Data coverage", "order": 10},
            {"id": "data-mix", "title": "Data mix", "order": 11},
            {"id": "data-quantity", "title": "Data quantity", "order": 12},
            {"id": "data-scaling-curves", "title": "Data scaling curves", "order": 13},
            {"id": "curriculum-data", "title": "Staged data strategies", "order": 14},
            {"id": "data-acquisition", "title": "Data acquisition", "order": 15},
            {"id": "annotation", "title": "Annotation guidelines", "order": 16},
            {"id": "augmentation-vs-synthesis", "title": "Augmentation versus synthesis", "order": 17},
            {"id": "why-synthetic-data", "title": "Why synthetic data", "order": 18},
            {"id": "rule-based-synthesis", "title": "Rule-based synthesis", "order": 19},
            {"id": "transformations-perturbation", "title": "Transformations and perturbation", "order": 20},
            {"id": "simulation", "title": "Simulation", "order": 21},
            {"id": "ai-synthesis", "title": "AI-powered synthesis", "order": 22},
            {"id": "self-play", "title": "Self-play", "order": 23},
            {"id": "paraphrase-translation", "title": "Paraphrasing and translation", "order": 24},
            {"id": "instruction-synthesis", "title": "Instruction-data synthesis", "order": 25},
            {"id": "reverse-instruction", "title": "Reverse instruction", "order": 26},
            {"id": "long-context-synthesis", "title": "Long-context synthesis", "order": 27},
            {"id": "code-synthesis", "title": "Coding-data synthesis", "order": 28},
            {"id": "data-verification", "title": "Data verification", "order": 29},
            {"id": "synthetic-limitations", "title": "Synthetic-data quality limitations", "order": 30},
            {"id": "imitation-limit", "title": "Superficial imitation", "order": 31},
            {"id": "model-collapse", "title": "Model collapse", "order": 32},
            {"id": "data-lineage", "title": "Data lineage", "order": 33},
            {"id": "distillation", "title": "Model distillation", "order": 34},
            {"id": "processing-principles", "title": "Data-processing principles", "order": 35},
            {"id": "inspect-data", "title": "Inspect data", "order": 36},
            {"id": "deduplication", "title": "Deduplicate data", "order": 37},
            {"id": "clean-filter", "title": "Clean and filter data", "order": 38},
            {"id": "format-data", "title": "Format data", "order": 39},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M08.L01.EX01",

            "title": "Design the Dataset Before Collecting It",

            "lesson_code": "M08.L01",

            "section_id": "data-scaling-curves",

            "placement": "after_section",

            "description": (
                "Turn a model behavior requirement into a concrete data-quality, "
                "coverage, and quantity plan."
            ),

            "instructions": (
                "Imagine you are finetuning a customer-support model for an online "
                "store.\n\n"
                "1. Define five behaviors the model should learn.\n"
                "2. Define two behaviors you explicitly do not want in the data.\n"
                "3. Decide whether you need single-turn, multi-turn, or both.\n"
                "4. Define six important data-coverage slices (for example topic, "
                "language, input length, typo rate, customer type, output format).\n"
                "5. Define what 'high quality' means using the six quality "
                "characteristics from the lesson.\n"
                "6. Propose an initial small pilot dataset size.\n"
                "7. Explain how you would train on 25%, 50%, and 100% subsets to "
                "estimate the value of collecting more data.\n"
                "8. Define what evidence would convince you that additional data "
                "has reached diminishing returns."
            ),

            "expected_output": (
                "A dataset design specification containing desired behaviors, "
                "coverage dimensions, quality criteria, pilot quantity, and a "
                "performance-scaling experiment."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "data-curation",
                "data-quality",
                "data-coverage",
                "data-quantity",
                "experiment-design",
            ],
        },

        {
            "id": "M08.L01.EX02",

            "title": "Build a Verified Synthetic-Data Pipeline",

            "lesson_code": "M08.L01",

            "section_id": "data-verification",

            "placement": "after_section",

            "description": (
                "Design synthetic-data generation together with verification so "
                "generated examples are not treated as truth automatically."
            ),

            "instructions": (
                "You want 20,000 training examples for a model that converts natural "
                "language into SQL.\n\n"
                "1. Create a coverage plan across schema complexity and query types.\n"
                "2. Decide which parts will come from real seed data and which will "
                "be synthetic.\n"
                "3. Design instruction generation.\n"
                "4. Design SQL response generation.\n"
                "5. Define deterministic checks: parser, schema validation, and SQL "
                "execution against test databases.\n"
                "6. Define what should happen to failed examples.\n"
                "7. Add a deduplication step.\n"
                "8. Add one AI-judge or semantic-quality check that deterministic "
                "execution cannot capture.\n"
                "9. Define how you will measure topic/query-type coverage after filtering.\n"
                "10. Explain how you will prevent benchmark contamination and record lineage.\n"
                "11. Define a held-out model evaluation to determine whether the "
                "synthetic dataset actually improves the system."
            ),

            "expected_output": (
                "A generation-and-verification pipeline with coverage targets, "
                "functional checks, rejection/correction loops, deduplication, "
                "lineage controls, and downstream model evaluation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "synthetic-data",
                "functional-verification",
                "instruction-data",
                "deduplication",
                "data-lineage",
            ],
        },

        {
            "id": "M08.L01.EX03",

            "title": "Audit and Process a Raw Training Dataset",

            "lesson_code": "M08.L01",

            "section_id": "format-data",

            "placement": "after_section",

            "description": (
                "Create a practical processing order for a messy instruction dataset."
            ),

            "instructions": (
                "Assume you receive 500,000 raw instruction-response examples from "
                "public datasets, internal application logs, and synthetic generation.\n\n"
                "1. List the source/provenance metadata you need to preserve.\n"
                "2. Define the first statistics and distributions you would inspect.\n"
                "3. Define a manual inspection sample.\n"
                "4. Design exact and near-duplicate detection.\n"
                "5. Define PII/licensing/toxicity/compliance filters.\n"
                "6. Define quality heuristics and AI-verification steps.\n"
                "7. Choose an efficient order for deduplication, filtering, and "
                "expensive verification, and justify it.\n"
                "8. Define how inter-annotator disagreement would be analyzed.\n"
                "9. Define how to select examples if your compute budget allows "
                "training on only 150,000 of the 500,000 examples.\n"
                "10. Define the final model chat-template conversion.\n"
                "11. Explain how you will protect the original raw dataset from "
                "processing-script bugs.\n"
                "12. Define the checks you run on a small trial before processing "
                "all 500,000 examples."
            ),

            "expected_output": (
                "An ordered data-processing plan covering inspection, provenance, "
                "deduplication, quality/compliance filtering, selection, formatting, "
                "trial runs, and reproducibility."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "data-inspection",
                "data-processing",
                "deduplication",
                "data-compliance",
                "data-formatting",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M08.L01.QZ01",

        "title": "Dataset Engineering — Knowledge Check",

        "lesson_code": "M08.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M08.L01.Q01",
                "section_id": "data-centric-ai",
                "question": "What best describes data-centric AI?",
                "options": [
                    "Improving system performance by improving the training data",
                    "Increasing model parameter count only",
                    "Replacing evaluation with more training",
                    "Using only synthetic data",
                ],
                "correct": 0,
                "explanation": (
                    "Data-centric AI focuses on dataset quality, diversity, labels, "
                    "coverage, and processing while keeping the model comparatively fixed."
                ),
            },
            {
                "id": "M08.L01.Q02",
                "section_id": "data-by-training-stage",
                "question": (
                    "Which data format is most directly associated with preference finetuning?"
                ),
                "options": [
                    "(instruction, winning response, losing response)",
                    "(raw text sequence only)",
                    "(image, bounding box) only",
                    "(query, vector embedding) only",
                ],
                "correct": 0,
                "explanation": (
                    "Preference finetuning learns from comparative examples indicating "
                    "which response is preferred."
                ),
            },
            {
                "id": "M08.L01.Q03",
                "section_id": "golden-trio",
                "question": "What are the three core dataset-curation criteria?",
                "options": [
                    "Quality, coverage, quantity",
                    "Accuracy, latency, throughput",
                    "Prompt, model, tool",
                    "Weights, gradients, optimizer",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter frames dataset design around quality, coverage/diversity, "
                    "and quantity."
                ),
            },
            {
                "id": "M08.L01.Q04",
                "section_id": "data-quality",
                "question": (
                    "A response is factually correct but far too verbose for a task "
                    "that requires concise answers. Which quality property is violated?"
                ),
                "options": [
                    "Alignment with task requirements",
                    "Uniqueness only",
                    "Data quantity",
                    "Simulation fidelity",
                ],
                "correct": 0,
                "explanation": (
                    "Quality means matching the target behavior, not merely factual correctness."
                ),
            },
            {
                "id": "M08.L01.Q05",
                "section_id": "data-coverage",
                "question": (
                    "Why might a support dataset include realistic typos in user queries?"
                ),
                "options": [
                    "To cover a pattern that appears in real usage",
                    "To make annotations less consistent",
                    "To increase duplicate count",
                    "To prevent tokenization",
                ],
                "correct": 0,
                "explanation": (
                    "Coverage should reflect the real distribution of user inputs, "
                    "including noisy or imperfect text where relevant."
                ),
            },
            {
                "id": "M08.L01.Q06",
                "section_id": "data-scaling-curves",
                "question": (
                    "What does a strongly flattening performance-vs-dataset-size curve suggest?"
                ),
                "options": [
                    "Additional examples are giving diminishing returns",
                    "The dataset definitely contains no duplicates",
                    "Full finetuning is impossible",
                    "The base model must be replaced immediately",
                ],
                "correct": 0,
                "explanation": (
                    "A plateau means that increasing quantity is producing smaller "
                    "marginal gains under the current setup."
                ),
            },
            {
                "id": "M08.L01.Q07",
                "section_id": "annotation",
                "question": "Why are annotation guidelines critical?",
                "options": [
                    "They make task requirements explicit and improve consistency",
                    "They eliminate the need for evaluation",
                    "They guarantee every annotator is a domain expert",
                    "They automatically deduplicate the data",
                ],
                "correct": 0,
                "explanation": (
                    "Clear guidelines make expected quality and edge-case handling "
                    "consistent across annotators and examples."
                ),
            },
            {
                "id": "M08.L01.Q08",
                "section_id": "augmentation-vs-synthesis",
                "question": "What distinguishes augmentation from synthesis?",
                "options": [
                    "Augmentation transforms existing real data; synthesis creates "
                    "artificial examples intended to model useful properties",
                    "Augmentation always uses LLMs; synthesis never uses LLMs",
                    "Only synthesis can produce images",
                    "Only augmentation can be automated",
                ],
                "correct": 0,
                "explanation": (
                    "Augmentation starts from an existing example, whereas synthesis "
                    "can create a new artificial example without a corresponding real source."
                ),
            },
            {
                "id": "M08.L01.Q09",
                "section_id": "simulation",
                "question": "Why use simulation for rare or dangerous events?",
                "options": [
                    "It can generate controlled examples without real-world risk",
                    "Simulation perfectly reproduces reality",
                    "It guarantees no distribution shift",
                    "It removes the need for validation",
                ],
                "correct": 0,
                "explanation": (
                    "Simulation is safer and cheaper for many rare situations, but "
                    "sim-to-real differences still require evaluation."
                ),
            },
            {
                "id": "M08.L01.Q10",
                "section_id": "paraphrase-translation",
                "question": "What is the purpose of back-translation?",
                "options": [
                    "Check whether a transformation preserved the original meaning/content",
                    "Increase the model's parameter count",
                    "Deduplicate exact strings only",
                    "Select an optimizer",
                ],
                "correct": 0,
                "explanation": (
                    "If translating back produces content very different from the "
                    "original, the intermediate translation may be poor."
                ),
            },
            {
                "id": "M08.L01.Q11",
                "section_id": "reverse-instruction",
                "question": "Why is reverse instruction useful?",
                "options": [
                    "It pairs AI-generated prompts with existing trusted high-quality responses",
                    "It removes all need for prompts",
                    "It guarantees a model will not hallucinate",
                    "It is a quantization method",
                ],
                "correct": 0,
                "explanation": (
                    "Using trusted existing content as the response avoids asking "
                    "AI to invent a long factual response from scratch."
                ),
            },
            {
                "id": "M08.L01.Q12",
                "section_id": "data-verification",
                "question": (
                    "What is the strongest verification method for synthetic code "
                    "when reliable tests are available?"
                ),
                "options": [
                    "Execute it against the tests",
                    "Judge whether it looks professional",
                    "Measure only response length",
                    "Count repeated keywords",
                ],
                "correct": 0,
                "explanation": (
                    "Functional correctness directly tests whether the generated "
                    "artifact performs the intended behavior."
                ),
            },
            {
                "id": "M08.L01.Q13",
                "section_id": "imitation-limit",
                "question": "What is superficial imitation?",
                "options": [
                    "A student copies the teacher's style without acquiring equal "
                    "underlying capability or factual reliability",
                    "The teacher is always smaller than the student",
                    "The dataset contains exact duplicates",
                    "The model is trained with too few epochs",
                ],
                "correct": 0,
                "explanation": (
                    "A model can learn to produce solution-like outputs without "
                    "actually possessing the teacher's reasoning competence."
                ),
            },
            {
                "id": "M08.L01.Q14",
                "section_id": "model-collapse",
                "question": "What is the intuition behind model collapse?",
                "options": [
                    "Recursive generated-data training can overrepresent common "
                    "patterns and lose rare parts of the real distribution",
                    "The GPU runs out of memory during inference",
                    "All synthetic data is always low quality",
                    "A model forgets its tokenizer after distillation",
                ],
                "correct": 0,
                "explanation": (
                    "Generated distributions can progressively narrow if models "
                    "mainly train on outputs from earlier models."
                ),
            },
            {
                "id": "M08.L01.Q15",
                "section_id": "distillation",
                "question": "What defines knowledge distillation?",
                "options": [
                    "A student model is trained to mimic a teacher model's behavior",
                    "All human labels are removed",
                    "Two datasets are concatenated",
                    "The same model generates and trains on unverified outputs",
                ],
                "correct": 0,
                "explanation": (
                    "In distillation, the teacher's behavior is the learning target "
                    "for the student."
                ),
            },
            {
                "id": "M08.L01.Q16",
                "section_id": "inspect-data",
                "question": "Why manually inspect raw examples even after plotting statistics?",
                "options": [
                    "Aggregate statistics can hide semantic, factual, and annotation problems",
                    "Manual inspection automatically fixes all examples",
                    "Statistics are never useful",
                    "It increases the number of training tokens",
                ],
                "correct": 0,
                "explanation": (
                    "Reading real examples can reveal problems that are difficult to "
                    "see from distributions alone."
                ),
            },
            {
                "id": "M08.L01.Q17",
                "section_id": "deduplication",
                "question": "Why are duplicates dangerous across train and test sets?",
                "options": [
                    "They can create evaluation contamination and inflated scores",
                    "They always reduce context length",
                    "They make tokenization impossible",
                    "They automatically violate every license",
                ],
                "correct": 0,
                "explanation": (
                    "A test example duplicated in training no longer measures "
                    "generalization fairly."
                ),
            },
            {
                "id": "M08.L01.Q18",
                "section_id": "clean-filter",
                "question": (
                    "If compute allows only a subset of a much larger clean dataset, "
                    "what is one principled next step?"
                ),
                "options": [
                    "Use importance/active-learning/data-pruning methods to select "
                    "high-value examples",
                    "Always take the first rows",
                    "Duplicate every example once",
                    "Ignore application relevance",
                ],
                "correct": 0,
                "explanation": (
                    "When data exceeds budget, example-selection methods can focus "
                    "training on examples expected to be most useful."
                ),
            },
            {
                "id": "M08.L01.Q19",
                "section_id": "format-data",
                "question": (
                    "Why should inference prompts match the format used during finetuning?"
                ),
                "options": [
                    "The model may learn and rely on separators, prefixes, and chat-template structure",
                    "Formatting determines GPU model size",
                    "It prevents all hallucinations",
                    "It is required only for synthetic data",
                ],
                "correct": 0,
                "explanation": (
                    "Even small formatting differences can shift model behavior "
                    "because the learned training distribution included particular templates."
                ),
            },
            {
                "id": "M08.L01.Q20",
                "section_id": "format-data",
                "type": "open",
                "question": (
                    "You inherit a 300,000-example instruction dataset from five "
                    "sources. Design the dataset-engineering workflow you would use "
                    "before finetuning. Include target behaviors, quality rules, "
                    "coverage analysis, annotation review, synthetic-data policy, "
                    "verification, lineage, deduplication, compliance, filtering, "
                    "formatting, a small pilot run, and the evaluation used to decide "
                    "whether the processed dataset is actually better."
                ),
            },
        ],

        "passing_score": 70,
    },
}
