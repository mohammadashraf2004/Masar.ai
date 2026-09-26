'use client'
import Link from 'next/link'
import { AlertTriangle } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { LOW_CREDITS, useCreditBalance } from '@/components/layout/WalletContext'

/**
 * The credit balance as a pill in the header: a 7px amber dot and the number in
 * mono. It links to Plans & offers, where credits are topped up, and turns to a
 * rose warning below LOW_CREDITS. Renders nothing until the balance is known.
 */
export function CreditsBadge({ className }: { className?: string }) {
  const { t, tf } = useI18n()
  const balance = useCreditBalance()

  if (balance === null) return null
  const low = balance < LOW_CREDITS

  return (
    <Link
      href="/billing"
      // The number alone says nothing to a screen reader.
      aria-label={tf('nav.creditsAria', { n: balance })}
      title={low ? t('nav.creditsLow') : t('nav.creditsBalance')}
      className={cn(
        'inline-flex min-h-[44px] items-center gap-2 rounded-full border px-3 font-mono text-xs transition-colors lg:h-[34px] lg:min-h-0',
        low
          ? 'border-rose/30 bg-rose/10 text-rose hover:bg-rose/20'
          : 'border-border bg-surface text-white hover:border-amber/30',
        className,
      )}
    >
      {low
        ? <AlertTriangle size={12} className="shrink-0" aria-hidden="true" />
        : <span className="h-[7px] w-[7px] shrink-0 rounded-full bg-amber" aria-hidden="true" />}
      <span>{balance.toLocaleString('en-US')}</span>
    </Link>
  )
}
