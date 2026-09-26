import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { DifficultyBadge } from '@/components/ui/index'
import { useLanguageStore } from '@/lib/language'

// The API sends the English slug; the reader sees their own language's word for it.
describe('DifficultyBadge', () => {
  it.each([
    ['beginner', 'Beginner', 'مبتدئ'],
    ['intermediate', 'Intermediate', 'متوسط'],
    ['advanced', 'Advanced', 'متقدم'],
  ])('says %s as %s in English and %s in Arabic', (slug, en, ar) => {
    const { unmount } = render(<DifficultyBadge level={slug} />)
    expect(screen.getByText(en)).toBeInTheDocument()
    unmount()

    useLanguageStore.setState({ language: 'ar' })
    render(<DifficultyBadge level={slug} />)
    expect(screen.getByText(ar)).toBeInTheDocument()
    expect(screen.queryByText(slug)).toBeNull()
  })

  it('keeps the colour the level always had: beginner green, intermediate amber, advanced rose', () => {
    render(
      <>
        <DifficultyBadge level="beginner" />
        <DifficultyBadge level="intermediate" />
        <DifficultyBadge level="advanced" />
      </>,
    )
    expect(screen.getByText('Beginner')).toHaveClass('text-emerald')
    expect(screen.getByText('Intermediate')).toHaveClass('text-amber-text')
    expect(screen.getByText('Advanced')).toHaveClass('text-rose')
  })

  it('shows a level it does not know as sent, in a neutral badge, rather than hiding or mistranslating it', () => {
    render(<DifficultyBadge level="expert" />)
    const badge = screen.getByText('expert')
    expect(badge).toHaveClass('text-soft')
    expect(badge).not.toHaveClass('text-emerald', 'text-rose')
  })
})
