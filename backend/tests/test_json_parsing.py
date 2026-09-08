"""
Regression tests for app.services.utils.parse_json_response — this is
shared by every LLM feature (mentor chat, code review, skill gap,
interview, roadmap, answer evaluation). A live test against a real LLM
response surfaced the bug this file guards against: some models emit
prose commentary before or after the JSON object even when told to
return only JSON, and the old implementation only handled a response
that was purely JSON.
"""
from app.services.utils import parse_json_response

FALLBACK = {"reply": "fallback", "is_correct": None}


def test_pure_json():
    raw = '{"reply": "hi", "is_correct": true, "score": 100}'
    result = parse_json_response(raw, FALLBACK)
    assert result == {"reply": "hi", "is_correct": True, "score": 100}


def test_json_wrapped_in_markdown_fence():
    raw = '```json\n{"reply": "hi", "score": 90}\n```'
    result = parse_json_response(raw, FALLBACK)
    assert result == {"reply": "hi", "score": 90}


def test_json_wrapped_in_bare_fence():
    raw = '```\n{"reply": "hi"}\n```'
    result = parse_json_response(raw, FALLBACK)
    assert result == {"reply": "hi"}


def test_prose_before_json():
    raw = 'Sure, here you go:\n\n{"reply": "hi", "score": 80}'
    result = parse_json_response(raw, FALLBACK)
    assert result == {"reply": "hi", "score": 80}


def test_prose_after_json_the_exact_live_bug():
    """This is the exact shape a real GPT-4o response took in production:
    a full prose reply, followed by a duplicate JSON object. The old
    parser fell back to `fallback` here, silently discarding a
    perfectly valid is_correct=True/score=100 verdict."""
    raw = (
        "That's a concise and accurate explanation! LangChain serves as an "
        "orchestration layer...\n\n"
        "How do you think integrating tools like retrievers or memory can "
        "enhance the capabilities of an LLM within the LangChain framework?\n\n"
        '{\n'
        '  "reply": "That\'s a concise and accurate explanation!",\n'
        '  "is_correct": true,\n'
        '  "score": 100,\n'
        '  "suggested_actions": ["Discuss retrievers", "Talk about memory"]\n'
        '}'
    )
    result = parse_json_response(raw, FALLBACK)
    assert result["is_correct"] is True
    assert result["score"] == 100
    assert result["suggested_actions"] == ["Discuss retrievers", "Talk about memory"]


def test_nested_braces_inside_string_values():
    raw = '{"reply": "use a dict like {\\"a\\": 1}", "score": 50}'
    result = parse_json_response(raw, FALLBACK)
    assert result["score"] == 50


def test_garbage_returns_fallback():
    raw = "I couldn't figure out how to respond in JSON, sorry!"
    result = parse_json_response(raw, FALLBACK)
    assert result == FALLBACK


def test_empty_string_returns_fallback():
    assert parse_json_response("", FALLBACK) == FALLBACK


def test_json_array_extracts_inner_object():
    # A bare top-level array isn't what any caller expects (every system
    # prompt in this codebase asks for a {...} object) — but if the model
    # wraps its object in a list anyway, pulling the inner object out is
    # more useful than discarding a perfectly good response.
    raw = '[{"a": 1}]'
    result = parse_json_response(raw, FALLBACK)
    assert result == {"a": 1}
