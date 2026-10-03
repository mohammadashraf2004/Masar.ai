import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import type { ReactNode } from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { CourseViewer } from './CourseViewer'
import { useLanguageStore } from '@/lib/language'
import type { Lesson, ToolCourse, ToolTopic } from '@/types'

vi.mock('@/hooks/useAuth', () => ({ useAuth: () => ({ user: { id: 1 }, isAuthenticated: true, isLoading: false }) }))
vi.mock('@/components/layout/AppShell', () => ({ AppShell: ({ children }: { children: ReactNode }) => <>{children}</> }))
vi.mock('@/components/layout/PageHeader', () => ({ PageHeader: ({ title }: { title: string }) => <h1>{title}</h1> }))
vi.mock('@/lib/api', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/lib/api')>()
  return {
    ...actual,
    api: { getToolCourse: vi.fn(), getCourseProgress: vi.fn(), getMyToolEnrollments: vi.fn(), updateToolTopicProgress: vi.fn() },
  }
})
import { api, resolveAssetUrl } from '@/lib/api'

const lesson = (over: Partial<Lesson>): Lesson => ({
  id: 1, title: 'Lesson', content: '', order: 1, has_code_examples: false, ...over,
})

const FIGURE_URL = '/learning/courses/course-008/assets/lora-low-rank-adaptation?exp=1&sig=abc'
const image = (key: string, alt: string, caption: string, extra: object = {}) =>
  ({ type: 'image' as const, asset_key: key, url: `/learning/courses/course-008/assets/${key}?exp=1&sig=abc`, alt, caption, ...extra })

const WITH_FIGURES = lesson({
  id: 1, title: 'Low-rank adaptation',
  content: 'ignored when blocks are present',
  blocks: [
    { type: 'markdown', content: '## The idea\n\nLoRA decomposes the update into two small matrices.' },
    { ...image('lora-low-rank-adaptation', 'Two small matrices beside a frozen weight', 'Only the small matrices are trained.'), url: FIGURE_URL },
    { type: 'markdown', content: 'The original weights stay frozen.\n\n```python\nprint("rank")\n```' },
    image('parameter-savings', 'Bar chart of trainable parameters', 'Far fewer trainable parameters', { figure_number: 'Figure 2' }),
    { type: 'markdown', content: 'So far fewer parameters are trained.' },
  ],
})
const PLAIN = lesson({ id: 2, title: 'Plain lesson', content: '## Plain heading\n\nJust prose, no figures.' })

const topic = (lessons: Lesson[]): ToolTopic => ({
  id: 10, title: 'Topic', slug: 't', description: null, order: 1, difficulty: 'beginner', skill_tags: [],
  technical_terms: [], prerequisite_ids: [], lessons, exercises: [], quizzes: [], projects: [],
} as unknown as ToolTopic)

const courseWith = (lessons: Lesson[]): ToolCourse => ({
  id: 5, slug: 'course-008', title: 'Vision-Language Models', description: null, icon: null, category: 'curriculum',
  difficulty: 'advanced', estimated_hours: null, related_track_ids: [], technical_terms: [], industry_skills: [],
  topics: [topic(lessons)],
} as unknown as ToolCourse)

beforeEach(() => {
  vi.mocked(api.getToolCourse).mockReset()
  vi.mocked(api.getCourseProgress).mockResolvedValue({ enrolled: true, progress_percentage: 10 } as never)
})

async function open(lessons: Lesson[]) {
  vi.mocked(api.getToolCourse).mockResolvedValue(courseWith(lessons))
  render(<CourseViewer slug="course-008" curriculum />)
  await screen.findByRole('heading', { name: /Vision-Language Models/ })
}

