import { render, screen, within } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import { LegalFooter } from '@/components/layout/LegalFooter'
import { useLanguageStore } from '@/lib/language'

describe('LegalFooter', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'en', mode: 'english_technical' }))

  it('renders the current year and every destination in English', () => {
    render(<LegalFooter />)
    const footer = screen.getByRole('contentinfo', { name: 'Legal information' })
    expect(footer).toHaveTextContent(`© ${new Date().getFullYear()} Masar Inc.`)
    expect(footer).toHaveTextContent('All rights reserved')
    expect(footer.querySelector('.brand-en')).toHaveTextContent('Masar')
    expect(footer.querySelector('.brand-ar')).toHaveClass('brand-ar')
    expect(within(footer).getByRole('link', { name: 'Terms of Use' })).toHaveAttribute('href', '/terms')
    expect(within(footer).getByRole('link', { name: 'Privacy Policy' })).toHaveAttribute('href', '/privacy')
    expect(within(footer).getByRole('link', { name: 'Refund Policy' })).toHaveAttribute('href', '/refund-policy')
    const linkedin = within(footer).getByRole('link', { name: 'LinkedIn' })
    expect(linkedin).toHaveAttribute(
      'href',
      'https://www.linkedin.com/company/masarai-learning',
    )
    expect(linkedin.parentElement).toContainElement(footer.querySelector('.brand-en'))
    expect(within(footer).getByRole('navigation')).not.toContainElement(linkedin)
    const reference = within(footer).getByText('+201044881008')
    expect(reference).toHaveAttribute('dir', 'ltr')
    expect(linkedin.parentElement).toContainElement(reference)
    expect(linkedin.compareDocumentPosition(reference) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  })

  it('renders the Arabic copy while keeping the company line left-to-right', () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    render(<LegalFooter />)
    const footer = screen.getByRole('contentinfo', { name: 'معلومات قانونية' })
    expect(within(footer).getByRole('link', { name: 'شروط الاستخدام' })).toHaveAttribute('href', '/terms')
    expect(within(footer).getByRole('link', { name: 'سياسة الخصوصية' })).toHaveAttribute('href', '/privacy')
    expect(within(footer).getByRole('link', { name: 'سياسة الاسترداد' })).toHaveAttribute('href', '/refund-policy')
    expect(footer).toHaveTextContent('جميع الحقوق محفوظة')
    expect(footer.querySelector('.brand-ar')).toHaveTextContent('مسار')
    expect(footer.querySelector('.brand-en')).toHaveClass('brand-en')
    expect(within(footer).getByText(`© ${new Date().getFullYear()} Masar Inc.`)).toHaveAttribute('dir', 'ltr')
    expect(within(footer).getByText('+201044881008')).toHaveAttribute('dir', 'ltr')
  })
})
