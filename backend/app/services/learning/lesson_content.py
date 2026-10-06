"""
app/services/learning/lesson_content.py

Turns a lesson body into the ordered blocks a client renders.

The body stays what it always was - Markdown in `lessons.content` - with authoring syntax on lines
of its own (syntax and parsing: `app.services.content.lesson_blocks`):

    {{image:<key>}} / {{image:<key>|caption}}   an image belongs here
    {{exercise:<id>}}                           the author wants that lesson exercise to come up here
    [[IMAGE_NEEDED: ...]]                       the image does not exist yet

This module is the one place that decides what a reader of the lesson gets for each of them. It produces

    [{"type": "markdown", ...}, {"type": "image", ...}, {"type": "markdown", ...}]

in the order the author wrote them, resolving image keys against the course's `course_assets`. It runs
when a lesson is read, so nothing is stored twice and a corrected caption reaches learners without
touching the lesson. The stored Markdown is never edited: validators, `seeds/link_images.py` and the
status tools still see every marker in it.

  * images        -> `image` blocks (or `image_missing` when the course no longer has the asset).
  * `{{exercise}}`-> nothing. Exercises are rendered by the lesson page's exercise section, paired to the
                     lesson by `exercise.lesson_id`, so the marker is source metadata. A marker in a lesson
                     that has no exercise at all becomes an `exercise_missing` block outside production
                     (a named diagnostic for the author) and is omitted in production.
  * `IMAGE_NEEDED`-> an `author_marker` block outside production (the title only, never the raw marker),
                     nothing in production.
  * Anything else that looks like authoring syntax is cut out of the prose (see `strip_authoring`).
  * In production the `content` / `content_ar` fields of the response are cleaned of all of it as well
    (`learner_markdown`): Markdown a client can read, without internal directives.

The English body gets the English alt text and caption, the Arabic body the Arabic ones; either falls
back to the other when only one was written (`alt_lang` / `caption_lang` say which language was used, so
a client can set the direction of what it shows), and a caption written at the spot in the lesson wins
over both. The picture itself is shared.

A body with no authoring syntax is left alone (`blocks` stays null): such lessons render exactly as before.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List, Mapping, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.course_asset import CourseAsset
from app.models.learning import Exercise
from app.services.assets.urls import asset_url
from app.services.content.lesson_blocks import (
    AuthorMarkerBlock, ExerciseBlock, FigureBlock, has_authoring_syntax, learner_markdown, split_lesson,
)

log = logging.getLogger(__name__)

_EXERCISE_HINT = "{{exercise"


def _pick(primary: Optional[str], fallback: Optional[str], language: str, fallback_language: str):
    """(text, language of that text): the reader's language when it was written, else the other one."""
    if primary:
        return primary, language
    return (fallback, fallback_language) if fallback else (None, language)


def lesson_blocks(text: Optional[str], assets: Mapping[str, CourseAsset], course_slug: str,
                  language: str = "en", *, exercise_count: Optional[int] = None,
                  production: Optional[bool] = None) -> Optional[List[Dict[str, Any]]]:
    """The body as blocks, or None when it holds no authoring syntax at all.

    `exercise_count` is how many exercises the lesson has in the database (None when unknown): a lesson
    with none cannot be showing the exercise an `{{exercise:..}}` marker points at. `production` defaults
    to the app's setting. An image whose key has no asset (removed after the lesson was imported) becomes
    an `image_missing` block - a visible "could not be shown" note in front of a learner, a named error
    for an author - and is logged; the marker itself is never shown."""
    if not has_authoring_syntax(text):
        return None
    if production is None:
        production = settings.is_production
    arabic = language == "ar"
    other = "en" if arabic else "ar"
    blocks: List[Dict[str, Any]] = []
    for block in split_lesson(text):
        if isinstance(block, FigureBlock):
            asset = assets.get(block.key)
            if asset is None:
                log.warning("lesson places image '%s' but course '%s' has no such asset", block.key, course_slug)
                blocks.append({"type": "image_missing", "asset_key": block.key})
                continue
            first, second = (asset.alt_ar, asset.alt) if arabic else (asset.alt, asset.alt_ar)
            alt, alt_lang = _pick(first, second, language, other)
            first, second = (asset.caption_ar, asset.caption) if arabic else (asset.caption, asset.caption_ar)
            caption, caption_lang = _pick(first, second, language, other)
            if block.caption:           # written at this spot: it is in the language of the lesson
                caption, caption_lang = block.caption, language
            blocks.append({
                "type": "image", "asset_key": asset.key, "url": asset_url(course_slug, asset.key),
                "alt": alt or "", "alt_lang": alt_lang, "caption": caption, "caption_lang": caption_lang,
                "figure_number": asset.figure_number, "width": asset.width, "height": asset.height,
            })
        elif isinstance(block, ExerciseBlock):
            if exercise_count == 0:
                log.warning("lesson of course '%s' points at exercise '%s' but has no exercise", course_slug, block.exercise_id)
                if not production:
                    blocks.append({"type": "exercise_missing", "exercise_id": block.exercise_id})
        elif isinstance(block, AuthorMarkerBlock):
            if not production:
                blocks.append({"type": "author_marker", "kind": block.kind, "title": block.title})
        elif blocks and blocks[-1]["type"] == "markdown":
            blocks[-1]["content"] += "\n\n" + block.content        # a hidden marker stood between two runs of prose
        else:
            blocks.append({"type": "markdown", "content": block.content})
    return blocks


def attach_lesson_blocks(db: Session, tool_course_id: int, course_slug: str, lessons: Iterable[Dict[str, Any]],
                         *, production: Optional[bool] = None) -> None:
    """Set `blocks` / `blocks_ar` on serialized lessons (dicts). One query for the course's figures and one
    for the lessons' exercise counts, and none at all when no lesson holds authoring syntax.

    In production the serialized `content` / `content_ar` are also cleaned of authoring syntax
    (`learner_markdown`), so no client sees a source marker in a response; outside production they keep the
    source as written, which is useful when authoring. Neither the stored body nor `blocks` (what the lesson page
    renders) is derived from the cleaned text."""
    lessons = list(lessons)
    if production is None:
        production = settings.is_production
    if not any(has_authoring_syntax(l.get("content")) or has_authoring_syntax(l.get("content_ar")) for l in lessons):
        return
    assets = {a.key: a for a in db.query(CourseAsset).filter(CourseAsset.tool_course_id == tool_course_id).all()}
    counts: Dict[int, int] = {}
    ids = [l["id"] for l in lessons if l.get("id") is not None
           and (_EXERCISE_HINT in (l.get("content") or "") or _EXERCISE_HINT in (l.get("content_ar") or ""))]
    if ids:
        counts = dict(db.query(Exercise.lesson_id, func.count(Exercise.id))
                      .filter(Exercise.lesson_id.in_(ids)).group_by(Exercise.lesson_id).all())
    for lesson in lessons:
        known = counts.get(lesson.get("id"), 0) if lesson.get("id") in ids else None
        lesson["blocks"] = lesson_blocks(lesson.get("content"), assets, course_slug, "en", exercise_count=known)
        lesson["blocks_ar"] = lesson_blocks(lesson.get("content_ar"), assets, course_slug, "ar", exercise_count=known)
        if production:
            for field in ("content", "content_ar"):
                if lesson.get(field):
                    lesson[field] = learner_markdown(lesson[field])
