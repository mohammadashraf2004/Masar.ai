"""Inline lesson figures end to end: manifest -> validation -> importer -> lesson API -> image route."""
import base64
import json
import time
from pathlib import Path

import pytest

from app.models.course_asset import CourseAsset
from app.services.assets import store as asset_store
from app.services.assets.urls import asset_url
from app.services.curriculum import importer, validate
from app.services.curriculum.assets import load_assets, safe_relative_path
from app.services.curriculum.spec import CurriculumError
from seeds import curriculum as cfg
from tests.curriculum_fixtures import make_spec
from tests.learning_fixtures import learn_catalog, learn_client, learn_db, logs_enabled, register  # noqa: F401

PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
# Enough of a JPEG for the magic-number check (the header parser simply finds no size).
JPEG = b"\xff\xd8\xff\xdb\x00\x43" + b"\x00" * 64

BODY = (
    "# Low-rank adaptation\n\nLoRA decomposes the update into two small matrices.\n\n"
    "{{figure:lora-architecture}}\n\nThe original weights stay frozen.\n\n"
    "{{figure:parameter-savings}}\n\nSo far fewer parameters are trained.\n"
)


def _write_course(root: Path, name: str = "COURSE-001_Test", manifest: dict = None, files: dict = None) -> Path:
    course = root / name
    (course / "assets").mkdir(parents=True)
    for rel, data in (files if files is not None else {"assets/lora.png": PNG, "assets/savings.jpg": JPEG}).items():
        (course / rel).write_bytes(data)
    if manifest is None:
        manifest = {"version": 1, "assets": [
            {"key": "lora-architecture", "file": "assets/lora.png", "alt": "LoRA adds two small matrices",
             "caption": "Low-rank matrices are trained; the weights stay frozen."},
            {"key": "parameter-savings", "file": "assets/savings.jpg", "alt": "Parameter counts compared",
             "caption": "Far fewer trainable parameters", "figure_number": "Figure 2", "source_reference": "book 1, fig 4"},
        ]}
    (course / "assets_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return course


# ─── Manifest loading ───────────────────────────────────────────────────────

def test_a_valid_manifest_is_read_and_the_file_itself_supplies_type_size_and_hash(tmp_path):
    course = _write_course(tmp_path)
    assets, problems = load_assets(course)
    assert problems == []
    lora, savings = assets
    assert (lora.key, lora.mime_type, lora.width, lora.height, lora.byte_size) == ("lora-architecture", "image/png", 1, 1, len(PNG))
    assert len(lora.sha256) == 64 and lora.storage_key == "COURSE-001_Test/assets/lora.png"
    assert savings.mime_type == "image/jpeg" and savings.figure_number == "Figure 2"


def test_a_folder_without_a_manifest_has_no_assets_and_no_problems(tmp_path):
    (tmp_path / "COURSE-002_Plain").mkdir()
    assert load_assets(tmp_path / "COURSE-002_Plain") == ([], [])


@pytest.mark.parametrize("entry,expected", [
    ({"key": "k", "file": "assets/lora.png", "alt": ""}, "no alt text"),
    ({"key": "k", "file": "assets/lora.png"}, "no alt text"),
    ({"key": "k", "file": "assets/missing.png", "alt": "x"}, "does not exist"),
    ({"key": "k", "file": "../outside.png", "alt": "x"}, "plain path inside the course folder"),
    ({"key": "k", "file": "/etc/passwd", "alt": "x"}, "plain path inside the course folder"),
    ({"key": "k", "file": "C:/windows/x.png", "alt": "x"}, "plain path inside the course folder"),
    ({"key": "k", "file": "assets\\lora.png", "alt": "x"}, "plain path inside the course folder"),
    ({"key": "k", "file": "assets/../assets/lora.png", "alt": "x"}, "plain path inside the course folder"),
    ({"key": "k", "file": "assets/fake.png", "alt": "x"}, "is not really image/png"),
    ({"key": "k", "file": "assets/vector.svg", "alt": "x"}, "not an allowed image type"),
    ({"key": "Bad_Key", "file": "assets/lora.png", "alt": "x"}, "key must be lowercase"),
    ({"key": "k", "type": "video", "file": "assets/lora.png", "alt": "x"}, "not supported"),
])
def test_an_unsound_asset_entry_is_a_problem_and_nothing_is_imported_from_it(tmp_path, entry, expected):
    course = _write_course(tmp_path, files={"assets/lora.png": PNG, "assets/fake.png": b"not a png at all", "assets/vector.svg": b"<svg/>"},
                           manifest={"version": 1, "assets": [entry]})
    assets, problems = load_assets(course)
    assert assets == []
    assert len(problems) == 1 and expected in problems[0], problems


def test_duplicate_keys_and_a_non_canonical_manifest_are_problems(tmp_path):
    entry = {"key": "k", "file": "assets/lora.png", "alt": "x"}
    course = _write_course(tmp_path, manifest={"version": 1, "assets": [entry, entry]})
    assets, problems = load_assets(course)
    assert len(assets) == 1 and "duplicate key" in problems[0]

    legacy = _write_course(tmp_path, name="COURSE-003_Legacy", manifest=[{"filename": "x.png"}])
    assert "not an asset manifest" in load_assets(legacy)[1][0]


def test_safe_relative_path():
    assert safe_relative_path("assets/a.png") and safe_relative_path("a.png")
    for bad in ("", "/a", "../a", "a/../b", "a//b", "./a", "a\\b", "c:/a", "a\0b"):
        assert not safe_relative_path(bad), bad


# ─── Validation ─────────────────────────────────────────────────────────────

def _spec(tmp_path, body=BODY):
    course = _write_course(tmp_path)
    spec = make_spec("COURSE-001")
    spec.assets, spec.asset_problems = load_assets(course)
    spec.modules[0].lessons[0].content = body
    return spec


def test_a_lesson_placing_only_known_figures_validates(tmp_path):
    validate.validate_courses([_spec(tmp_path)])


def test_an_unknown_figure_key_fails_validation_naming_the_lesson_and_the_key(tmp_path):
    spec = _spec(tmp_path, BODY.replace("parameter-savings", "no-such-figure"))
    with pytest.raises(CurriculumError) as caught:
        validate.validate_courses([spec])
    message = str(caught.value)
    assert "L001-0101" in message and "no-such-figure" in message and "no corresponding asset" in message


def test_a_figure_whose_file_is_missing_fails_validation(tmp_path):
    spec = _spec(tmp_path)
    (tmp_path / "COURSE-001_Test" / "assets" / "lora.png").unlink()
    spec.assets, spec.asset_problems = load_assets(tmp_path / "COURSE-001_Test")
    with pytest.raises(CurriculumError) as caught:
        validate.validate_courses([spec])
    assert "lora.png" in str(caught.value) and "does not exist" in str(caught.value)


def test_a_marker_that_is_not_on_its_own_line_fails_validation(tmp_path):
    with pytest.raises(CurriculumError) as caught:
        validate.validate_courses([_spec(tmp_path, "As {{figure:lora-architecture}} shows, ...")])
    assert "not on a line of its own" in str(caught.value)


def test_an_asset_no_lesson_places_is_a_warning_not_an_error(tmp_path):
    spec = _spec(tmp_path, "# Plain lesson\n\nNo figures here.")
    validate.validate_courses([spec])  # does not raise
    notes = [n for n in validate.warnings([spec]) if "unused asset" in n]
    assert len(notes) == 1 and "lora-architecture" in notes[0] and "parameter-savings" in notes[0]


# ─── Import + lesson API ────────────────────────────────────────────────────

@pytest.fixture()
def figure_course(learn_db, learn_catalog, tmp_path, monkeypatch):
    """COURSE-001 imported with a lesson that places two figures, its files served from a temp folder."""
    course = _write_course(tmp_path)
    monkeypatch.setattr(asset_store, "_store", asset_store.LocalCourseAssetStore(tmp_path))
    spec = make_spec("COURSE-001")
    spec.assets, spec.asset_problems = load_assets(course)
    spec.modules[0].lessons[0].content = BODY
    definitions = {d["course_id"]: d for d in cfg.COURSE_DIRECTORY_COURSES}
    report = importer.import_course(learn_db, spec, definitions["COURSE-001"])
    learn_db.commit()
    return report, tmp_path


def _course_json(client, who, slug="course-001"):
    response = client.get(f"/api/v1/tool-courses/{slug}", headers=who["headers"])
    assert response.status_code == 200, response.text
    return response.json()


def test_the_importer_stores_the_figures_and_a_reimport_changes_nothing(learn_db, figure_course):
    report, tmp = figure_course
    assert (report.assets.created, report.assets.updated) == (2, 0)
    rows = {a.key: a for a in learn_db.query(CourseAsset).all()}
    assert set(rows) == {"lora-architecture", "parameter-savings"}
    assert rows["lora-architecture"].alt == "LoRA adds two small matrices" and rows["lora-architecture"].mime_type == "image/png"

    spec = make_spec("COURSE-001")
    spec.assets, spec.asset_problems = load_assets(tmp / "COURSE-001_Test")
    definitions = {d["course_id"]: d for d in cfg.COURSE_DIRECTORY_COURSES}
    again = importer.import_course(learn_db, spec, definitions["COURSE-001"])
    assert (again.assets.created, again.assets.updated, again.assets.unchanged) == (0, 0, 2)

    spec.assets[0].alt = "A corrected description"
    changed = importer.import_course(learn_db, spec, definitions["COURSE-001"])
    assert (changed.assets.updated, changed.assets.unchanged) == (1, 1)

    spec.assets = spec.assets[:1]
    dropped = importer.import_course(learn_db, spec, definitions["COURSE-001"])
    assert "COURSE-001/asset/parameter-savings" in dropped.stale  # reported, never deleted
    assert learn_db.query(CourseAsset).count() == 2


def test_a_lesson_with_figures_is_returned_as_ordered_blocks(learn_client, figure_course):
    who = register(learn_client)
    lessons = _course_json(learn_client, who)["topics"][0]["lessons"]
    blocks = lessons[0]["blocks"]
    assert [b["type"] for b in blocks] == ["markdown", "image", "markdown", "image", "markdown"]
    assert blocks[0]["content"].startswith("# Low-rank adaptation") and "two small matrices" in blocks[0]["content"]
    first = blocks[1]
    assert first["asset_key"] == "lora-architecture"
    assert first["alt"] == "LoRA adds two small matrices"
    assert first["caption"] == "Low-rank matrices are trained; the weights stay frozen."
    assert (first["width"], first["height"], first["figure_number"]) == (1, 1, None)
    assert first["url"].startswith("/learning/courses/course-001/assets/lora-architecture?exp=") and "&sig=" in first["url"]
    assert blocks[2]["content"] == "The original weights stay frozen."
    assert blocks[3]["asset_key"] == "parameter-savings" and blocks[3]["figure_number"] == "Figure 2"
    assert blocks[4]["content"] == "So far fewer parameters are trained."
    # nothing about the file's location or origin reaches the browser
    body = json.dumps(blocks)
    for private in ("storage_key", "source_reference", "assets/lora.png", "book 1", "COURSE-001_Test", "sha256"):
        assert private not in body


def test_a_lesson_without_figures_is_unchanged_and_has_no_blocks(learn_client, figure_course):
    who = register(learn_client)
    lessons = _course_json(learn_client, who)["topics"][0]["lessons"]
    assert lessons[1]["blocks"] is None and lessons[1]["blocks_ar"] is None
    assert lessons[1]["content"] == "# Lesson 1.2\n\nBody of L001-0102."


def test_an_arabic_lesson_gets_arabic_blocks_and_no_english_ones(learn_client, learn_db, learn_catalog, tmp_path, monkeypatch):
    course = _write_course(tmp_path)
    monkeypatch.setattr(asset_store, "_store", asset_store.LocalCourseAssetStore(tmp_path))
    spec = make_spec("COURSE-001")
    spec.assets, spec.asset_problems = load_assets(course)
    spec.modules[0].lessons[0].content = "مقدمة عن التكييف\n\n{{figure:lora-architecture}}\n\nخاتمة"
    definitions = {d["course_id"]: d for d in cfg.COURSE_DIRECTORY_COURSES}
    importer.import_course(learn_db, spec, definitions["COURSE-001"])
    learn_db.commit()
    who = register(learn_client)
    lesson = _course_json(learn_client, who)["topics"][0]["lessons"][0]
    assert lesson["content"] == "" and lesson["blocks"] is None
    assert [b["type"] for b in lesson["blocks_ar"]] == ["markdown", "image", "markdown"]
    assert lesson["blocks_ar"][1]["asset_key"] == "lora-architecture"


def test_the_topic_endpoint_returns_the_same_blocks(learn_client, figure_course):
    who = register(learn_client)
    topic_id = _course_json(learn_client, who)["topics"][0]["id"]
    response = learn_client.get(f"/api/v1/tool-courses/topics/{topic_id}", headers=who["headers"])
    assert response.status_code == 200
    assert [b["type"] for b in response.json()["lessons"][0]["blocks"]] == ["markdown", "image", "markdown", "image", "markdown"]


def test_a_course_without_figures_is_unaffected(learn_client, learn_db, learn_catalog):
    from tests.curriculum_fixtures import import_small_courses
    import_small_courses(learn_db, ("COURSE-002",))
    who = register(learn_client)
    lessons = _course_json(learn_client, who, "course-002")["topics"][0]["lessons"]
    assert all(l["blocks"] is None for l in lessons)


def test_a_locked_lesson_has_neither_text_nor_figure_urls(learn_client, learn_db, figure_course):
    from app.models.learning_path import Course
    who = register(learn_client)
    course = learn_db.query(Course).filter(Course.slug == "course-001").one()
    course.is_free = False
    learn_db.commit()
    lesson = _course_json(learn_client, who)["topics"][0]["lessons"][0]
    assert lesson["is_locked"] is True and lesson["content"] == "" and not lesson["blocks"]
    assert "/assets/" not in json.dumps(lesson)


def test_a_figure_whose_asset_was_removed_is_left_out_and_its_marker_is_never_shown(learn_client, learn_db, figure_course):
    learn_db.query(CourseAsset).filter(CourseAsset.key == "parameter-savings").delete()
    learn_db.commit()
    who = register(learn_client)
    blocks = _course_json(learn_client, who)["topics"][0]["lessons"][0]["blocks"]
    assert [b["type"] for b in blocks] == ["markdown", "image", "markdown", "markdown"]
    assert "{{figure" not in json.dumps(blocks)


# ─── The image route ────────────────────────────────────────────────────────

def _path(url: str) -> str:
    return "/api/v1" + url


def test_a_signed_url_serves_the_image_with_its_type_and_caching_headers(learn_client, figure_course):
    response = learn_client.get(_path(asset_url("course-001", "lora-architecture")))
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png" and response.content == PNG
    assert response.headers["cache-control"] == "private, max-age=86400"
    assert response.headers["x-content-type-options"] == "nosniff" and response.headers["etag"].startswith('"')


def test_the_mime_type_follows_the_stored_type(learn_client, figure_course):
    response = learn_client.get(_path(asset_url("course-001", "parameter-savings")))
    assert response.status_code == 200 and response.headers["content-type"] == "image/jpeg"


def test_a_repeat_visit_with_the_etag_is_a_304(learn_client, figure_course):
    url = _path(asset_url("course-001", "lora-architecture"))
    etag = learn_client.get(url).headers["etag"]
    again = learn_client.get(url, headers={"If-None-Match": etag})
    assert again.status_code == 304 and again.content == b""


def test_the_lesson_url_and_the_image_route_agree(learn_client, figure_course):
    who = register(learn_client)
    url = _course_json(learn_client, who)["topics"][0]["lessons"][0]["blocks"][1]["url"]
    assert learn_client.get(_path(url)).status_code == 200  # no Authorization header: an <img> cannot send one


def test_a_missing_tampered_or_expired_signature_is_refused(learn_client, figure_course):
    good = asset_url("course-001", "lora-architecture")
    base = _path(good.split("?")[0])
    assert learn_client.get(base).status_code == 422
    assert learn_client.get(_path(good)[:-4] + "0000").status_code == 403
    assert learn_client.get(_path(good).replace("exp=", "exp=1")).status_code == 403
    past = asset_url("course-001", "lora-architecture", now=time.time() - 10 * 86400)
    assert learn_client.get(_path(past)).status_code == 403


def test_a_figure_cannot_be_read_through_another_course(learn_client, learn_db, figure_course):
    from tests.curriculum_fixtures import import_small_courses
    import_small_courses(learn_db, ("COURSE-002",))
    # a genuine signature for course-002, but the key belongs to course-001
    assert learn_client.get(_path(asset_url("course-002", "lora-architecture"))).status_code == 404
    # course-001's signature replayed against course-002's path
    replay = _path(asset_url("course-001", "lora-architecture")).replace("/course-001/", "/course-002/")
    assert learn_client.get(replay).status_code == 403
    assert learn_client.get(_path(asset_url("no-such-course", "lora-architecture"))).status_code == 404


@pytest.mark.parametrize("key", ["..", "%2e%2e", "..%2f..%2fetc%2fpasswd", "a%2Fb", "UPPER", "a_b", "x" * 130])
def test_a_key_that_is_not_a_plain_asset_key_never_reaches_the_filesystem(learn_client, figure_course, key):
    url = _path(asset_url("course-001", "lora-architecture")).replace("/lora-architecture?", f"/{key}?")
    response = learn_client.get(url)
    # the HTTP client may normalise `..` itself; whatever route it lands on, it is never an image or a file
    assert response.status_code < 500
    assert not response.headers.get("content-type", "").startswith("image/")
    assert b"root:" not in response.content


def test_the_store_refuses_a_storage_key_that_escapes_its_root(learn_client, learn_db, figure_course):
    _report, tmp = figure_course
    (tmp.parent / "secret.txt").write_text("do not serve")
    row = learn_db.query(CourseAsset).filter(CourseAsset.key == "lora-architecture").one()
    for escaping in (f"../{tmp.parent.name}/secret.txt", "../secret.txt", str((tmp.parent / "secret.txt").resolve()),
                     "COURSE-001_Test/../../secret.txt", "", "COURSE-001_Test"):
        row.storage_key = escaping
        learn_db.commit()
        response = learn_client.get(_path(asset_url("course-001", "lora-architecture")))
        assert response.status_code == 404, escaping
        assert b"do not serve" not in response.content


def test_the_local_store_only_opens_files_inside_its_root(tmp_path):
    (tmp_path / "inside").mkdir()
    (tmp_path / "inside" / "a.png").write_bytes(PNG)
    (tmp_path.parent / "outside.txt").write_text("x")
    store = asset_store.LocalCourseAssetStore(tmp_path / "inside")
    assert store.resolve("a.png") is not None
    for bad in ("../outside.txt", "/etc/passwd", "", ".", "nope.png", "a.png/../../outside.txt", "a\0.png"):
        assert store.resolve(bad) is None, bad


def test_urls_are_stable_within_a_day_and_bound_to_course_and_key():
    noon = 1_800_000_000
    assert asset_url("c", "k", now=noon) == asset_url("c", "k", now=noon + 3600)
    assert asset_url("c", "k", now=noon) != asset_url("c", "k", now=noon + 86400)
    assert asset_url("c", "k", now=noon) != asset_url("d", "k", now=noon)
    assert asset_url("c", "k", now=noon) != asset_url("c", "j", now=noon)
