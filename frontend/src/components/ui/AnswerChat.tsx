'use client'
import { useEffect, useRef, useState } from 'react'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { CodeCell } from '@/components/ui/CodeCell'
import { getErrorMessage } from '@/lib/utils'
import type { AnswerChatMessage } from '@/types'
import { Send, CheckCircle, HelpCircle, Bot, User } from 'lucide-react'

interface AnswerChatProps {
  /** Either an exercise id, or a [quizId, questionIndex] pair for an
   * open-ended quiz question. */
  target: { kind: 'exercise'; id: number } | { kind: 'quiz_question'; quizId: number; questionIndex: number }
  /** True when the answer is naturally code (renders an editable, syntax-highlighted code cell). */
  isCode?: boolean
  /** Scaffold code to pre-fill the cell with (e.g. exercise.starter_code) —
   * only applied when there's no conversation yet, so it never clobbers an
   * in-progress or already-submitted answer. */
  starterCode?: string
  placeholder?: string
}

export function AnswerChat({ target, isCode, starterCode, placeholder }: AnswerChatProps) {
  const { language, mode } = useI18n()
  const [messages, setMessages] = useState<AnswerChatMessage[]>([])
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null)
  const [draft, setDraft] = useState('')
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)

  const key = target.kind === 'exercise' ? `ex-${target.id}` : `q-${target.quizId}-${target.questionIndex}`

  // Reset when the thread being viewed changes — render-phase adjustment
  // rather than an effect, so there is no extra commit-then-rerender pass.
  const [trackedKey, setTrackedKey] = useState(key)
  if (key !== trackedKey) {
    setTrackedKey(key)
    setLoading(true)
    setMessages([])
    setIsCorrect(null)
  }

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const data = target.kind === 'exercise'
          ? await api.getExerciseAnswer(target.id)
          : await api.getQuizQuestionAnswer(target.quizId, target.questionIndex)
        if (!cancelled) {
          setMessages(data.messages)
          setIsCorrect(data.is_correct)
        }
      } catch {
        // 404 = no conversation yet, start with an empty thread —
        // pre-fill the scaffold code for the student to complete.
        if (!cancelled && isCode && starterCode) setDraft(starterCode)
      }
      if (!cancelled) setLoading(false)
    }
    load()
    return () => { cancelled = true }
  }, [key]) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function send() {
    if (!draft.trim() || sending) return
    setSending(true)
    setError('')
    const content = draft
    setDraft('')
    // Optimistic: show the user's message immediately.
    setMessages(prev => [...prev, { role: 'user', content }])
    try {
      // Same language settings as the mentor: the grader explains in the
      // reader's language and keeps terminology and code in English.
      const prefs = { language, terminology_mode: mode }
      const data = target.kind === 'exercise'
        ? await api.answerExercise(target.id, content, prefs)
        : await api.answerQuizQuestion(target.quizId, target.questionIndex, content, prefs)
      setMessages(data.messages)
      setIsCorrect(data.is_correct)
    } catch (err) {
      setError(getErrorMessage(err))
      // Roll back the optimistic message on failure.
      setMessages(prev => prev.slice(0, -1))
      setDraft(content)
    }
    setSending(false)
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      e.preventDefault()
      send()
    }
  }

  if (loading) {
    return <div className="flex justify-center py-6"><Spinner className="w-4 h-4" /></div>
  }

  return (
    <div className="rounded-lg border border-border overflow-hidden bg-surface">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-border bg-ink">
        <div className="flex items-center gap-2">
          <Bot size={13} className="text-amber" />
          <span className="text-xs font-medium text-ghost">AI evaluator</span>
        </div>
        {isCorrect === true && (
          <span className="flex items-center gap-1 text-xs text-emerald">
            <CheckCircle size={12} /> Correct
          </span>
        )}
        {isCorrect === false && (
          <span className="flex items-center gap-1 text-xs text-amber">
            <HelpCircle size={12} /> Keep going
          </span>
        )}
      </div>

      <div className="max-h-96 overflow-y-auto px-4 py-4 space-y-3">
        {messages.length === 0 && (
          <p className="text-xs text-ghost text-center py-4">
            Write your answer below — an AI will discuss it with you like a mentor, not just mark it right or wrong.
          </p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex gap-2.5 ${m.role === 'user' ? 'justify-end' : ''}`}>
            {m.role === 'assistant' && (
              <div className="w-6 h-6 rounded-full bg-amber/10 border border-amber/20 flex items-center justify-center shrink-0 mt-0.5">
                <Bot size={12} className="text-amber" />
              </div>
            )}
            <div className={`max-w-[85%] rounded-lg px-3.5 py-2.5 text-sm leading-relaxed whitespace-pre-wrap ${
              m.role === 'user'
                ? 'bg-amber/10 border border-amber/20 text-bright'
                : 'bg-void border border-border text-soft'
            }`}>
              {m.content}
            </div>
            {m.role === 'user' && (
              <div className="w-6 h-6 rounded-full bg-surface border border-border flex items-center justify-center shrink-0 mt-0.5">
                <User size={12} className="text-ghost" />
              </div>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {error && (
        <div className="mx-4 mb-2 px-3 py-2 rounded bg-rose/10 border border-rose/20 text-xs text-rose">
          {error}
        </div>
      )}

      <div className="p-3 border-t border-border">
        {isCode ? (
          <div className="space-y-2" onKeyDown={handleKeyDown}>
            <CodeCell
              value={draft}
              onChange={setDraft}
              placeholder={placeholder ?? '# Write your solution here…'}
            />
            <div className="flex items-center justify-between">
              <span className="text-xs text-ghost">⌘/Ctrl+Enter to submit</span>
              <Button size="sm" onClick={send} loading={sending} disabled={!draft.trim()}>
                <Send size={13} /> Submit code
              </Button>
            </div>
          </div>
        ) : (
          <div className="flex items-end gap-2">
            <textarea
              className="flex-1 bg-void border border-border rounded-lg px-3 py-2.5 text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 resize-none min-h-[44px] max-h-40"
              placeholder={placeholder ?? 'Write your answer… (⌘/Ctrl+Enter to send)'}
              value={draft}
              onChange={e => setDraft(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={2}
            />
            <Button size="sm" onClick={send} loading={sending} disabled={!draft.trim()}>
              <Send size={13} />
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}
