import '@testing-library/jest-dom/vitest'
import { createElement, forwardRef } from 'react'
import { cleanup } from '@testing-library/react'
import { afterEach, beforeEach, vi } from 'vitest'
import { resetLearningCatalogCache } from '@/hooks/learningCatalogCache'
import { useLanguageStore } from '@/lib/language'
import { resetNav } from './nav'

// jsdom has no layout engine. These tests therefore cover behaviour, structure,
// accessibility and text — including which language/direction a string is
// rendered in — but not how the page is *laid out*. Real RTL rendering and the
// mobile breakpoints are verified in an actual browser against the running app.

// React only allows `act()` in an environment that says it is a test one.
// Testing Library sets this itself, but only when the runner exposes global
// `beforeAll`/`afterAll` — Vitest does not unless `globals` is on.
;(globalThis as { IS_REACT_ACT_ENVIRONMENT?: boolean }).IS_REACT_ACT_ENVIRONMENT = true

// `next/link` needs the App Router's context; a plain anchor is what the tests
// care about (where does it point?).
// Like the real one, it forwards a ref to the anchor (a dialog focuses its main link).
vi.mock('next/link', () => ({
  default: forwardRef<HTMLAnchorElement, { href: string; children: React.ReactNode }>(function Link(
    { href, children, ...rest }, ref
  ) {
    return createElement('a', { href, ref, ...rest }, children)
  }),
}))

beforeEach(() => {
  // The app defaults to Arabic; most tests read more clearly in English, and
  // the ones about Arabic switch explicitly.
  useLanguageStore.setState({ language: 'en', mode: 'arabic_first', annotateTerms: true })
  resetLearningCatalogCache()
})

afterEach(() => {
  cleanup()
  resetNav()
  window.localStorage.clear()
})
