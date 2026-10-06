"""M10.L02 — People, UX, and Responsible ML Systems.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 11, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M10.L02"

MODULE_ORDER = 10

MODULE_TITLE = "ML Systems, Operations & Responsible AI"

MODULE_DESCRIPTION = (
    "Learn how ML systems are built and run in production: the infrastructure and "
    "tooling behind them (storage and compute, containers, workflow orchestration, "
    "ML platforms, model and feature stores, build-versus-buy), and the human side "
    "(UX for probabilistic systems, team structures, end-to-end ownership, and "
    "Responsible AI)."
)

SOURCE_CHAPTER = 11

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "People, UX, and Responsible ML Systems",

    "slug": "ml-systems-design-m10-l02-people-responsible-ml",

    "description": (
        "A production-focused guide to the human side of ML systems: user experience "
        "under probabilistic behavior, subject-matter experts and team structures, "
        "end-to-end ownership, and Responsible AI (fairness, privacy, transparency, "
        "accountability, and model cards)."
    ),

    "order": 2,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 4.0,

    "skill_tags": [
        "ml-user-experience",
        "consistency-accuracy-tradeoff",
        "human-in-the-loop",
        "smooth-failing",
        "speed-accuracy-tradeoff",
        "cross-functional-collaboration",
        "subject-matter-experts",
        "end-to-end-data-science",
        "responsible-ai",
        "fairness",
        "privacy",
        "transparency",
        "accountability",
        "bias-auditing",
        "disparate-impact",
        "model-cards",
    ],

    "prerequisite_ids": ["M10.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "People, UX, and Responsible ML Systems",

        "content": (
            "# People, UX, and Responsible ML Systems\n"
            "\n"
            "> **Lesson:** M10.L02  \n"
            "> **Module:** ML Systems, Operations & Responsible AI  \n"
            "> **Source alignment:** Chapter 11. Page numbers were not included "
            "in the supplied source. This lesson is an instructor-authored "
            "curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "This lesson continues from M10.L01: once the infrastructure exists, the "
            "remaining production questions are about people, user experience, and "
            "the wider effects of the system.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why probabilistic ML systems create UX challenges that deterministic software often does not.\n"
            "- Explain the consistency-accuracy and speed-accuracy trade-offs.\n"
            "- Design human-in-the-loop and smooth-failing experiences.\n"
            "- Explain why subject-matter experts should participate beyond data labeling.\n"
            "- Compare specialist team structures with end-to-end ML ownership.\n"
            "- Explain why infrastructure abstractions make end-to-end ownership more practical.\n"
            "- Define Responsible AI using fairness, privacy, transparency, and accountability.\n"
            "- Audit bias sources in data, labels, features, objectives, and evaluation.\n"
            "- Explain why anonymization alone may not protect sensitive data.\n"
            "- Explain privacy-accuracy and compactness-fairness trade-offs.\n"
            "- Explain the purpose and structure of model cards.\n"
            "- Explain why responsible-AI processes should begin early and be systematic.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. The human side of ML systems\n"
            "\n"
            "Infrastructure is only part of the production problem. ML systems are built by people, "
            "used by people, and can affect people who never interact directly with the model.\n"
            "\n"
            "Chapter 11 therefore shifts attention to three human dimensions:\n"
            "\n"
            "1. **user experience** under probabilistic model behavior,\n"
            "2. **team structure and collaboration** across technical and domain roles,\n"
            "3. **Responsible AI** and the wider societal effects of model design decisions.\n"
            "\n"
            "This extends the Chapter 10 infrastructure story: tooling should not only make systems scalable; "
            "it should also help people collaborate, understand behavior, and operate systems responsibly.\n"
            "\n"
            "[[IMAGE_NEEDED: Humans around an ML system | "
            "An ML system connected to end users, business stakeholders, data scientists, "
            "platform engineers, subject-matter experts, and wider society | Learner should "
            "notice that system quality depends on technical and human relationships]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Probabilistic systems create different UX problems\n"
            "\n"
            "The chapter highlights three properties that distinguish ML experiences from ordinary software.\n"
            "\n"
            "### Predictions can be inconsistent\n"
            "\n"
            "The same user and apparently similar input can receive different predictions at different times or contexts.\n"
            "\n"
            "### Predictions are mostly correct rather than guaranteed correct\n"
            "\n"
            "A model can be reliable on average while still producing failures whose exact inputs are difficult to predict beforehand.\n"
            "\n"
            "### Inference time can vary\n"
            "\n"
            "Large or sequence-based models can respond quickly to many inputs but take much longer on some queries.\n"
            "\n"
            "These properties affect trust, learnability, predictability, and perceived product quality.\n"
            "\n"
            "[[IMAGE_NEEDED: Deterministic software versus probabilistic ML UX | "
            "A side-by-side comparison of consistent deterministic behavior and probabilistic "
            "mostly-correct behavior with variable latency | Learner should notice why ML interfaces "
            "need explicit design for uncertainty and inconsistency]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Consistency versus accuracy\n"
            "\n"
            "Users expect important interface elements to remain understandable and findable.\n"
            "\n"
            "The chapter's Booking.com example describes an ML system that suggested accommodation filters "
            "based on a user's current browsing behavior.\n"
            "\n"
            "A purely accuracy-driven system could change suggested filters whenever its ranking changed. "
            "But if a filter the user had already relied on suddenly disappeared, the user experience could become confusing.\n"
            "\n"
            "The team therefore defined situations in which recommendations should stay stable and situations in which they could change.\n"
            "\n"
            "This creates the **consistency-accuracy trade-off**:\n"
            "\n"
            "> The currently highest-scoring model prediction is not always the best product decision if changing the interface harms continuity.\n"
            "\n"
            "[[IMAGE_NEEDED: Consistency-accuracy recommendation trade-off | "
            "One interface keeps previously used filters stable while another constantly replaces them with the newest ranked choices | "
            "Learner should notice why UX consistency can justify not serving the instantaneous top prediction]]\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Mostly-correct predictions and human-in-the-loop design\n"
            "\n"
            "A prediction does not need to be perfect to be useful if the user can cheaply recognize and correct errors.\n"
            "\n"
            "A customer-support operator, for example, may save time by editing a mostly-correct generated reply instead of writing from scratch.\n"
            "\n"
            "The same pattern fails when users lack the expertise needed to identify errors. Generated React code is less useful "
            "to a nonprogrammer if the code is broken and the user cannot repair it.\n"
            "\n"
            "One response is to produce multiple candidates and render them in a form the user can judge.\n"
            "\n"
            "```text\n"
            "User request\n"
            "    ↓\n"
            "Several model candidates\n"
            "    ↓\n"
            "Human-evaluable presentation\n"
            "    ↓\n"
            "User chooses or corrects\n"
            "```\n"
            "\n"
            "This is a common **human-in-the-loop** pattern: humans select, correct, or improve machine-generated outputs.\n"
            "\n"
            "[[IMAGE_NEEDED: Human-in-the-loop candidate selection | "
            "One request producing several model outputs rendered into user-evaluable alternatives, "
            "with a human selecting or editing the final result | Learner should notice that good UX "
            "translates model uncertainty into an action the user can understand]]\n"
            "\n"
            "{{exercise:M10.L02.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Smooth failing and the speed-accuracy trade-off\n"
            "\n"
            "A normally fast model can still exceed the latency budget on difficult inputs.\n"
            "\n"
            "The chapter describes using a fallback system that is less accurate but reliably faster.\n"
            "\n"
            "A fallback can be:\n"
            "\n"
            "- a heuristic,\n"
            "- a simpler model,\n"
            "- a cached prediction.\n"
            "\n"
            "```text\n"
            "Main model within latency limit → use main prediction\n"
            "Main model too slow             → use fast fallback\n"
            "```\n"
            "\n"
            "A system can even use another predictor to estimate whether the main model will be too slow for a particular query, "
            "although this routing model also adds some latency.\n"
            "\n"
            "This is a **speed-accuracy trade-off**: under strict latency requirements, a slightly worse prediction delivered in time "
            "can be preferable to a better prediction delivered too late.\n"
            "\n"
            "[[IMAGE_NEEDED: Smooth-failing inference path | "
            "A request routed to a high-quality primary model with a latency threshold and a guaranteed-fast fallback route | "
            "Learner should notice that graceful degradation can protect user experience without abandoning the better model]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Subject-matter experts should participate throughout the lifecycle\n"
            "\n"
            "ML systems often require people with deep domain knowledge—doctors, lawyers, bankers, farmers, stylists, and others.\n"
            "\n"
            "The chapter argues that SMEs should not be treated only as labelers.\n"
            "\n"
            "They can contribute to:\n"
            "\n"
            "- problem formulation,\n"
            "- feature engineering,\n"
            "- labeling and relabeling,\n"
            "- error analysis,\n"
            "- model evaluation,\n"
            "- reranking outputs,\n"
            "- user-interface design.\n"
            "\n"
            "Because production models may require continual labeling and relabeling, SME involvement can be an ongoing responsibility.\n"
            "\n"
            "A collaboration challenge is that domain experts may not use engineering tools such as Git.\n"
            "\n"
            "The chapter recommends involving them early and using low-code/no-code interfaces where appropriate so their expertise "
            "can enter the system without making engineers permanent intermediaries for every contribution.\n"
            "\n"
            "[[IMAGE_NEEDED: SME contributions across the ML lifecycle | "
            "A lifecycle from problem formulation to data, features, evaluation, and UI with SME contribution points at each stage | "
            "Learner should notice that domain expertise is useful far beyond the initial labeling task]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Two team structures, two different failure modes\n"
            "\n"
            "The chapter compares two organizational approaches.\n"
            "\n"
            "### Approach 1: separate production/platform team\n"
            "\n"
            "The data-science team develops a model and another team productionizes it.\n"
            "\n"
            "Advantages:\n"
            "\n"
            "- easier specialization,\n"
            "- easier hiring for narrower roles,\n"
            "- individuals can focus on one concern.\n"
            "\n"
            "Drawbacks emphasized by the source:\n"
            "\n"
            "- communication and coordination overhead,\n"
            "- one team blocking another,\n"
            "- harder cross-team debugging,\n"
            "- finger-pointing about ownership,\n"
            "- no one having enough context to optimize the whole system.\n"
            "\n"
            "### Approach 2: data scientists own the full process\n"
            "\n"
            "This reduces handoffs but expects one role to understand modeling, deployment, containerization, orchestration, "
            "workflows, distributed systems, and operations.\n"
            "\n"
            "The chapter argues that expecting every data scientist to become a low-level infrastructure expert is often unreasonable.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. End-to-end ownership becomes practical when tooling abstracts infrastructure\n"
            "\n"
            "The chapter's solution is not to force everyone to learn every infrastructure detail.\n"
            "\n"
            "Instead, specialists can build tools that let data scientists express what they need at a higher level:\n"
            "\n"
            "- where the data lives,\n"
            "- what workflow steps should run,\n"
            "- where code should execute,\n"
            "- what dependencies each step needs.\n"
            "\n"
            "The infrastructure platform then handles details such as containerization, distributed execution, and failover.\n"
            "\n"
            "This connects directly back to Chapter 10: the purpose of good MLOps infrastructure is partly to let practitioners "
            "own outcomes without personally implementing every underlying system.\n"
            "\n"
            "[[IMAGE_NEEDED: Full-cycle ownership through infrastructure abstractions | "
            "Data scientists defining data, steps, dependencies, and resource requirements above specialist-built infrastructure tools | "
            "Learner should notice how Chapter 10 tooling enables the team model discussed in Chapter 11]]\n"
            "\n"
            "{{exercise:M10.L02.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Responsible AI belongs inside system design\n"
            "\n"
            "The chapter defines Responsible AI around designing, developing, and deploying systems with awareness of their effects "
            "on users and society.\n"
            "\n"
            "The major areas named are:\n"
            "\n"
            "- **fairness**,\n"
            "- **privacy**,\n"
            "- **transparency**,\n"
            "- **accountability**.\n"
            "\n"
            "Responsible AI is not framed as a final compliance checklist added after modeling. "
            "The chapter treats it as a design responsibility that should influence objectives, data, features, evaluation, interfaces, and deployment choices.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Case study: automated grading exposes system-level failure\n"
            "\n"
            "The chapter studies the automated A-level grading system used in the United Kingdom during the COVID-19 pandemic.\n"
            "\n"
            "The public controversy cannot be understood using average model accuracy alone.\n"
            "\n"
            "The chapter identifies three broad failures:\n"
            "\n"
            "1. **setting the wrong objective**,\n"
            "2. **insufficient fine-grained evaluation**,\n"
            "3. **lack of transparency**.\n"
            "\n"
            "The lesson is important because none of these problems is simply 'choose a better neural network.'\n"
            "\n"
            "[[IMAGE_NEEDED: Responsible-AI failure chain in automated grading | "
            "Objective choice feeding model decisions, subgroup evaluation, and public transparency, "
            "with failure markers at all three stages | Learner should notice how harm can arise from the overall system design]]\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Wrong objectives can produce systematically wrong outcomes\n"
            "\n"
            "The grading system prioritized maintaining historical standards across schools rather than focusing only on each individual student's likely grade.\n"
            "\n"
            "Historical school performance therefore influenced current student outcomes.\n"
            "\n"
            "The chapter explains that this could disadvantage high-performing students from historically lower-performing schools.\n"
            "\n"
            "This reinforces an earlier systems-design principle:\n"
            "\n"
            "> A model can optimize the objective it was given and still be harmful because the objective itself encodes the wrong priority.\n"
            "\n"
            "Responsible AI begins before training, during problem and objective formulation.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Fine-grained evaluation and transparency are both necessary\n"
            "\n"
            "### Fine-grained evaluation\n"
            "\n"
            "Aggregate accuracy can hide unequal behavior across groups.\n"
            "\n"
            "The grading case suggests evaluating relevant slices such as school size and student background rather than relying only on one top-line number.\n"
            "\n"
            "This connects to the earlier lesson on slice-based evaluation: fair evaluation requires adequate data for the groups being evaluated.\n"
            "\n"
            "### Transparency\n"
            "\n"
            "Stakeholders should understand important system choices early enough to challenge them.\n"
            "\n"
            "If objectives, input use, or model behavior remain hidden until the system has already affected people, independent scrutiny arrives too late.\n"
            "\n"
            "Transparency is therefore part of trust and accountability, particularly for systems with serious social consequences.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Some decisions may be inappropriate to automate\n"
            "\n"
            "The chapter raises a deeper question than 'Is the model fair enough?'\n"
            "\n"
            "> **Should this decision be automated by an algorithm at all?**\n"
            "\n"
            "The chapter explicitly notes that some applications can be inappropriate or unethical regardless of which fairness framework is used.\n"
            "\n"
            "Responsible-AI work therefore includes critical thinking about whether a product or automated decision should exist, not only how to optimize it.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Case study: anonymized data can still reveal sensitive information\n"
            "\n"
            "The second case study concerns public fitness-tracking heatmap data.\n"
            "\n"
            "The released data had been described as anonymized and aggregated, yet patterns in the heatmap exposed sensitive activity around military facilities.\n"
            "\n"
            "The engineering lesson is:\n"
            "\n"
            "> **Removing obvious personally identifying fields does not guarantee privacy.**\n"
            "\n"
            "Sensitive information can emerge from locations, behavior, combinations of attributes, or external knowledge.\n"
            "\n"
            "The case also highlights consent and interface design. If privacy settings are difficult to understand or rely on opt-out behavior, "
            "users may expose information without understanding the consequences.\n"
            "\n"
            "The chapter argues for proactively safer defaults even when those defaults reduce the amount of data that can be collected.\n"
            "\n"
            "[[IMAGE_NEEDED: Indirect privacy leakage after anonymization | "
            "An aggregated map with direct identities removed but distinctive patterns still exposing sensitive locations or activity | "
            "Learner should notice that privacy risk can survive removal of names and obvious identifiers]]\n"
            "\n"
            "{{exercise:M10.L02.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Bias can enter through the entire workflow\n"
            "\n"
            "The chapter recommends auditing multiple possible sources rather than looking for one single 'fairness bug.'\n"
            "\n"
            "### Training data\n"
            "\n"
            "Underrepresented populations may receive worse model performance if development data does not represent the real population.\n"
            "\n"
            "### Labeling\n"
            "\n"
            "Subjective or inconsistently applied annotation criteria can inject human biases.\n"
            "\n"
            "### Feature engineering\n"
            "\n"
            "Features can contain sensitive information directly or act as proxies for protected characteristics.\n"
            "\n"
            "The chapter discusses **disparate impact**: apparently neutral selection logic can produce very different outcomes for different groups.\n"
            "\n"
            "### Model objective\n"
            "\n"
            "An objective that maximizes overall performance may favor a large majority group while smaller groups contribute little to the optimization signal.\n"
            "\n"
            "### Evaluation\n"
            "\n"
            "If evaluation does not measure relevant subgroups, bias can remain invisible.\n"
            "\n"
            "[[IMAGE_NEEDED: Bias sources across the ML lifecycle | "
            "A pipeline from training data through labeling, feature engineering, objective design, and evaluation, "
            "with possible bias entering at each stage | Learner should notice that Responsible AI is not confined to model architecture]]\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Data alone cannot explain the social context encoded in data\n"
            "\n"
            "A data-driven system still operates in a real social environment.\n"
            "\n"
            "Historical data can reflect differences in resources, institutions, demographics, culture, and prior discrimination.\n"
            "\n"
            "The chapter therefore recommends crossing disciplinary and functional boundaries to understand lived experience and context.\n"
            "\n"
            "For an equitable grading system, for example, the engineering team needs more than historical grade statistics; "
            "it also needs domain understanding of student populations and socioeconomic conditions.\n"
            "\n"
            "This is another reason SMEs and affected stakeholders should be involved early.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Desirable properties can conflict\n"
            "\n"
            "An ML system may aim for:\n"
            "\n"
            "- accuracy,\n"
            "- privacy,\n"
            "- fairness,\n"
            "- transparency,\n"
            "- low latency,\n"
            "- small model size.\n"
            "\n"
            "The chapter warns against evaluating one optimization under the assumption that all other properties remain unchanged.\n"
            "\n"
            "Improving one property can reduce another, and the cost may fall unevenly across groups.\n"
            "\n"
            "Responsible engineering therefore measures **multiple dimensions and subgroup effects** after important system changes.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Privacy versus accuracy can have unequal subgroup effects\n"
            "\n"
            "The chapter uses differential privacy as an example of a privacy-preserving technique.\n"
            "\n"
            "Higher privacy can reduce model accuracy.\n"
            "\n"
            "The important responsible-AI point is that accuracy loss may not be uniform. "
            "The cited work found stronger degradation for underrepresented classes and groups.\n"
            "\n"
            "Therefore the relevant evaluation is not only:\n"
            "\n"
            "```text\n"
            "How much overall accuracy did privacy cost?\n"
            "```\n"
            "\n"
            "but also:\n"
            "\n"
            "```text\n"
            "Which groups absorbed that accuracy loss?\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Privacy-accuracy trade-off by subgroup | "
            "An overall performance curve declining modestly as privacy strengthens, while an underrepresented subgroup declines more sharply | "
            "Learner should notice that average privacy-performance trade-offs can hide unequal impact]]\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Compression can preserve average accuracy while redistributing errors\n"
            "\n"
            "The chapter revisits pruning and quantization from the deployment chapter.\n"
            "\n"
            "A compressed model can preserve similar top-line accuracy while changing behavior substantially for a narrow subset of examples.\n"
            "\n"
            "The cited studies found that underrepresented features could be harmed disproportionately and that different compression techniques "
            "could have different disparate effects.\n"
            "\n"
            "This leads to a practical rule:\n"
            "\n"
            "> After compression or other major optimization, re-audit subgroup performance rather than checking only overall accuracy.\n"
            "\n"
            "[[IMAGE_NEEDED: Similar overall accuracy but different subgroup harm | "
            "Two models with nearly equal top-line accuracy but different error rates for a small underrepresented subgroup | "
            "Learner should notice why deployment optimization needs fine-grained reevaluation]]\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Address responsible-AI risks early\n"
            "\n"
            "The chapter uses a building-foundation analogy: fixing a bad foundation after an entire structure has been built is far more expensive "
            "than correcting it at the beginning.\n"
            "\n"
            "ML systems behave similarly.\n"
            "\n"
            "If fairness, privacy, transparency, or other concerns are postponed until after deployment, the cost of correction can be far larger because "
            "the system, data, product flows, and organizational processes are already built around the original decisions.\n"
            "\n"
            "The recommendation is to identify likely impacts and bias risks as early as possible.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Model cards improve transparency and handoffs\n"
            "\n"
            "A **model card** is a short document accompanying a trained model that communicates how the model was developed and evaluated, "
            "where it is intended to be used, and where its limitations lie.\n"
            "\n"
            "The chapter's adapted model-card structure includes:\n"
            "\n"
            "### Model details\n"
            "\n"
            "- developer or organization,\n"
            "- date and version,\n"
            "- model type,\n"
            "- training approach and features,\n"
            "- resources/citations,\n"
            "- license,\n"
            "- contact point.\n"
            "\n"
            "### Intended use\n"
            "\n"
            "- primary uses,\n"
            "- intended users,\n"
            "- out-of-scope uses.\n"
            "\n"
            "### Factors and metrics\n"
            "\n"
            "- relevant demographic, environmental, or technical factors,\n"
            "- evaluation factors,\n"
            "- model-performance measures,\n"
            "- decision thresholds,\n"
            "- variation approaches.\n"
            "\n"
            "### Data information\n"
            "\n"
            "- evaluation datasets,\n"
            "- motivation,\n"
            "- preprocessing,\n"
            "- training-data information where possible.\n"
            "\n"
            "### Quantitative and ethical analysis\n"
            "\n"
            "- unitary results,\n"
            "- intersectional results,\n"
            "- ethical considerations,\n"
            "- caveats and recommendations.\n"
            "\n"
            "[[IMAGE_NEEDED: Model card layout | "
            "A one-page structured model card with model details, intended use, factors, metrics, data, subgroup analysis, ethical considerations, and caveats | "
            "Learner should notice that model documentation should communicate context and limitations, not just accuracy]]\n"
            "\n"
            "{{exercise:M10.L02.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Responsible AI should be systematic, automated where appropriate, and kept current\n"
            "\n"
            "Model cards must be updated when models change. If a model is updated frequently, manual reporting can become expensive.\n"
            "\n"
            "Because model-card fields overlap with model-store metadata, the chapter points toward automated model-card generation where possible.\n"
            "\n"
            "Automation should reduce reporting friction, but human judgment is still needed for context, caveats, and ethical interpretation.\n"
            "\n"
            "The chapter also recommends systematic bias-mitigation processes instead of ad hoc reviews.\n"
            "\n"
            "Organizations can maintain shared internal tools, metrics, evaluation procedures, and—where useful—external audits.\n"
            "\n"
            "Finally, Responsible AI is a fast-moving field. New failure modes and mitigation techniques continue to emerge, so responsible practice "
            "requires staying current rather than freezing one checklist forever.\n"
            "\n"
            "{{exercise:M10.L02.EX05}}\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: The most accurate prediction always creates the best UX\n"
            "\n"
            "Consistency and latency can matter enough that the product should intentionally override the model's newest top prediction.\n"
            "\n"
            "### Misconception 2: Mostly-correct predictions are useful to every user\n"
            "\n"
            "They are most useful when users can recognize, choose among, or correct errors.\n"
            "\n"
            "### Misconception 3: SMEs are only needed for labeling\n"
            "\n"
            "Domain expertise can improve problem formulation, features, error analysis, evaluation, reranking, and interface design.\n"
            "\n"
            "### Misconception 4: End-to-end ownership means every data scientist should learn all low-level infrastructure\n"
            "\n"
            "The chapter argues that tooling and abstractions should let people own outcomes without implementing every infrastructure detail themselves.\n"
            "\n"
            "### Misconception 5: Aggregate accuracy is enough to evaluate socially consequential systems\n"
            "\n"
            "Subgroup performance, objectives, transparency, and downstream impact can matter as much as the top-line metric.\n"
            "\n"
            "### Misconception 6: Anonymized data is automatically safe to publish\n"
            "\n"
            "Sensitive patterns can remain inferable from behavior, location, combinations of attributes, or outside information.\n"
            "\n"
            "### Misconception 7: A fairness or privacy improvement affects every group equally\n"
            "\n"
            "The chapter's examples show that privacy and compression changes can impose larger performance costs on underrepresented groups.\n"
            "\n"
            "### Misconception 8: Responsible AI is a compliance checkbox added after development\n"
            "\n"
            "It begins with whether the system should exist, which objective it optimizes, how data is collected, and how impacts are measured.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Consistency-accuracy trade-off | Trade-off between serving the current highest-scoring prediction and preserving a stable user experience. |\n"
            "| Human-in-the-loop AI | Workflow where humans choose, correct, or improve model-generated predictions. |\n"
            "| Smooth failing | Gracefully falling back to a faster/safer system when the primary model cannot meet a requirement such as latency. |\n"
            "| Subject-matter expert (SME) | Person with specialized domain knowledge who can contribute across the ML lifecycle. |\n"
            "| Responsible AI | Practice of designing, developing, and deploying AI with attention to fairness, privacy, transparency, accountability, and societal impact. |\n"
            "| Disparate impact | Apparently neutral process producing substantially different outcomes for different groups. |\n"
            "| Differential privacy | Privacy approach discussed in the chapter that limits how much any one individual can influence released information. |\n"
            "| Model card | Structured document describing model details, intended use, evaluation, ethical considerations, limitations, and recommendations. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "1. Why do probabilistic systems create UX challenges that deterministic software often avoids?\n"
            "2. What is the consistency-accuracy trade-off?\n"
            "3. When are mostly-correct predictions useful?\n"
            "4. Why should multiple candidates be rendered in a form nonexpert users can judge?\n"
            "5. What is smooth failing?\n"
            "6. How does the speed-accuracy trade-off affect fallback design?\n"
            "7. Why should SMEs contribute beyond labeling?\n"
            "8. What are the main drawbacks of separating modeling and production teams?\n"
            "9. Why is expecting every data scientist to master low-level infrastructure problematic?\n"
            "10. How can platform abstractions enable end-to-end ownership?\n"
            "11. What four areas does the chapter name within Responsible AI?\n"
            "12. What were the three major failure categories in the automated-grading case?\n"
            "13. Why can an apparently reasonable objective still cause harmful outcomes?\n"
            "14. Why is subgroup evaluation necessary in addition to average accuracy?\n"
            "15. Why does transparency matter before a high-impact system is deployed?\n"
            "16. Why might some decisions be inappropriate to automate at all?\n"
            "17. Why is anonymization not a complete privacy guarantee?\n"
            "18. Where can bias enter during the ML lifecycle?\n"
            "19. Why is data alone insufficient for understanding social impact?\n"
            "20. What is the privacy-accuracy trade-off described in the chapter?\n"
            "21. Why can compression require renewed fairness auditing?\n"
            "22. Why should responsible-AI work begin early?\n"
            "23. What information should a model card communicate?\n"
            "24. Why should model-card generation be automated where possible?\n"
            "25. Why should responsible-AI reviews be systematic rather than ad hoc?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A production ML system is both a technical system and a human system. "
            "Infrastructure should make correct engineering easier, while UX design, team structure, "
            "fairness, privacy, transparency, and accountability determine whether that engineering "
            "actually creates a system people can trust and use responsibly.**\n"
        ),

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [

            {"id": "human-side", "title": "The human side of ML systems", "order": 1},
            {"id": "probabilistic-ux", "title": "Probabilistic systems create different UX problems", "order": 2},
            {"id": "consistency-accuracy", "title": "Consistency versus accuracy", "order": 3},
            {"id": "mostly-correct-human-loop", "title": "Mostly-correct predictions and human-in-the-loop design", "order": 4},
            {"id": "smooth-failing", "title": "Smooth failing and the speed-accuracy trade-off", "order": 5},
            {"id": "cross-functional-sme", "title": "Subject-matter experts should participate throughout the lifecycle", "order": 6},
            {"id": "team-structures", "title": "Two team structures, two different failure modes", "order": 7},
            {"id": "full-cycle-tools", "title": "End-to-end ownership becomes practical when tooling abstracts infrastructure", "order": 8},
            {"id": "responsible-ai", "title": "Responsible AI belongs inside system design", "order": 9},
            {"id": "grading-case", "title": "Case study: automated grading exposes system-level failure", "order": 10},
            {"id": "wrong-objective-bias", "title": "Wrong objectives can produce systematically wrong outcomes", "order": 11},
            {"id": "subgroup-transparency", "title": "Fine-grained evaluation and transparency are both necessary", "order": 12},
            {"id": "automation-boundary", "title": "Some decisions may be inappropriate to automate", "order": 13},
            {"id": "privacy-anonymization", "title": "Case study: anonymized data can still reveal sensitive information", "order": 14},
            {"id": "bias-sources", "title": "Bias can enter through the entire workflow", "order": 15},
            {"id": "data-not-enough", "title": "Data alone cannot explain the social context encoded in data", "order": 16},
            {"id": "responsible-tradeoffs", "title": "Desirable properties can conflict", "order": 17},
            {"id": "privacy-accuracy-tradeoff", "title": "Privacy versus accuracy can have unequal subgroup effects", "order": 18},
            {"id": "compactness-fairness-tradeoff", "title": "Compression can preserve average accuracy while redistributing errors", "order": 19},
            {"id": "act-early", "title": "Address responsible-AI risks early", "order": 20},
            {"id": "model-cards", "title": "Model cards improve transparency and handoffs", "order": 21},
            {"id": "responsible-processes", "title": "Responsible AI should be systematic, automated where appropriate, and kept current", "order": 22},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M10.L02.EX01",
            "title": "Design UX for a mostly-correct model",
            "lesson_code": "M10.L02",
            "section_id": "mostly-correct-human-loop",
            "placement": "after_section",
            "description": (
                "Apply consistency, human-in-the-loop, and smooth-failure principles to a user-facing ML feature."
            ),
            "instructions": (
                "You are building an AI assistant that generates editable customer-support replies.\n\n"
                "1. Explain why mostly-correct output can still be useful to trained operators.\n"
                "2. Describe one situation where output consistency matters more than always showing the newest top candidate.\n"
                "3. Design a human-in-the-loop interaction for uncertain replies.\n"
                "4. Add a smooth-failing rule for unusually slow requests.\n"
                "5. State one metric beyond model accuracy that you would monitor for UX quality."
            ),
            "expected_output": (
                "A user-experience design connecting model uncertainty, human correction, consistency, and latency fallback."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "ml-user-experience",
                "human-in-the-loop",
                "consistency-accuracy-tradeoff",
                "smooth-failing",
            ],
        },

        {
            "id": "M10.L02.EX02",
            "title": "Choose a team ownership model",
            "lesson_code": "M10.L02",
            "section_id": "full-cycle-tools",
            "placement": "after_section",
            "description": (
                "Reason about team boundaries and the tooling required for end-to-end ownership."
            ),
            "instructions": (
                "A company has data scientists, platform engineers, and healthcare SMEs building a medical ML system.\n\n"
                "1. List at least four contributions the SMEs should make beyond labeling.\n"
                "2. Give two risks of separating modeling and production into completely independent teams.\n"
                "3. Give two risks of forcing every data scientist to own low-level infrastructure.\n"
                "4. Propose one platform abstraction that would let data scientists own more of the lifecycle safely.\n"
                "5. Explain how that abstraction connects to the infrastructure concepts from Chapter 10."
            ),
            "expected_output": (
                "A team-and-tooling design that balances specialization with end-to-end context."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "cross-functional-collaboration",
                "subject-matter-experts",
                "end-to-end-data-science",
                "ml-platform",
            ],
        },

        {
            "id": "M10.L02.EX03",
            "title": "Audit a high-impact ML system before launch",
            "lesson_code": "M10.L02",
            "section_id": "privacy-anonymization",
            "placement": "after_section",
            "description": (
                "Apply the two responsible-AI case studies to a new system."
            ),
            "instructions": (
                "Imagine an automated scholarship-ranking system built from historical student data.\n\n"
                "1. State the intended objective and identify how choosing the wrong objective could harm students.\n"
                "2. Define at least four evaluation slices you would inspect.\n"
                "3. List what should be transparent to students, schools, or independent reviewers.\n"
                "4. Identify one reason anonymizing the historical dataset might still leave privacy risk.\n"
                "5. Explain what evidence would make you question whether the decision should be automated at all."
            ),
            "expected_output": (
                "A pre-launch responsible-AI audit covering objective design, subgroup evaluation, transparency, privacy, and automation boundaries."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "responsible-ai",
                "slice-evaluation",
                "transparency",
                "privacy",
            ],
        },

        {
            "id": "M10.L02.EX04",
            "title": "Write the skeleton of a model card",
            "lesson_code": "M10.L02",
            "section_id": "model-cards",
            "placement": "after_section",
            "description": (
                "Turn model-store and responsible-AI information into structured model documentation."
            ),
            "instructions": (
                "For a binary fraud-detection model, draft headings and short content for:\n"
                "1. model details,\n"
                "2. intended use and out-of-scope use,\n"
                "3. relevant factors,\n"
                "4. metrics and decision threshold,\n"
                "5. evaluation data,\n"
                "6. training-data summary,\n"
                "7. subgroup/intersectional analyses,\n"
                "8. ethical considerations,\n"
                "9. caveats and recommendations.\n\n"
                "Then identify which fields could be auto-generated from a model store and which require human review."
            ),
            "expected_output": (
                "A concise but complete model-card outline tied to model-store metadata and human responsibility."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "model-cards",
                "model-store",
                "transparency",
                "responsible-ai",
            ],
        },

        {
            "id": "M10.L02.EX05",
            "title": "Evaluate a responsible-AI trade-off",
            "lesson_code": "M10.L02",
            "section_id": "responsible-processes",
            "placement": "after_section",
            "description": (
                "Practice auditing a system change beyond top-line accuracy."
            ),
            "instructions": (
                "A team wants to compress a model and add a stronger privacy mechanism before deployment.\n\n"
                "1. State the expected operational benefits.\n"
                "2. Explain why overall accuracy alone is not enough after the changes.\n"
                "3. Define at least three subgroup analyses you would rerun.\n"
                "4. Explain the privacy-accuracy concern from the chapter.\n"
                "5. Explain the compactness-fairness concern from the chapter.\n"
                "6. Propose a repeatable review process so these checks happen for every future model update."
            ),
            "expected_output": (
                "A multidimensional evaluation plan covering performance, privacy, subgroup impact, and repeatable governance."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "privacy-accuracy-tradeoff",
                "compactness-fairness-tradeoff",
                "bias-auditing",
                "responsible-process",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M10.L02.QZ01",

        "title": "People, UX, and Responsible ML Systems — Knowledge Check",

        "lesson_code": "M10.L02",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M10.L02.Q01",
                "section_id": "probabilistic-ux",
                "question": "Why can ML systems create UX inconsistency that traditional deterministic software often avoids?",
                "options": [
                    "ML predictions can vary with probabilistic behavior and context.",
                    "ML systems cannot return outputs.",
                    "Traditional software has no interfaces.",
                    "ML models never use the same input twice.",
                ],
                "correct": 0,
                "explanation": (
                    "Probabilistic model behavior can change outputs even when users perceive the situation as similar."
                ),
            },

            {
                "id": "M10.L02.Q02",
                "section_id": "consistency-accuracy",
                "question": "What is the consistency-accuracy trade-off?",
                "options": [
                    "Choosing whether to use CPU or GPU.",
                    "Balancing the latest highest-scoring prediction against preserving a stable, understandable user experience.",
                    "Balancing train and test accuracy.",
                    "Choosing between batch and online prediction.",
                ],
                "correct": 1,
                "explanation": (
                    "The most accurate instantaneous recommendation can sometimes create a worse product experience if it causes confusing changes."
                ),
            },

            {
                "id": "M10.L02.Q03",
                "section_id": "mostly-correct-human-loop",
                "question": "When are mostly-correct predictions especially useful?",
                "options": [
                    "When users can recognize and cheaply correct the remaining errors.",
                    "Only when outputs are always perfect.",
                    "When users cannot inspect the result.",
                    "Only when no human is involved.",
                ],
                "correct": 0,
                "explanation": (
                    "Human expertise can turn a mostly-correct draft into a useful productivity tool."
                ),
            },

            {
                "id": "M10.L02.Q04",
                "section_id": "smooth-failing",
                "question": "What is smooth failing?",
                "options": [
                    "Silently deleting failed requests.",
                    "Falling back to a less optimal but reliable option when the primary system cannot meet a requirement such as latency.",
                    "Always using the largest model.",
                    "Disabling monitoring.",
                ],
                "correct": 1,
                "explanation": (
                    "A fallback can preserve acceptable user experience when the best model is too slow or otherwise unavailable."
                ),
            },

            {
                "id": "M10.L02.Q05",
                "section_id": "cross-functional-sme",
                "question": "Which statement best reflects the chapter's view of subject-matter experts?",
                "options": [
                    "They should only label the original training set.",
                    "They can contribute across formulation, features, labeling, error analysis, evaluation, reranking, and interface design.",
                    "They should be excluded after data collection.",
                    "They must become infrastructure engineers.",
                ],
                "correct": 1,
                "explanation": (
                    "Domain expertise can improve decisions throughout the ML lifecycle."
                ),
            },

            {
                "id": "M10.L02.Q06",
                "section_id": "team-structures",
                "question": "What is one major drawback of separating modeling and production into independent teams?",
                "options": [
                    "It always eliminates specialization.",
                    "Communication, debugging, and ownership can become fragmented across team boundaries.",
                    "It makes hiring impossible.",
                    "It prevents models from being deployed at all.",
                ],
                "correct": 1,
                "explanation": (
                    "Cross-team handoffs can create blockers, finger-pointing, and incomplete system context."
                ),
            },

            {
                "id": "M10.L02.Q07",
                "section_id": "full-cycle-tools",
                "question": "What makes end-to-end ownership more realistic for data scientists in the chapter?",
                "options": [
                    "Requiring every data scientist to implement cluster schedulers personally.",
                    "Infrastructure abstractions that hide containerization and distributed-system details behind simpler interfaces.",
                    "Removing platform engineers.",
                    "Avoiding production deployment.",
                ],
                "correct": 1,
                "explanation": (
                    "Good tooling lets practitioners own the workflow while specialists automate difficult infrastructure layers."
                ),
            },

            {
                "id": "M10.L02.Q08",
                "section_id": "responsible-ai",
                "question": "Which set contains the Responsible AI areas explicitly named in the chapter?",
                "options": [
                    "Fairness, privacy, transparency, and accountability",
                    "Only latency and throughput",
                    "Only accuracy and recall",
                    "Containers, schedulers, and GPUs",
                ],
                "correct": 0,
                "explanation": (
                    "The source names fairness, privacy, transparency, and accountability as major Responsible AI areas."
                ),
            },

            {
                "id": "M10.L02.Q09",
                "section_id": "grading-case",
                "question": "Which was NOT one of the three major failure categories highlighted in the automated-grading case?",
                "options": [
                    "Wrong objective",
                    "Insufficient fine-grained evaluation",
                    "Lack of transparency",
                    "Too little GPU memory",
                ],
                "correct": 3,
                "explanation": (
                    "The case study focuses on objective design, fine-grained evaluation, and transparency."
                ),
            },

            {
                "id": "M10.L02.Q10",
                "section_id": "subgroup-transparency",
                "question": "Why is aggregate accuracy insufficient for high-impact model evaluation?",
                "options": [
                    "It can hide much worse performance for important or disadvantaged subgroups.",
                    "Accuracy can never be computed.",
                    "Aggregate metrics always equal subgroup metrics.",
                    "Subgroup data is never useful.",
                ],
                "correct": 0,
                "explanation": (
                    "A top-line average can conceal concentrated harm."
                ),
            },

            {
                "id": "M10.L02.Q11",
                "section_id": "privacy-anonymization",
                "question": "What does the fitness-heatmap case demonstrate?",
                "options": [
                    "Removing obvious identifiers always makes public data safe.",
                    "Aggregated or anonymized data can still reveal sensitive patterns.",
                    "Location data has no privacy implications.",
                    "Opt-out defaults always guarantee informed consent.",
                ],
                "correct": 1,
                "explanation": (
                    "Indirect patterns can expose sensitive information even after direct identifiers are removed."
                ),
            },

            {
                "id": "M10.L02.Q12",
                "section_id": "bias-sources",
                "question": "Where can bias enter an ML system according to the chapter?",
                "options": [
                    "Only during model training.",
                    "Training data, labeling, feature engineering, objective design, and evaluation.",
                    "Only after deployment.",
                    "Only through protected attributes used directly.",
                ],
                "correct": 1,
                "explanation": (
                    "Bias can enter throughout the ML workflow, including through proxy variables and evaluation choices."
                ),
            },

            {
                "id": "M10.L02.Q13",
                "section_id": "privacy-accuracy-tradeoff",
                "question": "What important nuance does the chapter add to the privacy-accuracy trade-off?",
                "options": [
                    "Accuracy loss can be larger for underrepresented groups rather than evenly distributed.",
                    "Privacy always improves accuracy.",
                    "Every group always loses exactly the same accuracy.",
                    "Differential privacy has no effect on models.",
                ],
                "correct": 0,
                "explanation": (
                    "The cited result warns that an acceptable average accuracy loss can hide larger subgroup degradation."
                ),
            },

            {
                "id": "M10.L02.Q14",
                "section_id": "compactness-fairness-tradeoff",
                "question": "Why should compressed models be audited at subgroup level?",
                "options": [
                    "Compression can preserve top-line accuracy while changing behavior much more on narrow or underrepresented subsets.",
                    "Compression always increases every subgroup's accuracy.",
                    "Compressed models cannot be evaluated.",
                    "Model size is a fairness metric.",
                ],
                "correct": 0,
                "explanation": (
                    "Average performance can remain similar even when errors are redistributed unevenly."
                ),
            },

            {
                "id": "M10.L02.Q15",
                "section_id": "model-cards",
                "question": "What is the main purpose of a model card?",
                "options": [
                    "To document model context, intended use, evaluation, limitations, ethical considerations, and other important details.",
                    "To replace the model binary.",
                    "To store only training loss.",
                    "To hide out-of-scope uses.",
                ],
                "correct": 0,
                "explanation": (
                    "Model cards improve transparency and enable informed comparison and use of trained models."
                ),
            },

            {
                "id": "M10.L02.Q16",
                "section_id": "responsible-processes",
                "type": "open",
                "question": (
                    "Design a responsible-AI review for a new high-impact ML system. Include objective review, "
                    "stakeholder/SME involvement, bias sources to inspect, subgroup evaluation, privacy analysis, "
                    "transparency/model-card requirements, one system trade-off to audit, and a process for repeating "
                    "the review after future model updates."
                ),
            },
        ],

        "passing_score": 70,
    },
}
