import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { ChoiceGroup } from './ChoiceGroup'


describe('ChoiceGroup', () => {
  it('uses the shared dark foreground on a selected yellow choice', () => {
    render(
      <ChoiceGroup
        legend="Experience"
        choices={[{ value: 'beginner', label: 'Beginner' }]}
        value="beginner"
        onChange={vi.fn()}
      />,
    )

    const selected = screen.getByRole('radio', { name: 'Beginner' }).closest('label')
    expect(selected).toHaveClass('bg-amber', 'text-on-amber')
    expect(selected).not.toHaveClass('text-white')
  })
})
