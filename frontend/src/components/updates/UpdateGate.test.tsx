import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { UpdateGate } from '@/components/updates/UpdateGate'
import { useLanguageStore } from '@/lib/language'
import { FIRST_ROADMAP_INTRO, WHATS_NEW } from '@/lib/releases'
import { useAuthStore } from '@/lib/store'
import { NEEDS_ONBOARDING, NO_GAPS_YET, gapItem, path, profile, skillGaps, RAG_SKILL } from '@/test/fixtures'
import { setPathname } from '@/test/nav'
import type { User } from '@/types'

vi.mock('@/lib/api', () => ({
  api: {
    acknowledgeUpdate: vi.fn(), getMyLearningProfile: vi.fn(), getMyLearningPath: vi.fn(), getMySkillGaps: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const account = (over: Partial<User> = {}) =>
  ({ id: 7, email: 'a@example.com', full_name: 'Amira Hassan', requires_legal_acceptance: false, pending_updates: [], ...over }) as User

function signIn(over: Partial<User> = {}) {
  useAuthStore.setState({ token: 'tok', user: account(over), expiresAt: null, _hasHydrated: true })
}
const stored = () => useAuthStore.getState().user as User

// jsdom cannot navigate; a click on a link is all these tests need (the href is asserted).
beforeEach(() => {
  const stop = (e: Event) => { if ((e.target as Element).closest?.('a')) e.preventDefault() }
  document.addEventListener('click', stop)
  return () => document.removeEventListener('click', stop)
})

beforeEach(() => {
  useAuthStore.setState({ token: null, user: null, expiresAt: null, _hasHydrated: true })
  setPathname('/dashboard')
  vi.mocked(api.acknowledgeUpdate).mockReset()
  vi.mocked(api.acknowledgeUpdate).mockImplementation(async () => account({ pending_updates: [] }))
  vi.mocked(api.getMyLearningProfile).mockReset().mockResolvedValue(profile())
  vi.mocked(api.getMyLearningPath).mockReset().mockResolvedValue(path())
  vi.mocked(api.getMySkillGaps).mockReset().mockResolvedValue(skillGaps())
})

async function settled() {
  await act(async () => { await new Promise((resolve) => setTimeout(resolve, 0)) })
}

// ─── An account that existed before the release: "New in Masar" ──────────────

describe('What\'s New — an existing account', () => {
  beforeEach(() => signIn({ pending_updates: [WHATS_NEW] }))

  it('opens once, as a named and described dialog, with the three things that are new', async () => {
    render(<UpdateGate />)
    const dialog = await screen.findByRole('dialog', { name: 'New in Masar' })
    expect(dialog).toHaveAttribute('aria-modal', 'true')
    expect(dialog).toHaveAccessibleDescription('Your learning roadmap is now more personalized.')
    expect(within(dialog).getByRole('heading', { name: 'Skill gap analysis' })).toBeInTheDocument()
    expect(within(dialog).getByRole('heading', { name: 'Why this course?' })).toBeInTheDocument()
    expect(within(dialog).getByRole('heading', { name: 'A better roadmap' })).toBeInTheDocument()
    expect(dialog).toHaveTextContent('See the skills you already know')
    expect(dialog).toHaveTextContent('why each course appears in your roadmap')
    expect(dialog).toHaveTextContent('career goal, interests, existing skills, and learning progress')
  })

  it('leads to the existing roadmap, and offers "Maybe later"', async () => {
    render(<UpdateGate />)
    expect(await screen.findByRole('link', { name: 'Explore My Skill Gaps' })).toHaveAttribute('href', '/learn/masar')
    expect(screen.getByRole('button', { name: 'Maybe later' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Close' })).toBeInTheDocument()
  })

  it('is only an introduction: it draws no skill list, no course card and no progress of its own', async () => {
    render(<UpdateGate />)
    const dialog = await screen.findByRole('dialog')
    expect(within(dialog).queryByRole('progressbar')).toBeNull()
    expect(api.getMySkillGaps).not.toHaveBeenCalled()      // it does not even ask for the analysis
    expect(dialog).not.toHaveTextContent('RAG')
  })

  it('does not describe anything the app does not have — no engine, no AI, no percentages', async () => {
    render(<UpdateGate />)
    const text = (await screen.findByRole('dialog')).textContent ?? ''
    expect(text).not.toMatch(/deterministic|engine|algorithm|machine learning|AI-powered|%/i)
  })

  it('moves focus to the main action, so Enter takes the learner to the roadmap', async () => {
    render(<UpdateGate />)
    const cta = await screen.findByRole('link', { name: 'Explore My Skill Gaps' })
    expect(cta).toHaveFocus()
  })

  it('reads in Arabic, in formal Arabic, with the feature names in the app\'s own words', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<UpdateGate />)
    const dialog = await screen.findByRole('dialog', { name: 'جديد في مسار' })
    expect(dialog).toHaveAccessibleDescription('أصبح مسارك التعليمي أكثر تخصيصاً.')
    expect(within(dialog).getByRole('heading', { name: 'تحليل فجوات المهارات' })).toBeInTheDocument()
    expect(within(dialog).getByRole('heading', { name: 'لماذا هذه الدورة؟' })).toBeInTheDocument()   // the same words as the toggle itself
    expect(within(dialog).getByRole('link', { name: 'استكشف فجوات مهاراتي' })).toHaveAttribute('href', '/learn/masar')
    expect(within(dialog).getByRole('button', { name: 'ربما لاحقاً' })).toBeInTheDocument()
    expect(within(dialog).getByRole('button', { name: 'إغلاق' })).toBeInTheDocument()
  })

  it('puts the close button on the logical end edge, so it follows the reading direction', async () => {
    render(<UpdateGate />)
    const close = await screen.findByRole('button', { name: 'Close' })
    expect(close).toHaveClass('end-1.5')
    expect(close.className).not.toMatch(/\b(left|right)-/)
  })
})

describe('What\'s New — an existing account without a roadmap', () => {
  beforeEach(() => signIn({ pending_updates: [WHATS_NEW] }))

  it('does not lead to a skill gap that cannot exist: it says so and offers to build the roadmap', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    render(<UpdateGate />)
    const dialog = await screen.findByRole('dialog', { name: 'New in Masar' })
    expect(dialog).toHaveAccessibleDescription(/Build your roadmap to see the skills you know/)
    expect(within(dialog).getByRole('link', { name: 'Build My Roadmap' })).toHaveAttribute('href', '/onboarding/learning-profile')
    expect(within(dialog).queryByRole('link', { name: 'Explore My Skill Gaps' })).toBeNull()
    expect(api.getMyLearningPath).not.toHaveBeenCalled()
  })

  it('does the same for a learner who answered the questions but has no path', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(null)
    render(<UpdateGate />)
    expect(await screen.findByRole('link', { name: 'Build My Roadmap' })).toHaveAttribute('href', '/onboarding/learning-profile')
  })

  it('falls back to the roadmap page when it cannot tell — that page decides for itself', async () => {
    vi.mocked(api.getMyLearningProfile).mockRejectedValue(new Error('down'))
    render(<UpdateGate />)
    expect(await screen.findByRole('link', { name: 'Explore My Skill Gaps' })).toHaveAttribute('href', '/learn/masar')
  })

  it('draws nothing while it works out where the button leads — no flash of the wrong one', async () => {
    vi.mocked(api.getMyLearningProfile).mockReturnValue(new Promise(() => {}))
    const { container } = render(<UpdateGate />)
    await settled()
    expect(container).toBeEmptyDOMElement()
  })
})

// ─── Acknowledging ───────────────────────────────────────────────────────────

describe('acknowledging What\'s New', () => {
  beforeEach(() => signIn({ pending_updates: [WHATS_NEW] }))

  const ways: Array<[string, () => Promise<void>]> = [
    ['the main button', async () => { await userEvent.click(await screen.findByRole('link', { name: 'Explore My Skill Gaps' })) }],
    ['"Maybe later"', async () => { await userEvent.click(await screen.findByRole('button', { name: 'Maybe later' })) }],
    ['the close button', async () => { await userEvent.click(await screen.findByRole('button', { name: 'Close' })) }],
    ['Escape', async () => { await screen.findByRole('dialog'); await userEvent.keyboard('{Escape}') }],
  ]

  it.each(ways)('by %s: the server is told once, the dialog closes and it is gone from the stored account', async (_name, act_) => {
    render(<UpdateGate />)
    await act_()
    expect(api.acknowledgeUpdate).toHaveBeenCalledTimes(1)
    expect(api.acknowledgeUpdate).toHaveBeenCalledWith(WHATS_NEW)
    await waitFor(() => expect(screen.queryByRole('dialog')).toBeNull())
    expect(stored().pending_updates).toEqual([])
  })

  it('does not ask twice for a double click', async () => {
    render(<UpdateGate />)
    const later = await screen.findByRole('button', { name: 'Maybe later' })
    await userEvent.dblClick(later)
    expect(api.acknowledgeUpdate).toHaveBeenCalledTimes(1)
  })

  it('does not reappear after a remount, a refresh of the page, or a second visit to another page', async () => {
    const first = render(<UpdateGate />)
    await userEvent.click(await screen.findByRole('button', { name: 'Maybe later' }))
    first.unmount()
    for (const place of ['/dashboard', '/', '/learn']) {
      setPathname(place)
      const again = render(<UpdateGate />)
      await settled()
      expect(again.container).toBeEmptyDOMElement()
      again.unmount()
    }
    expect(api.acknowledgeUpdate).toHaveBeenCalledTimes(1)
  })

  it('takes only the list from the server\'s answer', async () => {
    vi.mocked(api.acknowledgeUpdate).mockImplementation(async () => account({ full_name: 'Someone Else', pending_updates: [FIRST_ROADMAP_INTRO] }))
    render(<UpdateGate />)
    await userEvent.click(await screen.findByRole('button', { name: 'Maybe later' }))
    await waitFor(() => expect(stored().pending_updates).toEqual([FIRST_ROADMAP_INTRO]))
    expect(stored().full_name).toBe('Amira Hassan')          // only the list was taken
  })

  it('never overwrites a different account that signed in while the request was out', async () => {
    let release: (u: User) => void = () => {}
    vi.mocked(api.acknowledgeUpdate).mockImplementation(() => new Promise<User>((r) => { release = r }))
    render(<UpdateGate />)
    await userEvent.click(await screen.findByRole('button', { name: 'Maybe later' }))
    signIn({ id: 99, full_name: 'Other Account', pending_updates: [WHATS_NEW] })
    await act(async () => { release(account({ id: 7, pending_updates: [] })) })
    expect(stored().id).toBe(99)
    expect(stored().pending_updates).toEqual([WHATS_NEW])
  })

  it('survives a failed request: no crash, navigation still works, and it is not asked again this session', async () => {
    vi.mocked(api.acknowledgeUpdate).mockRejectedValue(new Error('network'))
    render(<UpdateGate />)
    const cta = await screen.findByRole('link', { name: 'Explore My Skill Gaps' })
    await userEvent.click(cta)                                   // the link still navigates: nothing waits for the answer
    await settled()
    expect(api.acknowledgeUpdate).toHaveBeenCalledTimes(1)
    expect(screen.queryByRole('dialog')).toBeNull()              // not stuck open
    expect(stored().pending_updates).toEqual([])                 // not offered again until the server can be told
  })
})

// ─── Who is asked, and where ─────────────────────────────────────────────────

describe('when nothing is shown', () => {
  it.each([
    ['a signed-out visitor', () => useAuthStore.setState({ token: null, user: null })],
    ['an account with nothing pending', () => signIn({ pending_updates: [] })],
    ['a session that predates the field', () => signIn({ pending_updates: undefined })],
    ['an announcement this build cannot draw', () => signIn({ pending_updates: ['2031-01-something-else'] })],
  ])('%s', async (_name, setup) => {
    setup()
    const { container } = render(<UpdateGate />)
    await settled()
    expect(container).toBeEmptyDOMElement()
  })

  it('waits for the Terms to be accepted, and while it is not yet known whether they are', async () => {
    for (const requires of [true, undefined]) {
      signIn({ pending_updates: [WHATS_NEW], requires_legal_acceptance: requires })
      const { container, unmount } = render(<UpdateGate />)
      await settled()
      expect(container).toBeEmptyDOMElement()
      unmount()
    }
    signIn({ pending_updates: [WHATS_NEW], requires_legal_acceptance: false })
    render(<UpdateGate />)
    expect(await screen.findByRole('dialog')).toBeInTheDocument()
  })

  it.each(['/', '/dashboard', '/learn'])('appears where a learner lands: %s', async (place) => {
    signIn({ pending_updates: [WHATS_NEW] })
    setPathname(place)
    render(<UpdateGate />)
    expect(await screen.findByRole('dialog')).toBeInTheDocument()
  })

  it.each(['/exam/12', '/tools/langchain', '/tracks/ai-developer', '/courses/rag', '/onboarding/learning-profile', '/auth/login', '/terms', '/profile'])(
    'never interrupts %s', async (place) => {
      signIn({ pending_updates: [WHATS_NEW] })
      setPathname(place)
      const { container } = render(<UpdateGate />)
      await settled()
      expect(container).toBeEmptyDOMElement()
    })
})

// ─── A new account: the introduction, in its first roadmap ───────────────────

describe('the skill-gap introduction — a new account', () => {
  beforeEach(() => {
    signIn({ pending_updates: [FIRST_ROADMAP_INTRO] })
    setPathname('/learn')
  })

  it('is not the "What\'s New" an existing account gets — and is not shown while signing up or onboarding', async () => {
    for (const place of ['/auth/register', '/onboarding/learning-profile']) {
      setPathname(place)
      const { container, unmount } = render(<UpdateGate />)
      await settled()
      expect(container).toBeEmptyDOMElement()
      expect(screen.queryByRole('dialog', { name: 'New in Masar' })).toBeNull()
      unmount()
    }
    expect(api.getMySkillGaps).not.toHaveBeenCalled()
  })

  it('shows nothing until there is a roadmap to introduce — an account that has not built one sees no "skill gap"', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(NO_GAPS_YET)
    const { container } = render(<UpdateGate />)
    await settled()
    expect(container).toBeEmptyDOMElement()
  })

  it('shows nothing when the analysis cannot be loaded, rather than an introduction to nothing', async () => {
    vi.mocked(api.getMySkillGaps).mockRejectedValue(new Error('down'))
    const { container } = render(<UpdateGate />)
    await settled()
    expect(container).toBeEmptyDOMElement()
  })

  it('once the roadmap exists, says the skill gap is ready with the real number, and where to see it', async () => {
    render(<UpdateGate />)
    const dialog = await screen.findByRole('dialog', { name: 'Your skill gap is ready' })
    expect(dialog).toHaveAccessibleDescription(/Based on your career goal, field, level, and existing skills, Masar identified the skills you already know/)
    // skillGaps(): 1 in progress + 3 missing = 4 still to gain, of 5 relevant, 1 known — the server's numbers
    expect(within(dialog).getByText('4 skills to gain')).toBeInTheDocument()
    expect(within(dialog).getByText('You know 1 of 5 skills')).toBeInTheDocument()
    expect(within(dialog).getByRole('link', { name: 'View My Skill Gaps' })).toHaveAttribute('href', '/learn/masar')
  })

  it('uses whatever the backend counted — nothing is hard-coded', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      summary: { required: 30, known: 9, partial: 0, missing: 21, immediate: 3, coverage_pct: 30 },
      partial: [], missing: Array.from({ length: 21 }, (_, i) => gapItem({ slug: `s${i}`, name: `S${i}`, name_ar: null })),
    }))
    render(<UpdateGate />)
    expect(await screen.findByText('21 skills to gain')).toBeInTheDocument()
    expect(screen.getByText('You know 9 of 30 skills')).toBeInTheDocument()
  })

  it('is singular for one skill', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      summary: { required: 2, known: 1, partial: 0, missing: 1, immediate: 1, coverage_pct: 50 },
      partial: [], missing: [gapItem(RAG_SKILL)],
    }))
    render(<UpdateGate />)
    expect(await screen.findByText('1 skill to gain')).toBeInTheDocument()
  })

  it('does not say "0 skills to gain" for a learner with nothing left: it says they have it all', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      summary: { required: 3, known: 3, partial: 0, missing: 0, immediate: 0, coverage_pct: 100 },
      partial: [], missing: [], groups: [],
    }))
    render(<UpdateGate />)
    const dialog = await screen.findByRole('dialog', { name: 'Your skill gap is ready' })
    expect(dialog).toHaveAccessibleDescription(/there is nothing left to gain: you have added every skill your roadmap covers/)
    expect(dialog).not.toHaveTextContent(/0 skills? to gain/)
    expect(dialog).not.toHaveTextContent('skills to gain')
    expect(within(dialog).getByRole('link', { name: 'View My Roadmap' })).toHaveAttribute('href', '/learn/masar')
    expect(within(dialog).queryByRole('link', { name: 'View My Skill Gaps' })).toBeNull()
  })

  it('shows nothing when no skills are relevant yet', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      summary: { required: 0, known: 0, partial: 0, missing: 0, immediate: 0, coverage_pct: null },
      partial: [], missing: [], groups: [],
    }))
    const { container } = render(<UpdateGate />)
    await settled()
    expect(container).toBeEmptyDOMElement()
  })

  it('does not rebuild the roadmap inside the dialog: no skill list, no courses, no progress', async () => {
    render(<UpdateGate />)
    const dialog = await screen.findByRole('dialog')
    expect(within(dialog).queryByRole('list')).toBeNull()
    expect(within(dialog).queryByRole('progressbar')).toBeNull()
    expect(within(dialog).queryByRole('region')).toBeNull()
    expect(dialog).not.toHaveTextContent('RAG')            // a named skill from the analysis
    expect(dialog).not.toHaveTextContent('Vector')
  })

  it.each([
    ['the main button', async () => { await userEvent.click(await screen.findByRole('link', { name: 'View My Skill Gaps' })) }],
    ['"Maybe later"', async () => { await userEvent.click(await screen.findByRole('button', { name: 'Maybe later' })) }],
    ['Escape', async () => { await screen.findByRole('dialog'); await userEvent.keyboard('{Escape}') }],
  ])('is acknowledged once by %s and does not come back', async (_name, dismiss) => {
    const first = render(<UpdateGate />)
    await dismiss()
    expect(api.acknowledgeUpdate).toHaveBeenCalledTimes(1)
    expect(api.acknowledgeUpdate).toHaveBeenCalledWith(FIRST_ROADMAP_INTRO)
    await waitFor(() => expect(screen.queryByRole('dialog')).toBeNull())
    first.unmount()
    const again = render(<UpdateGate />)
    await settled()
    expect(again.container).toBeEmptyDOMElement()
  })

  it('reads in Arabic, with the plural of the number in the right form', async () => {
    useLanguageStore.setState({ language: 'ar' })
    const cases: Array<[number, string]> = [[1, 'مهارة واحدة ستكتسبها'], [2, 'مهارتان ستكتسبهما'], [4, '4 مهارات ستكتسبها'], [12, '12 مهارة ستكتسبها']]
    for (const [n, text] of cases) {
      vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
        summary: { required: n + 1, known: 1, partial: 0, missing: n, immediate: 0, coverage_pct: 10 },
        partial: [], missing: Array.from({ length: n }, (_, i) => gapItem({ slug: `s${i}`, name: `S${i}`, name_ar: null })),
      }))
      const { unmount } = render(<UpdateGate />)
      const dialog = await screen.findByRole('dialog', { name: 'فجوات مهاراتك جاهزة' })
      expect(within(dialog).getByText(text)).toBeInTheDocument()
      expect(within(dialog).getByRole('link', { name: 'عرض فجوات مهاراتي' })).toHaveAttribute('href', '/learn/masar')
      unmount()
    }
  })

  it('an account that already saw What\'s New is never introduced again: the server has nothing pending', async () => {
    signIn({ pending_updates: [] })
    const { container } = render(<UpdateGate />)
    await settled()
    expect(container).toBeEmptyDOMElement()
    expect(api.getMySkillGaps).not.toHaveBeenCalled()
  })
})
