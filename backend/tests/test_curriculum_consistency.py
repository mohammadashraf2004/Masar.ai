"""Static consistency of the canonical curriculum: course folders, manifests,
the registry (`seeds/curriculum.py`), the fixed track workflows and the
personalised-roadmap templates must all describe the same courses.

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
from app.services.code_grading.authoring import count_python_blanks
from app.services.curriculum import loaders, validate
from app.services.curriculum.spec import CurriculumError
from app.services.curriculum.loaders import manifest_prerequisites, read_json
from app.services.learning.prerequisites import find_cycle
from seeds import curriculum as cfg
from seeds.seed_learning_paths import FIELD_RULES

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
    for goal in (cfg.AI_DEVELOPER, cfg.AI_ENGINEER):
        order = [slug for slug, *_ in cfg.TRACK_WORKFLOWS[goal]]
        assert order.index("course-009") < order.index("course-012") < order.index("course-007"), goal
    for _id, goal, _title, _title_ar, items in cfg.TEMPLATES:
        slugs = [slug for slug, _field in items]
        if goal in (cfg.AI_DEVELOPER, cfg.AI_ENGINEER):
            assert slugs.index("course-012") < slugs.index("course-007"), goal


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


@pytest.mark.parametrize("goal", cfg.GOALS)
def test_a_required_course_has_every_hard_prerequisite_earlier_and_required(goal):
    """`track_workflow.is_locked` locks a course on ANY unfinished hard prerequisite, so
    a prerequisite that is absent from the track, later than the course, or optional
    would leave a required course permanently locked (or an optional one blocking)."""
    items = cfg.TRACK_WORKFLOWS[goal]
    position = {slug: i for i, (slug, *_rest) in enumerate(items)}
    required = {slug: req for slug, _rel, req, _section in items}
    for slug, _relation, is_required, _section in items:
        for prerequisite in REGISTRY[slug]["prerequisites"]:
            assert prerequisite in position, f"{goal}: {slug} needs {prerequisite}, which the track lacks"
            assert position[prerequisite] < position[slug], f"{goal}: {prerequisite} must precede {slug}"
            if is_required:
                assert required[prerequisite], f"{goal}: optional {prerequisite} blocks required {slug}"


def test_ai_engineer_sections_run_in_the_documented_order():
    sections = []
    for _slug, _rel, _req, section in cfg.TRACK_WORKFLOWS[cfg.AI_ENGINEER]:
        if section not in sections:
            sections.append(section)
    assert sections == ["foundations", "language-generative-ai", "application-production",
                        "advanced-ai-systems", "specializations"]
    order = [slug for slug, *_ in cfg.TRACK_WORKFLOWS[cfg.AI_ENGINEER]]
    # Multimodal needs at least one modality first: it comes after vision and speech.
    assert order.index("course-008") > order.index("course-014")
    assert order.index("course-008") > order.index("course-015")


def test_optional_specialisations_never_sit_between_required_courses():
    for goal, items in cfg.TRACK_WORKFLOWS.items():
        specialisations = {"course-008", "course-014", "course-015"}
        seen_optional_specialisation = False
        for slug, _rel, required, _section in items:
            if slug in specialisations and not required:
                seen_optional_specialisation = True
            elif seen_optional_specialisation:
                assert not required, f"{goal}: required {slug} follows an optional specialisation"


# ─── Roadmap templates ──────────────────────────────────────────────────────

def test_templates_list_only_canonical_courses_and_the_five_goals():
    assert {t[1] for t in cfg.TEMPLATES} == set(cfg.GOALS)
    for goal in cfg.GOALS:
        courses = cfg.template_courses(goal)
        assert courses and set(courses) <= CANONICAL, (goal, sorted(set(courses) - CANONICAL))


def test_template_course_sets_equal_the_workflow_minus_documented_extras():
    for goal in cfg.GOALS:
        workflow = {slug for slug, *_ in cfg.TRACK_WORKFLOWS[goal]}
        template = set(cfg.template_courses(goal))
        assert template <= workflow, (goal, sorted(template - workflow))
    # What a template deliberately leaves to the fixed workflow (optional, not part of a roadmap):
    assert {slug for slug, *_ in cfg.TRACK_WORKFLOWS[cfg.MLOPS_ENGINEER]} - set(
        cfg.template_courses(cfg.MLOPS_ENGINEER)) == {"course-002", "course-003", "course-006"}


def test_roadmap_hard_prerequisites_come_first_on_every_route():
    fields = ["nlp", "computer-vision", "speech", "multimodal", "data"]
    for goal in cfg.GOALS:
        for routed in ([], *[[f] for f in fields], fields):
            sequence = cfg.template_courses(goal, routed)
            position = {s: i for i, s in enumerate(sequence)}
            for slug in sequence:
                for prerequisite in REGISTRY[slug]["prerequisites"]:
                    assert prerequisite not in position or position[prerequisite] < position[slug], (goal, routed, slug)


# ─── Fields ─────────────────────────────────────────────────────────────────

def test_multimodal_needs_one_modality_and_recommends_two():
    rule = FIELD_RULES["multimodal"]
    assert set(rule["prerequisites"]) == {"nlp", "computer-vision", "speech"}
    assert (rule["prerequisite_min_required"], rule["prerequisite_recommended"]) == (1, 2)
    # ... and no hard course dependency forces all three modalities:
    assert not _closure("course-008") & {"course-004", "course-014", "course-015"}


def test_each_field_gates_its_own_course_in_every_template():
    gate = {"course-004": "nlp", "course-005": "nlp", "course-006": "nlp", "course-007": "nlp", "course-009": "nlp",
            "course-012": "nlp", "course-014": "computer-vision", "course-015": "speech", "course-008": "multimodal"}
    for _slug, _goal, _title, _title_ar, stages in cfg.TEMPLATES:
        for stage, field in stages:
            if stage in gate:
                assert field == gate[stage], (_slug, stage, field)


def test_vision_and_multimodal_routes_do_not_pull_the_llm_chain():
    for course in ("course-014", "course-008"):
        assert not _closure(course) & {"course-005", "course-006", "course-007", "course-009", "course-012"}, course


def test_a_speech_route_needs_only_the_llm_foundation():
    """COURSE-015 assumes an LLM application (005, hence 004). It must not drag in the
    RAG, agents, MCP, production-AI or cloud courses."""
    assert _closure("course-015") == {"course-001", "course-002", "course-003", "course-004", "course-005"}


def test_the_mlops_chain_does_not_require_the_llm_courses():
    for course in ("course-010", "course-011", "course-016"):
        assert not _closure(course) & {"course-004", "course-005", "course-006", "course-007", "course-012"}, course


# ─── Vocabulary seeding ─────────────────────────────────────────────────────

def test_vocabulary_seeding_covers_every_canonical_course():
    """`seed_vocabulary` only associates terms with a hard-coded launched set. It went
    stale once (COURSE-016 was silently excluded after it became canonical), so pin it
    to the registry: a new canonical course must be added to the seeding gate too."""
    from seeds import seed_vocabulary

    canonical_ids = {c["course_id"] for c in REGISTRY.values()}
    assert canonical_ids <= seed_vocabulary._LAUNCHED_COURSES
    seeded = {loaders.course_id_of(d) for d in seed_vocabulary._launched_course_dirs()}
    assert canonical_ids <= seeded


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


def _guided_python(specs, course_id, exercise_ids):
    exercises = {
        exercise.exercise_id: exercise
        for lesson in specs[course_id].lessons
        for exercise in lesson.exercises
        if exercise.exercise_id in exercise_ids
    }
    assert set(exercises) == set(exercise_ids)
    for exercise in exercises.values():
        assert exercise.exercise_type == "code"
        assert exercise.language == "python"
        assert exercise.starter_code and exercise.solution_code
        assert exercise.starter_code != exercise.solution_code
        assert 1 <= count_python_blanks(exercise.starter_code) <= 5
        assert count_python_blanks(exercise.solution_code) == 0
        # Hidden checks with feedback in both languages.
        assert exercise.tests
        assert all(test["feedback"]["en"] and test["feedback"]["ar"] for test in exercise.tests)
        assert exercise.hint_ar and exercise.success_message_ar
        assert "**التعليمات**" in exercise.description_ar


def test_course_016_implementation_tasks_are_real_code_exercises(specs):
    """Implementation prompts must not fall back to the legacy written-answer card."""
    _guided_python(specs, "COURSE-016", {
        "COURSE-016.M04.L01.EX04", "COURSE-016.M12.L01.EX02", "COURSE-016.M16.L01.EX02",
    })


def test_course_013_numpy_and_pandas_tasks_are_real_code_exercises(specs):
    _guided_python(specs, "COURSE-013", {"COURSE-013.M02.L01.EX01", "COURSE-013.M02.L01.EX02"})


def test_reviewed_code_backlog_is_classified_without_fake_grading(specs):
    from app.services.curriculum.code_classification import PENDING_BY_LANGUAGE, REVIEWED_CODE_BY_LANGUAGE
    from app.services.curriculum.guided import registry

    by_id = {
        exercise.exercise_id: exercise
        for course in specs.values()
        for lesson in course.lessons
        for exercise in lesson.exercises
    }
    # Every reviewed coding task now has a guided, graded definition: nothing
    # is left in the Run-only state that blocks course completion.
    assert len(REVIEWED_CODE_BY_LANGUAGE) >= 190
    assert PENDING_BY_LANGUAGE == {}
    assert not [eid for eid, exercise in by_id.items() if exercise.exercise_type == "code_pending"]
    for exercise_id in REVIEWED_CODE_BY_LANGUAGE:
        exercise = by_id[exercise_id]
        # The guided definition decides the editor language (a review may
        # have found, say, a Dockerfile task listed under Python).
        assert (exercise.exercise_type, exercise.language) == ("code", registry()[exercise_id].language)
        assert exercise.tests and exercise.solution_code

    # A workflow table/diagram is a written answer, even though its subject is
    # software. It must not become a fake code exercise just because its title
    # contains "Design".
    course_013 = {
        exercise.title: exercise
        for lesson in specs["COURSE-013"].lessons
        for exercise in lesson.exercises
    }
    workflow = course_013["Design a Complete Data-Team Workflow"]
    assert workflow.exercise_type == "legacy"
    assert workflow.starter_code is None
