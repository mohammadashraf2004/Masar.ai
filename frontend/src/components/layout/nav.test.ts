import { existsSync } from 'node:fs'
import { join } from 'node:path'
import { describe, expect, it } from 'vitest'
import { ADMIN_NAV, NAV, isActive, navFor } from '@/components/layout/nav'

const hrefs = (items: { href: string }[]) => items.map((i) => i.href)

describe('the navigation list', () => {
  it('keeps every destination the app already had', () => {
    for (const existing of ['/', '/dashboard', '/learn', '/explore', '/tracks', '/tools', '/glossary', '/mentor', '/community', '/challenges']) {
      expect(hrefs(NAV)).toContain(existing)
    }
  })

  it('adds Certificates, the handoff’s fifth destination', () => {
    expect(hrefs(NAV)).toContain('/certificates')
  })

  it("keeps the handoff's relative order: Home, Tracks, Courses (the tool courses), Certificates", () => {
    const at = (href: string) => hrefs(NAV).indexOf(href)
    expect(at('/')).toBeLessThan(at('/tracks'))
    expect(at('/tracks')).toBeLessThan(at('/tools'))
    expect(at('/tools')).toBeLessThan(at('/certificates'))
  })

  it('adds Plans & offers (Task 10) straight after Certificates, and keeps the mentor', () => {
    expect(hrefs(NAV).indexOf('/billing')).toBe(hrefs(NAV).indexOf('/certificates') + 1)
    expect(hrefs(NAV)).toContain('/mentor')
  })

  it('puts the personalised path ahead of the curriculum libraries', () => {
    expect(hrefs(NAV).indexOf('/learn')).toBeLessThan(hrefs(NAV).indexOf('/tracks'))
  })

  it('lists no destination twice', () => {
    expect(new Set(hrefs(NAV)).size).toBe(NAV.length)
  })

  it('gives every destination an i18n label and an icon', () => {
    for (const item of [...NAV, ...ADMIN_NAV]) {
      expect(item.label).toMatch(/^nav\./)
      expect(item.icon).toBeTruthy()
    }
  })
})

describe('navFor', () => {
  it('shows the admin page to an admin, after the ordinary destinations', () => {
    expect(hrefs(navFor('admin'))).toEqual([...hrefs(NAV), '/admin/analytics'])
  })

  it.each([['student'], ['mentor'], [undefined]])('shows nobody else the admin page (%s)', (role) => {
    expect(hrefs(navFor(role))).toEqual(hrefs(NAV))
  })
})

describe('isActive', () => {
  it('is the exact page or anything beneath it', () => {
    expect(isActive('/tracks', '/tracks')).toBe(true)
    expect(isActive('/tracks/ai-developer', '/tracks')).toBe(true)
  })

  // "Certificates" was in the sidebar for a while with no page behind it: a link every
  // signed-in learner could click into a 404. A destination is not one until it has a route.
  it('has a page behind every destination, so no link in the sidebar or the menu is a dead end', () => {
    // Vitest runs from the frontend root (jsdom gives import.meta.url an http origin, so it cannot locate files).
    const app = join(process.cwd(), 'src', 'app')
    for (const { href } of [...NAV, ...ADMIN_NAV]) {
      const page = join(app, ...href.split('/').filter(Boolean), 'page.tsx')
      expect(existsSync(page), `${href} has no ${page}`).toBe(true)
    }
  })

  it('does not treat a sibling that shares a prefix as the same section', () => {
    expect(isActive('/tracks-archive', '/tracks')).toBe(false)
    expect(isActive('/tools', '/tracks')).toBe(false)
  })

  it('marks Home only on the home page, not on every page', () => {
    expect(isActive('/', '/')).toBe(true)
    expect(isActive('/dashboard', '/')).toBe(false)
    expect(isActive('/tracks/x', '/')).toBe(false)
  })
})
