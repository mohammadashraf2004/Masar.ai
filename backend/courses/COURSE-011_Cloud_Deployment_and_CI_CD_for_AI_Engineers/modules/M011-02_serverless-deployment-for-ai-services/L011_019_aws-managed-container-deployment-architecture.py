"""Masar curriculum seed — L011-019."""

LESSON_META = {'lesson_id': 'L011-019', 'course_id': 'COURSE-011', 'module_id': 'M011-02', 'title': 'AWS Managed Container Deployment Architecture', 'slug': 'aws-managed-container-deployment-architecture', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply aws managed container deployment architecture concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['ECS', 'Fargate', 'ECR', 'Application Load Balancer', 'managed container runtime vs EC2']

SOURCE_REFERENCES = ['BOOK-011 Chapters 9 and 10']

FIGURE_REFERENCES = []

LESSON_MARKDOWN = '# L011-019 — AWS Managed Container Deployment Architecture\n\n## Learning objective\n\nApply aws managed container deployment architecture concepts to the deployment and operation of an existing production-oriented AI service.\n\n## Core topics\n\n- ECS\n- Fargate\n- ECR\n- Application Load Balancer\n- managed container runtime vs EC2\n\n## AI-engineering context\n\nUse these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n\n## Practice\n\nApply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n\n## Assessment focus\n\nThe learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n\n'

EXERCISES = [{'id': 'L011-019-EX1', 'title': 'Apply AWS Managed Container Deployment Architecture', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: ECS, Fargate, ECR. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-019-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to aws managed container deployment architecture. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-019-Q1', 'type': 'short_answer', 'question': 'What production problem is aws managed container deployment architecture intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: ECS, Fargate, ECR.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-019-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-019-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by AWS Managed Container Deployment Architecture.', 'answer': 'ECS, Fargate', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
