import type { BillingCatalog, PromoResult } from '@/lib/billing/types'

/**
 * Where the plans, packs, offer and promo codes come from.
 *
 * The page is written against `BillingCatalogSource`. The only implementation today is
 * a placeholder holding the numbers from the design handoff, so the page can be built,
 * reviewed and tested end to end; the real one calls the API (see docs/backend-requests.md,
 * "Billing"). Swap it here, in one place.
 *
 * Do not read these numbers as a price list: they are the handoff's example prices.
 */
export interface BillingCatalogSource {
  load(): Promise<BillingCatalog>
  /** Whether a code is good, decided by the server (never by the page). */
  validatePromo(code: string): Promise<PromoResult>
}

/** 4 days, 11 hours, 32 minutes: the handoff's countdown, counted from when the page loads. */
const PLACEHOLDER_OFFER_MS = ((4 * 24 + 11) * 60 + 32) * 60_000

const PLACEHOLDER_CODE = 'MASAR30'
const PLACEHOLDER_PERCENT = 30

export const placeholderCatalogSource: BillingCatalogSource = {
  async load() {
    return {
      currency: 'SAR',
      // Saudi VAT is 15% and consumer prices are shown tax-inclusive. Both are the catalog's to
      // say, so a business that prices ex-VAT changes two values here and nothing in the page.
      vatRate: 0.15,
      pricesIncludeVat: true,
      currentPlan: 'free',
      plans: [
        {
          id: 'free', monthly: 0, yearly: 0,
          features: [
            'billing.plan.free.f1', // TODO(product): confirm
            'billing.plan.free.f2', // TODO(product): confirm
            'billing.plan.free.f3', // TODO(product): confirm
          ],
        },
        {
          id: 'pro', monthly: 79, yearly: 63, popular: true,
          features: [
            'billing.plan.pro.f1', // TODO(product): confirm
            'billing.plan.pro.f2', // TODO(product): confirm
            'billing.plan.pro.f3', // TODO(product): confirm
            'billing.plan.pro.f4', // TODO(product): confirm
          ],
        },
        {
          id: 'career', monthly: 149, yearly: 119,
          features: [
            'billing.plan.career.f1', // TODO(product): confirm
            'billing.plan.career.f2', // TODO(product): confirm
            'billing.plan.career.f3', // TODO(product): confirm
            'billing.plan.career.f4', // TODO(product): confirm
            'billing.plan.career.f5', // TODO(product): confirm
          ],
        },
      ],
      packs: [
        { id: 'p1', credits: 500, bonus: 0, price: 49 },
        { id: 'p2', credits: 1200, bonus: 100, price: 99 },
        { id: 'p3', credits: 3000, bonus: 400, price: 229 },
      ],
      offer: {
        code: PLACEHOLDER_CODE,
        percent: PLACEHOLDER_PERCENT,
        endsAt: new Date(Date.now() + PLACEHOLDER_OFFER_MS).toISOString(),
      },
    }
  },

  async validatePromo(code) {
    return code.trim().toUpperCase() === PLACEHOLDER_CODE
      ? { valid: true, code: PLACEHOLDER_CODE, percent: PLACEHOLDER_PERCENT }
      : { valid: false, reason: 'invalid' }
  },
}

/** The catalog the app uses. */
export const billingCatalog: BillingCatalogSource = placeholderCatalogSource
