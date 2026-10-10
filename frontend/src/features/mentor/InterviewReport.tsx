'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/index'
import { mentorV2 } from '@/lib/api'
import { useMentorV2I18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'
import type { InterviewReportV2 } from './types'

/** A score out of 10 is "good" from 8: green, amber below. */
export const GOOD_SCORE = 8

/**
 * The report after a mock interview (Mentor v2 §2d): the score and verdict, each question with what
 * the learner said and a note (one open at a time), strengths and gaps, lessons to take next, and
 * the way to put them in this week's plan.
 */
export function InterviewReport({ id }: { id: string }) {
  const { t, tf, n, language } = useMentorV2I18n()
  const [report, setReport] = useState<InterviewReportV2 | null>(null)
  const [failed, setFailed] = useState(false)
  const [open, setOpen] = useState<number | null>(null)
  const [added, setAdded] = useState(false)

  useEffect(() => {
    let alive = true
    mentorV2.interviewReport(id, language).then((r) => { if (alive) setReport(r) }, () => { if (alive) setFailed(true) })
    return () => { alive = false }
  }, [id, language])

  if (failed) return <p role="alert" className="text-sm text-rose">{t('mentor.v2.failedNoCharge')}</p>
  if (!report) return <p role="status" className="py-10 text-center text-sm text-ghost">{t('mentor.v2.plan.loading')}</p>

  async function addToPlan() {
    if (!report) return
    await mentorV2.addToPlan(report.recommended.map((r) => ({ type: 'review' as const, title: r.title, minutes: r.minutes, refId: r.href })))
    setAdded(true)
  }

  return (
    <div className="flex flex-col gap-5">
      <Card className="flex flex-wrap items-center gap-x-8 gap-y-5 p-[22px] [background-image:radial-gradient(90%_120%_at_0%_0%,rgb(var(--acc)/var(--acc-soft-a)),transparent_60%)]">
        <div className="flex min-w-[220px] flex-[1_1_320px] flex-col gap-2">
          <span dir="auto" className="text-xs text-dim">{tf('mentor.v2.report.meta', { role: report.role, date: report.date, min: n(report.duration) })}</span>
          <span dir="ltr" className="self-start font-display text-[22px] font-bold text-white">{report.role}</span>
        </div>
        <div className="flex items-center gap-4">
          <span className="flex items-baseline gap-1" dir="ltr">
            <span data-testid="report-score" className="font-display text-[52px] font-extrabold leading-none text-white">{report.score}</span>
            <span className="font-mono text-sm text-ghost">{t('mentor.v2.report.of')}</span>
          </span>
          <span className="rounded-full border border-amber px-3 py-1 text-xs font-semibold text-amber-text">{report.verdict}</span>
        </div>
      </Card>

      <div className="flex flex-wrap items-start gap-5">
        <Card className="flex min-w-0 flex-[2_1_420px] flex-col p-5">
          <h2 className="ui-card-title mb-3">{t('mentor.v2.report.questions')}</h2>
          <ul className="flex flex-col">
            {report.questions.map((q, i) => {
              const expanded = open === i
              return (
                <li key={q.text} className="border-t border-border first:border-t-0">
                  <button
                    type="button"
                    aria-expanded={expanded}
                    onClick={() => setOpen(expanded ? null : i)}
                    className="flex min-h-[44px] w-full flex-col gap-2 py-3 text-start focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                  >
                    <span className="flex items-baseline gap-3">
                      <span dir="ltr" className="font-mono text-xs text-amber-text">{String(i + 1).padStart(2, '0')}</span>
                      <span dir="auto" className="min-w-0 flex-1 text-sm text-white">{q.text}</span>
                      <span dir="ltr" className="font-mono text-sm text-white">{q.score}</span>
                    </span>
                    <span className="progress-track h-1 w-full">
                      <span className={cn('progress-fill block', q.score >= GOOD_SCORE ? 'bg-emerald' : 'bg-amber')} style={{ width: `${Math.round(q.score * 10)}%` }} />
                    </span>
                  </button>
                  {expanded && (
                    <div className="mb-3 flex flex-col gap-2 text-[13px] leading-[1.7]">
                      <p dir="auto" className="rounded-lg bg-amber-soft px-3 py-2 text-bright">{tf('mentor.v2.report.said', { quote: q.quote })}</p>
                      <p dir="auto" className="text-soft"><span className="font-semibold text-amber-text">{t('mentor.v2.report.note')} </span>{q.note}</p>
                    </div>
                  )}
                </li>
              )
            })}
          </ul>
        </Card>

        <div className="flex min-w-0 flex-[1_1_300px] flex-col gap-5">
          <Card className="flex flex-col gap-3 p-5">
            <h2 className="ui-card-title">{t('mentor.v2.report.strengths')}</h2>
            <ul className="flex flex-col gap-2">
              {report.strengths.map((s) => (
                <li key={s} className="flex items-start gap-2.5 text-[13px] leading-[1.7] text-bright">
                  <span aria-hidden="true" className="mt-2 h-2 w-2 shrink-0 rounded-full bg-emerald" />
                  <span dir="auto">{s}</span>
                </li>
              ))}
            </ul>
            <h2 className="ui-card-title mt-1">{t('mentor.v2.report.gaps')}</h2>
            <ul className="flex flex-col gap-2">
              {report.gaps.map((g) => (
                <li key={g} className="flex items-start gap-2.5 text-[13px] leading-[1.7] text-bright">
                  <span aria-hidden="true" className="mt-2 h-2 w-2 shrink-0 rounded-full border-[1.5px] border-amber" />
                  <span dir="auto">{g}</span>
                </li>
              ))}
            </ul>
          </Card>

          <Card className="flex flex-col gap-1 p-5">
            <h2 className="ui-card-title mb-1">{t('mentor.v2.report.recommended')}</h2>
            {report.recommended.map((r) => (
              <Link
                key={r.title}
                href={r.href}
                className="flex min-h-[44px] items-center gap-3 border-t border-border py-2 text-[13px] text-bright first:border-t-0 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
              >
                <span dir="ltr" className="font-mono text-xs text-amber-text">{r.code}</span>
                <span dir="auto" className="min-w-0 flex-1">{r.title}</span>
                <span dir="ltr" className="font-mono text-xs text-ghost">{tf('mentor.v2.plan.minutes', { n: r.minutes })}</span>
              </Link>
            ))}
          </Card>

          <div className="flex flex-wrap gap-2">
            <Link href="/mentor/interview/new" className="inline-flex min-h-[44px] items-center rounded-lg bg-amber px-4 text-[13px] font-semibold text-on-amber hover:bg-amber2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring">
              {t('mentor.v2.report.new')}
            </Link>
            <button type="button" onClick={() => window.print()} className="min-h-[44px] rounded-lg border border-border px-4 text-[13px] text-bright hover:border-amber/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring">
              {t('mentor.v2.report.pdf')}
            </button>
            <button
              type="button"
              disabled={added}
              onClick={() => void addToPlan()}
              className="min-h-[44px] rounded-lg border border-border px-4 text-[13px] text-bright hover:border-amber/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-60"
            >
              {added ? t('mentor.v2.report.added') : t('mentor.v2.report.addToPlan')}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
