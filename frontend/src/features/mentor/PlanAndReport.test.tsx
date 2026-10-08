import { act, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { mentorV2 } from '@/lib/api'
import { ApprovedPlanCard, upcomingDays } from './ApprovedPlanCard'
import { InterviewReport } from './InterviewReport'
import { StudyPlan, formatMinutes, weekStartOf } from './StudyPlan'
import { tabFromParams } from './MentorHub'
import { mockExtraBlocks, mockPlan, resetMentorMock } from './mock'

beforeEach(() => {
  resetMentorMock()
  window.localStorage.clear()
  vi.spyOn(mentorV2, 'plan').mockImplementation(mockPlan as typeof mentorV2.plan)
})

// Saturday 3 October 2026: the week the plan covers starts today.
const SATURDAY = new Date(2026, 9, 3, 12, 0, 0)

describe('StudyPlan', () => {
  it('starts the week on Saturday and formats time as hours and minutes', () => {
    expect(weekStartOf(SATURDAY)).toBe('2026-10-03')
    expect(weekStartOf(new Date(2026, 9, 7))).toBe('2026-10-03')
    expect(weekStartOf(new Date(2026, 9, 9))).toBe('2026-10-03')
    expect(weekStartOf(new Date(2026, 9, 10))).toBe('2026-10-10')
    expect(formatMinutes(225)).toBe('3h 45m')
  })

  it('shows the goal, the totals, a card per day, and why', async () => {
    render(<StudyPlan now={SATURDAY} />)
    expect(await screen.findByText(/Finish the LangGraph memory unit/)).toBeInTheDocument()
    expect(screen.getByTestId('plan-total')).toHaveTextContent('3h 20m')
    expect(screen.getByTestId('plan-days')).toHaveTextContent('6 / 7')
    expect(screen.getAllByTestId('plan-day')).toHaveLength(7)
    expect(screen.getByText('Why this plan?')).toBeInTheDocument()
    expect(screen.getAllByRole('listitem').some((li) => li.textContent?.includes('Retrieval evaluation needs review'))).toBe(true)
  })

  it('marks tomorrow with an accent border, and a rest day as dimmed', async () => {
    render(<StudyPlan now={SATURDAY} />)
    await screen.findByText('Why this plan?')
    const days = screen.getAllByTestId('plan-day')
    expect(days[1]).toHaveAttribute('data-tomorrow', 'true')
    expect(days[1].className).toContain('border-amber')
    expect(days[1]).toHaveTextContent('· tomorrow')
    expect(days[0]).not.toHaveAttribute('data-tomorrow')
    expect(days[6]).toHaveAttribute('data-rest', 'true')
    expect(days[6].className).toContain('opacity-70')
    expect(days[6]).toHaveTextContent('Rest')
  })

  it('links every block to what it refers to, and labels its kind', async () => {
    render(<StudyPlan now={SATURDAY} />)
    await screen.findByText('Why this plan?')
    const day = screen.getAllByTestId('plan-day')[0]
    const links = within(day).getAllByRole('link')
    expect(links.map((l) => l.getAttribute('href'))).toEqual(['/courses/langgraph-agent-memory/lessons/1008', '/courses/langgraph-agent-memory/lessons/1008'])
    expect(within(day).getByText('Lesson')).toBeInTheDocument()
    expect(within(day).getByText('Exercise')).toBeInTheDocument()
  })

  it('regenerates another arrangement, and approving it keeps it for Home', async () => {
    const user = userEvent.setup()
    render(<StudyPlan now={SATURDAY} />)
    await screen.findByText('Why this plan?')
    const firstBefore = within(screen.getAllByTestId('plan-day')[0]).getAllByRole('link')[0].textContent
    await user.click(screen.getByRole('button', { name: 'Regenerate' }))
    await screen.findByText('Why this plan?')
    await act(async () => {})
    const firstAfter = within(screen.getAllByTestId('plan-day')[0]).getAllByRole('link')[0].textContent
    expect(firstAfter).not.toBe(firstBefore)

    await user.click(screen.getByRole('button', { name: 'Approve the plan' }))
    expect(await screen.findByRole('button', { name: 'Plan approved' })).toBeDisabled()
  })

  it('shows the approved plan on Home, and nothing before one is approved', async () => {
    const { unmount } = render(<ApprovedPlanCard now={SATURDAY} />)
    await act(async () => {})
    expect(screen.queryByTestId('approved-plan')).toBeNull()
    unmount()

    const user = userEvent.setup()
    render(<StudyPlan now={SATURDAY} />)
    await screen.findByText('Why this plan?')
    await user.click(screen.getByRole('button', { name: 'Approve the plan' }))
    await screen.findByRole('button', { name: 'Plan approved' })

    render(<ApprovedPlanCard now={SATURDAY} />)
    const card = await screen.findByTestId('approved-plan')
    expect(card).toHaveTextContent('This week\'s plan')
    expect(within(card).getAllByRole('link').length).toBeGreaterThan(0)
  })

  it('picks the next days that have something to do', async () => {
    const plan = await mockPlan({ weekStart: '2026-10-03' }, 'en')
    expect(upcomingDays(plan, '2026-10-03').map((d) => d.date)).toEqual(['2026-10-03', '2026-10-04'])
    expect(upcomingDays(plan, '2026-10-09')).toEqual([])
  })
})

describe('InterviewReport', () => {
  it('shows the score out of 10 and the verdict', async () => {
    render(<InterviewReport id="x" />)
    expect(await screen.findByTestId('report-score')).toHaveTextContent('7.4')
    expect(screen.getByText('/10')).toBeInTheDocument()
    expect(screen.getByText('Nearly ready')).toBeInTheDocument()
  })

  it('opens one question at a time, quoting what was said and the note', async () => {
    const user = userEvent.setup()
    render(<InterviewReport id="x" />)
    const rows = await screen.findAllByRole('button', { expanded: false })
    const questions = rows.filter((r) => /Why do we split|How do you measure|When do you prefer/.test(r.textContent ?? ''))
    expect(questions).toHaveLength(3)

    await user.click(questions[1])
    expect(screen.getByText(/You said: "I try it myself/)).toBeInTheDocument()
    expect(screen.getByText(/missing metrics such as recall@k/)).toBeInTheDocument()

    await user.click(questions[2])
    expect(screen.queryByText(/I try it myself/)).toBeNull()
    expect(screen.getByText(/You said: "When a conversation has to survive/)).toBeInTheDocument()
    expect(screen.getAllByRole('button', { expanded: true })).toHaveLength(1)
  })

  it('colours a score green from 8 and amber below', async () => {
    render(<InterviewReport id="x" />)
    await screen.findByTestId('report-score')
    const fills = Array.from(document.querySelectorAll('.progress-fill')).map((f) => f.className.includes('bg-emerald'))
    expect(fills).toEqual([true, false, true])
  })

  it('lists strengths with filled dots, gaps with hollow rings, and lessons with their course code', async () => {
    render(<InterviewReport id="x" />)
    await screen.findByTestId('report-score')
    expect(document.querySelectorAll('li > span.bg-emerald').length).toBe(2)
    expect(document.querySelectorAll('li > span.border-amber').length).toBe(2)
    const lesson = screen.getByRole('link', { name: /Evaluating retrieval with Ragas/ })
    expect(lesson).toHaveTextContent('COURSE-009')
    expect(lesson.className).toContain('min-h-[44px]')
  })

  it('adds the recommended lessons to this week’s plan', async () => {
    const user = userEvent.setup()
    render(<InterviewReport id="x" />)
    await screen.findByTestId('report-score')
    await user.click(screen.getByRole('button', { name: 'Add it to this week\'s plan' }))
    expect(await screen.findByRole('button', { name: 'Added to the plan' })).toBeDisabled()
    expect(mockExtraBlocks().map((b) => b.title)).toEqual(['Evaluating retrieval with Ragas', 'Advanced chunking'])
    const plan = await mockPlan({ weekStart: '2026-10-03' }, 'en')
    expect(plan.days[1].blocks.map((b) => b.title)).toEqual(expect.arrayContaining(['Advanced chunking']))
  })
})

describe('tabs', () => {
  const params = (q: string) => new URLSearchParams(q)
  it('reads ?tab=, and keeps the old ?mode=interview link working', () => {
    expect(tabFromParams(params(''))).toBe('chat')
    expect(tabFromParams(params('tab=review'))).toBe('review')
    expect(tabFromParams(params('tab=plan'))).toBe('plan')
    expect(tabFromParams(params('tab=interview'))).toBe('interview')
    expect(tabFromParams(params('mode=interview'))).toBe('interview')
    expect(tabFromParams(params('tab=nonsense'))).toBe('chat')
    expect(tabFromParams(params('tab=review&mode=interview'))).toBe('review')
  })
})
