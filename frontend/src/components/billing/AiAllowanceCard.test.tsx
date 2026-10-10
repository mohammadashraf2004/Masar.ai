import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { AiAllowanceCard } from '@/components/billing/AiAllowanceCard'
import { useLanguageStore } from '@/lib/language'
import type { AiAllowance } from '@/lib/api'

vi.mock('@/lib/api', () => ({ api: { getAiAllowance: vi.fn() } }))
import { api } from '@/lib/api'

const allowance = (over: Partial<AiAllowance> = {}): AiAllowance => ({
  limit: 50, window_seconds: 14400, used: 15, remaining: 35, next_credit_available_at: null, ...over,
})

function serve(value: AiAllowance | null, { trial = false } = {}) {
  vi.mocked(api.getAiAllowance).mockResolvedValue({
    plan: value || trial ? 'pro' : 'free', ai_allowance: value, all_courses_access: Boolean(value) || trial,
    ai_billing: value ? 'allowance' : 'wallet', trial,
  })
}

beforeEach(() => useLanguageStore.setState({ language: 'en' }))

describe('Pro included AI credits', () => {
  it('shows what the server reports, and explains the rolling window without promising a reset', async () => {
    serve(allowance())
    render(<AiAllowanceCard />)
    expect(await screen.findByText('35 of 50 credits left in the current 4-hour window')).toBeInTheDocument()
    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuenow', '15')
    expect(screen.getByText(/Each use counts for 4 hours, then its credits come back\. Nothing resets all at once\./)).toBeInTheDocument()
    expect(screen.getByText('Your course access never depends on AI credits.')).toBeInTheDocument()
    expect(screen.queryByText(/More AI credits from/)).toBeNull()
  })

  it('at the limit: the agreed message and when the next credits come back', async () => {
    serve(allowance({ used: 50, remaining: 0, next_credit_available_at: '2026-10-08T14:00:00Z' }))
    render(<AiAllowanceCard />)
    expect(await screen.findByRole('status')).toHaveTextContent(
      "You've used your 50 included AI credits for the current 4-hour window. Your course access remains available. " +
      'More AI credits will become available as earlier usage leaves the window.',
    )
    expect(screen.getByText(/^More AI credits from /)).toBeInTheDocument()
    expect(document.body.textContent).not.toMatch(/reset/i)
  })

  it('in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar' })
    serve(allowance({ used: 50, remaining: 0, next_credit_available_at: '2026-10-08T14:00:00Z' }))
    render(<AiAllowanceCard />)
    expect(await screen.findByText('أرصدة الذكاء الاصطناعي المضمّنة')).toBeInTheDocument()
    expect(screen.getByText('متبقٍّ 0 من 50 رصيدًا في نافذة الساعات الأربع الحالية')).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent('يظل وصولك إلى الدورات متاحًا')
    expect(screen.getByText(/^تتوفر أرصدة إضافية بدءًا من /)).toBeInTheDocument()
  })

  it('during the trial: every course is open, AI uses the wallet until the first payment', async () => {
    serve(null, { trial: true })
    render(<AiAllowanceCard />)
    expect(await screen.findByRole('heading', { name: 'AI during your free trial' })).toBeInTheDocument()
    expect(screen.getByText(/AI actions use your wallet credits until your first payment/)).toBeInTheDocument()
    expect(screen.queryByRole('progressbar')).toBeNull()
  })

  it('the trial notice in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar' })
    serve(null, { trial: true })
    render(<AiAllowanceCard />)
    expect(await screen.findByRole('heading', { name: 'الذكاء الاصطناعي خلال تجربتك المجانية' })).toBeInTheDocument()
    expect(screen.getByText(/تُستخدم أرصدة محفظتك لإجراءات الذكاء الاصطناعي حتى أول دفعة/)).toBeInTheDocument()
  })

  it('renders nothing on Free, whose AI actions are paid from the wallet', async () => {
    serve(null)
    const { container } = render(<AiAllowanceCard />)
    await vi.waitFor(() => expect(api.getAiAllowance).toHaveBeenCalled())
    expect(container).toBeEmptyDOMElement()
  })

  it('says so when the usage cannot be loaded', async () => {
    vi.mocked(api.getAiAllowance).mockRejectedValue(new Error('offline'))
    render(<AiAllowanceCard />)
    expect(await screen.findByText('Could not load your AI usage.')).toBeInTheDocument()
  })
})
