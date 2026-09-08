'use client'
import { useEffect, useRef, useState } from 'react'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { CodeCell } from '@/components/ui/CodeCell'
import { getErrorMessage } from '@/lib/utils'
import type { AnswerChatMessage } from '@/types'
import { Send, CheckCircle, HelpCircle, Bot, User, Code2, Undo2, RotateCcw } from 'lucide-react'

interface AnswerChatProps {
  /** Either an exercise id, or a [quizId, questionIndex] pair for an
   * open-ended quiz question. */
  target: { kind: 'exercise'; id: number } | { kind: 'quiz_question'; quizId: number; questionIndex: number }
  /** True when the answer is naturally code — renders the editor as its own
   * panel above the conversation, rather than as the chat's input box. */
  isCode?: boolean
  /** The exercise's scaffold. Pre-fills the editor on a fresh attempt and is
   * what "Start again" restores. */
  starterCode?: string
  placeholder?: string
}

/** Typing is grouped into undo steps by time: a burst of keystrokes is one
 *  step, so Undo moves back a meaningful edit rather than a character. */
const UNDO_COALESCE_MS = 600
/** Enough to walk back through a whole attempt; bounded so a long session
 *  can't grow the array without limit. */
const UNDO_LIMIT = 100

export function AnswerChat({ target, isCode, starterCode, placeholder }: AnswerChatProps) {
  const { language, mode } = useI18n()
  const [messages, setMessages] = useState<AnswerChatMessage[]>([])
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null)
  const [draft, setDraft] = useState('')
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')
  // Previous editor contents, oldest first. `draft` is the present, so the
  // last entry is what Undo restores.
  const [history, setHistory] = useState<string[]>([])
  const lastSnapshotAt = useRef(0)
  const bottomRef = useRef<HTMLDivElement>(null)

  const key = target.kind === 'exercise' ? `ex-${target.id}` : `q-${target.quizId}-${target.questionIndex}`
  const baseline = starterCode ?? ''

  // Reset when the thread being viewed changes — render-phase adjustment
  // rather than an effect, so there is no extra commit-then-rerender pass.
  const [trackedKey, setTrackedKey] = useState(key)
  if (key !== trackedKey) {
    setTrackedKey(key)
    setLoading(true)
    setMessages([])
    setIsCorrect(null)
    setHistory([])
    // The coalescing timestamp is deliberately NOT reset here: a ref must
    // not be written during render. It does not need to be — `history` is
    // empty above, and editDraft always snapshots when the history is
    // empty, whatever the timestamp says. The effect below clears it
    // anyway, for tidiness rather than correctness.
  }

  useEffect(() => {
    let cancelled = false
    lastSnapshotAt.current = 0
    async function load() {
      try {
        const data = target.kind === 'exercise'
          ? await api.getExerciseAnswer(target.id)
          : await api.getQuizQuestionAnswer(target.quizId, target.questionIndex)
        if (!cancelled) {
          setMessages(data.messages)
          setIsCorrect(data.is_correct)
          // Bring the student's most recent submission back into the editor
          // so a reload lands them where they left off, ready to edit. The
          // conversation already shows this text, so nothing is revealed
          // that wasn't on screen before.
          if (isCode) {
            const lastFromStudent = [...data.messages].reverse().find(m => m.role === 'user')
            if (lastFromStudent) setDraft(lastFromStudent.content)
            else if (starterCode) setDraft(starterCode)
          }
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

  // ── Undo history ────────────────────────────────────────────────────────
  /** Record `value` as an undo point unconditionally — for discrete actions
   *  (Start again) where every press should be reversible. */
  function snapshot(value: string) {
    lastSnapshotAt.current = Date.now()
    setHistory(h => [...h, value].slice(-UNDO_LIMIT))
  }

  /** The editor's onChange. Snapshots the *previous* text, coalescing a run
   *  of fast keystrokes into a single undo step. */
  function editDraft(next: string) {
    const now = Date.now()
    if (history.length === 0 || now - lastSnapshotAt.current > UNDO_COALESCE_MS) {
      lastSnapshotAt.current = now
      setHistory(h => [...h, draft].slice(-UNDO_LIMIT))
    }
    setDraft(next)
  }

  function undo() {
    if (history.length === 0) return
    // Read the entry out here rather than inside a state updater: React can
    // call an updater twice (StrictMode, concurrent rendering), and an
    // updater that also sets other state would then undo two steps.
    const previous = history[history.length - 1]
    setHistory(h => h.slice(0, -1))
    setDraft(previous)
    // The next keystroke starts a fresh undo step instead of coalescing
    // into the one we just consumed.
    lastSnapshotAt.current = 0
  }

  function startAgain() {
    if (draft === baseline) return
    snapshot(draft)   // so Undo rescues an accidental press
    setDraft(baseline)
  }

  async function send() {
    if (!draft.trim() || sending) return
    setSending(true)
    setError('')
    const content = draft
    // A code answer stays in the editor after submitting: the next move is
    // almost always to fix it and resubmit, and clearing it meant retyping
    // the whole solution. A prose answer is a chat message, so the box
    // empties the way a chat box should.
    if (!isCode) setDraft('')
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
      if (!isCode) setDraft(content)
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

  // ── The conversation, as its own panel ─────────────────────────────────
  const conversation = (
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
            {isCode
              ? 'Submit your code above and the AI will tell you exactly what to fix — not just whether it is right.'
              : 'Write your answer below — an AI will discuss it with you like a mentor, not just mark it right or wrong.'}
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

      {/* Prose answers are written here; code has its own panel above. */}
      {!isCode && (
        <div className="p-3 border-t border-border">
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
        </div>
      )}
    </div>
  )

  if (!isCode) return conversation

  // ── Code: editor and conversation are separate panels ──────────────────
  // They used to share one card, with the editor as the chat's input box.
  // That made "read the feedback, then fix the code" a scroll back and
  // forth inside a single scrolling region, and submitting cleared the
  // editor — so editing an answer again meant retyping it.
  return (
    <div className="space-y-3">
      <div className="rounded-lg border border-border overflow-hidden bg-surface">
        <div className="flex items-center justify-between px-4 py-2.5 border-b border-border bg-ink">
          <div className="flex items-center gap-2">
            <Code2 size={13} className="text-amber" />
            <span className="text-xs font-medium text-ghost">Your code</span>
          </div>
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={undo}
              disabled={history.length === 0}
              title="Undo the last edit"
              className="inline-flex items-center gap-1 px-2 py-1 rounded text-[11px] text-ghost border border-border hover:text-bright hover:border-amber/30 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            >
              <Undo2 size={11} /> Undo
            </button>
            <button
              type="button"
              onClick={startAgain}
              disabled={draft === baseline}
              title="Restore the starter code"
              className="inline-flex items-center gap-1 px-2 py-1 rounded text-[11px] text-ghost border border-border hover:text-bright hover:border-amber/30 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            >
              <RotateCcw size={11} /> Start again
            </button>
          </div>
        </div>

        <div className="p-3 space-y-2" onKeyDown={handleKeyDown}>
          <CodeCell
            value={draft}
            onChange={editDraft}
            placeholder={placeholder ?? '# Write your solution here…'}
          />
          <div className="flex items-center justify-between">
            <span className="text-xs text-ghost">⌘/Ctrl+Enter to submit</span>
            <Button size="sm" onClick={send} loading={sending} disabled={!draft.trim()}>
              <Send size={13} /> Submit code
            </Button>
          </div>
        </div>
      </div>

      {conversation}
    </div>
  )
}
