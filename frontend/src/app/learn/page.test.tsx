import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import LearnHubPage from '@/app/learn/page'
import { STRINGS } from '@/lib/i18n'
import { useLanguageStore } from '@/lib/language'
import { CATALOG, NEEDS_ONBOARDING, NO_RECOMMENDATIONS, course, profile, recommendation } from '@/test/fixtures'

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
}))
vi.mock('@/components/layout/AppShell', async () => {
  const { createElement } = await import('react')
  return { AppShell: ({ children }: { children: React.ReactNode }) => createElement('div', null, children) }
})
vi.mock('@/components/layout/PageHeader', async () => {
  const { createElement } = await import('react')
  return { PageHeader: ({ title }: { title: string }) => createElement('h1', null, title) }
})
vi.mock('@/lib/api', () => ({
  api: {
    getLearningLevels: vi.fn(), getLearningFields: vi.fn(), getCareerGoals: vi.fn(),
    getRecommendations: vi.fn(), getMyLearningProfile: vi.fn(), listCatalogCourses: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const ML = course({ id: 2, slug: 'course-001', title: 'Machine Learning Foundations', title_ar: 'أساسيات تعلم الآلة', module_count: 12, estimated_hours: 20 })
const DL = course({ id: 3, slug: 'course-002', title: 'Deep Learning Foundations', title_ar: null, module_count: 9 })

beforeEach(() => {
  vi.mocked(api.getLearningLevels).mockResolvedValue(CATALOG.levels)
  vi.mocked(api.getLearningFields).mockResolvedValue(CATALOG.fields)
  vi.mocked(api.getCareerGoals).mockResolvedValue(CATALOG.goals)
  vi.mocked(api.getRecommendations).mockResolvedValue(NO_RECOMMENDATIONS)
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.listCatalogCourses).mockReset()
  vi.mocked(api.listCatalogCourses).mockResolvedValue([ML, DL])
})

describe('Learn — every course, with no track chosen', () => {
  it('lists the whole catalogue without asking for a career goal', async () => {
    render(<LearnHubPage />)
    expect(await screen.findByRole('link', { name: 'Machine Learning Foundations' })).toHaveAttribute('href', '/courses/course-001')
    expect(screen.getByRole('link', { name: 'Deep Learning Foundations' })).toHaveAttribute('href', '/courses/course-002')
    // No goal, and no track, in the request: the unfiltered catalogue.
    expect(api.listCatalogCourses).toHaveBeenCalledWith({ level: [], field: [] })
    expect(screen.getByText('12 modules')).toBeInTheDocument()
    expect(screen.getByText('20h')).toBeInTheDocument()
  })

  it('narrows by difficulty and category on the server, and can be cleared', async () => {
    const user = userEvent.setup()
    render(<LearnHubPage />)
    await screen.findByRole('link', { name: 'Machine Learning Foundations' })
    const difficulty = screen.getByRole('group', { name: 'Difficulty' })
    await user.click(within(difficulty).getByRole('button', { name: /Beginner/ }))
    expect(api.listCatalogCourses).toHaveBeenLastCalledWith({ level: ['beginner'], field: [] })
    const category = screen.getByRole('group', { name: 'Category' })
    await user.click(within(category).getByRole('button', { name: /NLP/ }))
    expect(api.listCatalogCourses).toHaveBeenLastCalledWith({ level: ['beginner'], field: ['nlp'] })
    await user.click(within(difficulty).getByRole('button', { name: 'All' }))
    expect(api.listCatalogCourses).toHaveBeenLastCalledWith({ level: [], field: ['nlp'] })
  })

  it('offers only the categories the platform really has courses for', async () => {
    render(<LearnHubPage />)
    await screen.findByRole('link', { name: 'Machine Learning Foundations' })
    const category = screen.getByRole('group', { name: 'Category' })
    // "All" plus one chip per field that has at least one course: nothing is listed from a hard-coded set.
    expect(within(category).getAllByRole('button')).toHaveLength(1 + CATALOG.fields.filter((f) => f.course_count > 0).length)
  })

  it('says so when nothing matches, and when the catalogue cannot be loaded', async () => {
    vi.mocked(api.listCatalogCourses).mockResolvedValue([])
    const first = render(<LearnHubPage />)
    expect(await screen.findByText(STRINGS.en['cat.empty'])).toBeInTheDocument()
    first.unmount()
    vi.mocked(api.listCatalogCourses).mockRejectedValue(new Error('down'))
    render(<LearnHubPage />)
    expect(await screen.findByText(STRINGS.en['cat.loadError'])).toBeInTheDocument()
  })

  it('shows the career roadmaps as guidance beside the catalogue', async () => {
    render(<LearnHubPage />)
    await screen.findByRole('link', { name: 'Machine Learning Foundations' })
    const heading = screen.getByRole('heading', { name: 'Career roadmaps' })
    const section = heading.closest('section')!
    const links = within(section).getAllByRole('link').filter((l) => l.getAttribute('href')?.startsWith('/roadmaps/'))
    expect(links.map((l) => l.getAttribute('href'))).toEqual(CATALOG.goals.map((g) => `/roadmaps/${g.slug}`))
    expect(within(section).getByText(/guidance, not gates/)).toBeInTheDocument()
  })
})

describe('Learn — your learning and recommendations', () => {
  it('shows what the learner is taking and what to take next, each with the reason', async () => {
    vi.mocked(api.getRecommendations).mockResolvedValue({
      ...NO_RECOMMENDATIONS,
      continue_learning: [recommendation({
        course: { ...ML, enrollment: { status: 'in_progress', progress_percentage: 62 } },
        reason_code: 'in_progress', params: { percent: 62 }, reason: 'x',
      })],
      recommended_next: [recommendation({
        course: DL, reason_code: 'follows_completed',
        params: { courses: [{ slug: 'course-001', title: 'Machine Learning Foundations', title_ar: null }] }, reason: 'x',
      })],
      build_foundations: [recommendation({ course: course({ id: 9, slug: 'course-900', title: 'Python for AI' }), reason_code: 'strengthens_enrolled', params: { count: 2 }, reason: 'x' })],
    })
    render(<LearnHubPage />)
    const learning = (await screen.findByRole('heading', { name: 'Your learning' })).closest('section')!
    expect(await within(learning).findByText('You are 62% through this course.')).toBeInTheDocument()
    expect(within(learning).getByText('62% complete')).toBeInTheDocument()
    expect(within(learning).getByRole('link', { name: 'Continue' })).toHaveAttribute('href', '/courses/course-001')

    const next = screen.getByRole('heading', { name: 'Recommended for you' }).closest('section')!
    expect(within(next).getByText('Builds on Machine Learning Foundations, which you completed.')).toBeInTheDocument()

    const foundations = screen.getByRole('heading', { name: 'Build your foundations' }).closest('section')!
    expect(within(foundations).getByText('Strengthens skills needed by 2 of your courses.')).toBeInTheDocument()
  })

  it('still recommends something to a learner who has chosen no goal and enrolled in nothing', async () => {
    vi.mocked(api.getRecommendations).mockResolvedValue({
      ...NO_RECOMMENDATIONS, recommended_next: [recommendation({ course: ML })],
    })
    render(<LearnHubPage />)
    const next = (await screen.findByRole('heading', { name: 'Recommended for you' })).closest('section')!
    expect(await within(next).findByText('A good place to start: it assumes no earlier course.')).toBeInTheDocument()
    expect(screen.getByText(STRINGS.en['hub.yourLearning.empty'])).toBeInTheDocument()
  })

  it('does not put a finished course under "Recommended for you"', async () => {
    vi.mocked(api.getRecommendations).mockResolvedValue({
      ...NO_RECOMMENDATIONS,
      recommended_next: [recommendation({ course: DL })],
      completed: [recommendation({ course: { ...ML, enrollment: { status: 'completed', progress_percentage: 100 } }, reason_code: 'completed' })],
    })
    render(<LearnHubPage />)
    const next = (await screen.findByRole('heading', { name: 'Recommended for you' })).closest('section')!
    expect(within(next).queryByText('Machine Learning Foundations')).toBeNull()
    const done = screen.getByRole('heading', { name: 'Completed' }).closest('section')!
    expect(within(done).getByText('Machine Learning Foundations')).toBeInTheDocument()
  })

  it('writes the reason in Arabic, with the goal or course named in Arabic where it has one', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    vi.mocked(api.getRecommendations).mockResolvedValue({
      ...NO_RECOMMENDATIONS,
      recommended_next: [recommendation({
        course: ML, reason_code: 'follows_completed',
        params: { courses: [{ slug: 'c', title: 'Python', title_ar: 'بايثون' }] }, reason: 'English fallback',
      })],
    })
    render(<LearnHubPage />)
    expect(await screen.findByText('تبني على بايثون التي أكملتها.')).toBeInTheDocument()
    expect(screen.queryByText('English fallback')).toBeNull()
  })

  it('falls back to the server’s sentence for a reason this build does not know', async () => {
    vi.mocked(api.getRecommendations).mockResolvedValue({
      ...NO_RECOMMENDATIONS,
      recommended_next: [recommendation({ course: ML, reason_code: 'brand_new_reason', reason: 'The server says so.' })],
    })
    render(<LearnHubPage />)
    expect(await screen.findByText('The server says so.')).toBeInTheDocument()
  })

  it('shows an error with a retry when the recommendations fail, and still lists the courses', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getRecommendations).mockRejectedValueOnce(new Error('down'))
    render(<LearnHubPage />)
    expect(await screen.findByText(STRINGS.en['hub.loadError'])).toBeInTheDocument()
    expect(await screen.findByRole('link', { name: 'Machine Learning Foundations' })).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByRole('heading', { name: 'Your learning' })).toBeInTheDocument()
  })
})

describe('Learn — personalising is optional', () => {
  it('invites a learner who has not answered to a short set of questions, without redirecting them', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    render(<LearnHubPage />)
    expect(await screen.findByRole('link', { name: 'Personalize' })).toHaveAttribute('href', '/onboarding/quick')
    expect(await screen.findByRole('link', { name: 'Machine Learning Foundations' })).toBeInTheDocument()
  })

  it('does not nag a learner who has answered', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile({ onboarding_completed: true, needs_onboarding: false }))
    render(<LearnHubPage />)
    await screen.findByRole('heading', { name: 'Your learning' })
    expect(screen.queryByRole('link', { name: 'Personalize' })).toBeNull()
  })

  it('links to the personal roadmap only when the learner has one', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile({ has_active_path: true }))
    render(<LearnHubPage />)
    expect(await screen.findByRole('link', { name: 'Your personal roadmap' })).toHaveAttribute('href', '/learn/masar')
  })
})
