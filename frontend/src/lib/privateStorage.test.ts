import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { exerciseDraftKey } from '@/features/exercises/draftKeys'
import { exerciseCode } from '@/features/mentor/CodeReview'
import { exerciseDraft } from '@/features/mentor/draft'
import { buildSession } from '@/lib/mentor/interview'
import { interviewStore } from '@/lib/mentor/interviewStore'
import { useAuthStore } from '@/lib/store'
import type { User } from '@/types'

// A shared browser: account A works on an exercise and a mock interview, then account B signs in
// on the same browser. B must never see - or send to a Code Review - anything A wrote.

const signIn = (id: number) =>
  useAuthStore.setState({ user: { id } as User, token: `token-${id}`, expiresAt: Date.now() + 60_000 })

beforeEach(() => window.localStorage.clear())
afterEach(() => useAuthStore.setState({ user: null, token: null, expiresAt: null }))

describe('exercise drafts on a shared browser', () => {
  it('are read only by the account that wrote them, even when it never signed out', () => {
    signIn(1)
    window.localStorage.setItem(exerciseDraftKey(7, 'agent.py'), 'secret_of_account_a = 1\n')
    expect(exerciseDraft(7, 'python')).toBe('secret_of_account_a = 1\n')
    expect(exerciseCode('7', 'python')).toBe('secret_of_account_a = 1\n')

    // A's session expired without a sign-out, B signs in: the review falls back to the starter.
    signIn(2)
    expect(exerciseDraft(7, 'python')).toBeNull()
    expect(exerciseDraft(7)).toBeNull()
    expect(exerciseCode('7', 'python')).toBe('')

    // A's own draft is still there for A.
    signIn(1)
    expect(exerciseDraft(7, 'python')).toBe('secret_of_account_a = 1\n')
  })

  it('written before keys carried the account are never read', () => {
    signIn(2)
    window.localStorage.setItem('exercise:7:agent.py', 'left by someone else\n')
    expect(exerciseDraft(7, 'python')).toBeNull()
  })
})

describe('signing out', () => {
  it("removes every account's private learning data, and nothing else", () => {
    signIn(1)
    const private_ = [
      exerciseDraftKey(7, 'agent.py'),
      exerciseDraftKey(7, 'agent.py', 'abc123'),
      'exercise:7:agent.py',
      'exercise:u2:8:solution.sql',
      'masar:mentor-v2:thread:u1:lesson:3',
      'masar:mentor-v2:plan',
      'masar:mock-interviews:v1:u1',
      'masar:mock-interviews:v1',
    ]
    private_.forEach((key) => window.localStorage.setItem(key, 'x'))
    window.localStorage.setItem('language-prefs', '{"language":"ar"}')
    window.localStorage.setItem('masar-theme', 'dark')

    useAuthStore.getState().clearAuth()

    private_.forEach((key) => expect(window.localStorage.getItem(key), key).toBeNull())
    expect(window.localStorage.getItem('auth-storage')).toBeNull()
    expect(window.localStorage.getItem('language-prefs')).toBe('{"language":"ar"}')
    expect(window.localStorage.getItem('masar-theme')).toBe('dark')
  })
})

describe('mock interviews on a shared browser', () => {
  it('belong to the account that took them', () => {
    signIn(1)
    interviewStore.save(buildSession('iv-a', { role: 'AI Developer', type: 'technical', language: 'en', durationMin: 30 }))
    expect(interviewStore.list().map((s) => s.id)).toEqual(['iv-a'])

    signIn(2)
    expect(interviewStore.list()).toEqual([])
    expect(interviewStore.get('iv-a')).toBeNull()
    expect(interviewStore.active()).toBeNull()

    signIn(1)
    expect(interviewStore.get('iv-a')?.id).toBe('iv-a')
    useAuthStore.getState().clearAuth()
    signIn(1)
    expect(interviewStore.list()).toEqual([])
  })
})
