import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { OnboardingFlow } from '@/components/learning/OnboardingFlow'
import { useLanguageStore } from '@/lib/language'
import { CATALOG, FIELDS, GOALS, LEVELS, SKILL_OPTIONS, path } from '@/test/fixtures'

vi.mock('@/lib/api', () => ({
  api: { saveMyLearningProfile: vi.fn(), saveMyLearningPath: vi.fn(), getSkillOptions: vi.fn() },
}))
import { api } from '@/lib/api'

const onDone = vi.fn()

beforeEach(() => {
  vi.mocked(api.saveMyLearningProfile).mockResolvedValue({} as never)
  vi.mocked(api.saveMyLearningPath).mockResolvedValue(path())
  vi.mocked(api.getSkillOptions).mockResolvedValue(SKILL_OPTIONS)
  onDone.mockReset()
})

function renderFlow(props: Partial<React.ComponentProps<typeof OnboardingFlow>> = {}) {
  return render(<OnboardingFlow catalog={CATALOG} onDone={onDone} {...props} />)
}

const radio = (name: RegExp) => screen.getByRole('radio', { name })
const checkbox = (name: RegExp) => screen.getByRole('checkbox', { name })
const next = () => screen.getByRole('button', { name: /continue|متابعة/i })

async function chooseLevel(user: ReturnType<typeof userEvent.setup>, name: RegExp) {
  await user.click(radio(name))
  await user.click(next())
}

describe('step 1 — where are you now?', () => {
  it('offers the three levels, each with an explanation, from the catalogue', () => {
    renderFlow()
    expect(screen.getByRole('heading', { name: 'Where are you now?' })).toBeInTheDocument()
    expect(screen.getAllByRole('radio')).toHaveLength(LEVELS.length)
    for (const level of LEVELS) {
      expect(radio(new RegExp(level.name))).toHaveAccessibleName(new RegExp(level.description!.slice(0, 20)))
    }
  })

  it('will not continue until a level is chosen, and says why', () => {
    renderFlow()
    expect(next()).toBeDisabled()
    expect(screen.getByText('Choose your level to continue.')).toBeInTheDocument()
  })

  it('selects one level at a time', async () => {
    const user = userEvent.setup()
    renderFlow()
    await user.click(radio(/Beginner/))
    await user.click(radio(/Advanced/))
    expect(radio(/Beginner/)).toHaveAttribute('aria-checked', 'false')
    expect(radio(/Advanced/)).toHaveAttribute('aria-checked', 'true')
    expect(next()).toBeEnabled()
  })

  it('does not preselect a level — none is guessed for anyone', () => {
    renderFlow({ initial: { goal: 'ai-developer' } })
    screen.getAllByRole('radio').forEach((r) => expect(r).toHaveAttribute('aria-checked', 'false'))
    expect(next()).toBeDisabled()
  })
})

