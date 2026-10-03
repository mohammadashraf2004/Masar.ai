"""
app/services/assets/urls.py

The URL a lesson block carries for a figure.

Lesson responses are only sent to a learner who may read the lesson, and an
`<img>` element cannot send an Authorization header, so the URL itself is the
credential: it names the course and the figure and carries an expiry and an HMAC
of the three, made with the server's secret. Nobody can mint one, and one leaked
into a screenshot stops working in days.

The expiry is rounded to a day boundary, so the URL is the same for every learner
and every request during that day - the browser (and any CDN) can cache the image
- and changes once a day.

This is also the single place that decides what a figure's URL looks like. Serving
figures from a CDN later means changing `asset_url` (return the CDN's URL for the
asset's `storage_key`); lesson text, blocks and the browser are unaffected. The
path is relative to the API root, so the browser resolves it against whatever base
URL the deployment uses.
"""
from __future__ import annotations

import hashlib
import hmac
import time
from typing import Optional

from app.core.config import settings

_DAY = 86400
# A URL minted on day N stays valid until the end of day N+2: at least two full days.
_VALID_DAYS = 3


def _mac(course_slug: str, key: str, expires: int) -> str:
    message = f"course-asset|{course_slug}|{key}|{expires}".encode()
    return hmac.new(settings.SECRET_KEY.encode(), message, hashlib.sha256).hexdigest()[:32]


def _expiry(now: float) -> int:
    return (int(now // _DAY) + _VALID_DAYS) * _DAY


def asset_url(course_slug: str, key: str, *, now: Optional[float] = None) -> str:
    expires = _expiry(time.time() if now is None else now)
    return f"/learning/courses/{course_slug}/assets/{key}?exp={expires}&sig={_mac(course_slug, key, expires)}"


def is_valid(course_slug: str, key: str, expires: int, signature: str, *, now: Optional[float] = None) -> bool:
    if expires <= (time.time() if now is None else now):
        return False
    return hmac.compare_digest(_mac(course_slug, key, expires), signature or "")
