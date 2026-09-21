import { act, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { YourMasarCard } from '@/components/learning/YourMasarCard'
import { useLanguageStore } from '@/lib/language'
import { MULTIMODAL, NEEDS_ONBOARDING, NLP, path, profile, ref, step } from '@/test/fixtures'
import { router } from '@/test/nav'

vi.mock('@/lib/api', () => ({ api: { getMyLearningProfile: vi.fn(), getMyLearningPath: vi.fn() } }))
import { api } from '@/lib/api'

beforeEach(() => {
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.getMyLearningPath).mockResolvedValue(path())
})

// Let the component's requests finish and its state settle — inside act, so the
// resulting updates are applied before anything is asserted. Waiting only for
// the request is not enough: "the card is empty" is also true while it loads.
async function settle() {
  await act(async () => {
    await vi.waitFor(() => expect(api.getMyLearningProfile).toHaveBeenCalled())
    await new Promise((resolve) => setTimeout(resolve, 0))
  })
}

describe('the roadmap card — dashboard variant', () => {
  it('shows the goal, the route, the progress, what is current and what is next', async () => {
    render(<YourMasarCard />)
    expect(await screen.findByRole('heading', { name: 'AI Engineer' })).toBeInTheDocument()
    expect(screen.getByText('NLP & LLMs')).toBeInTheDocument()
    expect(screen.getByText('Your Roadmap')).toBeInTheDocument()
    expect(screen.getByText('72%')).toBeInTheDocument()
    expect(screen.getByRole('progressbar', { name: 'Roadmap progress' })).toHaveAttribute('aria-valuenow', '72')
    expect(screen.getByText('Current:').nextElementSibling).toHaveTextContent('LangChain')
    expect(screen.getByText('Next:').nextElementSibling).toHaveTextContent('RAG & Knowledge Systems')
  })

  it('leads with the next action: Continue Learning opens the current course\'s lessons', async () => {
    render(<YourMasarCard />)
    expect(await screen.findByRole('link', { name: /Continue Learning/ })).toHaveAttribute('href', '/tools/langchain')
    expect(screen.getByRole('link', { name: 'View Full Roadmap' })).toHaveAttribute('href', '/learn')
  })

  it('does not dump the curriculum: no stage or course list on the card', async () => {
    render(<YourMasarCard />)
    await screen.findByRole('heading', { name: /AI Engineer/ })
    expect(screen.queryByRole('list')).toBeNull()
    expect(screen.queryByText('NLP & LLM Engineering')).toBeNull()
    expect(screen.queryByText('Prompt Engineering')).toBeNull()
  })

  it('reports the percentage the server sent, rounded — it computes nothing', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(
      path({ progress: { path_pct: 33.4, overall_pct: 5, by_role: {}, by_field: {}, by_skill: {} } })
    )
    render(<YourMasarCard />)
    expect(await screen.findByText('33%')).toBeInTheDocument()
  })

  it('shows every field in the route, including ones the backend added', async () => {
    render(<YourMasarCard />)
    await screen.findByRole('heading', { name: 'AI Engineer' })
    expect(screen.getByText('NLP & LLMs')).toBeInTheDocument()
  })

  it('names the route under the goal, not inside its heading, so a long name never wraps into the title', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(path({ effective_fields: [ref(NLP), ref(MULTIMODAL)] }))
    render(<YourMasarCard />)
    const heading = await screen.findByRole('heading', { name: 'AI Engineer' })
    expect(within(heading).queryByText('NLP & LLMs')).toBeNull()
    const route = screen.getByText('NLP & LLMs').closest('p') as HTMLElement
    expect(route).toHaveTextContent('NLP & LLMs·Multimodal AI')
  })

  it('offers links, not buttons: a navigation is an anchor, with nothing interactive nested inside it', async () => {
    render(<YourMasarCard />)
    const link = await screen.findByRole('link', { name: /Continue Learning/ })
    expect(link.querySelector('button')).toBeNull()
    expect(screen.queryAllByRole('button')).toHaveLength(0)
  })

  it('leaves out "Next" when nothing follows the current course', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(path({ next_course: null }))
    render(<YourMasarCard />)
    await screen.findByRole('heading', { name: /AI Engineer/ })
    expect(screen.queryByText('Next:')).toBeNull()
  })

  it('says the roadmap is finished when the server does — and offers no Continue', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(path({ current_course: null, next_course: null, is_complete: true }))
    render(<YourMasarCard />)
    await screen.findByRole('heading', { name: /AI Engineer/ })
    expect(screen.getByRole('status')).toHaveTextContent('You have finished every required course on your roadmap.')
    expect(screen.queryByRole('link', { name: /Continue Learning/ })).toBeNull()
    expect(screen.getByRole('link', { name: 'View Full Roadmap' })).toBeInTheDocument()
  })

  it('does not claim a finish just because nothing is current', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(path({ current_course: null, next_course: null, is_complete: false }))
    render(<YourMasarCard />)
    await screen.findByRole('heading', { name: /AI Engineer/ })
    expect(screen.queryByRole('status')).toBeNull()
  })

  it('a course with no lesson page falls back to its catalogue page', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(
      path({ current_course: step({ course: { id: 5, slug: 'llm-integration', href: null } }) })
    )
    render(<YourMasarCard />)
    expect(await screen.findByRole('link', { name: /Continue Learning/ })).toHaveAttribute('href', '/courses/llm-integration')
  })
})

