"""The Arabic of a course lives in its ``ar/`` folder beside the English, is checked against that English,
and is imported with it - so a re-import never wipes it, and a bad file never gets in."""
import json
from pathlib import Path

import pytest

from app.models.learning import Exercise, Lesson, Quiz
from app.services.content.quiz_balance import rebalance_quiz
from app.services.curriculum import arabic, importer
from app.services.curriculum.arabic import attach_arabic
from app.services.curriculum.loaders import COURSES_ROOT, load_course_dir
from app.services.curriculum.spec import QuestionSpec
from app.services.language import arabic_review as R
from tests.curriculum_fixtures import make_spec
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.test_curriculum_import import DEFINITIONS

CODE = "```python\nmodel.fit(X, y)\n```"
# Learner-facing text blocks: a diagram, a block of variables, and a block that is only identifiers and numbers.
FLOW_EN = "```text\nData + examples\n      ↓\nLearning algorithm\n```"
FLOW_AR = "```text\nالبيانات + الأمثلة\n      ↓\nخوارزمية التعلّم (Learning algorithm)\n```"
VARS_EN = "```text\nX = information about the email\ny = spam or not spam\n```"
VARS_AR = "```text\nX = معلومات عن البريد الإلكتروني (email)\ny = بريد مزعج (spam) أو غير مزعج (not spam)\n```"
SHAPE = "```text\nX.shape = (10000, 12)\n```"
ENGLISH = (
    "# Learning\n\nA **model** learns from data. A model is trained on a dataset.\n\n"
    f"{CODE}\n\n{{{{exercise:E1}}}}\n\nThe workflow is:\n\n{FLOW_EN}\n\nFor one example:\n\n{VARS_EN}\n\n"
    f"The shape is:\n\n{SHAPE}\n\n| Email | Answer |\n|---|---|\n| Win a prize today | Spam |\n\n"
    "The dataset has features and a target. A feature describes a sample.\n"
)
ARABIC = (
    "# التعلّم\n\nيتعلّم الـ model من البيانات. يُدرَّب الـ model على dataset.\n\n"
    f"⟦CODE_0⟧\n\n{{{{exercise:E1}}}}\n\nسير العمل هو:\n\n{FLOW_AR}\n\nمثال واحد:\n\n{VARS_AR}\n\n"
    f"الشكل هو:\n\n{SHAPE}\n\n| البريد | الإجابة |\n|---|---|\n| اربح جائزة اليوم | Spam (مزعج) |\n\n"
    "يحتوي الـ dataset على features وعلى target. يصف الـ feature الـ sample.\n"
)


def _course(tmp_path: Path, lessons: int = 1):
    """A generated course whose first lesson has the content above, an exercise and three questions."""
    spec = make_spec("COURSE-001", modules=1, lessons=lessons)
    first = spec.modules[0].lessons[0]
    first.content = ENGLISH
    return spec, first


def _file(spec, lesson, **changes):
    questions = arabic.questions_by_lesson(spec)[lesson.lesson_id]
    body = {
        "schema_version": 1,
        "lesson_id": lesson.lesson_id,
        "source_hash": arabic.source_hash(arabic.source_payload(lesson, questions)),
        "title": "درس تجريبي",
        "exercises": [{"id": e.exercise_id, "title": f"تمرين {i}", "description": f"نفّذ المهمة {i}."}
                      for i, e in enumerate(lesson.exercises, 1)],
        "questions": [
            {"question": f"سؤال {i}؟", "options": [f"أ{i}", f"ب{i}", f"ج{i}", f"د{i}"], "explanation": f"شرح {i}."}
            for i, _ in enumerate(questions, 1)
        ],
    }
    body.update(changes)
    return body


def _attach(tmp_path, spec, lesson, body=ARABIC, **changes):
    """Write the lesson's `.json` (title, exercises, quiz) and its `.md` body, then load them."""
    folder = tmp_path / "ar"
    folder.mkdir(exist_ok=True)
    (folder / f"{lesson.lesson_id}.json").write_text(json.dumps(_file(spec, lesson, **changes), ensure_ascii=False), encoding="utf-8")
    if body is not None:
        (folder / f"{lesson.lesson_id}.md").write_text(body, encoding="utf-8")
    attach_arabic(spec, tmp_path)
    return spec


