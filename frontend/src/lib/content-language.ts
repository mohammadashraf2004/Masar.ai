import type { UiLanguage } from '@/lib/language'

/**
 * Choosing which language version of a piece of content to show.
 *
 * Every content row carries the original English field plus an optional
 * `*_ar` twin (added in migration 006). Arabic is not a translation layer
 * bolted on top — it is the primary field for Arabic-first courses — but
 * older courses only have English, and they must keep working untouched.
 *
 * So the rule is: ask for the reader's language, fall back to whatever
 * exists, and tell the caller when it fell back so the UI can say so
 * instead of silently showing the wrong language.
 */

export interface LocalizedText {
  text: string
  /** True when the requested language was unavailable and we fell back. */
  isFallback: boolean
  /** The language actually being shown. */
  shownIn: UiLanguage
}

function clean(value: string | null | undefined): string | undefined {
  const trimmed = value?.trim()
  return trimmed ? trimmed : undefined
}

export function pickText(
  en: string | null | undefined,
  ar: string | null | undefined,
  language: UiLanguage
): LocalizedText {
  const english = clean(en)
  const arabic = clean(ar)
  const wanted = language === 'ar' ? arabic : english
  const other = language === 'ar' ? english : arabic

  if (wanted) return { text: wanted, isFallback: false, shownIn: language }
  if (other) {
    return {
      text: other,
      isFallback: true,
      shownIn: language === 'ar' ? 'en' : 'ar',
    }
  }
  return { text: '', isFallback: false, shownIn: language }
}

/** Shorthand when the caller only needs the string. */
export function pick(
  en: string | null | undefined,
  ar: string | null | undefined,
  language: UiLanguage
): string {
  return pickText(en, ar, language).text
}

// ─── Shapes ──────────────────────────────────────────────────────────────
// Structural types, not interfaces the API objects must implement — any row
// carrying these fields works, which keeps existing types untouched.

interface Titled {
  title?: string
  title_ar?: string | null
}
interface Described {
  description?: string | null
  description_ar?: string | null
}
interface Contented {
  content?: string
  content_ar?: string | null
}

export function localizedTitle(row: Titled, language: UiLanguage): string {
  return pick(row.title, row.title_ar, language)
}

export function localizedDescription(row: Described, language: UiLanguage): string {
  return pick(row.description, row.description_ar, language)
}

export function localizedContent(row: Contented, language: UiLanguage): LocalizedText {
  return pickText(row.content, row.content_ar, language)
}
