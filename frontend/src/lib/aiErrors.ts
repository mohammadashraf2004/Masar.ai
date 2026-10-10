import { STRINGS } from '@/lib/i18n'
import { useLanguageStore } from '@/lib/language'

/** What the API answers (429) when Pro's included AI credits for the rolling 4-hour window are
 *  used up. Course access is unaffected and nothing was taken from the wallet. */
export const PRO_AI_LIMIT = 'pro_ai_limit_reached'

function errorCode(error: unknown): unknown {
  const detail = (error as { response?: { data?: { detail?: unknown } } } | null)?.response?.data?.detail
  return typeof detail === 'object' && detail !== null ? (detail as { error?: unknown }).error : undefined
}

export function isProAiLimit(error: unknown): boolean {
  return errorCode(error) === PRO_AI_LIMIT
}

/**
 * The allowance message in the reader's language for a refused AI request, or null for any other
 * failure. A plain function (not a hook) so the shared error formatter and older pages that are not
 * wired to `useI18n` show it too; it reads the language the reader chose.
 */
export function proAiLimitMessage(error: unknown): string | null {
  if (!isProAiLimit(error)) return null
  return STRINGS[useLanguageStore.getState().language]['mentor.error.proLimit']
}
