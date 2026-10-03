"""Masar curriculum seed — L011-081."""

LESSON_META = {'lesson_id': 'L011-081', 'course_id': 'COURSE-011', 'module_id': 'M011-06', 'title': 'Manual Production Deployment & Approval Gates', 'slug': 'manual-production-deployment-and-approval-gates', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply manual production deployment & approval gates concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['workflow_dispatch', 'manual production trigger', 'plan review', 'approve and deploy', 'safe production automation']

SOURCE_REFERENCES = ['Secondary DevOps source (source ID not provided) — Chapter 7: Automating Infrastructure with Terraform and CI/CD']

LESSON_MARKDOWN = ('# L011-081 — Manual Production Deployment & Approval Gates\n'
                   '\n'
                   '## Learning objective\n'
                   '\n'
                   'Apply manual production deployment & approval gates concepts to the deployment and operation of an existing production-oriented AI service.\n'
                   '\n'
                   '## Core topics\n'
                   '\n'
                   '- workflow_dispatch\n'
                   '- manual production trigger\n'
                   '- plan review\n'
                   '- approve and deploy\n'
                   '- safe production automation\n'
                   '\n'
                   '{{figure:production-approval}}\n'
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

EXERCISES = [{'id': 'L011-081-EX1', 'title': 'Apply Manual Production Deployment & Approval Gates', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: workflow_dispatch, manual production trigger, plan review. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-081-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to manual production deployment & approval gates. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-081-Q1', 'type': 'short_answer', 'question': 'What production problem is manual production deployment & approval gates intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: workflow_dispatch, manual production trigger, plan review.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-081-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-081-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Manual Production Deployment & Approval Gates.', 'answer': 'workflow_dispatch, manual production trigger', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
