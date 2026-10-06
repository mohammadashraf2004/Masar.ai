r"""
backend/seeds/link_images.py

Turn a request for an image into a link to the image, one explicitly named marker at a time.

    [[IMAGE_NEEDED: transformer processing pipeline | ... ]]      the image does not exist yet
    {{image:transformer-processing-pipeline}}                     the image exists and is linked

    # the markers still waiting (numbered per lesson) and the manifest images no lesson places yet
    python seeds/link_images.py list --course COURSE-004
    python seeds/link_images.py list --course COURSE-004 --lesson M01.L01

    # preview, then apply, ONE replacement: marker number (or a unique piece of its text) -> image key
    python seeds/link_images.py replace --course COURSE-004 --lesson M01.L01 --marker 2 --key transformer-flow
    python seeds/link_images.py replace --course COURSE-004 --lesson M01.L01 --marker 2 --key transformer-flow --write

    # several at once, from a file: [{"course": "COURSE-004", "lesson": "M01.L01", "marker": 2, "key": "..."}]
    python seeds/link_images.py replace --map links.json --write

    # one marker that several images belong to: list the keys (they become consecutive lines, in this order)
    python seeds/link_images.py replace --course COURSE-004 --lesson M01.L01 --marker 2 --key first-key,second-key --write

    # add images after one that is already linked: name that image's token instead of a marker number
    python seeds/link_images.py replace --course COURSE-004 --lesson M01.L01 --marker "{{image:first-key}}" --key third-key --write

    # put images where a concept is taught when no marker stands there: `after` is text that ENDS the block the
    # figures follow (unique in the lesson, on one line), `after_ar` the same block in the Arabic file; `remove`
    # names images to take out of where they stand now (they must share a line group with another image): a move
    python seeds/link_images.py place --map placements.json --write
    #   [{"course": "COURSE-012", "lesson": "M01.L05", "key": "reflexion-loop", "after": "...end of paragraph.",
    #     "after_ar": "...end of the Arabic paragraph.", "remove": ""}]

Nothing is guessed. A replacement happens only when the image key is in the course's manifest with its file in
place, the marker selector matches exactly one marker of that lesson, and that marker stands on a line of its own.
Anything else is refused with the reason. Without `--write` it only prints what it would do.

The English text (a Python module) and the Arabic text (`ar/<lesson>.md`) carry the same markers, and the Arabic
is checked against the English, so both are changed together or neither is. The Arabic file's `source_hash` is
brought up to date only if it was up to date before: a marker swap does not change the translation, but an
Arabic file that was already stale stays stale. After writing, the course is loaded and validated again; if that
finds a new problem, every file is put back as it was.

Nothing here touches the database, and nothing but the marker line is edited.
"""
import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.services.content.lesson_blocks import figure_keys, is_valid_key
from app.services.curriculum import arabic, images
from app.services.curriculum.loaders import COURSES_ROOT, course_dirs, course_id_of, load_course_dir
from app.services.curriculum.spec import CourseSpec, LessonSpec
from seeds.source_edit import SourceEditError, literal_kind_at, replace_in_literals

_REQUEST = re.compile(r"\[\[IMAGE_NEEDED(?:[^\[\]]|\[[^\[\]\n]*\])*\]\]")


class Refused(Exception):
    """A replacement that must not happen, with the reason."""


@dataclass
class Link:
    course: str
    lesson: str
    marker: str       # a 1-based number or a piece of the marker's text
    key: str


@dataclass
class Placement(Link):
    """Images that follow a block of text instead of replacing a marker. `marker` holds the English text the block ends with."""
    after_ar: str = ""   # the text the same block ends with in the Arabic file
    remove: str = ""     # images to take out of where they stand now (comma-separated): a move


def _load(course_id: str) -> CourseSpec:
    for directory in course_dirs(COURSES_ROOT):
        if course_id_of(directory) == course_id:
            return load_course_dir(directory)
    raise Refused(f"no course {course_id}")


