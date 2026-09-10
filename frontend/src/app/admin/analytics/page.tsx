'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Badge, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import type { AdminAnalyticsOverview, TopicCount } from '@/types'
import { Users, Zap, BookOpen, TrendingUp, Info } from 'lucide-react'

/**
 * Admin analytics — read-only, aggregates only.
 *
 * The role check below is a courtesy, not a control: it stops a student
 * from staring at a spinner that will only ever resolve to a 403. The
 * actual authorization lives in require_admin on the server, which this
 * page cannot influence.
 */

function Stat({ label, value, hint }: { label: string; value: string | number; hint?: string }) {
  return (
    <Card className="p-4">
      <div className="text-xs text-dim uppercase tracking-wide">{label}</div>
      <div className="mt-1 font-mono text-2xl text-bright">{value}</div>
      {hint && <div className="mt-1 text-xs text-ghost">{hint}</div>}
    </Card>
  )
}

function SectionTitle({ icon: Icon, children }: { icon: React.ElementType; children: React.ReactNode }) {
  return (
    <h2 className="flex items-center gap-2 text-sm font-semibold text-soft uppercase tracking-wide">
      <Icon size={14} className="text-amber" />
      {children}
    </h2>
  )
}

/** Funnel rows carry the count and its share of the stage above signup,
 *  which is the only comparison that means anything here. */
function FunnelRow({ label, value, total, note }: {
  label: string; value: number; total: number; note?: string
}) {
  const pct = total > 0 ? (value / total) * 100 : 0
  return (
    <div className="py-2 border-b border-border last:border-0">
      <div className="flex items-baseline justify-between gap-3">
        <span className="text-sm text-soft">
          {label}
          {note && <span className="ms-2 text-xs text-ghost">{note}</span>}
        </span>
        <span className="font-mono text-sm text-bright">
          {value}
          <span className="ms-2 text-xs text-dim">{pct.toFixed(0)}%</span>
        </span>
      </div>
      <div className="progress-track h-1 mt-1.5">
        <div className="progress-fill bg-gradient-to-r from-amber to-amber2"
             style={{ width: `${Math.min(100, Math.max(0, pct))}%` }} />
      </div>
    </div>
  )
}

function TopicTable({ title, rows }: { title: string; rows: TopicCount[] }) {
  return (
    <Card className="p-4">
      <div className="text-xs text-dim uppercase tracking-wide mb-2">{title}</div>
      {rows.length === 0 ? (
        <div className="text-sm text-ghost py-2">No data yet.</div>
      ) : (
        <div className="overflow-x-auto"><table className="w-full text-sm min-w-[20rem]">
          <tbody>
            {rows.map((row) => (
              <tr key={row.topic} className="border-b border-border last:border-0">
                <td className="py-1.5 pe-3 text-soft truncate">{row.topic}</td>
                <td className="py-1.5 text-right font-mono text-bright w-16">{row.count}</td>
              </tr>
            ))}
          </tbody>
        </table></div>
      )}
    </Card>
  )
}

