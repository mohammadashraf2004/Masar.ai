"""M02.L01 — Introduction to Machine Learning Systems Design.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 2, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M02.L01"

MODULE_ORDER = 2

MODULE_TITLE = "Designing Machine Learning Systems"

MODULE_DESCRIPTION = (
    "Learn how to turn a business need into a well-framed machine learning "
    "problem, define production requirements, choose task and objective "
    "formulations, and reason about the role of data."
)

SOURCE_CHAPTER = 2

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Introduction to Machine Learning Systems Design",

    "slug": "ml-systems-design-m02-l01",

    "description": (
        "A practical introduction to designing machine learning systems: "
        "connecting ML work to business goals, defining system requirements, "
        "framing problems correctly, choosing objectives, and treating ML "
        "development as an iterative data-driven process."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.0,

    "skill_tags": [
        "ml-systems-design",
        "business-objectives",
        "reliability",
        "scalability",
        "maintainability",
        "adaptability",
        "problem-framing",
        "classification",
        "regression",
        "objective-functions",
        "multi-objective-ml",
        "data-centric-ml",
    ],

    "prerequisite_ids": ["M01.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Introduction to Machine Learning Systems Design",

        "content": (
            "# Introduction to Machine Learning Systems Design\n"
            "\n"
            "> **Lesson:** M02.L01  \n"
            "> **Module:** Designing Machine Learning Systems  \n"
            "> **Source alignment:** Chapter 2. Page numbers were not included "
            "in the supplied source. This lesson is an instructor-authored "
            "curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why an ML project must begin with a real objective rather "
            "than with a model or algorithm.\n"
            "- Translate a business objective into a measurable ML objective.\n"
            "- Explain reliability, scalability, maintainability, and adaptability "
            "as requirements of production ML systems.\n"
            "- Describe the iterative lifecycle of an ML system.\n"
            "- Frame an ambiguous real-world problem as an ML problem with inputs, "
            "outputs, and an objective function.\n"
            "- Distinguish regression, binary classification, multiclass "
            "classification, and multilabel classification.\n"
            "- Explain why the same business problem can often be framed in "
            "multiple ML ways.\n"
            "- Explain what an objective function does and why multiple objectives "
            "are often easier to maintain when they are decoupled.\n"
            "- Reason about why data quality and quantity are central to modern ML "
            "systems.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Start with the objective, not the model\n"
            "\n"
            "A common mistake in machine learning is to begin by asking:\n"
            "\n"
            "> Which model should we train?\n"
            "\n"
            "That question comes too early. Before choosing a model, you should "
            "understand **why the system needs to exist at all**.\n"
            "\n"
            "A production ML project usually sits inside a larger organization. "
            "That organization cares about outcomes such as revenue, cost, "
            "retention, customer satisfaction, safety, operational efficiency, "
            "or some other measurable goal. The ML system is useful only if it "
            "contributes to one or more of those outcomes.\n"
            "\n"
            "This creates an important chain:\n"
            "\n"
            "```text\n"
            "Business objective\n"
            "      ↓\n"
            "Product or operational objective\n"
            "      ↓\n"
            "ML objective\n"
            "      ↓\n"
            "Model metric / system metric\n"
            "```\n"
            "\n"
            "For example, suppose an ecommerce company wants to increase the "
            "percentage of visits that end in a purchase.\n"
            "\n"
            "- **Business objective:** increase purchase-through rate.\n"
            "- **Product idea:** recommend products that are more relevant to the "
            "current user.\n"
            "- **ML objective:** rank products so that items the user is likely to "
            "buy appear near the top.\n"
            "- **Possible ML metrics:** ranking quality, precision, recall, or "
            "another predictive measure.\n"
            "\n"
            "Improving an ML metric matters only if that improvement helps the "
            "business outcome. A model that moves from 94.0% to 94.2% accuracy is "
            "not automatically more valuable if customer behavior, revenue, or "
            "cost does not improve.\n"
            "\n"
            "### Correlation is not enough\n"
            "\n"
            "The relationship between model metrics and business metrics can be "
            "surprisingly indirect. A more accurate recommender might improve "
            "customer satisfaction, but it might also help users find what they "
            "need faster and therefore spend less time on the service.\n"
            "\n"
            "For that reason, teams often need controlled experiments such as A/B "
            "tests to measure whether a new model actually improves the desired "
            "business outcome.\n"
            "\n"
            "[[IMAGE_NEEDED: From business objective to ML metric | "
            "A layered diagram showing a business goal at the top, followed by a "
            "product goal, an ML objective, and finally model/system metrics | "
            "Learner should notice that model metrics are proxies for a higher-level "
            "goal, not the final goal themselves]]\n"
            "\n"
            "### Example: fraud detection\n"
            "\n"
            "Fraud detection is attractive for ML because the connection between "
            "technical performance and business value can be relatively direct. "
            "If the system correctly blocks fraudulent transactions, the company "
            "can save money. Even here, however, false positives matter because "
            "blocking legitimate customers can also create business cost.\n"
            "\n"
            "{{exercise:M02.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Four core requirements of an ML system\n"
            "\n"
            "Once the objective is clear, the next question is not simply "
            "\"Which algorithm is best?\" A production system must satisfy "
            "engineering requirements too.\n"
            "\n"
            "Four broad requirements are especially useful:\n"
            "\n"
            "| Requirement | Core question |\n"
            "|---|---|\n"
            "| Reliability | Does the system keep doing the right job under faults and uncertainty? |\n"
            "| Scalability | Can it handle growth in traffic, models, data, or complexity? |\n"
            "| Maintainability | Can people understand, reproduce, modify, and operate it over time? |\n"
            "| Adaptability | Can it respond to changing data and changing business needs? |\n"
            "\n"
            "### Reliability\n"
            "\n"
            "A reliable system continues to perform its intended function at an "
            "acceptable level even when things go wrong: hardware failures, "
            "software bugs, bad inputs, human mistakes, or unexpected conditions.\n"
            "\n"
            "ML makes reliability harder because failure can be **silent**. A web "
            "server might return a visible 500 error, but an ML model can keep "
            "returning predictions that look valid while their quality has become "
            "poor. If users do not know the correct answer, they might never notice.\n"
            "\n"
            "This means reliability in ML involves more than uptime. It includes "
            "monitoring prediction quality, data quality, and system behavior.\n"
            "\n"
            "### Scalability\n"
            "\n"
            "An ML system may need to scale in several different dimensions:\n"
            "\n"
            "- **Traffic:** 10,000 predictions per day may become 10 million.\n"
            "- **Model complexity:** a small model may be replaced by a much larger "
            "one with greater memory and compute needs.\n"
            "- **Model count:** one model may become hundreds or thousands of "
            "customer-specific or task-specific models.\n"
            "- **Data:** training, feature, and monitoring datasets may grow rapidly.\n"
            "\n"
            "Scalability therefore means more than adding servers. A system with "
            "hundreds of models also needs automated tracking, monitoring, "
            "retraining, versioning, and reproducibility.\n"
            "\n"
            "### Maintainability\n"
            "\n"
            "ML systems are usually built by multiple groups: ML engineers, "
            "software engineers, platform or DevOps engineers, data engineers, "
            "product teams, and subject-matter experts.\n"
            "\n"
            "Maintainability improves when:\n"
            "\n"
            "- code is documented,\n"
            "- code, data, and model artifacts are versioned,\n"
            "- experiments can be reproduced,\n"
            "- interfaces between components are clear,\n"
            "- contributors can diagnose problems together,\n"
            "- knowledge does not disappear when one person leaves the team.\n"
            "\n"
            "### Adaptability\n"
            "\n"
            "The real world changes. User behavior changes, markets change, input "
            "distributions change, and the business may change its goals.\n"
            "\n"
            "An adaptable ML system is designed so that it can discover degraded "
            "performance and be updated without requiring the entire service to be "
            "rebuilt from scratch.\n"
            "\n"
            "[[IMAGE_NEEDED: Four requirements of production ML | "
            "A four-part diagram around an ML system labeled reliability, "
            "scalability, maintainability, and adaptability, with a short example "
            "for each | Learner should see that production quality is multidimensional "
            "and cannot be reduced to model accuracy alone]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. ML system development is an iterative cycle\n"
            "\n"
            "A beginner often imagines the workflow like this:\n"
            "\n"
            "```text\n"
            "Collect data → Train model → Deploy → Done\n"
            "```\n"
            "\n"
            "Real ML systems rarely work that way.\n"
            "\n"
            "A more realistic lifecycle is:\n"
            "\n"
            "```text\n"
            "1. Project scoping\n"
            "2. Data engineering\n"
            "3. Model development\n"
            "4. Deployment\n"
            "5. Monitoring and continual learning\n"
            "6. Business analysis\n"
            "             ↓\n"
            "        back to scoping\n"
            "```\n"
            "\n"
            "### Why the cycle loops\n"
            "\n"
            "Imagine building a system that decides whether to show an ad for a "
            "search query.\n"
            "\n"
            "You may begin by optimizing how often an ad is shown. Then, during "
            "error analysis, you discover that some labels are wrong. You relabel "
            "the data and retrain.\n"
            "\n"
            "Next, you discover that almost every example is negative, so the "
            "model learns to predict \"do not show\" nearly all the time. You need "
            "better data and retrain again.\n"
            "\n"
            "Later, the model performs well on an old test set but poorly on "
            "yesterday's traffic. Now the data distribution has changed, so the "
            "model is stale.\n"
            "\n"
            "Finally, the model may perform well technically while revenue falls. "
            "The business then changes the optimization target from impressions to "
            "click-through rate.\n"
            "\n"
            "The lesson is important:\n"
            "\n"
            "> **Model development is embedded inside a larger feedback loop.**\n"
            "\n"
            "[[IMAGE_NEEDED: Iterative ML system lifecycle | "
            "A circular lifecycle containing project scoping, data engineering, "
            "model development, deployment, monitoring/continual learning, and "
            "business analysis, with arrows looping back | Learner should notice "
            "that deployment is not the end of ML development]]\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Turn a real-world problem into an ML problem\n"
            "\n"
            "A business problem is not automatically an ML problem.\n"
            "\n"
            "Suppose a bank says:\n"
            "\n"
            "> \"Use machine learning to make customer support faster.\"\n"
            "\n"
            "This request does not yet tell us what the model should receive, "
            "predict, or optimize.\n"
            "\n"
            "After investigation, suppose the real bottleneck is routing support "
            "requests to the right department: accounting, inventory, HR, or IT.\n"
            "\n"
            "Now we can frame an ML problem:\n"
            "\n"
            "- **Input:** text of the customer request.\n"
            "- **Output:** one of four departments.\n"
            "- **Task:** multiclass classification.\n"
            "- **Objective:** make the predicted department match the correct "
            "department as closely as possible.\n"
            "\n"
            "A useful general framing is:\n"
            "\n"
            "```text\n"
            "ML problem = inputs + outputs + learning objective\n"
            "```\n"
            "\n"
            "If any of these are unclear, the ML problem itself is still unclear.\n"
            "\n"
            "### Why framing matters\n"
            "\n"
            "Two teams can start with the same business problem and create very "
            "different ML systems simply because they frame the problem differently. "
            "A good framing can make the system easier to train, easier to update, "
            "and more scalable.\n"
            "\n"
            "{{exercise:M02.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Classification, regression, and label structure\n"
            "\n"
            "The type of output you want strongly influences the ML task type.\n"
            "\n"
            "### Classification versus regression\n"
            "\n"
            "**Classification** predicts a category.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- spam / not spam,\n"
            "- fraud / legitimate,\n"
            "- accounting / inventory / HR / IT.\n"
            "\n"
            "**Regression** predicts a continuous numerical value.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- house price,\n"
            "- expected demand,\n"
            "- probability that a user will click an item.\n"
            "\n"
            "The same problem can sometimes be framed either way. House-price "
            "prediction is naturally regression, but you could instead create "
            "price buckets and predict the bucket. Likewise, a spam classifier can "
            "produce a continuous score between 0 and 1 and then apply a threshold.\n"
            "\n"
            "### Binary classification\n"
            "\n"
            "There are exactly two possible classes.\n"
            "\n"
            "Examples include fraud/not fraud or toxic/not toxic.\n"
            "\n"
            "### Multiclass classification\n"
            "\n"
            "There are more than two classes, but each example belongs to exactly "
            "one of them.\n"
            "\n"
            "For example, a ticket might go to exactly one department.\n"
            "\n"
            "### High-cardinality classification\n"
            "\n"
            "When the number of classes becomes very large, the task becomes much "
            "harder. Thousands of product categories or disease classes can create "
            "data scarcity for rare classes.\n"
            "\n"
            "One useful strategy is **hierarchical classification**:\n"
            "\n"
            "```text\n"
            "Product\n"
            "  ↓\n"
            "Fashion\n"
            "  ↓\n"
            "Shoes / Shirts / Jeans / Accessories\n"
            "```\n"
            "\n"
            "The first classifier chooses a broad group; another classifier then "
            "chooses a subgroup.\n"
            "\n"
            "### Multilabel classification\n"
            "\n"
            "An example can belong to multiple classes at the same time.\n"
            "\n"
            "For example, an article might be both **technology** and **finance**.\n"
            "\n"
            "A multilabel target can be represented as:\n"
            "\n"
            "```text\n"
            "[tech, entertainment, finance, politics]\n"
            "[  1 ,      0       ,    1   ,    0    ]\n"
            "```\n"
            "\n"
            "Multilabel systems introduce extra challenges because the system must "
            "decide not only *which* labels are likely, but also *how many* labels "
            "to output.\n"
            "\n"
            "[[IMAGE_NEEDED: ML task type map | "
            "A compact tree showing regression and classification, with "
            "classification branching into binary, multiclass, high-cardinality, "
            "and multilabel examples | Learner should notice that output structure "
            "determines the task formulation]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. The same problem can have multiple framings\n"
            "\n"
            "Suppose you want to predict which app a phone user will open next.\n"
            "\n"
            "### Framing A: multiclass classification\n"
            "\n"
            "Input:\n"
            "\n"
            "- user features,\n"
            "- context such as time and environment.\n"
            "\n"
            "Output:\n"
            "\n"
            "- one probability for every possible app.\n"
            "\n"
            "If there are `N` apps, the output has size `N`.\n"
            "\n"
            "The weakness is that the model architecture may depend on the number "
            "of apps. Adding a new app can therefore require model changes or "
            "retraining.\n"
            "\n"
            "### Framing B: scoring each app\n"
            "\n"
            "Instead, include the candidate app as part of the input:\n"
            "\n"
            "```text\n"
            "Input = user features + context + app features\n"
            "Output = likelihood of opening this app\n"
            "```\n"
            "\n"
            "Now the model returns one score for one candidate app. To compare `N` "
            "apps, run the model `N` times or score candidates in a batch.\n"
            "\n"
            "This framing has an important systems advantage: a new app can be "
            "evaluated through its features without redesigning an output layer "
            "whose size depends on the number of apps.\n"
            "\n"
            "### General lesson\n"
            "\n"
            "> **Problem framing is an engineering decision, not merely a mathematical label.**\n"
            "\n"
            "The framing affects data requirements, model architecture, evaluation, "
            "serving cost, scalability, and how easily the system can evolve.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Objective functions tell the model what to optimize\n"
            "\n"
            "Once a task is framed, the learning algorithm needs a mathematical "
            "signal telling it how wrong its predictions are.\n"
            "\n"
            "This is the role of the **objective function**, often called the "
            "**loss function**.\n"
            "\n"
            "For supervised learning, the loss usually compares the model's "
            "prediction with the ground-truth target.\n"
            "\n"
            "Common examples include:\n"
            "\n"
            "| Task | Common loss |\n"
            "|---|---|\n"
            "| Regression | Mean squared error (MSE/RMSE) or mean absolute error (MAE) |\n"
            "| Binary classification | Logistic / log loss |\n"
            "| Multiclass classification | Cross-entropy loss |\n"
            "\n"
            "### Cross-entropy example\n"
            "\n"
            "Suppose the class order is:\n"
            "\n"
            "```text\n"
            "[tech, entertainment, finance, politics]\n"
            "```\n"
            "\n"
            "The true class is politics:\n"
            "\n"
            "```text\n"
            "p = [0, 0, 0, 1]\n"
            "```\n"
            "\n"
            "The model predicts:\n"
            "\n"
            "```text\n"
            "q = [0.45, 0.20, 0.02, 0.33]\n"
            "```\n"
            "\n"
            "The model assigned only 0.33 probability to the correct class, so "
            "cross-entropy produces a loss that penalizes that mismatch.\n"
            "\n"
            "A simple implementation matching the chapter's example is:\n"
            "\n"
            "```python\n"
            "import numpy as np\n"
            "\n"
            "def cross_entropy(p, q):\n"
            "    return -sum(p[i] * np.log(q[i]) for i in range(len(p)))\n"
            "\n"
            "p = [0, 0, 0, 1]\n"
            "q = [0.45, 0.20, 0.02, 0.33]\n"
            "\n"
            "loss = cross_entropy(p, q)\n"
            "print(loss)\n"
            "```\n"
            "\n"
            "Because only the politics position has target value 1, the result is "
            "effectively `-log(0.33)`. A better prediction that places more "
            "probability on the correct class would produce a smaller loss.\n"
            "\n"
            "### Do not confuse three different ideas\n"
            "\n"
            "1. **Business objective:** what the organization wants.\n"
            "2. **ML objective:** what predictive behavior the ML system should "
            "produce.\n"
            "3. **Objective/loss function:** the mathematical function optimized "
            "during training.\n"
            "\n"
            "They are related, but they are not the same thing.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Multiple objectives and why decoupling helps\n"
            "\n"
            "Real systems often optimize several goals at once.\n"
            "\n"
            "Imagine ranking posts in a newsfeed. You might want to:\n"
            "\n"
            "- filter spam,\n"
            "- filter unsafe content,\n"
            "- reduce misinformation,\n"
            "- rank by quality,\n"
            "- rank by expected engagement.\n"
            "\n"
            "Some objectives can conflict. Highly engaging content is not always "
            "high-quality content.\n"
            "\n"
            "### Approach 1: combine losses into one model\n"
            "\n"
            "You could optimize:\n"
            "\n"
            "```text\n"
            "loss = α × quality_loss + β × engagement_loss\n"
            "```\n"
            "\n"
            "`α` and `β` determine how strongly each objective matters.\n"
            "\n"
            "The drawback is operational: changing the trade-off may require "
            "retraining the model.\n"
            "\n"
            "### Approach 2: decouple the objectives\n"
            "\n"
            "Train separate models:\n"
            "\n"
            "```text\n"
            "quality_model    → quality_score\n"
            "engagement_model → engagement_score\n"
            "```\n"
            "\n"
            "Then combine their outputs:\n"
            "\n"
            "```text\n"
            "final_score = α × quality_score + β × engagement_score\n"
            "```\n"
            "\n"
            "Now the team can adjust `α` and `β` without retraining the underlying "
            "models.\n"
            "\n"
            "This also helps maintenance because different objectives may change "
            "at different speeds. Spam behavior may evolve rapidly, while another "
            "quality signal may need updates less frequently.\n"
            "\n"
            "[[IMAGE_NEEDED: Coupled versus decoupled objectives | "
            "Side-by-side diagram: one model minimizing a weighted combined loss "
            "versus two independent models producing scores that are combined "
            "after inference | Learner should notice that decoupling allows weights "
            "to change without retraining both models]]\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Data is a first-class part of system design\n"
            "\n"
            "Modern ML progress has relied heavily on data. In many practical "
            "organizations, improving the data pipeline can matter as much as or "
            "more than searching for a cleverer algorithm.\n"
            "\n"
            "The chapter presents an ongoing debate:\n"
            "\n"
            "- One view emphasizes **better inductive biases, structure, and "
            "algorithmic intelligence** so systems can learn more efficiently.\n"
            "- Another view emphasizes **general methods, large-scale computation, "
            "and large datasets**.\n"
            "\n"
            "The practical conclusion for system designers is simpler than the "
            "philosophical debate:\n"
            "\n"
            "> **Data is essential, but more data is not automatically better data.**\n"
            "\n"
            "A larger dataset can hurt if it contains:\n"
            "\n"
            "- outdated examples,\n"
            "- incorrect labels,\n"
            "- irrelevant samples,\n"
            "- biased or unrepresentative observations.\n"
            "\n"
            "So the real target is not simply maximum quantity. You need enough "
            "relevant, representative, and sufficiently high-quality data for the "
            "problem you are trying to solve.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Better model metrics always mean better business results\n"
            "\n"
            "> \"If accuracy improves, the ML project is automatically more valuable.\"\n"
            "\n"
            "This is wrong because an ML metric is usually a proxy. It matters only "
            "to the extent that it improves the real outcome the organization cares "
            "about. Experiments may be needed to establish that relationship.\n"
            "\n"
            "### Misconception 2: Deployment is the final step\n"
            "\n"
            "> \"Once the model is deployed, the project is finished.\"\n"
            "\n"
            "Production introduces changing traffic, changing data, failures, new "
            "requirements, and business feedback. Monitoring and updating are part "
            "of the system lifecycle.\n"
            "\n"
            "### Misconception 3: The business request already defines the ML problem\n"
            "\n"
            "> \"Use AI to improve customer support\" is enough to start training.\n"
            "\n"
            "It is not. You still need to identify the model inputs, outputs, task "
            "type, training target, objective, and evaluation strategy.\n"
            "\n"
            "### Misconception 4: More data always helps\n"
            "\n"
            "More low-quality, stale, incorrectly labeled, or irrelevant data can "
            "make a model worse. Quantity and quality must be considered together.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Business objective | The real organizational outcome a project is intended to influence. |\n"
            "| ML objective | The predictive behavior or measurable ML goal chosen to support the business objective. |\n"
            "| Objective function | Mathematical function optimized during model training; often called a loss function. |\n"
            "| Reliability | Ability to continue performing the intended function at an acceptable level despite faults or uncertainty. |\n"
            "| Scalability | Ability to handle growth in traffic, data, model complexity, model count, or resource demand. |\n"
            "| Maintainability | Ease with which a system can be understood, reproduced, changed, debugged, and operated over time. |\n"
            "| Adaptability | Ability of a system to respond to changing data distributions and requirements. |\n"
            "| Classification | ML task that predicts categories. |\n"
            "| Regression | ML task that predicts continuous numerical values. |\n"
            "| Binary classification | Classification with exactly two possible classes. |\n"
            "| Multiclass classification | Classification with more than two mutually exclusive classes. |\n"
            "| Multilabel classification | Classification where one example may belong to several classes. |\n"
            "| High cardinality | A classification problem with a very large number of possible classes. |\n"
            "| Hierarchical classification | Classification in stages, from broad categories to more specific subcategories. |\n"
            "| Cross entropy | A common loss for multiclass classification that penalizes probability assigned away from the correct class. |\n"
            "| Decoupled objectives | Separate models or components optimize different goals before their outputs are combined. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why is improving accuracy not enough to prove that an ML project "
            "is successful?\n"
            "2. What is the difference between reliability and scalability?\n"
            "3. Why can an ML system fail even when its service is technically up?\n"
            "4. Why is ML development usually iterative rather than linear?\n"
            "5. What three elements should be clear when framing an ML problem?\n"
            "6. How does multilabel classification differ from multiclass classification?\n"
            "7. Why might scoring each candidate independently be easier to evolve "
            "than predicting over a fixed set of candidates?\n"
            "8. What is the difference between a business objective, an ML objective, "
            "and a loss function?\n"
            "9. Why can decoupling multiple objectives make maintenance easier?\n"
            "10. Why can adding more training data sometimes reduce model quality?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Designing an ML system means designing the entire path from a real "
            "objective to data, task framing, training, deployment, monitoring, and "
            "business feedback—not merely selecting an algorithm.**\n"
        ),

        "estimated_minutes": 120,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "objectives",
                "title": "Start with the objective, not the model",
                "order": 1,
            },
            {
                "id": "requirements",
                "title": "Four core requirements of an ML system",
                "order": 2,
            },
            {
                "id": "iterative-process",
                "title": "ML system development is an iterative cycle",
                "order": 3,
            },
            {
                "id": "problem-framing",
                "title": "Turn a real-world problem into an ML problem",
                "order": 4,
            },
            {
                "id": "task-types",
                "title": "Classification, regression, and label structure",
                "order": 5,
            },
            {
                "id": "multiple-framings",
                "title": "The same problem can have multiple framings",
                "order": 6,
            },
            {
                "id": "objective-functions",
                "title": "Objective functions tell the model what to optimize",
                "order": 7,
            },
            {
                "id": "multiple-objectives",
                "title": "Multiple objectives and why decoupling helps",
                "order": 8,
            },
            {
                "id": "data-role",
                "title": "Data is a first-class part of system design",
                "order": 9,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M02.L01.EX01",

            "title": "Connect an ML metric to a business outcome",

            "lesson_code": "M02.L01",

            "section_id": "objectives",

            "placement": "after_section",

            "description": (
                "Practice translating a business goal into an ML objective and "
                "choosing measurements that can test whether the system creates value."
            ),

            "instructions": (
                "You work for a subscription video platform that wants to reduce "
                "subscription cancellations.\n\n"
                "1. State the business objective.\n"
                "2. Propose one ML-powered product intervention.\n"
                "3. Define the prediction the model should make.\n"
                "4. Choose one ML metric for the model.\n"
                "5. Choose one business metric that should improve if the project "
                "is successful.\n"
                "6. Explain why improving the ML metric alone would not prove that "
                "the business objective improved.\n"
                "7. Propose a simple experiment that could test the connection."
            ),

            "expected_output": (
                "A short mapping from business objective → product intervention → "
                "ML objective → ML metric → business metric, plus an explanation "
                "of how an experiment could validate the relationship."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "business-objective-mapping",
                "ml-objective-design",
                "metric-reasoning",
            ],
        },

        {
            "id": "M02.L01.EX02",

            "title": "Frame a vague request as an ML problem",

            "lesson_code": "M02.L01",

            "section_id": "problem-framing",

            "placement": "after_section",

            "description": (
                "Turn an ambiguous operational request into a precise ML task."
            ),

            "instructions": (
                "A support manager says: 'Use AI to reduce the time customers wait "
                "for help.' You discover that most delay happens because requests "
                "are manually routed to one of six specialist teams.\n\n"
                "1. Define the model input.\n"
                "2. Define the model output.\n"
                "3. Identify the task type.\n"
                "4. Define the ground-truth label.\n"
                "5. State an appropriate ML objective.\n"
                "6. Name one business metric this system should eventually improve.\n"
                "7. Identify one production requirement—reliability, scalability, "
                "maintainability, or adaptability—that could become important and "
                "explain why."
            ),

            "expected_output": (
                "A concise ML problem specification containing inputs, outputs, "
                "task type, target labels, ML objective, business metric, and one "
                "system requirement with justification."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "problem-framing",
                "classification",
                "requirements-analysis",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M02.L01.QZ01",

        "title": "Introduction to Machine Learning Systems Design — Knowledge Check",

        "lesson_code": "M02.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M02.L01.Q01",
                "section_id": "objectives",
                "question": (
                    "A model's accuracy rises from 94.0% to 94.5%, but the target "
                    "business metric does not change. What is the best interpretation?"
                ),
                "options": [
                    "The project is automatically more successful.",
                    "The model improvement has not yet demonstrated additional business value.",
                    "The model must be overfitting.",
                    "Accuracy should never be used in production.",
                ],
                "correct": 1,
                "explanation": (
                    "A model metric is generally a proxy for a higher-level goal. "
                    "An improvement is valuable only if it helps the intended business "
                    "or product outcome."
                ),
            },

            {
                "id": "M02.L01.Q02",
                "section_id": "requirements",
                "question": (
                    "Which requirement is most directly concerned with a system "
                    "remaining useful when input distributions and business needs change?"
                ),
                "options": [
                    "Reliability",
                    "Scalability",
                    "Maintainability",
                    "Adaptability",
                ],
                "correct": 3,
                "explanation": (
                    "Adaptability concerns the system's ability to evolve as data "
                    "distributions and requirements change."
                ),
            },

            {
                "id": "M02.L01.Q03",
                "section_id": "iterative-process",
                "question": (
                    "Why is production ML development usually iterative?"
                ),
                "options": [
                    "Because models can only be trained once.",
                    "Because data, labels, requirements, and business feedback can reveal new problems after each stage.",
                    "Because deployment must always happen before training.",
                    "Because production systems cannot be monitored.",
                ],
                "correct": 1,
                "explanation": (
                    "Error analysis, fresh data, monitoring, and business outcomes "
                    "often force teams to revisit earlier decisions."
                ),
            },

            {
                "id": "M02.L01.Q04",
                "section_id": "problem-framing",
                "question": (
                    "Which set best describes the minimum elements needed to make "
                    "a vague real-world request into an ML problem?"
                ),
                "options": [
                    "GPU type, cloud vendor, and programming language",
                    "Input, output, and learning objective",
                    "Dataset size, neural-network depth, and optimizer",
                    "Dashboard, API, and database",
                ],
                "correct": 1,
                "explanation": (
                    "Problem framing begins by making the inputs, desired outputs, "
                    "and objective explicit."
                ),
            },

            {
                "id": "M02.L01.Q05",
                "section_id": "task-types",
                "question": (
                    "An article may simultaneously belong to technology, finance, "
                    "and politics. What kind of task is this?"
                ),
                "options": [
                    "Binary classification",
                    "Multiclass classification",
                    "Multilabel classification",
                    "Ordinary regression",
                ],
                "correct": 2,
                "explanation": (
                    "In multilabel classification, one example can have several "
                    "labels at the same time."
                ),
            },

            {
                "id": "M02.L01.Q06",
                "section_id": "multiple-framings",
                "question": (
                    "Why can independently scoring each candidate app be easier to "
                    "evolve than predicting one fixed distribution over all apps?"
                ),
                "options": [
                    "It guarantees perfect predictions.",
                    "It eliminates the need for app features.",
                    "Adding a new app does not necessarily require changing an output dimension tied to the total number of apps.",
                    "It converts every problem into binary classification.",
                ],
                "correct": 2,
                "explanation": (
                    "When the candidate itself is an input, new candidates can often "
                    "be scored without redesigning a fixed-size output space."
                ),
            },

            {
                "id": "M02.L01.Q07",
                "section_id": "objective-functions",
                "question": (
                    "What is the primary role of a loss or objective function during training?"
                ),
                "options": [
                    "It specifies the company's revenue target.",
                    "It measures how predictions differ from the desired target and guides optimization.",
                    "It decides which cloud provider to use.",
                    "It automatically chooses the best dataset.",
                ],
                "correct": 1,
                "explanation": (
                    "The training objective mathematically quantifies error or utility "
                    "so the learning algorithm has a signal to optimize."
                ),
            },

            {
                "id": "M02.L01.Q08",
                "section_id": "multiple-objectives",
                "question": (
                    "What is one operational advantage of using separate quality "
                    "and engagement models and combining their scores afterward?"
                ),
                "options": [
                    "The system no longer needs data.",
                    "The trade-off weights can be changed without necessarily retraining both models.",
                    "The objectives can no longer conflict.",
                    "Both models are guaranteed to use the same maintenance schedule.",
                ],
                "correct": 1,
                "explanation": (
                    "Decoupling allows downstream weighting to change independently "
                    "and also lets components evolve on different maintenance schedules."
                ),
            },

            {
                "id": "M02.L01.Q09",
                "section_id": "data-role",
                "question": (
                    "Which statement best reflects the lesson's conclusion about data?"
                ),
                "options": [
                    "More data always improves model performance.",
                    "Algorithm design makes data unnecessary.",
                    "Data is essential, but relevance and quality matter as well as quantity.",
                    "Only dataset size matters in modern ML.",
                ],
                "correct": 2,
                "explanation": (
                    "Large quantities of outdated, mislabeled, biased, or irrelevant "
                    "data can hurt rather than help."
                ),
            },

            {
                "id": "M02.L01.Q10",
                "section_id": "requirements",
                "type": "open",
                "question": (
                    "Imagine an ML service grows from one model and 10,000 requests "
                    "per day to 500 models and 5 million requests per day. Explain "
                    "two distinct scalability challenges this creates and one "
                    "maintainability practice that would help."
                ),
            },
        ],

        "passing_score": 70,
    },
}