def _lesson(course: CourseSpec, lesson_id: str) -> LessonSpec:
    lesson = next((l for l in course.lessons if l.lesson_id == lesson_id), None)
    if lesson is None:
        raise Refused(f"no lesson {lesson_id} in {course.course_id}")
    return lesson


def requests_in(text: str) -> List[str]:
    return _REQUEST.findall(text or "")


def _select(markers: List[str], selector: str, where: str) -> int:
    """Index of the one marker the selector names."""
    if not markers:
        raise Refused(f"{where}: no [[IMAGE_NEEDED]] marker left in this lesson")
    if selector.isdigit():
        number = int(selector)
        if not 1 <= number <= len(markers):
            raise Refused(f"{where}: there is no marker number {number} (the lesson has {len(markers)})")
        return number - 1
    hits = [i for i, m in enumerate(markers) if selector.lower() in m.lower()]
    if len(hits) != 1:
        listing = "\n".join(f"      {i + 1}. {markers[i][:110]}" for i in (hits or range(len(markers))))
        raise Refused(f"{where}: {'no marker contains' if not hits else 'several markers contain'} {selector!r}"
                      f" - pick one by number:\n{listing}")
    return hits[0]


def _on_own_line(text: str, marker: str) -> bool:
    """True when the marker (which may itself span several lines) starts a line and ends one."""
    at = text.find(marker)
    while at != -1:
        before, after = text[:at], text[at + len(marker):]
        if before.rsplit("\n", 1)[-1].strip() == "" and after.split("\n", 1)[0].strip() == "":
            return True
        at = text.find(marker, at + 1)
    return False


def _source_path(course: CourseSpec, lesson: LessonSpec) -> Path:
    for base in (COURSES_ROOT / course.source_dir, COURSES_ROOT / course.source_dir / course.course_id):
        if lesson.source_file and (base / lesson.source_file).is_file():
            return base / lesson.source_file
    raise Refused(f"{course.course_id} {lesson.lesson_id}: cannot find the English source file {lesson.source_file!r}")


def _source_forms(marker: str) -> List[str]:
    """The ways a marker can be spelt inside a Python string literal."""
    forms = [marker, marker.replace("'", "\\'"), marker.replace('"', '\\"'), json.dumps(marker, ensure_ascii=False)[1:-1]]
    # A marker that spans lines, in a file saved with Windows line endings (Python reads those back as "\n").
    forms.append(marker.replace("\n", "\r\n"))
    return list(dict.fromkeys(forms))


def _source_edit(text: str, marker: str, new: str, name: str, where: str) -> Tuple[str, str]:
    """The (old, new) text replacement that turns `marker` into `new` in a Python lesson module."""
    counts = [(form, text.count(form)) for form in _source_forms(marker)]
    found = [(form, n) for form, n in counts if n]
    if len(found) == 1 and found[0][1] == 1:
        old = found[0][0]
        keep = marker if new.startswith(marker) else ""     # unchanged text stays spelt the way the literal spells it
        tail = new[len(keep):]
        if "\n" in tail:       # several image lines: a line break must be spelt the way the literal spells it
            kind = literal_kind_at(text, text.find(old))
            if kind == "triple":
                tail = tail.replace("\n", "\r\n" if "\r\n" in text else "\n")
            elif kind == "single":
                tail = tail.replace("\n", "\\n")
            else:
                raise Refused(f"{where}: in {name}: the marker is in a raw or prefixed string - replace it by hand")
        new = (old if keep else "") + tail
        return old, new
    if not found:       # the marker is wrapped over several adjacent string literals
        try:
            return replace_in_literals(text, marker, new)
        except SourceEditError as exc:
            raise Refused(f"{where}: in {name}: {exc} - replace it by hand") from None
    raise Refused(f"{where}: the marker is not exactly once in {name} as written "
                  f"({sum(n for _f, n in counts)} matches) - replace it by hand")


