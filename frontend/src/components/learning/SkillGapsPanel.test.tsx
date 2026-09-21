import { act, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { SkillGapsPanel } from '@/components/learning/SkillGapsPanel'
import { useLanguageStore } from '@/lib/language'
import { EMBEDDINGS_SKILL, NO_GAPS_YET, RAG_SKILL, gapItem, skillGaps } from '@/test/fixtures'

vi.mock('@/lib/api', () => ({ api: { getMySkillGaps: vi.fn() } }))
import { api } from '@/lib/api'

beforeEach(() => {
  vi.mocked(api.getMySkillGaps).mockReset()
  vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps())
})

/** The per-field list is closed until asked for; open it the way a learner does. */
async function showGaps(name: string = 'Show the skills to gain') {
  await userEvent.click(await screen.findByRole('button', { name: new RegExp(name) }))
}

async function settle() {
  await act(async () => {
    await vi.waitFor(() => expect(api.getMySkillGaps).toHaveBeenCalled())
    await new Promise((resolve) => setTimeout(resolve, 0))
  })
}

describe('SkillGapsPanel — roadmap variant', () => {
  it('shows a placeholder while it loads', () => {
    vi.mocked(api.getMySkillGaps).mockReturnValue(new Promise(() => {}))
    render(<SkillGapsPanel />)
    expect(screen.getByRole('status', { name: 'Loading…' })).toBeInTheDocument()
  })

  it('shows the coverage summary from the server and what is still to gain, grouped by the server\'s groups', async () => {
    render(<SkillGapsPanel />)
    await screen.findByRole('heading', { name: 'Your skill gaps' })
    expect(screen.getByText('20%')).toBeInTheDocument()
    expect(screen.getByText('You know 1 of 5 skills')).toBeInTheDocument()
    await showGaps()
    const nlp = screen.getByRole('region', { name: /NLP & LLMs/ })
    expect(within(nlp).getByText('You know 1 of 3')).toBeInTheDocument()
    expect(within(nlp).getAllByRole('listitem').map((li) => li.getAttribute('data-status'))).toEqual(['partially_covered', 'missing'])
    expect(screen.getByRole('region', { name: /^General/ })).toBeInTheDocument()
    expect(screen.getByRole('region', { name: /^Tools & frameworks/ })).toBeInTheDocument()
  })

  it('does not list skills that are already known as gaps', async () => {
    render(<SkillGapsPanel />)
    await screen.findByRole('heading', { name: 'Your skill gaps' })
    expect(screen.queryByText('Embeddings')).toBeNull()
  })

  it('says why a skill matters, with the server\'s flags only', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      groups: [{
        key: 'field:nlp', kind: 'field', field: skillGaps().fields[0], total: 4, known_count: 0,
        skills: [
          gapItem(RAG_SKILL, { is_immediate: true }),
          gapItem(EMBEDDINGS_SKILL, { is_goal_required: true, course_count: 0 }),
          gapItem({ slug: 'evaluation', name: 'Evaluation', name_ar: null }, { covered_by_completed: true }),
        ],
      }],
    }))
    render(<SkillGapsPanel />)
    await showGaps()
    const rag = (await screen.findByText('RAG')).closest('li') as HTMLElement
    expect(within(rag).getByText('Now')).toBeInTheDocument()
    const emb = screen.getByText('Embeddings').closest('li') as HTMLElement
    expect(within(emb).getByText('Needed for your goal')).toBeInTheDocument()
    expect(within(emb).getByText('No published course yet')).toBeInTheDocument()
    const ev = screen.getByText('Evaluation').closest('li') as HTMLElement
    expect(within(ev).getByText('Covered by a course you finished')).toBeInTheDocument()
    expect(within(rag).queryByText('Needed for your goal')).toBeNull()
  })

  it('tells the learner when there is nothing left to gain', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      summary: { required: 2, known: 2, partial: 0, missing: 0, immediate: 0, coverage_pct: 100 },
      partial: [], missing: [], groups: [],
    }))
    render(<SkillGapsPanel />)
    expect(await screen.findByText('You have added every skill your roadmap covers.')).toBeInTheDocument()
    expect(screen.getByText('100%')).toBeInTheDocument()
  })

  it('explains that finishing a course does not add a skill', async () => {
    render(<SkillGapsPanel />)
    expect(await screen.findByText(/Finishing a course does not add a skill/)).toBeInTheDocument()
  })

  it('is read-only: nothing to tick, and the only button just shows or hides the list', async () => {
    render(<SkillGapsPanel />)
    await screen.findByRole('heading', { name: 'Your skill gaps' })
    await showGaps()
    expect(screen.queryAllByRole('checkbox')).toHaveLength(0)
    expect(screen.getAllByRole('button').map((b) => b.textContent)).toEqual(['Hide the skills to gain(4)'])
  })

  it('keeps the roadmap in view: the list of skills starts closed, and the toggle says so and how many it holds', async () => {
    render(<SkillGapsPanel />)
    await screen.findByRole('heading', { name: 'Your skill gaps' })
    const toggle = screen.getByRole('button', { name: /Show the skills to gain/ })
    expect(toggle).toHaveAttribute('aria-expanded', 'false')
    expect(toggle).toHaveTextContent('(4)')
    expect(screen.queryByRole('region', { name: /NLP & LLMs/ })).toBeNull()
    expect(screen.queryByText('RAG')).toBeNull()
    // the summary stays visible either way
    expect(screen.getByText('You know 1 of 5 skills')).toBeInTheDocument()
    await userEvent.click(toggle)
    expect(screen.getByRole('button', { name: /Hide the skills to gain/ })).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('region', { name: /NLP & LLMs/ })).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: /Hide the skills to gain/ }))
    expect(screen.queryByRole('region', { name: /NLP & LLMs/ })).toBeNull()
  })

  it('links to where the skills are edited', async () => {
    render(<SkillGapsPanel />)
    expect(await screen.findByRole('link', { name: 'Edit skills' })).toHaveAttribute('href', '/profile/learning')
  })

  it('lists every field the learner is on, each with its own progress', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      groups: [
        { key: 'field:nlp', kind: 'field', field: skillGaps().fields[0], total: 3, known_count: 1, skills: [gapItem(RAG_SKILL)] },
        { key: 'field:multimodal', kind: 'field', field: { slug: 'multimodal', name: 'Multimodal AI', name_ar: null, icon: 'layers' }, total: 2, known_count: 0, skills: [gapItem(EMBEDDINGS_SKILL, { group: null })] },
      ],
    }))
    render(<SkillGapsPanel />)
    await showGaps()
    expect(within(screen.getByRole('region', { name: /NLP & LLMs/ })).getByText('You know 1 of 3')).toBeInTheDocument()
    expect(within(screen.getByRole('region', { name: /Multimodal AI/ })).getByText('You know 0 of 2')).toBeInTheDocument()
  })

  it('keeps a very long skill name inside its row, and marks status with a badge only where it is status', async () => {
    const long = 'Retrieval-Augmented Generation Evaluation Frameworks and Observability Pipelines for Production Deployment'
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      groups: [{ key: 'general', kind: 'general', field: null, total: 1, known_count: 0,
        skills: [gapItem({ slug: 'long', name: long, name_ar: null }, { status: 'partially_covered', is_goal_required: true })] }],
    }))
    render(<SkillGapsPanel />)
    await showGaps()
    const row = screen.getByText(long).closest('li') as HTMLElement
    expect(screen.getByText(long).closest('.break-words')).toHaveClass('min-w-0')
    expect(within(row).getByText('In progress')).toHaveClass('border')               // a badge: it is status
    expect(within(row).getByText('Needed for your goal')).not.toHaveClass('border')  // plain text: it is context
  })

  it('flags a skill no published course teaches yet', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      groups: [{ key: 'general', kind: 'general', field: null, total: 1, known_count: 0, skills: [gapItem(EMBEDDINGS_SKILL, { course_count: 0 })] }],
    }))
    render(<SkillGapsPanel />)
    await showGaps()
    expect(within(screen.getByText('Embeddings').closest('li') as HTMLElement).getByText('No published course yet')).toBeInTheDocument()
  })

  it('has no list to open when everything is known — only the summary and the good news', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      summary: { required: 2, known: 2, partial: 0, missing: 0, immediate: 0, coverage_pct: 100 }, partial: [], missing: [], groups: [],
    }))
    render(<SkillGapsPanel />)
    await screen.findByText('You have added every skill your roadmap covers.')
    expect(screen.queryByRole('button', { name: /Show the skills to gain/ })).toBeNull()
  })

  it('has its own empty state for a learner with no roadmap yet', async () => {
    vi.mocked(api.getMySkillGaps).mockResolvedValue(NO_GAPS_YET)
    render(<SkillGapsPanel />)
    expect(await screen.findByText('No personalized skill gap yet. Build your roadmap first.')).toBeInTheDocument()
  })

  it('says when it could not load, and retries on request', async () => {
    vi.mocked(api.getMySkillGaps).mockRejectedValueOnce(new Error('boom'))
    render(<SkillGapsPanel />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load your skill gaps.')
    await userEvent.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByRole('heading', { name: 'Your skill gaps' })).toBeInTheDocument()
    expect(api.getMySkillGaps).toHaveBeenCalledTimes(2)
  })

  it('asks again when the roadmap it belongs to changes', async () => {
    const { rerender } = render(<SkillGapsPanel reloadKey={1} />)
    await screen.findByRole('heading', { name: 'Your skill gaps' })
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({
      summary: { required: 5, known: 3, partial: 0, missing: 2, immediate: 0, coverage_pct: 60 },
    }))
    rerender(<SkillGapsPanel reloadKey={2} />)
    expect(await screen.findByText('60%')).toBeInTheDocument()
    expect(api.getMySkillGaps).toHaveBeenCalledTimes(2)
  })

  it('reads in Arabic with Arabic group and field names and English terms kept', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<SkillGapsPanel />)
    expect(await screen.findByRole('heading', { name: 'فجوات مهاراتك' })).toBeInTheDocument()
    expect(screen.getByText('تعرف 1 من 5 مهارة')).toBeInTheDocument()
    await showGaps('عرض المهارات التي ستكتسبها')
    expect(screen.getByRole('region', { name: /^عام/ })).toBeInTheDocument()
    expect(screen.getByRole('region', { name: /^الأدوات والأطر/ })).toBeInTheDocument()
    expect(screen.getByText('RAG').closest('bdi')).toHaveAttribute('dir', 'ltr')
    await settle()
  })
})

