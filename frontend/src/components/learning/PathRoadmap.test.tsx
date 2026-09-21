import { cleanup, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it } from 'vitest'
import { AdvisoryList, MasarSummary, PathRoadmap } from '@/components/learning/PathRoadmap'
import { useLanguageStore } from '@/lib/language'
import {
  ADVANCED, AI_ENGINEER, FIELDS, LLMS_SKILL, MULTIMODAL, NLP, RAG_SKILL, VISION, path, pathCourse, ref, stage, step,
} from '@/test/fixtures'

describe('MasarSummary — the top of "Your Masar"', () => {
  it('shows the career goal, the fields, the level and the progress', () => {
    render(<MasarSummary path={path()} />)
    expect(screen.getByRole('heading', { name: 'AI Engineer' })).toBeInTheDocument()
    expect(screen.getByText('NLP & LLMs')).toBeInTheDocument()
    expect(screen.getByText('Intermediate')).toBeInTheDocument()
    expect(screen.getByText('72%')).toBeInTheDocument()
    expect(screen.getByText('14h left')).toBeInTheDocument()
    expect(screen.getByText('≈ 3 weeks')).toBeInTheDocument()
    expect(screen.getByText(/Overall/)).toHaveTextContent('64%')
  })

  it('reports the percentage the server sent — it does not compute its own', () => {
    render(<MasarSummary path={path({ progress: { path_pct: 12.6, overall_pct: 5, by_role: {}, by_field: {}, by_skill: {} } })} />)
    expect(screen.getByText('13%')).toBeInTheDocument()
  })

  it('shows a dash, not 0%, for a preview that has no progress', () => {
    render(<MasarSummary path={path({ progress: null })} />)
    expect(screen.getByText('—')).toBeInTheDocument()
    expect(screen.queryByText('0%')).toBeNull()
  })

  it('shows every field in the route, including ones the backend added', () => {
    render(<MasarSummary path={path({ fields: [ref(MULTIMODAL)], effective_fields: [ref(NLP), ref(MULTIMODAL)] })} />)
    expect(screen.getByText('NLP & LLMs')).toBeInTheDocument()
    expect(screen.getByText('Multimodal AI')).toBeInTheDocument()
  })

  it('names the current and the next course, and how far the counts are — all from the server', () => {
    render(<MasarSummary path={path()} />)
    expect(screen.getByText('Current')).toBeInTheDocument()
    expect(screen.getByText('LangChain')).toBeInTheDocument()
    expect(screen.getByText('Next')).toBeInTheDocument()
    expect(screen.getByText('RAG & Knowledge Systems')).toBeInTheDocument()
    expect(screen.getByText('7 of 10 done')).toBeInTheDocument()
    expect(screen.getByText('2 already known')).toBeInTheDocument()
  })

  it('continues to the current course\'s lessons', () => {
    render(<MasarSummary path={path()} />)
    expect(screen.getByRole('link', { name: /Continue Learning/ })).toHaveAttribute('href', '/tools/langchain')
  })

  it('offers no Continue when nothing is left to do', () => {
    render(<MasarSummary path={path({ current_course: null, next_course: null, is_complete: true })} />)
    expect(screen.queryByRole('link', { name: /Continue Learning/ })).toBeNull()
  })

  it('omits the counts for a preview that has no progress', () => {
    render(<MasarSummary path={path({ progress: null, current_course: null, next_course: null })} />)
    expect(screen.queryByText(/already known/)).toBeNull()
    expect(screen.queryByText(/ done$/)).toBeNull()
  })

  it('renders the actions it is given', () => {
    render(<MasarSummary path={path()} actions={<button>Rebuild</button>} />)
    expect(screen.getByRole('button', { name: 'Rebuild' })).toBeInTheDocument()
  })
})

