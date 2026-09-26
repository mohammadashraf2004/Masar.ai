"""Masar curriculum seed — L011-026."""

LESSON_META = {'lesson_id': 'L011-026', 'course_id': 'COURSE-011', 'module_id': 'M011-02', 'title': 'ECS Services & Managed Application Runtime', 'slug': 'ecs-services-and-managed-application-runtime', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply ecs services & managed application runtime concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['ECS services', 'desired task count', 'VPC and subnets', 'ALB integration', 'automatic task registration and lifecycle']

SOURCE_REFERENCES = ['BOOK-011 Chapters 9 and 10']

FIGURE_REFERENCES = []

LESSON_MARKDOWN = '# L011-026 — ECS Services & Managed Application Runtime\n\n## Learning objective\n\nApply ecs services & managed application runtime concepts to the deployment and operation of an existing production-oriented AI service.\n\n## Core topics\n\n- ECS services\n- desired task count\n- VPC and subnets\n- ALB integration\n- automatic task registration and lifecycle\n\n## AI-engineering context\n\nUse these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n\n## Practice\n\nApply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n\n## Assessment focus\n\nThe learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n\n'

EXERCISES = [{'id': 'L011-026-EX1', 'title': 'Apply ECS Services & Managed Application Runtime', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: ECS services, desired task count, VPC and subnets. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-026-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to ecs services & managed application runtime. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-026-Q1', 'type': 'short_answer', 'question': 'What production problem is ecs services & managed application runtime intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: ECS services, desired task count, VPC and subnets.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-026-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-026-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by ECS Services & Managed Application Runtime.', 'answer': 'ECS services, desired task count', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
