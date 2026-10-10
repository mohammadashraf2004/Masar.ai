'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { useLearningCatalog } from '@/hooks/useLearningCatalog'
import { OnboardingHeader } from '@/components/layout/OnboardingHeader'
import { LegalFooter } from '@/components/layout/LegalFooter'
import { OnboardingFlow, type OnboardingAnswers } from '@/components/learning/OnboardingFlow'
import { Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { labelText, roleLabel } from '@/lib/learning'
import type { LearningProfile } from '@/types'

/**
 * Onboarding is a focused flow, so it has no sidebar — like the sign-in pages.
 *
 * A learner arriving from the old role-based experience may already have a
 * career goal (carried over from their enrolment) and nothing else. That goal is
 * pre-selected and named; level and fields are left empty for them to answer,
 * never guessed.
 */
export default function LearningOnboardingPage() {
  const { isLoading: authLoading } = useAuth()
  const router = useRouter()
  const { t, tf, language, mode } = useI18n()
  const { catalog, error } = useLearningCatalog()
  const [profile, setProfile] = useState<LearningProfile | null>(null)
  const [profileLoaded, setProfileLoaded] = useState(false)

  useEffect(() => {
    if (authLoading) return
    api.getMyLearningProfile()
      .then(setProfile)
      .catch(() => {})
      .finally(() => setProfileLoaded(true))
  }, [authLoading])

  const ready = !authLoading && catalog && profileLoaded

  const initial: Partial<OnboardingAnswers> = {
    level: profile?.level?.slug ?? null,
    fields: profile?.fields.map((f) => f.slug) ?? [],
    goal: profile?.career_goal?.slug ?? null,
    skills: profile?.known_skills.map((s) => s.slug) ?? [],
  }
  const carriedGoal =
    profile?.source === 'migrated' && profile.career_goal
      ? labelText(roleLabel(profile.career_goal, { language, mode }))
      : null

  return (
    <div className="flex min-h-dvh flex-col bg-void px-4 pt-8 pb-[calc(1.25rem+env(safe-area-inset-bottom))] sm:px-6">
      <OnboardingHeader />

      <div className="flex-1">
        {error ? (
          <div className="mx-auto max-w-2xl text-center">
            <p role="alert" className="mb-4 text-sm text-rose">{t('onb.loadError')}</p>
            <Button variant="ghost" onClick={() => window.location.reload()}>{t('common.retry')}</Button>
          </div>
        ) : !ready ? (
          <div className="flex justify-center py-24"><Spinner announce className="h-6 w-6" /></div>
        ) : (
          <>
            {carriedGoal && (
              <p className="mx-auto mb-4 max-w-2xl rounded-md border border-sky/20 bg-sky/5 px-3 py-2.5 text-xs text-soft">
                {tf('banner.onboard.carried', { goal: carriedGoal })}
              </p>
            )}
            <OnboardingFlow catalog={catalog} initial={initial} onDone={() => router.replace('/learn/masar')} />
          </>
        )}
      </div>
      <LegalFooter className="mx-auto w-full max-w-2xl" />
    </div>
  )
}
