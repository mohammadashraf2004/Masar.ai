// [code-cell]
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
// [/code-cell]
import userEvent from '@testing-library/user-event'
import type { ReactNode } from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { LessonPage } from './LessonPage'
import { useLanguageStore } from '@/lib/language'
import { DEMO_COURSE_SLUG, DEMO_LESSON_ID } from './mockLesson'
import type { Exercise, Lesson, ToolCourse, ToolTopic } from '@/types'

const auth = vi.hoisted(() => ({ user: { id: 1 }, isAuthenticated: true, isLoading: false }))
vi.mock('@/hooks/useAuth', () => ({ useAuth: () => auth }))
vi.mock('@/components/layout/AppShell', () => ({ AppShell: ({ children }: { children: ReactNode }) => <>{children}</> }))
vi.mock('@/lib/api', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/lib/api')>()
  return {
    ...actual,
    // [code-cell]
    runExerciseTests: vi.fn(),
    submitExercise: vi.fn(),
    getExerciseAttemptState: vi.fn().mockResolvedValue(null),
    // [/code-cell]
    api: {
      getToolCourse: vi.fn(),
      getToolTopicProgress: vi.fn().mockResolvedValue({ lessons_completed: [], exercises_completed: [] }),
      updateToolTopicProgress: vi.fn().mockResolvedValue({}),
      getExerciseAnswer: vi.fn().mockRejectedValue(new Error('no conversation yet')),
      answerExercise: vi.fn(),
    },
  }
})
// [code-cell]
import { api, submitExercise } from '@/lib/api'
// [/code-cell]

// jsdom has no IntersectionObserver; the step switch's scroll tracking is
// covered on its own in useLessonScrollSteps.test.tsx — here it only needs
// to exist without throwing.
class FakeObserver {
  observe = vi.fn()
  disconnect = vi.fn()
}
vi.stubGlobal('IntersectionObserver', FakeObserver)
// jsdom has no scroll layout; AnswerChat scrolls its message list on every
// update, which jsdom doesn't implement.
Element.prototype.scrollIntoView = vi.fn()

beforeEach(() => {
  auth.isAuthenticated = true
  auth.isLoading = false
  useLanguageStore.setState({ language: 'en', mode: 'arabic_first', annotateTerms: true })
  vi.mocked(api.getToolCourse).mockReset()
  vi.mocked(api.updateToolTopicProgress).mockClear()
  vi.mocked(api.answerExercise).mockReset()
})

const lesson = (over: Partial<Lesson>): Lesson => ({
  id: 1, title: 'Lesson', content: '', order: 1, has_code_examples: false, ...over,
})
const exercise = (over: Partial<Exercise>): Exercise => ({
  id: 1, title: 'Exercise', description: 'Do the thing', difficulty: 'beginner', skill_tested: [], ...over,
})
const topic = (over: Partial<ToolTopic>): ToolTopic => ({
  id: 10, title: 'Module', slug: 'm', description: undefined, order: 1, difficulty: 'beginner', skill_tags: [],
  technical_terms: [], prerequisite_ids: [], lessons: [], exercises: [], quizzes: [], projects: [], ...over,
} as ToolTopic)
const courseWith = (topics: ToolTopic[]): ToolCourse => ({
  id: 5, slug: 'real-course', title: 'Real Course', title_ar: null, description: undefined, icon: undefined,
  category: 'curriculum', difficulty: 'intermediate', estimated_hours: null, related_track_ids: [],
  technical_terms: [], industry_skills: [], topics,
} as unknown as ToolCourse)

