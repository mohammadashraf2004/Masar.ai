'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Award, SlidersHorizontal } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { TrackWorkflowPath } from '@/components/learning/TrackWorkflowPath'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import type { RoleRef } from '@/types'

type View =
  | { kind: 'loading' }
  | { kind: 'error' }
  | { kind: 'empty' }
  | { kind: 'workflow'; careerGoal: RoleRef }

/**
 * Your Masar: the learner's server-owned career-track workflow.
 *
 * Course ordering, roles, progress and availability all come from the canonical
 * track workflow endpoint. The retired generated "Your Learning Path" view is
 * intentionally not fetched or rendered here.
 */
export default function MasarPage() {
  const { isLoading: authLoading } = useAuth()
  const router = useRouter()
  const { t } = useI18n()
  const [view, setView] = useState<View>({ kind: 'loading' })

  // Bumped by "try again" to re-run the load below.
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    if (authLoading) return
    let alive = true
    ;(async () => {
      try {
        const profile = await api.getMyLearningProfile()
        if (!alive) return
        if (profile.needs_onboarding) {
          router.replace('/onboarding/learning-profile')
          return
        }
        if (alive) {
          setView(profile.career_goal
            ? { kind: 'workflow', careerGoal: profile.career_goal }
            : { kind: 'empty' })
        }
      } catch {
        if (alive) setView({ kind: 'error' })
      }
    })()
    return () => {
      alive = false
    }
  }, [authLoading, router, attempt])

  function retry() {
    setView({ kind: 'loading' })
    setAttempt((n) => n + 1)
  }

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  return (
    <AppShell>
      <PageHeader title={t('learn.title')} contained />
      <PageBody>
        <div className="space-y-6">
          {view.kind === 'loading' && (
            <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>
          )}

          {view.kind === 'error' && (
            <Card className="p-8 text-center">
              <p role="alert" className="mb-4 text-sm text-rose">{t('learn.loadError')}</p>
              <Button variant="ghost" onClick={retry}>{t('common.retry')}</Button>
            </Card>
          )}

          {view.kind === 'empty' && (
            <Card className="p-8 text-center">
              <p className="mb-4 text-sm text-ghost">{t('learn.emptyBody')}</p>
              <Link href="/profile/learning" className={buttonStyles()}>{t('onb.build.cta')}</Link>
            </Card>
          )}

          {view.kind === 'workflow' && (
            <>
              <div className="flex flex-wrap justify-end gap-2">
                <Link href="/profile/learning" className={buttonStyles({ variant: 'ghost', size: 'sm' })}>
                  <SlidersHorizontal size={12} aria-hidden="true" /> {t('learn.editAnswers')}
                </Link>
                <Link href="/certificates" className={buttonStyles({ variant: 'ghost', size: 'sm' })}>
                  <Award size={12} aria-hidden="true" /> {t('nav.certificates')}
                </Link>
              </div>
              <TrackWorkflowPath goal={view.careerGoal.slug} />
            </>
          )}
        </div>
      </PageBody>
    </AppShell>
  )
}
