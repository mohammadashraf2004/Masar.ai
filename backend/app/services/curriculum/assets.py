"""
app/services/curriculum/assets.py

Reads a course folder's `assets_manifest.json` into `AssetSpec`s.

    {
      "version": 1,
      "assets": [
        {"key": "lora-low-rank-adaptation",
         "type": "image",
         "file": "assets/M01/lora-low-rank-adaptation.png",
         "lesson": "M01.L01",                      (optional; must be a real lesson of the course)
         "alt_en": "...", "alt_ar": "...",         (`alt` is the same as `alt_en`)
         "caption_en": "...", "caption_ar": "...", (`caption` is the same as `caption_en`)
         "figure_number": "Figure 4.2",            (optional; shown to learners)
         "source_reference": "..."}                (optional; never shown)
      ],
      "pending": [ ... ]                           (figures the curriculum calls for
                                                    that have no image yet; ignored here)
    }

The same entries may also be written as a map keyed by the image key, with or without the
`version` / `assets` wrapper:

    {"transformer-flow": {"file": "assets/M01/transformer-flow.png", "lesson": "M01.L01", "alt_en": "..."}}

One picture serves both languages; only its description and caption are per language.

The manifest says what each figure *is*. What the file is - its type, size,
hash, dimensions - is read from the file, so a `.png` that is really something
else, or a file that has gone missing, is a validation problem instead of a
broken image in front of a learner.

Nothing is guessed: a manifest that is missing, unreadable, or not in this
shape yields problems, never a partial import. Missing alt text, an image stored outside
`assets/`, the same file under two keys, and a file in `assets/` the manifest does not list are
warnings: worth fixing, not a reason to stop.
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.services.content.lesson_blocks import is_valid_key
from app.services.curriculum.spec import AssetSpec

MANIFEST_NAME = "assets_manifest.json"
MANIFEST_VERSION = 1
ASSETS_DIR = "assets"

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
# Top-level manifest keys that are metadata, not an image entry.
_NOT_ENTRIES = {"version", "course_id", "pending", "policy", "$schema", "description"}


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


@dataclass
class AssetLoad:
    """What reading a course's manifest found."""
    assets: List[AssetSpec] = field(default_factory=list)
    problems: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    # Keys the manifest declares whose file is missing or unusable.
    broken_keys: List[str] = field(default_factory=list)


def _text(value: Any) -> Optional[str]:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _first(entry: Dict[str, Any], *names: str) -> Optional[str]:
    for name in names:
        value = _text(entry.get(name))
        if value:
            return value
    return None


def _entries(manifest: Any) -> Tuple[Optional[List[Tuple[str, Any]]], str]:
    """`[(key, entry)]` from either spelling of the manifest, or `(None, reason)` when it is neither."""
    if not isinstance(manifest, dict):
        return None, "expected an object"
    if "assets" in manifest:
        assets = manifest["assets"]
        if isinstance(assets, list):
            if manifest.get("version") != MANIFEST_VERSION:
                return None, f"expected \"version\": {MANIFEST_VERSION}"
            return [((e.get("key") if isinstance(e, dict) else None) or "", e) for e in assets], ""
        if isinstance(assets, dict):
            if manifest.get("version") not in (None, MANIFEST_VERSION):
                return None, f"expected \"version\": {MANIFEST_VERSION}"
            return list(assets.items()), ""
        return None, "\"assets\" must be a list or an object keyed by image key"
    if "version" in manifest:
        return None, "no \"assets\""
    values = {k: v for k, v in manifest.items() if k not in _NOT_ENTRIES}
    if all(isinstance(v, dict) for v in values.values()):
        return list(values.items()), ""
    return None, "expected an \"assets\" list or an object keyed by image key"


