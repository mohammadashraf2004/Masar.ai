'use client'
import { useEffect } from 'react'
import { useI18n } from '@/lib/i18n'
import { formatAmount } from '@/lib/billing/pricing'
import type {
  CardFieldsProps, PaymentFailure, PaymentProvider, PaymentReceipt, PaymentRequest, PaymentResult,
} from '@/lib/billing/payments'
import type { PaymentMethodId } from '@/lib/billing/types'

/**
 * A payment provider that moves no money and remembers nothing beyond this browser tab.
 *
 * It stands in for a gateway until one is chosen (see payments.ts). It "takes" a payment
 * after a short pause, hands back an invoice number and keeps the receipt in
 * sessionStorage so the success page has something to show. It never touches the wallet:
 * nothing is charged and no credits are added.
 *
 * To see the failure states while building, add `?mockPayment=declined` (or `cancelled`,
 * `unavailable`) to the billing page's address; the mock reads it when a payment is made.
 */

export type MockOutcome = 'paid' | PaymentFailure

const RECEIPTS_KEY = 'masar-mock-receipts'
const FAILURES: readonly PaymentFailure[] = ['declined', 'cancelled', 'unavailable']

export function mockOutcomeFromUrl(): MockOutcome {
  if (typeof window === 'undefined') return 'paid'
  const asked = new URLSearchParams(window.location.search).get('mockPayment')
  return (FAILURES as readonly string[]).includes(asked ?? '') ? (asked as PaymentFailure) : 'paid'
}

function readReceipts(): Record<string, PaymentReceipt> {
  try {
    return JSON.parse(window.sessionStorage.getItem(RECEIPTS_KEY) ?? '{}')
  } catch {
    return {}
  }
}

function saveReceipt(receipt: PaymentReceipt) {
  try {
    window.sessionStorage.setItem(RECEIPTS_KEY, JSON.stringify({ ...readReceipts(), [receipt.invoiceId]: receipt }))
  } catch {
    // Storage blocked: the payment still "went through", the success page just has no receipt to show.
  }
}

/** INV-2026-09-26-0418: the date, then four digits. */
function makeInvoiceId(now = new Date()): string {
  const day = now.toISOString().slice(0, 10)
  const suffix = String(Math.floor(Math.random() * 10_000)).padStart(4, '0')
  return `INV-${day}-${suffix}`
}

/** Stands where a gateway's hosted fields would be: card details are never typed into our own inputs. */
function MockCardFields({ onReadyChange }: CardFieldsProps) {
  const { t } = useI18n()
  useEffect(() => {
    onReadyChange(true)
    return () => onReadyChange(false)
  }, [onReadyChange])

  return (
    <div
      role="group"
      aria-label={t('billing.card.fields')}
      className="flex min-h-[96px] flex-col items-center justify-center gap-1.5 rounded-lg border border-dashed border-border px-3 py-4 text-center"
      style={{ backgroundImage: 'repeating-linear-gradient(45deg, rgb(var(--card2)) 0 6px, transparent 6px 12px)' }}
    >
      <span className="font-mono text-[11px] tracking-wide text-ghost">HOSTED CARD FIELDS</span>
      <span className="text-xs text-dim">{t('billing.card.hosted')}</span>
    </div>
  )
}

export class MockPaymentProvider implements PaymentProvider {
  readonly id = 'mock'
  readonly isMock = true
  readonly CardFields = MockCardFields

  constructor(private readonly options: { delayMs?: number; outcome?: () => MockOutcome } = {}) {}

  /** The handoff's five methods. */
  async listMethods(): Promise<readonly PaymentMethodId[]> {
    return ['mada', 'apple', 'stc', 'card', 'tabby']
  }

  async pay(request: PaymentRequest): Promise<PaymentResult> {
    await new Promise((resolve) => setTimeout(resolve, this.options.delayMs ?? 900))
    const outcome = this.options.outcome?.() ?? 'paid'
    if (outcome !== 'paid') return { status: 'failed', reason: outcome }

    const invoiceId = makeInvoiceId()
    saveReceipt({
      invoiceId,
      cart: request.cart,
      cycle: request.cycle,
      amount: request.amount,
      currency: request.currency,
      method: request.method,
      paidAt: new Date().toISOString(),
    })
    return { status: 'paid', invoiceId }
  }

  async getReceipt(invoiceId: string): Promise<PaymentReceipt | null> {
    return readReceipts()[invoiceId] ?? null
  }

  /** A plain-text stand-in for the tax invoice a real gateway or the backend would issue. */
  async downloadInvoice(invoiceId: string): Promise<void> {
    const receipt = await this.getReceipt(invoiceId)
    if (!receipt) return
    const body = [
      'MASAR - TAX INVOICE (MOCK: NOTHING WAS CHARGED)',
      `Invoice:  ${receipt.invoiceId}`,
      `Date:     ${receipt.paidAt}`,
      `Item:     ${receipt.cart.type === 'plan' ? `${receipt.cart.id} plan (${receipt.cycle})` : `credit pack ${receipt.cart.id}`}`,
      `Method:   ${receipt.method}`,
      `Total:    ${receipt.currency} ${formatAmount(receipt.amount)} (VAT included)`,
      '',
    ].join('\n')
    const url = URL.createObjectURL(new Blob([body], { type: 'text/plain;charset=utf-8' }))
    const link = document.createElement('a')
    link.href = url
    link.download = `${receipt.invoiceId}.txt`
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(url)
  }
}
