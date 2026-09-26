'use client'
import { useId, useState } from 'react'
import Link from 'next/link'
import { ChevronDown, Clock } from 'lucide-react'
import { Badge, Card, ProgressBar } from '@/components/ui/index'
import { ReadinessBadge } from './CourseReadiness'
import { pick } from '@/lib/content-language'
import { useI18n } from '@/lib/i18n'
import { fieldLabel, labelText, levelLabel, roleLabel, skillLabel, titleLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { CatalogCourse, CatalogCourseDetail } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'
import { SkillChips } from './SkillChips'

const LEVEL_BADGE = { beginner: 'beginner', intermediate: 'intermediate', advanced: 'advanced' } as const
const MAX_SKILLS = 4
const EYEBROW = 'text-xs font-medium uppercase tracking-widest text-soft'

interface CourseCardProps {
  course: CatalogCourse | CatalogCourseDetail
  /** Open the details on first render (the course page does). */
  defaultOpen?: boolean
  className?: string
  showCourseLink?: boolean
}

/**
 * A course, with just enough to answer "why is this relevant to me": its level,
 * the fields it belongs to, the skills it teaches and the career goals it
 * serves. Anything more — the description, hours, what to know first — sits
 * behind the Details toggle so a page of cards stays scannable.
 */
export function CourseCard({ course, defaultOpen = false, className, showCourseLink = true }: CourseCardProps) {
  const { t, tf, language } = useI18n()
  const ctx = useLabelContext()
  const [open, setOpen] = useState(defaultOpen)
  const panelId = useId()

  const title = titleLabel(course, ctx)
  const description = pick(course.description, course.description_ar, language)
  const detail = course as Partial<CatalogCourseDetail>
  const objectives = (language === 'ar' && detail.learning_objectives_ar?.length
    ? detail.learning_objectives_ar
    : detail.learning_objectives) ?? []
  const levelVariant = LEVEL_BADGE[course.level.slug as keyof typeof LEVEL_BADGE] ?? 'ghost'

  return (
    <Card className={cn('flex flex-col p-4', !course.is_available && 'border-dashed', className)}>
      <div className="flex items-start justify-between gap-3">
        <h3 className="text-sm font-medium leading-snug text-bright">
          <Link href={`/courses/${course.slug}`} className="hover:text-amber-text transition-colors">
            <LearningLabel parts={title} />
          </Link>
        </h3>
        {course.is_available ? (
          <Badge variant={levelVariant} className="shrink-0">
            <LearningLabel parts={levelLabel(course.level, ctx)} />
          </Badge>
        ) : (
          <Badge variant="ghost" className="shrink-0">
            <Clock size={10} className="me-1" aria-hidden="true" />
            {t('course.comingSoon')}
          </Badge>
        )}
      </div>

      {course.fields.length > 0 && (
        <p className="mt-1.5 text-xs text-soft">
          {course.fields.map((f, i) => (
            <span key={f.slug}>
              {i > 0 && ' · '}
              <LearningLabel parts={fieldLabel(f, ctx, true)} />
            </span>
          ))}
        </p>
      )}

      {(course.estimated_hours > 0 || course.module_count) && (
        <p className="mt-1.5 flex flex-wrap gap-x-3 text-xs text-soft">
          {course.module_count ? <span>{tf('card.modules', { n: course.module_count })}</span> : null}
          {course.estimated_hours > 0 && <span>{tf('card.hours', { n: course.estimated_hours })}</span>}
        </p>
      )}

      {course.skills.length > 0 && (
        <div className="mt-3 space-y-1.5">
          <p className={EYEBROW}>{t('card.skills')}</p>
          <SkillChips skills={course.skills} max={MAX_SKILLS} />
        </div>
      )}

      {course.roles.length > 0 && (
        <p className="mt-3 text-xs leading-relaxed text-bright">
          <span className="text-soft">{t('card.relevantFor')}: </span>
          {course.roles.map((r, i) => (
            <span key={r.slug}>
              {i > 0 && ', '}
              <LearningLabel parts={roleLabel(r, ctx, true)} />
            </span>
          ))}
        </p>
      )}

      {course.enrollment ? (
        <div className="mt-3 space-y-1">
          <ProgressBar value={course.enrollment.progress_percentage} />
          <p className="text-xs text-soft">
            {course.enrollment.status === 'completed'
              ? t('enr.completed')
              : tf('enr.percent', { n: Math.round(course.enrollment.progress_percentage) })}
          </p>
        </div>
      ) : (
        course.readiness && course.readiness.state !== 'not_assessed' && course.is_available && (
          <p className="mt-3 flex flex-wrap items-center gap-2 text-xs text-soft">
            {t('rd.title')}: <ReadinessBadge state={course.readiness.state} />
          </p>
        )
      )}

      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        aria-controls={panelId}
        className="mt-3 inline-flex min-h-[44px] items-center gap-1 self-start text-xs text-amber-text hover:text-amber-text2 lg:min-h-0"
      >
        {open ? t('card.less') : t('card.details')}
        <ChevronDown size={12} className={cn('transition-transform', open && 'rotate-180')} aria-hidden="true" />
      </button>

      {open && (
        <div id={panelId} className="mt-1 space-y-3 border-t border-border pt-3 text-xs leading-relaxed text-soft">
          {description && <p dir="auto">{description}</p>}
          {objectives.length > 0 && (
            <div>
              <p className={cn(EYEBROW, 'mb-1')}>{t('card.objectives')}</p>
              <ul className="list-disc space-y-0.5 ps-4">
                {objectives.map((o) => <li key={o}>{o}</li>)}
              </ul>
            </div>
          )}
          {detail.prerequisites && detail.prerequisites.length > 0 && (
            <div>
              <p className={cn(EYEBROW, 'mb-1')}>{t('card.prerequisites')}</p>
              <ul className="space-y-0.5">
                {detail.prerequisites.map((p) => (
                  <li key={p.slug}>
                    <Link href={`/courses/${p.slug}`} className="text-amber-text hover:text-amber-text2">
                      {labelText(titleLabel(p, ctx))}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {detail.assumes && detail.assumes.length > 0 && (
            <p>
              <span className="text-soft">{t('card.assumes')}: </span>
              {detail.assumes.map((s) => labelText(skillLabel(s, ctx))).join(', ')}
            </p>
          )}
          {showCourseLink && course.is_available && course.href && (
            <Link
              href={course.href}
              className="inline-flex min-h-[44px] items-center text-amber-text hover:text-amber-text2 lg:min-h-0"
            >
              {t('learn.openCourse')}
            </Link>
          )}
        </div>
      )}

      <Link
        href={`/courses/${course.slug}`}
        className="mt-auto inline-flex min-h-[44px] items-center pt-3 text-xs font-medium text-amber-text hover:text-amber-text2 lg:min-h-0"
      >
        {course.enrollment && course.enrollment.status !== 'completed'
          ? t('curriculum.continue')
          : course.enrollment ? t('enr.review') : t('card.viewCourse')}
      </Link>
    </Card>
  )
}
