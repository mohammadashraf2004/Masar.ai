"""Every guided exercise definition, one module per course (``cNNN.py``)."""
from __future__ import annotations

import importlib
import pkgutil
from typing import Dict

from . import Guided


def _collect() -> Dict[str, Guided]:
    collected: Dict[str, Guided] = {}
    package = importlib.import_module(__package__)
    for info in sorted(pkgutil.iter_modules(package.__path__), key=lambda item: item.name):
        if not (info.name.startswith("c") and info.name[1:].isdigit()):
            continue
        module = importlib.import_module(f"{__package__}.{info.name}")
        for exercise_id, definition in module.EXERCISES.items():
            if exercise_id in collected:
                raise ValueError(f"guided exercise {exercise_id} is defined twice")
            collected[exercise_id] = definition
    return collected


ALL: Dict[str, Guided] = _collect()
