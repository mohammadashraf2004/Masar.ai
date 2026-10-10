import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/lib/api', () => ({ api: { getBillingCatalog: vi.fn(), checkoutSubscription: vi.fn(), initWalletTopUp: vi.fn() } }))

import { apiCatalogSource } from '@/lib/billing/catalog'
import { currencyLabel, formatMoney } from '@/lib/billing/money'
import { MockPaymentProvider, mockOutcomeFromUrl } from '@/lib/billing/mockPayments'
import { getPaymentProvider, type PaymentProvider, type PaymentRequest } from '@/lib/billing/payments'
import { KASHIER_NOT_CONFIGURED, KashierProvider } from '@/lib/billing/kashierProvider'
import {
  formatAmount, installment, monthlyYearTotal, priceOrder, round2, subtotalOf, yearlySavingPercent, yearlyTotal,
} from '@/lib/billing/pricing'
import type { BillingCatalog } from '@/lib/billing/types'
import { timeLeft } from '@/components/billing/OfferBanner'
import { api } from '@/lib/api'

/** What the backend's /billing/catalog actually returns: EGP, Free + Pro only, no offers yet. */
const catalog: BillingCatalog = {
  currency: 'EGP',
  vatRate: 0.14,
  pricesIncludeVat: true,
  currentPlan: 'free',
  plans: [
    { id: 'free', monthly: 0, yearly: 0, signupCredits: 40, features: ['billing.plan.free.f1', 'billing.plan.free.f2', 'billing.plan.free.f3'] },
    { id: 'pro', monthly: 299, yearly: 2199, signupCredits: 0, popular: true, features: ['billing.plan.pro.f1', 'billing.plan.pro.f2', 'billing.plan.pro.f3', 'billing.plan.pro.f4'] },
  ],
  packs: [
    { id: 'p1', credits: 500, bonus: 0, price: 100 },
    { id: 'p2', credits: 1200, bonus: 100, price: 300 },
    { id: 'p3', credits: 3000, bonus: 400, price: 700 },
  ],
  offer: null,
}

describe('formatting a price', () => {
  it('separates thousands and drops .00 from a whole number', () => {
    expect(formatAmount(1234)).toBe('1,234')
    expect(formatAmount(756)).toBe('756')
  })

  it('always shows two decimals on a fractional price', () => {
    expect(formatAmount(1234.56)).toBe('1,234.56')
    expect(formatAmount(529.2)).toBe('529.20')
    expect(formatAmount(12.5)).toBe('12.50')
  })

  it('rounds to two decimals without floating-point residue', () => {
    expect(round2(0.1 + 0.2)).toBe(0.3)
    expect(round2(226.8)).toBe(226.8)
    expect(round2(1.005)).toBe(1.01)
  })
})

