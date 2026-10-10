'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { Card, ProgressBar, Spinner } from '@/components/ui/index'
import { buttonStyles } from '@/components/ui/Button'
import { getHomeOverview } from '@/lib/api'
import { useAuthStore } from '@/lib/store'
import { cn } from '@/lib/utils'
import { useHomeI18n } from './strings'
// [mentor-v2]
import { ApprovedPlanCard } from '@/features/mentor/ApprovedPlanCard'
// [/mentor-v2]
import type { HomeMilestone, HomeOverview, Localized, MilestoneStatus } from './types'

/**
 * The signed-in Home (design: MasarApp.dc.html, screen "home"): greeting, where to
 * continue, readiness, the career track as a timeline, the next exam, two numbers
 * and the mentor's suggestion.
 *
 * Copy in the reader's language, Latin names (course, track, exam) left-to-right, and
 * scores, percentages and counts of credits in mono with Latin digits. The page is
 * RTL or LTR with the app; nothing here decides direction except the Latin islands.
 */
export function HomeScreen() {
  const [overview, setOverview] = useState<HomeOverview | null>(null)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    let alive = true
    getHomeOverview().then(
      (data) => { if (alive) setOverview(data) },
      () => { if (alive) setFailed(true) },
    )
    return () => { alive = false }
  }, [])

  return (
    <AppShell>
      {overview ? <HomeBody overview={overview} /> : (
        <div className="flex flex-1 items-center justify-center">
          {failed
            ? <p role="alert" className="text-sm text-rose">Could not load your home.</p>
            : <Spinner announce className="h-6 w-6" />}
        </div>
      )}
    </AppShell>
  )
}

function greetingKey(hour: number): 'morning' | 'evening' {
  return hour < 12 ? 'morning' : 'evening'
}