# ─── What a good file does ──────────────────────────────────────────────────

def test_a_good_file_attaches_with_the_english_code_put_back(tmp_path):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson)

    assert spec.arabic_problems == [] and spec.arabic_warnings == []
    assert lesson.title_ar == "درس تجريبي"
    assert CODE in lesson.content_ar and "⟦CODE" not in lesson.content_ar
    assert lesson.content == ENGLISH, "the English is never touched"
    assert [e.title_ar for e in lesson.exercises] == ["تمرين 1", "تمرين 2"]
    assert [q.ar["question"] for q in arabic.questions_by_lesson(spec)[lesson.lesson_id]] == ["سؤال 1؟", "سؤال 2؟", "سؤال 3؟"]


def test_a_course_without_an_ar_folder_is_simply_not_translated_yet(tmp_path):
    spec, lesson = _course(tmp_path)
    attach_arabic(spec, tmp_path)
    assert spec.arabic_problems == [] and lesson.content_ar is None and lesson.title_ar is None


def test_course_and_module_titles_come_from_the_course_file(tmp_path):
    spec, lesson = _course(tmp_path)
    (tmp_path / "ar").mkdir()
    (tmp_path / "ar" / "_course.json").write_text(json.dumps({
        "schema_version": 1, "course_id": "COURSE-001", "title": "أساسيات التعلّم الآلي",
        "modules": {spec.modules[0].module_id: {"title": "الوحدة الأولى", "description": "وصف الوحدة"}},
    }, ensure_ascii=False), encoding="utf-8")
    attach_arabic(spec, tmp_path)
    assert spec.arabic_problems == []
    assert spec.title_ar == "أساسيات التعلّم الآلي"
    assert (spec.modules[0].title_ar, spec.modules[0].description_ar) == ("الوحدة الأولى", "وصف الوحدة")


# ─── What a bad file must not do ────────────────────────────────────────────

@pytest.mark.parametrize("changes, expected", [
    ({"body": ARABIC.replace("⟦CODE_0⟧", "")}, "dropped 1 of 1 code placeholders"),
    ({"body": ARABIC.replace("⟦CODE_0⟧", "⟦CODE_0⟧\n\n⟦CODE_0⟧")}, "appear more than once"),
    ({"body": ARABIC.replace("⟦CODE_0⟧", "⟦CODE_0⟧\n\n⟦CODE_7⟧")}, "invented"),
    ({"body": ARABIC.replace("{{exercise:E1}}", "")}, "markers [] do not match"),
    ({"body": ARABIC.replace("{{exercise:E1}}", "{{exercise:E2}}")}, "do not match the English"),
    ({"body": ARABIC.replace("model", "نموذج").replace("dataset", "مجموعة بيانات")}, "no longer in English"),
    ({"body": ""}, "the body is empty"),
    ({"title": ""}, "title is empty"),
    ({"lesson_id": "L-OTHER"}, "does not match"),
    ({"schema_version": 2}, "schema_version"),
])
def test_a_file_that_does_not_line_up_with_the_english_is_a_problem_and_imports_nothing(tmp_path, changes, expected):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson, **changes)
    assert any(expected in p for p in spec.arabic_problems), spec.arabic_problems
    assert lesson.content_ar is None and lesson.title_ar is None


def test_every_question_must_line_up_with_the_english_one_by_position(tmp_path):
    spec, lesson = _course(tmp_path)
    good = _file(spec, lesson)["questions"]

    _attach(tmp_path, spec, lesson, questions=good[:2])
    assert any("2 questions against 3" in p for p in spec.arabic_problems)

    spec, lesson = _course(tmp_path)
    short = [dict(good[0], options=good[0]["options"][:3])] + good[1:]
    _attach(tmp_path, spec, lesson, questions=short)
    assert any("3 options against 4" in p for p in spec.arabic_problems)

    spec, lesson = _course(tmp_path)
    merged = [dict(good[0], options=["أ", "أ", "ج", "د"])] + good[1:]
    _attach(tmp_path, spec, lesson, questions=merged)
    assert any("became the same text" in p for p in spec.arabic_problems)

    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson, questions=[dict(good[0], explanation="")] + good[1:])
    assert any("has an explanation; the Arabic has none" in p for p in spec.arabic_problems)


