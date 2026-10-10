'use client'
import { useRouter } from 'next/navigation'
import { useAuth, useNextParam } from '@/hooks/useAuth'
import { useLearningCatalog } from '@/hooks/useLearningCatalog'
import { OnboardingHeader } from '@/components/layout/OnboardingHeader'
import { LegalFooter } from '@/components/layout/LegalFooter'
import { QuickOnboarding } from '@/components/learning/QuickOnboarding'
import { Button } from '@/components/ui/Button'
import { Spinner } from '@/components/ui/index'
import { useI18n } from '@/lib/i18n'

/**
 * The short first-time questions, on a focused page with no sidebar (like the
 * other onboarding page). Finishing or skipping both land on Explore: a learner never
 * has to answer these, or choose a career track, to start any course.
 */
export default function QuickOnboardingPage() {
  const { isLoading: authLoading } = useAuth()
  const router = useRouter()
  const { t } = useI18n()
  const { catalog, error } = useLearningCatalog()
  // A new account that signed up from "sign in to continue" goes back there.
  const next = useNextParam()
  const done = () => router.replace(next ?? '/explore')

  return (
    <div className="flex min-h-dvh flex-col bg-void px-4 pt-8 pb-[calc(1.25rem+env(safe-area-inset-bottom))] sm:px-6">
      <OnboardingHeader />
      <div className="flex-1">
        {error ? (
          <div className="mx-auto max-w-2xl text-center">
            <p role="alert" className="mb-4 text-sm text-rose">{t('onb.loadError')}</p>
            <Button variant="ghost" onClick={() => window.location.reload()}>{t('common.retry')}</Button>
          </div>
        ) : authLoading || !catalog ? (
          <div className="flex justify-center py-24"><Spinner announce className="h-6 w-6" /></div>
        ) : (
          <QuickOnboarding fields={catalog.fields} onDone={done} onSkip={done} />
        )}
      </div>
      <LegalFooter className="mx-auto w-full max-w-2xl" />
    </div>
  )
}
