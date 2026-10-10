import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { mentorV2 } from '@/lib/api'
import { useLanguageStore } from '@/lib/language'
import { MentorBlocks } from './MentorMessageView'
import { QuizBlock } from './QuizBlock'
import { resetMentorMock } from './mock'
import type { MentorBlock } from './types'

type Quiz = Extract<MentorBlock, { kind: 'quiz' }>
const quiz: Quiz = {
  kind: 'quiz',
  grounding: 'lesson',
  quizId: 'quiz-checkpointer-1',
  question: 'What makes the agent resume the same conversation?',
  options: [
    { id: 'a', text: 'Passing a stable thread_id inside config' },
    { id: 'b', text: 'Building a new graph on every call' },
    { id: 'c', text: 'Raising the temperature' },
  ],
}

const view = (onResult = vi.fn()) =>
  render(<QuizBlock block={quiz} onResult={onResult} renderFeedback={(blocks) => <MentorBlocks blocks={blocks} />} />)

beforeEach(() => {
  resetMentorMock()
  useLanguageStore.setState({ language: 'en' })
})
afterEach(() => vi.restoreAllMocks())

describe('QuizBlock', () => {
  it('lists the options with mono letters and at least 44px of height, and carries no answer', () => {
    view()
    const options = screen.getAllByRole('radio')
    expect(options).toHaveLength(3)
    expect(options.every((o) => o.className.includes('min-h-[44px]'))).toBe(true)
    expect(within(options[0]).getByText('A').className).toContain('font-mono')
    expect(JSON.stringify(quiz)).not.toMatch(/correct/i)
  })

  it('uses dark text on the yellow selected state', async () => {
    vi.spyOn(mentorV2, 'answerQuiz').mockReturnValue(new Promise(() => {}))
    view()

    const option = screen.getByRole('radio', { name: /thread_id/ })
    await userEvent.click(option)

    expect(option).toHaveClass('bg-amber', 'text-on-amber')
    expect(option).not.toHaveClass('text-white')
  })

  it('confirms a right pick and shows how far the skill moved, in mono', async () => {
    const onResult = vi.fn()
    view(onResult)
    await userEvent.click(screen.getByRole('radio', { name: /thread_id/ }))
    expect(await screen.findByText('Checkpointers 58 → 66')).toHaveClass('font-mono')
    expect(screen.getByRole('radio', { name: /thread_id/ })).toHaveAttribute('data-state', 'right')
    expect(onResult).toHaveBeenCalledWith(expect.objectContaining({ correct: true, skillDelta: { skill: 'Checkpointers', from: 58, to: 66 } }))
  })

  it('guides after a wrong pick without showing the right option, and lets the learner try again', async () => {
    view()
    await userEvent.click(screen.getByRole('radio', { name: /new graph/ }))
    expect(await screen.findByText(/Close\. Let us think it through together/)).toBeInTheDocument()
    expect(screen.getByRole('radio', { name: /new graph/ })).toHaveAttribute('data-state', 'wrong')
    // The right option is not marked, and every option is locked until the learner tries again.
    expect(screen.getByRole('radio', { name: /thread_id/ })).toHaveAttribute('data-state', 'idle')
    expect(screen.getAllByRole('radio').every((o) => o.hasAttribute('disabled'))).toBe(true)
    expect(screen.queryByText(/Checkpointers \d+ →/)).toBeNull()

    await userEvent.click(screen.getByRole('button', { name: 'Try again' }))
    expect(screen.getAllByRole('radio').every((o) => !o.hasAttribute('disabled') && o.getAttribute('data-state') === 'idle')).toBe(true)
    expect(screen.queryByText(/Close\./)).toBeNull()
  })
})

const EN_QUESTION = 'What makes the agent resume the same conversation on a new call?'
const AR_QUESTION = 'ما الذي يجعل الوكيل يستأنف نفس المحادثة عند استدعاء جديد؟'
const arabicBlock: Quiz = {
  ...quiz,
  lang: 'ar',
  question: AR_QUESTION,
  options: [
    { id: 'a', text: 'تمرير thread_id ثابت داخل config' },
    { id: 'b', text: 'إنشاء graph جديد في كل استدعاء' },
    { id: 'c', text: 'رفع قيمة temperature' },
  ],
}
const render_ = (block: Quiz) =>
  render(<QuizBlock block={block} renderFeedback={(blocks) => <MentorBlocks blocks={blocks} />} />)
const switchTo = (language: 'ar' | 'en') => act(async () => { useLanguageStore.setState({ language }) })

describe('QuizBlock follows the UI language', () => {
  it('asks for the same question again when the block is in the other language', async () => {
    const ask = vi.spyOn(mentorV2, 'quiz')
    render_(arabicBlock) // the UI is English
    expect(await screen.findByText(EN_QUESTION)).toBeInTheDocument()
    expect(ask).toHaveBeenCalledWith('quiz-checkpointer-1', 'en')
    // Same options, same ids: the learner's pick means the same thing in either language.
    expect(screen.getAllByRole('radio').map((o) => o.textContent)).toEqual(['APassing a stable thread_id inside config', 'BBuilding a new graph on every call', 'CRaising the temperature'])
  })

  it('does not ask when the block is already in the UI language, or says nothing about its language', async () => {
    const ask = vi.spyOn(mentorV2, 'quiz')
    render_({ ...quiz, lang: 'en' })
    render_(quiz)
    await act(async () => { await Promise.resolve() })
    expect(ask).not.toHaveBeenCalled()
  })

  it('switches in place when the learner changes language, and answers in the new language', async () => {
    const answer = vi.spyOn(mentorV2, 'answerQuiz')
    render_({ ...quiz, lang: 'en', question: EN_QUESTION })
    expect(screen.getByText(EN_QUESTION)).toBeInTheDocument()

    await switchTo('ar')
    expect(await screen.findByText(AR_QUESTION)).toBeInTheDocument()
    expect(screen.queryByText(EN_QUESTION)).toBeNull()

    await userEvent.click(screen.getByRole('radio', { name: /thread_id ثابت/ }))
    expect(await screen.findByText(/صحيح/)).toBeInTheDocument()
    expect(answer).toHaveBeenCalledWith({ quizId: 'quiz-checkpointer-1', optionId: 'a' }, 'ar')

    // Back to English: the question follows again.
    await switchTo('en')
    expect(await screen.findByText(EN_QUESTION)).toBeInTheDocument()
  })

  it('keeps the question, still answerable, when the other language cannot be had', async () => {
    const ask = vi.spyOn(mentorV2, 'quiz').mockRejectedValue(new Error('offline'))
    render_(arabicBlock)
    await waitFor(() => expect(ask).toHaveBeenCalled())
    expect(screen.getByText(AR_QUESTION)).toBeInTheDocument()
    await userEvent.click(screen.getAllByRole('radio')[0])
    expect(await screen.findByText(/Checkpointers 58 → 66/)).toBeInTheDocument()
  })

  it('offers the retry instead of leaving feedback in a language the question no longer is', async () => {
    render_({ ...quiz, lang: 'en', question: EN_QUESTION })
    await userEvent.click(screen.getByRole('radio', { name: /new graph/ }))
    expect(await screen.findByText(/Close\. Let us think it through together/)).toBeInTheDocument()

    await switchTo('ar')
    await waitFor(() => expect(screen.queryByText(/Close\./)).toBeNull())
    expect(await screen.findByText(AR_QUESTION)).toBeInTheDocument()
    expect(screen.getAllByRole('radio').every((o) => !o.hasAttribute('disabled'))).toBe(true)
  })
})
