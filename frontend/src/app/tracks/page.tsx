'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, ProgressBar, Badge, Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import type { CareerTrackSummary, Enrollment } from '@/types'
import { cn } from '@/lib/utils'
import {
  BarChart2, Brain, Code2, Server, Layers,
  CheckCircle, Lock, ArrowRight, ChevronRight,
  Clock, BookOpen, Target, Star
} from 'lucide-react'

// ─── Track metadata (visual config, not from API) ─────────────────────
const TRACK_META: Record<string, {
  icon: React.ElementType
  color: string
  borderColor: string
  bgColor: string
  textColor: string
  topics: string[]
  outcome: string
  contributesToApex: boolean
}> = {
  'data-analyst': {
    icon: BarChart2,
    color: 'sky',
    borderColor: 'border-sky/40',
    bgColor: 'bg-sky/5',
    textColor: 'text-sky',
    topics: ['Python & SQL', 'Pandas & NumPy', 'Data visualisation', 'Statistics', 'BI dashboards'],
    outcome: 'Analyse datasets, build dashboards, derive insights',
    contributesToApex: true,
  },
  'ml-engineer': {
    icon: Brain,
    color: 'violet',
    borderColor: 'border-violet/40',
    bgColor: 'bg-violet/5',
    textColor: 'text-violet',
    topics: ['Supervised learning', 'Deep learning', 'PyTorch', 'Model evaluation', 'Feature engineering'],
    outcome: 'Train and evaluate machine learning models',
    contributesToApex: true,
  },
  'ai-developer': {
    icon: Code2,
    color: 'amber',
    borderColor: 'border-amber/40',
    bgColor: 'bg-amber/5',
    textColor: 'text-amber',
    topics: ['LLM integration', 'RAG systems', 'Vector databases', 'FastAPI', 'Prompt engineering'],
    outcome: 'Build production AI apps with LLMs and APIs',
    contributesToApex: true,
  },
  'mlops-engineer': {
    icon: Server,
    color: 'emerald',
    borderColor: 'border-emerald/40',
    bgColor: 'bg-emerald/5',
    textColor: 'text-emerald',
    topics: ['Docker & K8s', 'CI/CD pipelines', 'Model monitoring', 'Cloud deployment', 'Experiment tracking'],
    outcome: 'Deploy and maintain ML systems at scale',
    contributesToApex: true,
  },
  'ai-engineer': {
    icon: Layers,
    color: 'amber',
    borderColor: 'border-amber/40',
    bgColor: 'bg-amber/10',
    textColor: 'text-amber',
    topics: ['All tracks combined', 'System architecture', 'Production AI', 'End-to-end pipelines'],
    outcome: 'Build complete AI systems from data to production',
    contributesToApex: false,
  },
}

const APEX_SLUG = 'ai-engineer'
const APEX_REQUIRED_COUNT = 3

type TrackStatus = 'locked' | 'available' | 'enrolled' | 'completed'

interface TrackWithStatus extends CareerTrackSummary {
  status: TrackStatus
  enrollment?: Enrollment
}

