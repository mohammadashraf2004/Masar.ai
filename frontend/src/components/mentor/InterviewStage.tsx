'use client'
import { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Mic, Square } from 'lucide-react'
import { CameraTile, InterviewerTile } from '@/components/mentor/CameraTile'
import { QuotaUpsell } from '@/components/mentor/QuotaUpsell'
import { Button } from '@/components/ui/Button'
import { Modal } from '@/components/ui/Modal'
import { Card, Spinner } from '@/components/ui/index'
import { useCamera } from '@/hooks/useCamera'
import type { useInterviewRun } from '@/hooks/useInterviewRun'
import { useSpeechRecognition } from '@/hooks/useSpeechRecognition'
import { useI18n, type StringKey } from '@/lib/i18n'
import { formatClock } from '@/lib/mentor/format'
import { MOCK_INTERVIEW_CREDITS, answeredCount, type InterviewSession, type QuestionRecord } from '@/lib/mentor/interview'
import { cn } from '@/lib/utils'

type Run = ReturnType<typeof useInterviewRun>

function useElapsed(startedAt: string, running: boolean) {
  const [now, setNow] = useState(() => Date.now())
  useEffect(() => {
    if (!running) return
    const timer = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(timer)
  }, [running])
  return Math.max(0, now - new Date(startedAt).getTime())
}

/**
 * The interview stage (handoff Task 12b): who is asking, who is answering, the question, the
 * answer box and the controls. It renders a session that is in progress; the setup and the
 * report are their own pages.
 */
export function InterviewStage({ run, session }: { run: Run; session: InterviewSession }) {
  const { t, tf } = useI18n()
  const router = useRouter()
  const camera = useCamera({ resumeIfGranted: true })
  const elapsed = useElapsed(session.startedAt, !run.finished)
  const [confirming, setConfirming] = useState(false)
  const [ending, setEnding] = useState(false)
  const keepGoing = useRef<HTMLButtonElement>(null)

  const total = session.durationMin * 60_000
  const answered = answeredCount(session)

  async function endNow() {
    setEnding(true)
    await run.finish()
    router.push(`/mentor/interview/${session.id}/report`)
  }

  return (
    <Card className="flex min-w-0 flex-[2_1_480px] flex-col gap-[18px] p-5">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
        <span dir="ltr" className="font-display text-base font-bold text-white">{session.role}</span>
        <span className="rounded-full border border-border px-2.5 py-0.5 text-xs text-dim">
          {t(`interview.type.${session.type}` as StringKey)}
        </span>
        {/* A retry asks questions already generated, so it costs nothing. */}
        {session.retryOf === null && (
          <span className="rounded-full border border-amber/40 px-2.5 py-0.5 text-xs text-amber-text">
            {tf('interview.perQuestion', { n: MOCK_INTERVIEW_CREDITS })}
          </span>
        )}
        <span
          className="ms-auto flex items-center gap-2 font-mono text-[13px] text-bright"
          role="timer"
          aria-label={tf('interview.timer', { elapsed: formatClock(elapsed), total: formatClock(total) })}
        >
          <span aria-hidden="true" className="h-2 w-2 rounded-full bg-rose" />
          <span dir="ltr" aria-hidden="true">{formatClock(elapsed)} / {formatClock(total)}</span>
        </span>
      </div>

      <div className="grid gap-3 [grid-template-columns:repeat(auto-fit,minmax(200px,1fr))]">
        <InterviewerTile busy={run.fetching} label={t('interview.interviewer')} />
        <CameraTile camera={camera} label={t('interview.you')} />
      </div>

      {run.current ? (
        <QuestionPanel
          key={run.current.id}
          run={run}
          session={session}
          question={run.current}
          index={run.index}
          onEnd={() => setConfirming(true)}
        />
      ) : run.complete ? (
        <div className="flex flex-col items-start gap-3">
          <Button onClick={() => void endNow()} loading={ending}>{t('interview.finish')}</Button>
        </div>
      ) : (
        <div className="flex flex-col gap-3" aria-live="polite">
          {run.error ? (
            <>
              <p role="alert" className="text-sm text-rose">{t(run.error)}</p>
              {run.error === 'mentor.error.credits' && <QuotaUpsell kind="credits" context="interview" />}
              <div className="flex flex-wrap gap-3">
                <Button variant="ghost" onClick={run.retry}>{t('common.retry')}</Button>
                {answered > 0 && <Button variant="ghost" onClick={() => setConfirming(true)}>{t('interview.end')}</Button>}
              </div>
            </>
          ) : (
            <p role="status" className="flex items-center gap-2 text-sm text-dim">
              <Spinner className="h-4 w-4" />
              {t('interview.loadingQuestion')}
            </p>
          )}
        </div>
      )}

      {confirming && (
        <Modal
          title={t('interview.end.title')}
          description={tf('interview.end.body', { n: answered })}
          initialFocus={keepGoing}
          onClose={() => setConfirming(false)}
          footer={
            <>
              <Button ref={keepGoing} variant="ghost" onClick={() => setConfirming(false)}>{t('interview.end.cancel')}</Button>
              <Button variant="danger" loading={ending} onClick={() => void endNow()}>
                {t('interview.end.confirm')}
              </Button>
            </>
          }
        />
      )}
    </Card>
  )
}

