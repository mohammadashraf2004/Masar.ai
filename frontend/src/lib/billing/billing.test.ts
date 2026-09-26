import { readFileSync } from 'node:fs'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { placeholderCatalogSource } from '@/lib/billing/catalog'
import { currencyLabel, formatMoney } from '@/lib/billing/money'
import { MockPaymentProvider, mockOutcomeFromUrl } from '@/lib/billing/mockPayments'
import { getPaymentProvider, type PaymentProvider, type PaymentRequest } from '@/lib/billing/payments'
import { PAYMOB_NOT_CONFIGURED, PaymobProvider } from '@/lib/billing/paymobProvider'
import {
  formatAmount, installment, monthlyYearTotal, priceOrder, round2, subtotalOf, yearlySavingPercent, yearlyTotal,
} from '@/lib/billing/pricing'
import type { BillingCatalog } from '@/lib/billing/types'
import { timeLeft } from '@/components/billing/OfferBanner'

let catalog: BillingCatalog
beforeEach(async () => {
  catalog = await placeholderCatalogSource.load()
})

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
  it('a yearly plan costs twelve of its monthly-billed-yearly prices', () => {
    const pro = catalog.plans.find((p) => p.id === 'pro')!
    expect(yearlyTotal(pro)).toBe(756)
    expect(monthlyYearTotal(pro)).toBe(948)
    expect(subtotalOf({ type: 'plan', id: 'pro' }, 'yearly', catalog)).toBe(756)
    expect(subtotalOf({ type: 'plan', id: 'pro' }, 'monthly', catalog)).toBe(79)
  })

  it('a pack costs its price, whatever the billing cycle', () => {
    expect(subtotalOf({ type: 'pack', id: 'p2' }, 'yearly', catalog)).toBe(99)
    expect(subtotalOf({ type: 'pack', id: 'p2' }, 'monthly', catalog)).toBe(99)
  })

  it('when prices include VAT the total is the subtotal, with no tax added', () => {
    expect(catalog.pricesIncludeVat).toBe(true)
    const order = priceOrder({ type: 'plan', id: 'pro' }, 'yearly', catalog, null)!
    expect(order).toMatchObject({ subtotal: 756, discount: 0, total: 756, vatIncluded: true, vatPercent: 15 })
    expect(priceOrder({ type: 'pack', id: 'p3' }, 'monthly', catalog, null)).toMatchObject({ subtotal: 229, total: 229 })
  })

  it('says how much of an inclusive total is VAT, without adding it', () => {
    // 756 / 1.15 = 657.39: the VAT inside it is the difference.
    expect(priceOrder({ type: 'plan', id: 'pro' }, 'yearly', catalog, null)!.vat).toBe(98.61)
  })

  it('when prices exclude VAT it is added to the discounted amount, at the catalog rate', () => {
    const exclusive = { ...catalog, pricesIncludeVat: false }
    expect(priceOrder({ type: 'plan', id: 'pro' }, 'yearly', exclusive, null)).toMatchObject({
      subtotal: 756, discount: 0, vat: 113.4, vatPercent: 15, vatIncluded: false, total: 869.4,
    })
    // the discount comes off first, and the tax is on what is left
    expect(priceOrder({ type: 'plan', id: 'pro' }, 'yearly', exclusive, { percent: 30 })).toMatchObject({
      subtotal: 756, discount: 226.8, vat: 79.38, total: 608.58,
    })
  })

  it('uses whatever VAT rate the catalog gives', () => {
    const order = priceOrder({ type: 'pack', id: 'p2' }, 'yearly', { ...catalog, pricesIncludeVat: false, vatRate: 0.05 }, null)!
    expect(order).toMatchObject({ vat: 4.95, vatPercent: 5, total: 103.95 })
  })

  it('takes a promo off the subtotal, rounded to the halala, and that is the total', () => {
    expect(priceOrder({ type: 'plan', id: 'pro' }, 'yearly', catalog, { percent: 30 })).toMatchObject({ subtotal: 756, discount: 226.8, total: 529.2 })
    expect(priceOrder({ type: 'pack', id: 'p1' }, 'yearly', catalog, { percent: 30 })).toMatchObject({ subtotal: 49, discount: 14.7, total: 34.3 })
  })

  it('has no price for something the catalog does not sell', () => {
    expect(priceOrder({ type: 'pack', id: 'nope' }, 'yearly', catalog, null)).toBeNull()
    expect(priceOrder({ type: 'plan', id: 'career' as never }, 'yearly', { ...catalog, plans: [] }, null)).toBeNull()
  })

  it('splits a Tabby payment into four, the first one today', () => {
    expect(installment(756)).toBe(189)
    expect(installment(529.2)).toBe(132.3)
  })

  it('says yearly saves 20% on the best paid plan', () => {
    expect(yearlySavingPercent(catalog.plans)).toBe(20)
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

  it('shows a currency it has no name for by its code', () => {
    expect(currencyLabel('EGP', 'ar')).toBe('EGP')
    expect(formatMoney(99, 'EGP', 'en')).toBe('EGP 99')
  })
})

