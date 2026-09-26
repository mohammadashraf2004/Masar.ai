"""Masar curriculum seed — L011-045."""

LESSON_META = {'lesson_id': 'L011-045', 'course_id': 'COURSE-011', 'module_id': 'M011-04', 'title': 'Building Clean, Traceable Commits', 'slug': 'building-clean-traceable-commits', 'status': 'approved', 'difficulty': 'intermediate-to-advanced', 'estimated_minutes': None, 'learning_objective': 'Apply building clean, traceable commits concepts to the deployment and operation of an existing production-oriented AI service.'}

TOPICS = ['focused staging', 'logical commits', 'commit messages', 'git diff and git log', 'conventional commit prefixes']

SOURCE_REFERENCES = ['Secondary DevOps source (source ID not provided) — Chapter 3: Mastering Version Control with Git and GitHub']

FIGURE_REFERENCES = []

LESSON_MARKDOWN = '# L011-045 — Building Clean, Traceable Commits\n\n## Learning objective\n\nApply building clean, traceable commits concepts to the deployment and operation of an existing production-oriented AI service.\n\n## Core topics\n\n- focused staging\n- logical commits\n- commit messages\n- git diff and git log\n- conventional commit prefixes\n\n## AI-engineering context\n\nUse these concepts to deploy or operate an **existing** FastAPI, LLM, RAG, or AI Agent service. Do not re-teach the application-domain fundamentals in this course.\n\n## Practice\n\nApply the lesson to a production-oriented AI backend and document the configuration, security boundary, validation method, and failure behavior relevant to this topic.\n\n## Assessment focus\n\nThe learner should be able to explain the purpose of the topic, configure or review the relevant deployment artifact, and diagnose a realistic failure without relying on trial-and-error console clicking.\n\n'

EXERCISES = [{'id': 'L011-045-EX1', 'title': 'Apply Building Clean, Traceable Commits', 'prompt': "Apply the lesson's concepts to an existing AI service. Cover at least: focused staging, logical commits, commit messages. Record the configuration or architecture decision and how you would validate it."}, {'id': 'L011-045-EX2', 'title': 'Failure and recovery exercise', 'prompt': 'Create or analyze one realistic failure related to building clean, traceable commits. Identify the observable symptom, likely cause, safe correction, and post-fix validation step.'}]

QUIZ = [{'id': 'L011-045-Q1', 'type': 'short_answer', 'question': 'What production problem is building clean, traceable commits intended to solve in an AI-service deployment?', 'answer': 'It addresses the deployment/operations concerns represented by: focused staging, logical commits, commit messages.', 'explanation': 'A correct answer should connect the concept to deployment reliability, security, repeatability, scalability, or operability rather than re-explaining AI application fundamentals.'}, {'id': 'L011-045-Q2', 'type': 'true_false', 'question': 'This lesson should be applied without considering security boundaries, failure behavior, or validation.', 'answer': False, 'explanation': 'Production deployment decisions must include security, failure handling, and verification.'}, {'id': 'L011-045-Q3', 'type': 'short_answer', 'question': 'Name two concrete topics covered by Building Clean, Traceable Commits.', 'answer': 'focused staging, logical commits', 'explanation': "The answer should use the lesson's declared core topics."}]

PROJECT = None
