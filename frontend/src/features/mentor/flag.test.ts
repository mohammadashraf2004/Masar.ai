import { afterEach, describe, expect, it, vi } from 'vitest'
import { mentorV2Enabled, mentorV2Live } from '@/features/mentor/flag'

/**
 * Which mentor screen a production build renders. The first mentor chat's endpoint (POST /mentor/chat)
 * is retired and answers 410, so the only working mentor is the v2 hub, which a build gets from
 * NEXT_PUBLIC_MENTOR_V2_LIVE. docker-compose.yml therefore defaults that build argument to
 * "message,quiz" (pinned by backend/tests/test_deploy_mentor_default.py).
 */
function productionBuild(live: string | undefined, v2 = '') {
  vi.stubEnv('NODE_ENV', 'production')
  vi.stubEnv('NEXT_PUBLIC_MENTOR_V2', v2)
  vi.stubEnv('NEXT_PUBLIC_MENTOR_V2_LIVE', live as string)
}

afterEach(() => vi.unstubAllEnvs())

describe('the mentor a production build renders', () => {
  it('is the v2 hub, talking to the real server, with the default live endpoints', () => {
    productionBuild('message,quiz')
    expect(mentorV2Enabled()).toBe(true)
    expect(mentorV2Live()).toBe(true)
  })

  it('is the v2 hub when only one of the two endpoints is live', () => {
    productionBuild(' Quiz ')
    expect(mentorV2Enabled()).toBe(true)
    expect(mentorV2Live()).toBe(true)
  })

  it('falls back to the retired chat screen only when nothing is live: the build the compose default prevents', () => {
    productionBuild('')
    expect(mentorV2Enabled()).toBe(false)
    productionBuild(undefined)
    expect(mentorV2Enabled()).toBe(false)
  })

  it('ignores an unknown value, so a typo cannot turn on live traffic', () => {
    productionBuild('mesage')
    expect(mentorV2Live()).toBe(false)
    expect(mentorV2Enabled()).toBe(false)
  })
})
