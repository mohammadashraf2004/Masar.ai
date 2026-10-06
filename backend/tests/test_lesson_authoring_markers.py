"""Authoring syntax in lesson bodies is never learner-facing.

`{{image:..}}`, `{{figure:..}}`, `{{exercise:..}}` and `[[IMAGE_NEEDED: ..]]` are parsed into typed blocks
(`app.services.content.lesson_blocks`) and turned into what a client may show by
`app.services.learning.lesson_content`. These tests pin that contract:

  * an unresolved image request is an author marker: a title in development, nothing in production;
  * an exercise marker is source metadata (the lesson page renders the lesson's exercises itself), validated
    against the lesson's exercises, and a diagnostic only when the lesson has none;
  * the stored Markdown keeps every marker (validators, `seeds/link_images.py` and the status tools read them);
  * Arabic readers get Arabic alt text and captions when the course wrote them, and say which language
    they are in when it did not.
"""
import json
import re
from types import SimpleNamespace

import pytest

from app.core.config import settings
from app.services.assets import store as asset_store
from app.services.content.lesson_blocks import (
    AuthorMarkerBlock, ExerciseBlock, FigureBlock, TextBlock, author_markers, exercise_ids, has_authoring_syntax,
    malformed_exercise_markers, split_lesson, strip_authoring,
)
from app.services.curriculum import images, importer, validate
from app.services.learning.lesson_content import lesson_blocks
from seeds import curriculum as cfg
from seeds.link_images import requests_in
from tests.learning_fixtures import learn_catalog, learn_client, learn_db, logs_enabled, register  # noqa: F401
from tests.test_lesson_images import AR, KEY, _course, _load

REQUEST = "[[IMAGE_NEEDED: Decomposition versus planning | Left: one goal breaking into subproblems | Notice the order]]"
WRAPPED = "[[IMAGE_NEEDED: Tokens | a [CLS] token and\n[1, 4, 384] shapes | Notice the batch]]"
RAW_TOKEN = re.compile(r"\{\{\s*(?:image|figure|exercise)|\[\[IMAGE_NEEDED", re.IGNORECASE)


def _row(**kwargs):
    base = dict(key=KEY, alt="Transformer processing flow", caption="Tokens flow through attention.",
                alt_ar="تدفق آلية Attention في Transformer", caption_ar="تتدفق الـ Tokens عبر طبقات Attention.",
                figure_number=None, width=10, height=10)
    base.update(kwargs)
    return SimpleNamespace(**base)


def _blocks(text, language="en", row=None, **kwargs):
    return lesson_blocks(text, {KEY: row or _row()}, "course-777", language, **kwargs)


def _types(blocks):
    return [b["type"] for b in blocks]


# ─── [[IMAGE_NEEDED]]: an author marker, never Markdown ─────────────────────

def test_an_image_request_is_recognised_as_an_author_marker_and_is_not_markdown():
    blocks = split_lesson(f"Before.\n\n{REQUEST}\n\n{WRAPPED}\n\nAfter.")
    assert [type(b).__name__ for b in blocks] == ["TextBlock", "AuthorMarkerBlock", "AuthorMarkerBlock", "TextBlock"]
    assert blocks[1].title == "Decomposition versus planning" and blocks[1].kind == "image_needed"
    assert "[CLS]" in blocks[2].text and "[1, 4, 384]" in blocks[2].text, "bracketed text and line wraps stay in one marker"
    assert not any("IMAGE_NEEDED" in b.content for b in blocks if isinstance(b, TextBlock))


def test_an_image_request_is_not_visible_to_a_learner_in_production():
    text = f"Before.\n\n{REQUEST}\n\nAfter."
    blocks = _blocks(text, production=True)
    assert _types(blocks) == ["markdown"], "the two runs of prose are one block again"
    assert blocks[0]["content"] == "Before.\n\nAfter."
    assert not RAW_TOKEN.search(json.dumps(blocks, ensure_ascii=False))
    assert "Decomposition" not in json.dumps(blocks), "not even its title"