describe('the lesson viewer with inline figures', () => {
  it('renders each figure between the text blocks the author placed around it, in order', async () => {
    await open([WITH_FIGURES])
    const body = document.querySelector('.lesson-blocks') as HTMLElement
    const parts = Array.from(body.children).map((el) =>
      el.tagName === 'FIGURE' ? `figure:${el.getAttribute('data-figure')}` : `text:${(el.textContent ?? '').slice(0, 8)}`)
    expect(parts).toEqual([
      'text:The idea',
      'figure:lora-low-rank-adaptation',
      'text:The orig',
      'figure:parameter-savings',
      'text:So far f',
    ])
  })

  it('shows alt text, captions and the figure number where the course sets one', async () => {
    await open([WITH_FIGURES])
    expect(screen.getByRole('img', { name: 'Two small matrices beside a frozen weight' })).toHaveAttribute('src', resolveAssetUrl(FIGURE_URL))
    expect(screen.getByText('Only the small matrices are trained.')).toBeInTheDocument()
    expect(screen.getByText('Figure 2 — Far fewer trainable parameters')).toBeInTheDocument()
  })

  it('keeps the rest of the lesson rendering: headings, code and prose around a figure', async () => {
    await open([WITH_FIGURES])
    expect(screen.getByRole('heading', { name: 'The idea' })).toBeInTheDocument()
    expect(document.querySelectorAll('.lesson-blocks pre')).toHaveLength(1)
  })

  it('does not render the raw content when blocks are given, and never shows a marker', async () => {
    await open([WITH_FIGURES])
    expect(screen.queryByText('ignored when blocks are present')).toBeNull()
    expect(document.body.textContent).not.toContain('{{figure')
  })

  it('renders a lesson without figures exactly as before', async () => {
    await open([PLAIN])
    expect(document.querySelector('.lesson-blocks')).toBeNull()
    expect(screen.getByRole('heading', { name: 'Plain heading' })).toBeInTheDocument()
    expect(document.querySelector('figure')).toBeNull()
    expect(document.querySelector('img')).toBeNull()
  })

  it('mixes a lesson with figures and one without in the same topic', async () => {
    const user = userEvent.setup()
    await open([WITH_FIGURES, PLAIN])
    await user.click(screen.getByText('Plain lesson'))
    expect(screen.getByRole('heading', { name: 'Plain heading' })).toBeInTheDocument()
    expect(document.querySelectorAll('figure')).toHaveLength(2)
  })

  it('lets a learner enlarge a figure from inside a lesson', async () => {
    const user = userEvent.setup()
    await open([WITH_FIGURES])
    await user.click(screen.getByRole('button', { name: /Enlarge figure: Two small matrices/ }))
    const dialog = screen.getByRole('dialog')
    expect(within(dialog).getByRole('img')).toHaveAttribute('src', resolveAssetUrl(FIGURE_URL))
  })

  it('shows the Arabic blocks when the lesson has them', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    await open([lesson({
      id: 3, title: 'Lesson', title_ar: 'درس', content: 'English', content_ar: 'عربي',
      blocks: [{ type: 'markdown', content: 'English' }, image('a', 'English alt', 'English caption')],
      blocks_ar: [{ type: 'markdown', content: 'نص عربي' }, image('a', 'وصف الصورة', 'شرح الصورة')],
    })])
    expect(await screen.findByText('نص عربي')).toBeInTheDocument()
    expect(screen.getByRole('img', { name: 'وصف الصورة' })).toBeInTheDocument()
    expect(screen.getByText('شرح الصورة')).toBeInTheDocument()
    expect(screen.queryByText('English caption')).toBeNull()
  })

  it('shows the English blocks, left-to-right, for an Arabic reader of an English-only lesson', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    await open([lesson({
      id: 4, title: 'Lesson', content: 'English body',
      blocks: [{ type: 'markdown', content: 'English body' }, image('a', 'English alt', 'English caption')],
    })])
    expect(await screen.findByText('English caption')).toBeInTheDocument()
    expect(document.querySelector('.lesson-blocks')).toHaveAttribute('dir', 'ltr')
  })

  it('shows neither text nor figures for a locked lesson', async () => {
    await open([lesson({ id: 5, title: 'Locked lesson', is_locked: true, course_slug: 'course-008', content: '', blocks: null })])
    expect(screen.getByText(/Purchase this course/)).toBeInTheDocument()
    expect(document.querySelector('figure')).toBeNull()
  })
})
