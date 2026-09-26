'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { CheckCircle, Clock, LockKeyhole, Play, RotateCcw } from 'lucide-react'
import { Badge, Card, ProgressBar, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { courseHref, labelText, skillLabel, titleLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type {
  CatalogCourse, CatalogCourseDetail, CourseRole, LearningPath, PathCourse,
} from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'
import { SkillChips } from './SkillChips'

/**
 * The catalogue gives the canonical curriculum a stable public identity
 * (`course-001` …). This recognises that server-provided identity without
 * mirroring its placement, roles, prerequisites, or order in the client.
 */
const isCurriculumCourse = (course: CatalogCourse) => /^course-\d{3}$/i.test(course.slug)

const ROLE_ORDER: CourseRole[] = ['core', 'supporting', 'optional']
const ROLE_KEY: Record<CourseRole, 'curriculum.role.core' | 'curriculum.role.supporting' | 'curriculum.role.optional'> = {
  core: 'curriculum.role.core',
  supporting: 'curriculum.role.supporting',
  optional: 'curriculum.role.optional',
}

type LoadState = 'idle' | 'loading' | 'ready' | 'error'
type DisplayState = 'not_started' | 'in_progress' | 'completed' | 'locked' | 'coming_soon'

const STATE_STYLE: Record<DisplayState, { icon: typeof Play; badge: 'amber' | 'emerald' | 'rose' | 'ghost' }> = {
  not_started: { icon: Play, badge: 'ghost' },
  in_progress: { icon: Play, badge: 'amber' },
  completed: { icon: CheckCircle, badge: 'emerald' },
  locked: { icon: LockKeyhole, badge: 'rose' },
  coming_soon: { icon: Clock, badge: 'ghost' },
}

function courseId(slug: string) {
  return slug.toUpperCase()
}

function statusFor(course: CatalogCourse, item: PathCourse | undefined, currentId?: number | null): DisplayState {
  // Learner state is only read from the generated path. When it does not name
  // a course, do not infer completion or a prerequisite lock locally.
  if (item?.state === 'completed' || item?.state === 'waived') return 'completed'
  if (item?.reason === 'prerequisite') return 'locked'
  if ((item?.completion_pct ?? 0) > 0 || currentId === course.id) return 'in_progress'
  if (!course.is_available) return 'coming_soon'
  return 'not_started'
}

function statusText(state: DisplayState, t: ReturnType<typeof useI18n>['t']) {
  switch (state) {
    case 'in_progress': return t('curriculum.inProgress')
    case 'completed': return t('curriculum.completed')
    case 'locked': return t('curriculum.locked')
    case 'coming_soon': return t('curriculum.comingSoon')
    default: return t('curriculum.notStarted')
  }
}

function roleVariant(role: CourseRole) {
  return role === 'core' ? 'amber' : role === 'supporting' ? 'sky' : 'ghost'
}

function actionText(state: DisplayState, t: ReturnType<typeof useI18n>['t']) {
  if (state === 'in_progress') return t('curriculum.continue')
  if (state === 'completed') return t('curriculum.review')
  if (state === 'locked') return t('curriculum.viewPrerequisites')
  if (state === 'not_started') return t('curriculum.start')
  return t('curriculum.viewDetails')
}

interface TrackCurriculumProps {
  /** The role slug from the backend path/profile, never a frontend track id. */
  careerGoal: string
  /** Optional learner state from the server-generated path. */
  path?: LearningPath | null
}

/**
 * The non-duplicated curriculum view for a career goal.
 *
 * `/learning/courses?career_goal=` supplies membership and the contextual
 * core/supporting/optional relationship. Course detail requests supply the
 * server-owned prerequisites. Tool courses and legacy track entries stay out
 * of this canonical-curriculum section; their existing catalogue pages remain
 * their own surfaces.
 */
export function TrackCurriculum({ careerGoal, path }: TrackCurriculumProps) {
  const { t } = useI18n()
  const [state, setState] = useState<LoadState>('idle')
  const [courses, setCourses] = useState<CatalogCourse[]>([])
  const [details, setDetails] = useState<Record<string, CatalogCourseDetail>>({})
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    // A narrow guard keeps older isolated component tests that mock only the
    // path API from pretending their incomplete mock is a real response.
    if (typeof api.listCatalogCourses !== 'function') return
    let stale = false
    // Start the request on the next microtask. Besides making the state reset
    // part of the external-request lifecycle, this prevents a synchronous
    // effect update when a learner switches between track previews.
    Promise.resolve()
      .then(() => {
        if (stale) return null
        setState('loading')
        setCourses([])
        setDetails({})
        return api.listCatalogCourses({ career_goal: [careerGoal] })
      })
      .then(async (received) => {
        if (received === null) return
        const canonical = received.filter(isCurriculumCourse)
        if (stale) return
        setCourses(canonical)
        setState('ready')

        if (typeof api.getCatalogCourse !== 'function') return
        const resolved = await Promise.all(canonical.map(async (course) => {
          try {
            return await api.getCatalogCourse(course.slug)
          } catch {
            // A list row is still useful if one supplementary detail request
            // fails; do not replace server data with a guessed prerequisite.
            return null
          }
        }))
        if (!stale) {
          setDetails(Object.fromEntries(
            resolved.filter((detail): detail is CatalogCourseDetail => detail !== null)
              .map((detail) => [detail.slug, detail])
          ))
        }
      })
      .catch(() => {
        if (!stale) setState('error')
      })

    return () => { stale = true }
  }, [careerGoal, attempt])

  const pathCourses = useMemo(() => {
    const entries = path?.stages.flatMap((stage) => stage.courses) ?? []
    return new Map(entries.map((item) => [item.course.id, item]))
  }, [path])

  const groups = useMemo(() => {
    const result = new Map<CourseRole, CatalogCourse[]>()
    for (const role of ROLE_ORDER) result.set(role, [])
    for (const course of courses) {
      const role = course.track_role
      if (role && result.has(role)) result.get(role)?.push(course)
    }
    return result
  }, [courses])

  if (state === 'idle') return null

  return (
    <section aria-labelledby="track-curriculum-title" className="space-y-4">
      <div>
        <h3 id="track-curriculum-title" className="text-xs font-medium uppercase tracking-widest text-soft">
          {t('curriculum.title')}
        </h3>
        <p className="mt-1 text-sm text-soft">{t('curriculum.subtitle')}</p>
      </div>

      {state === 'loading' && <div className="flex justify-center py-6"><Spinner announce className="h-5 w-5" /></div>}

      {state === 'error' && (
        <Card className="p-4">
          <p role="alert" className="text-sm text-rose">{t('curriculum.loadError')}</p>
          <button type="button" onClick={() => setAttempt((n) => n + 1)} className="mt-3 min-h-[44px] text-sm text-amber-text hover:text-amber-text2 lg:min-h-0">
            {t('curriculum.retry')}
          </button>
        </Card>
      )}

      {state === 'ready' && courses.length === 0 && (
        <Card className="p-4"><p className="text-sm text-soft">{t('curriculum.empty')}</p></Card>
      )}

      {state === 'ready' && ROLE_ORDER.map((role) => {
        const items = groups.get(role) ?? []
        if (items.length === 0) return null
        return (
          <section key={role} aria-label={t(ROLE_KEY[role])}>
            <div className="mb-2 flex items-center gap-2">
              <h4 className="text-sm font-semibold text-bright">{t(ROLE_KEY[role])}</h4>
              <Badge variant={roleVariant(role)}>{items.length}</Badge>
            </div>
            <div className="grid gap-3 md:grid-cols-2">
              {items.map((course) => (
                <CurriculumCourseCard
                  key={course.id}
                  course={course}
                  detail={details[course.slug]}
                  pathCourse={pathCourses.get(course.id)}
                  currentId={path?.current_course?.course.id}
                />
              ))}
            </div>
          </section>
        )
      })}
    </section>
  )
}

