"""Masar curriculum seed — L011-060."""

LESSON_META = {'lesson_id': 'L011-060', 'course_id': 'COURSE-011', 'module_id': 'M011-05', 'title': 'Diagnosing GitHub Actions Failures', 'slug': 'diagnosing-github-actions-failures', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply diagnosing github actions failures concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['workflow runs', 'failed jobs and steps', 'step logs', 'test/configuration errors', 'rerun jobs']

SOURCE_REFERENCES = ['Secondary DevOps source (source ID not provided) — Chapter 6: Constructing Your First CI/CD Pipeline']

FIGURE_REFERENCES = []

LESSON_MARKDOWN = '# L011-060 — Diagnosing GitHub Actions Failures\n\n## Learning objective\n\nApply diagnosing github actions failures concepts to the deployment and operation of an existing production-oriented AI service.\n\n## Core topics\n\n- workflow runs\n- failed jobs and steps\n- step logs\n- test/configuration errors\n- rerun jobs\n\n## AI-engineering context\n\nUse these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n\n## Practice\n\nApply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n\n## Assessment focus\n\nThe learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n\n'

EXERCISES = [{'id': 'L011-060-EX1', 'title': 'Apply Diagnosing GitHub Actions Failures', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: workflow runs, failed jobs and steps, step logs. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-060-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to diagnosing github actions failures. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-060-Q1', 'type': 'short_answer', 'question': 'What production problem is diagnosing github actions failures intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: workflow runs, failed jobs and steps, step logs.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-060-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-060-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Diagnosing GitHub Actions Failures.', 'answer': 'workflow runs, failed jobs and steps', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
