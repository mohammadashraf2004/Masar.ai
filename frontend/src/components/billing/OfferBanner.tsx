'use client'
import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/Button'
import { useI18n } from '@/lib/i18n'
import type { Offer } from '@/lib/billing/types'

export type PromoError = 'invalid' | 'expired' | 'unavailable'

/** The current time, refreshed on an interval, for a countdown that has to move. */
function useNow(everyMs: number): number {
  const [now, setNow] = useState(() => Date.now())
  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), everyMs)
    return () => clearInterval(id)
  }, [everyMs])
  return now
}

/** Days, hours and minutes left, each at least two digits. */
export function timeLeft(endsAt: string, now: number) {
  const ms = Math.max(0, Date.parse(endsAt) - now)
  const minutes = Math.floor(ms / 60_000)
  return {
    over: ms === 0,
    days: Math.floor(minutes / 1440),
    hours: Math.floor((minutes % 1440) / 60),
    minutes: minutes % 60,
  }
}

const pad = (n: number) => String(n).padStart(2, '0')

/**
 * The limited-offer banner: what it is, a live countdown to when it ends, and the code with
 * a button that applies it (and, applied, removes it again). The code is checked by the
 * server (the `onToggle` the page passes goes to the catalog), never by this component.
 */
export function OfferBanner({
  offer, applied, checking, error, onToggle,
}: {
  offer: Offer
  applied: boolean
  checking: boolean
  error: PromoError | null
  onToggle: () => void
}) {
  const { t, tf } = useI18n()
  const left = timeLeft(offer.endsAt, useNow(1000))

  const units: Array<[string, string]> = [
    [pad(left.days), t('billing.unit.days')],
    [pad(left.hours), t('billing.unit.hours')],
    [pad(left.minutes), t('billing.unit.minutes')],
  ]

  return (
    <section
      aria-label={tf('billing.offer.title', { pct: offer.percent })}
      className="flex flex-wrap items-center gap-5 rounded-xl border border-amber bg-surface px-[22px] py-5"
      style={{ backgroundImage: 'radial-gradient(80% 140% at 0% 50%, rgb(var(--acc) / var(--acc-soft-a)), transparent 65%)' }}
    >
      <div className="flex min-w-[300px] flex-[2_1_300px] flex-col gap-1.5">
        <span className="font-mono text-[11px] tracking-[0.14em] text-amber-text">{t('billing.offer.eyebrow')}</span>
        <h2 className="text-[17px] font-bold text-white">{tf('billing.offer.title', { pct: offer.percent })}</h2>
        <p className="text-[13px] text-dim">
          {left.over ? t('billing.offer.expired') : t('billing.offer.sub')}
        </p>
      </div>

      {!left.over && (
        <div
          dir="ltr"
          role="timer"
          aria-label={tf('billing.offer.countdown', { d: left.days, h: left.hours, m: left.minutes })}
          className="flex gap-2"
        >
          {units.map(([value, unit]) => (
            <div key={unit} aria-hidden="true" className="flex w-[58px] flex-col items-center gap-0.5 rounded-lg border border-border bg-panel py-2">
              <span className="font-mono text-xl font-medium text-white">{value}</span>
              <span className="text-[10px] text-ghost">{unit}</span>
            </div>
          ))}
        </div>
      )}

      <div className="flex flex-col items-start gap-1.5">
        <div className="flex items-center gap-2">
          <span dir="ltr" className="rounded-lg border border-dashed border-amber px-3.5 py-2.5 font-mono text-sm tracking-[0.1em] text-amber-text">
            {offer.code}
          </span>
          <Button
            variant={applied ? 'ghost' : 'amber'}
            aria-pressed={applied}
            loading={checking}
            disabled={left.over && !applied}
            onClick={onToggle}
            className={applied ? 'border-emerald text-emerald hover:border-emerald hover:text-emerald' : undefined}
          >
            {applied ? t('billing.promo.applied') : t('billing.promo.apply')}
          </Button>
        </div>
        {error && <p role="alert" className="text-xs text-rose">{t(`billing.promo.${error}`)}</p>}
      </div>
    </section>
  )
}
