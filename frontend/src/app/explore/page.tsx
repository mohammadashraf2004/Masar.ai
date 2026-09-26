'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowRight, X } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { useLearningCatalog } from '@/hooks/useLearningCatalog'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { CourseCard } from '@/components/learning/CourseCard'
import { LearningLabel, useLabelContext } from '@/components/learning/LearningLabel'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { fieldLabel, levelLabel, roleLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { CatalogCourse } from '@/types'

function Chip({ pressed, onClick, children }: { pressed: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      aria-pressed={pressed}
      onClick={onClick}
      className={cn(
        'min-h-[44px] rounded-full border px-3.5 py-1.5 text-sm transition-colors lg:min-h-0',
        pressed
          ? 'border-amber/50 bg-amber/10 text-amber-text'
          : 'border-border bg-panel text-soft hover:border-muted hover:text-bright'
      )}
    >
      {children}
    </button>
  )
}

const toggle = (list: string[], slug: string) =>
  list.includes(slug) ? list.filter((s) => s !== slug) : [...list, slug]

/**
 * Explore: browse the learning system without committing to a path.
 *
 * Filters combine — any-of within a group, all-of across groups — and the
 * filtering happens on the server, so the catalogue is never downloaded to be
 * sifted here. "View path" appears once a level, a field and a career goal are
 * chosen: exactly the combination the path generator takes.
 */
export default function ExplorePage() {
  const { isLoading: authLoading } = useAuth()
  const { t } = useI18n()
  const ctx = useLabelContext()
  const { catalog, error } = useLearningCatalog()
  const [levels, setLevels] = useState<string[]>([])
  const [fields, setFields] = useState<string[]>([])
  const [goals, setGoals] = useState<string[]>([])
  const [courses, setCourses] = useState<CatalogCourse[] | null>(null)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    if (authLoading) return
    let stale = false // a slower earlier response must never overwrite a newer one
    api.listCatalogCourses({ level: levels, field: fields, career_goal: goals })
      .then((rows) => {
        if (stale) return
        setCourses(rows)
        setFailed(false)
      })
      .catch(() => !stale && setFailed(true))
    return () => {
      stale = true
    }
  }, [authLoading, levels, fields, goals])

  const canView = levels.length === 1 && fields.length >= 1 && goals.length === 1
  const anyFilter = levels.length + fields.length + goals.length > 0
  const viewHref = canView
    ? `/paths/custom?level=${levels[0]}&fields=${fields.join(',')}&goal=${goals[0]}`
    : null

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  return (
    <AppShell>
      <PageHeader title={t('nav.explore')} subtitle={t('explore.subtitle')} />
      <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-5xl space-y-8">
          {error || failed ? (
            <p role="alert" className="text-sm text-rose">{t('explore.loadError')}</p>
          ) : !catalog ? (
            <div className="flex justify-center py-12"><Spinner announce className="h-6 w-6" /></div>
          ) : (
            <>
              <section className="space-y-5" aria-label="Filters">
                <div>
                  <h2 className="mb-2 text-xs font-medium uppercase tracking-widest text-ghost">{t('explore.byLevel')}</h2>
                  <div className="flex flex-wrap gap-2">
                    {catalog.levels.map((l) => (
                      <Chip key={l.slug} pressed={levels.includes(l.slug)} onClick={() => setLevels(toggle(levels, l.slug))}>
                        <LearningLabel parts={levelLabel(l, ctx)} />
                      </Chip>
                    ))}
                  </div>
                </div>
                <div>
                  <h2 className="mb-2 text-xs font-medium uppercase tracking-widest text-ghost">{t('explore.byField')}</h2>
                  <div className="flex flex-wrap gap-2">
                    {catalog.fields.map((f) => (
                      <Chip key={f.slug} pressed={fields.includes(f.slug)} onClick={() => setFields(toggle(fields, f.slug))}>
                        <LearningLabel parts={fieldLabel(f, ctx, true)} />
                      </Chip>
                    ))}
                  </div>
                </div>
                <div>
                  <h2 className="mb-2 text-xs font-medium uppercase tracking-widest text-ghost">{t('explore.byCareer')}</h2>
                  <div className="flex flex-wrap gap-2">
                    {catalog.goals.map((g) => (
                      <Chip key={g.slug} pressed={goals.includes(g.slug)} onClick={() => setGoals(toggle(goals, g.slug))}>
                        <LearningLabel parts={roleLabel(g, ctx, true)} />
                      </Chip>
                    ))}
                  </div>
                </div>
              </section>

              <Card className="flex flex-wrap items-center justify-between gap-3 p-4">
                <p className="text-sm text-soft" aria-live="polite">
                  {canView ? t('explore.yourPath') : t('explore.pickAll')}
                </p>
                <div className="flex flex-wrap gap-2">
                  {anyFilter && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => { setLevels([]); setFields([]); setGoals([]) }}
                    >
                      <X size={12} /> {t('explore.reset')}
                    </Button>
                  )}
                  {viewHref ? (
                    <Link href={viewHref} className={buttonStyles({ size: 'sm' })}>
                      {t('explore.viewPath')} <ArrowRight size={12} className="rtl:rotate-180" />
                    </Link>
                  ) : (
                    <Button size="sm" disabled>{t('explore.viewPath')}</Button>
                  )}
                  <Link href="/paths" className={buttonStyles({ variant: 'ghost', size: 'sm' })}>
                    {t('explore.readyMade')}
                  </Link>
                </div>
              </Card>

              <section aria-label={t('explore.courses')}>
                <h2 className="mb-3 text-xs font-medium uppercase tracking-widest text-ghost">
                  {t('explore.courses')}{courses ? ` (${courses.length})` : ''}
                </h2>
                {!courses ? (
                  <div className="flex justify-center py-10"><Spinner announce /></div>
                ) : courses.length === 0 ? (
                  <p className="py-10 text-center text-sm text-ghost">{t('explore.noResults')}</p>
                ) : (
                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
                    {courses.map((c) => <CourseCard key={c.id} course={c} />)}
                  </div>
                )}
              </section>
            </>
          )}
        </div>
      </div>
    </AppShell>
  )
}
