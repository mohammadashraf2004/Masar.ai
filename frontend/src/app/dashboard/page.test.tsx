import { render, waitFor, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import DashboardPage from './page'
import { useAuthStore } from '@/lib/store'
import { STRINGS } from '@/lib/i18n'
import { useLanguageStore } from '@/lib/language'
import { setPathname } from '@/test/nav'
import type { User } from '@/types'

vi.mock('@/lib/api', () => ({
  api: {
    getWallet: vi.fn(), search: vi.fn(), getMyEnrollments: vi.fn(), getSkillScores: vi.fn(),
    getMyLearningProfile: vi.fn(), getMyLearningPath: vi.fn(), getRecommendations: vi.fn(),
    getVocabulary: vi.fn(), getVocabularyProgress: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const user: User = {
  id: 1, email: 'amira@example.com', full_name: 'Amira Hassan', role: 'student', experience_level: 'beginner',
  is_verified: true, overall_readiness_score: 42, created_at: '2026-01-01T00:00:00Z',
  requires_legal_acceptance: false, pending_updates: [],
}

beforeEach(() => {
  setPathname('/dashboard')
  useAuthStore.setState({ token: 'tok', expiresAt: null, _hasHydrated: true, user })
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 100 })
  vi.mocked(api.getMyEnrollments).mockResolvedValue([])
  vi.mocked(api.getSkillScores).mockResolvedValue({ skills: [] } as never)
  vi.mocked(api.getMyLearningProfile).mockResolvedValue({ needs_onboarding: true, source: 'new', career_goal: null } as never)
  vi.mocked(api.getRecommendations).mockResolvedValue({ continue_learning: [], recommended_next: [] } as never)
})

describe('the phone\'s Challenges row', () => {
  it('sits under the roadmap card, says what challenges are and links to them', async () => {
    const { container } = render(<DashboardPage />)
    await waitFor(() => expect(container.querySelector('[data-tour="practice"]')).not.toBeNull())
    const row = container.querySelector<HTMLElement>('[data-tour="practice"]')!
    expect(within(row).getByRole('heading', { name: STRINGS.en['nav.challenges'] })).toBeInTheDocument()
    expect(within(row).getByText(STRINGS.en['dash.challenges.body'])).toBeInTheDocument()
    expect(within(row).getByRole('link', { name: new RegExp(STRINGS.en['dash.challenges.cta']) })).toHaveAttribute('href', '/challenges')
    // Only a phone has it: from `lg` the sidebar has Challenges.
    expect(row.className).toContain('lg:hidden')
    // Directly after the roadmap card.
    expect(container.querySelector('[data-tour="path"]')?.nextElementSibling).toBe(row)
  })

  it('is in Arabic for an Arabic reader', async () => {
    useLanguageStore.setState({ language: 'ar' })
    const { container } = render(<DashboardPage />)
    await waitFor(() => expect(container.querySelector('[data-tour="practice"]')).not.toBeNull())
    expect(within(container.querySelector<HTMLElement>('[data-tour="practice"]')!).getByText(STRINGS.ar['dash.challenges.body'])).toBeInTheDocument()
  })

  it('tags the mentor button the walkthrough points at on a phone', async () => {
    const { container } = render(<DashboardPage />)
    await waitFor(() => expect(container.querySelector('a[data-tour="mentor"]')).toHaveAttribute('href', '/mentor'))
  })
})
