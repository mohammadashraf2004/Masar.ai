import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import LearnPage from '@/app/learn/masar/page'
import { FIRST_ROADMAP_INTRO, WHATS_NEW } from '@/lib/releases'
import { useAuthStore } from '@/lib/store'
import { CATALOG, path, profile, skillGaps } from '@/test/fixtures'
import { setPathname } from '@/test/nav'
import type { User } from '@/types'

// The page inside the same shell composition the app uses: the gate sits beside
// the page, so this is the introduction as a learner meets it on the roadmap.
vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
}))
vi.mock('@/components/layout/AppShell', async () => {
  const { createElement, Fragment } = await import('react')
  const { UpdateGate: Gate } = await import('@/components/updates/UpdateGate')
  return { AppShell: ({ children }: { children: React.ReactNode }) => createElement(Fragment, null, createElement(Gate), children) }
})
vi.mock('@/components/layout/PageHeader', async () => {
  const { createElement } = await import('react')
  return { PageHeader: ({ title }: { title: string }) => createElement('h1', null, title) }
})
vi.mock('@/lib/api', () => ({
  api: {
    getLearningLevels: vi.fn(), getLearningFields: vi.fn(), getCareerGoals: vi.fn(),
    getMyLearningProfile: vi.fn(), getMyLearningPath: vi.fn(), saveMyLearningPath: vi.fn(), getMySkillGaps: vi.fn(),
    acknowledgeUpdate: vi.fn(),
  },
}))
import { api } from '@/lib/api'


const account = (over: Partial<User> = {}) =>
  ({ id: 7, email: 'a@example.com', full_name: 'Amira Hassan', requires_legal_acceptance: false, pending_updates: [], ...over }) as User

beforeEach(() => {
  setPathname('/learn')
  useAuthStore.setState({ token: 'tok', user: account({ pending_updates: [FIRST_ROADMAP_INTRO] }), expiresAt: null, _hasHydrated: true })
  vi.mocked(api.getLearningLevels).mockResolvedValue(CATALOG.levels)
  vi.mocked(api.getLearningFields).mockResolvedValue(CATALOG.fields)
  vi.mocked(api.getCareerGoals).mockResolvedValue(CATALOG.goals)
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.getMyLearningPath).mockResolvedValue(path())
  vi.mocked(api.getMySkillGaps).mockReset().mockResolvedValue(skillGaps())
  vi.mocked(api.acknowledgeUpdate).mockReset().mockResolvedValue(account({ pending_updates: [] }))
})

describe('a new learner arriving on their first roadmap', () => {
  it('sees the skill-gap introduction over the roadmap, with the real count', async () => {
    render(<LearnPage />)
    const dialog = await screen.findByRole('dialog', { name: 'Your skill gap is ready' })
    expect(within(dialog).getByText('4 skills to gain')).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'AI Engineer' })).toBeInTheDocument()   // the roadmap is under it
  })

  it('draws the analysis and the roadmap once — the introduction adds no second copy of either', async () => {
    render(<LearnPage />)
    const dialog = await screen.findByRole('dialog', { name: 'Your skill gap is ready' })
    await screen.findByRole('heading', { name: 'Your skill gaps' })
    expect(screen.getAllByRole('heading', { name: 'Your skill gaps' })).toHaveLength(1)
    expect(screen.getAllByRole('progressbar', { name: 'Skill coverage' })).toHaveLength(1)
    expect(document.querySelectorAll('li[data-status]').length).toBeGreaterThan(0)
    expect(dialog.querySelectorAll('li, [role=progressbar]')).toHaveLength(0)
  })

  it('leaves them on the same roadmap once they continue, and never shows it again', async () => {
    const { unmount } = render(<LearnPage />)
    await userEvent.click(await screen.findByRole('link', { name: 'View My Skill Gaps' }))
    await waitFor(() => expect(screen.queryByRole('dialog')).toBeNull())
    expect(await screen.findByRole('heading', { name: 'Your skill gaps' })).toBeInTheDocument()
    expect(api.acknowledgeUpdate).toHaveBeenCalledWith(FIRST_ROADMAP_INTRO)
    unmount()
    render(<LearnPage />)
    await screen.findByRole('heading', { name: 'AI Engineer' })
    expect(screen.queryByRole('dialog')).toBeNull()
  })
})

describe('an existing learner on the roadmap', () => {
  it('sees What\'s New there too, and Explore keeps them on the roadmap they are already viewing', async () => {
    useAuthStore.setState({ user: account({ pending_updates: [WHATS_NEW] }) })
    render(<LearnPage />)
    const dialog = await screen.findByRole('dialog', { name: 'New in Masar' })
    expect(within(dialog).getByRole('link', { name: 'Explore My Skill Gaps' })).toHaveAttribute('href', '/learn/masar')
    expect(screen.queryByRole('dialog', { name: 'Your skill gap is ready' })).toBeNull()   // one announcement at a time
  })
})
