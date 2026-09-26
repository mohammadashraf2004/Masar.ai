'use client'
import { useI18n, type StringKey } from '@/lib/i18n'
import { SCORE_DIMENSIONS, type ScoreDimension } from '@/lib/mentor/interview'

/** The three scores as 4px bars, `--acc` on a track, each with its label and "n/10". */
export function ScoreBars({ values }: { values: Record<ScoreDimension, number> }) {
  const { t } = useI18n()
  return (
    <ul className="space-y-2.5">
      {SCORE_DIMENSIONS.map((dimension) => {
        const value = values[dimension]
        return (
          <li key={dimension}>
            <div className="mb-1 flex items-baseline justify-between gap-3 text-xs">
              <span className="text-dim">{t(`interview.dim.${dimension}` as StringKey)}</span>
              <span dir="ltr" className="font-mono text-bright">{value}/10</span>
            </div>
            <div
              role="meter"
              aria-label={t(`interview.dim.${dimension}` as StringKey)}
              aria-valuemin={0}
              aria-valuemax={10}
              aria-valuenow={value}
              className="h-1 overflow-hidden rounded-full bg-muted"
            >
              <div className="h-full rounded-full bg-amber" style={{ width: `${Math.max(0, Math.min(10, value)) * 10}%` }} />
            </div>
          </li>
        )
      })}
    </ul>
  )
}