function CurriculumCourseCard({
  course, detail, pathCourse, currentId,
}: {
  course: CatalogCourse
  detail?: CatalogCourseDetail
  pathCourse?: PathCourse
  currentId?: number | null
}) {
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  const role = course.track_role
  // A filtered catalogue response must supply it, but a neutral fallback keeps
  // an incomplete response honest instead of inventing a role.
  if (!role) return null

  const status = statusFor(course, pathCourse, currentId)
  const style = STATE_STYLE[status]
  const Icon = style.icon
  const prerequisites = detail?.prerequisites ?? []
  const progress = pathCourse?.completion_pct
  const actionHref = status === 'locked' || !course.is_available
    ? `/courses/${course.slug}`
    : courseHref({ course })

  return (
    <Card data-course-id={courseId(course.slug)} data-track-role={role} data-status={status} className="flex flex-col p-4">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="font-mono text-[11px] text-soft" dir="ltr">{tf('curriculum.courseId', { id: courseId(course.slug) })}</p>
          <h5 className="mt-1 text-sm font-semibold leading-snug text-bright">
            <Link href={`/courses/${course.slug}`} className="hover:text-amber-text transition-colors">
              <LearningLabel parts={titleLabel(course, ctx)} />
            </Link>
          </h5>
        </div>
        <div className="flex shrink-0 flex-col items-end gap-1.5">
          <Badge variant={roleVariant(role)}>{t(ROLE_KEY[role])}</Badge>
          <Badge variant={style.badge}>
            <Icon size={10} className="me-1" aria-hidden="true" />
            {statusText(status, t)}
          </Badge>
        </div>
      </div>

      {course.skills.length > 0 && <SkillChips skills={course.skills} max={4} className="mt-3" />}

      <div className="mt-3 space-y-2 text-xs text-soft">
        {progress != null && progress > 0 && (
          <>
            <div className="flex items-center justify-between gap-3">
              <span>{t('learn.progress')}</span>
              <span className="font-mono text-amber-text" dir="ltr">{tf('curriculum.progress', { pct: Math.round(progress) })}</span>
            </div>
            <ProgressBar value={progress} />
          </>
        )}
        {course.estimated_hours > 0 && <p>{tf('card.hours', { n: course.estimated_hours })}</p>}
        {prerequisites.length > 0 && (
          <div>
            <p className="font-medium text-soft">{t('curriculum.prerequisites')}</p>
            <ul className="mt-1 space-y-0.5">
              {prerequisites.map((prerequisite) => (
                <li key={prerequisite.id}>
                  <Link href={`/courses/${prerequisite.slug}`} className="text-amber-text hover:text-amber-text2">
                    {labelText(titleLabel(prerequisite, ctx))}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <Link
        href={actionHref}
        className={cn(
          'mt-4 inline-flex min-h-[44px] items-center self-start text-sm text-amber-text hover:text-amber-text2 lg:min-h-0',
          status === 'coming_soon' && 'text-soft hover:text-bright'
        )}
      >
        {actionText(status, t)}
      </Link>
    </Card>
  )
}
