'use client'
import { Suspense, useMemo } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { ChatCard } from '@/components/mentor/ChatCard'
import { ChatSide } from '@/components/mentor/ChatSide'
import { InterviewSide } from '@/components/mentor/InterviewSide'
import { InterviewStage } from '@/components/mentor/InterviewStage'
import { buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { useAuth } from '@/hooks/useAuth'
import { useInterviewRun } from '@/hooks/useInterviewRun'
import { useInterviews } from '@/hooks/useInterviews'
import { useMentorChat } from '@/hooks/useMentorChat'
import { useI18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'

type Mode = 'chat' | 'interview'
const MODES: readonly Mode[] = ['chat', 'interview']

/**
 * The AI mentor (handoff Task 12): a chat and a mock interview behind one segmented control, the
 * mode kept in the URL (`?mode=interview`) so a link, a reload and the back button all land where
 * they should. What each mode is built on, and what is a stand-in, is in docs/backend-requests.md.
 */
export default function MentorPage() {
  return (
    <Suspense fallback={null}>
      <MentorScreen />
    </Suspense>
  )
}

function MentorScreen() {
  const { isLoading } = useAuth()
  const { t } = useI18n()
  const router = useRouter()
  const params = useSearchParams()
  const mode: Mode = params.get('mode') === 'interview' ? 'interview' : 'chat'

  if (isLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  return (
    <AppShell>
      <PageHeader
        title={t('nav.mentor')}
        subtitle={t('mentor.subtitle')}
        contained
        action={
          <div role="group" aria-label={t('mentor.modes')} className="flex gap-1 rounded-[10px] border border-border bg-surface p-1">
            {MODES.map((value) => (
              <button
                key={value}
                type="button"
                aria-pressed={mode === value}
                data-tour={value === 'interview' ? 'interview-tab' : undefined}
                onClick={() => router.replace(value === 'chat' ? '/mentor' : `/mentor?mode=${value}`, { scroll: false })}
                className={cn(
                  'min-h-[44px] rounded-[7px] border px-3.5 py-2 text-[13px] transition-colors lg:min-h-0',
                  'focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring',
                  mode === value ? 'border-border bg-panel font-semibold text-white' : 'border-transparent text-dim hover:text-bright',
                )}
              >
                {t(value === 'chat' ? 'mentor.mode.chat' : 'mentor.mode.interview')}
              </button>
            ))}
          </div>
        }
      />
      <PageBody footer={false}>
        <div className="flex flex-wrap items-start gap-5">
          {mode === 'chat' ? <ChatMode /> : <InterviewMode />}
        </div>
      </PageBody>
    </AppShell>
  )
}

function ChatMode() {
  const { user } = useAuth()
  const { t, language, mode } = useI18n()
  const params = useSearchParams()
  const prefs = useMemo(() => ({ language, terminology_mode: mode }), [language, mode])
  const chat = useMentorChat({ prefs, greeting: t('mentor.greeting'), search: params.toString() })
  const level = user?.experience_level ?? 'beginner'
  const readiness = Math.round(user?.overall_readiness_score ?? 0)

  return (
    <>
      <div className="min-w-0 flex-[2_1_480px]">
        <ChatCard chat={chat} />
      </div>
      <ChatSide chat={chat} name={user?.full_name ?? ''} level={level} readiness={readiness} />
    </>
  )
}

function InterviewMode() {
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
        <h2 className="text-base font-bold text-white">{t('interview.none.title')}</h2>
        <p className="max-w-prose text-sm leading-relaxed text-dim">{t('interview.none.body')}</p>
        <Link href="/mentor/interview/new" className={buttonStyles({ className: 'mt-1' })}>{t('interview.report.new')}</Link>
      </Card>
      <InterviewSide session={null} />
    </>
  )
}
