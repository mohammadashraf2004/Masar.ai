'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { Card, ProgressBar, Badge, Spinner } from '@/components/ui/index'
import { Button, buttonStyles } from '@/components/ui/Button'
import { api } from '@/lib/api'
import type { CareerTrackSummary, Enrollment } from '@/types'
import { cn } from '@/lib/utils'
import { isTrackComingSoon } from '@/lib/tracks'
import { useI18n, STRINGS, type StringKey } from '@/lib/i18n'
import { localizedTitle } from '@/lib/content-language'
import {
  BarChart2, Brain, Code2, Server, Layers,
  CheckCircle, ArrowRight, ChevronRight,
  Clock, BookOpen
} from 'lucide-react'

// ─── Track metadata (visual config, not from API) ─────────────────────
const TRACK_META: Record<string, {
  icon: React.ElementType
  // The progress-bar fill, as a whole class name: Tailwind only emits classes it
  // can read in the source, so it cannot be assembled as `bg-${colour}`.
  fill: string
  borderColor: string
  bgColor: string
  textColor: string
}> = {
  'data-analyst': {
    icon: BarChart2,
    fill: 'bg-sky',
    borderColor: 'border-sky/40',
    bgColor: 'bg-sky/5',
    textColor: 'text-sky',
  },
  'ml-engineer': {
    icon: Brain,
    fill: 'bg-violet',
    borderColor: 'border-violet/40',
    bgColor: 'bg-violet/5',
    textColor: 'text-violet',
  },
  'ai-developer': {
    icon: Code2,
    fill: 'bg-amber',
    borderColor: 'border-amber/40',
    bgColor: 'bg-amber/5',
    textColor: 'text-amber-text',
  },
  'mlops-engineer': {
    icon: Server,
    fill: 'bg-emerald',
    borderColor: 'border-emerald/40',
    bgColor: 'bg-emerald/5',
    textColor: 'text-emerald',
  },
  'ai-engineer': {
    icon: Layers,
    fill: 'bg-amber',
    borderColor: 'border-amber/40',
    bgColor: 'bg-amber/10',
    textColor: 'text-amber-text',
  },
}

type TrackStatus = 'locked' | 'available' | 'enrolled' | 'completed' | 'coming_soon'

interface TrackWithStatus extends CareerTrackSummary {
  status: TrackStatus
  enrollment?: Enrollment
}

