import { afterEach, describe, expect, it, vi } from 'vitest'
import { splitFences, withAttachment } from '@/lib/mentor/fences'
import {
  QUESTIONS_FOR,
  buildSession,
  dimensionAverage,
  endSession,
  freshCopy,
  isWeak,
  lastScored,
  overallScore,
  weakQuestions,
  type AnswerScore,
  type InterviewSession,
  type QuestionRecord,
} from '@/lib/mentor/interview'
import { MockInterviewStore } from '@/lib/mentor/interviewStore'
import { FREE_DAILY_LIMIT, MockMentorQuota, getMentorQuota, mockQuotaUsedFromUrl } from '@/lib/mentor/quota'
import { MockAnswerScorer, getAnswerScorer } from '@/lib/mentor/scoring'
import { formatClock } from '@/lib/mentor/format'

afterEach(() => vi.unstubAllEnvs())

const score = (a: number, s: number, c: number): AnswerScore => ({ accuracy: a, structure: s, clarity: c, note: { text: 'n' } })
const question = (over: Partial<QuestionRecord> = {}): QuestionRecord => ({
  id: 'q', text: 'What is RAG?', qtype: 'theoretical', hints: [], answer: 'a', skipped: false, score: null, ...over,
})
function session(questions: QuestionRecord[]): InterviewSession {
  return buildSession('s1', { role: 'AI Engineer', type: 'technical', language: 'en', durationMin: 30, questions })
}

describe('splitFences', () => {
  it('keeps prose as typed and pulls fenced code out', () => {
    expect(splitFences('why?\n\n```python\nprint(1)\n```\nthanks')).toEqual([
      { type: 'text', text: 'why?' },
      { type: 'code', code: 'print(1)', lang: 'python' },
      { type: 'text', text: 'thanks' },
    ])
  })
  it('handles an untagged fence and leaves an unclosed one as text', () => {
    expect(splitFences('```\nx = 1\n```')).toEqual([{ type: 'code', code: 'x = 1', lang: '' }])
    expect(splitFences('```\nnever closed')).toEqual([{ type: 'text', text: '```\nnever closed' }])
  })
  it('attaches code as a fence, on its own or after the typed text', () => {
    expect(withAttachment('fix this', 'a = 1\n')).toBe('fix this\n\n```\na = 1\n```')
    expect(withAttachment('', 'a = 1')).toBe('```\na = 1\n```')
    expect(withAttachment('hi', '  \n')).toBe('hi')
  })
})

describe('scores', () => {
  it('averages per dimension and overall, and ignores unscored answers', () => {
    const s = session([question({ score: score(8, 6, 4) }), question({ id: 'b', score: score(6, 6, 8) }), question({ id: 'c' })])
    expect(dimensionAverage(s, 'accuracy')).toBe(7)
    expect(dimensionAverage(s, 'clarity')).toBe(6)
    expect(overallScore(s)).toBe(6.3)
    expect(lastScored(s)?.id).toBe('b')
  })
  it('has no score when nothing was scored', () => {
    const s = session([question()])
    expect(overallScore(s)).toBeNull()
    expect(lastScored(s)).toBeNull()
    expect(dimensionAverage(s, 'structure')).toBeNull()
  })
  it('calls a skipped or low-scoring answer weak, and an unscored one not', () => {
    const skipped = question({ id: 'a', skipped: true, answer: '' })
    const low = question({ id: 'b', score: score(4, 5, 5) })
    const good = question({ id: 'c', score: score(8, 8, 8) })
    const unscored = question({ id: 'd' })
    expect([skipped, low, good, unscored].map(isWeak)).toEqual([true, true, false, false])
    expect(weakQuestions(session([skipped, low, good, unscored])).map((q) => q.id)).toEqual(['a', 'b'])
  })
})

describe('building sessions', () => {
  it('sizes a fresh interview by its length and a retry by its questions', () => {
    expect(buildSession('x', { role: 'r', type: 'technical', language: 'en', durationMin: 45 }).totalQuestions).toBe(QUESTIONS_FOR[45])
    const retry = buildSession('x', { role: 'r', type: 'technical', language: 'en', durationMin: 45, questions: [freshCopy(question())] })
    expect(retry.totalQuestions).toBe(1)
  })
  it('a retried question keeps its text and loses the answer and score', () => {
    const copy = freshCopy(question({ score: score(1, 1, 1), answer: 'old' }))
    expect(copy).toMatchObject({ text: 'What is RAG?', answer: null, skipped: false, score: null })
  })
  it('ends once', () => {
    const ended = endSession(session([]), new Date('2026-01-01T10:00:00Z'))
    expect(endSession(ended, new Date('2027-01-01T10:00:00Z')).endedAt).toBe('2026-01-01T10:00:00.000Z')
  })
})

