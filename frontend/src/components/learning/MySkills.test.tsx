import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { MySkillsSection } from '@/components/learning/MySkills'
import { useLanguageStore } from '@/lib/language'
import { MY_SKILLS, NEEDS_ONBOARDING, SKILL_OPTIONS, gapItem, path, profile, skillGaps } from '@/test/fixtures'

vi.mock('@/lib/api', () => ({
  api: {
    getMySkills: vi.fn(), getMyLearningProfile: vi.fn(), getSkillOptions: vi.fn(), saveMySkills: vi.fn(),
    getMySkillGaps: vi.fn(),
  },
}))
import { api } from '@/lib/api'

beforeEach(() => {
  vi.mocked(api.getMySkills).mockResolvedValue(MY_SKILLS)
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.getSkillOptions).mockResolvedValue(SKILL_OPTIONS)
  vi.mocked(api.getMySkillGaps).mockReset()
  vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps())
  vi.mocked(api.saveMySkills).mockResolvedValue({
    known: [{ skill: MY_SKILLS.known[0].skill, status: 'known', source: 'self_declared' },
      { skill: SKILL_OPTIONS[2], status: 'known', source: 'self_declared' }],
    learning: [], path: path(), roadmap_updated: true,
  })
})

const known = () => screen.getByRole('region', { name: 'Known' }) as HTMLElement
const learning = () => screen.getByRole('region', { name: 'Learning' }) as HTMLElement

describe('My Skills — what is known and what is being learned', () => {
  it('lists what the learner knows and what they are learning', async () => {
    render(<MySkillsSection />)
    await screen.findByRole('heading', { name: 'My Skills' })
    expect(within(await screen.findByRole('region', { name: 'Known' })).getAllByRole('listitem')).toHaveLength(2)
    expect(within(known()).getByText('LLM')).toBeInTheDocument()
    expect(within(known()).getByText('RAG')).toBeInTheDocument()
    expect(within(learning()).getByText('Embeddings')).toBeInTheDocument()
  })

  it('says how a skill became known when it is not simply the learner\'s word', async () => {
    render(<MySkillsSection />)
    await screen.findByRole('region', { name: 'Known' })
    const rag = within(known()).getByText('RAG').closest('li') as HTMLElement
    expect(rag).toHaveTextContent('From a finished course')
    expect(within(known()).getByText('LLM').closest('li')).not.toHaveTextContent('From a finished course')
  })

  it('says so when there is nothing yet', async () => {
    vi.mocked(api.getMySkills).mockResolvedValue({ known: [], learning: [] })
    render(<MySkillsSection />)
    expect(await screen.findByText('You have not added any skills yet.')).toBeInTheDocument()
    expect(screen.getByText('Nothing in progress yet.')).toBeInTheDocument()
  })

  it('shows a loading state, then an error with a retry that recovers', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getMySkills).mockRejectedValueOnce(new Error('down'))
    render(<MySkillsSection />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load your skills.')
    await user.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByRole('region', { name: 'Known' })).toBeInTheDocument()
  })

  it('shows a placeholder while loading', () => {
    vi.mocked(api.getMySkills).mockReturnValue(new Promise(() => {}))
    render(<MySkillsSection />)
    expect(screen.getByRole('status', { name: 'Loading…' })).toBeInTheDocument()
  })

  it('cannot edit before there is a career goal to choose skills for', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    render(<MySkillsSection />)
    expect(await screen.findByRole('button', { name: 'Edit skills' })).toBeDisabled()
    expect(screen.getByText('Finish your learning profile to choose your skills.')).toBeInTheDocument()
  })
})

