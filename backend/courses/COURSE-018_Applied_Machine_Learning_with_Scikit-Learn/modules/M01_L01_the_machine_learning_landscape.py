"""M01.L01 — The Machine Learning Landscape.

One source chapter -> one complete learner-facing lesson + inline Images +
inline Exercises + lesson Quiz.

Source alignment: Chapter 1 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "The Machine Learning Landscape"

MODULE_DESCRIPTION = (
    "Build the mental map needed for the rest of machine learning: what learning "
    "from data means, the main families of ML systems, how models generalize, "
    "what causes them to fail, and how to evaluate them correctly."
)

SOURCE_CHAPTER = 1

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "The Machine Learning Landscape",

    "slug": "machine-learning-foundations-m01-l01",

    "description": (
        "A foundation lesson that explains what machine learning is, why it is "
        "useful, how the major learning paradigms differ, how a typical ML "
        "workflow operates, and how to diagnose data, modeling, and evaluation "
        "failures."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.0,

    "skill_tags": [
        "machine-learning",
        "ml-foundations",
        "supervised-learning",
        "unsupervised-learning",
        "online-learning",
        "generalization",
        "model-evaluation",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # INLINE IMAGE RULES
    # =======================================================================
    #
    # Images are requested only where the supplied chapter contains an
    # important figure that materially improves understanding.
    #
    # Each IMAGE_NEEDED placeholder preserves the source figure number(s)
    # and also includes a stable key for later manual linking.
    #
    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "The Machine Learning Landscape",

        "content": (
            "# The Machine Learning Landscape\n"
            "\n"
            "> **Course:** Applied Machine Learning with Scikit-Learn  \n"
            "> **Lesson:** M01.L01  \n"
            "> **Module:** The Machine Learning Landscape  \n"
            "> **Source alignment:** Chapter 1, “The Machine Learning Landscape,” supplied by the course author. Page numbers were not included in the supplied extract. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain what it means for a machine to learn from data.\n"
            "- Describe why machine learning is useful when hand-written rules become difficult, brittle, or impossible to maintain.\n"
            "- Distinguish supervised, unsupervised, semi-supervised, self-supervised, and reinforcement learning.\n"
            "- Distinguish batch learning from online learning and explain data drift, learning rate, and out-of-core learning.\n"
            "- Compare instance-based and model-based learning as two approaches to generalization.\n"
            "- Describe the main steps of a typical machine learning workflow from data to inference.\n"
            "- Diagnose common data problems such as insufficient data, sampling bias, poor quality, and irrelevant features.\n"
            "- Explain overfitting, underfitting, regularization, model parameters, and hyperparameters.\n"
            "- Use training, validation, test, and train-dev sets for sound model evaluation and model selection.\n"
            "- Explain why no single machine learning model is best for every possible dataset.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. What machine learning is — and why we use it\n"
            "\n"
            "Machine learning is easiest to understand by starting with a simple idea:\n"
            "\n"
            "**A machine-learning system improves at a task by learning from experience, usually represented as data, instead of requiring a programmer to explicitly write every rule.**\n"
            "\n"
            "That definition has three important pieces:\n"
            "\n"
            "- **Task:** what the system is expected to do.\n"
            "- **Experience:** the examples or interactions it learns from.\n"
            "- **Performance measure:** how we decide whether it is getting better.\n"
            "\n"
            "For a spam filter:\n"
            "\n"
            "```text\n"
            "Task (T): classify a new email as spam or not spam\n"
            "Experience (E): previously labeled emails\n"
            "Performance (P): a measure such as classification accuracy\n"
            "```\n"
            "\n"
            "The examples used for learning form the **training set**. One individual example is a **training instance** or **sample**. The learned component that produces predictions is the **model**.\n"
            "\n"
            "This distinction matters. Merely storing a large amount of information is not the same as learning. A computer that contains every Wikipedia article has more data, but unless some process uses that data to improve performance on a task, it has not learned in the machine-learning sense.\n"
            "\n"
            "### Traditional programming versus machine learning\n"
            "\n"
            "Imagine building a spam filter using ordinary rules. You inspect spam messages, discover suspicious words or patterns, encode rules, test them, and keep adding exceptions.\n"
            "\n"
            "That can work, but the rule base tends to grow:\n"
            "\n"
            "```text\n"
            "if message contains \"free\" -> suspicious\n"
            "if sender looks unusual -> suspicious\n"
            "if message contains \"credit card\" -> suspicious\n"
            "...\n"
            "```\n"
            "\n"
            "The problem is not just the number of rules. The environment changes. Spammers adapt their wording, new patterns appear, and old rules become less useful.\n"
            "\n"
            "A machine-learning approach changes the job. Instead of manually specifying every spam pattern, you provide examples and let a learning algorithm discover predictive patterns from the data.\n"
            "\n"
            "[[IMAGE_NEEDED: Traditional programming versus machine learning workflow (Figures 1-1 and 1-2; key: traditional-vs-ml-workflow) | Recreate the source comparison: the traditional workflow studies the problem, writes rules, evaluates, analyzes errors, and repeatedly edits rules; the ML workflow studies the problem, trains a model from data, evaluates it, analyzes errors, and improves the data/model before launch | Learner should notice that ML moves much of the pattern discovery from hand-written rules into the training process]]\n"
            "\n"
            "### Why machine learning is useful\n"
            "\n"
            "Machine learning is especially valuable in four situations.\n"
            "\n"
            "**1. Rule-heavy problems**\n"
            "\n"
            "If a useful system requires hundreds or thousands of fragile rules, a learned model may be shorter, easier to maintain, and more accurate.\n"
            "\n"
            "**2. Problems with no practical hand-written solution**\n"
            "\n"
            "Speech recognition is a good example. It is unrealistic to manually write rules that cover thousands of words, different voices, accents, microphones, noise conditions, and languages.\n"
            "\n"
            "**3. Environments that change**\n"
            "\n"
            "A system can be retrained on recent data when user behavior, fraud patterns, market conditions, or other parts of the world change.\n"
            "\n"
            "**4. Problems where the patterns themselves are valuable**\n"
            "\n"
            "Machine learning can reveal correlations, segments, unusual cases, or other structures that humans may not have noticed. Searching large datasets for useful patterns is often called **data mining**.\n"
            "\n"
            "### What kinds of problems can ML solve?\n"
            "\n"
            "The chapter spans many application types. The important lesson is not to memorize every algorithm yet; it is to learn how to recognize the *kind of task*.\n"
            "\n"
            "| Application | ML task |\n"
            "|---|---|\n"
            "| Classify products from camera images | Image classification |\n"
            "| Locate a tumor pixel by pixel | Semantic segmentation |\n"
            "| Classify news or offensive comments | Text classification |\n"
            "| Condense a long document | Text summarization |\n"
            "| Estimate a numeric quantity such as revenue | Regression |\n"
            "| React to spoken commands | Speech recognition |\n"
            "| Detect suspicious credit-card transactions | Anomaly detection |\n"
            "| Group customers by behavior | Clustering |\n"
            "| Compress high-dimensional data for visualization | Dimensionality reduction |\n"
            "| Recommend a likely product | Recommender system |\n"
            "| Train a game-playing or control agent | Reinforcement learning |\n"
            "\n"
            "The same real system may contain several tasks. A personal assistant, for example, may need speech processing, language understanding, retrieval, question answering, and generation.\n"
            "\n"
            "### A useful mental model\n"
            "\n"
            "Do not ask only:\n"
            "\n"
            "> “Which algorithm should I use?”\n"
            "\n"
            "First ask:\n"
            "\n"
            "```text\n"
            "What is the task?\n"
            "What data do I have?\n"
            "What feedback or labels are available?\n"
            "How quickly does the world change?\n"
            "How will I measure success on unseen cases?\n"
            "```\n"
            "\n"
            "Those questions determine the family of learning system you need.\n"
            "\n"
            "---\n"
            "\n"
            "## 2. Learning by supervision: what kind of feedback does the model receive?\n"
            "\n"
            "One major way to classify machine-learning systems is by the kind of guidance they receive while learning.\n"
            "\n"
            "The main categories in this chapter are:\n"
            "\n"
            "- supervised learning\n"
            "- unsupervised learning\n"
            "- semi-supervised learning\n"
            "- self-supervised learning\n"
            "- reinforcement learning\n"
            "\n"
            "They are different answers to the question:\n"
            "\n"
            "**Where does the learning signal come from?**\n"
            "\n"
            "### Supervised learning\n"
            "\n"
            "In **supervised learning**, each training example comes with a desired answer.\n"
            "\n"
            "A labeled email might look conceptually like this:\n"
            "\n"
            "```text\n"
            "Input: email text\n"
            "Label: spam\n"
            "```\n"
            "\n"
            "A car-price example might look like this:\n"
            "\n"
            "```text\n"
            "Input features:\n"
            "- mileage\n"
            "- age\n"
            "- brand\n"
            "- engine size\n"
            "\n"
            "Target:\n"
            "- price\n"
            "```\n"
            "\n"
            "The two most common supervised tasks are **classification** and **regression**.\n"
            "\n"
            "**Classification** predicts a category:\n"
            "\n"
            "```text\n"
            "spam / not spam\n"
            "cat / dog\n"
            "fraud / legitimate\n"
            "```\n"
            "\n"
            "**Regression** predicts a numeric value:\n"
            "\n"
            "```text\n"
            "house price\n"
            "revenue\n"
            "temperature\n"
            "life-satisfaction score\n"
            "```\n"
            "\n"
            "The words **label** and **target** are often used almost interchangeably, but “label” is especially common in classification and “target” in regression.\n"
            "\n"
            "A **feature** is an input variable used to make the prediction. Features are also sometimes called predictors or attributes.\n"
            "\n"
            "One naming trap is worth remembering: **logistic regression is commonly used for classification**, despite the word “regression” in its name, because its output can be interpreted as a class probability.\n"
            "\n"
            "### Unsupervised learning\n"
            "\n"
            "In **unsupervised learning**, the data has no provided target labels. The system searches for useful structure.\n"
            "\n"
            "Important unsupervised tasks include:\n"
            "\n"
            "**Clustering**\n"
            "\n"
            "Group similar examples together without being told the group names. A business might discover customer segments from browsing and purchasing behavior.\n"
            "\n"
            "**Dimensionality reduction**\n"
            "\n"
            "Represent the important structure of many features using fewer dimensions. This can reduce storage and computation, remove redundancy, and sometimes improve learning.\n"
            "\n"
            "If several original variables are combined into a more useful representation, this is a form of **feature extraction**.\n"
            "\n"
            "**Visualization**\n"
            "\n"
            "Transform complex high-dimensional data into two or three dimensions so humans can inspect its structure.\n"
            "\n"
            "**Anomaly detection**\n"
            "\n"
            "Learn what normal data looks like and identify unusual cases, such as suspicious transactions or manufacturing defects.\n"
            "\n"
            "**Novelty detection**\n"
            "\n"
            "Detect examples that differ from the clean training distribution. It resembles anomaly detection, but novelty detection usually assumes that the training set itself contains only normal examples.\n"
            "\n"
            "**Association rule learning**\n"
            "\n"
            "Discover relationships such as:\n"
            "\n"
            "```text\n"
            "customers who often buy A and B also tend to buy C\n"
            "```\n"
            "\n"
            "This is useful for discovering co-occurrence patterns in transactional data.\n"
            "\n"
            "### Semi-supervised learning\n"
            "\n"
            "Real datasets are often mostly unlabeled because labeling can be expensive.\n"
            "\n"
            "**Semi-supervised learning** combines:\n"
            "\n"
            "```text\n"
            "a small amount of labeled data\n"
            "+\n"
            "a much larger amount of unlabeled data\n"
            "```\n"
            "\n"
            "Suppose a photo system clusters faces and discovers that many images contain the same person. A human may need to name that person only once, after which the system can propagate that information to similar images.\n"
            "\n"
            "A common pattern is:\n"
            "\n"
            "1. discover structure using unlabeled data,\n"
            "2. use a small number of labels to identify the groups,\n"
            "3. train or refine a supervised model using the expanded labeled set.\n"
            "\n"
            "### Self-supervised learning\n"
            "\n"
            "**Self-supervised learning** starts with unlabeled data but creates a prediction task from the data itself.\n"
            "\n"
            "For an image, you might hide part of the image and ask a model to reconstruct the missing region.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "original example\n"
            "      |\n"
            "create an artificial learning task\n"
            "      |\n"
            "input: corrupted or masked example\n"
            "target: information derived from the original example\n"
            "```\n"
            "\n"
            "The crucial idea is that a human did not manually provide the target. The data generated its own supervision.\n"
            "\n"
            "The learned representation can then be reused for another task. This is closely related to **transfer learning**: knowledge learned on one task is reused to help another task.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "large unlabeled image collection\n"
            "        |\n"
            "self-supervised pretraining\n"
            "        |\n"
            "general visual representation\n"
            "        |\n"
            "small labeled pet dataset\n"
            "        |\n"
            "fine-tuning\n"
            "        |\n"
            "pet classifier\n"
            "```\n"
            "\n"
            "Large pretrained models often follow this broad pattern: learn useful representations from huge amounts of raw data, then adapt those representations to downstream tasks.\n"
            "\n"
            "### Reinforcement learning\n"
            "\n"
            "**Reinforcement learning (RL)** uses a different learning signal.\n"
            "\n"
            "An **agent** interacts with an **environment**:\n"
            "\n"
            "```text\n"
            "observe state\n"
            "    |\n"
            "choose action\n"
            "    |\n"
            "environment changes\n"
            "    |\n"
            "receive reward or penalty\n"
            "    |\n"
            "improve policy\n"
            "```\n"
            "\n"
            "The **policy** describes which action the agent should choose in a given situation.\n"
            "\n"
            "The goal is not simply to predict a fixed label. The goal is to choose a sequence of actions that produces high reward over time.\n"
            "\n"
            "Robotic control and game-playing agents are classic examples.\n"
            "\n"
            "### The categories can be combined with other classifications\n"
            "\n"
            "A system is not just “supervised” or “online.” These properties describe different dimensions.\n"
            "\n"
            "A spam filter could be:\n"
            "\n"
            "```text\n"
            "supervised\n"
            "+\n"
            "online\n"
            "+\n"
            "model-based\n"
            "```\n"
            "\n"
            "These labels are not competitors; they answer different questions about the same system.\n"
            "\n"
            "[[IMAGE_NEEDED: Overview of machine learning categories (Figure 1-20; key: ml-system-categories-overview) | Recreate the source overview that organizes ML systems by learning supervision, training method, generalization approach, and other families such as ensemble, federated, and meta-learning | Learner should notice that ML categories describe different dimensions of a system and can be combined]]\n"
            "\n"
            "### Other families mentioned in the chapter\n"
            "\n"
            "The chapter briefly points to additional categories:\n"
            "\n"
            "- **Ensemble learning:** combine predictions from multiple models.\n"
            "- **Federated learning:** train across multiple devices or locations without centrally collecting all raw data.\n"
            "- **Meta-learning:** learn how to adapt to new tasks quickly.\n"
            "\n"
            "You do not need to master these yet. The important point is that machine learning contains several overlapping ways to classify systems.\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Batch learning versus online learning\n"
            "\n"
            "A second classification asks:\n"
            "\n"
            "**Can the model learn incrementally as new data arrives?**\n"
            "\n"
            "### Batch learning\n"
            "\n"
            "In **batch learning**, the model is trained on the available training data as a separate process. Once deployed, it normally makes predictions without continuing to learn.\n"
            "\n"
            "A simplified cycle is:\n"
            "\n"
            "```text\n"
            "collect data\n"
            "    |\n"
            "train model from the dataset\n"
            "    |\n"
            "evaluate\n"
            "    |\n"
            "deploy\n"
            "    |\n"
            "use for inference\n"
            "    |\n"
            "collect newer data\n"
            "    |\n"
            "train a new model version\n"
            "```\n"
            "\n"
            "This training is usually performed offline, which is why batch learning is often associated with **offline learning**.\n"
            "\n"
            "Batch learning is simple and reliable when change is slow. But retraining from scratch on a large dataset can require substantial:\n"
            "\n"
            "- CPU or GPU compute,\n"
            "- memory,\n"
            "- disk capacity,\n"
            "- disk I/O,\n"
            "- network I/O,\n"
            "- time,\n"
            "- money.\n"
            "\n"
            "### Data drift\n"
            "\n"
            "A deployed model lives in a changing world.\n"
            "\n"
            "If the relationship between the data and the task changes, performance may slowly deteriorate. The chapter describes this as **data drift** or **model rot**.\n"
            "\n"
            "A spam filter may encounter new spam strategies. A finance model may face changing market behavior. Even an image classifier can be affected by changes in cameras, image formats, lighting, resolution, or user behavior.\n"
            "\n"
            "The fix is not “train once and forget.” A production system needs monitoring and an update strategy.\n"
            "\n"
            "### Online learning\n"
            "\n"
            "In **online learning**, the system learns incrementally.\n"
            "\n"
            "New examples are processed one at a time or in small groups called **mini-batches**.\n"
            "\n"
            "```text\n"
            "new data -> learning step -> updated model\n"
            "new data -> learning step -> updated model\n"
            "new data -> learning step -> updated model\n"
            "```\n"
            "\n"
            "Each update can be much cheaper than retraining from scratch.\n"
            "\n"
            "Online learning is attractive when:\n"
            "\n"
            "- data changes quickly,\n"
            "- the system must react rapidly,\n"
            "- resources are constrained,\n"
            "- or the dataset is too large to fit into memory.\n"
            "\n"
            "[[IMAGE_NEEDED: Online learning lifecycle (Figure 1-13; key: online-learning-lifecycle) | Recreate the source process showing an initially trained and evaluated model launched into production and then updated continuously as new data arrives | Learner should notice that deployment does not necessarily end training in an online-learning system]]\n"
            "\n"
            "### Out-of-core learning\n"
            "\n"
            "A very large dataset may not fit into RAM.\n"
            "\n"
            "An online-capable algorithm can process it piece by piece:\n"
            "\n"
            "```text\n"
            "load chunk 1 -> update model\n"
            "load chunk 2 -> update model\n"
            "load chunk 3 -> update model\n"
            "...\n"
            "```\n"
            "\n"
            "This is called **out-of-core learning**.\n"
            "\n"
            "A terminology warning is important: out-of-core learning may be performed completely offline. The word “online” refers to **incremental updating**, not necessarily to a live internet-connected production system.\n"
            "\n"
            "### Learning rate\n"
            "\n"
            "An online system needs to decide how strongly to react to new observations.\n"
            "\n"
            "The **learning rate** controls the size or speed of adaptation.\n"
            "\n"
            "A high learning rate:\n"
            "\n"
            "- adapts quickly,\n"
            "- reacts strongly to new data,\n"
            "- but may forget useful older patterns or react to noise.\n"
            "\n"
            "A low learning rate:\n"
            "\n"
            "- adapts slowly,\n"
            "- is more stable,\n"
            "- but may lag behind genuine changes.\n"
            "\n"
            "If a system changes too aggressively and loses previously useful knowledge, the chapter refers to **catastrophic forgetting** or **catastrophic interference**.\n"
            "\n"
            "### Why online learning needs monitoring\n"
            "\n"
            "Incremental learning introduces a dangerous possibility: bad incoming data can damage the model quickly.\n"
            "\n"
            "Bad data may come from:\n"
            "\n"
            "- broken sensors,\n"
            "- software bugs,\n"
            "- corrupted records,\n"
            "- unusual outliers,\n"
            "- deliberate manipulation of a live system.\n"
            "\n"
            "Production online learning therefore needs safeguards:\n"
            "\n"
            "```text\n"
            "monitor input data\n"
            "monitor model performance\n"
            "detect abnormal behavior\n"
            "pause learning when necessary\n"
            "rollback to a known-good model if needed\n"
            "```\n"
            "\n"
            "Online learning is not “automatically better” than batch learning. It trades retraining cost and responsiveness for additional operational risk.\n"
            "\n"
            "{{exercise:M01.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Generalization: instance-based versus model-based learning\n"
            "\n"
            "The central purpose of machine learning is not to perform perfectly on examples the model has already seen.\n"
            "\n"
            "The goal is **generalization**:\n"
            "\n"
            "> perform well on new, unseen cases.\n"
            "\n"
            "Two broad strategies from the chapter are **instance-based learning** and **model-based learning**.\n"
            "\n"
            "### Instance-based learning\n"
            "\n"
            "Instance-based learning keeps the training examples, or a useful representation of them, and predicts by comparing a new case with known cases.\n"
            "\n"
            "The simplest idea is:\n"
            "\n"
            "```text\n"
            "new example\n"
            "    |\n"
            "find similar training examples\n"
            "    |\n"
            "use their outcomes to make a prediction\n"
            "```\n"
            "\n"
            "A similarity measure determines what “close” means.\n"
            "\n"
            "For a simple spam system, similarity might be based on shared words. In a numerical dataset, it may be geometric distance between feature vectors.\n"
            "\n"
            "A familiar example is **k-nearest neighbors (k-NN)**.\n"
            "\n"
            "If `k = 3`, the algorithm finds the three closest known examples and combines their labels or numeric targets.\n"
            "\n"
            "Advantages can include simplicity and good behavior on some small or changing datasets.\n"
            "\n"
            "Limitations include:\n"
            "\n"
            "- storing or accessing many training instances at prediction time,\n"
            "- potentially slow searches,\n"
            "- difficulty with very high-dimensional data,\n"
            "- heavy dependence on the chosen similarity measure.\n"
            "\n"
            "### Model-based learning\n"
            "\n"
            "Model-based learning takes a different route:\n"
            "\n"
            "```text\n"
            "training examples\n"
            "      |\n"
            "choose a model family\n"
            "      |\n"
            "learn model parameters\n"
            "      |\n"
            "trained model\n"
            "      |\n"
            "predict new cases\n"
            "```\n"
            "\n"
            "Instead of searching the training set for every prediction, the algorithm fits a model that summarizes a pattern in the data.\n"
            "\n"
            "[[IMAGE_NEEDED: Instance-based versus model-based generalization (Figures 1-15 and 1-16; key: instance-vs-model-based-learning) | Place the source ideas side by side: on the left a new point is classified from its nearest stored training examples; on the right a learned model or decision boundary represents the pattern and is used directly for prediction | Learner should notice the difference between comparing against remembered examples and learning a predictive representation]]\n"
            "\n"
            "### Model selection, parameters, and training\n"
            "\n"
            "Suppose we believe life satisfaction has an approximately linear relationship with GDP per capita.\n"
            "\n"
            "A simple linear model can be written as:\n"
            "\n"
            "```text\n"
            "predicted_life_satisfaction = theta_0 + theta_1 * GDP_per_capita\n"
            "```\n"
            "\n"
            "`theta_0` and `theta_1` are **model parameters**.\n"
            "\n"
            "Choosing a linear relationship is part of **model selection**.\n"
            "\n"
            "Finding parameter values that fit the training data is **training**.\n"
            "\n"
            "The learning algorithm needs an objective. A **cost function** or **loss function** measures how bad the predictions are. Training searches for parameter values that reduce that cost.\n"
            "\n"
            "A **utility function** or **fitness function** expresses the opposite idea: how good the model is.\n"
            "\n"
            "### A compact Scikit-Learn example\n"
            "\n"
            "The source chapter demonstrates the workflow with a linear regression model. The important code pattern is:\n"
            "\n"
            "```python\n"
            "import pandas as pd\n"
            "from sklearn.linear_model import LinearRegression\n"
            "\n"
            "data_root = \"https://github.com/ageron/data/raw/main/\"\n"
            "lifesat = pd.read_csv(data_root + \"lifesat/lifesat.csv\")\n"
            "\n"
            "X = lifesat[[\"GDP per capita (USD)\"]].values\n"
            "y = lifesat[[\"Life satisfaction\"]].values\n"
            "\n"
            "model = LinearRegression()\n"
            "model.fit(X, y)\n"
            "\n"
            "X_new = [[33_442.8]]\n"
            "prediction = model.predict(X_new)\n"
            "\n"
            "print(prediction)\n"
            "```\n"
            "\n"
            "Read it as a workflow, not just syntax:\n"
            "\n"
            "```text\n"
            "load data\n"
            "   ->\n"
            "separate features X and target y\n"
            "   ->\n"
            "choose model\n"
            "   ->\n"
            "fit model parameters using training data\n"
            "   ->\n"
            "predict for a new case\n"
            "```\n"
            "\n"
            "`model.fit(X, y)` is the learning step.\n"
            "\n"
            "`model.predict(X_new)` is **inference**: using the trained model on new input.\n"
            "\n"
            "The source example predicts a life-satisfaction value of roughly `6.02` for the new GDP value.\n"
            "\n"
            "[[IMAGE_NEEDED: Best-fit linear model for life satisfaction (Figure 1-19; key: fitted-linear-model-example) | Recreate the source scatter plot of GDP per capita versus life satisfaction with the learned best-fit line and the fitted parameter values | Learner should notice that training chooses parameter values that make the selected model fit the observed data as well as possible under the chosen objective]]\n"
            "\n"
            "### Parameters versus hyperparameters\n"
            "\n"
            "This distinction is fundamental.\n"
            "\n"
            "A **model parameter** is learned during training.\n"
            "\n"
            "Examples:\n"
            "\n"
            "```text\n"
            "linear-regression slope\n"
            "linear-regression intercept\n"
            "neural-network weights\n"
            "```\n"
            "\n"
            "A **hyperparameter** controls the learning process or model configuration and is chosen outside the ordinary parameter-fitting process.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "```text\n"
            "regularization strength\n"
            "number of neighbors k\n"
            "tree depth\n"
            "learning rate\n"
            "```\n"
            "\n"
            "You choose or tune hyperparameters; the training algorithm learns model parameters.\n"
            "\n"
            "### A typical machine-learning workflow\n"
            "\n"
            "At a high level:\n"
            "\n"
            "1. Understand the problem and define the task.\n"
            "2. Gather and inspect data.\n"
            "3. Select useful features and a target if the task is supervised.\n"
            "4. Choose a model family.\n"
            "5. Define an evaluation or optimization objective.\n"
            "6. Train the model.\n"
            "7. Evaluate it on data not used for fitting.\n"
            "8. Improve the data, features, model, or hyperparameters.\n"
            "9. Deploy the final model.\n"
            "10. Use it for inference and monitor it.\n"
            "\n"
            "This loop is more important than any single algorithm. Most real ML work consists of repeatedly improving different parts of this system.\n"
            "\n"
            "---\n"
            "\n"
            "## 5. The data can make or break the system\n"
            "\n"
            "The chapter summarizes ML failure in a useful way:\n"
            "\n"
            "```text\n"
            "bad data\n"
            "or\n"
            "bad model\n"
            "```\n"
            "\n"
            "In practice, data problems are often the first place to look.\n"
            "\n"
            "### Insufficient training data\n"
            "\n"
            "Most machine-learning algorithms need many examples to learn a stable pattern.\n"
            "\n"
            "A tiny dataset can make a model sensitive to chance. Complex perception tasks such as speech or image recognition may require enormous datasets unless the project can reuse a pretrained model through transfer learning.\n"
            "\n"
            "The deeper lesson is not “always collect more data.” It is:\n"
            "\n"
            "**The amount of data must be sufficient for the complexity of the task, variability of the real world, and flexibility of the model.**\n"
            "\n"
            "### Data versus algorithm sophistication\n"
            "\n"
            "The chapter discusses research showing that, on some difficult tasks, very different algorithms can reach similar performance once enough data is available.\n"
            "\n"
            "That does **not** mean algorithm choice is irrelevant.\n"
            "\n"
            "It means that improving the dataset can sometimes produce larger gains than endlessly tweaking the algorithm.\n"
            "\n"
            "A practical engineering mindset is:\n"
            "\n"
            "```text\n"
            "Do not optimize only the model.\n"
            "Ask whether better, broader, cleaner, or more representative data is the higher-value improvement.\n"
            "```\n"
            "\n"
            "### Nonrepresentative training data\n"
            "\n"
            "A model learns from what it sees.\n"
            "\n"
            "If the training sample differs from the cases encountered later, good training performance may mean very little.\n"
            "\n"
            "This can happen through:\n"
            "\n"
            "- missing parts of the population,\n"
            "- collecting data from a biased source,\n"
            "- selecting only popular or easy examples,\n"
            "- geographic or demographic imbalance,\n"
            "- changes between training time and deployment time.\n"
            "\n"
            "A small sample can be unrepresentative because of **sampling noise**.\n"
            "\n"
            "A large sample can still be unrepresentative because of a flawed collection process. That is **sampling bias**.\n"
            "\n"
            "**Nonresponse bias** is a special case: the people or entities that respond differ systematically from those that do not.\n"
            "\n"
            "The key lesson is:\n"
            "\n"
            "> Dataset size cannot repair a fundamentally biased sampling process.\n"
            "\n"
            "### Poor-quality data\n"
            "\n"
            "Training data may contain:\n"
            "\n"
            "- incorrect measurements,\n"
            "- duplicate records,\n"
            "- corrupted inputs,\n"
            "- mislabeled examples,\n"
            "- extreme outliers,\n"
            "- missing values,\n"
            "- inconsistent formats.\n"
            "\n"
            "Cleaning decisions are part of modeling.\n"
            "\n"
            "For missing values, possible choices include:\n"
            "\n"
            "- remove the affected rows,\n"
            "- remove the feature,\n"
            "- fill missing values using a defined strategy,\n"
            "- build separate handling for examples where that feature is unavailable.\n"
            "\n"
            "There is no universal answer. The decision depends on why the value is missing and how the model will be used.\n"
            "\n"
            "### Irrelevant features\n"
            "\n"
            "More features are not automatically better.\n"
            "\n"
            "Irrelevant inputs can add noise, increase computational cost, and give flexible models more opportunities to discover accidental patterns.\n"
            "\n"
            "**Feature engineering** includes:\n"
            "\n"
            "- **feature selection:** keep the most useful existing features,\n"
            "- **feature extraction:** combine or transform existing features,\n"
            "- **creating new features:** collect or derive additional information.\n"
            "\n"
            "A useful rule is:\n"
            "\n"
            "```text\n"
            "garbage in -> garbage out\n"
            "```\n"
            "\n"
            "But “garbage” includes more than errors. It can also mean data that is technically correct but irrelevant to the prediction task.\n"
            "\n"
            "[[IMAGE_NEEDED: Data quantity versus algorithm performance (Figure 1-21; key: data-scale-vs-algorithm-performance) | Recreate the source graph showing several learning algorithms improving as the amount of training data increases and becoming closer in test performance at large data scales | Learner should notice that data quantity can materially change the relative importance of algorithm choice, while not eliminating the need for good modeling]]\n"
            "\n"
            "---\n"
            "\n"
            "## 6. Overfitting, underfitting, and regularization\n"
            "\n"
            "A model must learn enough structure to solve the task without learning accidental details that do not generalize.\n"
            "\n"
            "This is the tension between **underfitting** and **overfitting**.\n"
            "\n"
            "### Overfitting\n"
            "\n"
            "A model **overfits** when it performs very well on the training data but poorly on new data.\n"
            "\n"
            "The model has effectively learned patterns that are specific to the training sample rather than stable properties of the problem.\n"
            "\n"
            "This is more likely when:\n"
            "\n"
            "- the model is very flexible,\n"
            "- the training set is small,\n"
            "- the data is noisy,\n"
            "- irrelevant features are present.\n"
            "\n"
            "A complex model may discover accidental rules that happen to be true in the training set but have no real predictive meaning.\n"
            "\n"
            "### How to reduce overfitting\n"
            "\n"
            "The chapter gives three major strategies:\n"
            "\n"
            "1. **Simplify the model.**\n"
            "2. **Gather more training data.**\n"
            "3. **Reduce noise or correct data problems.**\n"
            "\n"
            "Simplifying may mean:\n"
            "\n"
            "- using fewer parameters,\n"
            "- using fewer features,\n"
            "- constraining the model.\n"
            "\n"
            "### Regularization\n"
            "\n"
            "**Regularization** deliberately constrains a model to reduce the risk of overfitting.\n"
            "\n"
            "The idea is a tradeoff:\n"
            "\n"
            "```text\n"
            "too much flexibility\n"
            "-> can fit noise\n"
            "\n"
            "too little flexibility\n"
            "-> may miss real structure\n"
            "\n"
            "appropriate regularization\n"
            "-> enough flexibility to learn, enough constraint to generalize\n"
            "```\n"
            "\n"
            "For a linear model, a regularization constraint can discourage extreme parameter values. The model may fit the training data slightly worse while predicting unseen examples better.\n"
            "\n"
            "[[IMAGE_NEEDED: Regularization and generalization (Figure 1-24; key: regularization-reduces-overfitting) | Recreate the source comparison of linear models where the regularized model fits the original training examples less aggressively but generalizes better to examples that were not used during fitting | Learner should notice that the best training fit is not necessarily the best model for unseen data]]\n"
            "\n"
            "The **regularization strength** is a hyperparameter. If it is too weak, the model may overfit. If it is too strong, the model may become too simple.\n"
            "\n"
            "### Underfitting\n"
            "\n"
            "A model **underfits** when it is too simple to capture the important structure of the data.\n"
            "\n"
            "Typical signs include poor performance even on the training set.\n"
            "\n"
            "Possible fixes include:\n"
            "\n"
            "1. choose a more powerful model,\n"
            "2. create or select better features,\n"
            "3. reduce excessive constraints or regularization.\n"
            "\n"
            "### Diagnose before you “improve”\n"
            "\n"
            "A common beginner mistake is to react to every bad result by choosing a more complicated model.\n"
            "\n"
            "Instead, compare evidence.\n"
            "\n"
            "```text\n"
            "training performance poor\n"
            "-> suspect underfitting, poor features, or difficult/noisy data\n"
            "\n"
            "training performance strong\n"
            "but validation/test performance poor\n"
            "-> suspect overfitting\n"
            "```\n"
            "\n"
            "Model complexity should be a response to the diagnosis, not a default goal.\n"
            "\n"
            "### Deployment is another source of failure\n"
            "\n"
            "Even an accurate model may be unsuitable for production.\n"
            "\n"
            "Possible deployment problems include:\n"
            "\n"
            "- model too slow,\n"
            "- model too large,\n"
            "- memory requirements too high,\n"
            "- system does not scale,\n"
            "- security vulnerabilities,\n"
            "- difficult maintenance,\n"
            "- model becomes stale,\n"
            "- expensive retraining.\n"
            "\n"
            "This is why real ML systems need operational engineering in addition to statistical modeling. The chapter points to **MLOps** as the discipline that handles many of these production concerns.\n"
            "\n"
            "---\n"
            "\n"
            "## 7. Testing, validation, model selection, and data mismatch\n"
            "\n"
            "A model is useful only if it works on cases it has not already memorized.\n"
            "\n"
            "So evaluation must protect us from fooling ourselves.\n"
            "\n"
            "### Training set and test set\n"
            "\n"
            "A basic strategy is to divide the data into:\n"
            "\n"
            "```text\n"
            "training set\n"
            "+\n"
            "test set\n"
            "```\n"
            "\n"
            "The model learns from the training set.\n"
            "\n"
            "The test set estimates performance on unseen data.\n"
            "\n"
            "The error on unseen examples is the **generalization error** or **out-of-sample error**.\n"
            "\n"
            "If training error is low but test error is high, the model is probably overfitting.\n"
            "\n"
            "An `80/20` split is common, but it is not a law. With millions of examples, a much smaller percentage may still produce a very large and reliable test set.\n"
            "\n"
            "### Why the test set must stay untouched\n"
            "\n"
            "Suppose you compare many model types and hyperparameter settings using the test set.\n"
            "\n"
            "Each time you make a decision based on test performance, information from the test set influences the design.\n"
            "\n"
            "Eventually you may choose a model that is unusually good on that particular test set rather than truly good on future data.\n"
            "\n"
            "The test set has effectively become part of training.\n"
            "\n"
            "That is why model selection needs another dataset.\n"
            "\n"
            "### Validation set\n"
            "\n"
            "A **validation set**, also called a **development set** or **dev set**, is used to choose models and hyperparameters.\n"
            "\n"
            "A sound workflow is:\n"
            "\n"
            "```text\n"
            "training set -> fit candidate models\n"
            "validation set -> compare candidates and tune hyperparameters\n"
            "test set -> evaluate the final selected system once\n"
            "```\n"
            "\n"
            "After model selection, the best configuration can be retrained using the full training data available for fitting, including data that had temporarily been held out for validation, and then evaluated on the untouched test set.\n"
            "\n"
            "[[IMAGE_NEEDED: Holdout validation workflow (Figure 1-25; key: holdout-validation-workflow) | Recreate the source flow in which multiple models are trained on a reduced training set, compared on a validation/dev set, the best configuration is retrained on the full training data, and the final model is evaluated on the untouched test set | Learner should notice the separate roles of validation data for decisions and test data for final generalization estimation]]\n"
            "\n"
            "### Cross-validation\n"
            "\n"
            "A single validation set can be unstable when data is limited.\n"
            "\n"
            "If it is too small, the performance estimate is noisy.\n"
            "\n"
            "If it is too large, too little data remains for fitting candidate models.\n"
            "\n"
            "**Cross-validation** repeatedly changes which portion acts as validation data.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "split 1: train on most folds, validate on fold A\n"
            "split 2: train on most folds, validate on fold B\n"
            "split 3: train on most folds, validate on fold C\n"
            "...\n"
            "average the validation results\n"
            "```\n"
            "\n"
            "This gives a more stable estimate at the cost of training the model multiple times.\n"
            "\n"
            "### Data mismatch\n"
            "\n"
            "Sometimes abundant training data is easy to obtain, but real production data is scarce.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "training data: flower images downloaded from the web\n"
            "production data: flower photos taken by users with a mobile app\n"
            "```\n"
            "\n"
            "The two distributions may differ in:\n"
            "\n"
            "- camera quality,\n"
            "- framing,\n"
            "- lighting,\n"
            "- backgrounds,\n"
            "- resolution,\n"
            "- user behavior.\n"
            "\n"
            "The validation and test sets should resemble the **production data you actually care about**, not merely the abundant training source.\n"
            "\n"
            "But this creates a diagnostic problem.\n"
            "\n"
            "If a model is poor on the production-like dev set, is it:\n"
            "\n"
            "```text\n"
            "overfitting the training source?\n"
            "or\n"
            "suffering from mismatch between the training source and production data?\n"
            "```\n"
            "\n"
            "### Train-dev set\n"
            "\n"
            "A **train-dev set** helps separate these explanations.\n"
            "\n"
            "Use data from the same source as the training set but keep it out of training.\n"
            "\n"
            "Then compare:\n"
            "\n"
            "```text\n"
            "training set:\n"
            "used to fit the model\n"
            "\n"
            "train-dev set:\n"
            "same distribution as training data\n"
            "not used for fitting\n"
            "helps diagnose overfitting\n"
            "\n"
            "dev set:\n"
            "production-like distribution\n"
            "used for model development\n"
            "helps reveal data mismatch\n"
            "\n"
            "test set:\n"
            "production-like distribution\n"
            "used for final evaluation\n"
            "```\n"
            "\n"
            "Interpretation:\n"
            "\n"
            "```text\n"
            "poor train-dev performance\n"
            "-> the model is not generalizing even to the training distribution\n"
            "-> suspect overfitting or other model/data problems\n"
            "\n"
            "good train-dev performance\n"
            "but poor dev performance\n"
            "-> suspect data mismatch\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Train-dev strategy for data mismatch (Figure 1-26; key: train-dev-data-mismatch) | Recreate the source diagram with abundant training-source data divided into Train and Train-dev, while scarce production-like real data is divided into Dev and Test | Learner should notice that Train-dev separates ordinary overfitting from a mismatch between the training distribution and the production distribution]]\n"
            "\n"
            "### The No Free Lunch idea\n"
            "\n"
            "Choosing a model means making assumptions.\n"
            "\n"
            "A linear model assumes that a roughly linear structure is a useful approximation.\n"
            "\n"
            "A more flexible model makes different assumptions and can represent different patterns.\n"
            "\n"
            "The **No Free Lunch theorem** says that if you make no assumptions about the data-generating problem at all, no learning algorithm is guaranteed to be better than every other algorithm on every possible problem.\n"
            "\n"
            "Practical consequence:\n"
            "\n"
            "> Do not search for a universally “best” model.\n"
            "\n"
            "Instead:\n"
            "\n"
            "1. use knowledge of the problem to choose a small set of reasonable approaches,\n"
            "2. compare them using sound validation,\n"
            "3. keep the test set for the final estimate.\n"
            "\n"
            "### The full picture\n"
            "\n"
            "A reliable machine-learning project connects all of the chapter’s ideas:\n"
            "\n"
            "```text\n"
            "define task and metric\n"
            "        |\n"
            "collect representative data\n"
            "        |\n"
            "clean and engineer features\n"
            "        |\n"
            "choose learning setup\n"
            "        |\n"
            "select model family\n"
            "        |\n"
            "train\n"
            "        |\n"
            "validate and tune\n"
            "        |\n"
            "test once on held-out data\n"
            "        |\n"
            "deploy\n"
            "        |\n"
            "monitor data + model\n"
            "        |\n"
            "retrain or update when needed\n"
            "```\n"
            "\n"
            "{{exercise:M01.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> If a model has almost zero training error, it must be excellent.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Training performance only shows how well the model handles examples used during learning. A highly flexible model can memorize or exploit accidental patterns. Generalization to unseen data is the real objective.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> More data always fixes the problem.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "More data helps only when it is relevant and sufficiently representative. Millions of biased or incorrectly labeled examples can still produce a bad system.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> Online learning means the model must be learning live on the internet.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "“Online” refers to incremental learning. An incremental algorithm may process data offline, including very large datasets that do not fit into memory.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> A hyperparameter is just another model parameter.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Model parameters are learned from data during training. Hyperparameters configure the learning process or model structure and are selected outside that ordinary fitting step.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> The test set is the best place to choose models and tune hyperparameters.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Repeatedly using test performance to guide decisions leaks information from the test set into development. Use validation data for decisions and reserve the test set for final evaluation.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Machine learning | Building systems that improve at a task from experience/data rather than relying only on explicitly programmed rules |\n"
            "| Training set | Data used by the learning algorithm to fit a model |\n"
            "| Training instance / sample | One example in a dataset |\n"
            "| Model | The learned system or mathematical structure used to make predictions |\n"
            "| Feature | An input variable used by a model |\n"
            "| Label / target | The desired output in supervised learning |\n"
            "| Classification | Predicting a category |\n"
            "| Regression | Predicting a numeric value |\n"
            "| Supervised learning | Learning from examples with desired outputs |\n"
            "| Unsupervised learning | Learning structure from unlabeled data |\n"
            "| Semi-supervised learning | Learning from a small labeled set plus a larger unlabeled set |\n"
            "| Self-supervised learning | Creating supervision automatically from unlabeled data |\n"
            "| Transfer learning | Reusing knowledge learned for one task to help another task |\n"
            "| Reinforcement learning | Learning a policy through actions and rewards in an environment |\n"
            "| Batch learning | Training on the available dataset as a separate full training process |\n"
            "| Online learning | Updating a model incrementally from new examples or mini-batches |\n"
            "| Out-of-core learning | Incremental processing of a dataset too large to fit in memory |\n"
            "| Data drift | Change in the data or real-world relationship that can reduce a deployed model’s performance |\n"
            "| Instance-based learning | Predicting by comparing new cases with stored examples |\n"
            "| Model-based learning | Fitting a predictive model to training examples and using it for new cases |\n"
            "| Generalization | Performing well on examples not seen during training |\n"
            "| Model parameter | A value learned during model training |\n"
            "| Hyperparameter | A configuration chosen outside ordinary model-parameter fitting |\n"
            "| Loss / cost function | A function measuring how bad model predictions are |\n"
            "| Inference | Using a trained model to make predictions |\n"
            "| Sampling bias | Systematic nonrepresentativeness caused by how data was sampled |\n"
            "| Feature engineering | Selecting, extracting, transforming, or creating useful features |\n"
            "| Overfitting | Fitting training data too closely and generalizing poorly |\n"
            "| Underfitting | Using a model too simple to capture the important structure |\n"
            "| Regularization | Constraining a model to reduce overfitting |\n"
            "| Validation / dev set | Data used for model selection and hyperparameter tuning |\n"
            "| Test set | Held-out data used to estimate final generalization performance |\n"
            "| Train-dev set | Held-out training-distribution data used to separate overfitting from data mismatch |\n"
            "| Generalization error | Error measured on unseen cases |\n"
            "| MLOps | Engineering practices for deploying, operating, monitoring, and updating ML systems |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What are task `T`, experience `E`, and performance measure `P` in the spam-filter example?\n"
            "2. Why is downloading a huge collection of data not automatically machine learning?\n"
            "3. How do classification and regression differ?\n"
            "4. How do supervised, unsupervised, semi-supervised, self-supervised, and reinforcement learning differ in their learning signal?\n"
            "5. Why can online learning be useful even when the system is not learning live in production?\n"
            "6. What is the difference between instance-based and model-based generalization?\n"
            "7. What is the difference between a model parameter and a hyperparameter?\n"
            "8. Why can a huge dataset still fail because of sampling bias?\n"
            "9. How would you distinguish overfitting from underfitting using training and validation/test performance?\n"
            "10. Why should hyperparameter tuning use validation data rather than the final test set?\n"
            "11. What problem does a train-dev set help diagnose?\n"
            "12. What practical lesson should you take from the No Free Lunch theorem?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**Machine learning is not mainly about choosing a clever algorithm. It is about building a system that learns useful patterns from appropriate data and proves that those patterns generalize to new cases. The quality of the data, the learning setup, the model’s capacity, the evaluation design, and the production environment all matter.**\n"
        ),

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "what-is-ml",
                "title": "What machine learning is — and why we use it",
                "order": 1,
            },
            {
                "id": "training-supervision",
                "title": "Learning by supervision: what kind of feedback does the model receive?",
                "order": 2,
            },
            {
                "id": "batch-online",
                "title": "Batch learning versus online learning",
                "order": 3,
            },
            {
                "id": "generalization-workflow",
                "title": "Generalization: instance-based versus model-based learning",
                "order": 4,
            },
            {
                "id": "data-challenges",
                "title": "The data can make or break the system",
                "order": 5,
            },
            {
                "id": "model-challenges",
                "title": "Overfitting, underfitting, and regularization",
                "order": 6,
            },
            {
                "id": "evaluation-validation",
                "title": "Testing, validation, model selection, and data mismatch",
                "order": 7,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Classify the Learning System",

            "lesson_code": "M01.L01",

            "section_id": "batch-online",

            "placement": "after_section",

            "description": (
                "Practice classifying ML systems across independent dimensions "
                "instead of treating labels such as supervised, online, and "
                "model-based as mutually exclusive categories."
            ),

            "instructions": (
                "For each scenario below, classify the system by (a) training "
                "supervision, (b) batch versus online learning, and (c) "
                "instance-based versus model-based learning where the chapter "
                "provides enough information.\n\n"
                "1. A spam classifier is trained from human-labeled spam/ham "
                "messages, deployed, and incrementally updated every time users "
                "flag new spam.\n"
                "2. A retailer runs k-means on unlabeled purchase histories to "
                "discover customer groups.\n"
                "3. A k-nearest-neighbors regressor stores known examples and "
                "predicts a new value from the three closest examples.\n"
                "4. An image model learns by reconstructing masked regions of "
                "millions of unlabeled images before being fine-tuned on a small "
                "labeled pet dataset.\n"
                "5. A robot chooses actions, receives rewards or penalties, and "
                "improves the policy it uses to move.\n\n"
                "For each answer, write one sentence explaining which part of "
                "the scenario provides the evidence for your classification."
            ),

            "expected_output": (
                "A five-row table containing the scenario number, supervision "
                "type, update mode, generalization approach when identifiable, "
                "and a short justification. If one dimension cannot be "
                "determined from the scenario, explicitly write 'not specified' "
                "instead of guessing."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "ml-system-classification",
                "supervision-types",
                "batch-vs-online",
                "instance-vs-model",
                "reasoning",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Diagnose an ML Project",

            "lesson_code": "M01.L01",

            "section_id": "evaluation-validation",

            "placement": "after_section",

            "description": (
                "Use training, train-dev, dev, and test behavior to identify "
                "overfitting, data mismatch, and evaluation mistakes."
            ),

            "instructions": (
                "A flower classifier is trained mostly on high-quality web "
                "images, while the final product receives mobile-phone photos. "
                "Consider these observations:\n\n"
                "- Training accuracy: 99%.\n"
                "- Train-dev accuracy on held-out web images: 98%.\n"
                "- Dev accuracy on real mobile photos: 82%.\n"
                "- The team repeatedly tries hyperparameters until test "
                "accuracy is maximized.\n\n"
                "1. Is ordinary overfitting to the web training set the main "
                "problem suggested by the train versus train-dev results? Why?\n"
                "2. What do the train-dev versus dev results suggest?\n"
                "3. Propose two actions that address the most likely problem.\n"
                "4. Explain why repeatedly tuning against the test set is "
                "methodologically wrong.\n"
                "5. Redesign the roles of Train, Train-dev, Dev, and Test for "
                "this project."
            ),

            "expected_output": (
                "A concise written diagnosis identifying data mismatch as the "
                "main issue suggested by the supplied metrics, followed by two "
                "appropriate corrective actions and a correct four-set "
                "evaluation plan that keeps the final test set untouched during "
                "model development."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "generalization",
                "overfitting-diagnosis",
                "data-mismatch",
                "train-dev",
                "validation-design",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "The Machine Learning Landscape — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",

                "section_id": "what-is-ml",

                "question": (
                    "Which statement best captures what makes a system a "
                    "machine-learning system?"
                ),

                "options": [
                    "It stores a very large amount of information.",
                    "Its performance on a task improves through experience or data.",
                    "It contains at least one neural network.",
                    "It runs without any human-written code.",
                ],

                "correct": 1,

                "explanation": (
                    "Machine learning is defined by improvement on a task through "
                    "experience/data. Large storage, neural networks, or the "
                    "absence of hand-written code are not required."
                ),
            },

            {
                "id": "M01.L01.Q02",

                "section_id": "training-supervision",

                "question": (
                    "A dataset contains customer behavior but no customer-segment "
                    "labels. You want the system to discover groups of similar "
                    "customers. Which task best matches this goal?"
                ),

                "options": [
                    "Regression",
                    "Supervised classification",
                    "Clustering",
                    "Reinforcement learning",
                ],

                "correct": 2,

                "explanation": (
                    "Clustering is an unsupervised task that discovers groups in "
                    "unlabeled data."
                ),
            },

            {
                "id": "M01.L01.Q03",

                "section_id": "training-supervision",

                "question": (
                    "What is the key idea behind self-supervised learning?"
                ),

                "options": [
                    "A human manually labels every example.",
                    "The system receives only rewards and penalties.",
                    "Training labels or targets are generated from the unlabeled data itself.",
                    "The model stores examples and uses nearest-neighbor search.",
                ],

                "correct": 2,

                "explanation": (
                    "Self-supervised learning creates a supervised-style task from "
                    "the structure of raw unlabeled data, such as predicting a "
                    "masked portion of an input."
                ),
            },

            {
                "id": "M01.L01.Q04",

                "section_id": "batch-online",

                "question": (
                    "Which statement about online learning is correct?"
                ),

                "options": [
                    "It always happens on a live production server.",
                    "It means the model is updated incrementally from examples or mini-batches.",
                    "It requires the full dataset to be loaded into memory at once.",
                    "It cannot be used for out-of-core learning.",
                ],

                "correct": 1,

                "explanation": (
                    "Online learning means incremental learning. It can be used "
                    "offline and is especially useful for processing data in "
                    "chunks when the full dataset does not fit in memory."
                ),
            },

            {
                "id": "M01.L01.Q05",

                "section_id": "generalization-workflow",

                "question": (
                    "Which option correctly distinguishes a model parameter from "
                    "a hyperparameter?"
                ),

                "options": [
                    "Both are always learned automatically from the training data.",
                    "A model parameter is learned during fitting; a hyperparameter configures the learning process or model and is selected externally.",
                    "A hyperparameter is learned during fitting; a model parameter is always chosen manually.",
                    "There is no meaningful difference.",
                ],

                "correct": 1,

                "explanation": (
                    "Model parameters are fitted from data, while hyperparameters "
                    "such as regularization strength or k in k-NN are selected or "
                    "tuned outside ordinary parameter fitting."
                ),
            },

            {
                "id": "M01.L01.Q06",

                "section_id": "data-challenges",

                "question": (
                    "Why can a dataset with millions of examples still be a bad "
                    "training set?"
                ),

                "options": [
                    "Large datasets always make models underfit.",
                    "A large sample can still be systematically nonrepresentative because of sampling bias.",
                    "Machine learning works only with small datasets.",
                    "Large datasets cannot contain labels.",
                ],

                "correct": 1,

                "explanation": (
                    "Sample size does not remove systematic bias in the way data "
                    "was collected. A huge but unrepresentative dataset can still "
                    "generalize poorly."
                ),
            },

            {
                "id": "M01.L01.Q07",

                "section_id": "model-challenges",

                "question": (
                    "A model has extremely low training error but much worse "
                    "validation error. What is the most likely diagnosis?"
                ),

                "options": [
                    "Underfitting",
                    "Overfitting",
                    "Perfect generalization",
                    "The validation set has been used correctly, so no diagnosis is possible",
                ],

                "correct": 1,

                "explanation": (
                    "A large gap between strong training performance and weak "
                    "unseen-data performance is a classic sign of overfitting."
                ),
            },

            {
                "id": "M01.L01.Q08",

                "section_id": "evaluation-validation",

                "question": (
                    "Why should the final test set not be used repeatedly for "
                    "hyperparameter tuning?"
                ),

                "options": [
                    "Test sets cannot contain labels.",
                    "Repeated decisions based on test performance leak test-set information into development and make the final estimate optimistic.",
                    "Hyperparameters can only be tuned on the training set.",
                    "The test set must always be larger than the training set.",
                ],

                "correct": 1,

                "explanation": (
                    "Once test performance guides model decisions, the test set is "
                    "no longer an independent estimate of generalization. Use a "
                    "validation/dev set for tuning."
                ),
            },

            {
                "id": "M01.L01.Q09",

                "section_id": "evaluation-validation",

                "type": "open",

                "question": (
                    "A model performs well on a train-dev set drawn from the same "
                    "source as the training data, but poorly on a dev set that "
                    "matches production. What is the most likely problem, and "
                    "what would you change first?"
                ),
            },

            {
                "id": "M01.L01.Q10",

                "section_id": "evaluation-validation",

                "type": "open",

                "question": (
                    "Explain the practical lesson of the No Free Lunch theorem in "
                    "your own words. Why should it change how you approach model "
                    "selection?"
                ),
            },
        ],

        "passing_score": 70,
    },
}
