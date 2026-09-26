"""Masar curriculum seed — L011-057."""

LESSON_META = {'lesson_id': 'L011-057', 'course_id': 'COURSE-011', 'module_id': 'M011-05', 'title': 'Events & Triggers for AI Repositories', 'slug': 'events-and-triggers-for-ai-repositories', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply events & triggers for ai repositories concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['push events', 'pull_request events', 'branch filters', 'manual triggers', 'scheduled workflows']

SOURCE_REFERENCES = ['Secondary DevOps source (source ID not provided) — Chapter 6: Constructing Your First CI/CD Pipeline']

FIGURE_REFERENCES = []

LESSON_MARKDOWN = '# L011-057 — Events & Triggers for AI Repositories\n\n## Learning objective\n\nApply events & triggers for ai repositories concepts to the deployment and operation of an existing production-oriented AI service.\n\n## Core topics\n\n- push events\n- pull_request events\n- branch filters\n- manual triggers\n- scheduled workflows\n\n## AI-engineering context\n\nUse these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n\n## Practice\n\nApply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n\n## Assessment focus\n\nThe learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n\n'

EXERCISES = [{'id': 'L011-057-EX1', 'title': 'Apply Events & Triggers for AI Repositories', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: push events, pull_request events, branch filters. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-057-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to events & triggers for ai repositories. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-057-Q1', 'type': 'short_answer', 'question': 'What production problem is events & triggers for ai repositories intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: push events, pull_request events, branch filters.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-057-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-057-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Events & Triggers for AI Repositories.', 'answer': 'push events, pull_request events', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
