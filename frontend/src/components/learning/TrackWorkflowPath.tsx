'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { CheckCircle, Clock, LockKeyhole, Play, Sparkles } from 'lucide-react'
import { Badge, Card, ProgressBar, Spinner } from '@/components/ui/index'
import { buttonStyles } from '@/components/ui/Button'
import { api } from '@/lib/api'
import { pick } from '@/lib/content-language'
import { useI18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'
import type { CourseRole, TrackSection, TrackWorkflow, TrackWorkflowCourse, WorkflowStatus } from '@/types'

type LoadState = 'idle' | 'loading' | 'ready' | 'error'

const SECTION_ORDER: TrackSection[] = [
  'foundations', 'language-generative-ai', 'application-production',
  'advanced-ai-systems', 'specializations',
]

const STATUS_ICON: Record<WorkflowStatus, typeof Play> = {
  completed: CheckCircle,
  in_progress: Play,
  next: Sparkles,
  locked: LockKeyhole,
  available: Clock,
}

const STATUS_BADGE: Record<WorkflowStatus, 'amber' | 'emerald' | 'rose' | 'sky' | 'ghost'> = {
  completed: 'emerald',
  in_progress: 'amber',
  next: 'sky',
  locked: 'rose',
  available: 'ghost',
}

function roleVariant(role: CourseRole) {
  return role === 'core' ? 'amber' : role === 'supporting' ? 'sky' : 'ghost'
}

interface TrackWorkflowPathProps {
  /** The career goal slug from the backend, never a frontend track id. */
  goal: string
}

/**
 * The ordered, server-driven workflow for one of the five fixed career
 * tracks: connected steps (completed -> in progress -> next -> locked ->
 * available), with optional courses shown as visually distinct branches that
 * never block the main line. Order, role, required-ness, section and status
 * all come from `GET /learning/tracks/{goal}/workflow` - nothing here
 * reorders, re-weighs or re-derives what the server already decided.
 */
export function TrackWorkflowPath({ goal }: TrackWorkflowPathProps) {
  const { t, tf, language } = useI18n()
  const [state, setState] = useState<LoadState>('idle')
  const [workflow, setWorkflow] = useState<TrackWorkflow | null>(null)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    let stale = false
    // Deferred to the next microtask so the loading-state update happens
    // outside the effect body itself (avoids a synchronous setState-in-effect).
    Promise.resolve()
      .then(() => {
        if (stale) return null
        setState('loading')
        setWorkflow(null)
        return api.getTrackWorkflow(goal)
      })
      .then((data) => {
        if (stale || data === null) return
        setWorkflow(data)
        setState('ready')
      })
      .catch(() => {
        if (!stale) setState('error')
      })
    return () => { stale = true }
  }, [goal, attempt])

  const sections = useMemo(() => {
    if (!workflow) return []
    if (!workflow.has_sections) return [{ section: null as TrackSection | null, courses: workflow.courses }]
    const bySection = new Map<TrackSection | null, TrackWorkflowCourse[]>()
    for (const course of workflow.courses) {
      const key = course.section ?? null
      if (!bySection.has(key)) bySection.set(key, [])
      bySection.get(key)!.push(course)
    }
    const ordered: { section: TrackSection | null; courses: TrackWorkflowCourse[] }[] =
      SECTION_ORDER.filter((s) => bySection.has(s)).map((s) => ({ section: s, courses: bySection.get(s)! }))
    if (bySection.has(null)) ordered.push({ section: null, courses: bySection.get(null)! })
    return ordered
  }, [workflow])

  if (state === 'idle') return null

  return (
    <section aria-labelledby="track-workflow-title" className="space-y-6">
      <div>
        <p className="ui-eyebrow ui-eyebrow-accent">{t('workflow.title')}</p>
        <h2 id="track-workflow-title" className="ui-section-title mt-1">
          {workflow ? pick(workflow.career_goal.title, workflow.career_goal.title_ar, language) : t('workflow.title')}
        </h2>
        <p className="ui-description mt-1">{t('workflow.subtitle')}</p>
      </div>

      {state === 'loading' && <div className="flex justify-center py-6"><Spinner announce className="h-5 w-5" /></div>}

      {state === 'error' && (
        <Card className="p-4">
          <p role="alert" className="text-sm text-rose">{t('workflow.loadError')}</p>
          <button type="button" onClick={() => setAttempt((n) => n + 1)} className="mt-3 min-h-[44px] text-sm text-amber-text hover:text-amber-text2 lg:min-h-0">
            {t('workflow.retry')}
          </button>
        </Card>
      )}

      {state === 'ready' && workflow && (
        <>
          <Card className="border-amber/20 p-4">
            <p className="text-sm text-bright">
              {tf('workflow.summary', {
                completed: workflow.required_completed, total: workflow.required_total,
                pct: Math.round(workflow.progress_percent),
              })}
            </p>
            <ProgressBar value={workflow.progress_percent} className="mt-2" />
            <div className="mt-3 grid gap-1 text-xs text-soft sm:grid-cols-2">
              {workflow.current && (
                <span>{tf('workflow.current', { title: pick(workflow.current.title, workflow.current.title_ar, language) })}</span>
              )}
              {workflow.next && (
                <span>{tf('workflow.next', { title: pick(workflow.next.title, workflow.next.title_ar, language) })}</span>
              )}
            </div>
          </Card>

          {sections.map(({ section, courses }) => (
            <section key={section ?? 'main'} aria-labelledby={section ? `workflow-section-${section}` : undefined}>
              {section && (
                <h4 id={`workflow-section-${section}`} className="mb-3 border-b border-border pb-2 text-card-title font-semibold text-bright">
                  {t(`workflow.section.${section}` as const)}
                </h4>
              )}
              <ol className="space-y-3">
                {courses.map((course, index) => (
                  <li key={course.course_id}>
                    <WorkflowNode course={course} isLast={index === courses.length - 1} />
                  </li>
                ))}
              </ol>
            </section>
          ))}
        </>
      )}
    </section>
  )
}

