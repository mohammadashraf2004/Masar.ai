import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { api, mentorV2 } from '@/lib/api'
import { CodeReview, exerciseCode } from './CodeReview'
import { mockReview, resetMentorMock } from './mock'

beforeEach(() => {
  resetMentorMock()
  window.localStorage.clear()
  vi.spyOn(api, 'getCodeExercise').mockResolvedValue({
    id: 9007,
    title: 'Agent memory',
    language: 'python',
    starter_code: 'from langgraph.checkpoint.memory import MemorySaver\n\ngraph = builder.compile()\n\ndef run(message: str, thread_id: str):\n    return graph.invoke({"messages": [message]})\n',
  })
  vi.spyOn(mentorV2, 'review').mockImplementation(mockReview as typeof mentorV2.review)
})

async function requestReview() {
  const button = await screen.findByRole('button', { name: 'Ask for a review' })
  await waitFor(() => expect(button).toBeEnabled())
  await userEvent.click(button)
}

describe('CodeReview', () => {
  it('reads the exercise the learner has and says it was read, never run', async () => {
    render(<CodeReview exerciseId="9007" />)
    await requestReview()
    expect(await screen.findByRole('button', { name: /L3: compile without a checkpointer/ })).toBeInTheDocument()
    expect(screen.getByText('static read · not executed')).toBeInTheDocument()
    expect(screen.queryByText(/executed successfully|ran successfully|output:/i)).toBeNull()
    // The code panel keeps its dark surface and left-to-right direction whatever the page language is.
    expect(screen.getByLabelText('agent.py')).toHaveAttribute('dir', 'ltr')
  })

  it('uses the learner’s saved draft, not just the starter', async () => {
    window.localStorage.setItem('exercise:anon:9007:agent.py', 'graph = builder.compile(checkpointer=MemorySaver())\n')
    expect(exerciseCode('9007')).toContain('checkpointer=MemorySaver()')
    render(<CodeReview exerciseId="9007" />)
    await requestReview()
    await screen.findByText('Review notes')
    expect(screen.queryByRole('button', { name: /compile without a checkpointer/ })).toBeNull()
  })

  it('retries the same code under the same request id, and names every new review afresh', async () => {
    vi.mocked(mentorV2.review)
      .mockRejectedValueOnce(new Error('timeout of 30000ms exceeded'))
      .mockImplementation(mockReview as typeof mentorV2.review)
    render(<CodeReview exerciseId="9007" />)
    await requestReview()
    await screen.findByRole('alert')
    await requestReview()
    await screen.findByRole('button', { name: /L3: compile without a checkpointer/ })
    await userEvent.click(screen.getByRole('button', { name: 'One more hint' }))
    await waitFor(() => expect(mentorV2.review).toHaveBeenCalledTimes(3))

    const ids = vi.mocked(mentorV2.review).mock.calls.map((call) => call[0].requestId)
    expect(ids[0]).toMatch(/^rq-/)
    expect(ids[1]).toBe(ids[0])          // the timed-out review again: answered and charged once
    expect(ids[2]).not.toBe(ids[0])      // a deliberate new review after an answer
  })

  it('never reviews a draft another account left in this browser', async () => {
    const { useAuthStore } = await import('@/lib/store')
    const { exerciseDraftKey } = await import('@/features/exercises/draftKeys')
    useAuthStore.setState({ user: { id: 1 } as never })
    window.localStorage.setItem(exerciseDraftKey('9007', 'agent.py'),'account_a_secret = True\n')
    useAuthStore.setState({ user: { id: 2 } as never })
    try {
      render(<CodeReview exerciseId="9007" />)
      await requestReview()
      await waitFor(() => expect(mentorV2.review).toHaveBeenCalled())
      expect(vi.mocked(mentorV2.review).mock.calls[0][0].code).not.toContain('account_a_secret')
      expect(vi.mocked(mentorV2.review).mock.calls[0][0].code).toContain('graph = builder.compile()')
    } finally {
      useAuthStore.setState({ user: null })
    }
  })

  it('keeps a backend-fetched starter when asking for another hint', async () => {
    render(<CodeReview exerciseId="9007" />)
    await requestReview()
    await screen.findByRole('button', { name: /L3: compile without a checkpointer/ })

    await userEvent.click(screen.getByRole('button', { name: 'One more hint' }))
    await waitFor(() => expect(mentorV2.review).toHaveBeenCalledTimes(2))
    expect(vi.mocked(mentorV2.review).mock.calls[1][0].code).toContain('graph = builder.compile()')
  })

  it('opens the comment under a line when it is chosen, and the aside follows', async () => {
    render(<CodeReview exerciseId="9007" />)
    await requestReview()
    const line3 = await screen.findByRole('button', { name: /L3: compile without a checkpointer/ })
    // The first problem is open on arrival.
    expect(line3).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('note')).toHaveTextContent('The graph is built without memory')

    const asideRow = screen.getAllByRole('button').find((b) => b.textContent?.includes('thread_id never reaches invoke') && b.hasAttribute('aria-current') === false) as HTMLElement
    await userEvent.click(asideRow)
    expect(screen.getByRole('note')).toHaveTextContent('thread_id is a parameter but never goes into config')
    expect(screen.getByRole('button', { name: /L6: thread_id never reaches invoke/ })).toHaveAttribute('aria-expanded', 'true')
    expect(line3).toHaveAttribute('aria-expanded', 'false')
    expect(asideRow).toHaveAttribute('aria-current', 'true')
  })

  it('toggles a line’s comment closed when its line is chosen again', async () => {
    render(<CodeReview exerciseId="9007" />)
    await requestReview()
    const line3 = await screen.findByRole('button', { name: /L3:/ })
    await userEvent.click(line3)
    expect(screen.queryByRole('note')).toBeNull()
  })

  it('marks commented lines with a severity dot, and lines without a comment are not buttons', async () => {
    render(<CodeReview exerciseId="9007" />)
    await requestReview()
    await screen.findByRole('button', { name: /L3:/ })
    const dots = Array.from(document.querySelectorAll('[data-severity]')).map((d) => d.getAttribute('data-severity'))
    expect(dots).toEqual(['ok', 'issue', 'issue'])
    expect(screen.getAllByRole('button', { name: /^L\d+:/ })).toHaveLength(3)
  })

  it('shows debug steps, only the first unlocked, and unlocks another each time it looks again', async () => {
    render(<CodeReview exerciseId="9007" />)
    await requestReview()
    const card = await screen.findByTestId('debug-card')
    const unlocked = () => within(card).getAllByRole('listitem').filter((li) => li.getAttribute('data-unlocked') === 'true').length
    expect(unlocked()).toBe(1)
    await userEvent.click(within(card).getByRole('button', { name: 'One more hint' }))
    await screen.findByText('Review notes')
    expect(unlocked()).toBe(2)
  })

  it('reviews pasted code as a file of its own', async () => {
    render(<CodeReview exerciseId="9007" />)
    await screen.findByText('Review notes')
    await userEvent.click(screen.getByRole('button', { name: 'Paste another file' }))
    await userEvent.type(screen.getByLabelText('Paste the code to review'), 'graph = builder.compile()')
    await userEvent.click(screen.getByRole('button', { name: 'Review' }))
    expect(await screen.findByLabelText('pasted.py')).toBeInTheDocument()
    expect(await screen.findByRole('button', { name: /L1: compile without a checkpointer/ })).toBeInTheDocument()
  })
})
