"""Discover the 84 individual lesson definitions and assemble 20 levels."""
from importlib import import_module
from pathlib import Path


def load_levels():
    folders = sorted(p for p in Path(__file__).parent.glob("module_*") if p.is_dir())
    levels = []
    seen_slugs = set()
    for folder in folders:
        items = []
        names = sorted(p.stem for p in folder.glob("lesson_*.py"))
        for name in names:
            module = import_module(f"{__name__}.{folder.name}.{name}")
            topic = module.TOPIC
            if topic["slug"] in seen_slugs:
                raise ValueError(f"Duplicate topic slug: {topic['slug']}")
            seen_slugs.add(topic["slug"])
            if len(topic["quiz"]["questions"]) < 2 or not topic["lesson"]["content"]:
                raise ValueError(f"Incomplete lesson: {topic['slug']}")
            items.append(topic)
        if not items:
            continue
        orders = [t["order"] for t in items]
        if orders != list(range(1, len(orders) + 1)):
            raise ValueError(f"Invalid lesson ordering in {folder.name}: {orders}")
        first = import_module(f"{__name__}.{folder.name}.{names[0]}")
        levels.append({"title":f"Module {first.MODULE_ORDER:02d}: {first.MODULE_TITLE}",
                       "description":first.MODULE_DESCRIPTION,
                       "order":first.MODULE_ORDER,
                       "topics":items})
    if len(levels) != 20 or sum(len(x["topics"]) for x in levels) != 84:
        raise ValueError("Expected 20 modules and 84 lessons; inspect missing or extra files")
    return levels
