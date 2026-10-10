'use client'
import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { X, Check, BookOpen, ArrowRight } from 'lucide-react'
import { Badge, Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import { useRequireAuth } from '@/components/auth/AuthPrompt'
import { useI18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'
import type { VocabularyTermDetail } from '@/types'

/**
 * The AI Vocabulary term detail: definitions, aliases, related terms and
 * where a learner encounters the term in the curriculum. Fetches its own
 * data by slug so the list page never has to hold every term's full detail.
 */
export function VocabularyTermModal({
  slug,
  onClose,
  onNavigate,
}: {
  slug: string
  onClose: () => void
  onNavigate: (slug: string) => void
}) {
  const { t, language } = useI18n()
  const [slugState, setSlugState] = useState(slug)
  const [term, setTerm] = useState<VocabularyTermDetail | null>(null)
  const [failed, setFailed] = useState(false)
  const [saving, setSaving] = useState(false)
  const requireAuth = useRequireAuth()

  if (slug !== slugState) {
    setSlugState(slug)
    setTerm(null)
    setFailed(false)
  }

  useEffect(() => {
    let alive = true
    api.getVocabularyTerm(slug)
      .then((d) => alive && setTerm(d))
      .catch(() => alive && setFailed(true))
    return () => {
      alive = false
    }
  }, [slug])

  async function setStatus(status: 'learning' | 'mastered') {
    // Reading a term is public; tracking it is the learner's own progress.
    if (!requireAuth()) {
      onClose()
      return
    }
    setSaving(true)
    try {
      const updated = await api.recordVocabularyTermProgress(slug, status)
      setTerm(updated)
    } catch {}
    setSaving(false)
  }

  const status = term?.progress?.status ?? 'new'

  // Escape closes the modal, and focus moves onto it on open and back to
  // whatever had focus before (typically the term card that opened it) on
  // close — a modal that traps keyboard/screen-reader users without a way
  // back out is worse than no modal at all.
  const dialogRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
    const previouslyFocused = document.activeElement as HTMLElement | null
    dialogRef.current?.focus()
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', onKeyDown)
    return () => {
      document.removeEventListener('keydown', onKeyDown)
      previouslyFocused?.focus?.()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div
      ref={dialogRef}
      tabIndex={-1}
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 outline-none"
      onClick={onClose}
    >
      <div
        className="max-h-[85vh] w-full max-w-lg overflow-y-auto rounded-xl border border-border bg-panel p-5"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-4 flex items-start justify-between gap-3">
          <div className="min-w-0">
            {term && (
              <>
                <p className="font-display text-lg font-bold text-bright" dir={language === 'ar' ? 'rtl' : 'ltr'}>
                  {language === 'ar' ? term.term_ar : term.term_en}
                  {term.acronym && <span className="ms-2 text-sm text-ghost">({term.acronym})</span>}
                </p>
                {language === 'ar' && term.term_en !== term.term_ar && (
                  <p className="text-sm text-amber-text2" dir="ltr">{term.term_en}</p>
                )}
              </>
            )}
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label={t('common.close')}
            className="shrink-0 rounded p-1.5 text-ghost hover:bg-muted hover:text-bright"
          >
            <X size={16} />
          </button>
        </div>

        {!term && !failed && (
          <div className="flex justify-center py-10"><Spinner announce className="h-6 w-6" /></div>
        )}
        {failed && <p role="alert" className="py-6 text-center text-sm text-rose">{t('vocab.loadError')}</p>}

        {term && (
          <div className="space-y-4">
            <div className="flex flex-wrap gap-1.5">
              {term.category && <Badge variant="ghost">{term.category}</Badge>}
              <Badge variant="ghost">{term.difficulty}</Badge>
              {status !== 'new' && (
                <Badge variant={status === 'mastered' ? 'emerald' : 'sky'}>
                  {status === 'mastered' ? t('vocab.mastered') : t('vocab.learning')}
                </Badge>
              )}
            </div>

            {language === 'ar' && term.explanation_simple_ar && (
              <p className="text-sm leading-relaxed text-bright" dir="rtl">{term.explanation_simple_ar}</p>
            )}

            <div>
              <p className="mb-1 text-xs font-medium uppercase tracking-widest text-ghost">{t('vocab.definition')}</p>
              <p className="text-sm leading-relaxed text-soft" dir={language === 'ar' ? 'rtl' : 'ltr'}>
                {language === 'ar' ? term.definition_ar : term.definition_en}
              </p>
            </div>

            {language === 'ar' && term.why_it_matters_ar && (
              <div>
                <p className="mb-1 text-xs font-medium uppercase tracking-widest text-ghost">{t('vocab.whyItMatters')}</p>
                <p className="text-sm leading-relaxed text-soft" dir="rtl">{term.why_it_matters_ar}</p>
              </div>
            )}

            {language === 'ar' && term.example_ar && (
              <div>
                <p className="mb-1 text-xs font-medium uppercase tracking-widest text-ghost">{t('term.example')}</p>
                <p className="text-sm leading-relaxed text-soft" dir="rtl">{term.example_ar}</p>
              </div>
            )}

            {term.aliases.length > 0 && (
              <div className="flex flex-wrap gap-1.5" dir="ltr">
                {term.aliases.map((a) => (
                  <span key={a} className="rounded border border-border bg-muted/40 px-1.5 py-0.5 text-xs text-dim">{a}</span>
                ))}
              </div>
            )}

            {term.related_terms.length > 0 && (
              <div>
                <p className="mb-1.5 text-xs font-medium uppercase tracking-widest text-ghost">{t('vocab.relatedTerms')}</p>
                <div className="flex flex-wrap gap-1.5">
                  {term.related_terms.map((r) => (
                    <button
                      key={r.slug}
                      type="button"
                      onClick={() => onNavigate(r.slug)}
                      className="rounded-full border border-border px-2.5 py-1 text-xs text-soft hover:border-amber/30 hover:text-amber-text"
                      dir="ltr"
                    >
                      {language === 'ar' ? r.term_ar : r.term_en}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {term.courses.length > 0 && (
              <div>
                <p className="mb-1.5 text-xs font-medium uppercase tracking-widest text-ghost">{t('vocab.usedInCourses')}</p>
                <ul className="space-y-1">
                  {term.courses.map((c) => (
                    <li key={c.course_key} className="flex items-center justify-between text-xs">
                      <span className="text-soft">{c.course_title || c.course_key}</span>
                      {c.has_lesson_mapping && c.course_href ? (
                        <Link href={c.course_href} className="inline-flex items-center gap-1 text-amber-text hover:text-amber-text2">
                          {t('vocab.learnThisConcept')} <ArrowRight size={11} className="rtl:rotate-180" />
                        </Link>
                      ) : (
                        <span className="text-ghost">{t('vocab.usedNoLesson')}</span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {term.first_introduced?.href && (
              <Link
                href={term.first_introduced.href}
                className="inline-flex items-center gap-1.5 text-xs text-amber-text hover:text-amber-text2"
              >
                <BookOpen size={12} /> {t('vocab.learnThisConcept')} <ArrowRight size={11} className="rtl:rotate-180" />
              </Link>
            )}

            <div className="flex gap-2 border-t border-border pt-3">
              <Button
                size="sm"
                variant={status === 'learning' ? 'amber' : 'ghost'}
                onClick={() => setStatus('learning')}
                loading={saving}
                disabled={status === 'mastered'}
              >
                {t('vocab.markLearning')}
              </Button>
              <Button
                size="sm"
                variant={status === 'mastered' ? 'amber' : 'ghost'}
                onClick={() => setStatus('mastered')}
                loading={saving}
                disabled={status === 'mastered'}
                className={cn(status === 'mastered' && 'cursor-default')}
              >
                <Check size={12} /> {status === 'mastered' ? t('vocab.mastered') : t('vocab.markMastered')}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
