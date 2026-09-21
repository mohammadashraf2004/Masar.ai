import { describe, expect, it } from 'vitest'
import { STRINGS } from '@/lib/i18n'
import { mentorErrorKey } from '@/lib/mentorErrors'

// The shape axios gives a failed request: `response.status` and `response.data`.
const failed = (status: number, detail?: unknown) => ({ response: { status, data: { detail } } })

describe('mentorErrorKey — what the learner is told, by what actually failed', () => {
  it.each([
    ['an empty wallet (402 with the structured payload)', failed(402, { error: 'insufficient_credits', message: 'x' }), 'mentor.error.credits'],
    ['an empty wallet, whatever the status', failed(400, { error: 'insufficient_credits' }), 'mentor.error.credits'],
    ['an unverified email', failed(403, { error: 'email_verification_required', message: 'x' }), 'mentor.error.verify'],
    ['a rate limit', failed(429, 'Too many requests'), 'mentor.error.rateLimit'],
    ['input over the length limit', failed(422, [{ loc: ['body', 'content'], msg: 'too long' }]), 'mentor.error.invalid'],
    ['the provider failing (503, credits refunded)', failed(503, 'The mentor is unavailable right now. Your credits were refunded.'), 'mentor.error.unavailable'],
    ['an unhandled server error', failed(500, 'Internal server error'), 'mentor.error.unavailable'],
    ['a gateway timeout', failed(504), 'mentor.error.unavailable'],
  ])('%s', (_name, error, key) => {
    expect(mentorErrorKey(error)).toBe(key)
  })

  it('a request that never got a response is a connection problem', () => {
    // Offline, DNS, CORS, or axios giving up after its 30 s timeout.
    expect(mentorErrorKey({ code: 'ECONNABORTED', message: 'timeout of 30000ms exceeded' })).toBe('mentor.error.network')
    expect(mentorErrorKey(new Error('Network Error'))).toBe('mentor.error.network')
    expect(mentorErrorKey(null)).toBe('mentor.error.network')
    expect(mentorErrorKey(undefined)).toBe('mentor.error.network')
  })

  it('a 403 that is not the email gate is not reported as one', () => {
    expect(mentorErrorKey(failed(403, { error: 'forbidden' }))).toBe('mentor.error.unavailable')
    expect(mentorErrorKey(failed(403, 'Forbidden'))).toBe('mentor.error.unavailable')
  })

  it('never depends on server text', () => {
    // The same status gives the same key whatever the server wrote, so a
    // provider error message can never end up on screen through this path.
    expect(mentorErrorKey(failed(503, 'sk-secret leaked here'))).toBe(mentorErrorKey(failed(503, 'ok')))
  })

  it('every key it can return exists in both languages, and reads differently in each', () => {
    const keys = [
      'mentor.error.unavailable', 'mentor.error.credits', 'mentor.error.verify',
      'mentor.error.rateLimit', 'mentor.error.network', 'mentor.error.invalid',
    ] as const
    for (const key of keys) {
      expect(STRINGS.en[key], `en ${key}`).toBeTruthy()
      expect(STRINGS.ar[key], `ar ${key}`).toBeTruthy()
      expect(STRINGS.ar[key]).not.toBe(STRINGS.en[key])
      expect(STRINGS.ar[key]).toMatch(/[؀-ۿ]/)
    }
  })
})
