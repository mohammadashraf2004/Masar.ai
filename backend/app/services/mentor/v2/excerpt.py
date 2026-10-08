"""The part of a lesson the mentor sends to the model.

Real lessons are long (median ~33k characters, up to ~73k) and every provider message is clipped
to INPUT_DEFAULT_MAX_CHARACTERS, so sending "the lesson" meant sending its first third and
silently dropping the rest. Instead the lesson is cut at its headings into sections, and the
model gets: the outline (so it knows what the lesson covers), the opening, the section holding
the text the learner selected, and the sections whose words best match the question - in
lesson order, within a character budget. It is deterministic word overlap over the lesson's
own text: no embeddings, no second copy of the content.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

MAX_CHUNK_CHARS = 1_800
INTRO_CHARS = 900
OUTLINE_CHARS = 900
GAP = "\n\n[...]\n\n"

_HEADING = re.compile(r"^(#{1,4})\s+(.+?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")
_ARABIC_MARKS = re.compile(r"[ً-ْـ]")

# Words that say nothing about which section a question is about.
_STOP = {
    "the", "and", "for", "are", "but", "not", "you", "your", "with", "this", "that", "these", "those",
    "what", "why", "how", "when", "where", "which", "who", "does", "did", "can", "could", "would",
    "should", "will", "into", "from", "about", "than", "then", "there", "their", "they", "them",
    "have", "has", "had", "was", "were", "been", "being", "its", "it's", "also", "more", "most",
    "some", "such", "only", "very", "just", "like", "please", "explain", "mean", "means", "meaning",
    "simply", "simpler", "example", "another", "give", "tell", "understand", "dont", "don't",
    "lesson", "here", "use", "used", "using", "one", "two", "get", "make",
    "في", "من", "على", "إلى", "الى", "عن", "مع", "هذا", "هذه", "ذلك", "تلك", "التي", "الذي", "الذين",
    "ما", "ماذا", "لماذا", "كيف", "متى", "أين", "هل", "لا", "نعم", "أو", "او", "ثم", "كان", "كانت",
    "يكون", "هو", "هي", "هم", "نحن", "أنا", "انا", "انت", "أنت", "اشرح", "وضح", "بسط", "مثال", "يعني",
    "الدرس", "لكن", "لأن", "لان", "بين", "كل", "بعض", "عند", "اذا", "إذا", "قد", "لقد",
}


def _fold(text: str) -> str:
    text = _ARABIC_MARKS.sub("", text.lower())
    return text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")


def terms(text: Optional[str]) -> set[str]:
    """Content words of `text`, case/diacritic folded, Arabic and English."""
    if not text:
        return set()
    words = re.findall(r"[a-z0-9_]+|[؀-ۿ]+", _fold(text))
    return {word for word in words if len(word) >= 3 and word not in _STOP}


def plain(text: Optional[str]) -> str:
    """Markdown reduced to the words a reader sees, for comparing a selection with the source."""
    if not text:
        return ""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)            # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)          # links keep their text
    text = re.sub(r"\{\{[^}]*\}\}", " ", text)                     # {{figure:...}} markers
    text = re.sub(r"[*_`#>|~$\\]", " ", text)                       # emphasis, code, quotes, math
    return re.sub(r"\s+", " ", _fold(text)).strip()


@dataclass(frozen=True)
class Chunk:
    index: int
    heading: str
    text: str


def chunks(markdown: str) -> List[Chunk]:
    """Split at headings (never inside a code fence); long sections split at blank lines."""
    sections: List[tuple[str, List[str]]] = [("", [])]
    in_fence = False
    for line in markdown.splitlines():
        if _FENCE.match(line):
            in_fence = not in_fence
        match = None if in_fence else _HEADING.match(line)
        if match:
            sections.append((match.group(2).strip(), [line]))
        else:
            sections[-1][1].append(line)

    out: List[Chunk] = []
    for heading, lines in sections:
        body = "\n".join(lines).strip()
        if not body:
            continue
        if len(body) <= MAX_CHUNK_CHARS:
            out.append(Chunk(len(out), heading, body))
            continue
        current = ""
        for para in re.split(r"\n\s*\n", body):
            if current and len(current) + len(para) + 2 > MAX_CHUNK_CHARS:
                out.append(Chunk(len(out), heading, current))
                current = ""
            if len(para) > MAX_CHUNK_CHARS:
                for start in range(0, len(para), MAX_CHUNK_CHARS):
                    out.append(Chunk(len(out), heading, para[start:start + MAX_CHUNK_CHARS]))
                continue
            current = f"{current}\n\n{para}" if current else para
        if current:
            out.append(Chunk(len(out), heading, current))
    return out


def outline(markdown: str) -> str:
    headings: List[str] = []
    in_fence = False
    for line in markdown.splitlines():
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        match = None if in_fence else _HEADING.match(line)
        if match and len(match.group(1)) <= 3:
            headings.append(match.group(2).strip())
    text = " | ".join(headings)
    return text[:OUTLINE_CHARS]


def lesson_excerpt(markdown: str, *, query: str, selected: Optional[str], budget: int) -> str:
    """The lesson itself when it fits `budget`, else its outline, opening and best sections."""
    markdown = markdown or ""
    if len(markdown) <= budget:
        return markdown
    parts = chunks(markdown)
    if not parts:
        return markdown[:budget]
    wanted = terms(query)
    selected_plain = plain(selected)

    def score(chunk: Chunk) -> float:
        body = terms(chunk.text)
        value = len(wanted & body) + 2 * len(wanted & terms(chunk.heading))
        if selected_plain and len(selected_plain) >= 8 and selected_plain in plain(chunk.text):
            value += 1_000
        return value

    head = f"Lesson outline: {outline(markdown)}\n\n"
    room = budget - len(head)
    intro = parts[0].text[:INTRO_CHARS]
    picked = {0: intro}
    room -= len(intro) + len(GAP)
    scored = sorted(((score(c), c) for c in parts[1:]), key=lambda pair: (-pair[0], pair[1].index))
    relevant = [c for s, c in scored if s > 0]
    # Nothing in the question points anywhere ("explain this more simply" with no selection):
    # read on from the opening, which is where a learner who just arrived is.
    for chunk in (relevant or [c for _, c in sorted(scored, key=lambda pair: pair[1].index)]):
        cost = len(chunk.text) + len(GAP)
        if cost > room:
            continue
        picked[chunk.index] = chunk.text
        room -= cost
        if room < 200:
            break

    ordered = sorted(picked)
    text = ""
    for position, index in enumerate(ordered):
        if position:
            text += "\n\n" if index == ordered[position - 1] + 1 else GAP
        text += picked[index]
    return head + text
