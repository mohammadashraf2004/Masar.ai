"""Pre-launch learners keep the courses they were already taking.

Before the plan model every course was open to everyone. Migration 018 turns that
activity into course enrollments and 021 grandfathers them (`legacy_free`), but
both run inside `alembic upgrade head` - and on a database that predates
migration 011 the `courses` catalogue is still empty at that point (the seeds
fill it afterwards), so neither finds anything to convert. Without this step
those learners would find their courses locked.

`backfill_legacy_enrollments` runs once the catalogue is seeded
(`seeds/backfill_legacy_enrollments.py`). For every account created before
`legacy_before`, each course it was already working in before that moment - a
tool-course enrollment, progress in the course's tool topics, or progress in a
track level's topics (018's three mappings) - ends with an active `legacy_free`
enrollment, recorded in `course_enrollment_legacy_free` exactly as 021 records
its own, so 021's downgrade turns it back into `free`.

* Additive: a course held by purchase, admin grant or `legacy_free` is left as it
  is, an inactive enrollment stays inactive, nothing is deleted, and no wallet,
  progress row or legacy row is touched.
* Idempotent: a second run finds nothing to do.
* Bounded by `legacy_before`: activity or accounts from that moment on never
  count, so running it again after launch cannot grandfather anyone new.
"""
from datetime import datetime, timezone
from typing import Dict

from sqlalchemy import text
from sqlalchemy.orm import Session

# (user, course) pairs with pre-launch activity, one row per pair, with what 018
# would have recorded for it. Tool enrollments win over progress-only pairs.
_LEGACY_PAIRS = """
    SELECT DISTINCT ON (user_id, course_id)
           user_id, course_id, enrolled_at, learning_status, started_at, completed_at
      FROM (
        SELECT te.user_id, c.id AS course_id, 1 AS rank,
               COALESCE(te.enrolled_at, u.created_at) AS enrolled_at,
               CASE WHEN te.completed_at IS NOT NULL THEN 'completed'
                    WHEN COALESCE(te.progress_pct, 0) > 0 THEN 'in_progress'
                    ELSE 'enrolled' END AS learning_status,
               (SELECT MIN(up.started_at) FROM user_progress up
                  JOIN tool_topics tt ON tt.id = up.tool_topic_id
                 WHERE up.user_id = te.user_id AND tt.tool_course_id = te.tool_course_id
                   AND up.started_at < :cutoff) AS started_at,
               te.completed_at
          FROM tool_enrollments te
          JOIN users u ON u.id = te.user_id
          JOIN courses c ON c.tool_course_id = te.tool_course_id
         WHERE (u.created_at IS NULL OR u.created_at < :cutoff)
           AND COALESCE(te.enrolled_at, u.created_at, :cutoff - interval '1 second') < :cutoff
        UNION ALL
        SELECT up.user_id, c.id, 2, MIN(COALESCE(up.started_at, up.completed_at)), 'in_progress',
               MIN(up.started_at), NULL
          FROM user_progress up
          JOIN users u ON u.id = up.user_id
          JOIN tool_topics tt ON tt.id = up.tool_topic_id
          JOIN courses c ON c.tool_course_id = tt.tool_course_id
         WHERE (u.created_at IS NULL OR u.created_at < :cutoff)
           AND COALESCE(up.started_at, up.completed_at) < :cutoff
         GROUP BY up.user_id, c.id
        UNION ALL
        SELECT up.user_id, c.id, 3, MIN(COALESCE(up.started_at, up.completed_at)), 'in_progress',
               MIN(up.started_at), NULL
          FROM user_progress up
          JOIN users u ON u.id = up.user_id
          JOIN topics t ON t.id = up.topic_id
          JOIN courses c ON c.track_level_id = t.level_id
         WHERE (u.created_at IS NULL OR u.created_at < :cutoff)
           AND COALESCE(up.started_at, up.completed_at) < :cutoff
         GROUP BY up.user_id, c.id
      ) AS activity
     ORDER BY user_id, course_id, rank
"""


def backfill_legacy_enrollments(db: Session, legacy_before: datetime) -> Dict[str, int]:
    """Give every pre-launch learner an active `legacy_free` enrollment in each course
    they were already working in. Writes in the caller's transaction, does not commit.
    Returns counts: `pairs` found, enrollments `created`, `grandfathered` (now
    legacy_free), `already_entitled` (purchase / admin grant / legacy_free before this
    run) and `left_inactive` (an existing enrollment that is not active)."""
    if legacy_before.tzinfo is None:
        raise ValueError("legacy_before must carry a timezone")
    if legacy_before > datetime.now(timezone.utc):
        raise ValueError("legacy_before is in the future; use the moment the release window began")
    params = {"cutoff": legacy_before}

    before = dict(db.execute(text(f"""
        SELECT ce.source || ':' || ce.status AS kind, count(*)
          FROM ({_LEGACY_PAIRS}) l
          JOIN course_enrollments ce ON ce.user_id = l.user_id AND ce.course_id = l.course_id
         GROUP BY 1"""), params).all())
    pairs = db.execute(text(f"SELECT count(*) FROM ({_LEGACY_PAIRS}) l"), params).scalar()

    created = db.execute(text(f"""
        INSERT INTO course_enrollments
            (user_id, course_id, source, status, enrolled_at, learning_status, started_at, completed_at)
        SELECT user_id, course_id, 'free', 'active', COALESCE(enrolled_at, now()), learning_status,
               started_at, completed_at
          FROM ({_LEGACY_PAIRS}) l
        ON CONFLICT (user_id, course_id) DO NOTHING
        RETURNING id"""), params).fetchall()

    grandfathered = db.execute(text(f"""
        WITH granted AS (
            UPDATE course_enrollments ce SET source = 'legacy_free'
              FROM ({_LEGACY_PAIRS}) l
             WHERE ce.user_id = l.user_id AND ce.course_id = l.course_id
               AND ce.source = 'free' AND ce.status = 'active'
            RETURNING ce.id, ce.user_id, ce.course_id
        )
        INSERT INTO course_enrollment_legacy_free (enrollment_id, user_id, course_id, previous_source)
        SELECT id, user_id, course_id, 'free' FROM granted
        ON CONFLICT (enrollment_id) DO NOTHING
        RETURNING enrollment_id"""), params).fetchall()
    db.flush()

    entitled = sum(n for kind, n in before.items()
                   if kind.split(":")[0] in ("purchase", "admin_grant", "legacy_free") and kind.endswith(":active"))
    inactive = sum(n for kind, n in before.items() if not kind.endswith(":active"))
    return {"pairs": pairs, "created": len(created), "grandfathered": len(grandfathered),
            "already_entitled": entitled, "left_inactive": inactive}
