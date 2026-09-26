"""Masar curriculum seed — L011-064."""

LESSON_META = {'lesson_id': 'L011-064', 'course_id': 'COURSE-011', 'module_id': 'M011-05', 'title': 'Multi-Job GitHub Actions Workflows', 'slug': 'multi-job-github-actions-workflows', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply multi-job github actions workflows concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['multiple jobs', 'job outputs', 'needs dependencies', 'build job', 'deploy job', 'failure propagation']

SOURCE_REFERENCES = ['Secondary DevOps source (source ID not provided) — Chapter 6: Constructing Your First CI/CD Pipeline']

FIGURE_REFERENCES = []

LESSON_MARKDOWN = '# L011-064 — Multi-Job GitHub Actions Workflows\n\n## Learning objective\n\nApply multi-job github actions workflows concepts to the deployment and operation of an existing production-oriented AI service.\n\n## Core topics\n\n- multiple jobs\n- job outputs\n- needs dependencies\n- build job\n- deploy job\n- failure propagation\n\n## AI-engineering context\n\nUse these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n\n## Practice\n\nApply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n\n## Assessment focus\n\nThe learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n\n'

EXERCISES = [{'id': 'L011-064-EX1', 'title': 'Apply Multi-Job GitHub Actions Workflows', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: multiple jobs, job outputs, needs dependencies. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-064-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to multi-job github actions workflows. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-064-Q1', 'type': 'short_answer', 'question': 'What production problem is multi-job github actions workflows intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: multiple jobs, job outputs, needs dependencies.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-064-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-064-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Multi-Job GitHub Actions Workflows.', 'answer': 'multiple jobs, job outputs', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
