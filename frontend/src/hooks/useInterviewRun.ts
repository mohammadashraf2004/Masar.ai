'use client'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { api } from '@/lib/api'
import type { StringKey } from '@/lib/i18n'
import { mentorErrorKey } from '@/lib/mentorErrors'
import {
  difficultyFor,
  endSession,
  isFinished,
  newQuestion,
  topicFor,
  type AnswerScore,
  type InterviewSession,
  type QuestionRecord,
} from '@/lib/mentor/interview'
import { interviewStore } from '@/lib/mentor/interviewStore'
import { getAnswerScorer } from '@/lib/mentor/scoring'
import { useInterviews } from '@/hooks/useInterviews'

/** Applies a change to a saved interview. The store is the one source of truth. */
function update(id: string, change: (session: InterviewSession) => InterviewSession) {
  const session = interviewStore.get(id)
  if (session) interviewStore.save(change(session))
}

function patchQuestion(session: InterviewSession, questionId: string, patch: Partial<QuestionRecord>): InterviewSession {
  return { ...session, questions: session.questions.map((q) => (q.id === questionId ? { ...q, ...patch } : q)) }
}

/**
 * Runs one interview: which question is on screen, fetching the next one, saving each answer and
 * scoring it, and ending.
 *
 * Everything the learner did lives in `interviewStore`, so a reload resumes where they were. What
 * is on screen is derived from that: the first question without an answer is the current one;
 * when there is none and the interview is not full, the next one is fetched (which is also how
 * the first one arrives). A failed fetch stops there with `error` until `retry()`; the backend
 * refunds the credits of a failed generation, so trying again is free.
 */
export function useInterviewRun(id: string, level: string | undefined) {
  const { interviews, loaded } = useInterviews()
  const session = useMemo(() => interviews.find((s) => s.id === id) ?? null, [interviews, id])
  const scorer = useMemo(() => getAnswerScorer(), [])

  const [scoring, setScoring] = useState(0)
  const [error, setError] = useState<StringKey | null>(null)
  const inFlight = useRef(false)
  const scores = useRef<Set<Promise<void>>>(new Set())

  const index = session ? session.questions.findIndex((q) => q.answer === null && !q.skipped) : -1
  const current = session && index >= 0 ? session.questions[index] : null
  const finished = session ? isFinished(session) : false
  const needsQuestion = !!session && !finished && current === null && session.questions.length < session.totalQuestions
  // Every question is answered but the interview was never ended (a reload on the last question).
  const complete = !!session && !finished && current === null && session.questions.length >= session.totalQuestions
  const isLast = !!session && index >= 0 && index === session.totalQuestions - 1

  const loadNext = useCallback(async () => {
    if (inFlight.current) return
    const saved = interviewStore.get(id)
    if (!saved || saved.endedAt || saved.questions.length >= saved.totalQuestions) return
    inFlight.current = true
    try {
      const earlier = saved.questions
        .filter((q) => q.answer !== null)
        .map((q) => ({ question: q.text, answer: q.skipped ? '' : (q.answer ?? '') }))
      // The turn's id: asking again for the same turn (a retry, a reload, a dropped connection)
      // gets the same question back and is charged once; the next turn has its own.
      const turn = `iv-${saved.id}-q${saved.questions.length + 1}`.replace(/[^A-Za-z0-9_-]/g, '').slice(-64)
      const question = await api.getMockInterviewQuestion(topicFor(saved.role, saved.type), difficultyFor(level), earlier, saved.language, turn)
      update(id, (s) => (s.endedAt || s.questions.length >= s.totalQuestions ? s : { ...s, questions: [...s.questions, newQuestion(question)] }))
    } catch (err) {
      setError(mentorErrorKey(err))
    } finally {
      inFlight.current = false
    }
  }, [id, level])

  useEffect(() => {
    // Awaited so every state write inside `loadNext` follows an await boundary
    // (react-hooks/set-state-in-effect), as in challenges/page.tsx.
    if (needsQuestion && !error) void (async () => { await loadNext() })()
  }, [needsQuestion, error, loadNext])

  const settleScores = useCallback(async () => {
    await Promise.all(Array.from(scores.current))
  }, [])

  const finish = useCallback(async () => {
    await settleScores()
    update(id, (s) => endSession(s))
  }, [id, settleScores])

  /**
   * Saves the answer (or, with `null`, the skip) to the current question, starts scoring it, and
   * moves on. Resolves `true` when that was the last question and the interview has ended.
   */
  const submit = useCallback(
    async (answer: string | null): Promise<boolean> => {
      const saved = interviewStore.get(id)
      const question = saved?.questions.find((q) => q.answer === null && !q.skipped)
      if (!saved || !question || saved.endedAt) return false
      const text = answer?.trim() ?? ''
      const last = saved.questions.length >= saved.totalQuestions && saved.questions[saved.questions.length - 1].id === question.id
      update(id, (s) => patchQuestion(s, question.id, { answer: text, skipped: answer === null }))

      if (text && scorer) {
        setScoring((n) => n + 1)
        const run: Promise<void> = scorer
          .score({ question: question.text, answer: text, language: saved.language })
          .then((score: AnswerScore) => update(id, (s) => patchQuestion(s, question.id, { score })))
          .catch(() => {
            // An unscored answer is still an answer: the report lists it without a score.
          })
          .finally(() => {
            scores.current.delete(run)
            setScoring((n) => n - 1)
          })
        scores.current.add(run)
      }

      if (last) {
        await finish()
        return true
      }
      return false
    },
    [id, scorer, finish],
  )

  const retry = useCallback(() => setError(null), [])

  return {
    loaded,
    session,
    index,
    current,
    finished,
    complete,
    isLast,
    fetching: needsQuestion && !error,
    scoring: scoring > 0,
    /** Whether scores will be produced at all (false in a production build with no scorer). */
    scoringOn: scorer !== null,
    scoresAreMock: scorer?.isMock ?? false,
    error,
    submit,
    finish,
    retry,
  }
}
