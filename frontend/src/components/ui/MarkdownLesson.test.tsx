import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MarkdownLesson } from './MarkdownLesson'

const LESSON = [
  '# Lesson eyebrow',
  '',
  '## Section',
  '',
  'A paragraph with `inline_code` in it.',
  '',
  '```python',
  'def f():',
  '    return 1',
  '```',
  '',
  '```',
  'A --> B',
  '```',
  '',
  '- one',
  '- two',
  '',
  '> a tip',
  '',
  '| a | b |',
  '|---|---|',
  '| 1 | 2 |',
].join('\n')

function renderLesson(props: { dir?: 'rtl' | 'ltr'; compact?: boolean } = {}) {
  const { container } = render(<MarkdownLesson content={LESSON} dir="ltr" {...props} />)
  return container.querySelector('.lesson-content') as HTMLElement
}

describe('MarkdownLesson typography structure', () => {
  it('sets sizes in the shared stylesheet, not per element', () => {
    const root = renderLesson()
    // Element sizes come from the .lesson-content rules (--lc-* tokens); a
    // Tailwind size/leading/margin class on a block would fight them.
    const styled = root.querySelectorAll('h2, h3, p:not(.text-lc-label), ul, ol, li, pre')
    styled.forEach((el) => {
      expect(el.className).not.toMatch(/(^|\s)(text-(xs|sm|base|lg|xl|\[)|leading-|m[tby]-|space-y)/)
    })
  })

  it('renders each code block as a single <pre>, never nested', () => {
    const root = renderLesson()
    expect(root.querySelectorAll('pre')).toHaveLength(2)
    expect(root.querySelector('pre pre')).toBeNull()
  })

  it('keeps code left-to-right inside an RTL lesson', () => {
    const root = renderLesson({ dir: 'rtl' })
    expect(root.getAttribute('dir')).toBe('rtl')
    root.querySelectorAll('pre, code').forEach((el) => {
      expect(el.getAttribute('dir') === 'ltr' || el.closest('pre')?.getAttribute('dir') === 'ltr').toBe(true)
    })
  })

  it('wraps tables in a scroll container and marks callouts', () => {
    const root = renderLesson()
    expect(root.querySelector('.lesson-table-wrap > table')).not.toBeNull()
    expect(root.querySelector('.lesson-callout')).not.toBeNull()
  })

  it('offers a compact variant that only changes the token scope', () => {
    expect(renderLesson({ compact: true }).classList.contains('lesson-content--compact')).toBe(true)
    expect(renderLesson().classList.contains('lesson-content--compact')).toBe(false)
  })
})

describe('MarkdownLesson with blocks', () => {
  const figure = {
    type: 'image' as const, asset_key: 'fig', url: '/learning/courses/c/assets/fig?exp=1&sig=x', alt: 'A diagram', caption: 'A caption',
  }

  it('renders text runs and figures in the order given, inside one dir-carrying column', () => {
    const { container } = render(
      <MarkdownLesson
        content="ignored"
        dir="rtl"
        blocks={[
          { type: 'markdown', content: 'First run.' },
          figure,
          { type: 'markdown', content: 'Second run.' },
        ]}
      />,
    )
    const column = container.querySelector('.lesson-blocks') as HTMLElement
    expect(column.getAttribute('dir')).toBe('rtl')
    expect(Array.from(column.children).map((el) => el.tagName)).toEqual(['DIV', 'FIGURE', 'DIV'])
    expect(column.children[0].textContent).toBe('First run.')
    expect(column.children[2].textContent).toBe('Second run.')
    expect(container.querySelector('figure img')).toHaveAttribute('alt', 'A diagram')
  })

  it('puts an image exactly where it was placed: at the start, in the middle and at the end', () => {
    const order = (blocks: Parameters<typeof MarkdownLesson>[0]['blocks']) => {
      const { container, unmount } = render(<MarkdownLesson content="x" dir="ltr" blocks={blocks} />)
      const kinds = Array.from(container.querySelector('.lesson-blocks')!.children).map((el) => el.tagName)
      unmount()
      return kinds
    }
    const text = (content: string) => ({ type: 'markdown' as const, content })
    expect(order([figure, text('a'), text('b')])).toEqual(['FIGURE', 'DIV', 'DIV'])
    expect(order([text('a'), figure, text('b')])).toEqual(['DIV', 'FIGURE', 'DIV'])
    expect(order([text('a'), text('b'), figure])).toEqual(['DIV', 'DIV', 'FIGURE'])
  })

  it('shows an Arabic lesson its Arabic alt text and an RTL caption, and an English one its English', () => {
    const arabic = { ...figure, alt: 'تدفق المعالجة في Transformer', caption: 'تتدفق الرموز عبر الانتباه.' }
    const { container, unmount } = render(<MarkdownLesson content="x" dir="rtl" blocks={[arabic]} />)
    expect(screen.getByRole('img', { name: arabic.alt })).toBeInTheDocument()
    const caption = container.querySelector('figcaption') as HTMLElement
    expect(caption.textContent).toBe(arabic.caption)
    // The caption sits in the RTL column and sets no direction of its own, so it reads right to left
    // even when it opens with a Latin word.
    expect(caption.closest('[dir]')).toHaveAttribute('dir', 'rtl')
    expect(caption.hasAttribute('dir')).toBe(false)
    unmount()
    const english = render(<MarkdownLesson content="x" dir="ltr" blocks={[figure]} />)
    expect(screen.getByRole('img', { name: 'A diagram' })).toBeInTheDocument()
    expect(english.container.querySelector('figcaption')?.closest('[dir]')).toHaveAttribute('dir', 'ltr')
  })

  it('never prints the raw image token, and shows a visible note for an image the course no longer has', () => {
    const { container } = render(
      <MarkdownLesson
        content="ignored"
        dir="ltr"
        blocks={[{ type: 'markdown', content: 'Before.' }, { type: 'image_missing', asset_key: 'gone-image' }, { type: 'markdown', content: 'After.' }]}
      />,
    )
    const note = container.querySelector('[data-missing-image="gone-image"]') as HTMLElement
    expect(note).not.toBeNull()
    expect(note).toHaveAttribute('role', 'note')
    expect(note.textContent).toMatch(/could not be loaded/)
    expect(note.textContent).toContain('gone-image') // named outside production, for the author
    expect(Array.from(container.querySelector('.lesson-blocks')!.children)).toHaveLength(3)
  })

  it('shows consecutive images as independent figures, one after the other in source order, with no gallery wrapper', () => {
    const second = { ...figure, asset_key: 'second', alt: 'Second view', caption: 'Second caption' }
    const third = { ...figure, asset_key: 'third', alt: 'Third view', caption: null }
    const { container } = render(
      <MarkdownLesson
        content="ignored"
        dir="ltr"
        blocks={[
          { type: 'markdown', content: 'Before.' },
          figure,
          second,
          third,
          { type: 'markdown', content: 'After.' },
        ]}
      />,
    )
    const column = container.querySelector('.lesson-blocks') as HTMLElement
    expect(Array.from(column.children).map((el) => el.tagName)).toEqual(['DIV', 'FIGURE', 'FIGURE', 'FIGURE', 'DIV'])
    expect(Array.from(column.querySelectorAll('figure')).map((el) => el.getAttribute('data-figure'))).toEqual(['fig', 'second', 'third'])
    expect(screen.getAllByRole('img').map((img) => img.getAttribute('alt'))).toEqual(['A diagram', 'Second view', 'Third view'])
    expect(column.querySelectorAll('figure figure')).toHaveLength(0)
    expect(column.querySelectorAll('figcaption')).toHaveLength(2) // the third has no caption
  })

  it('falls back to the plain content when the lesson has no blocks (null or absent)', () => {
    for (const blocks of [null, undefined]) {
      const { container, unmount } = render(<MarkdownLesson content="Plain body." blocks={blocks} dir="ltr" />)
      expect(container.querySelector('.lesson-blocks')).toBeNull()
      expect(container.querySelector('.lesson-content')?.textContent).toBe('Plain body.')
      unmount()
    }
  })

  it('shows nothing for an empty list of blocks: the API sends one when a body held only authoring markers', () => {
    const { container } = render(<MarkdownLesson content="{{exercise:E1}}" blocks={[]} dir="ltr" />)
    expect(container.querySelector('.lesson-content')).toBeNull()
    expect(container.textContent).toBe('')
  })
})

describe('what the language walkthrough points at', () => {
  it('tags the first technical term of the lesson, and only that one', () => {
    const { container } = render(<MarkdownLesson content={'Retrieval uses Embeddings.\n\nRAG builds on Embeddings again, with RAG named twice.'} />)
    const tagged = container.querySelectorAll('[data-tour="lesson-terms"]')
    expect(tagged).toHaveLength(1)
    // The term itself, set left to right inside the (possibly Arabic) paragraph.
    expect(tagged[0]).toHaveAttribute('dir', 'ltr')
    expect(tagged[0].textContent).toMatch(/^[A-Za-z][\w -]*$/)
  })

  it('tags nothing when the lesson names no term', () => {
    const { container } = render(<MarkdownLesson content={'Nothing technical here.'} />)
    expect(container.querySelector('[data-tour="lesson-terms"]')).toBeNull()
  })
})
