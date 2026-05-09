import json
from typing import Any


def parse_json_response(raw: str, fallback: Any) -> Any:
    """
    Strip markdown fences and parse JSON.
    Returns fallback if parsing fails.
    """
    try:
        clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(clean)
    except (json.JSONDecodeError, ValueError):
        return fallback
