"""
app/services/assets/store.py

Where a course figure's bytes live, behind one small interface.

Today they are files in the courses folder that ships with the API image
(`LocalCourseAssetStore`). Tomorrow they can be an S3 bucket behind CloudFront:
write a store whose `response()` redirects to a signed object URL, return it from
`get_asset_store()`, and nothing else changes - not the lessons (they name a figure
key), not the database (`course_assets.storage_key` is just an opaque key the store
understands), not the browser (it follows the URL the API hands it).

The local store is the security boundary for the filesystem: it will only ever open
a file that sits inside its root, and only by a `storage_key` that came from the
database, never from a request.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Protocol

from fastapi import Response
from fastapi.responses import FileResponse

# backend/courses - the same folder the curriculum importer reads.
COURSES_ROOT = Path(__file__).resolve().parents[3] / "courses"

# A figure is content that changes only when a course is re-imported with a new
# file, and that changes its ETag. A day is long enough to matter and short enough
# that a corrected figure reaches learners the next morning.
CACHE_CONTROL = "private, max-age=86400"


class AssetStore(Protocol):
    def response(self, storage_key: str, *, mime_type: str, etag: str) -> Optional[Response]:
        """The HTTP response that delivers the asset, or None if it is not there."""


class LocalCourseAssetStore:
    def __init__(self, root: Path = COURSES_ROOT):
        self.root = root.resolve()

    def resolve(self, storage_key: str) -> Optional[Path]:
        """The file for `storage_key`, or None when it is absent or would leave the
        root (`..`, an absolute path, a symlink out). Resolving first and checking
        containment after is what defeats every traversal spelling at once."""
        if not storage_key or "\0" in storage_key:
            return None
        candidate = (self.root / storage_key).resolve()
        if self.root not in candidate.parents:
            return None
        return candidate if candidate.is_file() else None

    def response(self, storage_key: str, *, mime_type: str, etag: str) -> Optional[Response]:
        path = self.resolve(storage_key)
        if path is None:
            return None
        return FileResponse(
            path, media_type=mime_type,
            headers={
                "ETag": f'"{etag}"', "Cache-Control": CACHE_CONTROL,
                "Content-Disposition": "inline", "X-Content-Type-Options": "nosniff",
            },
        )


_store: AssetStore = LocalCourseAssetStore()


def get_asset_store() -> AssetStore:
    return _store
