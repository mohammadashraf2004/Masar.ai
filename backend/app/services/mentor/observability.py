"""One structured log line per mentor request, for every mentor mode.

The line carries what production debugging needs - mode, the resource ids, provider usage,
context size, what was charged, the outcome and a coarse error category - and deliberately
nothing private: no message text, no lesson text, no code, no tokens or secrets. The fields
are written into the message as JSON because the app's log format prints only the message;
they are also attached as `extra["mentor"]` for a structured handler.
"""
from __future__ import annotations

import json
import logging
import time
from contextlib import contextmanager
from typing import Any, Dict, Iterator, Optional

from app.core.metrics import collect_llm_usage

logger = logging.getLogger("app.mentor.events")

# The categories a failure is reported under. Free text never goes in the log line.
ERROR_CATEGORIES = {
    "insufficient_credits", "access_denied", "not_found", "invalid_request",
    "provider_error", "validation_failed", "internal_error", "limit_reached",
}


class MentorEvent:
    """Fields for one mentor request, filled in as it runs and logged once at the end."""

    def __init__(self, mode: str, user_id: int) -> None:
        self.fields: Dict[str, Any] = {"mentor_mode": mode, "user_id": user_id}
        self.outcome = "success"
        self.error_category: Optional[str] = None

    def set(self, **fields: Any) -> None:
        self.fields.update({key: value for key, value in fields.items() if value is not None})

    def fail(self, category: str) -> None:
        self.outcome = "failure"
        self.error_category = category if category in ERROR_CATEGORIES else "internal_error"


def _category_for_status(status: int) -> str:
    if status == 402:
        return "insufficient_credits"
    if status == 403:
        return "access_denied"
    if status == 404:
        return "not_found"
    if status in (409, 422):
        return "invalid_request"
    if status == 429:
        # A rate limit, the Pro allowance or the validation-failure pause: refused before any charge.
        return "limit_reached"
    if status == 503:
        return "provider_error"
    return "internal_error"


@contextmanager
def mentor_event(mode: str, user_id: int) -> Iterator[MentorEvent]:
    """Time a mentor request, collect its provider usage, and log one line when it ends -
    whether it returned, raised an HTTP error, or crashed."""
    from fastapi import HTTPException  # local: keep this module import-light

    event = MentorEvent(mode, user_id)
    started = time.perf_counter()
    with collect_llm_usage() as usage:
        try:
            yield event
        except HTTPException as exc:
            if event.outcome == "success":
                event.fail(_category_for_status(exc.status_code))
            raise
        except Exception:
            if event.outcome == "success":
                event.fail("internal_error")
            raise
        finally:
            calls = list(usage)
            event.set(
                latency_ms=int((time.perf_counter() - started) * 1000),
                provider_calls=len(calls),
                provider=calls[-1]["provider"] if calls else None,
                model=calls[-1]["model"] if calls else None,
                input_tokens=sum(c["input_tokens"] for c in calls) if calls else None,
                output_tokens=sum(c["output_tokens"] for c in calls) if calls else None,
            )
            event.fields["outcome"] = event.outcome
            if event.error_category:
                event.fields["error_category"] = event.error_category
            try:
                logger.info("mentor_event %s", json.dumps(event.fields, sort_keys=True, default=str),
                            extra={"mentor": dict(event.fields)})
            except Exception:  # noqa: BLE001 - telemetry must never break a request
                pass
