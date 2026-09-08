/**
 * Terminology lookup, normalization and in-text detection.
 *
 * Three jobs, all built off the one dictionary in `ai-terms.ts`:
 *
 *   1. normalization  — "التضمينات", "Embeddings", "embedding" all collapse
 *      to the same key, so Arabic and English searches hit the same lesson.
 *   2. lookup/search   — resolve a surface form to its dictionary entry.
 *   3. detection       — find every technical term in a run of lesson prose
 *      so the renderer can apply the first-mention rule.
 *
 * Detection never sees code: MarkdownLesson only annotates text nodes, and
 * its `code` renderer is left untouched. See ARABIC_FIRST_GUIDELINES.md.
 */
import { AI_TERMS, TERM_LIST, type TechnicalTermEntry } from './ai-terms'

export * from './ai-terms'
export * from './tech-names'
export * from './job-roles'

// ─── Normalization ───────────────────────────────────────────────────────

/** Arabic diacritics (tashkeel) and tatweel — decorative, never semantic. */
const AR_DIACRITICS = /[ؐ-ًؚ-ٰٟۖ-ۭـ]/g

/**
 * Fold the Arabic orthographic variants users actually type: hamza forms of
 * alef, alef maqsura vs ya, ta marbuta vs ha. A student typing "التضمينات"
 * or "التضمينات" (with or without hamza) means the same term.
 */
function foldArabic(input: string): string {
  return input
    .replace(AR_DIACRITICS, '')
    .replace(/[آأإٱ]/g, 'ا') // آ أ إ ٱ → ا
    .replace(/ى/g, 'ي') // ى → ي
    .replace(/ة/g, 'ه') // ة → ه
    .replace(/[ؤئ]/g, 'ء') // ؤ ئ → ء
}

/**
 * Strip the Arabic definite article. Handles both the attached form
 * ("التضمينات") and the standalone article Arabic prose glues onto an English
 * term ("الـ Embeddings") — the tatweel is already folded away by then, so
 * that one arrives as a bare "ال" and is dropped entirely.
 *
 * Kept in step with `_strip_article` in backend/app/content/terminology.py:
 * client and server must normalize a query the same way.
 */
function stripArabicArticle(word: string): string {
  const stripped = word.replace(/^ال/, '')
  if (!stripped) return ''
  return stripped.length >= 2 ? stripped : word
}

/**
 * Canonical key for any surface form, in either language.
 * Lowercases, folds Arabic orthography, treats `-`/`_`/whitespace alike, and
 * drops the Arabic article so "الـ RAG" and "rag" agree.
 */
