'use client'
import { useId, useState } from 'react'
import Link from 'next/link'
import { ChevronDown } from 'lucide-react'
import { useI18n, type StringKey } from '@/lib/i18n'
import { fieldLabel, labelText, roleLabel, titleLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { CourseWhy } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'
import { SkillChips } from './SkillChips'

interface WhyThisCourseProps {
  why: CourseWhy
  /** Opens expanded. The roadmap keeps it collapsed. */
  defaultOpen?: boolean
  className?: string
  /** Extra classes for the expanded panel (the roadmap widens it on a phone). */
  panelClassName?: string
}

const EYEBROW = 'text-xs font-medium uppercase tracking-widest text-soft'

/**
 * "Why this course?" — an expandable explanation of why one course is on the
 * learner's roadmap.
 *
 * It renders facts the backend derived from the catalogue (the goal, the
 * fields, the stage, the reasons, what the course teaches, what the learner
 * declared, what is left to gain, which later courses need this one). This
 * component only turns them into words in the reader's language: the reasons
 * arrive as codes, and each has one sentence in lib/i18n.ts, in both languages.
 * Nothing is inferred here, and a fact the server did not send is not drawn.
 */
export function WhyThisCourse({ why, defaultOpen = false, className, panelClassName }: WhyThisCourseProps) {
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  const [open, setOpen] = useState(defaultOpen)
  const panelId = useId()

  const reason = (code: CourseWhy['reasons'][number]): string => {
    const key = `why.reason.${code}` as StringKey
    switch (code) {
      case 'career_requirement':
        return tf(key, { n: why.goal_skills.length })
      case 'stage_requirement':
        return tf(key, { stage: labelText(titleLabel(why.stage, ctx)) })
      case 'skill_gap':
        return tf(key, { n: why.to_gain_count, total: why.taught_count })
      default:
        return t(key)
    }
  }

  const coverage =
    why.taught_count === 0 ? null
    : why.to_gain_count === 0 ? t('why.nothingToGain')
    : why.known_count > 0 ? tf('why.knownOf', { n: why.known_count, total: why.taught_count })
    : null

  return (
    <div className={className}>
      <button
        type="button"
        aria-expanded={open}
        aria-controls={panelId}
        onClick={() => setOpen((o) => !o)}
        className="inline-flex min-h-[44px] items-center gap-1 rounded text-xs font-medium text-amber hover:text-amber2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-amber lg:min-h-0"
      >
        {t('why.toggle')}
        <ChevronDown size={12} aria-hidden="true" className={cn('transition-transform', open && 'rotate-180')} />
      </button>

      {open && (
        <div
          id={panelId}
          role="region"
          aria-label={t('why.toggle')}
          className={cn('mt-1 space-y-4 rounded-md border border-border bg-surface/40 p-3 text-sm leading-relaxed text-soft sm:p-4', panelClassName)}
        >
          <dl className="space-y-2 text-sm">
            <div className="sm:flex sm:gap-3">
              <dt className={cn(EYEBROW, 'sm:w-24 sm:shrink-0 sm:pt-0.5')}>{t('why.goal')}</dt>
              <dd className="font-medium text-bright"><LearningLabel parts={roleLabel(why.career_goal, ctx)} /></dd>
            </div>
            {why.fields.length > 0 && (
              <div className="sm:flex sm:gap-3">
                <dt className={cn(EYEBROW, 'sm:w-24 sm:shrink-0 sm:pt-0.5')}>{why.fields.length > 1 ? t('why.fields') : t('why.field')}</dt>
                <dd className="font-medium text-bright">
                  {why.fields.map((f, i) => (
                    <span key={f.slug}>
                      {i > 0 && <span aria-hidden="true" className="text-soft">{' · '}</span>}
                      <LearningLabel parts={fieldLabel(f, ctx, true)} />
                    </span>
                  ))}
                </dd>
              </div>
            )}
          </dl>

          {why.reasons.length > 0 && (
            <ul className="list-disc space-y-1.5 ps-5 marker:text-dim">
              {why.reasons.map((code) => <li key={code}>{reason(code)}</li>)}
            </ul>
          )}

          {coverage && <p className="font-medium text-bright">{coverage}</p>}
          {why.known_skills.length > 0 && (
            <div className="space-y-1.5">
              <p className={EYEBROW}>{t('why.known')}</p>
              <SkillChips skills={why.known_skills} tone="known" />
            </div>
          )}
          {why.skills_to_gain.length > 0 && (
            <div className="space-y-1.5">
              <p className={EYEBROW}>{t('why.gain')}</p>
              <SkillChips skills={why.skills_to_gain} />
            </div>
          )}
          {why.prerequisite_for.length > 0 && (
            <div className="space-y-1.5">
              <p className={EYEBROW}>{t('why.unlocks')}</p>
              <ul className="space-y-1">
                {why.prerequisite_for.map((c) => (
                  <li key={c.slug}>
                    <Link href={`/courses/${c.slug}`} className="text-amber hover:text-amber2">
                      <LearningLabel parts={titleLabel(c, ctx)} />
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
