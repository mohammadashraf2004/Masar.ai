import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import ProfilePage from '@/app/profile/page'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import { setPathname } from '@/test/nav'
import type { User } from '@/types'

const student: User = {
  id: 1, email: 'layan@example.com', full_name: 'Layan Al-Harbi', role: 'student', experience_level: 'beginner',
  is_verified: true, overall_readiness_score: 72, created_at: '2026-01-05T00:00:00Z',
  requires_legal_acceptance: false, pending_updates: [], bio: '', github_url: '', linkedin_url: '',
} as User

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: useAuthStore.getState().user, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
  useSession: () => ({ user: useAuthStore.getState().user, isAuthenticated: true, isLoading: false }), useNextParam: () => null,
}))
vi.mock('@/lib/api', () => ({
  api: {
    getMyLearningPath: vi.fn(), getMySkillGaps: vi.fn(), getProfileActivity: vi.fn(), getScorecard: vi.fn(),
    getMyCertificates: vi.fn(), getMyCourses: vi.fn(), getLabProjects: vi.fn(),
    updateMe: vi.fn(), deleteAccount: vi.fn(), resendVerification: vi.fn(), logoutAllDevices: vi.fn(),
    getWallet: vi.fn(), search: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const skill = (slug: string, name: string, name_ar: string, over = {}) => ({
  slug, name, name_ar, status: 'partial', is_goal_required: true, is_immediate: false, course_count: 1, ...over,
})
const PATH = {
  is_saved: true, status: 'active',
  level: { slug: 'intermediate', name: 'Intermediate', name_ar: 'متوسط', rank: 2 },
  career_goal: { slug: 'ai-engineer', title: 'AI Engineer', title_ar: 'مهندس ذكاء اصطناعي' },
  fields: [], effective_fields: [], advisories: [], estimated_hours: 0, estimated_weeks: 0,
  stages: ['a', 'b', 'c', 'd', 'e'].map((slug, i) => ({ slug, position: i, title: slug, phase: '', kind: '', status: 'active', upcoming_count: 0, courses: [] })),
  current_stage_slug: 'c',
  progress: { path_pct: 46, overall_pct: 46, by_role: {}, by_field: {}, by_skill: { python: 88, rag: 41 } },
}
const GAPS = {
  available: true, fields: [], groups: [],
  summary: { required: 3, known: 1, partial: 1, missing: 1, immediate: 1, coverage_pct: 50 },
  known: [skill('python', 'Python', 'بايثون', { status: 'known' })],
  partial: [skill('rag', 'RAG Evaluation', 'تقييم RAG')],
  missing: [skill('langgraph', 'LangGraph', 'LangGraph', { status: 'missing', is_immediate: true })],
}
const ACTIVITY = {
  days: Array.from({ length: 84 }, (_, i) => ({ date: `2026-07-${String((i % 28) + 1).padStart(2, '0')}`, count: i > 80 ? 2 : 0 })),
  active_days: 3, current_streak: 3,
}

beforeEach(() => {
  useAuthStore.setState({ token: 'tok', expiresAt: null, _hasHydrated: true, user: student })
  useLanguageStore.setState({ language: 'en', mode: 'english_technical', annotateTerms: false })
  setPathname('/profile')
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 40 })
  vi.mocked(api.getMyLearningPath).mockResolvedValue(PATH as never)
  vi.mocked(api.getMySkillGaps).mockResolvedValue(GAPS as never)
  vi.mocked(api.getProfileActivity).mockResolvedValue(ACTIVITY)
  vi.mocked(api.getScorecard).mockResolvedValue({ total_study_minutes: 148 * 60 })
  vi.mocked(api.getMyCertificates).mockResolvedValue([
    { certificate_id: 'c1', track_title: 'Data Analyst', user_name: 'Layan', score: 92, issued_at: '2026-06-10T00:00:00Z', is_valid: true },
  ])
  vi.mocked(api.getMyCourses).mockResolvedValue([
    { course_id: 3, slug: 'llm-apis', title: 'LLM APIs', progress: 100, enrolled_at: '2026-08-01', access_type: 'free', status: 'completed', completed_at: '2026-09-02T00:00:00Z' },
    { course_id: 4, slug: 'rag', title: 'RAG', progress: 30, enrolled_at: '2026-09-01', access_type: 'free', status: 'in_progress' },
  ] as never)
  vi.mocked(api.getLabProjects).mockResolvedValue([])
})

describe('the profile page', () => {
  it('shows the learner, their path and real numbers', async () => {
    render(<ProfilePage />)
    expect(await screen.findByRole('heading', { level: 1, name: 'Layan Al-Harbi' })).toBeInTheDocument()
    expect(screen.getByText('Member since January 2026')).toBeInTheDocument()
    expect(await screen.findByText('AI Engineer')).toBeInTheDocument()
    expect(screen.getByText('Stage 3 of 5 · 46%')).toBeInTheDocument()
    expect(screen.getByText('Intermediate')).toBeInTheDocument()
    expect(screen.getByText('72')).toBeInTheDocument()
    await waitFor(() => expect(screen.getByText('148')).toBeInTheDocument())
    expect(screen.getByText('3')).toBeInTheDocument()
    expect(screen.getByText('days')).toBeInTheDocument()
  })

  it('maps skills from the path, names the next gap and draws the activity', async () => {
    render(<ProfilePage />)
    const python = await screen.findByRole('progressbar', { name: 'Python' })
    expect(python).toHaveAttribute('aria-valuenow', '88')
    expect(screen.getByRole('progressbar', { name: 'RAG Evaluation' }).firstElementChild).toHaveClass('bg-rose')
    expect(screen.getByText(/Next skill to learn: LangGraph\. Your current stage teaches it\./)).toBeInTheDocument()
    expect(screen.getByRole('img', { name: /3 active days/ })).toBeInTheDocument()
  })

  it('lists real achievements newest first and links certificates to verification', async () => {
    render(<ProfilePage />)
    const section = (await screen.findByRole('heading', { name: 'Achievements' })).closest('section') as HTMLElement
    await within(section).findByText('LLM APIs')
    const titles = within(section).getAllByRole('link').map(a => a.textContent)
    expect(titles[1]).toContain('LLM APIs')
    expect(titles[2]).toContain('Data Analyst')
    expect(within(section).getByText('Data Analyst').closest('a')).toHaveAttribute('href', '/verify/c1')
    expect(within(section).queryByText('RAG')).toBeNull()
  })

  it('shows honest empty states without a learning path or activity', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(null)
    vi.mocked(api.getMySkillGaps).mockRejectedValue(new Error('no path'))
    vi.mocked(api.getMyCertificates).mockResolvedValue([])
    vi.mocked(api.getMyCourses).mockResolvedValue([])
    render(<ProfilePage />)
    expect(await screen.findByText('Build your learning path to see your skills here.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Build your Masar' })).toHaveAttribute('href', '/learn/masar')
    expect(await screen.findByText('Finish a course, a project or an exam and it appears here.')).toBeInTheDocument()
  })

  it('speaks Arabic, right to left, with Arabic plural units', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: false })
    render(<ProfilePage />)
    expect(await screen.findByText('مهندس ذكاء اصطناعي')).toBeInTheDocument()
    expect(screen.getByText('AI Engineer')).toHaveAttribute('dir', 'ltr')
    expect(screen.getByText('المرحلة 3 من 5 · 46%')).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: 'الملف الشخصي' })).toHaveAttribute('aria-selected', 'true')
    expect(await screen.findByText('أيام')).toBeInTheDocument()
    expect(screen.getByText(/أقرب مهارة تنقصك: LangGraph/)).toBeInTheDocument()
  })

  it('edits the profile in the settings tab and saves through the API', async () => {
    const user = userEvent.setup()
    vi.mocked(api.updateMe).mockResolvedValue({ ...student, full_name: 'Layan H.' })
    render(<ProfilePage />)
    await user.click(await screen.findByRole('button', { name: 'Edit profile' }))
    expect(screen.getByRole('tab', { name: 'Settings' })).toHaveAttribute('aria-selected', 'true')
    const name = screen.getByLabelText('Full name')
    await user.clear(name)
    await user.type(name, 'Layan H.')
    expect(screen.getByLabelText('Email')).toHaveAttribute('readonly')
    await user.click(screen.getByRole('button', { name: /Save changes/ }))
    await waitFor(() => expect(api.updateMe).toHaveBeenCalledWith(expect.objectContaining({ full_name: 'Layan H.' })))
    expect(await screen.findByText('Saved')).toBeInTheDocument()
    expect(useAuthStore.getState().user?.full_name).toBe('Layan H.')
  })

  it('asks before deleting the account', async () => {
    const user = userEvent.setup()
    vi.mocked(api.deleteAccount).mockResolvedValue(undefined as never)
    render(<ProfilePage />)
    await user.click(await screen.findByRole('tab', { name: 'Settings' }))
    await user.click(screen.getByRole('button', { name: 'Delete account' }))
    expect(screen.getByText("This can't be undone from the app. Delete your account?")).toBeInTheDocument()
    expect(api.deleteAccount).not.toHaveBeenCalled()
    await user.click(screen.getByRole('button', { name: 'Delete account' }))
    await waitFor(() => expect(api.deleteAccount).toHaveBeenCalledOnce())
  })
})
