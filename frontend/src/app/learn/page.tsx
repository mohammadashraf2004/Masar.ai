'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { RefreshCw, SlidersHorizontal } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { useLearningCatalog } from '@/hooks/useLearningCatalog'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { AdvisoryList, MasarSummary, PathRoadmap } from '@/components/learning/PathRoadmap'
import { SkillGapsPanel } from '@/components/learning/SkillGapsPanel'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card, EmptyState, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import type { LearningPath } from '@/types'

type View =
  | { kind: 'loading' }
  | { kind: 'error' }
  | { kind: 'empty' }
  | { kind: 'path'; path: LearningPath }

/**
 * Your Masar: the learner's personalised path.
 *
 * Every number and every state on this screen — which stage is current, what
 * each percentage is, which courses are optional — is decided by the server and
 * only displayed here. A learner who has not finished onboarding is sent there
 * first, which is how a migrated account is asked for the new answers.
 */
export default function LearnPage() {
  const { isLoading: authLoading } = useAuth()
  const router = useRouter()
  const { t } = useI18n()
  const { catalog } = useLearningCatalog()
  const [view, setView] = useState<View>({ kind: 'loading' })
  const [rebuilding, setRebuilding] = useState(false)

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
        const path = await api.getMyLearningPath()
        if (alive) setView(path ? { kind: 'path', path } : { kind: 'empty' })
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

  async function rebuild() {
    setRebuilding(true)
    try {
      setView({ kind: 'path', path: await api.saveMyLearningPath({ regenerate: true }) })
    } catch {
      setView({ kind: 'error' })
    }
    setRebuilding(false)
  }

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  return (
    <AppShell>
      <PageHeader title={t('learn.title')} />
      <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl space-y-6">
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
            <Card>
              <EmptyState
                title={t('learn.emptyTitle')}
                description={t('learn.emptyBody')}
                action={
                  <Button loading={rebuilding} onClick={() => void rebuild()}>
                    {t('onb.build.cta')}
                  </Button>
                }
              />
            </Card>
          )}

          {view.kind === 'path' && (
            <>
              <MasarSummary
                path={view.path}
                actions={
                  <>
                    <Button variant="ghost" size="sm" loading={rebuilding} onClick={() => void rebuild()}>
                      <RefreshCw size={12} aria-hidden="true" /> {t('learn.rebuild')}
                    </Button>
                    <Link href="/profile/learning" className={buttonStyles({ variant: 'ghost', size: 'sm' })}>
                      <SlidersHorizontal size={12} aria-hidden="true" /> {t('learn.editAnswers')}
                    </Link>
                  </>
                }
              />
              <SkillGapsPanel variant="roadmap" reloadKey={view.path.id ?? 0} />
              <AdvisoryList path={view.path} catalogFields={catalog?.fields} />
              <PathRoadmap path={view.path} />
            </>
          )}
        </div>
      </div>
    </AppShell>
  )
}
