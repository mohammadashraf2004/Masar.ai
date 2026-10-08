import { createRef } from 'react'
import { act, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { mentorV2 } from '@/lib/api'
import { resetMentorMock, mockControl } from '@/features/mentor/mock'
import { clearThread, loadThread, scopeOf } from '@/features/mentor/threadStore'
import { LessonMentorLayer } from './LessonMentorLayer'
import { MentorQuizNote } from './MentorQuizNote'

vi.mock('@/components/layout/Logo', () => ({ LogoMark: () => null }))

function Lesson() {
  const ref = createRef<HTMLElement>()
  return (
    <div>
      <article ref={ref}>
        <p id="p">A Checkpointer captures a snapshot of the graph state after every node.</p>
      </article>
      <LessonMentorLayer articleRef={ref} courseId="langgraph-agent-memory" lessonId="1007" lessonNumber={7} />
    </div>
  )
}

function select() {
  act(() => {
    window.getSelection()!.selectAllChildren(document.getElementById('p')!)
    document.dispatchEvent(new Event('selectionchange'))
  })
}

beforeEach(() => { resetMentorMock(); clearThread() })
afterEach(() => { vi.restoreAllMocks(); window.getSelection()?.removeAllRanges() })

describe('the mentor inside a lesson', () => {
  it('sends the lesson ids and the selected text, and no exercise or code', async () => {
    const send = vi.spyOn(mentorV2, 'sendMessage')
    render(<Lesson />)
    select()
    await userEvent.click(screen.getByRole('button', { name: 'Explain this' }))
    const panel = await screen.findByTestId('lesson-mentor-panel')
    await within(panel).findByText('From this lesson')
    expect(send).toHaveBeenCalledTimes(1)
    const body = send.mock.calls[0][0]
    expect(body.intent).toBe('EXPLAIN')
    expect(body.context).toEqual({
      courseId: 'langgraph-agent-memory',
      lessonId: '1007',
      selectedText: 'A Checkpointer captures a snapshot of the graph state after every node.',
    })
  })

  it('quotes the selection, shows the intent and the grounding, and the lesson number', async () => {
    render(<Lesson />)
    select()
    await userEvent.click(screen.getByRole('button', { name: 'Simplify' }))
    const panel = await screen.findByTestId('lesson-mentor-panel')
    expect(within(panel).getByText('Lesson 7')).toBeInTheDocument()
    expect(within(panel).getByRole('blockquote', { name: 'Selected text' })).toHaveTextContent('A Checkpointer captures a snapshot')
    expect(await within(panel).findByText('SIMPLIFY')).toBeInTheDocument()
    expect(within(panel).getByText('From this lesson')).toBeInTheDocument()
    // The simplifying answer ends with a quick-check question.
    expect(within(panel).getByText('Quick check')).toBeInTheDocument()
  })

  it('keeps the exchange in the thread the hub chat reads', async () => {
    render(<Lesson />)
    select()
    await userEvent.click(screen.getByRole('button', { name: 'Why does it matter?' }))
    await screen.findByText('From this lesson')
    // The lesson's own thread: the hub shows it for this lesson, and never under another one.
    const thread = loadThread(scopeOf({ lessonId: '1007' }))
    expect(thread.map((m) => m.role)).toEqual(['learner', 'mentor'])
    expect(loadThread(scopeOf({ lessonId: '1008' }))).toEqual([])
    expect(loadThread()).toEqual([])
    expect(JSON.stringify(thread[0].blocks)).toContain('A Checkpointer captures a snapshot')
  })

  it('answers a quick check as a follow-up, still with no selection', async () => {
    const send = vi.spyOn(mentorV2, 'sendMessage')
    render(<Lesson />)
    select()
    await userEvent.click(screen.getByRole('button', { name: 'Simplify' }))
    const panel = await screen.findByTestId('lesson-mentor-panel')
    await userEvent.type(await within(panel).findByPlaceholderText('Write your answer…'), 'it forgets everything')
    await userEvent.click(within(panel).getByRole('button', { name: 'Send answer' }))
    await act(async () => {})
    expect(send).toHaveBeenCalledTimes(2)
    expect(send.mock.calls[1][0].context).toEqual({ courseId: 'langgraph-agent-memory', lessonId: '1007' })
  })

  it('says the provider failed and the charge was refunded, and retries the same question', async () => {
    const send = vi.spyOn(mentorV2, 'sendMessage')
    render(<Lesson />)
    select()
    mockControl.failNext = true
    await userEvent.click(screen.getByRole('button', { name: 'Explain this' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Any credits used were refunded')
    await userEvent.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByText('From this lesson')).toBeInTheDocument()
    expect(send).toHaveBeenCalledTimes(2)
    expect(send.mock.calls[1][0].context.selectedText).toContain('A Checkpointer')
  })

  it('closes with its button and is not there before a question is asked', async () => {
    render(<Lesson />)
    expect(screen.queryByTestId('lesson-mentor-panel')).toBeNull()
    select()
    await userEvent.click(screen.getByRole('button', { name: 'Explain this' }))
    await screen.findByTestId('lesson-mentor-panel')
    await userEvent.click(screen.getByRole('button', { name: 'Close the mentor' }))
    expect(screen.queryByTestId('lesson-mentor-panel')).toBeNull()
  })

  it('reports its open state so a wide lesson can reserve side-panel space', async () => {
    const onOpenChange = vi.fn()
    const ref = createRef<HTMLElement>()
    render(<div><article ref={ref}><p id="p">Selected lesson text.</p></article><LessonMentorLayer articleRef={ref} courseId="course" lessonId="1007" lessonNumber={7} onOpenChange={onOpenChange} /></div>)
    expect(onOpenChange).toHaveBeenLastCalledWith(false)
    select()
    await userEvent.click(screen.getByRole('button', { name: 'Explain this' }))
    await screen.findByTestId('lesson-mentor-panel')
    expect(onOpenChange).toHaveBeenLastCalledWith(true)
    await userEvent.click(screen.getByRole('button', { name: 'Close the mentor' }))
    expect(onOpenChange).toHaveBeenLastCalledWith(false)
  })
})

describe('a wrong quiz answer in a lesson', () => {
  it('gets the mentor’s guiding question, free, and never the right option', async () => {
    render(<MentorQuizNote quizId="quiz-checkpointer-1" optionId="b" />)
    const note = await screen.findByTestId('mentor-quiz-note')
    expect(note).toHaveTextContent('Close.')
    expect(note).toHaveTextContent('Mentor · no credits')
    expect(note).not.toHaveTextContent('thread_id inside config')
  })

  it('says nothing for a right answer', async () => {
    render(<MentorQuizNote quizId="quiz-checkpointer-1" optionId="a" />)
    await act(async () => {})
    expect(screen.queryByTestId('mentor-quiz-note')).toBeNull()
  })
})
