import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import VerifyCertificatePage from '@/app/verify/[id]/page'
import { useLanguageStore } from '@/lib/language'
import { setParams } from '@/test/nav'
import type { CertificateSummary } from '@/types'

vi.mock('@/lib/api', () => ({ api: { verifyCertificate: vi.fn() } }))
import { api } from '@/lib/api'

const ID = '0f8fad5b-d9cb-469f-a165-70867728950e'
const cert = (over: Partial<CertificateSummary> = {}): CertificateSummary => ({
  certificate_id: ID, track_title: 'AI Developer', user_name: 'Layan Al-Harbi', score: 88,
  issued_at: '2026-09-18T09:30:00Z', is_valid: true, ...over,
})
const httpError = (status: number) => Object.assign(new Error(`HTTP ${status}`), { isAxiosError: true, response: { status } })

beforeEach(() => {
  setParams({ id: ID })
})

// An employer opens this from a QR code or a link: no account, no app shell.
describe('the public verification page', () => {
  it('asks the API about the id in the link, without any sign-in', async () => {
    vi.mocked(api.verifyCertificate).mockResolvedValue(cert())
    render(<VerifyCertificatePage />)
    await screen.findByText('This certificate is valid.')
    expect(api.verifyCertificate).toHaveBeenCalledWith(ID)
    expect(screen.queryByRole('complementary')).toBeNull()
  })

  it('shows a valid certificate as evidence, in English', async () => {
    vi.mocked(api.verifyCertificate).mockResolvedValue(cert())
    render(<VerifyCertificatePage />)

    // (a spinner is a status too, so find the verdict by its words and check what it is)
    expect((await screen.findByText('This certificate is valid.')).closest('[role="status"]')).not.toBeNull()
    expect(screen.getByText('Layan Al-Harbi')).toBeInTheDocument()
    expect(screen.getByText('AI Developer')).toBeInTheDocument()
    expect(screen.getByText('Awarded to').closest('[dir="ltr"]')).not.toBeNull()
  })

  it('says a revoked certificate has been revoked, and still shows it', async () => {
    vi.mocked(api.verifyCertificate).mockResolvedValue(cert({ is_valid: false }))
    render(<VerifyCertificatePage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('This certificate has been revoked.')
    expect(screen.queryByText('This certificate is valid.')).toBeNull()
    expect(screen.getByText('Layan Al-Harbi')).toBeInTheDocument()
  })

  it('says no certificate matches when the link is not one', async () => {
    vi.mocked(api.verifyCertificate).mockRejectedValue(httpError(404))
    render(<VerifyCertificatePage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('No certificate matches this link.')
    expect(screen.queryByText('Awarded to')).toBeNull()
  })

  it('does not call a network failure "not found"', async () => {
    vi.mocked(api.verifyCertificate).mockRejectedValue(new Error('offline'))
    render(<VerifyCertificatePage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Could not check this certificate.')
    expect(screen.queryByText('No certificate matches this link.')).toBeNull()
  })

  it('speaks Arabic around the certificate for an Arabic reader', async () => {
    useLanguageStore.setState({ language: 'ar' })
    vi.mocked(api.verifyCertificate).mockResolvedValue(cert())
    render(<VerifyCertificatePage />)

    expect(await screen.findByText('هذه الشهادة صالحة.')).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('التحقق من الشهادة')
    expect(screen.getByText('Awarded to')).toBeInTheDocument()
  })
})
