import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import BillingPage from '@/app/billing/page'
import { MockPaymentProvider, type MockOutcome } from '@/lib/billing/mockPayments'
import type { PaymentProvider } from '@/lib/billing/payments'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import { router, setPathname } from '@/test/nav'
import type { User } from '@/types'
import type { BillingCatalogApi } from '@/lib/api'

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
  useSession: () => ({ user: null, isAuthenticated: true, isLoading: false }), useNextParam: () => null,
}))
vi.mock('@/lib/api', () => ({ api: {
  getWallet: vi.fn(), search: vi.fn(), getBillingCatalog: vi.fn(), startSubscriptionTrial: vi.fn(),
  getAiAllowance: vi.fn(),
} }))

// The provider is the test's to steer: which outcome it gives, or none at all (payments not open).
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

/** What the backend's /billing/catalog actually returns. */
const CATALOG: BillingCatalogApi = {
  currency: 'EGP', vat_rate: 0.14, prices_include_vat: true, current_plan: 'free' as const,
  plans: [
    { id: 'free' as const, monthly: 0, yearly: 0, signup_credits: 40, features: ['billing.plan.free.f1', 'billing.plan.free.f2', 'billing.plan.free.f3'] },
    { id: 'pro' as const, monthly: 299, yearly: 2199, signup_credits: 0, popular: true, features: ['billing.plan.pro.f1', 'billing.plan.pro.f2', 'billing.plan.pro.f3', 'billing.plan.pro.f4'] },
  ],
  packs: [
    { id: 'p1', credits: 500, bonus: 0, price: 100 },
    { id: 'p2', credits: 1200, bonus: 100, price: 300 },
    { id: 'p3', credits: 3000, bonus: 400, price: 700 },
  ],
  offer: null,
}

function useProvider(outcome: MockOutcome = 'paid'): MockPaymentProvider {
  const provider = new MockPaymentProvider({ delayMs: 0, outcome: () => outcome })
  held.provider = provider
  return provider
}

const total = () => within(screen.getByText('Total').closest('div') as HTMLElement)
const payButton = () => screen.getByRole('button', { name: /^Pay / })
const PRO = 'Pro — All Courses + AI Access'
const plan = (name: string) => within(screen.getByRole('heading', { level: 3, name }).closest('article') as HTMLElement)

async function renderBilling({ methods = true } = {}) {
  render(<BillingPage />)
  await screen.findByRole('heading', { level: 3, name: PRO })
  // the payment methods are the provider's to list, so they arrive a moment after the plans
  if (methods) await screen.findByRole('radio', { name: /mada/ })
}

beforeEach(() => {
  useAuthStore.setState({ token: 'tok', expiresAt: null, _hasHydrated: true, user: student })
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 1240 })
  vi.mocked(api.getBillingCatalog).mockResolvedValue(CATALOG)
  setPathname('/billing')
  window.sessionStorage.clear()
  useProvider()
})

