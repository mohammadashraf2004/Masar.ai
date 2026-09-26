'use client'
import Link from 'next/link'
import { Card, Spinner } from '@/components/ui/index'
import { buttonStyles } from '@/components/ui/Button'
import { ScoreBars } from '@/components/mentor/ScoreBars'
import { useInterviews } from '@/hooks/useInterviews'
import { useI18n } from '@/lib/i18n'
import { formatShortDate } from '@/lib/mentor/format'
import { isFinished, lastScored, overallScore, scoreAverage, type InterviewSession } from '@/lib/mentor/interview'
import { getAnswerScorer } from '@/lib/mentor/scoring'

/**
 * The interview mode's side column (handoff Task 12b): the last answer's score, and earlier
 * interviews. With no `session` (nothing in progress) only the history shows.
 */
export function InterviewSide({
  session,
  scoring = false,
  scoringOn,
  scoresAreMock,
}: {
  session: InterviewSession | null
  scoring?: boolean
  scoringOn?: boolean
  scoresAreMock?: boolean
}) {
  const { t, tf, language } = useI18n()
  const { interviews, loaded } = useInterviews()
  const past = interviews.filter(isFinished)
  const on = scoringOn ?? getAnswerScorer() !== null
  const last = session ? lastScored(session) : null
  const score = last?.score ?? null

  return (
    <div className="flex min-w-0 flex-[1_1_280px] flex-col gap-5">
      {session && (
        <Card className="p-5">
          <h2 className="mb-3 text-sm font-semibold text-white">{t(on ? 'interview.lastScore' : 'interview.scoresOff.title')}</h2>
          {!on ? (
            <p className="text-[13px] leading-relaxed text-dim">{t('interview.scoresOff')}</p>
          ) : score && last ? (
            <div className="space-y-4">
              <p dir="ltr" className="flex items-baseline gap-1">
                <span className="font-display text-[22px] font-extrabold text-white">{Math.round(scoreAverage(score) * 10) / 10}</span>
                <span className="text-sm text-ghost">/10</span>
              </p>
              <ScoreBars values={score} />
              <p className="rounded-lg bg-panel p-3 text-[13px] leading-relaxed text-soft">
                <span className="font-semibold text-amber-text">{t('interview.note.label')} </span>
                {'key' in score.note ? t(score.note.key) : score.note.text}
              </p>
              {scoresAreMock && <p className="text-xs text-ghost">{t('interview.mockScores')}</p>}
            </div>
          ) : scoring ? (
            <p role="status" className="flex items-center gap-2 text-[13px] text-dim">
              <Spinner className="h-4 w-4" />
              {t('interview.scoring')}
            </p>
          ) : (
            <p className="text-[13px] leading-relaxed text-dim">{t('interview.lastScore.none')}</p>
          )}
        </Card>
      )}

      <Card className="p-5">
        <h2 className="mb-2 text-sm font-semibold text-white">{t('interview.history')}</h2>
        {loaded && past.length === 0 ? (
          <p className="py-1 text-[13px] text-ghost">{t('interview.history.empty')}</p>
        ) : (
          <ul>
            {past.slice(0, 6).map((item) => {
              const overall = overallScore(item)
              return (
                <li key={item.id} className="border-t border-border first:border-t-0">
                  <Link
                    href={`/mentor/interview/${item.id}/report`}
                    className="flex min-h-[44px] items-center justify-between gap-3 py-2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                  >
                    <span className="min-w-0">
                      <span dir="ltr" className="block truncate font-display text-[13px] font-bold text-white">{item.role}</span>
                      <span className="block text-xs text-ghost">
                        {tf('interview.history.meta', { questions: item.questions.length, date: formatShortDate(item.startedAt, language) })}
                      </span>
                    </span>
                    <span dir="ltr" className="shrink-0 font-mono text-sm text-bright">
                      {overall === null ? (
                        <>
                          <span aria-hidden="true" className="text-ghost">—</span>
                          <span className="sr-only">{t('interview.history.unscored')}</span>
                        </>
                      ) : (
                        overall
                      )}
                    </span>
                  </Link>
                </li>
              )
            })}
          </ul>
        )}
        {/* Where they are kept is the browser's: a different device or a cleared browser has none. */}
        <p className="mt-2 text-xs text-ghost">{t('interview.history.local')}</p>
        <Link href="/mentor/interview/new" className={buttonStyles({ variant: 'outline', className: 'mt-3 w-full' })}>
          {t('interview.report.new')}
        </Link>
      </Card>
    </div>
  )
}