describe('pricing an order: VAT-inclusive, so nothing is added on top', () => {
  it('a yearly plan costs the total year price, not twelve times it', () => {
    const pro = catalog.plans.find((p) => p.id === 'pro')!
    expect(yearlyTotal(pro)).toBe(2199)
    expect(monthlyYearTotal(pro)).toBe(3588)
    expect(subtotalOf({ type: 'plan', id: 'pro' }, 'yearly', catalog)).toBe(2199)
    expect(subtotalOf({ type: 'plan', id: 'pro' }, 'monthly', catalog)).toBe(299)
  })

  it('a pack costs its price, whatever the billing cycle', () => {
    expect(subtotalOf({ type: 'pack', id: 'p2' }, 'yearly', catalog)).toBe(300)
    expect(subtotalOf({ type: 'pack', id: 'p2' }, 'monthly', catalog)).toBe(300)
  })

  it('when prices include VAT the total is the subtotal, with no tax added', () => {
    expect(catalog.pricesIncludeVat).toBe(true)
    const order = priceOrder({ type: 'plan', id: 'pro' }, 'yearly', catalog, null)!
    expect(order).toMatchObject({ subtotal: 2199, discount: 0, total: 2199, vatIncluded: true, vatPercent: 14 })
    expect(priceOrder({ type: 'pack', id: 'p3' }, 'monthly', catalog, null)).toMatchObject({ subtotal: 700, total: 700 })
  })

  it('says how much of an inclusive total is VAT, without adding it', () => {
    // 2199 / 1.14 = 1928.9474: the VAT inside it is the difference.
    expect(priceOrder({ type: 'plan', id: 'pro' }, 'yearly', catalog, null)!.vat).toBe(270.05)
  })

  it('when prices exclude VAT it is added to the discounted amount, at the catalog rate', () => {
    const exclusive = { ...catalog, pricesIncludeVat: false }
    expect(priceOrder({ type: 'plan', id: 'pro' }, 'yearly', exclusive, null)).toMatchObject({
      subtotal: 2199, discount: 0, vat: 307.86, vatPercent: 14, vatIncluded: false, total: 2506.86,
    })
    // the discount comes off first, and the tax is on what is left
    expect(priceOrder({ type: 'plan', id: 'pro' }, 'yearly', exclusive, { percent: 30 })).toMatchObject({
      subtotal: 2199, discount: 659.7, vat: 215.5, total: 1754.8,
    })
  })

  it('uses whatever VAT rate the catalog gives', () => {
    const order = priceOrder({ type: 'pack', id: 'p2' }, 'yearly', { ...catalog, pricesIncludeVat: false, vatRate: 0.05 }, null)!
    expect(order).toMatchObject({ vat: 15, vatPercent: 5, total: 315 })
  })

  it('takes a promo off the subtotal, rounded to the piastre, and that is the total', () => {
    expect(priceOrder({ type: 'plan', id: 'pro' }, 'yearly', catalog, { percent: 30 })).toMatchObject({ subtotal: 2199, discount: 659.7, total: 1539.3 })
    expect(priceOrder({ type: 'pack', id: 'p1' }, 'yearly', catalog, { percent: 30 })).toMatchObject({ subtotal: 100, discount: 30, total: 70 })
  })

  it('has no price for something the catalog does not sell', () => {
    expect(priceOrder({ type: 'pack', id: 'nope' }, 'yearly', catalog, null)).toBeNull()
    expect(priceOrder({ type: 'plan', id: 'pro' }, 'yearly', { ...catalog, plans: [] }, null)).toBeNull()
  })

  it('splits a Tabby payment into four, the first one today', () => {
    expect(installment(2199)).toBe(549.75)
    expect(installment(299)).toBe(74.75)
  })

  it('says yearly saves ~39% on the best paid plan (299 x 12 = 3,588 vs 2,199)', () => {
    expect(yearlySavingPercent(catalog.plans)).toBe(39)
    expect(yearlySavingPercent([{ id: 'free', monthly: 0, yearly: 0, features: [] }])).toBe(0)
  })
})

describe('the offer countdown', () => {
  const NOW = Date.parse('2026-09-26T12:00:00Z')

  it('counts days, hours and minutes left', () => {
    expect(timeLeft('2026-10-01T00:32:00Z', NOW)).toEqual({ over: false, days: 4, hours: 12, minutes: 32 })
  })

  it('is over once the time has passed, and never negative', () => {
    expect(timeLeft('2026-09-26T11:59:00Z', NOW)).toEqual({ over: true, days: 0, hours: 0, minutes: 0 })
  })
})

describe('money', () => {
  it('puts the currency before the number in English and after it in Arabic', () => {
    expect(formatMoney(1234.5, 'SAR', 'en')).toBe('SAR 1,234.50')
    expect(formatMoney(1234.5, 'SAR', 'ar')).toBe('1,234.50 ر.س')
  })

  it('names EGP in both languages, and falls back to the code for one it does not know', () => {
    expect(currencyLabel('EGP', 'ar')).toBe('ج.م')
    expect(formatMoney(99, 'EGP', 'en')).toBe('EGP 99')
    expect(currencyLabel('USD', 'ar')).toBe('USD')
  })
})