describe('plans & offers: the starting order', () => {
  it('opens on the yearly Pro plan, paid with mada', async () => {
    await renderBilling()
    expect(screen.getByRole('button', { name: 'Yearly', pressed: true })).toBeInTheDocument()
    expect(plan(PRO).getByRole('button', { name: 'Selected' })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByRole('radio', { name: /mada/ })).toBeChecked()
    expect(screen.getByText('Pro plan — Yearly')).toBeInTheDocument()
    expect(payButton()).toHaveTextContent('Pay EGP 2,199')
  })

  it('shows what yearly saves, worked out from the prices (299 x 12 = 3,588 vs 2,199)', async () => {
    await renderBilling()
    expect(screen.getByText('Save 39% yearly')).toBeInTheDocument()
  })

  it('shows each plan with its price, its year total and its features', async () => {
    await renderBilling()
    expect(plan(PRO).getByText('2,199')).toBeInTheDocument()
    expect(plan(PRO).getByText('EGP / year')).toBeInTheDocument()
    expect(plan(PRO).getByText('Billed yearly: EGP 2,199 instead of EGP 3,588 — save EGP 1,389')).toBeInTheDocument()
    expect(plan(PRO).getByText('Full access to every published course: all modules, lessons, exercises, quizzes and projects')).toBeInTheDocument()
    expect(plan(PRO).getByText('50 included AI credits per rolling 4 hours on the paid plan — credits you buy are kept for when they run out')).toBeInTheDocument()
    expect(plan(PRO).getByText('Most popular')).toBeInTheDocument()
    expect(plan('Free').getByText('Free forever')).toBeInTheDocument()
  })

  it('lists the credit packs with their bonuses, and the balance they add to', async () => {
    await renderBilling()
    expect(screen.getByRole('button', { name: /1,200.*EGP 300/ })).toHaveTextContent('+100 free')
    expect(screen.getByRole('button', { name: /500.*EGP 100/ })).not.toHaveTextContent('free')
    // (the sidebar's wallet card shows the same number, so find it by the words beside it)
    expect((await screen.findByText('Your balance')).textContent).toContain('1,240')
  })

  it('says so, rather than showing an empty card, when there are no credit packs', async () => {
    vi.mocked(api.getBillingCatalog).mockResolvedValue({ ...CATALOG, packs: [] })
    await renderBilling()
    expect(screen.getByText('Credit packs are not available right now. Please check back soon.')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Top up credits' })).toBeInTheDocument()
  })
})

describe('the total is VAT-inclusive', () => {
  it('says "VAT included" under the total and adds no tax line', async () => {
    await renderBilling()
    expect(total().getByText('EGP 2,199')).toBeInTheDocument()
    expect(total().getByText('VAT included')).toBeInTheDocument()
    // The words appear once, under the total: no "VAT 14%" line is added to the order.
    expect(screen.getAllByText(/VAT/)).toHaveLength(1)
    expect(screen.queryByText(/14%/)).toBeNull()
  })

  it('charges exactly what the subtotal says when there is no discount', async () => {
    await renderBilling()
    const summary = within(screen.getByText('Order summary').closest('div') as HTMLElement)
    expect(summary.getAllByText('EGP 2,199').length).toBeGreaterThanOrEqual(2)
    expect(payButton()).toHaveTextContent('Pay EGP 2,199')
  })
})

describe('choosing what to buy', () => {
  it('re-prices the plan when the billing cycle changes', async () => {
    const user = userEvent.setup()
    await renderBilling()
    await user.click(screen.getByRole('button', { name: 'Monthly' }))

    expect(screen.getByRole('button', { name: 'Monthly', pressed: true })).toBeInTheDocument()
    expect(plan(PRO).getByText('299')).toBeInTheDocument()
    expect(plan(PRO).getByText('Billed monthly · no automatic renewal · cancel any time')).toBeInTheDocument()
    expect(screen.getByText('Pro plan — Monthly')).toBeInTheDocument()
    expect(payButton()).toHaveTextContent('Pay EGP 299')
  })

  it('replaces the plan with a pack: one item at a time', async () => {
    const user = userEvent.setup()
    await renderBilling()
    await user.click(screen.getByRole('button', { name: /1,200.*EGP 300/ }))

    expect(screen.getByRole('button', { name: /1,200.*EGP 300/ })).toHaveAttribute('aria-pressed', 'true')
    expect(plan(PRO).getByRole('button', { name: 'Choose Pro' })).toBeInTheDocument()
    expect(screen.getByText('1,200 credits', { selector: 'span.text-sm' })).toBeInTheDocument()
    expect(screen.getByText('Includes 100 free bonus credits')).toBeInTheDocument()
    expect(payButton()).toHaveTextContent('Pay EGP 300')
  })

  it('shows the plan the account is on, and does not let it be bought', async () => {
    const user = userEvent.setup()
    await renderBilling()
    const current = plan('Free').getByRole('button', { name: 'Your current plan' })
    expect(current).toHaveAttribute('aria-disabled', 'true')

    await user.click(current)
    expect(plan(PRO).getByRole('button', { name: 'Selected' })).toBeInTheDocument()
    expect(payButton()).toHaveTextContent('Pay EGP 2,199')
  })

  it('does not turn Free or the current Pro plan into a checkout item for a Pro account', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getBillingCatalog).mockResolvedValueOnce({ ...CATALOG, current_plan: 'pro' })
    vi.mocked(api.getAiAllowance).mockResolvedValueOnce({
      plan: 'pro', all_courses_access: true, ai_billing: 'allowance', trial: false,
      ai_allowance: { limit: 50, window_seconds: 14400, used: 0, remaining: 50, next_credit_available_at: null },
    })
    await renderBilling()

    const free = plan('Free').getByRole('button', { name: 'Included with Pro' })
    const pro = plan(PRO).getByRole('button', { name: 'Your current plan' })
    expect(free).toHaveAttribute('aria-disabled', 'true')
    expect(pro).toHaveAttribute('aria-disabled', 'true')
    expect(screen.getByRole('button', { name: /500.*EGP 100/ })).toHaveAttribute('aria-pressed', 'true')
    expect(payButton()).toHaveTextContent('Pay EGP 100')

    await user.click(free)
    await user.click(pro)
    expect(payButton()).toHaveTextContent('Pay EGP 100')
    expect(screen.queryByText('Free plan — Yearly')).toBeNull()
    expect(screen.queryByText('Pro plan — Yearly')).toBeNull()
  })
})

