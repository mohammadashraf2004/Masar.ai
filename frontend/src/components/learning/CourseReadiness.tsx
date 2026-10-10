'use client'
import Link from 'next/link'
import { AlertTriangle, Check, CircleHelp } from 'lucide-react'
import { Badge, Card } from '@/components/ui/index'
import { Button, buttonStyles } from '@/components/ui/Button'
import { useI18n, type StringKey } from '@/lib/i18n'
import { skillLabel, titleLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { ReadinessReport, ReadinessState, ReviewItem, SkillStandingItem } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'

const STATE_BADGE: Record<ReadinessState, 'emerald' | 'amber' | 'rose' | 'ghost'> = {
  ready: 'emerald',
  mostly_ready: 'amber',
  needs_foundation: 'rose',
  not_assessed: 'ghost',
}

/** The word a learner reads for a readiness state, in their language. */
export function ReadinessBadge({ state, className }: { state: ReadinessState; className?: string }) {
  const { t } = useI18n()
  return (
    <Badge variant={STATE_BADGE[state]} className={className}>
      {t(`rd.state.${state}` as StringKey)}
    </Badge>
  )
}

function SkillList({ items, icon, tone }: { items: SkillStandingItem[]; icon: React.ReactNode; tone: string }) {
  const { t } = useI18n()
  const ctx = useLabelContext()
  return (
    <ul className="space-y-1">
      {items.map((item) => (
        <li key={item.skill.slug} className={cn('flex items-start gap-2 text-sm', tone)}>
          <span className="mt-0.5 shrink-0" aria-hidden="true">{icon}</span>
          <span>
            <LearningLabel parts={skillLabel(item.skill, ctx)} />
            {item.level !== 'not_assessed' && (
              <span className="text-soft"> · {t(`rd.level.${item.level}` as StringKey)}</span>
            )}
          </span>
        </li>
      ))}
    </ul>
  )
}

function ReviewList({ items }: { items: ReviewItem[] }) {
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  return (
    <ul className="space-y-2">
      {items.map((item) => (
        <li key={item.course.slug} className="text-sm">
          <div className="flex flex-wrap items-center gap-2">
            <Link href={`/courses/${item.course.slug}`} className="font-medium text-amber-text hover:text-amber-text2">
              <LearningLabel parts={titleLabel(item.course, ctx)} />
            </Link>
            <Badge variant={item.required ? 'amber' : 'ghost'}>{item.required ? t('rd.needed') : t('rd.helpful')}</Badge>
          </div>
          {item.modules.length > 0 && (
            <p className="mt-0.5 text-xs text-soft">
              {item.modules.map((m) => tf('rd.moduleN', { n: m.order })).join(' · ')}
            </p>
          )}
        </li>
      ))}
    </ul>
  )
}

interface CourseReadinessProps {
  report: ReadinessReport
  /** Open the short check. Omitted when the course has none, or it is already open. */
  onTakeCheck?: () => void
  className?: string
}

/**
 * How ready this learner is for a course, and what to do about it. It is advice:
 * there is no pass or fail and nothing here stops anyone from starting. The wording
 * and the strengths and gaps come from the server, which weighs the learner's own
 * progress, quiz results and earlier checks; this only lays them out.
 */
export function CourseReadiness({ report, onTakeCheck, className }: CourseReadinessProps) {
  const { t } = useI18n()
  const firstReview = report.recommended_review[0]
  const canCheck = report.assessment_available && onTakeCheck

  return (
    <Card className={cn('space-y-4 p-5', className)} aria-label={t('rd.title')}>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="ui-card-title">{t('rd.title')}</h2>
        <ReadinessBadge state={report.state} />
      </div>

      <p className="text-sm text-bright">{t(`rd.headline.${report.state}` as StringKey)}</p>
      {!report.has_prerequisites && <p className="text-xs text-soft">{t('rd.noPrereq')}</p>}

      {report.strengths.length > 0 && (
        <div className="space-y-1.5">
          <p className="text-xs font-medium uppercase tracking-widest text-soft">{t('rd.strong')}</p>
          <SkillList items={report.strengths} icon={<Check size={14} />} tone="text-emerald" />
        </div>
      )}

      {report.gaps.length > 0 && (
        <div className="space-y-1.5">
          <p className="text-xs font-medium uppercase tracking-widest text-soft">{t('rd.review')}</p>
          <SkillList items={report.gaps} icon={<AlertTriangle size={14} />} tone="text-amber-text" />
        </div>
      )}

      {report.recommended_review.length > 0 && (
        <div className="space-y-1.5">
          <p className="text-xs font-medium uppercase tracking-widest text-soft">{t('rd.preparation')}</p>
          <ReviewList items={report.recommended_review} />
        </div>
      )}

      {(firstReview || canCheck) && (
        <div className="flex flex-wrap gap-2">
          {firstReview && (
            <Link href={`/courses/${firstReview.course.slug}`} className={buttonStyles({ variant: 'ghost', size: 'sm' })}>
              {t('rd.reviewFirst')}
            </Link>
          )}
          {canCheck && (
            <Button variant="ghost" size="sm" onClick={onTakeCheck}>
              <CircleHelp size={13} aria-hidden="true" />
              {report.last_assessed_at ? t('rd.retakeCheck') : t('rd.takeCheck')}
            </Button>
          )}
        </div>
      )}

      <p className="text-xs text-soft">{t('rd.advisory')}</p>
    </Card>
  )
}
