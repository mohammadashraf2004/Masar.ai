"""Masar curriculum seed — L011-005."""

LESSON_META = {'lesson_id': 'L011-005', 'course_id': 'COURSE-011', 'module_id': 'M011-01', 'title': 'Production Traffic Architecture Preview', 'slug': 'production-traffic-architecture-preview', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply production traffic architecture preview concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['direct VM access vs production ingress', 'load balancers', 'Nginx reverse proxy', 'DNS and HTTPS', 'subdomain-based service architecture']

SOURCE_REFERENCES = ['BOOK-011 Chapters 1, 4, 5, 6, 7, 8']

LESSON_MARKDOWN = ('# L011-005 — Production Traffic Architecture Preview\n'
                   '\n'
                   '## Learning objective\n'
                   '\n'
                   'Apply production traffic architecture preview concepts to the deployment and operation of an existing production-oriented AI service.\n'
                   '\n'
                   '## Core topics\n'
                   '\n'
                   '- direct VM access vs production ingress\n'
                   '- load balancers\n'
                   '- Nginx reverse proxy\n'
                   '- DNS and HTTPS\n'
                   '- subdomain-based service architecture\n'
                   '\n'
                   '{{figure:final-subdomain-infrastructure}}\n'
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

EXERCISES = [{'id': 'L011-005-EX1', 'title': 'Apply Production Traffic Architecture Preview', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: direct VM access vs production ingress, load balancers, Nginx reverse proxy. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-005-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to production traffic architecture preview. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-005-Q1', 'type': 'short_answer', 'question': 'What production problem is production traffic architecture preview intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: direct VM access vs production ingress, load balancers, Nginx reverse proxy.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-005-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-005-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Production Traffic Architecture Preview.', 'answer': 'direct VM access vs production ingress, load balancers', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
