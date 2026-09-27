'use client'
import Link from 'next/link'
import { Linkedin } from 'lucide-react'
import { useI18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'
import { Logo } from '@/components/layout/Logo'

/** The site-wide legal bar. It stays in normal flow at the end of a page's scroller. */
export function LegalFooter({ className }: { className?: string }) {
  const { t } = useI18n()
  const year = new Date().getFullYear()
  const link = 'text-xs text-dim no-underline transition-colors hover:text-amber-text focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring'

  return (
    <footer
      aria-label={t('footer.aria')}
      className={cn('mt-auto flex-none pt-12', className)}
    >
      <div className="flex justify-center border-t border-border pb-[18px] pt-[22px]">
        <Logo size={24} className="gap-2" wordmarkClassName="text-[15px] text-white" />
      </div>
      <div className="flex flex-wrap items-center justify-between gap-x-6 gap-y-2.5">
        <div className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-ghost">
          <span dir="ltr" className="font-mono text-[11px]">© {year} Masar Inc.</span>
          <span>{t('footer.copyright')}</span>
        </div>
        <nav aria-label={t('footer.aria')} className="flex flex-wrap gap-x-[18px] gap-y-1">
          <Link href="/terms" className={link}>{t('legal.footer.terms')}</Link>
          <Link href="/privacy" className={link}>{t('legal.footer.privacy')}</Link>
          <a
            href="https://www.linkedin.com/company/masarai-learning"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LinkedIn"
            className={cn(link, 'inline-flex items-center')}
          >
            <Linkedin size={14} aria-hidden="true" />
          </a>
        </nav>
      </div>
    </footer>
  )
}
