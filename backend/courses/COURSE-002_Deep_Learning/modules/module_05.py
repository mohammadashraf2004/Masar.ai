"""M05.L01 — Fundamentals of Machine Learning.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 5, pages not provided in the supplied extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M05.L01"

MODULE_ORDER = 5

MODULE_TITLE = "Fundamentals of Machine Learning"

MODULE_DESCRIPTION = (
    "Build a rigorous mental model of generalization, overfitting, evaluation, "
    "model fitting, data quality, and regularization in deep learning."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Not provided in supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Fundamentals of Machine Learning",

    "slug": "deep-learning-foundations-m05-l01",

    "description": (
        "Understand optimization versus generalization, diagnose underfitting and "
        "overfitting, evaluate models correctly, improve model fit, and apply "
        "regularization techniques that improve performance on unseen data."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.5,

    "skill_tags": [
        "machine-learning",
        "generalization",
        "overfitting",
        "model-evaluation",
        "regularization",
        "feature-engineering",
        "dropout",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Fundamentals of Machine Learning",

        "content": (
            '# Fundamentals of Machine Learning\n'
            '\n'
            '> **Course:** Deep Learning Foundations  \n'
            '> **Lesson:** M05.L01  \n'
            '> **Module:** Fundamentals of Machine Learning  \n'
            '> **Source alignment:** BOOK-002, Chapter 5. The supplied chapter extract does not include page numbers. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n'
            '\n'
            '---\n'
            '\n'
            '## Learning outcomes\n'
            '\n'
            'By the end of this lesson, you should be able to:\n'
            '\n'
            '- Explain the tension between optimization and generalization.\n'
            '- Distinguish underfitting from overfitting using training and validation behavior.\n'
            '- Identify common causes of overfitting, including noisy data, ambiguous features, rare features, and spurious correlations.\n'
            '- Explain the manifold hypothesis and why interpolation helps deep learning generalize.\n'
            '- Use training, validation, and test sets correctly while avoiding information leaks.\n'
            '- Compare hold-out validation, K-fold validation, and iterated K-fold validation.\n'
            '- Diagnose training problems related to learning rate, batch size, architecture priors, and model capacity.\n'
            '- Apply common generalization techniques including data curation, feature engineering, early stopping, capacity control, weight regularization, and dropout.\n'
            '\n'
            '---\n'
            '\n'
            '## 1. Generalization is the real goal\n'
            '\n'
            'A machine-learning model is useful only if it works on data it has never seen before.\n'
            '\n'
            'That ability is called **generalization**.\n'
            '\n'
            'During training, however, we directly optimize only one thing: performance on the training data.\n'
            '\n'
            'This creates the central tension in machine learning:\n'
            '\n'
            '```text\n'
            'Optimization\n'
            '= make the model fit the training data better\n'
            '\n'
            'Generalization\n'
            '= make the model perform well on new, unseen data\n'
            '```\n'
            '\n'
            'At first, these goals usually move together. Training loss decreases and validation performance improves.\n'
            '\n'
            'But after enough training, they can separate.\n'
            '\n'
            'The model may continue improving on the training set while getting worse on unseen data.\n'
            '\n'
            'That is **overfitting**.\n'
            '\n'
            '### Underfitting versus overfitting\n'
            '\n'
            'A model is **underfit** when it has not yet captured enough useful structure in the training data.\n'
            '\n'
            'Typical signs:\n'
            '\n'
            '```text\n'
            'training loss      = still high\n'
            'validation loss    = also high\n'
            'training continues = both may improve\n'
            '```\n'
            '\n'
            'A model begins to **overfit** when it starts learning details that are specific to the training data but do not transfer to new examples.\n'
            '\n'
            'Typical pattern:\n'
            '\n'
            '```text\n'
            'training loss    ↓ keeps improving\n'
            'validation loss  ↓ improves at first\n'
            'validation loss  ↑ later gets worse\n'
            '```\n'
            '\n'
            'The point where validation performance is best is often close to the most useful balance between underfitting and overfitting.\n'
            '\n'
            '### Why overfitting happens\n'
            '\n'
            'Overfitting is not a rare edge case. It appears in essentially every machine-learning problem.\n'
            '\n'
            'Several data properties make it more likely.\n'
            '\n'
            '#### Noisy training data\n'
            '\n'
            'Real datasets often contain:\n'
            '\n'
            '- invalid inputs,\n'
            '- corrupted examples,\n'
            '- incorrect labels,\n'
            '- unusual outliers.\n'
            '\n'
            'If a model has enough capacity, it may spend effort memorizing these bad examples.\n'
            '\n'
            'That can hurt performance on normal unseen data.\n'
            '\n'
            '#### Ambiguous features\n'
            '\n'
            'Some problems are genuinely uncertain.\n'
            '\n'
            'For example, deciding whether a banana is:\n'
            '\n'
            '```text\n'
            'unripe\n'
            'ripe\n'
            'rotten\n'
            '```\n'
            '\n'
            'does not have perfectly sharp boundaries.\n'
            '\n'
            'Two humans may disagree on the same image.\n'
            '\n'
            'Likewise, the same weather measurements may sometimes be followed by rain and sometimes not.\n'
            '\n'
            'A model that becomes too confident about ambiguous regions may overfit instead of learning the broader pattern.\n'
            '\n'
            '#### Rare features and spurious correlations\n'
            '\n'
            'Suppose the word `"cherimoya"` appears only once in a sentiment dataset, and that one review is negative.\n'
            '\n'
            'A model might learn:\n'
            '\n'
            '```text\n'
            '"cherimoya" -> negative sentiment\n'
            '```\n'
            '\n'
            'even though the fruit itself has no negative meaning.\n'
            '\n'
            'This is a **spurious correlation**: a relationship that appears in the training sample but is not a reliable pattern in the real problem.\n'
            '\n'
            'Even features that appear many times can be misleading if small differences happen by chance.\n'
            '\n'
            '### Irrelevant features can reduce generalization\n'
            '\n'
            'The chapter gives a useful experiment with MNIST.\n'
            '\n'
            'Two versions of the input are compared:\n'
            '\n'
            '```text\n'
            'Original pixels + all-zero extra features\n'
            'Original pixels + random-noise extra features\n'
            '```\n'
            '\n'
            'Both contain the same useful information about the digit.\n'
            '\n'
            'But the random features create many opportunities for accidental correlations.\n'
            '\n'
            'As a result, the model trained with random-noise features generalizes worse.\n'
            '\n'
            'This leads to an important practical lesson:\n'
            '\n'
            '> More features are not automatically better.\n'
            '\n'
            'If you are uncertain whether a feature contains useful signal, **feature selection** can help.\n'
            '\n'
            'You can remove features that are weakly related to the prediction target and keep the input space cleaner.\n'
            '\n'
            '---\n'
            '\n'
            '## 2. Why deep learning can generalize\n'
            '\n'
            'A surprising property of deep neural networks is that they can memorize almost anything if they have enough capacity.\n'
            '\n'
            'You can even shuffle the labels in a dataset so that there is no real relationship between inputs and targets.\n'
            '\n'
            'A sufficiently large network can still drive the training loss down.\n'
            '\n'
            'But its validation performance will remain poor because there is no real pattern to generalize.\n'
            '\n'
            'This raises an important question:\n'
            '\n'
            '> If neural networks can memorize arbitrary mappings, why do they generalize at all?\n'
            '\n'
            'The chapter connects the answer to the structure of real-world data.\n'
            '\n'
            '### The manifold hypothesis\n'
            '\n'
            'Consider MNIST.\n'
            '\n'
            'Each digit image contains:\n'
            '\n'
            '```text\n'
            '28 × 28 = 784 pixels\n'
            '```\n'
            '\n'
            'Each pixel can take many possible values.\n'
            '\n'
            'Mathematically, the number of possible images is enormous.\n'
            '\n'
            'But almost all possible 28 × 28 arrays do **not** look like handwritten digits.\n'
            '\n'
            'Valid digits occupy only a tiny structured region of the full space.\n'
            '\n'
            'This motivates the **manifold hypothesis**:\n'
            '\n'
            '> Natural data tends to lie on a lower-dimensional, highly structured manifold inside the much larger space in which the data is represented.\n'
            '\n'
            'Examples include:\n'
            '\n'
            '- handwritten digits,\n'
            '- faces,\n'
            '- speech,\n'
            '- natural images,\n'
            '- natural language.\n'
            '\n'
            '### A simple geometric intuition\n'
            '\n'
            'Imagine a sheet of paper inside a room.\n'
            '\n'
            'The room is three-dimensional, but the paper is only two-dimensional.\n'
            '\n'
            'The paper occupies only a tiny structured part of the room.\n'
            '\n'
            'Similarly:\n'
            '\n'
            '```text\n'
            'high-dimensional input space\n'
            '        ↓\n'
            'natural data occupies\n'
            'a much smaller structured region\n'
            '```\n'
            '\n'
            'A **manifold** is a structured lower-dimensional space embedded inside a larger one.\n'
            '\n'
            '### Interpolation and local generalization\n'
            '\n'
            'If natural data lies on a smooth manifold, nearby valid examples are often meaningfully related.\n'
            '\n'
            'A model can learn from known examples and make sense of nearby unseen examples by **interpolation**.\n'
            '\n'
            'Conceptually:\n'
            '\n'
            '```text\n'
            'known example A\n'
            '      ↓\n'
            'nearby unseen example\n'
            '      ↓\n'
            'known example B\n'
            '```\n'
            '\n'
            'If the new example lies close to training examples on the learned manifold, the model has a chance to generalize correctly.\n'
            '\n'
            'This explains why the density and quality of training data matter so much.\n'
            '\n'
            '### Interpolation is not the same as arbitrary averaging\n'
            '\n'
            'The chapter distinguishes:\n'
            '\n'
            '```text\n'
            'linear interpolation in raw input space\n'
            '```\n'
            '\n'
            'from:\n'
            '\n'
            '```text\n'
            'interpolation along the latent manifold\n'
            '```\n'
            '\n'
            'A simple pixel-wise average of two handwritten digits may not look like a valid digit.\n'
            '\n'
            'But there may be a smooth path through the true digit manifold that gradually transforms one valid digit into another.\n'
            '\n'
            '### Deep learning as manifold fitting\n'
            '\n'
            'The chapter uses the intuition that deep learning learns a smooth, flexible mapping fitted to the data with gradient descent.\n'
            '\n'
            'Because the model is differentiable, the learned function is adjusted gradually.\n'
            '\n'
            'During training, there can be an intermediate stage where the model captures the broad structure of the data manifold before it starts memorizing training-specific details.\n'
            '\n'
            'That intermediate stage is where generalization is often best.\n'
            '\n'
            '### Training data is fundamental\n'
            '\n'
            'Generalization depends heavily on how well the training set covers the real data manifold.\n'
            '\n'
            'A useful principle is:\n'
            '\n'
            '```text\n'
            'better coverage of real data\n'
            '        ↓\n'
            'easier interpolation\n'
            '        ↓\n'
            'better generalization\n'
            '```\n'
            '\n'
            'So one of the strongest ways to improve a model is often:\n'
            '\n'
            '- collect more data,\n'
            '- improve label quality,\n'
            '- reduce noise,\n'
            '- cover important edge cases,\n'
            '- represent the problem with more informative features.\n'
            '\n'
            'If more data is not possible, the next strategy is to restrict or regularize the model so that it cannot memorize every training detail.\n'
            '\n'
            '---\n'
            '\n'
            '## 3. Evaluating machine-learning models correctly\n'
            '\n'
            'You cannot improve generalization unless you can measure it reliably.\n'
            '\n'
            'The standard solution is to separate data into:\n'
            '\n'
            '```text\n'
            'Training set\n'
            'Validation set\n'
            'Test set\n'
            '```\n'
            '\n'
            '### Training set\n'
            '\n'
            'Used to update model parameters.\n'
            '\n'
            '```text\n'
            'training data -> optimizer -> weight updates\n'
            '```\n'
            '\n'
            '### Validation set\n'
            '\n'
            'Used during development to make decisions such as:\n'
            '\n'
            '- number of layers,\n'
            '- layer size,\n'
            '- learning rate,\n'
            '- regularization strength,\n'
            '- training duration,\n'
            '- architecture choice.\n'
            '\n'
            'These choices are called **hyperparameters**.\n'
            '\n'
            '### Test set\n'
            '\n'
            'Used only for the final evaluation after model development is complete.\n'
            '\n'
            'The test set should approximate the kind of data the model will encounter in production.\n'
            '\n'
            '### Why validation and test sets must be separate\n'
            '\n'
            'Suppose you repeatedly:\n'
            '\n'
            '1. train a model,\n'
            '2. check performance on a dataset,\n'
            '3. change the model,\n'
            '4. check the same dataset again,\n'
            '5. repeat many times.\n'
            '\n'
            'Even if you never directly train on that dataset, your decisions gradually adapt to it.\n'
            '\n'
            'This is an **information leak**.\n'
            '\n'
            'The validation set is allowed to influence model development.\n'
            '\n'
            'The test set is not.\n'
            '\n'
            'So:\n'
            '\n'
            '```text\n'
            'training set   -> learns parameters\n'
            'validation set -> helps choose the model and hyperparameters\n'
            'test set       -> final unbiased evaluation\n'
            '```\n'
            '\n'
            'If you tune your model based on test performance, the test set is no longer a true test.\n'
            '\n'
            '### Simple hold-out validation\n'
            '\n'
            'The simplest evaluation method is:\n'
            '\n'
            '```text\n'
            'available development data\n'
            '        ↓\n'
            'training portion + validation portion\n'
            '```\n'
            '\n'
            'You train on the training portion and evaluate on the validation portion.\n'
            '\n'
            'After hyperparameters are chosen, you can train a final model using all non-test development data and evaluate once on the untouched test set.\n'
            '\n'
            'Hold-out validation works well when you have enough data.\n'
            '\n'
            'Its weakness appears when the validation set is small.\n'
            '\n'
            'If different random splits produce very different scores, your estimate may be unstable.\n'
            '\n'
            '### K-fold validation\n'
            '\n'
            'When data is limited, K-fold validation can give a more reliable estimate.\n'
            '\n'
            'Suppose:\n'
            '\n'
            '```text\n'
            'K = 5\n'
            '```\n'
            '\n'
            'Split the data into five equal parts.\n'
            '\n'
            'Then repeat:\n'
            '\n'
            '```text\n'
            'Fold 1 -> validation, folds 2-5 -> training\n'
            'Fold 2 -> validation, others   -> training\n'
            'Fold 3 -> validation, others   -> training\n'
            'Fold 4 -> validation, others   -> training\n'
            'Fold 5 -> validation, others   -> training\n'
            '```\n'
            '\n'
            'The final validation score is the average of all fold scores.\n'
            '\n'
            'This reduces dependence on one lucky or unlucky split.\n'
            '\n'
            '### Iterated K-fold validation with shuffling\n'
            '\n'
            'For very small datasets, you can repeat K-fold validation multiple times.\n'
            '\n'
            'Before each round:\n'
            '\n'
            '```text\n'
            'shuffle\n'
            'split into K folds\n'
            'evaluate all folds\n'
            '```\n'
            '\n'
            'Then average all the resulting scores.\n'
            '\n'
            'This can improve evaluation precision, but it is computationally expensive because many models must be trained.\n'
            '\n'
            '### Common-sense baselines\n'
            '\n'
            'Before tuning a complex model, define a trivial baseline.\n'
            '\n'
            'Examples:\n'
            '\n'
            '```text\n'
            '10-class balanced classification -> random accuracy ≈ 10%\n'
            'balanced binary classification   -> naive accuracy ≈ 50%\n'
            '90/10 imbalanced classification  -> always predict majority class = 90%\n'
            '```\n'
            '\n'
            'Your model should meaningfully beat the baseline.\n'
            '\n'
            'If it cannot, something is wrong:\n'
            '\n'
            '- the input may not contain useful predictive information,\n'
            '- the model may be inappropriate,\n'
            '- the target may be too noisy,\n'
            '- the implementation may be broken.\n'
            '\n'
            '### Evaluation pitfalls\n'
            '\n'
            '#### Data representativeness\n'
            '\n'
            'Training and evaluation splits should represent the real data distribution.\n'
            '\n'
            'If data is ordered by class and you split it without shuffling, one split may contain completely different classes from another.\n'
            '\n'
            '#### The arrow of time\n'
            '\n'
            'For future prediction problems:\n'
            '\n'
            '```text\n'
            'past -> future\n'
            '```\n'
            '\n'
            'do not randomly shuffle time-series data.\n'
            '\n'
            'That can leak future information into training.\n'
            '\n'
            'Instead:\n'
            '\n'
            '```text\n'
            'earlier data -> training\n'
            'later data   -> validation/test\n'
            '```\n'
            '\n'
            '#### Duplicate or redundant samples\n'
            '\n'
            'If the same example appears in both training and validation data, validation performance becomes misleading.\n'
            '\n'
            'The splits must be genuinely disjoint.\n'
            '\n'
            '{{exercise:M05.L01.EX01}}\n'
            '\n'
            '---\n'
            '\n'
            '## 4. Improving model fit before fighting overfitting\n'
            '\n'
            'A useful development strategy from the chapter is:\n'
            '\n'
            '> First make the model capable of learning and overfitting. Then work on improving generalization.\n'
            '\n'
            'Why?\n'
            '\n'
            'Because if the model cannot even fit the training data, you do not yet know whether generalization is the main problem.\n'
            '\n'
            'The chapter identifies three common situations.\n'
            '\n'
            '### Problem 1: Training does not get started\n'
            '\n'
            'Symptoms:\n'
            '\n'
            '```text\n'
            'training loss barely changes\n'
            'accuracy does not improve\n'
            '```\n'
            '\n'
            'Likely causes include the configuration of gradient descent.\n'
            '\n'
            'Important hyperparameters include:\n'
            '\n'
            '- optimizer,\n'
            '- weight initialization,\n'
            '- learning rate,\n'
            '- batch size.\n'
            '\n'
            'In practice, the chapter recommends starting by adjusting:\n'
            '\n'
            '```text\n'
            'learning rate\n'
            'batch size\n'
            '```\n'
            '\n'
            '### Learning rate\n'
            '\n'
            'If the learning rate is too high:\n'
            '\n'
            '```text\n'
            'update step is too large\n'
            '        ↓\n'
            'model overshoots useful regions\n'
            '        ↓\n'
            'training may stall or become unstable\n'
            '```\n'
            '\n'
            'If the learning rate is too low:\n'
            '\n'
            '```text\n'
            'updates are tiny\n'
            '        ↓\n'
            'training improves extremely slowly\n'
            '```\n'
            '\n'
            'A practical troubleshooting rule:\n'
            '\n'
            '> If training is stuck, try both lowering and increasing the learning rate.\n'
            '\n'
            '### Batch size\n'
            '\n'
            'A larger batch uses more examples to estimate each gradient.\n'
            '\n'
            'This often produces:\n'
            '\n'
            '```text\n'
            'less noisy gradient estimate\n'
            '```\n'
            '\n'
            'but requires more memory.\n'
            '\n'
            'Batch size and learning rate interact, so they should not always be considered independently.\n'
            '\n'
            '### Problem 2: The model trains but does not generalize\n'
            '\n'
            'Suppose training loss decreases but validation performance does not beat the baseline.\n'
            '\n'
            'Two major possibilities are:\n'
            '\n'
            '#### The input contains insufficient information\n'
            '\n'
            'If the target cannot be predicted from the features, no model can generalize.\n'
            '\n'
            'The shuffled-label MNIST experiment demonstrates this.\n'
            '\n'
            'The network can memorize, but there is no meaningful relationship to learn.\n'
            '\n'
            '#### The architecture has the wrong prior\n'
            '\n'
            'Different model architectures make different assumptions about data.\n'
            '\n'
            'For example:\n'
            '\n'
            '```text\n'
            'images      -> convolutional architectures are often appropriate\n'
            'sequences   -> sequence-aware architectures are often appropriate\n'
            'time series -> temporal structure matters\n'
            '```\n'
            '\n'
            'A model with the wrong architecture may have enough capacity to fit training data but still fail to capture the right structure.\n'
            '\n'
            'These built-in assumptions are called **architecture priors**.\n'
            '\n'
            '### Problem 3: The model cannot overfit\n'
            '\n'
            'If both training and validation performance improve but eventually stall, and the model never begins to overfit, the model may not have enough capacity.\n'
            '\n'
            '**Model capacity** refers to how much information and complexity the model can represent.\n'
            '\n'
            'You can increase capacity by:\n'
            '\n'
            '- adding more layers,\n'
            '- using larger layers,\n'
            '- using a more appropriate layer type,\n'
            '- choosing a stronger architecture.\n'
            '\n'
            'A useful development pattern is:\n'
            '\n'
            '```text\n'
            'too small\n'
            '   ↓\n'
            'increase capacity\n'
            '   ↓\n'
            'model can fit and eventually overfit\n'
            '   ↓\n'
            'regularize to recover better generalization\n'
            '```\n'
            '\n'
            '### Too much capacity\n'
            '\n'
            'A model can also be much larger than necessary.\n'
            '\n'
            'A very large model may:\n'
            '\n'
            '```text\n'
            'fit training data extremely fast\n'
            'overfit almost immediately\n'
            'develop a large train-validation gap\n'
            '```\n'
            '\n'
            'The goal is not to find the largest model.\n'
            '\n'
            'The goal is to find enough capacity to learn useful structure, then control overfitting.\n'
            '\n'
            '---\n'
            '\n'
            '## 5. Improving generalization\n'
            '\n'
            'Once the model can learn and overfit, the focus changes:\n'
            '\n'
            '```text\n'
            'before:\n'
            'Can the model fit?\n'
            '\n'
            'after:\n'
            'How do we make the useful fit generalize?\n'
            '```\n'
            '\n'
            'The chapter presents several major strategies.\n'
            '\n'
            '### 5.1 Dataset curation\n'
            '\n'
            'Improving the dataset is often more valuable than making the model more complicated.\n'
            '\n'
            'Important actions include:\n'
            '\n'
            '- collect enough data,\n'
            '- correct labeling errors,\n'
            '- inspect suspicious examples,\n'
            '- clean missing or corrupted values,\n'
            '- remove useless features,\n'
            '- cover important parts of the input space.\n'
            '\n'
            'A simple principle:\n'
            '\n'
            '> Better data usually improves generalization more reliably than a more complicated model.\n'
            '\n'
            '### 5.2 Feature engineering\n'
            '\n'
            'Feature engineering means applying human knowledge to transform raw inputs into representations that make the task easier.\n'
            '\n'
            'Consider a clock-reading task.\n'
            '\n'
            '#### Hard version\n'
            '\n'
            'Input:\n'
            '\n'
            '```text\n'
            'raw image pixels\n'
            '```\n'
            '\n'
            'The model must learn:\n'
            '\n'
            '- shapes,\n'
            '- hand positions,\n'
            '- geometry,\n'
            '- relationship between angles and time.\n'
            '\n'
            '#### Better engineered features\n'
            '\n'
            'Extract:\n'
            '\n'
            '```text\n'
            'tip coordinates of hour hand\n'
            'tip coordinates of minute hand\n'
            '```\n'
            '\n'
            '#### Even better\n'
            '\n'
            'Convert coordinates into:\n'
            '\n'
            '```text\n'
            'hand angles\n'
            '```\n'
            '\n'
            'At that point, the prediction problem becomes dramatically simpler.\n'
            '\n'
            'The goal of feature engineering is:\n'
            '\n'
            '```text\n'
            'make the latent structure simpler\n'
            'make the task easier\n'
            'reduce required model complexity\n'
            'reduce required training data\n'
            '```\n'
            '\n'
            'Deep learning reduces the need for manual feature engineering, but it does not make domain knowledge useless.\n'
            '\n'
            'Good features can still:\n'
            '\n'
            '- reduce compute requirements,\n'
            '- improve performance with limited data,\n'
            '- simplify the model.\n'
            '\n'
            '### 5.3 Early stopping\n'
            '\n'
            'Deep networks usually have far more parameters than strictly necessary.\n'
            '\n'
            'If you train long enough, the model may move from:\n'
            '\n'
            '```text\n'
            'underfit\n'
            '   ↓\n'
            'good generalization\n'
            '   ↓\n'
            'overfit\n'
            '```\n'
            '\n'
            '**Early stopping** means stopping training near the point where validation performance is best.\n'
            '\n'
            'Conceptually:\n'
            '\n'
            '```text\n'
            'epoch 1  -> underfit\n'
            'epoch 5  -> improving\n'
            'epoch 9  -> best validation\n'
            'epoch 15 -> overfitting\n'
            '\n'
            'stop around epoch 9\n'
            '```\n'
            '\n'
            'Instead of manually retraining after finding the best epoch, frameworks such as Keras can use callbacks that monitor validation performance and stop automatically.\n'
            '\n'
            '### 5.4 Reducing model size\n'
            '\n'
            'A smaller model has less capacity to memorize arbitrary details.\n'
            '\n'
            'If the model has limited memory, optimization pushes it toward compressed, reusable patterns.\n'
            '\n'
            'But making the model too small causes underfitting.\n'
            '\n'
            'So capacity control is a balance:\n'
            '\n'
            '```text\n'
            'too small  -> underfit\n'
            'reasonable -> useful fit\n'
            'too large  -> overfit quickly\n'
            '```\n'
            '\n'
            'There is no universal formula for the perfect number of layers or units.\n'
            '\n'
            'You must compare architectures using the validation set.\n'
            '\n'
            '### 5.5 Weight regularization\n'
            '\n'
            'Another strategy is to discourage large weight values.\n'
            '\n'
            'The idea is to add a penalty to the loss.\n'
            '\n'
            '#### L1 regularization\n'
            '\n'
            'Penalty is proportional to:\n'
            '\n'
            '```text\n'
            '|weight|\n'
            '```\n'
            '\n'
            '#### L2 regularization\n'
            '\n'
            'Penalty is proportional to:\n'
            '\n'
            '```text\n'
            'weight²\n'
            '```\n'
            '\n'
            'L2 is also commonly called **weight decay**.\n'
            '\n'
            'In Keras:\n'
            '\n'
            '```python\n'
            'from keras import layers\n'
            'from keras.regularizers import l2\n'
            '\n'
            'layer = layers.Dense(\n'
            '    16,\n'
            '    activation="relu",\n'
            '    kernel_regularizer=l2(0.002),\n'
            ')\n'
            '```\n'
            '\n'
            'The optimization objective becomes roughly:\n'
            '\n'
            '```text\n'
            'total loss\n'
            '=\n'
            'prediction loss\n'
            '+\n'
            'regularization penalty\n'
            '```\n'
            '\n'
            'This discourages unnecessarily extreme parameter values.\n'
            '\n'
            '### 5.6 Dropout\n'
            '\n'
            'Dropout is one of the most widely used neural-network regularization techniques.\n'
            '\n'
            'During training, dropout randomly sets some activations to zero.\n'
            '\n'
            'Example:\n'
            '\n'
            '```text\n'
            'before dropout:\n'
            '[0.2, 0.5, 1.3, 0.8, 1.1]\n'
            '\n'
            'after dropout:\n'
            '[0.0, 0.5, 1.3, 0.0, 1.1]\n'
            '```\n'
            '\n'
            'A dropout rate of:\n'
            '\n'
            '```text\n'
            '0.5\n'
            '```\n'
            '\n'
            'means roughly half of the selected activations are dropped during training.\n'
            '\n'
            'The randomness prevents the network from relying too heavily on fragile combinations of features.\n'
            '\n'
            'This makes memorization harder and encourages more robust representations.\n'
            '\n'
            'In Keras:\n'
            '\n'
            '```python\n'
            'model = keras.Sequential(\n'
            '    [\n'
            '        layers.Dense(16, activation="relu"),\n'
            '        layers.Dropout(0.5),\n'
            '        layers.Dense(16, activation="relu"),\n'
            '        layers.Dropout(0.5),\n'
            '        layers.Dense(1, activation="sigmoid"),\n'
            '    ]\n'
            ')\n'
            '```\n'
            '\n'
            'Dropout behaves differently during training and inference.\n'
            '\n'
            'During training:\n'
            '\n'
            '```text\n'
            'random activations are dropped\n'
            '```\n'
            '\n'
            'During inference:\n'
            '\n'
            '```text\n'
            'the full network is used with appropriate scaling behavior\n'
            '```\n'
            '\n'
            '{{exercise:M05.L01.EX02}}\n'
            '\n'
            '---\n'
            '\n'
            '## 6. A practical workflow for a new machine-learning problem\n'
            '\n'
            'The entire chapter can be turned into a development workflow.\n'
            '\n'
            '### Step 1 — Define a baseline\n'
            '\n'
            'Ask:\n'
            '\n'
            '```text\n'
            'What trivial performance level must the model beat?\n'
            '```\n'
            '\n'
            'Examples include:\n'
            '\n'
            '- random prediction,\n'
            '- majority-class prediction,\n'
            '- a simple heuristic.\n'
            '\n'
            '### Step 2 — Create reliable splits\n'
            '\n'
            'Build:\n'
            '\n'
            '```text\n'
            'training set\n'
            'validation set\n'
            'test set\n'
            '```\n'
            '\n'
            'Check for:\n'
            '\n'
            '- duplicates,\n'
            '- class imbalance,\n'
            '- time leakage,\n'
            '- unrepresentative splits.\n'
            '\n'
            '### Step 3 — Get training to work\n'
            '\n'
            'If training loss does not decrease:\n'
            '\n'
            '- inspect the implementation,\n'
            '- adjust learning rate,\n'
            '- adjust batch size,\n'
            '- verify preprocessing,\n'
            '- verify targets and loss function.\n'
            '\n'
            '### Step 4 — Verify some generalization\n'
            '\n'
            'If the model cannot beat the baseline:\n'
            '\n'
            '- ask whether the data contains signal,\n'
            '- inspect labels,\n'
            '- consider better features,\n'
            '- choose a more appropriate architecture.\n'
            '\n'
            '### Step 5 — Make sure the model can overfit\n'
            '\n'
            'If it cannot:\n'
            '\n'
            '- increase capacity,\n'
            '- train longer,\n'
            '- improve architecture priors.\n'
            '\n'
            'Being able to overfit proves that the model has enough representational power.\n'
            '\n'
            '### Step 6 — Find the overfitting boundary\n'
            '\n'
            'Monitor:\n'
            '\n'
            '```text\n'
            'training loss\n'
            'validation loss\n'
            'training metrics\n'
            'validation metrics\n'
            '```\n'
            '\n'
            'Identify where validation performance peaks.\n'
            '\n'
            '### Step 7 — Improve generalization\n'
            '\n'
            'Try:\n'
            '\n'
            '```text\n'
            'more or better data\n'
            'better features\n'
            'early stopping\n'
            'smaller model\n'
            'L1/L2 regularization\n'
            'dropout\n'
            '```\n'
            '\n'
            '### Step 8 — Re-evaluate honestly\n'
            '\n'
            'Use the validation set while developing.\n'
            '\n'
            'Use the test set only after development decisions are complete.\n'
            '\n'
            'A concise mental model is:\n'
            '\n'
            '```text\n'
            'Fit enough to learn\n'
            '        ↓\n'
            'Detect overfitting\n'
            '        ↓\n'
            'Regularize and improve data\n'
            '        ↓\n'
            'Maximize validation performance\n'
            '        ↓\n'
            'Evaluate once on test data\n'
            '```\n'
            '\n'
            '---\n'
            '\n'
            '## Important misconception\n'
            '\n'
            '### Misconception\n'
            '\n'
            '> "The best model is the model with the lowest training loss."\n'
            '\n'
            '### Why this is wrong\n'
            '\n'
            'Training loss measures how well the model fits examples it has already seen.\n'
            '\n'
            'Machine learning is useful because we want performance on unseen data.\n'
            '\n'
            'A model can achieve extremely low training loss by memorizing training examples while becoming worse on validation and test data.\n'
            '\n'
            'The real goal is not maximum training fit.\n'
            '\n'
            'The real goal is **generalization**.\n'
            '\n'
            '---\n'
            '\n'
            '## Key terminology\n'
            '\n'
            '| Term | Meaning |\n'
            '|---|---|\n'
            '| Optimization | Improving model performance on the training data |\n'
            '| Generalization | Performance on unseen data |\n'
            '| Underfitting | The model has not captured enough useful structure |\n'
            '| Overfitting | The model learns training-specific details that do not transfer |\n'
            '| Spurious correlation | A training-set relationship that appears predictive by chance |\n'
            '| Manifold hypothesis | The idea that natural data lies on structured low-dimensional regions inside larger input spaces |\n'
            '| Interpolation | Making sense of a new point using nearby known points on the learned data manifold |\n'
            '| Training set | Data used to update model parameters |\n'
            '| Validation set | Data used to guide model and hyperparameter choices |\n'
            '| Test set | Untouched data used for final evaluation |\n'
            '| Information leak | Indirect transfer of evaluation-set information into model development |\n'
            '| Hold-out validation | Evaluation using one fixed validation split |\n'
            '| K-fold validation | Evaluation by rotating through K different validation folds |\n'
            '| Common-sense baseline | A trivial reference performance that a useful model should beat |\n'
            '| Hyperparameter | A configuration chosen by the developer rather than learned as a model weight |\n'
            '| Architecture prior | Assumptions encoded by the choice of model architecture |\n'
            '| Model capacity | The amount of complexity or information a model can represent |\n'
            '| Feature engineering | Human-designed transformations that make the learning problem easier |\n'
            '| Early stopping | Ending training when validation performance stops improving |\n'
            '| Regularization | Techniques that constrain fitting to improve generalization |\n'
            '| L1 regularization | Penalty proportional to absolute weight values |\n'
            '| L2 regularization | Penalty proportional to squared weight values; also called weight decay |\n'
            '| Dropout | Randomly suppressing activations during training to reduce overfitting |\n'
            '\n'
            '---\n'
            '\n'
            '## Self-check\n'
            '\n'
            'Before continuing, make sure you can answer:\n'
            '\n'
            '1. What is the difference between optimization and generalization?\n'
            '2. How can you recognize underfitting and overfitting from training and validation behavior?\n'
            '3. Why can irrelevant features create spurious correlations?\n'
            '4. What does the manifold hypothesis say about natural data?\n'
            '5. Why does denser coverage of the data manifold help generalization?\n'
            '6. Why do we need separate validation and test sets?\n'
            '7. When is K-fold validation preferable to a simple hold-out split?\n'
            '8. Why is a common-sense baseline useful?\n'
            '9. What should you try when training loss refuses to decrease?\n'
            '10. What does it mean if a model trains but never beats a trivial baseline?\n'
            '11. What does it mean if a model cannot overfit?\n'
            '12. How do early stopping, L2 regularization, and dropout reduce overfitting?\n'
            '\n'
            '---\n'
            '\n'
            '## Retain this idea\n'
            '\n'
            '**Machine learning is the art of fitting enough to learn real structure without fitting so much that the model memorizes the training set. Reliable evaluation tells you where that boundary is, and better data plus regularization helps you stay on the generalizable side of it.**\n'
        ),

        "estimated_minutes": 150,

        "has_code_examples": True,

        "sections": [
            {
                "id": 'generalization-and-overfitting',
                "title": 'Generalization is the real goal',
                "order": 1,
            },
            {
                "id": 'why-deep-learning-generalizes',
                "title": 'Why deep learning can generalize',
                "order": 2,
            },
            {
                "id": 'model-evaluation',
                "title": 'Evaluating machine-learning models correctly',
                "order": 3,
            },
            {
                "id": 'improving-model-fit',
                "title": 'Improving model fit before fighting overfitting',
                "order": 4,
            },
            {
                "id": 'improving-generalization',
                "title": 'Improving generalization',
                "order": 5,
            },
            {
                "id": 'practical-workflow',
                "title": 'A practical workflow for a new machine-learning problem',
                "order": 6,
            }
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": 'M05.L01.EX01',
            "title": 'Design a Reliable Evaluation Protocol',
            "lesson_code": "M05.L01",
            "section_id": 'model-evaluation',
            "placement": "after_section",
            "description": 'Practice choosing data splits and evaluation methods while avoiding information leakage.',
            "instructions": '1. Imagine you have 6,000 labeled examples for a classification problem.\n2. Propose training, validation, and test splits and explain the role of each split.\n3. Explain why the test set must not be used while tuning the model.\n4. Describe when you would prefer K-fold validation over one fixed validation split.\n5. Add one evaluation warning for a time-series version of the same problem.',
            "expected_output": 'A short evaluation plan containing the three dataset roles, an explanation of information leakage, a K-fold use case, and one time-series precaution.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'model-evaluation',
                'data-splitting',
                'information-leakage',
            ],
        },

        {
            "id": 'M05.L01.EX02',
            "title": 'Diagnose and Regularize an Overfitting Model',
            "lesson_code": "M05.L01",
            "section_id": 'improving-generalization',
            "placement": "after_section",
            "description": 'Use training and validation behavior to select practical anti-overfitting strategies.',
            "instructions": '1. Assume training loss keeps decreasing but validation loss starts increasing after epoch 7.\n2. Identify the problem and explain why the lowest training loss is not the goal.\n3. Propose at least three interventions from the chapter.\n4. Explain how one intervention changes model capacity or learning behavior.\n5. Explain how you would decide which intervention actually helped.',
            "expected_output": 'A diagnosis of overfitting plus at least three chapter-supported interventions and an evaluation plan based on validation performance.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'overfitting',
                'regularization',
                'early-stopping',
                'validation',
            ],
        }
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M05.L01.QZ01",

        "title": "Fundamentals of Machine Learning — Knowledge Check",

        "lesson_code": "M05.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": 'M05.L01.Q01',
                "section_id": 'generalization-and-overfitting',
                "question": 'What is the central tension in machine learning described in the chapter?',
                "options": [
                    'Optimization versus generalization',
                    'Python versus NumPy',
                    'CPU versus GPU',
                    'Classification versus regression',
                ],
                "correct": 0,
                "explanation": 'Optimization improves fit to training data, while generalization measures performance on unseen data. Excessive optimization can eventually hurt generalization.',
            },

            {
                "id": 'M05.L01.Q02',
                "section_id": 'generalization-and-overfitting',
                "question": 'Which pattern most clearly indicates overfitting?',
                "options": [
                    'Training and validation loss are both unchanged from the start',
                    'Training loss improves while validation performance begins to degrade',
                    'Training loss is high and validation loss is equally high',
                    'The model has not started training',
                ],
                "correct": 1,
                "explanation": 'Overfitting appears when the model continues improving on training data but becomes worse on held-out data.',
            },

            {
                "id": 'M05.L01.Q03',
                "section_id": 'why-deep-learning-generalizes',
                "question": 'What does the manifold hypothesis suggest?',
                "options": [
                    'Natural data occupies structured lower-dimensional regions within a larger input space',
                    'Every possible input is equally likely',
                    'Neural networks cannot memorize random labels',
                    'Generalization requires linear interpolation only',
                ],
                "correct": 0,
                "explanation": 'The chapter argues that natural data lies on structured manifolds, making interpolation between nearby valid examples possible.',
            },

            {
                "id": 'M05.L01.Q04',
                "section_id": 'model-evaluation',
                "question": 'Why should the test set remain untouched during model development?',
                "options": [
                    'Because test data cannot have labels',
                    'Because using it to tune choices leaks information and biases the final generalization estimate',
                    'Because test data must always be larger than training data',
                    'Because test data is used to update weights',
                ],
                "correct": 1,
                "explanation": 'Any tuning based on test results makes the final test score less trustworthy as an estimate of performance on truly unseen data.',
            },

            {
                "id": 'M05.L01.Q05',
                "section_id": 'model-evaluation',
                "question": 'When is K-fold validation particularly useful?',
                "options": [
                    'When a single split is unstable because relatively little data is available',
                    'Only when millions of examples are available',
                    'When you want to train on the test set',
                    'When labels are unnecessary',
                ],
                "correct": 0,
                "explanation": 'K-fold validation reduces dependence on one particular validation split and is useful when data is limited.',
            },

            {
                "id": 'M05.L01.Q06',
                "section_id": 'improving-model-fit',
                "question": 'If training loss does not meaningfully decrease, what should you investigate first according to the chapter?',
                "options": [
                    'Only dropout',
                    'Gradient-descent configuration such as learning rate and batch size',
                    'Only the test-set size',
                    'Only L2 regularization',
                ],
                "correct": 1,
                "explanation": 'The chapter recommends checking gradient-descent configuration, with learning rate and batch size being especially practical parameters to tune.',
            },

            {
                "id": 'M05.L01.Q07',
                "section_id": 'improving-model-fit',
                "question": 'What does it often mean if a model can fit but never begins to overfit?',
                "options": [
                    'It may have insufficient model capacity',
                    'The test set is too large',
                    'The model has too much dropout only',
                    'Generalization is already perfect',
                ],
                "correct": 0,
                "explanation": 'If a model cannot overfit despite continued training, it may not have enough representational capacity or the right architecture.',
            },

            {
                "id": 'M05.L01.Q08',
                "section_id": 'improving-generalization',
                "question": 'Which statement about dropout is correct?',
                "options": [
                    'It randomly suppresses a fraction of activations during training',
                    'It permanently deletes model layers',
                    'It is only a data-splitting method',
                    'It always increases model capacity',
                ],
                "correct": 0,
                "explanation": 'Dropout injects randomness by zeroing selected activations during training, which can reduce fragile co-adaptations and overfitting.',
            },

            {
                "id": 'M05.L01.Q09',
                "section_id": 'improving-generalization',
                "question": 'What is L2 regularization?',
                "options": [
                    'A penalty proportional to squared weight values',
                    'A method for adding more layers',
                    'A validation-splitting technique',
                    'A way to shuffle labels',
                ],
                "correct": 0,
                "explanation": 'L2 regularization, also called weight decay in this context, adds a cost proportional to the square of model weights.',
            },

            {
                "id": 'M05.L01.Q10',
                "section_id": 'practical-workflow',
                "type": "open",
                "question": 'A model beats the baseline, then training loss keeps improving while validation loss worsens. Explain what stage of the workflow you are in and propose a chapter-supported plan to improve generalization.',
            }
        ],

        "passing_score": 70,
    },
}
