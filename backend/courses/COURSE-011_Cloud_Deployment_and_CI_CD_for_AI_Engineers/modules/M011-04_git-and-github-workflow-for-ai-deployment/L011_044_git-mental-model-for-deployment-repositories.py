"""Masar curriculum seed — L011-044."""

LESSON_META = {'lesson_id': 'L011-044', 'course_id': 'COURSE-011', 'module_id': 'M011-04', 'title': 'Git Mental Model for Deployment Repositories', 'slug': 'git-mental-model-for-deployment-repositories', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply git mental model for deployment repositories concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['working directory', 'staging area', 'local repository', 'git status/add/commit', 'traceable deployment changes']

SOURCE_REFERENCES = ['Secondary DevOps source (source ID not provided) — Chapter 3: Mastering Version Control with Git and GitHub']

LESSON_MARKDOWN = ('# L011-044 — Git Mental Model for Deployment Repositories\n'
                   '\n'
                   '## Learning objective\n'
                   '\n'
                   'Apply git mental model for deployment repositories concepts to the deployment and operation of an existing production-oriented AI service.\n'
                   '\n'
                   '## Core topics\n'
                   '\n'
                   '- working directory\n'
                   '- staging area\n'
                   '- local repository\n'
                   '- git status/add/commit\n'
                   '- traceable deployment changes\n'
                   '\n'
                   '{{figure:git-three-trees}}\n'
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

EXERCISES = [{'id': 'L011-044-EX1', 'title': 'Apply Git Mental Model for Deployment Repositories', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: working directory, staging area, local repository. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-044-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to git mental model for deployment repositories. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-044-Q1', 'type': 'short_answer', 'question': 'What production problem is git mental model for deployment repositories intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: working directory, staging area, local repository.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-044-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-044-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Git Mental Model for Deployment Repositories.', 'answer': 'working directory, staging area', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
