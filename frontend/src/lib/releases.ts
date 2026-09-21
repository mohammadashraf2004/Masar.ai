/**
 * The announcements this build knows how to draw. The identifiers are the
 * server's (backend `app/core/releases.py`) and stay exactly as written: an
 * acknowledgement is stored against them, so changing one would show the
 * announcement to everyone again.
 *
 * Whether an account is asked about one is the server's answer
 * (`user.pending_updates`); nothing here compares dates or versions.
 */

/** For an account that existed before the skill-gap release: what changed. */
export const WHATS_NEW = '2026-09-skill-gap'

/** For an account created after it: the feature, met in the first roadmap. */
export const FIRST_ROADMAP_INTRO = '2026-09-skill-gap-intro'
