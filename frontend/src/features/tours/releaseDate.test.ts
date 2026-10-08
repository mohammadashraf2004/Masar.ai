import { describe, expect, it } from 'vitest'
import { isNewAccount } from './eligibility'
import { TOURS_RELEASED_AT } from './registry'

/** The new Masar launch boundary: the start of 10 October 2026 in Cairo (UTC+3 that day). */
describe('TOURS_RELEASED_AT', () => {
  it('is the start of the launch day in Cairo, as one unambiguous instant', () => {
    expect(new Date(TOURS_RELEASED_AT).toISOString()).toBe('2026-10-09T21:00:00.000Z')
  })

  it('treats an account created before the launch as existing', () => {
    expect(isNewAccount({ created_at: '2026-10-09T20:59:59Z' })).toBe(false)
    expect(isNewAccount({ created_at: '2026-10-09T23:59:59+03:00' })).toBe(false)
  })

  it('treats an account created exactly at or after the launch as new', () => {
    expect(isNewAccount({ created_at: '2026-10-09T21:00:00Z' })).toBe(true)
    expect(isNewAccount({ created_at: '2026-10-10T00:00:00+03:00' })).toBe(true)
    expect(isNewAccount({ created_at: '2026-10-09T21:00:00.000000+00:00' })).toBe(true)
  })

  it('normalises timezones: the same instant gets the same answer whatever its offset', () => {
    expect(isNewAccount({ created_at: '2026-10-09T18:00:00-03:00' })).toBe(true)   // = 21:00Z
    expect(isNewAccount({ created_at: '2026-10-10T02:59:59+06:00' })).toBe(false)  // = 20:59:59Z
  })

  it('reads a timestamp without a zone as UTC, not as the browser clock', () => {
    expect(isNewAccount({ created_at: '2026-10-09T21:00:00' })).toBe(true)
    expect(isNewAccount({ created_at: '2026-10-09T20:59:59' })).toBe(false)
  })

  it('counts an unreadable date as an existing account', () => {
    expect(isNewAccount({ created_at: 'not a date' })).toBe(false)
  })
})