describe('paying', () => {
  it('starts the one-time seven-day trial without sending a payment', async () => {
    const user = userEvent.setup()
    const provider = useProvider()
    const pay = vi.spyOn(provider, 'pay')
    vi.mocked(api.getBillingCatalog).mockResolvedValueOnce({ ...CATALOG, trial_eligible: true })
    vi.mocked(api.startSubscriptionTrial).mockResolvedValueOnce({})
    render(<BillingPage />)

    const start = await screen.findByRole('button', { name: 'Start 7-day free trial' })
    expect(screen.getByText('7-day free trial · no charge today')).toBeInTheDocument()
    expect(screen.getByText('Plan price after trial')).toBeInTheDocument()
    expect(total().getByText('EGP 0')).toBeInTheDocument()
    expect(screen.queryByRole('radio')).toBeNull()
    await user.click(start)

    await waitFor(() => expect(api.startSubscriptionTrial).toHaveBeenCalledWith('pro', 'yearly'))
    expect(pay).not.toHaveBeenCalled()
    expect(router.push).toHaveBeenCalledWith('/billing/orders?trial=started')
  })

  it('lists the five methods, with the provider\'s own card fields and never a card input of ours', async () => {
    const user = userEvent.setup()
    await renderBilling()
    for (const name of ['mada', 'Apple Pay', 'STC Pay', 'Credit card', 'Tabby']) {
      expect(screen.getByRole('radio', { name: new RegExp(name) })).toBeInTheDocument()
    }
    expect(screen.queryByRole('group', { name: 'Card details' })).toBeNull()

    await user.click(screen.getByText('Credit card'))
    expect(screen.getByRole('group', { name: 'Card details' })).toHaveTextContent('HOSTED CARD FIELDS')
    expect(screen.queryByRole('textbox')).toBeNull()
    expect(document.querySelector('input[autocomplete^="cc-"]')).toBeNull()
    expect(payButton()).toBeEnabled()
  })

  it('offers the first quarter to pay today with Tabby', async () => {
    const user = userEvent.setup()
    await renderBilling()
    await user.click(screen.getByText('Tabby'))
    expect(screen.getByRole('button', { name: 'Pay EGP 549.75 today' })).toBeInTheDocument()
  })

  it('sends the order to the provider, then to the success page with the invoice', async () => {
    const user = userEvent.setup()
    const provider = useProvider()
    const pay = vi.spyOn(provider, 'pay')
    await renderBilling()
    await user.click(payButton())

    await waitFor(() => expect(router.push).toHaveBeenCalledWith(expect.stringMatching(/^\/billing\/success\?invoice=INV-\d{4}-\d{2}-\d{2}-\d{4}$/)))
    expect(pay).toHaveBeenCalledWith({
      cart: { type: 'plan', id: 'pro' }, cycle: 'yearly', method: 'mada', amount: 2199, currency: 'EGP', promoCode: null,
    })
  })

  it('disables the button and shows a spinner while the payment is processing, so it cannot be sent twice', async () => {
    const user = userEvent.setup()
    const provider = useProvider()
    let finish: (value: { status: 'paid'; invoiceId: string }) => void = () => {}
    const pay = vi.spyOn(provider, 'pay').mockReturnValue(new Promise((resolve) => { finish = resolve }))
    await renderBilling()
    await user.click(payButton())

    const busy = await screen.findByRole('button', { name: /^Pay / })
    expect(busy).toBeDisabled()
    expect(busy).toHaveAttribute('aria-busy', 'true')
    await user.click(busy)
    expect(pay).toHaveBeenCalledTimes(1)

    finish({ status: 'paid', invoiceId: 'INV-2026-09-26-0001' })
    await waitFor(() => expect(router.push).toHaveBeenCalledWith('/billing/success?invoice=INV-2026-09-26-0001'))
  })

  it.each([
    ['declined', 'The payment was declined. Try another method.'],
    ['cancelled', 'The payment was cancelled. Nothing was charged.'],
    ['unavailable', 'The payment could not be completed. Nothing was charged. Try again in a moment.'],
  ] as const)('says so above the button when the payment is %s, and lets the reader try again', async (outcome, message) => {
    const user = userEvent.setup()
    useProvider(outcome)
    await renderBilling()
    await user.click(payButton())

    expect(await screen.findByRole('alert')).toHaveTextContent(message)
    expect(router.push).not.toHaveBeenCalled()
    expect(payButton()).toBeEnabled()
  })

  it('forgets a failure once the order changes, because it was about the old order', async () => {
    const user = userEvent.setup()
    useProvider('declined')
    await renderBilling()
    await user.click(payButton())
    await screen.findByRole('alert')

    await user.click(screen.getByRole('button', { name: /500.*EGP 100/ }))
    expect(screen.queryByRole('alert')).toBeNull()
  })

  it('says it is a test when the provider is the mock', async () => {
    await renderBilling()
    expect(screen.getByText('Test mode: no money is taken and nothing is added to your account.')).toBeInTheDocument()
  })
})

