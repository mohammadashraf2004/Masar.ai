'use client'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { useLearningCatalog } from '@/hooks/useLearningCatalog'
import { Logo } from '@/components/layout/Logo'
import { LanguageSwitcher } from '@/components/ui/LanguageSwitcher'
import { QuickOnboarding } from '@/components/learning/QuickOnboarding'
import { Button } from '@/components/ui/Button'
import { Spinner } from '@/components/ui/index'
import { useI18n } from '@/lib/i18n'

/**
 * The short first-time questions, on a focused page with no sidebar (like the
 * other onboarding page). Finishing or skipping both land on Learn: a learner never
 * has to answer these, or choose a career track, to start any course.
 */
export default function QuickOnboardingPage() {
  const { isLoading: authLoading } = useAuth()
  const router = useRouter()
  const { t } = useI18n()
  const { catalog, error } = useLearningCatalog()

  return (
    <div className="min-h-dvh bg-void px-4 py-8 sm:px-6">
      <div className="mx-auto mb-8 flex max-w-2xl items-center justify-between">
        <Logo size={28} wordmarkClassName="text-sm" />
        <LanguageSwitcher />
      </div>
      {error ? (
        <div className="mx-auto max-w-2xl text-center">
          <p role="alert" className="mb-4 text-sm text-rose">{t('onb.loadError')}</p>
          <Button variant="ghost" onClick={() => window.location.reload()}>{t('common.retry')}</Button>
        </div>
      ) : authLoading || !catalog ? (
        <div className="flex justify-center py-24"><Spinner announce className="h-6 w-6" /></div>
      ) : (
        <QuickOnboarding fields={catalog.fields} onDone={() => router.replace('/learn')} onSkip={() => router.replace('/learn')} />
      )}
    </div>
  )
}
