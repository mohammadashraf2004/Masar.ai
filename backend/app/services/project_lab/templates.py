"""Canonical project templates on disk (backend/project_templates/<key>/workspace).

The template is the single source for starter files and the ONLY copy of the
read-only datasets: an attempt stores just the learner's editable files, and
everything else is served from here. The runner service mounts the same
folder read-only, so templates must never contain answers or validator logic.
"""
from __future__ import annotations

import csv
import io
import os
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from project_runner.executor import InvalidJob, safe_relative_path

TEMPLATES_ROOT = Path(__file__).resolve().parents[3] / "project_templates"
EDITABLE_EXTENSIONS = frozenset({".py", ".sql", ".md"})
LANGUAGES = {".py": "python", ".sql": "sql", ".md": "markdown", ".csv": "csv"}
_KEY = re.compile(r"^[a-z0-9][a-z0-9\-]{0,79}$")
CSV_PREVIEW_ROWS = 100


class WorkspacePathError(ValueError):
    """The requested path is not a canonical workspace-relative path."""


def canonical_path(raw: str) -> str:
    """Canonicalise a learner-supplied workspace path or raise
    WorkspacePathError. Rejects `..`, absolute paths, backslashes, hidden
    segments and anything else safe_relative_path does not accept. Callers
    must then also check the path is a file this workspace actually has."""
    try:
        return safe_relative_path(raw)
    except InvalidJob as exc:
        raise WorkspacePathError(str(exc)) from exc


def language_for(path: str) -> str:
    return LANGUAGES.get(os.path.splitext(path)[1].lower(), "text")


def is_read_only(path: str, read_only_paths: list[str]) -> bool:
    """A file is editable only if it has an editable extension and no
    read-only rule of the project covers it."""
    if os.path.splitext(path)[1].lower() not in EDITABLE_EXTENSIONS:
        return True
    for rule in read_only_paths or []:
        if rule.endswith("/") and path.startswith(rule):
            return True
        if path == rule:
            return True
    return False


@dataclass(frozen=True)
class TemplateFile:
    path: str
    size: int
    language: str


@dataclass
class ProjectTemplate:
    key: str
    root: Path
    files: dict[str, TemplateFile] = field(default_factory=dict)
    dirs: list[str] = field(default_factory=list)

    def read_text(self, path: str) -> str:
        if path not in self.files:
            raise KeyError(path)
        return (self.root / path).read_text(encoding="utf-8")

    def data_files(self) -> list[str]:
        return [p for p in self.files if p.startswith("data/")]

    def read_csv(self, path: str) -> list[dict[str, str]]:
        return list(csv.DictReader(io.StringIO(self.read_text(path))))

    def csv_preview(self, path: str, limit: int = CSV_PREVIEW_ROWS) -> dict:
        reader = csv.reader(io.StringIO(self.read_text(path)))
        columns = next(reader, [])
        rows, total = [], 0
        for row in reader:
            total += 1
            if len(rows) < limit:
                rows.append(row)
        return {"columns": columns, "rows": rows, "row_count": total, "truncated": total > limit}


@lru_cache(maxsize=32)
def load_template(key: str) -> ProjectTemplate:
    if not _KEY.match(key or ""):
        raise ValueError(f"invalid template key: {key!r}")
    root = (TEMPLATES_ROOT / key / "workspace").resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"project template not found: {key}")
    template = ProjectTemplate(key=key, root=root)
    for current, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith((".", "__")))
        rel_dir = Path(current).relative_to(root).as_posix()
        if rel_dir != ".":
            template.dirs.append(rel_dir)
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            rel = name if rel_dir == "." else f"{rel_dir}/{name}"
            full = Path(current) / name
            if full.is_symlink():
                continue
            template.files[rel] = TemplateFile(rel, full.stat().st_size, language_for(rel))
    return template