describe('LessonPage — the design fixture (mock lesson)', () => {
  it('shows the breadcrumb, title and meta row, with the content step active', async () => {
    render(<LessonPage courseSlug={DEMO_COURSE_SLUG} lessonParam={String(DEMO_LESSON_ID)} />)
    await screen.findByRole('heading', { name: 'Continuous memory in LangGraph' })
    expect(screen.getByRole('link', { name: 'AI Engineer' })).toHaveAttribute('href', '/tracks/ai-engineer')
    expect(screen.getByRole('link', { name: 'LangGraph' })).toHaveAttribute('href', `/courses/${DEMO_COURSE_SLUG}`)
    expect(screen.getByText('Lesson 7 of 12')).toBeInTheDocument()
    expect(screen.getByText('15 min read')).toBeInTheDocument()
    expect(screen.getByText('+40 credits')).toBeInTheDocument()
    // A full-width opaque bar, and scroll padding so a focused editor line never sits beneath it.
    expect(screen.getByTestId('lesson-step-switcher')).toHaveClass('sticky', 'top-14', 'lg:top-0', 'border-b', 'bg-void/95')
    expect(screen.getByTestId('lesson-scroll-container')).toHaveClass('max-lg:overflow-x-clip', 'lg:overflow-y-auto', 'lg:scroll-pt-28')
    expect(screen.getByRole('button', { name: '1 Content' })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByRole('button', { name: '2 Exercise' })).toHaveAttribute('aria-pressed', 'false')
    expect(screen.getByRole('button', { name: 'Next: Exercise' })).toBeInTheDocument()
  })

  it('renders the lesson body and the reused exercise card below the divider', async () => {
    render(<LessonPage courseSlug={DEMO_COURSE_SLUG} lessonParam={String(DEMO_LESSON_ID)} />)
    await screen.findByRole('heading', { name: 'Continuous memory in LangGraph' })
    expect(screen.getByText(/What is a Checkpointer/)).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Practice Exercises' })).toBeInTheDocument()
    expect(screen.getByText('Test what you learned in this lesson.')).toBeInTheDocument()
    expect(screen.getByText('Add a Checkpointer so the agent keeps conversation context')).toBeInTheDocument()
    expect(screen.getByText('Exercise 3 of 4')).toBeInTheDocument()
  })

  it('shows the module lesson list with done/current/locked marks, and locked rows are not links', async () => {
    render(<LessonPage courseSlug={DEMO_COURSE_SLUG} lessonParam={String(DEMO_LESSON_ID)} />)
    await screen.findByRole('heading', { name: 'Continuous memory in LangGraph' })
    const aside = screen.getByText('Module lessons').closest('div') as HTMLElement

    const current = within(aside).getByText('Continuous memory').closest('a')
    expect(current).toHaveAttribute('aria-current', 'page')

    const done = within(aside).getByText('State and MessagesState').closest('a')
    expect(done).toHaveAttribute('href', `/courses/${DEMO_COURSE_SLUG}/lessons/1005`)

    const locked = within(aside).getByText('Persisting to disk with SqliteSaver')
    expect(locked.closest('a')).toBeNull()
  })

  it('keeps exercise grading interactive without making it a requirement for lesson navigation', async () => {
    // [code-cell]
    const user = userEvent.setup()
    vi.mocked(submitExercise).mockResolvedValue({
      status: 'correct',
      passed: true,
      stdout: '', stderr: '', execution_time_ms: 4,
      tests_passed: 1, tests_total: 1,
      feedback: { code: 'CORRECT', message: 'Correct!', messages: { en: 'Correct!' } },
    })
    render(<LessonPage courseSlug={DEMO_COURSE_SLUG} lessonParam={String(DEMO_LESSON_ID)} />)
    await screen.findByRole('heading', { name: 'Continuous memory in LangGraph' })
    expect(screen.getByRole('link', { name: 'Next lesson' })).toHaveAttribute(
      'href', `/courses/${DEMO_COURSE_SLUG}/lessons/1008`,
    )

    const editor = await screen.findByRole('textbox', { name: 'add_checkpointer_agent.py' })
    fireEvent.change(editor, { target: { value: 'from langgraph.checkpoint.memory import MemorySaver\n' } })
    await user.click(screen.getByRole('button', { name: 'Check Answer' }))

    expect(await screen.findByText('Correct!')).toBeInTheDocument()
    // The mock lesson has no real topic to persist against — no progress call fires.
    expect(api.updateToolTopicProgress).not.toHaveBeenCalled()

    await user.click(screen.getByRole('button', { name: 'Mark as complete' }))
    expect(screen.getByText('Completed')).toBeInTheDocument()
    expect(api.updateToolTopicProgress).not.toHaveBeenCalled()
    // [/code-cell]
  })
})

