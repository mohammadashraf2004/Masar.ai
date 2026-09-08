/**
 * Which career tracks are open for enrolment.
 *
 * Only the AI Developer track has published content; the others are seeded as
 * shells (levels with no topics), so listing them as enrollable promises
 * lessons that are not there. Add a slug here as its content lands.
 *
 * This is presentation only — the enrol endpoint still accepts any track id,
 * so treat it as a product decision, not an access control.
 */
export const AVAILABLE_TRACK_SLUGS = new Set(['ai-developer'])

export function isTrackComingSoon(slug: string): boolean {
  return !AVAILABLE_TRACK_SLUGS.has(slug)
}