// ─── Page ─────────────────────────────────────────────────────────────
export default function TracksPage() {
  const router = useRouter()
  const { isLoading: authLoading } = useAuth()
  const { t, language, weeks } = useI18n()
  const [tracks, setTracks] = useState<TrackWithStatus[]>([])
  const [enrollments, setEnrollments] = useState<Enrollment[]>([])
  const [selected, setSelected] = useState<TrackWithStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [enrolling, setEnrolling] = useState(false)

  useEffect(() => {
    if (authLoading) return
    async function load() {
      try {
        const [allTracks, enrs] = await Promise.all([
          api.listTracks(),
          api.getMyEnrollments(),
        ])
        setEnrollments(enrs)
        const enrMap = new Map(enrs.map(e => [e.track_id, e]))

        const withStatus: TrackWithStatus[] = allTracks.map(track => {
          const enr = enrMap.get(track.id)
          let status: TrackStatus = 'available'
          // An existing enrolment wins: someone already in a track keeps their
          // way back into it, the same rule the tool courses use.
          if (enr) status = enr.completion_percentage >= 100 ? 'completed' : 'enrolled'
          else if (isTrackComingSoon(track.slug)) status = 'coming_soon'
          return { ...track, status, enrollment: enr }
        })

        // Every career track is shown alike. AI Engineer used to be a locked
        // "apex" unlocked by finishing three others; it is now a career goal
        // with its own routes (see /paths), so it is no longer set apart here.
        const rest = withStatus

        setTracks(rest)
        // Auto-select first enrolled, else the first track anyone can start —
        // opening on a coming-soon track shows a panel whose only action is
        // disabled.
        const firstActive = rest.find(track => track.status === 'enrolled')
          ?? rest.find(track => track.status !== 'coming_soon')
          ?? rest[0]
        if (firstActive) setSelected(firstActive)
      } catch {}
      setLoading(false)
    }
    load()
  }, [authLoading])

  async function handleEnroll(track: TrackWithStatus) {
    if (enrolling) return
    setEnrolling(true)
    try {
      const enr = await api.enroll(track.id)
      setTracks(prev => prev.map(tr =>
        tr.id === track.id ? { ...tr, status: 'enrolled', enrollment: enr } : tr
      ))
      setSelected(prev => prev?.id === track.id ? { ...track, status: 'enrolled', enrollment: enr } : prev)
      router.push(`/tracks/${track.slug}`)
    } catch {}
    setEnrolling(false)
  }

  if (authLoading || loading) return (
    <div className="min-h-dvh bg-void flex items-center justify-center">
      <Spinner announce className="w-6 h-6" />
    </div>
  )

  const metaSlug = selected ? (selected.slug in TRACK_META ? selected.slug : 'ai-engineer') : null
  const meta = metaSlug ? TRACK_META[metaSlug] : null
  // The copy for a track is in the i18n table, keyed by slug: an outcome line and up to five topics.
  const outcomeKey = `tracks.meta.${metaSlug}.outcome` as StringKey
  const topics = metaSlug
    ? [1, 2, 3, 4, 5]
        .map(i => `tracks.meta.${metaSlug}.topic${i}` as StringKey)
        .filter(key => key in STRINGS.en)
        .map(key => t(key))
    : []

  return (
    <AppShell>
      <PageHeader title={t('tracks.title')} subtitle={t('tracks.subtitle')} contained />

      <PageBody>
        <div className="space-y-8">

          {/* ── Flowchart section ─────────────────────────────────────── */}
          <div>
            {/* Where the personalised path lives. Tracks are the curriculum
                libraries behind it; the path itself is built from level, field
                and career goal. */}
            <Card className="mb-6 flex flex-wrap items-center justify-between gap-3 border-amber/20 p-4">
              <p className="max-w-xl text-sm text-soft">{t('tracks.intro')}</p>
              <Link href="/learn/masar" className={buttonStyles({ size: 'sm' })}>
                {t('tracks.openMasar')} <ArrowRight size={12} className="rtl:rotate-180" />
              </Link>
            </Card>

            <div className="text-xs font-medium text-ghost uppercase tracking-widest text-center mb-4">
              {t('tracks.libraries')}
            </div>

            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
              {tracks.map(track => {
                const m = TRACK_META[track.slug] ?? {}
                const Icon = m.icon ?? BookOpen
                const isSelected = selected?.id === track.id
                const pct = track.enrollment?.completion_percentage ?? 0
                const comingSoon = track.status === 'coming_soon'

                return (
                  <button
                    key={track.id}
                    onClick={() => setSelected(track)}
                    className={cn(
                      'text-start p-4 rounded-lg border transition-all duration-150',
                      isSelected
                        ? `${m.bgColor ?? 'bg-surface'} ${m.borderColor ?? 'border-border'} ring-1 ring-offset-1 ring-offset-void ${m.borderColor ?? ''}`
                        : 'bg-panel border-border hover:border-muted',
                      comingSoon && 'border-dashed'
                    )}
                  >
                    <Icon
                      size={20}
                      className={cn('mb-3', comingSoon ? 'text-ghost' : (m.textColor ?? 'text-ghost'))}
                    />
                    <div dir="auto" className="text-sm font-medium text-bright mb-1 leading-tight">
                      {localizedTitle(track, language)}
                    </div>
                    <div className="text-xs text-ghost mb-3">
                      {weeks(track.estimated_weeks)}
                    </div>

                    {/* An unpublished track has nothing to be a percentage of,
                        so the label stands in for the progress row. */}
                    {comingSoon ? (
                      <div className="flex items-center gap-1.5 text-xs text-ghost">
                        <Clock size={11} className="shrink-0" />
                        {t('course.comingSoon')}
                      </div>
                    ) : (
                      <>
                        {/* Progress bar */}
                        <div className="h-1 bg-muted rounded-full overflow-hidden mb-1.5">
                          <div
                            className={cn(
                              'h-full rounded-full transition-all duration-700',
                              track.status === 'completed' ? 'bg-emerald'
                              : track.status === 'enrolled'  ? (m.fill ?? 'bg-sky')
                              : 'bg-muted'
                            )}
                            style={{ width: `${pct}%` }}
                          />
                        </div>

                        <div className="flex items-center justify-between">
                          <span className="text-xs text-ghost">
                            {pct > 0 ? `${Math.round(pct)}%` : '0%'}
                          </span>
                          {track.status === 'completed' && (
                            <CheckCircle size={12} className="text-emerald" />
                          )}
                          {track.status === 'enrolled' && (
                            <span className={cn('text-xs', m.textColor)}>{t('tracks.active')}</span>
                          )}
                          {track.status === 'available' && (
                            <span className="text-xs text-ghost">—</span>
                          )}
                        </div>
                      </>
                    )}
                  </button>
                )
              })}
            </div>

          </div>

          {/* ── Selected track detail panel ───────────────────────────── */}
          {selected && meta && (
            <Card className={cn('p-6 border', meta.borderColor)}>
              <div className="flex items-start justify-between mb-5">
                <div className="flex items-center gap-3">
                  <div className={cn('w-10 h-10 rounded-lg flex items-center justify-center', meta.bgColor)}>
                    <meta.icon size={20} className={meta.textColor} />
                  </div>
                  <div>
                    <h2 dir="auto" className="font-display font-bold text-white text-lg">{localizedTitle(selected, language)}</h2>
                    <div className="flex items-center gap-2 mt-0.5">
                      <Badge variant="ghost">
                        <Clock size={10} className="me-1" />
                        {weeks(selected.estimated_weeks)}
                      </Badge>
                      {selected.status === 'enrolled' && (
                        <Badge variant="sky">{t('tracks.statusActive')}</Badge>
                      )}
                      {selected.status === 'completed' && (
                        <Badge variant="emerald">{t('tracks.statusCompleted')}</Badge>
                      )}
                      {selected.status === 'coming_soon' && (
                        <Badge variant="ghost">
                          <Clock size={10} className="me-1" />
                          {t('course.comingSoon')}
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>

                {/* CTA */}
                <div>
                  {selected.status === 'coming_soon' && (
                    <Button size="sm" variant="ghost" disabled>
                      {t('course.comingSoon')}
                    </Button>
                  )}
                  {selected.status === 'available' && (
                    <Button
                      onClick={() => handleEnroll(selected)}
                      loading={enrolling}
                      size="sm"
                    >
                      {t('tracks.enroll')}
                    </Button>
                  )}
                  {(selected.status === 'enrolled' || selected.status === 'completed') && (
                    <Link
                      href={`/tracks/${selected.slug}`}
                      className={buttonStyles({ size: 'sm', variant: selected.status === 'completed' ? 'ghost' : 'amber' })}
                    >
                      {selected.status === 'completed' ? t('tracks.reviewTrack') : t('course.continue')} <ArrowRight size={12} className="rtl:rotate-180" />
                    </Link>
                  )}
                </div>
              </div>

              <p className="text-sm text-soft mb-5 leading-relaxed">{t(outcomeKey)}</p>

              {/* Progress bar for enrolled */}
              {selected.enrollment && (
                <div className="mb-5">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs text-ghost">{t('tracks.overallProgress')}</span>
                    <span className={cn('text-xs font-mono', meta.textColor)}>
                      {Math.round(selected.enrollment.completion_percentage)}%
                    </span>
                  </div>
                  <ProgressBar
                    value={selected.enrollment.completion_percentage}
                    size="md"
                    color={
                      selected.status === 'completed' ? 'emerald'
                      : selected.slug === 'ai-developer' || selected.slug === 'mlops-engineer' ? 'emerald'
                      : 'amber'
                    }
                  />
                </div>
              )}

              {/* Topics grid */}
              <div>
                <div className="text-xs font-medium text-ghost uppercase tracking-widest mb-3">
                  {t('tracks.learnHeading')}
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {topics.map((topic, i) => {
                    const pct = selected.enrollment?.completion_percentage ?? 0
                    const topicsDone = Math.floor(topics.length * pct / 100)
                    const done = i < topicsDone
                    return (
                      <div
                        key={topic}
                        className={cn(
                          'flex items-center gap-2.5 px-3 py-2 rounded text-sm',
                          done
                            ? 'bg-emerald/5 border border-emerald/20'
                            : 'bg-surface border border-border'
                        )}
                      >
                        {done
                          ? <CheckCircle size={13} className="text-emerald shrink-0" />
                          : <ChevronRight size={13} className="text-ghost shrink-0" />
                        }
                        <span className={done ? 'text-soft' : 'text-dim'}>{topic}</span>
                      </div>
                    )
                  })}
                </div>
              </div>

            </Card>
          )}
        </div>
      </PageBody>
    </AppShell>
  )
}