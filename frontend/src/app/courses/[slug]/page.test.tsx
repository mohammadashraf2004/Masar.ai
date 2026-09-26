import { act, render, screen } from '@testing-library/react'
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
}))
vi.mock('@/components/layout/AppShell', () => ({ AppShell: ({ children }: { children: ReactNode }) => <>{children}</> }))
vi.mock('@/components/layout/PageHeader', () => ({ PageHeader: ({ title }: { title: string }) => <h1>{title}</h1> }))
vi.mock('@/lib/api', () => ({
  api: {
    getCatalogCourse: vi.fn(),
    getCourseAccess: vi.fn(),
    getCourseOffer: vi.fn(),
    checkoutCourse: vi.fn(),
    getCourseReadiness: vi.fn(),
    enrollInCourse: vi.fn(),
    setCoursePaused: vi.fn(),
    getReadinessAssessment: vi.fn(),
    submitReadinessAssessment: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const paidCourse: CatalogCourseDetail = {
  ...course({ is_free: false }),
  assumes: [], prerequisites: [], learning_objectives: [], learning_objectives_ar: [],
}

beforeEach(() => {
  vi.mocked(api.getCatalogCourse).mockResolvedValue(paidCourse)
  vi.mocked(api.getCourseOffer).mockResolvedValue({
    course_id: paidCourse.slug, price_amount: 149900, currency: 'EGP', original_price_amount: 199900,
  })
  vi.mocked(api.checkoutCourse).mockReset()
  vi.mocked(api.getCourseReadiness).mockResolvedValue(readinessReport())
})

const enrolledCourse = (): CatalogCourseDetail => ({
  ...paidCourse, enrollment: { status: 'in_progress', progress_percentage: 30 },
})

describe('paid course page: the rest of the copy', () => {
  it('has every string in Arabic: price fallback, benefits, and the free and owned notices', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    vi.mocked(api.getCourseAccess).mockResolvedValueOnce({ has_access: false, reason: 'purchase_required', enrollment_id: null })
    vi.mocked(api.getCourseOffer).mockRejectedValueOnce(new Error('no offer'))
    const first = render(<CoursePage />)
    for (const text of ['السعر غير متاح', 'وصول مدى الحياة', 'دروس بالعربية أولاً', 'مشاريع عملية', 'المرشد الذكي', 'شهادة']) {
      expect(await screen.findByText(text)).toBeInTheDocument()
    }
    for (const english of ['Price unavailable', 'Lifetime access', 'Arabic-first lessons', 'Practical projects', 'AI Mentor', 'Certificate']) {
      expect(screen.queryByText(english)).toBeNull()
    }
    first.unmount()

    vi.mocked(api.getCourseAccess).mockResolvedValueOnce({ has_access: true, reason: 'purchase', enrollment_id: 10 })
    const second = render(<CoursePage />)
    expect(await screen.findByText('أنت تملك هذه الدورة')).toBeInTheDocument()
    second.unmount()

    vi.mocked(api.getCatalogCourse).mockResolvedValueOnce({ ...paidCourse, is_free: true })
    vi.mocked(api.getCourseAccess).mockResolvedValueOnce({ has_access: true, reason: 'free', enrollment_id: null })
    render(<CoursePage />)
    expect(await screen.findByText('وصول مجاني للدورة')).toBeInTheDocument()
  })

  it('and in English, unchanged', async () => {
    vi.mocked(api.getCourseAccess).mockResolvedValueOnce({ has_access: false, reason: 'purchase_required', enrollment_id: null })
    render(<CoursePage />)
    for (const text of ['Lifetime access', 'Arabic-first lessons', 'Practical projects', 'AI Mentor', 'Certificate']) {
      expect(await screen.findByText(text)).toBeInTheDocument()
    }
  })
})

describe('paid course page', () => {
  it('has Arabic for both actions, from the string table', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    vi.mocked(api.getCourseAccess).mockResolvedValueOnce({ has_access: false, reason: 'purchase_required', enrollment_id: null })
    const first = render(<CoursePage />)
    expect(await screen.findByRole('button', { name: new RegExp(STRINGS.ar['course.buy']) })).toBeInTheDocument()
    expect(screen.queryByText(/Buy Course/)).toBeNull()
    first.unmount()
    vi.mocked(api.getCourseAccess).mockResolvedValueOnce({ has_access: true, reason: 'purchase', enrollment_id: 10 })
    vi.mocked(api.getCatalogCourse).mockResolvedValueOnce(enrolledCourse())
    render(<CoursePage />)
    expect(await screen.findByRole('link', { name: STRINGS.ar['course.continueLearning'] })).toHaveAttribute('href', paidCourse.href!)
    expect(STRINGS.ar['course.buy']).not.toBe(STRINGS.en['course.buy'])
  })

  it('renders the server price and Buy Course when access is locked', async () => {
    vi.mocked(api.getCourseAccess).mockResolvedValue({ has_access: false, reason: 'purchase_required', enrollment_id: null })
    render(<CoursePage />)
    expect(await screen.findByText(/EGP\s*1,499/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Buy Course/ })).toBeInTheDocument()
    expect(screen.queryByText('Continue Learning')).toBeNull()
  })

  it('shows ownership and Continue Learning instead of a buy button', async () => {
    vi.mocked(api.getCourseAccess).mockResolvedValue({ has_access: true, reason: 'purchase', enrollment_id: 10 })
    vi.mocked(api.getCatalogCourse).mockResolvedValue(enrolledCourse())
    render(<CoursePage />)
    expect(await screen.findByText('You own this course')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continue Learning' })).toHaveAttribute('href', paidCourse.href!)
    expect(screen.queryByRole('button', { name: /Buy Course/ })).toBeNull()
  })

  it('starts checkout through the backend without sending a price', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getCourseAccess).mockResolvedValue({ has_access: false, reason: 'purchase_required', enrollment_id: null })
    vi.mocked(api.checkoutCourse).mockReturnValue(new Promise(() => {}))
    render(<CoursePage />)
    await user.click(await screen.findByRole('button', { name: /Buy Course/ }))
    expect(api.checkoutCourse).toHaveBeenCalledWith(paidCourse.slug)
  })

  it('switches to Continue Learning when checkout reports existing ownership', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getCourseAccess).mockResolvedValue({ has_access: false, reason: 'purchase_required', enrollment_id: null })
    vi.mocked(api.checkoutCourse).mockRejectedValue({
      isAxiosError: true,
      response: { data: { detail: { code: 'COURSE_ALREADY_OWNED' } } },
    })
    render(<CoursePage />)
    await user.click(await screen.findByRole('button', { name: /Buy Course/ }))
    expect(await screen.findByText('You already own this course.')).toBeInTheDocument()
    // The page now treats them as the owner: the buy button is gone and they can enroll.
    expect(screen.queryByRole('button', { name: /Buy Course/ })).toBeNull()
    expect(screen.getByRole('button', { name: 'Enroll now' })).toBeInTheDocument()
  })
})

