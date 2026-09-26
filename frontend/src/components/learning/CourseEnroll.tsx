'use client'
import { useState } from 'react'
import Link from 'next/link'
import { CheckCircle2 } from 'lucide-react'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card, ProgressBar } from '@/components/ui/index'
import { api } from '@/lib/api'
import { pick } from '@/lib/content-language'
import { useI18n } from '@/lib/i18n'
import { courseHref } from '@/lib/learning'
import type { CatalogCourseDetail, EnrollmentBrief, EnrollResult, ReadinessState } from '@/types'

interface CourseEnrollProps {
  course: CatalogCourseDetail
  readinessState?: ReadinessState
  /** Called with the server's answer after enrolling, so the page can show the fresh readiness. */
  onEnrolled?: (result: EnrollResult) => void
}

/**
 * Enroll in this course. No track, goal or saved path is involved, and a learner
 * whose readiness is weak is never refused: the button just says "Start anyway".
 * Enrolling twice is harmless (the server returns the same enrollment), so there is
 * no state here that a double click could corrupt. Progress is the server's number.
 */
export function CourseEnroll({ course, readinessState, onEnrolled }: CourseEnrollProps) {
  const { t, tf, language } = useI18n()
  const [enrollment, setEnrollment] = useState<EnrollmentBrief | null>(course.enrollment ?? null)
  const [result, setResult] = useState<EnrollResult | null>(null)
  const [busy, setBusy] = useState(false)
  const [failed, setFailed] = useState(false)
  const href = courseHref({ course })

  async function enroll() {
    setBusy(true)
    setFailed(false)
    try {
      const done = await api.enrollInCourse(course.slug)
      setResult(done)
      setEnrollment({
        status: done.enrollment.status,
        progress_percentage: done.enrollment.progress_percentage,
        enrolled_at: done.enrollment.enrolled_at,
        started_at: done.enrollment.started_at,
        completed_at: done.enrollment.completed_at,
      })
      onEnrolled?.(done)
    } catch {
      setFailed(true)
    }
    setBusy(false)
  }

  async function setPaused(paused: boolean) {
    setBusy(true)
    setFailed(false)
    try {
      const row = await api.setCoursePaused(course.slug, paused)
      setEnrollment((prev) => ({
        ...(prev ?? { status: row.status, progress_percentage: row.progress_percentage }),
        status: row.status,
        progress_percentage: row.progress_percentage,
      }))
    } catch {
      setFailed(true)
    }
    setBusy(false)
  }

  if (!course.is_available) {
    return <Card className="p-5 text-sm text-soft">{t('enr.unavailable')}</Card>
  }

  const step = result?.start.recommended_module
  const stepTitle = step ? pick(step.title, step.title_ar, language) : null

  return (
    <Card className="space-y-4 p-5">
      {!enrollment ? (
        <Button size="lg" loading={busy} onClick={() => void enroll()}>
          {readinessState === 'needs_foundation' ? t('rd.startAnyway') : t('enr.enroll')}
        </Button>
      ) : (
        <>
          <div className="space-y-2">
            <p className="flex items-center gap-2 text-sm text-bright">
              {enrollment.status === 'completed' && <CheckCircle2 size={16} className="text-emerald" aria-hidden="true" />}
              {enrollment.status === 'completed'
                ? t('enr.completed')
                : enrollment.status === 'paused'
                  ? t('enr.paused')
                  : t('enr.enrolledNote')}
            </p>
            <ProgressBar value={enrollment.progress_percentage} />
            <p className="text-xs text-soft">{tf('enr.percent', { n: Math.round(enrollment.progress_percentage) })}</p>
          </div>

          {step && stepTitle && (
            <p className="text-sm text-soft">
              <span className="font-medium text-bright">{t('enr.firstStep')}: </span>
              {tf(result?.start.mode === 'resume' ? 'enr.resumeFrom' : 'enr.startFrom', { n: step.order, title: stepTitle })}
            </p>
          )}

          <div className="flex flex-wrap gap-2">
            {enrollment.status !== 'paused' && (
              <Link href={href} className={buttonStyles({ size: 'lg' })}>
                {enrollment.status === 'completed' ? t('enr.review') : t('course.continueLearning')}
              </Link>
            )}
            {enrollment.status === 'paused' && (
              <Button size="lg" loading={busy} onClick={() => void setPaused(false)}>{t('enr.resume')}</Button>
            )}
            {(enrollment.status === 'enrolled' || enrollment.status === 'in_progress') && (
              <Button variant="ghost" size="lg" loading={busy} onClick={() => void setPaused(true)}>{t('enr.pause')}</Button>
            )}
          </div>
        </>
      )}
      {failed && <p role="alert" className="text-sm text-rose">{t('enr.error')}</p>}
    </Card>
  )
}