def test_outside_production_an_author_sees_only_the_title_never_the_raw_marker():
    blocks = _blocks(f"Before.\n\n{REQUEST}\n\nAfter.", production=False)
    assert _types(blocks) == ["markdown", "author_marker", "markdown"]
    assert blocks[1] == {"type": "author_marker", "kind": "image_needed", "title": "Decomposition versus planning"}
    assert "IMAGE_NEEDED" not in json.dumps(blocks) and "Left: one goal" not in json.dumps(blocks)


def test_the_marker_stays_in_the_source_for_validators_and_the_linking_tool(tmp_path):
    text = f"Before.\n\n{REQUEST}\n\nAfter."
    _blocks(text, production=True)
    split_lesson(text)
    assert REQUEST in text and requests_in(text) == [REQUEST]
    spec = _load(_course(tmp_path, en=f"# T\n\n{REQUEST}\n", ar=None))
    assert REQUEST in spec.lessons[0].content and images.remaining_requests(spec) == {"M01.L01": 1}
    assert author_markers(spec.lessons[0].content)[0].title == "Decomposition versus planning"


def test_an_inline_or_unclosed_request_and_a_misspelt_marker_are_cut_out_of_the_prose():
    text = ("See [[IMAGE_NEEDED: inline | x | y]] for the idea.\n\n[[IMAGE_NEEDED: never closed | x\n\n"
            "Then {{image:Bad Key}} and {{ figure:x }} here.\n")
    shown = "".join(b.content for b in split_lesson(text) if isinstance(b, TextBlock))
    assert not RAW_TOKEN.search(shown), shown
    assert "for the idea." in shown and "here." in shown


def test_syntax_shown_inside_code_is_a_lesson_about_the_syntax_and_is_kept():
    text = ("Write the marker like this:\n\n```text\n{{image:key}}\n{{exercise:M01.L01.EX01}}\n"
            f"{REQUEST}\n```\n\nOr inline as `{{{{exercise:M01.L01.EX01}}}}` in prose.\n")
    assert split_lesson(text) == [TextBlock(text.strip("\n"))]
    assert strip_authoring(text) == text


# ─── {{exercise:..}} ────────────────────────────────────────────────────────

def test_an_exercise_marker_is_parsed_into_a_typed_block():
    blocks = split_lesson("Intro.\n\n{{exercise:M01.L02.EX04}}\n\nNext.")
    assert blocks == [TextBlock("Intro."), ExerciseBlock("M01.L02.EX04"), TextBlock("Next.")]
    assert exercise_ids("{{exercise:A.EX1}}\n\n{{exercise:A.EX2}}") == ["A.EX1", "A.EX2"]


def test_an_exercise_marker_is_never_rendered_as_text_and_the_prose_stays_one_flow():
    blocks = _blocks("Intro.\n\n{{exercise:M01.L02.EX04}}\n\nNext.", exercise_count=2, production=True)
    assert blocks == [{"type": "markdown", "content": "Intro.\n\nNext."}]
    assert "exercise" not in json.dumps(blocks)


def test_an_exercise_marker_in_a_lesson_with_no_exercise_is_a_diagnostic_outside_production_only():
    text = "Intro.\n\n{{exercise:M01.L02.EX04}}\n\nNext."
    dev = _blocks(text, exercise_count=0, production=False)
    assert _types(dev) == ["markdown", "exercise_missing", "markdown"]
    assert dev[1] == {"type": "exercise_missing", "exercise_id": "M01.L02.EX04"}
    prod = _blocks(text, exercise_count=0, production=True)
    assert prod == [{"type": "markdown", "content": "Intro.\n\nNext."}], "omitted for the learner"
    assert not RAW_TOKEN.search(json.dumps(prod) + json.dumps(dev))


def test_a_malformed_exercise_marker_is_reported_and_not_shown():
    text = "See {{exercise:M01.L01.EX01}} inline.\n\n{{exercise: spaced id}}\n\n{{exercise:ok.EX1}}\n"
    assert len(malformed_exercise_markers(text)) == 2
    shown = "".join(b.content for b in split_lesson(text) if isinstance(b, TextBlock))
    assert "{{" not in shown


