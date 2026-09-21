'use client'
import { useI18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'

export interface SkillGapSummaryProps {
  known: number
  partial: number
  missing: number
  /** How many skills are relevant to this learner's roadmap. */
  total: number
  /** Declared share of those skills, as the server reports it. Not recomputed here. */
  coveragePct: number | null
  /** Missing skills a required course in the current stage teaches. */
  immediate?: number
  className?: string
}

/**
 * "Skill coverage": how much of what this roadmap teaches the learner has said
 * they know, and how the rest divides into in-progress and still to gain.
 *
 * Purely presentational. The counts and the percentage come from the backend
 * (`GET /learning/my-skill-gaps`), so the roadmap, the dashboard and My Skills
 * can all draw the same summary and can never disagree about it.
 */
export function SkillGapSummary({ known, partial, missing, total, coveragePct, immediate = 0, className }: SkillGapSummaryProps) {
  const { t, tf } = useI18n()

  if (total === 0 || coveragePct === null) {
    return <p className={cn('text-sm text-soft', className)}>{t('gap.none')}</p>
  }
  const pct = Math.round(coveragePct)

  return (
    <section aria-label={t('gap.coverage')} className={className}>
      <div className="flex items-baseline justify-between gap-3 text-xs">
        <span className="font-medium uppercase tracking-widest text-soft">{t('gap.coverage')}</span>
        <span className="font-mono text-amber" dir="ltr">{pct}%</span>
      </div>
      <div
        role="progressbar"
        aria-label={t('gap.coverage')}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={pct}
        className="progress-track mt-1.5 h-2 w-full"
      >
        <div className="progress-fill bg-gradient-to-r from-emerald to-emerald" style={{ width: `${pct}%` }} />
      </div>
      <p className="mt-2 text-xs text-soft">{tf('gap.coverageOf', { known, total })}</p>
      <ul className="mt-1.5 flex flex-wrap gap-x-4 gap-y-1 text-xs">
        <li className="text-emerald">{tf('gap.legend.known', { n: known })}</li>
        {partial > 0 && <li className="text-amber">{tf('gap.legend.partial', { n: partial })}</li>}
        <li className="text-soft">{tf('gap.legend.missing', { n: missing })}</li>
        {immediate > 0 && <li className="text-bright">{tf('gap.immediateCount', { n: immediate })}</li>}
      </ul>
    </section>
  )
}
