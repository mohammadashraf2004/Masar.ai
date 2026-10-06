"""M02.L01 — Supervised Learning Foundations.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-001, Chapter 2, sections 2.1–2.2.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M02.L01"

MODULE_ORDER = 2

MODULE_TITLE = "Supervised Learning Foundations"

MODULE_DESCRIPTION = (
    "Understand the two major supervised-learning problem types and learn how "
    "generalization, overfitting, underfitting, model complexity, and dataset "
    "size affect whether a model succeeds on unseen data."
)

SOURCE_CHAPTER = 2

SOURCE_PAGES = "Sections 2.1–2.2"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Supervised Learning: Classification, Regression, and Generalization",

    "slug": "ml-foundations-m02-l01",

    "description": (
        "Learn how supervised learning uses labeled examples, distinguish "
        "classification from regression, and reason about generalization, "
        "overfitting, underfitting, and model complexity."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 1.0,

    "skill_tags": [
        "machine-learning",
        "supervised-learning",
        "classification",
        "regression",
        "generalization",
        "overfitting",
        "underfitting",
        "module-02",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Supervised Learning: Classification, Regression, and Generalization",

        "content": (
            "# Supervised Learning: Classification, Regression, and Generalization\n"
            "\n"
            "> **Course:** Machine Learning Foundations  \n"
            "> **Lesson:** M02.L01  \n"
            "> **Module:** Supervised Learning Foundations  \n"
            "> **Source alignment:** BOOK-001, Chapter 2, sections 2.1–2.2. "
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
            "- Explain what supervised learning learns from input/output examples.\n"
            "- Distinguish classification problems from regression problems.\n"
            "- Distinguish binary classification from multiclass classification.\n"
            "- Explain what generalization means and why unseen data matters.\n"
            "- Diagnose basic signs of overfitting and underfitting.\n"
            "- Explain how model complexity and dataset size affect generalization.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. What supervised learning is\n"
            "\n"
            "Supervised learning is used when we want a model to predict an "
            "outcome from an input and we already have examples where both the "
            "input and the correct output are known.\n"
            "\n"
            "You can think of each training example as a pair:\n"
            "\n"
            "```text\n"
            "input X  ->  correct answer y\n"
            "```\n"
            "\n"
            "A collection of these examples forms the **training set**. The "
            "model studies these examples and learns a relationship that it can "
            "use later when it receives a new input.\n"
            "\n"
            "### Intuition\n"
            "\n"
            "Imagine that you want to predict the selling price of a house. "
            "Your training data might look like this:\n"
            "\n"
            "```text\n"
            "Area      Bedrooms      Price\n"
            "100 m²    2             2,000,000\n"
            "150 m²    3             3,000,000\n"
            "200 m²    4             4,200,000\n"
            "```\n"
            "\n"
            "The area and number of bedrooms are inputs. The price is the "
            "known output. After learning from many examples, the model can be "
            "asked to predict the price of a house it has never seen before.\n"
            "\n"
            "The key point is that supervised learning does not only try to "
            "remember the training examples. Its real purpose is to learn a "
            "pattern that remains useful for new examples.\n"
            "\n"
            "### A simple mental model\n"
            "\n"
            "```text\n"
            "Labeled examples\n"
            "      ↓\n"
            "Training process\n"
            "      ↓\n"
            "Learned model\n"
            "      ↓\n"
            "New unseen input\n"
            "      ↓\n"
            "Prediction\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Classification vs. regression\n"
            "\n"
            "The two major supervised-learning problem types are "
            "**classification** and **regression**.\n"
            "\n"
            "The easiest way to distinguish them is to look at the type of "
            "answer the model must produce.\n"
            "\n"
            "### Classification: predict a category\n"
            "\n"
            "Classification predicts a class label chosen from a predefined "
            "set of possibilities.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "```text\n"
            "Email  -> spam / not spam\n"
            "Tumor  -> benign / malignant\n"
            "Image  -> cat / dog / bird\n"
            "Flower -> setosa / versicolor / virginica\n"
            "```\n"
            "\n"
            "If there are exactly two possible classes, the problem is called "
            "**binary classification**.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- spam vs. not spam\n"
            "- fraud vs. not fraud\n"
            "- malignant vs. benign\n"
            "\n"
            "If there are more than two classes, the problem is called "
            "**multiclass classification**.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- cat, dog, or bird\n"
            "- Arabic, English, French, or Spanish\n"
            "- several flower species\n"
            "\n"
            "### Positive and negative classes\n"
            "\n"
            "In binary classification, one class is often called the "
            "**positive class** and the other the **negative class**.\n"
            "\n"
            "The word *positive* does not mean good. It usually means the class "
            "we are focusing on detecting.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Spam detection:\n"
            "positive class -> spam\n"
            "negative class -> not spam\n"
            "```\n"
            "\n"
            "### Regression: predict a continuous number\n"
            "\n"
            "Regression predicts a numeric quantity whose possible values have "
            "a meaningful continuous ordering.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "```text\n"
            "House -> 3,250,000 EGP\n"
            "Employee -> 24,000 EGP monthly income\n"
            "Farm -> 18.6 tons of crop yield\n"
            "```\n"
            "\n"
            "A useful test is to ask whether nearby numeric answers are still "
            "similar answers.\n"
            "\n"
            "For example, if the true annual income is 40,000 and the model "
            "predicts 40,001, the prediction is extremely close. The output "
            "changes continuously.\n"
            "\n"
            "By contrast, there is no meaningful class halfway between "
            "\"English\" and \"French.\" Language prediction is therefore "
            "classification, not regression.\n"
            "\n"
            "### Quick decision rule\n"
            "\n"
            "| Question | Problem type |\n"
            "|---|---|\n"
            "| Which category does this belong to? | Classification |\n"
            "| How much, how many, or what numeric value? | Regression |\n"
            "\n"

            # Exercise EX01 is rendered here by the frontend.
            "{{exercise:M02.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Generalization: the real goal of learning\n"
            "\n"
            "A model is useful only if it performs well on data it did not see "
            "during training.\n"
            "\n"
            "This ability is called **generalization**.\n"
            "\n"
            "Suppose a model achieves:\n"
            "\n"
            "```text\n"
            "Training accuracy: 100%\n"
            "Test accuracy:      60%\n"
            "```\n"
            "\n"
            "The training score looks impressive, but the test score tells us "
            "that the model does not work nearly as well on unseen examples.\n"
            "\n"
            "A useful analogy is studying for an exam. A student can memorize "
            "the exact answers to practice questions without understanding the "
            "subject. If the exam contains new questions, the student may fail. "
            "A model can behave in the same way.\n"
            "\n"
            "### Training set and test set\n"
            "\n"
            "A common workflow is to split available labeled data into two parts:\n"
            "\n"
            "```text\n"
            "All labeled data\n"
            "      ↓\n"
            "┌───────────────┬───────────────┐\n"
            "│ Training set  │ Test set      │\n"
            "│ learn from it │ evaluate only │\n"
            "└───────────────┴───────────────┘\n"
            "```\n"
            "\n"
            "The model learns from the training set. The test set is held back "
            "so that we can estimate how well the model handles unseen data.\n"
            "\n"
            "### Minimal scikit-learn example\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import train_test_split\n"
            "\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X,\n"
            "    y,\n"
            "    random_state=0,\n"
            ")\n"
            "```\n"
            "\n"
            "Here, `X_train` and `y_train` are used to train a model, while "
            "`X_test` and `y_test` are reserved for evaluation.\n"
            "\n"
            "The important idea is not the syntax. It is the separation of "
            "**learning** from **evaluation**.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Overfitting, underfitting, and model complexity\n"
            "\n"
            "A model can fail because it is too complex or because it is too "
            "simple.\n"
            "\n"
            "### Overfitting\n"
            "\n"
            "**Overfitting** happens when a model follows the details and "
            "peculiarities of the training data too closely.\n"
            "\n"
            "Imagine that we have a tiny dataset of previous customers and want "
            "to predict who will buy a boat. We could create a complicated rule "
            "that perfectly explains every person in that small table. A "
            "perfect training score still does not guarantee that the rule will "
            "work for new customers.\n"
            "\n"
            "A common overfitting pattern is:\n"
            "\n"
            "```text\n"
            "Training performance -> extremely high\n"
            "Test performance     -> noticeably lower\n"
            "```\n"
            "\n"
            "The model has learned too much about the specific training examples "
            "and not enough about the broader pattern.\n"
            "\n"
            "### Underfitting\n"
            "\n"
            "**Underfitting** happens when the model is too simple to capture "
            "important structure in the data.\n"
            "\n"
            "A common underfitting pattern is:\n"
            "\n"
            "```text\n"
            "Training performance -> poor\n"
            "Test performance     -> poor\n"
            "```\n"
            "\n"
            "If the model cannot even represent the training pattern well, it "
            "usually cannot generalize well either.\n"
            "\n"
            "### The model-complexity trade-off\n"
            "\n"
            "You can imagine model complexity as a spectrum:\n"
            "\n"
            "```text\n"
            "too simple              balanced                too complex\n"
            "    ↓                      ↓                         ↓\n"
            "underfitting       good generalization          overfitting\n"
            "```\n"
            "\n"
            "As complexity increases, training performance can usually improve. "
            "But after some point, additional complexity may make the model "
            "focus too strongly on individual training examples and hurt "
            "generalization.\n"
            "\n"
            "The goal is not to maximize complexity. The goal is to find enough "
            "complexity to learn the real pattern without modeling accidental "
            "details of the training set.\n"
            "\n"
            "### How dataset size changes the picture\n"
            "\n"
            "The amount and variety of training data affect how much complexity "
            "a model can safely use.\n"
            "\n"
            "A rule supported by only a handful of examples is less convincing "
            "than a rule that continues to work across thousands of varied "
            "examples.\n"
            "\n"
            "More diverse data often allows a model to learn more detailed "
            "patterns without overfitting as easily.\n"
            "\n"
            "However, simply copying the same examples does not create new "
            "information. What helps is additional data that adds useful "
            "variation.\n"
            "\n"
            "This leads to an important practical lesson:\n"
            "\n"
            "> More useful, representative data can sometimes improve a machine-"
            "learning system more than repeatedly tuning the model.\n"
            "\n"

            "{{exercise:M02.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Misconceptions
            # ----------------------------------------------------------------

            "## Important misconception\n"
            "\n"
            "### Misconception\n"
            "\n"
            "> A model with 100% training accuracy must be an excellent model.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Training performance only tells us how well the model handles data "
            "it already learned from. A model can memorize training examples and "
            "still fail on unseen data. What we really care about is "
            "generalization performance.\n"
            "\n"
            "A large gap between training performance and test performance is "
            "often a warning sign that the model is overfitting.\n"
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
            "| Supervised learning | Learning from examples where both inputs and correct outputs are known |\n"
            "| Training set | Labeled examples used to fit the model |\n"
            "| Test set | Held-out examples used to evaluate performance on unseen data |\n"
            "| Classification | Predicting a class or category |\n"
            "| Binary classification | Classification with exactly two classes |\n"
            "| Multiclass classification | Classification with more than two classes |\n"
            "| Regression | Predicting a continuous numeric value |\n"
            "| Generalization | Performing well on new data that follows the same kind of pattern as the training data |\n"
            "| Overfitting | Fitting the training data too closely and failing to generalize |\n"
            "| Underfitting | Using a model that is too simple to capture important structure |\n"
            "| Model complexity | How flexible a model is in representing patterns in data |\n"
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
            "1. What information must be available for a supervised-learning training example?\n"
            "2. Why is spam detection classification while house-price prediction is regression?\n"
            "3. What does it mean for a model to generalize?\n"
            "4. What pattern in training and test performance can suggest overfitting?\n"
            "5. Why does adding diverse training data often help reduce overfitting risk?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**The goal of supervised learning is not to memorize the training "
            "set. It is to learn a relationship from labeled examples that "
            "continues to work on new, unseen data.**\n"
        ),

        "estimated_minutes": 60,

        "has_code_examples": True,

        "sections": [
            {
                "id": "supervised-learning",
                "title": "What supervised learning is",
                "order": 1,
            },
            {
                "id": "classification-vs-regression",
                "title": "Classification vs. regression",
                "order": 2,
            },
            {
                "id": "generalization",
                "title": "Generalization: the real goal of learning",
                "order": 3,
            },
            {
                "id": "overfitting-underfitting",
                "title": "Overfitting, underfitting, and model complexity",
                "order": 4,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M02.L01.EX01",

            "title": "Classification or Regression?",

            "lesson_code": "M02.L01",

            "section_id": "classification-vs-regression",

            "placement": "after_section",

            "description": (
                "Practice identifying whether a supervised-learning problem "
                "requires classification or regression."
            ),

            "instructions": (
                "For each scenario, decide whether it is classification or regression.\n"
                "\n"
                "1. Predict whether a bank transaction is fraudulent.\n"
                "2. Predict tomorrow's temperature in degrees Celsius.\n"
                "3. Predict which language a web page is written in.\n"
                "4. Predict the monthly rent of an apartment.\n"
                "5. Predict whether a customer will cancel a subscription.\n"
                "\n"
                "For each answer, explain whether the target is a category or "
                "a continuous numeric value."
            ),

            "expected_output": (
                "A five-row answer identifying each scenario as classification "
                "or regression, with one short justification per row."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "classification-vs-regression",
                "target-type-reasoning",
            ],
        },

        {
            "id": "M02.L01.EX02",

            "title": "Diagnose the Model",

            "lesson_code": "M02.L01",

            "section_id": "overfitting-underfitting",

            "placement": "after_section",

            "description": (
                "Use training and test performance to reason about "
                "underfitting, good generalization, and overfitting."
            ),

            "instructions": (
                "Consider these three models:\n"
                "\n"
                "Model A: training accuracy 62%, test accuracy 60%\n"
                "Model B: training accuracy 91%, test accuracy 89%\n"
                "Model C: training accuracy 100%, test accuracy 68%\n"
                "\n"
                "1. Which model most strongly suggests underfitting?\n"
                "2. Which model shows the best generalization pattern?\n"
                "3. Which model most strongly suggests overfitting?\n"
                "4. Explain your reasoning using the relationship between "
                "training and test performance."
            ),

            "expected_output": (
                "A short diagnosis for Models A, B, and C, with an explanation "
                "based on both training performance and test performance."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "generalization",
                "overfitting",
                "underfitting",
                "model-complexity",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M02.L01.QZ01",

        "title": "Supervised Learning Foundations — Knowledge Check",

        "lesson_code": "M02.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M02.L01.Q01",

                "section_id": "supervised-learning",

                "question": (
                    "What makes a training problem supervised?"
                ),

                "options": [
                    "The data contains only inputs and no expected outputs",
                    "Each training example includes an input and a known target",
                    "The model is always a neural network",
                    "The training data must contain exactly two features",
                ],

                "correct": 1,

                "explanation": (
                    "Supervised learning uses labeled examples: the model sees "
                    "inputs together with the outputs it should learn to predict."
                ),
            },

            {
                "id": "M02.L01.Q02",

                "section_id": "classification-vs-regression",

                "question": (
                    "Which task is a regression problem?"
                ),

                "options": [
                    "Classifying an email as spam or not spam",
                    "Identifying the language of a document",
                    "Predicting a house's selling price",
                    "Classifying a tumor as benign or malignant",
                ],

                "correct": 2,

                "explanation": (
                    "House price is a continuous numeric target. The other "
                    "choices require predicting categories."
                ),
            },

            {
                "id": "M02.L01.Q03",

                "section_id": "generalization",

                "question": (
                    "What does it mean for a model to generalize well?"
                ),

                "options": [
                    "It performs well on new unseen data of the same kind",
                    "It memorizes every training example",
                    "It always reaches 100% training accuracy",
                    "It uses the largest possible number of features",
                ],

                "correct": 0,

                "explanation": (
                    "Generalization is the ability to transfer what was learned "
                    "from the training data to new unseen examples."
                ),
            },

            {
                "id": "M02.L01.Q04",

                "section_id": "overfitting-underfitting",

                "question": (
                    "Which result most strongly suggests overfitting?"
                ),

                "options": [
                    "Training 60%, test 59%",
                    "Training 82%, test 81%",
                    "Training 90%, test 89%",
                    "Training 100%, test 65%",
                ],

                "correct": 3,

                "explanation": (
                    "Very high training performance combined with much lower "
                    "test performance is a classic sign that the model fits the "
                    "training data too closely."
                ),
            },

            {
                "id": "M02.L01.Q05",

                "section_id": "overfitting-underfitting",

                "type": "open",

                "question": (
                    "A model performs poorly on both the training set and the "
                    "test set. Explain what this may indicate, then describe one "
                    "change in model complexity that could be reasonable to try."
                ),
            },
        ],

        "passing_score": 70,
    },
}