def test_a_file_for_a_lesson_that_does_not_exist_is_reported(tmp_path):
    spec, lesson = _course(tmp_path)
    (tmp_path / "ar").mkdir()
    (tmp_path / "ar" / "L-NOPE.json").write_text("{}", encoding="utf-8")
    (tmp_path / "ar" / "L-NOPE.md").write_text("نص", encoding="utf-8")
    (tmp_path / "ar" / f"{lesson.lesson_id}.json").write_text("{ not json", encoding="utf-8")
    (tmp_path / "ar" / f"{lesson.lesson_id}.md").write_text(ARABIC, encoding="utf-8")
    attach_arabic(spec, tmp_path)
    assert any("no lesson 'L-NOPE'" in p for p in spec.arabic_problems)
    assert any("cannot be read as JSON" in p for p in spec.arabic_problems)


def test_the_json_and_the_md_must_come_as_a_pair(tmp_path):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson, body=None)
    assert any(".md beside it" in p for p in spec.arabic_problems), spec.arabic_problems
    assert lesson.content_ar is None and lesson.title_ar is None

    spec, lesson = _course(tmp_path)
    (tmp_path / "ar" / f"{lesson.lesson_id}.json").unlink()
    (tmp_path / "ar" / f"{lesson.lesson_id}.md").write_text(ARABIC, encoding="utf-8")
    attach_arabic(spec, tmp_path)
    assert any(".json beside it" in p for p in spec.arabic_problems), spec.arabic_problems
    assert lesson.content_ar is None


def test_the_body_does_not_belong_in_the_json_as_well(tmp_path):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson, content="a second copy of the body")
    assert any("has a 'content' key" in p for p in spec.arabic_problems)
    assert lesson.content_ar is None


def test_a_bom_and_windows_line_endings_change_nothing(tmp_path):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson)
    plain = lesson.content_ar

    spec, lesson = _course(tmp_path)
    (tmp_path / "ar" / f"{lesson.lesson_id}.md").write_bytes(("﻿" + ARABIC.replace("\n", "\r\n")).encode("utf-8"))
    attach_arabic(spec, tmp_path)
    assert spec.arabic_problems == []
    assert lesson.content_ar == plain, "the same text is stored whichever editor or checkout last saved the file"


def test_an_arabic_file_made_from_older_english_is_only_a_warning(tmp_path):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson, source_hash="0" * 64)
    assert spec.arabic_problems == []
    assert any("older English text" in w for w in spec.arabic_warnings)
    assert lesson.content_ar is not None, "a stale file is still shown; the warning says to re-check it"


def test_lowercase_react_verb_is_not_mistaken_for_the_react_framework():
    taught, mentioned = R.terminology_problems(
        "A service that must react instantly needs a different design.",
        "تحتاج الخدمة التي يجب أن تستجيب فوراً إلى تصميم مختلف.",
    )
    assert "React" not in taught and "React" not in mentioned


def test_capitalized_react_framework_still_has_to_remain_recognizable():
    taught, mentioned = R.terminology_problems(
        "React renders components for the browser.",
        "تعرض المكتبة المكوّنات في المتصفح.",
    )
    assert taught == [] and "React" in mentioned


def test_heading_hierarchy_and_order_are_structural_parity():
    result = R.review(
        "# Lesson\n\n## First\n\nText.\n\n### Detail\n\nText.",
        "# الدرس\n\n### الأول\n\nنص.\n\n## تفصيل\n\nنص.",
    )
    assert any("heading hierarchy/order" in problem for problem in result.problems)


def test_table_column_shape_is_structural_parity():
    result = R.review(
        "# Lesson\n\n| A | B |\n|---|---|\n| 1 | 2 |",
        "# الدرس\n\n| أ | ب |\n|---|---|\n| واحد |",
    )
    assert any("table shapes" in problem for problem in result.problems)


