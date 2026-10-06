"""M01.L01 — What Is Machine Learning?.

One Topic -> one Lesson with inline linked exercises + lesson quiz.
BOOK-001, Chapter 1, pages 1–4.
Instructor-authored structured lesson.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M01.L01"
MODULE_ORDER = 1
MODULE_TITLE = "ML Fundamentals & First Model"
MODULE_DESCRIPTION = (
    "Understand what machine learning is, how it differs from hand-written rules, "
    "and how data, features, targets and generalization form the foundation of an ML system."
)

SOURCE_CHAPTER = 1
SOURCE_PAGES = "1–4"


TOPIC = {
    "title": "What Is Machine Learning?",
    "slug": "ml-foundations-m01-l01",
    "description": (
        "Learn what machine learning means, why learning from examples can be more useful "
        "than manually programming every decision rule, and how inputs, outputs and available "
        "evidence define what a model can learn."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 0.75,

    "skill_tags": [
        "machine-learning",
        "foundations",
        "supervised-learning",
        "features",
        "generalization",
        "module-01",
    ],

    "prerequisite_ids": [],

    "lesson": {
        "title": "What Is Machine Learning?",

        "content": (
            "# What Is Machine Learning?\n"
            "\n"
            "> **Course:** Machine Learning Foundations  \n"
            "> **Lesson:** M01.L01  \n"
            "> **Module:** ML Fundamentals & First Model  \n"
            "> **Source alignment:** BOOK-001, Chapter 1, pages 1–4. "
            "This lesson is an instructor-authored curriculum adaptation rather than "
            "a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain machine learning in simple terms.\n"
            "- Distinguish learning from data from manually writing decision rules.\n"
            "- Identify the input and desired output of a prediction problem.\n"
            "- Explain what a **sample**, **feature**, and **target** represent.\n"
            "- Explain why an ML model should work on examples it has not seen before.\n"
            "- Recognize when the available data does not contain enough information "
            "to solve a prediction problem.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. The basic idea\n"
            "\n"
            "Machine learning is a way of extracting useful patterns or knowledge from data.\n"
            "\n"
            "Instead of programming every decision explicitly, we provide examples and allow "
            "an algorithm to discover patterns that can later help it make predictions.\n"
            "\n"
            "A simple mental model is:\n"
            "\n"
            "```text\n"
            "Data + examples\n"
            "      ↓\n"
            "Learning algorithm\n"
            "      ↓\n"
            "Learned model\n"
            "      ↓\n"
            "Prediction on new data\n"
            "```\n"
            "\n"
            "The important idea is that the useful decision pattern is learned from data rather "
            "than being completely written by the programmer beforehand.\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Traditional programming versus machine learning\n"
            "\n"
            "Imagine that we want to create an email spam detector.\n"
            "\n"
            "A rule-based system might start with code such as:\n"
            "\n"
            "```python\n"
            "if 'WIN MONEY' in email:\n"
            "    spam = True\n"
            "\n"
            "if 'FREE OFFER' in email:\n"
            "    spam = True\n"
            "```\n"
            "\n"
            "This may work for some messages, but real language is much more complicated.\n"
            "\n"
            "A spam message might say:\n"
            "\n"
            "```text\n"
            "Congratulations! You have been selected to receive a reward.\n"
            "```\n"
            "\n"
            "Our original rules miss it.\n"
            "\n"
            "We could add a rule for the word `reward`, but then a legitimate email such as:\n"
            "\n"
            "```text\n"
            "Your reward points have been updated.\n"
            "```\n"
            "\n"
            "might be marked incorrectly.\n"
            "\n"
            "As the task becomes more complicated, maintaining hand-written rules becomes "
            "increasingly difficult.\n"
            "\n"
            "Two important weaknesses are:\n"
            "\n"
            "1. Rules designed for one task are often highly specific to that task.\n"
            "2. Humans need to know how to express the decision process as explicit rules.\n"
            "\n"
            "Machine learning changes the approach by learning patterns from examples.\n"
            "\n"
            "For spam detection, we could instead collect examples such as:\n"
            "\n"
            "| Email | Correct answer |\n"
            "|---|---|\n"
            "| Win a prize today | Spam |\n"
            "| Meeting tomorrow at 10 | Not spam |\n"
            "| Claim your reward now | Spam |\n"
            "| Your order has shipped | Not spam |\n"
            "\n"
            "The algorithm can then use these examples to learn useful distinctions.\n"
            "\n"

            "{{exercise:M01.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Generalization: learning instead of memorizing\n"
            "\n"
            "A useful machine learning model should do more than remember the examples it was "
            "trained on.\n"
            "\n"
            "It should also work on **new examples it has never seen before**.\n"
            "\n"
            "This ability is called **generalization**.\n"
            "\n"
            "Imagine learning these examples:\n"
            "\n"
            "```text\n"
            "2 + 2 = 4\n"
            "3 + 3 = 6\n"
            "4 + 4 = 8\n"
            "```\n"
            "\n"
            "Then you are asked:\n"
            "\n"
            "```text\n"
            "10 + 10 = ?\n"
            "```\n"
            "\n"
            "If you learned the underlying pattern, you can answer correctly even though that "
            "exact example was never shown before.\n"
            "\n"
            "Machine learning aims for the same general principle: learn useful patterns that "
            "remain useful for unseen data.\n"
            "\n"
            "> **Key idea:** Memorizing known examples is not the same as learning a pattern "
            "that generalizes.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Inputs and outputs\n"
            "\n"
            "Many supervised machine learning problems can be described as learning a relationship "
            "between an input and a desired output.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Input → Model → Output\n"
            "```\n"
            "\n"
            "You will often see this written as:\n"
            "\n"
            "```text\n"
            "X → y\n"
            "```\n"
            "\n"
            "For spam detection:\n"
            "\n"
            "```text\n"
            "X = information about the email\n"
            "y = spam or not spam\n"
            "```\n"
            "\n"
            "For handwritten digit recognition:\n"
            "\n"
            "```text\n"
            "X = image of a handwritten digit\n"
            "y = actual digit\n"
            "```\n"
            "\n"
            "For credit-card fraud detection:\n"
            "\n"
            "```text\n"
            "X = transaction information\n"
            "y = fraudulent or legitimate\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Samples, features and targets\n"
            "\n"
            "Machine learning data is often easiest to understand as a table.\n"
            "\n"
            "Consider this dataset:\n"
            "\n"
            "| Customer | Age | Monthly spending | Purchases |\n"
            "|---|---:|---:|---:|\n"
            "| Ahmed | 24 | 1500 | 5 |\n"
            "| Sara | 31 | 3200 | 13 |\n"
            "| Omar | 45 | 4600 | 21 |\n"
            "\n"
            "Each row represents one entity we want to reason about.\n"
            "\n"
            "One row is called a **sample** or **data point**.\n"
            "\n"
            "The properties describing the sample are called **features**.\n"
            "\n"
            "So in this example:\n"
            "\n"
            "```text\n"
            "Sample:\n"
            "one customer\n"
            "\n"
            "Features:\n"
            "age\n"
            "monthly spending\n"
            "number of purchases\n"
            "```\n"
            "\n"
            "If we were predicting whether the customer will buy a product, that desired output "
            "would be the **target**.\n"
            "\n"
            "Suppose the dataset contains 10,000 customers and 12 features per customer.\n"
            "\n"
            "Then the input table has:\n"
            "\n"
            "```text\n"
            "10,000 rows × 12 columns\n"
            "```\n"
            "\n"
            "or:\n"
            "\n"
            "```text\n"
            "X.shape = (10000, 12)\n"
            "```\n"
            "\n"

            "{{exercise:M01.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 6. The model can only learn from available information\n"
            "\n"
            "A machine learning algorithm cannot magically recover information that is absent "
            "from its input data.\n"
            "\n"
            "Imagine trying to make an important prediction about a patient when the only feature "
            "you provide is the patient's last name.\n"
            "\n"
            "If the information needed for the prediction is not represented in that feature, "
            "changing to a more complicated model does not solve the fundamental problem.\n"
            "\n"
            "This gives us an important principle:\n"
            "\n"
            "> **A more powerful algorithm cannot compensate for missing evidence in the data.**\n"
            "\n"
            "Before choosing an algorithm, ask whether your features contain useful information "
            "for the target you want to predict.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Understand the task before choosing the model\n"
            "\n"
            "A common beginner mistake is to begin with:\n"
            "\n"
            "```text\n"
            "Which machine learning algorithm should I use?\n"
            "```\n"
            "\n"
            "A better starting point is to understand the problem and the data.\n"
            "\n"
            "Ask questions such as:\n"
            "\n"
            "- What question am I trying to answer?\n"
            "- Can my data answer that question?\n"
            "- Do I have enough representative data?\n"
            "- Which features are available?\n"
            "- Will those features support the desired prediction?\n"
            "- How will success be measured?\n"
            "- How will the prediction be used in the real application?\n"
            "\n"
            "A useful workflow is:\n"
            "\n"
            "```text\n"
            "Problem\n"
            "   ↓\n"
            "Understand the data\n"
            "   ↓\n"
            "Define the ML task\n"
            "   ↓\n"
            "Identify samples, features and target\n"
            "   ↓\n"
            "Define evaluation\n"
            "   ↓\n"
            "Choose a model\n"
            "   ↓\n"
            "Train and evaluate\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Worked scenario\n"
            "\n"
            "Suppose we want to predict whether a student will pass a course.\n"
            "\n"
            "| Study hours | Attendance | Previous score | Result |\n"
            "|---:|---:|---:|---|\n"
            "| 8 | 95 | 90 | Pass |\n"
            "| 1 | 40 | 35 | Fail |\n"
            "| 6 | 90 | 80 | Pass |\n"
            "| 2 | 55 | 42 | Fail |\n"
            "\n"
            "### Samples\n"
            "\n"
            "Each student is one sample.\n"
            "\n"
            "### Features\n"
            "\n"
            "```text\n"
            "Study hours\n"
            "Attendance\n"
            "Previous score\n"
            "```\n"
            "\n"
            "### Target\n"
            "\n"
            "```text\n"
            "Pass / Fail\n"
            "```\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "X = study hours + attendance + previous score\n"
            "y = pass or fail\n"
            "```\n"
            "\n"
            "The model could learn from previously observed students and later make a prediction "
            "for a new student.\n"
            "\n"
            "But we should still ask whether the selected features contain useful evidence and "
            "how the model's performance will eventually be evaluated.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconception\n"
            "\n"
            "### Misconception\n"
            "\n"
            "> If I use a sufficiently advanced algorithm, it can solve almost any prediction "
            "problem.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "An algorithm only has access to the information represented in its input data.\n"
            "\n"
            "If useful evidence is missing, increasing model complexity does not automatically "
            "create that evidence.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Machine learning | Learning useful patterns from data |\n"
            "| Sample | One example or one row |\n"
            "| Feature | A property describing a sample |\n"
            "| Target | The output we want to predict |\n"
            "| Model | The learned system used to produce predictions |\n"
            "| Generalization | Performing well on unseen examples |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Make sure you can answer these before continuing:\n"
            "\n"
            "1. What is the difference between hand-written rules and machine learning?\n"
            "2. What is a sample?\n"
            "3. What is a feature?\n"
            "4. What is a target?\n"
            "5. What does generalization mean?\n"
            "6. Why can a powerful algorithm still fail when important information is missing?\n"
            "\n"
            "---\n"
            "\n"

            "**Retain this idea:** Machine learning learns useful patterns from examples so "
            "that a model can make predictions on new data. The quality of the result depends "
            "not only on the algorithm but also on whether the available data contains useful "
            "information for the problem.\n"
        ),

        "estimated_minutes": 45,
        "has_code_examples": True,

        # Defines the intended order of sections for navigation,
        # analytics, exercise placement and future lesson rendering.
        "sections": [
            {
                "id": "what-is-machine-learning",
                "title": "The basic idea",
                "order": 1,
            },
            {
                "id": "rules-vs-machine-learning",
                "title": "Traditional programming versus machine learning",
                "order": 2,
            },
            {
                "id": "generalization",
                "title": "Generalization",
                "order": 3,
            },
            {
                "id": "inputs-and-outputs",
                "title": "Inputs and outputs",
                "order": 4,
            },
            {
                "id": "samples-features-targets",
                "title": "Samples, features and targets",
                "order": 5,
            },
            {
                "id": "feature-boundary",
                "title": "The model can only learn from available information",
                "order": 6,
            },
            {
                "id": "problem-framing",
                "title": "Understand the task before choosing the model",
                "order": 7,
            },
            {
                "id": "worked-scenario",
                "title": "Worked scenario",
                "order": 8,
            },
        ],
    },

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Rules or Machine Learning?",

            # Explicit relationship to lesson content.
            "lesson_code": "M01.L01",
            "section_id": "rules-vs-machine-learning",
            "placement": "after_section",

            "description": (
                "Design a simple rule-based spam detector, identify where those rules could fail, "
                "and explain why learning from labeled examples may handle a more varied set of "
                "messages."
            ),

            "instructions": (
                "1. Write three hand-crafted rules that could identify spam email.\n"
                "2. For each rule, write one legitimate email that could accidentally trigger it.\n"
                "3. Explain one limitation of maintaining a large collection of fixed rules.\n"
                "4. Explain how labeled examples could instead be used to train a machine "
                "learning system.\n"
                "5. Write 2–3 sentences comparing the two approaches."
            ),

            "expected_output": (
                "A short written comparison containing three spam rules, three failure examples, "
                "and an explanation of why learning from examples may generalize beyond fixed rules."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "machine-learning",
                "rule-based-systems",
                "reasoning",
                "generalization",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Frame a Machine Learning Problem",

            "lesson_code": "M01.L01",
            "section_id": "samples-features-targets",
            "placement": "after_section",

            "description": (
                "Choose a real prediction problem and identify its sample, features, target and "
                "intended user."
            ),

            "instructions": (
                "Choose one problem such as fraud detection, spam detection, customer churn, "
                "house-price prediction or image classification.\n\n"
                "Write:\n"
                "1. The prediction problem.\n"
                "2. What one sample represents.\n"
                "3. At least three possible features.\n"
                "4. The target to predict.\n"
                "5. Who will use the prediction.\n"
                "6. Whether the features contain enough useful evidence for the target.\n"
                "7. One important piece of information that may be missing."
            ),

            "expected_output": (
                "A structured ML problem definition containing the sample, features, target, "
                "intended user and a short evidence-quality assessment."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "problem-framing",
                "samples",
                "features",
                "targets",
                "evaluation-reasoning",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "What Is Machine Learning? — Knowledge Check",

        "lesson_code": "M01.L01",

        # Quiz is shown only after all lesson sections and inline exercises.
        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",
                "section_id": "what-is-machine-learning",

                "question": (
                    "Which statement best describes the central idea of machine learning?"
                ),

                "options": [
                    "A programmer manually writes every decision the system can make.",
                    "A model learns useful patterns from examples and uses them for predictions.",
                    "Machine learning means memorizing every training example.",
                    "Machine learning works without input data.",
                ],

                "correct": 1,

                "explanation": (
                    "Machine learning uses data and examples to learn useful patterns rather than "
                    "depending entirely on hand-written decision rules."
                ),
            },

            {
                "id": "M01.L01.Q02",
                "section_id": "rules-vs-machine-learning",

                "question": (
                    "Why can a large collection of hand-written decision rules become difficult "
                    "to maintain?"
                ),

                "options": [
                    "Rules cannot contain text.",
                    "Every ML problem must use images.",
                    "Real-world cases vary and task-specific rules may require many exceptions.",
                    "Rules always produce random outputs.",
                ],

                "correct": 2,

                "explanation": (
                    "Real-world decisions can contain many variations and exceptions, making "
                    "large task-specific rule systems difficult to design and maintain."
                ),
            },

            {
                "id": "M01.L01.Q03",
                "section_id": "generalization",

                "question": "What does generalization mean in machine learning?",

                "options": [
                    "The model remembers every training sample.",
                    "The model performs well on new examples it did not see during training.",
                    "The model uses every available feature.",
                    "The model always achieves perfect training accuracy.",
                ],

                "correct": 1,

                "explanation": (
                    "Generalization is the ability to apply learned patterns successfully to "
                    "previously unseen examples."
                ),
            },

            {
                "id": "M01.L01.Q04",
                "section_id": "samples-features-targets",

                "question": (
                    "A dataset contains 10,000 customers and 12 features for each customer. "
                    "What is the expected shape of X?"
                ),

                "options": [
                    "(12, 10000)",
                    "(10000, 12)",
                    "(10000,)",
                    "(12,)",
                ],

                "correct": 1,

                "explanation": (
                    "Rows represent samples and columns represent features, so the dataset "
                    "contains 10,000 rows and 12 feature columns."
                ),
            },

            {
                "id": "M01.L01.Q05",
                "section_id": "feature-boundary",

                "question": (
                    "Why might a very powerful algorithm still fail to predict a target?"
                ),

                "options": [
                    "Machine learning cannot use numbers.",
                    "The information needed for the prediction may not be present in the features.",
                    "Advanced models can only work with images.",
                    "Targets cannot contain categories.",
                ],

                "correct": 1,

                "explanation": (
                    "A model can only use the information represented in its inputs. Greater "
                    "algorithmic complexity does not automatically create missing evidence."
                ),
            },

            {
                "id": "M01.L01.Q06",
                "section_id": "problem-framing",
                "type": "open",

                "question": (
                    "Describe one prediction problem. Identify the sample, features, target and "
                    "intended user, then explain whether the available features contain useful "
                    "information for the prediction."
                ),
            },
        ],

        "passing_score": 70,
    },
}