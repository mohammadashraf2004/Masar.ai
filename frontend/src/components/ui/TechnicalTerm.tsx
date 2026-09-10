'use client'
import { useEffect, useId, useRef, useState } from 'react'
import { BookMarked, Check, X } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { useVocabularyStore } from '@/lib/vocabulary'
import { findTerm, rolesForTerm, type TechnicalTermEntry } from '@/content/terminology'

/**
 * The one place technical terminology is rendered.
 *
 * The whole Arabic-first policy comes down to a visual rule: the English
 * industry term is the prominent thing on screen, the Arabic is the
 * explanation underneath it. A student who only ever saw "قاعدة بيانات
 * المتجهات" cannot search Stack Overflow, read a paper, or recognise a line
 * in a job description — so `preferred` (English) is always the headline and
 * `ar` always the gloss, in every language setting.
 *
 * Two shapes:
 *   <TechnicalTerm term="Embeddings" />        inline, clickable, in prose
 *   <TermCard term="Embeddings" />             the vocabulary card
 */

interface TermLookupProps {
  /** Any surface form: dictionary id, English term, abbreviation or Arabic. */
  term: string
  /** Override the dictionary's Arabic gloss (rarely needed). */
  arabic?: string
  /** Override the dictionary's category label (rarely needed). */
  category?: string
}

function resolve(term: string): TechnicalTermEntry | undefined {
  return findTerm(term)
}

/** Records that the reader has now met this term. Fire-and-forget. */
function useEncountered(termId: string | undefined) {
  useEffect(() => {
    if (!termId) return
    // Read the action off the store rather than subscribing: a lesson can
    // render dozens of terms, and subscribing would re-render all of them
    // on every batch update.
    useVocabularyStore.getState().markEncountered([termId])
  }, [termId])
}

// ─── Definition panel (shared by the popover and the card) ───────────────

function TermDefinition({
  entry,
  arabicOverride,
  categoryOverride,
}: {
  entry: TechnicalTermEntry
  arabicOverride?: string
  categoryOverride?: string
}) {
  const { t, language } = useI18n()
  const roles = rolesForTerm(entry.id)

  // Built entirely from <span>s with block display rather than <div>/<p>:
  // this renders inside the inline popover, which itself sits inside a
  // lesson paragraph. A block element there is invalid nesting and closes
  // the surrounding <p> in the HTML parser.
  return (
    <span className="block space-y-2.5">
      <span className="block">
        {/* English first and largest — this is the form they must recognise. */}
        <span className="block font-display font-bold text-bright text-sm leading-tight" dir="ltr">
          {entry.preferred}
        </span>
        {entry.preferred !== entry.en && (
          <span className="block text-xs text-dim leading-tight mt-0.5" dir="ltr">
            {entry.en}
          </span>
        )}
        <span className="block text-xs text-amber2 mt-1" dir="rtl">
          {arabicOverride ?? entry.ar}
        </span>
      </span>

      <span
        className="block text-xs leading-relaxed text-soft"
        dir={language === 'ar' ? 'rtl' : 'ltr'}
      >
        {language === 'ar' ? entry.definitionAr : entry.definitionEn}
      </span>

      {entry.exampleAr && language === 'ar' && (
        <span
          className="block text-xs leading-relaxed text-dim border-s-2 border-amber/30 ps-2"
          dir="rtl"
        >
          <span className="text-ghost">{t('term.example')}: </span>
          {entry.exampleAr}
        </span>
      )}

      <span className="flex items-center gap-1.5 flex-wrap pt-0.5">
        <span className="text-[10px] px-1.5 py-0.5 rounded border border-border bg-muted/40 text-dim">
          {categoryOverride ?? entry.category}
        </span>
        {roles.slice(0, 2).map((role) => (
          <span
            key={role.id}
            className="text-[10px] px-1.5 py-0.5 rounded border border-sky/20 bg-sky/10 text-sky"
            dir="ltr"
          >
            {role.title}
          </span>
        ))}
      </span>
    </span>
  )
}

