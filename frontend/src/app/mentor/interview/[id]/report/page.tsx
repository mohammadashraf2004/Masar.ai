'use client'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { ScoreBars } from '@/components/mentor/ScoreBars'
import { buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { useAuth } from '@/hooks/useAuth'
import { useInterviews } from '@/hooks/useInterviews'
import { useI18n, type StringKey } from '@/lib/i18n'
import { formatShortDate } from '@/lib/mentor/format'
import {
  SCORE_DIMENSIONS,
  WEAK_BELOW,
  answeredCount,
  dimensionAverage,
  isWeak,
  overallScore,
  scoreAverage,
  weakQuestions,
  type InterviewSession,
  type ScoreDimension,
} from '@/lib/mentor/interview'
import { mentorMocksEnabled } from '@/lib/mentor/mocks'
// [mentor-v2]
import { InterviewReportPage as InterviewReportV2Page } from '@/features/mentor/InterviewReportPage'
import { mentorV2Enabled, mentorV2MocksAllowed } from '@/features/mentor/flag'
// [/mentor-v2]

/**
 * The interview report (handoff Task 12b, "needed but not designed"): the overall score, the
 * three averages, what went well and what to revisit, every question with its answer and its
 * scores, and a way to ask the weak ones again.
 *
 * Strengths and improvements are read off the scores (the best and worst of the three dimensions,
 * and every question under the bar); nothing is written that the scores do not say. With no
 * scorer (a production build today) the page says so and lists questions and answers only.
 */
function LegacyInterviewReport() {
  const { isLoading } = useAuth()
  const { t } = useI18n()
  const id = String(useParams<{ id: string }>().id ?? '')
  const { interviews, loaded } = useInterviews()
  const session = interviews.find((s) => s.id === id) ?? null

  if (isLoading || !loaded) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  if (!session) {
    return (
      <AppShell>
        <PageHeader title={t('interview.report.title')} contained />
        <PageBody>
          <Card className="flex flex-col items-start gap-4 p-6">
            <p role="alert" className="text-sm text-dim">{t('interview.report.notFound')}</p>
            <Link href="/mentor?mode=interview" className={buttonStyles({ variant: 'ghost' })}>{t('interview.report.back')}</Link>
          </Card>
        </PageBody>
      </AppShell>
    )
  }
  return <Report session={session} />
}

/** Text in another script than the sentence around it (an English role in an Arabic page) is
 *  isolated, so its punctuation stays with it instead of jumping to the other end of the line. */
const isolate = (text: string) => `⁨${text}⁩`

function Report({ session }: { session: InterviewSession }) {
  const { t, tf, language } = useI18n()
  const overall = overallScore(session)
  const averages = SCORE_DIMENSIONS.map((d) => [d, dimensionAverage(session, d)] as const)
  const scored = overall !== null
  const weak = weakQuestions(session)

  const ranked = averages
    .filter((entry): entry is readonly [ScoreDimension, number] => entry[1] !== null)
    .sort((a, b) => b[1] - a[1])
  const best = ranked[0]
  const worst = ranked[ranked.length - 1]
  const dimName = (d: ScoreDimension) => t(`interview.dim.${d}` as StringKey)

  return (
    <AppShell>
      <PageHeader
        title={t('interview.report.title')}
        subtitle={tf('interview.report.subtitle', { role: isolate(session.role), date: formatShortDate(session.startedAt, language) })}
        contained
      />
      <PageBody className="space-y-5">
        <div className="flex flex-wrap items-start gap-5">
          <Card className="flex min-w-0 flex-[1_1_300px] flex-col gap-4 p-[22px]">
            <h2 className="text-sm font-semibold text-white">{t('interview.report.overall')}</h2>
            {scored ? (
              <>
                <p dir="ltr" className="flex items-baseline gap-1.5">
                  <span data-testid="overall-score" className="font-display text-[40px] font-extrabold leading-none text-white">{overall}</span>
                  <span className="text-base text-ghost">/10</span>
                </p>
                <ScoreBars values={{ accuracy: averages[0][1] ?? 0, structure: averages[1][1] ?? 0, clarity: averages[2][1] ?? 0 }} />
              </>
            ) : (
              <p className="text-[13px] leading-relaxed text-dim">{t('interview.report.noScores')}</p>
            )}
            <p className="text-xs text-ghost">
              {tf('interview.report.answered', { n: answeredCount(session), total: session.totalQuestions })}
            </p>
            {scored && mentorMocksEnabled() && <p className="text-xs text-ghost">{t('interview.mockScores')}</p>}
          </Card>

          <div className="flex min-w-0 flex-[2_1_400px] flex-col gap-5">
            <Card className="p-[22px]">
              <h2 className="mb-3 text-sm font-semibold text-white">{t('interview.report.strengths')}</h2>
              {best ? (
                <p className="text-[13px] leading-relaxed text-soft">
                  {tf('interview.report.strong', { dim: dimName(best[0]), score: best[1] })}
                </p>
              ) : (
                <p className="text-[13px] text-ghost">{t('interview.report.nothing')}</p>
              )}
            </Card>
            <Card className="p-[22px]">
              <h2 className="mb-3 text-sm font-semibold text-white">{t('interview.report.improve')}</h2>
              {worst && best && worst[0] !== best[0] && worst[1] < WEAK_BELOW + 2 ? (
                <p className="mb-2 text-[13px] leading-relaxed text-soft">
                  {tf('interview.report.weak', { dim: dimName(worst[0]), score: worst[1] })}
                </p>
              ) : null}
              {weak.length > 0 ? (
                <ul className="space-y-1.5">
                  {weak.map((q) => (
                    <li key={q.id} dir="auto" className="text-[13px] leading-relaxed text-soft">
                      {tf('interview.report.revisit', { question: isolate(q.text) })}
                    </li>
                  ))}
                </ul>
              ) : (
                !(worst && best && worst[0] !== best[0] && worst[1] < WEAK_BELOW + 2) && (
                  <p className="text-[13px] text-ghost">{t('interview.report.nothing')}</p>
                )
              )}
            </Card>
          </div>
        </div>

        <section aria-labelledby="qbq" className="space-y-3">
          <h2 id="qbq" className="text-sm font-semibold text-white">{t('interview.report.questions')}</h2>
          {session.questions.map((q, i) => (
            <Card key={q.id} className="p-[22px]" data-weak={isWeak(q) ? 'true' : 'false'}>
              <div className="flex flex-wrap items-start justify-between gap-x-4 gap-y-1">
                <span className="font-mono text-xs text-amber-text">
                  {tf('interview.counter', { n: i + 1, total: session.totalQuestions })}
                </span>
                <span className="flex items-center gap-2 text-xs text-ghost">
                  {t(`interview.qtype.${q.qtype}` as StringKey)}
                  {q.score && <span dir="ltr" className="font-mono text-sm text-bright">{Math.round(scoreAverage(q.score) * 10) / 10}/10</span>}
                </span>
              </div>
              <p dir="auto" className="mt-2 text-base font-bold leading-[1.6] text-white">{q.text}</p>
              <div className="mt-3 flex flex-wrap gap-x-8 gap-y-4">
                <div className="min-w-0 flex-[2_1_260px]">
                  <p className="mb-1 text-xs text-ghost">{t('interview.report.yourAnswer')}</p>
                  {q.skipped ? (
                    <p className="text-[13px] text-dim">
                      <span className="font-medium text-rose">{t('interview.report.skipped')}</span> · {t('interview.note.empty')}
                    </p>
                  ) : (
                    <p dir="auto" className="whitespace-pre-wrap text-[13px] leading-[1.7] text-soft [overflow-wrap:anywhere]">{q.answer}</p>
                  )}
                  {q.score && (
                    <p className="mt-3 rounded-lg bg-panel p-3 text-[13px] leading-relaxed text-soft">
                      <span className="font-semibold text-amber-text">{t('interview.note.label')} </span>
                      {'key' in q.score.note ? t(q.score.note.key) : q.score.note.text}
                    </p>
                  )}
                </div>
                {q.score && (
                  <div className="min-w-0 flex-[1_1_220px]">
                    <ScoreBars values={q.score} />
                  </div>
                )}
              </div>
            </Card>
          ))}
        </section>

        <div className="flex flex-wrap items-center gap-3">
          {weak.length > 0 ? (
            <Link href={`/mentor/interview/new?retry=${encodeURIComponent(session.id)}`} className={buttonStyles()}>
              {t('interview.report.retry')}
            </Link>
          ) : (
            <p className="text-[13px] text-dim">{t('interview.report.retryNone')}</p>
          )}
          <Link href="/mentor/interview/new" className={buttonStyles({ variant: 'outline' })}>{t('interview.report.new')}</Link>
          <Link href="/mentor?mode=interview" className={buttonStyles({ variant: 'ghost' })}>{t('interview.report.back')}</Link>
        </div>
      </PageBody>
    </AppShell>
  )
}

// [mentor-v2] The v2 report has no server behind it yet (its content is a fixture), so it is shown
// only on a fixture build. With the live mentor - production - learners get the page above, which
// is built from their own interview.
export default function InterviewReportPage() {
  return mentorV2Enabled() && mentorV2MocksAllowed() ? <InterviewReportV2Page /> : <LegacyInterviewReport />
}
// [/mentor-v2]