describe('Edit Skills — reopens the same picker', () => {
  async function edit() {
    const user = userEvent.setup()
    render(<MySkillsSection />)
    await user.click(await screen.findByRole('button', { name: 'Edit skills' }))
    await screen.findByRole('checkbox', { name: /RAG/ })
    return user
  }

  it('asks for the skills of the learner\'s own goal, route and level', async () => {
    await edit()
    expect(api.getSkillOptions).toHaveBeenCalledWith({ career_goal: 'ai-engineer', level: 'intermediate', field: ['nlp'] })
    expect(screen.getByRole('heading', { name: 'Skills & Technologies I Know' })).toBeInTheDocument()
  })

  it('starts from what the learner declared — not from what a finished course taught', async () => {
    await edit()
    expect(screen.getByRole('checkbox', { name: /LLM/ })).toBeChecked()      // self-declared
    expect(screen.getByRole('checkbox', { name: /RAG/ })).not.toBeChecked()  // inferred from a course: not theirs to untick
  })

  it('saves the list, updates what is shown, and says the roadmap was rebuilt and progress kept', async () => {
    const user = await edit()
    await user.click(screen.getByRole('checkbox', { name: /RAG/ }))
    await user.click(screen.getByRole('button', { name: 'Save and update roadmap' }))

    await waitFor(() => expect(api.saveMySkills).toHaveBeenCalledWith(['llms', 'rag']))
    expect(await screen.findByRole('status')).toHaveTextContent('Saved. Your roadmap was updated and your progress is unchanged.')
    expect(screen.getByRole('link', { name: 'View roadmap' })).toHaveAttribute('href', '/learn/masar')
    expect(screen.queryByRole('checkbox')).toBeNull()                           // the picker closed
    expect(within(known()).getByText('RAG')).toBeInTheDocument()
  })

  it('says only "Saved" when there was no roadmap to rebuild', async () => {
    vi.mocked(api.saveMySkills).mockResolvedValue({ known: [], learning: [], path: null, roadmap_updated: false })
    const user = await edit()
    await user.click(screen.getByRole('button', { name: 'Save and update roadmap' }))
    expect(await screen.findByRole('status')).toHaveTextContent(/^Saved\.$/)
  })

  it('reports a failed save, keeps the picker and the selection open', async () => {
    vi.mocked(api.saveMySkills).mockRejectedValue(new Error('boom'))
    const user = await edit()
    await user.click(screen.getByRole('checkbox', { name: /RAG/ }))
    await user.click(screen.getByRole('button', { name: 'Save and update roadmap' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not save your skills. Please try again.')
    expect(screen.getByRole('checkbox', { name: /RAG/ })).toBeChecked()
  })

  it('cancels without saving', async () => {
    const user = await edit()
    await user.click(screen.getByRole('checkbox', { name: /RAG/ }))
    await user.click(screen.getByRole('button', { name: 'Cancel' }))
    expect(api.saveMySkills).not.toHaveBeenCalled()
    expect(screen.queryByRole('checkbox')).toBeNull()
    expect(within(known()).queryAllByRole('listitem')).toHaveLength(2)
  })

  it('can clear everything and save an empty list', async () => {
    const user = await edit()
    await user.click(screen.getByRole('button', { name: 'Clear all' }))
    await user.click(screen.getByRole('button', { name: 'Save and update roadmap' }))
    await waitFor(() => expect(api.saveMySkills).toHaveBeenCalledWith([]))
  })
})

describe('Arabic (RTL)', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' }))

  it('is written in Arabic', async () => {
    render(<MySkillsSection />)
    expect(await screen.findByRole('heading', { name: 'مهاراتي' })).toBeInTheDocument()
    expect(screen.getByRole('region', { name: 'أعرفها' })).toBeInTheDocument()
    expect(screen.getByRole('region', { name: 'أتعلّمها' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'تعديل المهارات' })).toBeInTheDocument()
    expect(within(screen.getByRole('region', { name: 'أعرفها' })).getByText('من دورة أنهيتها')).toBeInTheDocument()
  })
})

describe('My Skills — coverage against the roadmap', () => {
  it('shows how many skills the learner added, the coverage, and what they are working toward', async () => {
    render(<MySkillsSection />)
    expect(await screen.findByText('1 skills added by you')).toBeInTheDocument()   // MY_SKILLS: one self-declared, one from a course
    expect(await screen.findByText('20%')).toBeInTheDocument()
    expect(screen.getByRole('progressbar', { name: 'Skill coverage' })).toHaveAttribute('aria-valuenow', '20')
    expect(screen.getByRole('heading', { name: "Skills you're working toward" })).toBeInTheDocument()
  })

  it('does not turn a finished course into a known skill: it stays under "working toward", with a hint', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      partial: [], missing: [gapItem({ slug: 'evaluation', name: 'Evaluation', name_ar: null }, { covered_by_completed: true })], groups: [],
    }))
    render(<MySkillsSection />)
    const heading = await screen.findByRole('heading', { name: "Skills you're working toward" })
    const section = heading.closest('section') as HTMLElement
    const row = within(section).getByText('Evaluation').closest('li') as HTMLElement
    expect(row).toHaveAttribute('data-status', 'missing')
    expect(row).toHaveTextContent('Covered by a course you finished')
    expect(within(known()).queryByText('Evaluation')).toBeNull()
    expect(screen.getByText(/Finishing a course does not add a skill/)).toBeInTheDocument()
  })

  it('keeps the declared list as the only thing to edit: the gap list has no controls', async () => {
    render(<MySkillsSection />)
    const heading = await screen.findByRole('heading', { name: "Skills you're working toward" })
    const section = heading.closest('section') as HTMLElement
    expect(within(section).queryAllByRole('checkbox')).toHaveLength(0)
    expect(within(section).queryAllByRole('button')).toHaveLength(0)
  })

  it('asks the backend for the gaps again after a save, since the roadmap was rebuilt', async () => {
    const user = userEvent.setup()
    render(<MySkillsSection />)
    await screen.findByText('20%')
    expect(api.getMySkillGaps).toHaveBeenCalledTimes(1)
    await user.click(screen.getByRole('button', { name: 'Edit skills' }))
    await user.click(await screen.findByRole('button', { name: 'Save and update roadmap' }))
    await waitFor(() => expect(api.getMySkillGaps).toHaveBeenCalledTimes(2))
  })

  it('hides the coverage while the learner is editing', async () => {
    const user = userEvent.setup()
    render(<MySkillsSection />)
    await screen.findByText('20%')
    await user.click(screen.getByRole('button', { name: 'Edit skills' }))
    await screen.findByRole('button', { name: 'Save and update roadmap' })
    expect(screen.queryByRole('progressbar', { name: 'Skill coverage' })).toBeNull()
  })

  it('still shows the skills when the gaps cannot be loaded', async () => {
    vi.mocked(api.getMySkillGaps).mockRejectedValue(new Error('boom'))
    render(<MySkillsSection />)
    expect(await screen.findByText('Could not load your skill gaps.')).toBeInTheDocument()
    expect(within(await screen.findByRole('region', { name: 'Known' })).getByText('LLM')).toBeInTheDocument()
  })

  it('says there is no personalised gap yet for a learner without a roadmap', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue({ ...skillGaps(), available: false })
    render(<MySkillsSection />)
    expect(await screen.findByText('No personalized skill gap yet. Build your roadmap first.')).toBeInTheDocument()
  })

  it('reads in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<MySkillsSection />)
    expect(await screen.findByText('أضفت 1 مهارة')).toBeInTheDocument()
    expect(await screen.findByText('تعرف 1 من 5 مهارة')).toBeInTheDocument()
  })
})
