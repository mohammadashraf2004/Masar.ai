'use client'
import { useState } from 'react'
import Link from 'next/link'
import { buttonStyles } from '@/components/ui/Button'
import {
  ArrowRight, CheckCircle, ChevronDown, CircleDot, Circle, Clock, MinusCircle, AlertTriangle, Info, BadgeCheck,
} from 'lucide-react'
import { Badge, Card, ProgressBar } from '@/components/ui/index'
import { useI18n } from '@/lib/i18n'
import {
  advisoryText, courseHref, fieldLabel, labelText, levelLabel, roleLabel, skillLabel, titleLabel,
} from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { FieldRef, LearningPath, PathCourse, PathStage, PathStageStatus, RoadmapStep } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'
import { WhyThisCourse } from './WhyThisCourse'

// ─── Summary ─────────────────────────────────────────────────────────────────

/**
 * The top of "Your Masar": career goal, the fields, the level and how far along
 * the path is. Progress is whatever the server reports — it is derived from the
 * learner's lessons and never recomputed here.
 */
export function MasarSummary({ path, actions }: { path: LearningPath; actions?: React.ReactNode }) {
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  const pct = path.progress?.path_pct ?? null
  const progress = path.progress

  return (
    <Card className="p-5 sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs font-medium uppercase tracking-widest text-soft">{t('learn.title')}</p>
          <h2 className="mt-1 font-display text-lg font-bold leading-snug text-white sm:text-2xl">
            <LearningLabel parts={roleLabel(path.career_goal, ctx)} />
          </h2>
          <p className="mt-1.5 flex flex-wrap items-center gap-x-2 gap-y-1 text-sm text-soft">
            {path.effective_fields.map((f, i) => (
              <span key={f.slug} className="inline-flex items-center gap-2">
                {i > 0 && <span aria-hidden="true" className="text-soft">·</span>}
                <LearningLabel parts={fieldLabel(f, ctx, true)} />
              </span>
            ))}
            {path.effective_fields.length > 0 && <span aria-hidden="true" className="text-soft">·</span>}
            <LearningLabel parts={levelLabel(path.level, ctx)} />
          </p>
        </div>
        {actions && <div className="flex flex-wrap gap-2">{actions}</div>}
      </div>

      <div className="mt-5">
        <div className="mb-1.5 flex items-baseline justify-between text-xs">
          <span className="text-soft">{t('learn.progress')}</span>
          <span className="font-mono text-amber-text" dir="ltr">{pct === null ? '—' : `${Math.round(pct)}%`}</span>
        </div>
        <ProgressBar
          value={pct ?? 0}
          size="md"
          color={pct !== null && pct >= 100 ? 'emerald' : 'amber'}
        />
        <p className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-soft">
          {progress?.path_total != null && (
            <span>{tf('roadmap.counts', { done: progress.path_completed ?? 0, total: progress.path_total })}</span>
          )}
          {(progress?.path_known ?? 0) > 0 && <span>{tf('roadmap.knownCount', { n: progress?.path_known ?? 0 })}</span>}
          {path.estimated_hours > 0 && <span>{tf('learn.hoursLeft', { n: Math.round(path.estimated_hours) })}</span>}
          {path.estimated_weeks > 0 && <span>{tf('learn.weeks', { n: path.estimated_weeks })}</span>}
          {path.progress && <span>{t('learn.overall')}: <span dir="ltr">{Math.round(path.progress.overall_pct)}%</span></span>}
        </p>
      </div>

      {(path.current_course || path.next_course) && (
        <dl className="mt-5 grid gap-3 border-t border-border pt-4 sm:grid-cols-2">
          {path.current_course && <StepSummary label={t('roadmap.currentCourse')} step={path.current_course} lead />}
          {path.next_course && <StepSummary label={t('roadmap.nextCourse')} step={path.next_course} />}
        </dl>
      )}
      {path.current_course && (
        <div className="mt-4">
          <Link href={courseHref(path.current_course)} className={buttonStyles({ size: 'sm' })}>
            {t('card.continue')} <ArrowRight size={12} className="rtl:rotate-180" aria-hidden="true" />
          </Link>
        </div>
      )}
    </Card>
  )
}

