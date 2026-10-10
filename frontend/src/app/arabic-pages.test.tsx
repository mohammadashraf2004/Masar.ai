import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import DashboardPage from '@/app/dashboard/page'
import LoginPage from '@/app/auth/login/page'
import TracksPage from '@/app/tracks/page'
import { useLanguageStore } from '@/lib/language'
import { NO_RECOMMENDATIONS, path, profile } from '@/test/fixtures'
import type { CareerTrackSummary, Enrollment } from '@/types'

// Arabic is the default, and these are the pages a visitor meets first. Each used to
// put English sentences inside an Arabic, right-to-left page, where the punctuation
// lands at the wrong end ("?Forgot your password") - so what is pinned here is that
// every string on them comes from the language table, in both languages.

const auth = vi.hoisted(() => ({ readiness: 42 }))
vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: { full_name: 'Amira Hassan', overall_readiness_score: auth.readiness }, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
  useSession: () => ({ user: { full_name: 'Amira Hassan', overall_readiness_score: auth.readiness }, isAuthenticated: true, isLoading: false }), useNextParam: () => null,
}))
vi.mock('@/components/layout/AppShell', async () => {
  const { createElement } = await import('react')
  return { AppShell: ({ children }: { children: React.ReactNode }) => createElement('div', null, children) }
})
vi.mock('@/components/ui/VocabularyProgress', () => ({ VocabularyProgress: () => null }))
vi.mock('@/components/ui/PaymentResultBanner', () => ({ PaymentResultBanner: () => null }))
vi.mock('@/lib/api', () => ({
  api: {
    listTracks: vi.fn(), getMyEnrollments: vi.fn(), enroll: vi.fn(), getSkillScores: vi.fn(), getRoadmap: vi.fn(),
    getWallet: vi.fn(), getMyLearningProfile: vi.fn(), getMyLearningPath: vi.fn(), getRecommendations: vi.fn(), verifyEmail: vi.fn(), login: vi.fn(),
    forgotPassword: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const ARABIC_TRACK_TITLES: Record<string, string> = {
  'data-analyst': 'محلل بيانات',
  'ml-engineer': 'مهندس تعلم آلي',
  'ai-developer': 'مطور ذكاء اصطناعي',
  'mlops-engineer': 'مهندس MLOps',
  'ai-engineer': 'مهندس ذكاء اصطناعي',
}
const track = (id: number, slug: string, title: string, weeks: number): CareerTrackSummary =>
  ({ id, slug, title, title_en: title, title_ar: ARABIC_TRACK_TITLES[slug], description: '', description_ar: '', icon: '', estimated_weeks: weeks })
const TRACKS = [
  track(1, 'data-analyst', 'Data Analyst', 12), track(2, 'ml-engineer', 'ML Engineer', 16),
  track(3, 'ai-developer', 'AI Developer', 14), track(4, 'mlops-engineer', 'MLOps Engineer', 10),
  track(5, 'ai-engineer', 'AI Engineer', 24),
]
const ENROLLMENT: Enrollment = { id: 1, track_id: 3, track: TRACKS[2], completion_percentage: 0, enrolled_at: '2026-09-01T00:00:00Z' }

beforeEach(() => {
  auth.readiness = 42
  useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
  vi.mocked(api.listTracks).mockResolvedValue(TRACKS)
  vi.mocked(api.getMyEnrollments).mockResolvedValue([ENROLLMENT])
  vi.mocked(api.getSkillScores).mockResolvedValue({ readiness_score: 42, skills: [] })
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 100 })
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.getMyLearningPath).mockResolvedValue(path())
  vi.mocked(api.getRecommendations).mockResolvedValue(NO_RECOMMENDATIONS)
})

describe('sign in', () => {
  it('is in Arabic, with no English sentence left', () => {
    render(<LoginPage />)
    expect(screen.getByRole('heading', { level: 1, name: 'أهلاً بعودتك' })).toBeInTheDocument()
    expect(screen.getByText('سجّل الدخول لمتابعة رحلة تعلّمك.')).toBeInTheDocument()
    expect(screen.getByLabelText('البريد الإلكتروني')).toBeInTheDocument()
    expect(screen.getByLabelText('كلمة المرور')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'تسجيل الدخول' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'نسيت كلمة المرور؟' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'أنشئ حساباً' })).toHaveAttribute('href', '/auth/register')
    // the side panel too
    expect(screen.getByText('مهندس ذكاء اصطناعي جاهز للعمل')).toBeInTheDocument()
    expect(screen.getByText('دروس بالعربية أولاً، ومصطلحات بالإنجليزية')).toBeInTheDocument()
    for (const english of ['Welcome back', 'Sign in', 'Forgot your password?', 'Create one', 'AI-graded exercises and quizzes']) {
      expect(screen.queryByText(new RegExp(english))).toBeNull()
    }
  })

  it('lets the reader change the language from the sign-in page itself', () => {
    render(<LoginPage />)
    expect(screen.getAllByRole('button', { name: /العربية|English|ع/ }).length).toBeGreaterThan(0)
  })

  it('walks through the reset flow in Arabic', async () => {
    const user = userEvent.setup()
    render(<LoginPage />)
    await user.click(screen.getByRole('button', { name: 'نسيت كلمة المرور؟' }))
    expect(screen.getByRole('heading', { level: 1, name: 'إعادة تعيين كلمة المرور' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'أرسل رابط إعادة التعيين' })).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'العودة إلى تسجيل الدخول' }))
    expect(screen.getByRole('heading', { level: 1, name: 'أهلاً بعودتك' })).toBeInTheDocument()
  })

  it('still reads exactly as before in English', () => {
    useLanguageStore.setState({ language: 'en' })
    render(<LoginPage />)
    expect(screen.getByRole('heading', { level: 1, name: 'Welcome back' })).toBeInTheDocument()
    expect(screen.getByText('Sign in to continue your learning journey.')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Sign in' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Forgot your password?' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Create one' })).toBeInTheDocument()
    expect(screen.getByText('AI engineer.')).toBeInTheDocument()
  })
})

