"""
app/services/curriculum/images.py

Everything a course's lessons say about images, checked against what the course ships.

A lesson places an image with `{{image:<key>}}` (or `{{image:<key>|caption}}`) on a line of its own;
`[[IMAGE_NEEDED: ...]]` says the image does not exist yet. The English body and the Arabic body
(`ar/<lesson>.md`) may both place the same key - one picture, two descriptions.

    problems(course)   what must be fixed before anything is imported
    warnings(course)   what is worth fixing but does not stop an import
    report(course)     the counts `seeds/arabic_course_files.py status` prints

Pure functions of a loaded `CourseSpec`: no database, no files read here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterator, List, Tuple

from app.services.content.lesson_blocks import figure_keys, malformed_markers
from app.services.curriculum.spec import CourseSpec, LessonSpec

IMAGE_REQUEST = "[[IMAGE_NEEDED:"


def bodies(lesson: LessonSpec) -> Iterator[Tuple[str, str]]:
    """(language, text) for each body the lesson has."""
    yield "en", lesson.content or ""
    if lesson.content_ar:
        yield "ar", lesson.content_ar


def references(course: CourseSpec) -> List[Tuple[str, str, str]]:
    """(lesson id, language, key) for every image a lesson places, in order, repeats kept."""
    return [(lesson.lesson_id, lang, key)
            for lesson in course.lessons for lang, text in bodies(lesson) for key in figure_keys(text)]


def problems(course: CourseSpec) -> List[str]:
    out: List[str] = []
    cid = course.course_id
    keys = {a.key for a in course.assets}
    for lesson in course.lessons:
        for lang, text in bodies(lesson):
            where = f"{cid} {lesson.lesson_id}" + (" (ar)" if lang == "ar" else "")
            out += [f"{where}: image marker is not on a line of its own or is malformed: {m}"
                    for m in malformed_markers(text)]
            for key in dict.fromkeys(figure_keys(text)):
                if key not in keys:
                    out.append(f"{where}: references image '{key}' but no corresponding asset exists in "
                               f"{cid}'s assets_manifest.json")
    lessons = {lesson.lesson_id for lesson in course.lessons}
    if course.has_lesson_bodies:
        for asset in course.assets:
            if asset.lesson and asset.lesson not in lessons:
                out.append(f"{cid}: image '{asset.key}' belongs to lesson '{asset.lesson}', which is not a lesson of this course")
    return out


def unused_keys(course: CourseSpec) -> List[str]:
    placed = {key for _l, _lang, key in references(course)}
    return sorted(a.key for a in course.assets if a.key not in placed)


def remaining_requests(course: CourseSpec) -> Dict[str, int]:
    """Lesson id -> number of `[[IMAGE_NEEDED: ...]]` markers still in its English body."""
    counts = {lesson.lesson_id: (lesson.content or "").count(IMAGE_REQUEST) for lesson in course.lessons}
    return {lesson_id: n for lesson_id, n in counts.items() if n}


def arabic_metadata_gaps(course: CourseSpec) -> Tuple[List[str], List[str]]:
    """(keys without `alt_ar`, keys without `caption_ar`) among the images an Arabic lesson places. Images no
    Arabic lesson places are not asked for Arabic text: they never reach an Arabic reader."""
    by_key = {a.key: a for a in course.assets}
    used = list(dict.fromkeys(key for _l, lang, key in references(course) if lang == "ar" and key in by_key))
    return ([k for k in used if not by_key[k].alt_ar], [k for k in used if not by_key[k].caption_ar])


def warnings(course: CourseSpec) -> List[str]:
    cid = course.course_id
    notes: List[str] = list(course.asset_warnings)
    no_alt, no_caption = arabic_metadata_gaps(course)
    if no_alt:
        notes.append(f"{cid}: {len(no_alt)} image{'s' if len(no_alt) != 1 else ''} placed in Arabic lessons "
                     f"{'have' if len(no_alt) != 1 else 'has'} no alt_ar (Arabic readers get the English): {', '.join(no_alt)}")
    if no_caption:
        notes.append(f"{cid}: {len(no_caption)} image{'s' if len(no_caption) != 1 else ''} placed in Arabic lessons "
                     f"{'have' if len(no_caption) != 1 else 'has'} no caption_ar (Arabic readers get the English): {', '.join(no_caption)}")
    unused = unused_keys(course)
    if unused:
        notes.append(f"{cid}: unused asset{'s' if len(unused) != 1 else ''} (no lesson places "
                     f"{'them' if len(unused) != 1 else 'it'}): {', '.join(unused)}")
    requested = remaining_requests(course)
    if requested:
        notes.append(f"{cid}: {sum(requested.values())} image requests are still authoring placeholders, not linked "
                     f"figures (in {len(requested)} lessons)")
    return notes


@dataclass(frozen=True)
class ImageReport:
    course_id: str
    found: int             # images the manifest lists whose file is there and sound
    referenced: int        # of those, how many a lesson places
    missing: int           # images the manifest lists whose file is missing or unusable
    broken: int            # placements that name a key the manifest does not have, or are malformed
    unused: int            # found but never placed
    requests: int          # [[IMAGE_NEEDED]] markers still in English lesson bodies
    missing_alt_ar: int = 0      # images an Arabic lesson places that have no Arabic alt text
    missing_caption_ar: int = 0  # ... and no Arabic caption

    @property
    def interesting(self) -> bool:
        # A course with no finished assets can still have an important image
        # authoring backlog. Omitting request-only courses from `status` made
        # those placeholders invisible in its focused image report.
        return bool(
            self.found or self.missing or self.broken or self.referenced
            or self.unused or self.requests or self.missing_alt_ar or self.missing_caption_ar
        )


def report(course: CourseSpec) -> ImageReport:
    keys = {a.key for a in course.assets}
    placed = references(course)
    malformed = sum(len(malformed_markers(text)) for lesson in course.lessons for _l, text in bodies(lesson))
    unknown = len({(lid, lang, key) for lid, lang, key in placed if key not in keys})
    return ImageReport(
        course_id=course.course_id, found=len(keys),
        referenced=len(keys & {key for _l, _lang, key in placed}),
        missing=len(course.broken_asset_keys), broken=unknown + malformed,
        unused=len(unused_keys(course)), requests=sum(remaining_requests(course).values()),
        missing_alt_ar=len(arabic_metadata_gaps(course)[0]), missing_caption_ar=len(arabic_metadata_gaps(course)[1]),
    )


def format_report(r: ImageReport) -> str:
    return "\n".join([
        f"    Images found:      {r.found:>4}",
        f"    Images referenced: {r.referenced:>4}",
        f"    Missing images:    {r.missing:>4}",
        f"    Broken references: {r.broken:>4}",
        f"    Unused images:     {r.unused:>4}",
        f"    IMAGE_NEEDED left: {r.requests:>4}",
        f"    No Arabic alt:     {r.missing_alt_ar:>4}",
        f"    No Arabic caption: {r.missing_caption_ar:>4}",
    ])
