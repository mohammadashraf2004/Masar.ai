import type { PaymentProvider, PaymentReceipt, PaymentResult } from '@/lib/billing/payments'
import type { PaymentMethodId } from '@/lib/billing/types'
import { api } from '@/lib/api'

/**
 * Kashier, the gateway Masar takes payments through (it replaced Paymob for new payments).
 *
 * The page never prices or settles anything here: `pay()` asks the backend to open a checkout,
 * the backend creates a Kashier hosted payment session for its own immutable order amount, and
 * the shopper is redirected to Kashier's page. Pro is activated only by the backend's verified,
 * server-confirmed webhook - never by the redirect back, which only lands on a page that polls
 * the backend.
 *
 * Kashier's hosted page offers cards and mobile wallets itself, so there are no card fields of
 * ours (`CardFields` is absent) and no phone number is asked for here.
 */
export const KASHIER_NOT_CONFIGURED = 'This Kashier operation is not configured'

export class KashierProvider implements PaymentProvider {
  readonly id = 'kashier'
  readonly isMock = false

  async listMethods(): Promise<readonly PaymentMethodId[]> {
    return ['card', 'wallet']
  }

  async pay(request: Parameters<PaymentProvider['pay']>[0]): Promise<PaymentResult> {
    if (request.cart.type !== 'plan' || request.cart.id !== 'pro') {
      throw new Error(KASHIER_NOT_CONFIGURED)
    }
    if (request.method !== 'card' && request.method !== 'wallet') {
      return { status: 'failed', reason: 'unavailable' }
    }
    // Amount/currency in `request` are display values only. The backend selects the plan row
    // and sends its own amount to Kashier.
    const checkout = await api.checkoutSubscription('pro', request.cycle, request.method)
    return { status: 'redirect', url: checkout.payment_url }
  }

  async getReceipt(): Promise<PaymentReceipt | null> {
    throw new Error(KASHIER_NOT_CONFIGURED)
  }

  async downloadInvoice(): Promise<void> {
    throw new Error(KASHIER_NOT_CONFIGURED)
  }
}
