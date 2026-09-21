"""
app/core/legal.py

The single place that says which version of the Terms of Service and the
Privacy Policy is in force.

The server decides the versions. A client never sends one: registration and
re-acceptance take only "yes, I agree", and the server records the versions it
is currently publishing. That keeps a stale browser tab, or a hand-built
request, from recording acceptance of a document that no longer exists.

When a document changes materially, bump its constant here *and* update its
text in `app/content/legal_documents.py` (they live side by side so the two
cannot drift). Every account whose stored version differs from the current one
then reports `requires_legal_acceptance` and is asked to accept again; nobody
is silently marked as having accepted a version they never saw.
"""
from datetime import datetime
from typing import Optional

TERMS_VERSION = "2026-09-01"
PRIVACY_VERSION = "2026-09-01"


def acceptance_is_current(
    terms_version: Optional[str],
    terms_accepted_at: Optional[datetime],
    privacy_version: Optional[str],
    privacy_accepted_at: Optional[datetime],
) -> bool:
    """True only when the account has accepted the versions in force now.

    A missing timestamp counts as not accepted even if a version string is
    present: the pair is the record, and half of one is not a record.
    """
    return (
        terms_accepted_at is not None
        and terms_version == TERMS_VERSION
        and privacy_accepted_at is not None
        and privacy_version == PRIVACY_VERSION
    )
