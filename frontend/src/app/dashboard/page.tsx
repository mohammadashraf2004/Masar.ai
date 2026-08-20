'use client'
import { Suspense, useEffect, useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, ProgressBar, Badge, Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { PaymentResultBanner } from '@/components/ui/PaymentResultBanner'
import { api } from '@/lib/api'
import type { Enrollment, SkillScore, RoadmapWeek } from '@/types'
import { Brain, BookOpen, ArrowRight, Zap, Target, TrendingUp, Clock } from 'lucide-react'
import { scoreColor } from '@/lib/utils'

export default function DashboardPage() {
  const { user, isLoading: authLoading } = useAuth()
  const [enrollments, setEnrollments] = useState<Enrollment[]>([])
  const [skills, setSkills] = useState<SkillScore[]>([])
  const [roadmap, setRoadmap] = useState<RoadmapWeek[]>([])
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
        if (enr.length > 0) {
          try {
            const rm = await api.getRoadmap(enr[0].track.title)
            setRoadmap(rm.weeks)
          } catch {}
        }
      } catch {}
      setDataLoading(false)
    }
    load()
  }, [authLoading])

  if (authLoading) {
    return (
      <div className="min-h-screen bg-void flex items-center justify-center">
        <Spinner className="w-6 h-6" />
      </div>
    )
  }

  const readiness = user?.overall_readiness_score ?? 0

  return (
    <AppShell>
      <PageHeader
        title={`Good ${getGreeting()}, ${user?.full_name?.split(' ')[0] ?? 'Engineer'}`}
        subtitle="Here's your learning snapshot today."
      />

      <div className="flex-1 overflow-y-auto px-8 py-6 space-y-6">
        <Suspense fallback={null}>
          <PaymentResultBanner />
        </Suspense>

        {/* Metrics */}
        <div className="grid grid-cols-4 gap-4">
          {[
            { label: 'Readiness score', value: `${readiness.toFixed(0)}%`, sub: 'AI Engineer path', icon: Target, color: scoreColor(readiness) },
            { label: 'Tracks enrolled', value: enrollments.length, sub: dataLoading ? '…' : 'Active', icon: BookOpen, color: 'text-sky' },
            { label: 'Skills tracked', value: skills.length, sub: dataLoading ? '…' : 'Assessed', icon: TrendingUp, color: 'text-emerald' },
            { label: 'This week', value: roadmap[0]?.theme ?? '—', sub: roadmap[0] ? 'Current focus' : 'Generate roadmap', icon: Clock, color: 'text-violet' },
          ].map(({ label, value, sub, icon: Icon, color }) => (
            <Card key={label} glow className="p-5">
              <div className="flex items-start justify-between mb-3">
                <span className="text-xs text-ghost">{label}</span>
                <Icon size={14} className={color} />
              </div>
              <div className={`text-2xl font-display font-bold truncate ${color} mb-0.5`}>{value}</div>
              <div className="text-xs text-ghost">{sub}</div>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-3 gap-6">
          {/* Tracks + roadmap */}
          <div className="col-span-2 space-y-4">
            <h2 className="text-xs font-medium text-ghost uppercase tracking-widest">Your tracks</h2>

            {dataLoading ? (
              <Card className="p-8 flex items-center justify-center">
                <Spinner />
              </Card>
            ) : enrollments.length === 0 ? (
              <Card className="p-8 text-center">
                <BookOpen size={28} className="text-ghost mx-auto mb-3" />
                <p className="text-bright font-medium mb-1">No tracks yet</p>
                <p className="text-sm text-ghost mb-4">Start the AI Engineer path to begin.</p>
                <Link href="/tracks">
                  <Button size="sm">Browse tracks</Button>
                </Link>
              </Card>
            ) : (
              enrollments.map(en => (
                <Card key={en.id} glow className="p-5">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-lg">{en.track.icon}</span>
                        <span className="font-medium text-bright">{en.track.title}</span>
                      </div>
                      {en.target_job_title && <Badge variant="ghost">{en.target_job_title}</Badge>}
                    </div>
                    <span className="text-sm font-mono text-amber">{en.completion_percentage.toFixed(0)}%</span>
                  </div>
                  <ProgressBar value={en.completion_percentage} className="mb-4" />
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-ghost">{en.track.estimated_weeks}w program</span>
                    <Link href={`/tracks/${en.track.slug}`}>
                      <Button variant="ghost" size="sm">Continue <ArrowRight size={12} /></Button>
                    </Link>
                  </div>
                </Card>
              ))
            )}

            {roadmap.length > 0 && (
              <div>
                <h2 className="text-xs font-medium text-ghost uppercase tracking-widest mb-3">Weekly plan</h2>
                <div className="space-y-2">
                  {roadmap.slice(0, 4).map(week => (
                    <Card key={week.week} className="p-4 flex items-start gap-4">
                      <div className="shrink-0 w-8 h-8 rounded-md bg-amber/10 border border-amber/20 flex items-center justify-center">
                        <span className="text-xs font-mono text-amber">W{week.week}</span>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-medium text-bright">{week.theme}</span>
                          <Badge variant="ghost">{week.topics.length} topics</Badge>
                        </div>
                        <p className="text-xs text-ghost">{week.goal}</p>
                      </div>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Skill scores + mentor CTA */}
          <div className="space-y-4">
            <h2 className="text-xs font-medium text-ghost uppercase tracking-widest">Skill scores</h2>
            <Card className="p-4">
              {dataLoading ? (
                <div className="flex justify-center py-4"><Spinner /></div>
              ) : skills.length === 0 ? (
                <div className="text-center py-4">
                  <p className="text-xs text-ghost mb-3">No scores yet</p>
                  <Link href="/mentor">
                    <Button variant="ghost" size="sm">Run skill gap analysis</Button>
                  </Link>
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
                <Brain size={14} className="text-amber" />
                <span className="text-xs font-medium text-amber">AI Mentor</span>
              </div>
              <p className="text-xs text-dim mb-4 leading-relaxed">
                Ready to explain concepts, quiz you, or review your code.
              </p>
              <Link href="/mentor">
                <Button variant="outline" size="sm" className="w-full">
                  <Zap size={12} /> Open mentor
                </Button>
              </Link>
            </Card>
          </div>
        </div>
      </div>
    </AppShell>
  )
}

function getGreeting() {
  const h = new Date().getHours()
  if (h < 12) return 'morning'
  if (h < 18) return 'afternoon'
  return 'evening'
}
