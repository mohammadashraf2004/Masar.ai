import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import BuyCreditsPage from '@/app/billing/credits/page'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import { setSearch } from '@/test/nav'
import type { CreditPurchase } from '@/lib/api'
import type { User } from '@/types'

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
  useSession: () => ({ user: null, isAuthenticated: true, isLoading: false }), useNextParam: () => null,
}))
vi.mock('@/lib/api', () => ({ api: {
  getWallet: vi.fn(), search: vi.fn(), getBillingCatalog: vi.fn(), getCreditPurchases: vi.fn(),
  getPaymentStatus: vi.fn(), initWalletTopUp: vi.fn(),
} }))
vi.mock('@/lib/billing/payments', async (importOriginal) => ({
  ...(await importOriginal<typeof import('@/lib/billing/payments')>()),
  getPaymentProvider: () => held.provider,
}))
const held = vi.hoisted(() => ({ provider: null as unknown }))
import { api } from '@/lib/api'
import { KashierProvider } from '@/lib/billing/kashierProvider'

const student: User = {
  id: 1, email: 'layan@example.com', full_name: 'Layan Al-Harbi', role: 'student', experience_level: 'beginner',
  is_verified: true, overall_readiness_score: 42, created_at: '2026-01-01T00:00:00Z',
  requires_legal_acceptance: false, pending_updates: [],
}

const PACKS = [
  { id: '1', code: 'starter', name: 'Starter', credits: 50, bonus: 0, price: 29, popular: false },
  { id: '2', code: 'standard', name: 'Standard', credits: 150, bonus: 0, price: 69, popular: false },
  { id: '3', code: 'plus', name: 'Plus', credits: 400, bonus: 0, price: 149, popular: true },
  { id: '4', code: 'power', name: 'Power', credits: 1000, bonus: 0, price: 299, popular: false },
]
const CATALOG = {
  currency: 'EGP', vat_rate: 0.14, prices_include_vat: true, current_plan: 'free' as const,
  plans: [{ id: 'free' as const, monthly: 0, yearly: 0, signup_credits: 40, features: [] }],
  packs: PACKS, offer: null,
}
const order = (over: Partial<CreditPurchase> = {}): CreditPurchase => ({
  reference: 'wallet-abc', package: 'Plus', package_code: 'plus', credits: 400, price: 149, currency: 'EGP',
  status: 'paid', credits_reversed: 0, created_at: '2026-10-01T10:00:00Z', paid_at: '2026-10-01T10:01:00Z', ...over,
})

function renderPage() {
  // No WalletProvider here: the page gets its wallet from AppShell's, as in the app.
  return render(<BuyCreditsPage />)
}

beforeEach(() => {
  useAuthStore.setState({ token: 'tok', expiresAt: null, _hasHydrated: true, user: student })
  useLanguageStore.setState({ language: 'en' })
  setSearch('')
  held.provider = new KashierProvider()
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 130, purchased_credits: 90, included_credits: 40 })
  vi.mocked(api.getBillingCatalog).mockResolvedValue(CATALOG)
  vi.mocked(api.getCreditPurchases).mockResolvedValue([])
  vi.mocked(api.initWalletTopUp).mockResolvedValue({ checkout_url: 'https://checkout.test/x', merchant_order_id: 'wallet-1', reference: 'wallet-1' })
})

