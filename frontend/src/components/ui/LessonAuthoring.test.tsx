import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { MarkdownLesson } from './MarkdownLesson'
import { localizedBody } from '@/lib/content-language'
import type { ImageBlock, LessonBlock } from '@/types'

/**
 * Authoring syntax never reaches a learner. The API (the canonical parser of `{{image:..}}`,
 * `{{exercise:..}}` and `[[IMAGE_NEEDED: ..]]`) sends typed blocks; these tests pin what the page
 * does with them, and that it never falls back to printing the raw source.
 */
const RAW = /\{\{\s*(?:image|figure|exercise)|\[\[IMAGE_NEEDED/i

const arabicFigure: ImageBlock = {
  type: 'image',
  asset_key: 'attention-flow',
  url: '/learning/courses/course-008/assets/attention-flow?exp=1&sig=a',
  alt: 'تدفق آلية Attention في Transformer',
  alt_lang: 'ar',
  caption: 'تتدفق الـ Tokens عبر طبقات Attention وتُنتج Context Vectors.',
  caption_lang: 'ar',
  width: 800,
  height: 400,
}

afterEach(() => vi.unstubAllEnvs())

describe('authoring syntax in a lesson', () => {
  it('prints none of it: markdown blocks from the API carry prose only', () => {
    const { container } = render(
      <MarkdownLesson
        content="Fallback body {{exercise:M01.L01.EX01}} [[IMAGE_NEEDED: x]]"
        dir="ltr"
        blocks={[{ type: 'markdown', content: 'Intro.\n\nThen practise.' }]}
      />,
    )
    expect(container.textContent).toContain('Then practise.')
    expect(container.textContent).not.toMatch(RAW)
  })

  it('renders nothing for an empty block list instead of falling back to the raw source', () => {
    const { container } = render(
      <MarkdownLesson content="{{exercise:M01.L01.EX01}}\n\n[[IMAGE_NEEDED: x | y | z]]" dir="ltr" blocks={[]} />,
    )
    expect(container.textContent).toBe('')
    expect(container.textContent).not.toMatch(RAW)
  })

  it('treats an empty block list as an answer: the lesson body is not shown instead', () => {
    const body = localizedBody({ content: '{{exercise:E}}', content_ar: null, blocks: [], blocks_ar: null }, 'en')
    expect(body.blocks).toEqual([])
    expect(localizedBody({ content: 'Plain', content_ar: null, blocks: null, blocks_ar: null }, 'en').blocks).toBeNull()
  })

  it('shows an author-only note for an unresolved image request outside production, as a title and never the marker', () => {
    const blocks: LessonBlock[] = [
      { type: 'markdown', content: 'Before.' },
      { type: 'author_marker', kind: 'image_needed', title: 'Decomposition versus planning' },
      { type: 'markdown', content: 'After.' },
    ]
    const { container } = render(<MarkdownLesson content="x" dir="ltr" blocks={blocks} />)
    const note = container.querySelector('[data-author-note="image_needed"]') as HTMLElement
    expect(note).not.toBeNull()
    expect(note).toHaveAttribute('role', 'note')
    expect(note.textContent).toBe('Image needed: Decomposition versus planning')
    expect(container.textContent).not.toMatch(RAW)
  })

  it('shows a named diagnostic for an exercise marker with no exercise behind it outside production', () => {
    const { container } = render(
      <MarkdownLesson content="x" dir="ltr" blocks={[{ type: 'exercise_missing', exercise_id: 'M01.L02.EX04' }]} />,
    )
    const note = container.querySelector('[data-author-note="exercise_missing"]') as HTMLElement
    expect(note.textContent).toContain('M01.L02.EX04')
    expect(note.textContent).not.toMatch(RAW)
  })

  it('shows neither author note in a production build, even if a development API sent them', () => {
    vi.stubEnv('NODE_ENV', 'production')
    const { container } = render(
      <MarkdownLesson
        content="x"
        dir="ltr"
        blocks={[
          { type: 'markdown', content: 'Only the lesson.' },
          { type: 'author_marker', kind: 'image_needed', title: 'A figure' },
          { type: 'exercise_missing', exercise_id: 'M01.L02.EX04' },
        ]}
      />,
    )
    expect(container.querySelector('[data-author-note]')).toBeNull()
    expect(container.textContent).toBe('Only the lesson.')
  })

  it('still names an image the course no longer has, for the author, and never prints its token', () => {
    const { container } = render(
      <MarkdownLesson content="x" dir="ltr" blocks={[{ type: 'image_missing', asset_key: 'gone-image' }]} />,
    )
    expect(container.querySelector('[data-missing-image="gone-image"]')).not.toBeNull()
    expect(container.textContent).not.toMatch(/\{\{\s*image:/)
  })
})

describe('a figure the course no longer has, in a production build', () => {
  it('shows the generic note only: no key, no marker-shaped text, no diagnostic hook in the DOM', () => {
    vi.stubEnv('NODE_ENV', 'production')
    const { container } = render(
      <MarkdownLesson content="x" dir="ltr" blocks={[{ type: 'image_missing', asset_key: 'gone-image' }]} />,
    )
    const note = container.querySelector('[role="note"]') as HTMLElement
    expect(note).not.toBeNull()
    expect(note.textContent).toMatch(/could not be loaded/)
    expect(container.innerHTML).not.toContain('gone-image')
    expect(container.querySelector('[data-missing-image]')).toBeNull()
  })
})

describe('Arabic figure metadata', () => {
  it('uses the Arabic alt text and an RTL caption that keeps its English terms and punctuation', () => {
    const { container } = render(<MarkdownLesson content="x" dir="rtl" blocks={[arabicFigure]} />)
    expect(screen.getByRole('img', { name: arabicFigure.alt })).toHaveAttribute('lang', 'ar')
    const caption = container.querySelector('figcaption') as HTMLElement
    expect(caption).toHaveAttribute('dir', 'rtl')
    expect(caption).toHaveAttribute('lang', 'ar')
    expect(caption.textContent).toBe(arabicFigure.caption)
    expect(caption.textContent).toContain('Tokens')
    expect(caption.textContent).toContain('Context Vectors')
  })

  it('does not force the English fallback when Arabic text exists', () => {
    const { container } = render(<MarkdownLesson content="x" dir="rtl" blocks={[arabicFigure]} />)
    expect(container.textContent).not.toMatch(/Tokens flow through/)
    expect(container.querySelector('figcaption')?.textContent).toMatch(/[؀-ۿ]/)
  })

  it('keeps an English fallback caption left-to-right inside an Arabic lesson, so its punctuation stays put', () => {
    const fallback: ImageBlock = {
      ...arabicFigure, alt: 'Attention flow', alt_lang: 'en', caption: 'Tokens flow through attention.', caption_lang: 'en',
    }
    const { container } = render(<MarkdownLesson content="x" dir="rtl" blocks={[fallback]} />)
    expect(container.closest('body')).not.toBeNull()
    const caption = container.querySelector('figcaption') as HTMLElement
    expect(caption).toHaveAttribute('dir', 'ltr')
    expect(caption).toHaveAttribute('lang', 'en')
    expect(container.querySelector('.lesson-blocks')).toHaveAttribute('dir', 'rtl')
  })
})
