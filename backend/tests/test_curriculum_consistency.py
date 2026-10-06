"""Static consistency of the canonical curriculum: course folders, manifests,
and the registry (`seeds/curriculum.py`) must all describe the same courses.

No database: everything is read from the repository (the lesson files are
loaded by the same loaders the importer uses). A failure here means two of
those sources have drifted apart.
"""
import copy
import json
import re
from pathlib import Path

import pytest

from app.services.content.lesson_blocks import empty_anchors
from app.services.curriculum import loaders, validate
from app.services.curriculum.spec import CurriculumError
from app.services.curriculum.loaders import manifest_prerequisites, read_json
from app.services.learning.prerequisites import find_cycle
from seeds import curriculum as cfg

REGISTRY = {c["slug"]: c for c in cfg.COURSE_DIRECTORY_COURSES}
CANONICAL = set(REGISTRY)


def _closure(slug):
    seen, stack = [], list(REGISTRY[slug]["prerequisites"])
    while stack:
        item = stack.pop()
        if item not in seen:
            seen.append(item)
            stack.extend(REGISTRY[item]["prerequisites"])
    return set(seen)


@pytest.fixture(scope="module")
def specs():
    return {spec.course_id: spec for spec in (loaders.load_course_dir(d) for d in loaders.course_dirs())}


# ─── Course folders ─────────────────────────────────────────────────────────

def test_every_course_folder_loads_and_validates(specs):
    assert set(specs) == {c["course_id"] for c in cfg.COURSE_DIRECTORY_COURSES}
    validate.validate_courses(list(specs.values()))  # raises with every problem
    validate.validate_registry(
        list(specs.values()), cfg.COURSE_DIRECTORY_COURSES, goals=cfg.GOALS,
        stage_courses={stage[0]: stage[5] for stage in cfg.STAGES},
    )


def test_loaded_title_matches_the_registry_title(specs):
    for course in cfg.COURSE_DIRECTORY_COURSES:
        assert specs[course["course_id"]].title == course["title"], course["course_id"]


def test_module_numbers_shown_to_learners_have_no_gaps(specs):
    for spec in specs.values():
        assert [m.order for m in spec.modules] == list(range(1, len(spec.modules) + 1)), spec.course_id


def test_course_007_is_the_mcp_course_not_the_retired_llm_systems_course():
    registry = REGISTRY["course-007"]
    assert registry["title"] == "AI Agents with MCP"
    assert "mcp" in registry["skills"]
    folders = [d.name for d in loaders.course_dirs() if loaders.course_id_of(d) == "COURSE-007"]
    assert folders == ["COURSE-007_AI_Agents_With_MCP"]
    assert not list((Path(loaders.COURSES_ROOT) / folders[0]).glob("**/L007_*.py"))


def test_course_012_is_agents_foundations_and_comes_before_the_mcp_course():
    """012 is the general agent course (beginner lessons, its own MCP intro); 007 deepens MCP
    and needs only 005. 012 must therefore not require 007, and 007 recommends 012."""
    registry = REGISTRY["course-012"]
    assert registry["title"] == "AI Agents Foundations"
    assert registry["prerequisites"] == ["course-005"]
    assert "course-007" not in _closure("course-012")
    assert REGISTRY["course-007"]["prerequisites"] == ["course-005"]
    assert ("COURSE-012", "recommended") in loaders.read_manifest_prerequisites("COURSE-007")


# ─── Manifests describe the folder they sit in ──────────────────────────────

def _manifest(directory):
    nested = directory / loaders.course_id_of(directory)
    path = directory / "course_manifest.json"
    if not path.is_file() and (nested / "course_manifest.json").is_file():
        path = nested / "course_manifest.json"
    assert path.is_file(), f"{directory.name} has no course_manifest.json"
    return read_json(path)


def test_manifests_agree_with_what_the_loaders_read(specs):
    for directory in loaders.course_dirs():
        spec, manifest = specs[loaders.course_id_of(directory)], _manifest(directory)
        title = str(manifest.get("course_title") or manifest.get("title")).partition("|")[0].strip()
        assert title == spec.title, directory.name
        assert manifest["modules"] == len(spec.modules), directory.name
        assert manifest["lessons"] == sum(len(m.lessons) for m in spec.modules), directory.name


def test_manifest_prerequisites_match_the_registry():
    for directory in loaders.course_dirs():
        course = REGISTRY[loaders.course_id_of(directory).lower()]
        named = manifest_prerequisites(_manifest(directory))
        required = [cid.lower() for cid, kind in named if kind == "required"]
        assert required == course["prerequisites"], directory.name
        for cid, _kind in named:
            assert cid.lower() in CANONICAL and cid.lower() != course["slug"], (directory.name, cid)


# ─── Dependency graph ───────────────────────────────────────────────────────

def test_hard_prerequisites_are_acyclic_and_justified_by_the_registry_only():
    assert not find_cycle({slug: c["prerequisites"] for slug, c in REGISTRY.items()})


def test_no_lesson_body_carries_an_empty_extraction_anchor(specs):
    """`<a id="slug"></a>` lines came from book extraction; the lesson renderer neither draws nor
    links to them. The validator rejects them so a future chapter import cannot bring them back."""
    leftovers = [f"{c.course_id} {l.lesson_id} line {n}: {tag}"
                 for c in specs.values() for l in c.lessons for n, tag in empty_anchors(l.content)]
    assert not leftovers, leftovers[:10]


def test_the_validator_names_the_lesson_line_and_file_of_an_injected_anchor(specs):
    course = copy.deepcopy(specs["COURSE-001"])
    lesson = course.lessons[0]
    lesson.content = lesson.content.replace("\n", '\n<a id="dispersion"></a>\n', 1)
    problems = [p for p in validate.problems_in_course(course) if "extraction anchor" in p]
    assert len(problems) == 1
    assert lesson.lesson_id in problems[0] and "line 2" in problems[0] and lesson.source_file in problems[0]
    assert '<a id="dispersion"></a>' in problems[0]
    with pytest.raises(CurriculumError):
        validate.validate_courses([course])


def test_course_012_folder_carries_the_canonical_name():
    """The folder name is cosmetic for the loaders (they key on the COURSE-NNN prefix),
    but it must not keep describing the old course."""
    folders = [d.name for d in loaders.course_dirs() if loaders.course_id_of(d) == "COURSE-012"]
    assert folders == ["COURSE-012_AI_Agents_Foundations"]


def test_course_016_module_10_lessons_do_not_repeat_each_other(specs):
    """M10.L02 once carried all 28 infrastructure sections of M10.L01 on top of its own
    chapter 11 material. The two lessons must cover disjoint sections and exercises."""
    lessons = {l.lesson_id: l for l in specs["COURSE-016"].lessons}
    first, second = lessons["M10.L01"], lessons["M10.L02"]

    def headings(lesson):
        return {re.sub(r"^\d+\.\s*", "", h).strip().lower() for h in re.findall(r"(?m)^## (.+)$", lesson.content)}

    shared = (headings(first) & headings(second)) - {"learning outcomes", "important misconceptions",
                                                      "key terminology", "self-check", "retain this idea"}
    assert not shared, shared
    assert not {e.title for e in first.exercises} & {e.title for e in second.exercises}
    module = next(m for m in specs["COURSE-016"].modules if m.module_id == "M016-10")
    by_lesson = {lid: {q.question for q in module.quiz.questions if q.lesson_id == lid} for lid in ("M10.L01", "M10.L02")}
    assert all(by_lesson.values()), by_lesson
    assert not by_lesson["M10.L01"] & by_lesson["M10.L02"]
