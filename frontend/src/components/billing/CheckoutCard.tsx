'use client'
import { Lock } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useI18n, type StringKey } from '@/lib/i18n'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/index'
import { useMoney } from '@/lib/billing/money'
import { installment, type OrderTotals } from '@/lib/billing/pricing'
import type { PaymentFailure, PaymentProvider } from '@/lib/billing/payments'
import type { PaymentMethodId } from '@/lib/billing/types'

/** What the item in the order is called and what it comes with: already worded by the page. */
export interface OrderItem {
  name: string
  meta: string
}

/** The logo slot's label until each provider's official brand asset is supplied. */
const LOGO_SLOT: Record<PaymentMethodId, string> = { mada: 'mada', apple: 'Pay', stc: 'stc', card: 'VISA', wallet: 'wallet', tabby: 'tabby' }

/**
 * The order and the way to pay for it.
 *
 * When the catalog's prices include VAT the lines are the subtotal, the discount if there is one
 * and the total, with "VAT included" under it: no tax is added. When they do not, a VAT line is
 * added between the two. A card is never typed into a field of ours; the provider's hosted fields
 * are mounted where the card details go. The pay button shows the total, or a quarter of it with
 * Tabby (four payments, the first today).
 */
export function CheckoutCard({
  item, totals, currency, promo, methods, method, onMethod, provider, cardReady, onCardReady,
  processing, failure, onPay,
}: {
  item: OrderItem
  totals: OrderTotals
  currency: string
  promo: { code: string; percent: number } | null
  /** What the provider says it takes: the list is the provider's, not the page's. */
  methods: readonly PaymentMethodId[]
  method: PaymentMethodId | null
  onMethod: (method: PaymentMethodId) => void
  /** Null when payments are not open: everything shows, nothing can be bought. */
  provider: PaymentProvider | null
  cardReady: boolean
  onCardReady: (ready: boolean) => void
  processing: boolean
  failure: PaymentFailure | null
  onPay: () => void
}) {
  const { t, tf } = useI18n()
  const { money } = useMoney(currency)
  const CardFields = provider?.CardFields

  const payLabel = method === 'tabby'
    ? tf('billing.payToday', { amount: money(installment(totals.total)) })
    : tf('billing.pay', { amount: money(totals.total) })
  const blocked = !provider || !method || (method === 'card' && !!CardFields && !cardReady)

  return (
    <Card className="flex flex-col gap-4 p-[22px] lg:sticky lg:top-6">
      <h2 className="text-base font-bold text-white">{t('billing.summary')}</h2>

      <div className="flex items-start justify-between gap-2.5 rounded-[10px] bg-panel p-3.5">
        <div className="flex min-w-0 flex-col gap-0.5">
          <span className="text-sm font-semibold text-white">{item.name}</span>
          <span className="text-xs text-dim">{item.meta}</span>
        </div>
        <span className="whitespace-nowrap font-mono text-[13px] text-white">{money(totals.subtotal)}</span>
      </div>

      <dl className="flex flex-col gap-2.5 text-[13px]">
        <div className="flex justify-between text-dim">
          <dt>{t('billing.line.subtotal')}</dt>
          <dd className="font-mono">{money(totals.subtotal)}</dd>
        </div>
        {promo && (
          <div className="flex justify-between text-emerald">
            <dt>{tf('billing.line.discount', { code: promo.code, pct: promo.percent })}</dt>
            <dd className="font-mono">−{money(totals.discount)}</dd>
          </div>
        )}
        {!totals.vatIncluded && (
          <div className="flex justify-between text-dim">
            <dt>{tf('billing.line.vat', { pct: totals.vatPercent })}</dt>
            <dd className="font-mono">{money(totals.vat)}</dd>
          </div>
        )}
        <div className="flex items-baseline justify-between border-t border-border pt-3">
          <dt className="text-sm font-bold text-white">{t('billing.total')}</dt>
          <dd className="text-end">
            <span className="block font-display text-[22px] font-extrabold text-white">{money(totals.total)}</span>
            {/* Under the total, never a line added to it: the price already includes the tax. */}
            {totals.vatIncluded && <span className="block text-xs text-ghost">{t('billing.vatIncluded')}</span>}
          </dd>
        </div>
      </dl>

      {methods.length > 0 && (
      <fieldset className="flex flex-col gap-2 border-0 p-0">
        <legend className="mb-2 p-0 text-[13px] font-semibold text-white">{t('billing.method')}</legend>
        {methods.map((id) => {
          const selected = id === method
          return (
            <label
              key={id}
              className={cn(
                'flex min-h-[52px] cursor-pointer items-center gap-3 rounded-lg border px-3 py-2',
                selected ? 'border-amber bg-amber-soft' : 'border-border',
              )}
            >
              <input
                type="radio"
                name="payment-method"
                value={id}
                checked={selected}
                onChange={() => onMethod(id)}
                className="peer sr-only"
              />
              <span
                aria-hidden="true"
                className={cn(
                  'box-border h-4 w-4 shrink-0 rounded-full',
                  selected ? 'border-[5px] border-amber' : 'border-[1.5px] border-border',
                  'peer-focus-visible:outline peer-focus-visible:outline-2 peer-focus-visible:outline-offset-2 peer-focus-visible:outline-ring',
                )}
              />
              <span className="flex flex-1 flex-col gap-px">
                <span className="text-sm font-semibold text-white">{t(`billing.method.${id}` as StringKey)}</span>
                <span className="text-xs text-ghost">{t(`billing.method.${id}.sub` as StringKey)}</span>
              </span>
              {/* Until each provider's own brand asset is supplied: a neutral slot, not a logo we drew. */}
              <span
                aria-hidden="true"
                className="grid h-6 min-w-[44px] place-items-center rounded border border-border px-1.5 font-mono text-[9px] text-ghost"
                style={{ backgroundImage: 'repeating-linear-gradient(45deg, rgb(var(--card2)) 0 3px, transparent 3px 6px)' }}
              >
                {LOGO_SLOT[id]}
              </span>
            </label>
          )
        })}
      </fieldset>
      )}

      {method === 'card' && CardFields && <CardFields onReadyChange={onCardReady} />}

      {!provider && <p className="text-xs leading-relaxed text-dim">{t('billing.closed')}</p>}
      {provider?.isMock && <p className="text-xs leading-relaxed text-amber-text">{t('billing.mock')}</p>}

      {failure && (
        <p role="alert" className="rounded-lg border border-rose/20 bg-rose/10 px-3 py-2.5 text-xs text-rose">
          {t(`billing.error.${failure}` as StringKey)}
        </p>
      )}

      <Button
        onClick={onPay}
        loading={processing}
        disabled={blocked}
        className="h-[50px] w-full text-[15px] font-bold"
      >
        {payLabel}
      </Button>

      <p className="flex items-center justify-center gap-2 text-center text-xs text-ghost">
        <Lock size={13} aria-hidden="true" className="shrink-0" />
        <span>{t('billing.trust')}</span>
      </p>
    </Card>
  )
}
