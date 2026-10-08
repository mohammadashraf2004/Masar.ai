import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { VocabularyTermModal } from '@/components/vocabulary/VocabularyTermModal'
import type { VocabularyTermDetail } from '@/types'
import { useLanguageStore } from '@/lib/language'

vi.mock('@/lib/api', () => ({
  api: {
    getVocabularyTerm: vi.fn(),
    recordVocabularyTermProgress: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const DETAIL: VocabularyTermDetail = {
  slug: 'embedding', term_en: 'Embedding', term_ar: 'التمثيل المتجهي', acronym: null, aliases: ['embeddings'],
  category: 'Representation Learning', difficulty: 'beginner', tags: [], definition_en: 'def en', definition_ar: 'def ar',
  explanation_simple_ar: 'شرح', why_it_matters_ar: null, example_ar: null, related_terms: [], courses: [],
  first_introduced: null, progress: { status: 'new' },
}

beforeEach(() => {
  vi.mocked(api.getVocabularyTerm).mockResolvedValue(DETAIL)
})

describe('VocabularyTermModal', () => {
  it('fetches and renders the term detail by slug', async () => {
    render(<VocabularyTermModal slug="embedding" onClose={() => {}} onNavigate={() => {}} />)
    expect(await screen.findByText('Embedding')).toBeInTheDocument()
    expect(api.getVocabularyTerm).toHaveBeenCalledWith('embedding')
    expect(screen.getByText('def en')).toBeInTheDocument()
    expect(screen.queryByText('def ar')).not.toBeInTheDocument()
    expect(screen.queryByText('شرح')).not.toBeInTheDocument()
  })

  it('renders the stored Arabic definition in Arabic mode', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<VocabularyTermModal slug="embedding" onClose={() => {}} onNavigate={() => {}} />)
    expect(await screen.findByText('التمثيل المتجهي')).toBeInTheDocument()
    expect(screen.getByText('def ar')).toBeInTheDocument()
    expect(screen.queryByText('def en')).not.toBeInTheDocument()
  })

  it('shows a failure state when the fetch fails', async () => {
    vi.mocked(api.getVocabularyTerm).mockRejectedValue(new Error('down'))
    render(<VocabularyTermModal slug="embedding" onClose={() => {}} onNavigate={() => {}} />)
    expect(await screen.findByRole('alert')).toBeInTheDocument()
  })

  it('navigates to a related term when clicked', async () => {
    vi.mocked(api.getVocabularyTerm).mockResolvedValue({
      ...DETAIL,
      related_terms: [{ slug: 'vector_search', term_en: 'Vector Search', term_ar: 'البحث المتجهي' }],
    })
    const onNavigate = vi.fn()
    const user = userEvent.setup()
    render(<VocabularyTermModal slug="embedding" onClose={() => {}} onNavigate={onNavigate} />)
    await user.click(await screen.findByText('Vector Search'))
    expect(onNavigate).toHaveBeenCalledWith('vector_search')
  })

  it('shows "no published lesson yet" instead of a fake lesson CTA for a course-only mapping (COURSE-006)', async () => {
    vi.mocked(api.getVocabularyTerm).mockResolvedValue({
      ...DETAIL,
      courses: [
        { course_key: 'COURSE-006', course_title: 'Production AI Engineering', course_href: null, has_lesson_mapping: false },
      ],
    })
    render(<VocabularyTermModal slug="embedding" onClose={() => {}} onNavigate={() => {}} />)
    expect(await screen.findByText('Production AI Engineering')).toBeInTheDocument()
    expect(screen.getByText('No published lesson yet')).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: /Learn this concept/ })).not.toBeInTheDocument()
  })

  it('shows a real "Learn this concept" link when a course has a genuine lesson mapping', async () => {
    vi.mocked(api.getVocabularyTerm).mockResolvedValue({
      ...DETAIL,
      courses: [
        { course_key: 'COURSE-005', course_title: 'Applied LLM Engineering', course_href: '/courses/applied-llm-engineering/learn', has_lesson_mapping: true },
      ],
    })
    render(<VocabularyTermModal slug="embedding" onClose={() => {}} onNavigate={() => {}} />)
    const link = await screen.findByRole('link', { name: /Learn this concept/ })
    expect(link).toHaveAttribute('href', '/courses/applied-llm-engineering/learn')
  })

  it('calls onClose when the close button is clicked', async () => {
    const onClose = vi.fn()
    const user = userEvent.setup()
    render(<VocabularyTermModal slug="embedding" onClose={onClose} onNavigate={() => {}} />)
    await screen.findByText('Embedding')
    await user.click(screen.getByLabelText('Close'))
    expect(onClose).toHaveBeenCalled()
  })

  it('calls onClose when Escape is pressed', async () => {
    const onClose = vi.fn()
    const user = userEvent.setup()
    render(<VocabularyTermModal slug="embedding" onClose={onClose} onNavigate={() => {}} />)
    await screen.findByText('Embedding')
    await user.keyboard('{Escape}')
    expect(onClose).toHaveBeenCalled()
  })

  it('moves focus onto the dialog on open, and back to the trigger on close', async () => {
    const trigger = document.createElement('button')
    trigger.textContent = 'open'
    document.body.appendChild(trigger)
    trigger.focus()
    expect(document.activeElement).toBe(trigger)

    const { unmount } = render(<VocabularyTermModal slug="embedding" onClose={() => {}} onNavigate={() => {}} />)
    await screen.findByText('Embedding')
    expect(document.activeElement).toBe(screen.getByRole('dialog'))

    unmount()
    expect(document.activeElement).toBe(trigger)
    trigger.remove()
  })
})