describe('the API-backed catalog', () => {
  it('maps the backend catalog (snake_case, minor-unit-free) into the shape the page uses', async () => {
    vi.mocked(api.getBillingCatalog).mockResolvedValue({
      currency: 'EGP', vat_rate: 0.14, prices_include_vat: true, current_plan: 'free',
      plans: [
        { id: 'free', monthly: 0, yearly: 0, signup_credits: 40, features: ['billing.plan.free.f1'] },
        { id: 'pro', monthly: 299, yearly: 2199, signup_credits: 0, popular: true, features: ['billing.plan.pro.f1'] },
      ],
      packs: [{ id: 'p1', credits: 500, bonus: 0, price: 100 }],
      offer: null,
    })

    expect(await apiCatalogSource.load()).toEqual({
      currency: 'EGP', vatRate: 0.14, pricesIncludeVat: true, currentPlan: 'free',
      plans: [
        { id: 'free', monthly: 0, yearly: 0, signupCredits: 40, popular: undefined, features: ['billing.plan.free.f1'] },
        { id: 'pro', monthly: 299, yearly: 2199, signupCredits: 0, popular: true, features: ['billing.plan.pro.f1'] },
      ],
      packs: [{ id: 'p1', credits: 500, bonus: 0, price: 100 }],
      offer: null,
    })
  })

  it('has no promo codes yet: the backend has none to validate', async () => {
    expect(await apiCatalogSource.validatePromo('ANYTHING')).toEqual({ valid: false, reason: 'unavailable' })
  })
})

describe('the mock payment provider', () => {
  const request: PaymentRequest = {
    cart: { type: 'plan', id: 'pro' }, cycle: 'yearly', method: 'mada', amount: 2199, currency: 'EGP', promoCode: null,
  }
  beforeEach(() => window.sessionStorage.clear())

  it('says it is a mock, so the page can say so', () => {
    const provider = new MockPaymentProvider({ delayMs: 0 })
    expect(provider.isMock).toBe(true)
    expect(provider.CardFields).toBeTypeOf('function')
  })

  it("lists the handoff's five payment methods, in order", async () => {
    expect(await new MockPaymentProvider({ delayMs: 0 }).listMethods()).toEqual(['mada', 'apple', 'stc', 'card', 'tabby'])
  })

  it('takes a payment, returns an invoice number and remembers the receipt', async () => {
    const provider = new MockPaymentProvider({ delayMs: 0 })
    const result = await provider.pay(request)

    expect(result.status).toBe('paid')
    if (result.status !== 'paid') return
    expect(result.invoiceId).toMatch(/^INV-\d{4}-\d{2}-\d{2}-\d{4}$/)
    expect(await provider.getReceipt(result.invoiceId)).toMatchObject({ invoiceId: result.invoiceId, amount: 2199, currency: 'EGP', method: 'mada', cycle: 'yearly' })
  })

  it('knows nothing about an invoice it did not issue', async () => {
    expect(await new MockPaymentProvider({ delayMs: 0 }).getReceipt('INV-2026-01-01-0001')).toBeNull()
  })

  it.each(['declined', 'cancelled', 'unavailable'] as const)('can fail as %s, and then leaves no receipt', async (reason) => {
    const provider = new MockPaymentProvider({ delayMs: 0, outcome: () => reason })
    expect(await provider.pay(request)).toEqual({ status: 'failed', reason })
    expect(window.sessionStorage.getItem('masar-mock-receipts')).toBeNull()
  })

  it('reads a failure to simulate from the address, and pays otherwise', () => {
    window.history.replaceState({}, '', '/billing?mockPayment=declined')
    expect(mockOutcomeFromUrl()).toBe('declined')
    window.history.replaceState({}, '', '/billing?mockPayment=whatever')
    expect(mockOutcomeFromUrl()).toBe('paid')
    window.history.replaceState({}, '', '/billing')
    expect(mockOutcomeFromUrl()).toBe('paid')
  })

  it('downloads a plain-text invoice that says nothing was charged', async () => {
    const provider = new MockPaymentProvider({ delayMs: 0 })
    const paid = await provider.pay(request)
    if (paid.status !== 'paid') throw new Error('expected a payment')

    // jsdom's Blob has no .text(), so read it the long way.
    let body = ''
    const create = vi.fn((blob: Blob) => {
      const reader = new FileReader()
      reader.onload = () => { body = String(reader.result) }
      reader.readAsText(blob)
      return 'blob:invoice'
    })
    Object.assign(URL, { createObjectURL: create, revokeObjectURL: vi.fn() })
    const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})

    await provider.downloadInvoice(paid.invoiceId)
    await Promise.resolve()

    expect(click).toHaveBeenCalledTimes(1)
    await vi.waitFor(() => expect(body).toContain('NOTHING WAS CHARGED'))
    expect(body).toContain(paid.invoiceId)
    expect(body).toContain('EGP 2,199 (VAT included)')
    click.mockRestore()
  })
})

