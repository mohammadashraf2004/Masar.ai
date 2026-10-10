import { afterEach, describe, expect, it } from 'vitest'
import { isProAiLimit, proAiLimitMessage } from '@/lib/aiErrors'
import { useLanguageStore } from '@/lib/language'
import { getErrorMessage } from '@/lib/utils'

const limit = { response: { status: 429, data: { detail: {
  error: 'pro_ai_limit_reached', message: 'server English text', remaining: 0, next_credit_available_at: '2026-10-08T14:00:00Z',
} } } }
const rateLimited = { response: { status: 429, data: { detail: 'Too many requests' } } }

afterEach(() => useLanguageStore.setState({ language: 'en' }))

describe('the Pro allowance error, wherever an AI request fails', () => {
  it('is recognised only by its code, not by its status', () => {
    expect(isProAiLimit(limit)).toBe(true)
    expect(isProAiLimit(rateLimited)).toBe(false)
    expect(isProAiLimit({ response: { status: 402, data: { detail: { error: 'insufficient_credits' } } } })).toBe(false)
    expect(isProAiLimit(null)).toBe(false)
  })

  it('reads in English, and the shared formatter (exercise feedback, project hints, roadmap) uses it', () => {
    const english = "You've used your 50 included AI credits for the current 4-hour window. Your course access " +
      'remains available. More AI credits will become available as earlier usage leaves the window.'
    expect(proAiLimitMessage(limit)).toBe(english)
    expect(getErrorMessage(limit)).toBe(english)
    expect(getErrorMessage(limit)).not.toContain('server English text')
  })

  it('reads in Arabic for an Arabic reader', () => {
    useLanguageStore.setState({ language: 'ar' })
    expect(getErrorMessage(limit)).toContain('يظل وصولك إلى الدورات متاحًا')
    expect(proAiLimitMessage(limit)).toMatch(/[؀-ۿ]/)
  })

  it('leaves every other error as it was', () => {
    expect(proAiLimitMessage(rateLimited)).toBeNull()
    expect(getErrorMessage(rateLimited)).toBe('Too many requests')
  })
})