def test_table_shape_ignores_blank_lines_between_source_rows():
    result = R.review(
        "# Lesson\n\n| A | B |\n\n|---|---|\n\n| 1 | 2 |",
        "# الدرس\n\n| أ | ب |\n|---|---|\n| واحد | اثنان |",
    )
    assert not any("table shapes" in problem for problem in result.problems)


def test_code_cannot_be_translated_because_it_is_never_in_the_file(tmp_path):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson, body=ARABIC.replace("⟦CODE_0⟧", "```python\nنموذج.تدريب(X, y)\n```"))
    # An Arabic file that writes its own block has no placeholder left, which is already a problem.
    assert any("dropped 1 of 1 code placeholders" in p for p in spec.arabic_problems)


# ─── Code stays code; learner-facing text blocks are translated ──────────────

def test_only_executable_fences_are_masked_and_text_fences_stay_for_translation():
    masked, blocks = R.protect_code(ENGLISH)
    assert blocks == [CODE], "the python block is the only code block"
    assert "⟦CODE_0⟧" in masked and "⟦CODE_1⟧" not in masked
    assert FLOW_EN in masked and VARS_EN in masked and SHAPE in masked, "text blocks are left in the draft"


@pytest.mark.parametrize("info, is_text", [
    ("text", True), ("plaintext", True), ("txt", True), ("ascii", True), ("diagram", True), ("TEXT", True), ("", True),
    ("python", False), ("bash", False), ("json", False), ("yaml", False), ("javascript", False), ("dockerfile", False), ("sql", False),
])
def test_a_fence_is_text_or_code_by_its_info_string(info, is_text):
    assert R.is_text_fence(f"```{info}\nbody\n```") is is_text


def test_code_placeholders_are_numbered_over_code_only():
    english = "```text\na b c\n```\n\n```bash\nls\n```\n\n```text\nd e f\n```\n\n```python\nx = 1\n```\n"
    masked, blocks = R.protect_code(english)
    assert [R.fence_info(b) for b in blocks] == ["bash", "python"]
    assert "⟦CODE_0⟧" in masked and "⟦CODE_1⟧" in masked and "⟦CODE_2⟧" not in masked


def test_a_well_translated_lesson_passes_with_translated_text_blocks_and_identical_code(tmp_path):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson)
    assert spec.arabic_problems == [], spec.arabic_problems
    assert CODE in lesson.content_ar, "executable code is byte-identical"
    assert FLOW_AR in lesson.content_ar and FLOW_EN not in lesson.content_ar, "the diagram is Arabic"
    assert SHAPE in lesson.content_ar, "a block that is only an identifier and numbers needs no translation"


@pytest.mark.parametrize("body, expected", [
    # left in English: the exact failure of freezing every fence as code
    # (blocks are numbered over every fence: 1 is the python block, 2 the diagram, 3 the variables)
    (ARABIC.replace(FLOW_AR, FLOW_EN), "fenced block 2 (text): is learner-facing text that was left in English"),
    (ARABIC.replace(VARS_AR, VARS_EN), "fenced block 3 (text): is learner-facing text that was left in English"),
    # the diagram lost its shape, its arrow or its operator
    (ARABIC.replace("      ↓\n", ""), "fenced block 2 (text): has 2 lines against 3"),
    (ARABIC.replace("      ↓", "      ↑"), "the symbol"),
    (ARABIC.replace("البيانات + الأمثلة", "البيانات والأمثلة"), "the symbol '+' appears 0 times against 1"),
    # identifiers, variables and numbers are not translated
    # (a block with no words to translate may not change at all)
    (ARABIC.replace("X.shape = (10000, 12)", "X.شكل = (10000, 12)"), "has no words to translate"),
    (ARABIC.replace("(10000, 12)", "(١٠٠٠٠, ١٢)"), "has no words to translate"),
    (ARABIC.replace("X = معلومات", "س = معلومات"), "changed or lost: X"),
    (ARABIC.replace("y = بريد", "z = بريد"), "changed or lost: y"),
    # the fences themselves: kind and count
    (ARABIC.replace(VARS_AR, VARS_AR.replace("```text", "```python", 1)), "fenced blocks"),
    (ARABIC.replace(VARS_AR, "نص بلا كتلة"), "fenced blocks"),
    # a table cell or a sentence nobody translated
    (ARABIC.replace("اربح جائزة اليوم", "Win a prize today"), "left in English"),
    (ARABIC.replace("سير العمل هو:", "The workflow is the following one:"), "left in English"),
])
def test_text_blocks_and_prose_must_really_be_translated(tmp_path, body, expected):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson, body=body)
    assert any(expected in p for p in spec.arabic_problems), spec.arabic_problems
    assert lesson.content_ar is None


