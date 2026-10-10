'use client'
import Link from 'next/link'
import { useMentorV2I18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'
import type { MentorCourseOption } from './types'

/** The hub's course picker: the courses the learner is enrolled in, or general. */
export interface CoursePicker {
  options: MentorCourseOption[]
  /** The course attached now, or null for general. */
  selected: string | null
  /** Whether `selected` is one of the learner's courses (a lesson link can name another). */
  enrolled: boolean
  /** The attached course's name, for a course reached by a link that is not among `options`. */
  selectedTitle?: string
  onSelect: (courseId: string | null) => void
}

/**
 * What the mentor can see for the next message: the whole course the learner chose (the hub's
 * picker - only courses they are enrolled in), or nothing for "General". A single lesson or an
 * exercise's code is never attached here; that is the lesson's own mentor panel. The default (the
 * learner's most active course) is the server's. With no picker (the course list could not be
 * read), `courseTitle` names the attached course.
 */
export function ContextBar({ course, courseTitle }: { course?: CoursePicker; courseTitle?: string | null }) {
  const { t, tf, n } = useMentorV2I18n()
  const listed = !!course?.selected && course.options.some((option) => option.courseId === course.selected)
  const wholeCourse = course ? !!course.selected && course.enrolled : !!courseTitle

  return (
    <div data-testid="context-bar" data-tour="mentor-context" className="flex flex-wrap items-center gap-x-2 gap-y-1.5 border-b border-border bg-panel px-[18px] py-2">
      <span className="text-xs text-dim">{t('mentor.v2.sees')}</span>

      {course && (
        <span data-tour="mentor-course" className="inline-flex max-w-full items-center gap-1.5">
          <label htmlFor="mentor-course" className="sr-only">{t('mentor.v2.course.label')}</label>
          <select
            id="mentor-course"
            dir="auto"
            value={course.selected ?? ''}
            onChange={(event) => course.onSelect(event.target.value || null)}
            className={cn(
              'min-h-[44px] max-w-full truncate rounded-full border ps-3 pe-8 text-xs lg:min-h-[28px]',
              'focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring',
              course.selected ? 'border-amber bg-amber-soft text-amber-text' : 'border-border bg-surface text-bright',
            )}
          >
            <option value="">{t('mentor.v2.course.general')}</option>
            {course.options.map((option) => (
              <option key={option.courseId} value={option.courseId}>
                {tf('mentor.v2.course.progress', { name: option.title, done: n(option.lessonsDone), total: n(option.lessonsTotal) })}
              </option>
            ))}
            {course.selected && !listed && (
              <option value={course.selected} disabled>
                {tf('mentor.v2.course.preview', { name: course.selectedTitle ?? course.selected })}
              </option>
            )}
          </select>
          {course.options.length === 0 && (
            <span className="text-xs text-ghost">
              {t('mentor.v2.course.none')}{' '}
              <Link href="/explore" className="font-medium text-amber-text underline-offset-2 hover:underline">{t('mentor.v2.course.browse')}</Link>
            </span>
          )}
        </span>
      )}

      {wholeCourse ? (
        <span data-chip="course" dir="auto" className="inline-flex min-h-[44px] max-w-full items-center rounded-full border border-amber/40 px-3 text-xs text-amber-text lg:min-h-[28px]">
          <span className="min-w-0 truncate">{course ? t('mentor.v2.course.only') : courseTitle}</span>
        </span>
      ) : (
        // At least 16rem wide, so beside a long picker it wraps to its own line rather than a narrow column.
        <span className="min-w-[min(100%,16rem)] flex-1 text-xs text-ghost">{t('mentor.v2.nothingAttached')}</span>
      )}
    </div>
  )
}