def load_asset_manifest(course_dir: Path, store_root: Optional[Path] = None) -> AssetLoad:
    """Read, check and describe the course's images.

    `store_root` is the folder every `storage_key` is relative to (the courses root). It is not
    always `course_dir.parent`: a course folder wrapped in a redundant subfolder (COURSE-015)
    passes the wrapper's parent."""
    result = AssetLoad()
    manifest_file = course_dir / MANIFEST_NAME
    if not manifest_file.is_file():
        return result
    where = f"{course_dir.name}/{MANIFEST_NAME}"
    duplicates: List[str] = []

    def collect(pairs):
        out: Dict[str, Any] = {}
        for k, v in pairs:
            if k in out:
                duplicates.append(k)
            out[k] = v
        return out

    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"), object_pairs_hook=collect)
    except (OSError, ValueError) as exc:
        result.problems.append(f"{where}: cannot read JSON ({exc})")
        return result
    # Some historical exports use this filename for a planning inventory of
    # source-book figures that are explicitly *not* bundled. It is metadata,
    # not a malformed learner-facing asset manifest.
    if isinstance(manifest, dict) and isinstance(manifest.get("manual_figures"), list) \
            and "assets" not in manifest:
        return result
    entries, reason = _entries(manifest)
    if entries is None:
        result.problems.append(
            f"{where}: not an asset manifest ({reason}; expected an object with \"version\": {MANIFEST_VERSION} "
            f"and an \"assets\" list)")
        return result

    problems, warnings, assets = result.problems, result.warnings, result.assets
    # A key written twice in a map is lost by the JSON parser (the last one wins), so it is caught here.
    for key in dict.fromkeys(d for d in duplicates if is_valid_key(d)):
        problems.append(f"{where} asset '{key}': duplicate key")

    seen: Dict[str, int] = {}
    files_by_path: Dict[Path, str] = {}
    declared: set = set()
    root = course_dir.resolve()
    store = (store_root or course_dir.parent).resolve()
    assets_root = (course_dir / ASSETS_DIR).resolve()
    for index, (raw_key, entry) in enumerate(entries, start=1):
        label = f"{where} asset #{index}"
        if not isinstance(entry, dict):
            problems.append(f"{label}: not an object")
            continue
        key = _text(raw_key) or ""
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
        declared.add(path)
        mime = MIME_BY_EXTENSION.get(path.suffix.lower())
        if mime is None:
            problems.append(f"{label}: '{path.suffix}' is not an allowed image type ({', '.join(sorted(MIME_BY_EXTENSION))})")
            continue
        if not path.is_file():
            problems.append(f"{label}: file '{file}' does not exist")
            result.broken_keys.append(key)
            continue
        data = path.read_bytes()
        if not any(data.startswith(m) for m in _MAGIC[mime]):
            problems.append(f"{label}: '{file}' is not really {mime}")
            result.broken_keys.append(key)
            continue
        if len(data) > MAX_ASSET_BYTES:
            problems.append(f"{label}: '{file}' is {len(data) // 1024} KB (limit {MAX_ASSET_BYTES // 1024} KB)")
            result.broken_keys.append(key)
            continue
        alt, alt_ar = _first(entry, "alt_en", "alt"), _first(entry, "alt_ar")
        if not (alt or alt_ar):
            warnings.append(f"{label}: no alt text - every image needs a description for screen readers")
        if assets_root != path and assets_root not in path.parents:
            warnings.append(f"{label}: '{file}' is not under {ASSETS_DIR}/ - move it there")
        if path in files_by_path:
            warnings.append(f"{label}: uses the same file as '{files_by_path[path]}' ({file}) - two keys for one picture")
        else:
            files_by_path[path] = key
        try:
            storage_key = path.relative_to(store).as_posix()
        except ValueError:
            storage_key = f"{course_dir.name}/{file}"
        width, height = image_size(data)
        assets.append(AssetSpec(
            key=key, file=file, alt=alt or "", caption=_first(entry, "caption_en", "caption"),
            figure_number=_text(entry.get("figure_number")), source_reference=_text(entry.get("source_reference")),
            storage_key=storage_key, mime_type=mime, byte_size=len(data),
            sha256=hashlib.sha256(data).hexdigest(), width=width, height=height,
            alt_ar=alt_ar, caption_ar=_first(entry, "caption_ar"), lesson=_text(entry.get("lesson")),
        ))

    # A picture dropped into assets/ and never listed would silently never appear.
    if assets_root.is_dir():
        for found in sorted(p for p in assets_root.rglob("*") if p.is_file() and p.suffix.lower() in MIME_BY_EXTENSION):
            if found.resolve() not in declared:
                warnings.append(f"{where}: {found.relative_to(course_dir).as_posix()} is in {ASSETS_DIR}/ "
                                "but not in the manifest, so no lesson can place it")
    return result


def load_assets(course_dir: Path, store_root: Optional[Path] = None) -> Tuple[List[AssetSpec], List[str]]:
    """`(assets, problems)` for one course folder. A folder without a manifest has
    no assets and no problems (COURSE-001 to 007)."""
    loaded = load_asset_manifest(course_dir, store_root)
    return loaded.assets, loaded.problems
