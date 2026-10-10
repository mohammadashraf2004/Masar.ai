import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import type { ReactNode } from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import CoursePage from '@/app/courses/[slug]/page'
import { course, courseDetail, readinessReport } from '@/test/fixtures'
import { STRINGS } from '@/lib/i18n'
import { useLanguageStore } from '@/lib/language'
import type { CatalogCourseDetail } from '@/types'

vi.mock('next/navigation', () => ({
  useParams: () => ({ slug: 'rag-knowledge-systems' }),
  useRouter: () => ({ replace: vi.fn(), push: vi.fn() }),
  usePathname: () => '/courses/rag-knowledge-systems',
}))
vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: { id: 1 }, isAuthenticated: true, isLoading: false }),
  useSession: () => ({ user: { id: 1 }, isAuthenticated: true, isLoading: false }), useNextParam: () => null,
}))
vi.mock('@/components/layout/AppShell', () => ({ AppShell: ({ children }: { children: ReactNode }) => <>{children}</> }))
vi.mock('@/components/layout/PageHeader', () => ({ PageHeader: ({ title }: { title: string }) => <h1>{title}</h1> }))
vi.mock('@/lib/api', () => ({
  api: {
    getCatalogCourse: vi.fn(),
    getCourseAccess: vi.fn(),
    getCourseReadiness: vi.fn(),
    enrollInCourse: vi.fn(),
    setCoursePaused: vi.fn(),
    getReadinessAssessment: vi.fn(),
    submitReadinessAssessment: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const proOnlyCourse: CatalogCourseDetail = {
  ...course({ is_free: false }),
  assumes: [], prerequisites: [], learning_objectives: [], learning_objectives_ar: [],
}

beforeEach(() => {
  vi.mocked(api.getCatalogCourse).mockResolvedValue(proOnlyCourse)
  vi.mocked(api.getCourseReadiness).mockResolvedValue(readinessReport())
})

const enrolledCourse = (): CatalogCourseDetail => ({
  ...proOnlyCourse, enrollment: { status: 'in_progress', progress_percentage: 30 },
})

describe('a course beyond the free preview: the Pro upsell (backend-enforced, no price on this page)', () => {
  it('shows the two-lesson preview notice, a free-lessons link and an Upgrade to Pro link — no price, no buy button', async () => {
    vi.mocked(api.getCourseAccess).mockResolvedValue({
      has_access: false, reason: 'purchase_required', enrollment_id: null, free_lesson_count: 2,
    })
    render(<CoursePage />)
    expect(await screen.findByText('The first 2 lessons are free. Upgrade to Pro for the complete course.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Upgrade to Pro' })).toHaveAttribute('href', '/billing')
    expect(screen.getByRole('link', { name: 'Start free lessons' })).toHaveAttribute('href', `/courses/${proOnlyCourse.slug}/learn`)
    expect(screen.queryByRole('button', { name: /Buy Course/ })).toBeNull()
    expect(screen.queryByText(/EGP/)).toBeNull()
  })

  it('has the same notice in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    vi.mocked(api.getCourseAccess).mockResolvedValue({
      has_access: false, reason: 'purchase_required', enrollment_id: null, free_lesson_count: 2,
    })
    render(<CoursePage />)
    expect(await screen.findByText('أول درسين مجانيان. اشترك في Pro للوصول إلى الدورة كاملة.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'الترقية إلى Pro' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'ابدأ الدروس المجانية' })).toBeInTheDocument()
  })

  it('has no free-lessons link when the course has no preview lessons to offer', async () => {
    vi.mocked(api.getCourseAccess).mockResolvedValue({
      has_access: false, reason: 'purchase_required', enrollment_id: null, free_lesson_count: 0,
    })
    render(<CoursePage />)
    await screen.findByRole('link', { name: 'Upgrade to Pro' })
    expect(screen.queryByRole('link', { name: 'Start free lessons' })).toBeNull()
  })

  it('shows the Pro-plan notice, not a purchase notice, for a Pro subscriber', async () => {
    vi.mocked(api.getCourseAccess).mockResolvedValue({ has_access: true, reason: 'pro', enrollment_id: null })
    render(<CoursePage />)
    expect(await screen.findByText('Included with your Pro plan')).toBeInTheDocument()
    expect(screen.queryByText('You own this course')).toBeNull()
  })

  it('shows plain ownership for a legacy course purchase or admin grant', async () => {
    vi.mocked(api.getCourseAccess).mockResolvedValue({ has_access: true, reason: 'purchase', enrollment_id: 10 })
    vi.mocked(api.getCatalogCourse).mockResolvedValue(enrolledCourse())
    render(<CoursePage />)
    expect(await screen.findByText('You own this course')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continue Learning' })).toHaveAttribute('href', proOnlyCourse.href!)
  })
})

describe('a course on its own: no track, no goal', () => {
  // These exercise enrollment/readiness, which only needs `has_access`; a Pro
  // subscriber stands in for "this course is open" (no course is free outright
  // any more - see access_service.free_lesson_ids for the two-lesson preview).
  const open = (over: Partial<CatalogCourseDetail> = {}): CatalogCourseDetail => courseDetail({ is_free: false, ...over })

  beforeEach(() => {
    vi.mocked(api.getCourseAccess).mockResolvedValue({ has_access: true, reason: 'pro', enrollment_id: null })
    vi.mocked(api.enrollInCourse).mockReset()
  })

  it('opens from its own address and shows what the course is: modules, projects, roadmaps, skills', async () => {
    vi.mocked(api.getCatalogCourse).mockResolvedValue(open())
    render(<CoursePage />)
    expect(await screen.findByText('Chunking')).toBeInTheDocument()
    expect(api.getCatalogCourse).toHaveBeenCalledWith('rag-knowledge-systems')
    expect(screen.getByText('Build a retrieval pipeline')).toBeInTheDocument()
    expect(screen.getByText('Support bot')).toBeInTheDocument()
    // Informational: the roadmap is a link, never a requirement.
    expect(screen.getByRole('link', { name: 'AI Engineer' })).toHaveAttribute('href', '/roadmaps/ai-engineer')
    expect(screen.getByText('Informational only. You can enroll in this course directly.')).toBeInTheDocument()
  })

  it('enrolls with nothing but the course: no track, goal or score is sent', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getCatalogCourse).mockResolvedValue(open())
    vi.mocked(api.enrollInCourse).mockResolvedValue({
      enrollment: {
        course_id: 1, course_slug: 'rag-knowledge-systems', status: 'enrolled', source: 'free',
        progress_percentage: 0, enrolled_at: '2026-09-26T00:00:00Z',
      },
      created: true, readiness: readinessReport({ state: 'ready', gaps: [], recommended_review: [] }),
      start: { mode: 'start', recommended_module: { id: 11, order: 1, title: 'Chunking' }, preparation: [] },
    })
    render(<CoursePage />)
    await user.click(await screen.findByRole('button', { name: 'Enroll now' }))
    expect(api.enrollInCourse).toHaveBeenCalledWith('rag-knowledge-systems')
    expect(api.enrollInCourse).toHaveBeenCalledTimes(1)
    expect(await screen.findByText('You are enrolled')).toBeInTheDocument()
    expect(screen.getByText(/Start from module 1: Chunking/)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continue Learning' })).toHaveAttribute('href', '/tracks/ai-developer')
    // The fresh readiness the server sent replaces the old one.
    expect(screen.getByText('Ready')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Enroll now' })).toBeNull()
  })

  it('shows readiness as advice: strengths, what to review and what to study first', async () => {
    vi.mocked(api.getCatalogCourse).mockResolvedValue(open())
    render(<CoursePage />)
    expect(await screen.findByText('Mostly ready')).toBeInTheDocument()
    expect(screen.getByText('You can start now. A little review would help.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Embeddings & Semantic Search' })).toHaveAttribute('href', '/courses/embeddings-search')
    expect(screen.getByText('Module 2')).toBeInTheDocument()
    expect(screen.getByText('This is advice, not a requirement. You can start any course at any time.')).toBeInTheDocument()
  })

  it('never blocks a learner who needs more foundation: the button just says "Start anyway"', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getCatalogCourse).mockResolvedValue(open())
    vi.mocked(api.getCourseReadiness).mockResolvedValue(readinessReport({ state: 'needs_foundation', score: 20 }))
    render(<CoursePage />)
    expect(await screen.findByText('You can start this course, but we recommend reviewing first.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Review first' })).toHaveAttribute('href', '/courses/embeddings-search')
    const start = screen.getByRole('button', { name: 'Start anyway' })
    expect(start).toBeEnabled()
    vi.mocked(api.enrollInCourse).mockReturnValue(new Promise(() => {}))
    await user.click(start)
    expect(api.enrollInCourse).toHaveBeenCalledWith('rag-knowledge-systems')
  })

  it('still shows the course when readiness cannot be loaded', async () => {
    vi.mocked(api.getCatalogCourse).mockResolvedValue(open())
    vi.mocked(api.getCourseReadiness).mockRejectedValue(new Error('down'))
    render(<CoursePage />)
    expect(await screen.findByRole('button', { name: 'Enroll now' })).toBeInTheDocument()
    expect(screen.getByText('Chunking')).toBeInTheDocument()
    expect(screen.queryByText('Your readiness')).toBeNull()
  })

  it('shows progress for an enrolled learner, and a way to pause', async () => {
    vi.mocked(api.getCatalogCourse).mockResolvedValue(open({ enrollment: { status: 'in_progress', progress_percentage: 42 } }))
    render(<CoursePage />)
    expect(await screen.findByText('42% complete')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continue Learning' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Pause course' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Enroll now' })).toBeNull()
  })

  it('offers review once the course is completed', async () => {
    vi.mocked(api.getCatalogCourse).mockResolvedValue(open({ enrollment: { status: 'completed', progress_percentage: 100 } }))
    render(<CoursePage />)
    expect(await screen.findByRole('link', { name: 'Review course' })).toBeInTheDocument()
    expect(screen.getByText('Completed')).toBeInTheDocument()
  })

  it('takes the quick readiness check, sends only the answers, and shows the result the server worked out', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getCatalogCourse).mockResolvedValue(open())
    vi.mocked(api.getReadinessAssessment).mockResolvedValue({
      course_id: 1, course_slug: 'rag-knowledge-systems', question_count: 2, estimated_minutes: 2,
      questions: [
        { id: '7:0', skill: { slug: 'embeddings', name: 'Embeddings', name_ar: null }, question: 'What is an embedding?', options: ['A vector', 'A table'] },
        { id: '7:1', skill: { slug: 'llms', name: 'LLMs', name_ar: null }, question: 'What is a token?', options: ['A word piece', 'A GPU'] },
      ],
    })
    vi.mocked(api.submitReadinessAssessment).mockResolvedValue({
      assessment_id: 5, score: 50, correct_count: 1, question_count: 2, skill_results: { embeddings: 1, llms: 0 },
      questions: [], readiness: readinessReport({ state: 'ready', gaps: [], recommended_review: [] }),
    })
    render(<CoursePage />)
    await user.click(await screen.findByRole('button', { name: 'Take the quick check' }))
    const submit = await screen.findByRole('button', { name: 'See my result' })
    expect(submit).toBeDisabled()
    await user.click(screen.getByRole('radio', { name: 'A vector' }))
    await user.click(screen.getByRole('radio', { name: 'A word piece' }))
    await user.click(submit)
    // Question id -> option index. No score and no readiness: the server works those out.
    expect(api.submitReadinessAssessment).toHaveBeenCalledWith('rag-knowledge-systems', { '7:0': 0, '7:1': 0 })
    expect(await screen.findByText(/1 of 2 correct/)).toBeInTheDocument()
    expect(screen.getByText('Ready')).toBeInTheDocument()
  })

  it('has its readiness and enrollment copy in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    vi.mocked(api.getCatalogCourse).mockResolvedValue(open())
    render(<CoursePage />)
    expect(await screen.findByRole('button', { name: STRINGS.ar['enr.enroll'] })).toBeInTheDocument()
    expect(screen.getByText(STRINGS.ar['rd.state.mostly_ready'])).toBeInTheDocument()
    expect(screen.getByText(STRINGS.ar['rd.advisory'])).toBeInTheDocument()
    expect(screen.getByText(STRINGS.ar['cp.roadmaps'])).toBeInTheDocument()
  })
})
