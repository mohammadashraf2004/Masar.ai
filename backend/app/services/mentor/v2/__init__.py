"""
Mentor v2 - a course-aware learning companion rather than a chatbot.

    context.py      what the server knows about the learner's lesson, built from ids and the
                    learner's own progress (never from anything the client claims)
    intent.py       what the learner is asking for: an explicit intent, then keyword rules,
                    then (only when those cannot decide) the model
    blocks.py       the structured reply: parsing the model's output, and the validation layer
    message.py      POST /mentor/message end to end
    quiz.py         authored quiz questions as blocks, and POST /mentor/quiz/answer
    skills.py       skill confidence and status, folded from stored evidence
"""