def plan(link: Link) -> Tuple[CourseSpec, List[Tuple[Path, str, str, str, str]]]:
    """The edits for one link: [(file, old text, new text)], or raises `Refused`."""
    if isinstance(link, Placement):
        return plan_placement(link)
    course = _load(link.course)
    lesson = _lesson(course, link.lesson)
    where = f"{course.course_id} {lesson.lesson_id}"
    # One marker may take several images ("a,b,c"): they become consecutive lines, in this order.
    keys = [k.strip() for k in link.key.split(",") if k.strip()]
    if not keys:
        raise Refused(f"{where}: no image key given")
    known = {a.key for a in course.assets}
    placed = set(figure_keys(lesson.content))
    for key in keys:
        if not is_valid_key(key):
            raise Refused(f"{where}: {key!r} is not a valid image key")
        if key not in known:
            raise Refused(f"{where}: image '{key}' is not in {course.course_id}'s assets_manifest.json "
                          "(or its file is missing) - add it there first")
        if key in placed or keys.count(key) > 1:
            raise Refused(f"{where}: image '{key}' is already placed in this lesson")
    tokens = "\n".join("{{image:%s}}" % key for key in keys)
    english = requests_in(lesson.content)
    if link.marker.startswith("{{image:"):
        # add to an image that is already linked here: the new lines follow it
        marker = link.marker.strip()
        if lesson.content.count(marker) != 1:
            raise Refused(f"{where}: {marker} is not exactly once in this lesson")
        index, new = -1, marker + "\n" + tokens
    else:
        index = _select(english, link.marker, where)
        marker, new = english[index], tokens
    if not _on_own_line(lesson.content, marker):
        raise Refused(f"{where}: marker {index + 1} is inside a paragraph, not on a line of its own - "
                      "move it onto its own line by hand first")

    edits: List[Tuple[Path, str, str, str, str]] = []
    source = _source_path(course, lesson)
    text = source.read_text(encoding="utf-8")
    old_text, new_text = _source_edit(text, marker, new, source.name, where)
    edits.append((source, old_text, new_text, marker, new))

    folder = COURSES_ROOT / course.source_dir
    body = next((p for p in (folder / arabic.AR_DIR / f"{lesson.lesson_id}.md",
                             folder / course.course_id / arabic.AR_DIR / f"{lesson.lesson_id}.md") if p.is_file()), None)
    if body is not None:
        masked, error = arabic.read_body(body)
        if error:
            raise Refused(f"{where}: {error}")
        restored = arabic.R.restore_code(masked, arabic.R.protect_code(lesson.content or "")[1])
        theirs = requests_in(restored)
        if theirs != english:
            raise Refused(f"{where}: the Arabic file's markers differ from the English ones - fix `ar/` first")
        if figure_keys(restored) != figure_keys(lesson.content):
            raise Refused(f"{where}: the Arabic file places different images from the English - fix `ar/` first")
        nl = "\r\n" if b"\r\n" in body.read_bytes() else "\n"
        raw = body.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
        if raw.count(marker) != 1:
            raise Refused(f"{where}: the marker is not exactly once in ar/{body.name}")
        edits.append((body, marker.replace("\n", nl), new.replace("\n", nl), marker.replace("\n", nl), new.replace("\n", nl)))
    return course, edits


_TOKEN_LINE = re.compile(r"^\{\{image:[^{}\n]*\}\}$")


def _ends_a_block(text: str, snippet: str, where: str, label: str) -> str:
    """The text the new images follow. `snippet` (the last line or lines of a block) must appear once and end a block (a blank line
    follows it), outside a code block - or be the last line of a code block, when the images follow its closing fence."""
    if not snippet.strip():
        raise Refused(f"{where}: the {label} anchor is empty")
    count = text.count(snippet)
    if count != 1:
        raise Refused(f"{where}: the {label} anchor is in the text {count} times, not once: ...{snippet[-70:]!r}")
    end = text.index(snippet) + len(snippet)
    inside = text[:end].count("```") % 2 == 1
    if inside:
        rest = text[end + 4:]
        if text[end:end + 4] != "\n```" or not (rest.startswith("\n\n") or rest.strip() == ""):
            raise Refused(f"{where}: the {label} anchor is inside a code block but is not its last line: ...{snippet[-70:]!r}")
        return snippet + "\n```"
    if text[end:end + 2] != "\n\n" and text[end:].strip() != "":
        raise Refused(f"{where}: the {label} anchor does not end a block (a blank line must follow it): ...{snippet[-70:]!r}")
    return snippet


