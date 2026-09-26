import type { PaymentProvider, PaymentReceipt, PaymentResult } from '@/lib/billing/payments'
import type { PaymentMethodId } from '@/lib/billing/types'

/**
 * A stub for Paymob, the gateway the backend already integrates (`/payments/wallet/topup/init`,
 * a webhook, `credit_packages` priced in EGP).
 *
 * It exists so the interface is shown to fit a real gateway, and so a decision to use Paymob is a
 * matter of filling this in rather than of designing it. It is deliberately not wired: nothing
 * returns it from `getPaymentProvider()`, and every call that would touch money throws.
 *
 * What it will have to answer for: Paymob takes cards and mobile wallets, not mada, Apple Pay,
 * STC Pay or Tabby, so `listMethods()` is honest about that (and the page shows only these two);
 * it redirects to a hosted checkout rather than mounting card fields, so there is no `CardFields`;
 * and it prices in EGP where the design shows SAR.
 */
export const PAYMOB_NOT_CONFIGURED = 'PaymobProvider is not configured'

export class PaymobProvider implements PaymentProvider {
  readonly id = 'paymob'
  readonly isMock = false

  async listMethods(): Promise<readonly PaymentMethodId[]> {
    return ['card', 'wallet']
  }

  async pay(): Promise<PaymentResult> {
    throw new Error(PAYMOB_NOT_CONFIGURED)
  }

  async getReceipt(): Promise<PaymentReceipt | null> {
    throw new Error(PAYMOB_NOT_CONFIGURED)
  }

  async downloadInvoice(): Promise<void> {
    throw new Error(PAYMOB_NOT_CONFIGURED)
  }
}
