import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { LessonImage } from './LessonImage'
import { resolveAssetUrl } from '@/lib/api'
import { useLanguageStore } from '@/lib/language'
import type { ImageBlock } from '@/types'

const BLOCK: ImageBlock = {
  type: 'image',
  asset_key: 'lora-low-rank-adaptation',
  url: '/learning/courses/course-008/assets/lora-low-rank-adaptation?exp=1&sig=abc',
  alt: 'LoRA adds two small trainable matrices beside a frozen weight matrix',
  caption: 'Low-rank matrices are trained while the original weights stay frozen.',
  figure_number: null,
  width: 800,
  height: 400,
}

describe('LessonImage', () => {
  it('shows the figure with its alt text, caption and the size it will occupy', () => {
    render(<LessonImage block={BLOCK} />)
    const img = screen.getByRole('img', { name: BLOCK.alt })
    expect(img).toHaveAttribute('src', resolveAssetUrl(BLOCK.url))
    expect(img).toHaveAttribute('width', '800')
    expect(img).toHaveAttribute('height', '400')
    expect(screen.getByText(BLOCK.caption as string).tagName).toBe('FIGCAPTION')
  })

  it('never loads before it is about to be seen', () => {
    render(<LessonImage block={BLOCK} />)
    expect(screen.getByRole('img', { name: BLOCK.alt })).toHaveAttribute('loading', 'lazy')
  })

  it('never overflows the column: it scales down, on a light panel that reads in both themes', () => {
    const { container } = render(<LessonImage block={BLOCK} />)
    const img = container.querySelector('img') as HTMLImageElement
    expect(img.className).toMatch(/max-w-full/)
    expect(img.className).toMatch(/h-auto/)
    const frame = img.parentElement as HTMLElement
    expect(frame.className).toMatch(/max-w-full/)
    expect(frame.className).toMatch(/bg-white/)
  })

  it('puts the figure number before the caption only when the course sets one', () => {
    const { rerender } = render(<LessonImage block={BLOCK} />)
    expect(screen.getByText(BLOCK.caption as string)).toBeInTheDocument()
    rerender(<LessonImage block={{ ...BLOCK, figure_number: 'Figure 4.2' }} />)
    expect(screen.getByText(`Figure 4.2 — ${BLOCK.caption}`)).toBeInTheDocument()
    rerender(<LessonImage block={{ ...BLOCK, caption: null, figure_number: null }} />)
    expect(document.querySelector('figcaption')).toBeNull()
  })

  it('does not print the file name or the asset key to the learner', () => {
    const { container } = render(<LessonImage block={BLOCK} />)
    expect(container.textContent).not.toMatch(/\.png|\.jpg|B\d{5}|_HTML|lora-low-rank-adaptation/)
  })

  it('says so when the image cannot be loaded, and keeps the caption', () => {
    const { container } = render(<LessonImage block={BLOCK} />)
    fireEvent.error(container.querySelector('img')!)
    expect(screen.getByText('This figure could not be loaded.')).toBeInTheDocument()
    expect(screen.getByText(BLOCK.caption as string)).toBeInTheDocument()
  })

  it('has its interface text in Arabic', () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    render(<LessonImage block={BLOCK} />)
    expect(screen.getByRole('button', { name: `تكبير الصورة: ${BLOCK.alt}` })).toBeInTheDocument()
  })
})

describe('LessonImage enlarge view', () => {
  const openIt = async () => {
    const user = userEvent.setup()
    render(<LessonImage block={BLOCK} />)
    const trigger = screen.getByRole('button', { name: `Enlarge figure: ${BLOCK.alt}` })
    await user.click(trigger)
    return { user, trigger }
  }

  it('opens a dialog named after the figure, with the enlarged image and its caption', async () => {
    await openIt()
    const dialog = screen.getByRole('dialog', { name: BLOCK.alt })
    expect(dialog).toHaveAttribute('aria-modal', 'true')
    expect(dialog.querySelector('img')).toHaveAttribute('src', resolveAssetUrl(BLOCK.url))
    expect(dialog).toHaveTextContent(BLOCK.caption as string)
  })

  it('takes the whole width on a phone and fits the window on a desktop', async () => {
    await openIt()
    const enlarged = screen.getByRole('dialog').querySelector('img') as HTMLImageElement
    expect(enlarged.className).toMatch(/(^|\s)w-full(\s|$)/)
    expect(enlarged.className).toMatch(/sm:max-h-\[85vh\]/)
  })

  it('moves focus to the close button and closes with it, returning focus to the figure', async () => {
    const { user, trigger } = await openIt()
    const close = screen.getByRole('button', { name: 'Close' })
    expect(close).toHaveFocus()
    await user.click(close)
    expect(screen.queryByRole('dialog')).toBeNull()
    expect(trigger).toHaveFocus()
  })

  it('closes with Escape', async () => {
    const { user, trigger } = await openIt()
    await user.keyboard('{Escape}')
    expect(screen.queryByRole('dialog')).toBeNull()
    expect(trigger).toHaveFocus()
  })

  it('closes when the area outside the figure is tapped, but not when the figure itself is', async () => {
    const { user } = await openIt()
    await user.click(screen.getByRole('dialog').querySelector('img')!)
    expect(screen.getByRole('dialog')).toBeInTheDocument()
    await user.click(screen.getByRole('dialog'))
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('locks page scrolling while open and restores it after', async () => {
    const { user } = await openIt()
    expect(document.body.style.overflow).toBe('hidden')
    await user.keyboard('{Escape}')
    expect(document.body.style.overflow).toBe('')
  })

  it('keeps keyboard focus inside the view', async () => {
    const { user } = await openIt()
    await user.tab()
    expect(screen.getByRole('button', { name: 'Close' })).toHaveFocus()
  })
})
