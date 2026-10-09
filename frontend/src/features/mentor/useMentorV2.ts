'use client'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { api, mentorV2 } from '@/lib/api'
import { useMentorV2I18n, type StringKey } from '@/lib/i18n'
import { mentorErrorKey } from '@/lib/mentorErrors'
import { buildContext, DEFAULT_CONTEXT } from './context'
import { exerciseDraft } from './draft'
import { mentorV2Live } from './flag'
import { loadThread, saveThread, scopeOf } from './threadStore'
import { NEEDS_NO_TEXT } from './ActionChips'
import type { MentorContextRef, MentorIntent, MentorMessageV2 } from './types'

interface Options {
  /** The lesson/exercise the conversation starts from (the server's "last active"). */
  base?: MentorContextRef
  /** Fetch the proactive card on arrival (the hub does; the lesson panel does not). */
  proactive?: boolean
}

/** A send that failed: what to repeat, under the same request id, why it failed, and in which thread. */
interface Failure { text: string; intent: MentorIntent | null; requestId: string; errorKey: StringKey; scope: string }

let sequence = 0
const localId = (prefix: string) => `${prefix}-${Date.now().toString(36)}-${(sequence++).toString(36)}`
/** The id the server deduplicates a send by: a retry of the same send reuses it. */
export const newRequestId = () => `rq-${Date.now().toString(36)}-${(sequence++).toString(36)}-${Math.random().toString(36).slice(2, 8)}`

/** A 402 from the server: the wallet cannot pay. */
function isOutOfCredits(error: unknown): boolean {
  const response = (error as { response?: { status?: number; data?: { detail?: { error?: string } } } })?.response
  return response?.status === 402 || response?.data?.detail?.error === 'insufficient_credits'
}

/** The context of a request, with the learner's current draft when the code chip is on. */
function withDraft(context: MentorContextRef): MentorContextRef {
  if (!context.attachCode || !context.exerciseId) return context
  const code = exerciseDraft(context.exerciseId)
  return code ? { ...context, code } : context
}

/**
 * The Mentor v2 conversation. The server decides the reply, what it costs, what grounds it and what
 * the learner's skills are; this holds only the thread on screen, which context chips are on, which
 * action is chosen, and the credits spent since the balance was read (`creditCost` of each reply,
 * never computed here).
 *
 * The thread shown is the one for the current scope - the attached lesson, or general - the same
 * rule the server uses for history, so a lesson's conversation never appears under another lesson.
 */
