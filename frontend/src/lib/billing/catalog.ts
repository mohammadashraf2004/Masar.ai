import type { BillingCatalog, Plan, PromoResult } from '@/lib/billing/types'
import { api } from '@/lib/api'

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

export const apiCatalogSource: BillingCatalogSource = {
  async load() {
    const catalog = await api.getBillingCatalog()
    return {
      currency: catalog.currency,
      vatRate: catalog.vat_rate,
      pricesIncludeVat: catalog.prices_include_vat,
      currentPlan: catalog.current_plan,
      trialEligible: catalog.trial_eligible,
      plans: catalog.plans.map((plan) => ({
        id: plan.id,
        monthly: plan.monthly,
        yearly: plan.yearly,
        popular: plan.popular,
        signupCredits: plan.signup_credits,
        features: plan.features as Plan['features'],
      })),
      packs: catalog.packs,
      offer: catalog.offer,
      refundPolicy: catalog.refund_policy,
    }
  },

  async validatePromo(_code) {
    return { valid: false, reason: 'unavailable' }
  },
}

/** The catalog the app uses. */
export const billingCatalog: BillingCatalogSource = apiCatalogSource
