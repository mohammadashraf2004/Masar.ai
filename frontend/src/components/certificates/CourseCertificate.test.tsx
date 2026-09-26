import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { CourseCertificate } from '@/components/certificates/CourseCertificate'
import { useLanguageStore } from '@/lib/language'

const ID = '0f8fad5b-d9cb-469f-a165-70867728950e'
const base = {
  recipient: 'Layan Al-Harbi',
  title: 'AI Developer',
  certificateId: ID,
  issuedAt: '2026-09-18T09:30:00Z',
  verifyUrl: `https://masar.ai/verify/${ID}`,
}

describe('CourseCertificate', () => {
  it('prints the holder, the title, the number, the date and the verification block', () => {
    render(<CourseCertificate {...base} />)
    expect(screen.getByText('Layan Al-Harbi')).toBeInTheDocument()
    expect(screen.getByText('AI Developer')).toBeInTheDocument()
    expect(screen.getByText(`NO. ${ID.toUpperCase()}`)).toBeInTheDocument()
    expect(screen.getByText('18 Sep 2026')).toBeInTheDocument()
    expect(screen.getByText('VERIFIED')).toBeInTheDocument()
    expect(screen.getByText('0F8FAD5B · 2026')).toBeInTheDocument()
    // A real QR code, not a placeholder, and a short address to read it from.
    expect(screen.getByTitle('QR code: verify this certificate').closest('svg')).toBeInTheDocument()
    expect(screen.getByText('masar.ai/verify/0F8FAD5B…')).toBeInTheDocument()
  })

  it('is English and left-to-right whatever the page language is', () => {
    useLanguageStore.setState({ language: 'ar' })
    const { container } = render(<CourseCertificate {...base} />)
    const root = container.firstElementChild as HTMLElement
    expect(root).toHaveAttribute('dir', 'ltr')
    expect(root).toHaveAttribute('lang', 'en')
    expect(screen.getByText('Awarded to')).toBeInTheDocument()
    expect(screen.getByText('Date issued')).toBeInTheDocument()
  })

  it('reads the date in UTC, so the same certificate names the same day everywhere', () => {
    render(<CourseCertificate {...base} issuedAt="2026-09-18T23:59:00Z" />)
    expect(screen.getByText('18 Sep 2026')).toBeInTheDocument()
  })

  describe('the exam variant (what the API can issue today)', () => {
    it('says PROFESSIONAL CERTIFICATION for a passed exam, not a completed course', () => {
      render(<CourseCertificate {...base} variant="exam" examScore={86} />)
      expect(screen.getByText('PROFESSIONAL CERTIFICATION')).toBeInTheDocument()
      expect(screen.getByText('for passing the proctored certification exam for')).toBeInTheDocument()
      expect(screen.queryByText('CERTIFICATE OF COMPLETION')).toBeNull()
      expect(screen.queryByText(/completing every lesson/)).toBeNull()
      expect(screen.queryByText(/career track$/)).toBeNull()
    })

    it('fills the info row with Date issued and Exam score, out of 100', () => {
      render(<CourseCertificate {...base} variant="exam" examScore={86} />)
      expect(screen.getAllByText(/^(Date issued|Exam score|Course duration)$/).map((e) => e.textContent)).toEqual(['Date issued', 'Exam score'])
      expect(screen.getByText('86')).toBeInTheDocument()
      expect(screen.getByText('/100')).toBeInTheDocument()
    })

    it('rounds a fractional score the way the exam page shows it', () => {
      render(<CourseCertificate {...base} variant="exam" examScore={87.6} />)
      expect(screen.getByText('88')).toBeInTheDocument()
    })

    it('leaves the score cell out, rather than guess, when the score is not known', () => {
      render(<CourseCertificate {...base} variant="exam" />)
      expect(screen.queryByText('Exam score')).toBeNull()
      expect(screen.getAllByText(/^(Date issued|Exam score|Course duration)$/)).toHaveLength(1)
    })
  })

  describe("the course variant (the handoff's, and the default)", () => {
    it('is CERTIFICATE OF COMPLETION unless told it is an exam', () => {
      render(<CourseCertificate {...base} />)
      expect(screen.getByText('CERTIFICATE OF COMPLETION')).toBeInTheDocument()
      expect(screen.queryByText('PROFESSIONAL CERTIFICATION')).toBeNull()
    })

    it('adds the parent track and the duration when it has them', () => {
      render(<CourseCertificate {...base} variant="course" trackTitle="AI Engineer" durationHours={24} />)
      expect(screen.getByText('CERTIFICATE OF COMPLETION')).toBeInTheDocument()
      expect(screen.getByText('for completing every lesson, exercise and graded project of')).toBeInTheDocument()
      expect(screen.getByText('A core course of the AI Engineer career track')).toBeInTheDocument()
      expect(screen.getByText('Course duration')).toBeInTheDocument()
      expect(screen.getByText('24')).toBeInTheDocument()
      expect(screen.getByText('hours')).toBeInTheDocument()
    })

    it('fills the info row with Date issued and Course duration, and never an exam score', () => {
      render(<CourseCertificate {...base} variant="course" trackTitle="AI Engineer" durationHours={24} />)
      expect(screen.getAllByText(/^(Date issued|Exam score|Course duration)$/).map((e) => e.textContent)).toEqual(['Date issued', 'Course duration'])
      expect(screen.queryByText('/100')).toBeNull()
    })
  })

  it('sizes in container units and marks itself for the print rules', () => {
    const { container } = render(<CourseCertificate {...base} />)
    const root = container.firstElementChild as HTMLElement
    expect(root).toHaveClass('certificate-root')
    expect(root.style.containerType).toBe('inline-size')
    expect((root.firstElementChild as HTMLElement).style.aspectRatio).toBe('1.414')
  })
})
