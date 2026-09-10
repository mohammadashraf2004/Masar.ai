'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Badge, Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import type { AdminAnalyticsOverview, TopicCount, AdminUserLookup, AdminGrantResult } from '@/types'
import { getErrorMessage } from '@/lib/utils'
import { Users, Zap, BookOpen, TrendingUp, Info, Gift, Search, AlertTriangle, CheckCircle } from 'lucide-react'

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

/**
 * Grant credits to an account, by email.
 *
 * Deliberately one screen and one confirmation: the operator types the
 * address they already have from a support thread, sees whose account it is
 * and what they currently hold, then commits. Looking the user up first is
 * what makes the amount safe to type — a grant cannot be undone from here,
 * and the wrong recipient is the expensive mistake, not the wrong number.
 *
 * Authorization is `require_admin` on both endpoints. Nothing here is a
 * control; the page-level role check only avoids showing a form that would
 * only ever 403.
 */
function GrantCredits() {
  const [email, setEmail] = useState('')
  const [credits, setCredits] = useState('')
  const [reason, setReason] = useState('')

  const [found, setFound] = useState<AdminUserLookup | null>(null)
  const [looking, setLooking] = useState(false)
  const [granting, setGranting] = useState(false)
  const [result, setResult] = useState<AdminGrantResult | null>(null)
  const [error, setError] = useState('')

  // Any edit to the address invalidates the account shown beside it.
  function onEmailChange(next: string) {
    setEmail(next)
    setFound(null)
    setResult(null)
    setError('')
  }

  async function lookup() {
    const target = email.trim()
    if (!target || looking) return
    setLooking(true)
    setError('')
    setResult(null)
    try {
      setFound(await api.adminLookupUser(target))
    } catch (err) {
      setFound(null)
      setError(getErrorMessage(err))
    } finally {
      setLooking(false)
    }
  }

  async function grant() {
    const amount = Number(credits)
    if (!found || granting) return
    if (!Number.isInteger(amount) || amount <= 0) {
      setError('Enter a whole number of credits above zero.')
      return
    }
    setGranting(true)
    setError('')
    try {
      const res = await api.adminGrantCredits(
        found.email,
        amount,
        reason.trim() || 'Admin grant',
      )
      setResult(res)
      // Reset the amount but keep the account on screen, so granting twice
      // by accident takes a deliberate retype.
      setCredits('')
      setReason('')
      setFound({ ...found, credit_balance: res.new_balance })
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setGranting(false)
    }
  }

  return (
    <section className="space-y-3">
      <SectionTitle icon={Gift}>Grant credits</SectionTitle>

      <Card className="p-4 sm:p-5 space-y-4">
        {/* Step 1 — who */}
        <div className="flex flex-col sm:flex-row gap-2 sm:items-end">
          <div className="flex-1 min-w-0">
            <label htmlFor="grant-email" className="text-xs font-medium text-soft tracking-wide uppercase block mb-1.5">
              Account email
            </label>
            <input
              id="grant-email"
              type="email"
              autoComplete="off"
              className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50"
              placeholder="student@example.com"
              value={email}
              onChange={e => onEmailChange(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); void lookup() } }}
            />
          </div>
          <Button
            type="button"
            variant="ghost"
            onClick={() => void lookup()}
            loading={looking}
            disabled={!email.trim()}
            className="sm:w-auto w-full"
          >
            <Search size={13} /> Find
          </Button>
        </div>

        {/* Step 2 — confirm the account, then the amount */}
        {found && (
          <div className="space-y-4 border-t border-border pt-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="min-w-0">
                <p className="text-sm text-bright truncate">{found.full_name}</p>
                <p className="text-xs text-ghost truncate">{found.email} · id {found.user_id}</p>
              </div>
              <div className="text-end shrink-0">
                <p className="font-mono text-lg text-amber">{found.credit_balance}</p>
                <p className="text-xs text-ghost">current balance</p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <label htmlFor="grant-credits" className="text-xs font-medium text-soft tracking-wide uppercase block mb-1.5">
                  Credits
                </label>
                <input
                  id="grant-credits"
                  type="number"
                  min={1}
                  max={100000}
                  inputMode="numeric"
                  className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm font-mono text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50"
                  placeholder="500"
                  value={credits}
                  onChange={e => { setCredits(e.target.value); setError(''); setResult(null) }}
                />
              </div>
              <div className="sm:col-span-2">
                <label htmlFor="grant-reason" className="text-xs font-medium text-soft tracking-wide uppercase block mb-1.5">
                  Reason <span className="text-ghost normal-case">— shown on their statement</span>
                </label>
                <input
                  id="grant-reason"
                  className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50"
                  placeholder="Admin grant"
                  maxLength={200}
                  value={reason}
                  onChange={e => setReason(e.target.value)}
                />
              </div>
            </div>

            {/* Quick amounts — the three that come up most in support. */}
            <div className="flex flex-wrap gap-2">
              {[100, 250, 500, 1000].map(n => (
                <button
                  key={n}
                  type="button"
                  onClick={() => { setCredits(String(n)); setError(''); setResult(null) }}
                  className="px-3 py-1.5 rounded-full text-xs font-mono border border-border text-dim hover:text-bright hover:border-amber/30 transition-colors min-h-[36px]"
                >
                  +{n}
                </button>
              ))}
            </div>

            <Button
              type="button"
              onClick={() => void grant()}
              loading={granting}
              disabled={!credits.trim()}
              className="w-full sm:w-auto"
            >
              <Gift size={13} />
              Grant {credits.trim() ? `${credits} credits` : 'credits'} to {found.full_name.split(' ')[0]}
            </Button>
          </div>
        )}

        {error && (
          <div className="flex items-start gap-2 px-3 py-2.5 rounded-lg bg-rose/10 border border-rose/20 text-xs text-rose">
            <AlertTriangle size={13} className="shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {result && (
          <div className="flex items-start gap-2 px-3 py-2.5 rounded-lg bg-emerald/10 border border-emerald/20 text-xs text-emerald">
            <CheckCircle size={13} className="shrink-0 mt-0.5" />
            <span>
              Granted {result.credits_granted} credits to {result.full_name} ({result.email}).
              New balance {result.new_balance}.
            </span>
          </div>
        )}

        <p className="text-xs text-ghost leading-relaxed">
          Recorded as a bonus transaction on the account&apos;s statement and written to
          the admin audit log. Grants cannot be reversed from this screen.
        </p>
      </Card>
    </section>
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
          {/* Operations first: this is the one thing on the page you come
              here to *do*, rather than read. */}
          <GrantCredits />

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
