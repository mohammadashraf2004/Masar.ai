import { afterEach, describe, expect, it, vi } from 'vitest'
import { api, mentorV2 } from '@/lib/api'

// How the quiz question reaches the real server when the quiz endpoint is live.

const http = () => (api as unknown as { http: { get: (url: string, config?: unknown) => Promise<{ data: unknown }> } }).http

afterEach(() => {
  vi.restoreAllMocks()
  process.env.NEXT_PUBLIC_MENTOR_V2_LIVE = ''
})

describe('mentorV2.quiz', () => {
  it('asks the server for the same question in the language, when the quiz endpoint is live', async () => {
    process.env.NEXT_PUBLIC_MENTOR_V2_LIVE = 'quiz'
    const block = { kind: 'quiz', quizId: '12:0', lang: 'ar', question: 'س', options: [], grounding: 'lesson' }
    const get = vi.spyOn(http(), 'get').mockResolvedValue({ data: block })

    await expect(mentorV2.quiz('12:0', 'ar')).resolves.toEqual(block)
    expect(get).toHaveBeenCalledWith('/mentor/quiz/12%3A0', { params: { language: 'ar' } })
  })

  it('stays on the local stand-in until the quiz endpoint is live', async () => {
    const get = vi.spyOn(http(), 'get')
    await expect(mentorV2.quiz('quiz-checkpointer-1', 'en')).resolves.toMatchObject({ lang: 'en' })
    expect(get).not.toHaveBeenCalled()
  })
})
