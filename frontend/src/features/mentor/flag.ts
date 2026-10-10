/**
 * Whether the Mentor v2 hub (context bar, hint ladder, weekly plan, in-lesson mentor)
 * replaces the current mentor. It is on in `next dev`, and in a build only with
 * NEXT_PUBLIC_MENTOR_V2=1. Endpoint rollout is intentionally separate below: message and quiz may
 * be live while other endpoints are still fixtures.
 */
export function mentorV2Enabled(): boolean {
  if (process.env.NODE_ENV === 'test') return false
  return process.env.NODE_ENV === 'development'
    || process.env.NEXT_PUBLIC_MENTOR_V2 === '1'
    || mentorV2EndpointLive('message')
    || mentorV2EndpointLive('quiz')
}

export type MentorV2LiveEndpoint = 'message' | 'quiz'

/** Endpoints graduate independently. Unknown values are ignored, so a typo cannot accidentally
 * turn the entire mock surface into live traffic. */
export function mentorV2EndpointLive(endpoint: MentorV2LiveEndpoint): boolean {
  return (process.env.NEXT_PUBLIC_MENTOR_V2_LIVE ?? '')
    .split(',')
    .map((value) => value.trim().toLowerCase())
    .filter(Boolean)
    .includes(endpoint)
}

/**
 * Whether the hub talks to the real server. Then no fixture may ever reach a learner: the learner
 * model, the weekly plan and hints come from their real endpoints, and the surfaces that have no
 * real endpoint yet (the proactive suggestion card, the v2 interview report) are not shown at all.
 * Fixtures are only for a build with no live endpoint (design work in `next dev`).
 */
export function mentorV2Live(): boolean {
  return mentorV2EndpointLive('message') || mentorV2EndpointLive('quiz')
}

export function mentorV2MocksAllowed(): boolean {
  return !mentorV2Live()
}

/**
 * Whether learners can run a mock interview. Until it is ready the interview tab, its setup and
 * report pages show "coming soon" instead, and its walkthrough does not run. A build turns it on
 * with NEXT_PUBLIC_MOCK_INTERVIEW=1.
 */
export function mockInterviewAvailable(): boolean {
  return process.env.NEXT_PUBLIC_MOCK_INTERVIEW === '1'
}