export function normalizeTerm(input: string): string {
  if (!input) return ''
  // Character classes are written as explicit ranges rather than \p{L}/\p{N}:
  // the project type-checks against an es5 target, where unicode property
  // escapes are a compile error. Latin + digits + the Arabic block is the
  // full alphabet this dictionary is written in.
  const folded = foldArabic(input.toLowerCase())
    .replace(/[-_/]+/g, ' ')
    .replace(/[^0-9a-z\u0600-\u06FF@+ ]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
  return folded.split(' ').map(stripArabicArticle).filter(Boolean).join(' ').trim()
}

// ─── Index ───────────────────────────────────────────────────────────────

/** Every surface form of a term, in both languages. */
export function surfaceFormsOf(term: TechnicalTermEntry): string[] {
  return [term.en, term.ar, term.preferred, term.abbreviation, ...(term.aliases ?? [])].filter(
    (s): s is string => Boolean(s)
  )
}

const SURFACE_INDEX: Map<string, TechnicalTermEntry> = (() => {
  const index = new Map<string, TechnicalTermEntry>()
  for (const term of TERM_LIST) {
    for (const surface of surfaceFormsOf(term)) {
      const key = normalizeTerm(surface)
      // First writer wins: a term's own en/ar/preferred are registered
      // before another term's alias can shadow them.
      if (key && !index.has(key)) index.set(key, term)
    }
  }
  return index
})()

/** Resolve any surface form (English, Arabic, abbreviation, alias) to a term. */
export function findTerm(query: string): TechnicalTermEntry | undefined {
  if (!query) return undefined
  return AI_TERMS[query] ?? SURFACE_INDEX.get(normalizeTerm(query))
}

/**
 * Every normalized surface form a search for `query` should also match.
 * "التضمينات" expands to embeddings/embedding/embed/… so a search in either
 * language reaches the same content — no duplicate Arabic/English courses.
 */
export function expandQuery(query: string): string[] {
  const normalized = normalizeTerm(query)
  if (!normalized) return []
  const term = findTerm(query)
  if (!term) return [normalized]
  const forms = new Set([normalized, ...surfaceFormsOf(term).map(normalizeTerm)])
  return Array.from(forms).filter(Boolean)
}

/** Fuzzy-ish term search for the glossary UI: exact, then prefix, then substring. */
export function searchTerms(query: string, limit = 20): TechnicalTermEntry[] {
  const normalized = normalizeTerm(query)
  if (!normalized) return TERM_LIST.slice(0, limit)

  const scored: Array<{ term: TechnicalTermEntry; score: number }> = []
  for (const term of TERM_LIST) {
    let best = 0
    for (const surface of surfaceFormsOf(term)) {
      const key = normalizeTerm(surface)
      if (!key) continue
      if (key === normalized) best = Math.max(best, 3)
      else if (key.startsWith(normalized)) best = Math.max(best, 2)
      else if (key.includes(normalized)) best = Math.max(best, 1)
    }
    if (best === 0 && normalizeTerm(term.definitionAr).includes(normalized)) best = 0.5
    if (best > 0) scored.push({ term, score: best })
  }
  return scored
    .sort((a, b) => b.score - a.score || a.term.en.localeCompare(b.term.en))
    .slice(0, limit)
    .map((s) => s.term)
}

// ─── In-text detection ───────────────────────────────────────────────────

/**
 * Surfaces we auto-detect in lesson prose. Deliberately narrower than the
 * search index: `aliases` exist to make search forgiving, but auto-linking
 * every alias ("tools", "recall", "cache") would litter the page.
 */
function detectableSurfaces(term: TechnicalTermEntry): string[] {
  const forms = new Set<string>([term.preferred, term.en, term.ar])
  if (term.abbreviation) forms.add(term.abbreviation)
  return Array.from(forms).filter((s) => s.length >= 2)
}

function escapeRegExp(input: string): string {
  return input.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

interface SurfaceEntry {
  surface: string
  termId: string
}

const DETECTABLE: SurfaceEntry[] = TERM_LIST.flatMap((term) =>
  detectableSurfaces(term).map((surface) => ({ surface, termId: term.id }))
  // Longest first so "Vector Database" wins over "Vector".
).sort((a, b) => b.surface.length - a.surface.length)

const DETECTION_RE = new RegExp(
  DETECTABLE.map((entry) => escapeRegExp(entry.surface)).join('|'),
  'gi'
)

const SURFACE_TO_TERM: Map<string, string> = new Map(
  DETECTABLE.map((entry) => [entry.surface.toLowerCase(), entry.termId])
)

/** A character that would make a match part of a longer word. */
function isWordChar(char: string | undefined): boolean {
  return char !== undefined && /[0-9A-Za-z_\u0600-\u06FF]/.test(char)
}

export interface TermMatch {
  start: number
  end: number
  surface: string
  term: TechnicalTermEntry
}

/**
 * Every technical term occurring in `text`, in order, with word boundaries
 * verified manually — lookbehind is still not universally supported and this
 * runs on every paragraph of every lesson.
 */
export function matchTermsInText(text: string): TermMatch[] {
  if (!text) return []
  const matches: TermMatch[] = []
  DETECTION_RE.lastIndex = 0

  let match: RegExpExecArray | null
  while ((match = DETECTION_RE.exec(text)) !== null) {
    const start = match.index
    const end = start + match[0].length
    if (isWordChar(text[start - 1]) || isWordChar(text[end])) continue

    const termId = SURFACE_TO_TERM.get(match[0].toLowerCase())
    const term = termId ? AI_TERMS[termId] : undefined
    if (!term) continue

    matches.push({ start, end, surface: match[0], term })
  }
  return matches
}
