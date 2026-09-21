"""
app/services/learning/prerequisites.py

Prerequisite logic, in one place and free of any database access.

Two different things are called "prerequisite" in the learning model, and
both live here so the rules are never re-implemented at a call site:

  * **Course prerequisites** — a directed graph. A course may need others
    first. The graph must be acyclic; `find_cycle` proves it and
    `topological_order` uses it.
  * **Field prerequisites** — a *threshold*, not a chain. "At least `k` of
    these fields" (Multimodal: any one of NLP / Vision / Speech, ideally two).
    `evaluate_threshold` answers it.

Everything takes plain values (ids, slugs, dicts) so it can be tested — and
reasoned about — without a session.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Hashable, Iterable, List, Mapping, Optional, Sequence, Set, TypeVar

K = TypeVar("K", bound=Hashable)


class PrerequisiteCycleError(ValueError):
    """The prerequisite graph contains a cycle, so no valid order exists."""

    def __init__(self, cycle: Sequence[Hashable]):
        self.cycle = list(cycle)
        super().__init__("prerequisite cycle: " + " -> ".join(str(node) for node in self.cycle))


def find_cycle(edges: Mapping[K, Iterable[K]]) -> Optional[List[K]]:
    """Return one cycle as a closed path (`[a, b, c, a]`), or None.

    `edges[node]` is the set of things `node` depends on. Iterative depth-first
    search with three colours, so a deep chain cannot hit the recursion limit
    and a node reachable by two routes is not mistaken for a cycle.
    """
    WHITE, GREY, BLACK = 0, 1, 2
    colour: Dict[K, int] = {}
    nodes = list(edges)
    # Targets that only appear on the right-hand side are leaves.
    for targets in list(edges.values()):
        for target in targets:
            if target not in edges:
                nodes.append(target)

    for root in nodes:
        if colour.get(root, WHITE) != WHITE:
            continue
        stack: List[tuple] = [(root, iter(edges.get(root, ())))]
        path: List[K] = [root]
        colour[root] = GREY
        while stack:
            node, children = stack[-1]
            advanced = False
            for child in children:
                state = colour.get(child, WHITE)
                if state == GREY:
                    return path[path.index(child):] + [child]
                if state == WHITE:
                    colour[child] = GREY
                    path.append(child)
                    stack.append((child, iter(edges.get(child, ()))))
                    advanced = True
                    break
            if not advanced:
                colour[node] = BLACK
                stack.pop()
                path.pop()
    return None


def topological_order(nodes: Sequence[K], edges: Mapping[K, Iterable[K]]) -> List[K]:
    """`nodes` reordered so every node follows the nodes it depends on.

    Stable: among nodes that are ready at the same moment the caller's order
    wins, so a curated sequence is disturbed only where a prerequisite forces
    it. Only edges between members of `nodes` count — a prerequisite outside
    the set is somebody else's concern (the generator decides whether to pull
    it in). Raises `PrerequisiteCycleError` rather than returning a partial
    order.
    """
    members = set(nodes)
    remaining = list(nodes)
    placed: Set[K] = set()
    ordered: List[K] = []

    while remaining:
        for node in remaining:
            needs = {dep for dep in edges.get(node, ()) if dep in members and dep != node}
            if needs <= placed:
                ordered.append(node)
                placed.add(node)
                remaining.remove(node)
                break
        else:
            cycle = find_cycle({n: [d for d in edges.get(n, ()) if d in members] for n in remaining})
            raise PrerequisiteCycleError(cycle or remaining)
    return ordered


def transitive_prerequisites(start: K, edges: Mapping[K, Iterable[K]]) -> List[K]:
    """Everything `start` depends on, nearest first, without repeats.

    Safe on a cyclic graph: a node is visited once, so it terminates.
    """
    seen: Set[K] = {start}
    ordered: List[K] = []
    frontier: List[K] = [start]
    while frontier:
        next_frontier: List[K] = []
        for node in frontier:
            for dep in edges.get(node, ()):
                if dep not in seen:
                    seen.add(dep)
                    ordered.append(dep)
                    next_frontier.append(dep)
        frontier = next_frontier
    return ordered


@dataclass(frozen=True)
class ThresholdResult:
    """Outcome of an "at least k of these" rule."""

    satisfied: List[str]          # prerequisites the learner already has
    missing: List[str]            # prerequisites they do not
    met: bool                     # satisfied >= min_required
    recommended_met: bool         # satisfied >= recommended
    shortfall: int                # how many more are needed to be `met`


def evaluate_threshold(
    prerequisites: Sequence[str],
    have: Iterable[str],
    *,
    min_required: int,
    recommended: int,
) -> ThresholdResult:
    """Apply a field's prerequisite rule to what a learner has.

    `min_required` is capped at the number of prerequisites that exist: a rule
    saying "2 of these" over a single listed field would otherwise be
    unsatisfiable, and an unsatisfiable rule is a data error the learner
    should not pay for.
    """
    owned = set(have)
    listed = list(dict.fromkeys(prerequisites))
    satisfied = [p for p in listed if p in owned]
    missing = [p for p in listed if p not in owned]
    need = min(max(min_required, 0), len(listed))
    want = min(max(recommended, need), len(listed))
    return ThresholdResult(
        satisfied=satisfied,
        missing=missing,
        met=len(satisfied) >= need,
        recommended_met=len(satisfied) >= want,
        shortfall=max(0, need - len(satisfied)),
    )
