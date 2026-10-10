'use client'
import { useEffect, useMemo, useState } from 'react'
import { Search } from 'lucide-react'
import { useSession } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { LegalFooter } from '@/components/layout/LegalFooter'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Spinner, EmptyState, Badge } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { VocabularyTermModal } from '@/components/vocabulary/VocabularyTermModal'
import { useI18n } from '@/lib/i18n'
import { api } from '@/lib/api'
import { cn } from '@/lib/utils'
import type { MyCourse, VocabularyTermSummary } from '@/types'

const PAGE_SIZE = 24
const DIFFICULTIES = ['beginner', 'intermediate', 'advanced'] as const
const STATUSES = ['learning', 'mastered', 'new'] as const

type CourseCount = {
  course_key: string
  term_count: number
  course_title?: string | null
  course_slug?: string | null
  course_href?: string | null
}
type CategoryCount = { category: string; term_count: number }

function useDebounced<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delayMs)
    return () => clearTimeout(id)
  }, [value, delayMs])
  return debounced
}

/**
 * AI Vocabulary: the normalized global term dictionary (migration 022),
 * browsable by search, course, category, difficulty and learning status.
 * Every count and filter option comes from the API — nothing here is a
 * hard-coded catalogue.
 */
export default function GlossaryPage() {
  // Public: the vocabulary is for everyone; progress is shown when signed in.
  const { isLoading: authLoading, isAuthenticated } = useSession()
  const { t, language } = useI18n()

  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounced(query, 300)
  const [category, setCategory] = useState('')
  const [difficulty, setDifficulty] = useState('')
  const [courseKey, setCourseKey] = useState('')
  const [status, setStatus] = useState('')

  const [categories, setCategories] = useState<string[]>([])
  const [categoryCounts, setCategoryCounts] = useState<CategoryCount[]>([])
  const [courses, setCourses] = useState<CourseCount[]>([])

  const [items, setItems] = useState<VocabularyTermSummary[] | null>(null)
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [failed, setFailed] = useState(false)
  const [selected, setSelected] = useState<string | null>(null)

  // "From Your Masar" and "Continue Learning" — both real data, no second
  // recommendation engine and no hardcoded track/course tables: the learner's
  // own enrolled courses (already fetched for /learn/my-courses) matched
  // against the vocabulary API's own course_key<->course_slug mapping, and
  // the learner's own vocabulary progress. null = not loaded yet, [] = loaded
  // and genuinely empty (both render nothing, not a loading/error state).
  const [myCourses, setMyCourses] = useState<MyCourse[] | null>(null)
  const [fromMasarTerms, setFromMasarTerms] = useState<VocabularyTermSummary[] | null>(null)
  const [continueLearningTerms, setContinueLearningTerms] = useState<VocabularyTermSummary[] | null>(null)

  useEffect(() => {
    if (authLoading) return
    api.getVocabularyCategories().then((res) => { setCategories(res.categories); setCategoryCounts(res.counts) }).catch(() => {})
    api.getVocabularyCourseCounts().then(setCourses).catch(() => {})
    if (!isAuthenticated) return
    api.getMyCourses().then(setMyCourses).catch(() => setMyCourses([]))
    api.listVocabularyTerms({ status: 'learning', page_size: 6 }).then((res) => setContinueLearningTerms(res.items)).catch(() => setContinueLearningTerms([]))
  }, [authLoading, isAuthenticated])

  // Once both the learner's enrolled courses and the vocabulary API's course
  // list are in, match the learner's active (in-progress, else most recently
  // enrolled) course's slug against a vocabulary course_key — the only two
  // real data sources this needs, no separate mapping table. Derived with
  // useMemo (not setState in the effect below) so it's always in sync with
  // its inputs; the effect's only job is the side effect — fetching that
  // course's terms.
  const fromMasarCourse = useMemo(() => {
    if (!myCourses || myCourses.length === 0 || courses.length === 0) return null
    const active =
      myCourses.find((c) => c.status === 'in_progress') ??
      [...myCourses].sort((a, b) => (b.enrolled_at || '').localeCompare(a.enrolled_at || ''))[0]
    if (!active) return null
    const match = courses.find((c) => c.course_slug === active.slug)
    if (!match) return null
    return { courseKey: match.course_key, title: match.course_title || active.title }
  }, [myCourses, courses])

  useEffect(() => {
    if (!fromMasarCourse) return
    let stale = false
    api
      .listVocabularyTerms({ course_id: fromMasarCourse.courseKey, page_size: 6 })
      .then((res) => !stale && setFromMasarTerms(res.items))
      .catch(() => !stale && setFromMasarTerms([]))
    return () => {
      stale = true
    }
  }, [fromMasarCourse])

  // A filter change starts the list over at page 1. Adjusted during render
  // (not in an effect) by comparing against the filter set the last render
  // saw — the pattern React recommends for "reset state when a prop/derived
  // value changes" instead of a setState-in-effect cascade.
  const filtersKey = `${debouncedQuery}|${category}|${difficulty}|${courseKey}|${status}`
  const [prevFiltersKey, setPrevFiltersKey] = useState(filtersKey)
  if (filtersKey !== prevFiltersKey) {
    setPrevFiltersKey(filtersKey)
    setPage(1)
  }

  useEffect(() => {
    if (authLoading) return
    let stale = false
    api.listVocabularyTerms({
      search: debouncedQuery || undefined,
      category: category || undefined,
      difficulty: difficulty || undefined,
      course_id: courseKey || undefined,
      status: (status as 'new' | 'learning' | 'mastered') || undefined,
      page,
      page_size: PAGE_SIZE,
    })
      .then((res) => {
        if (stale) return
        setItems((prev) => (page === 1 ? res.items : [...(prev ?? []), ...res.items]))
        setTotal(res.total)
        setFailed(false)
      })
      .catch(() => !stale && setFailed(true))
    return () => {
      stale = true
    }
  }, [authLoading, debouncedQuery, category, difficulty, courseKey, status, page])

  const hasMore = (items?.length ?? 0) < total
  const anyFilter = !!(query || category || difficulty || courseKey || status)

  const sortedCourses = useMemo(
    () => [...courses].sort((a, b) => a.course_key.localeCompare(b.course_key)),
    [courses]
  )

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  return (
    <AppShell>
      <PageHeader title={t('term.glossaryTitle')} subtitle={t('term.glossarySubtitle')} contained />

      {selected && (
        <VocabularyTermModal slug={selected} onClose={() => setSelected(null)} onNavigate={setSelected} />
      )}

      <div className="flex flex-1 flex-col overflow-y-auto px-4 pt-6 pb-[calc(1.25rem+env(safe-area-inset-bottom))] sm:px-6 lg:px-8">
        <div className="mx-auto w-full max-w-5xl space-y-6">
          <div className="space-y-3">
            <div className="relative">
              <Search size={14} className="pointer-events-none absolute top-1/2 -translate-y-1/2 start-3 text-ghost" />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={t('term.searchPlaceholder')}
                className="min-h-[44px] w-full rounded-lg border border-border bg-surface ps-9 pe-3 py-2.5 text-base text-bright outline-none transition-colors placeholder:text-ghost focus:border-amber/40 md:text-sm lg:min-h-0"
              />
            </div>

            <div className="flex flex-wrap gap-2">
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="min-h-[44px] rounded-lg border border-border bg-surface px-2.5 py-1.5 text-sm text-soft lg:min-h-0"
              >
                <option value="">{t('term.allCategories')}</option>
                {categories.map((c) => <option key={c} value={c}>{c}</option>)}
              </select>

              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="min-h-[44px] rounded-lg border border-border bg-surface px-2.5 py-1.5 text-sm text-soft lg:min-h-0"
              >
                <option value="">{t('vocab.allDifficulties')}</option>
                {DIFFICULTIES.map((d) => <option key={d} value={d}>{t(`vocab.difficulty.${d}` as const)}</option>)}
              </select>

              <select
                value={courseKey}
                onChange={(e) => setCourseKey(e.target.value)}
                className="min-h-[44px] rounded-lg border border-border bg-surface px-2.5 py-1.5 text-sm text-soft lg:min-h-0"
              >
                <option value="">{t('vocab.allCourses')}</option>
                {sortedCourses.map((c) => (
                  <option key={c.course_key} value={c.course_key}>{c.course_title || c.course_key} ({c.term_count})</option>
                ))}
              </select>

              <select
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                className="min-h-[44px] rounded-lg border border-border bg-surface px-2.5 py-1.5 text-sm text-soft lg:min-h-0"
              >
                <option value="">{t('vocab.allStatuses')}</option>
                {STATUSES.map((s) => <option key={s} value={s}>{t(`vocab.status.${s}` as const)}</option>)}
              </select>
            </div>
          </div>

          {!!fromMasarTerms?.length && (
            <section aria-labelledby="vocab-from-masar-heading" className="space-y-2">
              <div>
              <h2 id="vocab-from-masar-heading" className="text-card-title font-semibold text-bright">{t('vocab.fromYourMasar')}</h2>
                {fromMasarCourse && (
                  <p className="text-xs text-ghost">{t('vocab.fromYourMasarSubtitle').replace('{course}', fromMasarCourse.title)}</p>
                )}
              </div>
              <div className="flex flex-wrap gap-2">
                {fromMasarTerms.map((term) => (
                  <button
                    key={term.slug}
                    type="button"
                    onClick={() => setSelected(term.slug)}
                    className="min-h-[36px] rounded-full border border-amber/20 bg-amber/5 px-3 py-1.5 text-xs font-medium text-amber-text hover:bg-amber/10"
                  >
                    {language === 'ar' ? term.term_ar : term.term_en}
                  </button>
                ))}
              </div>
            </section>
          )}

          {!!continueLearningTerms?.length && (
            <section aria-labelledby="vocab-continue-learning-heading" className="space-y-2">
              <h2 id="vocab-continue-learning-heading" className="text-card-title font-semibold text-bright">{t('vocab.continueLearning')}</h2>
              <div className="flex flex-wrap gap-2">
                {continueLearningTerms.map((term) => (
                  <button
                    key={term.slug}
                    type="button"
                    onClick={() => setSelected(term.slug)}
                    className="min-h-[36px] rounded-full border border-border bg-surface px-3 py-1.5 text-xs font-medium text-soft hover:border-amber/30"
                  >
                    {language === 'ar' ? term.term_ar : term.term_en}
                  </button>
                ))}
              </div>
            </section>
          )}

          {courses.length > 0 && (
            <section aria-labelledby="vocab-browse-course-heading" className="space-y-2">
              <h2 id="vocab-browse-course-heading" className="text-card-title font-semibold text-bright">{t('vocab.browseByCourse')}</h2>
              <div className="flex flex-wrap gap-2">
                {sortedCourses.map((c) => (
                  <button
                    key={c.course_key}
                    type="button"
                    aria-pressed={courseKey === c.course_key}
                    onClick={() => setCourseKey((prev) => (prev === c.course_key ? '' : c.course_key))}
                    className={cn(
                      'min-h-[36px] rounded-lg border px-3 py-1.5 text-start text-xs font-medium transition-colors',
                      courseKey === c.course_key
                        ? 'border-amber/40 bg-amber/10 text-amber-text'
                        : 'border-border bg-surface text-soft hover:border-amber/20'
                    )}
                  >
                    <span dir="ltr">{c.course_title || c.course_key}</span>
                    <span className="ms-1.5 text-ghost">{t('vocab.termCount').replace('{n}', String(c.term_count))}</span>
                  </button>
                ))}
              </div>
            </section>
          )}

          {categoryCounts.length > 0 && (
            <section aria-labelledby="vocab-browse-category-heading" className="space-y-2">
              <h2 id="vocab-browse-category-heading" className="text-card-title font-semibold text-bright">{t('vocab.browseByCategory')}</h2>
              <div className="flex flex-wrap gap-2">
                {categoryCounts.map((c) => (
                  <button
                    key={c.category}
                    type="button"
                    aria-pressed={category === c.category}
                    onClick={() => setCategory((prev) => (prev === c.category ? '' : c.category))}
                    className={cn(
                      'min-h-[36px] rounded-lg border px-3 py-1.5 text-xs font-medium transition-colors',
                      category === c.category
                        ? 'border-amber/40 bg-amber/10 text-amber-text'
                        : 'border-border bg-surface text-soft hover:border-amber/20'
                    )}
                  >
                    {c.category}
                    <span className="ms-1.5 text-ghost">{t('vocab.termCount').replace('{n}', String(c.term_count))}</span>
                  </button>
                ))}
              </div>
            </section>
          )}

          {failed && !items && (
            <Card className="p-8 text-center">
              <p role="alert" className="text-sm text-rose">{t('vocab.loadError')}</p>
            </Card>
          )}

          {!failed && items === null && (
            <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>
          )}

          {items !== null && items.length === 0 && (
            <EmptyState icon={<Search size={28} />} title={t(anyFilter ? 'term.empty' : 'vocab.emptyCatalog')} />
          )}

          {items !== null && items.length > 0 && (
            <>
              <div className="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
                {items.map((term) => {
                  const isMastered = term.progress?.status === 'mastered'
                  return (
                    <Card
                      key={term.slug}
                      className={cn('cursor-pointer p-4', isMastered ? 'border-emerald/25' : 'hover:border-amber/20')}
                      onClick={() => setSelected(term.slug)}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="min-w-0">
                          <p className="ui-card-title" dir="ltr">
                            {language === 'ar' ? term.term_ar : term.term_en}
                            {term.acronym && <span className="ms-1 text-xs text-ghost">({term.acronym})</span>}
                          </p>
                          {language === 'ar' && term.term_en !== term.term_ar && (
                            <p className="mt-0.5 text-xs text-amber-text2" dir="ltr">{term.term_en}</p>
                          )}
                        </div>
                        {term.category && (
                          <span className="shrink-0 rounded border border-border bg-muted/40 px-1.5 py-0.5 text-xs text-dim">
                            {term.category}
                          </span>
                        )}
                      </div>
                      {(language === 'ar' ? term.explanation_simple_ar : term.definition_en) && (
                        <p className="ui-description mt-2.5 line-clamp-2" dir={language === 'ar' ? 'rtl' : 'ltr'}>
                          {language === 'ar' ? term.explanation_simple_ar : term.definition_en}
                        </p>
                      )}
                      <div className="mt-3 flex items-center justify-between">
                        <span className="text-xs text-ghost">
                          {term.course_count > 0 ? t('vocab.courseCount').replace('{n}', String(term.course_count)) : ''}
                        </span>
                        {isMastered && <Badge variant="emerald">{t('vocab.mastered')}</Badge>}
                      </div>
                    </Card>
                  )
                })}
              </div>

              {hasMore && (
                <div className="flex justify-center">
                  <Button variant="ghost" onClick={() => setPage((p) => p + 1)}>{t('common.loadMore')}</Button>
                </div>
              )}
            </>
          )}
        </div>
        <LegalFooter className="mx-auto w-full max-w-5xl" />
      </div>
    </AppShell>
  )
}
