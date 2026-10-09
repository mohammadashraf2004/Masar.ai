import { act, render, renderHook, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { api, MENTOR_MESSAGE_TIMEOUT_MS, mentorV2 } from '@/lib/api'
import { useAuthStore } from '@/lib/store'
import { mentorV2Live, mentorV2MocksAllowed } from './flag'
import { lessonHref, planBlockHref } from './links'
import { GroundingPill } from './MentorMessageView'
import { StudyPlan } from './StudyPlan'
import { clearThread, loadThread, saveThread, scopeOf, threadKey } from './threadStore'
import { useMentorV2 } from './useMentorV2'
import type { MentorMessageV2, StudyPlanV2 } from './types'

// With the production setting (NEXT_PUBLIC_MENTOR_V2_LIVE=message,quiz) the hub talks to the real
// server, and no fixture - invented skills, suggestions, hints, plans or interview reports - may
// ever reach a learner.

type Http = { get: (...args: unknown[]) => Promise<{ data: unknown }>; post: (...args: unknown[]) => Promise<{ data: unknown }> }
const http = () => (api as unknown as { http: Http }).http

const reply = (over: Partial<MentorMessageV2> = {}): MentorMessageV2 & { sessionId: number } => ({
  id: 'm1', role: 'mentor', creditCost: 2, sessionId: 1,
  blocks: [{ kind: 'text', text: 'ok', grounding: 'general' }], ...over,
})

beforeEach(() => {
  process.env.NEXT_PUBLIC_MENTOR_V2_LIVE = 'message,quiz'
  window.localStorage.clear()
})

afterEach(() => {
  vi.restoreAllMocks()
  process.env.NEXT_PUBLIC_MENTOR_V2_LIVE = ''
  useAuthStore.setState({ user: null, token: null, expiresAt: null })
})

describe('the live mentor never serves a fixture', () => {
  it('knows it is live, and allows no fixtures', () => {
    expect(mentorV2Live()).toBe(true)
    expect(mentorV2MocksAllowed()).toBe(false)
    process.env.NEXT_PUBLIC_MENTOR_V2_LIVE = ''
    expect(mentorV2MocksAllowed()).toBe(true)
  })

  it('reads the learner model and the weekly plan from the server', async () => {
    const get = vi.spyOn(http(), 'get').mockResolvedValue({ data: { position: { track: '', course: '', lesson: '' }, skills: [] } })
    await mentorV2.learner('en')
    expect(get).toHaveBeenCalledWith('/mentor/learner', { params: { language: 'en' } })

    get.mockResolvedValue({ data: { goal: 'g', totalMinutes: 0, days: [], reasons: [] } })
    await mentorV2.plan({ weekStart: '2026-10-03', variant: 1 }, 'ar')
    expect(get).toHaveBeenLastCalledWith('/mentor/plan', { params: { weekStart: '2026-10-03', variant: 1, language: 'ar' } })
  })

  it('shows no suggestion or proactive card rather than an invented one', async () => {
    const get = vi.spyOn(http(), 'get')
    const post = vi.spyOn(http(), 'post')
    expect(await mentorV2.suggestion('en')).toBeNull()
    expect(await mentorV2.proactive('en')).toBeNull()
    expect(get).not.toHaveBeenCalled()
    expect(post).not.toHaveBeenCalled()
  })

  it('asks the real mentor for a hint about the real exercise, with the learner draft', async () => {
    const post = vi.spyOn(http(), 'post').mockResolvedValue({ data: reply({ intent: 'HINT' }) })
    await mentorV2.hint({ exerciseId: '9007', level: 2, code: 'x = 1  # my draft', requestId: 'rq-12345678' }, 'en')
    expect(post).toHaveBeenCalledWith('/mentor/message', expect.objectContaining({
      intent: 'HINT', hintLevel: 2, requestId: 'rq-12345678', language: 'en',
      context: { exerciseId: '9007', attachCode: true, code: 'x = 1  # my draft' },
    }), { timeout: MENTOR_MESSAGE_TIMEOUT_MS })
  })

  it('waits for a send longer than the server may take, so a retry never races a send still running', async () => {
    const post = vi.spyOn(http(), 'post').mockResolvedValue({ data: reply() })
    await mentorV2.sendMessage({ text: 'Why sqrt(d_k)?', context: { lessonId: '42' }, requestId: 'rq-1' }, 'en')
    const [, , config] = post.mock.calls[0] as [string, unknown, { timeout: number }]
    // The API worker is killed at 60 s (gunicorn --timeout 60); the client default is 30 s.
    expect(config.timeout).toBeGreaterThan(60_000)
  })

  it('gives the solution only after confirmation, from the exercise itself, free', async () => {
    const post = vi.spyOn(http(), 'post').mockResolvedValue({ data: { solution_code: 'def f():\n    return 1' } })
    await expect(mentorV2.hint({ exerciseId: '9007', level: 4 }, 'en')).rejects.toThrow()
    expect(post).not.toHaveBeenCalled()

    const message = await mentorV2.hint({ exerciseId: '9007', level: 4, confirm: true }, 'en')
    expect(post).toHaveBeenCalledWith('/practice/exercises/9007/solution')
    expect(message.creditCost).toBe(0)
    expect(message.blocks[0]).toMatchObject({ kind: 'hint', level: 4, code: 'def f():\n    return 1' })
  })
})

describe('links to real Masar content are built by the app', () => {
  it('builds a lesson link only from a course slug and a numeric lesson id', () => {
    expect(lessonHref('course-004', '12')).toBe('/courses/course-004/lessons/12')
    expect(lessonHref('course-004', 'M02.L03')).toBeNull()
    expect(lessonHref('../admin', '12')).toBeNull()
    expect(lessonHref(undefined, '12')).toBeNull()
  })

  it('never follows a plan block somewhere unexpected', () => {
    expect(planBlockHref({ type: 'lesson', title: 't', minutes: 30, refId: 'lesson:12', courseId: 'course-004', lessonId: '12' }))
      .toBe('/courses/course-004/lessons/12')
    expect(planBlockHref({ type: 'review', title: 't', minutes: 15, refId: 'mentor:chat' })).toBe('/mentor')
    expect(planBlockHref({ type: 'lesson', title: 't', minutes: 15, refId: '//evil.example/x' })).toBe('/learn')
    expect(planBlockHref({ type: 'lesson', title: 't', minutes: 15, refId: 'https://evil.example' })).toBe('/learn')
  })

  it('names an extra-concept source by its verified title and links to it, never by a database id', () => {
    const { rerender } = render(<GroundingPill grounding="extra" sourceLessonId="1237" sourceCourseId="course-004" sourceTitle="Self-Attention" />)
    const link = screen.getByRole('link', { name: 'Extra concept · Self-Attention' })
    expect(link).toHaveAttribute('href', '/courses/course-004/lessons/1237')

    rerender(<GroundingPill grounding="extra" sourceLessonId="1237" />)
    expect(screen.queryByRole('link')).toBeNull()
    expect(screen.getByText('Extra concept')).toBeInTheDocument()
    expect(document.body.textContent).not.toContain('1237')
  })
})

describe('the weekly plan', () => {
  const SATURDAY = new Date(2026, 9, 3, 12, 0, 0)
  const week = (blocks: StudyPlanV2['days'][number]['blocks']): StudyPlanV2 => ({
    status: 'ok', goal: 'Continue Applied NLP', totalMinutes: 60, reasons: ['Applied NLP: 1 of 4 lessons completed'],
    days: Array.from({ length: 7 }, (_, i) => ({ date: `2026-10-0${3 + i}`, blocks: i === 0 ? blocks : [] })),
  })

  it('links each block to the real lesson and says the plan is built from progress', async () => {
    vi.spyOn(mentorV2, 'plan').mockResolvedValue(week([
      { type: 'lesson', title: 'Applied NLP · Self-Attention', minutes: 60, refId: 'lesson:12', courseId: 'course-004', lessonId: '12' },
    ]))
    await act(async () => { render(<StudyPlan now={SATURDAY} />) })
    expect(screen.getByRole('link', { name: /Self-Attention/ })).toHaveAttribute('href', '/courses/course-004/lessons/12')
    expect(screen.getByText('Built from your enrolments and progress. Free.')).toBeInTheDocument()
  })

  it('says so when there is no enrolment, instead of inventing a week', async () => {
    vi.spyOn(mentorV2, 'plan').mockResolvedValue({ ...week([]), status: 'no_enrollment', goal: '', reasons: [] })
    await act(async () => { render(<StudyPlan now={SATURDAY} />) })
    expect(screen.getByTestId('plan-empty')).toHaveTextContent('Enroll in a course to get a weekly plan')
    expect(screen.getByRole('link', { name: 'Browse courses' })).toHaveAttribute('href', '/learn')
    expect(screen.queryAllByTestId('plan-day')).toHaveLength(0)
  })
})

describe('conversation copies on this browser', () => {
  it('are kept per account and per lesson, and logging out removes them all', () => {
    useAuthStore.setState({ user: { id: 1 } as never })
    saveThread([reply()], scopeOf({ lessonId: '12' }))
    expect(threadKey(scopeOf({ lessonId: '12' }))).toBe('masar:mentor-v2:thread:1:lesson:12')
    expect(loadThread(scopeOf({ lessonId: '12' }))).toHaveLength(1)
    expect(loadThread(scopeOf({ lessonId: '13' }))).toEqual([])

    useAuthStore.setState({ user: { id: 2 } as never })
    expect(loadThread(scopeOf({ lessonId: '12' }))).toEqual([])

    useAuthStore.setState({ user: { id: 1 } as never })
    window.localStorage.setItem('masar:mentor-v2:plan', '{}')
    useAuthStore.getState().clearAuth()
    expect(Object.keys(window.localStorage).filter((key) => key.startsWith('masar:mentor-v2:'))).toEqual([])
    clearThread()
  })
})

describe('a retried send', () => {
  beforeEach(() => { vi.spyOn(api, 'getMentorThread').mockResolvedValue([]) })

  it('reuses its request id, so the server answers it once and charges once', async () => {
    const send = vi.spyOn(mentorV2, 'sendMessage')
      .mockRejectedValueOnce(new Error('Network Error'))
      .mockResolvedValueOnce(reply())
    const { result } = renderHook(() => useMentorV2({ base: { courseId: 'course-004', lessonId: '12' } }))

    await act(async () => { await result.current.send('Explain this') })
    expect(result.current.failure?.errorKey).toBe('mentor.error.network')
    await act(async () => { await result.current.retry() })

    expect(send).toHaveBeenCalledTimes(2)
    const [first, second] = send.mock.calls.map((call) => call[0])
    expect(first.requestId).toMatch(/^rq-/)
    expect(second.requestId).toBe(first.requestId)
    expect(second.context).toEqual({ courseId: 'course-004', lessonId: '12' })
    expect(result.current.failure).toBeNull()
    expect(result.current.messages.map((m) => m.role)).toEqual(['learner', 'mentor'])
  })

  it('starts a new server conversation after "new conversation"', async () => {
    const send = vi.spyOn(mentorV2, 'sendMessage').mockResolvedValue(reply())
    const { result } = renderHook(() => useMentorV2({ base: { lessonId: '12' } }))
    await act(async () => { await result.current.send('one') })
    act(() => { result.current.newThread() })
    await act(async () => { await result.current.send('two') })
    await act(async () => { await result.current.send('three') })
    expect(send.mock.calls.map((call) => call[0].fresh)).toEqual([undefined, true, undefined])
    expect(result.current.messages.filter((m) => m.role === 'learner')).toHaveLength(2)
  })
})

describe('a lesson thread on a new device', () => {
  it('shows the conversation the server is continuing for that lesson', async () => {
    const server = [
      { id: 's1-0', role: 'learner' as const, creditCost: 0, blocks: [{ kind: 'text' as const, text: 'Why sqrt(d_k)?', grounding: 'general' as const }] },
      reply({ id: 's1-1' }),
    ]
    const thread = vi.spyOn(api, 'getMentorThread').mockResolvedValue(server)
    const { result } = renderHook(() => useMentorV2({ base: { lessonId: '42' } }))
    await act(async () => { await Promise.resolve() })
    expect(thread).toHaveBeenCalledWith('42')
    expect(result.current.messages.map((m) => m.id)).toEqual(['s1-0', 's1-1'])
  })

  it('keeps this browser copy when there is one', async () => {
    saveThread([reply({ id: 'local' })], scopeOf({ lessonId: '42' }))
    const thread = vi.spyOn(api, 'getMentorThread').mockResolvedValue([reply({ id: 'server' })])
    const { result } = renderHook(() => useMentorV2({ base: { lessonId: '42' } }))
    await act(async () => { await Promise.resolve() })
    expect(thread).not.toHaveBeenCalled()
    expect(result.current.messages.map((m) => m.id)).toEqual(['local'])
  })
})
