import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { api, mentorV2 } from '@/lib/api'
import { useLanguageStore } from '@/lib/language'
import { MentorChat } from './MentorChat'
import { mockControl, mockProactive, resetMentorMock } from './mock'
import { clearThread } from './threadStore'

vi.mock('@/components/layout/Logo', () => ({ LogoMark: () => null }))

const BASE = {
  courseId: 'langgraph-agent-memory',
  courseTitle: 'LangGraph Agent Memory',
  lessonId: '1007',
  lessonNumber: 7,
  lessonTitle: 'Checkpointers',
  exerciseId: '9007',
  exerciseTitle: 'agent.py',
}

async function open() {
  vi.spyOn(api, 'getMentorSessions').mockResolvedValue([])
  await act(async () => { render(<MentorChat base={BASE} />) })
  await screen.findByText('What the mentor knows about you')
  return userEvent.setup()
}

// The composer is the only textarea (a quick-check answer is an input).
const box = () => document.querySelector('textarea') as HTMLTextAreaElement

beforeEach(() => {
  resetMentorMock()
  clearThread()
  // The hub opens with one free proactive card a day; most tests are about replies, so it is spent first.
  mockControl.now = () => 0
  mockProactive('en')
})
afterEach(() => {
  vi.restoreAllMocks()
  window.history.replaceState({}, '', '/mentor')
})

describe('MentorChat context', () => {
  it('sends the lesson and the code ids with every message', async () => {
    const send = vi.spyOn(mentorV2, 'sendMessage')
    const user = await open()
    await user.type(box(), 'what is a checkpointer?')
    await user.keyboard('{Enter}')
    await waitFor(() => expect(send).toHaveBeenCalled())
    expect(send.mock.calls[0][0].context).toEqual({ courseId: 'langgraph-agent-memory', lessonId: '1007', exerciseId: '9007', attachCode: true })
  })

  it('answers in general, with no pill, when both chips are removed', async () => {
    const send = vi.spyOn(mentorV2, 'sendMessage')
    const user = await open()
    await user.click(screen.getByRole('button', { name: /^Remove LangGraph/ }))
    await user.click(screen.getByRole('button', { name: /^Remove agent\.py/ }))
    expect(screen.getByText(/Nothing\. The mentor will answer in general/)).toBeInTheDocument()
    await user.type(box(), 'what is a checkpointer?')
    await user.keyboard('{Enter}')
    await waitFor(() => expect(send).toHaveBeenCalled())
    expect(send.mock.calls[0][0].context).toEqual({})
    await screen.findByText(/A general answer, not tied to a lesson/)
    expect(document.querySelector('[data-grounding]')).toBeNull()
  })

  it('cites the lesson on an answer that has one', async () => {
    const user = await open()
    await user.type(box(), 'what is a checkpointer?')
    await user.keyboard('{Enter}')
    expect(await screen.findByText('From this lesson')).toBeInTheDocument()
  })
})

describe('MentorChat actions', () => {
  it('sends the chosen action as the intent, overriding what the words say', async () => {
    const send = vi.spyOn(mentorV2, 'sendMessage')
    const user = await open()
    await user.click(screen.getByRole('button', { name: 'Simplify' }))
    expect(screen.getByRole('button', { name: 'Simplify' })).toHaveAttribute('aria-pressed', 'true')
    // The placeholder follows the mode.
    expect(screen.getByPlaceholderText('Which part did you not understand?')).toBeInTheDocument()
    // "why" would be read as WHY on its own.
    await user.type(screen.getByPlaceholderText('Which part did you not understand?'), 'why do I need a thread id')
    await user.keyboard('{Enter}')
    await waitFor(() => expect(send).toHaveBeenCalled())
    expect(send.mock.calls[0][0].intent).toBe('SIMPLIFY')
    expect((await screen.findAllByText('SIMPLIFY')).length).toBeGreaterThan(0)
    // A chosen action applies to one message.
    expect(screen.getByRole('button', { name: 'Simplify' })).toHaveAttribute('aria-pressed', 'false')
  })

  it('guesses the intent from the words only when no action is chosen', async () => {
    const send = vi.spyOn(mentorV2, 'sendMessage')
    const user = await open()
    await user.type(box(), 'why do I need a thread id')
    await user.keyboard('{Enter}')
    await waitFor(() => expect(send).toHaveBeenCalled())
    expect(send.mock.calls[0][0].intent).toBeUndefined()
    expect((await screen.findAllByText('WHY')).length).toBeGreaterThan(0)
  })

  it('a hint on the exercise starts the ladder at level 1 and never at the solution', async () => {
    const hint = vi.spyOn(mentorV2, 'hint')
    const user = await open()
    await user.click(screen.getByRole('button', { name: 'Hint' }))
    await user.click(screen.getByRole('button', { name: 'Send' }))
    expect(await screen.findByTestId('hint-ladder')).toBeInTheDocument()
    expect(hint).toHaveBeenCalledTimes(1)
    // The ladder starts at level 1 for the attached exercise (with the request id and any draft).
    expect(hint.mock.calls[0][0]).toMatchObject({ exerciseId: '9007', level: 1 })
    expect(hint.mock.calls[0][0].level).not.toBe(4)
  })

  it('lets quiz, hint and review go with nothing typed, but not a plain message', async () => {
    const user = await open()
    expect(screen.getByRole('button', { name: 'Send' })).toBeDisabled()
    await user.click(screen.getByRole('button', { name: 'Quiz me' }))
    expect(screen.getByRole('button', { name: 'Send' })).toBeEnabled()
    await user.click(screen.getByRole('button', { name: 'Quiz me' }))
    await user.click(screen.getByRole('button', { name: 'Explain' }))
    expect(screen.getByRole('button', { name: 'Send' })).toBeDisabled()
  })
})