// ─── Inline term ─────────────────────────────────────────────────────────

interface TechnicalTermProps extends TermLookupProps {
  /**
   * First mention in this lesson: renders `Embeddings (التضمينات)` per the
   * first-mention rule. Later mentions render the English term alone.
   */
  firstMention?: boolean
  className?: string
}

export function TechnicalTerm({
  term,
  arabic,
  category,
  firstMention = false,
  className,
}: TechnicalTermProps) {
  const entry = resolve(term)
  const { mode } = useI18n()
  const [open, setOpen] = useState(false)
  const wrapRef = useRef<HTMLSpanElement>(null)
  const panelId = useId()

  useEncountered(entry?.id)

  useEffect(() => {
    if (!open) return
    const onClick = (e: MouseEvent) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target as Node)) setOpen(false)
    }
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false)
    }
    document.addEventListener('mousedown', onClick)
    document.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('mousedown', onClick)
      document.removeEventListener('keydown', onKey)
    }
  }, [open])

  // Unknown term — render the text unchanged rather than inventing a chip.
  if (!entry) return <>{term}</>

  // In English Technical mode the Arabic gloss is dropped: the reader has
  // opted into the phrasing used at work.
  const showGloss = firstMention && mode !== 'english_technical'

  return (
    <span ref={wrapRef} className={cn('relative inline-block', className)}>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        aria-controls={open ? panelId : undefined}
        className={cn(
          'inline items-baseline text-start font-medium transition-colors',
          'text-amber2 hover:text-amber border-b border-dotted border-amber/40 hover:border-amber',
          firstMention && 'border-solid'
        )}
        dir="ltr"
      >
        {entry.preferred}
      </button>
      {showGloss && (
        <span className="text-dim" dir="rtl">
          {' '}
          ({entry.ar})
        </span>
      )}

      {open && (
        <span
          id={panelId}
          role="dialog"
          className="absolute z-50 top-full mt-2 start-0 w-72 max-w-[calc(100vw-2rem)] p-3.5 rounded-lg bg-ink border border-border shadow-2xl block text-start"
        >
          <TermDefinition entry={entry} arabicOverride={arabic} categoryOverride={category} />
        </span>
      )}
    </span>
  )
}

// ─── Vocabulary card ─────────────────────────────────────────────────────

interface TermCardProps extends TermLookupProps {
  className?: string
  /** Show the "mark as learned" control (glossary and course pages). */
  actionable?: boolean
}

export function TermCard({ term, arabic, category, className, actionable = true }: TermCardProps) {
  const entry = resolve(term)
  const { t } = useI18n()
  const learned = useVocabularyStore((s) => (entry ? s.learned.has(entry.id) : false))
  const markLearned = useVocabularyStore((s) => s.markLearned)

  useEncountered(entry?.id)

  if (!entry) return null

  return (
    <div
      className={cn(
        'p-4 rounded-lg bg-panel border transition-colors',
        learned ? 'border-emerald/25' : 'border-border hover:border-amber/20',
        className
      )}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="min-w-0">
          <p className="font-display font-bold text-bright text-sm truncate" dir="ltr">
            {entry.preferred}
          </p>
          {entry.preferred !== entry.en && (
            <p className="text-[11px] text-dim truncate" dir="ltr">
              {entry.en}
            </p>
          )}
          <p className="text-xs text-amber2 mt-0.5" dir="rtl">
            {arabic ?? entry.ar}
          </p>
        </div>
        <span className="text-[10px] px-1.5 py-0.5 rounded border border-border bg-muted/40 text-dim shrink-0">
          {category ?? entry.category}
        </span>
      </div>

      <p className="text-xs leading-relaxed text-soft" dir="rtl">
        {entry.definitionAr}
      </p>

      {actionable && (
        <button
          type="button"
          onClick={() => markLearned(entry.id)}
          disabled={learned}
          className={cn(
            'mt-3 inline-flex items-center gap-1.5 text-[11px] px-2 py-1 rounded border transition-colors',
            learned
              ? 'border-emerald/25 bg-emerald/10 text-emerald cursor-default'
              : 'border-border text-ghost hover:text-amber hover:border-amber/30'
          )}
        >
          {learned ? <Check size={11} /> : <BookMarked size={11} />}
          {learned ? t('term.learned') : t('term.markLearned')}
        </button>
      )}
    </div>
  )
}

