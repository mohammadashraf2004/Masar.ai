import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import LearningOnboardingPage from '@/app/onboarding/learning-profile/page'
import { useLanguageStore } from '@/lib/language'
import { CATALOG, NEEDS_ONBOARDING, SKILL_OPTIONS, path, profile } from '@/test/fixtures'
import { router } from '@/test/nav'

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
}))
vi.mock('@/lib/api', () => ({
  api: {
    getLearningLevels: vi.fn(), getLearningFields: vi.fn(), getCareerGoals: vi.fn(),
    getMyLearningProfile: vi.fn(), saveMyLearningProfile: vi.fn(), saveMyLearningPath: vi.fn(),
    getSkillOptions: vi.fn(),
  },
}))
import { api } from '@/lib/api'

beforeEach(() => {
  vi.mocked(api.getLearningLevels).mockResolvedValue(CATALOG.levels)
  vi.mocked(api.getLearningFields).mockResolvedValue(CATALOG.fields)
  vi.mocked(api.getCareerGoals).mockResolvedValue(CATALOG.goals)
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
  vi.mocked(api.saveMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.saveMyLearningPath).mockResolvedValue(path())
  vi.mocked(api.getSkillOptions).mockResolvedValue(SKILL_OPTIONS)
})

describe('the onboarding page', () => {
  it('starts a new learner at "Where are you now?" with nothing chosen', async () => {
    render(<LearningOnboardingPage />)
    expect(await screen.findByRole('heading', { name: 'Where are you now?' })).toBeInTheDocument()
    screen.getAllByRole('radio').forEach((r) => expect(r).toHaveAttribute('aria-checked', 'false'))
    expect(screen.queryByText(/kept your earlier career goal/)).toBeNull()
  })

  it('takes a migrated learner in with their old career goal kept and named — and level and fields empty', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile({
      level: null, fields: [], onboarding_completed: false, needs_onboarding: true, source: 'migrated',
      career_goal: { slug: 'ai-developer', title: 'AI Developer', title_ar: 'مطوّر تطبيقات ذكاء اصطناعي', icon: 'code' },
    }))
    render(<LearningOnboardingPage />)
    expect(await screen.findByText('We kept your earlier career goal: AI Developer.')).toBeInTheDocument()
    screen.getAllByRole('radio').forEach((r) => expect(r).toHaveAttribute('aria-checked', 'false')) // no level guessed

    await user.click(screen.getByRole('radio', { name: /Beginner/ }))
    await user.click(screen.getByRole('button', { name: /Continue/ }))
    expect(screen.getAllByRole('checkbox').filter((c) => c.getAttribute('aria-checked') === 'true')).toHaveLength(0) // no field guessed
    await user.click(screen.getByRole('checkbox', { name: /NLP & LLMs/ }))
    await user.click(screen.getByRole('button', { name: /Continue/ }))
    expect(screen.getByRole('radio', { name: /AI Developer/ })).toHaveAttribute('aria-checked', 'true') // the kept goal
  })

  it('completes the flow and lands on Your Masar', async () => {
    const user = userEvent.setup()
    render(<LearningOnboardingPage />)
    await user.click(await screen.findByRole('radio', { name: /Intermediate/ }))
    await user.click(screen.getByRole('button', { name: /Continue/ }))
    await user.click(screen.getByRole('checkbox', { name: /NLP & LLMs/ }))
    await user.click(screen.getByRole('button', { name: /Continue/ }))
    await user.click(screen.getByRole('radio', { name: /AI Engineer/ }))
    await user.click(screen.getByRole('button', { name: /Continue/ }))
    await user.click(await screen.findByRole('checkbox', { name: /RAG/ }))
    await user.click(screen.getByRole('button', { name: /Build My Roadmap/ }))
    await waitFor(() => expect(router.replace).toHaveBeenCalledWith('/learn/masar'))
    expect(api.saveMyLearningProfile).toHaveBeenCalledWith(expect.objectContaining({ known_skills: ['rag'] }))
  })

  it('shows an error with a retry when the options cannot be loaded', async () => {
    vi.mocked(api.getLearningFields).mockRejectedValue(new Error('down'))
    render(<LearningOnboardingPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load the options')
    expect(screen.getByRole('button', { name: 'Try again' })).toBeInTheDocument()
  })

  it('still works if the profile call fails — onboarding must never be blocked by it', async () => {
    vi.mocked(api.getMyLearningProfile).mockRejectedValue(new Error('down'))
    render(<LearningOnboardingPage />)
    expect(await screen.findByRole('heading', { name: 'Where are you now?' })).toBeInTheDocument()
  })

  it('is written in Arabic for an Arabic reader', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    render(<LearningOnboardingPage />)
    expect(await screen.findByRole('heading', { name: 'أين أنت الآن؟' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'ابنِ مسارك' })).toBeInTheDocument()
  })

  it('starts the skills step from the skills the learner already declared', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile({
      level: null, fields: [], career_goal: null,
      known_skills: [{ slug: 'rag', name: 'RAG', name_ar: null }], onboarding_completed: false, needs_onboarding: true,
    }))
    render(<LearningOnboardingPage />)
    await user.click(await screen.findByRole('radio', { name: /Intermediate/ }))
    await user.click(screen.getByRole('button', { name: /Continue/ }))
    await user.click(screen.getByRole('checkbox', { name: /NLP & LLMs/ }))
    await user.click(screen.getByRole('button', { name: /Continue/ }))
    await user.click(screen.getByRole('radio', { name: /AI Engineer/ }))
    await user.click(screen.getByRole('button', { name: /Continue/ }))
    expect(await screen.findByRole('checkbox', { name: /RAG/ })).toBeChecked()
  })
})
