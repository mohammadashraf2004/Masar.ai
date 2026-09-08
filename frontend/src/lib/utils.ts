import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

export function formatRelative(iso: string) {
  const diff = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'just now'
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  return formatDate(iso)
}

export function difficultyColor(d: string) {
  return { beginner: 'text-emerald', intermediate: 'text-amber', advanced: 'text-rose' }[d] ?? 'text-soft'
}

export function difficultyBg(d: string) {
  return {
    beginner: 'bg-emerald/10 text-emerald border-emerald/20',
    intermediate: 'bg-amber/10 text-amber border-amber/20',
    advanced: 'bg-rose/10 text-rose border-rose/20',
  }[d] ?? 'bg-muted text-soft'
}

export function scoreColor(score: number) {
  if (score >= 75) return 'text-emerald'
  if (score >= 50) return 'text-amber'
  return 'text-rose'
}

export function scoreGradient(score: number) {
  if (score >= 75) return 'from-emerald to-emerald/50'
  if (score >= 50) return 'from-amber to-amber/50'
  return 'from-rose to-rose/50'
}

/**
 * Returns `url` only if it is safe to put in an href/src, otherwise
 * undefined.
 *
 * React does NOT sanitize href — `<a href={userValue}>` with a
 * "javascript:" value executes that script in the viewer's origin when
 * clicked, which (with the access token in localStorage) is a one-click
 * account takeover. The API rejects these schemes on write, so this is
 * defence in depth for rows that predate that validation and for any
 * future field that skips it.
 */
export function safeUrl(url?: string | null): string | undefined {
  if (!url) return undefined
  try {
    const parsed = new URL(url, window.location.origin)
    return parsed.protocol === 'http:' || parsed.protocol === 'https:' ? url : undefined
  } catch {
    return undefined
  }
}

/** FastAPI returns 422 as `detail: [{loc, msg, ...}]`. Render it as
 *  something a person can act on ("Password: ...") instead of the raw
 *  axios string, which only says "Request failed with status code 422"
 *  and leaves the user with no idea what to change. */
function formatValidationErrors(detail: unknown[]): string {
  const parts = detail
    .map((d) => {
      if (!d || typeof d !== 'object') return null
      const { loc, msg } = d as { loc?: unknown[]; msg?: string }
      if (!msg) return null
      // loc is like ["body", "password"] — the last segment is the field.
      const field = Array.isArray(loc)
        ? String(loc[loc.length - 1] ?? '').replace(/_/g, ' ')
        : ''
      const label = field && field !== 'body' ? field[0].toUpperCase() + field.slice(1) : ''
      // Pydantic prefixes custom validator messages with "Value error, ".
      const clean = msg.replace(/^Value error,\s*/, '')
      return label ? `${label}: ${clean}` : clean
    })
    .filter(Boolean)
  return parts.length ? parts.join('. ') : 'Please check the details you entered.'
}

export function getErrorMessage(error: unknown): string {
  // Only ever surfaces the API's own `detail`, which the backend
  // sanitizes; a 500 carries an opaque error_id rather than a traceback.
  // Never render a raw axios error (its message embeds the full request
  // URL, and says nothing useful) or `response.data` wholesale.
  if (typeof error === 'object' && error !== null && 'response' in error) {
    const resp = (error as {
      response?: { status?: number; data?: { detail?: unknown; error_id?: string } }
    }).response
    const detail = resp?.data?.detail
    if (typeof detail === 'string') return detail
    // 422 validation errors arrive as an array of field problems.
    if (Array.isArray(detail)) return formatValidationErrors(detail)
    // 402 insufficient-credits returns a structured detail object.
    if (detail && typeof detail === 'object' && 'message' in detail) {
      return String((detail as { message: unknown }).message)
    }
    if (resp?.data?.error_id) {
      return `Something went wrong on our side. Reference: ${resp.data.error_id}`
    }
    if (resp?.status === 429) return 'Too many attempts. Please wait a moment and try again.'
    if (resp?.status === 401) return 'Invalid email or password.'
    if (!resp) return 'Could not reach the server. Check your connection and try again.'
    return 'An error occurred'
  }
  if (error instanceof Error) return error.message
  return 'An unexpected error occurred'
}
