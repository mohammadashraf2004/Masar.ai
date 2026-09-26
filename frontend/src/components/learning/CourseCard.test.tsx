import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it } from 'vitest'
import { CourseCard } from '@/components/learning/CourseCard'
import { useLanguageStore } from '@/lib/language'
import { ADVANCED, AI_ENGINEER, GOALS, MULTIMODAL, NLP, SYSTEM_SKILL, course, ref, role } from '@/test/fixtures'
import type { CatalogCourseDetail } from '@/types'

describe('CourseCard — why is this course relevant?', () => {
  it('shows the level, the fields, the skills and who it is relevant for', () => {
    render(<CourseCard course={course()} />)
    expect(screen.getByRole('link', { name: 'RAG & Knowledge Systems' })).toHaveAttribute('href', '/courses/rag-knowledge-systems')
    expect(screen.getByText('Intermediate')).toBeInTheDocument()
    expect(screen.getByText('NLP & LLMs')).toBeInTheDocument()
    const skills = within(screen.getByText('Skills').parentElement as HTMLElement)
    expect(skills.getByText('RAG')).toBeInTheDocument()
    expect(skills.getByText('Embeddings')).toBeInTheDocument()
    expect(screen.getByText(/Relevant for/).closest('p')).toHaveTextContent('Relevant for: AI Developer, AI Engineer')
  })

  it('does not overload the card: at most four skills, with a count for the rest', () => {
    render(<CourseCard course={course()} />) // five skills
    const skills = screen.getByText('Skills').parentElement as HTMLElement
    expect(within(skills).getAllByRole('listitem')).toHaveLength(5) // four chips + "+1"
    expect(within(skills).getByText('+1')).toBeInTheDocument()
  })

  it('keeps the description, hours and link behind a Details toggle', async () => {
    const user = userEvent.setup()
    render(<CourseCard course={course()} />)
    const toggle = screen.getByRole('button', { name: /Details/ })
    expect(toggle).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByText('Build retrieval-augmented applications.')).toBeNull()

    await user.click(toggle)
    expect(toggle).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByText('Build retrieval-augmented applications.')).toBeInTheDocument()
    expect(screen.getByText('40.5h')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Open course' })).toHaveAttribute('href', '/tracks/ai-developer')

    await user.click(toggle)
    expect(screen.queryByText('Build retrieval-augmented applications.')).toBeNull()
  })

  it('can open already expanded, as the course page does', () => {
    render(<CourseCard course={course()} defaultOpen />)
    expect(screen.getByText('Build retrieval-augmented applications.')).toBeInTheDocument()
  })

  it('shows what to know first when it has the detail', async () => {
    const detail: CatalogCourseDetail = {
      ...course(),
      assumes: [SYSTEM_SKILL],
      prerequisites: [{ id: 5, slug: 'llm-integration', title: 'LLM Integration', title_ar: null }],
      learning_objectives: ['Explain what problem RAG solves'], learning_objectives_ar: [],
    }
    render(<CourseCard course={detail} defaultOpen />)
    expect(screen.getByRole('link', { name: 'LLM Integration' })).toHaveAttribute('href', '/courses/llm-integration')
    expect(screen.getByText('Explain what problem RAG solves')).toBeInTheDocument()
    expect(screen.getByText(/Assumes you know/).closest('p')).toHaveTextContent('System Design')
  })

  it('marks a course whose lessons are not published as coming soon and offers no link in', async () => {
    const user = userEvent.setup()
    render(<CourseCard course={course({ slug: 'pinecone', title: 'Pinecone', is_available: false, href: '/tools/pinecone' })} />)
    expect(screen.getByText('Coming soon')).toBeInTheDocument()
    expect(screen.queryByText('Intermediate')).toBeNull() // the level badge gives way to it
    await user.click(screen.getByRole('button', { name: /Details/ }))
    expect(screen.queryByRole('link', { name: 'Open course' })).toBeNull()
  })

  it('tolerates a sparse course — no fields, skills or roles', () => {
    render(<CourseCard course={course({ fields: [], skills: [], roles: [], description: null, description_ar: null })} />)
    expect(screen.queryByText('Skills')).toBeNull()
    expect(screen.queryByText(/Relevant for/)).toBeNull()
  })

  it('uses a distinct badge colour per level', () => {
    const { rerender } = render(<CourseCard course={course()} />)
    const intermediate = (screen.getByText('Intermediate').closest('span[class*="border"]') as HTMLElement).className
    rerender(<CourseCard course={course({ level: ADVANCED })} />)
    const advanced = (screen.getByText('Advanced').closest('span[class*="border"]') as HTMLElement).className
    expect(intermediate).not.toBe(advanced)
  })

  it('has a touch-sized Details control for phones', () => {
    render(<CourseCard course={course()} />)
    expect(screen.getByRole('button', { name: /Details/ }).className).toContain('min-h-[44px]')
  })

  it('is one card for a course in several fields and serving several goals', () => {
    render(<CourseCard course={course({ fields: [ref(NLP), ref(MULTIMODAL)], roles: GOALS.map(role) })} />)
    expect(screen.getAllByRole('link', { name: 'RAG & Knowledge Systems' })).toHaveLength(1)
    expect(screen.getByText('NLP & LLMs')).toBeInTheDocument()
    expect(screen.getByText('Multimodal AI')).toBeInTheDocument()
    expect(screen.getByText(/Relevant for/).closest('p')).toHaveTextContent('Data Analyst, ML Engineer, AI Developer, MLOps Engineer, AI Engineer')
  })
})