def _lesson_with_exercise_markers(tmp_path, body_en, body_ar=None):
    return _load(_course(tmp_path, en=body_en, ar=body_ar))


def test_a_marker_for_an_exercise_the_lesson_has_is_valid_and_one_it_lacks_is_blocking(tmp_path):
    spec = _lesson_with_exercise_markers(tmp_path, "# T\n\n{{exercise:M01.L01.EX01}}\n\nText.\n")
    ids = [e.exercise_id for e in spec.lessons[0].exercises]
    assert ids and ids[0].endswith("M01.L01.EX01") or ids[0].endswith("EX01"), ids
    assert validate.exercise_marker_problems(spec) == []
    broken = _lesson_with_exercise_markers(tmp_path / "b", "# T\n\n{{exercise:M01.L01.EX09}}\n\nText.\n")
    problems = validate.exercise_marker_problems(broken)
    assert len(problems) == 1 and "references exercise 'M01.L01.EX09'" in problems[0] and "M01.L01" in problems[0]
    assert any("EX09" in p for p in validate.problems_in_course(broken)), "unknown exercise ids block the import"


def test_an_inline_exercise_marker_is_blocking_in_either_language(tmp_path):
    spec = _load(_course(tmp_path, en="# T\n\nA {{exercise:M01.L01.EX01}} inline.\n", ar=None))
    assert any("not on a line of its own" in p for p in validate.exercise_marker_problems(spec))


# ─── Images: tokens, Arabic metadata, fallback ──────────────────────────────

def test_an_image_token_is_never_rendered_literally_and_figure_is_still_accepted():
    for token in ("{{image:transformer-flow}}", "{{figure:transformer-flow}}", "  {{image:transformer-flow|A caption}}  "):
        blocks = _blocks(f"Before.\n\n{token}\n\nAfter.", production=True)
        assert _types(blocks) == ["markdown", "image", "markdown"], token
        assert not RAW_TOKEN.search(json.dumps(blocks)), token
    assert split_lesson("{{figure:a-b}}") == [FigureBlock("a-b")] == split_lesson("{{image:a-b}}")


def test_the_arabic_body_gets_the_arabic_alt_and_caption_and_the_english_body_the_english_ones():
    arabic = [b for b in _blocks("{{image:transformer-flow}}", "ar") if b["type"] == "image"][0]
    english = [b for b in _blocks("{{image:transformer-flow}}", "en") if b["type"] == "image"][0]
    assert arabic["alt"] == "تدفق آلية Attention في Transformer" and arabic["alt_lang"] == "ar"
    assert arabic["caption"] == "تتدفق الـ Tokens عبر طبقات Attention." and arabic["caption_lang"] == "ar"
    assert english["alt"] == "Transformer processing flow" and english["alt_lang"] == "en"
    assert english["caption"] == "Tokens flow through attention." and english["caption_lang"] == "en"
    assert arabic["url"] == english["url"], "one picture"


def test_mixed_arabic_and_english_technical_terms_reach_the_client_unchanged():
    caption = "يوضح الشكل كيف يحوّل Self-Attention الـ Embeddings إلى Context Vectors (انظر KV Cache)."
    block = [b for b in _blocks("{{image:transformer-flow}}", "ar", row=_row(caption_ar=caption)) if b["type"] == "image"][0]
    assert block["caption"] == caption and block["caption_lang"] == "ar"


def test_missing_localized_text_falls_back_and_says_which_language_it_is_in():
    only_english = _row(alt_ar=None, caption_ar=None)
    ar = [b for b in _blocks("{{image:transformer-flow}}", "ar", row=only_english) if b["type"] == "image"][0]
    assert (ar["alt"], ar["alt_lang"]) == ("Transformer processing flow", "en")
    assert (ar["caption"], ar["caption_lang"]) == ("Tokens flow through attention.", "en")
    only_arabic = _row(alt="", caption=None)
    en = [b for b in _blocks("{{image:transformer-flow}}", "en", row=only_arabic) if b["type"] == "image"][0]
    assert (en["alt_lang"], en["caption_lang"]) == ("ar", "ar")
    nothing = _row(alt_ar=None, caption_ar=None, caption=None)
    bare = [b for b in _blocks("{{image:transformer-flow}}", "ar", row=nothing) if b["type"] == "image"][0]
    assert bare["caption"] is None and bare["alt_lang"] == "en"


