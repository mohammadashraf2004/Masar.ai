'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/index'
import { mentorV2 } from '@/lib/api'
import { useMentorV2I18n, type MentorV2Key } from '@/lib/i18n'
import { cn } from '@/lib/utils'
import { buttonStyles } from '@/components/ui/Button'
import { mentorV2Live } from './flag'
import { planBlockHref } from './links'
import type { PlanBlockType, StudyPlanV2 } from './types'

const TYPE_TONE: Record<PlanBlockType, string> = {
  lesson: 'text-amber-text',
  exercise: 'text-emerald',
  review: 'text-rose',
  interview: 'text-white',
}

const iso = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`

/** The Saturday that starts this week's plan (the learner's week in Masar runs Saturday to Friday). */
export function weekStartOf(now: Date): string {
  const d = new Date(now)
  d.setHours(0, 0, 0, 0)
  d.setDate(d.getDate() - ((d.getDay() + 1) % 7))
  return iso(d)
}

export function formatMinutes(total: number): string {
  return `${Math.floor(total / 60)}h ${String(total % 60).padStart(2, '0')}m`
}

/**
 * The weekly plan (Mentor v2 §2c): a summary (goal, total time, active days), one card per day with
 * its blocks linking to what to do, and the server's reasons for the plan. The server builds it from
 * the learner's enrolments and progress (free; no model call), so every block is a real lesson.
 * "Approve" keeps it on this device, so Home can show it; "Regenerate" asks for another arrangement.
 */
export function StudyPlan({ now = new Date() }: { now?: Date }) {
  const { t, tf, language } = useMentorV2I18n()
  const [plan, setPlan] = useState<StudyPlanV2 | null>(null)
  const [variant, setVariant] = useState(0)
  const [busy, setBusy] = useState(true)
  const [failed, setFailed] = useState(false)
  const [approved, setApproved] = useState(false)
  const weekStart = weekStartOf(now)
  const tomorrow = iso(new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1))

  // Only the answer sets state here (the busy flag is raised by the button that asks for another plan).
  useEffect(() => {
    let alive = true
    mentorV2.plan({ weekStart, variant }, language).then(
      (next) => { if (alive) { setPlan(next); setFailed(false); setBusy(false) } },
      () => { if (alive) { setFailed(true); setBusy(false) } },
    )
    return () => { alive = false }
  }, [weekStart, variant, language])

  const dateLabel = (isoDate: string) =>
    new Date(`${isoDate}T00:00:00`).toLocaleDateString(language === 'ar' ? 'ar-u-nu-latn-ca-gregory' : 'en-GB', { weekday: 'short', day: 'numeric', month: 'short' })

  if (failed) return <p role="alert" className="text-sm text-rose">{t('mentor.v2.failedNoCharge')}</p>
  if (!plan) return <p role="status" className="py-10 text-center text-sm text-ghost">{t('mentor.v2.plan.loading')}</p>

  const active = plan.days.filter((d) => d.blocks.length > 0).length

  if (plan.status === 'no_enrollment') {
    return (
      <Card className="flex flex-col items-start gap-3 p-6" data-testid="plan-empty">
        <p dir="auto" className="text-sm leading-relaxed text-bright">{t('mentor.v2.plan.empty')}</p>
        <Link href="/explore" className={buttonStyles({ size: 'sm' })}>{t('mentor.v2.plan.browse')}</Link>
      </Card>
    )
  }

  return (
    <div className="flex flex-col gap-5" aria-busy={busy}>
      <Card className="flex flex-wrap items-center gap-x-6 gap-y-4 p-5">
        <div className="flex min-w-[220px] flex-[1_1_320px] flex-col gap-1.5">
          <span className="text-xs text-dim">{tf('mentor.v2.plan.week', { date: dateLabel(weekStart) })}</span>
          <p dir="auto" className="text-[17px] font-bold leading-snug text-white">{plan.goal}</p>
          {mentorV2Live() && <span className="text-xs text-ghost">{t('mentor.v2.plan.source')}</span>}
        </div>
        <div dir="ltr" className="flex items-center gap-5 font-mono text-sm text-white">
          <span data-testid="plan-total">{formatMinutes(plan.totalMinutes)}</span>
          <span data-testid="plan-days">{active} / {plan.days.length}</span>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            disabled={busy}
            onClick={() => { setBusy(true); setApproved(false); setVariant((v) => v + 1) }}
            className="min-h-[44px] rounded-lg border border-border px-3.5 text-[13px] text-bright hover:border-amber/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-40"
          >
            {t('mentor.v2.plan.regenerate')}
          </button>
          <button
            type="button"
            disabled={busy || approved}
            onClick={() => { void mentorV2.approvePlan(plan).then(() => setApproved(true)) }}
            className="min-h-[44px] rounded-lg bg-amber px-4 text-[13px] font-semibold text-on-amber hover:bg-amber2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-60"
          >
            {approved ? t('mentor.v2.plan.approved') : t('mentor.v2.plan.approve')}
          </button>
        </div>
      </Card>

      <ul className="grid gap-3 [grid-template-columns:repeat(auto-fill,minmax(150px,1fr))]">
        {plan.days.map((day) => {
          const rest = day.blocks.length === 0
          const isTomorrow = day.date === tomorrow
          return (
            <li
              key={day.date}
              data-testid="plan-day"
              data-tomorrow={isTomorrow || undefined}
              data-rest={rest || undefined}
              className={cn('flex min-w-0 flex-col gap-2 rounded-xl border bg-surface p-3', isTomorrow ? 'border-amber' : 'border-border', rest && 'opacity-70')}
            >
              <span className="text-xs font-semibold text-white">
                {dateLabel(day.date)}{isTomorrow ? ` ${t('mentor.v2.plan.tomorrow')}` : ''}
              </span>
              {rest && <span className="text-xs text-ghost">{t('mentor.v2.plan.rest')}</span>}
              {day.blocks.map((block, i) => (
                <Link
                  key={`${block.refId}-${i}`}
                  href={planBlockHref(block)}
                  className="flex min-h-[44px] flex-col gap-1 rounded-lg bg-panel p-2.5 hover:bg-panel/70 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                >
                  <span className="flex items-center justify-between gap-2 text-xs">
                    <span className={cn('font-semibold', TYPE_TONE[block.type])}>{t(`mentor.v2.plan.type.${block.type}` as MentorV2Key)}</span>
                    <span dir="ltr" className="font-mono text-ghost">{tf('mentor.v2.plan.minutes', { n: block.minutes })}</span>
                  </span>
                  <span dir="auto" className="text-[13px] leading-snug text-bright">
                    {block.title}{block.continues ? ` (${t('mentor.v2.plan.continues')})` : ''}
                  </span>
                </Link>
              ))}
            </li>
          )
        })}
      </ul>

      <Card className="flex flex-col gap-3 p-5">
        <h2 className="ui-card-title">{t('mentor.v2.plan.why')}</h2>
        <ol className="flex flex-col gap-2.5">
          {plan.reasons.map((reason, i) => (
            <li key={reason} className="flex gap-2.5 text-[13px] leading-[1.7] text-bright">
              <span dir="ltr" className="font-mono text-xs text-amber-text">{String(i + 1).padStart(2, '0')}</span>
              <span dir="auto">{reason}</span>
            </li>
          ))}
        </ol>
      </Card>
    </div>
  )
}
