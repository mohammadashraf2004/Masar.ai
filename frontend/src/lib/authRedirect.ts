/**
 * Where to go after signing in, carried as `?next=` on the sign-in and sign-up
 * pages.
 *
 * `next` arrives from the address bar, so it is untrusted: only a path on this
 * site is ever followed. Anything that could leave the site — an absolute URL,
 * a protocol-relative `//host`, a backslash a browser treats as a slash, a
 * control character — or that points back at an auth page (a loop) is dropped,
 * and the caller falls back to its ordinary destination.
 */

const ORIGIN = 'https://masar.invalid'

export function safeNext(raw: string | null | undefined): string | null {
  if (!raw) return null
  const value = raw.trim()
  if (!value.startsWith('/') || value.startsWith('//')) return null
  // Backslashes (`/\evil.com`) and control characters (`/\tevil.com`) are
  // normalised away by browsers into something that leaves the site.
  if (/[\\\u0000-\u001f\u007f]/.test(value)) return null
  let url: URL
  try {
    url = new URL(value, ORIGIN)
  } catch {
    return null
  }
  if (url.origin !== ORIGIN) return null
  if (url.pathname === '/auth' || url.pathname.startsWith('/auth/')) return null
  return url.pathname + url.search + url.hash
}

/** The page being looked at now, as a `next` value. */
export function currentPath(): string {
  if (typeof window === 'undefined') return '/'
  return window.location.pathname + window.location.search
}

/** The `next` this page was opened with, if it is safe to follow. */
export function nextFromLocation(): string | null {
  if (typeof window === 'undefined') return null
  return safeNext(new URLSearchParams(window.location.search).get('next'))
}

/** `/auth/login?next=…` or `/auth/register?next=…`; no `next` when it is not safe. */
export function authHref(kind: 'login' | 'register', next?: string | null): string {
  const target = safeNext(next ?? null)
  const base = kind === 'login' ? '/auth/login' : '/auth/register'
  return target ? `${base}?next=${encodeURIComponent(target)}` : base
}

// Pages that are the learning itself or someone's own account. Everything else
// (home, catalogues, course/track/challenge overviews, tools, vocabulary,
// plans, legal, certificate verification) can be browsed without signing in.
const ACCOUNT_PAGES: RegExp[] = [
  /^\/dashboard(\/|$)/,
  /^\/learn(\/|$)/,
  /^\/mentor(\/|$)/,
  /^\/profile(\/|$)/,
  /^\/onboarding(\/|$)/,
  /^\/certificates(\/|$)/,
  /^\/community(\/|$)/,
  /^\/exam(\/|$)/,
  /^\/admin(\/|$)/,
  /^\/billing\/(orders|success|course-success)(\/|$)/,
  /^\/courses\/[^/]+\/(learn|lessons)(\/|$)/,
  /^\/tools\/[^/]+/,
  /^\/challenges\/projects\/[^/]+\/workspace(\/|$)/,
]

/** True when `href` is a page that needs an account (see ACCOUNT_PAGES). */
export function needsAccount(href: string): boolean {
  const path = href.split(/[?#]/, 1)[0]
  return ACCOUNT_PAGES.some((pattern) => pattern.test(path))
}