describe('PathRoadmap — the stages', () => {
  it('lists the stages in the order the server sent them', () => {
    render(<PathRoadmap path={path()} />)
    const titles = ['AI Foundations', 'Machine Learning', 'NLP & LLM Engineering', 'RAG Engineering', 'AI Engineer Capstone']
    const nodes = titles.map((title) => screen.getByText(title))
    nodes.slice(1).forEach((node, i) => {
      expect(nodes[i].compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
    })
  })

  it('carries each stage\'s status from the server', () => {
    render(<PathRoadmap path={path()} />)
    const statuses = Array.from(document.querySelectorAll('li[data-status]')).map((li) => li.getAttribute('data-status'))
    expect(statuses).toEqual(['completed', 'coming_soon', 'current', 'upcoming', 'coming_soon'])
  })

  it('makes the current stage prominent — flagged, labelled and already open', () => {
    render(<PathRoadmap path={path()} />)
    const current = document.querySelector<HTMLElement>('li[aria-current="step"]')!
    expect(current).toHaveAttribute('data-status', 'current')
    expect(within(current).getByText('Current stage')).toBeInTheDocument()
    expect(within(current).getByRole('link', { name: 'Prompt Engineering' })).toBeInTheDocument()
    expect(within(current).getByRole('link', { name: 'LangChain' })).toBeInTheDocument()
    // Exactly one stage is "current".
    expect(document.querySelectorAll('li[aria-current="step"]')).toHaveLength(1)
  })

  it('keeps the other stages collapsed until asked, and collapses them again', async () => {
    const user = userEvent.setup()
    render(<PathRoadmap path={path()} />)
    const rag = document.querySelector<HTMLElement>('li[data-status="upcoming"]')!
    expect(within(rag).queryByRole('link')).toBeNull()

    await user.click(within(rag).getByRole('button'))
    expect(within(rag).getAllByRole('link').length).toBeGreaterThan(0)
    expect(within(rag).getByRole('button')).toHaveAttribute('aria-expanded', 'true')

    await user.click(within(rag).getByRole('button'))
    expect(within(rag).queryByRole('link')).toBeNull()
  })

  it('says "coming soon" for a stage with nothing published, and does not pretend it can be opened', () => {
    render(<PathRoadmap path={path()} />)
    const ml = document.querySelectorAll<HTMLElement>('li[data-status="coming_soon"]')[0]
    expect(within(ml).getByRole('button')).toBeDisabled()
    expect(ml).toHaveTextContent('Coming soon')
    expect(ml).toHaveTextContent('3 more planned')
  })

  it('separates the facts under a stage title — "3 more planned" never runs into "Coming soon"', () => {
    render(<PathRoadmap path={path()} />)
    const ml = document.querySelectorAll<HTMLElement>('li[data-status="coming_soon"]')[0]
    expect(ml).toHaveTextContent('3 more planned · Coming soon')
    // ...and in Arabic, where the same run-together was seen in the browser.
    cleanup()
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    render(<PathRoadmap path={path()} />)
    expect(document.querySelectorAll<HTMLElement>('li[data-status="coming_soon"]')[0]).toHaveTextContent('3 قادمة · قريباً')
  })

  it('shows a stage that is optional at the learner\'s level as such — not as 0%', () => {
    const skippable = stage({
      slug: 'foundations', title: 'AI Foundations', status: 'skippable', progress_pct: null,
      courses: [pathCourse({ state: 'optional', reason: 'below_level' })],
    })
    render(<PathRoadmap path={path({ stages: [skippable], current_stage_slug: null })} />)
    const item = document.querySelector<HTMLElement>('li[data-status="skippable"]')!
    expect(item).toHaveTextContent('Optional for your level')
    expect(item).not.toHaveTextContent('%')
  })

  it('shows completed stages with a completed marker', () => {
    render(<PathRoadmap path={path()} />)
    expect(document.querySelector('li[data-status="completed"]')).toHaveTextContent('Completed')
  })

  it('counts courses with correct singular and plural', () => {
    render(<PathRoadmap path={path()} />)
    expect(document.querySelector('li[data-status="completed"]')).toHaveTextContent('1 course')
    expect(document.querySelector('li[data-status="current"]')).toHaveTextContent('3 courses')
  })

  it('shows a stage\'s own progress from the server', () => {
    render(<PathRoadmap path={path()} />)
    expect(document.querySelector('li[data-status="current"]')).toHaveTextContent('50%')
  })

  it('congratulates a learner who has finished every required stage', () => {
    const done = path({
      stages: [stage({ status: 'completed', progress_pct: 100, courses: [pathCourse({ state: 'completed' })] })],
      current_stage_slug: null, is_complete: true,
    })
    render(<PathRoadmap path={done} />)
    expect(screen.getByRole('status')).toHaveTextContent('You have finished every required stage.')
  })

  it('does not claim completion for a path where nothing is required yet', () => {
    const idle = path({ stages: [stage({ status: 'coming_soon', courses: [] })], current_stage_slug: null })
    render(<PathRoadmap path={idle} />)
    expect(screen.queryByRole('status')).toBeNull()
  })
})

describe('PathRoadmap — the courses inside a stage', () => {
  it('marks each course completed, current, upcoming or optional, and says why a course is optional', () => {
    render(<PathRoadmap path={path()} />)
    const current = document.querySelector<HTMLElement>('li[aria-current="step"]')!
    const row = (name: string) => within(current).getByRole('link', { name }).closest('li') as HTMLElement
    expect(row('Prompt Engineering')).toHaveTextContent('Completed')
    expect(row('Prompt Engineering')).toHaveAttribute('data-state', 'completed')
    // LangChain is the course the server named as the current one.
    expect(row('LangChain')).toHaveTextContent('Current')
    expect(row('LangChain')).toHaveAttribute('data-state', 'current')
    expect(row('LLM Integration')).toHaveTextContent('Optional')
    expect(row('LLM Integration')).toHaveTextContent('Below your level')
  })

  describe('the four states a learner sees: completed, already know, current, upcoming', () => {
    const known = pathCourse({
      course: { id: 30, slug: 'llm-integration', title: 'LLM Integration' }, state: 'waived', reason: 'known_skills',
      known_skills: [LLMS_SKILL],
    })
    const upcoming = pathCourse({ course: { id: 31, slug: 'rag-knowledge-systems', title: 'RAG & Knowledge Systems' }, state: 'required' })
    const currentCourse = pathCourse({ course: { id: 32, slug: 'prompt-engineering', title: 'Prompt Engineering' }, state: 'required' })
    const done = pathCourse({ course: { id: 33, slug: 'foundations', title: 'AI Foundations' }, state: 'completed', completion_pct: 100 })
    const roadmap = () => path({
      stages: [stage({ status: 'current', courses: [done, known, currentCourse, upcoming] })],
      current_course: step({ course: { id: 32, slug: 'prompt-engineering', title: 'Prompt Engineering' } }),
    })
    const row = (name: string) => screen.getByRole('link', { name }).closest('li') as HTMLElement

    it('labels each in the learner\'s words', () => {
      render(<PathRoadmap path={roadmap()} />)
      expect(row('AI Foundations')).toHaveTextContent('Completed')
      expect(row('LLM Integration')).toHaveTextContent('Already know')
      expect(row('Prompt Engineering')).toHaveTextContent('Current')
      expect(row('RAG & Knowledge Systems')).toHaveTextContent('Upcoming')
      expect(row('AI Foundations')).toHaveAttribute('data-state', 'completed')
      expect(row('LLM Integration')).toHaveAttribute('data-state', 'known')
      expect(row('Prompt Engineering')).toHaveAttribute('data-state', 'current')
      expect(row('RAG & Knowledge Systems')).toHaveAttribute('data-state', 'upcoming')
    })

    it('never uses the technical word "waived" or calls a known course skipped', () => {
      render(<PathRoadmap path={roadmap()} />)
      expect(document.body).not.toHaveTextContent(/waived/i)
      expect(row('LLM Integration')).not.toHaveTextContent(/skipped|missed|failed/i)
    })

    it('says why a course is known, from what the learner declared', () => {
      render(<PathRoadmap path={roadmap()} />)
      expect(row('LLM Integration')).toHaveTextContent('You told us you know: LLM')
    })

    it('does not fade a known course like an optional one', () => {
      render(<PathRoadmap path={roadmap()} />)
      expect(row('LLM Integration').className).not.toContain('opacity')
    })

    it('tells apart the four states without colour: each has its own text', () => {
      render(<PathRoadmap path={roadmap()} />)
      const labels = ['AI Foundations', 'LLM Integration', 'Prompt Engineering', 'RAG & Knowledge Systems']
        .map((name) => within(row(name)).getByText(/^(Completed|Already know|Current|Upcoming)$/).textContent)
      expect(new Set(labels).size).toBe(4)
    })

    it('shows a partly known required course with what is already known', () => {
      const partial = pathCourse({ state: 'required', known_skills: [RAG_SKILL] })
      render(<PathRoadmap path={path({ stages: [stage({ status: 'current', courses: [partial] })], current_course: null })} />)
      expect(screen.getByText('You already know 1 of 5 skills here: RAG')).toBeInTheDocument()
    })

    it('explains a known course even when the server sent no skill list', () => {
      const bare = pathCourse({ state: 'waived', reason: null, known_skills: [] })
      render(<PathRoadmap path={path({ stages: [stage({ status: 'current', courses: [bare] })], current_course: null })} />)
      expect(screen.getByText('You told us you know this')).toBeInTheDocument()
    })

    it('says on the stage header how many known courses it holds, even while collapsed', () => {
      render(<PathRoadmap path={path({
        stages: [stage({ status: 'upcoming', courses: [known, upcoming] }), stage({ slug: 'rag', status: 'upcoming', courses: [upcoming] })],
        current_course: null,
      })} />)
      const items = screen.getAllByRole('listitem').filter((li) => li.hasAttribute('data-status'))
      expect(within(items[0]).getByRole('button', { expanded: false })).toHaveTextContent('1 already known')
      expect(within(items[1]).getByRole('button')).not.toHaveTextContent(/already known/)
    })

    it('marks only the course the server called current', () => {
      render(<PathRoadmap path={roadmap()} />)
      expect(document.querySelectorAll('[data-state="current"]')).toHaveLength(1)
    })
  })

  it('shows a partly finished course\'s percentage', () => {
    const partial = path({
      stages: [stage({ status: 'current', courses: [pathCourse({ state: 'required', completion_pct: 40 })] })],
      current_stage_slug: 'nlp-llm',
    })
    render(<PathRoadmap path={partial} />)
    expect(screen.getByText('40%', { selector: 'span.font-mono' })).toBeInTheDocument()
  })

  it('links every course to its catalogue page', () => {
    render(<PathRoadmap path={path()} />)
    const current = document.querySelector<HTMLElement>('li[aria-current="step"]')!
    expect(within(current).getByRole('link', { name: 'LangChain' })).toHaveAttribute('href', '/courses/langchain')
  })

  it('shows a prerequisite the server pulled in, labelled as one', () => {
    const withPrereq = path({
      stages: [stage({ status: 'current', courses: [pathCourse({ reason: 'prerequisite' })] })],
      current_stage_slug: 'nlp-llm',
    })
    render(<PathRoadmap path={withPrereq} />)
    expect(screen.getByText(/Prerequisite/)).toBeInTheDocument()
  })

  it('ignores an unknown reason code rather than printing a raw key', () => {
    const odd = path({
      stages: [stage({ status: 'current', courses: [pathCourse({ reason: 'invented_by_a_future_server' })] })],
      current_stage_slug: 'nlp-llm',
    })
    render(<PathRoadmap path={odd} />)
    expect(document.body).not.toHaveTextContent('invented_by_a_future_server')
    expect(document.body).not.toHaveTextContent('courseReason')
  })
})

describe('AdvisoryList — notes about the route', () => {
  it('shows the notes a beginner asking for Multimodal is given', () => {
    const p = path({
      level: { slug: 'beginner', name: 'Beginner', name_ar: 'مبتدئ', rank: 1 },
      fields: [ref(MULTIMODAL)], effective_fields: [ref(NLP), ref(MULTIMODAL)],
      advisories: [
        { code: 'field_above_level', severity: 'info', params: { field: 'multimodal', level: 'beginner', min_level: 'advanced' } },
        { code: 'prerequisite_route_added', severity: 'warning', params: { field: 'multimodal', added: ['nlp'] } },
        { code: 'prerequisites_recommended', severity: 'info', params: { field: 'multimodal', have: 1, recommended: 2, suggested: ['computer-vision', 'speech'] } },
      ],
    })
    render(<AdvisoryList path={p} catalogFields={FIELDS.map(ref)} />)
    const notes = screen.getAllByRole('note')
    expect(notes).toHaveLength(3)
    expect(notes[0]).toHaveTextContent('Multimodal AI is an advanced field')
    expect(notes[1]).toHaveTextContent('We added NLP & LLMs first')
    expect(notes[2]).toHaveTextContent('Computer Vision / Speech & Voice AI')
  })

  it('names a suggested field that is not in the route only when the catalogue is known', () => {
    const p = path({
      advisories: [{ code: 'prerequisites_recommended', severity: 'info', params: { field: 'multimodal', have: 1, recommended: 2, suggested: ['computer-vision'] } }],
    })
    const { rerender } = render(<AdvisoryList path={p} catalogFields={[ref(VISION), ref(MULTIMODAL)]} />)
    expect(screen.getByRole('note')).toHaveTextContent('Computer Vision')
    rerender(<AdvisoryList path={p} />)
    expect(screen.getByRole('note')).toHaveTextContent('computer-vision') // falls back to the slug
  })

  it('renders nothing for admin-only advisories', () => {
    const { container } = render(
      <AdvisoryList path={path({ advisories: [
        { code: 'prerequisite_cycle', severity: 'warning', params: { course_ids: [1, 2, 1] } },
        { code: 'no_template_fallback', severity: 'info', params: {} },
      ] })} />
    )
    expect(container).toBeEmptyDOMElement()
  })

  it('explains a route with no published content', () => {
    render(<AdvisoryList path={path({ advisories: [{ code: 'no_available_courses', severity: 'info', params: {} }] })} />)
    expect(screen.getByRole('note')).toHaveTextContent('still being written')
  })
})

describe('Arabic (RTL) rendering', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' }))

  it('reads stage titles in Arabic, falling back to English where there is no twin', () => {
    render(<PathRoadmap path={path()} />)
    expect(screen.getByText('أسس الذكاء الاصطناعي')).toBeInTheDocument()
    expect(screen.getByText('هندسة NLP والـ LLMs')).toBeInTheDocument()
    // LangChain has no Arabic title: it stays LangChain rather than going blank.
    expect(screen.getByRole('link', { name: 'LangChain' })).toBeInTheDocument()
  })

  it('counts courses with the Arabic plural forms', () => {
    render(<PathRoadmap path={path()} />)
    expect(document.querySelector('li[data-status="completed"]')).toHaveTextContent('دورة واحدة')
    expect(document.querySelector('li[data-status="current"]')).toHaveTextContent('3 دورات')
  })

  it('labels the current stage and course states in Arabic', () => {
    render(<PathRoadmap path={path()} />)
    const current = document.querySelector<HTMLElement>('li[aria-current="step"]')!
    expect(current).toHaveTextContent('المرحلة الحالية')
    expect(current).toHaveTextContent('الحالية') // the current course
    expect(current).toHaveTextContent('اختيارية')
    expect(current).toHaveTextContent('أقل من مستواك')
  })

  it('keeps numbers left-to-right inside the right-to-left page', () => {
    render(<MasarSummary path={path()} />)
    expect(screen.getByText('72%')).toHaveAttribute('dir', 'ltr')
  })

  it('summarises the Masar with the goal glossed and the level in Arabic', () => {
    render(<MasarSummary path={path({ level: ADVANCED })} />)
    expect(screen.getByRole('heading')).toHaveTextContent('AI Engineer (مهندس ذكاء اصطناعي)')
    expect(screen.getByText('متقدم')).toBeInTheDocument()
    expect(screen.getByText('مسارك')).toBeInTheDocument()
    expect(screen.getByText('المتبقي 14 ساعة')).toBeInTheDocument()
  })
})
