import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it } from 'vitest'
import { ThemeToggle } from '@/components/layout/ThemeToggle'
import { useLanguageStore } from '@/lib/language'
import { THEME_STORAGE_KEY } from '@/lib/theme'

afterEach(() => document.documentElement.removeAttribute('data-theme'))

describe('ThemeToggle', () => {
  it('offers both themes as named buttons in a labelled group, dark pressed by default', () => {
    render(<ThemeToggle />)
    expect(screen.getByRole('group', { name: 'Theme' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Dark' })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByRole('button', { name: 'Light' })).toHaveAttribute('aria-pressed', 'false')
  })

  it('switches the document theme, moves the pressed state, and remembers the choice', async () => {
    const user = userEvent.setup()
    render(<ThemeToggle />)
    await user.click(screen.getByRole('button', { name: 'Light' }))
    expect(document.documentElement).toHaveAttribute('data-theme', 'light')
    expect(screen.getByRole('button', { name: 'Light' })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByRole('button', { name: 'Dark' })).toHaveAttribute('aria-pressed', 'false')
    expect(window.localStorage.getItem(THEME_STORAGE_KEY)).toBe('light')

    await user.click(screen.getByRole('button', { name: 'Dark' }))
    expect(document.documentElement).toHaveAttribute('data-theme', 'dark')
    expect(screen.getByRole('button', { name: 'Dark' })).toHaveAttribute('aria-pressed', 'true')
  })

  it('starts on the theme the document already carries (the inline script ran first)', () => {
    document.documentElement.setAttribute('data-theme', 'light')
    render(<ThemeToggle />)
    expect(screen.getByRole('button', { name: 'Light' })).toHaveAttribute('aria-pressed', 'true')
  })

  it('is labelled in Arabic for an Arabic reader: فاتح / داكن', () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<ThemeToggle />)
    expect(screen.getByRole('group', { name: 'المظهر' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'فاتح' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'داكن' })).toHaveAttribute('aria-pressed', 'true')
  })

  it('holds each option to the 44px touch target below lg', () => {
    render(<ThemeToggle />)
    for (const name of ['Light', 'Dark']) {
      expect(screen.getByRole('button', { name })).toHaveClass('min-h-[44px]', 'lg:min-h-0')
    }
  })
})
