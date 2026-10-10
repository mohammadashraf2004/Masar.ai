import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import type { ReactNode } from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import CoursePage from '@/app/courses/[slug]/page'
import { AuthPromptDialog, useAuthPrompt } from '@/components/auth/AuthPrompt'
import { course } from '@/test/fixtures'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import type { CatalogCourseDetail } from '@/types'

// A signed-out visitor on a course overview: the real hooks, no session.
vi.mock('next/navigation', () => ({
  useParams: () => ({ slug: 'course-007' }),
  useRouter: () => ({ replace: vi.fn(), push: vi.fn() }),
  usePathname: () => '/courses/course-007',
}))
vi.mock('@/components/layout/AppShell', () => ({
  AppShell: ({ children }: { children: ReactNode }) => <>{children}<AuthPromptDialog /></>,
}))
vi.mock('@/components/layout/PageHeader', () => ({ PageHeader: ({ title }: { title: string }) => <h1>{title}</h1> }))
vi.mock('@/lib/api', () => ({
  api: {
    getCatalogCourse: vi.fn(),
    getCourseAccess: vi.fn(),
    getCourseReadiness: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const toolCourse: CatalogCourseDetail = {
  ...course({ slug: 'course-007', kind: 'tool_course', href: '/courses/course-007/learn' }),
  assumes: [], prerequisites: [], learning_objectives: [], learning_objectives_ar: [],
  modules: [{
    id: 70, order: 1, title: 'Agents and tools', title_ar: 'الوكلاء والأدوات', lesson_count: 2,
    exercise_count: 0, quiz_count: 0, project_count: 0,
    lessons: [
      { id: 701, order: 1, title: 'What an agent is', title_ar: 'ما هو الوكيل' },
      { id: 702, order: 2, title: 'Calling a tool', title_ar: 'استدعاء أداة' },
    ],
  }],
}

beforeEach(() => {
  useAuthStore.setState({ token: null, user: null, expiresAt: null, _hasHydrated: true })
  useAuthPrompt.setState({ open: false, next: null })
  useLanguageStore.setState({ language: 'en', mode: 'arabic_first' })
  vi.mocked(api.getCatalogCourse).mockResolvedValue(toolCourse)
})

describe('a course overview for a signed-out visitor', () => {
  it('shows the course and its lesson names, and asks nothing of the account API', async () => {
    render(<CoursePage />)
    expect(await screen.findByText('Agents and tools')).toBeInTheDocument()
    expect(screen.getByText('What an agent is')).toBeInTheDocument()
    expect(screen.getByText('Calling a tool')).toBeInTheDocument()
    expect(api.getCourseAccess).not.toHaveBeenCalled()
    expect(api.getCourseReadiness).not.toHaveBeenCalled()
    // No Pro upsell or enrolment controls for someone without an account.
    expect(screen.queryByRole('link', { name: 'Upgrade to Pro' })).toBeNull()
    expect(screen.getByText('Lessons open after you sign in.')).toBeInTheDocument()
  })

  it('"Sign in to start learning" opens the sign-in dialog, returning to this course', async () => {
    const u = userEvent.setup()
    render(<CoursePage />)
    await u.click(await screen.findByRole('button', { name: 'Sign in to start learning' }))
    const dialog = screen.getByRole('dialog', { name: 'Sign in to continue learning' })
    expect(dialog).toHaveTextContent('Create your free Masar account to access lessons, exercises, and challenges.')
    expect(within(dialog).getByRole('link', { name: 'Sign in' })).toHaveAttribute('href', '/auth/login?next=%2Fcourses%2Fcourse-007')
    expect(within(dialog).getByRole('link', { name: 'Create free account' })).toHaveAttribute('href', '/auth/register?next=%2Fcourses%2Fcourse-007')
  })

  it('a lesson name opens the sign-in dialog for that lesson instead of the lesson', async () => {
    const u = userEvent.setup()
    render(<CoursePage />)
    const lesson = await screen.findByRole('link', { name: 'Calling a tool' })
    expect(lesson).toHaveAttribute('href', '/courses/course-007/lessons/702')
    await u.click(lesson)
    const dialog = screen.getByRole('dialog', { name: 'Sign in to continue learning' })
    expect(within(dialog).getByRole('link', { name: 'Sign in' }))
      .toHaveAttribute('href', '/auth/login?next=%2Fcourses%2Fcourse-007%2Flessons%2F702')
  })

  it('is written in Arabic for an Arabic reader', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    const u = userEvent.setup()
    render(<CoursePage />)
    expect(await screen.findByText('ما هو الوكيل')).toBeInTheDocument()
    await u.click(screen.getByRole('button', { name: 'سجّل الدخول لبدء التعلّم' }))
    const dialog = screen.getByRole('dialog', { name: 'سجّل الدخول لمتابعة التعلّم' })
    expect(dialog).toHaveTextContent('أنشئ حسابك المجاني للوصول إلى الدروس والتمارين والتحديات.')
    expect(within(dialog).getByRole('link', { name: 'إنشاء حساب مجاني' })).toBeInTheDocument()
  })
})

describe('the same page once signed in', () => {
  it('asks the server what this account may open (Free/Pro is unchanged)', async () => {
    useAuthStore.setState({ token: 'tok', user: { id: 1 } as never, expiresAt: null, _hasHydrated: true })
    vi.mocked(api.getCourseAccess).mockResolvedValue({
      has_access: false, reason: 'purchase_required', enrollment_id: null, free_lesson_count: 2,
    })
    vi.mocked(api.getCourseReadiness).mockRejectedValue(new Error('n/a'))
    render(<CoursePage />)
    expect(await screen.findByRole('link', { name: 'Upgrade to Pro' })).toBeInTheDocument()
    expect(api.getCourseAccess).toHaveBeenCalledWith('course-007')
    expect(screen.queryByRole('button', { name: 'Sign in to start learning' })).toBeNull()
  })
})