describe('when payments are not open (no provider)', () => {
  beforeEach(() => {
    held.provider = null as PaymentProvider | null
  })

  it('shows everything, says nothing can be bought yet, and cannot be paid', async () => {
    await renderBilling({ methods: false })
    expect(screen.getByText(/Online payments are temporarily unavailable/)).toBeInTheDocument()
    expect(payButton()).toBeDisabled()
    expect(screen.queryByText(/Test mode/)).toBeNull()
  })

  it('has no list of methods of its own to fall back on', async () => {
    await renderBilling({ methods: false })
    expect(screen.queryByRole('radio')).toBeNull()
    expect(screen.queryByText('Payment method')).toBeNull()
  })
})

describe('what the catalog and the provider decide', () => {
  it('shows only the methods the provider lists, and preselects the first', async () => {
    held.provider = Object.assign(new MockPaymentProvider({ delayMs: 0 }), {
      listMethods: async () => ['card', 'wallet'] as const,
    })
    render(<BillingPage />)
    await screen.findByRole('radio', { name: /Credit card/ })

    expect(screen.getAllByRole('radio').map((r) => r.getAttribute('value'))).toEqual(['card', 'wallet'])
    expect(screen.getByRole('radio', { name: /Credit card/ })).toBeChecked()
    expect(screen.getByRole('radio', { name: /Mobile wallet/ })).toBeInTheDocument()
    expect(screen.queryByRole('radio', { name: /mada/ })).toBeNull()
  })

  it('lets the reader choose another of the listed methods', async () => {
    const user = userEvent.setup()
    await renderBilling()
    await user.click(screen.getByText('Tabby'))
    expect(screen.getByRole('radio', { name: /Tabby/ })).toBeChecked()
  })

  it('adds a VAT line at the catalog rate when the prices do not include VAT', async () => {
    vi.mocked(api.getBillingCatalog).mockResolvedValueOnce({ ...CATALOG, prices_include_vat: false })
    await renderBilling()

    expect(screen.getByText('VAT 14%')).toBeInTheDocument()
    expect(screen.getByText('EGP 307.86')).toBeInTheDocument()
    expect(total().getByText('EGP 2,506.86')).toBeInTheDocument()
    expect(screen.queryByText('VAT included')).toBeNull()
    expect(payButton()).toHaveTextContent('Pay EGP 2,506.86')
  })

  it('shows whatever currency the catalog says, not a hardcoded one', async () => {
    vi.mocked(api.getBillingCatalog).mockResolvedValueOnce({ ...CATALOG, currency: 'USD' })
    await renderBilling()

    expect(plan(PRO).getByText('USD / year')).toBeInTheDocument()
    expect(plan(PRO).getByText('Billed yearly: USD 2,199 instead of USD 3,588 — save USD 1,389')).toBeInTheDocument()
    expect(payButton()).toHaveTextContent('Pay USD 2,199')
  })

  it('takes each plan\'s feature lines from the catalog', async () => {
    vi.mocked(api.getBillingCatalog).mockResolvedValueOnce({
      ...CATALOG,
      plans: [{ id: 'pro', monthly: 299, yearly: 2199, signup_credits: 0, features: ['billing.plan.free.f1'] }],
    })
    await renderBilling()
    expect(plan(PRO).getByText('First 2 lessons of every course')).toBeInTheDocument()
    expect(plan(PRO).queryByText('Full access to every published course: all modules, lessons, exercises, quizzes and projects')).toBeNull()
  })
})

