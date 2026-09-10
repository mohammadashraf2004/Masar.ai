'use client'
import { useEffect, useMemo, useState } from 'react'
import { Search, Briefcase } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Spinner, ProgressBar, EmptyState } from '@/components/ui/index'
import { TermDetailModal } from '@/components/ui/TechnicalTerm'
import { useI18n } from '@/lib/i18n'
import { useVocabularyStore } from '@/lib/vocabulary'
import { cn } from '@/lib/utils'
import {
  TERM_LIST,
  TERM_CATEGORIES,
  searchTerms,
  JOB_ROLES,
  type TermCategory,
} from '@/content/terminology'
import { Check, Circle } from 'lucide-react'

/**
 * The vocabulary page: every technical term the platform teaches, searchable
 * in either language, with the role each one shows up in.
 *
 * Search here is the same normalization the course search uses, so
 * "التضمينات", "embedding" and "Embeddings" all land on the same entry —
 * a student should never have to guess which language the platform indexed.
 */
export default function GlossaryPage() {
  const { isLoading } = useAuth()
  const { t, language } = useI18n()
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState<TermCategory | 'all'>('all')
  const [selected, setSelected] = useState<string | null>(null)

  const learned = useVocabularyStore((s) => s.learned)
  const encountered = useVocabularyStore((s) => s.encountered)
  const markLearned = useVocabularyStore((s) => s.markLearned)
  const load = useVocabularyStore((s) => s.load)

  useEffect(() => {
    load()
  }, [load])

  const results = useMemo(() => {
    const base = query.trim() ? searchTerms(query, 200) : TERM_LIST
    return category === 'all' ? base : base.filter((term) => term.category === category)
  }, [query, category])

  const pct = TERM_LIST.length === 0 ? 0 : Math.round((learned.size / TERM_LIST.length) * 100)

  if (isLoading) {
    return (
      <div className="min-h-dvh bg-void flex items-center justify-center">
        <Spinner className="w-6 h-6" />
      </div>
    )
  }

  return (
    <AppShell>
      <PageHeader title={t('term.glossaryTitle')} subtitle={t('term.glossarySubtitle')} />

      {selected && <TermDetailModal term={selected} onClose={() => setSelected(null)} />}

      <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="max-w-5xl mx-auto space-y-6">
          {/* ── Progress ── */}
          <Card className="p-5">
            <div className="flex items-baseline justify-between mb-2">
              <span className="text-sm text-bright">{t('term.glossaryTitle')}</span>
              <span className="text-xs font-mono text-amber">
                {learned.size} / {TERM_LIST.length} · {pct}%
              </span>
            </div>
            <ProgressBar value={pct} size="md" color={pct >= 80 ? 'emerald' : 'amber'} />
          </Card>

          {/* ── Search + categories ── */}
          <div className="space-y-3">
            <div className="relative">
              <Search
                size={14}
                className="absolute top-1/2 -translate-y-1/2 start-3 text-ghost pointer-events-none"
              />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={t('term.searchPlaceholder')}
                className="w-full bg-surface border border-border rounded-lg ps-9 pe-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:border-amber/40 outline-none transition-colors"
              />
            </div>

            <div className="flex items-center gap-1.5 flex-wrap">
              {(['all', ...TERM_CATEGORIES] as const).map((value) => (
                <button
                  key={value}
                  onClick={() => setCategory(value as TermCategory | 'all')}
                  className={cn(
                    'px-2.5 py-1 rounded-full border text-xs transition-colors',
                    category === value
                      ? 'border-amber/30 bg-amber/10 text-amber'
                      : 'border-border text-ghost hover:text-soft'
                  )}
                >
                  {value === 'all' ? t('term.allCategories') : value}
                </button>
              ))}
            </div>
          </div>

          {/* ── Terms ── */}
          {results.length === 0 ? (
            <EmptyState icon={<Search size={28} />} title={t('term.empty')} />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {results.map((term) => {
                const isLearned = learned.has(term.id)
                const isSeen = encountered.has(term.id)
                return (
                  <Card
                    key={term.id}
                    className={cn(
                      'p-4 cursor-pointer',
                      isLearned ? 'border-emerald/25' : 'hover:border-amber/20'
                    )}
                    onClick={() => setSelected(term.id)}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <p className="font-display font-bold text-bright text-sm" dir="ltr">
                          {term.preferred}
                        </p>
                        {term.preferred !== term.en && (
                          <p className="text-[11px] text-dim truncate" dir="ltr">
                            {term.en}
                          </p>
                        )}
                        <p className="text-xs text-amber2 mt-0.5" dir="rtl">
                          {term.ar}
                        </p>
                      </div>
                      <span className="text-[10px] px-1.5 py-0.5 rounded border border-border bg-muted/40 text-dim shrink-0">
                        {term.category}
                      </span>
                    </div>

                    <p
                      className="text-xs leading-relaxed text-soft mt-2.5"
                      dir={language === 'ar' ? 'rtl' : 'ltr'}
                    >
                      {language === 'ar' ? term.definitionAr : term.definitionEn}
                    </p>

                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation()
                        markLearned(term.id)
                      }}
                      disabled={isLearned}
                      className={cn(
                        'mt-3 inline-flex items-center gap-1.5 text-[11px] px-2 py-1 rounded border transition-colors',
                        isLearned
                          ? 'border-emerald/25 bg-emerald/10 text-emerald cursor-default'
                          : 'border-border text-ghost hover:text-amber hover:border-amber/30'
                      )}
                    >
                      {isLearned ? <Check size={11} /> : <Circle size={9} />}
                      {isLearned ? t('term.learned') : isSeen ? t('term.markLearned') : t('term.markLearned')}
                    </button>
                  </Card>
                )
              })}
            </div>
          )}

          {/* ── Where the vocabulary is used ── */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Briefcase size={14} className="text-sky" />
              <h2 className="text-sm font-medium text-bright">{t('term.seenIn')}</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {JOB_ROLES.map((role) => (
                <Card key={role.id} className="p-4">
                  <p className="font-display font-bold text-bright text-sm" dir="ltr">
                    {role.title}
                  </p>
                  <p className="text-xs text-soft leading-relaxed mt-1" dir="rtl">
                    {role.summaryAr}
                  </p>
                  <div className="flex flex-wrap gap-1.5 mt-3">
                    {role.tools.map((tool) => (
                      <span
                        key={tool}
                        className="text-[10px] px-1.5 py-0.5 rounded border border-border bg-muted/40 text-dim"
                        dir="ltr"
                      >
                        {tool}
                      </span>
                    ))}
                  </div>
                  <ul className="mt-3 space-y-1.5">
                    {role.jdPhrases.map((phrase) => (
                      <li
                        key={phrase}
                        className="text-[11px] text-ghost leading-relaxed ps-2.5 border-s border-border"
                        dir="ltr"
                      >
                        {phrase}
                      </li>
                    ))}
                  </ul>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  )
}
