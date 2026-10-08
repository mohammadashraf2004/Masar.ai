import { beforeEach, describe, expect, it } from 'vitest'
import {
  COOLDOWN_MS, HintConfirmRequired, MESSAGE_CREDITS, detectIntent, mockAddToPlan, mockAnswerQuiz, mockControl, mockHint,
  mockLearner, mockPlan, mockProactive, mockQuiz, mockResolveSuggestion, mockReview, mockSendMessage, mockSuggestion, resetMentorMock,
} from './mock'

// The rules the real Mentor v2 server must keep, written down as tests against the stand-in the screens are built on.

beforeEach(() => resetMentorMock())

describe('intent', () => {
  it('prefers the intent the learner chose to its own reading of the text', () => {
    expect(detectIntent('why do we need embeddings?', 'SIMPLIFY')).toBe('SIMPLIFY')
    expect(detectIntent('why do we need embeddings?')).toBe('WHY')
    expect(detectIntent('hello there')).toBe('GENERAL_QUESTION')
  })
})

describe('messages', () => {
  const lesson = { courseId: 'langgraph-agent-memory', lessonId: '1007' }

  it('grounds an answer in the lesson only when the lesson is in the context', async () => {
    const withLesson = await mockSendMessage({ text: 'explain', context: lesson }, 'en')
    const without = await mockSendMessage({ text: 'explain', context: {} }, 'en')
    const grounding = (m: typeof withLesson) => m.blocks.flatMap((b) => (b.kind === 'text' ? [b.grounding] : []))
    expect(grounding(withLesson)).toEqual(['lesson'])
    expect(grounding(without)).toEqual(['general'])
  })

  it('labels what the lesson does not teach as an extra concept, with its lesson', async () => {
    const reply = await mockSendMessage({ text: 'explain', intent: 'EXPLAIN', context: { ...lesson, selectedText: 'SqliteSaver keeps state on disk' } }, 'en')
    const text = reply.blocks.find((b) => b.kind === 'text')
    expect(text).toMatchObject({ grounding: 'extra', sourceLessonId: '8' })
  })

  it('charges one ordinary message, and nothing for a quick quiz', async () => {
    expect((await mockSendMessage({ text: 'explain', context: lesson }, 'en')).creditCost).toBe(MESSAGE_CREDITS)
    expect((await mockSendMessage({ text: '', intent: 'QUIZ', context: lesson }, 'en')).creditCost).toBe(0)
  })

  it('never puts the answer in a quiz block', async () => {
    const reply = await mockSendMessage({ text: '', intent: 'QUIZ', context: lesson }, 'en')
    const quiz = reply.blocks.find((b) => b.kind === 'quiz')
    expect(quiz).toBeTruthy()
    expect(JSON.stringify(quiz)).not.toMatch(/correct|answer/i)
    // `lang` says which language the text is written in; nothing else is added.
    expect(Object.keys(quiz as object).sort()).toEqual(['grounding', 'kind', 'lang', 'options', 'question', 'quizId'])
  })

  it('serves the same quiz question in the language asked for, with the same option ids', async () => {
    const reply = await mockSendMessage({ text: '', intent: 'QUIZ', context: lesson }, 'en')
    const quiz = reply.blocks.find((b) => b.kind === 'quiz')
    if (quiz?.kind !== 'quiz') throw new Error('no quiz block')
    const arabic = await mockQuiz(quiz.quizId, 'ar')
    expect(arabic).toMatchObject({ lang: 'ar', quizId: quiz.quizId })
    expect(arabic.question).not.toBe(quiz.question)
    expect(arabic.options.map((o) => o.id)).toEqual(quiz.options.map((o) => o.id))
    expect(JSON.stringify(arabic)).not.toMatch(/correct|answer/i)
    await expect(mockQuiz('no-such-quiz', 'ar')).rejects.toThrow('quiz_not_found')
  })

  it('fails like a provider outage once, and the next call works', async () => {
    mockControl.failNext = true
    await expect(mockSendMessage({ text: 'explain', context: lesson }, 'en')).rejects.toThrow('provider_unavailable')
    await expect(mockSendMessage({ text: 'explain', context: lesson }, 'en')).resolves.toBeTruthy()
  })
})