describe('step 2 — what are you interested in?', () => {
  async function toFields(level = /Intermediate/) {
    const user = userEvent.setup()
    renderFlow()
    await chooseLevel(user, level)
    return user
  }

  it('lists every field the backend serves — including one the frontend has never heard of', async () => {
    const robotics = { ...FIELDS[0], slug: 'robotics', name: 'Robotics', name_ar: 'الروبوتات', icon: 'cpu', position: 7 }
    const user = userEvent.setup()
    renderFlow({ catalog: { ...CATALOG, fields: [...FIELDS, robotics] } })
    await chooseLevel(user, /Intermediate/)
    expect(screen.getAllByRole('checkbox')).toHaveLength(FIELDS.length + 1)
    expect(checkbox(/Robotics/)).toBeInTheDocument()
  })

  it('allows several fields, not just one', async () => {
    const user = await toFields()
    await user.click(checkbox(/NLP & LLMs/))
    await user.click(checkbox(/Speech & Voice AI/))
    expect(checkbox(/NLP & LLMs/)).toHaveAttribute('aria-checked', 'true')
    expect(checkbox(/Speech & Voice AI/)).toHaveAttribute('aria-checked', 'true')
    await user.click(checkbox(/NLP & LLMs/))
    expect(checkbox(/NLP & LLMs/)).toHaveAttribute('aria-checked', 'false')
  })

  it('needs at least one field to continue', async () => {
    const user = await toFields()
    expect(next()).toBeDisabled()
    expect(screen.getByText('Choose at least one field to continue.')).toBeInTheDocument()
    await user.click(checkbox(/Machine Learning/))
    expect(next()).toBeEnabled()
  })

  it('marks Multimodal as Advanced — and only Multimodal', async () => {
    await toFields()
    expect(within(checkbox(/Multimodal AI/)).getByText('Advanced')).toBeInTheDocument()
    for (const f of FIELDS.filter((f) => f.slug !== 'multimodal')) {
      expect(within(checkbox(new RegExp(f.name.replace(/[&]/g, '\\&')))).queryByText('Advanced')).toBeNull()
    }
  })

  it('tells a beginner that Multimodal is an advanced path — without blocking them', async () => {
    const user = await toFields(/Beginner/)
    await user.click(checkbox(/Multimodal AI/))
    expect(screen.getByRole('note')).toHaveTextContent(/Multimodal AI is an advanced path/)
    expect(screen.getByRole('note')).toHaveTextContent(/instead of blocking you/)
    // ...and names, from the catalogue, the fields that prepare for it.
    expect(screen.getByRole('note')).toHaveTextContent(
      'we recommend building knowledge in: NLP & LLMs / Computer Vision / Speech & Voice AI'
    )
    expect(next()).toBeEnabled()
  })

  it('gives an intermediate learner the same explanation', async () => {
    const intermediate = await toFields(/Intermediate/)
    await intermediate.click(checkbox(/Multimodal AI/))
    expect(screen.getByRole('note')).toBeInTheDocument()
  })

  it('shows no explanation to an advanced learner', async () => {
    const user = await toFields(/Advanced/)
    await user.click(checkbox(/Multimodal AI/))
    expect(screen.queryByRole('note')).toBeNull()
  })

  it('is honest about fields that have no published content yet', async () => {
    await toFields()
    expect(within(checkbox(/Computer Vision/)).getByText('Content coming soon')).toBeInTheDocument()
    expect(within(checkbox(/NLP & LLMs/)).queryByText('Content coming soon')).toBeNull()
  })
})

describe('step 3 — what is your career goal?', () => {
  async function toGoals() {
    const user = userEvent.setup()
    renderFlow()
    await chooseLevel(user, /Intermediate/)
    await user.click(checkbox(/NLP & LLMs/))
    await user.click(next())
    return user
  }

  it('offers the five career goals and explains that goal and field are separate', async () => {
    await toGoals()
    expect(screen.getAllByRole('radio')).toHaveLength(GOALS.length)
    for (const goal of GOALS) expect(radio(new RegExp(goal.title))).toBeInTheDocument()
    expect(screen.getByText(/AI Engineer \+ NLP is a different journey from AI Engineer \+ Computer Vision/)).toBeInTheDocument()
  })

  it('needs a goal to continue', async () => {
    const user = await toGoals()
    expect(next()).toBeDisabled()
    await user.click(radio(/AI Engineer/))
    expect(next()).toBeEnabled()
  })

  it('preselects a career goal carried over from an old enrolment, and nothing else', async () => {
    const user = userEvent.setup()
    renderFlow({ initial: { goal: 'ai-developer' } })
    await chooseLevel(user, /Beginner/)
    await user.click(checkbox(/NLP & LLMs/))
    await user.click(next())
    expect(radio(/AI Developer/)).toHaveAttribute('aria-checked', 'true')
  })
})