describe('the Kashier provider: redirects to a backend-priced hosted checkout', () => {
  const proRequest: PaymentRequest = { cart: { type: 'plan', id: 'pro' }, cycle: 'yearly', method: 'card', amount: 2199, currency: 'EGP', promoCode: null }

  it('lists cards and mobile wallets, and nothing the gateway does not take', async () => {
    const provider = new KashierProvider()
    expect(provider.isMock).toBe(false)
    expect(await provider.listMethods()).toEqual(['card', 'wallet'])
  })

  it('asks the backend for a checkout order and redirects to its hosted URL, never pricing the sale itself', async () => {
    vi.mocked(api.checkoutSubscription).mockResolvedValue({ order_id: 7, payment_url: 'https://checkout.kashier.io/session/7', amount: 219900, currency: 'EGP' })
    const provider = new KashierProvider()

    expect(await provider.pay(proRequest)).toEqual({ status: 'redirect', url: 'https://checkout.kashier.io/session/7' })
    expect(api.checkoutSubscription).toHaveBeenCalledWith('pro', 'yearly', 'card')
  })

  it('sells credit packs by id only: the backend prices the pack and redirects to its hosted URL', async () => {
    vi.mocked(api.initWalletTopUp).mockResolvedValue({ checkout_url: 'https://checkout.kashier.io/session/9', merchant_order_id: 'wallet-9', reference: 'wallet-9' })
    const provider = new KashierProvider()
    const pack: PaymentRequest = { ...proRequest, cart: { type: 'pack', id: '3' }, amount: 1 }
    expect(await provider.pay(pack)).toEqual({ status: 'redirect', url: 'https://checkout.kashier.io/session/9' })
    // the amount on the request is display-only: only the package id and method leave the browser
    expect(api.initWalletTopUp).toHaveBeenCalledWith({ package_id: 3, method: 'card' })
  })

  it('refuses any plan other than Pro: nothing else sells through it', async () => {
    const provider = new KashierProvider()
    await expect(provider.pay({ ...proRequest, cart: { type: 'plan', id: 'free' } })).rejects.toThrow(KASHIER_NOT_CONFIGURED)
  })

  it('fails cleanly for a method Kashier does not take', async () => {
    const provider = new KashierProvider()
    expect(await provider.pay({ ...proRequest, method: 'mada' })).toEqual({ status: 'failed', reason: 'unavailable' })
  })

  it('has no card fields of its own: it redirects to a hosted checkout', () => {
    const provider: PaymentProvider = new KashierProvider()
    expect(provider.CardFields).toBeUndefined()
  })

  it('is not what the app uses by default, whatever the environment', () => {
    for (const env of ['development', 'production']) {
      vi.stubEnv('NODE_ENV', env)
      vi.stubEnv('NEXT_PUBLIC_PAYMENTS_MOCK', '1')
      expect(getPaymentProvider()?.id).not.toBe('kashier')
    }
    vi.unstubAllEnvs()
  })

  it('is used once NEXT_PUBLIC_PAYMENTS_PROVIDER explicitly selects it', () => {
    vi.stubEnv('NEXT_PUBLIC_PAYMENTS_PROVIDER', 'kashier')
    expect(getPaymentProvider()?.id).toBe('kashier')
    vi.unstubAllEnvs()
  })

  it('no longer starts Paymob: the retired value selects no real provider in production', () => {
    vi.stubEnv('NODE_ENV', 'production')
    vi.stubEnv('NEXT_PUBLIC_PAYMENTS_PROVIDER', 'paymob')
    expect(getPaymentProvider()).toBeNull()
    vi.unstubAllEnvs()
  })
})

describe('which payment provider the app uses', () => {
  afterEach(() => vi.unstubAllEnvs())

  it('is the mock in development', () => {
    vi.stubEnv('NODE_ENV', 'development')
    expect(getPaymentProvider()?.isMock).toBe(true)
  })

  it('is none in a production build, so no payment can appear to succeed', () => {
    vi.stubEnv('NODE_ENV', 'production')
    vi.stubEnv('NEXT_PUBLIC_PAYMENTS_MOCK', '')
    expect(getPaymentProvider()).toBeNull()
  })

  it('is the mock in a production build only when a staging site asks for it', () => {
    vi.stubEnv('NODE_ENV', 'production')
    vi.stubEnv('NEXT_PUBLIC_PAYMENTS_MOCK', '1')
    expect(getPaymentProvider()?.isMock).toBe(true)
  })
})
