import { existsSync } from 'node:fs'
import { join } from 'node:path'
import { describe, expect, it } from 'vitest'
import { ADMIN_NAV, NAV, isActive, navFor } from '@/components/layout/nav'

const hrefs = (items: { href: string }[]) => items.map((i) => i.href)

describe('the navigation list', () => {
  it('lists the primary destinations, including Learning Tracks', () => {
    expect(hrefs(NAV)).toEqual([
      '/', '/learn/masar', '/explore', '/tracks', '/mentor', '/challenges', '/community', '/tools', '/glossary',
    ])
  })

  it('no longer carries Dashboard, My Courses, Certificates or Plans as primary destinations', () => {
    for (const removed of ['/dashboard', '/learn/my-courses', '/certificates', '/billing']) {
      expect(hrefs(NAV)).not.toContain(removed)
    }
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
    expect(isActive('/tools', '/tools')).toBe(true)
    expect(isActive('/tools/x', '/tools')).toBe(true)
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
    expect(isActive('/tools-archive', '/tools')).toBe(false)
    expect(isActive('/tools', '/tracks')).toBe(false)
  })

  it('marks Home only on the home page, not on every page', () => {
    expect(isActive('/', '/')).toBe(true)
    expect(isActive('/dashboard', '/')).toBe(false)
    expect(isActive('/tools/x', '/')).toBe(false)
  })
})
