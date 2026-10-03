"""
app/services/learning/lesson_content.py

Turns a lesson body into the ordered blocks a client renders.

The body stays what it always was - Markdown in `lessons.content` - with
`{{figure:<key>}}` on a line of its own wherever a figure belongs (syntax and
parsing: `app.services.content.lesson_blocks`). This module resolves each key
against the course's `course_assets` and produces

    [{"type": "markdown", ...}, {"type": "image", ...}, {"type": "markdown", ...}]

in the order the author wrote them. It runs when a lesson is read, so nothing is
stored twice and a corrected caption reaches learners without touching the lesson.

A body with no marker is left alone (`blocks` stays null): lessons without figures
render exactly as before.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List, Mapping, Optional

from sqlalchemy.orm import Session

from app.models.course_asset import CourseAsset
from app.services.assets.urls import asset_url
from app.services.content.lesson_blocks import FigureBlock, has_figures, split_lesson

log = logging.getLogger(__name__)

_MARKER_HINT = "{{figure"


def lesson_blocks(text: Optional[str], assets: Mapping[str, CourseAsset], course_slug: str) -> Optional[List[Dict[str, Any]]]:
    """The body as blocks, or None when it places no figure. A figure whose key has
    no asset (removed after the lesson was imported) is left out and logged; the
    marker itself is never shown to a learner."""
    if not text or _MARKER_HINT not in text or not has_figures(text):
        return None
    blocks: List[Dict[str, Any]] = []
    for block in split_lesson(text):
        if isinstance(block, FigureBlock):
            asset = assets.get(block.key)
            if asset is None:
                log.warning("lesson places figure '%s' but course '%s' has no such asset", block.key, course_slug)
                continue
            blocks.append({
                "type": "image", "asset_key": asset.key, "url": asset_url(course_slug, asset.key),
                "alt": asset.alt, "caption": asset.caption, "figure_number": asset.figure_number,
                "width": asset.width, "height": asset.height,
            })
        else:
            blocks.append({"type": "markdown", "content": block.content})
    return blocks


def attach_lesson_blocks(db: Session, tool_course_id: int, course_slug: str, lessons: Iterable[Dict[str, Any]]) -> None:
    """Set `blocks` / `blocks_ar` on serialized lessons (dicts). One query for the
    course's figures, and none at all when no lesson places one."""
    lessons = list(lessons)
    if not any(_MARKER_HINT in (l.get("content") or "") or _MARKER_HINT in (l.get("content_ar") or "") for l in lessons):
        return
    assets = {a.key: a for a in db.query(CourseAsset).filter(CourseAsset.tool_course_id == tool_course_id).all()}
    for lesson in lessons:
        lesson["blocks"] = lesson_blocks(lesson.get("content"), assets, course_slug)
        lesson["blocks_ar"] = lesson_blocks(lesson.get("content_ar"), assets, course_slug)