describe('MentorChat credits', () => {
  it('shows the out-of-credits bar for the credits=0 mock state', async () => {
    window.history.replaceState({}, '', '/mentor?credits=0')
    await open()
    expect(await screen.findByTestId('mentor-upsell')).toHaveTextContent('You are out of credits')
    expect(screen.queryByRole('button', { name: 'Send' })).toBeNull()
  })

  it('shows the cost the server charged, and a quick quiz as free', async () => {
    const user = await open()
    await user.type(box(), 'what is a checkpointer?')
    await user.keyboard('{Enter}')
    expect(await screen.findByText('-2 credits')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Quiz me' }))
    await user.click(screen.getByRole('button', { name: 'Send' }))
    expect(await screen.findByTestId('quiz-block')).toBeInTheDocument()
    const costs = screen.getAllByTestId('message-cost').map((c) => c.textContent)
    expect(costs).toEqual(['-2 credits', 'No credits'])
  })

  it('states the price and that automatic messages and quick quizzes are free', async () => {
    await open()
    expect(screen.getByText('2 credits per message · automatic mentor messages and quick quizzes are free')).toBeInTheDocument()
  })

  it('says nothing was charged when the reply fails, and retries without sending the words twice', async () => {
    const user = await open()
    mockControl.failNext = true
    await user.type(box(), 'what is a checkpointer?')
    await user.keyboard('{Enter}')
    // The server's 503 (provider down, credits refunded) reads as such - not as a generic failure.
    expect(await screen.findByRole('alert')).toHaveTextContent('The mentor is unavailable right now. Any credits used were refunded.')
    expect(document.querySelectorAll('[data-role="learner"]')).toHaveLength(1)
    await user.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByText('From this lesson')).toBeInTheDocument()
    expect(screen.queryByRole('alert')).toBeNull()
    expect(document.querySelectorAll('[data-role="learner"]')).toHaveLength(1)
  })
})

describe('MentorChat proactive card', () => {
  it('opens with a free card, once, and its answers do not count as spending', async () => {
    resetMentorMock()
    clearThread()
    mockControl.now = () => 10 * 24 * 3600 * 1000
    await open()
    const card = await screen.findByTestId('proactive-card')
    expect(within(card).getByText('No credits')).toBeInTheDocument()
    expect(within(card).getByText(/PROACTIVE · QUIZ/)).toBeInTheDocument()
    expect(within(card).getByText('You just finished a lesson')).toBeInTheDocument()
    // A proactive card has no cost line of its own.
    expect(within(card).queryByTestId('message-cost')).toBeNull()
  })

  it('answering the quiz refetches what the mentor knows', async () => {
    resetMentorMock()
    clearThread()
    mockControl.now = () => 20 * 24 * 3600 * 1000
    const learner = vi.spyOn(mentorV2, 'learner')
    const user = await open()
    const card = await screen.findByTestId('proactive-card')
    const before = learner.mock.calls.length
    await user.click(within(card).getByRole('radio', { name: /thread_id/ }))
    await waitFor(() => expect(learner.mock.calls.length).toBeGreaterThan(before))
    expect(await screen.findByText('0.66')).toBeInTheDocument()
  })
})

describe('MentorChat in Arabic', () => {
  it('speaks the brief’s copy', async () => {
    useLanguageStore.setState({ language: 'ar' })
    vi.spyOn(api, 'getMentorSessions').mockResolvedValue([])
    await act(async () => { render(<MentorChat base={BASE} />) })
    expect(await screen.findByText('يرى المرشد:')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'اشرح' })).toBeInTheDocument()
    expect(screen.getByText('رصيدان لكل رسالة · رسائل المرشد التلقائية والاختبارات السريعة مجانية')).toBeInTheDocument()
  })
})
