import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { LegalDocumentPage } from '@/components/legal/LegalDocumentPage'
import { useLanguageStore } from '@/lib/language'
import type { LegalDocument } from '@/types'

vi.mock('@/lib/api', () => ({ api: { getLegalDocument: vi.fn() } }))
import { api } from '@/lib/api'

const TERMS: LegalDocument = {
  kind: 'terms', version: '2026-09-01', language: 'en', title: 'Terms of Service',
  intro: 'These terms govern your use of Masar.',
  sections: [
    { heading: '1. Who we are', body: ['Masar is a learning platform.', 'A second paragraph.'] },
    { heading: '2. Your account', body: ['Keep your password secret.'] },
  ],
}
const TERMS_AR: LegalDocument = {
  ...TERMS, language: 'ar', title: 'شروط الخدمة', intro: 'تنظّم هذه الشروط استخدامك لمنصة مسار.',
  sections: [{ heading: '١. من نحن', body: ['مسار منصة تعلّم.'] }],
}

beforeEach(() => {
  vi.mocked(api.getLegalDocument).mockImplementation(async (kind, lang) => ({
    ...(lang === 'ar' ? TERMS_AR : TERMS), kind,
  }))
})

describe('a legal document page', () => {
  it('shows the document the API serves, with its version', async () => {
    render(<LegalDocumentPage kind="terms" />)
    expect(await screen.findByRole('heading', { level: 1, name: 'Terms of Service' })).toBeInTheDocument()
    expect(screen.getByText('Version 2026-09-01')).toBeInTheDocument()
    expect(screen.getByText('These terms govern your use of Masar.')).toBeInTheDocument()
    expect(screen.getAllByRole('heading', { level: 2 }).map((h) => h.textContent)).toEqual(['1. Who we are', '2. Your account'])
    expect(screen.getByText('A second paragraph.')).toBeInTheDocument()
  })

  it('takes the wording and the version from the API — it holds neither itself', async () => {
    vi.mocked(api.getLegalDocument).mockResolvedValue({ ...TERMS, version: '2031-01-01', title: 'Whatever the server says' })
    render(<LegalDocumentPage kind="terms" />)
    expect(await screen.findByRole('heading', { level: 1, name: 'Whatever the server says' })).toBeInTheDocument()
    expect(screen.getByText('Version 2031-01-01')).toBeInTheDocument()
  })

  it('asks for the document of its kind, in the interface language', async () => {
    render(<LegalDocumentPage kind="privacy" />)
    await screen.findByRole('heading', { level: 1 })
    expect(api.getLegalDocument).toHaveBeenCalledWith('privacy', 'en')
  })

  it('shows a loading state, then an error with a retry that recovers', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getLegalDocument).mockRejectedValueOnce(new Error('down'))
    render(<LegalDocumentPage kind="terms" />)
    expect(screen.getByRole('status', { name: 'Loading…' })).toBeInTheDocument()
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load this document.')
    await user.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByRole('heading', { level: 1, name: 'Terms of Service' })).toBeInTheDocument()
  })

  it('links the two documents from the footer, and links back home', async () => {
    render(<LegalDocumentPage kind="terms" />)
    await screen.findByRole('heading', { level: 1 })
    const footer = screen.getByRole('contentinfo')
    expect(within(footer).getByRole('link', { name: 'Terms of Use' })).toHaveAttribute('href', '/terms')
    expect(within(footer).getByRole('link', { name: 'Privacy Policy' })).toHaveAttribute('href', '/privacy')
    expect(screen.getByRole('link', { name: 'Back' })).toHaveAttribute('href', '/')
  })

  it('needs no account: it renders for a signed-out visitor without asking for a session', async () => {
    render(<LegalDocumentPage kind="terms" />)
    expect(await screen.findByRole('article')).toBeInTheDocument()
  })
})

describe('Arabic (RTL)', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' }))

  it('fetches and shows the Arabic text of the same document', async () => {
    render(<LegalDocumentPage kind="terms" />)
    expect(await screen.findByRole('heading', { level: 1, name: 'شروط الخدمة' })).toBeInTheDocument()
    expect(api.getLegalDocument).toHaveBeenCalledWith('terms', 'ar')
    expect(screen.getByText('الإصدار 2026-09-01')).toBeInTheDocument()
    expect(screen.getByText('مسار منصة تعلّم.')).toBeInTheDocument()
  })
})
