import { fireEvent, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import type { ReactNode } from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { CourseViewer } from './CourseViewer'
import { useLanguageStore } from '@/lib/language'
// [code-cell]
import type { Exercise, Lesson, ToolCourse, ToolTopic } from '@/types'
// [/code-cell]

const auth = vi.hoisted(() => ({ user: { id: 1 }, isAuthenticated: true, isLoading: false }))
vi.mock('@/hooks/useAuth', () => ({ useAuth: () => auth }))
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

const topic = (lessons: Lesson[], exercises: Exercise[] = []): ToolTopic => ({
  id: 10, title: 'Topic', slug: 't', description: null, order: 1, difficulty: 'beginner', skill_tags: [],
  technical_terms: [], prerequisite_ids: [], lessons, exercises, quizzes: [], projects: [],
} as unknown as ToolTopic)

const courseWith = (lessons: Lesson[]): ToolCourse => ({
  id: 5, slug: 'course-008', title: 'Vision-Language Models', description: null, icon: null, category: 'curriculum',
  difficulty: 'advanced', estimated_hours: null, related_track_ids: [], technical_terms: [], industry_skills: [],
  topics: [topic(lessons)],
} as unknown as ToolCourse)

beforeEach(() => {
  auth.isAuthenticated = true
  auth.isLoading = false
  vi.mocked(api.getToolCourse).mockReset()
  vi.mocked(api.getCourseProgress).mockResolvedValue({ enrolled: true, progress_percentage: 10 } as never)
})

async function open(lessons: Lesson[]) {
  vi.mocked(api.getToolCourse).mockResolvedValue(courseWith(lessons))
  render(<CourseViewer slug="course-008" curriculum />)
  await screen.findByRole('heading', { name: /Vision-Language Models/ })
}

describe('the lesson viewer with inline figures', () => {
  it('waits for persisted authentication before requesting protected lesson content', async () => {
    auth.isLoading = true
    vi.mocked(api.getToolCourse).mockResolvedValue(courseWith([PLAIN]))
    const view = render(<CourseViewer slug="course-008" curriculum />)

    expect(api.getToolCourse).not.toHaveBeenCalled()

    auth.isLoading = false
    view.rerender(<CourseViewer slug="course-008" curriculum />)
    await screen.findByRole('heading', { name: /Vision-Language Models/ })
    expect(api.getToolCourse).toHaveBeenCalledWith('course-008')
  })

  it('clearly labels the COURSE-016 Kubernetes module as an optional specialization', async () => {
    const optionalCourse = courseWith([PLAIN])
    optionalCourse.slug = 'course-016'
    optionalCourse.title = 'Machine Learning Systems & MLOps Engineering'
    optionalCourse.topics[0].title = 'Kubernetes Operations for ML Workloads'
    optionalCourse.topics[0].completion_required = false
    optionalCourse.topics[0].is_optional = true
    vi.mocked(api.getToolCourse).mockResolvedValue(optionalCourse)

    render(<CourseViewer slug="course-016" curriculum />)
    await screen.findByRole('heading', { name: /Machine Learning Systems/ })

    expect(screen.getAllByText('Optional Kubernetes specialization').length).toBeGreaterThan(0)
  })

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
    const openLesson = screen.getByRole('link', { name: 'Open lesson' })
    expect(openLesson).toHaveAttribute(
      'href', '/courses/course-008/lessons/2',
    )
    expect(
      openLesson.compareDocumentPosition(screen.getByRole('heading', { name: 'Plain heading' }))
      & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy()
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
    expect(screen.getByText('Locked lesson')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Open lesson' })).toHaveAttribute(
      'href', '/courses/course-008/lessons/5',
    )
    expect(screen.getByText(/Purchase this course/)).toBeInTheDocument()
    expect(document.querySelector('figure')).toBeNull()
  })

  // [code-cell]
  it('uses the code cell for a canonical course exercise without starter code', async () => {
    const course = courseWith([PLAIN])
    course.topics[0] = topic([PLAIN], [{
      id: 81,
      title: 'Architecture exercise',
      description: 'Write a small Python answer.',
      exercise_type: 'code',
      language: 'python',
      grading_available: true,
      difficulty: 'intermediate',
      skill_tested: ['python'],
    }])
    vi.mocked(api.getToolCourse).mockResolvedValue(course)
    render(<CourseViewer slug="course-008" curriculum />)
    await screen.findByRole('heading', { name: /Vision-Language Models/ })
    await userEvent.click(screen.getByRole('button', { name: /^Exercises/ }))
    expect(await screen.findByRole('textbox', { name: 'architecture_exercise.py' })).toHaveValue('# Write your solution here\n')
    expect(screen.getByRole('tab', { name: 'architecture_exercise.py' })).toHaveAttribute('aria-selected', 'true')
    expect(screen.queryByRole('tab', { name: 'tests.py' })).toBeNull()
    expect(screen.getByTestId('course-page-scroll')).toHaveClass('flex-1', 'overflow-y-auto', 'overflow-x-hidden')
    expect(screen.getByTestId('course-content-scroll')).not.toHaveClass('overflow-y-auto')
  })
  // [/code-cell]

  it('keeps the section switcher visible and compacts the topic rail while reading', async () => {
    await open([PLAIN])

    expect(screen.getByTestId('course-section-switcher')).toHaveClass('sticky', 'top-0')
    const scroller = screen.getByTestId('course-page-scroll')
    const rail = screen.getByTestId('course-topic-rail')
    expect(rail).toHaveClass('lg:w-56', 'xl:w-64')

    fireEvent.scroll(scroller, { target: { scrollTop: 120 } })
    expect(rail).toHaveClass('lg:w-20')

    fireEvent.scroll(scroller, { target: { scrollTop: 0 } })
    expect(rail).toHaveClass('lg:w-56', 'xl:w-64')
  })

  it('moves through available exercises and quizzes with the bottom Next button', async () => {
    const course = courseWith([PLAIN])
    course.topics[0] = {
      ...topic([PLAIN], [{
        id: 82,
        title: 'Practice the architecture',
        description: 'Write the answer.',
        difficulty: 'beginner',
        skill_tested: [],
      }]),
      quizzes: [{ id: 91, title: 'Topic check', questions: [], passing_score: 70 }],
    }
    vi.mocked(api.getToolCourse).mockResolvedValue(course)
    render(<CourseViewer slug="course-008" curriculum />)
    await screen.findByRole('heading', { name: /Vision-Language Models/ })

    const nextExercises = screen.getByRole('button', { name: 'Next: Exercises' })
    await userEvent.click(nextExercises)

    expect(screen.getByRole('button', { name: /^Exercises/ })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByText('Practice the architecture')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Next: Quiz' })).toBeInTheDocument()
  })

  it('advances from the final quiz or project to the next module', async () => {
    const course = courseWith([PLAIN])
    const firstTopic = {
      ...topic([PLAIN]),
      title: 'Current module',
      quizzes: [{
        id: 92,
        title: 'Final check',
        questions: [],
        passing_score: 70,
        is_locked: true,
        course_slug: 'course-008',
      }],
    }
    const nextTopic = {
      ...topic([lesson({ id: 3, title: 'Next lesson', order: 1 })]),
      id: 11,
      order: 2,
      slug: 'next',
      title: 'Next module',
    }
    course.topics = [firstTopic, nextTopic]
    vi.mocked(api.getToolCourse).mockResolvedValue(course)
    render(<CourseViewer slug="course-008" curriculum />)
    await screen.findByRole('heading', { name: /Vision-Language Models/ })

    await userEvent.click(screen.getByRole('button', { name: /^Quiz/ }))
    const nextModule = screen.getByRole('button', { name: 'Next module: Next module' })
    await userEvent.click(nextModule)

    expect(screen.getByRole('heading', { name: 'Next module' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /^Lessons/ })).toHaveAttribute('aria-pressed', 'true')
  })
})
