"""Masar curriculum seed — L011-075."""

LESSON_META = {'lesson_id': 'L011-075', 'course_id': 'COURSE-011', 'module_id': 'M011-06', 'title': 'Terraform State — Why Infrastructure Needs Memory', 'slug': 'terraform-state-why-infrastructure-needs-memory', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply terraform state — why infrastructure needs memory concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['terraform.tfstate', 'code-to-resource mapping', 'ephemeral CI runners', 'local state limitations', 'collaborative state requirements']

SOURCE_REFERENCES = ['Secondary DevOps source (source ID not provided) — Chapter 7: Automating Infrastructure with Terraform and CI/CD']

LESSON_MARKDOWN = ('# L011-075 — Terraform State — Why Infrastructure Needs Memory\n'
                   '\n'
                   '## Learning objective\n'
                   '\n'
                   'Apply terraform state — why infrastructure needs memory concepts to the deployment and operation of an existing production-oriented AI service.\n'
                   '\n'
                   '## Core topics\n'
                   '\n'
                   '- terraform.tfstate\n'
                   '- code-to-resource mapping\n'
                   '- ephemeral CI runners\n'
                   '- local state limitations\n'
                   '- collaborative state requirements\n'
                   '\n'
                   '{{figure:terraform-state-flow}}\n'
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

EXERCISES = [{'id': 'L011-075-EX1', 'title': 'Apply Terraform State — Why Infrastructure Needs Memory', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: terraform.tfstate, code-to-resource mapping, ephemeral CI runners. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-075-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to terraform state — why infrastructure needs memory. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-075-Q1', 'type': 'short_answer', 'question': 'What production problem is terraform state — why infrastructure needs memory intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: terraform.tfstate, code-to-resource mapping, ephemeral CI runners.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-075-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-075-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Terraform State — Why Infrastructure Needs Memory.', 'answer': 'terraform.tfstate, code-to-resource mapping', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