describe.each([
  ['en', 'Buy Course'],
  ['ar', STRINGS.ar['course.buy']],
] as const)('checkout errors in %s', (language, buyLabel) => {
  const failure = (code?: string) => ({
    isAxiosError: true,
    response: { data: { detail: code ? { code } : 'boom' } },
  })
  const cases: Array<[string, string | undefined, 'course.err.owned' | 'course.err.unavailable' | 'course.err.checkout']> = [
    ['the course is already owned', 'COURSE_ALREADY_OWNED', 'course.err.owned'],
    ['the course cannot be bought right now', 'COURSE_OFFER_UNAVAILABLE', 'course.err.unavailable'],
    ['anything else goes wrong', undefined, 'course.err.checkout'],
  ]

  beforeEach(() => {
    useLanguageStore.setState({ language, mode: 'arabic_first', annotateTerms: true })
    vi.mocked(api.getCourseAccess).mockResolvedValue({ has_access: false, reason: 'purchase_required', enrollment_id: null })
  })

  it.each(cases)('when %s, says so in the reader’s language', async (_name, code, key) => {
    const user = userEvent.setup()
    vi.mocked(api.checkoutCourse).mockRejectedValue(failure(code))
    render(<CoursePage />)
    await user.click(await screen.findByRole('button', { name: new RegExp(buyLabel) }))
    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS[language][key])
  })

  it('has the handoff wording, and the two languages differ', () => {
    const arabic = {
      'course.err.owned': 'أنت تملك هذه الدورة بالفعل.',
      'course.err.unavailable': 'هذه الدورة غير متاحة للشراء حالياً.',
      'course.err.checkout': 'تعذّر بدء الدفع. حاول مرة أخرى.',
    } as const
    for (const [key, text] of Object.entries(arabic)) {
      expect(STRINGS.ar[key as keyof typeof arabic]).toBe(text)
      expect(STRINGS.en[key as keyof typeof arabic]).not.toBe(text)
    }
  })

  it('the message follows a language change instead of staying in the one it was raised in', async () => {
    const user = userEvent.setup()
    vi.mocked(api.checkoutCourse).mockRejectedValue(failure())
    render(<CoursePage />)
    await user.click(await screen.findByRole('button', { name: new RegExp(buyLabel) }))
    await screen.findByRole('alert')
    const other = language === 'en' ? 'ar' : 'en'
    act(() => useLanguageStore.setState({ language: other }))
    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS[other]['course.err.checkout'])
  })
})

