import type { StringKey } from '@/lib/i18n'

/**
 * What billing is made of. Nothing here knows which payment gateway exists, or
 * where the prices come from: the page is written against these shapes, the catalog
 * (`catalog.ts`) supplies them and a `PaymentProvider` (`payments.ts`) takes the money.
 *
 * Every price is in the catalog's currency. Whether it already contains VAT is the
 * catalog's to say (`pricesIncludeVat`), together with the rate: the page adds a tax
 * line only when the prices do not include it.
 */

export type BillingCycle = 'monthly' | 'yearly'

export type PlanId = 'free' | 'pro'

export type RefundStatus =
  | 'not_requested' | 'requested' | 'under_review' | 'approved'
  | 'rejected' | 'processing' | 'refunded' | 'failed'

export interface RefundPolicySummary {
  version: string
  trial_days: number
  request_window_days: number
  review_required: boolean
  original_payment_method_when_supported: boolean
  provider_processing_time_applies: boolean
  cancellation_is_not_refund: boolean
  subscription_credits_granted: number
}

export interface SubscriptionOrder {
  reference_number: string
  plan: PlanId
  billing_period: BillingCycle
  amount: number
  currency: string
  status: 'pending' | 'paid' | 'failed' | 'cancelled' | 'refunded'
  created_at: string
  paid_at: string | null
  refund_eligible: boolean
  refund_ineligibility_reason: string | null
  refund: {
    status: RefundStatus
    requested_at: string | null
    processed_at: string | null
    amount: number | null
    reason: string | null
    provider_reference: string | null
  }
  refund_policy: RefundPolicySummary
  timeline?: Array<{
    type: 'payment' | 'refund'
    status: string
    from_status?: string
    amount?: number
    currency?: string
    created_at: string
  }>
}

export interface Plan {
  id: PlanId
  /** Per month, paid month by month. */
  monthly: number
  /** Total charged for a full year. */
  yearly: number
  signupCredits?: number
  popular?: boolean
  /** The plan's feature lines, as language-table keys. Product copy: see the catalog. */
  features: StringKey[]
}

export interface CreditPack {
  id: string
  /** Stable key from the server's catalogue ("starter", "standard", "plus", "power"). */
  code?: string | null
  name?: string
  /** The one the catalogue recommends. */
  popular?: boolean
  credits: number
  /** Extra credits given free with the pack. */
  bonus: number
  price: number
}

/** A time-limited offer with a code. */
export interface Offer {
  code: string
  /** Whole percent off, e.g. 30. */
  percent: number
  /** ISO time the offer ends. The countdown counts down to it. */
  endsAt: string
}

export interface BillingCatalog {
  /** ISO code, e.g. "SAR". */
  currency: string
  /** VAT as a fraction (0.15 is 15%). */
  vatRate: number
  /** True when every price already contains VAT: the total is then the sum of the prices, and
   *  the page says "VAT included" under it instead of adding a line. */
  pricesIncludeVat: boolean
  /** The plan the account is on now. It cannot be "bought". */
  currentPlan: PlanId
  trialEligible?: boolean
  plans: Plan[]
  packs: CreditPack[]
  offer: Offer | null
  refundPolicy?: RefundPolicySummary
}

/** One item at a time: choosing a plan or a pack replaces what was chosen before. */
export type CartItem = { type: 'plan'; id: PlanId } | { type: 'pack'; id: string }

export type PaymentMethodId = 'mada' | 'apple' | 'stc' | 'card' | 'wallet' | 'tabby'

export type PromoResult =
  | { valid: true; code: string; percent: number }
  | { valid: false; reason: 'invalid' | 'expired' | 'unavailable' }
