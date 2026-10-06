"""M01.L02 — Learning Rules and Representations from Data.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 1, pages not provided in the supplied extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = 'M01.L02'

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
    "title": 'Learning Rules and Representations from Data',

    "slug": 'deep-learning-foundations-m01-l02',

    "description": 'Learn the three ingredients of machine learning and why useful data representations can turn difficult tasks into simpler ones.',

    "order": 2,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 0.85,

    "skill_tags": [
        'representations',
        'targets',
        'feedback',
        'hypothesis-space',
        'module-01',
    ],

    "prerequisite_ids": ['M01.L01'],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": 'Learning Rules and Representations from Data',

        "content": (
            '# Learning Rules and Representations from Data\n'
            '\n'
            '> **Course:** Deep Learning Foundations  \n'
            '> **Lesson:** M01.L02  \n'
            '> **Module:** Deep Learning Foundations  \n'
            '> **Source alignment:** BOOK-002, Chapter 1. The supplied extract does not include page numbers. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n'
            '\n'
            '---\n'
            '\n'
            '## Learning outcomes\n'
            '\n'
            'By the end of this lesson, you should be able to:\n'
            '\n'
            '- Identify the three ingredients needed for learning from examples.\n'
            '- Explain what a data representation is.\n'
            '- Describe why a better representation can make a task easier.\n'
            '- Explain learning as a search for useful transformations guided by feedback.\n'
            '\n'
            '---\n'
            '\n'
            '## 1. Three ingredients for learning\n'
            '\n'
            'A machine-learning system needs more than raw data. The chapter highlights three ingredients.\n'
            '\n'
            '### 1. Input data points\n'
            '\n'
            'These are the examples the model receives.\n'
            '\n'
            'Examples:\n'
            '\n'
            '```text\n'
            'Speech recognition -> audio files\n'
            'Image tagging      -> images\n'
            'Point classification -> (x, y) coordinates\n'
            '```\n'
            '\n'
            '### 2. Expected outputs\n'
            '\n'
            'These are the answers associated with the examples.\n'
            '\n'
            'Examples:\n'
            '\n'
            '```text\n'
            'Audio file -> transcript\n'
            'Image      -> "dog"\n'
            'Point      -> "black"\n'
            '```\n'
            '\n'
            '### 3. A way to measure performance\n'
            '\n'
            'The model needs feedback about how well it is doing. A useful measurement tells us how far the current output is from the desired output.\n'
            '\n'
            'Without feedback, the system has no direction for improvement.\n'
            '\n'
            'A compact mental model is:\n'
            '\n'
            '```text\n'
            'Input + Expected output + Feedback\n'
            '                 ↓\n'
            '              Learning\n'
            '```\n'
            '\n'
            'This feedback is what makes adjustment possible.\n'
            '\n'
            '---\n'
            '\n'
            '## 2. Representations change the view of data\n'
            '\n'
            'A **representation** is a way of encoding or expressing data.\n'
            '\n'
            'The same information can have multiple representations.\n'
            '\n'
            'For example, a color image can be represented using RGB values or HSV values. The underlying image is the same, but the numerical description changes.\n'
            '\n'
            'Why does this matter?\n'
            '\n'
            'Because some tasks become easier in one representation than another.\n'
            '\n'
            'A useful representation exposes the structure needed for the task.\n'
            '\n'
            'Imagine trying to organize books. If every book is described only by physical weight, finding science-fiction books is difficult. If the representation includes genre, the same sorting task becomes easy.\n'
            '\n'
            'The information has not magically changed. The **representation** has become more useful for the goal.\n'
            '\n'
            '### Machine learning perspective\n'
            '\n'
            'A machine-learning model transforms input data into representations that make the desired output easier to produce.\n'
            '\n'
            'That is why learning representations is central to both machine learning and deep learning.\n'
            '\n'
            '{{exercise:M01.L02.EX01}}\n'
            '\n'
            '---\n'
            '\n'
            '## 3. Worked example: separating points\n'
            '\n'
            'Suppose we have points described by coordinates:\n'
            '\n'
            '```text\n'
            '(x, y)\n'
            '```\n'
            '\n'
            'Some points are black and some are white.\n'
            '\n'
            'Our task is:\n'
            '\n'
            "> Given a point's coordinates, predict whether it belongs to the black class or the white class.\n"
            '\n'
            'The pieces of the learning problem are:\n'
            '\n'
            '```text\n'
            'Input            -> (x, y)\n'
            'Expected output  -> black or white\n'
            'Performance      -> percentage classified correctly\n'
            '```\n'
            '\n'
            'Now suppose the points are awkwardly arranged in the original coordinate system. A simple rule cannot separate them.\n'
            '\n'
            'We transform the coordinates.\n'
            '\n'
            'After the transformation, imagine the points look like this:\n'
            '\n'
            '```text\n'
            'white points | black points\n'
            'white points | black points\n'
            'white points | black points\n'
            '             |\n'
            '            x=0\n'
            '```\n'
            '\n'
            'Now the classification rule is easy:\n'
            '\n'
            '```text\n'
            'if x > 0 -> black\n'
            'if x < 0 -> white\n'
            '```\n'
            '\n'
            'The important achievement was not a complicated final rule. It was finding a **representation** in which the rule became simple.\n'
            '\n'
            'This is a central intuition for machine learning:\n'
            '\n'
            '> Hard problem in one representation -> easy problem in a better representation.\n'
            '\n'
            '---\n'
            '\n'
            '## 4. Learning as a guided search\n'
            '\n'
            'In the coordinate example, a human could invent a useful transformation by hand.\n'
            '\n'
            'But real problems are much more complicated.\n'
            '\n'
            'Consider handwritten digits. You might manually design features such as:\n'
            '\n'
            '- number of closed loops,\n'
            '- vertical and horizontal pixel histograms,\n'
            '- edge patterns.\n'
            '\n'
            'These hand-designed features may work for some examples, but creating and maintaining them is difficult.\n'
            '\n'
            'Machine learning tries to automate this process.\n'
            '\n'
            'A learning algorithm searches through a predefined set of possible transformations or rules. This set of possibilities is called a **hypothesis space**.\n'
            '\n'
            'The search is guided by feedback:\n'
            '\n'
            '```text\n'
            'Try a candidate transformation/rule\n'
            '              ↓\n'
            'Measure performance\n'
            '              ↓\n'
            'Keep moving toward better solutions\n'
            '```\n'
            '\n'
            'The algorithm is not searching through every imaginable mathematical idea. It searches through the types of operations allowed by its model.\n'
            '\n'
            'That makes the hypothesis space important: it defines what kinds of solutions the learner is capable of finding.\n'
            '\n'
            '{{exercise:M01.L02.EX02}}\n'
            '\n'
            '---\n'
            '\n'
            '## Important misconception\n'
            '\n'
            '### Misconception\n'
            '\n'
            '> "Machine learning is mainly about memorizing the correct labels."\n'
            '\n'
            '### Why this is wrong\n'
            '\n'
            'The deeper goal is to discover useful structure that transforms inputs into outputs. A model must learn representations or rules that work beyond the individual training examples. The chapter emphasizes meaningful data transformation, not simple storage of answers.\n'
            '\n'
            '---\n'
            '\n'
            '## Key terminology\n'
            '\n'
            '| Term | Meaning |\n'
            '|---|---|\n'
            '| Input | The data presented to a model |\n'
            '| Target / expected output | The desired answer associated with an input |\n'
            '| Feedback signal | A measurement used to judge and improve the model |\n'
            '| Representation | A way of encoding or expressing data |\n'
            '| Transformation | An operation that converts one representation into another |\n'
            '| Hypothesis space | The predefined set of candidate operations or solutions a learning algorithm can search |\n'
            '\n'
            '---\n'
            '\n'
            '## Self-check\n'
            '\n'
            'Before continuing, make sure you can answer:\n'
            '\n'
            '1. What three ingredients are required for learning from examples?\n'
            '2. Why can two representations of the same data lead to different task difficulty?\n'
            '3. In the point-classification example, what made the final rule simple?\n'
            '4. What does a hypothesis space control?\n'
            '\n'
            '---\n'
            '\n'
            '## Retain this idea\n'
            '\n'
            '**Machine learning searches for useful representations and rules, using feedback to move toward transformations that make the task easier.**\n'
        ),

        "estimated_minutes": 50,

        "has_code_examples": False,

        "sections": [
            {
                "id": 'three-ingredients-for-learning',
                "title": 'Three ingredients for learning',
                "order": 1,
            },
            {
                "id": 'representations-change-the-view',
                "title": 'Representations change the view of data',
                "order": 2,
            },
            {
                "id": 'coordinate-change-example',
                "title": 'Worked example: separating points',
                "order": 3,
            },
            {
                "id": 'learning-as-search',
                "title": 'Learning as a guided search',
                "order": 4,
            }
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": 'M01.L02.EX01',
            "title": 'Identify Inputs, Targets, and Feedback',
            "lesson_code": 'M01.L02',
            "section_id": 'representations-change-the-view',
            "placement": "after_section",
            "description": 'Practice decomposing learning tasks into the three ingredients described in the chapter.',
            "instructions": '1. For speech recognition, identify the input and expected output.\n2. For image tagging, identify the input and expected output.\n3. Propose one simple performance measure for each task.\n4. Explain why feedback is necessary for learning.',
            "expected_output": 'A two-row table containing input, expected output, and performance measure, followed by a short explanation.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'problem-formulation',
                'feedback-signals',
            ],
        },

        {
            "id": 'M01.L02.EX02',
            "title": 'Representation Before Rule',
            "lesson_code": 'M01.L02',
            "section_id": 'learning-as-search',
            "placement": "after_section",
            "description": 'Reason about how changing a representation can simplify classification.',
            "instructions": '1. Imagine two classes of 2D points that overlap awkwardly in the original axes.\n2. Explain why repeatedly adding complicated rules may be less attractive than finding a better representation.\n3. Describe what the learning algorithm would evaluate while searching candidate transformations.\n4. In one sentence, explain what the hypothesis space limits.',
            "expected_output": 'A short written analysis connecting representation quality, feedback, and hypothesis space.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'representation-reasoning',
                'hypothesis-space',
            ],
        }
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": 'M01.L02.QZ01',

        "title": 'Learning Rules and Representations from Data — Knowledge Check',

        "lesson_code": 'M01.L02',

        "placement": "lesson_end",

        "questions": [
            {
                "id": 'M01.L02.Q01',
                "section_id": 'three-ingredients-for-learning',
                "question": 'Which item is NOT one of the three ingredients highlighted for machine learning?',
                "options": [
                    'Input data points',
                    'Expected outputs',
                    'A way to measure performance',
                    'A guarantee that the first prediction is correct',
                ],
                "correct": 3,
                "explanation": 'Learning requires examples, expected outputs, and feedback. Initial predictions can be poor; improvement happens through learning.',
            },

            {
                "id": 'M01.L02.Q02',
                "section_id": 'representations-change-the-view',
                "question": 'What is a representation?',
                "options": [
                    'Only the final prediction',
                    'A way of encoding or expressing data',
                    'A hardware accelerator',
                    'A manually written label only',
                ],
                "correct": 1,
                "explanation": 'A representation is a particular way of expressing the same underlying information.',
            },

            {
                "id": 'M01.L02.Q03',
                "section_id": 'coordinate-change-example',
                "question": 'What is the main lesson of the coordinate-change example?',
                "options": [
                    'A useful transformation can make a difficult classification rule simple',
                    'Coordinates are always better than images',
                    'Machine learning only works with two dimensions',
                    'Accuracy cannot measure classification performance',
                ],
                "correct": 0,
                "explanation": 'The example demonstrates that choosing or learning a better representation can expose a simple decision rule.',
            },

            {
                "id": 'M01.L02.Q04',
                "section_id": 'learning-as-search',
                "question": 'What does the hypothesis space represent?',
                "options": [
                    'The training labels only',
                    'All data stored on the computer',
                    'The final accuracy score',
                    'The predefined set of possible operations or solutions the learning algorithm can search',
                ],
                "correct": 3,
                "explanation": 'The hypothesis space defines the family of candidate transformations or rules available to the learner.',
            },

            {
                "id": 'M01.L02.Q05',
                "section_id": 'learning-as-search',
                "type": "open",
                "question": 'Give a new example where changing the representation of data could make a task easier, and explain what information the better representation exposes.',
            }
        ],

        "passing_score": 70,
    },
}
