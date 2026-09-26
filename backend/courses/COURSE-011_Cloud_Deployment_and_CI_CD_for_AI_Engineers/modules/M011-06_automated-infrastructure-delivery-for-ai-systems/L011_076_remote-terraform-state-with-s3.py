"""Masar curriculum seed — L011-076."""

LESSON_META = {'lesson_id': 'L011-076', 'course_id': 'COURSE-011', 'module_id': 'M011-06', 'title': 'Remote Terraform State with S3', 'slug': 'remote-terraform-state-with-s3', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply remote terraform state with s3 concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['remote backend', 'S3 state storage', 'state key', 'IAM backend permissions', 'terraform init and state migration']

SOURCE_REFERENCES = ['Secondary DevOps source (source ID not provided) — Chapter 7: Automating Infrastructure with Terraform and CI/CD']

FIGURE_REFERENCES = []

LESSON_MARKDOWN = '# L011-076 — Remote Terraform State with S3\n\n## Learning objective\n\nApply remote terraform state with s3 concepts to the deployment and operation of an existing production-oriented AI service.\n\n## Core topics\n\n- remote backend\n- S3 state storage\n- state key\n- IAM backend permissions\n- terraform init and state migration\n\n## AI-engineering context\n\nUse these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n\n## Practice\n\nApply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n\n## Assessment focus\n\nThe learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n\n'

EXERCISES = [{'id': 'L011-076-EX1', 'title': 'Apply Remote Terraform State with S3', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: remote backend, S3 state storage, state key. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-076-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to remote terraform state with s3. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-076-Q1', 'type': 'short_answer', 'question': 'What production problem is remote terraform state with s3 intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: remote backend, S3 state storage, state key.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-076-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-076-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Remote Terraform State with S3.', 'answer': 'remote backend, S3 state storage', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
