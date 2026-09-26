'use client'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { useMoney } from '@/lib/billing/money'
import { formatAmount } from '@/lib/billing/pricing'
import type { CreditPack } from '@/lib/billing/types'

/** One credit pack: a tile you press to put it in the order (which replaces whatever was in it). */
export function PackTile({
  pack, currency, selected, onChoose,
}: {
  pack: CreditPack
  currency: string
  selected: boolean
  onChoose: () => void
}) {
  const { t, tf } = useI18n()
  const { money } = useMoney(currency)
  return (
    <button
      type="button"
      onClick={onChoose}
      aria-pressed={selected}
      className={cn(
        'flex flex-col gap-1 rounded-[10px] border p-4 text-start transition-colors',
        'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring',
        selected ? 'border-amber bg-amber-soft' : 'border-border bg-void hover:border-muted',
      )}
    >
      <span className="flex min-h-[22px] items-center justify-between">
        <span aria-hidden="true" className="h-2 w-2 rounded-full bg-amber" />
        {pack.bonus > 0 && (
          <span className="rounded-full border border-emerald px-2 text-[11px] text-emerald">{tf('billing.packs.bonus', { n: pack.bonus })}</span>
        )}
      </span>
      <span className="font-mono text-2xl font-medium text-white">{formatAmount(pack.credits)}</span>
      <span className="text-xs text-dim">{t('billing.packs.credits')}</span>
      <span className="mt-2.5 border-t border-border pt-2.5 text-sm font-semibold text-amber-text">
        {money(pack.price)}
      </span>
    </button>
  )
}