describe('the roadmap card — home variant', () => {
  it('is compact: "Your Masar", what you are learning now, what is next, one button', async () => {
    render(<YourMasarCard variant="home" />)
    expect(await screen.findByText('Your Masar')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'AI Engineer' })).toBeInTheDocument()
    expect(screen.getByText('NLP & LLMs')).toBeInTheDocument()
    expect(screen.getByText('72%')).toBeInTheDocument()
    expect(screen.getByText("You're currently learning:").nextElementSibling).toHaveTextContent('LangChain')
    expect(screen.getByText('Next:').nextElementSibling).toHaveTextContent('RAG & Knowledge Systems')
    expect(screen.getByRole('link', { name: /Continue Roadmap/ })).toHaveAttribute('href', '/learn')
    expect(screen.queryByRole('link', { name: /Continue Learning/ })).toBeNull()
  })
})

describe('the roadmap card — no roadmap yet', () => {
  it('invites a learner who has not answered the onboarding — with a link, not a redirect', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    render(<YourMasarCard variant="home" />)
    expect(await screen.findByText('Build your personalized roadmap')).toBeInTheDocument()
    expect(screen.getByText('Tell us your goal and what you already know.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Build My Roadmap/ })).toHaveAttribute('href', '/onboarding/learning-profile')
    expect(router.replace).not.toHaveBeenCalled()
    expect(router.push).not.toHaveBeenCalled()
    expect(api.getMyLearningPath).not.toHaveBeenCalled()
  })

  it('says the same on the dashboard', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    render(<YourMasarCard />)
    expect(await screen.findByText('Build your personalized roadmap')).toBeInTheDocument()
  })

  it('sends a learner who answered but has no path to Your Masar, where it can be built', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(null)
    render(<YourMasarCard />)
    expect(await screen.findByRole('link', { name: /Build My Roadmap/ })).toHaveAttribute('href', '/learn')
  })

  it('is told which career goal was kept from their old enrolment', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile({
      level: null, fields: [], onboarding_completed: false, needs_onboarding: true, source: 'migrated',
      career_goal: { slug: 'ai-developer', title: 'AI Developer', title_ar: 'مطوّر تطبيقات ذكاء اصطناعي', icon: 'code' },
    }))
    render(<YourMasarCard />)
    expect(await screen.findByText('We kept your earlier career goal: AI Developer.')).toBeInTheDocument()
  })

  it('is not told about a kept goal when there was none', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    render(<YourMasarCard />)
    await screen.findByText('Build your personalized roadmap')
    expect(screen.queryByText(/kept your earlier career goal/)).toBeNull()
  })
})

describe('the roadmap card — loading and errors', () => {
  it('shows a placeholder while it loads, not an empty gap', async () => {
    vi.mocked(api.getMyLearningProfile).mockReturnValue(new Promise(() => {}))
    render(<YourMasarCard />)
    expect(screen.getByRole('status', { name: 'Loading…' })).toBeInTheDocument()
    expect(screen.queryByRole('link')).toBeNull()
  })

  it('says so when the roadmap cannot be loaded — and retries', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getMyLearningProfile).mockRejectedValueOnce(new Error('down'))
    render(<YourMasarCard />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load your roadmap.')
    await user.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByRole('heading', { name: /AI Engineer/ })).toBeInTheDocument()
  })

  it('reports a path request that fails the same way', async () => {
    vi.mocked(api.getMyLearningPath).mockRejectedValue(new Error('down'))
    render(<YourMasarCard />)
    await settle()
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load your roadmap.')
  })
})

describe('Arabic (RTL)', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' }))

  it('prompts in Arabic', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    render(<YourMasarCard />)
    expect(await screen.findByText('ابنِ مسارك المخصص')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /ابنِ مساري/ })).toHaveAttribute('href', '/onboarding/learning-profile')
  })

  it('summarises the roadmap in Arabic, keeping the goal in English with its gloss', async () => {
    render(<YourMasarCard />)
    const heading = await screen.findByRole('heading', { name: /AI Engineer/ })
    expect(heading).toHaveTextContent('AI Engineer (مهندس ذكاء اصطناعي)')
    expect(screen.getByText('مسارك')).toBeInTheDocument()
    expect(screen.getByText('الحالية:')).toBeInTheDocument()
    expect(screen.getByText('التالية:')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /واصل التعلّم/ })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'عرض المسار كاملاً' })).toBeInTheDocument()
  })

  it('keeps the percentage left-to-right inside the right-to-left card', async () => {
    render(<YourMasarCard />)
    expect(await screen.findByText('72%')).toHaveAttribute('dir', 'ltr')
  })

  it('names the current course in Arabic where the catalogue has an Arabic title', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(
      path({ current_course: step({ course: { id: 9, slug: 'prompt-engineering', title: 'Prompt Engineering', title_ar: 'هندسة الـ Prompts' } }) })
    )
    render(<YourMasarCard />)
    expect(await screen.findByText('هندسة الـ Prompts')).toBeInTheDocument()
  })
})
