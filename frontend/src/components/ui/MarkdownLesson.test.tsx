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