describe('a course on its own: no track, no goal', () => {
  const free = (over: Partial<CatalogCourseDetail> = {}): CatalogCourseDetail => courseDetail({ is_free: true, ...over })

  beforeEach(() => {
    vi.mocked(api.getCourseAccess).mockResolvedValue({ has_access: true, reason: 'free', enrollment_id: null })
    vi.mocked(api.enrollInCourse).mockReset()
  })

  it('opens from its own address and shows what the course is: modules, projects, roadmaps, skills', async () => {
    vi.mocked(api.getCatalogCourse).mockResolvedValue(free())
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
    vi.mocked(api.getCatalogCourse).mockResolvedValue(free())
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
    vi.mocked(api.getCatalogCourse).mockResolvedValue(free())
    render(<CoursePage />)
    expect(await screen.findByText('Mostly ready')).toBeInTheDocument()
    expect(screen.getByText('You can start now. A little review would help.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Embeddings & Semantic Search' })).toHaveAttribute('href', '/courses/embeddings-search')
    expect(screen.getByText('Module 2')).toBeInTheDocument()
    expect(screen.getByText('This is advice, not a requirement. You can start any course at any time.')).toBeInTheDocument()
  })

  it('never blocks a learner who needs more foundation: the button just says "Start anyway"', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getCatalogCourse).mockResolvedValue(free())
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
    vi.mocked(api.getCatalogCourse).mockResolvedValue(free())
    vi.mocked(api.getCourseReadiness).mockRejectedValue(new Error('down'))
    render(<CoursePage />)
    expect(await screen.findByRole('button', { name: 'Enroll now' })).toBeInTheDocument()
    expect(screen.getByText('Chunking')).toBeInTheDocument()
    expect(screen.queryByText('Your readiness')).toBeNull()
  })

  it('shows progress for an enrolled learner, and a way to pause', async () => {
    vi.mocked(api.getCatalogCourse).mockResolvedValue(free({ enrollment: { status: 'in_progress', progress_percentage: 42 } }))
    render(<CoursePage />)
    expect(await screen.findByText('42% complete')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continue Learning' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Pause course' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Enroll now' })).toBeNull()
  })

  it('offers review once the course is completed', async () => {
    vi.mocked(api.getCatalogCourse).mockResolvedValue(free({ enrollment: { status: 'completed', progress_percentage: 100 } }))
    render(<CoursePage />)
    expect(await screen.findByRole('link', { name: 'Review course' })).toBeInTheDocument()
    expect(screen.getByText('Completed')).toBeInTheDocument()
  })

  it('takes the quick readiness check, sends only the answers, and shows the result the server worked out', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getCatalogCourse).mockResolvedValue(free())
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
    vi.mocked(api.getCatalogCourse).mockResolvedValue(free())
    render(<CoursePage />)
    expect(await screen.findByRole('button', { name: STRINGS.ar['enr.enroll'] })).toBeInTheDocument()
    expect(screen.getByText(STRINGS.ar['rd.state.mostly_ready'])).toBeInTheDocument()
    expect(screen.getByText(STRINGS.ar['rd.advisory'])).toBeInTheDocument()
    expect(screen.getByText(STRINGS.ar['cp.roadmaps'])).toBeInTheDocument()
  })
})
