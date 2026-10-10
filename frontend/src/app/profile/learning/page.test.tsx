import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import LearningProfilePage from '@/app/profile/learning/page'
import CoursePage from '@/app/courses/[slug]/page'
import { useLanguageStore } from '@/lib/language'
import { CATALOG, MY_SKILLS, NEEDS_ONBOARDING, NLP, SKILL_OPTIONS, VISION, course, path, profile, ref, skillGaps } from '@/test/fixtures'
import { setParams } from '@/test/nav'
import type { CatalogCourseDetail } from '@/types'

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
    getMyLearningProfile: vi.fn(), saveMyLearningProfile: vi.fn(), saveMyLearningPath: vi.fn(),
    getCatalogCourse: vi.fn(), getMySkills: vi.fn(), saveMySkills: vi.fn(), getSkillOptions: vi.fn(),
    getMySkillGaps: vi.fn(), getCourseAccess: vi.fn(), getCourseReadiness: vi.fn(),
  },
}))
import { api } from '@/lib/api'

beforeEach(() => {
  vi.mocked(api.getMySkillGaps).mockResolvedValue(skillGaps())
  vi.mocked(api.getLearningLevels).mockResolvedValue(CATALOG.levels)
  vi.mocked(api.getLearningFields).mockResolvedValue(CATALOG.fields)
  vi.mocked(api.getCareerGoals).mockResolvedValue(CATALOG.goals)
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.saveMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.saveMyLearningPath).mockResolvedValue(path())
  vi.mocked(api.getMySkills).mockResolvedValue(MY_SKILLS)
  vi.mocked(api.getSkillOptions).mockResolvedValue(SKILL_OPTIONS)
})

describe('the learning profile page', () => {
  it('shows the saved answers selected', async () => {
    render(<LearningProfilePage />)
    expect(await screen.findByRole('radio', { name: /Intermediate/ })).toHaveAttribute('aria-checked', 'true')
    expect(screen.getByRole('checkbox', { name: /NLP & LLMs/ })).toHaveAttribute('aria-checked', 'true')
    expect(screen.getByRole('radio', { name: /AI Engineer/ })).toHaveAttribute('aria-checked', 'true')
  })

  it('cannot be saved until level, a field and a goal are all chosen', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    const user = userEvent.setup()
    render(<LearningProfilePage />)
    const save = await screen.findByRole('button', { name: 'Save and rebuild' })
    expect(save).toBeDisabled()
    await user.click(screen.getByRole('radio', { name: /Beginner/ }))
    await user.click(screen.getByRole('checkbox', { name: /Computer Vision/ }))
    expect(save).toBeDisabled()
    await user.click(screen.getByRole('radio', { name: /ML Engineer/ }))
    expect(save).toBeEnabled()
  })

  it('saves the answers and rebuilds the path', async () => {
    const user = userEvent.setup()
    render(<LearningProfilePage />)
    await user.click(await screen.findByRole('checkbox', { name: /Computer Vision/ }))
    await user.click(screen.getByRole('button', { name: 'Save and rebuild' }))
    await waitFor(() => expect(api.saveMyLearningPath).toHaveBeenCalledWith({ regenerate: true }))
    expect(api.saveMyLearningProfile).toHaveBeenCalledWith({
      level: 'intermediate', fields: ['nlp', 'computer-vision'], career_goal: 'ai-engineer',
    })
    expect(await screen.findByRole('status')).toHaveTextContent('Saved. Your Masar was rebuilt.')
    expect(screen.getByRole('link', { name: 'Your Masar' })).toHaveAttribute('href', '/learn/masar')
  })

  it('reports a failed save', async () => {
    const user = userEvent.setup()
    vi.mocked(api.saveMyLearningProfile).mockRejectedValue(new Error('boom'))
    render(<LearningProfilePage />)
    await user.click(await screen.findByRole('button', { name: 'Save and rebuild' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not save')
  })

  it('explains an advanced field against the level currently chosen', async () => {
    const user = userEvent.setup()
    render(<LearningProfilePage />)
    await user.click(await screen.findByRole('checkbox', { name: /Multimodal AI/ }))
    expect(screen.getByRole('note')).toHaveTextContent('advanced path')
    await user.click(screen.getByRole('radio', { name: /Advanced/ }))
    expect(screen.queryByRole('note')).toBeNull()
  })

  it('is written in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    render(<LearningProfilePage />)
    expect(await screen.findByRole('button', { name: 'احفظ وأعد البناء' })).toBeInTheDocument()
  })
})

describe('the course page', () => {
  const detail: CatalogCourseDetail = {
    ...course(), assumes: [], learning_objectives: [], learning_objectives_ar: [],
    prerequisites: [{ id: 5, slug: 'llm-integration', title: 'LLM Integration', title_ar: null }],
  }

  beforeEach(() => {
    setParams({ slug: 'rag-knowledge-systems' })
    vi.mocked(api.getCourseAccess).mockResolvedValue({ has_access: true, reason: 'free', enrollment_id: null })
    vi.mocked(api.getCourseReadiness).mockRejectedValue(new Error('not needed here'))
  })

  it('shows the course opened, with why it matters and where to start', async () => {
    vi.mocked(api.getCatalogCourse).mockResolvedValue(detail)
    render(<CoursePage />)
    expect(await screen.findByRole('heading', { name: 'RAG & Knowledge Systems' })).toBeInTheDocument()
    expect(api.getCatalogCourse).toHaveBeenCalledWith('rag-knowledge-systems')
    expect(await screen.findByText('Build retrieval-augmented applications.')).toBeInTheDocument()
    // Open to anyone with access, with no track or goal involved: enrolling is one click away.
    expect(screen.getByRole('button', { name: 'Enroll now' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'LLM Integration' })).toHaveAttribute('href', '/courses/llm-integration')
  })

  it('says so when the course does not exist', async () => {
    vi.mocked(api.getCatalogCourse).mockRejectedValue({ response: { status: 404 } })
    render(<CoursePage />)
    expect(await screen.findByText('This course does not exist.')).toBeInTheDocument()
  })

  it('titles the page in Arabic for an Arabic reader', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    vi.mocked(api.getCatalogCourse).mockResolvedValue(detail)
    render(<CoursePage />)
    expect(await screen.findByRole('heading', { level: 1 })).toHaveTextContent('أنظمة RAG والمعرفة')
  })

  it('has no field-specific assumptions about which fields exist', async () => {
    vi.mocked(api.getCatalogCourse).mockResolvedValue({ ...detail, fields: [ref(NLP), ref(VISION)] })
    render(<CoursePage />)
    expect(await screen.findByText('Computer Vision')).toBeInTheDocument()
  })
})