describe('the placeholder catalog', () => {
  it('says the currency, the VAT rate and that prices include it', () => {
    expect(catalog.currency).toBe('SAR')
    expect(catalog.vatRate).toBe(0.15)
    expect(catalog.pricesIncludeVat).toBe(true)
  })

  it('marks every plan feature line as unconfirmed product copy', () => {
    const source = readFileSync(join(process.cwd(), 'src', 'lib', 'billing', 'catalog.ts'), 'utf8')
    const featureLines = source.split('\n').filter((line) => /'billing\.plan\.\w+\.f\d'/.test(line))
    expect(featureLines.length).toBe(catalog.plans.flatMap((p) => p.features).length)
    for (const line of featureLines) expect(line).toContain('// TODO(product): confirm')
  })

  it('has a plan the account is on, three plans, three packs and an offer', () => {
    expect(catalog.currentPlan).toBe('free')
    expect(catalog.plans.map((p) => p.id)).toEqual(['free', 'pro', 'career'])
    expect(catalog.packs).toHaveLength(3)
    expect(catalog.offer?.code).toBe('MASAR30')
    expect(Date.parse(catalog.offer!.endsAt)).toBeGreaterThan(Date.now())
  })

  it('accepts its own code in any case and refuses any other', async () => {
    expect(await placeholderCatalogSource.validatePromo(' masar30 ')).toEqual({ valid: true, code: 'MASAR30', percent: 30 })
    expect(await placeholderCatalogSource.validatePromo('SAVE50')).toEqual({ valid: false, reason: 'invalid' })
  })
})

describe('the mock payment provider', () => {
  const request: PaymentRequest = {
    cart: { type: 'plan', id: 'pro' }, cycle: 'yearly', method: 'mada', amount: 756, currency: 'SAR', promoCode: null,
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
    expect(await provider.getReceipt(result.invoiceId)).toMatchObject({ invoiceId: result.invoiceId, amount: 756, currency: 'SAR', method: 'mada', cycle: 'yearly' })
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
    expect(body).toContain('SAR 756 (VAT included)')
    click.mockRestore()
  })
})

describe('the Paymob stub', () => {
  it('lists cards and mobile wallets, and nothing the gateway does not take', async () => {
    const provider = new PaymobProvider()
    expect(provider.isMock).toBe(false)
    expect(await provider.listMethods()).toEqual(['card', 'wallet'])
  })

  it('throws "not configured" for everything that would touch money', async () => {
    const provider = new PaymobProvider()
    const request: PaymentRequest = { cart: { type: 'plan', id: 'pro' }, cycle: 'yearly', method: 'card', amount: 756, currency: 'SAR', promoCode: null }
    await expect(provider.pay()).rejects.toThrow('PaymobProvider is not configured')
    await expect(provider.getReceipt()).rejects.toThrow(PAYMOB_NOT_CONFIGURED)
    await expect(provider.downloadInvoice()).rejects.toThrow(PAYMOB_NOT_CONFIGURED)
    expect(request.method).toBe('card')
  })

  it('has no card fields of its own: it redirects to a hosted checkout', () => {
    const provider: PaymentProvider = new PaymobProvider()
    expect(provider.CardFields).toBeUndefined()
  })

  it('is not what the app uses, whatever the environment', () => {
    for (const env of ['development', 'production']) {
      vi.stubEnv('NODE_ENV', env)
      vi.stubEnv('NEXT_PUBLIC_PAYMENTS_MOCK', '1')
      expect(getPaymentProvider()?.id).not.toBe('paymob')
    }
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
