'use client'
import Link from 'next/link'
import { Clock } from 'lucide-react'
import { AppShell } from '@/components/layout/AppShell'
import { PageBody } from '@/components/layout/PageContainer'
import { PageHeader } from '@/components/layout/PageHeader'
import { InterviewSide } from '@/components/mentor/InterviewSide'
import { InterviewStage } from '@/components/mentor/InterviewStage'
import { buttonStyles } from '@/components/ui/Button'
import { Badge, Card, Spinner } from '@/components/ui/index'
import { useAuth } from '@/hooks/useAuth'
import { useInterviewRun } from '@/hooks/useInterviewRun'
import { useInterviews } from '@/hooks/useInterviews'
import { useI18n } from '@/lib/i18n'
import { mockInterviewAvailable } from './flag'

/**
 * The mock-interview mode of the mentor: the running interview, or the invitation to start one.
 * It was part of `app/mentor/page.tsx`; the hub tab and the page now share it. Render it inside a
 * wrapping flex row, as it returns the stage and its side column as siblings.
 */
export function InterviewMode() {
  return mockInterviewAvailable() ? <AvailableInterviewMode /> : <InterviewComingSoon />
}

function AvailableInterviewMode() {
  const { interviews, loaded } = useInterviews()
  const active = loaded ? (interviews.find((s) => s.endedAt === null) ?? null) : null

  if (!loaded) {
    return <div className="flex w-full justify-center py-16"><Spinner announce className="h-6 w-6" /></div>
  }
  return active ? <ActiveInterview id={active.id} /> : <NoInterview />
}

function ActiveInterview({ id }: { id: string }) {
  const { user } = useAuth()
  const run = useInterviewRun(id, user?.experience_level)
  if (!run.session) return null
  return (
    <>
      <InterviewStage run={run} session={run.session} />
      <InterviewSide session={run.session} scoring={run.scoring} scoringOn={run.scoringOn} scoresAreMock={run.scoresAreMock} />
    </>
  )
}

function NoInterview() {
  const { t } = useI18n()
  return (
    <>
      <Card className="flex min-w-0 flex-[2_1_480px] flex-col items-start gap-3 p-6">
        <h2 className="ui-card-title">{t('interview.none.title')}</h2>
        <p className="max-w-prose text-sm leading-relaxed text-dim">{t('interview.none.body')}</p>
        <Link href="/mentor/interview/new" className={buttonStyles({ className: 'mt-1' })}>{t('interview.report.new')}</Link>
      </Card>
      <InterviewSide session={null} />
    </>
  )
}

/** What learners see while the mock interview is not open yet (see `mockInterviewAvailable`). */
export function InterviewComingSoon({ backLink = false }: { backLink?: boolean }) {
  const { t } = useI18n()
  return (
    <Card data-testid="interview-coming-soon" className="flex w-full min-w-0 flex-col items-start gap-3 p-6">
      <Badge variant="ghost" className="gap-1"><Clock size={12} aria-hidden /> {t('interview.soon.badge')}</Badge>
      <h2 className="ui-card-title">{t('interview.soon.title')}</h2>
      <p className="max-w-prose text-sm leading-relaxed text-dim">{t('interview.soon.body')}</p>
      {backLink && (
        <Link href="/mentor" className={buttonStyles({ variant: 'ghost', className: 'mt-1' })}>{t('interview.report.back')}</Link>
      )}
    </Card>
  )
}

/** The interview setup and report routes while the mock interview is not open yet: a saved link
 *  to either lands on the same notice as the tab. */
export function InterviewComingSoonPage() {
  const { isLoading } = useAuth()
  const { t } = useI18n()
  if (isLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }
  return (
    <AppShell>
      <PageHeader title={t('mentor.mode.interview')} subtitle={t('mentor.subtitle')} contained />
      <PageBody>
        <InterviewComingSoon backLink />
      </PageBody>
    </AppShell>
  )
}
