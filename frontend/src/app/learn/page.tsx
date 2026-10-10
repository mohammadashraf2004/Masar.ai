'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowRight, Sparkles } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { useLearningCatalog } from '@/hooks/useLearningCatalog'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { CourseCatalog } from '@/components/learning/CourseCatalog'
import { LearningLabel, useLabelContext } from '@/components/learning/LearningLabel'
import { RecommendationGrid } from '@/components/learning/RecommendationGrid'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { roleLabel } from '@/lib/learning'
import type { LearningProfile, Recommendations } from '@/types'

const SECTION_TITLE = 'mb-3 text-base font-semibold text-bright'

/**
 * Learn: the front door to the courses, with no track or career goal required.
 *
 *   Your learning        the courses you are in
 *   Recommended for you  what to take next, each with the reason
 *   Explore courses      every published course
 *   Career roadmaps      guidance, not gates
 *
 * Recommendations are computed by the server from real progress and readiness;
 * a learner who has chosen nothing still gets a sensible list, and any course can
 * be opened and enrolled in from the catalogue below regardless of it.
 */
export default function LearnHubPage() {
  const { isLoading: authLoading } = useAuth()
  const { t } = useI18n()
  const ctx = useLabelContext()
  const { catalog } = useLearningCatalog()
  const [recs, setRecs] = useState<Recommendations | null>(null)
  const [profile, setProfile] = useState<LearningProfile | null>(null)
  const [failed, setFailed] = useState(false)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    if (authLoading) return
    let alive = true
    api.getRecommendations()
      .then((r) => alive && (setRecs(r), setFailed(false)))
      .catch(() => alive && setFailed(true))
    // Only used to offer "personalise": its failure must not hide the courses.
    api.getMyLearningProfile().then((p) => alive && setProfile(p)).catch(() => {})
    return () => {
      alive = false
    }
  }, [authLoading, attempt])

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  const yourLearning = recs?.continue_learning ?? []
  const recommended = recs?.recommended_next ?? []
  const foundations = recs?.build_foundations ?? []
  const completed = recs?.completed ?? []

  return (
    <AppShell>
      <PageHeader title={t('hub.title')} contained />
      <PageBody>
        <div className="space-y-10">
          {profile && !profile.onboarding_completed && (
            <Card className="flex flex-wrap items-center justify-between gap-3 border-amber/20 p-4">
              <div className="max-w-xl">
                <p className="flex items-center gap-2 text-sm font-medium text-bright">
                  <Sparkles size={14} className="text-amber-text" aria-hidden="true" />
                  {t('hub.personalize.title')}
                </p>
                <p className="mt-1 text-xs text-soft">{t('hub.personalize.body')}</p>
              </div>
              <Link href="/onboarding/quick" className={buttonStyles({ size: 'sm' })}>
                {t('hub.personalize.cta')}
              </Link>
            </Card>
          )}

          {failed ? (
            <Card className="p-8 text-center">
              <p role="alert" className="mb-4 text-sm text-rose">{t('hub.loadError')}</p>
              <Button variant="ghost" onClick={() => setAttempt((n) => n + 1)}>{t('common.retry')}</Button>
            </Card>
          ) : !recs ? (
            <div className="flex justify-center py-10"><Spinner announce className="h-6 w-6" /></div>
          ) : (
            <>
              <section aria-labelledby="hub-learning">
                <div className="flex flex-wrap items-baseline justify-between gap-2">
                  <h2 id="hub-learning" className={SECTION_TITLE}>{t('hub.yourLearning')}</h2>
                  {yourLearning.length > 0 && (
                    <Link href="/learn/my-courses" className="mb-3 text-xs text-amber-text hover:text-amber-text2">
                      {t('nav.myCourses')}
                    </Link>
                  )}
                </div>
                {yourLearning.length > 0 ? (
                  <RecommendationGrid items={yourLearning} />
                ) : (
                  <p className="text-sm text-soft">{t('hub.yourLearning.empty')}</p>
                )}
              </section>

              <section aria-labelledby="hub-recommended">
                <h2 id="hub-recommended" className={SECTION_TITLE}>{t('hub.recommended')}</h2>
                {recommended.length > 0 ? (
                  <RecommendationGrid items={recommended} />
                ) : (
                  <p className="text-sm text-soft">{t('hub.recommended.empty')}</p>
                )}
              </section>

              {foundations.length > 0 && (
                <section aria-labelledby="hub-foundations">
                  <h2 id="hub-foundations" className={SECTION_TITLE}>{t('hub.foundations')}</h2>
                  <RecommendationGrid items={foundations} />
                </section>
              )}
            </>
          )}

          <section aria-labelledby="hub-explore">
            <h2 id="hub-explore" className={SECTION_TITLE}>{t('hub.explore')}</h2>
            <CourseCatalog />
          </section>

          <section aria-labelledby="hub-roadmaps">
            <h2 id="hub-roadmaps" className={SECTION_TITLE}>{t('hub.roadmaps')}</h2>
            <p className="mb-4 max-w-3xl text-sm text-soft">{t('hub.roadmaps.blurb')}</p>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {(catalog?.goals ?? []).map((goal) => (
                <Link key={goal.slug} href={`/roadmaps/${goal.slug}`} className="block">
                  <Card glow className="h-full p-4">
                    <p className="text-sm font-medium text-bright"><LearningLabel parts={roleLabel(goal, ctx)} /></p>
                    <p className="mt-3 inline-flex items-center gap-1 text-xs text-amber-text">
                      {t('hub.roadmaps.open')} <ArrowRight size={11} className="rtl:rotate-180" aria-hidden="true" />
                    </p>
                  </Card>
                </Link>
              ))}
            </div>
            {profile?.has_active_path && (
              <p className="mt-4 text-sm">
                <Link href="/learn/masar" className="text-amber-text hover:text-amber-text2">{t('hub.yourMasar')}</Link>
              </p>
            )}
          </section>

          {completed.length > 0 && (
            <section aria-labelledby="hub-completed">
              <h2 id="hub-completed" className={SECTION_TITLE}>{t('hub.completed')}</h2>
              <RecommendationGrid items={completed} />
            </section>
          )}
        </div>
      </PageBody>
    </AppShell>
  )
}