describe('the interview store', () => {
  it('keeps sessions newest first, finds the active one, and tells subscribers', () => {
    const store = new MockInterviewStore()
    const listener = vi.fn()
    const off = store.subscribe(listener)
    const older = buildSession('old', { role: 'r', type: 'technical', language: 'en', durationMin: 15 }, new Date('2026-01-01'))
    const newer = buildSession('new', { role: 'r', type: 'technical', language: 'en', durationMin: 15 }, new Date('2026-02-01'))
    store.save(endSession(older))
    store.save(newer)
    expect(store.list().map((s) => s.id)).toEqual(['new', 'old'])
    expect(store.active()?.id).toBe('new')
    expect(store.get('old')?.endedAt).not.toBeNull()
    expect(listener).toHaveBeenCalledTimes(2)
    off()
    store.save(newer)
    expect(listener).toHaveBeenCalledTimes(2)
  })
  it('survives corrupt storage', () => {
    window.localStorage.setItem('masar:mock-interviews:v1:anon', '{not json')
    expect(new MockInterviewStore().list()).toEqual([])
  })
})

describe('the mock scorer', () => {
  it('is deterministic, in range, and rewards a longer, more specific answer', async () => {
    const scorer = new MockAnswerScorer({ delayMs: 0 })
    const short = await scorer.score({ question: 'q', answer: 'It depends.', language: 'en' })
    const long = await scorer.score({
      question: 'q', language: 'en',
      answer: 'RAG retrieves documents first. It then feeds them to the model. In my last project we cut hallucinations by 30 percent. The index is refreshed nightly.',
    })
    expect(await scorer.score({ question: 'q', answer: 'It depends.', language: 'en' })).toEqual(short)
    for (const v of [short.accuracy, short.structure, short.clarity, long.accuracy, long.structure, long.clarity]) {
      expect(v).toBeGreaterThanOrEqual(1)
      expect(v).toBeLessThanOrEqual(9)
    }
    expect(long.accuracy).toBeGreaterThan(short.accuracy)
  })
  it('is off in a production build unless the build opts in', () => {
    vi.stubEnv('NODE_ENV', 'production')
    expect(getAnswerScorer()).toBeNull()
    expect(getMentorQuota()).toBeNull()
    vi.stubEnv('NEXT_PUBLIC_MENTOR_MOCKS', '1')
    expect(getAnswerScorer()?.isMock).toBe(true)
  })
})

describe('the mock mentor quota', () => {
  const memory = () => {
    const data = new Map<string, string>()
    return { getItem: (k: string) => data.get(k) ?? null, setItem: (k: string, v: string) => void data.set(k, v) }
  }
  it('counts a day and runs out at the limit', () => {
    const quota = new MockMentorQuota({ storage: memory(), limit: 2, now: () => new Date(2026, 0, 5, 9) })
    expect(quota.status()).toMatchObject({ left: 2, exhausted: false })
    quota.consume()
    expect(quota.consume()).toMatchObject({ used: 2, left: 0, exhausted: true })
  })
  it('starts again the next day', () => {
    const storage = memory()
    new MockMentorQuota({ storage, limit: 1, now: () => new Date(2026, 0, 5) }).consume()
    expect(new MockMentorQuota({ storage, limit: 1, now: () => new Date(2026, 0, 6) }).status().exhausted).toBe(false)
  })
  it('the Free plan is 20 a day, and ?mockQuotaUsed jumps to the limit', () => {
    expect(FREE_DAILY_LIMIT).toBe(20)
    expect(mockQuotaUsedFromUrl('?mockQuotaUsed=20')).toBe(20)
    expect(mockQuotaUsedFromUrl('?mockQuotaUsed=abc')).toBeNull()
    expect(getMentorQuota('mockQuotaUsed=20')?.status().exhausted).toBe(true)
  })
})

describe('formatClock', () => {
  it('does not wrap minutes at 59', () => {
    expect(formatClock(12 * 60_000 + 41_000)).toBe('12:41')
    expect(formatClock(45 * 60_000)).toBe('45:00')
    expect(formatClock(-5)).toBe('00:00')
  })
})
