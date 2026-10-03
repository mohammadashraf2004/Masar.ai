"""Masar curriculum seed — L011-009."""

LESSON_META = {'lesson_id': 'L011-009', 'course_id': 'COURSE-011', 'module_id': 'M011-01', 'title': 'Scaling Architecture: Images, Templates, Health Checks & Global Load Balancing', 'slug': 'scaling-architecture-images-templates-health-checks-and-global-load-balancing', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply scaling architecture: images, templates, health checks & global load balancing concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['reusable VM images', 'instance templates', 'managed instance groups', 'health checks and autohealing', 'autoscaling and multi-region/global load balancing']

SOURCE_REFERENCES = ['BOOK-011 Chapters 1, 4, 5, 6, 7, 8']

LESSON_MARKDOWN = ('# L011-009 — Scaling Architecture: Images, Templates, Health Checks & Global Load Balancing\n'
                   '\n'
                   '## Learning objective\n'
                   '\n'
                   'Apply scaling architecture: images, templates, health checks & global load balancing concepts to the deployment and operation of an existing production-oriented AI service.\n'
                   '\n'
                   '## Core topics\n'
                   '\n'
                   '- reusable VM images\n'
                   '- instance templates\n'
                   '- managed instance groups\n'
                   '- health checks and autohealing\n'
                   '- autoscaling and multi-region/global load balancing\n'
                   '\n'
                   'The autoscaling configuration below ties group size to an explicit utilization signal and capacity limits.\n'
                   '\n'
                   '{{figure:gcp-instance-group-autoscaling}}\n'
                   '\n'
                   '## AI-engineering context\n'
                   '\n'
                   'Use these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n'
                   '\n'
                   'Autohealing then needs a health check with thresholds that distinguish a transient miss from an unhealthy instance.\n'
                   '\n'
                   '{{figure:gcp-instance-group-health-check}}\n'
                   '\n'
                   '## Practice\n'
                   '\n'
                   'Apply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n'
                   '\n'
                   'Finally, verify how the public frontend and routing rules connect to the health-checked backend service.\n'
                   '\n'
                   '{{figure:gcp-global-load-balancer}}\n'
                   '\n'
                   '## Assessment focus\n'
                   '\n'
                   'The learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n'
                   '\n')

EXERCISES = [{'id': 'L011-009-EX1', 'title': 'Apply Scaling Architecture: Images, Templates, Health Checks & Global Load Balancing', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: reusable VM images, instance templates, managed instance groups. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-009-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to scaling architecture: images, templates, health checks & global load balancing. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-009-Q1', 'type': 'short_answer', 'question': 'What production problem is scaling architecture: images, templates, health checks & global load balancing intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: reusable VM images, instance templates, managed instance groups.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-009-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-009-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Scaling Architecture: Images, Templates, Health Checks & Global Load Balancing.', 'answer': 'reusable VM images, instance templates', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = {'id': 'M011-01-PROJECT', 'title': 'Cloud Foundation Architecture Lab', 'brief': "Integrate the module's lessons into a coherent AI-engineering deliverable for cloud & aws deployment foundations.", 'requirements': ['Use an existing AI workload rather than rebuilding FastAPI/LLM/RAG/Agent fundamentals.', 'Document architecture and security boundaries.', 'Demonstrate a working validation path.', 'Include at least one failure/recovery or rollback scenario.', 'Preserve stable course/module/lesson identifiers in any generated artifacts.']}
