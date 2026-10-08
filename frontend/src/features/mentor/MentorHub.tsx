'use client'
import { useEffect, useMemo, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { AppShell } from '@/components/layout/AppShell'
import { PageBody } from '@/components/layout/PageContainer'
import { PageHeader } from '@/components/layout/PageHeader'
import { Spinner } from '@/components/ui/index'
import { useAuth } from '@/hooks/useAuth'
import { useI18n, useMentorV2I18n, type MentorV2Key } from '@/lib/i18n'
import { cn } from '@/lib/utils'
import { CodeReview } from './CodeReview'
import { api } from '@/lib/api'
import type { MentorContextSelection } from './types'
import { InterviewMode } from './InterviewTab'
import { MentorChat } from './MentorChat'
import { StudyPlan } from './StudyPlan'

export const TABS = ['chat', 'review', 'plan', 'interview'] as const
export type MentorTab = (typeof TABS)[number]

/** `?tab=` wins; the old `?mode=interview` link still lands on the interview. */
export function tabFromParams(params: { get(name: string): string | null }): MentorTab {
  const tab = params.get('tab')
  if ((TABS as readonly string[]).includes(tab ?? '')) return tab as MentorTab
  return params.get('mode') === 'interview' ? 'interview' : 'chat'
}

/**
 * The mentor hub (Mentor v2 §2): four tabs, kept in `?tab=`. Chat, code review and the weekly plan are
 * the new ones; the interview tab is the existing mock interview, unchanged.
 */
export function MentorHub() {
  const { isLoading } = useAuth()
  const { t: tOld } = useI18n()
  const { t } = useMentorV2I18n()
  const { language } = useMentorV2I18n()
  const router = useRouter()
  const params = useSearchParams()
  const tab = tabFromParams(params)

  // The lesson the mentor starts from: the server's last-active one, or the ids a link carries
  // (the exercise's "ask for a review" button opens `?tab=review&exerciseId=…`).
  const lessonId = params.get('lessonId') ?? undefined
  const exerciseId = params.get('exerciseId') ?? undefined
  const requested = useMemo(() => ({ lessonId, exerciseId }), [lessonId, exerciseId])
  const [base, setBase] = useState<MentorContextSelection>({})

  useEffect(() => {
    if (isLoading) return
    let stale = false
    api.getMentorV2Context(requested, language)
      .then((context) => { if (!stale) setBase(context) })
      .catch(() => { if (!stale) setBase({}) })
    return () => { stale = true }
  }, [isLoading, requested, language])

  if (isLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  function go(next: MentorTab) {
    const query = new URLSearchParams()
    if (next !== 'chat') query.set('tab', next)
    if (next === 'review' && exerciseId) query.set('exerciseId', exerciseId)
    if (lessonId) query.set('lessonId', lessonId)
    const qs = query.toString()
    router.replace(qs ? `/mentor?${qs}` : '/mentor', { scroll: false })
  }

  return (
    <AppShell>
      <PageHeader
        title={tOld('nav.mentor')}
        subtitle={t('mentor.v2.subtitle')}
        contained
        action={
          <div
            role="group"
            aria-label={t('mentor.v2.tabs.label')}
            className="flex max-w-full flex-none gap-1 overflow-x-auto rounded-[10px] border border-border bg-surface p-1 [scrollbar-width:none]"
          >
            {TABS.map((value) => (
              <button
                key={value}
                type="button"
                aria-pressed={tab === value}
                data-tour={value === 'interview' ? 'interview-tab' : undefined}
                onClick={() => go(value)}
                className={cn(
                  'min-h-[44px] shrink-0 whitespace-nowrap rounded-[7px] border px-3.5 text-[13px] transition-colors lg:h-9 lg:min-h-0',
                  'focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring',
                  tab === value ? 'border-border bg-panel font-semibold text-white' : 'border-transparent text-dim hover:text-bright',
                )}
              >
                {t(`mentor.v2.tabs.${value}` as MentorV2Key)}
              </button>
            ))}
          </div>
        }
      />
      <PageBody footer={false}>
        <div className="flex flex-wrap items-start gap-5">
          {tab === 'chat' && <MentorChat key={`${base.courseId ?? ''}:${base.lessonId ?? ''}:${base.exerciseId ?? ''}`} base={base} />}
          {tab === 'review' && <div className="w-full"><CodeReview key={exerciseId ?? 'default'} exerciseId={exerciseId} /></div>}
          {tab === 'plan' && <div className="w-full"><StudyPlan /></div>}
          {tab === 'interview' && <InterviewMode />}
        </div>
      </PageBody>
    </AppShell>
  )
}