describe('Arabic (RTL) rendering', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' }))

  it('reads the title, level and description in Arabic', async () => {
    const user = userEvent.setup()
    render(<CourseCard course={course()} />)
    expect(screen.getByRole('link', { name: 'أنظمة RAG والمعرفة' })).toBeInTheDocument()
    expect(screen.getByText('متوسط')).toBeInTheDocument()
    expect(screen.getByText('المهارات')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: /التفاصيل/ }))
    expect(screen.getByText('ابنِ تطبيقات تعتمد على الاسترجاع.')).toBeInTheDocument()
    expect(screen.getByText('40.5 ساعة')).toBeInTheDocument()
  })

  it('shows skills through the terminology dictionary — RAG with its Arabic gloss, in an LTR run', () => {
    render(<CourseCard course={course()} />)
    const rag = screen.getByText('RAG')
    expect(rag.closest('bdi')).toHaveAttribute('dir', 'ltr')
    expect(rag.closest('li')).toHaveTextContent(/RAG \(.+\)/)
  })

  it('falls back to English where the course has no Arabic twin, instead of going blank', () => {
    render(<CourseCard course={course({ title_ar: null, description_ar: null })} defaultOpen />)
    expect(screen.getByRole('link', { name: 'RAG & Knowledge Systems' })).toBeInTheDocument()
    expect(screen.getByText('Build retrieval-augmented applications.')).toBeInTheDocument()
  })

  it('names the career goals with their Arabic gloss', () => {
    render(<CourseCard course={course({ roles: [AI_ENGINEER] })} />)
    expect(screen.getByText(/مناسبة لـ/).closest('p')).toHaveTextContent('AI Engineer (مهندس ذكاء اصطناعي)')
  })
})

describe('CourseCard — enrollment and readiness on the card', () => {
  it('shows the size of the course on the card itself, without opening the details', () => {
    render(<CourseCard course={course({ module_count: 12 })} />)
    expect(screen.getByText('12 modules')).toBeInTheDocument()
    expect(screen.getByText('40.5h')).toBeInTheDocument()
  })

  it('offers "View course" to a learner who is not enrolled, and shows their readiness', () => {
    render(<CourseCard course={course({ readiness: { state: 'mostly_ready', score: 78 } })} />)
    expect(screen.getByRole('link', { name: 'View course' })).toHaveAttribute('href', '/courses/rag-knowledge-systems')
    expect(screen.getByText('Mostly ready')).toBeInTheDocument()
    expect(screen.queryByText(/complete/)).toBeNull()
  })

  it('shows progress and "Continue" for an enrolled learner, in place of readiness', () => {
    render(<CourseCard course={course({
      enrollment: { status: 'in_progress', progress_percentage: 42 }, readiness: { state: 'ready', score: 90 },
    })} />)
    expect(screen.getByText('42% complete')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continue' })).toHaveAttribute('href', '/courses/rag-knowledge-systems')
    expect(screen.queryByText('Ready')).toBeNull()
  })

  it('offers a review of a completed course', () => {
    render(<CourseCard course={course({ enrollment: { status: 'completed', progress_percentage: 100 } })} />)
    expect(screen.getByText('Completed')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Review course' })).toBeInTheDocument()
  })

  it('says nothing about readiness while it has not been assessed', () => {
    render(<CourseCard course={course({ readiness: { state: 'not_assessed', score: 0 } })} />)
    expect(screen.queryByText('Not assessed yet')).toBeNull()
  })
})
