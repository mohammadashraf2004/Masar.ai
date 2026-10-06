"""M06.L01 — The Universal Workflow of Machine Learning.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 6, page range not provided in supplied source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M06.L01"

MODULE_ORDER = 6

MODULE_TITLE = "The Universal Workflow of Machine Learning"

MODULE_DESCRIPTION = (
    "Learn the complete lifecycle of a real machine learning project: frame "
    "the problem, collect and understand data, define success, build and "
    "validate a model, deploy it, monitor production behavior, and maintain "
    "the system as data and requirements change."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Chapter 6 — page range not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "The Universal Workflow of Machine Learning",

    "slug": "deep-learning-foundations-m06-l01",

    "description": (
        "Understand how real machine learning projects move from a business "
        "problem to data collection, model development, deployment, "
        "monitoring, and continuous improvement."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.25,

    "skill_tags": [
        "machine-learning",
        "ml-workflow",
        "problem-framing",
        "data-collection",
        "data-quality",
        "validation",
        "baseline",
        "generalization",
        "deployment",
        "monitoring",
        "concept-drift",
        "module-06",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "The Universal Workflow of Machine Learning",

        "content": (
            "# The Universal Workflow of Machine Learning\n"
            "\n"
            "> **Course:** Deep Learning Foundations  \n"
            "> **Lesson:** M06.L01  \n"
            "> **Module:** The Universal Workflow of Machine Learning  \n"
            "> **Source alignment:** BOOK-002, Chapter 6. "
            "The supplied source did not specify a page range. "
            "This lesson is an instructor-authored curriculum adaptation "
            "rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Learning outcomes
            # ----------------------------------------------------------------

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why real machine learning projects start from a problem "
            "rather than from a ready-made dataset.\n"
            "- Frame a business problem as an appropriate machine learning task.\n"
            "- Identify inputs, targets, constraints, and assumptions.\n"
            "- Explain why dataset quality and representativeness strongly affect "
            "generalization.\n"
            "- Recognize sampling bias, target leakage, and concept drift.\n"
            "- Choose a success metric that reflects the actual project goal.\n"
            "- Prepare data using vectorization, normalization, and missing-value "
            "handling.\n"
            "- Choose an appropriate validation strategy.\n"
            "- Explain what it means to beat a baseline and achieve statistical power.\n"
            "- Explain why deliberately reaching overfitting can help determine "
            "appropriate model capacity.\n"
            "- Tune and regularize a model using validation performance.\n"
            "- Distinguish validation data from final test data.\n"
            "- Select an appropriate deployment environment.\n"
            "- Explain inference optimization techniques such as pruning and "
            "quantization.\n"
            "- Explain why production monitoring and continuous data collection "
            "are part of the machine learning lifecycle.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. Define the Task Before Building the Model\n"
            "\n"
            "Tutorials often begin with a clean dataset and a clearly defined "
            "prediction task.\n"
            "\n"
            "Real projects usually do not.\n"
            "\n"
            "You normally begin with a problem such as:\n"
            "\n"
            "```text\n"
            "Detect fraudulent transactions.\n"
            "Recommend music to users.\n"
            "Identify spam messages.\n"
            "Predict whether somebody will click an advertisement.\n"
            "Find defective products on a production line.\n"
            "```\n"
            "\n"
            "Before training anything, you need to translate the real-world "
            "problem into a precise machine learning problem.\n"
            "\n"
            "A useful high-level workflow is:\n"
            "\n"
            "```text\n"
            "Real-world problem\n"
            "      ↓\n"
            "Define inputs and targets\n"
            "      ↓\n"
            "Choose task type\n"
            "      ↓\n"
            "Collect and understand data\n"
            "      ↓\n"
            "Choose success metric\n"
            "```\n"
            "\n"
            "### Start with the business context\n"
            "\n"
            "Ask why the problem matters.\n"
            "\n"
            "Questions to investigate include:\n"
            "\n"
            "- What value will solving this problem create?\n"
            "- Who will use the model?\n"
            "- How will predictions affect an existing process?\n"
            "- What input data is available?\n"
            "- What data could realistically be collected?\n"
            "- What are the latency, privacy, cost, or hardware constraints?\n"
            "- Is machine learning even the appropriate solution?\n"
            "\n"
            "A technically impressive model can still be useless if it solves "
            "the wrong problem.\n"
            "\n"
            "### Define inputs and targets\n"
            "\n"
            "Every supervised learning project requires examples containing:\n"
            "\n"
            "```text\n"
            "input X\n"
            "→ information available to the model\n"
            "\n"
            "target Y\n"
            "→ what the model is expected to predict\n"
            "```\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Spam detector\n"
            "\n"
            "Input:\n"
            "message content or derived message features\n"
            "\n"
            "Target:\n"
            "spam / not spam\n"
            "```\n"
            "\n"
            "You can only learn a prediction task when appropriate examples and "
            "targets exist or can be collected.\n"
            "\n"
            "### Identify the task type\n"
            "\n"
            "Once you understand the input and target, map the problem to the "
            "appropriate machine learning task.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "```text\n"
            "Spam detection\n"
            "→ binary classification\n"
            "\n"
            "Photo containing multiple concepts\n"
            "→ multiclass, multilabel classification\n"
            "\n"
            "Ad click-through rate prediction\n"
            "→ scalar regression\n"
            "\n"
            "Retrieve satellite images similar to known sites\n"
            "→ ranking / similarity problem\n"
            "```\n"
            "\n"
            "Do not force every problem into the same model type.\n"
            "\n"
            "Sometimes a non-deep-learning method—or even ordinary statistical "
            "analysis—is more appropriate.\n"
            "\n"
            "### Understand existing solutions\n"
            "\n"
            "Before replacing a process, learn how it works today.\n"
            "\n"
            "Perhaps the organization already uses:\n"
            "\n"
            "- manual review,\n"
            "- a rule-based system,\n"
            "- a statistical model,\n"
            "- or another machine learning model.\n"
            "\n"
            "This existing solution may become your baseline later.\n"
            "\n"
            "### Understand constraints early\n"
            "\n"
            "The environment where a model will run can change your technical "
            "choices dramatically.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Encrypted private messages\n"
            "→ server may not be allowed to see the input\n"
            "→ on-device inference may be required\n"
            "\n"
            "Factory inspection\n"
            "→ prediction must happen immediately\n"
            "→ low latency may be more important than maximum model size\n"
            "```\n"
            "\n"
            "### Recognize your assumptions\n"
            "\n"
            "At the start of a project, two major assumptions are being made:\n"
            "\n"
            "1. The target can be predicted from the proposed inputs.\n"
            "2. The available data contains enough information to learn that "
            "relationship.\n"
            "\n"
            "These are hypotheses, not guarantees.\n"
            "\n"
            "If the required information is not present in the input, a more "
            "powerful neural network will not magically create it.\n"
            "\n"
            "### Consider ethical consequences\n"
            "\n"
            "A machine learning project is not automatically valid simply "
            "because it is technically possible to build a model.\n"
            "\n"
            "You should ask:\n"
            "\n"
            "- Is the target meaningful and valid?\n"
            "- Could the labels encode human prejudice?\n"
            "- Who could be harmed by incorrect predictions?\n"
            "- Does deployment make questionable judgments appear more objective "
            "simply because an algorithm produced them?\n"
            "\n"
            "Technical design choices can have real-world consequences.\n"
            "\n"
            "### Data collection is often the hardest part\n"
            "\n"
            "Once the task is defined, you need data.\n"
            "\n"
            "This often means:\n"
            "\n"
            "```text\n"
            "collect examples\n"
            "      ↓\n"
            "create annotations\n"
            "      ↓\n"
            "verify annotation quality\n"
            "      ↓\n"
            "store and version the dataset\n"
            "```\n"
            "\n"
            "For supervised learning, labels may come from:\n"
            "\n"
            "- existing historical records,\n"
            "- user behavior,\n"
            "- sensors,\n"
            "- human annotators,\n"
            "- domain experts,\n"
            "- or specialized labeling services.\n"
            "\n"
            "### Annotation quality matters\n"
            "\n"
            "The quality of your labels directly affects what your model can "
            "learn.\n"
            "\n"
            "A medical dataset may require qualified specialists, while a simple "
            "cat-versus-dog dataset may not.\n"
            "\n"
            "Poor or inconsistent annotations create noisy targets.\n"
            "\n"
            "If the targets themselves are unreliable, even a highly optimized "
            "model may produce poor results.\n"
            "\n"
            "### Representative data\n"
            "\n"
            "Training data should resemble the data the model will encounter "
            "after deployment.\n"
            "\n"
            "Imagine training a food-recognition model using professionally lit "
            "restaurant photographs.\n"
            "\n"
            "Production users then upload:\n"
            "\n"
            "```text\n"
            "dark phone photos\n"
            "unusual camera angles\n"
            "partially eaten meals\n"
            "motion blur\n"
            "different lighting\n"
            "```\n"
            "\n"
            "A model may achieve excellent test accuracy on data similar to its "
            "training set and still perform badly in production.\n"
            "\n"
            "The problem is not necessarily the neural network.\n"
            "\n"
            "The dataset may simply not represent reality.\n"
            "\n"
            "### Concept drift\n"
            "\n"
            "Even representative data does not stay representative forever.\n"
            "\n"
            "Production behavior may change over time.\n"
            "\n"
            "This is called **concept drift**.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "```text\n"
            "fraud strategies change\n"
            "language changes\n"
            "consumer preferences change\n"
            "product catalogs change\n"
            "music tastes change\n"
            "```\n"
            "\n"
            "A model trained on past data assumes that future data will retain "
            "useful similarities to the past.\n"
            "\n"
            "That assumption must be monitored after deployment.\n"
            "\n"
            "### Sampling bias\n"
            "\n"
            "Sampling bias occurs when the examples you collect are not a "
            "representative sample of the population or environment you care "
            "about.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "population you care about\n"
            "        ≠\n"
            "population your dataset represents\n"
            "```\n"
            "\n"
            "If the dataset systematically excludes or overrepresents certain "
            "groups, your measurements and model behavior can become biased.\n"
            "\n"
            "### Understand your dataset before training\n"
            "\n"
            "Do not treat data as a black box.\n"
            "\n"
            "Before model development:\n"
            "\n"
            "- inspect raw examples,\n"
            "- inspect their labels,\n"
            "- visualize numerical distributions,\n"
            "- examine missing values,\n"
            "- check class balance,\n"
            "- inspect geographic patterns when location matters,\n"
            "- and investigate suspicious features.\n"
            "\n"
            "### Target leakage\n"
            "\n"
            "A dangerous problem occurs when a feature contains information "
            "about the target that would not actually be available when the "
            "model is used.\n"
            "\n"
            "For example, suppose you want to predict whether a patient will "
            "later be diagnosed with a disease, but one of your training "
            "features directly records that diagnosis.\n"
            "\n"
            "The model appears excellent during development because the answer "
            "is effectively hidden inside the input.\n"
            "\n"
            "In production, that information may not exist yet.\n"
            "\n"
            "Always ask:\n"
            "\n"
            "> Will this exact feature be available at prediction time?\n"
            "\n"
            "### Define success before training\n"
            "\n"
            "You cannot optimize a project effectively without deciding how "
            "success will be measured.\n"
            "\n"
            "Possible metrics include:\n"
            "\n"
            "```text\n"
            "accuracy\n"
            "precision\n"
            "recall\n"
            "ROC AUC\n"
            "false-positive rate\n"
            "false-negative rate\n"
            "customer retention\n"
            "business revenue\n"
            "```\n"
            "\n"
            "The chosen metric should reflect the real goal of the project.\n"
            "\n"
            "For example, in fraud detection, false negatives and false "
            "positives may matter much more than an abstract overall accuracy "
            "number.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Develop a Model That Actually Generalizes\n"
            "\n"
            "Once the problem, data, and success criteria are understood, model "
            "development can begin.\n"
            "\n"
            "The development process can be summarized as:\n"
            "\n"
            "```text\n"
            "Prepare data\n"
            "    ↓\n"
            "Choose validation protocol\n"
            "    ↓\n"
            "Beat a simple baseline\n"
            "    ↓\n"
            "Increase capacity until overfitting appears\n"
            "    ↓\n"
            "Regularize and tune\n"
            "    ↓\n"
            "Train final model\n"
            "    ↓\n"
            "Evaluate once on test data\n"
            "```\n"
            "\n"
            "### Data vectorization\n"
            "\n"
            "Neural networks operate on tensors.\n"
            "\n"
            "Raw data therefore has to be transformed into numerical "
            "representations suitable for the model.\n"
            "\n"
            "This process is called **vectorization**.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "```text\n"
            "text\n"
            "→ numerical token representations\n"
            "\n"
            "image\n"
            "→ tensor of pixel values\n"
            "\n"
            "tabular record\n"
            "→ feature vector\n"
            "```\n"
            "\n"
            "### Value normalization\n"
            "\n"
            "Neural networks generally train more easily when numerical inputs "
            "have reasonable and relatively homogeneous scales.\n"
            "\n"
            "Problematic input:\n"
            "\n"
            "```text\n"
            "feature A → 0.1 to 0.8\n"
            "feature B → 500 to 50,000\n"
            "feature C → -3 to 4\n"
            "```\n"
            "\n"
            "A common normalization procedure is:\n"
            "\n"
            "```python\n"
            "x -= x.mean(axis=0)\n"
            "x /= x.std(axis=0)\n"
            "```\n"
            "\n"
            "Afterward, each feature is roughly centered around zero with a "
            "standard deviation near one.\n"
            "\n"
            "Another common case is image scaling:\n"
            "\n"
            "```text\n"
            "0–255 pixel values\n"
            "       ↓ divide by 255\n"
            "0–1 values\n"
            "```\n"
            "\n"
            "### Handling missing values\n"
            "\n"
            "Real datasets often contain incomplete records.\n"
            "\n"
            "For categorical features, one possible strategy is to introduce "
            "a dedicated category representing a missing value.\n"
            "\n"
            "For numerical features, possible strategies include replacing the "
            "missing value using statistics such as the mean or median.\n"
            "\n"
            "The important principle is to handle missingness deliberately "
            "rather than pretending it does not exist.\n"
            "\n"
            "If missing values will occur in production, training should expose "
            "the model to similar situations whenever possible.\n"
            "\n"
            "### Choose an evaluation protocol\n"
            "\n"
            "The purpose of validation is to estimate how well your model will "
            "generalize to unseen production data.\n"
            "\n"
            "Three common strategies are:\n"
            "\n"
            "```text\n"
            "Hold-out validation\n"
            "→ useful when plenty of data is available\n"
            "\n"
            "K-fold cross-validation\n"
            "→ useful when the dataset is small\n"
            "\n"
            "Iterated K-fold validation\n"
            "→ useful when you need an even more reliable estimate from limited data\n"
            "```\n"
            "\n"
            "Regardless of the method, validation data should represent the "
            "production distribution and should not contain duplicated or "
            "near-duplicated examples from the training set.\n"
            "\n"
            "### Beat a baseline first\n"
            "\n"
            "Your first modeling goal is not to build the most complicated "
            "network possible.\n"
            "\n"
            "It is to beat a reasonable baseline.\n"
            "\n"
            "A baseline might be:\n"
            "\n"
            "- random guessing,\n"
            "- predicting the majority class,\n"
            "- predicting the average target,\n"
            "- an existing rule-based system,\n"
            "- or a simple statistical model.\n"
            "\n"
            "If your model cannot beat a simple baseline, increasing model "
            "complexity may not solve the real problem.\n"
            "\n"
            "Perhaps the inputs simply do not contain enough useful information.\n"
            "\n"
            "### Statistical power\n"
            "\n"
            "When your model reliably performs better than a meaningful "
            "baseline, it demonstrates that useful predictive signal exists.\n"
            "\n"
            "The chapter refers to this as achieving **statistical power**.\n"
            "\n"
            "At this point, you know that learning something useful from the "
            "data is possible.\n"
            "\n"
            "### Architecture priors\n"
            "\n"
            "Choosing the model architecture should reflect the structure of "
            "the problem.\n"
            "\n"
            "Depending on the task, you might consider:\n"
            "\n"
            "```text\n"
            "Dense network\n"
            "ConvNet\n"
            "recurrent architecture\n"
            "Transformer\n"
            "or even a non-deep-learning approach\n"
            "```\n"
            "\n"
            "Researching previous successful approaches for similar problems "
            "can save substantial time.\n"
            "\n"
            "### Loss functions are not always business metrics\n"
            "\n"
            "The metric used to evaluate project success is not always suitable "
            "as a differentiable training loss.\n"
            "\n"
            "For example, a project might be evaluated using ROC AUC, but the "
            "model may be trained using crossentropy because crossentropy works "
            "well with gradient-based optimization.\n"
            "\n"
            "The loss is therefore sometimes a trainable proxy for the metric "
            "you ultimately care about.\n"
            "\n"
            "### Common output configurations\n"
            "\n"
            "| Task | Last activation | Common loss | Example metric |\n"
            "|---|---|---|---|\n"
            "| Binary classification | Sigmoid | Binary crossentropy | Accuracy / ROC AUC |\n"
            "| Single-label multiclass classification | Softmax | Categorical crossentropy | Accuracy / top-k accuracy |\n"
            "| Multilabel classification | Sigmoid | Binary crossentropy | Binary accuracy / ROC AUC |\n"
            "| Regression | None | Mean squared error | Mean absolute error |\n"
            "\n"
            "### Why deliberately create an overfitting model?\n"
            "\n"
            "Once your small model beats the baseline, you need to know whether "
            "it has enough capacity.\n"
            "\n"
            "A useful strategy is to increase model capacity until you can "
            "clearly observe overfitting.\n"
            "\n"
            "You can do this by:\n"
            "\n"
            "```text\n"
            "adding more layers\n"
            "making layers larger\n"
            "training for more epochs\n"
            "```\n"
            "\n"
            "You are looking for behavior like:\n"
            "\n"
            "```text\n"
            "training performance continues improving\n"
            "validation performance begins getting worse\n"
            "```\n"
            "\n"
            "Why intentionally cross into overfitting?\n"
            "\n"
            "Because now you know the model has enough capacity to fit the "
            "training problem.\n"
            "\n"
            "The useful model capacity lies near the boundary between:\n"
            "\n"
            "```text\n"
            "underfitting\n"
            "        ↕\n"
            "good generalization\n"
            "        ↕\n"
            "overfitting\n"
            "```\n"
            "\n"
            "### Regularization and tuning\n"
            "\n"
            "Once the model can overfit, the next objective is to maximize "
            "generalization.\n"
            "\n"
            "Possible experiments include:\n"
            "\n"
            "- changing the number of layers,\n"
            "- changing the number of units,\n"
            "- adding dropout,\n"
            "- adding L1 or L2 regularization,\n"
            "- changing the learning rate,\n"
            "- changing other hyperparameters,\n"
            "- improving feature engineering,\n"
            "- removing useless features,\n"
            "- collecting more data,\n"
            "- improving annotation quality.\n"
            "\n"
            "Each experiment should be judged using validation data—not the "
            "final test set.\n"
            "\n"
            "### Validation overfitting\n"
            "\n"
            "There is a subtle danger here.\n"
            "\n"
            "If you repeatedly make decisions based on one validation set, you "
            "are gradually adapting your entire development process to that "
            "validation set.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "train model\n"
            "   ↓\n"
            "check validation\n"
            "   ↓\n"
            "change architecture\n"
            "   ↓\n"
            "check validation\n"
            "   ↓\n"
            "change hyperparameters\n"
            "   ↓\n"
            "check validation\n"
            "   ↓\n"
            "repeat many times\n"
            "```\n"
            "\n"
            "Eventually, the development process itself may overfit the "
            "validation data.\n"
            "\n"
            "That is why a separate test set is still needed.\n"
            "\n"
            "### Final model evaluation\n"
            "\n"
            "After selecting the final configuration:\n"
            "\n"
            "1. Train the final model using the available development data.\n"
            "2. Evaluate it one final time on the untouched test set.\n"
            "\n"
            "If test performance is substantially worse than validation "
            "performance, your validation procedure may have been unreliable or "
            "your development process may have overfit the validation data.\n"
            "\n"

            # Exercise EX01 is rendered here by the frontend.
            "{{exercise:M06.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Deploy the Model as Part of a Real System\n"
            "\n"
            "A model sitting inside a notebook is not yet a production machine "
            "learning system.\n"
            "\n"
            "After successful final evaluation, the model must be integrated "
            "into the environment where people or software will actually use "
            "its predictions.\n"
            "\n"
            "### Set realistic expectations\n"
            "\n"
            "Stakeholders may assume that an AI system understands a problem "
            "like a human or that a high accuracy number means near-perfect "
            "behavior.\n"
            "\n"
            "You should explain:\n"
            "\n"
            "- what the model can do,\n"
            "- what it cannot do,\n"
            "- where it tends to fail,\n"
            "- what errors look like,\n"
            "- and what the operational consequences of those errors are.\n"
            "\n"
            "Instead of only saying:\n"
            "\n"
            "```text\n"
            "The model has 98% accuracy.\n"
            "```\n"
            "\n"
            "it may be more useful to communicate:\n"
            "\n"
            "```text\n"
            "How many valid cases are incorrectly rejected?\n"
            "How many fraudulent cases are missed?\n"
            "How many cases require manual review each day?\n"
            "```\n"
            "\n"
            "This connects technical metrics to business consequences.\n"
            "\n"
            "### Prediction thresholds are business decisions too\n"
            "\n"
            "Suppose a fraud classifier produces a probability.\n"
            "\n"
            "You still need to choose the threshold at which a transaction will "
            "be flagged.\n"
            "\n"
            "Different thresholds change the balance between:\n"
            "\n"
            "```text\n"
            "false positives\n"
            "and\n"
            "false negatives\n"
            "```\n"
            "\n"
            "This is not purely a mathematical decision. The correct tradeoff "
            "depends on the business context.\n"
            "\n"
            "### Training versus inference\n"
            "\n"
            "During development, the model performs training operations.\n"
            "\n"
            "After deployment, the production model usually performs only "
            "**inference**:\n"
            "\n"
            "```text\n"
            "new input\n"
            "   ↓\n"
            "trained model\n"
            "   ↓\n"
            "prediction\n"
            "```\n"
            "\n"
            "Because the production artifact no longer needs to train, it can "
            "often be optimized for speed and memory usage.\n"
            "\n"
            "### Option 1: serve the model through an API\n"
            "\n"
            "One common architecture is:\n"
            "\n"
            "```text\n"
            "Application\n"
            "    ↓ network request\n"
            "Model server\n"
            "    ↓\n"
            "Prediction\n"
            "    ↓ network response\n"
            "Application\n"
            "```\n"
            "\n"
            "This approach can work well when:\n"
            "\n"
            "- reliable internet connectivity is available,\n"
            "- network latency is acceptable,\n"
            "- the server is allowed to access the input,\n"
            "- and centralized compute resources are desirable.\n"
            "\n"
            "Models can be exported to deployment-oriented formats rather than "
            "being tied to the original Python training process.\n"
            "\n"
            "Examples mentioned in the source include TensorFlow SavedModel and "
            "ONNX.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```python\n"
            "model.export(\"path/to/model\", format=\"onnx\")\n"
            "```\n"
            "\n"
            "The exported artifact can then be loaded by an inference runtime.\n"
            "\n"
            "### Option 2: run the model on the device\n"
            "\n"
            "Sometimes the model should run directly on:\n"
            "\n"
            "```text\n"
            "smartphone\n"
            "camera\n"
            "robot\n"
            "embedded computer\n"
            "microcontroller\n"
            "```\n"
            "\n"
            "On-device deployment is useful when:\n"
            "\n"
            "- latency must be very low,\n"
            "- internet connectivity may be unavailable,\n"
            "- input data is sensitive,\n"
            "- or the application must work offline.\n"
            "\n"
            "However, devices have limits on:\n"
            "\n"
            "- memory,\n"
            "- compute,\n"
            "- battery power,\n"
            "- and model size.\n"
            "\n"
            "This creates a tradeoff between model quality and runtime "
            "efficiency.\n"
            "\n"
            "### Option 3: run the model in the browser\n"
            "\n"
            "Another possibility is client-side browser inference.\n"
            "\n"
            "Advantages can include:\n"
            "\n"
            "- reducing server-side compute cost,\n"
            "- keeping user data on the user's machine,\n"
            "- avoiding network round-trip latency,\n"
            "- and allowing offline use after assets are downloaded.\n"
            "\n"
            "The model still needs to be small enough to avoid excessive CPU, "
            "GPU, or memory usage.\n"
            "\n"
            "### Deployment is a systems decision\n"
            "\n"
            "A useful decision table is:\n"
            "\n"
            "| Requirement | Likely direction |\n"
            "|---|---|\n"
            "| Large centralized compute | Server/API |\n"
            "| Must work offline | Device/browser |\n"
            "| Highly sensitive input | Device/browser |\n"
            "| Very strict latency | Device/local inference |\n"
            "| Tiny hardware | Optimized on-device model |\n"
            "| Easy centralized updates | Server/API |\n"
            "\n"
            "There is no universally correct deployment choice.\n"
            "\n"
            "### Inference optimization\n"
            "\n"
            "Deployment environments often require smaller and faster models.\n"
            "\n"
            "Two techniques introduced in the chapter are pruning and "
            "quantization.\n"
            "\n"
            "#### Weight pruning\n"
            "\n"
            "Not every learned coefficient contributes equally to the final "
            "prediction.\n"
            "\n"
            "Pruning removes less important weights so the model may require "
            "less memory and computation.\n"
            "\n"
            "The tradeoff is:\n"
            "\n"
            "```text\n"
            "smaller / faster model\n"
            "        ↕\n"
            "possible reduction in predictive performance\n"
            "```\n"
            "\n"
            "#### Weight quantization\n"
            "\n"
            "Models are often trained with `float32` weights.\n"
            "\n"
            "Quantization can represent weights using lower-precision values "
            "such as `int8` for inference.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "float32 weight\n"
            "→ 32 bits\n"
            "\n"
            "int8 weight\n"
            "→ 8 bits\n"
            "```\n"
            "\n"
            "Using fewer bits can substantially reduce model size.\n"
            "\n"
            "The source describes a built-in Keras workflow such as:\n"
            "\n"
            "```python\n"
            "model.quantize(\"int8\")\n"
            "```\n"
            "\n"
            "Optimization is especially important for mobile and embedded "
            "deployment.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Monitor and Maintain the Model After Launch\n"
            "\n"
            "Deployment is not the end of the machine learning lifecycle.\n"
            "\n"
            "It is the beginning of the model's life in the real world.\n"
            "\n"
            "After launch, monitor:\n"
            "\n"
            "```text\n"
            "model predictions\n"
            "system reliability\n"
            "production data\n"
            "user behavior\n"
            "business outcomes\n"
            "```\n"
            "\n"
            "### Production metrics matter\n"
            "\n"
            "A model may have good offline accuracy but fail to improve the "
            "real product.\n"
            "\n"
            "For example, after deploying a recommendation system, you may care "
            "about whether:\n"
            "\n"
            "- users listen longer,\n"
            "- engagement increases,\n"
            "- retention changes,\n"
            "- or revenue improves.\n"
            "\n"
            "These outcomes may matter more than the original offline model "
            "metric.\n"
            "\n"
            "### A/B testing\n"
            "\n"
            "One way to estimate whether a new model actually improves the "
            "product is randomized A/B testing.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "production users\n"
            "      ↓\n"
            "random assignment\n"
            "   ↙       ↘\n"
            "old system  new model\n"
            "   ↓          ↓\n"
            "compare real outcomes\n"
            "```\n"
            "\n"
            "The control group continues using the previous process while the "
            "experimental group uses the new model.\n"
            "\n"
            "Differences in outcomes can then provide evidence about the "
            "model's real-world impact.\n"
            "\n"
            "### Manual audits\n"
            "\n"
            "When possible, periodically inspect model predictions on fresh "
            "production data.\n"
            "\n"
            "You can sample new cases, obtain trusted human annotations, and "
            "compare them with model predictions.\n"
            "\n"
            "This can reveal errors that were not present in the original test "
            "set.\n"
            "\n"
            "### Monitor production data\n"
            "\n"
            "You should also monitor whether the input distribution is changing.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "new slang appears\n"
            "new fraud strategy emerges\n"
            "new hardware changes image appearance\n"
            "product catalog changes\n"
            "new user population arrives\n"
            "```\n"
            "\n"
            "These changes may make the training distribution increasingly "
            "different from production.\n"
            "\n"
            "### Concept drift means models age\n"
            "\n"
            "A deployed model should not be assumed to remain useful forever.\n"
            "\n"
            "As production behavior changes, performance can gradually decline.\n"
            "\n"
            "Different domains drift at different speeds.\n"
            "\n"
            "Fraud detection may require extremely frequent updates because "
            "adversaries actively change their behavior.\n"
            "\n"
            "Other systems may remain useful for substantially longer.\n"
            "\n"
            "### Start collecting data for the next model immediately\n"
            "\n"
            "A strong production loop looks like:\n"
            "\n"
            "```text\n"
            "deploy model v1\n"
            "     ↓\n"
            "collect production data\n"
            "     ↓\n"
            "identify difficult examples\n"
            "     ↓\n"
            "annotate new data\n"
            "     ↓\n"
            "train model v2\n"
            "     ↓\n"
            "evaluate\n"
            "     ↓\n"
            "deploy model v2\n"
            "     ↓\n"
            "repeat\n"
            "```\n"
            "\n"
            "Samples the current model finds difficult can be particularly "
            "valuable because they expose weaknesses in the current decision "
            "boundary or representation.\n"
            "\n"
            "### The complete universal workflow\n"
            "\n"
            "The entire lifecycle can now be summarized as:\n"
            "\n"
            "```text\n"
            "1. DEFINE THE TASK\n"
            "\n"
            "Understand the business problem\n"
            "→ define inputs and targets\n"
            "→ choose task type\n"
            "→ collect and annotate data\n"
            "→ inspect the dataset\n"
            "→ choose success metric\n"
            "\n"
            "2. DEVELOP THE MODEL\n"
            "\n"
            "Prepare data\n"
            "→ choose validation protocol\n"
            "→ beat a baseline\n"
            "→ scale model until it can overfit\n"
            "→ regularize and tune\n"
            "→ select final configuration\n"
            "→ evaluate on test data\n"
            "\n"
            "3. DEPLOY AND OPERATE\n"
            "\n"
            "Set expectations\n"
            "→ export inference model\n"
            "→ choose serving environment\n"
            "→ optimize inference\n"
            "→ monitor production\n"
            "→ collect new data\n"
            "→ retrain future models\n"
            "```\n"
            "\n"
            "This is why model training is only one part of machine learning "
            "engineering.\n"
            "\n"
            "A successful machine learning system depends on the entire "
            "workflow.\n"
            "\n"

            # Exercise EX02 is rendered here by the frontend.
            "{{exercise:M06.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Misconceptions
            # ----------------------------------------------------------------

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> A machine learning project begins by choosing the neural-network "
            "architecture.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A real project begins by understanding the problem, available "
            "data, targets, constraints, and measure of success. Model selection "
            "comes later.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> If test accuracy is high, the model will automatically work well "
            "in production.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The test set may not represent production data. Distribution "
            "differences, sampling bias, or concept drift can cause production "
            "performance to be much worse.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> More model complexity can always compensate for bad data.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A model can only learn patterns present in the available data. "
            "Missing predictive information, noisy labels, or unrepresentative "
            "samples cannot automatically be fixed by adding more layers.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> The validation set and test set serve the same purpose.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Validation data guides model-development decisions. The test set "
            "should remain untouched until final evaluation so it can provide a "
            "less biased estimate of generalization.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> Overfitting should never occur during development.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The workflow deliberately encourages increasing capacity until "
            "overfitting appears. This demonstrates that the model has enough "
            "capacity. The next step is to regularize and tune back toward the "
            "best generalization point.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> Deployment is the final step, after which the project is complete.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Production data changes, concept drift occurs, and user behavior "
            "changes. Deployed models require monitoring, auditing, new data "
            "collection, and eventual retraining.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Key terminology
            # ----------------------------------------------------------------

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Problem framing | Translating a real-world need into a precise prediction task |\n"
            "| Input | Information available to the model at prediction time |\n"
            "| Target | Value or class the model is expected to predict |\n"
            "| Annotation | Human- or system-provided target associated with a sample |\n"
            "| Representative data | Data that resembles the distribution the model will face in production |\n"
            "| Sampling bias | Systematic mismatch caused by how the dataset was collected |\n"
            "| Concept drift | Change in production data or relationships over time |\n"
            "| Target leakage | Input information that improperly reveals the target and would not be available in production |\n"
            "| Success metric | Measurement used to define whether the project is achieving its goal |\n"
            "| Vectorization | Converting raw data into numerical tensors suitable for a model |\n"
            "| Normalization | Rescaling numerical values to make optimization easier |\n"
            "| Hold-out validation | Reserving a fixed portion of data for validation |\n"
            "| K-fold validation | Repeatedly training with different partitions used for validation |\n"
            "| Baseline | Simple reference performance that the model should beat |\n"
            "| Statistical power | Evidence that the model can learn useful predictive signal beyond a simple baseline |\n"
            "| Architecture prior | Choice of model family based on assumptions about the task structure |\n"
            "| Hyperparameter | Configuration chosen by the developer rather than learned directly during training |\n"
            "| Regularization | Technique used to reduce overfitting and improve generalization |\n"
            "| Inference | Using a trained model to produce predictions |\n"
            "| Pruning | Removing less important model weights to reduce compute and memory |\n"
            "| Quantization | Representing model parameters with lower numerical precision |\n"
            "| A/B testing | Comparing a new system with a control system using randomized production groups |\n"
            "| Production monitoring | Tracking model, data, system, and business behavior after deployment |\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Self-check
            # ----------------------------------------------------------------

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why should a machine learning project begin with problem framing?\n"
            "2. What two major hypotheses are made when defining a supervised learning task?\n"
            "3. Why does representative training data matter?\n"
            "4. What is concept drift?\n"
            "5. What is sampling bias?\n"
            "6. What is target leakage?\n"
            "7. Why must the project success metric reflect the real-world goal?\n"
            "8. What is vectorization?\n"
            "9. Why are numerical features often normalized?\n"
            "10. When is K-fold validation preferable to a simple hold-out set?\n"
            "11. What is the purpose of a baseline?\n"
            "12. Why might you intentionally increase model size until it overfits?\n"
            "13. Why should tuning decisions be based on validation data rather than test data?\n"
            "14. When might on-device inference be preferable to a remote API?\n"
            "15. What is the difference between pruning and quantization?\n"
            "16. Why should a deployed model continue collecting fresh data?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**Machine learning is not simply model training. A successful "
            "project begins by defining the real problem and building a "
            "representative dataset, continues through careful validation and "
            "model development, and extends after deployment through monitoring, "
            "data collection, and continual model improvement.**\n"
            "\n"
            "Remember the complete workflow:\n"
            "\n"
            "```text\n"
            "DEFINE\n"
            "problem\n"
            "→ data\n"
            "→ metric\n"
            "\n"
            "DEVELOP\n"
            "preprocess\n"
            "→ validate\n"
            "→ baseline\n"
            "→ overfit\n"
            "→ regularize\n"
            "→ test\n"
            "\n"
            "DEPLOY\n"
            "ship\n"
            "→ monitor\n"
            "→ collect new data\n"
            "→ retrain\n"
            "```\n"
        ),

        "estimated_minutes": 135,

        "has_code_examples": True,

        "sections": [
            {
                "id": "define-task",
                "title": "Define the Task Before Building the Model",
                "order": 1,
            },
            {
                "id": "develop-model",
                "title": "Develop a Model That Actually Generalizes",
                "order": 2,
            },
            {
                "id": "deploy-model",
                "title": "Deploy the Model as Part of a Real System",
                "order": 3,
            },
            {
                "id": "monitor-maintain",
                "title": "Monitor and Maintain the Model After Launch",
                "order": 4,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M06.L01.EX01",

            "title": "Design an End-to-End ML Development Plan",

            "lesson_code": "M06.L01",

            "section_id": "develop-model",

            "placement": "after_section",

            "description": (
                "Practice moving from problem framing through preprocessing, "
                "validation, baselines, model capacity, and final evaluation."
            ),

            "instructions": (
                "Imagine you are asked to build a system that detects fraudulent "
                "online transactions.\n\n"
                "Create a development plan that answers the following:\n"
                "1. What could the model inputs be?\n"
                "2. What is the target?\n"
                "3. What machine learning task type is this?\n"
                "4. What data would you need to collect?\n"
                "5. Give one example of possible sampling bias.\n"
                "6. Give one example of possible target leakage.\n"
                "7. Choose at least two useful success metrics and explain why.\n"
                "8. Describe how you would create the training, validation, and "
                "test sets.\n"
                "9. Define a simple baseline the model should beat.\n"
                "10. Explain how you would know that your model can overfit.\n"
                "11. Name two regularization or tuning experiments you might try.\n"
                "12. Explain when you would finally use the test set."
            ),

            "expected_output": (
                "A structured project plan covering framing, dataset design, "
                "evaluation, baseline construction, model development, "
                "overfitting detection, tuning, and final testing."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "problem-framing",
                "data-quality",
                "validation",
                "baseline",
                "generalization",
                "model-development",
            ],
        },

        {
            "id": "M06.L01.EX02",

            "title": "Choose a Deployment and Monitoring Strategy",

            "lesson_code": "M06.L01",

            "section_id": "monitor-maintain",

            "placement": "after_section",

            "description": (
                "Practice selecting a deployment architecture and designing a "
                "production monitoring and maintenance plan."
            ),

            "instructions": (
                "Consider these three systems:\n\n"
                "A. A spam detector for end-to-end encrypted private messages.\n"
                "B. A recommendation model for a cloud-based streaming service.\n"
                "C. A computer-vision model that removes defective items from a "
                "factory conveyor belt in real time.\n\n"
                "For each system:\n"
                "1. Choose server/API, browser, or on-device deployment.\n"
                "2. Explain the main latency, connectivity, privacy, and hardware "
                "considerations behind your choice.\n"
                "3. State whether pruning or quantization could be useful and why.\n"
                "4. Name at least two production metrics you would monitor.\n"
                "5. Describe how you would collect new production examples for "
                "future retraining.\n"
                "6. Give one example of concept drift that could affect the "
                "system.\n"
                "7. Explain how an A/B test could be used for one of the systems."
            ),

            "expected_output": (
                "A comparison table or structured written analysis describing "
                "deployment location, operational constraints, optimization, "
                "monitoring, concept drift, and future retraining."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "deployment",
                "inference",
                "optimization",
                "monitoring",
                "concept-drift",
                "ab-testing",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M06.L01.QZ01",

        "title": "The Universal Workflow of Machine Learning — Knowledge Check",

        "lesson_code": "M06.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M06.L01.Q01",

                "section_id": "define-task",

                "question": (
                    "Which activity should normally happen before choosing a "
                    "neural-network architecture?"
                ),

                "options": [
                    "Increase the model depth until it overfits",
                    "Understand the problem, available data, targets, constraints, and success criteria",
                    "Quantize the model to int8",
                    "Deploy a REST API",
                ],

                "correct": 1,

                "explanation": (
                    "Real machine learning projects begin by defining the "
                    "problem and understanding the data and constraints. Model "
                    "architecture is chosen only after the task has been framed."
                ),
            },

            {
                "id": "M06.L01.Q02",

                "section_id": "define-task",

                "question": (
                    "A training feature contains information that would only "
                    "become known after the prediction is supposed to happen. "
                    "What problem does this describe?"
                ),

                "options": [
                    "Concept drift",
                    "Regularization",
                    "Target leakage",
                    "Quantization",
                ],

                "correct": 2,

                "explanation": (
                    "Target leakage occurs when the model receives information "
                    "during training that reveals the target but would not be "
                    "available in the real prediction environment."
                ),
            },

            {
                "id": "M06.L01.Q03",

                "section_id": "develop-model",

                "question": (
                    "Why might a developer intentionally increase model "
                    "capacity until validation performance begins to degrade?"
                ),

                "options": [
                    "To prove that the model has enough capacity and locate the boundary between underfitting and overfitting",
                    "Because the most overfit model should always be deployed",
                    "To eliminate the need for validation data",
                    "Because larger models cannot use regularization",
                ],

                "correct": 0,

                "explanation": (
                    "A model that can overfit has demonstrated sufficient "
                    "capacity. The developer can then regularize and tune the "
                    "model back toward the configuration with the best "
                    "generalization."
                ),
            },

            {
                "id": "M06.L01.Q04",

                "section_id": "deploy-model",

                "question": (
                    "Which situation most strongly favors running inference "
                    "directly on the user's device?"
                ),

                "options": [
                    "The application has unlimited network connectivity and no privacy constraints",
                    "The model is only used once during development",
                    "The application requires private inputs to remain local and must work with poor connectivity",
                    "The server has a larger GPU than the device",
                ],

                "correct": 2,

                "explanation": (
                    "On-device inference is especially useful when privacy, "
                    "offline operation, or strict latency make remote inference "
                    "undesirable or impossible."
                ),
            },

            {
                "id": "M06.L01.Q05",

                "section_id": "monitor-maintain",

                "type": "open",

                "question": (
                    "A model performed well during testing but its production "
                    "performance has gradually declined over six months. Explain "
                    "at least three possible causes described in this lesson, "
                    "what evidence you would collect, and how you would update "
                    "the machine learning system."
                ),
            },
        ],

        "passing_score": 70,
    },
}