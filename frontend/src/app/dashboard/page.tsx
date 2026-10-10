'use client'
import { Suspense, useEffect, useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { VocabularyProgress } from '@/components/ui/VocabularyProgress'
import { Card, ProgressBar, Badge, Spinner } from '@/components/ui/index'
import { Button, buttonStyles } from '@/components/ui/Button'
import { PaymentResultBanner } from '@/components/ui/PaymentResultBanner'
import { LearningSuggestions } from '@/components/learning/LearningSuggestions'
import { YourMasarCard } from '@/components/learning/YourMasarCard'
import { api } from '@/lib/api'
import { useI18n, type StringKey } from '@/lib/i18n'
import { localizedTitle } from '@/lib/content-language'
import type { Enrollment, SkillScore, RoadmapWeek } from '@/types'
import { Brain, BookOpen, ArrowRight, Zap, Target, TrendingUp, Clock } from 'lucide-react'
import { scoreColor, getErrorMessage } from '@/lib/utils'

// What one run of "Generate roadmap" costs. The API charges it; this is only what the page says.
const ROADMAP_CREDITS = 5

export default function DashboardPage() {
  const { user, isLoading: authLoading } = useAuth()
  const { t, tf, language, weeks } = useI18n()
  const [enrollments, setEnrollments] = useState<Enrollment[]>([])
  const [skills, setSkills] = useState<SkillScore[]>([])
  const [roadmap, setRoadmap] = useState<RoadmapWeek[]>([])
  const [roadmapLoading, setRoadmapLoading] = useState(false)
  const [roadmapError, setRoadmapError] = useState('')
  const [dataLoading, setDataLoading] = useState(true)

  useEffect(() => {
    if (authLoading) return
    async function load() {
      try {
        const [enr, scoreData] = await Promise.all([
          api.getMyEnrollments(),
          api.getSkillScores(),
        ])
        setEnrollments(enr)
        setSkills(scoreData.skills)
        // The roadmap is NOT fetched here. Generating one is a live LLM call
        // that costs 5 credits, and doing it on mount billed the student for
        // simply opening — or re-opening — this page, with the cost hidden
        // because the failure path was swallowed. It is now explicit: see
        // generateRoadmap below.
      } catch {}
      setDataLoading(false)
    }
    load()
  }, [authLoading])

  async function generateRoadmap() {
    if (roadmapLoading || enrollments.length === 0) return
    setRoadmapLoading(true)
    setRoadmapError('')
    try {
      const rm = await api.getRoadmap(enrollments[0].track.title)
      setRoadmap(rm.weeks)
    } catch (err) {
      // Deliberately surfaced rather than swallowed: running out of credits
      // is the most likely failure here, and the student needs to be told.
      const detail = (err as { response?: { data?: { detail?: unknown } } })?.response?.data?.detail
      if (typeof detail === 'object' && detail !== null && 'error' in detail
          && (detail as { error?: string }).error === 'insufficient_credits') {
        setRoadmapError(t('dash.noCredits'))
      } else {
        setRoadmapError(getErrorMessage(err))
      }
    }
    setRoadmapLoading(false)
  }

  if (authLoading) {
    return (
      <div className="min-h-dvh bg-void flex items-center justify-center">
        <Spinner announce className="w-6 h-6" />
      </div>
    )
  }

  const readiness = user?.overall_readiness_score ?? 0
  const first = user?.full_name?.split(' ')[0]

  return (
    <AppShell>
      <PageHeader
        title={first ? tf(`dash.greeting.${getGreeting()}` as StringKey, { name: first }) : t('nav.dashboard')}
        subtitle={t('dash.subtitle')}
        wrapTitle
        contained
      />

      <PageBody className="space-y-6">
        <Suspense fallback={null}>
          <PaymentResultBanner />
        </Suspense>

        {/* The new path-based experience; an account that has not answered the
            new onboarding is prompted here rather than redirected. */}
        <YourMasarCard />

        {/* A phone has no sidebar to find the challenges in; the desktop has it there. The
            walkthrough's "practice" step points at this on a phone. */}
        <Card data-tour="practice" className="flex items-center justify-between gap-3 p-4 lg:hidden">
          <div className="min-w-0">
            <h2 className="ui-card-title">{t('nav.challenges')}</h2>
            <p className="mt-0.5 text-xs leading-relaxed text-soft">{t('dash.challenges.body')}</p>
          </div>
          <Link href="/challenges" className={buttonStyles({ variant: 'outline', size: 'sm', className: 'shrink-0' })}>
            {t('dash.challenges.cta')} <ArrowRight size={12} className="rtl:rotate-180" aria-hidden="true" />
          </Link>
        </Card>

        {/* Continue / recommended next: works with no career goal or roadmap at all. */}
        <LearningSuggestions />

        {/* Metrics. Amber and nothing else: the number is the headline colour, the icon
            sits in a 36px amber-soft square, and a status colour appears only where the
            value itself means good or bad - a readiness score, once there is one. A
            fresh account's 0% is "nothing yet", not "bad", so it stays plain. */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { label: t('dash.stat.readiness'), value: `${readiness.toFixed(0)}%`, sub: t('dash.stat.overall'), icon: Target, tone: readiness > 0 ? scoreColor(readiness) : 'text-white' },
            { label: t('dash.stat.tracks'), value: enrollments.length, sub: dataLoading ? '…' : t('dash.stat.active'), icon: BookOpen, tone: 'text-white' },
            { label: t('dash.stat.skills'), value: skills.length, sub: dataLoading ? '…' : t('dash.stat.assessed'), icon: TrendingUp, tone: 'text-white' },
            { label: t('dash.stat.week'), value: roadmap[0]?.theme ?? '—', sub: roadmap[0] ? t('dash.stat.focus') : t('dash.stat.generate'), icon: Clock, tone: 'text-white' },
          ].map(({ label, value, sub, icon: Icon, tone }) => (
            <Card key={label} glow className="p-5">
              <div className="flex items-start justify-between gap-3 mb-3">
                <span className="text-xs text-dim">{label}</span>
                <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-amber-soft text-amber-text">
                  <Icon size={16} aria-hidden="true" />
                </span>
              </div>
              <div dir="auto" className={`text-2xl font-display font-bold truncate ${tone} mb-0.5`}>{value}</div>
              <div className="text-xs text-ghost">{sub}</div>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Tracks + roadmap */}
          <div className="lg:col-span-2 space-y-4">
            <h2 className="ui-eyebrow">{t('dash.yourTracks')}</h2>

            {dataLoading ? (
              <Card className="p-8 flex items-center justify-center">
                <Spinner announce />
              </Card>
            ) : enrollments.length === 0 ? (
              <Card className="p-8 text-center">
                <BookOpen size={28} className="text-ghost mx-auto mb-3" />
                <p className="text-bright font-medium mb-1">{t('dash.noTracks')}</p>
                <p className="text-sm text-ghost mb-4">{t('dash.noTracksBody')}</p>
                <Link href="/tracks" className={buttonStyles({ size: 'sm' })}>
                  {t('dash.browseTracks')}
                </Link>
              </Card>
            ) : (
              enrollments.map(en => (
                <Card key={en.id} glow className="p-5">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span dir="auto" className="font-medium text-bright">{localizedTitle(en.track, language)}</span>
                      </div>
                      {en.target_job_title && <Badge variant="ghost" dir="auto">{en.target_job_title}</Badge>}
                    </div>
                    <span className="text-sm font-mono text-amber-text">{en.completion_percentage.toFixed(0)}%</span>
                  </div>
                  <ProgressBar value={en.completion_percentage} className="mb-4" />
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-ghost">{tf('dash.program', { weeks: weeks(en.track.estimated_weeks) })}</span>
                    <Link href={`/tracks/${en.track.slug}`} className={buttonStyles({ variant: 'ghost', size: 'sm' })}>
                      {t('course.continue')} <ArrowRight size={12} className="rtl:rotate-180" />
                    </Link>
                  </div>
                </Card>
              ))
            )}

            {enrollments.length > 0 && (
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h2 className="ui-eyebrow">{t('dash.weeklyPlan')}</h2>
                  <Button
                    variant="ghost"
                    size="sm"
                    loading={roadmapLoading}
                    onClick={() => void generateRoadmap()}
                  >
                    {roadmap.length > 0 ? t('dash.regenerate') : t('dash.generateRoadmap')}
                    <span className="ms-1.5 text-xs text-ghost">{tf('dash.creditsCost', { n: ROADMAP_CREDITS })}</span>
                  </Button>
                </div>

                {roadmapError && (
                  <p role="alert" dir="auto" className="mb-3 text-xs text-rose leading-relaxed">{roadmapError}</p>
                )}

                {roadmap.length === 0 && !roadmapLoading && !roadmapError && (
                  <p className="mb-3 text-xs text-ghost leading-relaxed">
                    {tf('dash.roadmapHint', { track: localizedTitle(enrollments[0].track, language), n: ROADMAP_CREDITS })}
                  </p>
                )}

                <div className="space-y-2">
                  {roadmap.slice(0, 4).map(week => (
                    <Card key={week.week} className="p-4 flex items-start gap-4">
                      <div className="shrink-0 w-8 h-8 rounded-md bg-amber/10 border border-amber/20 flex items-center justify-center">
                        <span className="text-xs font-mono text-amber-text">W{week.week}</span>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span dir="auto" className="text-sm font-medium text-bright">{week.theme}</span>
                          <Badge variant="ghost">{tf('dash.topicsCount', { n: week.topics.length })}</Badge>
                        </div>
                        <p dir="auto" className="text-xs text-ghost">{week.goal}</p>
                      </div>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Vocabulary + skill scores + mentor CTA */}
          <div className="space-y-4">
            {/* Terminology progress sits above skill scores deliberately:
                being able to name a concept in English is the difference
                between understanding it and being hireable for it. */}
            <VocabularyProgress limit={6} />

            <h2 className="ui-eyebrow">{t('dash.skillScores')}</h2>
            <Card className="p-4">
              {dataLoading ? (
                <div className="flex justify-center py-4"><Spinner announce /></div>
              ) : skills.length === 0 ? (
                <div className="text-center py-4">
                  <p className="text-xs text-ghost">{t('dash.noScores')}</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {skills.map(s => (
                    <div key={s.skill}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-soft capitalize">{s.skill}</span>
                        <span className={`text-xs font-mono ${scoreColor(s.score)}`}>{s.score.toFixed(0)}%</span>
                      </div>
                      <ProgressBar
                        value={s.score}
                        color={s.score >= 75 ? 'emerald' : s.score >= 50 ? 'amber' : 'rose'}
                      />
                    </div>
                  ))}
                </div>
              )}
            </Card>

            <Card className="p-5 bg-gradient-to-br from-amber/5 to-transparent border-amber/20">
              <div className="flex items-center gap-2 mb-2">
                <Brain size={14} className="text-amber-text" />
                <span className="text-xs font-medium text-amber-text">{t('dash.mentor')}</span>
              </div>
              <p className="text-xs text-dim mb-4 leading-relaxed">
                {t('dash.mentorBody')}
              </p>
              <Link href="/mentor" data-tour="mentor" className={buttonStyles({ variant: 'outline', size: 'sm', className: 'w-full' })}>
                <Zap size={12} /> {t('dash.openMentor')}
              </Link>
            </Card>
          </div>
        </div>
      </PageBody>
    </AppShell>
  )
}

function getGreeting() {
  const h = new Date().getHours()
  if (h < 12) return 'morning'
  if (h < 18) return 'afternoon'
  return 'evening'
}
