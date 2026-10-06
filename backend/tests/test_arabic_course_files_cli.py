"""seeds/arabic_course_files.py - `skeleton`, `assemble` and `status` - on a throwaway copy of COURSE-001."""
import json
import shutil

import pytest

from app.services.curriculum import arabic
from app.services.curriculum.loaders import COURSES_ROOT, load_course_dir
from seeds import arabic_course_files as cli

REAL = next(p for p in COURSES_ROOT.iterdir() if p.name.startswith("COURSE-001"))
LESSON = "M01.L01"


@pytest.fixture()
def course(tmp_path, monkeypatch):
    """COURSE-001's English, with no Arabic, in a temp courses root the tool is pointed at."""
    root = tmp_path / "courses"
    shutil.copytree(REAL, root / REAL.name, ignore=shutil.ignore_patterns("ar", "__pycache__"))
    monkeypatch.setattr(cli, "COURSES_ROOT", root)
    return root / REAL.name


@pytest.fixture()
def drafts(tmp_path):
    """What a translator hands over: the body as a Markdown file, the rest as a small JSON file."""
    real = json.loads((REAL / "ar" / f"{LESSON}.json").read_text(encoding="utf-8"))
    body = tmp_path / "body.md"
    body.write_bytes((REAL / "ar" / f"{LESSON}.md").read_bytes())
    rest = tmp_path / "rest.json"
    rest.write_text(json.dumps({k: real[k] for k in ("title", "exercises", "questions")}, ensure_ascii=False), encoding="utf-8")
    return body, rest


def test_skeleton_prints_the_masked_english_and_a_template_with_no_body_key(course, capsys):
    assert cli.skeleton("COURSE-001", LESSON, write=False) == 0
    out = json.loads(capsys.readouterr().out)
    content = out["english"]["content"]
    # executable code is a placeholder; learner-facing `text` blocks are left in for the translator
    assert "⟦CODE_0⟧" in content and "⟦CODE_1⟧" not in content and "```python" not in content
    assert content.count("```text") == 18 and "Learning algorithm" in content
    assert "content" not in out["template"]
    assert len(out["template"]["questions"]) == len(out["english"]["questions"]) == 6
    assert out["template"]["source_hash"] == arabic.source_hash(out["english"])


def test_skeleton_write_makes_the_pair_and_never_overwrites_work(course):
    assert cli.skeleton("COURSE-001", LESSON, write=True) == 0
    target = course / "ar" / f"{LESSON}.md"
    assert target.read_text(encoding="utf-8") == "" and (course / "ar" / f"{LESSON}.json").is_file()

    target.write_text("عمل قيد التنفيذ", encoding="utf-8")
    assert cli.skeleton("COURSE-001", LESSON, write=True) == 1
    assert target.read_text(encoding="utf-8") == "عمل قيد التنفيذ"


def test_audit_lists_untagged_fences_and_text_blocks_that_look_like_code(course, capsys):
    # COURSE-001 as it is: no untagged fence, and two `text` blocks in M06 that are really Python
    assert cli.audit(["COURSE-001"]) == 0
    out = capsys.readouterr().out
    assert "UNTAGGED" not in out
    assert "text block that looks like code" in out and "scaler.fit(X_train)" in out

    # one fence loses its tag: the audit shows it and asks for a decision (non-zero exit)
    lesson = course / "lessons" / "lesson_01_what_is_machine_learning.py"
    source = lesson.read_text(encoding="utf-8")
    assert '"```text\\n"' in source
    lesson.write_text(source.replace('"```text\\n"', '"```\\n"', 1), encoding="utf-8")
    assert cli.audit(["COURSE-001"]) == 1
    assert "UNTAGGED" in capsys.readouterr().out


def test_assemble_writes_a_readable_md_and_a_json_without_the_body(course, drafts):
    body, rest = drafts
    assert cli.assemble("COURSE-001", LESSON, str(body), str(rest), force=False) == 0

    md = (course / "ar" / f"{LESSON}.md").read_text(encoding="utf-8")
    meta = json.loads((course / "ar" / f"{LESSON}.json").read_text(encoding="utf-8"))
    assert md.startswith("# ما هو Machine Learning") and md.count("\n") > 100 and md.endswith("\n")
    assert "⟦CODE_0⟧" in md
    assert set(meta) == {"schema_version", "lesson_id", "source_hash", "title", "exercises", "questions"}

    spec = load_course_dir(course)
    assert spec.arabic_problems == [] and spec.arabic_warnings == []
    lesson = next(l for l in spec.lessons if l.lesson_id == LESSON)
    assert lesson.content_ar.count("```") == lesson.content.count("```") and "⟦CODE" not in lesson.content_ar
    assert meta["source_hash"] == arabic.source_hash(arabic.source_payload(lesson, arabic.questions_by_lesson(spec)[LESSON]))


def test_assemble_refuses_to_replace_without_force(course, drafts, tmp_path):
    body, rest = drafts
    assert cli.assemble("COURSE-001", LESSON, str(body), str(rest), force=False) == 0
    changed = tmp_path / "changed.md"
    changed.write_text(body.read_text(encoding="utf-8") + "\nسطر إضافي\n", encoding="utf-8")

    assert cli.assemble("COURSE-001", LESSON, str(changed), str(rest), force=False) == 1
    assert "سطر إضافي" not in (course / "ar" / f"{LESSON}.md").read_text(encoding="utf-8")
    assert cli.assemble("COURSE-001", LESSON, str(changed), str(rest), force=True) == 0
    assert "سطر إضافي" in (course / "ar" / f"{LESSON}.md").read_text(encoding="utf-8")


def test_status_counts_what_is_translated_and_fails_on_a_broken_file(course, drafts, capsys):
    assert cli.status(["COURSE-001"]) == 0
    assert capsys.readouterr().out.split("\n")[1].split() == ["COURSE-001", "7", "0", "36", "0"]

    body, rest = drafts
    cli.assemble("COURSE-001", LESSON, str(body), str(rest), force=False)
    capsys.readouterr()  # the "wrote ..." line
    assert cli.status(["COURSE-001"]) == 0
    assert capsys.readouterr().out.split("\n")[1].split() == ["COURSE-001", "7", "1", "36", "6"]

    (course / "ar" / f"{LESSON}.md").write_text("لا شيفرة هنا", encoding="utf-8")
    assert cli.status(["COURSE-001"]) == 1
    out = capsys.readouterr().out
    assert "PROBLEMS" in out and "dropped 1 of 1 code placeholders" in out
