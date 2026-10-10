"""Every course's example answers (``c001.py`` ...), merged into one registry."""
from __future__ import annotations

import importlib
import os
import pkgutil
import re
from typing import Dict

from . import Example

_PACKAGE = __name__.rsplit(".", 1)[0]


def _collect() -> Dict[str, Example]:
    merged: Dict[str, Example] = {}
    names = sorted(info.name for info in pkgutil.iter_modules([os.path.dirname(__file__)]))
    for name in names:
        # c001.py, or a course split into parts: c009_a.py, c009_b.py ...
        if not re.fullmatch(r"c\d{3}(_[a-z])?", name):
            continue
        examples: Dict[str, Example] = importlib.import_module(f"{_PACKAGE}.{name}").EXAMPLES
        duplicates = sorted(set(examples) & set(merged))
        if duplicates:
            raise ValueError(f"example answers defined twice: {duplicates}")
        merged.update(examples)
    return merged


ALL: Dict[str, Example] = _collect()
