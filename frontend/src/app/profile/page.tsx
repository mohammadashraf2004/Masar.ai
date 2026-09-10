'use client'
import { useState, useEffect } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { useAuthStore } from '@/lib/store'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Badge, ProgressBar, Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { api } from '@/lib/api'
import { getErrorMessage, scoreColor } from '@/lib/utils'
import {
  User, Save, CheckCircle, ShieldCheck, Trophy,
  Zap, Clock, DollarSign, AlertTriangle, Target,
  Code2, BookOpen, Brain, RefreshCw, Star,
  TrendingUp, Award, Activity, Lock, Mail, LogOut, Trash2
} from 'lucide-react'

// ─── Types ────────────────────────────────────────────────────────────────────
interface Scorecard {
  certs_earned: number
  exams_attempted: number
  exam_pass_rate: number | null
  avg_latency_ms: number | null
  p95_latency_ms: number | null
  cost_per_1k_requests: number | null
  total_tokens_used: number
  hallucination_rate: number | null
  retrieval_precision: number | null
  code_quality_score: number | null
  avg_project_score: number | null
  projects_submitted: number
  quizzes_passed: number
  mentor_sessions_count: number
  total_study_minutes: number
  overall_grade: string | null
  hire_ready: boolean
  last_computed_at: string | null
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function fmt(val: number | null | undefined, decimals = 1, suffix = ''): string {
  if (val === null || val === undefined) return '—'
  return `${val.toFixed(decimals)}${suffix}`
}

function fmtMs(ms: number | null | undefined): string {
  if (ms === null || ms === undefined) return '—'
  return ms >= 1000 ? `${(ms / 1000).toFixed(2)}s` : `${Math.round(ms)}ms`
}

function fmtMinutes(mins: number): string {
  if (mins < 60) return `${mins}m`
  const h = Math.floor(mins / 60)
  const m = mins % 60
  return m ? `${h}h ${m}m` : `${h}h`
}

function gradeColor(grade: string | null): string {
  if (!grade) return 'text-ghost'
  if (grade === 'A+' || grade === 'A') return 'text-emerald'
  if (grade === 'B+' || grade === 'B') return 'text-amber'
  if (grade === 'C') return 'text-sky'
  return 'text-rose'
}

function latencyColor(ms: number | null): string {
  if (!ms) return 'text-ghost'
  if (ms < 800) return 'text-emerald'
  if (ms < 2000) return 'text-amber'
  return 'text-rose'
}

function hallucinationColor(rate: number | null): string {
  if (rate === null || rate === undefined) return 'text-ghost'
  if (rate < 0.05) return 'text-emerald'
  if (rate < 0.15) return 'text-amber'
  return 'text-rose'
}

// ─── Metric card ──────────────────────────────────────────────────────────────
function MetricCard({
  icon: Icon, label, value, sub, valueClass = 'text-bright', locked = false
}: {
  icon: any; label: string; value: string; sub?: string
  valueClass?: string; locked?: boolean
}) {
  return (
    <Card className="p-4 relative">
      {locked && (
        <div className="absolute inset-0 bg-void/60 backdrop-blur-[1px] rounded-lg flex flex-col items-center justify-center gap-1 z-10">
          <Lock size={14} className="text-ghost" />
          <span className="text-xs text-ghost">No data yet</span>
        </div>
      )}
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-ghost">{label}</span>
        <Icon size={13} className="text-ghost" />
      </div>
      <div className={`text-xl font-mono font-bold mb-0.5 ${valueClass}`}>{value}</div>
      {sub && <div className="text-xs text-ghost">{sub}</div>}
    </Card>
  )
}

// ─── Section header ───────────────────────────────────────────────────────────
function SectionHeader({ icon: Icon, label, color = 'text-amber' }: {
  icon: any; label: string; color?: string
}) {
  return (
    <div className="flex items-center gap-2 mb-3">
      <Icon size={13} className={color} />
      <span className={`text-xs font-medium uppercase tracking-widest ${color}`}>{label}</span>
    </div>
  )
}

// ─── Main page ────────────────────────────────────────────────────────────────
export default function ProfilePage() {
  const { user } = useAuth()
  const { token, logout } = useAuthStore()

  const [resendingVerification, setResendingVerification] = useState(false)
  const [verificationSent, setVerificationSent] = useState(false)
  const [loggingOutAll, setLoggingOutAll] = useState(false)
  const [confirmingDelete, setConfirmingDelete] = useState(false)
  const [deleting, setDeleting] = useState(false)

  async function handleResendVerification() {
    setResendingVerification(true)
    try {
      await api.resendVerification()
      setVerificationSent(true)
    } catch { /* ignore — rate limited or already verified */ }
    setResendingVerification(false)
  }

  async function handleLogoutAll() {
    setLoggingOutAll(true)
    try {
      await api.logoutAllDevices()
    } finally {
      logout() // also clears this device's session
    }
  }

  async function handleDeleteAccount() {
    setDeleting(true)
    try {
      await api.deleteAccount()
      logout()
    } catch {
      setDeleting(false)
    }
  }

  const [form, setForm] = useState({
    full_name: user?.full_name ?? '',
    bio: user?.bio ?? '',
    github_url: user?.github_url ?? '',
    linkedin_url: user?.linkedin_url ?? '',
    experience_level: user?.experience_level ?? 'beginner',
  })
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const [formError, setFormError] = useState('')

  const [scorecard, setScorecard] = useState<Scorecard | null>(null)
  const [scorecardLoading, setScorecardLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  // Load scorecard
  useEffect(() => {
    async function load() {
      try {
        const data = await api.getScorecard()
        setScorecard(data)
      } catch { /* no scorecard yet */ }
      setScorecardLoading(false)
    }
    load()
  }, [])

  const refreshScorecard = async () => {
    setRefreshing(true)
    try {
      const data = await api.getScorecard(true)
      setScorecard(data)
    } catch { /* ignore */ }
    setRefreshing(false)
  }

  async function handleSave(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    setFormError('')
    try {
      const updated = await api.updateMe(form)
      // Refresh the cached user only — reusing setAuth's default TTL
      // here would silently extend the session on every profile save.
      if (token) useAuthStore.setState({ user: updated })
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } catch (err) {
      setFormError(getErrorMessage(err))
    }
    setSaving(false)
  }

  if (!user) return null

  const sc = scorecard
  const hasActivity = sc && (
    sc.exams_attempted > 0 || sc.projects_submitted > 0 || sc.mentor_sessions_count > 0
  )

  return (
    <AppShell>
      <PageHeader title="Profile" subtitle="Your account, preferences, and verified engineer scorecard." />

      <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="max-w-4xl space-y-6">

          {/* ── Top: avatar + grade badge ── */}
          <Card className="p-6">
            <div className="flex items-center gap-5">
              <div className="w-16 h-16 rounded-full bg-amber/10 border-2 border-amber/30 flex items-center justify-center shrink-0">
                <span className="text-2xl font-display font-bold text-amber">
                  {user.full_name.charAt(0).toUpperCase()}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 flex-wrap">
                  <h2 className="font-display font-bold text-bright text-lg">{user.full_name}</h2>
                  {sc?.hire_ready && (
                    <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald/10 border border-emerald/30 text-xs font-semibold text-emerald">
                      <ShieldCheck size={11} />
                      Hire Ready
                    </span>
                  )}
                  {sc?.overall_grade && (
                    <span className={`px-2.5 py-1 rounded-full bg-surface border border-border text-xs font-mono font-bold ${gradeColor(sc.overall_grade)}`}>
                      Grade {sc.overall_grade}
                    </span>
                  )}
                </div>
                <p className="text-sm text-ghost">{user.email}</p>
                <div className="flex items-center gap-3 mt-1.5 flex-wrap">
                  <span className="text-xs px-2 py-0.5 rounded bg-amber/10 border border-amber/20 text-amber capitalize">
                    {user.experience_level}
                  </span>
                  <span className="text-xs text-ghost capitalize">{user.role}</span>
                  {sc?.certs_earned ? (
                    <span className="flex items-center gap-1 text-xs text-emerald">
                      <Trophy size={11} /> {sc.certs_earned} certification{sc.certs_earned !== 1 ? 's' : ''}
                    </span>
                  ) : null}
                </div>
              </div>
              <div className="text-end shrink-0">
                <div className="text-3xl font-display font-bold text-amber">
                  {user.overall_readiness_score.toFixed(0)}%
                </div>
                <div className="text-xs text-ghost">Readiness score</div>
              </div>
            </div>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* ── Left: edit form ── */}
            <div className="lg:col-span-1 space-y-4">
              <Card className="p-5">
                <h3 className="font-medium text-bright mb-4 flex items-center gap-2 text-sm">
                  <User size={14} className="text-ghost" />
                  Edit profile
                </h3>
                <form onSubmit={handleSave} className="space-y-3">
                  <Input
                    label="Full name"
                    value={form.full_name}
                    onChange={e => setForm(p => ({ ...p, full_name: e.target.value }))}
                  />
                  <div>
                    <label className="text-xs font-medium text-soft tracking-wide uppercase block mb-1.5">Bio</label>
                    <textarea
                      className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 min-h-20 resize-none"
                      placeholder="Your goals and background…"
                      value={form.bio}
                      onChange={e => setForm(p => ({ ...p, bio: e.target.value }))}
                    />
                  </div>
                  <div>
                    <label className="text-xs font-medium text-soft tracking-wide uppercase block mb-1.5">Level</label>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-1.5">
                      {(['beginner', 'intermediate', 'advanced'] as const).map(level => (
                        <button
                          key={level}
                          type="button"
                          onClick={() => setForm(p => ({ ...p, experience_level: level }))}
                          className={`py-1.5 rounded border text-xs transition-all capitalize ${
                            form.experience_level === level
                              ? 'bg-amber/10 border-amber/40 text-amber'
                              : 'bg-surface border-border text-ghost hover:text-soft'
                          }`}
                        >
                          {level}
                        </button>
                      ))}
                    </div>
                  </div>
                  <Input
                    label="GitHub"
                    placeholder="https://github.com/…"
                    value={form.github_url}
                    onChange={e => setForm(p => ({ ...p, github_url: e.target.value }))}
                  />
                  <Input
                    label="LinkedIn"
                    placeholder="https://linkedin.com/in/…"
                    value={form.linkedin_url}
                    onChange={e => setForm(p => ({ ...p, linkedin_url: e.target.value }))}
                  />
                  {formError && (
                    <div className="px-3 py-2 rounded bg-rose/10 border border-rose/20 text-xs text-rose">{formError}</div>
                  )}
                  <Button type="submit" loading={saving} variant={saved ? 'ghost' : 'amber'} className="w-full">
                    {saved ? <><CheckCircle size={13} className="text-emerald" /> Saved</> : <><Save size={13} /> Save changes</>}
                  </Button>
                </form>
              </Card>

              {/* Account info */}
              <Card className="p-5">
                <h3 className="font-medium text-bright mb-3 text-sm">Account</h3>
                <div className="space-y-2 text-sm">
                  {[
                    { label: 'Email', value: user.email },
                    { label: 'Member since', value: new Date(user.created_at).toLocaleDateString() },
                    { label: 'Role', value: user.role },
                  ].map(({ label, value }) => (
                    <div key={label} className="flex items-center justify-between py-2 border-b border-border last:border-0">
                      <span className="text-ghost text-xs">{label}</span>
                      <span className="text-soft text-xs capitalize">{value}</span>
                    </div>
                  ))}
                </div>

                {!user.is_verified && (
                  <div className="mt-3 pt-3 border-t border-border">
                    {verificationSent ? (
                      <p className="text-xs text-emerald flex items-center gap-1.5">
                        <CheckCircle size={12} /> Verification email sent — check your inbox.
                      </p>
                    ) : (
                      <button
                        onClick={handleResendVerification}
                        disabled={resendingVerification}
                        className="text-xs text-amber hover:text-amber2 flex items-center gap-1.5 disabled:opacity-50"
                      >
                        <Mail size={12} /> Email not verified — resend verification link
                      </button>
                    )}
                  </div>
                )}
              </Card>

              {/* Danger zone */}
              <Card className="p-5">
                <h3 className="font-medium text-bright mb-3 text-sm">Session &amp; account</h3>
                <div className="space-y-2">
                  <Button variant="outline" size="sm" className="w-full justify-start" onClick={handleLogoutAll} loading={loggingOutAll}>
                    <LogOut size={13} /> Log out on all devices
                  </Button>

                  {!confirmingDelete ? (
                    <button
                      onClick={() => setConfirmingDelete(true)}
                      className="w-full flex items-center gap-2 text-xs text-rose hover:text-rose/80 py-2"
                    >
                      <Trash2 size={13} /> Delete account
                    </button>
                  ) : (
                    <div className="px-3 py-3 rounded-lg bg-rose/5 border border-rose/20 space-y-2">
                      <p className="text-xs text-rose leading-relaxed">
                        This deactivates your account and removes your personal info. This can&apos;t be undone from the app.
                      </p>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" className="flex-1" onClick={() => setConfirmingDelete(false)}>
                          Cancel
                        </Button>
                        <button
                          onClick={handleDeleteAccount}
                          disabled={deleting}
                          className="flex-1 text-xs font-medium text-void bg-rose hover:bg-rose/90 rounded-lg disabled:opacity-50"
                        >
                          {deleting ? 'Deleting…' : 'Confirm delete'}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </Card>
            </div>

            {/* ── Right: Engineer Scorecard ── */}
            <div className="col-span-2 space-y-5">

              {/* Header */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ShieldCheck size={16} className="text-amber" />
                  <h3 className="font-display font-bold text-bright">Engineer Scorecard</h3>
                  <Badge variant="amber">Verified</Badge>
                </div>
                <button
                  onClick={refreshScorecard}
                  disabled={refreshing}
                  className="flex items-center gap-1.5 text-xs text-ghost hover:text-soft transition-colors"
                >
                  <RefreshCw size={12} className={refreshing ? 'animate-spin' : ''} />
                  {sc?.last_computed_at
                    ? `Updated ${new Date(sc.last_computed_at).toLocaleDateString()}`
                    : 'Compute'}
                </button>
              </div>

              {scorecardLoading ? (
                <Card className="p-12 flex items-center justify-center">
                  <Spinner className="w-5 h-5" />
                </Card>
              ) : !hasActivity ? (
                <Card className="p-10 text-center">
                  <Activity size={32} className="text-ghost mx-auto mb-3" />
                  <p className="text-bright font-medium mb-1">No activity yet</p>
                  <p className="text-xs text-ghost max-w-xs mx-auto leading-relaxed">
                    Complete exams, submit projects, and use the AI mentor to build your verified scorecard.
                  </p>
                </Card>
              ) : (
                <div className="space-y-5">

                  {/* Hire-ready banner */}
                  {sc?.hire_ready && (
                    <div className="flex items-center gap-3 px-4 py-3 bg-emerald/5 border border-emerald/20 rounded-lg">
                      <ShieldCheck size={18} className="text-emerald flex-shrink-0" />
                      <div>
                        <p className="text-sm font-semibold text-emerald">Hire-Ready Engineer</p>
                        <p className="text-xs text-ghost">You meet all benchmarks for a production AI Engineer role.</p>
                      </div>
                      <div className={`ml-auto text-3xl font-mono font-bold ${gradeColor(sc.overall_grade)}`}>
                        {sc.overall_grade}
                      </div>
                    </div>
                  )}

                  {/* Certification */}
                  <div>
                    <SectionHeader icon={Trophy} label="Certification" color="text-amber" />
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      <MetricCard
                        icon={Award}
                        label="Certs earned"
                        value={`${sc!.certs_earned}`}
                        sub="verified badges"
                        valueClass="text-emerald"
                        locked={sc!.certs_earned === 0}
                      />
                      <MetricCard
                        icon={Target}
                        label="Exam pass rate"
                        value={fmt(sc!.exam_pass_rate, 0, '%')}
                        sub={`${sc!.exams_attempted} attempted`}
                        valueClass={sc!.exam_pass_rate && sc!.exam_pass_rate >= 70 ? 'text-emerald' : 'text-amber'}
                        locked={sc!.exams_attempted === 0}
                      />
                      <MetricCard
                        icon={Star}
                        label="Avg project score"
                        value={fmt(sc!.avg_project_score, 1, '/100')}
                        sub={`${sc!.projects_submitted} submitted`}
                        valueClass={scoreColor(sc!.avg_project_score ?? 0)}
                        locked={sc!.projects_submitted === 0}
                      />
                    </div>
                  </div>

                  {/* Performance */}
                  <div>
                    <SectionHeader icon={Zap} label="Performance" color="text-sky" />
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      <MetricCard
                        icon={Clock}
                        label="Avg latency"
                        value={fmtMs(sc!.avg_latency_ms)}
                        sub="LLM response time"
                        valueClass={latencyColor(sc!.avg_latency_ms)}
                        locked={sc!.avg_latency_ms === null}
                      />
                      <MetricCard
                        icon={Activity}
                        label="P95 latency"
                        value={fmtMs(sc!.p95_latency_ms)}
                        sub="95th percentile"
                        valueClass={latencyColor(sc!.p95_latency_ms)}
                        locked={sc!.p95_latency_ms === null}
                      />
                      <MetricCard
                        icon={DollarSign}
                        label="Cost / 1K req"
                        value={sc!.cost_per_1k_requests !== null ? `$${sc!.cost_per_1k_requests!.toFixed(4)}` : '—'}
                        sub={`${sc!.total_tokens_used.toLocaleString()} tokens total`}
                        valueClass="text-sky"
                        locked={sc!.cost_per_1k_requests === null}
                      />
                    </div>
                  </div>

                  {/* Quality */}
                  <div>
                    <SectionHeader icon={ShieldCheck} label="Quality" color="text-emerald" />
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <Card className="p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs text-ghost">Hallucination rate</span>
                          <AlertTriangle size={13} className="text-ghost" />
                        </div>
                        {sc!.hallucination_rate !== null ? (
                          <>
                            <div className={`text-xl font-mono font-bold mb-1 ${hallucinationColor(sc!.hallucination_rate)}`}>
                              {(sc!.hallucination_rate! * 100).toFixed(1)}%
                            </div>
                            <ProgressBar
                              value={100 - sc!.hallucination_rate! * 100}
                              color={sc!.hallucination_rate! < 0.05 ? 'emerald' : sc!.hallucination_rate! < 0.15 ? 'amber' : 'rose'}
                            />
                            <p className="text-xs text-ghost mt-1">
                              {sc!.hallucination_rate! < 0.05 ? 'Excellent accuracy' : sc!.hallucination_rate! < 0.15 ? 'Acceptable' : 'Needs improvement'}
                            </p>
                          </>
                        ) : (
                          <div className="flex flex-col items-start gap-1">
                            <Lock size={14} className="text-ghost" />
                            <span className="text-xs text-ghost">No data yet</span>
                          </div>
                        )}
                      </Card>

                      <Card className="p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs text-ghost">Retrieval precision</span>
                          <Target size={13} className="text-ghost" />
                        </div>
                        {sc!.retrieval_precision !== null ? (
                          <>
                            <div className={`text-xl font-mono font-bold mb-1 ${scoreColor(sc!.retrieval_precision!)}`}>
                              {sc!.retrieval_precision!.toFixed(1)}%
                            </div>
                            <ProgressBar
                              value={sc!.retrieval_precision!}
                              color={sc!.retrieval_precision! >= 75 ? 'emerald' : sc!.retrieval_precision! >= 50 ? 'amber' : 'rose'}
                            />
                          </>
                        ) : (
                          <div className="flex flex-col items-start gap-1">
                            <Lock size={14} className="text-ghost" />
                            <span className="text-xs text-ghost">No data yet</span>
                          </div>
                        )}
                      </Card>

                      <Card className="p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs text-ghost">Code quality</span>
                          <Code2 size={13} className="text-ghost" />
                        </div>
                        {sc!.code_quality_score !== null ? (
                          <>
                            <div className={`text-xl font-mono font-bold mb-1 ${scoreColor(sc!.code_quality_score!)}`}>
                              {sc!.code_quality_score!.toFixed(1)}<span className="text-xs text-ghost">/100</span>
                            </div>
                            <ProgressBar
                              value={sc!.code_quality_score!}
                              color={sc!.code_quality_score! >= 75 ? 'emerald' : sc!.code_quality_score! >= 50 ? 'amber' : 'rose'}
                            />
                          </>
                        ) : (
                          <div className="flex flex-col items-start gap-1">
                            <Lock size={14} className="text-ghost" />
                            <span className="text-xs text-ghost">Submit a project first</span>
                          </div>
                        )}
                      </Card>

                      <Card className="p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs text-ghost">Overall grade</span>
                          <TrendingUp size={13} className="text-ghost" />
                        </div>
                        {sc!.overall_grade ? (
                          <>
                            <div className={`text-3xl font-mono font-bold mb-1 ${gradeColor(sc!.overall_grade)}`}>
                              {sc!.overall_grade}
                            </div>
                            <p className="text-xs text-ghost">
                              {sc!.overall_grade === 'A+' ? 'Exceptional' :
                               sc!.overall_grade === 'A'  ? 'Excellent' :
                               sc!.overall_grade === 'B+' ? 'Very good' :
                               sc!.overall_grade === 'B'  ? 'Good' :
                               sc!.overall_grade === 'C'  ? 'Developing' : 'Needs work'}
                            </p>
                          </>
                        ) : (
                          <div className="flex flex-col items-start gap-1">
                            <Lock size={14} className="text-ghost" />
                            <span className="text-xs text-ghost">No grade yet</span>
                          </div>
                        )}
                      </Card>
                    </div>
                  </div>

                  {/* Activity summary */}
                  <div>
                    <SectionHeader icon={BookOpen} label="Activity" color="text-violet" />
                    <Card className="p-4">
                      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 divide-x-0 lg:divide-x divide-border">
                        {[
                          { icon: Brain,    label: 'Mentor sessions', value: `${sc!.mentor_sessions_count}` },
                          { icon: BookOpen, label: 'Quizzes passed',  value: `${sc!.quizzes_passed}` },
                          { icon: Code2,    label: 'Projects done',   value: `${sc!.projects_submitted}` },
                          { icon: Clock,    label: 'Study time',      value: fmtMinutes(sc!.total_study_minutes) },
                        ].map(({ icon: Icon, label, value }) => (
                          <div key={label} className="lg:ps-4 lg:first:ps-0">
                            <div className="flex items-center gap-1.5 mb-1">
                              <Icon size={11} className="text-ghost" />
                              <span className="text-xs text-ghost">{label}</span>
                            </div>
                            <span className="text-lg font-mono font-bold text-bright">{value}</span>
                          </div>
                        ))}
                      </div>
                    </Card>
                  </div>

                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  )
}
