"""M01.L01 — AI, Machine Learning, and Deep Learning.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 1, pages not provided in the supplied extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = 'M01.L01'

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
    "title": 'AI, Machine Learning, and Deep Learning',

    "slug": 'deep-learning-foundations-m01-l01',

    "description": 'Understand how AI, machine learning, and deep learning relate, and why learning from examples differs from writing explicit rules.',

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 0.75,

    "skill_tags": [
        'artificial-intelligence',
        'machine-learning',
        'deep-learning',
        'foundations',
        'module-01',
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": 'AI, Machine Learning, and Deep Learning',

        "content": (
            '# AI, Machine Learning, and Deep Learning\n'
            '\n'
            '> **Course:** Deep Learning Foundations  \n'
            '> **Lesson:** M01.L01  \n'
            '> **Module:** Deep Learning Foundations  \n'
            '> **Source alignment:** BOOK-002, Chapter 1. The supplied extract does not include page numbers. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n'
            '\n'
            '---\n'
            '\n'
            '## Learning outcomes\n'
            '\n'
            'By the end of this lesson, you should be able to:\n'
            '\n'
            '- Explain the relationship between artificial intelligence, machine learning, and deep learning.\n'
            '- Distinguish rule-based symbolic AI from systems that learn from data.\n'
            '- Explain how machine learning reverses the usual programming workflow.\n'
            '- Identify when a system is being explicitly programmed and when it is being trained from examples.\n'
            '\n'
            '---\n'
            '\n'
            '## 1. AI as the broad field\n'
            '\n'
            'Artificial intelligence, or AI, is the broadest idea in this lesson. A useful working definition is: **AI is the effort to automate intellectual tasks that people normally perform.**\n'
            '\n'
            'That definition is deliberately broad. An AI system does not have to learn. A programmer can build an AI system by writing explicit rules.\n'
            '\n'
            'Imagine a small chess program that contains many hand-written rules for evaluating moves. It may automate an intellectual task, so it belongs to AI, even if it never learns from previous games.\n'
            '\n'
            'This older style of AI is often called **symbolic AI**. The programmer represents knowledge with explicit symbols and rules, then writes logic that manipulates those symbols.\n'
            '\n'
            'A helpful relationship is:\n'
            '\n'
            '```text\n'
            'Artificial Intelligence\n'
            '├── Rule-based / symbolic approaches\n'
            '└── Machine Learning\n'
            '    └── Deep Learning\n'
            '```\n'
            '\n'
            'So deep learning is inside machine learning, and machine learning is inside the broader field of AI.\n'
            '\n'
            '### Why this distinction matters\n'
            '\n'
            'Beginners often use the terms AI, machine learning, and deep learning as if they mean exactly the same thing. They do not.\n'
            '\n'
            '- **AI** is the broad goal or field.\n'
            '- **Machine learning** is one major way to build AI systems.\n'
            '- **Deep learning** is one family of machine-learning methods.\n'
            '\n'
            'Keeping this hierarchy clear will make later terminology much easier.\n'
            '\n'
            '---\n'
            '\n'
            '## 2. Symbolic AI and its limits\n'
            '\n'
            'For many years, researchers hoped that enough carefully written rules could reproduce intelligent behavior.\n'
            '\n'
            'That works well for some problems with clear logic. If a task can be described precisely with rules, a programmer can often encode those rules directly.\n'
            '\n'
            'But many real-world problems are messy.\n'
            '\n'
            'Consider image recognition. You could try to write rules such as:\n'
            '\n'
            '```text\n'
            'If the image contains two triangular ears,\n'
            'two eyes,\n'
            'whisker-like edges,\n'
            'and a certain face shape,\n'
            'then predict "cat."\n'
            '```\n'
            '\n'
            'The problem is that real cat images vary enormously:\n'
            '\n'
            '- different breeds,\n'
            '- different lighting,\n'
            '- different camera angles,\n'
            '- partially hidden faces,\n'
            '- unusual backgrounds,\n'
            '- kittens and adult cats.\n'
            '\n'
            'The rule set quickly becomes fragile and difficult to maintain.\n'
            '\n'
            'The same difficulty appears in speech recognition and natural-language translation. It is hard to manually write every rule needed to handle real variation.\n'
            '\n'
            'This limitation created demand for a different approach: instead of writing every rule ourselves, can we let the machine discover useful rules from examples?\n'
            '\n'
            '{{exercise:M01.L01.EX01}}\n'
            '\n'
            '---\n'
            '\n'
            '## 3. Machine learning reverses the programming workflow\n'
            '\n'
            'Traditional programming usually looks like this:\n'
            '\n'
            '```text\n'
            'Data + Human-written rules\n'
            '          ↓\n'
            '       Program\n'
            '          ↓\n'
            '        Answers\n'
            '```\n'
            '\n'
            'Machine learning changes the direction:\n'
            '\n'
            '```text\n'
            'Data + Expected answers\n'
            '          ↓\n'
            '   Learning algorithm\n'
            '          ↓\n'
            '   Learned model/rules\n'
            '```\n'
            '\n'
            'Suppose you want to classify vacation photos as **food** or **landscape**.\n'
            '\n'
            'With explicit programming, you would try to invent rules that distinguish food photos from landscape photos.\n'
            '\n'
            'With machine learning, you instead collect many examples:\n'
            '\n'
            '```text\n'
            'photo_001.jpg -> food\n'
            'photo_002.jpg -> landscape\n'
            'photo_003.jpg -> food\n'
            'photo_004.jpg -> landscape\n'
            '```\n'
            '\n'
            'The system studies the examples and learns statistical structure that helps it classify new photos.\n'
            '\n'
            'This is why we say a machine-learning system is **trained** rather than fully programmed by hand.\n'
            '\n'
            '### A useful mental model\n'
            '\n'
            'Traditional programming asks:\n'
            '\n'
            '> What rules should the computer follow?\n'
            '\n'
            'Machine learning asks:\n'
            '\n'
            '> What examples can I give the computer so it can learn a useful rule?\n'
            '\n'
            'The programmer is still very important. Humans still choose the task, collect or prepare data, choose an algorithm, define how success is measured, and evaluate the result. What changes is that the final decision rule is learned from data rather than completely specified by hand.\n'
            '\n'
            '---\n'
            '\n'
            '## 4. Where deep learning fits\n'
            '\n'
            'Deep learning is a **subfield of machine learning**.\n'
            '\n'
            'It uses models with many successive layers that learn increasingly useful representations of the input data.\n'
            '\n'
            'For now, do not worry about how those layers work. The important relationship is:\n'
            '\n'
            '```text\n'
            'AI\n'
            '└── Machine Learning\n'
            '    └── Deep Learning\n'
            '```\n'
            '\n'
            'A deep-learning model is therefore both:\n'
            '\n'
            '- a machine-learning model, because it learns from data, and\n'
            '- an AI technique, because machine learning belongs to AI.\n'
            '\n'
            'But the reverse statements are not true:\n'
            '\n'
            '- not every AI system uses machine learning,\n'
            '- not every machine-learning system uses deep learning.\n'
            '\n'
            '{{exercise:M01.L01.EX02}}\n'
            '\n'
            '---\n'
            '\n'
            '## Important misconception\n'
            '\n'
            '### Misconception\n'
            '\n'
            '> "AI, machine learning, and deep learning are three names for the same thing."\n'
            '\n'
            '### Why this is wrong\n'
            '\n'
            'They describe different levels of a hierarchy. AI is the broadest field. Machine learning is an approach inside AI that learns from data. Deep learning is a particular approach inside machine learning that learns through multiple layers of representations.\n'
            '\n'
            '---\n'
            '\n'
            '## Key terminology\n'
            '\n'
            '| Term | Meaning |\n'
            '|---|---|\n'
            '| Artificial intelligence | The broad effort to automate intellectual tasks normally performed by humans |\n'
            '| Symbolic AI | AI based mainly on explicit human-written symbols and rules |\n'
            '| Machine learning | A way to learn useful rules or statistical structure from examples |\n'
            '| Training | The process through which a model adjusts itself using data |\n'
            '| Deep learning | Machine learning based on multiple successive layers of learned representations |\n'
            '\n'
            '---\n'
            '\n'
            '## Self-check\n'
            '\n'
            'Before continuing, make sure you can answer:\n'
            '\n'
            '1. Why can an AI system exist without machine learning?\n'
            '2. Why are explicit rules difficult for problems such as image recognition?\n'
            '3. How does machine learning reverse the usual programming workflow?\n'
            '4. Why is every deep-learning model also a machine-learning model?\n'
            '\n'
            '---\n'
            '\n'
            '## Retain this idea\n'
            '\n'
            '**AI is the broad field, machine learning learns from examples, and deep learning is a layered form of machine learning.**\n'
        ),

        "estimated_minutes": 45,

        "has_code_examples": False,

        "sections": [
            {
                "id": 'ai-as-the-broad-field',
                "title": 'AI as the broad field',
                "order": 1,
            },
            {
                "id": 'symbolic-ai-and-its-limits',
                "title": 'Symbolic AI and its limits',
                "order": 2,
            },
            {
                "id": 'machine-learning-reverses-programming',
                "title": 'Machine learning reverses the programming workflow',
                "order": 3,
            },
            {
                "id": 'where-deep-learning-fits',
                "title": 'Where deep learning fits',
                "order": 4,
            }
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": 'M01.L01.EX01',
            "title": 'Rules or Learning?',
            "lesson_code": 'M01.L01',
            "section_id": 'symbolic-ai-and-its-limits',
            "placement": "after_section",
            "description": 'Practice distinguishing explicit rule-based automation from learning from examples.',
            "instructions": '1. Consider these three systems: a tax calculator with fixed rules, an email spam classifier trained on labeled messages, and a chess program containing only hand-written move rules.\n2. For each system, decide whether it is rule-based AI/automation or machine learning.\n3. Explain which system must learn from examples.\n4. Identify one reason the spam problem is harder to solve with exhaustive hand-written rules.',
            "expected_output": 'A three-row classification table plus a short explanation of why the spam classifier benefits from learning from examples.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'ai-vs-ml',
                'rule-based-reasoning',
            ],
        },

        {
            "id": 'M01.L01.EX02',
            "title": 'Build the Hierarchy',
            "lesson_code": 'M01.L01',
            "section_id": 'where-deep-learning-fits',
            "placement": "after_section",
            "description": 'Reinforce the containment relationship among AI, machine learning, and deep learning.',
            "instructions": "1. Draw or write a three-level hierarchy using AI, machine learning, and deep learning.\n2. State whether each sentence is true or false: 'Every AI system is deep learning'; 'Every deep-learning model is machine learning'; 'Machine learning is broader than AI.'\n3. Correct every false statement.\n4. Give one short sentence explaining what makes machine learning different from purely hand-written rules.",
            "expected_output": 'A hierarchy plus three true/false answers with corrections and one explanatory sentence.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'concept-hierarchy',
                'terminology',
            ],
        }
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": 'M01.L01.QZ01',

        "title": 'AI, Machine Learning, and Deep Learning — Knowledge Check',

        "lesson_code": 'M01.L01',

        "placement": "lesson_end",

        "questions": [
            {
                "id": 'M01.L01.Q01',
                "section_id": 'ai-as-the-broad-field',
                "question": 'Which statement best describes artificial intelligence in this chapter?',
                "options": [
                    'Only systems built with neural networks',
                    'The broad effort to automate intellectual tasks normally performed by humans',
                    'Only software that learns without human involvement',
                    'A synonym for deep learning',
                ],
                "correct": 1,
                "explanation": 'AI is the broad field. It includes learning-based methods and approaches that rely on explicit human-written rules.',
            },

            {
                "id": 'M01.L01.Q02',
                "section_id": 'symbolic-ai-and-its-limits',
                "question": 'Why did symbolic AI struggle with tasks such as image classification?',
                "options": [
                    'Images cannot be stored on computers',
                    'Symbolic AI cannot execute logical rules',
                    'It is difficult to write explicit rules that cover the large variation in complex real-world data',
                    'Machine learning requires no data',
                ],
                "correct": 2,
                "explanation": 'Complex perceptual tasks contain too much variation for a manageable set of brittle hand-written rules.',
            },

            {
                "id": 'M01.L01.Q03',
                "section_id": 'machine-learning-reverses-programming',
                "question": 'What is supplied to a supervised machine-learning system during training?',
                "options": [
                    'Examples of inputs together with expected outputs',
                    'Only a final rule written by the programmer',
                    'No data, only hardware',
                    'Only random predictions',
                ],
                "correct": 0,
                "explanation": 'The model receives examples and expected answers, then learns statistical structure that helps produce useful rules or predictions.',
            },

            {
                "id": 'M01.L01.Q04',
                "section_id": 'where-deep-learning-fits',
                "question": 'Which relationship is correct?',
                "options": [
                    'AI is a subfield of deep learning',
                    'Deep learning and machine learning are unrelated',
                    'Machine learning contains AI',
                    'Deep learning is a subfield of machine learning, which is part of AI',
                ],
                "correct": 3,
                "explanation": 'The chapter presents deep learning inside machine learning, and machine learning inside the broader field of AI.',
            },

            {
                "id": 'M01.L01.Q05',
                "section_id": 'where-deep-learning-fits',
                "type": "open",
                "question": 'You are given thousands of labeled animal photos and asked to build a classifier. Explain why this setup naturally fits machine learning rather than trying to write every visual rule by hand.',
            }
        ],

        "passing_score": 70,
    },
}