describe('Buy credits', () => {
  it('shows the four server-priced packs and highlights Plus as the most popular', async () => {
    renderPage()
    const packs = within(await screen.findByRole('region', { name: 'Credit packs' }))
    expect(packs.getAllByRole('button')).toHaveLength(4)
    expect(packs.getByRole('button', { name: /Starter.*50.*EGP 29/ })).toBeInTheDocument()
    expect(packs.getByRole('button', { name: /Power.*1,000.*EGP 299/ })).toBeInTheDocument()
    const plus = packs.getByRole('button', { name: /Plus/ })
    expect(plus).toHaveTextContent('Most popular')
    expect(plus).toHaveAttribute('aria-pressed', 'true') // preselected
    expect(packs.getByRole('button', { name: /Standard/ })).not.toHaveTextContent('Most popular')
  })

  it('splits the balance into purchased and included credits, and explains the difference', async () => {
    renderPage()
    const balance = within(await screen.findByTestId('credits-balance'))
    await waitFor(() => expect(balance.getByText('130')).toBeInTheDocument())
    expect(balance.getByText('90')).toBeInTheDocument()
    expect(balance.getByText('40')).toBeInTheDocument()
    expect(balance.getByText(/never expire/i)).toBeInTheDocument()
    expect(screen.getByText(/Purchased credits are separate/)).toBeInTheDocument()
  })

  it('starts the checkout for the chosen pack by id only (the server prices it) and redirects', async () => {
    const assign = vi.fn()
    vi.stubGlobal('location', { ...window.location, assign, search: '' })
    const user = userEvent.setup()
    renderPage()
    await user.click(await screen.findByRole('button', { name: /Standard/ }))
    await user.click(screen.getByRole('button', { name: 'Buy credits' }))
    await waitFor(() => expect(assign).toHaveBeenCalledWith('https://checkout.test/x'))
    expect(api.initWalletTopUp).toHaveBeenCalledWith({ package_id: 2, method: 'card' })
    vi.unstubAllGlobals()
  })

  it('says so when too many unpaid orders are open, and nothing was started', async () => {
    vi.mocked(api.initWalletTopUp).mockRejectedValue({ response: { status: 429 } })
    const user = userEvent.setup()
    renderPage()
    await user.click(await screen.findByRole('button', { name: 'Buy credits' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('unpaid credit orders')
  })

  it('cannot buy when payments are not open, or in a test-mode provider', async () => {
    held.provider = null
    renderPage()
    expect(await screen.findByRole('button', { name: 'Buy credits' })).toBeDisabled()
    expect(screen.getByText(/Payments are not open yet/)).toBeInTheDocument()
  })

  it('lists the purchase history with each order’s status', async () => {
    vi.mocked(api.getCreditPurchases).mockResolvedValue([
      order({ reference: 'wallet-1', status: 'paid' }),
      order({ reference: 'wallet-2', package: 'Starter', credits: 50, price: 29, status: 'pending' }),
      order({ reference: 'wallet-3', status: 'partially_refunded', credits_reversed: 100 }),
      order({ reference: 'wallet-4', status: 'chargeback' }),
    ])
    renderPage()
    const history = within(await screen.findByTestId('credits-history-list'))
    expect(await history.findByText('Paid')).toBeInTheDocument()
    expect(history.getByText('Waiting for payment')).toBeInTheDocument()
    expect(history.getByText('Partly refunded')).toBeInTheDocument()
    expect(history.getByText('Disputed')).toBeInTheDocument()
    expect(history.getByText(/100 credits taken back/)).toBeInTheDocument()
  })

  it('shows an empty history message', async () => {
    renderPage()
    expect(await screen.findByText('You have not bought credits yet.')).toBeInTheDocument()
  })
})

describe('coming back from the checkout', () => {
  beforeEach(() => setSearch('reference=wallet-abc'))

  it('confirms only what the server records: paid -> success and a refreshed balance', async () => {
    vi.mocked(api.getPaymentStatus).mockResolvedValue({ kind: 'wallet_topup', status: 'confirmed', order: order() })
    renderPage()
    expect(await screen.findByRole('status')).toHaveTextContent('400 credits were added')
    expect(api.getPaymentStatus).toHaveBeenCalledWith('wallet-abc')
    // the wallet is read again once settled (initial load + refresh)
    await waitFor(() => expect(vi.mocked(api.getWallet).mock.calls.length).toBeGreaterThanOrEqual(2))
  })

  it('says the payment is being confirmed while the server still has it pending', async () => {
    vi.mocked(api.getPaymentStatus).mockResolvedValue({ kind: 'wallet_topup', status: 'pending', order: order({ status: 'pending' }) })
    renderPage()
    expect(await screen.findByRole('status')).toHaveTextContent('confirming your payment')
    expect(screen.queryByText(/were added/)).not.toBeInTheDocument()
  })

  it('shows a failure and adds nothing when the order failed', async () => {
    vi.mocked(api.getPaymentStatus).mockResolvedValue({ kind: 'wallet_topup', status: 'failed', order: order({ status: 'failed' }) })
    renderPage()
    expect(await screen.findByRole('alert')).toHaveTextContent('did not go through')
  })

  it('never claims success from the address alone when the server cannot find the order', async () => {
    vi.mocked(api.getPaymentStatus).mockRejectedValue({ response: { status: 404 } })
    renderPage()
    await waitFor(() => expect(api.getPaymentStatus).toHaveBeenCalled())
    expect(screen.queryByText(/were added/)).not.toBeInTheDocument()
    expect(await screen.findByRole('status')).toBeInTheDocument()
  })
})

describe('Arabic', () => {
  it('is fully in Arabic, and the packs and history use Arabic text', async () => {
    useLanguageStore.setState({ language: 'ar' })
    vi.mocked(api.getCreditPurchases).mockResolvedValue([order({ status: 'refunded', credits_reversed: 400 })])
    renderPage()
    expect(await screen.findByRole('heading', { name: 'شراء الرصيد' })).toBeInTheDocument()
    expect(await screen.findByRole('button', { name: 'اشترِ الرصيد' })).toBeInTheDocument()
    expect(screen.getByRole('region', { name: 'باقات الرصيد' })).toBeInTheDocument()
    expect(await screen.findByText('مستردة')).toBeInTheDocument()
  })
})
