'use client'
import { useRouter } from 'next/navigation'
import { ArrowLeft, ArrowRight } from 'lucide-react'
import { Logo } from '@/components/layout/Logo'
import { LanguageSwitcher } from '@/components/ui/LanguageSwitcher'
import { useI18n } from '@/lib/i18n'

/**
 * The top bar of the focused onboarding pages: a back arrow, the logo, and the
 * language control. It spans the page column (`w-full`): inside a flex column,
 * `mx-auto` alone would shrink it to its content and push the logo against the
 * language button.
 */
export function OnboardingHeader() {
  const router = useRouter()
  const { t, isRtl } = useI18n()
  const Arrow = isRtl ? ArrowRight : ArrowLeft

  // A learner who landed here directly has no page to go back to; send them home.
  const goBack = () => {
    if (window.history.length > 1) router.back()
    else router.push('/')
  }

  return (
    <div className="mx-auto mb-8 flex w-full max-w-2xl items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={goBack}
          aria-label={t('onb.back')}
          title={t('onb.back')}
          className="-ms-2 inline-flex min-h-[44px] min-w-[44px] items-center justify-center rounded-md text-dim transition-colors hover:bg-surface hover:text-bright lg:min-h-[32px] lg:min-w-[32px]"
        >
          <Arrow size={18} aria-hidden="true" className="shrink-0" />
        </button>
        <Logo size={28} wordmarkClassName="text-sm" />
      </div>
      <LanguageSwitcher />
    </div>
  )
}