@pytest.mark.parametrize("body, expected", [
    # a line dropped, a bullet-like line dropped, two lines merged into one: each is caught in its own section
    (ARABIC.replace("الشكل هو:\n\n", ""), "lines against"),
    (ARABIC.replace("مثال واحد:\n\n", ""), "lines against"),
    # two English lines glued into one Arabic line
    (ARABIC.replace("مثال واحد:\n\n", "مثال واحد: "), "lines against"),
    (ARABIC.replace("الشكل هو:\n\n", "الشكل هو: "), "lines against"),
    (ARABIC.replace("يتعلّم الـ model من البيانات. يُدرَّب الـ model على dataset.\n\n", ""), "lines against"),
    (ARABIC.replace("\n\nيحتوي الـ dataset على features وعلى target. يصف الـ feature الـ sample.\n", "\n"), "lines against"),
    (ARABIC.replace("| اربح جائزة اليوم | Spam (مزعج) |\n", ""), "lines against"),
    (ARABIC + "\nسطر زائد لم يكن في الأصل.\n", "lines against"),
])
def test_nothing_may_be_omitted_merged_or_added(tmp_path, body, expected):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson, body=body)
    assert any(expected in p for p in spec.arabic_problems), spec.arabic_problems
    assert lesson.content_ar is None


def test_section_parity_reports_the_section_it_happened_in():
    english = "# One\n\nfirst line\n\nsecond line\n\n## Two\n\nonly line\n"
    assert R.section_parity_problems(english, "# واحد\n\nالسطر الأول\n\nالسطر الثاني\n\n## اثنان\n\nالسطر الوحيد\n") == []
    problems = R.section_parity_problems(english, "# واحد\n\nالسطران معًا\n\n## اثنان\n\nالسطر الوحيد\n")
    assert len(problems) == 1 and problems[0].startswith("section 1") and "2 lines against 3" in problems[0]
    # fenced blocks count as one line each, so translating a block's insides cannot hide a missing sentence
    assert R.sections("# T\n\n```text\na\nb\nc\n```\n\nafter\n")[-1][1] == 3


def test_exercise_and_quiz_text_left_in_english_is_a_problem(tmp_path):
    spec, lesson = _course(tmp_path)
    good = _file(spec, lesson)
    exercises = [dict(good["exercises"][0], description="Do the task of the lesson carefully")] + good["exercises"][1:]
    _attach(tmp_path, spec, lesson, exercises=exercises)
    assert any("was left in English" in p for p in spec.arabic_problems), spec.arabic_problems

    spec, lesson = _course(tmp_path)
    questions = [dict(good["questions"][0], question="Which option is the right one here?")] + good["questions"][1:]
    _attach(tmp_path, spec, lesson, questions=questions)
    assert any("question 1: some of it was left in English" in p for p in spec.arabic_problems), spec.arabic_problems


# ─── The importer ───────────────────────────────────────────────────────────

def test_the_twin_follows_the_english_when_the_importer_reorders_the_options():
    authored = [
        QuestionSpec("Which is right?", ["wrong one", "RIGHT", "wrong two", "wrong three"], 1, "Because.", "Q-1", "L1",
                     ar={"question": "أيها صحيح؟", "options": ["خطأ ١", "صحيح", "خطأ ٢", "خطأ ٣"], "explanation": "لأن."}),
    ]
    served, _ = rebalance_quiz("Quiz", [q.as_json() for q in authored])

    twin = importer._arabic_twin(authored, served)

    assert twin is not None
    english, shown = served[0], twin[0]
    # Whatever order the English ended up in, the Arabic option at the key is the Arabic of the right answer,
    # and the key itself is the English's, copied - not read from the Arabic.
    assert shown["correct"] == english["correct"]
    assert shown["options"][shown["correct"]] == "صحيح"
    assert english["options"][english["correct"]] == "RIGHT"
    pairs = dict(zip(authored[0].options, authored[0].ar["options"]))
    assert [pairs[o] for o in english["options"]] == shown["options"]
    assert shown["question"] == "أيها صحيح؟" and shown["lesson_id"] == "L1"


