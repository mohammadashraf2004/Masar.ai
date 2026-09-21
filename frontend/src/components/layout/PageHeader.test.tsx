import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { PageHeader } from '@/components/layout/PageHeader'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import type { User } from '@/types'

vi.mock('@/lib/api', () => ({ api: { getWallet: vi.fn() } }))
import { api } from '@/lib/api'

beforeEach(() => {
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 50 })
})

// jsdom has no layout, so what is pinned here is the structure that lets the
// title wrap; that it really does at 320px is checked in a real browser.
describe('PageHeader', () => {
  const LONG_EN = 'Career tracks and the learning paths that lead to a job you want'
  const LONG_AR = 'مسارات مهنية وخطط تعلم تقودك إلى الوظيفة التي تريدها'

  it.each([['English', 'Career tracks'], ['Arabic', 'المسارات المهنية'], ['a long English title', LONG_EN], ['a long Arabic title', LONG_AR]])(
    'lets %s wrap on a phone and truncates it to one line from sm up',
    (_label, title) => {
      render(<PageHeader title={title} />)
      const h1 = screen.getByRole('heading', { level: 1 })
      // Below sm there is no truncation: the only truncate utility is behind sm:
      expect(h1.className.split(/\s+/)).not.toContain('truncate')
      expect(h1).toHaveClass('break-words', 'sm:truncate')
      expect(h1).not.toHaveClass('line-clamp-2')
    },
  )

  it('gives every title room on a phone by letting the controls move to their own row', () => {
    render(<PageHeader title="Career tracks" />)
    const block = screen.getByRole('heading', { level: 1 }).parentElement as HTMLElement
    expect(block).toHaveClass('min-w-[10rem]', 'sm:min-w-0', 'flex-1')
    expect(block.parentElement).toHaveClass('flex-wrap')
  })

  it('does not change the desktop structure: one row, title left, controls right, no clamp', () => {
    render(<PageHeader title="Explore" action={<button type="button">Go</button>} />)
    const h1 = screen.getByRole('heading', { level: 1 })
    const block = h1.parentElement as HTMLElement
    const row = block.parentElement as HTMLElement
    expect(row).toHaveClass('flex')
    expect(block).toHaveClass('sm:min-w-0')
    // the action only leaves DOM order below sm
    const action = screen.getByRole('button', { name: 'Go' }).parentElement as HTMLElement
    expect(action).toHaveClass('order-last', 'sm:order-none', 'w-full', 'sm:w-auto')
  })

  it('lets a sentence-length title wrap onto two lines at every width', () => {
    render(<PageHeader title="Good afternoon, Amira" wrapTitle />)
    const h1 = screen.getByRole('heading', { level: 1 })
    expect(h1).toHaveClass('line-clamp-2', 'break-words')
    expect(h1.className.split(/\s+/)).not.toContain('sm:truncate')
  })

  it('keeps the action controls in the header on a phone', () => {
    render(<PageHeader title="Career tracks" action={<button type="button">New</button>} />)
    expect(screen.getByRole('button', { name: 'New' })).toBeInTheDocument()
  })

  it('lets a long subtitle wrap onto two lines at every width instead of cutting it off on a desktop', () => {
    render(<PageHeader title="Career tracks" subtitle="The curriculum libraries behind your Masar. Browse and enrol in the ones with published lessons." />)
    const sub = screen.getByText(/curriculum libraries/)
    expect(sub).toHaveClass('line-clamp-2')
    expect(sub.className).not.toMatch(/truncate/)
  })
})

describe('PageHeader — the account menu', () => {
  beforeEach(() => {
    useAuthStore.setState({
      token: 'tok', expiresAt: null, _hasHydrated: true,
      user: { full_name: 'Amira Hassan', email: 'amira@example.com', experience_level: 'beginner', role: 'student' } as User,
    })
  })

  it('has a name that is not just an initial, and says whether it is open', async () => {
    const user = userEvent.setup()
    render(<PageHeader title="Explore" />)
    const trigger = screen.getByRole('button', { name: 'Profile menu: Amira Hassan' })
    expect(trigger).toHaveAttribute('type', 'button')
    expect(trigger).toHaveAttribute('aria-expanded', 'false')
    await user.click(trigger)
    expect(trigger).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('link', { name: /Profile & Scorecard/ })).toBeInTheDocument()
  })

  it('closes on Escape and hands focus back to the avatar', async () => {
    const user = userEvent.setup()
    render(<PageHeader title="Explore" />)
    const trigger = screen.getByRole('button', { name: /Profile menu/ })
    await user.click(trigger)
    expect(screen.getByRole('link', { name: /Profile & Scorecard/ })).toBeInTheDocument()
    await user.keyboard('{Escape}')
    expect(screen.queryByRole('link', { name: /Profile & Scorecard/ })).toBeNull()
    expect(trigger).toHaveAttribute('aria-expanded', 'false')
    expect(trigger).toHaveFocus()
  })

  it('closes when the pointer goes elsewhere', async () => {
    const user = userEvent.setup()
    render(<div><PageHeader title="Explore" /><p>elsewhere</p></div>)
    await user.click(screen.getByRole('button', { name: /Profile menu/ }))
    await user.click(screen.getByText('elsewhere'))
    expect(screen.queryByRole('link', { name: /Profile & Scorecard/ })).toBeNull()
  })

  it('is named in Arabic for an Arabic reader', () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<PageHeader title="استكشف" />)
    expect(screen.getByRole('button', { name: 'قائمة الحساب: Amira Hassan' })).toBeInTheDocument()
  })
})
