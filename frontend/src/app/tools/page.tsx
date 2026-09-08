'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Badge, Spinner, ProgressBar } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import type { ToolCourseSummary, ToolEnrollment, SearchResults } from '@/types'
import { ArrowRight, CheckCircle, Layers, Boxes, Server, Database, Clock, Search } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { localizedTitle, localizedDescription } from '@/lib/content-language'

const CATEGORY_META: Record<string, { icon: React.ElementType; color: string }> = {
  'LLM & AI Application Layer': { icon: Layers, color: 'amber' },
  'Vector Databases':           { icon: Database, color: 'sky' },
  'MLOps & Infrastructure':     { icon: Server, color: 'emerald' },
  'Data Tools':                 { icon: Boxes, color: 'violet' },
}
const CATEGORY_ORDER = Object.keys(CATEGORY_META)

export default function ToolsPage() {
  const { isLoading: authLoading } = useAuth()
  const { t, language } = useI18n()
  const [courses, setCourses] = useState<ToolCourseSummary[]>([])
  const [enrollments, setEnrollments] = useState<ToolEnrollment[]>([])
  const [loading, setLoading] = useState(true)
  const [enrollingId, setEnrollingId] = useState<number | null>(null)
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResults | null>(null)
  const [searching, setSearching] = useState(false)

  // Search runs server-side because the query has to be expanded through the
  // terminology dictionary — "التضمينات" must find the Embeddings material,
  // which no amount of client-side substring matching on titles would do.
  useEffect(() => {
    const trimmed = query.trim()
    if (trimmed.length < 2) return
    const handle = setTimeout(async () => {
      setSearching(true)
      try {
        setResults(await api.search(trimmed))
      } catch {
        setResults(null)
      }
      setSearching(false)
    }, 250)
    return () => clearTimeout(handle)
  }, [query])

  useEffect(() => {
    if (authLoading) return
    async function load() {
      try {
        const [c, e] = await Promise.all([api.listToolCourses(), api.getMyToolEnrollments()])
        setCourses(c)
        setEnrollments(e)
      } catch {}
      setLoading(false)
    }
    load()
  }, [authLoading])

  async function handleEnroll(course: ToolCourseSummary) {
    setEnrollingId(course.id)
    try {
      const enr = await api.enrollToolCourse(course.id)
      setEnrollments(prev => [...prev.filter(e => e.tool_course_id !== course.id), enr])
    } catch {}
    setEnrollingId(null)
  }

  if (authLoading || loading) return (
    <div className="min-h-screen bg-void flex items-center justify-center">
      <Spinner className="w-6 h-6" />
    </div>
  )

  const searchActive = query.trim().length >= 2
  const shownResults = searchActive ? results : null

  const enrMap = new Map(enrollments.map(e => [e.tool_course_id, e]))
  const byCategory = new Map<string, ToolCourseSummary[]>()
  for (const c of courses) {
    const key = c.category ?? 'Other'
    if (!byCategory.has(key)) byCategory.set(key, [])
    byCategory.get(key)!.push(c)
  }
  const orderedCategories = [
    ...CATEGORY_ORDER.filter(c => byCategory.has(c)),
    ...Array.from(byCategory.keys()).filter(c => !CATEGORY_ORDER.includes(c)),
  ]

  return (
    <AppShell>
      <PageHeader
        title={t('nav.tools')}
        subtitle="No prerequisites, no tracks — pick any tool and start. Great alongside or independent of a career track."
      />

      <div className="flex-1 overflow-y-auto px-8 py-6">
        <div className="max-w-5xl mx-auto space-y-10">
          {/* ── Bilingual search ── */}
          <div>
            <div className="relative">
              <Search
                size={14}
                className="absolute top-1/2 -translate-y-1/2 start-3 text-ghost pointer-events-none"
              />
              <input
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder={t('course.search')}
                className="w-full bg-surface border border-border rounded-lg ps-9 pe-3 py-2.5 text-sm text-bright placeholder:text-ghost focus:border-amber/40 outline-none transition-colors"
              />
            </div>
            <p className="text-xs text-ghost mt-1.5">{t('course.searchHint')}</p>
          </div>

          {shownResults && (
            <div className="space-y-3">
              {/* The term the query resolved to, shown in both languages —
                  this is where a student learns that what they searched for
                  in Arabic has an English name. */}
              {shownResults.matched_terms.map(term => (
                <Card key={term.id} className="p-4 border-amber/20">
                  <p className="font-display font-bold text-bright text-sm" dir="ltr">
                    {term.preferred}
                  </p>
                  <p className="text-xs text-amber2 mt-0.5" dir="rtl">{term.ar}</p>
                  <p className="text-xs text-soft leading-relaxed mt-2" dir="rtl">
                    {term.definitionAr}
                  </p>
                </Card>
              ))}

              {shownResults.hits.length === 0 && !searching ? (
                <p className="text-sm text-ghost py-6 text-center">{t('course.noResults')}</p>
              ) : (
                shownResults.hits.map(hit => (
                  <Link key={`${hit.kind}-${hit.id}`} href={hit.href} className="block">
                    <Card className="p-4 hover:border-amber/20">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge variant="ghost" className="text-[10px]">{hit.kind.replace('_', ' ')}</Badge>
                        {hit.parent_title && (
                          <span className="text-xs text-ghost truncate">{hit.parent_title}</span>
                        )}
                      </div>
                      <p className="text-sm text-bright">
                        {localizedTitle(hit, language) || hit.title}
                      </p>
                      {(hit.description || hit.description_ar) && (
                        <p className="text-xs text-ghost leading-relaxed mt-1 line-clamp-2">
                          {localizedDescription(hit, language)}
                        </p>
                      )}
                    </Card>
                  </Link>
                ))
              )}
            </div>
          )}

          {!searchActive && orderedCategories.map(category => {
            const meta = CATEGORY_META[category] ?? { icon: Boxes, color: 'ghost' }
            const Icon = meta.icon
            return (
              <div key={category}>
                <div className="flex items-center gap-2 mb-4">
                  <Icon size={15} className={`text-${meta.color}`} />
                  <h2 className="text-sm font-medium text-bright">{category}</h2>
                  <span className="text-xs text-ghost">
                    {byCategory.get(category)!.length} {t('course.tools')}
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  {byCategory.get(category)!.map(course => {
                    const enr = enrMap.get(course.id)
                    const comingSoon = course.topic_count === 0 && !enr
                    return (
                      <Card
                        key={course.id}
                        className={cn('p-5 flex flex-col', comingSoon && 'opacity-60')}
                      >
                        <div className="flex items-start justify-between mb-3">
                          <span className={cn('text-2xl', comingSoon && 'grayscale')}>{course.icon}</span>
                          {comingSoon ? (
                            <Badge variant="ghost">
                              <Clock size={10} className="me-1" /> {t('course.comingSoon')}
                            </Badge>
                          ) : (
                            <Badge variant={course.difficulty}>{course.difficulty}</Badge>
                          )}
                        </div>
                        <h3 className="font-medium text-bright text-sm mb-1.5">
                          {localizedTitle(course, language)}
                        </h3>
                        <p className="text-xs text-ghost leading-relaxed mb-4 flex-1">
                          {localizedDescription(course, language)}
                        </p>

                        {enr ? (
                          <div className="mb-3">
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs text-ghost">
                                {enr.progress_pct >= 100 ? t('course.completed') : t('course.inProgress')}
                              </span>
                              <span className="text-xs font-mono text-amber">{Math.round(enr.progress_pct)}%</span>
                            </div>
                            <ProgressBar value={enr.progress_pct} size="sm" color={enr.progress_pct >= 100 ? 'emerald' : 'amber'} />
                          </div>
                        ) : !comingSoon ? (
                          <div className="flex items-center gap-3 mb-3 text-xs text-ghost">
                            {course.estimated_hours && <span>{course.estimated_hours}h</span>}
                            {course.topic_count > 0 && (
                              <span>{course.topic_count} {t('course.topics')}</span>
                            )}
                          </div>
                        ) : null}

                        {enr ? (
                          <Link href={`/tools/${course.slug}`}>
                            <Button size="sm" variant={enr.progress_pct >= 100 ? 'ghost' : 'amber'} className="w-full">
                              {enr.progress_pct >= 100
                                ? <><CheckCircle size={12} /> {t('course.review')}</>
                                : <>{t('course.continue')} <ArrowRight size={12} className="rtl:rotate-180" /></>}
                            </Button>
                          </Link>
                        ) : comingSoon ? (
                          <Button size="sm" variant="outline" className="w-full" disabled>
                            {t('course.comingSoon')}
                          </Button>
                        ) : (
                          <Button
                            size="sm"
                            variant="outline"
                            className="w-full"
                            loading={enrollingId === course.id}
                            onClick={() => handleEnroll(course)}
                          >
                            {t('course.startLearning')}
                          </Button>
                        )}
                      </Card>
                    )
                  })}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </AppShell>
  )
}
