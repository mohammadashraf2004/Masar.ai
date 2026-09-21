"""
app/core/releases.py

Which product announcements exist, and which of them an account still has to
see. The server decides both: a client never chooses what counts as an update,
it can only say "I have seen this one".

An announcement is a stable identifier, never a date or a counter, so it can be
acknowledged once and stay acknowledged. The next release adds its own
identifier here; nothing about an old one changes.

The skill-gap release has two presentations of one idea:

  * ``WHATS_NEW`` - for an account that existed before the release. It learns
    what changed the next time it signs in.
  * ``FIRST_ROADMAP_INTRO`` - for an account created after it. Nothing has
    "changed" for that learner, so they are introduced to the feature in their
    first roadmap instead. Registration records ``WHATS_NEW`` as already seen,
    which is what makes an account new for this purpose - no date is compared.

An account is only ever asked about one of them: seeing ``WHATS_NEW`` covers the
introduction (it has been introduced), and the introduction only becomes due
once ``WHATS_NEW`` is out of the way.
"""
from typing import Dict, FrozenSet, Iterable, List, Tuple

WHATS_NEW = "2026-09-skill-gap"
FIRST_ROADMAP_INTRO = "2026-09-skill-gap-intro"

# Everything a client may acknowledge. Anything else is refused, so an account
# cannot pre-dismiss an announcement that has not shipped.
KNOWN_RELEASES: FrozenSet[str] = frozenset({WHATS_NEW, FIRST_ROADMAP_INTRO})

# Acknowledging the key also acknowledges the values: one introduction per
# release, however the learner met it.
COVERS: Dict[str, Tuple[str, ...]] = {
    WHATS_NEW: (FIRST_ROADMAP_INTRO,),
}


def with_covered(release_id: str) -> List[str]:
    """`release_id` and everything acknowledging it covers."""
    return [release_id, *COVERS.get(release_id, ())]


def pending_updates(acknowledged: Iterable[str]) -> List[str]:
    """The announcements the account still has to see, in the order to show them.

    At most one at a time: the introduction is only due after ``WHATS_NEW`` has
    been dealt with, which for an existing account also closes it.
    """
    done = set(acknowledged)
    if WHATS_NEW not in done:
        return [WHATS_NEW]
    if FIRST_ROADMAP_INTRO not in done:
        return [FIRST_ROADMAP_INTRO]
    return []