def test_a_caption_written_at_the_spot_is_in_the_language_of_the_lesson():
    block = [b for b in _blocks("{{image:transformer-flow|اقرأه من اليسار.}}", "ar") if b["type"] == "image"][0]
    assert block["caption"] == "اقرأه من اليسار." and block["caption_lang"] == "ar"


# ─── Order ──────────────────────────────────────────────────────────────────

def test_several_images_followed_by_an_exercise_keep_their_order():
    text = "{{image:a-one}}\n{{image:a-two}}\n{{image:a-three}}\n{{exercise:M01.L01.EX01}}\n"
    assert [type(b).__name__ for b in split_lesson(text)] == ["FigureBlock"] * 3 + ["ExerciseBlock"]
    rows = {k: _row(key=k) for k in ("a-one", "a-two", "a-three")}
    blocks = lesson_blocks(text, rows, "c", "en", exercise_count=1, production=True)
    assert [b["asset_key"] for b in blocks] == ["a-one", "a-two", "a-three"] and _types(blocks) == ["image"] * 3


def test_image_then_prose_then_exercise_keeps_that_order_and_hides_only_the_marker():
    text = "{{image:transformer-flow}}\n\nNow try it yourself.\n\n{{exercise:M01.L01.EX01}}\n"
    assert [type(b).__name__ for b in split_lesson(text)] == ["FigureBlock", "TextBlock", "ExerciseBlock"]
    blocks = _blocks(text, exercise_count=1, production=True)
    assert _types(blocks) == ["image", "markdown"] and blocks[1]["content"] == "Now try it yourself."


def test_a_body_without_authoring_syntax_is_left_alone():
    assert not has_authoring_syntax("# Plain\n\nNothing to see {{ image_url }} here.\n")
    assert _blocks("# Plain\n\nNothing to see {{ image_url }} here.\n") is None
    assert strip_authoring("a {{ image_url }} b") == "a {{ image_url }} b"


# ─── Arabic metadata of linked images: warnings, never blockers ─────────────

def _manifest_entry(**extra):
    from tests.test_lesson_images import ENTRY
    return {**ENTRY, **extra}


def test_a_linked_image_without_arabic_alt_or_caption_is_a_warning_and_not_a_problem(tmp_path):
    entry = _manifest_entry()
    entry.pop("alt_ar"), entry.pop("caption_ar")
    spec = _load(_course(tmp_path, manifest={"version": 1, "assets": {KEY: entry}}))
    assert validate.problems_in_course(spec) == []
    notes = [w for w in validate.warnings([spec]) if "alt_ar" in w or "caption_ar" in w]
    assert len(notes) == 2 and KEY in notes[0] and KEY in notes[1]
    report = images.report(spec)
    assert (report.missing_alt_ar, report.missing_caption_ar) == (1, 1)


def test_unlinked_or_english_only_images_are_not_asked_for_arabic_text(tmp_path):
    entry = _manifest_entry()
    entry.pop("alt_ar"), entry.pop("caption_ar")
    # placed only in the English body: no Arabic reader sees it
    spec = _load(_course(tmp_path, ar=AR.replace("{{image:transformer-flow}}\n\n", ""),
                         manifest={"version": 1, "assets": {KEY: entry}}))
    assert [w for w in validate.warnings([spec]) if "alt_ar" in w or "caption_ar" in w] == []
    unlinked = _load(_course(tmp_path / "u", en="# T\n\nText.\n", ar=None, manifest={"version": 1, "assets": {KEY: entry}}))
    assert [w for w in validate.warnings([unlinked]) if "alt_ar" in w] == []
    assert validate.problems_in_course(unlinked) == []


