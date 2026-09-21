import type { StringKey } from '@/lib/i18n'

/**
 * Which message a failed AI request deserves.
 *
 * The mentor page used to show one fixed sentence — "Could not reach the
 * mentor. Check your API configuration." — for every failure. That is right
 * for almost none of them and wrong for the ones a learner actually meets:
 * an unverified email (403), an empty wallet (402) and a rate limit (429) are
 * things the learner can fix, and each read as "the mentor is broken".
 *
 * Returns a key rather than a string so the message follows the reader's
 * language. Only ever reads the status and the machine-readable `error` code;
 * it never surfaces server text, which for a 5xx is deliberately opaque.
 */
export function mentorErrorKey(error: unknown): StringKey {
  const resp = (error as {
    response?: { status?: number; data?: { detail?: unknown } }
  } | null)?.response

  // No response at all: offline, DNS, CORS, or the client's own timeout.
  if (!resp) return 'mentor.error.network'

  const detail = resp.data?.detail
  const code = typeof detail === 'object' && detail !== null
    ? (detail as { error?: unknown }).error
    : undefined

  if (resp.status === 402 || code === 'insufficient_credits') return 'mentor.error.credits'
  if (resp.status === 403 && code === 'email_verification_required') return 'mentor.error.verify'
  if (resp.status === 429) return 'mentor.error.rateLimit'
  // 422: the input broke a length limit or a schema rule.
  if (resp.status === 422) return 'mentor.error.invalid'
  // 503 is the backend saying the provider failed and the credits came back;
  // anything else 5xx is the same to the learner.
  return 'mentor.error.unavailable'
}
