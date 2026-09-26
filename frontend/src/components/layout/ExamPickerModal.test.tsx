import { render, screen, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ExamPickerModal } from '@/components/layout/ExamPickerModal'
import type { CertificateSummary } from '@/types'

vi.mock('@/lib/api', () => ({
  api: { getMyAttempts: vi.fn(), getMyCertificates: vi.fn(), getMyEnrollments: vi.fn(), getExamsForTrack: vi.fn() },
}))
import { api } from '@/lib/api'

const TRACK = { id: 1, name: 'AI Developer', slug: 'ai-developer' }
const exam = (id: number, title: string) => ({
  id, title, description: `About ${title}`, duration_minutes: 60, total_points: 100, passing_score: 70, max_attempts: 3,
})
const certificate = (over: Partial<CertificateSummary> = {}): CertificateSummary => ({
  certificate_id: '0f8fad5b-d9cb-469f-a165-70867728950e', track_title: 'AI Developer', user_name: 'Layan Al-Harbi',
  score: 88, issued_at: '2026-09-18T09:30:00Z', is_valid: true, ...over,
})

const card = (title: string) => screen.getByRole('heading', { name: title }).parentElement as HTMLElement

beforeEach(() => {
  vi.mocked(api.getMyEnrollments).mockResolvedValue([{ track: TRACK }] as never)
  vi.mocked(api.getExamsForTrack).mockResolvedValue([exam(7, 'AI Developer Certification'), exam(8, 'RAG Certification')])
  vi.mocked(api.getMyAttempts).mockResolvedValue([])
  vi.mocked(api.getMyCertificates).mockResolvedValue([])
})

// The picker marks an exam "Certified" from the certificates API. That API used to send no
// exam id, so the lookup matched nothing and only attempt history could ever mark one.
describe('the exam picker: which exams are certified', () => {
  it('marks the exam a certificate was issued for, from the exam id the certificates API sends', async () => {
    vi.mocked(api.getMyCertificates).mockResolvedValue([certificate({ exam_id: 7 })])
    render(<ExamPickerModal onClose={() => {}} />)
    await screen.findByRole('heading', { name: 'AI Developer Certification' })

    expect(within(card('AI Developer Certification')).getByText('Certified')).toBeInTheDocument()
    expect(within(card('AI Developer Certification')).getByRole('button', { name: 'Retake Exam' })).toBeInTheDocument()
    // and only that one
    expect(within(card('RAG Certification')).getByText('Available')).toBeInTheDocument()
    expect(within(card('RAG Certification')).queryByText('Certified')).toBeNull()
  })

  it('still knows the exam is certified when the attempts could not be loaded', async () => {
    // This is the case the certificate lookup exists for: attempt history failed, the certificates did not.
    vi.mocked(api.getMyAttempts).mockRejectedValue(new Error('offline'))
    vi.mocked(api.getMyCertificates).mockResolvedValue([certificate({ exam_id: 7 })])
    render(<ExamPickerModal onClose={() => {}} />)
    await screen.findByRole('heading', { name: 'AI Developer Certification' })

    expect(within(card('AI Developer Certification')).getByText('Certified')).toBeInTheDocument()
  })

  it('marks nothing from a certificate that carries no exam id, rather than everything', async () => {
    vi.mocked(api.getMyCertificates).mockResolvedValue([certificate({ exam_id: undefined }), certificate({ certificate_id: 'b', exam_id: null })])
    render(<ExamPickerModal onClose={() => {}} />)
    await screen.findByRole('heading', { name: 'AI Developer Certification' })

    expect(screen.queryByText('Certified')).toBeNull()
    expect(screen.getAllByText('Available')).toHaveLength(2)
  })

  it('still marks an exam passed from the attempt history, as before', async () => {
    vi.mocked(api.getMyAttempts).mockResolvedValue([{ exam_id: 8, score: 91, passed: true }])
    render(<ExamPickerModal onClose={() => {}} />)
    await screen.findByRole('heading', { name: 'RAG Certification' })

    expect(within(card('RAG Certification')).getByText('Certified')).toBeInTheDocument()
    expect(within(card('AI Developer Certification')).queryByText('Certified')).toBeNull()
  })
})
