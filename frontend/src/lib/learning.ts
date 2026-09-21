/**
 * Presentation helpers for the learning-path screens.
 *
 * Nothing here decides what a path contains — that is the backend's job. These
 * functions only turn what the API sent into text and labels, and they lean on
 * the systems the app already has instead of adding parallel ones:
 *
 *   - language and terminology mode come from lib/language.ts,
 *   - "pick the Arabic or English twin" is `pick` from lib/content-language.ts,
 *   - a skill such as "RAG" resolves through the terminology dictionary
 *     (`findTerm`), so it gets exactly the gloss the lessons give it.
 */
import { findTerm } from '@/content/terminology'
import { pick } from '@/lib/content-language'
import type { StringKey } from '@/lib/i18n'
import type { TerminologyMode, UiLanguage } from '@/lib/language'
import type { CatalogCourse, PathAdvisory, Skill } from '@/types'

/** How an entity name should read for the reader's language and mode. */
export interface LabelParts {
  primary: string
  /** Direction of `primary`: English terms always run left-to-right. */
  primaryDir: 'ltr' | 'rtl'
  /** An Arabic gloss to show in parentheses after the primary, when wanted. */
  gloss?: string
}

interface LabelContext {
  language: UiLanguage
  mode: TerminologyMode
}

/**
 * `term` — a technical name (a field, a career goal, a skill). Follows the
 * Arabic-first policy (docs/content/ARABIC_FIRST_GUIDELINES.md): the English
 * term stays the working vocabulary and Arabic explains it once, as
 * `NLP (معالجة اللغة الطبيعية)`. English Technical mode drops the gloss.
 *
 * `label` — an ordinary word the interface owns (a level, a stage title).
 * These read in Arabic in Arabic, and only English Technical asks for English.
 *
 * `dense` is for lists where the same name repeats many times: Industry Mode
 * then shows the English term alone, and Arabic First keeps the gloss.
 */
export function learningLabel(
  en: string,
  ar: string | null | undefined,
  ctx: LabelContext,
  options: { kind?: 'term' | 'label'; dense?: boolean } = {}
): LabelParts {
  const { kind = 'term', dense = false } = options
  const arabic = ar?.trim() || undefined

  if (ctx.language === 'en') return { primary: en, primaryDir: 'ltr' }

  if (kind === 'label') {
    if (ctx.mode === 'english_technical' || !arabic) return { primary: en, primaryDir: 'ltr' }
    return { primary: arabic, primaryDir: 'rtl' }
  }

  // Technical term, Arabic interface.
  if (ctx.mode === 'english_technical' || !arabic) return { primary: en, primaryDir: 'ltr' }
  if (ctx.mode === 'industry' && dense) return { primary: en, primaryDir: 'ltr' }
  return { primary: en, primaryDir: 'ltr', gloss: arabic }
}

/** The label as one plain string — for sentences and aria-labels. */
export function labelText(parts: LabelParts): string {
  return parts.gloss ? `${parts.primary} (${parts.gloss})` : parts.primary
}

export interface Named {
  name: string
  name_ar?: string | null
}
export interface Titled {
  title: string
  title_ar?: string | null
}

export const levelLabel = (level: Named, ctx: LabelContext) =>
  learningLabel(level.name, level.name_ar, ctx, { kind: 'label' })

export const fieldLabel = (field: Named, ctx: LabelContext, dense = false) =>
  learningLabel(field.name, field.name_ar, ctx, { kind: 'term', dense })

export const roleLabel = (role: Titled, ctx: LabelContext, dense = false) =>
  learningLabel(role.title, role.title_ar, ctx, { kind: 'term', dense })

/** Stage and course titles are authored Arabic-first with English terms inline,
 *  so they are labels, not terms. */
export const titleLabel = (item: Titled, ctx: LabelContext) =>
  learningLabel(item.title, item.title_ar, ctx, { kind: 'label' })

/**
 * A skill, through the terminology dictionary when it has an entry. "RAG",
 * "Embeddings" and "LLMs" therefore read exactly as they do in the lessons
 * (including the first-mention gloss); a skill the dictionary has never heard
 * of falls back to its own name.
 */
export function skillLabel(skill: Skill, ctx: LabelContext): LabelParts {
  const term = findTerm(skill.name) ?? findTerm(skill.slug)
  if (!term) return { primary: skill.name, primaryDir: 'ltr' }
  const showGloss = ctx.language === 'ar' && ctx.mode === 'arabic_first'
  return { primary: term.preferred, primaryDir: 'ltr', gloss: showGloss ? term.ar : undefined }
}

/** The title to show for a course or stage, picking the reader's language and
 *  falling back to English when no Arabic twin exists. */
export function localizedName(item: Titled, language: UiLanguage): string {
  return pick(item.title, item.title_ar, language)
}

/** Where "Continue" goes: the lessons themselves when the catalogue knows where
 *  they live, else the course's own page. */
export function courseHref(step: { course: Pick<CatalogCourse, 'href' | 'slug'> }): string {
  return step.course.href ?? `/courses/${step.course.slug}`
}

// ─── Advisories ──────────────────────────────────────────────────────────────

interface AdvisoryContext extends LabelContext {
  /** The `tf` returned by `useI18n()`. */
  tf: (key: StringKey, vars?: Record<string, string | number>) => string
  fields: Record<string, Named>
}

/**
 * The sentence for an advisory the learner should see, or null when it is not
 * for them. The server also raises catalogue-configuration advisories
 * (a prerequisite cycle, a missing template); those are for admins and are
 * deliberately never rendered to a learner.
 */
export function advisoryText(advisory: PathAdvisory, ctx: AdvisoryContext): string | null {
  const name = (slug: unknown) => {
    const field = ctx.fields[String(slug)]
    return field ? labelText(fieldLabel(field, ctx, true)) : String(slug)
  }
  const list = (slugs: unknown, separator: string) =>
    (Array.isArray(slugs) ? slugs : []).map(name).join(separator)
  const params = advisory.params

  switch (advisory.code) {
    case 'field_above_level':
      return ctx.tf('advisory.field_above_level', { field: name(params.field) })
    case 'prerequisite_route_added':
      return ctx.tf('advisory.prerequisite_route_added', {
        field: name(params.field),
        added: list(params.added, ', '),
      })
    case 'prerequisites_recommended':
      return ctx.tf('advisory.prerequisites_recommended', {
        field: name(params.field),
        have: Number(params.have ?? 0),
        recommended: Number(params.recommended ?? 0),
        suggested: list(params.suggested, ' / '),
      })
    case 'no_available_courses':
      return ctx.tf('advisory.no_available_courses')
    default:
      return null
  }
}
