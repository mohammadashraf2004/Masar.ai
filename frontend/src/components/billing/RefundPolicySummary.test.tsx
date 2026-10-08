import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import { RefundPolicySummary } from '@/components/billing/RefundPolicySummary'
import { useLanguageStore } from '@/lib/language'

describe('RefundPolicySummary', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'en', mode: 'english_technical' }))

  it('explains review, timing, and cancellation in English', () => {
    render(<RefundPolicySummary />)
    expect(screen.getByRole('heading', { name: 'Refund policy' })).toBeInTheDocument()
    expect(screen.getByText(/submission does not guarantee approval/i)).toBeInTheDocument()
    expect(screen.getByText(/does not automatically refund/i)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Read the complete Refund Policy' })).toHaveAttribute('href', '/refund-policy')
  })

  it('shows the same policy in Arabic', () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    render(<RefundPolicySummary />)
    expect(screen.getByRole('heading', { name: 'سياسة الاسترداد' })).toBeInTheDocument()
    expect(screen.getByText(/لا يعني تقديم الطلب الموافقة عليه/)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'اقرأ سياسة الاسترداد كاملة' })).toHaveAttribute('href', '/refund-policy')
  })
})
