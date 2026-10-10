import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import DashboardPage from '@/app/dashboard/page'
import RegisterPage from '@/app/auth/register/page'
import TracksPage from '@/app/tracks/page'
import { AppShell } from '@/components/layout/AppShell'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import { NEEDS_ONBOARDING, NO_RECOMMENDATIONS, path, profile } from '@/test/fixtures'
import { expectLinkStyledAsButton, expectMirroredArrow } from '@/test/interactive'
import { router, resetNav } from '@/test/nav'
import type { CareerTrackSummary, Enrollment, User } from '@/types'

// The redesign must not break what was already there: the role-based tracks
// page, sign-up, the sidebar and the dashboard. These are the screens an
// existing learner lands on.

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: { full_name: 'Amira Hassan', overall_readiness_score: 42 }, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
  useSession: () => ({ user: { full_name: 'Amira Hassan', overall_readiness_score: 42 }, isAuthenticated: true, isLoading: false }), useNextParam: () => null,
}))
vi.mock('@/components/layout/PageHeader', async () => {
  const { createElement } = await import('react')
  return { PageHeader: ({ title, subtitle }: { title: string; subtitle?: string }) =>
    createElement('header', null, createElement('h1', null, title), subtitle ? createElement('p', null, subtitle) : null) }
})
vi.mock('@/components/ui/VocabularyProgress', () => ({ VocabularyProgress: () => null }))
vi.mock('@/components/ui/PaymentResultBanner', () => ({ PaymentResultBanner: () => null }))
vi.mock('@/lib/api', () => ({
  api: {
    listTracks: vi.fn(), getMyEnrollments: vi.fn(), enroll: vi.fn(), getSkillScores: vi.fn(),
    register: vi.fn(), getWallet: vi.fn(),
    getMyLearningProfile: vi.fn(), getMyLearningPath: vi.fn(), getRecommendations: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const track = (id: number, slug: string, title: string, weeks: number): CareerTrackSummary =>
  ({ id, slug, title, description: '', icon: '', estimated_weeks: weeks })
const TRACKS = [
  track(1, 'data-analyst', 'Data Analyst', 12), track(2, 'ml-engineer', 'ML Engineer', 16),
  track(3, 'ai-developer', 'AI Developer', 14), track(4, 'mlops-engineer', 'MLOps Engineer', 10),
  track(5, 'ai-engineer', 'AI Engineer', 24),
]
const ENROLLMENT: Enrollment = { id: 1, track_id: 3, track: TRACKS[2], completion_percentage: 0, enrolled_at: '2026-09-01T00:00:00Z' }

beforeEach(() => {
  useLanguageStore.setState({ language: 'en', mode: 'english_technical' })
  vi.mocked(api.listTracks).mockResolvedValue(TRACKS)
  vi.mocked(api.getMyEnrollments).mockResolvedValue([ENROLLMENT])
  vi.mocked(api.getSkillScores).mockResolvedValue({ readiness_score: 42, skills: [] })
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 100 })
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.getMyLearningPath).mockResolvedValue(path())
  vi.mocked(api.getRecommendations).mockResolvedValue(NO_RECOMMENDATIONS)
})

describe('the tracks page — no longer a "complete three to unlock AI Engineer" flowchart', () => {
  async function renderTracks() {
    render(<TracksPage />)
    await screen.findByRole('link', { name: 'Explore AI Developer' })
  }

  it('drops every trace of the old apex framing', async () => {
    await renderTracks()
    const text = document.body.textContent ?? ''
    for (const retired of [/Complete any 3/i, /Full Stack AI Engineer/i, /to unlock/i, /End goal/i, /Requirement chips/i, /0 \/ 3/, /contributes to/i]) {
      expect(text).not.toMatch(retired)
    }
  })

  it('uses the five career-track catalogue from the design', async () => {
    await renderTracks()
    expect(screen.getByRole('heading', { name: 'Career tracks' })).toBeInTheDocument()
    expect(screen.getAllByRole('link', { name: /Explore (Data|ML|AI|MLOps)/ })).toHaveLength(5)
  })

  it('shows AI Engineer like any other track, not locked away', async () => {
    await renderTracks()
    expect(screen.getByRole('link', { name: 'Explore AI Engineer' })).toHaveAttribute('href', '/tracks/ai-engineer')
    expect(screen.queryByText(/locked|unlock/i)).toBeNull()
  })

  it('routes the CTA to the canonical track detail', async () => {
    vi.mocked(api.listTracks).mockResolvedValue(TRACKS.map(t => t.slug === 'ai-developer'
      ? { ...t, status: 'current', cta_href: '/courses/course-005/learn', progress: 46 }
      : t))
    render(<TracksPage />)
    const links = await screen.findAllByRole('link', { name: 'Explore Track' })
    expect(links.find(link => link.getAttribute('href') === '/tracks/ai-developer')).toBeDefined()
  })
})

describe('registration', () => {
  function fillAndSubmit(user: ReturnType<typeof userEvent.setup>) {
    return (async () => {
      await user.type(screen.getByLabelText('Full name'), 'Amira Hassan')
      await user.type(screen.getByLabelText('Email'), 'amira@example.com')
      await user.type(screen.getByLabelText('Password'), 'correcthorsebattery')
      await user.click(screen.getByRole('checkbox', { name: /I agree to the/ }))
      await user.click(screen.getByRole('button', { name: /Create account/ }))
    })()
  }

  beforeEach(() => {
    useAuthStore.setState({ token: null, user: null, expiresAt: null, _hasHydrated: true })
    vi.mocked(api.register).mockResolvedValue({
      access_token: 'tok', token_type: 'bearer', expires_in: 3600,
      user: { id: 7, email: 'amira@example.com', full_name: 'Amira Hassan' } as User,
    })
  })

  it('goes straight into the new onboarding', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)
    await fillAndSubmit(user)
    await waitFor(() => expect(router.replace).toHaveBeenCalledWith('/onboarding/quick'))
  })

  it('no longer asks for the level here — it is asked once, in onboarding', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)
    expect(screen.queryByText(/Experience level/i)).toBeNull()
    expect(screen.queryByText('Beginner')).toBeNull()
    await fillAndSubmit(user)
    await waitFor(() => expect(api.register).toHaveBeenCalled())
    // The three fields plus the agreement — the API supplies its own default for the legacy level.
    expect(vi.mocked(api.register).mock.calls[0][0]).toEqual({
      full_name: 'Amira Hassan', email: 'amira@example.com', password: 'correcthorsebattery',
      accept_terms: true, accept_privacy: true,
    })
  })

  it('no longer promises a fixed "AI engineer roadmap"', () => {
    render(<RegisterPage />)
    expect(screen.queryByText(/personalized AI engineer roadmap/i)).toBeNull()
    expect(screen.getByText(/where you are and where you want to go/)).toBeInTheDocument()
  })
})

