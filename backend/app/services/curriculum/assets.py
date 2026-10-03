"""
app/services/curriculum/assets.py

Reads a course folder's `assets_manifest.json` into `AssetSpec`s.

    {
      "version": 1,
      "assets": [
        {"key": "lora-low-rank-adaptation",
         "type": "image",
         "file": "assets/lora-low-rank-adaptation.png",
         "alt": "...", "caption": "...",
         "figure_number": "Figure 4.2",            (optional; shown to learners)
         "source_reference": "..."}                (optional; never shown)
      ],
      "pending": [ ... ]                           (figures the curriculum calls for
                                                    that have no image yet; ignored here)
    }

The manifest says what each figure *is*. What the file is - its type, size,
hash, dimensions - is read from the file, so a `.png` that is really something
else, or a file that has gone missing, is a validation problem instead of a
broken image in front of a learner.

Nothing is guessed: a manifest that is missing, unreadable, or not in this
shape yields problems, never a partial import.
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.services.content.lesson_blocks import is_valid_key
from app.services.curriculum.spec import AssetSpec

MANIFEST_NAME = "assets_manifest.json"
MANIFEST_VERSION = 1

# SVG is left out on purpose: an SVG can carry script, and these are served from
# the API's own origin. Raster formats only.
MIME_BY_EXTENSION: Dict[str, str] = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp",
}
_MAGIC = {
    "image/png": (b"\x89PNG\r\n\x1a\n",),
    "image/jpeg": (b"\xff\xd8\xff",),
    "image/gif": (b"GIF87a", b"GIF89a"),
    "image/webp": (b"RIFF",),
}
MAX_ASSET_BYTES = 5 * 1024 * 1024
_WINDOWS_DRIVE = re.compile(r"^[A-Za-z]:")


def safe_relative_path(value: str) -> bool:
    """True for a plain relative path: no absolute path, drive letter, backslash,
    empty segment or `..`."""
    if not value or value.startswith("/") or "\\" in value or _WINDOWS_DRIVE.match(value) or "\0" in value:
        return False
    parts = value.split("/")
    return all(p not in ("", ".", "..") for p in parts)


def image_size(data: bytes) -> Tuple[Optional[int], Optional[int]]:
    """Width and height from the file header, or (None, None) if not readable."""
    try:
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", data[16:24])
        if data[:6] in (b"GIF87a", b"GIF89a"):
            return struct.unpack("<HH", data[6:10])
        if data[:2] == b"\xff\xd8":
            i = 2
            while i + 9 < len(data):
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                if marker in (0xC0, 0xC1, 0xC2):
                    height, width = struct.unpack(">HH", data[i + 5:i + 9])
                    return width, height
                i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            chunk = data[12:16]
            if chunk == b"VP8X":
                return 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little")
            if chunk == b"VP8 ":
                w, h = struct.unpack("<HH", data[26:30])
                return w & 0x3FFF, h & 0x3FFF
    except (struct.error, IndexError):
        pass
    return None, None


def _text(value: Any) -> Optional[str]:
    return value.strip() if isinstance(value, str) and value.strip() else None


def load_assets(course_dir: Path) -> Tuple[List[AssetSpec], List[str]]:
    """`(assets, problems)` for one course folder. A folder without a manifest has
    no assets and no problems (COURSE-001 to 007)."""
    manifest_file = course_dir / MANIFEST_NAME
    if not manifest_file.is_file():
        return [], []
    where = f"{course_dir.name}/{MANIFEST_NAME}"
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [], [f"{where}: cannot read JSON ({exc})"]
    if not isinstance(manifest, dict) or manifest.get("version") != MANIFEST_VERSION \
            or not isinstance(manifest.get("assets"), list):
        return [], [f"{where}: not an asset manifest (expected an object with \"version\": {MANIFEST_VERSION} and an \"assets\" list)"]

    problems: List[str] = []
    assets: List[AssetSpec] = []
    seen: Dict[str, int] = {}
    root = course_dir.resolve()
    for index, entry in enumerate(manifest["assets"], start=1):
        label = f"{where} asset #{index}"
        if not isinstance(entry, dict):
            problems.append(f"{label}: not an object")
            continue
        key = _text(entry.get("key")) or ""
        label = f"{where} asset '{key or index}'"
        if not is_valid_key(key):
            problems.append(f"{label}: key must be lowercase words joined by hyphens (a-z, 0-9, '-')")
            continue
        if key in seen:
            problems.append(f"{label}: duplicate key")
            continue
        seen[key] = index
        if (entry.get("type") or "image") != "image":
            problems.append(f"{label}: type '{entry.get('type')}' is not supported (only 'image')")
            continue
        file = _text(entry.get("file")) or ""
        if not safe_relative_path(file):
            problems.append(f"{label}: file '{file}' must be a plain path inside the course folder")
            continue
        path = (course_dir / file).resolve()
        if root != path and root not in path.parents:
            problems.append(f"{label}: file '{file}' leaves the course folder")
            continue
        mime = MIME_BY_EXTENSION.get(path.suffix.lower())
        if mime is None:
            problems.append(f"{label}: '{path.suffix}' is not an allowed image type ({', '.join(sorted(MIME_BY_EXTENSION))})")
            continue
        if not path.is_file():
            problems.append(f"{label}: file '{file}' does not exist")
            continue
        data = path.read_bytes()
        if not any(data.startswith(m) for m in _MAGIC[mime]):
            problems.append(f"{label}: '{file}' is not really {mime}")
            continue
        if len(data) > MAX_ASSET_BYTES:
            problems.append(f"{label}: '{file}' is {len(data) // 1024} KB (limit {MAX_ASSET_BYTES // 1024} KB)")
            continue
        alt = _text(entry.get("alt"))
        if not alt:
            problems.append(f"{label}: no alt text - every figure needs a description for screen readers")
            continue
        width, height = image_size(data)
        assets.append(AssetSpec(
            key=key, file=file, alt=alt, caption=_text(entry.get("caption")),
            figure_number=_text(entry.get("figure_number")), source_reference=_text(entry.get("source_reference")),
            storage_key=f"{course_dir.name}/{file}", mime_type=mime, byte_size=len(data),
            sha256=hashlib.sha256(data).hexdigest(), width=width, height=height,
        ))
    return assets, problems
