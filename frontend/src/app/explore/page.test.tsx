import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import ExplorePage from '@/app/explore/page'
import { useLanguageStore } from '@/lib/language'
import { CATALOG, course } from '@/test/fixtures'

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
  useSession: () => ({ user: null, isAuthenticated: true, isLoading: false }), useNextParam: () => null,
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
    listCatalogCourses: vi.fn(), listTracks: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const RAG = course()
const AGENTS = course({ id: 2, slug: 'ai-agents-orchestration', title: 'AI Agents & Orchestration', title_ar: 'الـ AI Agents والـ Orchestration' })

function deferred<T>() {
  let resolve!: (value: T) => void
  const promise = new Promise<T>((res) => { resolve = res })
  return { promise, resolve }
}

beforeEach(() => {
  vi.mocked(api.getLearningLevels).mockResolvedValue(CATALOG.levels)
  vi.mocked(api.getLearningFields).mockResolvedValue(CATALOG.fields)
  vi.mocked(api.getCareerGoals).mockResolvedValue(CATALOG.goals)
  vi.mocked(api.listCatalogCourses).mockResolvedValue([RAG, AGENTS])
  vi.mocked(api.listTracks).mockResolvedValue([])
})

const lastFilters = () => vi.mocked(api.listCatalogCourses).mock.calls.at(-1)![0]
const chip = (name: RegExp) => screen.getByRole('button', { name })

async function ready() {
  render(<ExplorePage />)
  await screen.findByRole('button', { name: /Beginner/ })
}