describe('the career tracks page', () => {
  async function renderTracks() {
    render(<TracksPage />)
    await screen.findByRole('link', { name: 'استكشف مطور ذكاء اصطناعي' })
  }

  it('is in Arabic, with no English sentence left', async () => {
    await renderTracks()
    expect(screen.getByRole('heading', { level: 1, name: 'المسارات المهنية' })).toBeInTheDocument()
    expect(screen.getByText(/اختر المسار الأقرب للوظيفة التي تستهدفها/)).toBeInTheDocument()
    for (const english of ['Career tracks', 'Curriculum libraries', 'Open your Masar', 'Coming soon', "What you'll learn", 'Overall progress']) {
      expect(screen.queryByText(new RegExp(english))).toBeNull()
    }
  })

  it('makes every whole card open its detail route', async () => {
    await renderTracks()
    expect(screen.getByRole('link', { name: 'استكشف مهندس MLOps' })).toHaveAttribute('href', '/tracks/mlops-engineer')
  })

  it('uses the Arabic track title on the Arabic screen', async () => {
    await renderTracks()
    expect(screen.getByRole('heading', { name: 'مهندس MLOps' })).toHaveAttribute('dir', 'auto')
  })

  it('receives bilingual canonical track titles from the catalogue', () => {
    for (const item of TRACKS) {
      expect(item.title_en).toBeTruthy()
      expect(item.title_ar).toBeTruthy()
    }
  })
})

describe('the dashboard stat tiles', () => {
  const tile = (label: string) => screen.getByText(label).closest('.p-5') as HTMLElement

  async function renderDashboard() {
    render(<DashboardPage />)
    await screen.findByText(ENROLLMENT.track.title_ar ?? ENROLLMENT.track.title)
  }

  it('are in Arabic', async () => {
    await renderDashboard()
    for (const label of ['مؤشر الجاهزية', 'المسارات المسجّل بها', 'المهارات المتتبَّعة', 'هذا الأسبوع']) {
      expect(screen.getByText(label)).toBeInTheDocument()
    }
    for (const english of ['Readiness score', 'Tracks enrolled', 'Skills tracked', 'This week', 'Overall', 'Assessed']) {
      expect(screen.queryByText(english)).toBeNull()
    }
  })

  it('and so is the rest of the page: the sections, the roadmap prompt, the mentor', async () => {
    await renderDashboard()
    for (const arabic of ['مساراتك', 'الخطة الأسبوعية', 'درجات المهارات', 'المرشد الذكي', 'افتح المرشد']) {
      expect(screen.getByText(arabic)).toBeInTheDocument()
    }
    expect(screen.getByText(/أنشئ خطة أسبوعية مخصّصة لمسار مطور ذكاء اصطناعي/)).toBeInTheDocument()
    expect(screen.getByText('برنامج 14 أسبوعاً')).toBeInTheDocument()
    expect(screen.queryByText('Your tracks')).toBeNull()
    expect(screen.queryByText(/Generate a personalised weekly plan/)).toBeNull()
  })

  it('use amber only: a 36px amber-soft square with an amber icon, and the number in the headline colour', async () => {
    await renderDashboard()
    for (const label of ['مؤشر الجاهزية', 'المسارات المسجّل بها', 'المهارات المتتبَّعة', 'هذا الأسبوع']) {
      const t = tile(label)
      const square = t.querySelector('span.grid') as HTMLElement
      expect(square).toHaveClass('h-9', 'w-9', 'rounded-lg', 'bg-amber-soft', 'text-amber-text')
      expect(square.querySelector('svg')).not.toBeNull()
      // no decorative hues left: sky, emerald and violet are for states
      expect(t.innerHTML).not.toMatch(/text-(sky|emerald|violet)/)
    }
    expect(tile('المسارات المسجّل بها').children[1]).toHaveClass('text-white')
    expect(tile('المهارات المتتبَّعة').children[1]).toHaveClass('text-white')
    expect(tile('هذا الأسبوع').children[1]).toHaveClass('text-white')
  })

  it('colour the readiness score only once it means something good or bad', async () => {
    auth.readiness = 82
    const { unmount } = render(<DashboardPage />)
    await screen.findByText(ENROLLMENT.track.title_ar ?? ENROLLMENT.track.title)
    expect(within(tile('مؤشر الجاهزية')).getByText('82%')).toHaveClass('text-emerald')
    unmount()

    auth.readiness = 42
    render(<DashboardPage />)
    await screen.findByText(ENROLLMENT.track.title_ar ?? ENROLLMENT.track.title)
    expect(within(tile('مؤشر الجاهزية')).getByText('42%')).toHaveClass('text-rose')
  })

  it("leave a fresh account's 0% plain: it is nothing yet, not bad", async () => {
    auth.readiness = 0
    await renderDashboard()
    const value = within(tile('مؤشر الجاهزية')).getByText('0%')
    expect(value).toHaveClass('text-white')
    expect(value).not.toHaveClass('text-rose')
  })
})
