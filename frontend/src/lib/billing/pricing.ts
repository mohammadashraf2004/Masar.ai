import type { BillingCatalog, BillingCycle, CartItem, Plan } from '@/lib/billing/types'

/**
 * The arithmetic of an order. Pure, so it is tested without a page.
 *
 * Whether VAT is already in the prices is the catalog's to say. When it is (Saudi consumer
 * prices are shown tax-inclusive) the total is `subtotal - discount` and nothing is added;
 * the page says "VAT included" under it. When it is not, VAT at the catalog's rate is added
 * to the discounted amount.
 */

/** Whole halalas, then back: no 0.1 + 0.2 in a price. */
export function round2(n: number): number {
  return Math.round((n + Number.EPSILON) * 100) / 100
}

/** "1,234.56", or "1,234" for a whole number: the `.00` is dropped. */
export function formatAmount(n: number): string {
  return Number.isInteger(n)
    ? n.toLocaleString('en-US')
    : n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

/** What the year costs paid up front, and what it would cost month by month. */
export function yearlyTotal(plan: Plan): number {
  return round2(plan.yearly * 12)
}
export function monthlyYearTotal(plan: Plan): number {
  return round2(plan.monthly * 12)
}

/** How much cheaper paying yearly is, in whole percent, for the best paid plan. */
export function yearlySavingPercent(plans: Plan[]): number {
  const savings = plans.filter((p) => p.monthly > 0).map((p) => (1 - p.yearly / p.monthly) * 100)
  return savings.length ? Math.round(Math.max(...savings)) : 0
}

/** The price of the chosen item before any discount, or null for an item the catalog does not have. */
export function subtotalOf(cart: CartItem, cycle: BillingCycle, catalog: BillingCatalog): number | null {
  if (cart.type === 'plan') {
    const plan = catalog.plans.find((p) => p.id === cart.id)
    if (!plan) return null
    return cycle === 'yearly' ? yearlyTotal(plan) : plan.monthly
  }
  const pack = catalog.packs.find((p) => p.id === cart.id)
  return pack ? pack.price : null
}

export interface OrderTotals {
  subtotal: number
  discount: number
  /** The VAT in the order: contained in the total when `vatIncluded`, added to it when not. */
  vat: number
  /** The rate that produced `vat`, as a whole percent (15). */
  vatPercent: number
  vatIncluded: boolean
  /** What is charged. */
  total: number
}

export function priceOrder(
  cart: CartItem,
  cycle: BillingCycle,
  catalog: BillingCatalog,
  promo: { percent: number } | null,
): OrderTotals | null {
  const subtotal = subtotalOf(cart, cycle, catalog)
  if (subtotal === null) return null
  const discount = promo ? round2((subtotal * promo.percent) / 100) : 0
  const net = round2(subtotal - discount)
  const vatPercent = Math.round(catalog.vatRate * 100)
  if (catalog.pricesIncludeVat) {
    // The tax is inside `net`: this is only how much of it, for anything that wants to say.
    return { subtotal, discount, vat: round2(net - net / (1 + catalog.vatRate)), vatPercent, vatIncluded: true, total: net }
  }
  const vat = round2(net * catalog.vatRate)
  return { subtotal, discount, vat, vatPercent, vatIncluded: false, total: round2(net + vat) }
}

/** Tabby: four equal payments, the first one today. */
export function installment(total: number): number {
  return round2(total / 4)
}
