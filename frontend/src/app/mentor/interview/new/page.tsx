'use client'
import { Suspense, useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { CameraTile } from '@/components/mentor/CameraTile'
import { ChoiceGroup } from '@/components/mentor/ChoiceGroup'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { useAuth } from '@/hooks/useAuth'
import { useCamera } from '@/hooks/useCamera'
import { useInterviews } from '@/hooks/useInterviews'
import { useMicCheck } from '@/hooks/useMicCheck'
import { useSpeechSupported } from '@/hooks/useSpeechRecognition'
import { api } from '@/lib/api'
import { useI18n, type StringKey } from '@/lib/i18n'
import {
  DURATIONS,
  INTERVIEW_TYPES,
  MOCK_INTERVIEW_CREDITS,
  QUESTIONS_FOR,
  buildSession,
  endSession,
  freshCopy,
  weakQuestions,
  type Duration,
  type InterviewLanguage,
  type InterviewType,
} from '@/lib/mentor/interview'
import { interviewStore, newInterviewId } from '@/lib/mentor/interviewStore'
import type { CareerTrackSummary } from '@/types'

/**
 * The interview setup step (handoff Task 12b, "needed but not designed"): role, type, language
 * and length, a camera and microphone check, and what it costs. Built from the same chips, cards
 * and buttons as the rest of the mentor. `?retry=<id>` asks the weak questions of an earlier
 * interview again, and then the role, type and length are that interview's.
 */
export default function InterviewSetupPage() {
  return (
    <Suspense fallback={null}>
      <Setup />
    </Suspense>
  )
}

function Setup() {
  const { isLoading } = useAuth()
  const { t, tf, language } = useI18n()
  const router = useRouter()
  const retryId = useSearchParams().get('retry')
  const { interviews, loaded } = useInterviews()
  const camera = useCamera()
  const speechSupported = useSpeechSupported()
  const mic = useMicCheck()

  const [tracks, setTracks] = useState<CareerTrackSummary[] | null>(null)
  const [tracksFailed, setTracksFailed] = useState(false)
  const [attempt, setAttempt] = useState(0)
  const [pickedRole, setRole] = useState<string | null>(null)
  const [pickedType, setType] = useState<InterviewType>('technical')
  const [pickedLanguage, setInterviewLanguage] = useState<InterviewLanguage>(language)
  const [pickedDuration, setDuration] = useState<Duration>(30)

  // A retry: the earlier interview's weak questions, and its role, type, language and length.
  const source = useMemo(() => (retryId ? (interviews.find((s) => s.id === retryId) ?? null) : null), [interviews, retryId])
  const weak = useMemo(() => (source ? weakQuestions(source) : []), [source])
  const retrying = source !== null && weak.length > 0
  const inProgress = loaded && interviews.some((s) => s.endedAt === null)
  // What is chosen: the earlier interview's own settings when retrying, else the picks.
  const role = retrying && source ? source.role : pickedRole
  const type = retrying && source ? source.type : pickedType
  const interviewLanguage = retrying && source ? source.language : pickedLanguage
  const duration = retrying && source ? source.durationMin : pickedDuration


  useEffect(() => {
    if (isLoading) return
    let alive = true
    api
      .listTracks()
      .then((list) => alive && setTracks(list))
      .catch(() => alive && setTracksFailed(true))
    return () => {
      alive = false
    }
  }, [isLoading, attempt])

  if (isLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  const roleChoices = (tracks ?? []).map((track) => ({
    value: track.title,
    label: language === 'ar' && track.title_ar ? track.title_ar : track.title,
  }))
  // A retry's role may not be one of today's tracks: keep it selectable rather than lose it.
  if (retrying && source && !roleChoices.some((c) => c.value === source.role)) {
    roleChoices.unshift({ value: source.role, label: source.role })
  }

  const questions = retrying ? weak.length : QUESTIONS_FOR[duration]
  const cost = questions * MOCK_INTERVIEW_CREDITS
  const ready = role !== null && (loaded || !retryId)

  function start() {
    if (!role) return
    const running = interviewStore.active()
    if (running) interviewStore.save(endSession(running))
    const id = newInterviewId()
    interviewStore.save(
      buildSession(id, {
        role,
        type,
        language: interviewLanguage,
        durationMin: duration,
        questions: retrying ? weak.map(freshCopy) : undefined,
        retryOf: retrying && source ? source.id : null,
      }),
    )
    router.push('/mentor?mode=interview')
  }

  const micMessage: Record<string, StringKey> = {
    idle: 'interview.mic.idle',
    testing: 'interview.mic.testing',
    ok: 'interview.mic.ok',
    denied: 'interview.mic.denied',
    none: 'interview.mic.none',
    error: 'interview.mic.error',
  }

  return (
    <AppShell>
      <PageHeader title={t('interview.setup.title')} subtitle={t('mentor.subtitle')} contained />
      <PageBody>
        <div className="flex flex-wrap items-start gap-5">
          <Card className="flex min-w-0 flex-[2_1_480px] flex-col gap-6 p-[22px]">
            {retrying && (
              <p role="note" className="rounded-lg border border-amber/30 bg-amber-soft p-3 text-[13px] text-bright">
                {tf('interview.setup.retry', { n: weak.length })}
              </p>
            )}
            {inProgress && (
              <p role="note" className="rounded-lg border border-border bg-panel p-3 text-[13px] text-dim">
                {t('interview.setup.inProgress')}
              </p>
            )}

            {tracksFailed ? (
              <div className="flex flex-wrap items-center gap-3">
                <p role="alert" className="text-sm text-rose">{t('interview.tracks.error')}</p>
                <Button variant="ghost" size="sm" onClick={() => { setTracksFailed(false); setAttempt((n) => n + 1) }}>{t('common.retry')}</Button>
              </div>
            ) : tracks === null && !retrying ? (
              <Spinner announce className="h-5 w-5" />
            ) : (
              <ChoiceGroup legend={t('interview.role')} choices={roleChoices} value={role} onChange={setRole} disabled={retrying} dir="auto" />
            )}

            <ChoiceGroup
              legend={t('interview.type')}
              choices={INTERVIEW_TYPES.map((value) => ({ value, label: t(`interview.type.${value}` as StringKey) }))}
              value={type}
              onChange={setType}
              disabled={retrying}
            />

            <div className="space-y-2">
              <ChoiceGroup
                legend={t('interview.language')}
                choices={[
                  { value: 'ar' as const, label: t('lang.arabic') },
                  { value: 'en' as const, label: t('lang.english') },
                ]}
                value={interviewLanguage}
                onChange={setInterviewLanguage}
                disabled={retrying}
              />
              <p className="text-xs text-ghost">{t('interview.langNote')}</p>
            </div>

            <ChoiceGroup
              legend={t('interview.duration')}
              choices={DURATIONS.map((value) => ({ value, label: tf('interview.minutes', { n: value }) }))}
              value={duration}
              onChange={setDuration}
              disabled={retrying}
            />
          </Card>

          <div className="flex min-w-0 flex-[1_1_280px] flex-col gap-5">
            <Card className="flex flex-col gap-4 p-5">
              <div>
                <h2 className="text-sm font-semibold text-white">{t('interview.check.title')}</h2>
                <p className="mt-1 text-xs leading-relaxed text-ghost">{t('interview.check.optional')}</p>
              </div>
              <CameraTile camera={camera} label={t('interview.check.camera')} />
              {speechSupported && (
                <div className="flex flex-wrap items-center justify-between gap-2 border-t border-border pt-3">
                  <div className="min-w-0">
                    <p className="text-[13px] font-medium text-soft">{t('interview.check.mic')}</p>
                    <p role="status" className="text-xs text-dim">{t(micMessage[mic.state])}</p>
                  </div>
                  <Button variant="ghost" size="sm" onClick={() => void mic.test()} loading={mic.state === 'testing'}>
                    {t('interview.check.micBtn')}
                  </Button>
                </div>
              )}
            </Card>

            <Card className="flex flex-col gap-3 p-5">
              <p className="text-[13px] text-dim">{tf('interview.questions', { n: questions })}</p>
              <p className="text-[13px] font-medium text-bright">
                {retrying ? t('interview.cost.retry') : tf('interview.cost', { n: cost, per: MOCK_INTERVIEW_CREDITS })}
              </p>
              <Button onClick={start} disabled={!ready} size="lg">{t('interview.start')}</Button>
              <Link href="/mentor?mode=interview" className={buttonStyles({ variant: 'ghost', className: 'w-full' })}>
                {t('interview.report.back')}
              </Link>
            </Card>
          </div>
        </div>
      </PageBody>
    </AppShell>
  )
}