function StepSummary({ label, step, lead }: { label: string; step: RoadmapStep; lead?: boolean }) {
  const ctx = useLabelContext()
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-widest text-soft">{label}</dt>
      <dd className={cn('mt-1 text-sm', lead ? 'font-semibold text-white' : 'text-bright')}>
        <LearningLabel parts={titleLabel(step.course, ctx)} />
      </dd>
    </div>
  )
}

// ─── Advisories ──────────────────────────────────────────────────────────────

export function AdvisoryList({ path, catalogFields = [] }: { path: LearningPath; catalogFields?: FieldRef[] }) {
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  // An advisory can name a field that is not in the route — a *suggested*
  // modality — so names are looked up in the whole catalogue, with the path's
  // own fields as the fallback when it has not loaded.
  const fields = Object.fromEntries(
    [...path.fields, ...path.effective_fields, ...catalogFields].map((f) => [f.slug, f])
  )
  const items = path.advisories
    .map((a) => ({ advisory: a, text: advisoryText(a, { ...ctx, tf, fields }) }))
    .filter((x): x is { advisory: typeof x.advisory; text: string } => x.text !== null)

  if (items.length === 0) return null
  return (
    <ul className="space-y-2" aria-label={t('learn.notes')}>
      {items.map(({ advisory, text }, i) => {
        const warn = advisory.severity === 'warning'
        const Icon = warn ? AlertTriangle : Info
        return (
          <li
            key={`${advisory.code}-${i}`}
            role="note"
            className={cn(
              'flex items-start gap-2.5 rounded-md border px-3 py-2.5 text-xs leading-relaxed',
              warn ? 'border-amber/30 bg-amber/5 text-soft' : 'border-sky/20 bg-sky/5 text-soft'
            )}
          >
            <Icon size={13} className={cn('mt-0.5 shrink-0', warn ? 'text-amber-text' : 'text-sky')} aria-hidden="true" />
            <span>{text}</span>
          </li>
        )
      })}
    </ul>
  )
}

// ─── Stages ──────────────────────────────────────────────────────────────────

const STATUS_ICON: Record<PathStageStatus, { icon: typeof Circle; tone: string }> = {
  completed: { icon: CheckCircle, tone: 'text-emerald' },
  current: { icon: CircleDot, tone: 'text-amber-text' },
  upcoming: { icon: Circle, tone: 'text-soft' },
  coming_soon: { icon: Clock, tone: 'text-soft' },
  skippable: { icon: MinusCircle, tone: 'text-soft' },
}

const KNOWN_REASONS = new Set(['below_level', 'prerequisite'])

/**
 * What a learner sees for a course. The API's `waived` is an implementation
 * word; on screen it is "Already know". Which course is *current* is the
 * server's answer (`path.current_course`) — this only marks it.
 */
type RowKind = 'completed' | 'known' | 'current' | 'upcoming' | 'optional'

function rowKind(item: PathCourse, isCurrent: boolean): RowKind {
  if (item.state === 'completed') return 'completed'
  if (item.state === 'waived') return 'known'
  if (item.state === 'optional') return 'optional'
  return isCurrent ? 'current' : 'upcoming'
}

const ROW_STYLE: Record<RowKind, { icon: typeof Circle; tone: string; badge: 'emerald' | 'sky' | 'amber' | 'ghost' }> = {
  completed: { icon: CheckCircle, tone: 'text-emerald', badge: 'emerald' },
  known: { icon: BadgeCheck, tone: 'text-sky', badge: 'sky' },
  current: { icon: ArrowRight, tone: 'text-amber-text', badge: 'amber' },
  upcoming: { icon: Circle, tone: 'text-dim', badge: 'ghost' },
  optional: { icon: MinusCircle, tone: 'text-dim', badge: 'ghost' },
}