def test_a_quiz_is_translated_whole_or_not_at_all():
    done = QuestionSpec("A?", ["a", "b"], 0, "x", "Q-1", "L1", ar={"question": "أ؟", "options": ["١", "٢"], "explanation": "ش"})
    todo = QuestionSpec("B?", ["a", "b"], 0, "x", "Q-2", "L1")
    served = [q.as_json() for q in (done, todo)]
    assert importer._arabic_twin([done, todo], served) is None
    assert importer._arabic_twin([done], served[:1]) is not None


def test_arabic_is_imported_beside_the_english_and_survives_a_re_import(learn_db, learn_catalog, tmp_path):
    spec, lesson = _course(tmp_path, lessons=2)
    _attach(tmp_path, spec, lesson)
    other = spec.modules[0].lessons[1]
    # Only one of the module's two lessons is translated, so its quiz has no complete twin yet.
    importer.import_course(learn_db, spec, DEFINITIONS["COURSE-001"])
    learn_db.commit()

    row = learn_db.query(Lesson).filter(Lesson.source_key == f"COURSE-001/{lesson.lesson_id}").one()
    assert row.content == ENGLISH and CODE in row.content_ar and row.title == lesson.title and row.title_ar == "درس تجريبي"
    assert learn_db.query(Lesson).filter(Lesson.source_key == f"COURSE-001/{other.lesson_id}").one().content_ar is None
    exercise = learn_db.query(Exercise).filter(Exercise.lesson_id == row.id).order_by(Exercise.id).first()
    assert exercise.title_ar == "تمرين 1" and exercise.description_ar == "نفّذ المهمة 1." and exercise.description.startswith("Do task")
    assert learn_db.query(Quiz).filter(Quiz.source_key.like("COURSE-001/%")).one().questions_ar is None

    # A second run with the same folder changes nothing, and the Arabic is still there.
    again = importer.import_course(learn_db, spec, DEFINITIONS["COURSE-001"])
    learn_db.commit()
    assert again.lessons.updated == 0 and again.exercises.updated == 0 and again.quizzes.updated == 0
    learn_db.expire_all()
    assert "model" in learn_db.query(Lesson).filter(Lesson.id == row.id).one().content_ar


def test_a_fully_translated_module_gets_a_quiz_twin_that_grades_like_the_english(learn_db, learn_catalog, tmp_path):
    spec, lesson = _course(tmp_path, lessons=1)
    _attach(tmp_path, spec, lesson)
    importer.import_course(learn_db, spec, DEFINITIONS["COURSE-001"])
    learn_db.commit()

    quiz = learn_db.query(Quiz).filter(Quiz.source_key.like("COURSE-001/%")).one()
    assert len(quiz.questions_ar) == len(quiz.questions) == 3
    for english, shown in zip(quiz.questions, quiz.questions_ar):
        assert shown["correct"] == english["correct"] and len(shown["options"]) == len(english["options"])
        assert shown["question"].startswith("سؤال")
    assert quiz.title_ar is None, "the module has no Arabic title in this fixture"


def test_taking_the_arabic_out_of_the_folder_takes_it_out_of_the_catalogue(learn_db, learn_catalog, tmp_path):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson)
    importer.import_course(learn_db, spec, DEFINITIONS["COURSE-001"])
    learn_db.commit()

    plain, _ = _course(tmp_path)
    importer.import_course(learn_db, plain, DEFINITIONS["COURSE-001"])
    learn_db.commit()
    learn_db.expire_all()
    row = learn_db.query(Lesson).filter(Lesson.source_key == f"COURSE-001/{lesson.lesson_id}").one()
    assert row.content_ar is None, "the folder is the source of truth, as it is for the English"


# ─── The real course ────────────────────────────────────────────────────────

