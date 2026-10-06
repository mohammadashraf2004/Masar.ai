"""M04.L01 — Classification and Regression with Neural Networks.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 4, page range not provided in supplied source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M04.L01"

MODULE_ORDER = 4

MODULE_TITLE = "Classification and Regression"

MODULE_DESCRIPTION = (
    "Learn how to build complete neural-network workflows for binary "
    "classification, multiclass classification, and scalar regression, "
    "including preprocessing, model design, validation, evaluation, "
    "prediction, and overfitting detection."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Chapter 4 — page range not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Classification and Regression with Neural Networks",

    "slug": "deep-learning-foundations-m04-l01",

    "description": (
        "Build an intuitive and practical understanding of the three common "
        "neural-network tasks on vector data: binary classification, "
        "multiclass classification, and scalar regression."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.0,

    "skill_tags": [
        "deep-learning",
        "classification",
        "binary-classification",
        "multiclass-classification",
        "regression",
        "data-preprocessing",
        "validation",
        "overfitting",
        "cross-validation",
        "module-04",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Classification and Regression with Neural Networks",

        "content": (
            "# Classification and Regression with Neural Networks\n"
            "\n"
            "> **Course:** Deep Learning Foundations  \n"
            "> **Lesson:** M04.L01  \n"
            "> **Module:** Classification and Regression  \n"
            "> **Source alignment:** BOOK-002, Chapter 4. "
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
            "- Distinguish classification from regression.\n"
            "- Distinguish binary, multiclass, and multilabel classification.\n"
            "- Explain the roles of samples, predictions, targets, labels, "
            "classes, and loss values.\n"
            "- Prepare text data for a Dense neural network using vector "
            "representations.\n"
            "- Design a basic binary classification network.\n"
            "- Explain why sigmoid is appropriate for a two-class output.\n"
            "- Design a basic single-label multiclass classification network.\n"
            "- Explain why softmax is appropriate for mutually exclusive classes.\n"
            "- Choose between categorical and sparse categorical crossentropy.\n"
            "- Recognize an information bottleneck in intermediate layers.\n"
            "- Build a basic scalar regression network.\n"
            "- Explain why regression uses different losses and metrics from "
            "classification.\n"
            "- Normalize numerical features correctly without leaking test data.\n"
            "- Explain the purpose of validation data and K-fold validation.\n"
            "- Recognize overfitting from training and validation behavior.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. Classification and Regression: Know the Problem First\n"
            "\n"
            "Before choosing a neural-network architecture, you need to know "
            "what kind of prediction problem you are solving.\n"
            "\n"
            "The three main problem types in this lesson are:\n"
            "\n"
            "```text\n"
            "Binary classification\n"
            "→ choose between two classes\n"
            "\n"
            "Multiclass classification\n"
            "→ choose one class from many classes\n"
            "\n"
            "Scalar regression\n"
            "→ predict one continuous numerical value\n"
            "```\n"
            "\n"
            "The problem type affects several decisions:\n"
            "\n"
            "- the final layer of the network,\n"
            "- the activation used in that layer,\n"
            "- the loss function,\n"
            "- the evaluation metric,\n"
            "- and sometimes how the labels are encoded.\n"
            "\n"
            "### Core terminology\n"
            "\n"
            "Suppose a model receives information about a house and tries to "
            "predict its price.\n"
            "\n"
            "The house information is the **sample** or **input**.\n"
            "\n"
            "The model's guessed price is the **prediction** or **output**.\n"
            "\n"
            "The actual known price is the **target**.\n"
            "\n"
            "The difference between the model prediction and the target is "
            "summarized by a **loss**.\n"
            "\n"
            "For classification problems, we also use the ideas of classes "
            "and labels.\n"
            "\n"
            "For example, in a cat-versus-dog classifier:\n"
            "\n"
            "```text\n"
            "classes = {cat, dog}\n"
            "\n"
            "sample = one image\n"
            "label  = cat\n"
            "```\n"
            "\n"
            "### Binary classification\n"
            "\n"
            "Binary classification means each sample belongs to one of two "
            "mutually exclusive classes.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "```text\n"
            "positive review / negative review\n"
            "spam / not spam\n"
            "fraud / not fraud\n"
            "```\n"
            "\n"
            "### Multiclass classification\n"
            "\n"
            "Multiclass classification means there are more than two possible "
            "classes.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "news article\n"
            "    ↓\n"
            "business\n"
            "sports\n"
            "politics\n"
            "technology\n"
            "...\n"
            "```\n"
            "\n"
            "If every sample belongs to exactly one class, the task is "
            "**single-label multiclass classification**.\n"
            "\n"
            "### Multilabel classification\n"
            "\n"
            "A multilabel problem is different.\n"
            "\n"
            "One sample may belong to several classes simultaneously.\n"
            "\n"
            "For example, an image might contain:\n"
            "\n"
            "```text\n"
            "cat\n"
            "+\n"
            "dog\n"
            "+\n"
            "person\n"
            "```\n"
            "\n"
            "All three labels could be valid for the same image.\n"
            "\n"
            "### Regression\n"
            "\n"
            "Regression predicts continuous numerical values instead of "
            "discrete categories.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "```text\n"
            "house price\n"
            "temperature\n"
            "delivery time\n"
            "energy consumption\n"
            "```\n"
            "\n"
            "If the target is one number, the task is **scalar regression**.\n"
            "\n"
            "If the target contains several continuous values, it is "
            "**vector regression**.\n"
            "\n"
            "### The main pattern\n"
            "\n"
            "Keep this distinction in mind:\n"
            "\n"
            "```text\n"
            "Classification\n"
            "→ Which category?\n"
            "\n"
            "Regression\n"
            "→ What numerical value?\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Binary Classification: Positive or Negative Reviews\n"
            "\n"
            "The first end-to-end workflow is a sentiment classifier.\n"
            "\n"
            "The goal is simple:\n"
            "\n"
            "```text\n"
            "Movie review\n"
            "     ↓\n"
            "Neural network\n"
            "     ↓\n"
            "Positive or negative\n"
            "```\n"
            "\n"
            "### The dataset\n"
            "\n"
            "The example uses movie reviews from IMDb.\n"
            "\n"
            "The dataset contains 50,000 strongly polarized reviews:\n"
            "\n"
            "```text\n"
            "25,000 training reviews\n"
            "25,000 test reviews\n"
            "```\n"
            "\n"
            "Each group contains an equal split of positive and negative "
            "reviews.\n"
            "\n"
            "The text has already been converted into sequences of integer "
            "word indices.\n"
            "\n"
            "Conceptually, a review may look like:\n"
            "\n"
            "```text\n"
            "[1, 14, 22, 16, ..., 178, 32]\n"
            "```\n"
            "\n"
            "Each integer refers to a word in a vocabulary.\n"
            "\n"
            "The labels are:\n"
            "\n"
            "```text\n"
            "0 → negative\n"
            "1 → positive\n"
            "```\n"
            "\n"
            "### Limiting the vocabulary\n"
            "\n"
            "The example keeps only the 10,000 most frequent words.\n"
            "\n"
            "This reduces the size of the representation and removes very "
            "rare words that are unlikely to provide much useful signal in "
            "this introductory setup.\n"
            "\n"
            "### Why preprocessing is necessary\n"
            "\n"
            "The reviews are variable-length sequences.\n"
            "\n"
            "A Dense network expects batches represented by regular tensors, "
            "so the reviews must first be converted into a fixed-size "
            "numerical representation.\n"
            "\n"
            "One approach is **multi-hot encoding**.\n"
            "\n"
            "Suppose our vocabulary contains ten words and a review contains "
            "words with indices 5 and 8.\n"
            "\n"
            "The review can be represented as:\n"
            "\n"
            "```text\n"
            "index:  0 1 2 3 4 5 6 7 8 9\n"
            "value:  0 0 0 0 0 1 0 0 1 0\n"
            "```\n"
            "\n"
            "A value of 1 means that the corresponding vocabulary word "
            "appears in the review.\n"
            "\n"
            "For a 10,000-word vocabulary, each review becomes a vector of "
            "length 10,000.\n"
            "\n"
            "A simple implementation is:\n"
            "\n"
            "```python\n"
            "import numpy as np\n"
            "\n"
            "def multi_hot_encode(sequences, num_classes):\n"
            "    results = np.zeros((len(sequences), num_classes))\n"
            "    for i, sequence in enumerate(sequences):\n"
            "        results[i][sequence] = 1.0\n"
            "    return results\n"
            "```\n"
            "\n"
            "After preprocessing:\n"
            "\n"
            "```text\n"
            "input review → vector of 10,000 values\n"
            "target       → 0 or 1\n"
            "```\n"
            "\n"
            "### Building the binary classifier\n"
            "\n"
            "The example uses:\n"
            "\n"
            "```python\n"
            "model = keras.Sequential([\n"
            "    layers.Dense(16, activation=\"relu\"),\n"
            "    layers.Dense(16, activation=\"relu\"),\n"
            "    layers.Dense(1, activation=\"sigmoid\"),\n"
            "])\n"
            "```\n"
            "\n"
            "The two intermediate layers learn useful internal "
            "representations of the review.\n"
            "\n"
            "The final layer contains exactly one unit because the desired "
            "output is one probability-like score.\n"
            "\n"
            "### Why sigmoid?\n"
            "\n"
            "The sigmoid activation maps its input into the interval from "
            "0 to 1.\n"
            "\n"
            "So the final output can be interpreted as something like:\n"
            "\n"
            "```text\n"
            "0.02 → very likely negative\n"
            "0.48 → uncertain\n"
            "0.93 → very likely positive\n"
            "```\n"
            "\n"
            "This makes a single sigmoid unit a natural output for a binary "
            "classification problem.\n"
            "\n"
            "### Why ReLU in the intermediate layers?\n"
            "\n"
            "Without nonlinear activation functions, a stack of Dense layers "
            "would remain limited to linear or affine transformations.\n"
            "\n"
            "Using ReLU introduces nonlinearity and allows the network to "
            "learn richer representations.\n"
            "\n"
            "### Choosing the loss\n"
            "\n"
            "For this binary classifier, the example uses:\n"
            "\n"
            "```python\n"
            "model.compile(\n"
            "    optimizer=\"adam\",\n"
            "    loss=\"binary_crossentropy\",\n"
            "    metrics=[\"accuracy\"],\n"
            ")\n"
            "```\n"
            "\n"
            "`binary_crossentropy` is a suitable loss when the model produces "
            "a probability for a two-class classification task.\n"
            "\n"
            "### Training, validation, and testing are different\n"
            "\n"
            "A very important workflow distinction is:\n"
            "\n"
            "```text\n"
            "Training set\n"
            "→ learn model parameters\n"
            "\n"
            "Validation set\n"
            "→ make development choices\n"
            "\n"
            "Test set\n"
            "→ perform final evaluation\n"
            "```\n"
            "\n"
            "For example, the validation set can help you decide:\n"
            "\n"
            "- how many epochs to train,\n"
            "- how large the model should be,\n"
            "- or which configuration works better.\n"
            "\n"
            "You should not repeatedly use the test set for these decisions, "
            "because then it stops functioning as an unbiased final check.\n"
            "\n"
            "### Detecting overfitting\n"
            "\n"
            "During training, you may observe:\n"
            "\n"
            "```text\n"
            "training loss      ↓\n"
            "training accuracy  ↑\n"
            "\n"
            "validation loss    improves, then gets worse\n"
            "validation accuracy improves, then stops improving\n"
            "```\n"
            "\n"
            "This means that the model continues becoming better at the "
            "training data while becoming less useful on unseen data.\n"
            "\n"
            "That is **overfitting**.\n"
            "\n"
            "In the chapter example, validation performance peaks after only "
            "a few epochs, so the model is retrained for a shorter duration "
            "instead of blindly continuing to optimize the training set.\n"
            "\n"
            "### Making predictions\n"
            "\n"
            "A trained binary classifier returns one score per review.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "review A → 0.99\n"
            "review B → 0.01\n"
            "review C → 0.61\n"
            "```\n"
            "\n"
            "The first two predictions are highly confident. The third is "
            "less confident.\n"
            "\n"

            # Exercise EX01 is rendered here by the frontend.
            "{{exercise:M04.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Multiclass Classification: Predicting a News Topic\n"
            "\n"
            "Binary classification has two possible classes.\n"
            "\n"
            "Now suppose we have many mutually exclusive classes.\n"
            "\n"
            "The chapter's example classifies Reuters newswires into 46 "
            "different topics.\n"
            "\n"
            "Each newswire belongs to one topic, so this is:\n"
            "\n"
            "```text\n"
            "single-label\n"
            "+\n"
            "multiclass\n"
            "+\n"
            "classification\n"
            "```\n"
            "\n"
            "### Preparing the input\n"
            "\n"
            "The newswire text is represented in the same general way as the "
            "movie-review example.\n"
            "\n"
            "The vocabulary is restricted to the 10,000 most frequent words, "
            "and input sequences are converted into fixed-size vectors.\n"
            "\n"
            "### Preparing multiclass labels\n"
            "\n"
            "Each label is originally an integer between 0 and 45.\n"
            "\n"
            "There are two common ways to handle these labels.\n"
            "\n"
            "#### Option 1: one-hot encoding\n"
            "\n"
            "Suppose the correct class is class 3 out of five possible "
            "classes.\n"
            "\n"
            "A one-hot representation would be:\n"
            "\n"
            "```text\n"
            "[0, 0, 0, 1, 0]\n"
            "```\n"
            "\n"
            "Only the correct class receives a 1.\n"
            "\n"
            "For 46 classes, every target becomes a vector of length 46.\n"
            "\n"
            "With one-hot labels, use:\n"
            "\n"
            "```text\n"
            "categorical_crossentropy\n"
            "```\n"
            "\n"
            "#### Option 2: integer labels\n"
            "\n"
            "You can also keep the labels as integers:\n"
            "\n"
            "```text\n"
            "0\n"
            "1\n"
            "2\n"
            "...\n"
            "45\n"
            "```\n"
            "\n"
            "Then use:\n"
            "\n"
            "```text\n"
            "sparse_categorical_crossentropy\n"
            "```\n"
            "\n"
            "The underlying classification objective is the same; the main "
            "difference is the expected label representation.\n"
            "\n"
            "### Designing the output layer\n"
            "\n"
            "For N mutually exclusive classes, the final layer should contain "
            "N units.\n"
            "\n"
            "For 46 topics:\n"
            "\n"
            "```python\n"
            "layers.Dense(46, activation=\"softmax\")\n"
            "```\n"
            "\n"
            "The model therefore produces a vector such as:\n"
            "\n"
            "```text\n"
            "[0.01, 0.00, 0.04, ..., 0.62, ..., 0.02]\n"
            "```\n"
            "\n"
            "There are 46 values, one for every class.\n"
            "\n"
            "Softmax makes them form a probability distribution:\n"
            "\n"
            "```text\n"
            "all probabilities sum to 1\n"
            "```\n"
            "\n"
            "The class with the largest probability becomes the predicted "
            "class.\n"
            "\n"
            "In NumPy:\n"
            "\n"
            "```python\n"
            "predicted_class = np.argmax(predictions[0])\n"
            "```\n"
            "\n"
            "### A suitable architecture\n"
            "\n"
            "The chapter uses larger intermediate layers than in the binary "
            "example:\n"
            "\n"
            "```python\n"
            "model = keras.Sequential([\n"
            "    layers.Dense(64, activation=\"relu\"),\n"
            "    layers.Dense(64, activation=\"relu\"),\n"
            "    layers.Dense(46, activation=\"softmax\"),\n"
            "])\n"
            "```\n"
            "\n"
            "Why use 64 units instead of very small hidden layers?\n"
            "\n"
            "Because the model must preserve enough information to distinguish "
            "between 46 possible outputs.\n"
            "\n"
            "### Information bottlenecks\n"
            "\n"
            "Imagine this architecture:\n"
            "\n"
            "```text\n"
            "64 units\n"
            "   ↓\n"
            "4 units\n"
            "   ↓\n"
            "46 classes\n"
            "```\n"
            "\n"
            "The four-unit layer forces all useful information through a very "
            "small representation.\n"
            "\n"
            "If relevant information is discarded there, later layers cannot "
            "recover it.\n"
            "\n"
            "This is an **information bottleneck**.\n"
            "\n"
            "The source demonstrates that such a narrow layer substantially "
            "reduces validation accuracy in this example.\n"
            "\n"
            "### Accuracy and top-k accuracy\n"
            "\n"
            "Ordinary accuracy asks:\n"
            "\n"
            "> Was the highest-probability class exactly correct?\n"
            "\n"
            "For many-class problems, another useful metric is **top-k "
            "accuracy**.\n"
            "\n"
            "Top-3 accuracy asks:\n"
            "\n"
            "> Was the true class somewhere among the model's three highest "
            "probability predictions?\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Model top predictions:\n"
            "1. class 12\n"
            "2. class 7\n"
            "3. class 4\n"
            "\n"
            "true class = 7\n"
            "```\n"
            "\n"
            "Normal accuracy marks this prediction as wrong because class 7 "
            "was not first.\n"
            "\n"
            "Top-3 accuracy marks it as successful because class 7 appears "
            "among the top three predictions.\n"
            "\n"
            "### Validation still matters\n"
            "\n"
            "As with binary classification, training for more epochs does not "
            "guarantee better generalization.\n"
            "\n"
            "Training and validation curves should be monitored so that you "
            "can identify when the model begins to overfit.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Scalar Regression: Predicting House Prices\n"
            "\n"
            "Classification predicts categories.\n"
            "\n"
            "Regression predicts continuous numerical values.\n"
            "\n"
            "The chapter's regression example predicts the median house price "
            "of a California district using numerical information about that "
            "district.\n"
            "\n"
            "### Input features\n"
            "\n"
            "Each sample contains eight numerical variables describing a "
            "district, including location and housing or population-related "
            "measurements.\n"
            "\n"
            "The small dataset used in the chapter contains:\n"
            "\n"
            "```text\n"
            "480 training samples\n"
            "120 test samples\n"
            "8 features per sample\n"
            "```\n"
            "\n"
            "So the training input has shape:\n"
            "\n"
            "```text\n"
            "(480, 8)\n"
            "```\n"
            "\n"
            "The target is one continuous house-price value per sample.\n"
            "\n"
            "### Why normalization matters\n"
            "\n"
            "Different numerical features can use very different scales.\n"
            "\n"
            "For example, one feature might contain values near 2 while "
            "another contains values in the thousands.\n"
            "\n"
            "Training can become more difficult when raw features have very "
            "different ranges.\n"
            "\n"
            "A common solution is feature-wise normalization:\n"
            "\n"
            "```text\n"
            "normalized_value =\n"
            "    (value - training_mean) / training_standard_deviation\n"
            "```\n"
            "\n"
            "In NumPy:\n"
            "\n"
            "```python\n"
            "mean = train_data.mean(axis=0)\n"
            "std = train_data.std(axis=0)\n"
            "\n"
            "x_train = (train_data - mean) / std\n"
            "x_test = (test_data - mean) / std\n"
            "```\n"
            "\n"
            "Notice something extremely important:\n"
            "\n"
            "```text\n"
            "mean and std are calculated from TRAINING DATA only\n"
            "```\n"
            "\n"
            "The same training statistics are then used to transform the test "
            "data.\n"
            "\n"
            "You should not calculate preprocessing statistics from the test "
            "set because that would allow information from the evaluation data "
            "to influence your workflow.\n"
            "\n"
            "This is a form of **data leakage**.\n"
            "\n"
            "### Scaling the targets\n"
            "\n"
            "In the source example, house prices are also divided by 100,000 "
            "to bring target values into a smaller numerical range.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "$283,000\n"
            "    ↓ divide by 100,000\n"
            "2.83\n"
            "```\n"
            "\n"
            "After prediction, the value can be converted back into dollars "
            "by multiplying by 100,000.\n"
            "\n"
            "### Building the regression network\n"
            "\n"
            "The source uses a relatively small model because the dataset "
            "contains few training samples:\n"
            "\n"
            "```python\n"
            "model = keras.Sequential([\n"
            "    layers.Dense(64, activation=\"relu\"),\n"
            "    layers.Dense(64, activation=\"relu\"),\n"
            "    layers.Dense(1),\n"
            "])\n"
            "```\n"
            "\n"
            "The final layer contains one unit because we want one numerical "
            "prediction.\n"
            "\n"
            "Notice that there is no activation function on the final layer.\n"
            "\n"
            "This allows the model to predict values across an unrestricted "
            "numerical range.\n"
            "\n"
            "If we used sigmoid instead, the output would be restricted to "
            "the interval between 0 and 1, which would be inappropriate for "
            "an unrestricted house-price target.\n"
            "\n"
            "### Regression loss: mean squared error\n"
            "\n"
            "The model is compiled using:\n"
            "\n"
            "```python\n"
            "model.compile(\n"
            "    optimizer=\"adam\",\n"
            "    loss=\"mean_squared_error\",\n"
            "    metrics=[\"mean_absolute_error\"],\n"
            ")\n"
            "```\n"
            "\n"
            "**Mean squared error**, or MSE, is commonly used as a regression "
            "loss.\n"
            "\n"
            "Conceptually, it measures squared prediction errors.\n"
            "\n"
            "If:\n"
            "\n"
            "```text\n"
            "target     = 3.0\n"
            "prediction = 2.5\n"
            "```\n"
            "\n"
            "then the error is:\n"
            "\n"
            "```text\n"
            "3.0 - 2.5 = 0.5\n"
            "```\n"
            "\n"
            "and the squared error is:\n"
            "\n"
            "```text\n"
            "0.5² = 0.25\n"
            "```\n"
            "\n"
            "MSE averages these squared errors across samples.\n"
            "\n"
            "### Regression metric: mean absolute error\n"
            "\n"
            "The example also monitors **mean absolute error**, or MAE.\n"
            "\n"
            "MAE answers a very intuitive question:\n"
            "\n"
            "> On average, how far are the predictions from the correct values?\n"
            "\n"
            "If targets were divided by 100,000 and the model has:\n"
            "\n"
            "```text\n"
            "MAE = 0.30\n"
            "```\n"
            "\n"
            "then the average error in the original scale is approximately:\n"
            "\n"
            "```text\n"
            "0.30 × 100,000\n"
            "= $30,000\n"
            "```\n"
            "\n"
            "Accuracy is not appropriate here because regression is not about "
            "choosing an exact discrete class.\n"
            "\n"
            "### Why use a smaller model with little data?\n"
            "\n"
            "The less training data you have, the easier it is for a model to "
            "memorize patterns that do not generalize.\n"
            "\n"
            "A smaller network can reduce this risk.\n"
            "\n"
            "This gives us a useful rule of thumb from the chapter:\n"
            "\n"
            "```text\n"
            "less data\n"
            "→ be cautious with model capacity\n"
            "→ prefer a relatively small model\n"
            "```\n"
            "\n"
            "### Why one validation split may be unreliable\n"
            "\n"
            "Suppose you only have a few hundred samples.\n"
            "\n"
            "If you reserve 100 samples for validation, your measured "
            "performance may depend strongly on exactly which 100 samples "
            "happened to be selected.\n"
            "\n"
            "A different validation split might produce a noticeably "
            "different result.\n"
            "\n"
            "This is where **K-fold cross-validation** becomes useful.\n"
            "\n"
            "### K-fold cross-validation\n"
            "\n"
            "Suppose:\n"
            "\n"
            "```text\n"
            "K = 4\n"
            "```\n"
            "\n"
            "Split the training data into four parts:\n"
            "\n"
            "```text\n"
            "Fold A\n"
            "Fold B\n"
            "Fold C\n"
            "Fold D\n"
            "```\n"
            "\n"
            "Then perform four training runs.\n"
            "\n"
            "```text\n"
            "Run 1:\n"
            "validate on A\n"
            "train on B + C + D\n"
            "\n"
            "Run 2:\n"
            "validate on B\n"
            "train on A + C + D\n"
            "\n"
            "Run 3:\n"
            "validate on C\n"
            "train on A + B + D\n"
            "\n"
            "Run 4:\n"
            "validate on D\n"
            "train on A + B + C\n"
            "```\n"
            "\n"
            "You then average the validation results.\n"
            "\n"
            "This usually produces a more reliable estimate than depending on "
            "one small validation split.\n"
            "\n"
            "### Choosing the number of epochs\n"
            "\n"
            "The same overfitting principle still applies to regression.\n"
            "\n"
            "Training may initially improve validation MAE, but after enough "
            "epochs the validation score can stop improving or worsen.\n"
            "\n"
            "The chapter uses validation history to identify an appropriate "
            "training duration and then trains a fresh final model using the "
            "selected configuration.\n"
            "\n"
            "### Making a regression prediction\n"
            "\n"
            "A prediction may look like:\n"
            "\n"
            "```text\n"
            "model output = 2.83\n"
            "```\n"
            "\n"
            "Because the target was divided by 100,000:\n"
            "\n"
            "```text\n"
            "2.83 × 100,000\n"
            "≈ $283,000\n"
            "```\n"
            "\n"

            # Exercise EX02 is rendered here by the frontend.
            "{{exercise:M04.L01.EX02}}\n"
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
            "> Classification and regression are basically the same because "
            "both produce numbers.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The meaning of the output is different.\n"
            "\n"
            "Classification predicts membership in discrete categories, while "
            "regression predicts continuous numerical values.\n"
            "\n"
            "That difference affects the final activation, loss function, and "
            "evaluation metric.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> The test set can be checked after every experiment to decide "
            "which model to keep.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Repeatedly using test results to guide model design means the test "
            "set begins influencing your decisions.\n"
            "\n"
            "Use training data for learning, validation data for development "
            "choices, and preserve the test set for final evaluation.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> If training accuracy keeps improving, the model is definitely "
            "getting better.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Training performance can continue improving even after "
            "validation performance begins getting worse.\n"
            "\n"
            "That is a classic sign of overfitting.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> A multiclass classifier can always use a tiny intermediate "
            "layer because the final layer can reconstruct missing "
            "information.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "If an intermediate layer discards important information, later "
            "layers cannot recover information that is no longer present.\n"
            "\n"
            "An excessively narrow hidden representation may create an "
            "information bottleneck.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> Test data should be normalized using its own mean and standard "
            "deviation.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Preprocessing statistics should be learned from the training "
            "data and then applied unchanged to validation or test data.\n"
            "\n"
            "Using information calculated from the test set introduces data "
            "leakage into the evaluation workflow.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> Accuracy is a natural evaluation metric for house-price "
            "regression.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Regression outputs are continuous. Metrics such as MAE describe "
            "how far numerical predictions are from their targets and are "
            "therefore more meaningful for this kind of task.\n"
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
            "| Sample | One input example given to the model |\n"
            "| Prediction | The model's output for a sample |\n"
            "| Target | The correct value the model should ideally predict |\n"
            "| Loss | Numerical measure of disagreement between prediction and target |\n"
            "| Class | One possible category in a classification task |\n"
            "| Label | The class assigned to one specific sample |\n"
            "| Binary classification | Choosing between two mutually exclusive classes |\n"
            "| Multiclass classification | Choosing one class from more than two possibilities |\n"
            "| Multilabel classification | Assigning several labels to one sample |\n"
            "| Scalar regression | Predicting one continuous numerical value |\n"
            "| Vector regression | Predicting several continuous numerical values |\n"
            "| Multi-hot encoding | Vector indicating which vocabulary items are present |\n"
            "| One-hot encoding | Vector with one 1 marking the correct categorical class |\n"
            "| Sigmoid | Activation mapping a scalar into the 0-to-1 interval |\n"
            "| Softmax | Activation producing a probability distribution across classes |\n"
            "| Binary crossentropy | Common loss for binary probability classification |\n"
            "| Categorical crossentropy | Common loss for one-hot multiclass classification |\n"
            "| Sparse categorical crossentropy | Multiclass crossentropy used with integer labels |\n"
            "| Mean squared error | Common regression loss based on squared errors |\n"
            "| Mean absolute error | Regression metric measuring average absolute prediction error |\n"
            "| Validation set | Held-out data used to guide model-development decisions |\n"
            "| Test set | Data reserved for final evaluation |\n"
            "| Overfitting | Improving on training data while generalization becomes worse |\n"
            "| Information bottleneck | Intermediate representation too small to preserve useful information |\n"
            "| Feature normalization | Rescaling each feature using statistics such as training mean and standard deviation |\n"
            "| Data leakage | Allowing information from evaluation data to influence training or preprocessing choices |\n"
            "| K-fold validation | Repeated validation where each of K partitions becomes validation data once |\n"
            "| Top-k accuracy | Whether the correct class is among the model's k highest-scoring predictions |\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Self-check
            # ----------------------------------------------------------------

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer these questions:\n"
            "\n"
            "1. What is the fundamental difference between classification and regression?\n"
            "2. How is binary classification different from multiclass classification?\n"
            "3. How is multiclass classification different from multilabel classification?\n"
            "4. Why does a binary classifier commonly end with one sigmoid unit?\n"
            "5. Why does a 46-class classifier end with 46 softmax units?\n"
            "6. What is the difference between categorical and sparse categorical crossentropy?\n"
            "7. What is an information bottleneck?\n"
            "8. What role does a validation set play?\n"
            "9. Why should the test set not be used for repeated model-selection decisions?\n"
            "10. What does it mean when training loss improves but validation loss becomes worse?\n"
            "11. Why are numerical features often normalized before regression training?\n"
            "12. Why must normalization statistics come from the training set?\n"
            "13. Why does scalar regression commonly use one output unit without sigmoid?\n"
            "14. What does MAE tell you?\n"
            "15. Why is K-fold validation useful when the dataset is small?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**The type of machine-learning problem determines how you prepare "
            "targets, design the output layer, choose the loss function, and "
            "evaluate the model. Binary classification commonly uses one "
            "sigmoid output with binary crossentropy; single-label multiclass "
            "classification uses one softmax output per class with categorical "
            "crossentropy; scalar regression commonly uses one unrestricted "
            "output with a regression loss such as mean squared error. In all "
            "cases, validation performance matters more than simply making "
            "training performance better.**\n"
            "\n"
            "Keep this map in mind:\n"
            "\n"
            "```text\n"
            "BINARY CLASSIFICATION\n"
            "2 classes\n"
            "→ 1 sigmoid output\n"
            "→ binary crossentropy\n"
            "\n"
            "MULTICLASS CLASSIFICATION\n"
            "N mutually exclusive classes\n"
            "→ N softmax outputs\n"
            "→ categorical crossentropy\n"
            "  or sparse categorical crossentropy\n"
            "\n"
            "SCALAR REGRESSION\n"
            "1 continuous target\n"
            "→ 1 unrestricted output\n"
            "→ mean squared error\n"
            "→ evaluate with a metric such as MAE\n"
            "```\n"
        ),

        "estimated_minutes": 120,

        "has_code_examples": True,

        "sections": [
            {
                "id": "problem-types",
                "title": "Classification and Regression: Know the Problem First",
                "order": 1,
            },
            {
                "id": "binary-classification",
                "title": "Binary Classification: Positive or Negative Reviews",
                "order": 2,
            },
            {
                "id": "multiclass-classification",
                "title": "Multiclass Classification: Predicting a News Topic",
                "order": 3,
            },
            {
                "id": "regression",
                "title": "Scalar Regression: Predicting House Prices",
                "order": 4,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M04.L01.EX01",

            "title": "Design a Binary Sentiment Classifier",

            "lesson_code": "M04.L01",

            "section_id": "binary-classification",

            "placement": "after_section",

            "description": (
                "Practice connecting a binary classification problem to its "
                "input representation, output layer, activation, loss "
                "function, and validation strategy."
            ),

            "instructions": (
                "Imagine you are building a model that classifies customer "
                "feedback as positive or negative.\n\n"
                "1. Identify the number of output classes.\n"
                "2. Choose an appropriate final Dense layer and activation.\n"
                "3. Choose an appropriate loss function.\n"
                "4. Explain what an output value of `0.92` would mean.\n"
                "5. Explain why text must be converted into numerical tensors "
                "before being given to the network.\n"
                "6. Describe the roles of the training, validation, and test "
                "sets.\n"
                "7. Suppose training accuracy continues increasing while "
                "validation accuracy begins decreasing. Name the problem and "
                "explain what you would conclude."
            ),

            "expected_output": (
                "A short architecture proposal and written explanation covering "
                "the sigmoid output, binary crossentropy, numerical text "
                "representation, dataset splits, and overfitting."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "binary-classification",
                "sigmoid",
                "binary-crossentropy",
                "validation",
                "overfitting",
            ],
        },

        {
            "id": "M04.L01.EX02",

            "title": "Choose the Correct Workflow",

            "lesson_code": "M04.L01",

            "section_id": "regression",

            "placement": "after_section",

            "description": (
                "Practice selecting output layers, losses, metrics, "
                "preprocessing, and validation strategies for classification "
                "and regression problems."
            ),

            "instructions": (
                "For each scenario below, identify the problem type and choose "
                "a suitable output design.\n\n"
                "A. Predict whether an email is spam or not spam.\n"
                "B. Classify a news article into one of 25 topics.\n"
                "C. Predict the selling price of a house.\n\n"
                "For each scenario:\n"
                "1. State whether it is binary classification, multiclass "
                "classification, or scalar regression.\n"
                "2. State the number of output units.\n"
                "3. Choose the final activation.\n"
                "4. Choose a suitable loss function.\n"
                "5. Choose a useful evaluation metric.\n\n"
                "Then answer:\n"
                "6. Why should numerical feature normalization use statistics "
                "computed from the training set only?\n"
                "7. Why might K-fold validation be more reliable than one "
                "small validation split when only a few hundred samples are "
                "available?\n"
                "8. If a regression target was divided by 100,000 and MAE is "
                "0.27, approximately how large is the average error in the "
                "original target scale?"
            ),

            "expected_output": (
                "A table comparing the three workflows plus short written "
                "answers. For the final calculation, the expected average "
                "error is approximately 27,000 units of the original target "
                "scale."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "problem-framing",
                "output-layer-selection",
                "loss-selection",
                "feature-normalization",
                "cross-validation",
                "regression-metrics",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M04.L01.QZ01",

        "title": "Classification and Regression — Knowledge Check",

        "lesson_code": "M04.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M04.L01.Q01",

                "section_id": "problem-types",

                "question": (
                    "Which task is an example of scalar regression?"
                ),

                "options": [
                    "Classifying an image as cat or dog",
                    "Choosing one topic from 20 news categories",
                    "Predicting tomorrow's temperature as a numerical value",
                    "Assigning several labels to the same photograph",
                ],

                "correct": 2,

                "explanation": (
                    "Scalar regression predicts one continuous numerical "
                    "target. Temperature is a continuous value rather than a "
                    "discrete category."
                ),
            },

            {
                "id": "M04.L01.Q02",

                "section_id": "binary-classification",

                "question": (
                    "Which output configuration best matches a standard "
                    "binary classification problem?"
                ),

                "options": [
                    "One output unit with sigmoid",
                    "One output unit with softmax",
                    "46 output units with sigmoid",
                    "One output unit with no activation and mean squared error",
                ],

                "correct": 0,

                "explanation": (
                    "For two mutually exclusive classes, one sigmoid output can "
                    "represent a probability-like score between 0 and 1. "
                    "Binary crossentropy is commonly paired with this setup."
                ),
            },

            {
                "id": "M04.L01.Q03",

                "section_id": "multiclass-classification",

                "question": (
                    "A single-label classification problem has 30 classes. "
                    "Which final layer is most appropriate?"
                ),

                "options": [
                    "Dense(1, activation=\"sigmoid\")",
                    "Dense(30, activation=\"softmax\")",
                    "Dense(1) with no activation",
                    "Dense(4, activation=\"relu\")",
                ],

                "correct": 1,

                "explanation": (
                    "For N mutually exclusive classes, the final layer should "
                    "typically have N units with softmax so that the model "
                    "produces a probability distribution over all N classes."
                ),
            },

            {
                "id": "M04.L01.Q04",

                "section_id": "regression",

                "question": (
                    "Why should the mean and standard deviation used to "
                    "normalize test features be calculated from the training "
                    "data?"
                ),

                "options": [
                    "Because test data cannot contain floating-point values",
                    "Because neural networks cannot calculate test statistics",
                    "Because training statistics are always numerically smaller",
                    "Because using information from the test set would leak evaluation information into the workflow",
                ],

                "correct": 3,

                "explanation": (
                    "Preprocessing parameters should be learned from training "
                    "data. Computing them from the test set lets information "
                    "from the final evaluation data influence preprocessing, "
                    "which compromises the independence of the test set."
                ),
            },

            {
                "id": "M04.L01.Q05",

                "section_id": "regression",

                "type": "open",

                "question": (
                    "You receive a dataset with 500 samples. Each sample has "
                    "10 numerical features and one continuous target. Explain "
                    "how you would prepare the features, design the final model "
                    "output, choose a loss and evaluation metric, validate the "
                    "model, detect overfitting, and finally evaluate it on the "
                    "test set."
                ),
            },
        ],

        "passing_score": 70,
    },
}