def _joiner(anchor: str) -> str:
    """Images that follow an image line join it as the next line; otherwise they are a block of their own."""
    return "\n" if _TOKEN_LINE.match(anchor.strip()) else "\n\n"


def _removals(text: str, removed: List[str], where: str, label: str) -> List[Tuple[str, str]]:
    """(old text, new text) pairs that take the named images out of the run of image lines that holds them."""
    lines = text.split("\n")
    groups: Dict[Tuple[int, int], List[str]] = {}
    for key in removed:
        pattern = re.compile(r"^\{\{image:%s(?:\|[^{}]*)?\}\}$" % re.escape(key))
        hits = [i for i, line in enumerate(lines) if pattern.match(line.strip())]
        if len(hits) != 1:
            raise Refused(f"{where}: {label}: image '{key}' is on {len(hits)} lines of its own, not one - move it by hand")
        first = last = hits[0]
        while first > 0 and _TOKEN_LINE.match(lines[first - 1].strip()):
            first -= 1
        while last < len(lines) - 1 and _TOKEN_LINE.match(lines[last + 1].strip()):
            last += 1
        groups.setdefault((first, last), []).append(key)
    out = []
    for (first, last), keys in groups.items():
        kept = [line for line in lines[first:last + 1] if not any(line.strip().startswith("{{image:%s" % k) and
                                                                  re.match(r"^\{\{image:%s(?:\||\})" % re.escape(k), line.strip())
                                                                  for k in keys)]
        if not kept:
            raise Refused(f"{where}: {label}: taking out {', '.join(keys)} would leave no image there - remove the line by hand")
        out.append(("\n".join(lines[first:last + 1]), "\n".join(kept)))
    return out


def plan_placement(link: "Placement") -> Tuple[CourseSpec, List[Tuple[Path, str, str, str, str]]]:
    """Edits that put images after a named block in both languages (and take moved images out of their old place)."""
    course = _load(link.course)
    lesson = _lesson(course, link.lesson)
    where = f"{course.course_id} {lesson.lesson_id}"
    keys = [k.strip() for k in link.key.split(",") if k.strip()]
    removed = [k.strip() for k in link.remove.split(",") if k.strip()]
    if not keys:
        raise Refused(f"{where}: no image key given")
    known = {a.key for a in course.assets}
    placed = set(figure_keys(lesson.content))
    for key in keys:
        if not is_valid_key(key):
            raise Refused(f"{where}: {key!r} is not a valid image key")
        if key not in known:
            raise Refused(f"{where}: image '{key}' is not in {course.course_id}'s assets_manifest.json "
                          "(or its file is missing) - add it there first")
        if keys.count(key) > 1 or (key in placed and key not in removed):
            raise Refused(f"{where}: image '{key}' is already placed in this lesson")
    for key in removed:
        if key not in placed:
            raise Refused(f"{where}: image '{key}' is not placed in this lesson, so it cannot be moved")
    tokens = "\n".join("{{image:%s}}" % key for key in keys)

    english = lesson.content
    anchor = _ends_a_block(english, link.marker, where, "English")
    steps = _removals(english, removed, where, "English") if removed else []
    for old, _new in steps:
        if english.count(old) != 1:
            raise Refused(f"{where}: the image lines being changed are not exactly once in this lesson")
    steps.append((anchor, anchor + _joiner(anchor) + tokens))

    edits: List[Tuple[Path, str, str, str, str]] = []
    source = _source_path(course, lesson)
    text = source.read_text(encoding="utf-8")
    for marker, new in steps:
        old_text, new_text = _source_edit(text, marker, new, source.name, where)
        edits.append((source, old_text, new_text, marker, new))

    folder = COURSES_ROOT / course.source_dir
    body = next((p for p in (folder / arabic.AR_DIR / f"{lesson.lesson_id}.md",
                             folder / course.course_id / arabic.AR_DIR / f"{lesson.lesson_id}.md") if p.is_file()), None)
    if body is not None:
        masked, error = arabic.read_body(body)
        if error:
            raise Refused(f"{where}: {error}")
        restored = arabic.R.restore_code(masked, arabic.R.protect_code(lesson.content or "")[1])
        if figure_keys(restored) != figure_keys(lesson.content):
            raise Refused(f"{where}: the Arabic file places different images from the English - fix `ar/` first")
        if not link.after_ar:
            raise Refused(f"{where}: this lesson has an Arabic file - give `after_ar`, the Arabic block the images follow")
        nl = "\r\n" if b"\r\n" in body.read_bytes() else "\n"
        raw = body.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
        anchor_ar = _ends_a_block(raw, link.after_ar, where, "Arabic")
        ar_steps = _removals(raw, removed, where, "Arabic") if removed else []
        for old, _new in ar_steps:
            if raw.count(old) != 1:
                raise Refused(f"{where}: the Arabic image lines being changed are not exactly once in ar/{body.name}")
        ar_steps.append((anchor_ar, anchor_ar + _joiner(anchor_ar) + tokens))
        for old, new in ar_steps:
            edits.append((body, old.replace("\n", nl), new.replace("\n", nl), old.replace("\n", nl), new.replace("\n", nl)))
    return course, edits