describe('SkillGapsPanel — profile variant', () => {
  it('shows the coverage and the skills the learner is working toward, without the roadmap\'s groups', async () => {
    render(<SkillGapsPanel variant="profile" />)
    expect(await screen.findByText('20%')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: "Skills you're working toward" })).toBeInTheDocument()
    expect(screen.queryByRole('region', { name: /^General/ })).toBeNull()
    const items = within(screen.getByRole('heading', { name: "Skills you're working toward" }).parentElement as HTMLElement).getAllByRole('listitem')
    expect(items.map((li) => li.getAttribute('data-status'))).toEqual(['partially_covered', 'missing', 'missing', 'missing'])
  })

  it('shortens a long list and links to the roadmap for the rest', async () => {
    const many = Array.from({ length: 12 }, (_, i) => gapItem({ slug: `skill-${i}`, name: `Skill ${i}`, name_ar: null }))
    vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps({ partial: [], missing: many, groups: [] }))
    render(<SkillGapsPanel variant="profile" />)
    await screen.findByRole('heading', { name: "Skills you're working toward" })
    expect(screen.getAllByRole('listitem').filter((li) => li.getAttribute('data-status'))).toHaveLength(8)
    expect(screen.getByText(/\+4/)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'See all skill gaps' })).toHaveAttribute('href', '/learn')
  })

  it('has no editable control', async () => {
    render(<SkillGapsPanel variant="profile" />)
    await screen.findByText('20%')
    expect(screen.queryAllByRole('checkbox')).toHaveLength(0)
  })
})