describe('LessonPage — a real lesson with no exercise', () => {
  it('waits for auth hydration before loading the protected course payload', async () => {
    auth.isLoading = true
    vi.mocked(api.getToolCourse).mockResolvedValue(courseWith([
      topic({ id: 19, lessons: [lesson({ id: 99, title: 'Hydrated lesson' })] }),
    ]))
    const view = render(<LessonPage courseSlug="real-course" lessonParam="99" />)

    expect(api.getToolCourse).not.toHaveBeenCalled()

    auth.isLoading = false
    view.rerender(<LessonPage courseSlug="real-course" lessonParam="99" />)
    expect(await screen.findByRole('heading', { name: 'Hydrated lesson' })).toBeInTheDocument()
  })

  it('hides the step switch and the divider, and shows "Next lesson" at the end of the article', async () => {
    const l1 = lesson({ id: 101, title: 'First', order: 1 })
    const l2 = lesson({ id: 102, title: 'Second', order: 2 })
    vi.mocked(api.getToolCourse).mockResolvedValue(courseWith([topic({ id: 20, lessons: [l1, l2], exercises: [] })]))

    render(<LessonPage courseSlug="real-course" lessonParam="101" />)
    await screen.findByRole('heading', { name: 'First' })

    expect(screen.queryByRole('button', { name: '1 Content' })).toBeNull()
    expect(screen.queryByRole('heading', { name: 'Practice Exercises' })).toBeNull()
    expect(screen.getByRole('link', { name: 'Next lesson' })).toHaveAttribute('href', '/courses/real-course/lessons/102')
    expect(screen.getByRole('button', { name: 'Mark as complete' })).toBeInTheDocument()
  })

  it('only pairs an exercise with a lesson through a matching lesson_id, not just a shared topic', async () => {
    const l1 = lesson({ id: 201, title: 'Paired', order: 1 })
    const unrelated = exercise({ id: 301, title: 'Unrelated exercise', lesson_id: 999 })
    vi.mocked(api.getToolCourse).mockResolvedValue(courseWith([topic({ id: 21, lessons: [l1], exercises: [unrelated] })]))

    render(<LessonPage courseSlug="real-course" lessonParam="201" />)
    await screen.findByRole('heading', { name: 'Paired' })
    expect(screen.queryByText('Unrelated exercise')).toBeNull()
    expect(screen.queryByRole('button', { name: '1 Content' })).toBeNull()
  })

  it('continues from the last lesson of one module to the first lesson of the next', async () => {
    const lastInModule = lesson({ id: 301, title: 'Module one ending', order: 2 })
    const firstInNext = lesson({ id: 302, title: 'Module two beginning', order: 1 })
    vi.mocked(api.getToolCourse).mockResolvedValue(courseWith([
      topic({ id: 31, order: 1, title: 'Module one', lessons: [lastInModule] }),
      topic({ id: 32, order: 2, title: 'Module two', lessons: [firstInNext] }),
    ]))

    render(<LessonPage courseSlug="real-course" lessonParam="301" />)
    await screen.findByRole('heading', { name: 'Module one ending' })

    expect(screen.getByRole('link', { name: 'Next lesson' })).toHaveAttribute(
      'href', '/courses/real-course/lessons/302',
    )
  })

  it('renders every exercise owned by the lesson below its content, but never the module quiz', async () => {
    const current = lesson({ id: 401, title: 'Scoped lesson', content: 'Unique lesson content', order: 1 })
    const first = exercise({ id: 501, title: 'First scoped exercise', lesson_id: current.id })
    const second = exercise({ id: 502, title: 'Second scoped exercise', lesson_id: current.id })
    const unrelated = exercise({ id: 503, title: 'Another lesson exercise', lesson_id: 999 })
    vi.mocked(api.getToolCourse).mockResolvedValue(courseWith([topic({
      id: 23,
      lessons: [current],
      exercises: [first, unrelated, second],
      quizzes: [{ id: 601, title: 'Module quiz must stay separate', questions: [], passing_score: 70 }],
    })]))

    render(<LessonPage courseSlug="real-course" lessonParam="401" />)
    await screen.findByRole('heading', { name: 'Scoped lesson' })

    const content = screen.getByText('Unique lesson content')
    const practice = screen.getByRole('heading', { name: 'Practice Exercises' })
    const navigation = screen.getByRole('navigation', { name: 'Lesson navigation' })
    expect(screen.getByText('First scoped exercise')).toBeInTheDocument()
    expect(screen.getByText('Second scoped exercise')).toBeInTheDocument()
    expect(screen.queryByText('Another lesson exercise')).toBeNull()
    expect(screen.queryByText('Module quiz must stay separate')).toBeNull()
    expect(content.compareDocumentPosition(practice) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
    expect(practice.compareDocumentPosition(navigation) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  })
})

describe('LessonPage — unknown lesson', () => {
  it('shows a not-found state instead of a route error', async () => {
    vi.mocked(api.getToolCourse).mockResolvedValue(courseWith([topic({ id: 22, lessons: [lesson({ id: 1, title: 'Only' })] })]))
    render(<LessonPage courseSlug="real-course" lessonParam="999" />)
    await waitFor(() => expect(screen.getByText('This course does not exist.')).toBeInTheDocument())
  })
})
