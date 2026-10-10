import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import GlossaryPage from '@/app/glossary/page'
import { useAuthStore } from '@/lib/store'
import { useAuthPrompt } from '@/components/auth/AuthPrompt'
import type { MyCourse, VocabularyListResponse, VocabularyTermDetail, VocabularyTermSummary } from '@/types'

let mockIsAuthenticated = true
vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: mockIsAuthenticated, isLoading: false }),
  useGuest: () => {},
  useSession: () => ({ user: null, isAuthenticated: mockIsAuthenticated, isLoading: false }), useNextParam: () => null,
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
    listVocabularyTerms: vi.fn(),
    getVocabularyCategories: vi.fn(),
    getVocabularyCourseCounts: vi.fn(),
    getVocabularyTerm: vi.fn(),
    recordVocabularyTermProgress: vi.fn(),
    getMyCourses: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const RAG: VocabularyTermSummary = {
  slug: 'retrieval_augmented_generation', term_en: 'Retrieval-Augmented Generation', term_ar: 'التوليد المعزز بالاسترجاع',
  acronym: 'RAG', explanation_simple_ar: 'شرح مبسط', category: 'RAG', difficulty: 'intermediate', course_count: 3,
  definition_en: 'English RAG definition', definition_ar: 'تعريف RAG بالعربية',
  progress: { status: 'new' },
}
const EMBEDDING: VocabularyTermSummary = {
  slug: 'embedding', term_en: 'Embedding', term_ar: 'التمثيل المتجهي',
  acronym: null, explanation_simple_ar: 'تمثيل رقمي', category: 'Representation Learning', difficulty: 'beginner', course_count: 5,
  definition_en: 'English embedding definition', definition_ar: 'تعريف التمثيل بالعربية',
  progress: { status: 'mastered' },
}

const LIST_RESPONSE: VocabularyListResponse = { items: [RAG, EMBEDDING], total: 2, page: 1, page_size: 24 }

const DETAIL: VocabularyTermDetail = {
  slug: 'retrieval_augmented_generation', term_en: 'Retrieval-Augmented Generation', term_ar: 'التوليد المعزز بالاسترجاع',
  acronym: 'RAG', aliases: ['RAG'], category: 'RAG', difficulty: 'intermediate', tags: [],
  definition_en: 'def en', definition_ar: 'def ar', explanation_simple_ar: 'شرح مبسط', why_it_matters_ar: 'مهم لأن...',
  example_ar: 'مثال', related_terms: [{ slug: 'embedding', term_en: 'Embedding', term_ar: 'التمثيل المتجهي' }],
  courses: [{ course_key: 'COURSE-005', course_title: 'Applied LLM Engineering', course_href: '/courses/applied-llm-engineering/learn', has_lesson_mapping: true }],
  first_introduced: { course_key: 'COURSE-005', lesson_key: 'L005-001', lesson_title: 'Intro', href: '/courses/applied-llm-engineering/learn' },
  progress: { status: 'new' },
}

const MY_COURSE: MyCourse = {
  course_id: 1, slug: 'applied-llm-engineering', title: 'Applied LLM Engineering', href: '/courses/applied-llm-engineering/learn',
  progress: 40, enrolled_at: '2026-01-01T00:00:00Z', access_type: 'purchase', status: 'in_progress',
}

const EMPTY_RESPONSE: VocabularyListResponse = { items: [], total: 0, page: 1, page_size: 6 }

