"""Masar curriculum seed — L011-029."""

LESSON_META = {'lesson_id': 'L011-029', 'course_id': 'COURSE-011', 'module_id': 'M011-02', 'title': 'GCP Cloud Run vs AWS ECS/Fargate', 'slug': 'gcp-cloud-run-vs-aws-ecs-fargate', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply gcp cloud run vs aws ecs/fargate concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['runtime comparison', 'registry comparison', 'load-balancer integration', 'autoscaling differences', 'architecture selection criteria']

SOURCE_REFERENCES = ['BOOK-011 Chapters 9 and 10']

FIGURE_REFERENCES = []

LESSON_MARKDOWN = '# L011-029 — GCP Cloud Run vs AWS ECS/Fargate\n\n## Learning objective\n\nApply gcp cloud run vs aws ecs/fargate concepts to the deployment and operation of an existing production-oriented AI service.\n\n## Core topics\n\n- runtime comparison\n- registry comparison\n- load-balancer integration\n- autoscaling differences\n- architecture selection criteria\n\n## AI-engineering context\n\nUse these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n\n## Practice\n\nApply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n\n## Assessment focus\n\nThe learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n\n'

EXERCISES = [{'id': 'L011-029-EX1', 'title': 'Apply GCP Cloud Run vs AWS ECS/Fargate', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: runtime comparison, registry comparison, load-balancer integration. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-029-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to gcp cloud run vs aws ecs/fargate. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-029-Q1', 'type': 'short_answer', 'question': 'What production problem is gcp cloud run vs aws ecs/fargate intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: runtime comparison, registry comparison, load-balancer integration.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-029-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-029-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by GCP Cloud Run vs AWS ECS/Fargate.', 'answer': 'runtime comparison, registry comparison', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
