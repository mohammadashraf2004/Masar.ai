"""Reusable validators that any project can use through validator_config."""
from __future__ import annotations

import re

from ..validation import CheckResult, ValidationContext, ValidationResult, from_checks, validator

_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S")
_WORD = re.compile(r"\w+")


def _norm(heading: str) -> str:
    return heading.strip().rstrip(":：").strip().casefold()


def sections(markdown: str) -> dict[str, str]:
    """Every heading (normalised) -> the body under it, up to the next heading
    of the same or a higher level. A repeated heading keeps its first body."""
    lines = markdown.splitlines()
    found: dict[str, str] = {}
    for index, line in enumerate(lines):
        match = _HEADING.match(line)
        if not match:
            continue
        level = len(match.group(1))
        body = []
        for following in lines[index + 1:]:
            nxt = _HEADING.match(following)
            if nxt and len(nxt.group(1)) <= level:
                break
            body.append(following)
        found.setdefault(_norm(match.group(2)), "\n".join(body))
    return found


def find_section(markdown: str, heading: str, aliases: list[str] | tuple[str, ...] = ()) -> str | None:
    """The body under `heading` or any of its aliases (e.g. the Arabic
    heading), or None when the document has none of them."""
    found = sections(markdown)
    for name in (heading, *aliases):
        if _norm(name) in found:
            return found[_norm(name)]
    return None


def own_text(body: str, template_lines: set[str]) -> str:
    """The section without the template's placeholder lines, so words the
    learner did not write never count."""
    return "\n".join(line for line in body.splitlines() if line.strip() and line.strip() not in template_lines)


def word_count(text: str) -> int:
    return len(_WORD.findall(text))


def item_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if _ITEM.match(line))


def _quote(heading: str, aliases: list[str]) -> tuple[str, str]:
    en = f"“{heading}”"
    ar = f"“{heading}”" + (f" (أو “{aliases[0]}”)" if aliases else "")
    return en, ar


def section_checks(ctx: ValidationContext, path: str, spec: dict) -> list[CheckResult]:
    """Checks for one section spec:
        heading, aliases, min_words, min_items,
        terms: [{"any": [...], "label": {"en", "ar"}}]  (each must appear)
    """
    heading = spec["heading"]
    aliases = list(spec.get("aliases", []))
    slug = re.sub(r"[^a-z0-9]+", "_", heading.casefold()).strip("_")
    en_name, ar_name = _quote(heading, aliases)
    try:
        template_lines = {line.strip() for line in ctx.template.read_text(path).splitlines()}
    except KeyError:
        template_lines = set()
    body = find_section(ctx.file_text(path) or "", heading, aliases)
    present = body is not None
    text = own_text(body or "", template_lines)
    checks = [CheckResult(
        f"{slug}_present", present,
        None if present else {
            "en": f"Keep the {en_name} heading in {path} and write under it.",
            "ar": f"أبقِ العنوان {ar_name} في {path} واكتب تحته.",
        },
        label={"en": f"{en_name} section", "ar": f"قسم {ar_name}"},
    )]
    min_words = int(spec.get("min_words", 0))
    if min_words:
        ok = present and word_count(text) >= min_words
        checks.append(CheckResult(f"{slug}_written", ok, None if ok else {
            "en": f"Under {en_name}, replace the placeholder with your own writing — at least {min_words} words.",
            "ar": f"تحت {ar_name} استبدل النص المؤقت بكتابتك أنت — {min_words} كلمة على الأقل.",
        }, label={"en": f"{en_name} is written in your own words", "ar": f"{ar_name} مكتوب بكلماتك"}))
    min_items = int(spec.get("min_items", 0))
    if min_items:
        ok = present and item_count(text) >= min_items
        checks.append(CheckResult(f"{slug}_items", ok, None if ok else {
            "en": f"List at least {min_items} separate points under {en_name}, one per line starting with “-”.",
            "ar": f"اكتب {min_items} نقاط منفصلة على الأقل تحت {ar_name}، كل نقطة في سطر يبدأ بـ “-”.",
        }, label={"en": f"{en_name} has at least {min_items} points", "ar": f"في {ar_name} {min_items} نقاط على الأقل"}))
    lowered = text.casefold()
    for index, term in enumerate(spec.get("terms", [])):
        ok = present and any(option.casefold() in lowered for option in term["any"])
        label = term["label"]
        checks.append(CheckResult(f"{slug}_term_{index}", ok, None if ok else term.get("message", {
            "en": f"{en_name} should cover: {label['en']}.",
            "ar": f"يجب أن يتناول {ar_name}: {label['ar']}.",
        }), label=label))
    return checks


@validator("common.markdown_sections")
async def markdown_sections(ctx: ValidationContext) -> ValidationResult:
    """A Markdown file has the required sections, each written by the learner.

    config: file, sections: [section spec, ...] (see section_checks).
    """
    path = ctx.config["file"]
    checks: list[CheckResult] = []
    for spec in ctx.config["sections"]:
        checks.extend(section_checks(ctx, path, spec))
    return from_checks(checks)


@validator("common.markdown_section")
async def markdown_section(ctx: ValidationContext) -> ValidationResult:
    """One section. config: file, heading, aliases, min_words."""
    spec = {"heading": ctx.config["heading"], "aliases": ctx.config.get("aliases", []),
            "min_words": int(ctx.config.get("min_words", 10))}
    return from_checks(section_checks(ctx, ctx.config["file"], spec))