// ─── Page ─────────────────────────────────────────────────────────────
export default function TracksPage() {
  const router = useRouter()
  const { isLoading: authLoading } = useAuth()
  const [tracks, setTracks] = useState<TrackWithStatus[]>([])
  const [apexTrack, setApexTrack] = useState<TrackWithStatus | null>(null)
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

        const withStatus: TrackWithStatus[] = allTracks.map(t => {
          const enr = enrMap.get(t.id)
          let status: TrackStatus = 'available'
          if (enr) status = enr.completion_percentage >= 100 ? 'completed' : 'enrolled'
          return { ...t, status, enrollment: enr }
        })

        const apex = withStatus.find(t => t.slug === APEX_SLUG)
        const rest = withStatus.filter(t => t.slug !== APEX_SLUG)

        setTracks(rest)
        setApexTrack(apex ?? null)
        // Auto-select first enrolled or first available
        const firstActive = rest.find(t => t.status === 'enrolled') ?? rest[0]
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
      setTracks(prev => prev.map(t =>
        t.id === track.id ? { ...t, status: 'enrolled', enrollment: enr } : t
      ))
      setSelected(prev => prev?.id === track.id ? { ...track, status: 'enrolled', enrollment: enr } : prev)
      router.push(`/tracks/${track.slug}`)
    } catch {}
    setEnrolling(false)
  }

  const completedCount = tracks.filter(t => t.status === 'completed').length
  const enrolledCount  = tracks.filter(t => t.status === 'enrolled').length
  const apexProgress   = Math.round((completedCount / APEX_REQUIRED_COUNT) * 100)
  const apexUnlocked   = completedCount >= APEX_REQUIRED_COUNT

  if (authLoading || loading) return (
    <div className="min-h-screen bg-void flex items-center justify-center">
      <Spinner className="w-6 h-6" />
    </div>
  )

  const meta = selected ? (TRACK_META[selected.slug] ?? TRACK_META['ai-engineer']) : null

  return (
    <AppShell>
      <PageHeader
        title="Career tracks"
        subtitle="Choose your specialisation path. Complete tracks to unlock Full Stack AI Engineer."
      />

      <div className="flex-1 overflow-y-auto px-8 py-6">
        <div className="max-w-4xl mx-auto space-y-8">

          {/* ── Flowchart section ─────────────────────────────────────── */}
          <div>
            {/* Specialisation tracks */}
            <div className="text-xs font-medium text-ghost uppercase tracking-widest text-center mb-4">
              Choose your specialisation
            </div>

            <div className="grid grid-cols-4 gap-3">
              {tracks.map(track => {
                const m = TRACK_META[track.slug] ?? {}
                const Icon = m.icon ?? BookOpen
                const isSelected = selected?.id === track.id
                const pct = track.enrollment?.completion_percentage ?? 0

                return (
                  <button
                    key={track.id}
                    onClick={() => setSelected(track)}
                    className={cn(
                      'text-left p-4 rounded-lg border transition-all duration-150',
                      isSelected
                        ? `${m.bgColor ?? 'bg-surface'} ${m.borderColor ?? 'border-border'} ring-1 ring-offset-1 ring-offset-void ${m.borderColor ?? ''}`
                        : 'bg-panel border-border hover:border-muted'
                    )}
                  >
                    <Icon
                      size={20}
                      className={cn('mb-3', m.textColor ?? 'text-ghost')}
                    />
                    <div className="text-sm font-medium text-bright mb-1 leading-tight">
                      {track.title}
                    </div>
                    <div className="text-xs text-ghost mb-3">
                      {track.estimated_weeks}w
                    </div>

                    {/* Progress bar */}
                    <div className="h-1 bg-muted rounded-full overflow-hidden mb-1.5">
                      <div
                        className={cn(
                          'h-full rounded-full transition-all duration-700',
                          track.status === 'completed' ? 'bg-emerald'
                          : track.status === 'enrolled'  ? `bg-${m.color ?? 'sky'}`
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
                        <span className={cn('text-xs', m.textColor)}>active</span>
                      )}
                      {track.status === 'available' && (
                        <span className="text-xs text-ghost">—</span>
                      )}
                    </div>
                  </button>
                )
              })}
            </div>

            {/* Connector lines */}
            <div className="flex justify-center my-2">
              <svg width="580" height="24" viewBox="0 0 580 24">
                {[72, 217, 362, 508].map((x, i) => (
                  <line
                    key={i}
                    x1={x} y1={0}
                    x2={290} y2={24}
                    stroke="currentColor"
                    strokeWidth="0.5"
                    strokeDasharray="4 3"
                    className="text-border"
                  />
                ))}
              </svg>
            </div>

            {/* Apex track */}
            {apexTrack && (
              <div className={cn(
                'mx-auto max-w-sm rounded-lg border-2 p-5 text-center transition-all',
                apexUnlocked
                  ? 'border-amber/60 bg-amber/5'
                  : 'border-border bg-panel opacity-80'
              )}>
                <div className="flex items-center justify-center gap-2 mb-1">
                  {apexUnlocked
                    ? <Star size={16} className="text-amber" />
                    : <Lock size={14} className="text-ghost" />
                  }
                  <span className={cn(
                    'text-xs font-medium uppercase tracking-widest',
                    apexUnlocked ? 'text-amber' : 'text-ghost'
                  )}>
                    {apexUnlocked ? 'Unlocked' : 'End goal'}
                  </span>
                </div>

                <h3 className="font-display font-bold text-base text-bright mb-0.5">
                  {apexTrack.title}
                </h3>
                <p className="text-xs text-ghost mb-4">
                  Complete any {APEX_REQUIRED_COUNT} tracks to unlock
                </p>

                {/* Apex progress */}
                <div className="flex items-center gap-3 mb-3">
                  <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
                    <div
                      className="h-full bg-amber rounded-full transition-all duration-700"
                      style={{ width: `${apexProgress}%` }}
                    />
                  </div>
                  <span className="text-xs font-mono text-amber shrink-0">
                    {completedCount} / {APEX_REQUIRED_COUNT}
                  </span>
                </div>

                {/* Requirement chips */}
                <div className="flex gap-2 flex-wrap justify-center mb-4">
                  {tracks.map(t => (
                    <span
                      key={t.id}
                      className={cn(
                        'text-xs px-2.5 py-1 rounded-full border',
                        t.status === 'completed'
                          ? 'bg-emerald/10 border-emerald/30 text-emerald'
                          : 'bg-surface border-border text-ghost'
                      )}
                    >
                      {t.status === 'completed' && <CheckCircle size={10} className="inline mr-1" />}
                      {t.title}
                    </span>
                  ))}
                </div>

                {apexUnlocked ? (
                  <Link href={`/tracks/${apexTrack.slug}`}>
                    <Button variant="amber" size="sm" className="w-full">
                      Start full stack path <ArrowRight size={12} />
                    </Button>
                  </Link>
                ) : (
                  <Button variant="ghost" size="sm" className="w-full" disabled>
                    Complete {APEX_REQUIRED_COUNT - completedCount} more track{APEX_REQUIRED_COUNT - completedCount !== 1 ? 's' : ''} to unlock
                  </Button>
                )}
              </div>
            )}
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
                    <h2 className="font-display font-bold text-white text-lg">{selected.title}</h2>
                    <div className="flex items-center gap-2 mt-0.5">
                      <Badge variant="ghost">
                        <Clock size={10} className="mr-1" />
                        {selected.estimated_weeks} weeks
                      </Badge>
                      {selected.status === 'enrolled' && (
                        <Badge variant="sky">Active</Badge>
                      )}
                      {selected.status === 'completed' && (
                        <Badge variant="emerald">Completed</Badge>
                      )}
                    </div>
                  </div>
                </div>

                {/* CTA */}
                <div>
                  {selected.status === 'available' && (
                    <Button
                      onClick={() => handleEnroll(selected)}
                      loading={enrolling}
                      size="sm"
                    >
                      Enroll now
                    </Button>
                  )}
                  {(selected.status === 'enrolled' || selected.status === 'completed') && (
                    <Link href={`/tracks/${selected.slug}`}>
                      <Button size="sm" variant={selected.status === 'completed' ? 'ghost' : 'amber'}>
                        {selected.status === 'completed' ? 'Review track' : 'Continue'} <ArrowRight size={12} />
                      </Button>
                    </Link>
                  )}
                </div>
              </div>

              <p className="text-sm text-soft mb-5 leading-relaxed">{meta.outcome}</p>

              {/* Progress bar for enrolled */}
              {selected.enrollment && (
                <div className="mb-5">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs text-ghost">Overall progress</span>
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
                  What you'll learn
                </div>
                <div className="grid grid-cols-2 gap-2">
                  {meta.topics.map((topic, i) => {
                    const pct = selected.enrollment?.completion_percentage ?? 0
                    const topicsDone = Math.floor(meta.topics.length * pct / 100)
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

              {/* Contributes to apex notice */}
              {meta.contributesToApex && (
                <div className="mt-4 flex items-center gap-2 text-xs text-ghost border-t border-border pt-4">
                  <Target size={12} className="text-amber shrink-0" />
                  <span>Completing this track contributes to the Full Stack AI Engineer goal</span>
                </div>
              )}
            </Card>
          )}
        </div>
      </div>
    </AppShell>
  )
}