function CourseRow({ item, isCurrent }: { item: PathCourse; isCurrent: boolean }) {
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  const { course, state, reason } = item
  const kind = rowKind(item, isCurrent)
  const { icon: Icon, tone, badge } = ROW_STYLE[kind]
  const badgeText =
    kind === 'completed' ? t('courseState.completed')
    : kind === 'known' ? t('roadmap.known')
    : kind === 'current' ? t('roadmap.current')
    : kind === 'optional' ? t('courseState.optional')
    : t('roadmap.upcoming')

  const knownNames = (item.known_skills ?? []).map((s) => labelText(skillLabel(s, ctx))).join(', ')
  // Why a course reads the way it does, in the learner's words. A known course
  // is never presented as skipped or missed: it says what the learner told us.
  let note: string | null = null
  if (kind === 'known') {
    note = knownNames ? tf('roadmap.knownBecause', { skills: knownNames }) : t('courseReason.known_skills')
  } else if (kind === 'upcoming' || kind === 'current') {
    if (knownNames) {
      note = tf('roadmap.partial', {
        n: item.known_skills.length,
        total: Math.max(course.skills.length, item.known_skills.length),
        skills: knownNames,
      })
    }
  }

  return (
    <li data-state={kind} className="flex items-start gap-3 py-3">
      <Icon size={16} className={cn('mt-0.5 shrink-0', tone)} aria-hidden="true" />
      {/* The status sits beside the title on a wide row and drops under it on a
          narrow one, so a long Arabic title keeps the whole row instead of
          sharing ~150px with a badge. */}
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-start justify-between gap-x-3 gap-y-1.5">
          <div className="min-w-0 flex-1 basis-40">
            <Link href={`/courses/${course.slug}`} className="text-sm text-bright hover:text-amber-text transition-colors">
              <LearningLabel parts={titleLabel(course, ctx)} />
            </Link>
            <p className="mt-0.5 flex flex-wrap items-center gap-x-2 text-xs text-soft">
              <LearningLabel parts={levelLabel(course.level, ctx)} />
              {reason && KNOWN_REASONS.has(reason) && (
                <span>· {t(`courseReason.${reason}` as Parameters<typeof t>[0])}</span>
              )}
            </p>
            {note && <p className="mt-1 text-xs leading-relaxed text-soft">{note}</p>}
          </div>
          <div className="flex shrink-0 items-center gap-2.5">
            {(state === 'required') && (item.completion_pct ?? 0) > 0 && (
              <span className="font-mono text-xs text-amber-text" dir="ltr">{Math.round(item.completion_pct ?? 0)}%</span>
            )}
            <Badge variant={badge}>{badgeText}</Badge>
          </div>
        </div>
        {item.why && (state === 'required' || state === 'optional') && (
          <WhyThisCourse why={item.why} panelClassName="max-sm:-ms-7" />
        )}
      </div>
    </li>
  )
}

