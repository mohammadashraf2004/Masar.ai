import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import PathsPage from '@/app/paths/page'
import PathPreviewPage from '@/app/paths/[slug]/page'
import { useLanguageStore } from '@/lib/language'
import {
  ADVANCED, AI_ENGINEER, CATALOG, GOALS, MULTIMODAL, NLP, VISION, path, profile, ref, role, summary,
} from '@/test/fixtures'
import { router, setParams, setSearch } from '@/test/nav'

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
    listLearningPaths: vi.fn(), getLearningPath: vi.fn(), generateLearningPath: vi.fn(),
    getMyLearningProfile: vi.fn(), saveMyLearningProfile: vi.fn(), saveMyLearningPath: vi.fn(),
  },
}))
import { api } from '@/lib/api'

beforeEach(() => {
  vi.mocked(api.getLearningLevels).mockResolvedValue(CATALOG.levels)
  vi.mocked(api.getLearningFields).mockResolvedValue(CATALOG.fields)
  vi.mocked(api.getCareerGoals).mockResolvedValue(CATALOG.goals)
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile({ has_active_path: false }))
  vi.mocked(api.saveMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.saveMyLearningPath).mockResolvedValue(path())
})

describe('Paths — the journeys the configuration defines', () => {
  const cv = summary({ slug: 'ai-engineer-computer-vision', field: ref(VISION), available_course_count: 2, course_count: 2, stage_count: 8 })
  const core = summary({ slug: 'ai-engineer', field: null, stage_count: 5 })
  const mlNlp = summary({ slug: 'ml-engineer-nlp', career_goal: role(GOALS[1]), field: ref(NLP) })

  beforeEach(() => {
    vi.mocked(api.listLearningPaths).mockResolvedValue([core, summary(), cv, mlNlp])
  })

  it('groups routes under their career goal — AI Engineer has several, not one', async () => {
    render(<PathsPage />)
    const aiEngineer = await screen.findByRole('region', { name: 'AI Engineer' })
    expect(aiEngineer.querySelectorAll('a')).toHaveLength(3)
    expect(screen.getByRole('region', { name: 'ML Engineer' }).querySelectorAll('a')).toHaveLength(1)
  })

  it('links each route to its own page', async () => {
    render(<PathsPage />)
    await screen.findByRole('region', { name: 'AI Engineer' })
    const hrefs = screen.getAllByRole('link').map((a) => a.getAttribute('href'))
    expect(hrefs).toEqual(expect.arrayContaining(['/paths/ai-engineer', '/paths/ai-engineer-nlp', '/paths/ai-engineer-computer-vision']))
  })

  it('names the shared core route as such', async () => {
    render(<PathsPage />)
    expect(await screen.findByText('Shared core')).toBeInTheDocument()
  })

  it('shows what a route contains: stages, courses, hours and recommended level', async () => {
    render(<PathsPage />)
    const card = (await screen.findByText('Computer Vision')).closest('a') as HTMLElement
    expect(card).toHaveTextContent('8 stages')
    expect(card).toHaveTextContent('2 courses')
    expect(card).toHaveTextContent('150h')
    expect(card).toHaveTextContent('Recommended level: Intermediate')
  })

  it('shows an error rather than a blank page', async () => {
    vi.mocked(api.listLearningPaths).mockRejectedValue(new Error('down'))
    render(<PathsPage />)
    expect(await screen.findByRole('alert')).toBeInTheDocument()
  })

  it('reads in Arabic with the route\'s field glossed', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    render(<PathsPage />)
    expect(await screen.findByText('المسار الأساسي')).toBeInTheDocument()
    expect(screen.getAllByText(/مهندس ذكاء اصطناعي/).length).toBeGreaterThan(0)
  })
})

describe('Path preview — a predefined route', () => {
  beforeEach(() => {
    setParams({ slug: 'ai-engineer-computer-vision' })
    vi.mocked(api.getLearningPath).mockResolvedValue(path({ progress: null, is_saved: false, status: 'preview', id: null }))
  })

  it('loads the path the slug names, at the goal\'s default level', async () => {
    render(<PathPreviewPage />)
    expect(await screen.findByRole('heading', { name: 'AI Engineer' })).toBeInTheDocument()
    expect(api.getLearningPath).toHaveBeenCalledWith('ai-engineer-computer-vision', undefined)
    expect(api.generateLearningPath).not.toHaveBeenCalled()
  })

  it('lets the learner see the same route at another level', async () => {
    const user = userEvent.setup()
    render(<PathPreviewPage />)
    await screen.findByRole('heading', { name: 'AI Engineer' })
    await user.click(screen.getByRole('radio', { name: /Advanced/ }))
    await waitFor(() => expect(api.getLearningPath).toHaveBeenLastCalledWith('ai-engineer-computer-vision', 'advanced'))
    expect(screen.getByRole('radio', { name: /Intermediate/ })).toBeInTheDocument()
  })

  it('shows a preview with a dash rather than progress it has no basis for', async () => {
    render(<PathPreviewPage />)
    await screen.findByRole('heading', { name: 'AI Engineer' })
    expect(screen.getByText('—')).toBeInTheDocument()
  })

  it('says the path does not exist when the server says 404', async () => {
    vi.mocked(api.getLearningPath).mockRejectedValue({ response: { status: 404 } })
    render(<PathPreviewPage />)
    expect(await screen.findByText('This path does not exist.')).toBeInTheDocument()
  })

  it('shows a generic error for any other failure', async () => {
    vi.mocked(api.getLearningPath).mockRejectedValue({ response: { status: 500 } })
    render(<PathPreviewPage />)
    expect(await screen.findByRole('alert')).toBeInTheDocument()
  })

  it('shows the notes for a route that needed explaining, naming fields the route does not include', async () => {
    vi.mocked(api.getLearningPath).mockResolvedValue(path({
      fields: [ref(MULTIMODAL)], effective_fields: [ref(NLP), ref(MULTIMODAL)],
      advisories: [{ code: 'prerequisites_recommended', severity: 'info', params: { field: 'multimodal', have: 1, recommended: 2, suggested: ['computer-vision'] } }],
    }))
    render(<PathPreviewPage />)
    expect(await screen.findByRole('note')).toHaveTextContent('Computer Vision')
  })
})

