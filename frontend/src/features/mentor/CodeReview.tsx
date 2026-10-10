'use client'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { codeCellColors } from '@/features/exercises/CodeCell/codeCellTheme'
import { Card } from '@/components/ui/index'
import { api, mentorV2 } from '@/lib/api'
import { useI18n, useMentorV2I18n, type MentorV2Key, type StringKey } from '@/lib/i18n'
import { mentorErrorKey } from '@/lib/mentorErrors'
import { cn } from '@/lib/utils'
import { exerciseFileName } from '@/features/exercises/lessonExerciseFiles'
import { contextLabels } from './context'
import { exerciseDraft } from './draft'
import type { ReviewResult, ReviewSeverity } from './types'
import { newRequestId } from './useMentorV2'

/** The code surface keeps the dark palette in both themes (the same one the exercise cell uses). */
const SEVERITY_COLOR: Record<ReviewSeverity, string> = { ok: '#10B981', suggestion: '#F59E0B', issue: '#F43F5E' }
const SEVERITY_TEXT: Record<ReviewSeverity, string> = { ok: 'text-emerald', suggestion: 'text-amber-text', issue: 'text-rose' }

/** What the learner has in the exercise: their saved draft (in whatever language the exercise is),
 * or '' when they have not edited it - the starter is then fetched. Reading it is all a review does. */
export function exerciseCode(exerciseId: string, language?: string | null): string {
  return (exerciseId && exerciseDraft(exerciseId, language)) || ''
}

/**
 * A static review of the learner's code (Mentor v2 §2b). The server reads the code and comments on
 * lines; it never runs it, and the panel says so on its tab bar. Selecting a commented line opens its
 * comment under it and highlights the matching note in the aside, and the other way round.
 */