function WorkflowNode({ course, isLast }: { course: TrackWorkflowCourse; isLast: boolean }) {
  const { t, tf, language } = useI18n()
  const Icon = STATUS_ICON[course.status]
  const isOptional = course.role === 'optional' || !course.required
  const ctaHref = `/courses/${course.slug}`
  const ctaDisabled = course.status === 'locked'

  return (
    <div className="flex gap-3">
      <div className="flex flex-col items-center">
        <span
          className={cn(
            'flex h-8 w-8 shrink-0 items-center justify-center rounded-full border text-xs font-mono',
            course.status === 'completed' && 'border-emerald/40 bg-emerald/10 text-emerald',
            course.status === 'in_progress' && 'border-amber/40 bg-amber/10 text-amber-text',
            course.status === 'next' && 'border-sky/40 bg-sky/10 text-sky',
            course.status === 'locked' && 'border-border bg-panel text-ghost',
            course.status === 'available' && 'border-border bg-panel text-soft',
          )}
          aria-hidden="true"
        >
          {course.order}
        </span>
        {!isLast && <span className="mt-1 min-h-[2rem] flex-1 border-s-2 border-border/60" aria-hidden="true" />}
      </div>

      <Card
        data-course-id={course.slug.toUpperCase()}
        data-workflow-status={course.status}
        data-workflow-role={course.role}
        className={cn(
          'min-w-0 flex-1 p-4',
          isOptional && 'border-dashed',
          course.status === 'in_progress' && 'border-amber/40',
          course.status === 'next' && 'border-sky/40',
        )}
      >
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <h5 className="ui-card-title">
              <Link href={ctaHref} className="hover:text-amber-text transition-colors">{pick(course.title, course.title_ar, language)}</Link>
            </h5>
          </div>
          <Badge variant={STATUS_BADGE[course.status]} className="shrink-0">
            <Icon size={10} className="me-1" aria-hidden="true" />
            {t(`workflow.status.${course.status}` as const)}
          </Badge>
        </div>

        <div className="mt-2 flex flex-wrap items-center gap-2">
          <Badge variant={roleVariant(course.role)}>{t(`curriculum.role.${course.role}` as const)}</Badge>
          {course.role !== 'optional' && isOptional && <Badge variant="ghost">{t('workflow.optional')}</Badge>}
          {!course.is_available && <Badge variant="ghost">{t('workflow.comingSoon')}</Badge>}
        </div>

        {course.progress_percent > 0 && (
          <div className="mt-3 space-y-1">
            <ProgressBar value={course.progress_percent} />
            <p className="ui-caption" dir="ltr">{Math.round(course.progress_percent)}%</p>
          </div>
        )}

        <div className="ui-caption mt-3 space-y-1">
          {(course.estimated_hours > 0 || course.lesson_count > 0) && (
            <p>
              {course.estimated_hours > 0 && tf('workflow.hourCount', { n: Math.round(course.estimated_hours) })}
              {course.estimated_hours > 0 && (course.lesson_count > 0 || course.module_count > 0) && ' · '}
              {course.lesson_count > 0 && tf('workflow.lessonCount', { n: course.lesson_count })}
              {course.lesson_count > 0 && course.module_count > 0 && ' · '}
              {course.module_count > 0 && tf('workflow.moduleCount', { n: course.module_count })}
            </p>
          )}
          {course.status === 'locked' && course.prerequisites.length > 0 && (
            <p>{tf('workflow.prerequisitesNeeded', { titles: course.prerequisites.map((p) => pick(p.title, p.title_ar, language)).join(', ') })}</p>
          )}
        </div>

        {ctaDisabled ? (
          <span
            aria-disabled="true"
            className={cn(buttonStyles({ variant: 'ghost', size: 'sm' }), 'mt-4 inline-flex min-h-[44px] opacity-60 lg:min-h-0')}
          >
            {t('workflow.cta.locked')}
          </span>
        ) : (
          <Link
            href={ctaHref}
            className={cn(
              buttonStyles({ variant: course.status === 'next' || course.status === 'in_progress' ? 'amber' : 'ghost', size: 'sm' }),
              'mt-4 inline-flex min-h-[44px] lg:min-h-0',
            )}
          >
            {!course.is_available ? t('workflow.cta.details') : t(`workflow.cta.${course.status}` as const)}
          </Link>
        )}
      </Card>
    </div>
  )
}