def test_a_linked_image_with_arabic_metadata_raises_no_warning(tmp_path):
    spec = _load(_course(tmp_path))
    assert [w for w in validate.warnings([spec]) if "alt_ar" in w or "caption_ar" in w] == []
    assert images.report(spec).missing_alt_ar == 0


# ─── The real courses ───────────────────────────────────────────────────────

def test_every_marker_in_the_real_courses_names_an_exercise_its_lesson_has():
    from app.services.curriculum.loaders import COURSES_ROOT, course_dirs, load_course_dir
    problems = []
    for directory in course_dirs(COURSES_ROOT):
        problems += validate.exercise_marker_problems(load_course_dir(directory))
    assert problems == []


def test_no_real_lesson_shows_authoring_syntax_to_a_learner_in_production():
    from app.services.curriculum.loaders import COURSES_ROOT, course_dirs, load_course_dir
    leaked = []
    for directory in course_dirs(COURSES_ROOT):
        course = load_course_dir(directory)
        assets = {a.key: SimpleNamespace(key=a.key, alt=a.alt, caption=a.caption, alt_ar=a.alt_ar, caption_ar=a.caption_ar,
                                         figure_number=None, width=None, height=None) for a in course.assets}
        for lesson in course.lessons:
            for text, language in ((lesson.content, "en"), (lesson.content_ar, "ar")):
                blocks = lesson_blocks(text, assets, course.course_id.lower(), language, exercise_count=1, production=True)
                if blocks is not None and RAW_TOKEN.search(json.dumps(blocks, ensure_ascii=False)):
                    leaked.append((course.course_id, lesson.lesson_id, language))
    assert leaked == []


def test_every_linked_image_in_the_real_courses_has_arabic_alt_and_caption():
    from app.services.curriculum.loaders import COURSES_ROOT, course_dirs, load_course_dir
    gaps = []
    for directory in course_dirs(COURSES_ROOT):
        course = load_course_dir(directory)
        no_alt, no_caption = images.arabic_metadata_gaps(course)
        gaps += [(course.course_id, k) for k in no_alt + no_caption]
    assert gaps == []


# ─── The API ────────────────────────────────────────────────────────────────

def _import_lesson(learn_db, tmp_path, monkeypatch, *, en, ar, exercises=True):
    course = _course(tmp_path, en=en, ar=ar)
    monkeypatch.setattr(asset_store, "_store", asset_store.LocalCourseAssetStore(tmp_path))
    from tests.curriculum_fixtures import make_spec
    spec = make_spec("COURSE-001")
    loaded = _load(course)
    spec.assets = loaded.assets
    lesson = spec.modules[0].lessons[0]
    lesson.content, lesson.content_ar = loaded.lessons[0].content, loaded.lessons[0].content_ar
    if not exercises:
        lesson.exercises = []
    definitions = {d["course_id"]: d for d in cfg.COURSE_DIRECTORY_COURSES}
    importer.import_course(learn_db, spec, definitions["COURSE-001"])
    learn_db.commit()


def _api_lesson(client, who):
    response = client.get("/api/v1/tool-courses/course-001", headers=who["headers"])
    assert response.status_code == 200, response.text
    return response.json()["topics"][0]["lessons"][0]


BODY_EN = (f"# Reflexion\n\nIt retries.\n\n{{{{image:{KEY}}}}}\n\nThen practise.\n\n{{{{exercise:M01.L01.EX01}}}}\n\n{REQUEST}\n")
BODY_AR = (f"# Reflexion\n\nيعيد المحاولة.\n\n{{{{image:{KEY}}}}}\n\nثم تمرّن.\n\n{{{{exercise:M01.L01.EX01}}}}\n\n{REQUEST}\n")


