import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
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

  it('falls back to the plain content when there are no blocks (null or empty)', () => {
    for (const blocks of [null, undefined, []]) {
      const { container, unmount } = render(<MarkdownLesson content="Plain body." blocks={blocks} dir="ltr" />)
      expect(container.querySelector('.lesson-blocks')).toBeNull()
      expect(container.querySelector('.lesson-content')?.textContent).toBe('Plain body.')
      unmount()
    }
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
