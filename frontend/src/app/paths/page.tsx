'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowRight } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { LearningLabel, useLabelContext } from '@/components/learning/LearningLabel'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { fieldLabel, levelLabel, roleLabel } from '@/lib/learning'
import type { PathSummary } from '@/types'

/**
 * The journeys the configuration defines: one per career goal — its shared core
 * — and one per specialisation route. The list is derived by the backend from
 * the path templates, so a route added there appears here untouched.
 */
export default function PathsPage() {
  const { isLoading: authLoading } = useAuth()
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  const [paths, setPaths] = useState<PathSummary[] | null>(null)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    if (authLoading) return
    api.listLearningPaths().then(setPaths).catch(() => setFailed(true))
  }, [authLoading])

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  // Group by career goal, keeping the server's order.
  const groups: Array<{ goal: PathSummary['career_goal']; items: PathSummary[] }> = []
  for (const p of paths ?? []) {
    const group = groups.find((g) => g.goal.slug === p.career_goal.slug)
    if (group) group.items.push(p)
    else groups.push({ goal: p.career_goal, items: [p] })
  }

  return (
    <AppShell>
      <PageHeader title={t('paths.title')} subtitle={t('paths.subtitle')} />
      <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-5xl space-y-8">
          {failed ? (
            <p role="alert" className="text-sm text-rose">{t('explore.loadError')}</p>
          ) : !paths ? (
            <div className="flex justify-center py-12"><Spinner announce className="h-6 w-6" /></div>
          ) : (
            groups.map(({ goal, items }) => (
              <section key={goal.slug} aria-label={goal.title}>
                <h2 className="mb-3 text-sm font-semibold text-bright">
                  <LearningLabel parts={roleLabel(goal, ctx)} />
                </h2>
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {items.map((p) => (
                    <Link key={p.slug} href={`/paths/${p.slug}`} className="block">
                      <Card glow className="h-full p-4">
                        <p className="text-sm font-medium text-bright">
                          {p.field ? <LearningLabel parts={fieldLabel(p.field, ctx)} /> : t('paths.core')}
                        </p>
                        <p className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-xs text-ghost">
                          <span>{p.stage_count} {t('paths.stages')}</span>
                          <span>{tf('learn.courses.many', { n: p.available_course_count })}</span>
                          {p.estimated_hours > 0 && <span>{tf('card.hours', { n: Math.round(p.estimated_hours) })}</span>}
                        </p>
                        {p.recommended_level && (
                          <p className="mt-2 text-xs text-dim">
                            {t('paths.recommendedLevel')}: <LearningLabel parts={levelLabel(p.recommended_level, ctx)} />
                          </p>
                        )}
                        <p className="mt-3 inline-flex items-center gap-1 text-xs text-amber">
                          {t('paths.openPath')} <ArrowRight size={11} className="rtl:rotate-180" />
                        </p>
                      </Card>
                    </Link>
                  ))}
                </div>
              </section>
            ))
          )}
        </div>
      </div>
    </AppShell>
  )
}