describe('step 4 — Before we build your roadmap', () => {
  async function toSkills(user: ReturnType<typeof userEvent.setup>) {
    await chooseLevel(user, /Intermediate/)
    await user.click(checkbox(/NLP & LLMs/))
    await user.click(checkbox(/Speech & Voice AI/))
    await user.click(next())
    await user.click(radio(/AI Engineer/))
    await user.click(next())
    await screen.findByRole('checkbox', { name: /RAG/ }) // the skills have loaded
  }
  const build = () => screen.getByRole('button', { name: /Build My Roadmap/ })

  it('asks what the learner already knows, in the words the product uses', async () => {
    const user = userEvent.setup()
    renderFlow()
    await toSkills(user)
    expect(screen.getByRole('heading', { name: 'Before we build your roadmap' })).toBeInTheDocument()
    expect(screen.getByText(/Tell us what you already know\. We'll use this to skip what you've already learned/)).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Skills & Technologies I Know' })).toBeInTheDocument()
    expect(screen.getByText(/Select everything you're comfortable with/)).toBeInTheDocument()
  })

  it('takes the skills from the API, for this goal, route and level', async () => {
    const user = userEvent.setup()
    renderFlow()
    await toSkills(user)
    expect(api.getSkillOptions).toHaveBeenCalledWith({
      career_goal: 'ai-engineer', level: 'intermediate', field: ['nlp', 'speech'],
    })
    expect(screen.getAllByRole('checkbox')).toHaveLength(SKILL_OPTIONS.length)
  })

  it('lists whatever the API sends — a skill the interface has never heard of included', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getSkillOptions).mockResolvedValue([
      ...SKILL_OPTIONS,
      { slug: 'guardrails', name: 'Guardrails', name_ar: null, kind: 'skill', group: null, is_required: false, course_count: 1 },
    ])
    renderFlow()
    await chooseLevel(user, /Intermediate/)
    await user.click(checkbox(/NLP & LLMs/))
    await user.click(next())
    await user.click(radio(/AI Engineer/))
    await user.click(next())
    expect(await screen.findByRole('checkbox', { name: /Guardrails/ })).toBeInTheDocument()
  })

  it('groups skills by what the catalogue says, and keeps tools apart from skills', async () => {
    const user = userEvent.setup()
    renderFlow()
    await toSkills(user)
    const nlp = screen.getByRole('group', { name: /NLP & LLMs/ })
    expect(within(nlp).getByRole('checkbox', { name: /RAG/ })).toBeInTheDocument()
    expect(within(nlp).queryByRole('checkbox', { name: /LangChain/ })).toBeNull()
    const tools = screen.getByRole('group', { name: 'Tools & frameworks' })
    expect(within(tools).getByRole('checkbox', { name: /LangChain/ })).toBeInTheDocument()
    expect(within(tools).getByRole('checkbox', { name: /FastAPI/ })).toBeInTheDocument()
    expect(within(tools).getByText(/Knowing a tool is not the same as knowing the skill/)).toBeInTheDocument()
  })

  it('marks what the goal requires', async () => {
    const user = userEvent.setup()
    renderFlow()
    await toSkills(user)
    expect(within(screen.getByRole('checkbox', { name: /Evaluation/ }).closest('label') as HTMLElement)
      .getByText('Needed for this goal')).toBeInTheDocument()
  })

  it('offers real, labelled checkboxes the keyboard can operate', async () => {
    const user = userEvent.setup()
    renderFlow()
    await toSkills(user)
    const rag = screen.getByRole('checkbox', { name: /RAG/ }) as HTMLInputElement
    expect(rag.tagName).toBe('INPUT')
    expect(rag).not.toBeChecked()
    rag.focus()
    await user.keyboard(' ')
    expect(rag).toBeChecked()
    await user.keyboard(' ')
    expect(rag).not.toBeChecked()
    // the label is the target: a tap anywhere on the row toggles it
    const llm = screen.getByRole('checkbox', { name: /LLM/ })
    await user.click(llm.closest('label') as HTMLElement)
    expect(llm).toBeChecked()
  })

  it('every skill row is at least 44px tall on a phone', async () => {
    const user = userEvent.setup()
    renderFlow()
    await toSkills(user)
    const label = screen.getByRole('checkbox', { name: /RAG/ }).closest('label') as HTMLElement
    expect(label.className).toContain('min-h-[44px]')
  })

  it('selects all, clears all, and says how many are chosen', async () => {
    const user = userEvent.setup()
    renderFlow()
    await toSkills(user)
    expect(screen.getByText('0 selected')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Select all' }))
    screen.getAllByRole('checkbox').forEach((c) => expect(c).toBeChecked())
    expect(screen.getByText(`${SKILL_OPTIONS.length} selected`)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Clear all' }))
    screen.getAllByRole('checkbox').forEach((c) => expect(c).not.toBeChecked())
    expect(screen.getByRole('button', { name: 'Clear all' })).toBeDisabled()
  })

  it('does not require any skill: someone who knows none goes straight on', async () => {
    const user = userEvent.setup()
    renderFlow()
    await toSkills(user)
    expect(build()).toBeEnabled()
    await user.click(build())
    await waitFor(() => expect(onDone).toHaveBeenCalled())
    expect(api.saveMyLearningProfile).toHaveBeenCalledWith({
      level: 'intermediate', fields: ['nlp', 'speech'], career_goal: 'ai-engineer', known_skills: [],
    })
  })

  it('saves the profile with the skills, then asks the server to build the path, then hands it over', async () => {
    const user = userEvent.setup()
    const built = path({ id: 99 })
    vi.mocked(api.saveMyLearningPath).mockResolvedValue(built)
    renderFlow()
    await toSkills(user)
    await user.click(screen.getByRole('checkbox', { name: /LLM/ }))
    await user.click(screen.getByRole('checkbox', { name: /LangChain/ }))
    await user.click(build())

    await waitFor(() => expect(onDone).toHaveBeenCalledWith(built))
    expect(api.saveMyLearningProfile).toHaveBeenCalledWith({
      level: 'intermediate', fields: ['nlp', 'speech'], career_goal: 'ai-engineer',
      known_skills: ['llms', 'langchain'],
    })
    expect(api.saveMyLearningPath).toHaveBeenCalledWith({ regenerate: true })
    const [profileCall] = vi.mocked(api.saveMyLearningProfile).mock.invocationCallOrder
    const [pathCall] = vi.mocked(api.saveMyLearningPath).mock.invocationCallOrder
    expect(profileCall).toBeLessThan(pathCall)
  })

  it('starts from the skills a learner already declared', async () => {
    const user = userEvent.setup()
    renderFlow({ initial: { skills: ['rag'] } })
    await chooseLevel(user, /Intermediate/)
    await user.click(checkbox(/NLP & LLMs/))
    await user.click(next())
    await user.click(radio(/AI Engineer/))
    await user.click(next())
    expect(await screen.findByRole('checkbox', { name: /RAG/ })).toBeChecked()
  })

  it('never decides anything itself — it sends the answers and shows what comes back', async () => {
    const user = userEvent.setup()
    renderFlow()
    await chooseLevel(user, /Beginner/)
    await user.click(checkbox(/Multimodal AI/))
    await user.click(next())
    await user.click(radio(/AI Engineer/))
    await user.click(next())
    await screen.findByRole('checkbox', { name: /RAG/ })
    await user.click(build())
    await waitFor(() => expect(onDone).toHaveBeenCalled())
    // Multimodal for a beginner is sent as chosen; the route to it is the server's.
    expect(api.saveMyLearningProfile).toHaveBeenCalledWith({
      level: 'beginner', fields: ['multimodal'], career_goal: 'ai-engineer', known_skills: [],
    })
  })

  it('shows a loading state while the skills load', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getSkillOptions).mockReturnValue(new Promise(() => {}))
    renderFlow()
    await chooseLevel(user, /Intermediate/)
    await user.click(checkbox(/NLP & LLMs/))
    await user.click(next())
    await user.click(radio(/AI Engineer/))
    await user.click(next())
    expect(screen.getByRole('status', { name: 'Loading…' })).toBeInTheDocument()
    expect(screen.queryAllByRole('checkbox')).toHaveLength(0)
  })

  it('reports a skills failure and retries — without blocking the build', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getSkillOptions).mockRejectedValueOnce(new Error('down'))
    renderFlow()
    await chooseLevel(user, /Intermediate/)
    await user.click(checkbox(/NLP & LLMs/))
    await user.click(next())
    await user.click(radio(/AI Engineer/))
    await user.click(next())
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load the skills')
    expect(build()).toBeEnabled()
    await user.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByRole('checkbox', { name: /RAG/ })).toBeInTheDocument()
  })

  it('says the skills are the learner\'s own view, not a test result', async () => {
    const user = userEvent.setup()
    renderFlow()
    await toSkills(user)
    expect(screen.getByText(/your own view of what you know/)).toBeInTheDocument()
  })

  it('reports a failed build, keeps the answers, and lets the learner try again', async () => {
    const user = userEvent.setup()
    vi.mocked(api.saveMyLearningPath).mockRejectedValueOnce(new Error('boom'))
    renderFlow()
    await toSkills(user)
    await user.click(screen.getByRole('checkbox', { name: /RAG/ }))
    await user.click(build())

    expect(await screen.findByRole('alert')).toHaveTextContent(/Your answers are saved/)
    expect(onDone).not.toHaveBeenCalled()
    expect(screen.getByRole('checkbox', { name: /RAG/ })).toBeChecked() // the selection survived

    await user.click(build())
    await waitFor(() => expect(onDone).toHaveBeenCalledTimes(1))
  })

  it('goes back without losing answers, skills included', async () => {
    const user = userEvent.setup()
    renderFlow()
    await toSkills(user)
    await user.click(screen.getByRole('checkbox', { name: /RAG/ }))
    await user.click(screen.getByRole('button', { name: /back/i }))
    await user.click(screen.getByRole('button', { name: /back/i }))
    expect(checkbox(/NLP & LLMs/)).toHaveAttribute('aria-checked', 'true')
    await user.click(next())
    await user.click(next())
    expect(await screen.findByRole('checkbox', { name: /RAG/ })).toBeChecked()
  })
})

