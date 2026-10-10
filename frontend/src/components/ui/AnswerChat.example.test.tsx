import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { api } from '@/lib/api'
import { useLanguageStore } from '@/lib/language'
import { AnswerChat } from './AnswerChat'

vi.mock('@/lib/api', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/lib/api')>()
  return {
    ...actual,
    api: {
      getExerciseAnswer: vi.fn(),
      answerExercise: vi.fn(),
      getExerciseExample: vi.fn(),
    },
  }
})

const mocked = api as unknown as {
  getExerciseAnswer: ReturnType<typeof vi.fn>
  answerExercise: ReturnType<typeof vi.fn>
  getExerciseExample: ReturnType<typeof vi.fn>
}

const EXAMPLE = {
  example_answer: 'Recursion solves a problem by calling the same function on a smaller case until a base case stops it.',
  example_answer_ar: 'العودية تحل المشكلة باستدعاء الدالة نفسها على حالة أصغر حتى توقفها حالة أساسية.',
}

function conversation(overrides: Record<string, unknown> = {}) {
  return {
    id: 1, exercise_id: 7, messages: [
      { role: 'user', content: 'It calls itself.' },
      { role: 'assistant', content: 'Close - what stops it?' },
    ],
    is_correct: false, score: 40, example_available: true, ...overrides,
  }
}

async function renderChat() {
  await act(async () => {
    render(<AnswerChat target={{ kind: 'exercise', id: 7 }} isCode={false} />)
  })
}

beforeEach(() => {
  vi.clearAllMocks()
  // jsdom has no layout, so it has no scrollIntoView either.
  Element.prototype.scrollIntoView = vi.fn()
  useLanguageStore.setState({ language: 'en', mode: 'arabic_first', annotateTerms: true })
})

describe('AnswerChat example answer', () => {
  it('offers nothing before the first evaluated answer', async () => {
    mocked.getExerciseAnswer.mockRejectedValue(Object.assign(new Error('404'), { response: { status: 404 } }))
    await renderChat()
    expect(screen.queryByRole('button', { name: 'Show an example answer' })).toBeNull()
    expect(mocked.getExerciseExample).not.toHaveBeenCalled()
  })

  it('opens the example after an evaluated answer, in the interface language', async () => {
    mocked.getExerciseAnswer.mockResolvedValue(conversation())
    mocked.getExerciseExample.mockResolvedValue(EXAMPLE)
    await renderChat()
    await userEvent.click(await screen.findByRole('button', { name: 'Show an example answer' }))
    expect(await screen.findByText(EXAMPLE.example_answer)).toBeInTheDocument()
    expect(screen.getByText(/Yours can be worded differently/)).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: 'Hide the example answer' }))
    expect(screen.queryByText(EXAMPLE.example_answer)).toBeNull()
    expect(mocked.getExerciseExample).toHaveBeenCalledOnce()
  })

  it('shows the Arabic example to an Arabic reader', async () => {
    useLanguageStore.setState({ language: 'ar' })
    mocked.getExerciseAnswer.mockResolvedValue(conversation())
    mocked.getExerciseExample.mockResolvedValue(EXAMPLE)
    await renderChat()
    await userEvent.click(await screen.findByRole('button', { name: 'عرض مثال لإجابة' }))
    expect(await screen.findByText(EXAMPLE.example_answer_ar)).toBeInTheDocument()
  })

  it('unlocks right after the first answer is evaluated', async () => {
    mocked.getExerciseAnswer.mockRejectedValue(Object.assign(new Error('404'), { response: { status: 404 } }))
    mocked.answerExercise.mockResolvedValue(conversation())
    await renderChat()
    await userEvent.type(screen.getByRole('textbox'), 'It calls itself.')
    await userEvent.click(screen.getByRole('button', { name: /send|إرسال/i }))
    expect(await screen.findByRole('button', { name: 'Show an example answer' })).toBeInTheDocument()
  })
})
