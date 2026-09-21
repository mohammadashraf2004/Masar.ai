import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { useRef, useState } from 'react'
import { describe, expect, it, vi } from 'vitest'
import { Modal } from '@/components/ui/Modal'
import { useLanguageStore } from '@/lib/language'

function Harness({ onClose = () => {}, withDescription = true }: { onClose?: () => void; withDescription?: boolean }) {
  const main = useRef<HTMLButtonElement>(null)
  return (
    <>
      <button>Before</button>
      <Modal
        title="A title"
        description={withDescription ? 'A description' : undefined}
        onClose={onClose}
        initialFocus={main}
        footer={<><button ref={main}>Main</button><button>Other</button></>}
      >
        <a href="/somewhere">A link</a>
      </Modal>
      <button>After</button>
    </>
  )
}

describe('Modal', () => {
  it('is a modal dialog with an accessible name and description', () => {
    render(<Harness />)
    const dialog = screen.getByRole('dialog', { name: 'A title' })
    expect(dialog).toHaveAttribute('aria-modal', 'true')
    expect(dialog).toHaveAccessibleDescription('A description')
    expect(screen.getByRole('heading', { name: 'A title' })).toBeInTheDocument()
  })

  it('has no description attribute when there is no description to point at', () => {
    render(<Harness withDescription={false} />)
    expect(screen.getByRole('dialog')).not.toHaveAttribute('aria-describedby')
  })

  it('moves focus in, to the main action', () => {
    render(<Harness />)
    expect(screen.getByRole('button', { name: 'Main' })).toHaveFocus()
  })

  it('takes focus itself when it names no main action', () => {
    render(<Modal title="T" onClose={() => {}}><p>x</p></Modal>)
    expect(screen.getByRole('dialog')).toHaveFocus()
  })

  it('keeps Tab inside: forward from the last control wraps to the first, and Shift+Tab wraps back', async () => {
    render(<Harness />)
    const close = screen.getByRole('button', { name: 'Close' })
    const other = screen.getByRole('button', { name: 'Other' })
    other.focus()
    await userEvent.tab()
    expect(close).toHaveFocus()
    await userEvent.tab({ shift: true })
    expect(other).toHaveFocus()
    expect(screen.getByRole('button', { name: 'After' })).not.toHaveFocus()
    expect(screen.getByRole('button', { name: 'Before' })).not.toHaveFocus()
  })

  it('pulls focus back in if it ever finds itself outside', async () => {
    render(<Harness />)
    screen.getByRole('button', { name: 'Before' }).focus()
    await userEvent.tab()
    expect(screen.getByRole('button', { name: 'Close' })).toHaveFocus()
  })

  it('dismisses on Escape, and on the close button', async () => {
    const onClose = vi.fn()
    render(<Harness onClose={onClose} />)
    await userEvent.keyboard('{Escape}')
    expect(onClose).toHaveBeenCalledTimes(1)
    await userEvent.click(screen.getByRole('button', { name: 'Close' }))
    expect(onClose).toHaveBeenCalledTimes(2)
  })

  it('is not dismissed by a click on the backdrop — an announcement is closed on purpose', async () => {
    const onClose = vi.fn()
    const { container } = render(<Harness onClose={onClose} />)
    await userEvent.click(container.querySelector('.fixed') as HTMLElement)
    expect(onClose).not.toHaveBeenCalled()
  })

  it('works from the keyboard alone: Enter on a link-like control and Space on a button both activate', async () => {
    const onMain = vi.fn()
    const onLink = vi.fn((e: { preventDefault: () => void }) => e.preventDefault())
    render(
      <Modal title="T" onClose={() => {}} footer={<button onClick={onMain}>Go</button>}>
        <a href="/x" onClick={onLink}>Link</a>
      </Modal>
    )
    screen.getByRole('link', { name: 'Link' }).focus()
    await userEvent.keyboard('{Enter}')
    expect(onLink).toHaveBeenCalledTimes(1)
    screen.getByRole('button', { name: 'Go' }).focus()
    await userEvent.keyboard(' ')
    expect(onMain).toHaveBeenCalledTimes(1)
    await userEvent.keyboard('{Enter}')
    expect(onMain).toHaveBeenCalledTimes(2)
  })

  it('returns focus to where it was when it closes', async () => {
    function Page() {
      const [open, setOpen] = useState(false)
      return (
        <>
          <button onClick={() => setOpen(true)}>Open</button>
          {open && <Modal title="T" onClose={() => setOpen(false)}><p>x</p></Modal>}
        </>
      )
    }
    render(<Page />)
    const opener = screen.getByRole('button', { name: 'Open' })
    await userEvent.click(opener)
    expect(screen.getByRole('dialog')).toHaveFocus()
    await userEvent.keyboard('{Escape}')
    expect(screen.queryByRole('dialog')).toBeNull()
    expect(opener).toHaveFocus()
  })

  it('stays inside a short screen: the panel scrolls, the close button is a real 44px target', () => {
    render(<Harness />)
    const dialog = screen.getByRole('dialog')
    expect(dialog.className).toMatch(/max-h-\[calc\(100dvh-2rem\)\]/)
    expect(dialog.className).toMatch(/overflow-y-auto/)
    expect(screen.getByRole('button', { name: 'Close' })).toHaveClass('h-11', 'w-11')
  })

  it('labels the close button in the reader\'s language', () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<Harness />)
    expect(screen.getByRole('button', { name: 'إغلاق' })).toBeInTheDocument()
  })
})
