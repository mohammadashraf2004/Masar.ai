"""Masar curriculum seed — L011-046."""

LESSON_META = {'lesson_id': 'L011-046', 'course_id': 'COURSE-011', 'module_id': 'M011-04', 'title': 'Local and Remote Repository Workflow', 'slug': 'local-and-remote-repository-workflow', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply local and remote repository workflow concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['GitHub remote repositories', 'origin', 'clone', 'push', 'pull and fetch']

SOURCE_REFERENCES = ['Secondary DevOps source (source ID not provided) — Chapter 3: Mastering Version Control with Git and GitHub']

FIGURE_REFERENCES = []

LESSON_MARKDOWN = '# L011-046 — Local and Remote Repository Workflow\n\n## Learning objective\n\nApply local and remote repository workflow concepts to the deployment and operation of an existing production-oriented AI service.\n\n## Core topics\n\n- GitHub remote repositories\n- origin\n- clone\n- push\n- pull and fetch\n\n## AI-engineering context\n\nUse these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n\n## Practice\n\nApply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n\n## Assessment focus\n\nThe learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n\n'

EXERCISES = [{'id': 'L011-046-EX1', 'title': 'Apply Local and Remote Repository Workflow', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: GitHub remote repositories, origin, clone. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-046-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to local and remote repository workflow. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-046-Q1', 'type': 'short_answer', 'question': 'What production problem is local and remote repository workflow intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: GitHub remote repositories, origin, clone.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-046-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-046-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Local and Remote Repository Workflow.', 'answer': 'GitHub remote repositories, origin', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
