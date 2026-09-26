import { render, screen, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { CreditsBadge } from '@/components/layout/CreditsBadge'
import { WalletProvider } from '@/components/layout/WalletContext'
import { useLanguageStore } from '@/lib/language'

vi.mock('@/lib/api', () => ({ api: { getWallet: vi.fn() } }))
import { api } from '@/lib/api'

const renderBadge = () => render(<WalletProvider><CreditsBadge /></WalletProvider>)

beforeEach(() => {
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 1240 })
})

describe('CreditsBadge', () => {
  it('shows the balance in a pill that links to Plans & offers, where credits are topped up', async () => {
    renderBadge()
    const pill = await screen.findByRole('link', { name: '1240 credits' })
    expect(pill).toHaveAttribute('href', '/billing')
    // The design shows 1,240: thousands separated, Latin digits, in every language.
    expect(pill).toHaveTextContent('1,240')
  })

  it('says what the number is to a screen reader, in the reader’s language', async () => {
    useLanguageStore.setState({ language: 'ar' })
    renderBadge()
    expect(await screen.findByRole('link', { name: '1240 رصيد' })).toBeInTheDocument()
  })

  it('renders nothing until the balance is known, and never a made-up zero', async () => {
    let resolve: (v: { credit_balance: number }) => void = () => {}
    vi.mocked(api.getWallet).mockReturnValue(new Promise((r) => { resolve = r }))
    const { container } = renderBadge()
    expect(container).toBeEmptyDOMElement()
    resolve({ credit_balance: 300 })
    expect(await screen.findByRole('link', { name: '300 credits' })).toBeInTheDocument()
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
    const pill = await screen.findByRole('link', { name: '12 credits' })
    expect(pill).toHaveAttribute('title', 'Low credits — top up')
    expect(pill.className).toContain('text-rose')
  })

  it('is an ordinary pill at 20 credits and above', async () => {
    vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 20 })
    renderBadge()
    const pill = await screen.findByRole('link', { name: '20 credits' })
    expect(pill).toHaveAttribute('title', 'Your credit balance')
    expect(pill.className).not.toContain('text-rose')
  })

  it('holds the 44px touch target below lg', async () => {
    renderBadge()
    expect(await screen.findByRole('link', { name: '1240 credits' })).toHaveClass('min-h-[44px]', 'lg:min-h-0')
  })
})