describe('Path preview — a custom combination from Explore', () => {
  beforeEach(() => {
    setParams({ slug: 'custom' })
    setSearch('level=intermediate&fields=nlp,speech&goal=ai-engineer')
    vi.mocked(api.generateLearningPath).mockResolvedValue(path())
  })

  it('asks the server to generate exactly that combination', async () => {
    render(<PathPreviewPage />)
    await screen.findByRole('heading', { name: 'AI Engineer' })
    expect(api.generateLearningPath).toHaveBeenCalledWith({
      level: 'intermediate', fields: ['nlp', 'speech'], career_goal: 'ai-engineer',
    })
    expect(api.getLearningPath).not.toHaveBeenCalled()
  })

  it('explains itself when the link is missing its level or goal — and calls nothing', async () => {
    setSearch('fields=nlp')
    render(<PathPreviewPage />)
    expect(await screen.findByText('This path does not exist.')).toBeInTheDocument()
    expect(api.generateLearningPath).not.toHaveBeenCalled()
  })

  it('shows the server\'s route for a beginner who asked for Multimodal, notes and all', async () => {
    setSearch('level=beginner&fields=multimodal&goal=ai-engineer')
    vi.mocked(api.generateLearningPath).mockResolvedValue(path({
      level: { slug: 'beginner', name: 'Beginner', name_ar: 'مبتدئ', rank: 1 },
      fields: [ref(MULTIMODAL)], effective_fields: [ref(NLP), ref(MULTIMODAL)],
      advisories: [
        { code: 'field_above_level', severity: 'info', params: { field: 'multimodal', level: 'beginner', min_level: 'advanced' } },
        { code: 'prerequisite_route_added', severity: 'warning', params: { field: 'multimodal', added: ['nlp'] } },
      ],
    }))
    render(<PathPreviewPage />)
    const notes = await screen.findAllByRole('note')
    expect(notes[0]).toHaveTextContent('Multimodal AI is an advanced field')
    expect(notes[1]).toHaveTextContent('We added NLP & LLMs first')
  })
})

describe('Path preview — making it the learner\'s Masar', () => {
  beforeEach(() => {
    setParams({ slug: 'custom' })
    setSearch('level=advanced&fields=multimodal&goal=ai-engineer')
    // The server routes Multimodal through NLP: effective fields differ from the request.
    vi.mocked(api.generateLearningPath).mockResolvedValue(path({
      level: ADVANCED, fields: [ref(MULTIMODAL)], effective_fields: [ref(NLP), ref(MULTIMODAL)], career_goal: AI_ENGINEER,
    }))
  })

  it('saves the answers the learner gave — not the routes the server added — then builds and opens the path', async () => {
    const user = userEvent.setup()
    render(<PathPreviewPage />)
    await user.click(await screen.findByRole('button', { name: 'Make this my Masar' }))
    await waitFor(() => expect(router.push).toHaveBeenCalledWith('/learn/masar'))
    expect(api.saveMyLearningProfile).toHaveBeenCalledWith({
      level: 'advanced', fields: ['multimodal'], career_goal: 'ai-engineer',
    })
    expect(api.saveMyLearningPath).toHaveBeenCalledWith({ regenerate: true })
  })

  it('warns that it replaces an existing Masar', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile({ has_active_path: true }))
    render(<PathPreviewPage />)
    expect(await screen.findByText(/replaces your current Masar/)).toBeInTheDocument()
  })

  it('does not warn a learner who has none', async () => {
    render(<PathPreviewPage />)
    await screen.findByRole('button', { name: 'Make this my Masar' })
    expect(screen.queryByText(/replaces your current Masar/)).toBeNull()
  })

  it('reports a failed save and stays put', async () => {
    const user = userEvent.setup()
    vi.mocked(api.saveMyLearningPath).mockRejectedValue(new Error('boom'))
    render(<PathPreviewPage />)
    await user.click(await screen.findByRole('button', { name: 'Make this my Masar' }))
    expect(await screen.findByRole('alert')).toBeInTheDocument()
    expect(router.push).not.toHaveBeenCalled()
  })
})