def _stored_hash(course: CourseSpec, lesson: LessonSpec) -> Tuple[Optional[Path], Optional[str], bool]:
    """(the Arabic JSON, the hash it stores, whether that hash matches the English as it is now)."""
    folder = COURSES_ROOT / course.source_dir
    for base in (folder, folder / course.course_id):
        path = base / arabic.AR_DIR / f"{lesson.lesson_id}.json"
        if path.is_file():
            stored = json.loads(path.read_text(encoding="utf-8")).get("source_hash")
            payload = arabic.source_payload(lesson, arabic.questions_by_lesson(course).get(lesson.lesson_id, []))
            return path, stored, stored == arabic.source_hash(payload)
    return None, None, False


def apply_links(links: List[Link], write: bool) -> int:
    """Plan every link, then (with `write`) apply them all or none. Returns the exit code."""
    plans = []
    for link in links:
        label = f"{link.course} {link.lesson} marker {link.marker} -> {link.key}"
        try:
            plans.append((link, *plan(link)))
        except Refused as exc:
            print(f"REFUSED  {label}\n         {exc}")
            return 1
        print(f"{'WILL REPLACE' if write else 'would replace'}  {label}")
        for path, old, new, _marker, _token in plans[-1][2]:
            print(f"         {path.relative_to(COURSES_ROOT).as_posix()}: {old[:90]}{'...' if len(old) > 90 else ''}  ->  {new}")
    if not write:
        print("\nNothing written (add --write).")
        return 0

    # What is wrong today (so only NEW problems revert the change), and which Arabic hashes are current.
    _remember_baseline([link.course for link, *_ in plans])
    fresh: Dict[Path, bool] = {}
    for link, course, _edits in plans:
        path, _stored, ok = _stored_hash(course, _lesson(course, link.lesson))
        if path is not None:
            fresh[path] = ok
    originals: Dict[Path, str] = {}
    try:
        for _link, _course, edits in plans:
            for path, old, new, marker, token in edits:
                if path not in originals:
                    originals[path] = path.read_bytes().decode("utf-8")
                current = path.read_bytes().decode("utf-8")
                if path.suffix == ".py":
                    # an earlier link in this run may have rewritten a fragment this marker shares
                    old, new = _source_edit(current, marker, token, path.name, "this run")
                if current.count(old) != 1:
                    raise Refused(f"{path.name}: two links in one run touch the same marker")
                path.write_bytes(current.replace(old, new, 1).encode("utf-8"))
        for course_id in dict.fromkeys(link.course for link, *_ in plans):
            course = _load(course_id)
            for link, *_ in (p for p in plans if p[0].course == course_id):
                lesson = _lesson(course, link.lesson)
                path, stored, _ = _stored_hash(course, lesson)
                if path is not None and fresh.get(path):
                    payload = arabic.source_payload(lesson, arabic.questions_by_lesson(course).get(lesson.lesson_id, []))
                    if path not in originals:
                        originals[path] = path.read_bytes().decode("utf-8")
                    path.write_bytes(path.read_bytes().decode("utf-8").replace(stored, arabic.source_hash(payload), 1).encode("utf-8"))
            course = _load(course_id)
            before = len(_baseline.get(course_id, []))
            found = images.problems(course) + course.asset_problems + course.arabic_problems
            if len(found) > before:
                raise Refused(f"{course_id}: validation found {len(found) - before} new problem(s) after the change:\n    "
                              + "\n    ".join(found[:5]))
    except Refused as exc:
        for path, text in originals.items():
            path.write_bytes(text.encode("utf-8"))
        print(f"\nREVERTED  {exc}")
        return 1
    print(f"\nWrote {len(originals)} file(s).")
    return 0


