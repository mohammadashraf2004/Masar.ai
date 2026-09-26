"""Masar curriculum seed — L011-042."""

LESSON_META = {'lesson_id': 'L011-042', 'course_id': 'COURSE-011', 'module_id': 'M011-03', 'title': 'Deployment Health & Runtime Validation', 'slug': 'deployment-health-and-runtime-validation', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply deployment health & runtime validation concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['health endpoints', 'readiness awareness', 'smoke tests', 'startup verification', 'post-deployment functional checks']

SOURCE_REFERENCES = ['BOOK-011 Chapters 11, 12, 13']

FIGURE_REFERENCES = []

LESSON_MARKDOWN = '# L011-042 — Deployment Health & Runtime Validation\n\n## Learning objective\n\nApply deployment health & runtime validation concepts to the deployment and operation of an existing production-oriented AI service.\n\n## Core topics\n\n- health endpoints\n- readiness awareness\n- smoke tests\n- startup verification\n- post-deployment functional checks\n\n## AI-engineering context\n\nUse these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n\n## Practice\n\nApply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n\n## Assessment focus\n\nThe learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n\n'

EXERCISES = [{'id': 'L011-042-EX1', 'title': 'Apply Deployment Health & Runtime Validation', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: health endpoints, readiness awareness, smoke tests. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-042-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to deployment health & runtime validation. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-042-Q1', 'type': 'short_answer', 'question': 'What production problem is deployment health & runtime validation intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: health endpoints, readiness awareness, smoke tests.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-042-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-042-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Deployment Health & Runtime Validation.', 'answer': 'health endpoints, readiness awareness', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