function HomeBody({ overview }: { overview: HomeOverview }) {
  const { language, tf, n } = useHomeI18n()
  const user = useAuthStore((s) => s.user)
  const first = user?.full_name?.split(' ')[0] ?? ''
  const pick = (value: Localized) => value[language]
  const { continueLearning: cont, readiness, track, exam, stats, mentor } = overview
  const stagesDone = track.milestones.filter((m) => m.status === 'done').length
  const greeting = greetingKey(new Date().getHours()) === 'morning'
    ? (language === 'ar' ? 'صباح الخير' : 'Good morning')
    : (language === 'ar' ? 'مساء الخير' : 'Good evening')

  return (
    <>
      <PageHeader
        contained
        wrapTitle
        title={first ? (language === 'ar' ? `${greeting}، ${first}` : `${greeting}, ${first}`) : greeting}
        subtitle={tf('home.subtitle', { n: n(exam.pointsAway) })}
      />
      <PageBody className="flex flex-col gap-5">
        <div className="flex flex-wrap gap-5">
          <ContinueCard overview={overview} />
          <Card className="flex min-w-0 flex-[1_1_280px] flex-col gap-4 p-[22px]">
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-white">{tf('home.readiness.title')}</span>
              <span className="text-xs text-emerald">
                {/* The number is an LTR island: in an RTL line "+6" would otherwise read "6+". */}
                <bdi dir="ltr" className="font-mono">+{readiness.weeklyDelta}</bdi> {tf('home.readiness.week')}
              </span>
            </div>
            <div className="flex items-baseline gap-1.5">
              <span className="font-display text-[52px] font-extrabold leading-none text-white">{readiness.score}</span>
              <span dir="ltr" className="font-mono text-sm text-ghost">/100</span>
            </div>
            <ul className="flex flex-col gap-2.5">
              {readiness.skills.map((skill) => (
                <li key={skill.name.en} className="flex flex-col gap-[5px]">
                  <div className="flex justify-between text-xs">
                    <span className="text-bright">{pick(skill.name)}</span>
                    <span className="font-mono text-dim">{skill.value}</span>
                  </div>
                  <ProgressBar value={skill.value} />
                </li>
              ))}
            </ul>
          </Card>
        </div>

        <div className="flex flex-wrap gap-5">
          <Card data-tour="path" className="flex min-w-0 flex-[2_1_420px] flex-col gap-[18px] p-[22px]">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div className="flex flex-col gap-1">
                <span className="text-xs text-dim">{tf('home.track.label')}</span>
                <div className="flex flex-wrap items-baseline gap-2">
                  <span className="text-[17px] font-bold text-white">{pick(track.title)}</span>
                  {/* The Latin name next to the Arabic one; in English it would only repeat the title. */}
                  {language === 'ar' && (
                    <span dir="ltr" className="font-display text-[13px] font-semibold text-ghost">{track.en}</span>
                  )}
                </div>
              </div>
              <span className="rounded-full border border-border px-2.5 py-1 font-mono text-xs text-dim">
                {tf('home.track.stages', { done: n(stagesDone), total: n(track.milestones.length) })}
              </span>
            </div>
            <ol className="flex flex-col">
              {track.milestones.map((m, i) => (
                <MilestoneRow key={m.title.en} milestone={m} last={i === track.milestones.length - 1} />
              ))}
            </ol>
          </Card>

          <div className="flex min-w-0 flex-[1_1_280px] flex-col gap-5">
            <Card className="flex flex-col gap-3.5 p-[22px]">
              <span className="text-xs text-dim">{tf('home.exam.label')}</span>
              <span dir="ltr" className="self-end font-display text-[17px] font-bold text-white">{exam.title}</span>
              <span className="text-[13px] text-dim">{tf('home.exam.meta', { min: n(exam.minutes) })}</span>
              <ul className="flex flex-col gap-2 text-[13px]">
                {exam.requirements.map((r) => (
                  <li key={r.label.en} className="flex items-center gap-2 text-bright">
                    <span
                      aria-hidden="true"
                      className={cn('h-2 w-2 shrink-0 rounded-full', r.done ? 'bg-emerald' : 'border-[1.5px] border-amber')}
                    />
                    <span>{pick(r.label)}</span>
                    {r.value && <span dir="ltr" className="ms-auto font-mono text-ghost">{r.value}</span>}
                  </li>
                ))}
              </ul>
              {/* Not a button that does nothing: it is a disabled one until eligibility is real. */}
              <button
                type="button"
                disabled
                className="flex h-11 items-center justify-center rounded-lg border border-border text-sm text-ghost disabled:cursor-default"
              >
                {tf('home.exam.book')}
              </button>
            </Card>
            <div className="flex gap-5">
              <StatCard label={tf('home.stats.streak')} value={stats.streakDays} />
              <StatCard label={tf('home.stats.graded')} value={stats.gradedExercises} tour="practice" />
            </div>
          </div>
        </div>

        {/* [mentor-v2] the plan approved in the mentor's weekly-plan tab; nothing until one is */}
        <ApprovedPlanCard />
        {/* [/mentor-v2] */}
        <Card className="flex flex-wrap items-start gap-4 px-[22px] py-5">
          <span aria-hidden="true" className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-amber-soft">
            <span className="h-2.5 w-2.5 rounded-full bg-amber" />
          </span>
          <div className="flex min-w-0 flex-[1_1_260px] flex-col gap-1">
            <span className="text-[13px] font-semibold text-white">{tf('home.mentor.title')}</span>
            <p className="text-sm leading-[1.7] text-bright [text-wrap:pretty]">{pick(mentor.tip)}</p>
          </div>
          <Link
            href={mentor.href}
            data-tour="mentor"
            className={buttonStyles({ variant: 'ghost', className: 'h-10 px-4 text-[13px] text-bright' })}
          >
            {tf('home.mentor.open')}
          </Link>
        </Card>
      </PageBody>
    </>
  )
}