describe('the sidebar', () => {
  beforeEach(() => resetNav())

  it('keeps Your Masar and Explore among the consolidated destinations', () => {
    render(<AppShell><p>page</p></AppShell>)
    const hrefs = screen.getAllByRole('link').map((a) => a.getAttribute('href'))
    for (const existing of ['/', '/tools', '/glossary', '/mentor', '/community', '/challenges']) {
      expect(hrefs).toContain(existing)
    }
    expect(hrefs).toContain('/learn/masar')
    expect(hrefs).toContain('/explore')
  })

  it('puts the personalised path ahead of Explore', () => {
    render(<AppShell><p>page</p></AppShell>)
    const hrefs = screen.getAllByRole('link').map((a) => a.getAttribute('href'))
    expect(hrefs.indexOf('/learn/masar')).toBeLessThan(hrefs.indexOf('/explore'))
  })

  // The "Ask your AI mentor" quick action that used to sit above the sign-out button is gone
  // (the handoff's sidebar has none; the mentor is in the navigation). Its arrow-mirroring guard
  // went with it. The sidebar's structure is pinned in components/layout/AppShell.test.tsx.

  it('labels the new entries in Arabic for an Arabic reader', () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    render(<AppShell><p>page</p></AppShell>)
    expect(screen.getByRole('link', { name: 'مسارك' })).toHaveAttribute('href', '/learn/masar')
    expect(screen.getByRole('link', { name: 'استكشف' })).toHaveAttribute('href', '/explore')
  })
})