_baseline: Dict[str, List[str]] = {}


def _remember_baseline(course_ids: List[str]) -> None:
    for course_id in dict.fromkeys(course_ids):
        course = _load(course_id)
        _baseline[course_id] = images.problems(course) + course.asset_problems + course.arabic_problems


def list_markers(course_id: str, lesson_id: Optional[str]) -> int:
    course = _load(course_id)
    placed = {key for _l, _lang, key in images.references(course)}
    print(course.course_id)
    for lesson in course.lessons:
        if lesson_id and lesson.lesson_id != lesson_id:
            continue
        markers = requests_in(lesson.content)
        if not markers:
            continue
        print(f"  {lesson.lesson_id}  ({len(markers)} waiting)")
        for number, marker in enumerate(markers, start=1):
            own = "" if _on_own_line(lesson.content, marker) else "   [inside a paragraph]"
            print(f"    {number:>3}. {marker[:120]}{'...' if len(marker) > 120 else ''}{own}")
    free = [a for a in course.assets if a.key not in placed]
    print(f"  manifest images no lesson places yet: {len(free)}")
    for asset in free:
        print(f"    {asset.key}   {asset.file}" + (f"   (lesson {asset.lesson})" if asset.lesson else ""))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p_list = sub.add_parser("list")
    p_list.add_argument("--course", required=True)
    p_list.add_argument("--lesson")
    p_place = sub.add_parser("place")
    p_place.add_argument("--map", required=True, help="JSON file: a list of {course, lesson, key, after, after_ar, remove?}")
    p_place.add_argument("--write", action="store_true")
    p_replace = sub.add_parser("replace")
    p_replace.add_argument("--course")
    p_replace.add_argument("--lesson")
    p_replace.add_argument("--marker", help="the marker's number from `list`, or a unique piece of its text")
    p_replace.add_argument("--key")
    p_replace.add_argument("--map", help="JSON file: a list of {course, lesson, marker, key}")
    p_replace.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "list":
            return list_markers(args.course, args.lesson)
        if args.command == "place":
            entries = json.loads(Path(args.map).read_text(encoding="utf-8"))
            placements = [Placement(e["course"], e["lesson"], e["after"], e["key"], e.get("after_ar", ""), e.get("remove", ""))
                          for e in entries]
            return apply_links(placements, args.write)
        if args.map:
            entries = json.loads(Path(args.map).read_text(encoding="utf-8"))
            links = [Link(e["course"], e["lesson"], str(e["marker"]), e["key"]) for e in entries]
        elif args.course and args.lesson and args.marker is not None and args.key:
            links = [Link(args.course, args.lesson, str(args.marker), args.key)]
        else:
            parser.error("replace needs --map, or all of --course --lesson --marker --key")
        return apply_links(links, args.write)
    except Refused as exc:
        print(f"REFUSED  {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