describe('hints', () => {
  it('refuses the solution without the learner confirming, and gives it with', async () => {
    await expect(mockHint({ exerciseId: '9007', level: 4 }, 'en')).rejects.toBeInstanceOf(HintConfirmRequired)
    const solution = await mockHint({ exerciseId: '9007', level: 4, confirm: true }, 'en')
    const hint = solution.blocks.find((b) => b.kind === 'hint')
    expect(hint).toMatchObject({ level: 4 })
    expect((hint as { code?: string }).code).toContain('checkpointer=MemorySaver()')
  })

  it('keeps the first three levels to words, with no code', async () => {
    for (const level of [1, 2, 3] as const) {
      const hint = (await mockHint({ exerciseId: '9007', level }, 'en')).blocks[0] as { code?: string }
      expect(hint.code).toBeUndefined()
    }
  })
})

describe('quiz answers', () => {
  it('moves the skill on a right answer, and says how far', async () => {
    const result = await mockAnswerQuiz({ quizId: 'quiz-checkpointer-1', optionId: 'a' }, 'en')
    expect(result.correct).toBe(true)
    expect(result.skillDelta).toEqual({ skill: 'Checkpointers', from: 58, to: 66 })
    const learner = await mockLearner('en')
    expect(learner.skills.find((s) => s.name === 'Checkpointers')?.confidence).toBe(0.66)
  })

  it('never reveals the right option after a wrong one, and does not move the skill', async () => {
    const result = await mockAnswerQuiz({ quizId: 'quiz-checkpointer-1', optionId: 'b' }, 'en')
    expect(result.correct).toBe(false)
    expect(result.skillDelta).toBeUndefined()
    expect(JSON.stringify(result)).not.toContain('thread_id inside config')
    expect(result.feedback.some((b) => b.kind === 'check')).toBe(true)
    const learner = await mockLearner('en')
    expect(learner.skills.find((s) => s.name === 'Checkpointers')?.confidence).toBe(0.58)
  })
})

describe('code review', () => {
  const starter = 'from langgraph.checkpoint.memory import MemorySaver\n\ngraph = builder.compile()\n\ndef run(message: str, thread_id: str):\n    return graph.invoke({"messages": [message]})\n'

  it('reads the code and says it did not run it', async () => {
    const result = await mockReview({ exerciseId: '9007', code: starter, lang: 'python' }, 'en')
    expect(result.executed).toBe(false)
    expect(result.comments.map((c) => [c.line, c.severity])).toEqual([[1, 'ok'], [3, 'issue'], [6, 'issue']])
  })

  it('finds nothing wrong in code that passes the checkpointer and the thread id', async () => {
    const fixed = 'from langgraph.checkpoint.memory import MemorySaver\n\ngraph = builder.compile(checkpointer=MemorySaver())\n\ndef run(message, thread_id):\n    return graph.invoke({"messages": [message]}, {"configurable": {"thread_id": thread_id}})\n'
    const result = await mockReview({ exerciseId: '9008', code: fixed, lang: 'python' }, 'en')
    expect(result.comments.some((c) => c.severity === 'issue')).toBe(false)
  })

  it('unlocks one more debug step each time it looks at the same exercise again', async () => {
    const unlocked = async () => (await mockReview({ exerciseId: '9009', code: starter, lang: 'python' }, 'en')).debugSteps.filter((s) => s.unlocked).length
    expect([await unlocked(), await unlocked(), await unlocked()]).toEqual([1, 2, 3])
  })
})

describe('suggestions and proactive messages', () => {
  it('offers one suggestion, then none for 24 hours', async () => {
    let now = 1_000_000
    mockControl.now = () => now
    const first = await mockSuggestion('en')
    expect(first).not.toBeNull()
    await mockResolveSuggestion(first!.id)
    expect(await mockSuggestion('en')).toBeNull()
    now += COOLDOWN_MS - 1
    expect(await mockSuggestion('en')).toBeNull()
    now += 2
    expect(await mockSuggestion('en')).not.toBeNull()
  })

  it('opens a free card once a day', () => {
    let now = 5_000_000
    mockControl.now = () => now
    const card = mockProactive('en')
    expect(card).toMatchObject({ creditCost: 0, proactive: { trigger: expect.any(String) } })
    expect(mockProactive('en')).toBeNull()
    now += COOLDOWN_MS + 1
    expect(mockProactive('en')).not.toBeNull()
  })
})

describe('weekly plan', () => {
  it('lays out seven days with a rest day, and adds what the report recommends', async () => {
    const plan = await mockPlan({ weekStart: '2026-10-03' }, 'en')
    expect(plan.days).toHaveLength(7)
    expect(plan.days[6].blocks).toEqual([])
    expect(plan.totalMinutes).toBe(200)
    await mockAddToPlan([{ type: 'review', title: 'Ragas', minutes: 20, refId: '/x' }])
    const again = await mockPlan({ weekStart: '2026-10-03' }, 'en')
    expect(again.totalMinutes).toBe(220)
  })
})
