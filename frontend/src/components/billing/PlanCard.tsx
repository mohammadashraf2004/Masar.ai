'use client'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useI18n, type StringKey } from '@/lib/i18n'
import { buttonStyles } from '@/components/ui/Button'
import { useMoney } from '@/lib/billing/money'
import { formatAmount, monthlyYearTotal, yearlyTotal } from '@/lib/billing/pricing'
import type { BillingCycle, Plan } from '@/lib/billing/types'

/**
 * One plan. The card is not itself a button: its call to action is, stretched to cover the
 * card, so the whole card selects it while there is still exactly one control to tab to.
 * The current plan is shown but cannot be chosen (nothing is bought to stay on it).
 */
export function PlanCard({
  plan, currency, cycle, selected, current, onChoose,
}: {
  plan: Plan
  currency: string
  cycle: BillingCycle
  selected: boolean
  current: boolean
  onChoose: () => void
}) {
  const { t, tf } = useI18n()
  const free = plan.monthly === 0
  const price = cycle === 'yearly' ? plan.yearly : plan.monthly
  const { money, label: currencyName } = useMoney(currency)
  const name = t(`billing.plan.${plan.id}.name` as StringKey)

  const note = free
    ? t('billing.note.free')
    : cycle === 'yearly'
      ? tf('billing.note.yearly', { total: money(yearlyTotal(plan)), list: money(monthlyYearTotal(plan)) })
      : t('billing.note.monthly')

  return (
    <article
      className={cn(
        'relative flex flex-col gap-3 rounded-xl border bg-surface p-[22px]',
        selected ? 'border-amber' : 'border-border',
      )}
      style={selected ? { boxShadow: '0 0 0 4px rgb(var(--acc) / var(--acc-soft-a))' } : undefined}
    >
      <div className="flex items-center justify-between gap-2.5">
        <h3 className="text-lg font-bold text-white">{name}</h3>
        {plan.popular && (
          <span className="rounded-full bg-amber px-2.5 py-0.5 text-[11px] font-semibold text-on-amber">{t('billing.popular')}</span>
        )}
      </div>

      <p className="text-[13px] leading-relaxed text-dim">{t(`billing.plan.${plan.id}.desc` as StringKey)}</p>

      <div className="flex items-baseline gap-1.5">
        <span className="font-display text-[40px] font-extrabold leading-none text-white">{formatAmount(price)}</span>
        <span className="text-[13px] text-dim">{free ? currencyName : tf('billing.perMonth', { currency: currencyName })}</span>
      </div>

      <p className="min-h-[18px] text-xs text-ghost">{note}</p>

      <ul className="flex flex-col gap-[9px] border-t border-border pt-3.5">
        {plan.features.map((key) => (
          <li key={key} className="flex items-start gap-2.5 text-[13px] leading-relaxed text-bright">
            <Check size={14} strokeWidth={2.6} aria-hidden="true" className="mt-1 shrink-0 text-emerald" />
            <span>{t(key)}</span>
          </li>
        ))}
      </ul>

      {/* The current plan is a label, not a choice: aria-disabled rather than disabled, so it
          stays in the tab order and reads at full strength instead of at a disabled 40%. */}
      <button
        type="button"
        onClick={current ? undefined : onChoose}
        aria-disabled={current || undefined}
        aria-pressed={current ? undefined : selected}
        className={cn(
          buttonStyles({ variant: selected ? 'amber' : 'ghost', size: 'lg' }),
          'mt-auto h-11',
          current
            ? 'cursor-default text-ghost hover:border-border hover:bg-transparent hover:text-ghost'
            // the stretched hit area: the whole card, one control
            : "after:absolute after:inset-0 after:content-['']",
        )}
      >
        {current ? t('billing.cta.current') : selected ? t('billing.cta.selected') : tf('billing.cta.choose', { name })}
      </button>
    </article>
  )
}
