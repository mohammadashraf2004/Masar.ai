"""`{{image:key}}` end to end: the course folder (manifest, English and Arabic bodies) -> validation -> the
lesson API -> the validation-only / import command line, and the tool that links a finished image to its
`[[IMAGE_NEEDED]]` request."""
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.models.course_asset import CourseAsset
from app.services.assets import store as asset_store
from app.services.content.lesson_blocks import FigureBlock, TextBlock, figure_keys, malformed_markers, split_lesson
from app.services.curriculum import arabic, images, importer, validate
from app.services.curriculum.assets import load_asset_manifest
from app.services.curriculum.loaders import load_course_dir
from app.services.curriculum.spec import CurriculumError
from app.services.learning.lesson_content import lesson_blocks
from seeds import curriculum as cfg
from tests.learning_fixtures import learn_catalog, learn_client, learn_db, logs_enabled, register  # noqa: F401
from tests.test_course_assets import JPEG, PNG

KEY = "transformer-flow"
EN = "# Transformers\n\nA model reads tokens.\n\n{{image:transformer-flow}}\n\nThe model predicts the next token.\n"
AR = ("# المحولات\n\nيقرأ النموذج الرموز.\n\n{{image:transformer-flow}}\n\nيتنبأ النموذج بالرمز التالي.\n")
ENTRY = {"file": "assets/M01/transformer-flow.png", "lesson": "M01.L01",
         "alt_en": "Transformer processing flow", "alt_ar": "تدفق المعالجة في Transformer",
         "caption_en": "Tokens flow through attention.", "caption_ar": "تتدفق الرموز عبر الانتباه."}