def test_the_lesson_api_never_sends_authoring_syntax_in_production(learn_client, learn_db, learn_catalog, tmp_path, monkeypatch):
    _import_lesson(learn_db, tmp_path, monkeypatch, en=BODY_EN, ar=BODY_AR)
    monkeypatch.setattr(type(settings), "is_production", property(lambda self: True))
    lesson = _api_lesson(learn_client, register(learn_client))
    for field in ("blocks", "blocks_ar"):
        shown = json.dumps(lesson[field], ensure_ascii=False)
        assert not RAW_TOKEN.search(shown), shown
        assert _types(lesson[field]) == ["markdown", "image", "markdown"], lesson[field]
    arabic = [b for b in lesson["blocks_ar"] if b["type"] == "image"][0]
    assert arabic["alt"] == "تدفق المعالجة في Transformer" and arabic["alt_lang"] == "ar"
    # the readable Markdown fields carry no source marker either, and keep everything a learner reads
    for field, expected in (("content", "# Reflexion\n\nIt retries.\n\nThen practise."),
                            ("content_ar", "# Reflexion\n\nيعيد المحاولة.\n\nثم تمرّن.")):
        assert not RAW_TOKEN.search(lesson[field]), lesson[field]
        assert lesson[field].strip() == expected, repr(lesson[field])


def test_the_lesson_api_shows_an_author_only_note_in_development_and_a_diagnostic_for_a_missing_exercise(learn_client, learn_db, learn_catalog, tmp_path, monkeypatch):
    _import_lesson(learn_db, tmp_path, monkeypatch, en=BODY_EN, ar=BODY_AR, exercises=False)
    monkeypatch.setattr(type(settings), "is_production", property(lambda self: False))
    lesson = _api_lesson(learn_client, register(learn_client))
    assert _types(lesson["blocks"]) == ["markdown", "image", "markdown", "exercise_missing", "author_marker"]
    assert lesson["blocks"][3]["exercise_id"] == "M01.L01.EX01"
    assert not RAW_TOKEN.search(json.dumps(lesson["blocks"]) + json.dumps(lesson["blocks_ar"]))


def test_the_development_api_keeps_the_source_in_content_for_authors(learn_client, learn_db, learn_catalog, tmp_path, monkeypatch):
    _import_lesson(learn_db, tmp_path, monkeypatch, en=BODY_EN, ar=BODY_AR)
    monkeypatch.setattr(type(settings), "is_production", property(lambda self: False))
    lesson = _api_lesson(learn_client, register(learn_client))
    for field in ("content", "content_ar"):
        assert "{{exercise:M01.L01.EX01}}" in lesson[field] and f"{{{{image:{KEY}}}}}" in lesson[field]
        assert "[[IMAGE_NEEDED:" in lesson[field]


def test_production_content_blocks_and_both_languages_are_free_of_every_marker(learn_client, learn_db, learn_catalog, tmp_path, monkeypatch):
    _import_lesson(learn_db, tmp_path, monkeypatch, en=BODY_EN, ar=BODY_AR)
    monkeypatch.setattr(type(settings), "is_production", property(lambda self: True))
    lesson = _api_lesson(learn_client, register(learn_client))
    everything = json.dumps({k: lesson[k] for k in ("content", "content_ar", "blocks", "blocks_ar")}, ensure_ascii=False)
    for needle in ("{{image:", "{{figure:", "{{exercise:", "[[IMAGE_NEEDED"):
        assert needle not in everything, needle


# ─── The shared sanitizer (`learner_markdown`) ──────────────────────────────

from app.services.content.lesson_blocks import learner_markdown  # noqa: E402

MIXED = ("# Title\n\nIntro line.\n\n{{image:a-b}}\n{{image:c-d|cap}}\n\nText with {{exercise:X.EX1}} inline.\n\n"
         "{{exercise:M01.L01.EX01}}\n\n[[IMAGE_NEEDED: t | x\ny | z]]\n\n```text\n{{image:keep}}\n[[IMAGE_NEEDED: keep]]\n```\n\n"
         "- item\n\n{{exercise:M01.L01.EX02}}\n")


def test_learner_markdown_drops_authoring_lines_and_keeps_every_other_character():
    cleaned = learner_markdown(MIXED)
    assert cleaned == ("# Title\n\nIntro line.\n\nText with  inline.\n\n"
                       "```text\n{{image:keep}}\n[[IMAGE_NEEDED: keep]]\n```\n\n- item\n\n")
    # the syntax a lesson shows inside code is the lesson's own text, and is kept
    assert "{{image:keep}}" in cleaned and "[[IMAGE_NEEDED: keep]]" in cleaned
    assert MIXED.startswith("# Title"), "the input is not modified"


