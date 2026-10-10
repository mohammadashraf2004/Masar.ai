'use client'
import { useEffect, useId, useRef, useState } from 'react'
import Link from 'next/link'
import { AlertTriangle, Plus } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { buttonStyles } from '@/components/ui/Button'
import { LOW_CREDITS, useCreditBalance } from '@/components/layout/WalletContext'

/** Where credits are bought: the Buy credits page. */
export const ADD_CREDITS_HREF = '/billing/credits'

/**
 * The credit balance as a pill in the header: a 7px amber dot and the number in
 * mono, turning to a rose warning below LOW_CREDITS. Pressing it opens a small
 * panel with the balance, what credits are for, and an Add credits button that
 * goes to the packs on the billing page. Renders nothing until the balance is
 * known.
 */
export function CreditsBadge({ className }: { className?: string }) {
  const { t, tf } = useI18n()
  const balance = useCreditBalance()
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)
  const trigger = useRef<HTMLButtonElement>(null)
  const panelId = useId()

  // Close on outside click, or on Escape (handing focus back to the pill).
  useEffect(() => {
    if (!open) return
    const onMouseDown = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Escape') return
      setOpen(false)
      trigger.current?.focus()
    }
    document.addEventListener('mousedown', onMouseDown)
    document.addEventListener('keydown', onKeyDown)
    return () => {
      document.removeEventListener('mousedown', onMouseDown)
      document.removeEventListener('keydown', onKeyDown)
    }
  }, [open])

  if (balance === null) return null
  const low = balance < LOW_CREDITS

  return (
    <div className={cn('relative', className)} ref={ref}>
      <button
        ref={trigger}
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        aria-controls={open ? panelId : undefined}
        // The number alone says nothing to a screen reader.
        aria-label={tf('nav.creditsAria', { n: balance })}
        title={low ? t('nav.creditsLow') : t('nav.creditsBalance')}
        className={cn(
          'inline-flex min-h-[44px] items-center gap-2 rounded-full border px-3 font-mono text-xs transition-colors lg:h-[34px] lg:min-h-0',
          low
            ? 'border-rose/30 bg-rose/10 text-rose hover:bg-rose/20'
            : 'border-border bg-surface text-white hover:border-amber/30',
          open && !low && 'border-amber/30',
        )}
      >
        {low
          ? <AlertTriangle size={12} className="shrink-0" aria-hidden="true" />
          : <span className="h-[7px] w-[7px] shrink-0 rounded-full bg-amber" aria-hidden="true" />}
        <span>{balance.toLocaleString('en-US')}</span>
      </button>

      {open && (
        <div
          id={panelId}
          role="dialog"
          aria-label={t('nav.creditsBalance')}
          className="absolute end-0 top-full z-50 mt-2 w-64 max-w-[calc(100vw-2rem)] overflow-hidden rounded-xl border border-border bg-ink shadow-2xl"
        >
          <div className="px-4 pb-3 pt-3.5">
            <p className="text-xs font-medium text-ghost">{t('nav.creditsBalance')}</p>
            <p className="mt-1 flex items-baseline gap-1.5">
              <span className={cn('font-mono text-2xl font-semibold', low ? 'text-rose' : 'text-bright')}>
                {balance.toLocaleString('en-US')}
              </span>
              <span className="text-xs text-soft">{t('nav.credits')}</span>
            </p>
            <p className={cn('mt-2 text-xs leading-snug', low ? 'text-rose' : 'text-soft')}>
              {low ? t('nav.creditsPanel.low') : t('nav.creditsPanel.info')}
            </p>
          </div>
          <div className="border-t border-border p-3">
            <Link
              href={ADD_CREDITS_HREF}
              onClick={() => setOpen(false)}
              className={buttonStyles({ variant: 'amber', size: 'sm', className: 'w-full' })}
            >
              <Plus size={14} aria-hidden="true" />
              {t('nav.addCredits')}
            </Link>
          </div>
        </div>
      )}
    </div>
  )
}
