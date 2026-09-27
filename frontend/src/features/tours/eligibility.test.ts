import { beforeEach, describe, expect, it } from 'vitest'
import type { User } from '@/types'
import { blockedRoute, isNewAccount, modalOpen, pickTour, showsNewTag } from './eligibility'
import { TOURS_STORAGE_KEY, getRecord, saveRecord } from './records'
import { tourById } from './registry'
import { markTourSession, resetTourSession, tourRanThisSession } from './session'
import { OLD_ACCOUNT, student } from './tourTestKit'

const NEW = student()                                    // signed up after the tours shipped
const OLD: User = student({ id: 8, created_at: OLD_ACCOUNT })
const seenOnce = (user: User, id: Parameters<typeof saveRecord>[1], version = 1) =>
  saveRecord(user.id, id, { status: 'done', version })

beforeEach(() => resetTourSession())

describe('who is new', () => {
  it('splits accounts at the release date', () => {
    expect(isNewAccount(NEW)).toBe(true)
    expect(isNewAccount(OLD)).toBe(false)
    expect(isNewAccount({ created_at: 'not a date' })).toBe(false)
  })

  it('gives the "New" tag to an existing account\'s feature tours only', () => {
    expect(showsNewTag(tourById('mentor-interview'), OLD)).toBe(true)
    expect(showsNewTag(tourById('language'), OLD)).toBe(true)
    expect(showsNewTag(tourById('mentor-interview'), NEW)).toBe(false)
    expect(showsNewTag(tourById('onboarding'), OLD)).toBe(false)
  })
})

describe('which tour is due', () => {
  it('runs the onboarding on the first visit to home after signing up', () => {
    expect(pickTour('/dashboard', NEW, false)?.id).toBe('onboarding')
  })

  it('does not give an existing account the first-run onboarding', () => {
    expect(pickTour('/dashboard', OLD, false)).toBeNull()
  })

  it('runs a feature tour the first time its route opens', () => {
    expect(pickTour('/mentor', OLD, false)?.id).toBe('mentor-interview')
    expect(pickTour('/mentor', NEW, false)?.id).toBe('mentor-interview')
    expect(pickTour('/glossary', OLD, false)).toBeNull()
  })

  it('does not show a tour again once there is a record for its version', () => {
    seenOnce(NEW, 'onboarding')
    expect(pickTour('/dashboard', NEW, false)).toBeNull()
  })

  it('shows it again for a version newer than the one that was seen', () => {
    seenOnce(NEW, 'onboarding', 0)
    expect(pickTour('/dashboard', NEW, false)?.id).toBe('onboarding')
  })

  it('counts a skip as seen', () => {
    saveRecord(NEW.id, 'onboarding', { status: 'skipped', version: 1 })
    expect(pickTour('/dashboard', NEW, false)).toBeNull()
  })

  it('keeps one account\'s records from another\'s', () => {
    seenOnce(student({ id: 99 }), 'onboarding')
    expect(pickTour('/dashboard', NEW, false)?.id).toBe('onboarding')
  })

  it('starts nothing when a tour has already run this session', () => {
    expect(pickTour('/dashboard', NEW, true)).toBeNull()
    expect(pickTour('/mentor', OLD, true)).toBeNull()
  })
})

describe('the language tour comes after the onboarding', () => {
  it('waits for a new account to finish (or skip) the onboarding', () => {
    seenOnce(NEW, 'mentor-interview')
    expect(pickTour('/mentor', NEW, false)).toBeNull()
    saveRecord(NEW.id, 'onboarding', { status: 'skipped', version: 1 })
    expect(pickTour('/mentor', NEW, false)?.id).toBe('language')
  })

  it('does not wait for the onboarding an existing account is never given', () => {
    seenOnce(OLD, 'mentor-interview')
    expect(pickTour('/mentor', OLD, false)?.id).toBe('language')
  })

  it('runs on a lesson as well as the mentor', () => {
    expect(pickTour('/courses/langgraph/learn', OLD, false)?.id).toBe('language')
    expect(pickTour('/tools/qdrant', OLD, false)?.id).toBe('language')
  })

  it('is never in the same session as the onboarding', () => {
    // A new account: the onboarding runs on home ...
    const first = pickTour('/dashboard', NEW, tourRanThisSession())
    expect(first?.id).toBe('onboarding')
    markTourSession()
    seenOnce(NEW, 'onboarding')
    // ... and even with it done and a lesson open, nothing else starts until the next session.
    expect(pickTour('/courses/langgraph/learn', NEW, tourRanThisSession())).toBeNull()
    expect(pickTour('/mentor', NEW, tourRanThisSession())).toBeNull()
    resetTourSession()
    expect(pickTour('/courses/langgraph/learn', NEW, tourRanThisSession())?.id).toBe('language')
  })
})

describe('where a tour must not start', () => {
  it('is never on a payment, exam or sign-in page', () => {
    for (const path of ['/billing', '/billing/success', '/exam', '/exam/12', '/auth/login', '/onboarding/quick']) {
      expect(blockedRoute(path), path).toBe(true)
    }
    for (const path of ['/dashboard', '/mentor', '/billingx']) expect(blockedRoute(path), path).toBe(false)
  })

  it('is never over another dialog, but the tour\'s own card is not one', () => {
    expect(modalOpen()).toBe(false)
    const dialog = document.createElement('div')
    dialog.setAttribute('role', 'dialog')
    dialog.setAttribute('aria-modal', 'true')
    document.body.appendChild(dialog)
    expect(modalOpen()).toBe(true)
    dialog.setAttribute('data-tour-card', '')
    expect(modalOpen()).toBe(false)
    dialog.remove()
  })
})

describe('records', () => {
  it('are kept per account, in the shape { status, version, at }', () => {
    saveRecord(7, 'onboarding', { status: 'done', version: 1, at: '2026-09-28T10:00:00.000Z' })
    saveRecord(7, 'language', { status: 'skipped', version: 1 })
    expect(getRecord(7, 'onboarding')).toEqual({ status: 'done', version: 1, at: '2026-09-28T10:00:00.000Z' })
    expect(getRecord(7, 'language')).toMatchObject({ status: 'skipped', version: 1 })
    expect(getRecord(8, 'onboarding')).toBeUndefined()
    expect(Object.keys(JSON.parse(window.localStorage.getItem(TOURS_STORAGE_KEY) ?? '{}'))).toEqual(['7'])
  })

  it('ignore what is not a record', () => {
    window.localStorage.setItem(TOURS_STORAGE_KEY, JSON.stringify({ 7: { onboarding: { status: 'maybe', version: 'x' } } }))
    expect(getRecord(7, 'onboarding')).toBeUndefined()
    window.localStorage.setItem(TOURS_STORAGE_KEY, '{not json')
    expect(getRecord(7, 'onboarding')).toBeUndefined()
  })
})
