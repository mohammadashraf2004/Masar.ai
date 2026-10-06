"""M01.L03 — How Deep Learning Learns.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 1, pages not provided in the supplied extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = 'M01.L03'

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
    "title": 'How Deep Learning Learns',

    "slug": 'deep-learning-foundations-m01-l03',

    "description": 'Understand layered representations, neural-network parameters, loss, backpropagation, optimizers, and the core training loop.',

    "order": 3,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 1.0,

    "skill_tags": [
        'neural-networks',
        'weights',
        'loss',
        'backpropagation',
        'training-loop',
        'module-01',
    ],

    "prerequisite_ids": ['M01.L02'],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": 'How Deep Learning Learns',

        "content": (
            '# How Deep Learning Learns\n'
            '\n'
            '> **Course:** Deep Learning Foundations  \n'
            '> **Lesson:** M01.L03  \n'
            '> **Module:** Deep Learning Foundations  \n'
            '> **Source alignment:** BOOK-002, Chapter 1. The supplied extract does not include page numbers. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n'
            '\n'
            '---\n'
            '\n'
            '## Learning outcomes\n'
            '\n'
            'By the end of this lesson, you should be able to:\n'
            '\n'
            '- Explain what the word deep means in deep learning.\n'
            '- Describe neural-network layers, weights, and parameters at a high level.\n'
            '- Explain the role of a loss function.\n'
            '- Describe the training loop involving prediction, loss, backpropagation, and parameter updates.\n'
            '\n'
            '---\n'
            '\n'
            '## 1. Deep means layered representations\n'
            '\n'
            'The word **deep** does not mean that a neural network has deep human-like understanding.\n'
            '\n'
            'It refers to **depth**: many successive layers of learned representations.\n'
            '\n'
            'A shallow approach might transform data only once or twice.\n'
            '\n'
            'Deep learning uses a sequence:\n'
            '\n'
            '```text\n'
            'Input\n'
            '  ↓\n'
            'Layer 1 representation\n'
            '  ↓\n'
            'Layer 2 representation\n'
            '  ↓\n'
            'Layer 3 representation\n'
            '  ↓\n'
            '...\n'
            '  ↓\n'
            'Output\n'
            '```\n'
            '\n'
            'Each layer receives a representation and transforms it into another representation.\n'
            '\n'
            'For image classification, an intuitive mental model is:\n'
            '\n'
            '```text\n'
            'pixels\n'
            '  ↓\n'
            'simple visual structure\n'
            '  ↓\n'
            'more useful patterns\n'
            '  ↓\n'
            'task-specific representation\n'
            '  ↓\n'
            'class prediction\n'
            '```\n'
            '\n'
            'The exact internal features may not line up perfectly with human concepts such as "edge" or "shape," but the key idea remains: information passes through many learned transformations.\n'
            '\n'
            'The chapter describes this as a multistage **information-distillation** process. As the data passes through layers, the representation becomes increasingly useful for the task.\n'
            '\n'
            '---\n'
            '\n'
            '## 2. Weights define layer transformations\n'
            '\n'
            'A neural-network layer performs a mathematical transformation.\n'
            '\n'
            'The exact behavior of that transformation is controlled by numbers called **weights**, also called **parameters**.\n'
            '\n'
            'A tiny simplified example is:\n'
            '\n'
            '```text\n'
            'output = input × weight\n'
            '```\n'
            '\n'
            'If the input is 5 and the weight is 2:\n'
            '\n'
            '```text\n'
            'output = 5 × 2 = 10\n'
            '```\n'
            '\n'
            'Real neural networks are much more complicated and may contain millions or more parameters, but the principle is the same:\n'
            '\n'
            '> Change the weights, and you change what the network computes.\n'
            '\n'
            'Training therefore becomes a parameter-search problem:\n'
            '\n'
            '> Find values for all the weights so that inputs are mapped to useful outputs.\n'
            '\n'
            'At initialization, the weights do not yet represent a good solution. The network needs a way to evaluate its predictions and improve them.\n'
            '\n'
            '{{exercise:M01.L03.EX01}}\n'
            '\n'
            '---\n'
            '\n'
            '## 3. Loss measures prediction quality\n'
            '\n'
            'Suppose the true target for an image is:\n'
            '\n'
            '```text\n'
            'cat\n'
            '```\n'
            '\n'
            'But the model predicts:\n'
            '\n'
            '```text\n'
            'cat = 0.10\n'
            'dog = 0.90\n'
            '```\n'
            '\n'
            'The prediction is poor.\n'
            '\n'
            'A **loss function** converts this mismatch into a numerical score.\n'
            '\n'
            'The exact formula depends on the task, but conceptually:\n'
            '\n'
            '```text\n'
            'Prediction + True target\n'
            '          ↓\n'
            '      Loss function\n'
            '          ↓\n'
            '      Loss score\n'
            '```\n'
            '\n'
            'A high loss indicates that the current prediction is far from what we want.\n'
            '\n'
            'A lower loss indicates a better fit for that example.\n'
            '\n'
            'This is important because the network cannot improve based on a vague instruction such as "be more correct." It needs a quantity that can act as a feedback signal.\n'
            '\n'
            'The learning objective is therefore to adjust the model so that the loss becomes smaller.\n'
            '\n'
            '---\n'
            '\n'
            '## 4. The training loop\n'
            '\n'
            'The fundamental training cycle is:\n'
            '\n'
            '```text\n'
            '1. Feed an input into the network\n'
            '2. Produce a prediction\n'
            '3. Compare prediction with target\n'
            '4. Compute loss\n'
            '5. Determine how parameters contributed to the loss\n'
            '6. Adjust parameters\n'
            '7. Repeat\n'
            '```\n'
            '\n'
            "The chapter identifies **backpropagation** as the central algorithm used to determine how the network's parameters should be adjusted.\n"
            '\n'
            'You do not need the mathematics yet. For now, use this mental model:\n'
            '\n'
            '```text\n'
            'FORWARD\n'
            'Input -> Layers -> Prediction\n'
            '                    |\n'
            '                    v\n'
            '                  Loss\n'
            '                    |\n'
            '                    v\n'
            'BACKWARD       error signal\n'
            '                    |\n'
            '                    v\n'
            '              adjust weights\n'
            '```\n'
            '\n'
            'An **optimizer** uses the information from the learning process to make small changes to the weights in a direction that lowers the loss.\n'
            '\n'
            'At the beginning, the weights are assigned initial values and the outputs are not useful. Repeating the cycle across many examples gradually improves the weights.\n'
            '\n'
            'A compact pseudo-code version is:\n'
            '\n'
            '```python\n'
            'for input_data, target in training_data:\n'
            '    prediction = model(input_data)\n'
            '    loss = loss_function(prediction, target)\n'
            '\n'
            '    # Backpropagation computes information needed for parameter updates.\n'
            '    gradients = backward(loss)\n'
            '\n'
            '    optimizer.update(model.parameters, gradients)\n'
            '```\n'
            '\n'
            'This code is conceptual rather than tied to a specific framework. Its purpose is to show the learning sequence.\n'
            '\n'
            '{{exercise:M01.L03.EX02}}\n'
            '\n'
            '---\n'
            '\n'
            '## Important misconception\n'
            '\n'
            '### Misconception\n'
            '\n'
            '> "The network learns because someone manually tells every hidden layer which feature to detect."\n'
            '\n'
            '### Why this is wrong\n'
            '\n'
            "Deep learning learns the parameters controlling its internal representations from examples. Humans design the model and training process, but the chapter's central idea is that the useful layered representations are learned rather than hand-crafted one by one.\n"
            '\n'
            '---\n'
            '\n'
            '## Key terminology\n'
            '\n'
            '| Term | Meaning |\n'
            '|---|---|\n'
            '| Layer | A stage that transforms one representation into another |\n'
            '| Depth | The number of successive representation layers in a model |\n'
            '| Neural network | A layered model used to learn transformations from data |\n'
            "| Weight / parameter | A learnable numerical value controlling a layer's behavior |\n"
            '| Loss function | A function that measures how far a prediction is from its target |\n'
            '| Optimizer | The mechanism that updates parameters to reduce loss |\n'
            '| Backpropagation | The algorithm used to propagate error information so parameters can be adjusted |\n'
            '| Training loop | The repeated cycle of prediction, loss calculation, and parameter updates |\n'
            '\n'
            '---\n'
            '\n'
            '## Self-check\n'
            '\n'
            'Before continuing, make sure you can answer:\n'
            '\n'
            '1. What does deep mean in deep learning?\n'
            '2. What do weights control?\n'
            '3. Why does the network need a loss function?\n'
            '4. What happens during one training iteration?\n'
            '\n'
            '---\n'
            '\n'
            '## Retain this idea\n'
            '\n'
            '**Deep learning trains layered representations by repeatedly predicting, measuring loss, propagating error information backward, and updating weights.**\n'
        ),

        "estimated_minutes": 60,

        "has_code_examples": True,

        "sections": [
            {
                "id": 'deep-means-layered-representations',
                "title": 'Deep means layered representations',
                "order": 1,
            },
            {
                "id": 'weights-define-layer-transformations',
                "title": 'Weights define layer transformations',
                "order": 2,
            },
            {
                "id": 'loss-measures-error',
                "title": 'Loss measures prediction quality',
                "order": 3,
            },
            {
                "id": 'training-loop-and-backpropagation',
                "title": 'The training loop',
                "order": 4,
            }
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": 'M01.L03.EX01',
            "title": 'Trace a Layered Model',
            "lesson_code": 'M01.L03',
            "section_id": 'weights-define-layer-transformations',
            "placement": "after_section",
            "description": 'Practice reasoning about layers and learnable parameters without needing advanced mathematics.',
            "instructions": "1. Write a four-stage path from input image to class prediction using three intermediate layers.\n2. Label the numbers controlling each layer as weights or parameters.\n3. Explain what would happen to the network's output if its weights changed.\n4. State why training can be described as finding useful parameter values.",
            "expected_output": 'A labeled flow diagram and a short explanation of the role of weights.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'layered-representations',
                'parameter-reasoning',
            ],
        },

        {
            "id": 'M01.L03.EX02',
            "title": 'Walk Through One Training Step',
            "lesson_code": 'M01.L03',
            "section_id": 'training-loop-and-backpropagation',
            "placement": "after_section",
            "description": 'Apply the complete prediction-to-update training sequence.',
            "instructions": "1. Assume the target is 'cat' but the model strongly predicts 'dog.'\n2. Describe what the loss function should indicate.\n3. Explain the role of backpropagation at a conceptual level.\n4. Explain what the optimizer changes before the next prediction.",
            "expected_output": 'A numbered four-step explanation of one training iteration.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'loss',
                'backpropagation',
                'optimizer',
            ],
        }
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": 'M01.L03.QZ01',

        "title": 'How Deep Learning Learns — Knowledge Check',

        "lesson_code": 'M01.L03',

        "placement": "lesson_end",

        "questions": [
            {
                "id": 'M01.L03.Q01',
                "section_id": 'deep-means-layered-representations',
                "question": 'What does the word deep refer to in deep learning?',
                "options": [
                    'Human-like consciousness',
                    'A large training file',
                    'Successive layers of learned representations',
                    'The physical depth of the computer',
                ],
                "correct": 2,
                "explanation": 'Depth refers to the number of successive representation transformations used by the model.',
            },

            {
                "id": 'M01.L03.Q02',
                "section_id": 'weights-define-layer-transformations',
                "question": 'What are weights in a neural network?',
                "options": [
                    'Learnable numerical parameters that control layer transformations',
                    'Labels attached to examples',
                    'Only the final predictions',
                    'Fixed rules that can never change',
                ],
                "correct": 0,
                "explanation": 'Weights are numerical parameters whose values determine how layers transform their inputs.',
            },

            {
                "id": 'M01.L03.Q03',
                "section_id": 'loss-measures-error',
                "question": 'What is the main purpose of the loss function?',
                "options": [
                    'Store the dataset',
                    'Measure the mismatch between predictions and targets',
                    'Add more training examples',
                    'Choose the hardware',
                ],
                "correct": 1,
                "explanation": "The loss provides a numerical feedback signal indicating how well the model's current output matches the target.",
            },

            {
                "id": 'M01.L03.Q04',
                "section_id": 'training-loop-and-backpropagation',
                "question": 'Which sequence best describes training?',
                "options": [
                    'Update weights -> delete target -> stop',
                    'Target -> hardware -> random label -> stop',
                    'Loss -> input -> prediction -> never update',
                    'Input -> prediction -> loss -> backpropagation/update -> repeat',
                ],
                "correct": 3,
                "explanation": 'Training repeatedly makes predictions, measures error, propagates error information, and updates model parameters.',
            },

            {
                "id": 'M01.L03.Q05',
                "section_id": 'training-loop-and-backpropagation',
                "type": "open",
                "question": 'Explain the roles of the loss function, backpropagation, and the optimizer as three distinct parts of the same training cycle.',
            }
        ],

        "passing_score": 70,
    },
}