function ContinueCard({ overview }: { overview: HomeOverview }) {
  const { language, tf, n } = useHomeI18n()
  const c = overview.continueLearning
  return (
    <Card
      data-tour="learn"
      className="flex min-w-0 flex-[2_1_420px] flex-col gap-4 p-[22px] [background-image:radial-gradient(90%_120%_at_0%_0%,rgb(var(--acc)/var(--acc-soft-a)),transparent_60%)]"
    >
      <div className="flex items-center gap-2.5">
        {/* Inline spacing: the app cancels Tailwind tracking under lang="ar", and this label is Latin. */}
        <span className="font-mono text-xs text-amber-text" style={{ letterSpacing: '0.12em' }}>
          {tf('home.continue.eyebrow')}
        </span>
        <span className="text-xs text-dim">{tf('home.continue.label')}</span>
      </div>
      <div className="flex flex-col gap-1.5">
        <span dir="ltr" className="self-end font-display text-[22px] font-bold text-white">{c.courseTitle}</span>
        <span className="text-base font-semibold text-bright">
          {tf('home.continue.lesson', { n: n(c.lessonNumber), title: c.lessonTitle[language] })}
        </span>
      </div>
      <div className="flex flex-col gap-2">
        <ProgressBar value={c.percent} size="md" />
        <div className="flex justify-between text-xs text-dim">
          <span>{tf('home.continue.meta', { n: n(c.lessonNumber), total: n(c.lessonTotal), min: n(c.minutesLeft) })}</span>
          <span className="font-mono">{c.percent}%</span>
        </div>
      </div>
      <div className="flex flex-wrap gap-2.5">
        <Link href={c.lessonHref} className={buttonStyles({ className: 'h-11 px-5 font-semibold' })}>
          {tf('home.continue.go')}
        </Link>
        <Link href={c.planHref} className={buttonStyles({ variant: 'ghost', className: 'h-11 px-[18px] text-bright' })}>
          {tf('home.continue.plan')}
        </Link>
      </div>
    </Card>
  )
}

function StatCard({ label, value, tour }: { label: string; value: number; tour?: string }) {
  return (
    <Card data-tour={tour} className="flex flex-1 flex-col gap-1.5 p-[18px]">
      <span className="text-xs text-dim">{label}</span>
      <span className="font-display text-[28px] font-extrabold text-white">{value}</span>
    </Card>
  )
}

const TAG_TONE: Record<MilestoneStatus, string> = {
  done: 'border-emerald text-emerald',
  now: 'border-amber text-amber-text',
  lock: 'border-border text-ghost',
}

/** One stage on the career-track timeline: a 14px rail column (node and the line to the
 *  next stage), then the title, its meta and a status tag. */
function MilestoneRow({ milestone: m, last }: { milestone: HomeMilestone; last: boolean }) {
  const { language, tf } = useHomeI18n()
  const tag = m.status === 'done' ? tf('home.track.done') : m.status === 'now' ? tf('home.track.now') : tf('home.track.lock')
  return (
    <li data-status={m.status} className="flex items-stretch gap-3.5">
      <div className="flex w-3.5 flex-none flex-col items-center">
        <span
          aria-hidden="true"
          className={cn(
            'mt-[3px] box-border h-3.5 w-3.5 flex-none rounded-full',
            m.status === 'done' && 'border-2 border-amber bg-amber',
            m.status === 'now' && 'border-2 border-amber shadow-[0_0_0_4px_rgb(var(--acc)/var(--acc-soft-a))]',
            m.status === 'lock' && 'border-[1.5px] border-border',
          )}
        />
        <span
          aria-hidden="true"
          className={cn('min-h-[18px] w-0.5 flex-1', last ? 'bg-transparent' : m.status === 'done' ? 'bg-amber' : 'bg-border')}
        />
      </div>
      <div className="flex flex-1 items-start justify-between gap-2.5 pb-4">
        <div className="flex min-w-0 flex-col gap-0.5">
          <span className={cn('text-sm', m.status === 'now' ? 'font-bold' : 'font-medium', m.status === 'lock' ? 'text-dim' : 'text-white')}>
            {m.title[language]}
          </span>
          <span className="text-xs text-ghost">{m.meta[language]}</span>
        </div>
        <span className={cn('whitespace-nowrap rounded-full border px-2 py-0.5 text-xs', TAG_TONE[m.status])}>
          {tag}
          {m.status === 'now' && <> · <bdi dir="ltr">{m.percent ?? 0}%</bdi></>}
        </span>
      </div>
    </li>
  )
}
