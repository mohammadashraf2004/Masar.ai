import { act, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { TrackCurriculum } from '@/components/learning/TrackCurriculum'
import { api } from '@/lib/api'
import { course, path, pathCourse, stage } from '@/test/fixtures'
import type { CatalogCourse, CatalogCourseDetail, CourseFilters, CourseRole } from '@/types'

vi.mock('@/lib/api', () => ({ api: { listCatalogCourses: vi.fn(), getCatalogCourse: vi.fn() } }))

function curriculumCourse(
  slug: string,
  title: string,
  role: CourseRole,
  extra: Partial<CatalogCourse> = {},
): CatalogCourse {
  return course({ slug, title, track_role: role, ...extra })
}

function detail(row: CatalogCourse, prerequisites: CatalogCourseDetail['prerequisites'] = []): CatalogCourseDetail {
  return {
    ...row,
    assumes: [], prerequisites, learning_objectives: [], learning_objectives_ar: [],
  }
}

function mockCatalogue(rows: CatalogCourse[], prerequisiteMap: Record<string, CatalogCourseDetail['prerequisites']> = {}) {
  vi.mocked(api.listCatalogCourses).mockResolvedValue(rows)
  vi.mocked(api.getCatalogCourse).mockImplementation(async (slug) => {
    const row = rows.find((item) => item.slug === slug)
    if (!row) throw new Error('missing fixture')
    return detail(row, prerequisiteMap[slug])
  })
}

describe('TrackCurriculum — backend catalogue integration', () => {
  beforeEach(() => vi.clearAllMocks())

  it.each([
    'data-analyst', 'ml-engineer', 'ai-developer', 'mlops-engineer', 'ai-engineer',
  ])('requests and renders the canonical %s track from its API slug', async (goal) => {
    mockCatalogue([curriculumCourse('course-013', 'Applied Data Analysis with Python', 'core')])
    render(<TrackCurriculum careerGoal={goal} />)

    expect(await screen.findByText('Applied Data Analysis with Python')).toBeInTheDocument()
    expect(api.listCatalogCourses).toHaveBeenCalledWith({ career_goal: [goal] })
  })

  it('uses the role returned for the active track, so one shared course can change role', async () => {
    vi.mocked(api.listCatalogCourses).mockImplementation(async (filters: CourseFilters = {}) => {
      const role = filters.career_goal?.[0] === 'mlops-engineer' ? 'core' : 'supporting'
      return [curriculumCourse('course-006', 'Production AI Engineering', role)]
    })
    vi.mocked(api.getCatalogCourse).mockImplementation(async (slug) => detail(
      curriculumCourse(slug, 'Production AI Engineering', 'supporting')
    ))

    const { rerender } = render(<TrackCurriculum careerGoal="ai-developer" />)
    expect((await screen.findByText('Production AI Engineering')).closest('[data-course-id]')).toHaveAttribute('data-track-role', 'supporting')

    await act(async () => rerender(<TrackCurriculum careerGoal="mlops-engineer" />))
    await vi.waitFor(() => {
      expect(screen.getByText('Production AI Engineering').closest('[data-course-id]')).toHaveAttribute('data-track-role', 'core')
    })
  })

  it('marks optional work as optional without treating it as a blocker', async () => {
    mockCatalogue([curriculumCourse('course-008', 'Vision-Language & Multimodal AI Engineering', 'optional')])
    render(<TrackCurriculum careerGoal="ml-engineer" />)

    const card = (await screen.findByText('Vision-Language & Multimodal AI Engineering')).closest('[data-course-id]') as HTMLElement
    expect(card).toHaveAttribute('data-track-role', 'optional')
    expect(card).toHaveAttribute('data-status', 'not_started')
    expect(within(card).getByText('Optional')).toBeInTheDocument()
  })

  it('uses the backend path prerequisite reason for a locked course and lists API prerequisites', async () => {
    const second = curriculumCourse('course-002', 'Deep Learning Foundations', 'core', { id: 202, is_available: true, href: '/tracks/ml-engineer' })
    mockCatalogue([second], {
      'course-002': [{ id: 201, slug: 'course-001', title: 'Machine Learning Foundations', title_ar: null }],
    })
    const lockedPath = path({
      stages: [stage({ courses: [pathCourse({ course: { id: 202, slug: 'course-002' }, reason: 'prerequisite' })] })],
      current_course: null,
    })
    render(<TrackCurriculum careerGoal="ml-engineer" path={lockedPath} />)

    const card = (await screen.findByText('Deep Learning Foundations')).closest('[data-course-id]') as HTMLElement
    expect(card).toHaveAttribute('data-status', 'locked')
    expect(within(card).getByText('Locked')).toBeInTheDocument()
    expect(within(card).getByRole('link', { name: 'View prerequisites' })).toHaveAttribute('href', '/courses/course-002')
    expect(within(card).getByRole('link', { name: 'Machine Learning Foundations' })).toHaveAttribute('href', '/courses/course-001')
  })

  it('uses server progress and current-course identity for Continue, then follows the API navigation href', async () => {
    const current = curriculumCourse('course-010', 'AI Service Engineering with FastAPI', 'core', {
      id: 210, is_available: true, href: '/tracks/ai-developer',
    })
    mockCatalogue([current])
    const activePath = path({
      stages: [stage({ courses: [pathCourse({ course: { id: 210, slug: 'course-010' }, completion_pct: 40 })] })],
      current_course: { ...path().current_course!, course: current },
    })
    render(<TrackCurriculum careerGoal="ai-developer" path={activePath} />)

    const card = (await screen.findByText('AI Service Engineering with FastAPI')).closest('[data-course-id]') as HTMLElement
    expect(card).toHaveAttribute('data-status', 'in_progress')
    expect(within(card).getByText('40% complete')).toBeInTheDocument()
    expect(within(card).getByRole('link', { name: 'Continue' })).toHaveAttribute('href', '/tracks/ai-developer')
  })

  it('offers Start for an unlocked course and Review for a completed course using their API routes', async () => {
    const first = curriculumCourse('course-001', 'Machine Learning Foundations', 'core', {
      id: 211, is_available: true, href: '/tracks/ml-engineer',
    })
    const done = curriculumCourse('course-003', 'Applied Deep Learning', 'core', {
      id: 213, is_available: true, href: '/tracks/ml-engineer',
    })
    mockCatalogue([first, done])
    const completedPath = path({
      stages: [stage({ courses: [pathCourse({ course: { id: 213, slug: 'course-003' }, state: 'completed', completion_pct: 100 })] })],
      current_course: null,
    })
    render(<TrackCurriculum careerGoal="ml-engineer" path={completedPath} />)

    const firstCard = (await screen.findByText('Machine Learning Foundations')).closest('[data-course-id]') as HTMLElement
    const doneCard = screen.getByText('Applied Deep Learning').closest('[data-course-id]') as HTMLElement
    expect(firstCard).toHaveAttribute('data-status', 'not_started')
    expect(within(firstCard).getByRole('link', { name: 'Start course' })).toHaveAttribute('href', '/tracks/ml-engineer')
    expect(doneCard).toHaveAttribute('data-status', 'completed')
    expect(within(doneCard).getByRole('link', { name: 'Review course' })).toHaveAttribute('href', '/tracks/ml-engineer')
  })

  it('keeps COURSE-009 distinct from the legacy RAG row and keeps tools out of the curriculum section', async () => {
    mockCatalogue([
      curriculumCourse('course-009', 'Enterprise RAG Engineering', 'core'),
      course({ slug: 'rag-knowledge-systems', title: 'RAG & Knowledge Systems', track_role: 'core' }),
      course({ slug: 'langchain', title: 'LangChain', kind: 'tool_course', track_role: 'supporting' }),
    ])
    render(<TrackCurriculum careerGoal="ai-developer" />)

    expect(await screen.findByText('Enterprise RAG Engineering')).toBeInTheDocument()
    expect(screen.queryByText('RAG & Knowledge Systems')).toBeNull()
    expect(screen.queryByText('LangChain')).toBeNull()
  })

  it('shows a planned course and its details route instead of inventing a start action', async () => {
    mockCatalogue([curriculumCourse('course-013', 'Applied Data Analysis with Python', 'core', {
      is_available: false, href: '/tracks/data-analyst',
    })])
    render(<TrackCurriculum careerGoal="data-analyst" />)

    const card = (await screen.findByText('Applied Data Analysis with Python')).closest('[data-course-id]') as HTMLElement
    expect(card).toHaveAttribute('data-course-id', 'COURSE-013')
    expect(card).toHaveAttribute('data-status', 'coming_soon')
    expect(within(card).getByRole('link', { name: 'Course details' })).toHaveAttribute('href', '/courses/course-013')
  })

  it('renders an API failure instead of stale or hard-coded curriculum, and retries', async () => {
    const user = userEvent.setup()
    vi.mocked(api.listCatalogCourses).mockRejectedValueOnce(new Error('down'))
    vi.mocked(api.listCatalogCourses).mockResolvedValueOnce([])
    render(<TrackCurriculum careerGoal="ai-engineer" />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load this track’s curriculum')
    await user.click(screen.getByRole('button', { name: 'Try again' }))
    await vi.waitFor(() => expect(api.listCatalogCourses).toHaveBeenCalledTimes(2))
    expect(await screen.findByText(/No curriculum courses are available/)).toBeInTheDocument()
  })
})
