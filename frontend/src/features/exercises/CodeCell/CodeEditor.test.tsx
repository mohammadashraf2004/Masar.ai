import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { CodeEditor } from './CodeEditor'

describe('CodeEditor', () => {
  it('makes the full code surface focus the editable textarea', () => {
    const { container } = render(
      <CodeEditor value={'first = 1\nsecond = 2'} onChange={vi.fn()} ariaLabel="agent.py" />,
    )

    const textarea = screen.getByRole('textbox', { name: 'agent.py' })
    expect(textarea.parentElement).toHaveStyle({ flex: '1 0 auto' })

    const gutter = container.querySelector('[aria-hidden="true"]')
    expect(gutter).not.toBeNull()
    fireEvent.mouseDown(gutter!)
    expect(textarea).toHaveFocus()
  })
})