function QuestionPanel({
  run,
  session,
  question,
  index,
  onEnd,
}: {
  run: Run
  session: InterviewSession
  question: QuestionRecord
  index: number
  onEnd: () => void
}) {
  const { t, tf } = useI18n()
  const router = useRouter()
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const field = useRef<HTMLTextAreaElement>(null)

  const speech = useSpeechRecognition({
    lang: session.language === 'ar' ? 'ar-SA' : 'en-US',
    onText: (text) => setDraft((d) => (d.trim() ? `${d.trimEnd()} ${text}` : text)),
  })

  async function go(answer: string | null) {
    if (busy) return
    if (speech.listening) speech.stop()
    setBusy(true)
    const ended = await run.submit(answer)
    if (ended) router.push(`/mentor/interview/${session.id}/report`)
    // Otherwise this panel is replaced by the next question's (it is keyed by question), or by
    // the "preparing" line while it is fetched.
  }

  const position = index + 1
  const pillCount = session.totalQuestions

  return (
    <div className="flex flex-col gap-[18px]">
      <div className="flex flex-col gap-2.5">
        <div className="flex items-center justify-between gap-3">
          <span className="font-mono text-xs text-amber-text">
            {tf('interview.counter', { n: position, total: pillCount })}
          </span>
          <ol aria-hidden="true" className="flex items-center gap-1.5">
            {Array.from({ length: pillCount }, (_, i) => (
              <li
                key={i}
                className={cn('h-1.5 rounded-full', i === index ? 'w-[18px]' : 'w-2', i <= index ? 'bg-amber' : 'bg-border')}
              />
            ))}
          </ol>
        </div>
        <h2 className="text-[19px] font-bold leading-[1.6] text-white" dir="auto">{question.text}</h2>
        {question.hints.length > 0 && (
          <details className="text-sm">
            <summary className="min-h-[44px] cursor-pointer py-2 text-ghost hover:text-soft focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring lg:min-h-0 lg:py-0">
              {t('interview.hints')}
            </summary>
            <ul className="mt-2 space-y-1 ps-3">
              {question.hints.map((hint, i) => (
                <li key={i} dir="auto" className="text-xs text-dim">→ {hint}</li>
              ))}
            </ul>
          </details>
        )}
      </div>

      <div>
        <label htmlFor="interview-answer" className="mb-1.5 block text-xs text-ghost">{t('interview.answer.label')}</label>
        <textarea
          id="interview-answer"
          ref={field}
          dir="auto"
          value={draft}
          disabled={busy}
          onChange={(e) => setDraft(e.target.value)}
          placeholder={t(speech.supported ? 'interview.answer.placeholderMic' : 'interview.answer.placeholder')}
          className="min-h-[110px] w-full resize-y rounded-lg border border-border bg-void px-3.5 py-3 text-base leading-[1.7] text-bright placeholder:text-ghost focus:border-amber/50 focus:outline-none md:text-sm"
        />
        {speech.problem && (
          <p role="status" className="mt-1.5 text-xs text-dim">
            {t(speech.problem === 'denied' ? 'interview.mic.denied' : speech.problem === 'none' ? 'interview.mic.none' : 'interview.mic.error')}
          </p>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-2.5">
        {speech.supported && (
          <button
            type="button"
            aria-pressed={speech.listening}
            aria-label={t(speech.listening ? 'interview.mic.off' : 'interview.mic.on')}
            title={t(speech.listening ? 'interview.mic.off' : 'interview.mic.on')}
            disabled={busy}
            onClick={() => (speech.listening ? speech.stop() : speech.start())}
            className={cn(
              'grid h-11 w-11 shrink-0 place-items-center rounded-full border transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-40',
              speech.listening ? 'border-rose bg-rose text-on-solid' : 'border-border bg-panel text-bright hover:border-amber/40',
            )}
          >
            {speech.listening ? <Square size={16} aria-hidden="true" /> : <Mic size={18} aria-hidden="true" />}
          </button>
        )}
        <Button variant="ghost" disabled={busy} onClick={() => void go(null)}>{t('interview.skip')}</Button>
        <Button disabled={busy || draft.trim() === ''} loading={busy} onClick={() => void go(draft)}>
          {t(run.isLast ? 'interview.finish' : 'interview.next')}
        </Button>
        <button
          type="button"
          onClick={onEnd}
          className="ms-auto inline-flex min-h-[44px] items-center justify-center rounded border border-rose/50 px-4 py-2 text-sm font-medium text-rose transition-colors hover:bg-rose/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring lg:min-h-0"
        >
          {t('interview.end')}
        </button>
      </div>
    </div>
  )
}
