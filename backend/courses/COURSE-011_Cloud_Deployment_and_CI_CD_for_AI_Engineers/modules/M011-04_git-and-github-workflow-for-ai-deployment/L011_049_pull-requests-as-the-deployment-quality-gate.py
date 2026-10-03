"""Masar curriculum seed — L011-049."""

LESSON_META = {'lesson_id': 'L011-049', 'course_id': 'COURSE-011', 'module_id': 'M011-04', 'title': 'Pull Requests as the Deployment Quality Gate', 'slug': 'pull-requests-as-the-deployment-quality-gate', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply pull requests as the deployment quality gate concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['pull requests', 'base and compare branches', 'reviewers', 'change descriptions', 'merge workflow']

SOURCE_REFERENCES = ['Secondary DevOps source (source ID not provided) — Chapter 3: Mastering Version Control with Git and GitHub']

LESSON_MARKDOWN = ('# L011-049 — Pull Requests as the Deployment Quality Gate\n'
                   '\n'
                   '## Learning objective\n'
                   '\n'
                   'Apply pull requests as the deployment quality gate concepts to the deployment and operation of an existing production-oriented AI service.\n'
                   '\n'
                   '## Core topics\n'
                   '\n'
                   '- pull requests\n'
                   '- base and compare branches\n'
                   '- reviewers\n'
                   '- change descriptions\n'
                   '- merge workflow\n'
                   '\n'
                   '{{figure:pull-request}}\n'
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

EXERCISES = [{'id': 'L011-049-EX1', 'title': 'Apply Pull Requests as the Deployment Quality Gate', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: pull requests, base and compare branches, reviewers. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-049-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to pull requests as the deployment quality gate. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-049-Q1', 'type': 'short_answer', 'question': 'What production problem is pull requests as the deployment quality gate intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: pull requests, base and compare branches, reviewers.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-049-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-049-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Pull Requests as the Deployment Quality Gate.', 'answer': 'pull requests, base and compare branches', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