function StageRow({ stage, isLast, currentId }: { stage: PathStage; isLast: boolean; currentId?: number }) {
  const { t, tf, courseCount } = useI18n()
  const ctx = useLabelContext()
  const isCurrent = stage.status === 'current'
  // The current stage opens itself so the learner lands on their next step;
  // every other stage is one tap away.
  const [open, setOpen] = useState(isCurrent)
  const { icon: Icon, tone } = STATUS_ICON[stage.status]
  const hasCourses = stage.courses.length > 0
  // What to say under the title, in order. Joined with a separator below so two
  // facts ("3 more planned", "Coming soon") never run together.
  const meta: string[] = []
  if (hasCourses) meta.push(courseCount(stage.courses.length))
  if (stage.upcoming_count > 0) meta.push(tf('learn.planned', { n: stage.upcoming_count }))
  // Known courses can sit in a collapsed stage; say so on the header.
  const knownHere = stage.courses.filter((c) => c.state === 'waived').length
  if (knownHere > 0) meta.push(tf('roadmap.knownCount', { n: knownHere }))
  if (!hasCourses && stage.status === 'coming_soon') meta.push(t('stage.comingSoon'))
  if (stage.status === 'skippable') meta.push(t('stage.skippable'))
  if (stage.status === 'completed') meta.push(t('stage.completed'))

  return (
    <li
      data-status={stage.status}
      aria-current={isCurrent ? 'step' : undefined}
      className="relative ps-9 sm:ps-10"
    >
      {/* Timeline: the icon sits on a line that runs to the next stage. */}
      <span className="absolute start-0 top-4 flex h-7 w-7 items-center justify-center rounded-full bg-void">
        <Icon size={isCurrent ? 22 : 18} className={tone} aria-hidden="true" />
      </span>
      {!isLast && <span className="absolute start-[13px] top-11 bottom-0 w-px bg-border" aria-hidden="true" />}

      <div
        className={cn(
          'mb-3 rounded-lg border transition-colors',
          isCurrent
            ? 'border-amber/50 bg-amber/5 shadow-[0_0_24px_rgba(245,158,11,0.08)]'
            : 'border-border bg-panel',
          (stage.status === 'coming_soon' || stage.status === 'skippable') && 'border-dashed'
        )}
      >
        <button
          type="button"
          onClick={() => hasCourses && setOpen((o) => !o)}
          aria-expanded={hasCourses ? open : undefined}
          disabled={!hasCourses}
          className={cn(
            'flex w-full items-center justify-between gap-3 text-start',
            isCurrent ? 'p-4' : 'px-4 py-3',
            hasCourses ? 'min-h-[44px] cursor-pointer' : 'cursor-default'
          )}
        >
          <span className="min-w-0">
            <span className={cn('block leading-snug', isCurrent ? 'text-base font-semibold text-white' : 'text-sm font-medium text-bright')}>
              <LearningLabel parts={titleLabel(stage, ctx)} />
            </span>
            <span className="mt-0.5 block text-xs text-soft">
              {isCurrent && <span className="me-2 font-medium text-amber-text">{t('stage.current')}</span>}
              {meta.map((part, i) => (
                <span key={i}>{i > 0 && ' · '}{part}</span>
              ))}
            </span>
          </span>
          <span className="flex shrink-0 items-center gap-3">
            {stage.progress_pct != null && stage.status !== 'completed' && (
              <span className="font-mono text-xs text-amber-text" dir="ltr">{Math.round(stage.progress_pct)}%</span>
            )}
            {hasCourses && (
              <ChevronDown size={14} className={cn('text-soft transition-transform', open && 'rotate-180')} aria-hidden="true" />
            )}
          </span>
        </button>

        {isCurrent && stage.progress_pct != null && (
          <div className="px-4 pb-1">
            <ProgressBar value={stage.progress_pct} />
          </div>
        )}

        {open && hasCourses && (
          <ul className="divide-y divide-border px-3 pb-1 sm:px-4">
            {stage.courses.map((c) => <CourseRow key={c.course.id} item={c} isCurrent={c.course.id === currentId} />)}
          </ul>
        )}
      </div>
    </li>
  )
}

export function PathRoadmap({ path }: { path: LearningPath }) {
  const { t } = useI18n()
  // Whether the roadmap is finished is the server's answer, not an inference.
  const finished = path.is_complete === true

  return (
    <div>
      <h3 className="mb-3 text-xs font-medium uppercase tracking-widest text-soft">{t('learn.pathTitle')}</h3>
      {finished && (
        <p role="status" className="mb-3 rounded-md border border-emerald/30 bg-emerald/5 px-3 py-2.5 text-xs text-emerald">
          {t('learn.complete')}
        </p>
      )}
      <ol aria-label={t('learn.pathTitle')}>
        {path.stages.map((stage, i) => (
          <StageRow key={stage.slug} stage={stage} isLast={i === path.stages.length - 1} currentId={path.current_course?.course.id} />
        ))}
      </ol>
    </div>
  )
}

/** Plain-text summary of a path, for aria-labels and tests. */
export function pathTitle(path: LearningPath, ctx: ReturnType<typeof useLabelContext>): string {
  const goal = labelText(roleLabel(path.career_goal, ctx))
  const fields = path.effective_fields.map((f) => labelText(fieldLabel(f, ctx, true))).join(' + ')
  return fields ? `${goal} — ${fields}` : goal
}
