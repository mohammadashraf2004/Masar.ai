"""M01.L04 — Why Deep Learning Matters and the Rise of Generative AI.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 1, pages not provided in the supplied extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = 'M01.L04'

MODULE_ORDER = 1

MODULE_TITLE = "Deep Learning Foundations"

MODULE_DESCRIPTION = (
    "Build the conceptual foundation for artificial intelligence, machine learning, "
    "deep learning, learned representations, neural-network training, and modern "
    "generative AI."
)

SOURCE_CHAPTER = 1

SOURCE_PAGES = "Not provided in supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": 'Why Deep Learning Matters and the Rise of Generative AI',

    "slug": 'deep-learning-foundations-m01-l04',

    "description": "Understand feature learning, scalability, reusability, foundation models, self-supervised learning, and the chapter's warning about AI hype.",

    "order": 4,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 0.9,

    "skill_tags": [
        'feature-engineering',
        'foundation-models',
        'self-supervised-learning',
        'generative-ai',
    ],

    "prerequisite_ids": ['M01.L03'],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": 'Why Deep Learning Matters and the Rise of Generative AI',

        "content": (
            '# Why Deep Learning Matters and the Rise of Generative AI\n'
            '\n'
            '> **Course:** Deep Learning Foundations  \n'
            '> **Lesson:** M01.L04  \n'
            '> **Module:** Deep Learning Foundations  \n'
            '> **Source alignment:** BOOK-002, Chapter 1. The supplied extract does not include page numbers. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n'
            '\n'
            '---\n'
            '\n'
            '## Learning outcomes\n'
            '\n'
            'By the end of this lesson, you should be able to:\n'
            '\n'
            '- Explain why deep learning reduced dependence on manual feature engineering.\n'
            "- Describe the chapter's three major strengths of deep learning: simplicity, scalability, and reusability.\n"
            '- Explain foundation models and self-supervised learning at a high level.\n'
            '- Separate demonstrated AI capabilities from speculative short-term claims.\n'
            '\n'
            '---\n'
            '\n'
            '## 1. What makes deep learning different\n'
            '\n'
            'Earlier machine-learning workflows often depended heavily on **feature engineering**.\n'
            '\n'
            'Feature engineering means manually designing useful representations of raw data before a model can solve the task.\n'
            '\n'
            'For handwritten digits, a developer might invent features such as:\n'
            '\n'
            '- number of loops,\n'
            '- horizontal pixel patterns,\n'
            '- vertical pixel patterns.\n'
            '\n'
            'For a simple problem, this can work well.\n'
            '\n'
            'But for complex perception problems, feature engineering becomes difficult and brittle.\n'
            '\n'
            'Deep learning changes the workflow by learning multiple levels of features automatically from the training data.\n'
            '\n'
            'A simplified comparison is:\n'
            '\n'
            '```text\n'
            'Traditional workflow\n'
            'Raw data -> hand-designed features -> learning algorithm -> output\n'
            '\n'
            'Deep-learning workflow\n'
            'Raw data -> learned layered representations -> output\n'
            '```\n'
            '\n'
            'This does not mean humans disappear from the workflow. Humans still design datasets, model architectures, objectives, evaluation procedures, and deployment systems. The important change is that many task-specific internal representations are learned automatically.\n'
            '\n'
            '---\n'
            '\n'
            '## 2. Three strengths: simplicity, scalability, and reusability\n'
            '\n'
            "The chapter groups deep learning's major advantages into three categories.\n"
            '\n'
            '### Simplicity\n'
            '\n'
            'Deep learning can replace complicated pipelines of hand-designed feature transformations with an end-to-end learned model.\n'
            '\n'
            'This reduces the amount of manual feature engineering needed for many difficult tasks.\n'
            '\n'
            '### Scalability\n'
            '\n'
            'Deep-learning training can take advantage of GPUs and other specialized hardware.\n'
            '\n'
            'Models are commonly trained using small batches of data, which allows learning procedures to work with very large datasets as computational resources grow.\n'
            '\n'
            '### Versatility and reusability\n'
            '\n'
            'A trained deep-learning model can often be adapted or continued with additional data instead of rebuilding everything from zero.\n'
            '\n'
            'A learned model may also be reused for a new task.\n'
            '\n'
            'This idea leads directly to **foundation models**.\n'
            '\n'
            '{{exercise:M01.L04.EX01}}\n'
            '\n'
            '---\n'
            '\n'
            '## 3. Foundation models and self-supervised learning\n'
            '\n'
            'A **foundation model** is a large model trained broadly enough that it can support many downstream tasks.\n'
            '\n'
            'A simple mental model is:\n'
            '\n'
            '```text\n'
            'Large pretrained model\n'
            '      /      |      \\\n'
            '   Task A  Task B  Task C\n'
            '```\n'
            '\n'
            'Instead of collecting a fully labeled dataset for every possible task, a large model first learns general-purpose representations from enormous amounts of data.\n'
            '\n'
            'One important method that enables this scale is **self-supervised learning**.\n'
            '\n'
            'In ordinary supervised learning, humans may provide labels:\n'
            '\n'
            '```text\n'
            'image -> "cat"\n'
            'image -> "dog"\n'
            '```\n'
            '\n'
            'In self-supervised learning, the training target can be derived from the input data itself.\n'
            '\n'
            'For language, an intuitive example is predicting a missing or next piece of text:\n'
            '\n'
            '```text\n'
            '"Machine learning can learn from ____"\n'
            '```\n'
            '\n'
            'The text itself supplies the learning signal.\n'
            '\n'
            'For images, a model can be trained to reconstruct information from a corrupted or transformed version of an image.\n'
            '\n'
            'Because targets can be generated from the data itself, self-supervised learning can use large collections of unlabeled text or images.\n'
            '\n'
            'This is one of the central ideas behind the modern wave of generative AI described in the chapter.\n'
            '\n'
            '---\n'
            '\n'
            '## 4. Capabilities, hype, and the long-term view\n'
            '\n'
            'The chapter describes major progress in areas such as:\n'
            '\n'
            '- image classification,\n'
            '- speech transcription,\n'
            '- machine translation,\n'
            '- recommendation systems,\n'
            '- game playing,\n'
            '- generative text and images,\n'
            '- programming assistance.\n'
            '\n'
            'It also warns readers not to confuse rapid practical progress with every dramatic prediction made about AI.\n'
            '\n'
            'The chapter reviews earlier periods in AI history when very high expectations were followed by disappointment and reduced investment, often called **AI winters**.\n'
            '\n'
            'The lesson for a practitioner is not "AI is unimportant." It is almost the opposite:\n'
            '\n'
            '> Evaluate systems by demonstrated capabilities, evidence, and clear limitations instead of assuming that every near-term prediction will come true.\n'
            '\n'
            'The chapter also distinguishes useful cognitive automation from broader claims about fully autonomous human-like intelligence.\n'
            '\n'
            'For learning purposes, the important habit is disciplined evaluation:\n'
            '\n'
            '```text\n'
            'What can the system actually do?\n'
            'On what kind of data?\n'
            'Under what conditions?\n'
            'How is performance measured?\n'
            'Where does it fail?\n'
            '```\n'
            '\n'
            'This habit will matter throughout machine learning engineering.\n'
            '\n'
            '{{exercise:M01.L04.EX02}}\n'
            '\n'
            '---\n'
            '\n'
            '## Important misconception\n'
            '\n'
            '### Misconception\n'
            '\n'
            '> "Because modern generative AI is impressive, every prediction about near-term general intelligence must also be correct."\n'
            '\n'
            '### Why this is wrong\n'
            '\n'
            'Demonstrated capabilities and predictions about future systems are different kinds of claims. The chapter encourages skepticism toward short-term hype while still emphasizing the long-term usefulness and broad impact of deep learning.\n'
            '\n'
            '---\n'
            '\n'
            '## Key terminology\n'
            '\n'
            '| Term | Meaning |\n'
            '|---|---|\n'
            '| Feature engineering | Manually designing useful input representations for a model |\n'
            '| Scalability | The ability to benefit from more data and computational resources |\n'
            '| Reusability | The ability to adapt learned models or representations to additional tasks |\n'
            '| Foundation model | A broadly pretrained model that can support many downstream tasks |\n'
            '| Self-supervised learning | Learning in which training targets are derived from the input data itself |\n'
            '| Generative AI | Models that generate new text, images, or other content from learned patterns |\n'
            '| AI winter | A historical period of reduced interest and funding after inflated expectations were not met |\n'
            '\n'
            '---\n'
            '\n'
            '## Self-check\n'
            '\n'
            'Before continuing, make sure you can answer:\n'
            '\n'
            '1. What problem does automatic representation learning reduce?\n'
            '2. Why is scalability important for deep learning?\n'
            '3. How does self-supervised learning reduce dependence on manual labels?\n'
            "4. What practical lesson should an ML engineer take from the chapter's discussion of hype?\n"
            '\n'
            '---\n'
            '\n'
            '## Retain this idea\n'
            '\n'
            '**Deep learning became powerful because it learns reusable representations at scale, but strong engineering requires separating demonstrated capability from speculation.**\n'
        ),

        "estimated_minutes": 55,

        "has_code_examples": False,

        "sections": [
            {
                "id": 'what-makes-deep-learning-different',
                "title": 'What makes deep learning different',
                "order": 1,
            },
            {
                "id": 'three-strengths',
                "title": 'Three strengths: simplicity, scalability, and reusability',
                "order": 2,
            },
            {
                "id": 'foundation-models-and-self-supervision',
                "title": 'Foundation models and self-supervised learning',
                "order": 3,
            },
            {
                "id": 'capabilities-hype-and-long-term-view',
                "title": 'Capabilities, hype, and the long-term view',
                "order": 4,
            }
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": 'M01.L04.EX01',
            "title": 'Feature Engineering vs Learned Features',
            "lesson_code": 'M01.L04',
            "section_id": 'three-strengths',
            "placement": "after_section",
            "description": 'Compare a hand-designed ML pipeline with a deep-learning workflow.',
            "instructions": '1. Choose a task such as handwritten-digit recognition.\n2. List two features a human might design manually.\n3. Explain how deep learning changes who discovers useful internal representations.\n4. Connect the example to one of the three strengths: simplicity, scalability, or reusability.',
            "expected_output": 'A short comparison containing two manual features, the deep-learning alternative, and one linked advantage.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'feature-engineering',
                'deep-learning-workflows',
            ],
        },

        {
            "id": 'M01.L04.EX02',
            "title": 'Separate Capability from Prediction',
            "lesson_code": 'M01.L04',
            "section_id": 'capabilities-hype-and-long-term-view',
            "placement": "after_section",
            "description": 'Practice evaluating AI claims with evidence-focused questions.',
            "instructions": '1. Write one example of a demonstrated capability mentioned in the lesson.\n2. Write one example of a broad future claim that would require additional evidence.\n3. List three questions you would ask before accepting the future claim.\n4. Explain why skepticism can coexist with optimism about long-term AI usefulness.',
            "expected_output": 'A capability/claim comparison followed by three evaluation questions and a short explanation.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'evidence-evaluation',
                'ai-hype-literacy',
            ],
        }
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": 'M01.L04.QZ01',

        "title": 'Why Deep Learning Matters and the Rise of Generative AI — Knowledge Check',

        "lesson_code": 'M01.L04',

        "placement": "lesson_end",

        "questions": [
            {
                "id": 'M01.L04.Q01',
                "section_id": 'what-makes-deep-learning-different',
                "question": 'What is feature engineering?',
                "options": [
                    'Manually designing useful representations or features for a learning system',
                    'Only buying faster hardware',
                    'Generating random labels',
                    'Measuring network depth',
                ],
                "correct": 0,
                "explanation": 'Feature engineering is the manual design of representations that make a problem easier for the learning algorithm.',
            },

            {
                "id": 'M01.L04.Q02',
                "section_id": 'three-strengths',
                "question": 'Which set matches the three broad strengths emphasized in the chapter?',
                "options": [
                    'Secrecy, randomness, and compression',
                    'Simplicity, scalability, and versatility/reusability',
                    'Only speed, only accuracy, and only cost',
                    'Symbolic rules, manual features, and no retraining',
                ],
                "correct": 1,
                "explanation": "The chapter organizes deep learning's strengths around simplicity, scalability, and versatility/reusability.",
            },

            {
                "id": 'M01.L04.Q03',
                "section_id": 'foundation-models-and-self-supervision',
                "question": 'What is a key advantage of self-supervised learning?',
                "options": [
                    'It requires every example to be manually labeled',
                    'It prevents model reuse',
                    'It can derive training targets from the input data itself',
                    'It removes the need for data',
                ],
                "correct": 2,
                "explanation": 'Self-supervision creates learning signals from the input data, enabling training on large quantities of unlabeled data.',
            },

            {
                "id": 'M01.L04.Q04',
                "section_id": 'capabilities-hype-and-long-term-view',
                "question": 'What practical attitude does the chapter encourage toward dramatic AI predictions?',
                "options": [
                    'Accept all predictions because current models are impressive',
                    'Reject all AI progress as hype',
                    'Ignore measured capabilities',
                    'Judge claims using demonstrated evidence, conditions, and limitations',
                ],
                "correct": 3,
                "explanation": 'The chapter argues for distinguishing real capabilities from speculative short-term claims and evaluating evidence carefully.',
            },

            {
                "id": 'M01.L04.Q05',
                "section_id": 'capabilities-hype-and-long-term-view',
                "type": "open",
                "question": 'Explain how foundation models, self-supervised learning, and model reuse are connected, using a concrete example of a model being adapted to more than one task.',
            }
        ],

        "passing_score": 70,
    },
}
