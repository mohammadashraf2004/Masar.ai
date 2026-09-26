import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import CertificatesPage from '@/app/certificates/page'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import { setPathname } from '@/test/nav'
import type { CertificateSummary, User } from '@/types'

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
}))
vi.mock('@/lib/api', () => ({ api: { getMyCertificates: vi.fn(), getWallet: vi.fn(), search: vi.fn() } }))
// Printing is the browser's; what matters here is that the button asks for it.
vi.mock('@/lib/certificates', async (importOriginal) => ({
  ...(await importOriginal<typeof import('@/lib/certificates')>()),
  printCertificate: vi.fn(),
}))
import { api } from '@/lib/api'
import { printCertificate, verifyUrlFor } from '@/lib/certificates'

const ID_NEW = '0f8fad5b-d9cb-469f-a165-70867728950e'
const ID_OLD = '7c9e6679-7425-40de-944b-e07fc1f90ae7'
const cert = (over: Partial<CertificateSummary>): CertificateSummary => ({
  certificate_id: ID_NEW, track_title: 'AI Developer', user_name: 'Layan Al-Harbi', score: 88,
  issued_at: '2026-09-18T09:30:00Z', is_valid: true, ...over,
})
const NEWEST = cert({})
const OLDEST = cert({ certificate_id: ID_OLD, track_title: 'Data Analyst', issued_at: '2026-06-14T09:30:00Z' })

const student: User = {
  id: 1, email: 'layan@example.com', full_name: 'Layan Al-Harbi', role: 'student', experience_level: 'beginner',
  is_verified: true, overall_readiness_score: 42, created_at: '2026-01-01T00:00:00Z',
  requires_legal_acceptance: false, pending_updates: [],
}

const certificateOnPage = () => document.querySelector('.certificate-root') as HTMLElement

beforeEach(() => {
  useAuthStore.setState({ token: 'tok', expiresAt: null, _hasHydrated: true, user: student })
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 100 })
  vi.mocked(api.getMyCertificates).mockResolvedValue([OLDEST, NEWEST])
  vi.mocked(printCertificate).mockClear()
  setPathname('/certificates')
})

describe('the certificates page', () => {
  it('shows the newest certificate, and lists every one newest first', async () => {
    render(<CertificatesPage />)
    await screen.findByText('Certificate history')

    expect(within(certificateOnPage()).getByText('AI Developer')).toBeInTheDocument()
    expect(within(certificateOnPage()).getByText('Layan Al-Harbi')).toBeInTheDocument()
    // an exam certificate: PROFESSIONAL CERTIFICATION, with the exam score in the info row
    expect(within(certificateOnPage()).getByText('PROFESSIONAL CERTIFICATION')).toBeInTheDocument()
    expect(within(certificateOnPage()).getByText('Exam score')).toBeInTheDocument()
    expect(within(certificateOnPage()).getByText('88')).toBeInTheDocument()
    expect(within(certificateOnPage()).getByText('/100')).toBeInTheDocument()

    const rows = within(screen.getByRole('list', { name: 'Certificate history' })).getAllByRole('button')
    expect(rows).toHaveLength(2)
    expect(rows[0]).toHaveTextContent('AI Developer')
    expect(rows[1]).toHaveTextContent('Data Analyst')
    expect(rows[0]).toHaveAttribute('aria-current', 'true')
    expect(rows[1]).not.toHaveAttribute('aria-current')
  })

  it('shows the one you pick', async () => {
    const user = userEvent.setup()
    render(<CertificatesPage />)
    await screen.findByText('Certificate history')

    await user.click(within(screen.getByRole('list', { name: 'Certificate history' })).getByRole('button', { name: /Data Analyst/ }))

    expect(within(certificateOnPage()).getByText('Data Analyst')).toBeInTheDocument()
    expect(within(certificateOnPage()).getByText('14 Jun 2026')).toBeInTheDocument()
    expect(screen.getByLabelText('Verification link')).toHaveValue(verifyUrlFor(ID_OLD))
  })

  it('offers the verification link to copy, and says when it has been copied', async () => {
    const user = userEvent.setup()
    render(<CertificatesPage />)
    await screen.findByText('Certificate history')

    await user.click(screen.getByRole('button', { name: 'Copy verification link' }))

    expect(await navigator.clipboard.readText()).toBe(verifyUrlFor(ID_NEW))
    expect(await screen.findByRole('status')).toHaveTextContent('Link copied')
  })

  it('opens LinkedIn with the verification link, in a new tab that cannot reach back', async () => {
    render(<CertificatesPage />)
    const share = await screen.findByRole('link', { name: /Share on LinkedIn/ })
    expect(share).toHaveAttribute('href', `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(verifyUrlFor(ID_NEW))}`)
    expect(share).toHaveAttribute('target', '_blank')
    expect(share).toHaveAttribute('rel', expect.stringContaining('noopener'))
  })

  it('prints the certificate for "Download PDF"', async () => {
    const user = userEvent.setup()
    render(<CertificatesPage />)
    await user.click(await screen.findByRole('button', { name: /Download PDF/ }))
    expect(printCertificate).toHaveBeenCalledTimes(1)
  })

  it('follows the reader\'s language around the certificate, but the certificate stays English', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<CertificatesPage />)

    expect(await screen.findByText('سجلّ الشهادات')).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('الشهادات')
    expect(screen.getByRole('button', { name: /نسخ رابط التحقّق/ })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /تحميل PDF/ })).toBeInTheDocument()

    expect(certificateOnPage()).toHaveAttribute('dir', 'ltr')
    expect(within(certificateOnPage()).getByText('Awarded to')).toBeInTheDocument()
    // The list row's date is in Arabic (Western digits, as everywhere else in the app).
    expect(screen.getByText(/اختبار مهني · 18 سبتمبر 2026 · 0F8FAD5B/)).toBeInTheDocument()
  })

  describe('with no certificates yet', () => {
    beforeEach(() => {
      vi.mocked(api.getMyCertificates).mockResolvedValue([])
    })

    it('says so and points at the tracks, where the exams are', async () => {
      render(<CertificatesPage />)
      expect(await screen.findByText('No certificates yet')).toBeInTheDocument()
      expect(screen.getByRole('link', { name: 'Browse tracks' })).toHaveAttribute('href', '/tracks')
      expect(certificateOnPage()).toBeNull()
    })

    it('offers no certificate actions with nothing to act on', async () => {
      render(<CertificatesPage />)
      await screen.findByText('No certificates yet')
      expect(screen.queryByRole('button', { name: /Copy verification link/ })).toBeNull()
      expect(screen.queryByRole('button', { name: /Download PDF/ })).toBeNull()
      expect(screen.queryByRole('link', { name: /LinkedIn/ })).toBeNull()
    })

    it('says it in Arabic too', async () => {
      useLanguageStore.setState({ language: 'ar' })
      render(<CertificatesPage />)
      expect(await screen.findByText('لا توجد شهادات بعد')).toBeInTheDocument()
      expect(screen.getByRole('link', { name: 'تصفّح المسارات' })).toHaveAttribute('href', '/tracks')
    })
  })

  it('says when the certificates could not be loaded, and tries again on request', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getMyCertificates).mockRejectedValueOnce(new Error('offline'))
    render(<CertificatesPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load your certificates.')
    await user.click(screen.getByRole('button', { name: 'Try again' }))

    await waitFor(() => expect(within(certificateOnPage()).getByText('AI Developer')).toBeInTheDocument())
    expect(api.getMyCertificates).toHaveBeenCalledTimes(2)
  })
})
