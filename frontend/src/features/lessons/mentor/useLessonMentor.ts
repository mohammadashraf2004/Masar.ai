'use client'
import { useCallback, useRef, useState } from 'react'
import { mentorV2 } from '@/lib/api'
import { useMentorV2I18n, type StringKey } from '@/lib/i18n'
import { mentorErrorKey } from '@/lib/mentorErrors'
import { loadThread, saveThread, scopeOf } from '@/features/mentor/threadStore'
import { newRequestId } from '@/features/mentor/useMentorV2'
import type { MentorIntent, MentorMessageV2 } from '@/features/mentor/types'

export interface PanelExchange {
  /** What the learner selected, shown quoted at the top. */
  quote: string | null
  question: string
  intent: MentorIntent | null
  reply: MentorMessageV2 | null
}

let sequence = 0

/**
 * The in-lesson mentor. A question here carries the lesson's ids and the selected text and nothing
 * else (the server adds the lesson and this lesson's earlier turns); the exchange is appended to the
 * lesson's thread the hub chat reads, so it shows up there too. The lesson page mounts one per
 * lesson (keyed by lesson id), so moving to another lesson starts with an empty panel.
 */
export function useLessonMentor({ courseId, lessonId }: { courseId: string; lessonId: string }) {
  const { language } = useMentorV2I18n()
  const [open, setOpen] = useState(false)
  const [exchanges, setExchanges] = useState<PanelExchange[]>([])
  const [loading, setLoading] = useState(false)
  const [failed, setFailed] = useState<StringKey | null>(null)
  const last = useRef<{ text: string; intent: MentorIntent | null; quote: string | null; requestId: string } | null>(null)

  const run = useCallback(async (text: string, intent: MentorIntent | null, selectedText: string | null, requestId: string) => {
    last.current = { text, intent, quote: selectedText, requestId }
    setOpen(true)
    setLoading(true)
    setFailed(null)
    const exchange: PanelExchange = { quote: selectedText, question: text, intent, reply: null }
    setExchanges((prev) => [...prev, exchange])
    try {
      const context = { courseId, lessonId, ...(selectedText ? { selectedText } : {}) }
      const reply = await mentorV2.sendMessage({ text, intent: intent ?? undefined, context, requestId }, language)
      setExchanges((prev) => prev.map((e) => (e === exchange ? { ...e, reply } : e)))
      const asked: MentorMessageV2 = {
        id: `lp-${Date.now().toString(36)}-${(sequence++).toString(36)}`,
        role: 'learner',
        intent: intent ?? undefined,
        creditCost: 0,
        blocks: [{ kind: 'text', text: selectedText ? `«${selectedText}»\n${text}` : text, grounding: 'general' }],
      }
      const scope = scopeOf(context)
      saveThread([...loadThread(scope), asked, reply], scope)
    } catch (error) {
      // The server refunds a failed reply; the panel says why and keeps the question for a retry.
      setExchanges((prev) => prev.filter((e) => e !== exchange))
      setFailed(mentorErrorKey(error))
    } finally {
      setLoading(false)
    }
  }, [courseId, lessonId, language])

  const ask = useCallback((text: string, intent: MentorIntent | null, selectedText: string | null) =>
    run(text, intent, selectedText, newRequestId()), [run])

  const retry = useCallback(() => {
    // Same request id: a send the server already answered comes back without a second charge.
    if (last.current) void run(last.current.text, last.current.intent, last.current.quote, last.current.requestId)
  }, [run])

  return { open, setOpen, exchanges, loading, failed, ask, retry }
}
