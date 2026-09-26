import { render, screen, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import RoadmapPage from '@/app/roadmaps/[slug]/page'
import { STRINGS } from '@/lib/i18n'
import { useLanguageStore } from '@/lib/language'
import { GOALS, course } from '@/test/fixtures'
import { setParams } from '@/test/nav'
import type { TrackDetail } from '@/types'

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
vi.mock('@/lib/api', () => ({ api: { getCareerRoadmap: vi.fn() } }))
import { api } from '@/lib/api'

const python = course({ id: 1, slug: 'course-013', title: 'Applied Data Analysis with Python', title_ar: null })
const ml = course({ id: 2, slug: 'course-001', title: 'Machine Learning Foundations', enrollment: { status: 'in_progress', progress_percentage: 40 } })

const roadmap: TrackDetail = {
  ...GOALS[2], course_count: 2, available_course_count: 2,
  courses: [
    { course: python, track_role: 'supporting', position: 1 },
    { course: ml, track_role: 'core', position: 2 },
  ],
}

beforeEach(() => {
  setParams({ slug: GOALS[2].slug })
  vi.mocked(api.getCareerRoadmap).mockResolvedValue(roadmap)
})

describe('a career roadmap', () => {
  it('lists the recommended courses in order, as guidance not gates', async () => {
    render(<RoadmapPage />)
    expect(await screen.findByText(/recommend for becoming/)).toBeInTheDocument()
    expect(api.getCareerRoadmap).toHaveBeenCalledWith(GOALS[2].slug)
    const items = screen.getAllByRole('listitem').filter((li) => li.parentElement?.tagName === 'OL')
    expect(items).toHaveLength(2)
    expect(within(items[0]).getByText('Step 1')).toBeInTheDocument()
    expect(within(items[0]).getByText('Supporting')).toBeInTheDocument()
    expect(within(items[1]).getByText('Core')).toBeInTheDocument()
    expect(screen.getByText('They are guidance, not gates. Open any course and enroll directly.')).toBeInTheDocument()
  })

  it('links each course to its own page: the same canonical course, enrollable on its own', async () => {
    render(<RoadmapPage />)
    expect(await screen.findByRole('link', { name: 'Applied Data Analysis with Python' })).toHaveAttribute('href', '/courses/course-013')
    expect(screen.getByRole('link', { name: 'Machine Learning Foundations' })).toHaveAttribute('href', '/courses/course-001')
  })

  it('shows the learner’s own progress on a course that is on the roadmap', async () => {
    render(<RoadmapPage />)
    expect(await screen.findByText('40% complete')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continue' })).toHaveAttribute('href', '/courses/course-001')
  })

  it('says so when the roadmap is empty, missing or fails', async () => {
    vi.mocked(api.getCareerRoadmap).mockResolvedValueOnce({ ...roadmap, courses: [] })
    const first = render(<RoadmapPage />)
    expect(await screen.findByText(STRINGS.en['rm.empty'])).toBeInTheDocument()
    first.unmount()
    vi.mocked(api.getCareerRoadmap).mockRejectedValueOnce({ response: { status: 404 } })
    render(<RoadmapPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.en['rm.loadError'])
  })

  it('reads in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    render(<RoadmapPage />)
    expect(await screen.findByText(STRINGS.ar['rm.note'])).toBeInTheDocument()
    expect(screen.getByText(STRINGS.ar['rm.step'].replace('{n}', '1'))).toBeInTheDocument()
  })
})