export default function AdminAnalyticsPage() {
  const router = useRouter()
  const { user, isLoading: authLoading } = useAuth()
  const [data, setData] = useState<AdminAnalyticsOverview | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const isAdmin = user?.role === 'admin'

  useEffect(() => {
    if (authLoading) return
    if (user && !isAdmin) {
      router.replace('/dashboard')
      return
    }
    if (!isAdmin) return
    api.getAnalyticsOverview()
      .then(setData)
      .catch(() => setError('Could not load analytics.'))
      .finally(() => setLoading(false))
  }, [authLoading, user, isAdmin, router])

  if (authLoading || (isAdmin && loading)) {
    return (
      <AppShell>
        <PageHeader title="Analytics" />
        <div className="p-6"><Spinner /></div>
      </AppShell>
    )
  }

  if (!isAdmin) {
    return (
      <AppShell>
        <PageHeader title="Analytics" />
        <div className="p-6 text-sm text-dim">Admins only.</div>
      </AppShell>
    )
  }

  if (error || !data) {
    return (
      <AppShell>
        <PageHeader title="Analytics" />
        <div className="p-6 text-sm text-rose">{error || 'No data.'}</div>
      </AppShell>
    )
  }

  const { users, activation, learning, ai_usage, retention } = data
  const features = Object.entries(ai_usage.credits_by_feature)
    .sort((a, b) => b[1] - a[1])

  return (
    <AppShell>
      <PageHeader
        title="Analytics"
        subtitle={`Product metrics · generated ${new Date(data.generated_at).toLocaleString()}`}
      />

      {/* AppShell pins its panes only from lg up, so the page
          owns its own scroll container — without `flex-1 overflow-y-auto`
          everything below the fold is simply clipped. Same structure the
          dashboard and community pages use. */}
      <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="max-w-5xl space-y-8">
          {/* ── Users ─────────────────────────────────────────────────── */}
          <section className="space-y-3">
            <SectionTitle icon={Users}>Users</SectionTitle>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <Stat label="Total" value={users.total} />
              <Stat label="New today" value={users.new_today} hint="since 00:00 UTC" />
              <Stat label="New · 7 days" value={users.new_last_7_days} hint="rolling" />
              <Stat label="New · 30 days" value={users.new_last_30_days} hint="rolling" />
            </div>
            <Card className="p-4 flex items-start gap-3">
              <div className="flex-1">
                <div className="text-xs text-dim uppercase tracking-wide">Verified</div>
                <div className="mt-1 font-mono text-2xl text-bright">{users.verified}</div>
              </div>
              {!users.verification_reliable && (
                <div className="flex-1 flex items-start gap-2 text-xs text-dim">
                  <Info size={14} className="text-amber flex-shrink-0 mt-0.5" />
                  <span>
                    <Badge variant="amber" className="me-2">unreliable</Badge>
                    {users.verification_note}
                  </span>
                </div>
              )}
            </Card>
          </section>

          {/* ── Activation ────────────────────────────────────────────── */}
          <section className="space-y-3">
            <SectionTitle icon={TrendingUp}>Activation funnel</SectionTitle>
            <Card className="p-4">
              <FunnelRow label="Signed up" value={activation.signed_up} total={activation.signed_up} />
              <FunnelRow
                label="Verified email"
                value={activation.verified}
                total={activation.signed_up}
                note={activation.verification_reliable ? undefined : '(delivery not configured)'}
              />
              <FunnelRow label="Started learning" value={activation.started_learning} total={activation.signed_up} />
              <FunnelRow label="Completed first lesson" value={activation.completed_first_lesson} total={activation.signed_up} />
              <p className="mt-3 text-xs text-ghost leading-relaxed">
                Started learning = has at least one topic-progress record.
                Completed first lesson = at least one lesson marked complete on any topic.
              </p>
            </Card>
          </section>

          {/* ── Learning ──────────────────────────────────────────────── */}
          <section className="space-y-3">
            <SectionTitle icon={BookOpen}>Learning activity</SectionTitle>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <Stat label="Lessons completed" value={learning.lessons_completed} />
              <Stat label="Exercises completed" value={learning.exercises_completed} />
            </div>
            <div className="grid md:grid-cols-2 gap-3">
              <TopicTable title="Most started topics" rows={learning.most_started_topics} />
              <TopicTable title="Most completed topics" rows={learning.most_completed_topics} />
            </div>
          </section>

          {/* ── AI usage ──────────────────────────────────────────────── */}
          <section className="space-y-3">
            <SectionTitle icon={Zap}>AI credits</SectionTitle>
            <div className="grid md:grid-cols-3 gap-3">
              <Stat label="Credits burned" value={ai_usage.total_credits_burned} hint="all time" />
              <Card className="p-4 md:col-span-2">
                <div className="text-xs text-dim uppercase tracking-wide mb-2">By feature</div>
                {features.length === 0 ? (
                  <div className="text-sm text-ghost py-2">No AI spend recorded yet.</div>
                ) : (
                  <div className="overflow-x-auto"><table className="w-full text-sm min-w-[20rem]">
                    <tbody>
                      {features.map(([feature, credits]) => (
                        <tr key={feature} className="border-b border-border last:border-0">
                          <td className="py-1.5 pe-3 text-soft">{feature.replace(/_/g, ' ')}</td>
                          <td className="py-1.5 text-right font-mono text-bright w-20">{credits}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table></div>
                )}
              </Card>
            </div>
          </section>

          {/* ── Retention ─────────────────────────────────────────────── */}
          <section className="space-y-3">
            <SectionTitle icon={TrendingUp}>Retention</SectionTitle>
            <Card className="p-4">
              {retention.available ? (
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <Stat label="D1" value={`${retention.d1?.toFixed(1)}%`} />
                  <Stat label="D7" value={`${retention.d7?.toFixed(1)}%`} />
                  <Stat label="D30" value={`${retention.d30?.toFixed(1)}%`} />
                </div>
              ) : (
                // Deliberately shows nothing rather than a number the data
                // cannot support — see the backend controller for why.
                <div className="flex items-start gap-2">
                  <Info size={14} className="text-amber flex-shrink-0 mt-0.5" />
                  <div className="text-sm text-dim">
                    <Badge variant="ghost" className="me-2">unavailable</Badge>
                    {retention.reason}
                  </div>
                </div>
              )}
            </Card>
          </section>
        </div>
      </div>
    </AppShell>
  )
}
