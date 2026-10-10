import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { CreditsBadge } from '@/components/layout/CreditsBadge'
import { WalletProvider } from '@/components/layout/WalletContext'
import { useLanguageStore } from '@/lib/language'
import { useAuthStore } from '@/lib/store'

vi.mock('@/lib/api', () => ({ api: { getWallet: vi.fn() } }))
import { api } from '@/lib/api'

const renderBadge = () => render(<WalletProvider><CreditsBadge /></WalletProvider>)

beforeEach(() => {
  useAuthStore.setState({ token: 'test-token', _hasHydrated: true })
  useLanguageStore.setState({ language: 'en' })
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 1240 })
})

describe('CreditsBadge', () => {
  it('shows the balance in a pill', async () => {
    renderBadge()
    const pill = await screen.findByRole('button', { name: '1240 credits' })
    // The design shows 1,240: thousands separated, Latin digits, in every language.
    expect(pill).toHaveTextContent('1,240')
    expect(pill).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('says what the number is to a screen reader, in the reader’s language', async () => {
    useLanguageStore.setState({ language: 'ar' })
    renderBadge()
    expect(await screen.findByRole('button', { name: '1240 رصيد' })).toBeInTheDocument()
  })

  it('renders nothing until the balance is known, and never a made-up zero', async () => {
    let resolve: (v: { credit_balance: number }) => void = () => {}
    vi.mocked(api.getWallet).mockReturnValue(new Promise((r) => { resolve = r }))
    const { container } = renderBadge()
    expect(container).toBeEmptyDOMElement()
    resolve({ credit_balance: 300 })
    expect(await screen.findByRole('button', { name: '300 credits' })).toBeInTheDocument()
  })

  it('stays out of the way when the wallet cannot be read', async () => {
    vi.mocked(api.getWallet).mockRejectedValue(new Error('offline'))
    const { container } = renderBadge()
    await waitFor(() => expect(api.getWallet).toHaveBeenCalled())
    expect(container).toBeEmptyDOMElement()
  })

  it('turns to a warning, and says so, below 20 credits', async () => {
    vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 12 })
    renderBadge()
    const pill = await screen.findByRole('button', { name: '12 credits' })
    expect(pill).toHaveAttribute('title', 'Low credits — top up')
    expect(pill.className).toContain('text-rose')
  })

  it('is an ordinary pill at 20 credits and above', async () => {
    vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 20 })
    renderBadge()
    const pill = await screen.findByRole('button', { name: '20 credits' })
    expect(pill).toHaveAttribute('title', 'Your credit balance')
    expect(pill.className).not.toContain('text-rose')
  })

  it('holds the 44px touch target below lg', async () => {
    renderBadge()
    expect(await screen.findByRole('button', { name: '1240 credits' })).toHaveClass('min-h-[44px]', 'lg:min-h-0')
  })

  describe('the panel it opens', () => {
    it('shows the balance, what credits are for, and an Add credits button to the packs', async () => {
      renderBadge()
      const pill = await screen.findByRole('button', { name: '1240 credits' })
      fireEvent.click(pill)

      const panel = screen.getByRole('dialog', { name: 'Your credit balance' })
      expect(pill).toHaveAttribute('aria-expanded', 'true')
      expect(panel).toHaveTextContent('1,240')
      expect(panel).toHaveTextContent('Your course access never depends on them')
      expect(screen.getByRole('link', { name: 'Add credits' })).toHaveAttribute('href', '/billing/credits')
    })

    it('warns in the panel too when the balance is low', async () => {
      vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 5 })
      renderBadge()
      fireEvent.click(await screen.findByRole('button', { name: '5 credits' }))
      expect(screen.getByRole('dialog')).toHaveTextContent('running low')
    })

    it('is in Arabic when the reader’s language is Arabic', async () => {
      useLanguageStore.setState({ language: 'ar' })
      renderBadge()
      fireEvent.click(await screen.findByRole('button', { name: '1240 رصيد' }))
      expect(screen.getByRole('link', { name: 'إضافة رصيد' })).toHaveAttribute('href', '/billing/credits')
    })

    it('closes on a second press, on Escape, on an outside click, and when Add credits is chosen', async () => {
      renderBadge()
      const pill = await screen.findByRole('button', { name: '1240 credits' })

      fireEvent.click(pill)
      fireEvent.click(pill)
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument()

      fireEvent.click(pill)
      fireEvent.keyDown(document, { key: 'Escape' })
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
      expect(pill).toHaveFocus()

      fireEvent.click(pill)
      fireEvent.mouseDown(document.body)
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument()

      fireEvent.click(pill)
      fireEvent.click(screen.getByRole('link', { name: 'Add credits' }))
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    })
  })
})