describe('Explore — browsing without committing', () => {
  it('shows the three groups of filters, all from the catalogue', async () => {
    await ready()
    expect(screen.getByRole('heading', { name: 'By level' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'By field' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'By career goal' })).toBeInTheDocument()
    for (const name of ['Beginner', 'Intermediate', 'Advanced', 'Data & Analytics', 'Computer Vision', 'Multimodal AI',
      'Data Analyst', 'ML Engineer', 'AI Developer', 'MLOps Engineer', 'AI Engineer']) {
      expect(chip(new RegExp(name.replace('&', '\\&')))).toBeInTheDocument()
    }
  })

  it('starts with every course, unfiltered', async () => {
    await ready()
    await screen.findByRole('link', { name: 'RAG & Knowledge Systems' })
    expect(lastFilters()).toEqual({
      level: [], field: [], career_goal: [], available_only: true, curriculum_only: true,
    })
    expect(screen.getByRole('heading', { name: /Courses \(2\)/ })).toBeInTheDocument()
  })

  it('combines filters: Intermediate + NLP + AI Engineer', async () => {
    const user = userEvent.setup()
    await ready()
    await user.click(chip(/Intermediate/))
    await user.click(chip(/NLP & LLMs/))
    await user.click(chip(/^AI Engineer/))
    await waitFor(() => expect(lastFilters()).toEqual({
      level: ['intermediate'], field: ['nlp'], career_goal: ['ai-engineer'],
      available_only: true, curriculum_only: true,
    }))
  })

  it('lets several values in one group be chosen together', async () => {
    const user = userEvent.setup()
    await ready()
    await user.click(chip(/NLP & LLMs/))
    await user.click(chip(/Speech & Voice AI/))
    await waitFor(() => expect(lastFilters()?.field).toEqual(['nlp', 'speech']))
    await user.click(chip(/NLP & LLMs/))
    await waitFor(() => expect(lastFilters()?.field).toEqual(['speech']))
  })

  it('reports which chips are pressed, for assistive technology', async () => {
    const user = userEvent.setup()
    await ready()
    expect(chip(/Advanced/)).toHaveAttribute('aria-pressed', 'false')
    await user.click(chip(/Advanced/))
    expect(chip(/Advanced/)).toHaveAttribute('aria-pressed', 'true')
  })

  it('shows the matching courses as cards', async () => {
    await ready()
    const rag = await screen.findByRole('link', { name: 'RAG & Knowledge Systems' })
    expect(rag).toHaveAttribute('href', '/courses/rag-knowledge-systems')
    expect(screen.getByRole('link', { name: 'AI Agents & Orchestration' })).toBeInTheDocument()
  })

  it('says so when nothing matches', async () => {
    vi.mocked(api.listCatalogCourses).mockResolvedValue([])
    await ready()
    expect(await screen.findByText('No course matches this combination yet.')).toBeInTheDocument()
  })

  it('never lets a slow earlier answer overwrite a newer one', async () => {
    const user = userEvent.setup()
    const slow = deferred<ReturnType<typeof course>[]>()
    vi.mocked(api.listCatalogCourses)
      .mockReset()
      .mockResolvedValueOnce([RAG, AGENTS])       // initial load
      .mockReturnValueOnce(slow.promise)          // first click — slow
      .mockResolvedValueOnce([AGENTS])            // second click — fast
    await ready()
    await screen.findByRole('link', { name: 'RAG & Knowledge Systems' })
    await user.click(chip(/Beginner/))
    await user.click(chip(/Intermediate/))
    await screen.findByRole('heading', { name: /Courses \(1\)/ })
    slow.resolve([RAG, AGENTS, RAG]) // the stale answer finally lands
    await new Promise((r) => setTimeout(r, 20))
    expect(screen.getByRole('heading', { name: /Courses \(1\)/ })).toBeInTheDocument()
  })

  it('shows an error instead of a blank page when the catalogue cannot load', async () => {
    vi.mocked(api.getLearningFields).mockRejectedValue(new Error('down'))
    render(<ExplorePage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load the catalogue')
  })
})

describe('Explore — View path', () => {
  // The enabled control is a link wrapping a button (the app's usual pattern);
  // the disabled one is a bare button. Ask for each by what it actually is.
  const viewPathLink = () => screen.getByText('View path').closest('a')
  const viewPathButton = () => screen.getByText('View path').closest('button') as HTMLElement

  it('waits until a level, a field and a career goal are chosen', async () => {
    const user = userEvent.setup()
    await ready()
    expect(viewPathLink()).toBeNull()
    expect(viewPathButton()).toBeDisabled()
    expect(screen.getByText('Choose a level, a field and a career goal to preview the path.')).toBeInTheDocument()

    await user.click(chip(/Intermediate/))
    await user.click(chip(/NLP & LLMs/))
    expect(viewPathLink()).toBeNull() // still no career goal
    await user.click(chip(/^AI Engineer/))
    expect(viewPathLink()).not.toBeNull()
    expect(screen.getByText('Your combination')).toBeInTheDocument()
  })

  it('links to the path for exactly that combination', async () => {
    const user = userEvent.setup()
    await ready()
    await user.click(chip(/Intermediate/))
    await user.click(chip(/NLP & LLMs/))
    await user.click(chip(/Speech & Voice AI/))
    await user.click(chip(/^AI Engineer/))
    expect(viewPathLink()).toHaveAttribute('href', '/tracks/ai-engineer')
  })

  it('is not offered for an ambiguous combination such as two levels', async () => {
    const user = userEvent.setup()
    await ready()
    await user.click(chip(/Beginner/))
    await user.click(chip(/Advanced/))
    await user.click(chip(/NLP & LLMs/))
    await user.click(chip(/^AI Engineer/))
    expect(viewPathLink()).toBeNull()
    expect(viewPathButton()).toBeDisabled()
  })

  it('clears every filter at once', async () => {
    const user = userEvent.setup()
    await ready()
    await user.click(chip(/Beginner/))
    await user.click(chip(/Speech & Voice AI/))
    await user.click(screen.getByRole('button', { name: /Clear filters/ }))
    await waitFor(() => expect(lastFilters()).toEqual({
      level: [], field: [], career_goal: [], available_only: true, curriculum_only: true,
    }))
    expect(screen.queryByRole('button', { name: /Clear filters/ })).toBeNull()
  })

  it('offers the ready-made paths too', async () => {
    await ready()
    expect(screen.getByRole('link', { name: /Ready-made paths/ })).toHaveAttribute('href', '/tracks')
  })
})

describe('Explore — Arabic (RTL)', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' }))

  it('renders the filters and headings in Arabic, with technical names glossed', async () => {
    render(<ExplorePage />)
    expect(await screen.findByRole('heading', { name: 'حسب المستوى' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'حسب المجال' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'حسب الهدف المهني' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'مبتدئ' })).toBeInTheDocument()
    const nlp = screen.getByRole('button', { name: /NLP & LLMs/ })
    expect(within(nlp).getByText('NLP & LLMs').closest('bdi')).toHaveAttribute('dir', 'ltr')
  })

  it('says View path in Arabic', async () => {
    render(<ExplorePage />)
    expect(await screen.findByText('عرض المسار')).toBeInTheDocument()
  })
})

describe('Explore — small screens', () => {
  it('gives every filter chip a touch-sized target', async () => {
    await ready()
    const chips = screen.getAllByRole('button', { pressed: false })
    expect(chips.length).toBeGreaterThanOrEqual(14)
    chips.forEach((c) => expect(c.className).toContain('min-h-[44px]'))
  })
})