// ─── Course vocabulary panel ─────────────────────────────────────────────

export function CourseVocabulary({ terms, className }: { terms: string[]; className?: string }) {
  const { t } = useI18n()
  const resolved = terms.map(resolve).filter((e): e is TechnicalTermEntry => Boolean(e))
  if (resolved.length === 0) return null

  return (
    <div className={className}>
      <div className="flex items-center gap-2 mb-3">
        <BookMarked size={14} className="text-amber" />
        <h3 className="text-sm font-medium text-bright">{t('term.inThisCourse')}</h3>
        <span className="text-xs text-ghost">{resolved.length}</span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {resolved.map((entry) => (
          <TermCard key={entry.id} term={entry.id} />
        ))}
      </div>
    </div>
  )
}

// ─── Full-screen term detail (used from the glossary) ────────────────────

export function TermDetailModal({ term, onClose }: { term: string; onClose: () => void }) {
  const entry = resolve(term)
  const { t } = useI18n()
  const roles = entry ? rolesForTerm(entry.id) : []

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onClose])

  if (!entry) return null

  return (
    <>
      <div className="fixed inset-0 bg-void/80 backdrop-blur-sm z-40" onClick={onClose} />
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="bg-ink border border-border rounded-xl shadow-2xl w-full max-w-md pointer-events-auto max-h-[80vh] overflow-y-auto">
          <div className="flex items-start justify-between gap-3 px-5 py-4 border-b border-border">
            <div className="min-w-0">
              <p className="font-display font-bold text-white text-lg leading-tight" dir="ltr">
                {entry.preferred}
              </p>
              {entry.preferred !== entry.en && (
                <p className="text-xs text-dim" dir="ltr">
                  {entry.en}
                </p>
              )}
              <p className="text-sm text-amber2 mt-1" dir="rtl">
                {entry.ar}
              </p>
            </div>
            <button
              onClick={onClose}
              aria-label={t('common.close')}
              className="w-11 h-11 lg:w-7 lg:h-7 rounded flex items-center justify-center text-ghost hover:text-bright hover:bg-surface transition-colors shrink-0"
            >
              <X size={15} />
            </button>
          </div>

          <div className="px-5 py-4 space-y-4">
            <p className="text-sm leading-relaxed text-soft" dir="rtl">
              {entry.definitionAr}
            </p>
            <p className="text-xs leading-relaxed text-dim" dir="ltr">
              {entry.definitionEn}
            </p>

            {entry.exampleAr && (
              <p
                className="text-xs leading-relaxed text-soft border-s-2 border-amber/30 ps-3"
                dir="rtl"
              >
                <span className="text-ghost">{t('term.example')}: </span>
                {entry.exampleAr}
              </p>
            )}

            {roles.length > 0 && (
              <div>
                <p className="text-xs text-ghost mb-2">{t('term.relatedRoles')}</p>
                <div className="flex flex-wrap gap-1.5">
                  {roles.map((role) => (
                    <span
                      key={role.id}
                      className="text-[11px] px-2 py-0.5 rounded border border-sky/20 bg-sky/10 text-sky"
                      dir="ltr"
                    >
                      {role.title}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {roles[0] && (
              <div>
                <p className="text-xs text-ghost mb-2">{t('term.jdPhrases')}</p>
                <ul className="space-y-1.5">
                  {roles[0].jdPhrases.map((phrase) => (
                    <li
                      key={phrase}
                      className="text-xs text-dim leading-relaxed ps-3 border-s border-border"
                      dir="ltr"
                    >
                      {phrase}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
