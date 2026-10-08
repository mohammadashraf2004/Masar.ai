"""Complete legacy scaffolded exercises already present in a local database.

The old AI Developer seed data is no longer part of the source catalog, but
development databases can still contain those exercises and learner progress
that points at them.  This idempotent backfill preserves the rows, supplies
the missing reference implementations, and attaches deterministic grading.

Run from ``backend/`` with ``--apply`` to commit.  Without it the script audits
and rolls back after validating every official solution and untouched starter.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal
# Register every relationship target before SQLAlchemy configures mappers.
import app.models.user, app.models.learning, app.models.progress  # noqa: F401,E402
import app.models.community, app.models.wallet, app.models.auth_token  # noqa: F401,E402
import app.models.challenge, app.models.exam, app.models.tool_course  # noqa: F401,E402
from app.models.learning import Exercise
from app.services.code_grading import PythonGrader, TextGrader
from app.services.code_grading.authoring import (
    build_fill_in_blank_exercise,
    build_static_python_tests,
)


SOLUTION_OVERRIDES: dict[str, str] = {
    "Add a Fourth Action: Rewrite for Tone": '''if choice == "1":
    instruction = "Summarize the text briefly."
elif choice == "2":
    instruction = "Explain the text in very simple language."
elif choice == "3":
    instruction = "Translate the text to English."
elif choice == "4":
    instruction = "Rewrite the text in a clear, friendly tone while preserving its meaning."
else:
    print("Invalid choice.")
    exit()
''',
    "Trace and Implement a Calculator Tool": '''def multiply(a, b):
    return a * b


tool_definition = {
    "type": "function",
    "name": "multiply",
    "description": "Multiply two numbers and return the result.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"},
        },
        "required": ["a", "b"],
    },
}
''',
    "Build and Extend the Semantic Search Engine": '''from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    "Students must complete 160 credit hours to graduate.",
    "The minimum GPA required for graduation is 2.0.",
    "The cost of one credit hour is 1330 EGP.",
    "Students must register their courses before the registration deadline.",
    "The university library opens at 8 AM.",
    "Scholarship applications close at the end of September.",
    "Final exams begin in the first week of January.",
]

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
document_embeddings = model.encode(documents)

def semantic_search(query, top_k=3, threshold=0.60):
    query_embedding = model.encode(query)
    scores = cosine_similarity([query_embedding], document_embeddings)[0]
    ranked_indices = scores.argsort()[::-1]
    results = []
    for index in ranked_indices:
        score = float(scores[index])
        if score < threshold:
            continue
        results.append({"text": documents[index], "score": score})
        if len(results) >= top_k:
            break
    return results

example_queries = [
    "How much does a credit hour cost?",
    "What GPA do I need to graduate?",
    "When does the library open?",
    "How do I repair my car?",
    "When is the scholarship deadline?",
    "When do final exams start?",
]
query_results = {query: semantic_search(query) for query in example_queries}
''',
    "Sketch a Visual Support Pipeline": '''def diagnose_ui_issue(image, question):
    prompt = f"Inspect this UI screenshot and diagnose the issue: {question}"
    response = vlm.generate(image=image, prompt=prompt)
    return response


answer = diagnose_ui_issue(image, "Why is the submit button not working?")
print(answer)
# Production should add validation, confidence checks, monitoring, and human review.
''',
    "Object Detection vs VLM Output": '''detections = [
    {"object": "person", "box": [100, 50, 250, 400]},
    {"object": "car", "box": [300, 100, 600, 350]},
]

vlm_answer = "A person is standing beside a car in an outdoor scene."
# The VLM adds relationships and scene context that bounding boxes do not express.
''',
    "Design a Document Classification Router": '''def route_document(document):
    doc_type = classify_document(document)
    if doc_type == "invoice":
        return accounting_pipeline(document)
    if doc_type == "contract":
        return legal_pipeline(document)
    if doc_type == "resume":
        return recruitment_pipeline(document)
    raise ValueError(f"Unsupported document type: {doc_type}")
''',
    "Add a Confidence Gate to an OCR Pipeline": '''def gate_ocr_results(ocr_results, threshold=0.70):
    accepted = []
    needs_review = []
    for result in ocr_results:
        if result["confidence"] >= threshold:
            accepted.append(result)
        else:
            needs_review.append(result)
    return accepted, needs_review

# Low-confidence numeric fields should be reviewed because a plausible auto-correction can silently change meaning.
''',
    "Sketch a Streaming Voice Loop": '''def voice_loop_streaming():
    audio = record_audio()
    text = speech_to_text(audio)
    for partial_text in llm.stream(text):
        audio_chunk = text_to_speech(partial_text)
        play(audio_chunk)

# Speaking each partial chunk reduces time to first audio and perceived latency.
''',
    "Compute a Simple Word Error Rate": '''def word_error_rate(reference: list[str], hypothesis: list[str]) -> float:
    if not reference:
        return 0.0 if not hypothesis else 1.0
    previous = list(range(len(hypothesis) + 1))
    for i, expected in enumerate(reference, start=1):
        current = [i]
        for j, actual in enumerate(hypothesis, start=1):
            substitution = previous[j - 1] + (expected != actual)
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1
            current.append(min(substitution, insertion, deletion))
        previous = current
    return previous[-1] / len(reference)

example_wer = word_error_rate(
    ["I", "want", "to", "book", "a", "flight"],
    ["I", "want", "book", "a", "flight"],
)
''',
    "Separate Display Text from Speech Text": '''def format_for_speech(data: dict) -> str:
    return (
        f"The weather in {data['city']} is {data['condition'].lower()}, "
        f"with a temperature of {data['temperature']} degrees Celsius."
    )

# Display text can be compact and structured; speech should sound natural when read aloud.
''',
    "Route Retrieved Evidence by Modality": '''def build_multimodal_context(question: str, evidence: list[dict]) -> dict:
    context = {"question": question, "text": [], "image": [], "table": []}
    for item in evidence:
        modality = item.get("type")
        if modality in {"text", "image", "table"}:
            context[modality].append(item.get("content"))
    return context

# Rerank and cap evidence first to control cost and keep irrelevant context from distracting the VLM.
''',
    "Implement a Tool Risk Policy": '''TOOL_RISK = {
    "search_database": "low",
    "send_email": "medium",
    "make_payment": "high",
    "delete_file": "high",
}

def is_tool_allowed(tool_name: str, source: str) -> bool:
    risk = TOOL_RISK.get(tool_name, "high")
    if source == "image" and risk == "high":
        return False
    return risk == "low"
''',
    "Stub the Multimodal Assistant Router and State": '''def route_input(request):
    if request.get("image") is not None:
        return "vision"
    if request.get("audio") is not None:
        return "speech"
    return "text"

def handle_registration_request(image, text, student_id):
    extracted = vlm_extract(image, text)
    decision = agent_decide(extracted)
    evidence = retrieve_registration_policy(decision)
    courses = get_student_courses(student_id)
    answer = reason_over_context(extracted, evidence, courses)
    return answer
''',
}


def config_tests(exercise: Exercise) -> tuple[str, str, list[dict[str, Any]]] | None:
    feedback = {"en": "Add every required configuration entry.", "ar": "أضف جميع إدخالات الإعداد المطلوبة."}

    def blank(index: int, pattern: str, concept: str, concept_ar: str) -> dict[str, Any]:
        return {
            "id": f"blank_{index}", "type": "regex_all", "static": True,
            "patterns": [pattern],
            "feedback": {
                "en": f"Blank {index}: complete {concept}.",
                "ar": f"الفراغ {index}: أكمل {concept_ar}.",
            },
        }

    if exercise.title == "Write a Dockerfile for a FastAPI AI Service":
        starter = '''# project/Dockerfile
FROM ___

WORKDIR ___

COPY requirements.txt ___

RUN ___

COPY app ___

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        return "dockerfile", starter, [
            blank(1, r"^\s*FROM\s+python:3\.12-slim\s*$", "the Python base image", "صورة Python الأساسية"),
            blank(2, r"^\s*WORKDIR\s+/app\s*$", "the working directory", "مجلد العمل"),
            blank(3, r"^\s*COPY\s+requirements\.txt\s+\.?\s*$", "the dependency-copy destination", "وجهة نسخ الاعتماديات"),
            blank(4, r"^\s*RUN\s+pip\s+install\b.*-r\s+requirements\.txt\s*$", "the dependency installation command", "أمر تثبيت الاعتماديات"),
            blank(5, r"^\s*COPY\s+(?:app\s+\./app|\.\s+\.)\s*$", "the application-copy destination", "وجهة نسخ التطبيق"),
            {"id": "required_instructions", "type": "regex_all", "static": True, "feedback": feedback, "patterns": [
                r"^\s*FROM\s+python:3\.12-slim\s*$", r"^\s*WORKDIR\s+/app\s*$",
                r"^\s*COPY\s+requirements\.txt\s+\.?\s*$", r"^\s*RUN\s+pip\s+install\b.*-r\s+requirements\.txt\s*$",
                r"^\s*COPY\s+(?:app\s+\./app|\.\s+\.)\s*$", r"^\s*CMD\s+.*uvicorn.*0\.0\.0\.0.*8000.*$",
            ]},
            {"id": "cache_order", "type": "regex_ordered", "static": True, "feedback": feedback, "patterns": [
                r"COPY\s+requirements\.txt", r"RUN\s+pip\s+install", r"COPY\s+(?:app|\.)",
            ]},
            {"id": "no_baked_api_key", "type": "regex_none", "static": True, "feedback": {
                "en": "Do not bake API keys into the image.", "ar": "لا تضع مفاتيح API داخل الصورة.",
            }, "patterns": [r"^\s*(?:ENV|ARG)\s+\w*API_?KEY\b"]},
        ]
    if exercise.title == "Write a compose.yaml for a RAG Stack":
        starter = '''# compose.yaml
services:
  api:
    build: ___
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: ___
      QDRANT_URL: ___
    depends_on:
      - db
      - qdrant

  db:
    image: ___
    volumes:
      - postgres_data:/var/lib/postgresql/data

  qdrant:
    image: ___
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  postgres_data:
  qdrant_data:
'''
        return "yaml", starter, [
            blank(1, r"^\s{4}build\s*:\s*\.\s*$", "the API build context", "مسار بناء خدمة API"),
            blank(2, r"DATABASE_URL\s*:\s*postgresql://[^\s]*@db:5432/[^\s]+", "the database service URL", "رابط خدمة قاعدة البيانات"),
            blank(3, r"QDRANT_URL\s*:\s*http://qdrant:6333", "the Qdrant service URL", "رابط خدمة Qdrant"),
            blank(4, r"image\s*:\s*postgres:16", "the PostgreSQL image", "صورة PostgreSQL"),
            blank(5, r"image\s*:\s*qdrant/qdrant", "the Qdrant image", "صورة Qdrant"),
            {"id": "required_services", "type": "regex_all", "static": True, "feedback": feedback, "patterns": [
                r"^services\s*:", r"^\s{2}api\s*:", r"^\s{2}db\s*:", r"^\s{2}qdrant\s*:",
                r"build\s*:\s*\.?\s*$", r"8000:8000", r"DATABASE_URL\s*:", r"QDRANT_URL\s*:",
                r"depends_on\s*:", r"image\s*:\s*postgres:16", r"image\s*:\s*qdrant/qdrant",
                r"postgres_data:/var/lib/postgresql/data", r"qdrant_data:/qdrant/storage",
            ]},
            {"id": "service_hostnames", "type": "regex_none", "static": True, "feedback": {
                "en": "Use db and qdrant service names, not localhost.",
                "ar": "استخدم اسمي الخدمتين db وqdrant بدل localhost.",
            }, "patterns": [r"(?:DATABASE_URL|QDRANT_URL)[^\n]*localhost"]},
        ]
    return None


async def complete(*, apply: bool) -> tuple[int, list[str]]:
    db = SessionLocal()
    python_grader, text_grader = PythonGrader(), TextGrader()
    changed = 0
    problems: list[str] = []
    try:
        exercises = db.query(Exercise).filter(
            Exercise.starter_code.isnot(None), Exercise.starter_code != "",
        ).order_by(Exercise.id).all()
        for exercise in exercises:
            # Canonical course rows are synchronized by import_courses.py and
            # may depend on packages available only in the isolated runner.
            # This backfill is solely for source-less legacy/tool rows.
            if exercise.source_key:
                continue
            if exercise.exercise_type == "code_pending":
                continue
            if exercise.title in SOLUTION_OVERRIDES:
                exercise.solution_code = SOLUTION_OVERRIDES[exercise.title]
            config = config_tests(exercise)
            if config:
                language, starter, tests = config
                exercise.starter_code = starter
                exercise.hint = "Fill the five `___` fields, then submit the completed configuration."
                grader = text_grader
            elif exercise.exercise_type == "code" and exercise.grading_tests and exercise.solution_code:
                language = exercise.language or "python"
                tests = list(exercise.grading_tests)
                grader = python_grader if language == "python" else text_grader
            else:
                if not exercise.solution_code:
                    problems.append(f"{exercise.id} {exercise.title}: missing official solution")
                    continue
                try:
                    tests = build_static_python_tests(exercise.starter_code, exercise.solution_code)
                except (SyntaxError, ValueError) as exc:
                    problems.append(f"{exercise.id} {exercise.title}: cannot build Python tests ({exc})")
                    continue
                language, grader = "python", python_grader
            if language == "python":
                try:
                    starter, tests, labels = build_fill_in_blank_exercise(
                        exercise.starter_code or "", exercise.solution_code or "", tests,
                    )
                except (SyntaxError, ValueError) as exc:
                    problems.append(f"{exercise.id} {exercise.title}: cannot create blanks ({exc})")
                    continue
                exercise.starter_code = starter
                exercise.hint = (
                    "Fill the `___` expressions using the lesson concepts, then submit your completed program."
                )
                if not exercise.success_message:
                    concepts = ", ".join(label.replace("the ", "", 1) for label in labels[:3])
                    exercise.success_message = f"Correct! The missing expressions complete {concepts}."
            exercise.exercise_type = "code"
            exercise.language = language
            exercise.grading_tests = tests
            exercise.hint = exercise.hint or "Complete the missing fields, then submit your implementation."
            exercise.success_message = exercise.success_message or "Correct! Your implementation satisfies the required checks."
            solution = await grader.grade(exercise.solution_code or "", tests)
            starter = await grader.grade(exercise.starter_code or "", tests)
            if not solution.passed:
                problems.append(f"{exercise.id} {exercise.title}: official solution failed {solution.failed_test_id}")
                continue
            if starter.passed:
                problems.append(f"{exercise.id} {exercise.title}: untouched starter receives full marks")
                continue
            changed += 1
        if problems or not apply:
            db.rollback()
        else:
            db.commit()
        return changed, problems
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="commit the validated changes")
    args = parser.parse_args()
    changed, problems = asyncio.run(complete(apply=args.apply))
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    verb = "completed" if args.apply else "validated (dry run)"
    print(f"OK: {changed} existing code exercises {verb}; official solutions pass and starters fail")


if __name__ == "__main__":
    main()
