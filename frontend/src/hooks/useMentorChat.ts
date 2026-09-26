'use client'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { api } from '@/lib/api'
import type { StringKey } from '@/lib/i18n'
import { mentorErrorKey } from '@/lib/mentorErrors'
import { getMentorQuota, type MentorQuota, type QuotaStatus } from '@/lib/mentor/quota'
import type { LanguagePrefs } from '@/types'
import type { MentorMessage, MentorSession } from '@/types'

export interface Thread {
  id: number
  title: string
  /** ISO time the conversation last changed. */
  at: string
  messages: MentorMessage[]
}

const TITLE_LENGTH = 50

/**
 * A thread is labelled by the first thing the learner said in it, cut to 50 characters, never by
 * the API's title: that is the same text for a session `chat` created, but a session made by "new
 * conversation" is called "New Session" for good. A thread with nothing said yet has no label
 * (the list shows a neutral one).
 */
export function threadTitle(session: Pick<MentorSession, 'messages'>): string {
  const first = session.messages?.find((m) => m.role === 'user')?.content?.trim()
  return first ? first.slice(0, TITLE_LENGTH) : ''
}

export function toThread(session: MentorSession): Thread {
  return {
    id: session.id,
    title: threadTitle(session),
    at: session.updated_at ?? session.created_at,
    messages: (session.messages ?? []).map((m) => ({
      role: m.role,
      content: m.content,
      timestamp: m.timestamp,
    })),
  }
}

interface Options {
  prefs: LanguagePrefs
  /** The mentor's first line, in the reader's language. */
  greeting: string
  /** The page's query string, for `?mockQuotaUsed=`. */
  search: string
}

/**
 * The mentor conversation: what the API supports, and no more.
 *
 * - Replies arrive whole (the API does not stream), so "the mentor is typing" is the wait.
 * - Threads are the API's sessions. It always continues the *latest* one (`/mentor/chat` takes no
 *   session id), so an earlier thread can be read but not continued: sending from it goes to the
 *   latest, which the page says.
 * - The daily message quota is `MockMentorQuota` (see lib/mentor/quota.ts); the real limit today
 *   is the wallet, and a 402 raises the same upsell.
 */
export function useMentorChat({ prefs, greeting, search }: Options) {
  const greetingMessage = useCallback(
    (): MentorMessage => ({ role: 'assistant', content: greeting, timestamp: new Date().toISOString() }),
    [greeting],
  )

  const [threads, setThreads] = useState<Thread[]>([])
  const [threadsLoaded, setThreadsLoaded] = useState(false)
  // The conversation the composer writes to (the latest one), and the earlier one being read.
  const [messages, setMessages] = useState<MentorMessage[]>(() => [
    { role: 'assistant', content: greeting, timestamp: new Date(0).toISOString() },
  ])
  const [viewing, setViewing] = useState<Thread | null>(null)
  const [loading, setLoading] = useState(false)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [online, setOnline] = useState(true)
  const [creditsShort, setCreditsShort] = useState(false)
  const [quota, setQuota] = useState<MentorQuota | null>(null)
  const [quotaStatus, setQuotaStatus] = useState<QuotaStatus | null>(null)
  // Messages delivered since the page opened: each cost credits the wallet balance (read once)
  // does not yet reflect.
  const [delivered, setDelivered] = useState(0)
  const busy = useRef(false)
  const started = useRef(false)

  useEffect(() => {
    const q = getMentorQuota(search)
    setQuota(q)
    setQuotaStatus(q ? q.status() : null)
    // The quota is read once, on arrival: `?mockQuotaUsed=` sets the count and must not
    // be applied again when the page's query string changes for another reason.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const refreshThreads = useCallback(async () => {
    try {
      const sessions = await api.getMentorSessions()
      // Latest first: the API's own order puts a session with no `updated_at` (a fresh one) first
      // and is otherwise by that time, so sort by the time shown rather than trust it.
      const next = sessions.map(toThread).sort((a, b) => Date.parse(b.at) - Date.parse(a.at))
      setThreads(next)
      return next
    } catch {
      return null
    } finally {
      setThreadsLoaded(true)
    }
  }, [])

  // Arrive on the latest conversation, as the API will continue it.
  useEffect(() => {
    if (started.current) return
    started.current = true
    void (async () => {
      const next = await refreshThreads()
      const latest = next?.[0]
      if (latest && latest.messages.length > 0) setMessages(latest.messages)
    })()
  }, [refreshThreads])

  const send = useCallback(
    async (text: string): Promise<boolean> => {
      const content = text.trim()
      if (!content || busy.current) return false
      if (quota && quota.status().exhausted) return false
      busy.current = true
      setViewing(null)
      setSuggestions([])
      setCreditsShort(false)
      setMessages((prev) => [...prev, { role: 'user', content, timestamp: new Date().toISOString() }])
      setLoading(true)
      try {
        // The mentor answers in the reader's language and terminology mode: the same policy the
        // lessons follow, applied server-side.
        const res = await api.chat(content, undefined, prefs)
        setMessages((prev) => [...prev, { role: 'assistant', content: res.reply, timestamp: new Date().toISOString() }])
        setSuggestions(res.suggested_actions ?? [])
        setOnline(true)
        setDelivered((n) => n + 1)
        if (quota) setQuotaStatus(quota.consume())
        void refreshThreads()
        return true
      } catch (err) {
        const key: StringKey = mentorErrorKey(err)
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: key, timestamp: new Date().toISOString(), error: true },
        ])
        if (key === 'mentor.error.credits') setCreditsShort(true)
        setOnline(key !== 'mentor.error.network' && key !== 'mentor.error.unavailable')
        return false
      } finally {
        busy.current = false
        setLoading(false)
      }
    },
    [prefs, quota, refreshThreads],
  )

  const newConversation = useCallback(async () => {
    if (busy.current) return
    busy.current = true
    try {
      await api.newMentorSession()
      setMessages([greetingMessage()])
      setViewing(null)
      setSuggestions([])
      setCreditsShort(false)
      void refreshThreads()
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: mentorErrorKey(err), timestamp: new Date().toISOString(), error: true },
      ])
    } finally {
      busy.current = false
    }
  }, [greetingMessage, refreshThreads])

  const openThread = useCallback(
    (id: number) => {
      const thread = threads.find((t) => t.id === id)
      if (!thread) return
      // The first one is the latest: the one the API continues, so it is simply the conversation.
      if (threads[0]?.id === id) {
        setViewing(null)
        setMessages(thread.messages.length > 0 ? thread.messages : [greetingMessage()])
        return
      }
      setViewing(thread)
    },
    [threads, greetingMessage],
  )

  const backToLatest = useCallback(() => setViewing(null), [])

  // Error bubbles carry a message key so they follow the reader's language; everything else is text.
  const shown = useMemo(() => (viewing ? viewing.messages : messages), [viewing, messages])

  return {
    messages: shown,
    viewing,
    threads,
    threadsLoaded,
    activeThreadId: viewing?.id ?? threads[0]?.id ?? null,
    loading,
    suggestions,
    online,
    creditsShort,
    delivered,
    quota,
    quotaStatus,
    send,
    newConversation,
    openThread,
    backToLatest,
  }
}
