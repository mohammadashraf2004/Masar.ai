'use client'
import { useEffect, useState } from 'react'
import { Sparkles } from 'lucide-react'
import { api, type AiAllowance } from '@/lib/api'
import { useI18n } from '@/lib/i18n'

/**
 * Pro's included AI credits: how many are left in the rolling 4-hour window and, once they
 * are used up, when the next ones come back. Everything shown is what the server reports
 * (`GET /billing/ai-allowance`); nothing is counted in the browser.
 *
 * During the seven-day trial it says instead that AI actions are paid from the wallet until the
 * first payment. Renders nothing on Free (whose AI is always paid from the wallet) or while loading.
 */
export function AiAllowanceCard() {
  const { t, tf, language } = useI18n()
  const [allowance, setAllowance] = useState<AiAllowance | null>(null)
  const [trial, setTrial] = useState(false)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    let alive = true
    api.getAiAllowance()
      .then((body) => {
        if (!alive) return
        setAllowance(body.ai_allowance)
        setTrial(body.trial && body.ai_billing === 'wallet')
      })
      .catch(() => { if (alive) setFailed(true) })
    return () => { alive = false }
  }, [])

  if (failed) return <p role="status" className="text-xs text-dim">{t('billing.ai.loadError')}</p>
  if (trial) {
    return (
      <section aria-labelledby="ai-trial-title" className="rounded-xl border border-border bg-surface p-[22px]">
        <div className="flex items-start gap-3">
          <Sparkles size={18} aria-hidden="true" className="mt-0.5 shrink-0 text-amber-text" />
          <div className="min-w-0 flex-1 space-y-1">
            <h2 id="ai-trial-title" className="text-base font-bold text-white">{t('billing.ai.trialTitle')}</h2>
            <p className="text-[13px] leading-relaxed text-bright">{t('billing.ai.trialBody')}</p>
          </div>
        </div>
      </section>
    )
  }
  if (!allowance) return null

  const exhausted = allowance.remaining === 0
  const next = allowance.next_credit_available_at
    ? new Intl.DateTimeFormat(language === 'ar' ? 'ar-EG' : 'en-GB', { hour: 'numeric', minute: '2-digit', weekday: 'short' })
        .format(new Date(allowance.next_credit_available_at))
    : null
  const usedPct = Math.min(100, Math.round((allowance.used / allowance.limit) * 100))

  return (
    <section aria-labelledby="ai-allowance-title" className="rounded-xl border border-border bg-surface p-[22px]">
      <div className="flex items-start gap-3">
        <Sparkles size={18} aria-hidden="true" className="mt-0.5 shrink-0 text-amber-text" />
        <div className="min-w-0 flex-1 space-y-2">
          <h2 id="ai-allowance-title" className="text-base font-bold text-white">{t('billing.ai.title')}</h2>
          <p className="text-sm text-bright" data-testid="ai-allowance-remaining">
            {tf('billing.ai.remaining', { remaining: allowance.remaining, limit: allowance.limit })}
          </p>
          <div
            role="progressbar"
            aria-label={t('billing.ai.title')}
            aria-valuemin={0}
            aria-valuemax={allowance.limit}
            aria-valuenow={allowance.used}
            className="h-1.5 overflow-hidden rounded-full bg-panel"
          >
            <div className="h-full rounded-full bg-amber" style={{ width: `${usedPct}%` }} />
          </div>
          {exhausted ? (
            <p role="status" className="text-[13px] leading-relaxed text-bright">{t('billing.ai.limit')}</p>
          ) : (
            <p className="text-xs leading-relaxed text-dim">{t('billing.ai.rolling')}</p>
          )}
          {next && <p className="text-xs font-semibold text-amber-text">{tf('billing.ai.next', { time: next })}</p>}
          <p className="text-xs text-dim">{t('billing.ai.access')}</p>
        </div>
      </div>
    </section>
  )
}