export function useMentorV2({ base = DEFAULT_CONTEXT, proactive = false }: Options = {}) {
  const { language } = useMentorV2I18n()
  const [lessonOn, setLessonOn] = useState(true)
  const [codeOn, setCodeOn] = useState(true)
  const context = useMemo(() => buildContext(base, { lesson: lessonOn, code: codeOn }), [base, lessonOn, codeOn])
  const scope = scopeOf(context)
  const [thread, setThread] = useState<{ scope: string; messages: MentorMessageV2[] }>(() => ({ scope, messages: loadThread(scope) }))
  const messages = thread.scope === scope ? thread.messages : loadThread(scope)
  const [loading, setLoading] = useState(false)
  const [failed, setFailure] = useState<Failure | null>(null)
  // A failure belongs to the thread it happened in; switching thread does not carry it along.
  const failure = failed && failed.scope === scope ? failed : null
  const [creditsShort, setCreditsShort] = useState(false)
  const [spent, setSpent] = useState(0)
  const [intent, setIntent] = useState<MentorIntent | null>(null)
  // Bumped after any quiz answer, so the learner model refetches.
  const [learnerVersion, setLearnerVersion] = useState(0)
  const busy = useRef(false)
  // The next send starts a new server-side conversation ("New conversation" was pressed).
  const freshNext = useRef(false)

  useEffect(() => { if (thread.scope === scope) saveThread(thread.messages, thread.scope) }, [thread, scope])

  // This browser has no copy of the thread (another device, or cleared storage): show what the
  // server is continuing, so "explain that" never refers to turns the learner cannot see.
  useEffect(() => {
    if (!mentorV2Live() || loadThread(scope).length > 0) return
    let alive = true
    api.getMentorThread(context.lessonId).then((server) => {
      if (!alive || server.length === 0) return
      setThread((prev) => (prev.scope === scope && prev.messages.length > 0 ? prev : { scope, messages: server }))
    }, () => { /* nothing to show: the thread starts empty */ })
    return () => { alive = false }
  }, [scope, context.lessonId])

  const update = useCallback((change: (prev: MentorMessageV2[]) => MentorMessageV2[]) => {
    setThread((prev) => (prev.scope === scope ? { scope, messages: change(prev.messages) } : { scope, messages: change(loadThread(scope)) }))
  }, [scope])

  useEffect(() => {
    if (!proactive) return
    let alive = true
    mentorV2.proactive(language).then((message) => {
      if (alive && message) update((prev) => (prev.some((m) => m.proactive) && prev.length > 0 ? prev : [...prev, message]))
    }).catch(() => {})
    return () => { alive = false }
    // On arrival only: the server's cooldown decides whether there is a card at all.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const append = useCallback((message: MentorMessageV2) => {
    update((prev) => [...prev, message])
    // A replayed reply answers a send whose own response never arrived here (a timeout, a dropped
    // connection), so its cost - charged once, by the server - has not been counted yet.
    setSpent((n) => n + message.creditCost)
  }, [update])

  const call = useCallback(async (text: string, chosen: MentorIntent | null, requestId: string) => {
    const request = withDraft(context)
    const fresh = freshNext.current
    // A hint on an exercise the mentor can see starts the ladder at level 1; otherwise it is an ordinary message.
    const reply = chosen === 'HINT' && request.exerciseId
      ? await mentorV2.hint({ exerciseId: request.exerciseId, level: 1, lessonId: request.lessonId, code: request.code, requestId }, language)
      : await mentorV2.sendMessage({ text, intent: chosen ?? undefined, context: request, requestId, ...(fresh ? { fresh: true } : {}) }, language)
    freshNext.current = false
    return reply
  }, [context, language])

  const fail = useCallback((error: unknown, attempt: Omit<Failure, 'errorKey' | 'scope'>) => {
    if (isOutOfCredits(error)) setCreditsShort(true)
    else setFailure({ ...attempt, errorKey: mentorErrorKey(error), scope })
  }, [scope])

  const send = useCallback(async (raw: string, explicit?: MentorIntent | null): Promise<boolean> => {
    const chosen = explicit === undefined ? intent : explicit
    const text = raw.trim()
    if (busy.current) return false
    if (!text && !(chosen && NEEDS_NO_TEXT.includes(chosen))) return false
    busy.current = true
    setLoading(true)
    setFailure(null)
    setCreditsShort(false)
    const requestId = newRequestId()
    if (text) {
      update((prev) => [...prev, {
        id: localId('l'), role: 'learner', intent: chosen ?? undefined, creditCost: 0,
        blocks: [{ kind: 'text', text, grounding: 'general' }],
      }])
    }
    try {
      append(await call(text, chosen, requestId))
      setIntent(null)
      return true
    } catch (error) {
      fail(error, { text, intent: chosen ?? null, requestId })
      return false
    } finally {
      busy.current = false
      setLoading(false)
    }
  }, [append, call, fail, intent, update])

  const retry = useCallback(async () => {
    const last = failure
    if (!last || busy.current) return
    // The failed attempt's own message is already in the thread; only the call is repeated - with
    // the same request id, so a send the server did answer is returned, not charged twice.
    setFailure(null)
    busy.current = true
    setLoading(true)
    try {
      append(await call(last.text, last.intent, last.requestId))
    } catch (error) {
      fail(error, last)
    } finally {
      busy.current = false
      setLoading(false)
    }
  }, [append, call, fail, failure])

  /** An inline answer to a "quick check" question goes back as a normal message. */
  const answerCheck = useCallback((answer: string) => send(answer, null), [send])

  const onQuizResult = useCallback(() => setLearnerVersion((v) => v + 1), [])

  const newThread = useCallback(() => {
    update(() => [])
    setFailure(null)
    freshNext.current = true
  }, [update])

  return {
    messages, loading, failure, creditsShort, spent,
    intent, setIntent,
    lessonOn, setLessonOn, codeOn, setCodeOn,
    context,
    learnerVersion,
    send, retry, answerCheck, append, onQuizResult, newThread,
  }
}
