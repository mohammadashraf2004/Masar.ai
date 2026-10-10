'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/index'
import { mentorV2 } from '@/lib/api'
import { useMentorV2I18n, type MentorV2Key } from '@/lib/i18n'
import { formatMinutes } from './StudyPlan'
import { planBlockHref } from './links'
import type { PlanDay, StudyPlanV2 } from './types'

const iso = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`

/** The next two days with something in them: where "approve the plan" in the mentor ends up on Home. */
export function upcomingDays(plan: StudyPlanV2, today: string, count = 2): PlanDay[] {
  return plan.days.filter((d) => d.date >= today && d.blocks.length > 0).slice(0, count)
}

/** This week's approved plan, on Home. Renders nothing until a plan has been approved. */
export function ApprovedPlanCard({ now = new Date() }: { now?: Date }) {
  const { t, tf, language } = useMentorV2I18n()
  const [plan, setPlan] = useState<StudyPlanV2 | null>(null)

  useEffect(() => {
    let alive = true
    mentorV2.approvedPlan().then((p) => { if (alive) setPlan(p) }, () => {})
    return () => { alive = false }
  }, [])

  if (!plan) return null
  const days = upcomingDays(plan, iso(now))
  if (days.length === 0) return null
  const label = (date: string) =>
    new Date(`${date}T00:00:00`).toLocaleDateString(language === 'ar' ? 'ar-u-nu-latn-ca-gregory' : 'en-GB', { weekday: 'short', day: 'numeric', month: 'short' })

  return (
    <Card data-testid="approved-plan" className="flex flex-col gap-3 p-[22px]">
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm font-semibold text-white">{t('mentor.v2.plan.thisWeek')}</span>
        <span dir="ltr" className="font-mono text-xs text-dim">{formatMinutes(plan.totalMinutes)}</span>
      </div>
      {days.map((day) => (
        <div key={day.date} className="flex flex-col gap-1.5">
          <span className="text-xs text-dim">{label(day.date)}</span>
          {day.blocks.map((b, i) => (
            <Link key={`${b.refId}-${i}`} href={planBlockHref(b)} className="flex min-h-[44px] items-center justify-between gap-3 rounded-lg bg-panel px-3 py-2 text-[13px] text-bright hover:text-white">
              <span dir="auto" className="min-w-0 flex-1">{b.title}</span>
              <span className="text-xs text-dim">{t(`mentor.v2.plan.type.${b.type}` as MentorV2Key)} · <span dir="ltr" className="font-mono">{tf('mentor.v2.plan.minutes', { n: b.minutes })}</span></span>
            </Link>
          ))}
        </div>
      ))}
    </Card>
  )
}
