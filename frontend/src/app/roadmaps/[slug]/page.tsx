'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { useSession } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { CourseCard } from '@/components/learning/CourseCard'
import { LearningLabel, useLabelContext } from '@/components/learning/LearningLabel'
import { buttonStyles } from '@/components/ui/Button'
import { Badge, Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { pick } from '@/lib/content-language'
import { useI18n, type StringKey } from '@/lib/i18n'
import { labelText, roleLabel } from '@/lib/learning'
import type { TrackDetail } from '@/types'

/**
 * A career roadmap: the courses we recommend for a role, in order. It is guidance
 * only. Each course here is the same canonical course the catalogue lists (there
 * is no per-roadmap copy), and any of them can be opened and enrolled in without
 * following the order, or without this roadmap at all.
 */
export default function RoadmapPage() {
  // Public: a roadmap is something to explore before signing up.
  const { isLoading: authLoading } = useSession()
  const { slug } = useParams() as { slug: string }
  const { t, tf, language } = useI18n()
  const ctx = useLabelContext()
  const [roadmap, setRoadmap] = useState<TrackDetail | null>(null)
  const [state, setState] = useState<'loading' | 'ready' | 'missing' | 'error'>('loading')

  useEffect(() => {
    if (authLoading) return
    let alive = true
    api.getCareerRoadmap(slug)
      .then((r) => alive && (setRoadmap(r), setState('ready')))
      .catch((err: { response?: { status?: number } }) => alive && setState(err?.response?.status === 404 ? 'missing' : 'error'))
    return () => {
      alive = false
    }
  }, [authLoading, slug])

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  const title = roadmap ? labelText(roleLabel(roadmap, ctx)) : t('rm.title')
  const description = roadmap ? pick(roadmap.description, roadmap.description_ar, language) : ''

  return (
    <AppShell>
      <PageHeader title={title} dirAuto contained />
      <PageBody>
        {state === 'loading' && <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>}
        {(state === 'missing' || state === 'error') && (
          <Card className="space-y-3 p-8 text-center">
            <p role="alert" className="text-sm text-rose">{t('rm.loadError')}</p>
            <Link href="/explore" className={buttonStyles({ variant: 'ghost', size: 'sm' })}>{t('nav.explore')}</Link>
          </Card>
        )}
        {state === 'ready' && roadmap && (
          <div className="space-y-6">
            <div className="max-w-3xl space-y-2">
              <p className="text-sm text-bright">
                {tf('rm.intro', { role: labelText(roleLabel(roadmap, ctx)) })}
              </p>
              {description && <p className="text-sm text-soft" dir="auto">{description}</p>}
              <p className="text-xs text-soft">{t('rm.note')}</p>
              <Link href="/tracks" className="inline-block text-xs text-amber-text hover:text-amber-text2">{t('rm.seePaths')}</Link>
            </div>

            {roadmap.courses.length === 0 ? (
              <p className="py-10 text-center text-sm text-ghost">{t('rm.empty')}</p>
            ) : (
              <ol className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
                {roadmap.courses.map((entry) => (
                  <li key={entry.course.id} className="flex flex-col gap-2">
                    <p className="flex items-center justify-between gap-2 text-xs text-soft">
                      <span>{tf('rm.step', { n: entry.position })}</span>
                      <Badge variant={entry.track_role === 'core' ? 'amber' : 'ghost'}>
                        {t(`card.role.${entry.track_role}` as StringKey)}
                      </Badge>
                    </p>
                    <CourseCard course={entry.course} className="flex-1" />
                  </li>
                ))}
              </ol>
            )}
          </div>
        )}
      </PageBody>
    </AppShell>
  )
}