export function CodeReview({ exerciseId }: { exerciseId?: string }) {
  const { t, tf, n, language } = useMentorV2I18n()
  const { t: tMain } = useI18n()
  const id = exerciseId ?? ''
  // The exercise's own language decides the file the draft is under and what the reviewer is told.
  const [codeLanguage, setCodeLanguage] = useState<string | null>(null)
  const [pasted, setPasted] = useState<string | null>(null)
  const [pasting, setPasting] = useState(false)
  const [draft, setDraft] = useState('')
  // What the learner has now. The hub keys this component by exercise, so a new exercise starts fresh.
  const [code, setCode] = useState(() => exerciseCode(id))
  const [result, setResult] = useState<ReviewResult | null>(null)
  const [selected, setSelected] = useState<number | null>(null)
  const [busy, setBusy] = useState(false)
  const [failed, setFailed] = useState<StringKey | null>(null)
  // The review that has not been answered yet. Trying the same code again after a failure or a
  // timeout reuses its request id, so the server answers and charges it once (it may still be
  // running, or have finished after the browser gave up); any other review gets a new id.
  const unanswered = useRef<{ text: string; forExercise: boolean; requestId: string } | null>(null)

  useEffect(() => {
    if (!id) return
    let stale = false
    api.getCodeExercise(id).then(
      (exercise) => {
        if (stale) return
        setCodeLanguage(exercise.language ?? 'python')
        setCode(exerciseCode(id, exercise.language) || exercise.starter_code || '')
      },
      () => { /* The review button remains disabled until code is pasted. */ },
    )
    return () => { stale = true }
  }, [id])

  const source = pasted ?? code
  const fileName = pasted !== null ? 'pasted.py' : exerciseFileName(codeLanguage)
  const labels = contextLabels({ exerciseId: id }, language, n)

  const fetchReview = useCallback((text: string, forExercise: boolean, requestId: string) => {
    const lang = forExercise ? codeLanguage ?? 'python' : 'python'
    const body = forExercise ? { exerciseId: id, code: text, lang, requestId } : { code: text, lang, requestId }
    return mentorV2.review(body, language)
  }, [codeLanguage, id, language])

  const apply = useCallback((next: ReviewResult) => {
    setResult(next)
    setSelected(next.comments.find((c) => c.severity !== 'ok')?.line ?? next.comments[0]?.line ?? null)
    setBusy(false)
  }, [])

  const run = useCallback((text: string, forExercise: boolean) => {
    setBusy(true)
    setFailed(null)
    const previous = unanswered.current
    const requestId = previous && previous.text === text && previous.forExercise === forExercise ? previous.requestId : newRequestId()
    unanswered.current = { text, forExercise, requestId }
    fetchReview(text, forExercise, requestId).then(
      (next) => { unanswered.current = null; apply(next) },
      (error) => { setFailed(mentorErrorKey(error)); setBusy(false) },
    )
  }, [apply, fetchReview])

  const byLine = useMemo(() => new Map((result?.comments ?? []).map((c) => [c.line, c])), [result])
  const lines = source.split('\n')

  function reviewAgain() {
    // Prefer a newly saved draft, but keep the fetched starter when no draft exists.
    const fresh = (pasted ?? exerciseCode(id, codeLanguage)) || code
    if (pasted === null) setCode(fresh)
    run(fresh, pasted === null)
  }

  return (
    <div className="flex flex-wrap items-start gap-5">
      <div className="flex min-w-0 flex-[2_1_520px] flex-col gap-3.5">
        <div className="flex flex-wrap items-center gap-2.5 text-xs">
          <span className="text-dim">{t('mentor.v2.review.source')}</span>
          <span dir="ltr" className="rounded-full border border-amber bg-amber-soft px-2.5 py-1 font-mono text-amber-text">
            {pasted !== null ? 'pasted.py' : labels.code ?? 'agent.py'}
          </span>
          <button
            type="button"
            onClick={() => setPasting((v) => !v)}
            className="min-h-[44px] rounded-lg border border-border px-3 text-[13px] text-bright hover:border-amber/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring lg:min-h-[36px]"
          >
            {t('mentor.v2.review.paste')}
          </button>
          <button
            type="button"
            disabled={busy || !source.trim()}
            onClick={() => run(source, pasted === null && Boolean(id))}
            className="min-h-[44px] rounded-lg bg-amber px-4 text-[13px] font-semibold text-on-amber disabled:opacity-40 lg:min-h-[36px]"
          >
            {t('mentor.v2.review.request')}
          </button>
        </div>

        {pasting && (
          <form
            className="flex flex-col gap-2"
            onSubmit={(e) => {
              e.preventDefault()
              if (!draft.trim()) return
              setPasted(draft)
              setPasting(false)
              run(draft, false)
            }}
          >
            <textarea
              dir="ltr"
              rows={6}
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              aria-label={t('mentor.v2.review.pastePlaceholder')}
              placeholder={t('mentor.v2.review.pastePlaceholder')}
              className="w-full resize-y rounded-lg border border-border bg-void px-3 py-2.5 font-mono text-xs leading-[1.7] text-bright placeholder:text-ghost focus:border-amber/50 focus:outline-none"
            />
            <div className="flex gap-2">
              <button type="submit" disabled={!draft.trim()} className="min-h-[44px] rounded-lg bg-amber px-4 text-[13px] font-semibold text-on-amber disabled:opacity-40">{t('mentor.v2.review.pasteSubmit')}</button>
              <button type="button" onClick={() => setPasting(false)} className="min-h-[44px] rounded-lg border border-border px-4 text-[13px] text-bright">{t('mentor.v2.review.pasteCancel')}</button>
            </div>
          </form>
        )}

        <section
          dir="ltr"
          aria-label={fileName}
          className="min-w-0 overflow-hidden rounded-xl border"
          style={{ background: codeCellColors.background, borderColor: codeCellColors.line }}
        >
          <div className="flex h-[42px] items-center border-b px-3" style={{ background: codeCellColors.chrome, borderColor: codeCellColors.line }}>
            <span className="relative px-1 py-1.5 font-mono text-xs" style={{ color: codeCellColors.bright }}>
              {fileName}
              <span aria-hidden="true" className="absolute inset-x-0 bottom-0 h-0.5" style={{ background: codeCellColors.amber }} />
            </span>
            <span className="ms-auto font-mono text-xs" style={{ color: codeCellColors.muted }}>{t('mentor.v2.review.static')}</span>
          </div>

          <div className="overflow-x-auto py-3.5" data-testid="review-code">
            {lines.map((line, index) => {
              const number = index + 1
              const comment = byLine.get(number)
              const active = selected === number
              const row = (
                <>
                  <span aria-hidden="true" className="w-11 shrink-0 select-none pe-3.5 text-end" style={{ color: codeCellColors.gutter }}>{number}</span>
                  <span className="min-w-0 flex-1 whitespace-pre" style={{ color: codeCellColors.text }}>{line || ' '}</span>
                  {comment && <span aria-hidden="true" data-severity={comment.severity} className="me-3 ms-2 mt-[9px] h-2 w-2 shrink-0 rounded-full" style={{ background: SEVERITY_COLOR[comment.severity] }} />}
                </>
              )
              const rowClass = 'flex w-full min-w-max font-mono text-[12.5px] leading-[1.75]'
              return (
                <div key={number}>
                  {comment ? (
                    <button
                      type="button"
                      aria-expanded={active}
                      aria-label={`${tf('mentor.v2.review.line', { n: number })}: ${comment.title}`}
                      onClick={() => setSelected(active ? null : number)}
                      className={cn(rowClass, 'text-start focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring')}
                      style={{ background: active ? 'rgba(245,158,11,.10)' : undefined }}
                    >
                      {row}
                    </button>
                  ) : (
                    <div className={rowClass}>{row}</div>
                  )}
                  {comment && active && (
                    <div
                      dir="rtl"
                      role="note"
                      className="my-1.5 me-3 rounded-lg border p-3 text-start"
                      style={{ background: '#111620', borderColor: SEVERITY_COLOR[comment.severity], marginInlineStart: 44 }}
                    >
                      <p className="text-[13px] font-semibold" style={{ color: SEVERITY_COLOR[comment.severity] }}>{comment.title}</p>
                      <p className="mt-1 text-[13px] leading-[1.7]" style={{ color: codeCellColors.text }}>{comment.text}</p>
                    </div>
                  )}
                </div>
              )
            })}
            {!source && <p className="px-4 font-mono text-xs" style={{ color: codeCellColors.muted }}>{t('mentor.v2.review.noNotes')}</p>}
          </div>
        </section>
        {failed && <p role="alert" className="text-xs text-rose">{tMain(failed)}</p>}
      </div>

      <div className="flex min-w-0 flex-[1_1_300px] flex-col gap-5">
        <Card className="flex flex-col gap-3 p-5" aria-busy={busy}>
          <h2 className="ui-card-title">{t('mentor.v2.review.notes')}</h2>
          {busy && <p role="status" className="text-xs text-ghost">{t('mentor.v2.review.reviewing')}</p>}
          {result?.summary && <p dir="auto" className="text-[13px] leading-[1.7] text-bright" data-testid="review-summary">{result.summary}</p>}
          {result && result.comments.length === 0 && <p className="text-xs text-ghost">{t('mentor.v2.review.noNotes')}</p>}
          <ul className="flex flex-col">
            {result?.comments.map((c) => (
              <li key={c.line} className="border-t border-border first:border-t-0">
                <button
                  type="button"
                  aria-current={selected === c.line ? 'true' : undefined}
                  onClick={() => setSelected(c.line)}
                  className={cn(
                    'flex min-h-[44px] w-full items-center gap-2.5 py-2 text-start text-[13px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring',
                    selected === c.line ? 'text-white' : 'text-soft hover:text-bright',
                  )}
                >
                  <span aria-hidden="true" className="h-2 w-2 shrink-0 rounded-full" style={{ background: SEVERITY_COLOR[c.severity] }} />
                  <span className="min-w-0 flex-1"><span className={cn('font-medium', SEVERITY_TEXT[c.severity])}>{t(`mentor.v2.review.severity.${c.severity}` as MentorV2Key)}</span> — {c.title}</span>
                  <span dir="ltr" className="font-mono text-xs text-ghost">{tf('mentor.v2.review.line', { n: c.line })}</span>
                </button>
              </li>
            ))}
          </ul>
        </Card>

        {result && (
          <Card className="flex flex-col gap-3 p-5" data-testid="debug-card">
            <h2 className="ui-card-title">{t('mentor.v2.review.debug')}</h2>
            <ol className="flex flex-col gap-2.5">
              {result.debugSteps.map((step, i) => (
                <li key={i} data-unlocked={step.unlocked} className={cn('flex gap-2.5 text-[13px] leading-[1.7]', step.unlocked ? 'text-bright' : 'text-ghost')}>
                  <span dir="ltr" className="font-mono text-xs text-amber-text">{i + 1}</span>
                  <span>{step.text}</span>
                </li>
              ))}
            </ol>
            <div className="flex flex-wrap gap-2">
              <button type="button" disabled={busy} onClick={reviewAgain} className="min-h-[44px] rounded-lg bg-amber px-3.5 text-[13px] font-semibold text-on-amber disabled:opacity-40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring">
                {t('mentor.v2.review.fixed')}
              </button>
              <button type="button" disabled={busy} onClick={reviewAgain} className="min-h-[44px] rounded-lg border border-border px-3.5 text-[13px] text-bright disabled:opacity-40 hover:border-amber/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring">
                {t('mentor.v2.review.moreHint')}
              </button>
            </div>
          </Card>
        )}
      </div>
    </div>
  )
}