def test_course_001_arabic_loads_clean_and_keeps_every_code_block_and_marker():
    folder = next(p for p in COURSES_ROOT.iterdir() if p.name.startswith("COURSE-001"))
    lesson_files = sorted((folder / "ar").glob("M*.json"))
    assert lesson_files, "COURSE-001 has no lesson Arabic yet"
    for lesson_json in lesson_files:
        assert "content" not in json.loads(lesson_json.read_text(encoding="utf-8")), lesson_json.name
        body = lesson_json.with_suffix(".md")
        assert body.is_file() and body.read_text(encoding="utf-8").count("\n") > 20, f"{body.name} is a normal multi-line document"
    spec = load_course_dir(folder)
    assert spec.arabic_problems == [], spec.arabic_problems
    translated = [l for l in spec.lessons if l.content_ar]
    assert translated, "COURSE-001 has no Arabic yet"
    for lesson in translated:
        en_fences, ar_fences = R.fences(lesson.content), R.fences(lesson.content_ar)
        assert [R.fence_info(b) for b in ar_fences] == [R.fence_info(b) for b in en_fences], lesson.lesson_id
        for english, translated_block in zip(en_fences, ar_fences):
            if R.is_text_fence(english):
                # learner-facing: Arabic wherever the English has words to translate
                words = R.english_words(R._FENCE_PARTS.match(english).group(2))
                if words:
                    assert R._ARABIC.search(translated_block), (lesson.lesson_id, english)
            else:
                assert translated_block == english, "executable code is byte-identical"
        assert arabic._MARKER.findall(lesson.content_ar) == arabic._MARKER.findall(lesson.content)
        for exercise in lesson.exercises:
            assert exercise.title_ar and exercise.description_ar, (lesson.lesson_id, exercise.exercise_id)

    first = next(l for l in translated if l.lesson_id == "M01.L01")
    kinds = [R.fence_info(b) for b in R.fences(first.content)]
    assert kinds.count("python") == 1 and kinds.count("text") == 18, "M01.L01: one code block, eighteen text blocks"
    assert R.untranslated_lines(first.content_ar) == []


def test_course_001_is_translated_in_full_and_every_quiz_twin_keeps_its_key():
    spec = load_course_dir(next(p for p in COURSES_ROOT.iterdir() if p.name.startswith("COURSE-001")))
    assert spec.arabic_problems == [], spec.arabic_problems
    assert not [w for w in spec.arabic_warnings if "older English" in w], "a lesson was translated from older English"

    # every lesson, every exercise, the course and every module
    assert [l.lesson_id for l in spec.lessons if l.content_ar] == [l.lesson_id for l in spec.lessons] == [f"M0{n}.L01" for n in range(1, 8)]
    assert all(l.title_ar for l in spec.lessons)
    assert all(e.title_ar and e.description_ar for l in spec.lessons for e in l.exercises)
    assert spec.title_ar and all(m.title_ar and m.description_ar for m in spec.modules)

    # nothing is shorter, merged or left in English: the same sections, the same lines, no invisible characters
    for lesson in spec.lessons:
        assert R.section_parity_problems(lesson.content, lesson.content_ar) == [], lesson.lesson_id
        assert R.untranslated_lines(lesson.content_ar) == [], lesson.lesson_id
        assert R.invisible_characters(lesson.content_ar) == [], lesson.lesson_id
        code = [b for b in R.fences(lesson.content) if not R.is_text_fence(b)]
        assert [b for b in R.fences(lesson.content_ar) if not R.is_text_fence(b)] == code, lesson.lesson_id

    # every one of the 36 questions has a twin, and after the importer rebalances the options the Arabic
    # option at the key is still the Arabic of the English right answer
    checked = 0
    for module in spec.modules:
        quiz = module.quiz
        served, _ = rebalance_quiz(quiz.title, [q.as_json() for q in quiz.questions])
        twin = importer._arabic_twin(quiz.questions, served)
        assert twin is not None and len(twin) == len(served), module.module_id
        for question, english, shown in zip(quiz.questions, served, twin):
            checked += 1
            if question.is_open:
                continue
            assert shown["correct"] == english["correct"]
            assert len(shown["options"]) == len(english["options"])
            assert shown["options"][shown["correct"]] == question.ar["options"][question.correct], module.module_id
    assert checked == 36


