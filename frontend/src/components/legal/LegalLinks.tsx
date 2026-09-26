'use client'
import Link from 'next/link'
import { useI18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'

/**
 * "Terms · Privacy" — the footer links every public surface carries (home,
 * sign-in, sign-up, the sidebar), so the documents are one click away whether
 * or not someone has an account. Each is a real link to a real page.
 */
export function LegalLinks({ className }: { className?: string }) {
  const { t } = useI18n()
  const link =
    'inline-flex min-h-[44px] items-center text-xs text-soft underline-offset-2 hover:text-bright hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring lg:min-h-0'
  return (
    <nav aria-label={`${t('legal.footer.terms')} / ${t('legal.footer.privacy')}`} className={cn('flex items-center gap-4', className)}>
      <Link href="/terms" className={link}>{t('legal.footer.terms')}</Link>
      <Link href="/privacy" className={link}>{t('legal.footer.privacy')}</Link>
    </nav>
  )
}
