import json
from typing import Any


class EmptyProviderReply(RuntimeError):
    """The provider answered, but with no text to show."""


def require_text(raw: Any) -> str:
    """The provider's answer, or EmptyProviderReply if there is none.

    A model can return nothing at all (a refusal, a length cutoff before the
    first token). Callers that carry on regardless turn that into a paid
    blank — an empty review, a 0% readiness score, a blank interview question
    — or crash in the JSON parser. Raising instead lets the controller
    refund and tell the student to try again.
    """
    if not isinstance(raw, str) or not raw.strip():
        raise EmptyProviderReply("the provider returned no text")
    return raw


def _iter_balanced_objects(text: str):
    """Yields each substring of `text` that is a balanced top-level
    {...} block, in the order they appear. Doesn't validate JSON —
    just brace-matching."""
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    yield text[start:i + 1]
                    start = None


def parse_json_response(raw: str, fallback: Any) -> Any:
    """
    Extract and parse a JSON object from an LLM response. Handles:
      - a clean JSON object as the entire response (the common case)
      - JSON wrapped in ```json ... ``` fences
      - prose commentary before and/or after the JSON object — some
        models "think out loud" first even when told to return only
        JSON, especially without a strict JSON-mode flag

    Tries each candidate in order and returns the first that parses as
    a dict. Returns `fallback` if nothing in the response parses.
    """
    text = raw.strip()
    if text.startswith("```"):
        # Strip a single pair of code fences (```json ... ``` or ``` ... ```)
        # without assuming they're the only content on their lines.
        text = text.lstrip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.rstrip("`").strip()

    # Fast path: the whole (fence-stripped) string is valid JSON.
    try:
        candidate = json.loads(text)
        if isinstance(candidate, dict):
            return candidate
    except json.JSONDecodeError:
        pass

    # Slow path: scan for balanced {...} blocks anywhere in the original
    # raw text (prose before/after is common) and use the first that
    # parses as a JSON object.
    for block in _iter_balanced_objects(raw):
        try:
            candidate = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            return candidate

    return fallback