describe('the dashboard greeting', () => {
  const at = (hour: number) => vi.spyOn(Date.prototype, 'getHours').mockReturnValue(hour)

  it('greets by the time of day, in English, with the first name', async () => {
    for (const [hour, text] of [[8, 'Good morning, Amira'], [14, 'Good afternoon, Amira'], [20, 'Good evening, Amira']] as const) {
      const spy = at(hour)
      const { unmount } = render(<DashboardPage />)
      expect(await screen.findByRole('heading', { level: 1, name: text })).toBeInTheDocument()
      unmount()
      spy.mockRestore()
    }
  })

  it('says the same in formal Arabic — the morning greeting, then the evening one (Arabic has no separate "afternoon")', async () => {
    useLanguageStore.setState({ language: 'ar' })
    for (const [hour, text] of [[8, 'صباح الخير، Amira'], [14, 'مساء الخير، Amira'], [20, 'مساء الخير، Amira']] as const) {
      const spy = at(hour)
      const { unmount } = render(<DashboardPage />)
      expect(await screen.findByRole('heading', { level: 1, name: text })).toBeInTheDocument()
      unmount()
      spy.mockRestore()
    }
  })

  it('has its subtitle in both languages, and no hard-coded English left in Arabic', async () => {
    const { unmount } = render(<DashboardPage />)
    expect(await screen.findByText("Here's your learning snapshot today.")).toBeInTheDocument()
    unmount()
    useLanguageStore.setState({ language: 'ar' })
    render(<DashboardPage />)
    expect(await screen.findByText('ملخص تعلّمك اليوم.')).toBeInTheDocument()
    expect(screen.queryByText(/Good (morning|afternoon|evening)/)).toBeNull()
    expect(screen.queryByText(/learning snapshot/)).toBeNull()
  })
})

describe('the dashboard — old learners keep everything and are invited in', () => {
  it('still shows their enrolled tracks', async () => {
    render(<DashboardPage />)
    expect(await screen.findByText('AI Developer')).toBeInTheDocument()
    // Two different destinations, two different labels: the track's "Continue"
    // and the roadmap card's "Continue Learning" must not be indistinguishable.
    expect(screen.getByRole('link', { name: 'Continue' })).toHaveAttribute('href', '/tracks/ai-developer')
    expect(screen.getByRole('link', { name: /Continue Learning/ })).toHaveAttribute('href', '/tools/langchain')
  })

  it('invites an account that has not done the new onboarding — without redirecting it', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    render(<DashboardPage />)
    expect(await screen.findByText('Build your personalized roadmap')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Build My Roadmap/ })).toHaveAttribute('href', '/onboarding/learning-profile')
    expect(router.replace).not.toHaveBeenCalled()
    expect(await screen.findByText('AI Developer')).toBeInTheDocument() // the old dashboard is intact
  })

  it('shows the roadmap prominently — above the metrics — with the next action', async () => {
    render(<DashboardPage />)
    const card = (await screen.findByText('Your Roadmap')).closest('div[class*="p-5"]') as HTMLElement
    expect(within(card).getByText('72%')).toBeInTheDocument()
    expect(within(card).getByRole('link', { name: /Continue Learning/ })).toHaveAttribute('href', '/tools/langchain')
    expect(within(card).getByRole('link', { name: 'View Full Roadmap' })).toHaveAttribute('href', '/learn/masar')
    // ahead of the metrics tiles in the page
    const metrics = screen.getByText('Readiness score')
    expect(card.compareDocumentPosition(metrics) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  })

  it('no longer labels the readiness score as "AI Engineer path"', async () => {
    render(<DashboardPage />)
    await screen.findByText('AI Developer')
    expect(document.body).not.toHaveTextContent('AI Engineer path')
    expect(screen.getByText('Overall')).toBeInTheDocument()
  })

  it('no longer tells an empty dashboard to "start the AI Engineer path"', async () => {
    vi.mocked(api.getMyEnrollments).mockResolvedValue([])
    render(<DashboardPage />)
    expect(await screen.findByText('Build your Masar, or browse the curriculum libraries.')).toBeInTheDocument()
    expect(document.body).not.toHaveTextContent('Start the AI Engineer path')
  })
})

