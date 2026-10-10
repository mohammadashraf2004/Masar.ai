import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import BillingSuccessPage from '@/app/billing/success/page'
import { MockPaymentProvider } from '@/lib/billing/mockPayments'
import type { PaymentReceipt } from '@/lib/billing/payments'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import { setPathname, setSearch } from '@/test/nav'
import type { User } from '@/types'
import type { BillingCatalogApi } from '@/lib/api'

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
  useSession: () => ({ user: null, isAuthenticated: true, isLoading: false }), useNextParam: () => null,
}))
vi.mock('@/lib/api', () => ({ api: { getWallet: vi.fn(), search: vi.fn(), getBillingCatalog: vi.fn() } }))

const held = vi.hoisted(() => ({ provider: null as unknown }))
vi.mock('@/lib/billing/payments', async (importOriginal) => ({
  ...(await importOriginal<typeof import('@/lib/billing/payments')>()),
  getPaymentProvider: () => held.provider,
}))
import { api } from '@/lib/api'

const student: User = {
  id: 1, email: 'layan@example.com', full_name: 'Layan Al-Harbi', role: 'student', experience_level: 'beginner',
  is_verified: true, overall_readiness_score: 42, created_at: '2026-01-01T00:00:00Z',
  requires_legal_acceptance: false, pending_updates: [],
}

const INVOICE = 'INV-2026-09-26-0418'
const receipt = (over: Partial<PaymentReceipt> = {}): PaymentReceipt => ({
  invoiceId: INVOICE, cart: { type: 'plan', id: 'pro' }, cycle: 'yearly', amount: 756, currency: 'SAR', method: 'mada',
  paidAt: '2026-09-26T09:30:00Z', ...over,
})

function provideReceipt(found: PaymentReceipt | null) {
  const provider = new MockPaymentProvider({ delayMs: 0 })
  vi.spyOn(provider, 'getReceipt').mockResolvedValue(found)
  held.provider = provider
  return provider
}

beforeEach(() => {
  useAuthStore.setState({ token: 'tok', expiresAt: null, _hasHydrated: true, user: student })
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 100 })
  const catalog: BillingCatalogApi = {
    currency: 'EGP', vat_rate: 0.14, prices_include_vat: true, current_plan: 'free',
    plans: [
      { id: 'free', monthly: 0, yearly: 0, signup_credits: 40, features: ['billing.plan.free.f1'] },
      { id: 'pro', monthly: 299, yearly: 2199, signup_credits: 0, popular: true, features: ['billing.plan.pro.f1'] },
    ],
    packs: [{ id: 'p2', credits: 1200, bonus: 100, price: 300 }],
    offer: null,
  }
  vi.mocked(api.getBillingCatalog).mockResolvedValue(catalog)
  setPathname('/billing/success')
  setSearch(`invoice=${INVOICE}`)
})

// The page a payment lands on. It shows what the provider says the invoice was, not what the address claims.
describe('the payment-successful page', () => {
  it('confirms a plan that was bought, with its invoice number', async () => {
    provideReceipt(receipt())
    render(<BillingSuccessPage />)

    expect(await screen.findByRole('heading', { name: 'Payment successful' })).toBeInTheDocument()
    expect(screen.getByText('Your Pro plan (Yearly) is active. Enjoy every track and course.')).toBeInTheDocument()
    expect(screen.getByText(INVOICE)).toHaveAttribute('dir', 'ltr')
  })

  it('confirms a credit pack, counting its bonus credits in', async () => {
    provideReceipt(receipt({ cart: { type: 'pack', id: 'p2' } }))
    render(<BillingSuccessPage />)

    expect(await screen.findByText('1,300 credits are on their way to your wallet.')).toBeInTheDocument()
  })

  it('offers the way home and the invoice', async () => {
    const user = userEvent.setup()
    const provider = provideReceipt(receipt())
    const download = vi.spyOn(provider, 'downloadInvoice').mockResolvedValue()
    render(<BillingSuccessPage />)

    expect(await screen.findByRole('link', { name: 'Back to home' })).toHaveAttribute('href', '/dashboard')
    await user.click(screen.getByRole('button', { name: 'Download invoice' }))
    expect(download).toHaveBeenCalledWith(INVOICE)
  })

  it('says it was a test when the provider is the mock', async () => {
    provideReceipt(receipt())
    render(<BillingSuccessPage />)
    expect(await screen.findByText('Test mode: no money is taken and nothing is added to your account.')).toBeInTheDocument()
  })

  it('does not claim a success for an invoice the provider does not know', async () => {
    provideReceipt(null)
    render(<BillingSuccessPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('We could not find that payment.')
    expect(screen.queryByText('Payment successful')).toBeNull()
    expect(screen.getByRole('link', { name: 'Back to plans' })).toHaveAttribute('href', '/billing')
  })

  it('does not claim a success for a visit with no invoice at all', async () => {
    setSearch('')
    provideReceipt(receipt())
    render(<BillingSuccessPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('We could not find that payment.')
  })

  it('shows nothing of a payment when no provider is open', async () => {
    held.provider = null
    render(<BillingSuccessPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('We could not find that payment.')
  })

  it('reads in Arabic for an Arabic reader', async () => {
    useLanguageStore.setState({ language: 'ar' })
    provideReceipt(receipt())
    render(<BillingSuccessPage />)

    expect(await screen.findByRole('heading', { name: 'تمّ الدفع بنجاح' })).toBeInTheDocument()
    expect(screen.getByText('تمّ تفعيل خطة Pro (سنوي). استمتع بكل المسارات والدورات.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'العودة للرئيسية' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'تحميل الفاتورة' })).toBeInTheDocument()
  })
})
