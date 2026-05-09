'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card } from '@/components/ui/index'
import { Badge } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import { CareerTrackSummary, Enrollment } from '@/types'
import { ArrowRight, Clock, CheckCircle } from 'lucide-react'

export default function TracksPage() {
  useAuth()
  const [tracks, setTracks] = useState<CareerTrackSummary[]>([])
  const [enrollments, setEnrollments] = useState<Enrollment[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([api.listTracks(), api.getMyEnrollments()])
      .then(([t, e]) => { setTracks(t); setEnrollments(e) })
      .finally(() => setLoading(false))
  }, [])

  const enrolledIds = new Set(enrollments.map(e => e.track_id))

  return (
    <AppShell>
      <PageHeader
        title="Career tracks"
        subtitle="Choose a path and get a personalized roadmap to job-readiness."
      />

      <div className="flex-1 overflow-y-auto px-8 py-6">
        {loading ? (
          <div className="grid grid-cols-2 gap-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-48 rounded-lg bg-panel border border-border animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4">
            {tracks.map(track => {
              const enrolled = enrolledIds.has(track.id)
              return (
                <Card key={track.id} glow className="p-6 flex flex-col">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="text-3xl mb-2">{track.icon}</div>
                      <h3 className="font-display font-700 text-white text-lg">{track.title}</h3>
                    </div>
                    {enrolled && (
                      <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald/10 border border-emerald/20">
                        <CheckCircle size={11} className="text-emerald" />
                        <span className="text-xs text-emerald">Enrolled</span>
                      </div>
                    )}
                  </div>

                  <p className="text-sm text-ghost leading-relaxed flex-1 mb-5">
                    {track.description}
                  </p>

                  <div className="flex items-center gap-3 mb-4">
                    <Badge variant="ghost">
                      <Clock size={10} className="mr-1" />
                      {track.estimated_weeks} weeks
                    </Badge>
                  </div>

                  <Link href={`/tracks/${track.slug}`}>
                    <Button
                      variant={enrolled ? 'ghost' : 'amber'}
                      size="sm"
                      className="w-full"
                    >
                      {enrolled ? 'Continue learning' : 'View track'}
                      <ArrowRight size={12} />
                    </Button>
                  </Link>
                </Card>
              )
            })}
          </div>
        )}
      </div>
    </AppShell>
  )
}