def _course(root: Path, *, en: str = EN, ar=AR, manifest=None, files=None, name="COURSE-777_Images") -> Path:
    """A consolidated-layout course folder with one lesson, one exercise, one question and (optionally) Arabic."""
    course = root / name
    (course / "modules").mkdir(parents=True)
    for rel, data in (files if files is not None else {"assets/M01/transformer-flow.png": PNG}).items():
        (course / rel).parent.mkdir(parents=True, exist_ok=True)
        (course / rel).write_bytes(data)
    (course / "course_manifest.json").write_text(json.dumps(
        {"course_id": "COURSE-777", "course_title": "Images", "prerequisites": []}), encoding="utf-8")
    (course / "module_quizzes.json").write_text(json.dumps({"schema_version": 1, "course_id": "COURSE-777", "modules": [
        {"module_id": "M777-01", "quiz_id": "QUIZ-M777-01", "question_sources": []}]}), encoding="utf-8")
    (course / "modules" / "module_01.py").write_text(
        "LESSON_CODE = 'M01.L01'\nMODULE_ORDER = 1\nMODULE_TITLE = 'Foundations'\nMODULE_DESCRIPTION = 'The base.'\n"
        f"TOPIC = {{'title': 'Transformers', 'order': 1, 'difficulty': 'beginner', "
        f"'lesson': {{'title': 'Transformers', 'content': {en!r}, 'estimated_minutes': 10}}, "
        "'exercises': [{'id': 'EX01', 'title': 'Try', 'description': 'Do it'}], "
        "'quiz': {'questions': [{'id': 'Q01', 'question': 'Ready?', 'options': ['Yes', 'No'], 'correct': 0}]}}\n",
        encoding="utf-8")
    manifest = {"version": 1, "assets": {KEY: ENTRY}} if manifest is None else manifest
    (course / "assets_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    if ar is not None:
        spec = load_course_dir(course)
        lesson = spec.lessons[0]
        questions = arabic.questions_by_lesson(spec)[lesson.lesson_id]
        (course / "ar").mkdir()
        (course / "ar" / "M01.L01.json").write_text(json.dumps({
            "schema_version": 1, "lesson_id": "M01.L01",
            "source_hash": arabic.source_hash(arabic.source_payload(lesson, questions)),
            "title": "المحولات", "exercises": [{"id": e.exercise_id, "title": "جرّب", "description": "نفّذ المهمة."} for e in lesson.exercises],
            "questions": [{"question": "هل أنت جاهز؟", "options": ["نعم", "لا"], "explanation": ""}],
        }, ensure_ascii=False), encoding="utf-8")
        (course / "ar" / "M01.L01.md").write_text(ar, encoding="utf-8")
    return course


def _snapshot(course: Path):
    return {p: p.read_bytes() for p in course.rglob("*") if p.is_file() and "__pycache__" not in p.parts}


def _load(course: Path):
    return load_course_dir(course)


def _problems(course: Path):
    spec = _load(course)
    return validate.problems_in_course(spec)


# ─── The marker ─────────────────────────────────────────────────────────────

def test_an_image_marker_and_a_marker_with_a_caption_are_both_recognised():
    blocks = split_lesson("a\n\n{{image:one}}\n\nb\n\n{{image:two|Only the small matrices are trained.}}\n\nc")
    assert blocks == [TextBlock("a"), FigureBlock("one"), TextBlock("b"),
                      FigureBlock("two", "Only the small matrices are trained."), TextBlock("c")]
    assert figure_keys("{{figure:old}}\n{{image:new}}") == ["old", "new"]  # the first spelling still works


@pytest.mark.parametrize("position", ["start", "middle", "end"])
def test_an_image_renders_exactly_where_its_marker_is_never_moved(position):
    body = {"start": "{{image:k}}\n\nfirst\n\nsecond", "middle": "first\n\n{{image:k}}\n\nsecond",
            "end": "first\n\nsecond\n\n{{image:k}}"}[position]
    kinds = ["image" if isinstance(b, FigureBlock) else b.content for b in split_lesson(body)]
    assert kinds == {"start": ["image", "first\n\nsecond"], "middle": ["first", "image", "second"],
                     "end": ["first\n\nsecond", "image"]}[position]


@pytest.mark.parametrize("line", [
    "see {{image:inline}} here",       # in the middle of a sentence
    "{{image:Upper-Case}}", "{{image:under_score}}", "{{image:}}", "{{image}}",
    "{{image:missing-brace}", "{{ image: spaced }}", "{{image:k|}}", "{{image:k|   }}",
    "{{image:k|caption with {braces}}}", "{{image:k||two bars}}x",
])
def test_a_malformed_image_token_is_reported_and_never_left_for_a_learner(line):
    assert malformed_markers(f"text\n\n{line}\n\nmore") != []
    assert not any(isinstance(b, FigureBlock) for b in split_lesson(f"text\n\n{line}\n\nmore"))


def test_template_syntax_in_code_or_prose_about_images_is_not_taken_for_a_marker():
    assert malformed_markers("```jinja\n{{ image.url }}\n```\n\nUse `{{ image_url }}` in the template.") == []
    assert malformed_markers("{{image:ok|A caption, with punctuation (and brackets) - fine.}}") == []


# ─── The course folder ──────────────────────────────────────────────────────

def test_a_valid_reference_in_both_languages_validates_and_is_counted(tmp_path):
    course = _course(tmp_path)
    spec = _load(course)
    assert validate.problems_in_course(spec) == [] and spec.arabic_problems == []
    assert images.references(spec) == [("M01.L01", "en", KEY), ("M01.L01", "ar", KEY)]
    report = images.report(spec)
    assert (report.found, report.referenced, report.missing, report.broken, report.unused) == (1, 1, 0, 0, 0)
    assert [w for w in validate.warnings([spec]) if "terms mentioned" not in w] == []  # (glossary notes are not about images)


def test_the_same_picture_serves_both_languages_with_their_own_alt_and_caption(tmp_path):
    spec = _load(_course(tmp_path))
    asset = {a.key: a for a in spec.assets}
    row = type("Row", (), {"key": KEY, "alt": asset[KEY].alt, "caption": asset[KEY].caption, "alt_ar": asset[KEY].alt_ar,
                           "caption_ar": asset[KEY].caption_ar, "figure_number": None, "width": 1, "height": 1})()
    lesson = spec.lessons[0]
    english = [b for b in lesson_blocks(lesson.content, {KEY: row}, "course-777", "en") if b["type"] == "image"][0]
    arabic_block = [b for b in lesson_blocks(lesson.content_ar, {KEY: row}, "course-777", "ar") if b["type"] == "image"][0]
    assert (english["alt"], english["caption"]) == ("Transformer processing flow", "Tokens flow through attention.")
    assert (arabic_block["alt"], arabic_block["caption"]) == ("تدفق المعالجة في Transformer", "تتدفق الرموز عبر الانتباه.")
    assert english["url"] == arabic_block["url"], "one physical image"
    assert spec.assets[0].storage_key == "COURSE-777_Images/assets/M01/transformer-flow.png"


def test_an_inline_caption_wins_over_the_manifest_and_may_be_translated(tmp_path):
    en = EN.replace("{{image:transformer-flow}}", "{{image:transformer-flow|Read it left to right.}}")
    ar = AR.replace("{{image:transformer-flow}}", "{{image:transformer-flow|اقرأه من اليسار إلى اليمين.}}")
    spec = _load(_course(tmp_path, en=en, ar=ar))
    assert validate.problems_in_course(spec) == [] and spec.arabic_problems == []
    row = type("Row", (), {"key": KEY, "alt": "a", "caption": "manifest", "alt_ar": "أ", "caption_ar": "بيان",
                           "figure_number": None, "width": 1, "height": 1})()
    lesson = spec.lessons[0]
    assert [b["caption"] for b in lesson_blocks(lesson.content, {KEY: row}, "c", "en") if b["type"] == "image"] == ["Read it left to right."]
    assert [b["caption"] for b in lesson_blocks(lesson.content_ar, {KEY: row}, "c", "ar") if b["type"] == "image"] == ["اقرأه من اليسار إلى اليمين."]


def test_missing_arabic_text_falls_back_to_the_english_and_back(tmp_path):
    row = type("Row", (), {"key": KEY, "alt": "English alt", "caption": None, "alt_ar": None, "caption_ar": "تعليق",
                           "figure_number": None, "width": None, "height": None})()
    block = lambda text, lang: [b for b in lesson_blocks(text, {KEY: row}, "c", lang) if b["type"] == "image"][0]
    assert block("{{image:transformer-flow}}", "ar")["alt"] == "English alt"
    assert block("{{image:transformer-flow}}", "en")["caption"] == "تعليق"
    only_arabic = SimpleNamespace(key=KEY, alt="", caption=None, alt_ar="وصف", caption_ar=None, figure_number=None, width=None, height=None)
    assert [b for b in lesson_blocks("{{image:transformer-flow}}", {KEY: only_arabic}, "c", "en") if b["type"] == "image"][0]["alt"] == "وصف"


def test_an_arabic_body_must_place_the_same_images_as_the_english(tmp_path):
    spec = _load(_course(tmp_path, ar=AR.replace("{{image:transformer-flow}}", "")))
    assert any("markers [] do not match" in p for p in spec.arabic_problems)


def test_an_unknown_key_is_a_blocking_problem_naming_the_lesson_and_key(tmp_path):
    problems = _problems(_course(tmp_path, en=EN.replace(KEY, "no-such-image"), ar=None))
    assert any("M01.L01" in p and "no-such-image" in p and "no corresponding asset" in p for p in problems), problems


def test_a_manifest_entry_whose_file_is_missing_is_blocking_and_counted(tmp_path):
    course = _course(tmp_path, files={})
    spec = _load(course)
    problems = validate.problems_in_course(spec)
    assert any("does not exist" in p for p in problems) and any("no corresponding asset" in p for p in problems)
    assert images.report(spec).missing == 1


def test_a_malformed_token_in_a_lesson_is_blocking(tmp_path):
    problems = _problems(_course(tmp_path, en=EN.replace("{{image:transformer-flow}}", "see {{image:transformer-flow}} here"), ar=None))
    assert any("not on a line of its own or is malformed" in p for p in problems)
    assert images.report(_load(_course(tmp_path / "again", en=EN.replace("{{image:transformer-flow}}", "{{image:}}"), ar=None))).broken == 1


def test_a_duplicate_key_is_blocking_in_both_manifest_spellings(tmp_path):
    listed = {"version": 1, "assets": [{"key": KEY, **ENTRY}, {"key": KEY, **ENTRY}]}
    assert any("duplicate key" in p for p in load_asset_manifest(_course(tmp_path / "a", manifest=listed, ar=None)).problems)
    # a map written with the same key twice: the JSON parser would silently keep the last, so the text is checked
    text = json.dumps({"version": 1, "assets": {KEY: ENTRY}})
    doubled = text[:-2] + ", " + json.dumps(KEY) + ": " + json.dumps(ENTRY) + "}}"
    course = _course(tmp_path / "b", ar=None)
    (course / "assets_manifest.json").write_text(doubled, encoding="utf-8")
    assert any("duplicate key" in p for p in load_asset_manifest(course).problems)


@pytest.mark.parametrize("file", ["../outside.png", "assets/../../outside.png", "/etc/passwd", "C:/Windows/x.png",
                                  "assets\\transformer-flow.png"])
def test_a_path_that_leaves_the_course_is_rejected(tmp_path, file):
    manifest = {KEY: {**ENTRY, "file": file}}
    loaded = load_asset_manifest(_course(tmp_path, manifest=manifest, ar=None))
    assert loaded.assets == [] and loaded.problems and "course folder" in loaded.problems[0]


def test_a_symlink_that_leaves_the_course_is_rejected(tmp_path):
    outside = tmp_path / "secret.png"
    outside.write_bytes(PNG)
    course = _course(tmp_path / "c", files={}, manifest={KEY: {**ENTRY, "file": "assets/link.png"}}, ar=None)
    (course / "assets").mkdir(exist_ok=True)
    try:
        os.symlink(outside, course / "assets" / "link.png")
    except (OSError, NotImplementedError):
        pytest.skip("symlinks are not available here")
    loaded = load_asset_manifest(course)
    assert loaded.assets == [] and "leaves the course folder" in loaded.problems[0]


def test_an_image_stored_outside_assets_is_a_warning_not_an_error(tmp_path):
    course = _course(tmp_path, manifest={KEY: {**ENTRY, "file": "flow.png"}}, files={"flow.png": PNG}, ar=None)
    loaded = load_asset_manifest(course)
    assert loaded.problems == [] and len(loaded.assets) == 1
    assert any("not under assets/" in w for w in loaded.warnings)


def test_an_image_for_an_unknown_lesson_is_blocking_but_a_missing_lesson_field_is_not(tmp_path):
    bad = _problems(_course(tmp_path / "a", manifest={KEY: {**ENTRY, "lesson": "M09.L09"}}, ar=None))
    assert any("belongs to lesson 'M09.L09'" in p for p in bad)
    free = _problems(_course(tmp_path / "b", manifest={KEY: {k: v for k, v in ENTRY.items() if k != "lesson"}}, ar=None))
    assert free == []


def test_unused_images_and_remaining_requests_are_warnings_only(tmp_path):
    en = "# T\n\nNo image here.\n\n[[IMAGE_NEEDED: a diagram | what | notice]]\n"
    spec = _load(_course(tmp_path, en=en, ar=None))
    assert validate.problems_in_course(spec) == []
    notes = validate.warnings([spec])
    assert any("unused asset" in n and KEY in n for n in notes)
    assert any("1 image requests are still authoring placeholders" in n for n in notes)
    report = images.report(spec)
    assert (report.found, report.referenced, report.unused, report.requests) == (1, 0, 1, 1)
    request_only = _load(_course(
        tmp_path / "request-only", en=en, ar=None,
        manifest={"version": 1, "assets": {}}, files={},
    ))
    assert images.report(request_only).interesting, "request-only courses must appear in the focused status report"
    validate.validate_courses([spec])  # does not raise


def test_a_missing_alt_text_and_one_picture_under_two_keys_are_warnings(tmp_path):
    manifest = {"a-one": {"file": ENTRY["file"]}, "a-two": {"file": ENTRY["file"], "alt_en": "x"}}
    loaded = load_asset_manifest(_course(tmp_path, manifest=manifest, ar=None))
    assert loaded.problems == [] and len(loaded.assets) == 2
    assert any("no alt text" in w for w in loaded.warnings)
    assert any("two keys for one picture" in w for w in loaded.warnings)


def test_a_file_dropped_into_assets_but_not_listed_is_a_warning(tmp_path):
    course = _course(tmp_path, ar=None, files={"assets/M01/transformer-flow.png": PNG, "assets/M01/forgotten.jpg": JPEG})
    assert any("forgotten.jpg" in w and "not in the manifest" in w for w in load_asset_manifest(course).warnings)


def test_both_manifest_spellings_and_the_old_alt_names_are_read(tmp_path):
    old = {"version": 1, "assets": [{"key": KEY, "file": ENTRY["file"], "alt": "Old alt", "caption": "Old caption"}]}
    a = load_asset_manifest(_course(tmp_path / "a", manifest=old, ar=None)).assets[0]
    assert (a.alt, a.caption, a.alt_ar) == ("Old alt", "Old caption", None)
    wrapped = load_asset_manifest(_course(tmp_path / "b", ar=None)).assets[0]
    bare = load_asset_manifest(_course(tmp_path / "c", manifest={KEY: ENTRY}, ar=None)).assets[0]
    assert wrapped.alt == bare.alt == "Transformer processing flow" and bare.lesson == "M01.L01"


def test_a_course_without_images_loads_and_validates_exactly_as_before(tmp_path):
    course = _course(tmp_path, en="# Plain\n\nNothing to see.\n", ar=None, manifest={}, files={})
    (course / "assets_manifest.json").unlink()
    spec = _load(course)
    assert spec.assets == [] and spec.asset_problems == [] and spec.asset_warnings == []
    assert validate.problems_in_course(spec) == [] and validate.warnings([spec]) == []
    assert not images.report(spec).interesting


# ─── The lesson API ─────────────────────────────────────────────────────────

def _import(learn_db, tmp_path, monkeypatch, **kwargs):
    course = _course(tmp_path, **kwargs)
    monkeypatch.setattr(asset_store, "_store", asset_store.LocalCourseAssetStore(tmp_path))
    from tests.curriculum_fixtures import make_spec
    spec = make_spec("COURSE-001")
    loaded = _load(course)
    spec.assets = loaded.assets
    spec.modules[0].lessons[0].content = loaded.lessons[0].content
    spec.modules[0].lessons[0].content_ar = loaded.lessons[0].content_ar
    definitions = {d["course_id"]: d for d in cfg.COURSE_DIRECTORY_COURSES}
    importer.import_course(learn_db, spec, definitions["COURSE-001"])
    learn_db.commit()


def _lesson(client, who):
    response = client.get("/api/v1/tool-courses/course-001", headers=who["headers"])
    assert response.status_code == 200, response.text
    return response.json()["topics"][0]["lessons"][0]


def test_the_api_serves_each_language_its_own_alt_and_caption_for_one_picture(learn_client, learn_db, learn_catalog, tmp_path, monkeypatch):
    _import(learn_db, tmp_path, monkeypatch)
    row = learn_db.query(CourseAsset).one()
    assert (row.alt, row.alt_ar, row.caption_ar) == ("Transformer processing flow", "تدفق المعالجة في Transformer", "تتدفق الرموز عبر الانتباه.")
    lesson = _lesson(learn_client, register(learn_client))
    english = [b for b in lesson["blocks"] if b["type"] == "image"][0]
    arabic_block = [b for b in lesson["blocks_ar"] if b["type"] == "image"][0]
    assert english["alt"] == "Transformer processing flow" and arabic_block["alt"] == "تدفق المعالجة في Transformer"
    assert english["url"] == arabic_block["url"]
    assert [b["type"] for b in lesson["blocks"]] == ["markdown", "image", "markdown"]
    assert "{{image" not in json.dumps(lesson["blocks"]) + json.dumps(lesson["blocks_ar"])
    for private in ("storage_key", "assets/M01", "COURSE-777_Images", "sha256"):
        assert private not in json.dumps(lesson)


def test_an_image_removed_after_import_shows_a_named_gap_never_the_raw_token(learn_client, learn_db, learn_catalog, tmp_path, monkeypatch):
    _import(learn_db, tmp_path, monkeypatch)
    learn_db.query(CourseAsset).delete()
    learn_db.commit()
    lesson = _lesson(learn_client, register(learn_client))
    assert [b["type"] for b in lesson["blocks"]] == ["markdown", "image_missing", "markdown"]
    assert lesson["blocks"][1] == {"type": "image_missing", "asset_key": KEY}
    assert "{{image" not in json.dumps(lesson["blocks"])


# ─── The command line: --validate-only and a normal import ─────────────────

class _NoDatabase(Exception):
    pass


@pytest.fixture()
def cli(monkeypatch, tmp_path):
    """`seeds/import_courses.py` with the course folders replaced by `tmp_path/<built by the test>`."""
    from seeds import import_courses

    def use(course: Path):
        monkeypatch.setattr(import_courses, "load_all_courses", lambda only=None: [load_course_dir(course)])
        monkeypatch.setattr(import_courses.validate, "validate_registry", lambda *a, **k: None)

    def no_database(*_a, **_k):
        raise _NoDatabase("the database was touched")

    monkeypatch.setattr(import_courses, "SessionLocal", no_database)
    monkeypatch.setattr(import_courses, "require_migrated_schema", no_database)
    return import_courses, use


def test_validate_only_checks_the_images_and_never_opens_the_database(cli, tmp_path, monkeypatch, capsys):
    import_courses, use = cli
    use(_course(tmp_path))
    monkeypatch.setattr("sys.argv", ["import_courses.py", "--validate-only"])
    import_courses.main()                                   # valid: returns, database untouched
    assert "Validated 1 courses" in capsys.readouterr().out

    use(_course(tmp_path / "broken", en=EN.replace(KEY, "no-such-image"), ar=None))
    with pytest.raises(SystemExit) as stopped:
        import_courses.main()
    assert stopped.value.code == 1
    assert "no-such-image" in capsys.readouterr().err


def test_a_normal_import_does_not_start_for_a_broken_image_reference(cli, tmp_path, monkeypatch, capsys):
    import_courses, use = cli
    use(_course(tmp_path, en=EN.replace(KEY, "no-such-image"), ar=None))
    monkeypatch.setattr("sys.argv", ["import_courses.py"])
    with pytest.raises(SystemExit) as stopped:
        import_courses.main()      # a _NoDatabase error here would mean it got past validation
    assert stopped.value.code == 1 and "nothing was imported" in capsys.readouterr().err


# ─── Linking a finished image to its request ────────────────────────────────

REQUEST = "[[IMAGE_NEEDED: transformer pipeline | tokens through attention | order of the steps]]"
OTHER = "[[IMAGE_NEEDED: training loop | forward, loss, backward | the cycle repeats]]"
EN_REQ = f"# Transformers\n\nA model reads tokens.\n\n{REQUEST}\n\nThen it predicts.\n\n{OTHER}\n"
AR_REQ = f"# المحولات\n\nيقرأ النموذج الرموز.\n\n{REQUEST}\n\nثم يتنبأ.\n\n{OTHER}\n"


@pytest.fixture()
def linking(tmp_path, monkeypatch):
    from seeds import link_images
    course = _course(tmp_path, en=EN_REQ, ar=AR_REQ)
    monkeypatch.setattr(link_images, "COURSES_ROOT", tmp_path)
    return link_images, course


def _link(link_images, marker, key=KEY, write=False):
    return link_images.apply_links([link_images.Link("COURSE-777", "M01.L01", str(marker), key)], write)


def test_the_link_tool_previews_without_writing(linking, capsys):
    link_images, course = linking
    before = _snapshot(course)
    assert _link(link_images, 1) == 0
    assert "would replace" in capsys.readouterr().out
    assert _snapshot(course) == before


def test_the_link_tool_replaces_exactly_one_marker_in_both_languages_and_keeps_the_translation_current(linking):
    link_images, course = linking
    assert _link(link_images, "pipeline", write=True) == 0          # a unique piece of the text selects it
    spec = _load(course)
    assert spec.lessons[0].content.count(f"{{{{image:{KEY}}}}}") == 1 and OTHER in spec.lessons[0].content
    assert REQUEST not in spec.lessons[0].content and REQUEST not in spec.lessons[0].content_ar
    assert spec.lessons[0].content_ar.count(f"{{{{image:{KEY}}}}}") == 1
    assert spec.arabic_problems == [] and not [w for w in spec.arabic_warnings if "older English" in w], "the Arabic file is still current"
    assert validate.problems_in_course(spec) == []


def test_an_arabic_file_that_was_already_stale_stays_stale(linking):
    link_images, course = linking
    path = course / "ar" / "M01.L01.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["source_hash"] = "0" * 64
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    assert _link(link_images, 1, write=True) == 0
    assert json.loads(path.read_text(encoding="utf-8"))["source_hash"] == "0" * 64


@pytest.mark.parametrize("marker, key, reason", [
    ("model", KEY, "no marker contains"),                       # no match
    ("IMAGE_NEEDED", KEY, "several markers contain"),           # ambiguous: never guessed
    (9, KEY, "no marker number 9"),
    (1, "not-in-manifest", "not in COURSE-777's assets_manifest.json"),
    (1, "Bad Key", "not a valid image key"),
])
def test_the_link_tool_refuses_what_it_cannot_do_unambiguously_and_changes_nothing(linking, capsys, marker, key, reason):
    link_images, course = linking
    before = _snapshot(course)
    assert _link(link_images, marker, key, write=True) == 1
    assert reason in capsys.readouterr().out
    assert _snapshot(course) == before


def test_the_link_tool_refuses_a_marker_inside_a_paragraph(tmp_path, monkeypatch, capsys):
    from seeds import link_images
    inline = f"# T\n\nSee {REQUEST} for the idea.\n"
    _course(tmp_path, en=inline, ar=None)
    monkeypatch.setattr(link_images, "COURSES_ROOT", tmp_path)
    assert _link(link_images, 1, write=True) == 1
    assert "not on a line of its own" in capsys.readouterr().out


def test_the_link_tool_puts_everything_back_if_validation_finds_a_new_problem(linking, monkeypatch, capsys):
    link_images, course = linking
    before = _snapshot(course)
    # the Arabic file loses its marker between planning and checking: the result must not stand
    real, calls = link_images.images.problems, []

    def after_the_change(course):
        calls.append(1)
        return real(course) + (["injected problem"] if len(calls) > 1 else [])   # 1st call = the baseline

    monkeypatch.setattr(link_images.images, "problems", after_the_change)
    assert _link(link_images, 1, write=True) == 1
    assert "REVERTED" in capsys.readouterr().out
    assert _snapshot(course) == before


# ─── Editing the Python source the English lives in ─────────────────────────

def test_a_marker_wrapped_over_several_string_literals_is_replaced_and_nothing_else_moves():
    from seeds.source_edit import replace_in_literals
    marker = "[[IMAGE_NEEDED: The agentic stack | Three layers: reasoning LLM, orchestration, and tools. | The LLM requests actions.]]"
    source = (
        'TOPIC = {"content": (\n'
        "    'Intro text.\\n'\n"
        "    '\\n'\n"
        "    '[[IMAGE_NEEDED: The agentic stack | Three layers: reasoning LLM, '\n"
        "    'orchestration, and tools. | The LLM requests actions.]]\\n'\n"
        "    '\\n'\n"
        "    'After the image.\\n'\n"
        "), 'other': 1}\n"
    )
    old, new = replace_in_literals(source, marker, "{{image:agentic-stack}}")
    edited = source.replace(old, new, 1)
    namespace = {}
    exec(edited, namespace)       # still valid Python
    assert namespace["TOPIC"]["content"] == "Intro text.\n\n{{image:agentic-stack}}\n\nAfter the image.\n"
    assert edited.startswith("TOPIC = {") and edited.endswith("), 'other': 1}\n")
    assert "'Intro text.\\n'" in edited and "'After the image.\\n'" in edited   # untouched lines stay as written


def test_two_markers_that_share_a_string_fragment_can_both_be_replaced():
    from seeds.source_edit import replace_in_literals
    a, b = "[[IMAGE_NEEDED: one | x | y]]", "[[IMAGE_NEEDED: two | x | y]]"
    source = f"X = ('{a}\\n\\n{b}\\n')\n"
    old, new = replace_in_literals(source, a, "{{image:one}}")
    source = source.replace(old, new, 1)
    old, new = replace_in_literals(source, b, "{{image:two}}")
    namespace = {}
    exec(source.replace(old, new, 1), namespace)
    assert namespace["X"] == "{{image:one}}\n\n{{image:two}}\n"


@pytest.mark.parametrize("source", ['X = r"""[[IMAGE_NEEDED: a | b | c]]"""\n', 'X = f"[[IMAGE_NEEDED: a | b | c]]{1}"\n'])
def test_text_in_a_raw_or_prefixed_literal_is_refused_not_guessed(source):
    from seeds.source_edit import SourceEditError, replace_in_literals
    with pytest.raises(SourceEditError):
        replace_in_literals(source, "[[IMAGE_NEEDED: a | b | c]]", "{{image:k}}")


def test_the_link_tool_handles_a_multi_line_marker_in_a_windows_line_ending_triple_quoted_module(tmp_path, monkeypatch):
    from seeds import link_images
    marker = "[[IMAGE_NEEDED: transformer pipeline |\nsteps in order |\nnotice the order]]"
    en = f"# Transformers\n\nA model reads tokens.\n\n{marker}\n\nThen it predicts.\n"
    course = _course(tmp_path, en=en, ar=None)
    module = course / "modules" / "module_01.py"
    # the way COURSE-008 is stored: the body as one triple-quoted string, saved with CRLF
    module.write_bytes((
        "LESSON_CODE = 'M01.L01'\nMODULE_ORDER = 1\nMODULE_TITLE = 'Foundations'\nMODULE_DESCRIPTION = 'The base.'\n"
        f'TOPIC = {{"title": "Transformers", "order": 1, "difficulty": "beginner", "lesson": {{"title": "Transformers", '
        f'"content": """{en}""", "estimated_minutes": 10}}, '
        '"exercises": [{"id": "EX01", "title": "Try", "description": "Do it"}], '
        '"quiz": {"questions": [{"id": "Q01", "question": "Ready?", "options": ["Yes", "No"], "correct": 0}]}}\n'
    ).replace("\n", "\r\n").encode("utf-8"))
    monkeypatch.setattr(link_images, "COURSES_ROOT", tmp_path)
    assert _link(link_images, "transformer pipeline", write=True) == 0
    spec = _load(course)
    assert "{{image:transformer-flow}}" in spec.lessons[0].content and "IMAGE_NEEDED" not in spec.lessons[0].content
    assert module.read_bytes().count(b"\r\n") == module.read_bytes().count(b"\n"), "line endings are kept"


# ─── The real course folders ────────────────────────────────────────────────

@pytest.fixture(scope="module")
def real_image_courses():
    from app.services.curriculum.loaders import load_all_courses
    return load_all_courses(only=[f"COURSE-{n:03d}" for n in range(8, 15)])


def test_every_linked_image_in_the_real_courses_is_in_both_languages_in_the_same_order(real_image_courses):
    placed = 0
    for course in real_image_courses:
        assert validate.problems_in_course(course) == [], course.course_id
        for lesson in course.lessons:
            english, arabic_keys = figure_keys(lesson.content), figure_keys(lesson.content_ar or "")
            assert english == arabic_keys, (course.course_id, lesson.lesson_id, english, arabic_keys)
            placed += len(english)
    assert placed >= 100, "the supplied images that could be matched with confidence are linked"


def test_linked_images_replaced_their_request_in_place_and_unlinked_requests_are_untouched(real_image_courses):
    for course in real_image_courses:
        report = images.report(course)
        assert (report.missing, report.broken) == (0, 0), course.course_id
        assert report.referenced + report.unused == report.found
        for lesson in course.lessons:
            blocks = split_lesson(lesson.content)
            # a linked image always has prose on at least one side: it was swapped into the text, not collected apart
            if any(isinstance(b, FigureBlock) for b in blocks):
                assert any(isinstance(b, TextBlock) for b in blocks), (course.course_id, lesson.lesson_id)


# ─── One marker, several images ─────────────────────────────────────────────

SECOND, THIRD = "second-image", "third-image"
THREE_IMAGES = {
    KEY: ENTRY, SECOND: {**ENTRY, "file": "assets/M01/second.png"}, THIRD: {**ENTRY, "file": "assets/M01/third.png"},
}
THREE_FILES = {"assets/M01/transformer-flow.png": PNG, "assets/M01/second.png": PNG, "assets/M01/third.png": PNG}


def _several(tmp_path, monkeypatch, en=EN_REQ, ar=AR_REQ):
    from seeds import link_images
    course = _course(tmp_path, en=en, ar=ar, manifest={"version": 1, "assets": THREE_IMAGES}, files=THREE_FILES)
    monkeypatch.setattr(link_images, "COURSES_ROOT", tmp_path)
    return link_images, course


def _keys_and_blocks(course):
    spec = _load(course)
    lesson = spec.lessons[0]
    return spec, figure_keys(lesson.content), figure_keys(lesson.content_ar or ""), split_lesson(lesson.content)


def test_one_marker_takes_several_images_as_consecutive_lines_in_both_languages(tmp_path, monkeypatch):
    link_images, course = _several(tmp_path, monkeypatch)
    link = link_images.Link("COURSE-777", "M01.L01", "transformer pipeline |", f"{KEY},{SECOND},{THIRD}")
    assert link_images.apply_links([link], True) == 0
    spec, english, arabic_keys, blocks = _keys_and_blocks(course)
    assert english == arabic_keys == [KEY, SECOND, THIRD], "same keys, same order, in both languages"
    kinds = [type(b).__name__ for b in blocks]
    assert kinds == ["TextBlock", "FigureBlock", "FigureBlock", "FigureBlock", "TextBlock", "AuthorMarkerBlock"], kinds   # the other request is still an authoring marker
    assert OTHER in spec.lessons[0].content, "the other request is untouched"
    assert validate.problems_in_course(spec) == [] and spec.arabic_problems == []
    # the lesson text around the images is exactly what it was
    assert spec.lessons[0].content.startswith("# Transformers\n\nA model reads tokens.\n\n{{image:transformer-flow}}\n{{image:second-image}}\n{{image:third-image}}\n\nThen it predicts.")


def test_several_images_in_a_windows_line_ending_triple_quoted_module(tmp_path, monkeypatch):
    link_images, course = _several(tmp_path, monkeypatch, ar=None)
    module = course / "modules" / "module_01.py"
    body = EN_REQ.replace(REQUEST, REQUEST.replace(" | ", " |\n"))   # a marker that itself spans lines
    module.write_bytes((
        "LESSON_CODE = 'M01.L01'\nMODULE_ORDER = 1\nMODULE_TITLE = 'Foundations'\nMODULE_DESCRIPTION = 'The base.'\n"
        'TOPIC = {"title": "Transformers", "order": 1, "difficulty": "beginner", "lesson": {"title": "Transformers", '
        f'"content": """{body}""", "estimated_minutes": 10}}, '
        '"exercises": [{"id": "EX01", "title": "Try", "description": "Do it"}], '
        '"quiz": {"questions": [{"id": "Q01", "question": "Ready?", "options": ["Yes", "No"], "correct": 0}]}}\n'
    ).replace("\n", "\r\n").encode("utf-8"))
    link = link_images.Link("COURSE-777", "M01.L01", "transformer pipeline |", f"{KEY},{SECOND}")
    assert link_images.apply_links([link], True) == 0
    _spec, english, _arabic, blocks = _keys_and_blocks(course)
    assert english == [KEY, SECOND] and [type(b).__name__ for b in blocks][1:3] == ["FigureBlock", "FigureBlock"]
    raw = module.read_bytes()
    assert raw.count(b"\r\n") == raw.count(b"\n"), "line endings are kept"


def test_images_can_be_added_after_one_that_is_already_linked(tmp_path, monkeypatch):
    link_images, course = _several(tmp_path, monkeypatch)
    first = link_images.Link("COURSE-777", "M01.L01", "transformer pipeline |", KEY)
    assert link_images.apply_links([first], True) == 0
    more = link_images.Link("COURSE-777", "M01.L01", "{{image:transformer-flow}}", f"{SECOND},{THIRD}")
    assert link_images.apply_links([more], True) == 0
    spec, english, arabic_keys, _blocks = _keys_and_blocks(course)
    assert english == arabic_keys == [KEY, SECOND, THIRD]
    assert validate.problems_in_course(spec) == []


def test_several_links_in_one_run_may_share_a_python_module(tmp_path, monkeypatch):
    link_images, course = _several(tmp_path, monkeypatch)
    links = [link_images.Link("COURSE-777", "M01.L01", "transformer pipeline |", f"{KEY},{SECOND}"),
             link_images.Link("COURSE-777", "M01.L01", "training loop |", THIRD)]
    assert link_images.apply_links(links, True) == 0
    _spec, english, arabic_keys, _blocks = _keys_and_blocks(course)
    assert english == arabic_keys == [KEY, SECOND, THIRD]


@pytest.mark.parametrize("keys, reason", [
    (f"{KEY},{KEY}", "already placed in this lesson"),
    (f"{KEY},not-in-manifest", "not in COURSE-777's assets_manifest.json"),
    (" , ", "no image key given"),
])
def test_a_list_of_keys_is_refused_whole_when_any_key_is_wrong(tmp_path, monkeypatch, capsys, keys, reason):
    link_images, course = _several(tmp_path, monkeypatch)
    before = _snapshot(course)
    assert link_images.apply_links([link_images.Link("COURSE-777", "M01.L01", "transformer pipeline |", keys)], True) == 1
    assert reason in capsys.readouterr().out
    assert _snapshot(course) == before


def test_an_image_already_in_the_lesson_is_not_placed_twice(tmp_path, monkeypatch, capsys):
    link_images, course = _several(tmp_path, monkeypatch)
    assert link_images.apply_links([link_images.Link("COURSE-777", "M01.L01", "transformer pipeline |", KEY)], True) == 0
    assert link_images.apply_links([link_images.Link("COURSE-777", "M01.L01", "training loop |", KEY)], True) == 1
    assert "already placed in this lesson" in capsys.readouterr().out


# ─── Placing images after the text that teaches them (no marker to swap) ────

PLAIN_EN = ("# Transformers\n\nA model reads tokens.\n\nIt can't skip a step.\n\n```python\nx = 1\ny = 2\n```\n\n"
            "Then it predicts.\n\n{{image:transformer-flow}}\n\nThe end.\n")
PLAIN_AR = ("# المحولات\n\nيقرأ النموذج الرموز.\n\nلا يمكنه تخطي خطوة.\n\n⟦CODE_0⟧\n\n"
            "ثم يتنبأ.\n\n{{image:transformer-flow}}\n\nالنهاية.\n")


def _plain(tmp_path, monkeypatch):
    return _several(tmp_path, monkeypatch, en=PLAIN_EN, ar=PLAIN_AR)


def _place(link_images, after, key, after_ar="", remove=""):
    return link_images.apply_links([link_images.Placement("COURSE-777", "M01.L01", after, key, after_ar, remove)], True)


def test_an_image_is_placed_after_the_block_that_teaches_it_in_both_languages(tmp_path, monkeypatch):
    link_images, course = _plain(tmp_path, monkeypatch)
    assert _place(link_images, "A model reads tokens.", SECOND, "يقرأ النموذج الرموز.") == 0
    spec, english, arabic_keys, _blocks = _keys_and_blocks(course)
    assert english == arabic_keys == [SECOND, KEY], "same keys in the same order in both languages"
    assert "A model reads tokens.\n\n{{image:second-image}}\n\nIt can't skip a step." in spec.lessons[0].content
    assert "يقرأ النموذج الرموز.\n\n{{image:second-image}}\n\nلا يمكنه" in spec.lessons[0].content_ar
    assert validate.problems_in_course(spec) == [] and spec.arabic_problems == []
    # nothing but the image line (and its blank line) was added
    assert spec.lessons[0].content.replace("{{image:second-image}}\n\n", "").rstrip("\n") == PLAIN_EN.rstrip("\n")


def test_an_image_can_follow_a_code_block_when_the_anchor_is_its_last_line(tmp_path, monkeypatch):
    link_images, course = _plain(tmp_path, monkeypatch)
    assert _place(link_images, "y = 2", SECOND, "⟦CODE_0⟧") == 0
    spec, english, arabic_keys, _blocks = _keys_and_blocks(course)
    assert english == arabic_keys == [SECOND, KEY]
    assert "x = 1\ny = 2\n```\n\n{{image:second-image}}\n\nThen it predicts." in spec.lessons[0].content
    assert spec.lessons[0].content.replace("{{image:second-image}}\n\n", "").rstrip("\n") == PLAIN_EN.rstrip("\n")
    assert validate.problems_in_course(spec) == [] and spec.arabic_problems == []


def test_images_follow_an_image_that_is_already_there_as_the_next_lines(tmp_path, monkeypatch):
    link_images, course = _plain(tmp_path, monkeypatch)
    assert _place(link_images, "{{image:transformer-flow}}", f"{SECOND},{THIRD}", "{{image:transformer-flow}}") == 0
    spec, english, arabic_keys, blocks = _keys_and_blocks(course)
    assert english == arabic_keys == [KEY, SECOND, THIRD]
    assert "{{image:transformer-flow}}\n{{image:second-image}}\n{{image:third-image}}\n\nThe end." in spec.lessons[0].content
    assert validate.problems_in_course(spec) == []


def test_an_image_can_be_moved_without_touching_its_neighbours(tmp_path, monkeypatch):
    link_images, course = _plain(tmp_path, monkeypatch)
    assert _place(link_images, "{{image:transformer-flow}}", SECOND, "{{image:transformer-flow}}") == 0
    assert _place(link_images, "It can't skip a step.", SECOND, "لا يمكنه تخطي خطوة.", remove=SECOND) == 0
    spec, english, arabic_keys, _blocks = _keys_and_blocks(course)
    assert english == arabic_keys == [SECOND, KEY]
    content = spec.lessons[0].content
    assert "It can't skip a step.\n\n{{image:second-image}}\n\n```python" in content
    assert "Then it predicts.\n\n{{image:transformer-flow}}\n\nThe end." in content, "the neighbour stayed where it was"
    assert content.replace("{{image:second-image}}\n\n", "").rstrip("\n") == PLAIN_EN.rstrip("\n")
    assert validate.problems_in_course(spec) == [] and spec.arabic_problems == []


@pytest.mark.parametrize("after, key, after_ar, remove, reason", [
    (".", SECOND, ".", "", "times, not once"),                             # not unique
    ("A model reads", SECOND, "يقرأ النموذج", "", "does not end a block"),        # stops in the middle of a line
    ("x = 1", SECOND, "x = 1", "", "not its last line"),                   # inside a code block
    ("A model reads tokens.", SECOND, "", "", "give `after_ar`"),                # the Arabic place is not named
    ("A model reads tokens.", SECOND, "غير موجود", "", "times, not once"),         # not in the Arabic file
    ("A model reads tokens.", KEY, "يقرأ النموذج الرموز.", "", "already placed in this lesson"),
    ("A model reads tokens.", SECOND, "يقرأ النموذج الرموز.", KEY, "would leave no image there"),   # nothing to move it beside
    ("A model reads tokens.", "not-in-manifest", "يقرأ النموذج الرموز.", "", "not in COURSE-777's assets_manifest.json"),
])
def test_a_placement_that_is_not_exact_is_refused_and_changes_nothing(tmp_path, monkeypatch, capsys, after, key, after_ar, remove, reason):
    link_images, course = _plain(tmp_path, monkeypatch)
    before = _snapshot(course)
    assert _place(link_images, after, key, after_ar, remove) == 1
    assert reason in capsys.readouterr().out
    assert _snapshot(course) == before


def test_a_placement_is_reverted_if_validation_finds_a_new_problem(tmp_path, monkeypatch, capsys):
    link_images, course = _plain(tmp_path, monkeypatch)
    before = _snapshot(course)
    real, calls = link_images.images.problems, []

    def after_the_change(spec):
        calls.append(1)
        return real(spec) + (["injected problem"] if len(calls) > 1 else [])

    monkeypatch.setattr(link_images.images, "problems", after_the_change)
    assert _place(link_images, "A model reads tokens.", SECOND, "يقرأ النموذج الرموز.") == 1
    assert "REVERTED" in capsys.readouterr().out
    assert _snapshot(course) == before
