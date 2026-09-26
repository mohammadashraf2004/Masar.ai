import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import MyCoursesPage from '@/app/learn/my-courses/page'
import { STRINGS } from '@/lib/i18n'
import { useLanguageStore } from '@/lib/language'
import type { MyCourse } from '@/types'

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
}))
vi.mock('@/components/layout/AppShell', async () => {
  const { createElement } = await import('react')
  return { AppShell: ({ children }: { children: React.ReactNode }) => createElement('div', null, children) }
})
vi.mock('@/components/layout/PageHeader', async () => {
  const { createElement } = await import('react')
  return { PageHeader: ({ title }: { title: string }) => createElement('h1', null, title) }
})
vi.mock('@/lib/api', () => ({ api: { getMyCourses: vi.fn() } }))
import { api } from '@/lib/api'

const mine = (over: Partial<MyCourse> = {}): MyCourse => ({
  course_id: 1, slug: 'course-001', title: 'Machine Learning Foundations', title_ar: 'أساسيات تعلم الآلة',
  href: '/tools/ml', progress: 42.4, enrolled_at: '2026-09-01T00:00:00Z', access_type: 'free',
  status: 'in_progress', module_count: 12, ...over,
})

beforeEach(() => {
  vi.mocked(api.getMyCourses).mockResolvedValue([mine()])
})

describe('my courses', () => {
  it('lists the enrolled courses with live progress and a way to continue', async () => {
    render(<MyCoursesPage />)
    expect(await screen.findByText('Machine Learning Foundations')).toBeInTheDocument()
    expect(screen.getByText('42%')).toBeInTheDocument()
    expect(screen.getByText('12 modules')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continue' })).toHaveAttribute('href', '/tools/ml')
    expect(screen.getByRole('link', { name: 'Course details' })).toHaveAttribute('href', '/courses/course-001')
  })

  it('marks a completed course and offers a review, and a paused one as paused', async () => {
    vi.mocked(api.getMyCourses).mockResolvedValue([
      mine({ status: 'completed', progress: 100 }),
      mine({ course_id: 2, slug: 'course-002', title: 'Deep Learning', status: 'paused' }),
    ])
    render(<MyCoursesPage />)
    expect(await screen.findByText('Completed')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Review course' })).toBeInTheDocument()
    expect(screen.getByText('Paused')).toBeInTheDocument()
  })

  it('points a learner with no courses at the catalogue, not at a track', async () => {
    vi.mocked(api.getMyCourses).mockResolvedValue([])
    render(<MyCoursesPage />)
    expect(await screen.findByText(STRINGS.en['mc.empty'])).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Browse courses' })).toHaveAttribute('href', '/learn')
  })

  it('shows an error when the list cannot be loaded', async () => {
    vi.mocked(api.getMyCourses).mockRejectedValue(new Error('down'))
    render(<MyCoursesPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.en['mc.error'])
  })

  it('is in Arabic, with the Arabic title', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    render(<MyCoursesPage />)
    expect(await screen.findByText('أساسيات تعلم الآلة')).toBeInTheDocument()
    expect(screen.getByText(STRINGS.ar['mc.progress'])).toBeInTheDocument()
    expect(screen.queryByText('Progress')).toBeNull()
  })
})
