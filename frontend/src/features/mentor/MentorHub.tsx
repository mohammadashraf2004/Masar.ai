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
import { api } from '@/lib/api'
import type { MentorContextSelection, MentorCourseOption } from './types'
import { wholeCourse } from './context'
import { InterviewMode } from './InterviewTab'
import { mockInterviewAvailable } from './flag'
import { MentorChat } from './MentorChat'
import { StudyPlan } from './StudyPlan'

/** "General" in the course picker: the mentor sees no course and no lesson. */
const NOTHING_ATTACHED: MentorContextSelection = {}

export const TABS = ['chat', 'plan', 'interview'] as const
export type MentorTab = (typeof TABS)[number]

/** `?tab=` wins; the old `?mode=interview` link still lands on the interview. An unknown tab (the
 * removed `?tab=review` included) opens the chat. */
export function tabFromParams(params: { get(name: string): string | null }): MentorTab {
  const tab = params.get('tab')
  if ((TABS as readonly string[]).includes(tab ?? '')) return tab as MentorTab
  return params.get('mode') === 'interview' ? 'interview' : 'chat'
}

/** The "Soon" tag on a tab whose feature is not open yet. */
export function SoonPill({ label }: { label: string }) {
  return (
    <span className="ms-1.5 rounded-full border border-border bg-muted/40 px-1.5 py-px text-[10px] font-medium text-ghost">
      {label}
    </span>
  )
}

/**
 * The mentor hub (Mentor v2 §2): three tabs, kept in `?tab=`. Chat and the weekly plan are the new
 * ones; the interview tab is the existing mock interview, unchanged.
 */
export function MentorHub() {
  const { isLoading } = useAuth()
  const { t: tOld } = useI18n()
  const { t } = useMentorV2I18n()
  const { language } = useMentorV2I18n()
  const router = useRouter()
  const params = useSearchParams()
  const tab = tabFromParams(params)

  // The course the mentor talks about: the one a lesson link (`?lessonId=` / `?exerciseId=`) belongs
  // to, the one chosen in the picker (`?courseId=slug`; an empty `?courseId=` is "General"), else the
  // server's default - the learner's most active course. Always the whole course: the lesson the
  // server resolves is only how it finds the course, and is not attached.
  const lessonId = params.get('lessonId') ?? undefined
  const exerciseId = params.get('exerciseId') ?? undefined
  const courseParam = params.get('courseId')
  const general = courseParam === '' && !lessonId && !exerciseId
  const requested = useMemo(
    () => (lessonId || exerciseId ? { lessonId, exerciseId } : { courseId: courseParam || undefined }),
    [lessonId, exerciseId, courseParam],
  )
  const [base, setBase] = useState<MentorContextSelection>({})
  const [courses, setCourses] = useState<MentorCourseOption[] | undefined>(undefined)

  useEffect(() => {
    if (isLoading || general) return
    let stale = false
    api.getMentorV2Context(requested, language)
      .then((context) => { if (!stale) setBase(wholeCourse(context)) })
      .catch(() => { if (!stale) setBase({}) })
    return () => { stale = true }
  }, [isLoading, requested, general, language])

  useEffect(() => {
    if (isLoading) return
    let stale = false
    // No picker when the list cannot be read: never an empty "enrol in a course" that is not true.
    api.getMentorCourses(language)
      .then((list) => { if (!stale) setCourses(list) })
      .catch(() => { if (!stale) setCourses(undefined) })
    return () => { stale = true }
  }, [isLoading, language])

  const attached = general ? NOTHING_ATTACHED : base

  if (isLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  function go(next: MentorTab) {
    const query = new URLSearchParams()
    if (next !== 'chat') query.set('tab', next)
    if (lessonId) query.set('lessonId', lessonId)
    if (courseParam !== null) query.set('courseId', courseParam)
    const qs = query.toString()
    router.replace(qs ? `/mentor?${qs}` : '/mentor', { scroll: false })
  }

  /** The picker: a course the learner is enrolled in (its next lesson attached), or general. */
  function selectCourse(courseId: string | null) {
    const query = new URLSearchParams()
    if (tab !== 'chat') query.set('tab', tab)
    query.set('courseId', courseId ?? '')
    router.replace(`/mentor?${query.toString()}`, { scroll: false })
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
            data-tour="mentor-tabs"
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
                {value === 'interview' && !mockInterviewAvailable() && <SoonPill label={tOld('interview.soon.badge')} />}
              </button>
            ))}
          </div>
        }
      />
      <PageBody footer={false}>
        <div className="flex flex-wrap items-start gap-5">
          {tab === 'chat' && (
            <MentorChat
              key={attached.courseId ?? ''}
              base={attached}
              courses={courses}
              onSelectCourse={selectCourse}
            />
          )}
          {tab === 'plan' && <div className="w-full"><StudyPlan /></div>}
          {tab === 'interview' && <InterviewMode />}
        </div>
      </PageBody>
    </AppShell>
  )
}
