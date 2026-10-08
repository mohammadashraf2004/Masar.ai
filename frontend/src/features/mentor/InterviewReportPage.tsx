'use client'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { AppShell } from '@/components/layout/AppShell'
import { PageBody } from '@/components/layout/PageContainer'
import { PageHeader } from '@/components/layout/PageHeader'
import { buttonStyles } from '@/components/ui/Button'
import { Spinner } from '@/components/ui/index'
import { useAuth } from '@/hooks/useAuth'
import { useMentorV2I18n } from '@/lib/i18n'
import { InterviewReport } from './InterviewReport'

/** `/mentor/interview/[id]/report` with the v2 report: where "View the report" at the end of an interview lands. */
export function InterviewReportPage() {
  const { isLoading } = useAuth()
  const { t } = useMentorV2I18n()
  const id = String(useParams<{ id: string }>().id ?? '')

  if (isLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }
  return (
    <AppShell>
      <PageHeader
        title={t('mentor.v2.report.title')}
        contained
        action={<Link href="/mentor?tab=interview" className={buttonStyles({ variant: 'ghost' })}>{t('mentor.v2.report.back')}</Link>}
      />
      <PageBody><InterviewReport id={id} /></PageBody>
    </AppShell>
  )
}
