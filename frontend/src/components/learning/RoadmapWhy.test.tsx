import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { PathRoadmap } from '@/components/learning/PathRoadmap'
import { YourMasarCard } from '@/components/learning/YourMasarCard'
import { useLanguageStore } from '@/lib/language'
import { path, pathCourse, profile, stage, step, why } from '@/test/fixtures'

vi.mock('@/lib/api', () => ({ api: { getMyLearningProfile: vi.fn(), getMyLearningPath: vi.fn() } }))
import { api } from '@/lib/api'

const RAG = { id: 1, slug: 'rag-knowledge-systems', title: 'RAG & Knowledge Systems' }

function roadmapWith(...courses: ReturnType<typeof pathCourse>[]) {
  return path({ stages: [stage({ slug: 'rag', status: 'current', courses })], current_stage_slug: 'rag' })
}

describe('the roadmap — "Why this course?" on each course', () => {
  it('offers the explanation, collapsed, on a course that is still to do', () => {
    render(<PathRoadmap path={roadmapWith(pathCourse({ course: RAG, why: why() }))} />)
    expect(screen.getByRole('button', { name: /Why this course\?/ })).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByText("You're working toward:")).toBeNull()
  })

  it('opens to the backend\'s facts for that course only', async () => {
    render(<PathRoadmap path={roadmapWith(
      pathCourse({ course: RAG, why: why() }),
      pathCourse({ course: { id: 2, slug: 'advanced-rag', title: 'Advanced RAG' }, why: why({ reasons: ['prerequisite'], known_skills: [], skills_to_gain: [], taught_count: 0, known_count: 0, to_gain_count: 0 }) }),
    )} />)
    const first = screen.getByText('RAG & Knowledge Systems').closest('li') as HTMLElement
    await userEvent.click(within(first).getByRole('button', { name: /Why this course\?/ }))
    expect(within(first).getByText('You still need 3 of the 4 skills it teaches.')).toBeInTheDocument()
    const second = screen.getByText('Advanced RAG').closest('li') as HTMLElement
    expect(within(second).queryByText(/You still need/)).toBeNull()
  })

  it('does not explain a finished course or one the learner already knows', () => {
    render(<PathRoadmap path={roadmapWith(
      pathCourse({ course: RAG, state: 'completed', why: why() }),
      pathCourse({ course: { id: 2, slug: 'advanced-rag', title: 'Advanced RAG' }, state: 'waived', reason: 'known_skills', why: why() }),
    )} />)
    expect(screen.queryByRole('button', { name: /Why this course\?/ })).toBeNull()
  })

  it('explains an optional course too — why it is there even though it is below the level', () => {
    render(<PathRoadmap path={roadmapWith(pathCourse({ course: RAG, state: 'optional', reason: 'below_level', why: why() }))} />)
    expect(screen.getByRole('button', { name: /Why this course\?/ })).toBeInTheDocument()
  })

  it('shows nothing for a course the server sent no explanation for, rather than making one up', () => {
    render(<PathRoadmap path={roadmapWith(pathCourse({ course: RAG }))} />)
    expect(screen.queryByRole('button', { name: /Why this course\?/ })).toBeNull()
  })

  it('keeps the status beside the title and the explanation inside the same row', async () => {
    render(<PathRoadmap path={roadmapWith(pathCourse({ course: RAG, why: why() }))} />)
    await userEvent.click(screen.getByRole('button', { name: /Why this course\?/ }))
    const row = screen.getByText('RAG & Knowledge Systems').closest('li') as HTMLElement
    expect(within(row).getByText('Upcoming')).toBeInTheDocument()
    expect(within(row).getByRole('region', { name: 'Why this course?' })).toBeInTheDocument()
    // the panel widens past the icon column on a phone
    expect(within(row).getByRole('region')).toHaveClass('max-sm:-ms-7')
  })

  it('opens each course\'s explanation on its own', async () => {
    render(<PathRoadmap path={roadmapWith(
      pathCourse({ course: RAG, why: why() }),
      pathCourse({ course: { id: 2, slug: 'advanced-rag', title: 'Advanced RAG' }, why: why() }),
    )} />)
    const toggles = screen.getAllByRole('button', { name: /Why this course\?/ })
    await userEvent.click(toggles[1])
    expect(toggles[0]).toHaveAttribute('aria-expanded', 'false')
    expect(toggles[1]).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getAllByRole('region', { name: 'Why this course?' })).toHaveLength(1)
  })

  it('reads in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<PathRoadmap path={roadmapWith(pathCourse({ course: RAG, why: why() }))} />)
    await userEvent.click(screen.getByRole('button', { name: /لماذا هذه الدورة؟/ }))
    expect(screen.getByText('ما زلت تحتاج 3 من أصل 4 مهارات تدرّسها.')).toBeInTheDocument()
  })
})

describe('the roadmap card — skills to gain and why', () => {
  beforeEach(() => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile())
    vi.mocked(api.getMyLearningPath).mockResolvedValue(path({ current_course: step({ why: why() }) }))
  })

  it('dashboard: says how many skills the current course would add and leaves the explanation to the roadmap', async () => {
    render(<YourMasarCard />)
    expect(await screen.findByText('3 skills to gain')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Continue Learning/ })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'View Full Roadmap' })).toHaveAttribute('href', '/learn')
    expect(screen.queryByRole('button', { name: /Why this course\?/ })).toBeNull()
  })

  it('dashboard: is a summary — no explanation and no skill names on the card', async () => {
    render(<YourMasarCard />)
    await screen.findByText('3 skills to gain')
    expect(screen.queryByRole('region', { name: 'Why this course?' })).toBeNull()
    expect(screen.queryByText('Vector Databases')).toBeNull()
  })

  it('home: shows the number but not the full explanation', async () => {
    render(<YourMasarCard variant="home" />)
    expect(await screen.findByText('3 skills to gain')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Why this course\?/ })).toBeNull()
    expect(screen.getByRole('link', { name: /Continue Roadmap/ })).toHaveAttribute('href', '/learn')
  })

  it('uses the singular for one skill and says so when there is nothing to gain', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(path({ current_course: step({ why: why({ to_gain_count: 1 }) }) }))
    const { unmount } = render(<YourMasarCard />)
    expect(await screen.findByText('1 skill to gain')).toBeInTheDocument()
    unmount()
    vi.mocked(api.getMyLearningPath).mockResolvedValue(path({ current_course: step({ why: why({ to_gain_count: 0 }) }) }))
    render(<YourMasarCard />)
    expect(await screen.findByText('You already know every skill it teaches')).toBeInTheDocument()
  })

  it('shows neither when the server sent no explanation, or when the roadmap is finished', async () => {
    vi.mocked(api.getMyLearningPath).mockResolvedValue(path({ current_course: step(), next_course: null }))
    const { unmount } = render(<YourMasarCard />)
    await screen.findByRole('link', { name: /Continue Learning/ })
    expect(screen.queryByText(/skills? to gain/)).toBeNull()
    unmount()
    vi.mocked(api.getMyLearningPath).mockResolvedValue(path({ current_course: null, next_course: null, is_complete: true }))
    render(<YourMasarCard />)
    await screen.findByText(/finished every required course/)
    expect(screen.queryByRole('button', { name: /Why this course\?/ })).toBeNull()
  })

  it('reads in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<YourMasarCard />)
    expect(await screen.findByText('3 مهارات ستكتسبها')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /لماذا هذه الدورة؟/ })).toBeNull()
  })
})
