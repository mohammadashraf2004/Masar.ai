import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { WhyThisCourse } from '@/components/learning/WhyThisCourse'
import { useLanguageStore } from '@/lib/language'
import { EMBEDDINGS_SKILL, LANGCHAIN_SKILL, MULTIMODAL, NLP, RAG_SKILL, ref, why } from '@/test/fixtures'

async function open() {
  await userEvent.click(screen.getByRole('button', { name: /Why this course\?/ }))
  return screen.getByRole('region', { name: 'Why this course?' })
}

describe('WhyThisCourse', () => {
  it('starts collapsed, and the toggle says so', () => {
    render(<WhyThisCourse why={why()} />)
    const toggle = screen.getByRole('button', { name: /Why this course\?/ })
    expect(toggle).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByRole('region')).toBeNull()
  })

  it('opens to the goal, the field, the stage and the reasons — each a sentence built from a code', async () => {
    render(<WhyThisCourse why={why()} />)
    const panel = await open()
    expect(screen.getByRole('button', { name: /Why this course\?/ })).toHaveAttribute('aria-expanded', 'true')
    expect(within(panel).getByText('Career goal').nextElementSibling).toHaveTextContent('AI Engineer')
    expect(within(panel).getByText('Field').nextElementSibling).toHaveTextContent('NLP & LLMs')
    expect(within(panel).getByText('It covers 1 of the skills your career goal requires.')).toBeInTheDocument()
    expect(within(panel).getByText('It belongs to a field on your route.')).toBeInTheDocument()
    expect(within(panel).getByText('It is a step in the “RAG Engineering” stage of your path.')).toBeInTheDocument()
    expect(within(panel).getByText('You still need 3 of the 4 skills it teaches.')).toBeInTheDocument()
  })

  it('shows what is already known and what will be gained', async () => {
    render(<WhyThisCourse why={why()} />)
    const panel = await open()
    expect(within(panel).getByText('You already know 1 of 4 skills here')).toBeInTheDocument()
    const known = within(panel).getByText('You already know').parentElement as HTMLElement
    expect(within(known).getByText('Embeddings')).toBeInTheDocument()
    const gain = within(panel).getByText("Skills you'll gain").parentElement as HTMLElement
    expect(within(gain).getAllByRole('listitem').map((li) => li.textContent)).toEqual(['RAG', 'Vector Databases', 'Evaluation'])
  })

  it('celebrates full coverage instead of listing skills to gain', async () => {
    render(<WhyThisCourse why={why({
      reasons: ['stage_requirement'], known_skills: [RAG_SKILL, EMBEDDINGS_SKILL], skills_to_gain: [],
      skills_taught: [RAG_SKILL, EMBEDDINGS_SKILL], taught_count: 2, known_count: 2, to_gain_count: 0,
    })} />)
    const panel = await open()
    expect(within(panel).getByText('You already know every skill this course teaches.')).toBeInTheDocument()
    expect(within(panel).queryByText("Skills you'll gain")).toBeNull()
    expect(within(panel).queryByText(/You still need/)).toBeNull()
  })

  it('has nothing to say about skills for a course that teaches none, and does not pretend', async () => {
    render(<WhyThisCourse why={why({
      reasons: ['stage_requirement'], skills_taught: [], known_skills: [], skills_to_gain: [], goal_skills: [],
      taught_count: 0, known_count: 0, to_gain_count: 0,
    })} />)
    const panel = await open()
    expect(within(panel).queryByText(/You already know/)).toBeNull()
    expect(within(panel).queryByText("Skills you'll gain")).toBeNull()
  })

  it('names only the reasons the server sent — and each one at most once', async () => {
    render(<WhyThisCourse why={why({ reasons: ['prerequisite'] })} />)
    const panel = await open()
    expect(within(panel).getAllByRole('listitem').filter((li) => li.closest('ul')?.className.includes('list-disc'))).toHaveLength(1)
    expect(within(panel).getByText('Other courses on your roadmap build on it, so it comes first.')).toBeInTheDocument()
    expect(within(panel).queryByText(/career goal requires/)).toBeNull()
  })

  it('shows every field of the route it belongs to', async () => {
    render(<WhyThisCourse why={why({ fields: [ref(MULTIMODAL)] })} />)
    const panel = await open()
    expect(within(panel).getByText('Career goal').nextElementSibling).toHaveTextContent('AI Engineer')
    expect(within(panel).getByText('Field').nextElementSibling).toHaveTextContent('Multimodal AI')
  })

  it('uses the server\'s counts as given rather than counting the lists itself', async () => {
    render(<WhyThisCourse why={why({ to_gain_count: 9, taught_count: 11 })} />)
    expect(within(await open()).getByText('You still need 9 of the 11 skills it teaches.')).toBeInTheDocument()
  })

  it('keeps a tool a tool: it is listed as a skill to gain like any other the course teaches', async () => {
    render(<WhyThisCourse why={why({ skills_to_gain: [RAG_SKILL, LANGCHAIN_SKILL], to_gain_count: 2, taught_count: 3 })} />)
    expect(within(await open()).getByText('LangChain')).toBeInTheDocument()
  })

  it('names the later courses that need this one first — the backend\'s list, as links', async () => {
    render(<WhyThisCourse why={why({
      reasons: ['prerequisite'],
      prerequisite_for: [
        { id: 7, slug: 'advanced-rag', title: 'Advanced RAG', title_ar: 'RAG المتقدم' },
        { id: 8, slug: 'ai-agents', title: 'AI Agents', title_ar: null },
      ],
    })} />)
    const panel = await open()
    const list = within(panel).getByText('Courses that build on it').nextElementSibling as HTMLElement
    expect(within(list).getAllByRole('link').map((a) => [a.textContent, a.getAttribute('href')])).toEqual([
      ['Advanced RAG', '/courses/advanced-rag'], ['AI Agents', '/courses/ai-agents'],
    ])
  })

  it('draws only what the server sent: no list of dependants, no field row, no reasons, no skills when they are empty', async () => {
    render(<WhyThisCourse why={why({
      fields: [], reasons: [], prerequisite_for: [], known_skills: [], skills_to_gain: [], goal_skills: [],
      skills_taught: [], taught_count: 0, known_count: 0, to_gain_count: 0,
    })} />)
    const panel = await open()
    expect(within(panel).getByText('Career goal')).toBeInTheDocument()   // the goal is always sent
    expect(within(panel).queryByText('Field')).toBeNull()
    expect(within(panel).queryByText('Courses that build on it')).toBeNull()
    expect(within(panel).queryByText('You already know')).toBeNull()
    expect(within(panel).queryByText("Skills you'll gain")).toBeNull()
    expect(within(panel).queryAllByRole('listitem')).toHaveLength(0)
  })

  it('says "Fields" when the route holds more than one', async () => {
    render(<WhyThisCourse why={why({ fields: [ref(NLP), ref(MULTIMODAL)] })} />)
    const panel = await open()
    expect(within(panel).queryByText('Field')).toBeNull()
    expect(within(panel).getByText('Fields').nextElementSibling).toHaveTextContent('NLP & LLMs · Multimodal AI')
  })

  it('lists skills as the same chips a course card uses, the known ones tinted apart from those still to gain', async () => {
    render(<WhyThisCourse why={why()} />)
    const panel = await open()
    const known = within(panel).getByText('Embeddings').closest('li') as HTMLElement
    const gain = within(panel).getByText('RAG').closest('li') as HTMLElement
    expect(known).toHaveClass('rounded', 'border', 'text-sky')
    expect(gain).toHaveClass('rounded', 'border', 'text-soft')
  })

  it('reads left-to-right in English: Latin terms are isolated as LTR, nothing is forced RTL', async () => {
    render(<WhyThisCourse why={why()} defaultOpen />)
    const panel = screen.getByRole('region', { name: 'Why this course?' })
    expect(within(panel).getByText('RAG').closest('bdi')).toHaveAttribute('dir', 'ltr')
    expect(panel.querySelector('[dir="rtl"]')).toBeNull()
  })

  it('has a toggle a keyboard can drive: a real button that names the region it controls', async () => {
    render(<WhyThisCourse why={why()} />)
    const toggle = screen.getByRole('button', { name: /Why this course\?/ })
    toggle.focus()
    await userEvent.keyboard('{Enter}')
    expect(toggle).toHaveAttribute('aria-expanded', 'true')
    expect(document.getElementById(toggle.getAttribute('aria-controls') as string)).toBe(screen.getByRole('region'))
    await userEvent.keyboard(' ')
    expect(toggle).toHaveAttribute('aria-expanded', 'false')
  })

  it('can open expanded', () => {
    render(<WhyThisCourse why={why()} defaultOpen />)
    expect(screen.getByRole('region', { name: 'Why this course?' })).toBeInTheDocument()
  })

  it('reads in Arabic: the sentences translate, the technical terms stay recognisable', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<WhyThisCourse why={why()} defaultOpen />)
    const panel = screen.getByRole('region', { name: 'لماذا هذه الدورة؟' })
    expect(within(panel).getByText('الهدف المهني').nextElementSibling).toHaveTextContent('AI Engineer (مهندس ذكاء اصطناعي)')
    expect(within(panel).getByText('المجال').nextElementSibling).toHaveTextContent('NLP & LLMs')
    expect(within(panel).getByText('تغطي 1 من المهارات التي يتطلبها هدفك المهني.')).toBeInTheDocument()
    expect(within(panel).getByText('ما زلت تحتاج 3 من أصل 4 مهارات تدرّسها.')).toBeInTheDocument()
    expect(within(panel).getByText('تعرف 1 من 4 مهارات هنا')).toBeInTheDocument()
    expect(within(panel).getByText('RAG')).toBeInTheDocument()                     // terms stay English...
    expect(within(panel).getByText('RAG').closest('bdi')).toHaveAttribute('dir', 'ltr')   // ...and isolated from the RTL sentence
    expect(within(panel).getByText(/هندسة الـ RAG/)).toBeInTheDocument()            // the Arabic stage title
  })

  it('reads in Arabic with the labels and the dependants in Arabic too', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<WhyThisCourse why={why({
      fields: [ref(NLP), ref(MULTIMODAL)],
      prerequisite_for: [{ id: 7, slug: 'advanced-rag', title: 'Advanced RAG', title_ar: 'RAG المتقدم' }],
    })} defaultOpen />)
    const panel = screen.getByRole('region', { name: 'لماذا هذه الدورة؟' })
    expect(within(panel).getByText('المجالات')).toBeInTheDocument()
    expect(within(panel).getByText('دورات تبني عليها')).toBeInTheDocument()
    expect(within(panel).getByRole('link', { name: /RAG المتقدم/ })).toHaveAttribute('href', '/courses/advanced-rag')
  })
})
