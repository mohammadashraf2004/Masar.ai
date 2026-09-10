'use client'
import { useState } from 'react'
import { AlertCircle, CheckCircle, Lightbulb, Send, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { CodeCell } from '@/components/ui/CodeCell'
import { api } from '@/lib/api'
import { getErrorMessage } from '@/lib/utils'
import type { CodeReviewResult, Project, ProjectHint } from '@/types'

/**
 * Project submission: write the code, get it reviewed, ask for a hint when
 * stuck.
 *
 * What this replaces: a "GitHub repo URL" input next to a description box.
 * The URL was never fetched by anything — the *description* was what got
 * sent to the AI reviewer — so the form asked for a repo and then reviewed
 * a paragraph about it. Now the code cell holds the actual solution (the
 * same cell exercises use), notes are optional context, and the repo field
 * is gone rather than left there implying a review that never happened.
 *
 * Every outcome stays visible — saved, saved-without-review, or failed with
 * the server's reason — and the button refuses to fire with an empty cell,
 * which the API now also enforces.
 */
export function ProjectSubmit({ project }: { project: Project }) {
  const [open, setOpen] = useState(false)
  const [code, setCode] = useState('')
  const [notes, setNotes] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [submitted, setSubmitted] = useState<{
    at: string
    review: CodeReviewResult | null
  } | null>(null)

  // ── Hints ──
  const [hintsOpen, setHintsOpen] = useState(false)
  const [stuckOn, setStuckOn] = useState('')
  const [hints, setHints] = useState<ProjectHint[]>([])
  const [hintLoading, setHintLoading] = useState(false)
  const [hintError, setHintError] = useState('')

  const canSubmit = code.trim().length > 0

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    if (!canSubmit || submitting) return

    setSubmitting(true)
    setError('')
    try {
      const result = await api.submitProject(project.id, {
        code,
        // Sent only when actually filled in — the server caps it at 2k.
        description: notes.trim() || undefined,
      })
      setSubmitted({ at: result.submitted_at, review: result.ai_review ?? null })
      setOpen(false)
    } catch (err) {
      setError(getErrorMessage(err))
    }
    setSubmitting(false)
  }

  async function askForHint() {
    if (!stuckOn.trim() || hintLoading) return
    setHintLoading(true)
    setHintError('')
    try {
      const result = await api.getProjectHint(project.id, {
        stuck_on: stuckOn,
        // The tutor sees whatever is in the cell, so it can point at the
        // actual bug instead of guessing at the brief.
        code: code.trim() || undefined,
        previous_hints: hints.map((h) => h.hint),
      })
      setHints((prev) => [...prev, result])
      setStuckOn('')
    } catch (err) {
      // Same 402 shape the challenge hint returns.
      const detail = (err as { response?: { data?: { detail?: unknown } } })?.response?.data?.detail
      if (typeof detail === 'object' && detail !== null && 'error' in detail
          && (detail as { error?: string }).error === 'insufficient_credits') {
        setHintError('Not enough credits for a hint. Top up from your wallet.')
      } else {
        setHintError(getErrorMessage(err))
      }
    }
    setHintLoading(false)
  }

  return (
    <div className="space-y-3">
      {!submitted && (
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={() => setOpen((o) => !o)}>
            Submit project
          </Button>
          <Button variant="ghost" size="sm" onClick={() => setHintsOpen((o) => !o)}>
            <Lightbulb size={13} /> Need help?
          </Button>
        </div>
      )}

      {/* ── Hints: available while working, not only after submitting ── */}
      {hintsOpen && !submitted && (
        <div className="space-y-3 border-t border-border pt-4">
          <p className="text-xs text-ghost leading-relaxed">
            Describe what you&apos;re stuck on. The mentor gives a hint that points you at the
            right idea — it won&apos;t write the project for you. Costs 1 credit per hint.
          </p>

          <div className="flex items-start gap-2">
            <input
              className="flex-1 bg-surface border border-border rounded px-3 py-2 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50"
              placeholder="e.g. my merge produces duplicate rows"
              value={stuckOn}
              onChange={(e) => setStuckOn(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault()
                  void askForHint()
                }
              }}
            />
            <Button
              size="sm"
              loading={hintLoading}
              disabled={!stuckOn.trim()}
              onClick={() => void askForHint()}
            >
              <Lightbulb size={13} /> Hint
            </Button>
          </div>

          {hintError && (
            <div className="flex items-start gap-2 px-3 py-2 rounded bg-rose/10 border border-rose/20">
              <AlertCircle size={13} className="text-rose shrink-0 mt-0.5" />
              <p className="text-xs text-rose leading-relaxed">{hintError}</p>
            </div>
          )}

          {hints.map((h, i) => (
            <div key={i} className="p-3 rounded bg-surface border border-border space-y-1.5">
              <div className="flex items-center gap-1.5">
                <Lightbulb size={12} className="text-amber" />
                <span className="text-[11px] font-medium uppercase tracking-wider text-amber">
                  Hint {i + 1}
                </span>
              </div>
              <p className="text-xs text-soft leading-relaxed">{h.hint}</p>
              {h.concept && (
                <p className="text-xs text-dim">
                  Look up:{' '}
                  <span className="font-mono text-bright" dir="ltr">{h.concept}</span>
                </p>
              )}
              {h.next_step && (
                <p className="text-xs text-dim leading-relaxed">Next: {h.next_step}</p>
              )}
            </div>
          ))}
        </div>
      )}

      {open && (
        <form onSubmit={submit} className="space-y-3 border-t border-border pt-4">
          <div className="space-y-1.5">
            <label className="text-[11px] font-medium uppercase tracking-wider text-amber">
              Your solution
            </label>
            <CodeCell
              value={code}
              onChange={setCode}
              placeholder="# Write your solution here"
              minHeight={200}
            />
          </div>

          <textarea
            className="w-full bg-surface border border-border rounded px-3 py-2 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 min-h-16 resize-none"
            placeholder="Optional: notes on your approach and key decisions."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            maxLength={2000}
          />

          <div className="flex items-center gap-3">
            <Button type="submit" size="sm" loading={submitting} disabled={!canSubmit}>
              <Send size={13} /> Submit for AI review
            </Button>
            {!canSubmit && (
              <span className="text-xs text-ghost">Write your code first.</span>
            )}
          </div>
        </form>
      )}

      {error && (
        <div className="flex items-start gap-2 px-3 py-2 rounded bg-rose/10 border border-rose/20">
          <AlertCircle size={13} className="text-rose shrink-0 mt-0.5" />
          <p className="text-xs text-rose leading-relaxed">{error}</p>
        </div>
      )}

      {submitted && (
        <div className="space-y-3">
          <div className="flex items-start gap-2 px-3 py-2.5 rounded bg-emerald/5 border border-emerald/20">
            <CheckCircle size={13} className="text-emerald shrink-0 mt-0.5" />
            <div>
              <p className="text-xs text-emerald font-medium">Submitted</p>
              <p className="text-xs text-ghost mt-0.5">
                {new Date(submitted.at).toLocaleString()}
              </p>
            </div>
          </div>

          {submitted.review ? (
            <div className="p-4 rounded bg-surface border border-border">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles size={13} className="text-amber" />
                <span className="text-sm font-medium text-bright">
                  AI review — {submitted.review.score}/100
                </span>
              </div>
              <p className="text-xs text-soft leading-relaxed">{submitted.review.summary}</p>
              {submitted.review.improvements?.length > 0 && (
                <ul className="mt-2.5 space-y-1">
                  {submitted.review.improvements.slice(0, 3).map((item) => (
                    <li key={item} className="text-xs text-dim leading-relaxed ps-2.5 border-s border-border">
                      {item}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ) : (
            // Saved, but the reviewer was unreachable — a provider outage
            // must not cost the student their submission.
            <p className="text-xs text-ghost leading-relaxed">
              Saved, but the AI review didn&apos;t come back this time. Submit again to retry it.
            </p>
          )}

          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              setSubmitted(null)
              setOpen(true)
            }}
          >
            Submit again
          </Button>
        </div>
      )}
    </div>
  )
}