beforeEach(() => {
  mockIsAuthenticated = true
  useAuthStore.setState({ token: 'tok', _hasHydrated: true })
  useAuthPrompt.setState({ open: false, next: null })
  // The "All Terms" list uses page_size 24 (or omits it); "From Your Masar"
  // and "Continue Learning" both request page_size 6. Keeping those two
  // kinds of calls distinct here (instead of always returning the same two
  // terms everywhere) is what keeps `getByText('Retrieval-Augmented
  // Generation')` unambiguous in the tests below — on the real page these
  // are three separate, independently-loaded sections that may well repeat
  // a term, which is correct, not a bug.
  vi.mocked(api.listVocabularyTerms).mockImplementation(async (params) => {
    if (params?.page_size === 6) return EMPTY_RESPONSE
    return LIST_RESPONSE
  })
  vi.mocked(api.getVocabularyCategories).mockResolvedValue({
    categories: ['RAG', 'Representation Learning'],
    counts: [{ category: 'RAG', term_count: 2 }, { category: 'Representation Learning', term_count: 1 }],
  })
  vi.mocked(api.getVocabularyCourseCounts).mockResolvedValue([
    { course_key: 'COURSE-005', term_count: 3, course_title: 'Applied LLM Engineering', course_slug: 'applied-llm-engineering', course_href: '/courses/applied-llm-engineering/learn' },
    { course_key: 'COURSE-006', term_count: 1, course_title: 'Production AI Engineering', course_slug: 'production-ai-engineering', course_href: '/courses/production-ai-engineering/learn' },
    { course_key: 'COURSE-015', term_count: 2, course_title: 'Voice AI Engineering', course_slug: 'voice-ai-engineering', course_href: '/courses/voice-ai-engineering/learn' },
  ])
  vi.mocked(api.getVocabularyTerm).mockResolvedValue(DETAIL)
  vi.mocked(api.recordVocabularyTermProgress).mockResolvedValue({ ...DETAIL, progress: { status: 'mastered' } })
  vi.mocked(api.getMyCourses).mockResolvedValue([MY_COURSE])
})

