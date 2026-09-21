import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import LearnPage from '@/app/learn/page'
import { useLanguageStore } from '@/lib/language'
import { CATALOG, MULTIMODAL, NEEDS_ONBOARDING, NLP, path, profile, ref, skillGaps, stage } from '@/test/fixtures'
import { router } from '@/test/nav'

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
    getMyLearningProfile: vi.fn(), getMyLearningPath: vi.fn(), saveMyLearningPath: vi.fn(), getMySkillGaps: vi.fn(),
  },
}))
import { api } from '@/lib/api'

beforeEach(() => {
  vi.mocked(api.getLearningLevels).mockResolvedValue(CATALOG.levels)
  vi.mocked(api.getLearningFields).mockResolvedValue(CATALOG.fields)
  vi.mocked(api.getCareerGoals).mockResolvedValue(CATALOG.goals)
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.getMyLearningPath).mockResolvedValue(path())
  vi.mocked(api.getMySkillGaps).mockReset()
  vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps())
})

describe('Your Masar — the personalised dashboard', () => {
  it('shows the goal, fields, level and progress at the top', async () => {
    render(<LearnPage />)
    expect(await screen.findByRole('heading', { name: 'AI Engineer' })).toBeInTheDocument()
    expect(screen.getByText('NLP & LLMs')).toBeInTheDocument()
    expect(screen.getByText('72%')).toBeInTheDocument()
  })

  it('shows the roadmap with the current stage open', async () => {
    render(<LearnPage />)
    await screen.findByRole('heading', { name: 'AI Engineer' })
    const current = document.querySelector<HTMLElement>('li[aria-current="step"]')!
    expect(within(current).getByText('NLP & LLM Engineering')).toBeInTheDocument()
    expect(within(current).getByRole('link', { name: 'LangChain' })).toBeInTheDocument()
    expect(document.querySelectorAll('li[data-status]')).toHaveLength(5)
  })

  it('shows the notes for a route that needed explaining', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(path({
      fields: [ref(MULTIMODAL)], effective_fields: [ref(NLP), ref(MULTIMODAL)],
      advisories: [{ code: 'prerequisite_route_added', severity: 'warning', params: { field: 'multimodal', added: ['nlp'] } }],
    }))
    render(<LearnPage />)
    expect(await screen.findByRole('note')).toHaveTextContent('We added NLP & LLMs first')
  })

  it('links to editing the answers', async () => {
    render(<LearnPage />)
    await screen.findByRole('heading', { name: 'AI Engineer' })
    expect(screen.getByRole('link', { name: /Edit my answers/ })).toHaveAttribute('href', '/profile/learning')
  })

  it('does not nest a button inside a link: a navigation is an anchor', async () => {
    render(<LearnPage />)
    await screen.findByRole('heading', { name: 'AI Engineer' })
    for (const link of screen.getAllByRole('link')) expect(link.querySelector('button')).toBeNull()
  })

  it('offers "Edit skills" once, beside the coverage it changes — not as a second copy of "Edit my answers"', async () => {
    render(<LearnPage />)
    await screen.findByRole('heading', { name: 'Your skill gaps' })
    expect(screen.getAllByRole('link', { name: 'Edit skills' })).toHaveLength(1)
  })

  it('rebuilds the path on request and shows the new one', async () => {
    const user = userEvent.setup()
    vi.mocked(api.saveMyLearningPath).mockResolvedValue(path({
      stages: [stage({ slug: 'rag', title: 'RAG Engineering', status: 'current', courses: [] })], current_stage_slug: 'rag',
    }))
    render(<LearnPage />)
    await user.click(await screen.findByRole('button', { name: /Rebuild my Masar/ }))
    await waitFor(() => expect(api.saveMyLearningPath).toHaveBeenCalledWith({ regenerate: true }))
    expect(await screen.findByText('RAG Engineering')).toBeInTheDocument()
    expect(screen.queryByText('NLP & LLM Engineering')).toBeNull()
  })
})

describe('Your Masar — learners who have not answered the new onboarding', () => {
  it('sends a new learner to onboarding and loads no path', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    render(<LearnPage />)
    await waitFor(() => expect(router.replace).toHaveBeenCalledWith('/onboarding/learning-profile'))
    expect(api.getMyLearningPath).not.toHaveBeenCalled()
  })

  it('does the same for an account migrated from the old role-based enrolment', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile({
      level: null, fields: [], onboarding_completed: false, needs_onboarding: true, source: 'migrated',
    }))
    render(<LearnPage />)
    await waitFor(() => expect(router.replace).toHaveBeenCalledWith('/onboarding/learning-profile'))
  })

  it('does not redirect a learner who has finished onboarding', async () => {
    render(<LearnPage />)
    await screen.findByRole('heading', { name: 'AI Engineer' })
    expect(router.replace).not.toHaveBeenCalled()
  })
})

describe('Your Masar — the other states', () => {
  it('offers to build one when the learner has answered but has no path yet', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getMyLearningPath).mockResolvedValue(null)
    vi.mocked(api.saveMyLearningPath).mockResolvedValue(path())
    render(<LearnPage />)
    expect(await screen.findByText('No Masar yet')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: /Build My Roadmap/ }))
    expect(await screen.findByRole('heading', { name: 'AI Engineer' })).toBeInTheDocument()
  })

  it('shows an error with a way to retry, and recovers', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getMyLearningPath).mockRejectedValueOnce(new Error('down'))
    render(<LearnPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load your Masar')
    await user.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByRole('heading', { name: 'AI Engineer' })).toBeInTheDocument()
  })
})

describe('Your Masar — Arabic (RTL)', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' }))

  it('is written in Arabic, keeping the career goal in English with its gloss', async () => {
    render(<LearnPage />)
    const heading = await screen.findByRole('heading', { name: /AI Engineer/ })
    expect(heading).toHaveTextContent('AI Engineer (مهندس ذكاء اصطناعي)')
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('مسارك')
    expect(screen.getByText('مسارك التعليمي')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /أعد بناء مساري/ })).toBeInTheDocument()
  })
})

describe('Your Masar — skill gaps', () => {
  it('shows the skill-gap panel between the summary and the roadmap', async () => {
    render(<LearnPage />)
    expect(await screen.findByRole('heading', { name: 'Your skill gaps' })).toBeInTheDocument()
    expect(screen.getByText('20%')).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: /Show the skills to gain/ }))
    expect(screen.getByRole('region', { name: /NLP & LLMs/ })).toBeInTheDocument()
  })

  it('asks for the gaps again when the roadmap is rebuilt', async () => {
    vi.mocked(api.saveMyLearningPath).mockResolvedValue(path({ id: 2 }))
    render(<LearnPage />)
    await screen.findByRole('heading', { name: 'Your skill gaps' })
    expect(api.getMySkillGaps).toHaveBeenCalledTimes(1)
    await userEvent.click(screen.getByRole('button', { name: /Rebuild/ }))
    await waitFor(() => expect(api.getMySkillGaps).toHaveBeenCalledTimes(2))
  })

  it('does not break the roadmap when the gaps cannot be loaded', async () => {
    vi.mocked(api.getMySkillGaps).mockRejectedValue(new Error('boom'))
    render(<LearnPage />)
    expect(await screen.findByText('Could not load your skill gaps.')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'AI Engineer' })).toBeInTheDocument()
  })

  it('shows no gap panel while the learner has no roadmap', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(null as never)
    render(<LearnPage />)
    await screen.findByText('No Masar yet')
    expect(screen.queryByRole('heading', { name: 'Your skill gaps' })).toBeNull()
  })
})
