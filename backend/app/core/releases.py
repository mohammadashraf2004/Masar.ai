"""
app/core/releases.py

Registry for active product announcements. Retired announcements stay in the
database as harmless audit rows, but are removed from this registry so they can
never block a later announcement or reappear in the UI.
"""
from typing import Dict, FrozenSet, Iterable, List, Tuple

# Everything a client may acknowledge. Anything else is refused, so an account
# cannot pre-dismiss an announcement that has not shipped.
KNOWN_RELEASES: FrozenSet[str] = frozenset()

# Acknowledging the key also acknowledges the values: one introduction per
# release, however the learner met it.
COVERS: Dict[str, Tuple[str, ...]] = {}


def with_covered(release_id: str) -> List[str]:
    """`release_id` and everything acknowledging it covers."""
    return [release_id, *COVERS.get(release_id, ())]


def pending_updates(acknowledged: Iterable[str]) -> List[str]:
    """The announcements the account still has to see, in the order to show them.

    At most one at a time. There are currently no active announcements.
    """
    del acknowledged
    return []
