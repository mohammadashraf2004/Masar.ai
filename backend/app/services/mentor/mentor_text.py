"""Small text helpers shared by Mentor v2 retrieval and validation.

Deliberately simple lexical matching, no embeddings: the mentor's context
is one lesson, its module and its prerequisites, small enough that word
overlap ranks it well. The same normalisation is used for retrieval and
for the validator's "is this actually in the course?" check, so the two
agree on what counts as a match.
"""
import re
from typing import Iterable, List, Set

_DIACRITICS = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
_TOKEN = re.compile(r"[\w؀-ۿ]+", re.UNICODE)
_ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

_STOPWORDS = {
    # English
    "the", "and", "for", "are", "but", "not", "you", "your", "with", "this", "that",
    "from", "have", "has", "was", "were", "what", "why", "how", "when", "which", "who",
    "can", "does", "into", "its", "our", "out", "use", "using", "will", "would", "then",
    "than", "them", "they", "there", "here", "about", "each", "also", "just", "like",
    # Arabic (already normalised: no hamza forms, ة→ه, ى→ي)
    "في", "من", "علي", "الي", "عن", "مع", "هذا", "هذه", "ذلك", "تلك", "التي", "الذي",
    "كان", "كانت", "يكون", "او", "ثم", "لكن", "لان", "اذا", "ان", "انه", "انها", "كل",
    "بعد", "قبل", "عند", "هو", "هي", "هم", "نحن", "انت", "ما", "ماذا", "لماذا", "كيف",
    "متي", "اين", "هل", "لا", "نعم", "قد", "لقد", "به", "بها", "له", "لها", "ليش", "ليه",
    "شو", "ايش", "يعني", "اصلا", "بس", "مش",
}


def normalize(text: str) -> str:
    text = (text or "").lower().translate(_ARABIC_DIGITS)
    text = _DIACRITICS.sub("", text)
    return (
        text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
        .replace("ة", "ه").replace("ى", "ي")
    )


def tokens(text: str) -> List[str]:
    out = []
    for tok in _TOKEN.findall(normalize(text)):
        # Arabic definite article: "الذاكرة" and "ذاكرة" should match.
        if tok.startswith("ال") and len(tok) > 4:
            tok = tok[2:]
        if len(tok) < 3 or tok in _STOPWORDS:
            continue
        out.append(tok)
    return out


def token_set(text: str) -> Set[str]:
    return set(tokens(text))


def overlap(a: Iterable[str], b: Set[str]) -> int:
    return len(set(a) & b)


def squash(text: str) -> str:
    """Whitespace- and case-insensitive form for "does X appear in Y"."""
    return re.sub(r"\s+", " ", normalize(text)).strip()


def split_chunks(markdown: str, max_chars: int = 700) -> List[str]:
    """Split a lesson body into paragraph-sized chunks, keeping fenced code
    blocks whole so a retrieved snippet is never half a function."""
    if not markdown:
        return []
    parts: List[str] = []
    buf: List[str] = []
    in_fence = False
    for line in markdown.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            buf.append(line)
            if not in_fence:
                parts.append("\n".join(buf))
                buf = []
            continue
        if in_fence:
            buf.append(line)
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            if buf:
                parts.append("\n".join(buf))
                buf = []
            if line.strip():
                buf.append(line)
            continue
        buf.append(line)
    if buf:
        parts.append("\n".join(buf))

    chunks: List[str] = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        while len(p) > max_chars:
            chunks.append(p[:max_chars])
            p = p[max_chars:]
        # A lone heading carries the topic but no content; fold it into the
        # next chunk rather than ranking it on its own.
        if chunks and chunks[-1].lstrip().startswith("#") and "\n" not in chunks[-1]:
            chunks[-1] = chunks[-1] + "\n" + p
        else:
            chunks.append(p)
    return chunks