describe('Pro: all courses, included AI credits and plain terms', () => {
  it('states how Pro works before anyone pays: manual renewal, cancellation, Kashier', async () => {
    await renderBilling()
    const terms = within(screen.getByRole('complementary', { name: 'How Pro works' }))
    expect(terms.getByText(/does not renew automatically/)).toBeInTheDocument()
    expect(terms.getByText('Cancel any time: Pro stays until the end of the period you paid for.')).toBeInTheDocument()
    expect(terms.getByText('Payments are processed by Kashier. Masar never sees your card details.')).toBeInTheDocument()
    expect(terms.getByText(/During the trial, AI actions use your wallet credits/)).toBeInTheDocument()
    expect(screen.queryByText(/Renews every month/)).toBeNull()
  })

  it('shows a Pro subscriber their included AI credits and, at the limit, that courses stay open', async () => {
    vi.mocked(api.getBillingCatalog).mockResolvedValueOnce({ ...CATALOG, current_plan: 'pro' })
    vi.mocked(api.getAiAllowance).mockResolvedValue({
      plan: 'pro', all_courses_access: true, ai_billing: 'allowance', trial: false,
      ai_allowance: { limit: 50, window_seconds: 14400, used: 50, remaining: 0, next_credit_available_at: '2026-10-08T14:00:00Z' },
    })
    await renderBilling()
    expect(await screen.findByText('0 of 50 credits left in the current 4-hour window')).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent(
      "You've used your 50 included AI credits for the current 4-hour window. Your course access remains available.",
    )
  })

  it('shows no allowance on Free, whose AI actions are paid from the wallet', async () => {
    await renderBilling()
    expect(screen.queryByText('Included AI credits')).toBeNull()
    expect(api.getAiAllowance).not.toHaveBeenCalled()
  })
})

describe('in Arabic', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'ar' }))

  it('is Arabic throughout, with the currency after the number and "شامل الضريبة" under the total', async () => {
    render(<BillingPage />)
    expect(await screen.findByRole('heading', { level: 1, name: 'الخطط والعروض' })).toBeInTheDocument()
    await screen.findByRole('radio', { name: /مدى/ })

    expect(screen.getByText('وفّر 39% سنوياً')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'سنوي', pressed: true })).toBeInTheDocument()
    expect(screen.getByText('يُدفع سنوياً 2,199 ج.م بدلاً من 3,588 ج.م — وفّر 1,389 ج.م')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'ادفع 2,199 ج.م' })).toBeInTheDocument()

    const totalRow = within(screen.getByText('الإجمالي').closest('div') as HTMLElement)
    expect(totalRow.getByText('2,199 ج.م')).toBeInTheDocument()
    expect(totalRow.getByText('شامل الضريبة')).toBeInTheDocument()
    // no English sentence is left
    for (const english of ['Order summary', 'Payment method', 'VAT included', 'Most popular']) {
      expect(screen.queryByText(english)).toBeNull()
    }
  })

  it('names Pro and its terms in Arabic, and never promises an automatic renewal', async () => {
    render(<BillingPage />)
    expect(await screen.findByRole('heading', { level: 3, name: 'Pro — كل الدورات + الذكاء الاصطناعي' })).toBeInTheDocument()
    expect(screen.getByText(/لا تتجدد خطة Pro تلقائيًا/)).toBeInTheDocument()
    expect(screen.getByText(/50 رصيدًا مضمّنًا للذكاء الاصطناعي/)).toBeInTheDocument()
    expect(screen.queryByText(/تجديد تلقائي/)).toBeNull()
  })

  it('names the methods in Arabic and keeps the brand names as they are', async () => {
    render(<BillingPage />)
    await screen.findByRole('heading', { level: 1, name: 'الخطط والعروض' })
    expect(screen.getByRole('radio', { name: /مدى/ })).toBeChecked()
    expect(screen.getByRole('radio', { name: /Apple Pay/ })).toBeInTheDocument()
    expect(screen.getByRole('radio', { name: /تابي/ })).toBeInTheDocument()
  })
})
