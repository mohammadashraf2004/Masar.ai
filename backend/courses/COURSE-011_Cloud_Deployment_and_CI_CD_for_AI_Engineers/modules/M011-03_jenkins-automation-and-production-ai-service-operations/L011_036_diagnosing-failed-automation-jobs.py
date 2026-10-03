"""Masar curriculum seed — L011-036."""

LESSON_META = {'lesson_id': 'L011-036', 'course_id': 'COURSE-011', 'module_id': 'M011-03', 'title': 'Diagnosing Failed Automation Jobs', 'slug': 'diagnosing-failed-automation-jobs', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply diagnosing failed automation jobs concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['failed builds', 'console logs', 'cloud exceptions', 'missing dependencies/resources', 'fix-rerun-verify loop']

SOURCE_REFERENCES = ['BOOK-011 Chapters 11, 12, 13']

LESSON_MARKDOWN = ('# L011-036 — Diagnosing Failed Automation Jobs\n'
                   '\n'
                   '## Learning objective\n'
                   '\n'
                   'Apply diagnosing failed automation jobs concepts to the deployment and operation of an existing production-oriented AI service.\n'
                   '\n'
                   '## Core topics\n'
                   '\n'
                   '- failed builds\n'
                   '- console logs\n'
                   '- cloud exceptions\n'
                   '- missing dependencies/resources\n'
                   '- fix-rerun-verify loop\n'
                   '\n'
                   '{{figure:jenkins-failure}}\n'
                   '\n'
                   '## AI-engineering context\n'
                   '\n'
                   'Use these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n'
                   '\n'
                   '## Practice\n'
                   '\n'
                   'Apply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n'
                   '\n'
                   '## Assessment focus\n'
                   '\n'
                   'The learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n')

EXERCISES = [{'id': 'L011-036-EX1', 'title': 'Apply Diagnosing Failed Automation Jobs', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: failed builds, console logs, cloud exceptions. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-036-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to diagnosing failed automation jobs. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-036-Q1', 'type': 'short_answer', 'question': 'What production problem is diagnosing failed automation jobs intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: failed builds, console logs, cloud exceptions.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-036-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-036-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Diagnosing Failed Automation Jobs.', 'answer': 'failed builds, console logs', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