@pytest.mark.parametrize("sentence, doubled", [
    # the page glosses glossary terms itself, so an author's own parenthetical doubles it
    ("طول متجه (vector) الـ features لديها 1.", True),
    ("أثناء التقييم (evaluation) نختبر.", True),
    ("ثم نحسب Evaluation (التقييم) للـ model.", True),
    ("هذا يعني (deployment) في الإنتاج.", True),
    # written once, in English, or with a parenthetical that is not a glossary term, is fine
    ("طول الـ vector الخاص بالـ features لديها 1.", False),
    ("أثناء الـ evaluation نختبر الـ model.", False),
    ("يستخدم (syntax) صياغة خاصة، ويُسمّى Sample (عيّنة).", False),
])
def test_a_glossary_term_is_written_once_because_the_page_glosses_it_itself(sentence, doubled):
    assert bool(R.glossary_doubling(sentence)) is doubled, R.glossary_doubling(sentence)


def test_the_arabic_phrases_the_page_swaps_for_glossary_terms_are_listed_for_review():
    found = R.arabic_replacements("تدرّب على مسار المعالجة المسبقة الصحيح. وفي الذاكرة نحفظ البيانات.")
    assert [(surface, term) for surface, term, _ in found] == [("مسار المعالجة", "Pipeline"), ("الذاكرة", "Memory")]
    assert "[[مسار المعالجة]] المسبقة" in found[0][2], "the context shows the word left dangling after the swap"
    assert R.arabic_replacements("طول الـ vector الخاص بالـ features") == [], "an English term is not a replacement"


def test_a_doubled_gloss_blocks_the_import(tmp_path):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson, body=ARABIC.replace("يتعلّم الـ model من البيانات.", "يتعلّم الـ model أثناء التقييم (evaluation) من البيانات."))
    assert any("gloss twice" in p for p in spec.arabic_problems), spec.arabic_problems
    assert lesson.content_ar is None


@pytest.mark.parametrize("char", ["‌", "​", "‏", " ", "‮"])
def test_invisible_characters_are_a_problem_in_the_body_and_in_the_json(tmp_path, char):
    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson, body=ARABIC.replace("يتعلّم الـ model", f"يتعلّم{char} الـ model"))
    assert any("invisible character" in p for p in spec.arabic_problems), spec.arabic_problems
    assert lesson.content_ar is None

    spec, lesson = _course(tmp_path)
    _attach(tmp_path, spec, lesson, title=f"درس{char} تجريبي")
    assert any("invisible character" in p for p in spec.arabic_problems), spec.arabic_problems


def test_an_image_request_may_contain_bracketed_text():
    """`[CLS]` or `[1, 4, 384]` inside an IMAGE_NEEDED request must not hide the marker from the parity
    check or make the whole line count as untranslated English."""
    marker = "[[IMAGE_NEEDED: Tokens | Show “Hello” becoming [CLS], Hello, [SEP] | Notice the [1, 4, 384] shape]]"
    assert arabic._MARKER.findall(f"قبل\n{marker}\nبعد") == [marker]
    assert not R.left_in_english(marker)
    other = marker.replace("Tokens", "Other")
    assert arabic._MARKER.findall(f"{marker}\n{other}") == [marker, other]


def test_an_image_request_may_be_wrapped_over_several_lines():
    """The 98 requests of COURSE-008 are wrapped over four lines; they are one marker, not four lines of prose."""
    marker = "[[IMAGE_NEEDED: Padding |\nShow a signal with padding around its borders |\nLearner should notice that [0, 0] values extend the signal]]"
    text = f"Intro text only here today.\n\n{marker}\n\nواحد."
    assert arabic._MARKER.findall(text) == [marker]
    # only the real prose line is reported; the lines of the wrapped request are not
    assert R.untranslated_lines(text) == ["Intro text only here today."]
    english = f"## A\n\nOne.\n\n{marker}\n\nTwo."
    arabic_text = f"## أ\n\nواحد.\n\n{marker}\n\nاثنان."
    assert R.section_parity_problems(english, arabic_text) == []