describe('progress indicator', () => {
  it('says which of the four steps this is', async () => {
    const user = userEvent.setup()
    renderFlow()
    expect(screen.getByText('Step 1 of 4')).toBeInTheDocument()
    await chooseLevel(user, /Beginner/)
    expect(screen.getByText('Step 2 of 4')).toBeInTheDocument()
    expect(screen.getByRole('list', { name: 'Step 2 of 4' }).querySelector('[aria-current="step"]')).not.toBeNull()
  })
})

describe('Arabic (RTL) rendering', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' }))

  it('renders the flow in Arabic, level names included', async () => {
    renderFlow()
    expect(screen.getByRole('heading', { name: 'أين أنت الآن؟' })).toBeInTheDocument()
    expect(screen.getByText('الخطوة 1 من 4')).toBeInTheDocument()
    expect(screen.getByRole('radio', { name: /مبتدئ/ })).toBeInTheDocument()
    expect(screen.getByRole('radio', { name: /متوسط/ })).toBeInTheDocument()
  })

  it('keeps English technical terms left-to-right inside the Arabic page, glossed in Arabic', async () => {
    const user = userEvent.setup()
    renderFlow()
    await user.click(screen.getByRole('radio', { name: /متوسط/ }))
    await user.click(next())
    const nlp = screen.getByRole('checkbox', { name: /NLP & LLMs/ })
    const term = within(nlp).getByText('NLP & LLMs')
    expect(term.closest('bdi')).toHaveAttribute('dir', 'ltr')
    const gloss = within(nlp).getByText('معالجة اللغة الطبيعية والـ LLMs')
    expect(gloss.closest('bdi')).toHaveAttribute('dir', 'rtl')
    expect(nlp).toHaveTextContent('NLP & LLMs (معالجة اللغة الطبيعية والـ LLMs)')
  })

  it('shows an English Technical reader the English names alone', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'english_technical' })
    const user = userEvent.setup()
    renderFlow()
    await user.click(screen.getByRole('radio', { name: /Intermediate/ }))
    await user.click(next())
    const nlp = screen.getByRole('checkbox', { name: /NLP & LLMs/ })
    expect(within(nlp).getByText('NLP & LLMs')).toBeInTheDocument()
    expect(within(nlp).queryByText('معالجة اللغة الطبيعية والـ LLMs')).toBeNull() // no gloss beside the name
  })

  it('explains the advanced path in Arabic', async () => {
    const user = userEvent.setup()
    renderFlow()
    await user.click(screen.getByRole('radio', { name: /مبتدئ/ }))
    await user.click(next())
    await user.click(screen.getByRole('checkbox', { name: /Multimodal AI/ }))
    expect(screen.getByRole('note')).toHaveTextContent('مسار متقدم')
    expect(within(screen.getByRole('checkbox', { name: /Multimodal AI/ })).getByText('متقدم')).toBeInTheDocument()
  })

  it('asks the skills question in Arabic, with English skill names kept left-to-right', async () => {
    const user = userEvent.setup()
    renderFlow()
    await user.click(screen.getByRole('radio', { name: /متوسط/ }))
    await user.click(next())
    await user.click(screen.getByRole('checkbox', { name: /NLP & LLMs/ }))
    await user.click(next())
    await user.click(screen.getByRole('radio', { name: /AI Engineer/ }))
    await user.click(next())
    expect(await screen.findByRole('heading', { name: 'قبل أن نبني مسارك' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'المهارات والتقنيات التي أعرفها' })).toBeInTheDocument()
    expect(screen.getByText('تم اختيار 0')).toBeInTheDocument()
    const rag = screen.getByRole('checkbox', { name: /RAG/ })
    expect(rag.closest('label')?.querySelector('bdi')).toHaveAttribute('dir', 'ltr')
    expect(screen.getByRole('group', { name: 'الأدوات والأطر' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'ابنِ مساري' })).toBeInTheDocument()
  })
})