describe('AI Vocabulary page', () => {
  it('loads and renders terms from the API', async () => {
    render(<GlossaryPage />)
    expect(await screen.findByText('Retrieval-Augmented Generation')).toBeInTheDocument()
    expect(screen.getByText('Embedding')).toBeInTheDocument()
  })

  it('shows a loading state before the first response', () => {
    vi.mocked(api.listVocabularyTerms).mockReturnValue(new Promise(() => {}))
    render(<GlossaryPage />)
    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('shows an API failure state', async () => {
    vi.mocked(api.listVocabularyTerms).mockRejectedValue(new Error('down'))
    render(<GlossaryPage />)
    expect(await screen.findByRole('alert')).toBeInTheDocument()
  })

  it('shows an empty state when nothing matches a search', async () => {
    const user = userEvent.setup()
    vi.mocked(api.listVocabularyTerms).mockResolvedValue({ items: [], total: 0, page: 1, page_size: 24 })
    render(<GlossaryPage />)
    await user.type(await screen.findByPlaceholderText('Search a term in Arabic or English'), 'nonexistent')
    expect(await screen.findByText('No term matches that search.')).toBeInTheDocument()
  })

  it('shows an empty catalog state with no filters applied', async () => {
    vi.mocked(api.listVocabularyTerms).mockResolvedValue({ items: [], total: 0, page: 1, page_size: 24 })
    render(<GlossaryPage />)
    expect(await screen.findByText('No vocabulary terms yet.')).toBeInTheDocument()
  })

  it('searches in English', async () => {
    const user = userEvent.setup()
    render(<GlossaryPage />)
    await screen.findByText('Embedding')
    await user.type(screen.getByPlaceholderText('Search a term in Arabic or English'), 'Embedding')
    await waitFor(() => {
      expect(api.listVocabularyTerms).toHaveBeenLastCalledWith(
        expect.objectContaining({ search: 'Embedding' })
      )
    })
  })

  it('searches in Arabic', async () => {
    const user = userEvent.setup()
    render(<GlossaryPage />)
    await screen.findByText('Embedding')
    await user.type(screen.getByPlaceholderText('Search a term in Arabic or English'), 'التمثيل')
    await waitFor(() => {
      expect(api.listVocabularyTerms).toHaveBeenLastCalledWith(
        expect.objectContaining({ search: 'التمثيل' })
      )
    })
  })

  it('filters by category', async () => {
    const user = userEvent.setup()
    render(<GlossaryPage />)
    await screen.findByText('Embedding')
    await user.selectOptions(screen.getByDisplayValue('All'), 'RAG')
    await waitFor(() => {
      expect(api.listVocabularyTerms).toHaveBeenLastCalledWith(expect.objectContaining({ category: 'RAG' }))
    })
  })

  it('filters by difficulty', async () => {
    const user = userEvent.setup()
    render(<GlossaryPage />)
    await screen.findByText('Embedding')
    await user.selectOptions(screen.getByDisplayValue('All levels'), 'advanced')
    await waitFor(() => {
      expect(api.listVocabularyTerms).toHaveBeenLastCalledWith(expect.objectContaining({ difficulty: 'advanced' }))
    })
  })

  it('filters by course', async () => {
    const user = userEvent.setup()
    render(<GlossaryPage />)
    await screen.findByText('Embedding')
    await user.selectOptions(screen.getByDisplayValue('All courses'), 'COURSE-005')
    await waitFor(() => {
      expect(api.listVocabularyTerms).toHaveBeenLastCalledWith(expect.objectContaining({ course_id: 'COURSE-005' }))
    })
  })

  it('opens term detail with related terms and a lesson deep link', async () => {
    const user = userEvent.setup()
    render(<GlossaryPage />)
    await user.click(await screen.findByText('Retrieval-Augmented Generation'))

    const dialog = await screen.findByRole('dialog')
    expect(within(dialog).getByText('Embedding')).toBeInTheDocument() // related term
    const links = within(dialog).getAllByRole('link', { name: /Learn this concept/ })
    expect(links.length).toBeGreaterThan(0)
    expect(links[0]).toHaveAttribute('href', '/courses/applied-llm-engineering/learn')
  })

  it('records progress from the term detail', async () => {
    const user = userEvent.setup()
    render(<GlossaryPage />)
    await user.click(await screen.findByText('Retrieval-Augmented Generation'))
    const dialog = await screen.findByRole('dialog')
    await user.click(within(dialog).getByText('I know this'))
    await waitFor(() => {
      expect(api.recordVocabularyTermProgress).toHaveBeenCalledWith('retrieval_augmented_generation', 'mastered')
    })
  })

  it('signed out, tracking a term asks them to sign in and records nothing', async () => {
    mockIsAuthenticated = false
    useAuthStore.setState({ token: null })
    const user = userEvent.setup()
    render(<GlossaryPage />)
    await user.click(await screen.findByText('Retrieval-Augmented Generation'))
    const dialog = await screen.findByRole('dialog')
    await user.click(within(dialog).getByText('I know this'))
    expect(api.recordVocabularyTermProgress).not.toHaveBeenCalled()
    expect(useAuthPrompt.getState().open).toBe(true)
  })

  describe('From Your Masar', () => {
    it('shows terms from the learner’s active enrolled course, matched via course_slug', async () => {
      vi.mocked(api.listVocabularyTerms).mockImplementation(async (params) => {
        if (params?.course_id === 'COURSE-005' && params?.page_size === 6) return { items: [RAG], total: 1, page: 1, page_size: 6 }
        if (params?.page_size === 6) return EMPTY_RESPONSE
        return LIST_RESPONSE
      })
      render(<GlossaryPage />)
      const heading = await screen.findByText('From Your Masar')
      const section = heading.closest('section')!
      expect(within(section).getByText(/Applied LLM Engineering/)).toBeInTheDocument()
      expect(within(section).getByText('Retrieval-Augmented Generation')).toBeInTheDocument()
      await waitFor(() => {
        expect(api.listVocabularyTerms).toHaveBeenCalledWith(
          expect.objectContaining({ course_id: 'COURSE-005', page_size: 6 })
        )
      })
    })

    it('hides gracefully when the learner has no enrolled courses', async () => {
      vi.mocked(api.getMyCourses).mockResolvedValue([])
      render(<GlossaryPage />)
      await screen.findByText('Embedding')
      expect(screen.queryByText('From Your Masar')).not.toBeInTheDocument()
    })

    it('hides gracefully when unauthenticated', async () => {
      mockIsAuthenticated = false
      render(<GlossaryPage />)
      await screen.findByText('Embedding')
      expect(screen.queryByText('From Your Masar')).not.toBeInTheDocument()
      expect(api.getMyCourses).not.toHaveBeenCalled()
    })
  })

  describe('Continue Learning', () => {
    it('shows a section for terms with "learning" progress', async () => {
      vi.mocked(api.listVocabularyTerms).mockImplementation(async (params) => {
        if (params?.status === 'learning' && params?.page_size === 6) return { items: [EMBEDDING], total: 1, page: 1, page_size: 6 }
        if (params?.page_size === 6) return EMPTY_RESPONSE
        return LIST_RESPONSE
      })
      render(<GlossaryPage />)
      expect(await screen.findByText('Continue Learning')).toBeInTheDocument()
      await waitFor(() => {
        expect(api.listVocabularyTerms).toHaveBeenCalledWith(
          expect.objectContaining({ status: 'learning', page_size: 6 })
        )
      })
    })

    it('hides when there are no terms in "learning" status', async () => {
      vi.mocked(api.listVocabularyTerms).mockImplementation(async (params) => {
        if (params?.status === 'learning') return { items: [], total: 0, page: 1, page_size: 6 }
        return LIST_RESPONSE
      })
      render(<GlossaryPage />)
      await screen.findByText('Embedding')
      expect(screen.queryByText('Continue Learning')).not.toBeInTheDocument()
    })
  })

  describe('Browse by Course', () => {
    it('lists every course from backend data, including COURSE-006 and COURSE-015', async () => {
      render(<GlossaryPage />)
      expect(await screen.findByText('Browse by Course')).toBeInTheDocument()
      expect(screen.getByText('Production AI Engineering')).toBeInTheDocument()
      expect(screen.getByText('Voice AI Engineering')).toBeInTheDocument()
    })

    it('filters the list when a course is clicked', async () => {
      const user = userEvent.setup()
      render(<GlossaryPage />)
      await screen.findByText('Browse by Course')
      await user.click(screen.getByText('Production AI Engineering'))
      await waitFor(() => {
        expect(api.listVocabularyTerms).toHaveBeenLastCalledWith(
          expect.objectContaining({ course_id: 'COURSE-006' })
        )
      })
    })
  })

  describe('Browse by Category', () => {
    it('lists categories with their real term counts', async () => {
      render(<GlossaryPage />)
      expect(await screen.findByText('Browse by Category')).toBeInTheDocument()
      const section = screen.getByText('Browse by Category').closest('section')!
      expect(within(section).getByText('RAG')).toBeInTheDocument()
      expect(within(section).getByText('2 terms')).toBeInTheDocument()
    })

    it('filters the list when a category is clicked', async () => {
      const user = userEvent.setup()
      render(<GlossaryPage />)
      await screen.findByText('Browse by Category')
      const section = screen.getByText('Browse by Category').closest('section')!
      await user.click(within(section).getByText('RAG'))
      await waitFor(() => {
        expect(api.listVocabularyTerms).toHaveBeenLastCalledWith(expect.objectContaining({ category: 'RAG' }))
      })
    })
  })

  describe('pagination', () => {
    it('resets to page 1 when a filter changes', async () => {
      const user = userEvent.setup()
      vi.mocked(api.listVocabularyTerms).mockImplementation(async (params) => {
        if (params?.page_size === 6) return EMPTY_RESPONSE
        return { items: [RAG, EMBEDDING], total: 40, page: 1, page_size: 24 }
      })
      render(<GlossaryPage />)
      await screen.findByText('Embedding')
      await user.click(screen.getByText('Load more'))
      await waitFor(() => {
        expect(api.listVocabularyTerms).toHaveBeenLastCalledWith(expect.objectContaining({ page: 2 }))
      })
      await user.selectOptions(screen.getByDisplayValue('All levels'), 'advanced')
      await waitFor(() => {
        expect(api.listVocabularyTerms).toHaveBeenLastCalledWith(expect.objectContaining({ page: 1, difficulty: 'advanced' }))
      })
    })
  })
})