def test_learner_markdown_leaves_a_body_without_authoring_syntax_untouched_and_never_empties_one():
    plain = "# Plain\n\nA {{ image_url }} template.\n\n```python\nx = 1\n```\n"
    assert learner_markdown(plain) is plain
    assert learner_markdown("") == "" and learner_markdown(None) is None
    assert learner_markdown("{{image:a}}\n\nFirst paragraph.\n") == "First paragraph.\n"
    assert learner_markdown("Only text\n\n{{exercise:A.EX1}}\n") .strip() == "Only text"
    assert learner_markdown("Before\n{{image:a}}\nAfter\n") == "Before\nAfter\n"


def test_learner_markdown_treats_arabic_bodies_the_same_way():
    arabic = "# المحولات\n\nيقرأ النموذج الرموز.\n\n{{image:transformer-flow}}\n\nثم يتنبأ.\n\n{{exercise:M01.L01.EX01}}\n\n" + REQUEST + "\n"
    assert learner_markdown(arabic).strip() == "# المحولات\n\nيقرأ النموذج الرموز.\n\nثم يتنبأ."
    assert not RAW_TOKEN.search(learner_markdown(arabic))


def test_learner_markdown_removes_internal_course_and_source_metadata_in_both_languages():
    english = (
        "# Lesson\n\n> **Course:** Internal course name  \n> **Lesson:** M01.L01  \n"
        "> **Module:** Internal module  \n> **Source alignment:** BOOK-001, Chapter 1.\n\n---\n\nLearner prose.\n"
    )
    arabic = (
        "# الدرس\n\n> **المقرر:** اسم المقرر الداخلي  \n> **الدرس:** M01.L01  \n"
        "> **الوحدة:** الوحدة الداخلية  \n> **مواءمة المصدر:** BOOK-001، الفصل 1.\n\n---\n\nنص المتعلم.\n"
    )
    assert learner_markdown(english) == "# Lesson\n\n---\n\nLearner prose.\n"
    assert learner_markdown(arabic) == "# الدرس\n\n---\n\nنص المتعلم.\n"


def test_source_metadata_shown_as_code_is_preserved():
    shown = "```markdown\n> **Source alignment:** an example\n```\n"
    assert learner_markdown(shown) == shown


def test_the_real_courses_serialize_to_learner_markdown_without_a_marker():
    from app.services.curriculum.loaders import COURSES_ROOT, course_dirs, load_course_dir
    leaked, emptied = [], []
    for directory in course_dirs(COURSES_ROOT):
        course = load_course_dir(directory)
        for lesson in course.lessons:
            for text in (lesson.content, lesson.content_ar):
                if not text:
                    continue
                cleaned = learner_markdown(text)
                if RAW_TOKEN.search(cleaned):
                    leaked.append((course.course_id, lesson.lesson_id))
                if len(cleaned.strip()) < 0.5 * len(strip_authoring(text).strip()):
                    emptied.append((course.course_id, lesson.lesson_id))
    assert leaked == [] and emptied == []


def test_the_real_courses_do_not_serialize_internal_source_metadata_to_learners():
    from app.services.curriculum.loaders import COURSES_ROOT, course_dirs, load_course_dir
    metadata = re.compile(
        r"^(?:>\s*)?(?:\*\*)?(?:Course|Lesson|Module|Source alignment|"
        r"المقرر|الدرس|الوحدة|مواءمة المصدر):",
        re.IGNORECASE | re.MULTILINE,
    )
    leaked = []
    for directory in course_dirs(COURSES_ROOT):
        course = load_course_dir(directory)
        for lesson in course.lessons:
            for language, text in (("en", lesson.content), ("ar", lesson.content_ar)):
                if text and metadata.search(learner_markdown(text) or ""):
                    leaked.append((course.course_id, lesson.lesson_id, language))
    assert leaked == []