describe('controls that navigate are links; controls that act are buttons', () => {
  // A link that holds a button is two tab stops for one control. Each of these
  // used to be `<Link><Button/></Link>`.
  async function renderDashboard() {
    render(<DashboardPage />)
    await screen.findByText('AI Developer')
  }

  it('the dashboard: an enrolled track, the mentor and the empty skill list', async () => {
    vi.mocked(api.getSkillScores).mockResolvedValue({ readiness_score: 0, skills: [] })
    await renderDashboard()
    const cont = screen.getByRole('link', { name: 'Continue' })
    expectLinkStyledAsButton(cont, '/tracks/ai-developer')
    expectMirroredArrow(cont)
    expect(screen.getByText('Skill scores')).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: /Run skill gap analysis/ })).toBeNull()
    const mentor = screen.getByRole('link', { name: /Open mentor/ })
    expectLinkStyledAsButton(mentor, '/mentor')
    expect(mentor.className).toContain('w-full') // still fills its card
  })

  it('the dashboard with no tracks: Browse tracks', async () => {
    vi.mocked(api.getMyEnrollments).mockResolvedValue([])
    render(<DashboardPage />)
    expectLinkStyledAsButton(await screen.findByRole('link', { name: 'Browse tracks' }), '/tracks')
  })

  it('the tracks page: the card and its CTA are real links', async () => {
    vi.mocked(api.listTracks).mockResolvedValue(TRACKS.map(t => t.slug === 'ai-developer'
      ? { ...t, status: 'current', cta_href: '/courses/course-005/learn' }
      : t))
    render(<TracksPage />)
    expect(await screen.findByRole('link', { name: 'Explore AI Developer' })).toHaveAttribute('href', '/tracks/ai-developer')
    const cta = screen.getAllByRole('link', { name: 'Explore Track' }).find(link => link.getAttribute('href') === '/tracks/ai-developer')
    expect(cta).toBeDefined()
    expectLinkStyledAsButton(cta as HTMLElement, '/tracks/ai-developer')
  })

  it('a link is one tab stop and Enter follows it', async () => {
    const user = userEvent.setup()
    render(<TracksPage />)
    const masar = await screen.findByRole('link', { name: 'Explore Data Analyst' })
    const followed = vi.fn((e: Event) => e.preventDefault()) // jsdom cannot navigate
    masar.addEventListener('click', followed)
    let stops = 0
    for (let i = 0; i < 60 && document.activeElement !== masar; i++) {
      await user.tab()
      if (document.activeElement === masar) stops++
    }
    expect(document.activeElement).toBe(masar)
    await user.tab() // one press moves past it: nothing focusable is inside
    expect(masar.contains(document.activeElement)).toBe(false)
    expect(stops).toBe(1)
    masar.focus()
    await user.keyboard('{Enter}')
    expect(followed).toHaveBeenCalledTimes(1)
  })

  it.each([
    ['done', '/certificates'],
    ['open', '/courses/course-001'],
  ] as const)('track status %s keeps canonical detail navigation as a link', async (status, href) => {
    vi.mocked(api.listTracks).mockResolvedValue([{ ...TRACKS[0], status, cta_href: href }])
    render(<TracksPage />)
    expect(await screen.findByRole('link', { name: 'Explore Track' })).toHaveAttribute('href', '/tracks/data-analyst')
  })

  it('an Arabic reader gets the same links, with the arrows mirrored', async () => {
    useLanguageStore.setState({ language: 'ar' })
    await renderDashboard()
    // "Continue" is in Arabic now: the dashboard used to leave it in English on an Arabic page.
    expectMirroredArrow(screen.getByRole('link', { name: /أكمل/ }))
  })
})
