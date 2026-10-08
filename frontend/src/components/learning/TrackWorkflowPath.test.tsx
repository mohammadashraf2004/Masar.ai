import { render, screen, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { TrackWorkflowPath } from '@/components/learning/TrackWorkflowPath'
import { api } from '@/lib/api'
import type { TrackWorkflow, TrackWorkflowCourse } from '@/types'

vi.mock('@/lib/api', () => ({ api: { getTrackWorkflow: vi.fn() } }))

function wcourse(overrides: Partial<TrackWorkflowCourse> = {}): TrackWorkflowCourse {
  return {
    course_id: 1, slug: 'course-001', title: 'Machine Learning Foundations', title_ar: null,
    order: 1, role: 'core', required: true, section: null, status: 'available',
    progress_percent: 0, is_available: true, estimated_hours: 10, module_count: 5, lesson_count: 40,
    prerequisites: [],
    ...overrides,
  }
}

function workflow(overrides: Partial<TrackWorkflow> = {}): TrackWorkflow {
  const courses = overrides.courses ?? [wcourse()]
  return {
    career_goal: { slug: 'ml-engineer', title: 'ML Engineer' },
    courses,
    required_total: courses.filter((c) => c.required).length,
    required_completed: courses.filter((c) => c.status === 'completed').length,
    progress_percent: 0,
    current: null,
    next: null,
    has_sections: false,
    ...overrides,
  }
}

describe('TrackWorkflowPath — backend-driven career track workflow', () => {
  beforeEach(() => vi.clearAllMocks())

  it('renders the workflow in the server-given order, never re-sorted on the client', async () => {
    vi.mocked(api.getTrackWorkflow).mockResolvedValue(workflow({
      courses: [
        wcourse({ course_id: 1, slug: 'course-013', title: 'Applied Data Analysis with Python', order: 1 }),
        wcourse({ course_id: 2, slug: 'course-001', title: 'Machine Learning Foundations', order: 2, role: 'supporting', required: false }),
      ],
    }))
    render(<TrackWorkflowPath goal="data-analyst" />)

    const titles = await screen.findAllByRole('heading', { level: 5 })
    expect(titles.map((h) => h.textContent)).toEqual([
      'Applied Data Analysis with Python', 'Machine Learning Foundations',
    ])
    expect(api.getTrackWorkflow).toHaveBeenCalledWith('data-analyst')
  })

  it('shows a completed course as completed, with a Review CTA', async () => {
    vi.mocked(api.getTrackWorkflow).mockResolvedValue(workflow({
      courses: [wcourse({ status: 'completed', progress_percent: 100 })],
    }))
    render(<TrackWorkflowPath goal="ml-engineer" />)

    const card = (await screen.findByText('Machine Learning Foundations')).closest('[data-course-id]') as HTMLElement
    expect(card).toHaveAttribute('data-workflow-status', 'completed')
    expect(within(card).getByText('Completed')).toBeInTheDocument()
    expect(within(card).getByRole('link', { name: 'Review' })).toBeInTheDocument()
  })

  it('shows an in-progress course with its progress percentage and a Continue CTA', async () => {
    vi.mocked(api.getTrackWorkflow).mockResolvedValue(workflow({
      courses: [wcourse({ status: 'in_progress', progress_percent: 42 })],
    }))
    render(<TrackWorkflowPath goal="ml-engineer" />)

    const card = (await screen.findByText('Machine Learning Foundations')).closest('[data-course-id]') as HTMLElement
    expect(within(card).getByText('In progress')).toBeInTheDocument()
    expect(within(card).getByText('42%')).toBeInTheDocument()
    expect(within(card).getByRole('link', { name: 'Continue' })).toBeInTheDocument()
  })

  it('marks the first reachable, not-started course as next, with a Start CTA', async () => {
    vi.mocked(api.getTrackWorkflow).mockResolvedValue(workflow({
      courses: [wcourse({ status: 'next' })],
      next: { id: 1, slug: 'course-001', title: 'Machine Learning Foundations' },
    }))
    render(<TrackWorkflowPath goal="ml-engineer" />)

    const card = (await screen.findByText('Machine Learning Foundations')).closest('[data-course-id]') as HTMLElement
    expect(within(card).getByText('Next up')).toBeInTheDocument()
    expect(within(card).getByRole('link', { name: 'Start' })).toBeInTheDocument()
    expect(await screen.findByText('Next: Machine Learning Foundations')).toBeInTheDocument()
  })

  it('shows a locked course with its unmet prerequisite and a disabled Locked CTA', async () => {
    vi.mocked(api.getTrackWorkflow).mockResolvedValue(workflow({
      courses: [wcourse({
        status: 'locked',
        prerequisites: [{ id: 9, slug: 'course-002', title: 'Deep Learning Foundations' }],
      })],
    }))
    render(<TrackWorkflowPath goal="ml-engineer" />)

    const card = (await screen.findByText('Machine Learning Foundations')).closest('[data-course-id]') as HTMLElement
    expect(card).toHaveAttribute('data-workflow-status', 'locked')
    expect(within(card).getAllByText('Locked')).toHaveLength(2) // the status badge and the disabled CTA
    expect(within(card).getByText('Requires: Deep Learning Foundations')).toBeInTheDocument()
    expect(within(card).getByText('Locked', { selector: '[aria-disabled="true"]' })).toBeInTheDocument()
    expect(within(card).queryByRole('link', { name: 'Locked' })).not.toBeInTheDocument()
  })

  it('badges an optional course as Optional without blocking it', async () => {
    vi.mocked(api.getTrackWorkflow).mockResolvedValue(workflow({
      courses: [wcourse({ role: 'optional', required: false, status: 'available' })],
    }))
    render(<TrackWorkflowPath goal="ml-engineer" />)

    const card = (await screen.findByText('Machine Learning Foundations')).closest('[data-course-id]') as HTMLElement
    expect(within(card).getByText('Optional')).toBeInTheDocument()
    expect(within(card).queryByText('Locked')).not.toBeInTheDocument()
  })

  it('badges core/supporting/optional roles distinctly', async () => {
    vi.mocked(api.getTrackWorkflow).mockResolvedValue(workflow({
      courses: [
        wcourse({ course_id: 1, slug: 'course-001', title: 'Course One', role: 'core' }),
        wcourse({ course_id: 2, slug: 'course-002', title: 'Course Two', role: 'supporting' }),
        wcourse({ course_id: 3, slug: 'course-003', title: 'Course Three', role: 'optional', required: false }),
      ],
    }))
    render(<TrackWorkflowPath goal="ml-engineer" />)

    expect((await screen.findByText('Course One')).closest('[data-course-id]')).toHaveAttribute('data-workflow-role', 'core')
    expect(screen.getByText('Course Two').closest('[data-course-id]')).toHaveAttribute('data-workflow-role', 'supporting')
    expect(screen.getByText('Course Three').closest('[data-course-id]')).toHaveAttribute('data-workflow-role', 'optional')
  })

  it('shows compact duration, module, and lesson metadata supplied by the backend', async () => {
    vi.mocked(api.getTrackWorkflow).mockResolvedValue(workflow())
    render(<TrackWorkflowPath goal="ml-engineer" />)

    const card = (await screen.findByText('Machine Learning Foundations')).closest('[data-course-id]') as HTMLElement
    expect(within(card).getByText('10 hours · 40 lessons · 5 modules')).toBeInTheDocument()
  })

  it('shows required-only progress in the header, computed by the server', async () => {
    vi.mocked(api.getTrackWorkflow).mockResolvedValue(workflow({
      required_total: 7, required_completed: 4, progress_percent: 57,
    }))
    render(<TrackWorkflowPath goal="ml-engineer" />)

    expect(await screen.findByText('4 of 7 required courses completed · 57% path progress')).toBeInTheDocument()
  })

  it('renders AI Engineer as named sections, in server order', async () => {
    vi.mocked(api.getTrackWorkflow).mockResolvedValue(workflow({
      has_sections: true,
      courses: [
        wcourse({ course_id: 1, slug: 'course-001', title: 'Foundations Course', section: 'foundations', order: 1 }),
        wcourse({ course_id: 2, slug: 'course-008', title: 'Specialization Course', section: 'specializations', order: 14, role: 'optional', required: false }),
      ],
    }))
    render(<TrackWorkflowPath goal="ai-engineer" />)

    const headings = await screen.findAllByRole('heading', { level: 4 })
    expect(headings.map((h) => h.textContent)).toEqual([
      'Foundations', 'Specializations (optional)',
    ])
  })

  it('shows the same shared course as completed consistently, driven by the server response', async () => {
    vi.mocked(api.getTrackWorkflow).mockImplementation(async (goal) => workflow({
      career_goal: { slug: goal, title: goal },
      courses: [wcourse({ slug: 'course-013', title: 'Applied Data Analysis with Python', status: 'completed' })],
    }))

    const { rerender } = render(<TrackWorkflowPath goal="data-analyst" />)
    expect((await screen.findByText('Applied Data Analysis with Python')).closest('[data-course-id]'))
      .toHaveAttribute('data-workflow-status', 'completed')

    rerender(<TrackWorkflowPath goal="ml-engineer" />)
    expect((await screen.findByText('Applied Data Analysis with Python')).closest('[data-course-id]'))
      .toHaveAttribute('data-workflow-status', 'completed')
  })
})
