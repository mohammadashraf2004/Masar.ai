"""The real course folders: every figure a lesson places exists, and figures sit where they help, not at the end."""
import pytest

from app.services.content.lesson_blocks import FigureBlock, figure_keys, split_lesson
from app.services.curriculum import validate
from app.services.curriculum.loaders import load_all_courses

IMAGE_COURSES = {f"COURSE-{n:03d}" for n in range(8, 15)}


@pytest.fixture(scope="module")
def courses():
    # COURSE-001..015: the figure-bearing set this file was written for.
    # (COURSE-016 also loads cleanly now and carries its own assets; it is covered
    # by the structural tests in test_curriculum_consistency.py.)
    return load_all_courses(only=[f"COURSE-{n:03d}" for n in range(1, 16)])


def test_the_course_structure_is_unchanged_by_inline_figures(courses):
    assert (len(courses), sum(len(c.modules) for c in courses), sum(len(c.lessons) for c in courses)) == (15, 105, 181)


def test_every_placed_figure_resolves_and_every_manifest_is_sound(courses):
    validate.validate_courses(courses)  # raises, listing every problem, otherwise
    for course in courses:
        assert course.asset_problems == []
        keys = {a.key for a in course.assets}
        for lesson in course.lessons:
            assert set(figure_keys(lesson.content)) <= keys, lesson.lesson_id


def test_courses_one_to_seven_have_no_assets_and_are_untouched(courses):
    for course in courses:
        if course.course_id not in IMAGE_COURSES:
            assert course.assets == []
            assert all(not figure_keys(l.content) for l in course.lessons)


@pytest.mark.xfail(strict=True, reason=(
    "The 2026-09 content restructure replaced the lesson files that placed `{{figure:key}}` markers with "
    "files carrying [[IMAGE_NEEDED]] placeholders, so figures in COURSE-008..011, 013 and 014 are shipped but "
    "unplaced (see `validate.warnings`). Re-place them; this test then XPASSes and the mark must be removed."))
def test_the_image_courses_ship_their_figures_and_place_them(courses):
    by_id = {c.course_id: c for c in courses}
    assert {cid for cid in IMAGE_COURSES if by_id[cid].assets} == IMAGE_COURSES
    placed = {(c.course_id, k) for c in courses for l in c.lessons for k in figure_keys(l.content)}
    unplaced = {(c.course_id, a.key) for c in courses for a in c.assets} - placed
    assert unplaced == set()


def test_every_shipped_figure_has_alt_text_and_a_readable_caption(courses):
    for course in courses:
        for asset in course.assets:
            assert asset.alt and asset.caption, (course.course_id, asset.key)
            assert not asset.alt.lower().endswith((".png", ".jpg")) and "_HTML" not in asset.alt
            assert asset.width and asset.height, (course.course_id, asset.key)


def test_figures_are_woven_into_the_lesson_never_appended_at_the_end(courses):
    for course in courses:
        for lesson in course.lessons:
            blocks = split_lesson(lesson.content)
            if not any(isinstance(b, FigureBlock) for b in blocks):
                continue
            assert not isinstance(blocks[0], FigureBlock), lesson.lesson_id       # not before the lesson starts
            assert not isinstance(blocks[-1], FigureBlock), lesson.lesson_id      # not dumped after it ends


def test_the_old_list_of_manual_visual_references_is_gone_from_lessons_that_now_show_their_figures(courses):
    for course in courses:
        for lesson in course.lessons:
            if figure_keys(lesson.content):
                text = lesson.content.lower()
                for stale in ("## visual assets", "## visual reference", "## manual visual references", "verify reuse rights",
                              "add manually", "manually add"):
                    assert stale not in text, (lesson.lesson_id, stale)
