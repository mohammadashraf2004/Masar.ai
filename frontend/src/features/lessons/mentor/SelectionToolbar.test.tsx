import { createRef } from 'react'
import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { SelectionToolbar, wordCount } from './SelectionToolbar'

function Page({ onAsk = vi.fn() }: { onAsk?: (intent: string, text: string, label: string) => void }) {
  const ref = createRef<HTMLElement>()
  return (
    <div>
      <aside id="aside">The lesson module list</aside>
      <article ref={ref} id="article">
        <p id="long">A Checkpointer captures a snapshot of the graph state after every node.</p>
        <p id="short">Two words</p>
      </article>
      <SelectionToolbar articleRef={ref} onAsk={onAsk as never} />
    </div>
  )
}

function select(id: string) {
  const node = document.getElementById(id)!
  act(() => {
    window.getSelection()!.selectAllChildren(node)
    document.dispatchEvent(new Event('selectionchange'))
  })
}

afterEach(() => { window.getSelection()?.removeAllRanges() })

describe('SelectionToolbar', () => {
  it('counts words', () => {
    expect(wordCount('  a  b\nc ')).toBe(3)
    expect(wordCount('')).toBe(0)
  })

  it('appears over a selection of three or more words inside the article, with five actions', () => {
    render(<Page />)
    expect(screen.queryByRole('toolbar')).toBeNull()
    select('long')
    const bar = screen.getByRole('toolbar', { name: 'Ask the mentor about the selected text' })
    expect(Array.from(bar.querySelectorAll('button')).map((b) => b.textContent)).toEqual(['Explain this', 'Simplify', 'Example', 'Why does it matter?', 'Quiz me'])
  })

  it('stays away from a short selection', () => {
    render(<Page />)
    select('short')
    expect(screen.queryByRole('toolbar')).toBeNull()
  })

  it('stays away from a selection outside the article', () => {
    render(<Page />)
    select('aside')
    expect(screen.queryByRole('toolbar')).toBeNull()
  })

  it('hides on Escape and on scroll', () => {
    render(<Page />)
    select('long')
    act(() => { document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' })) })
    expect(screen.queryByRole('toolbar')).toBeNull()
    select('long')
    expect(screen.getByRole('toolbar')).toBeInTheDocument()
    act(() => { document.dispatchEvent(new Event('scroll')) })
    expect(screen.queryByRole('toolbar')).toBeNull()
  })

  it('hides when the selection is cleared', () => {
    render(<Page />)
    select('long')
    act(() => { window.getSelection()!.removeAllRanges(); document.dispatchEvent(new Event('selectionchange')) })
    expect(screen.queryByRole('toolbar')).toBeNull()
  })

  it('asks the mentor with the chosen intent and the selected text only, then closes', async () => {
    const onAsk = vi.fn()
    render(<Page onAsk={onAsk} />)
    select('long')
    await userEvent.click(screen.getByRole('button', { name: 'Why does it matter?' }))
    expect(onAsk).toHaveBeenCalledWith('WHY', 'A Checkpointer captures a snapshot of the graph state after every node.', 'Why does it matter?')
    expect(screen.queryByRole('toolbar')).toBeNull()
  })

  it('does not take the selection away when a button is pressed', () => {
    render(<Page />)
    select('long')
    const down = new MouseEvent('mousedown', { bubbles: true, cancelable: true })
    screen.getByRole('button', { name: 'Simplify' }).dispatchEvent(down)
    expect(down.defaultPrevented).toBe(true)
  })
})
