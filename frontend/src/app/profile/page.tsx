'use client'
import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { Award, CheckCircle, Link2, LogOut, Mail, Save, Trash2, UserRound } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { useAuthStore } from '@/lib/store'
import { AppShell } from '@/components/layout/AppShell'
import { LegalFooter } from '@/components/layout/LegalFooter'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { api } from '@/lib/api'
import { countForm, useI18n } from '@/lib/i18n'
import { cn, getErrorMessage } from '@/lib/utils'
import type { CertificateSummary, LearningPath, MyCourse, ProfileActivity, SkillGapItem, SkillGaps } from '@/types'
import type { LabProjectCard } from '@/features/project-lab/types'

type Tab = 'profile' | 'settings'

interface Achievement {
  key: string
  kind: 'certificate' | 'project' | 'course'
  title: string
  subtitle: string
  date: string
  href?: string
}

const card = 'rounded-xl border border-border bg-surface'

// ─── Page ─────────────────────────────────────────────────────────────────────
export default function ProfilePage() {
  const { user } = useAuth()
  const { t, language } = useI18n()
  const [tab, setTab] = useState<Tab>('profile')

  if (!user) return null

  return (
    <AppShell>
      <div className="flex flex-1 flex-col overflow-y-auto px-4 pt-6 pb-[calc(1.25rem+env(safe-area-inset-bottom))] sm:px-6 lg:px-8">
        <div className="mx-auto flex w-full max-w-[1120px] flex-col gap-5">
          <div role="tablist" aria-label={t('profile.tab.profile')} className="flex gap-1.5 self-start rounded-full border border-border bg-surface p-1">
            {(['profile', 'settings'] as const).map(value => (
              <button
                key={value}
                type="button"
                role="tab"
                aria-selected={tab === value}
                onClick={() => setTab(value)}
                className={cn(
                  'flex h-9 items-center rounded-full px-4 text-sm transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring',
                  tab === value ? 'bg-amber font-semibold text-on-amber' : 'text-dim hover:text-bright',
                )}
              >
                {t(`profile.tab.${value}`)}
              </button>
            ))}
          </div>

          {tab === 'profile'
            ? <ProfileView language={language} onEdit={() => setTab('settings')} />
            : <SettingsView onDone={() => setTab('profile')} />}
        </div>
        <LegalFooter className="mx-auto w-full max-w-[1120px]" />
      </div>
    </AppShell>
  )
}

// ─── Profile tab ──────────────────────────────────────────────────────────────
function ProfileView({ language, onEdit }: { language: 'en' | 'ar'; onEdit: () => void }) {
  const { user } = useAuth()
  const { t, tf } = useI18n()
  const [path, setPath] = useState<LearningPath | null>(null)
  const [gaps, setGaps] = useState<SkillGaps | null>(null)
  const [activity, setActivity] = useState<ProfileActivity | null>(null)
  const [studyMinutes, setStudyMinutes] = useState<number | null>(null)
  const [certificates, setCertificates] = useState<CertificateSummary[]>([])
  const [courses, setCourses] = useState<MyCourse[]>([])
  const [projects, setProjects] = useState<LabProjectCard[]>([])

  useEffect(() => {
    let live = true
    const settle = <T,>(promise: Promise<T>, set: (value: T) => void) =>
      promise.then(value => { if (live) set(value) }).catch(() => { /* the section shows its empty state */ })
    settle(api.getMyLearningPath(), setPath)
    settle(api.getMySkillGaps(), setGaps)
    settle(api.getProfileActivity(84), setActivity)
    settle(api.getScorecard(), sc => setStudyMinutes((sc as { total_study_minutes?: number }).total_study_minutes ?? 0))
    settle(api.getMyCertificates(), setCertificates)
    settle(api.getMyCourses(), setCourses)
    settle(api.getLabProjects(), setProjects)
    return () => { live = false }
  }, [])

  const local = (en: string, ar?: string | null) => (language === 'ar' && ar ? ar : en)
  const monthYear = (iso: string) =>
    new Date(iso).toLocaleDateString(language === 'ar' ? 'ar-u-nu-latn-ca-gregory' : 'en-GB', { month: 'long', year: 'numeric' })

  if (!user) return null
  const stageIndex = path?.stages.findIndex(stage => stage.slug === path.current_stage_slug) ?? -1
  const pathPct = Math.round(path?.progress?.path_pct ?? path?.progress?.overall_pct ?? 0)
  const streak = activity?.current_streak ?? null
  const hours = studyMinutes === null ? null : Math.round(studyMinutes / 60)

  const stats = [
    { label: t('profile.stat.readiness'), value: Math.round(user.overall_readiness_score ?? 0), unit: '/100' },
    { label: t('profile.stat.streak'), value: streak, unit: streak === null ? '' : t(`profile.unit.days.${countForm(streak, language)}`) },
    { label: t('profile.stat.hours'), value: hours, unit: t('profile.unit.hours') },
    { label: t('profile.stat.certificates'), value: certificates.length, unit: t('profile.unit.earned') },
  ]

  return (
    <div className="flex flex-col gap-5">
      {/* ── Identity ── */}
      <section
        className={cn(card, 'flex flex-wrap items-center gap-6 rounded-[14px] p-7')}
        style={{ backgroundImage: `radial-gradient(70% 140% at ${language === 'ar' ? '100%' : '0%'} 0%, rgb(var(--acc) / 0.10), transparent 60%)` }}
      >
        <div className="grid size-[88px] flex-none place-items-center rounded-full border-2 border-amber bg-muted text-[34px] font-bold text-bright shadow-[0_0_0_5px_rgb(var(--acc)/0.12)]" aria-hidden="true">
          {user.full_name.charAt(0).toUpperCase()}
        </div>
        <div className="flex min-w-0 flex-[1_1_300px] flex-col gap-2">
          <h1 className="m-0 text-[26px] font-bold text-bright"><bdi>{user.full_name}</bdi></h1>
          <div className="flex flex-wrap gap-x-4 gap-y-2 text-sm text-dim">
            <span>{tf('profile.memberSince', { date: monthYear(user.created_at) })}</span>
            {path?.level && <span className="text-amber-text">{local(path.level.name, path.level.name_ar)}</span>}
          </div>
          {path ? (
            <div className="flex flex-wrap items-baseline gap-2">
              <span className="text-[15px] font-semibold text-bright">{local(path.career_goal.title, path.career_goal.title_ar)}</span>
              {language === 'ar' && path.career_goal.title_ar && (
                <span dir="ltr" className="font-display text-sm font-semibold text-ghost">{path.career_goal.title}</span>
              )}
              {stageIndex >= 0 && (
                <span className="rounded-full border border-border px-2.5 py-0.5 font-mono text-xs text-dim">
                  {tf('profile.stage', { n: stageIndex + 1, total: path.stages.length, pct: pathPct })}
                </span>
              )}
            </div>
          ) : (
            <Link href="/learn/masar" className="text-sm text-amber-text hover:text-amber-text2">{t('profile.buildPath')}</Link>
          )}
        </div>
        <div className="flex flex-wrap gap-2.5">
          <Link href="/profile/learning" className={buttonStyles({ variant: 'outline', className: 'h-11 gap-2' })}>
            <Link2 size={16} aria-hidden="true" />
            {t('profile.learningProfile')}
          </Link>
          <Button className="h-11" onClick={onEdit}>{t('profile.edit')}</Button>
        </div>
      </section>

      {/* ── Numbers ── */}
      <div className="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4">
        {stats.map(stat => (
          <div key={stat.label} className={cn(card, 'flex flex-col gap-1.5 px-5 py-[18px]')}>
            <span className="text-xs text-dim">{stat.label}</span>
            <div className="flex items-baseline gap-1.5">
              <span className="font-display text-[32px] font-extrabold leading-[1.1] text-bright">{stat.value ?? '—'}</span>
              <span className="text-xs text-ghost">{stat.unit}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="flex flex-wrap gap-5">
        <SkillMap path={path} gaps={gaps} language={language} />
        <ActivityMap activity={activity} language={language} />
      </div>

      <Achievements
        certificates={certificates}
        courses={courses}
        projects={projects}
        language={language}
      />
    </div>
  )
}

function SkillMap({ path, gaps, language }: { path: LearningPath | null; gaps: SkillGaps | null; language: 'en' | 'ar' }) {
  const { t, tf } = useI18n()
  const names = useMemo(() => {
    const all: SkillGapItem[] = gaps ? [...gaps.known, ...gaps.partial, ...gaps.missing] : []
    return new Map(all.map(item => [item.slug, item]))
  }, [gaps])
  const skills = Object.entries(path?.progress?.by_skill ?? {})
    .filter(([slug]) => names.has(slug))
    .map(([slug, value]) => ({ skill: names.get(slug)!, value: Math.round(value) }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 6)
  const gap = gaps?.missing.find(item => item.is_immediate) ?? gaps?.missing[0]
  const name = (item: SkillGapItem) => (language === 'ar' && item.name_ar ? item.name_ar : item.name)

  return (
    <section className={cn(card, 'flex min-w-0 flex-[1_1_340px] flex-col gap-4 p-[22px]')}>
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-[15px] font-semibold text-bright">{t('profile.skills.title')}</h2>
        <span className="text-xs text-ghost">{t('profile.skills.source')}</span>
      </div>
      {skills.length === 0 ? (
        <p className="text-sm text-dim">{t('profile.skills.empty')}</p>
      ) : (
        <ul className="flex flex-col gap-4">
          {skills.map(({ skill, value }) => (
            <li key={skill.slug} className="flex flex-col gap-1.5">
              <div className="flex justify-between gap-2.5 text-sm">
                <span dir="auto" className="text-bright">{name(skill)}</span>
                <span className="font-mono text-dim" dir="ltr">{value}%</span>
              </div>
              <div className="h-[5px] overflow-hidden rounded-[3px] bg-muted" role="progressbar" aria-valuenow={value} aria-valuemin={0} aria-valuemax={100} aria-label={name(skill)}>
                <div className={cn('h-full', value < 50 ? 'bg-rose' : 'bg-amber')} style={{ width: `${value}%` }} />
              </div>
            </li>
          ))}
        </ul>
      )}
      {gap && (
        <div className="flex items-start gap-2.5 rounded-lg bg-muted px-3.5 py-3 text-sm leading-7 text-soft">
          <span className="pt-0.5 font-mono text-[11px] text-amber-text">GAP</span>
          <span className="[text-wrap:pretty]">
            {tf(gap.is_immediate ? 'profile.skills.gapNow' : 'profile.skills.gapLater', { skill: name(gap) })}{' '}
            <Link href="/learn/masar" className="text-amber-text hover:text-amber-text2">{t('profile.skills.openPath')}</Link>
          </span>
        </div>
      )}
    </section>
  )
}

function ActivityMap({ activity, language }: { activity: ProfileActivity | null; language: 'en' | 'ar' }) {
  const { t, tf } = useI18n()
  const days = activity?.days ?? []
  const max = Math.max(1, ...days.map(day => day.count))
  const shade = (count: number) =>
    count === 0 ? 'bg-muted' : count <= max / 3 ? 'bg-amber/25' : count <= (2 * max) / 3 ? 'bg-amber/50' : 'bg-amber'

  return (
    <section className={cn(card, 'flex min-w-0 flex-[1_1_340px] flex-col gap-3.5 p-[22px]')}>
      <h2 className="text-[15px] font-semibold text-bright">{t('profile.activity.title')}</h2>
      <div
        dir="ltr"
        role="img"
        aria-label={`${t('profile.activity.title')}: ${tf(`profile.activity.days.${countForm(activity?.active_days ?? 0, language)}`, { n: activity?.active_days ?? 0 })}`}
        className="grid grid-flow-col grid-cols-12 grid-rows-7 gap-1"
      >
        {(days.length ? days : Array.from({ length: 84 }, () => ({ date: '', count: 0 }))).map((day, index) => (
          <div
            key={day.date || index}
            title={day.date ? tf('profile.activity.cell', { date: day.date, n: day.count }) : undefined}
            className={cn('aspect-square rounded-[2px]', shade(day.count))}
          />
        ))}
      </div>
      <div className="flex flex-wrap justify-between gap-2 text-xs text-dim">
        <span>
          {tf(`profile.activity.days.${countForm(activity?.active_days ?? 0, language)}`, { n: activity?.active_days ?? 0 })}
          <span className="text-ghost"> · {t('profile.activity.note')}</span>
        </span>
        <div className="flex items-center gap-1" aria-hidden="true">
          <span>{t('profile.activity.less')}</span>
          <span className="size-2.5 rounded-[2px] bg-muted" />
          <span className="size-2.5 rounded-[2px] bg-amber/35" />
          <span className="size-2.5 rounded-[2px] bg-amber" />
          <span>{t('profile.activity.more')}</span>
        </div>
      </div>
    </section>
  )
}

function Achievements({ certificates, courses, projects, language }: {
  certificates: CertificateSummary[]
  courses: MyCourse[]
  projects: LabProjectCard[]
  language: 'en' | 'ar'
}) {
  const { t, tf } = useI18n()
  const local = (en: string, ar?: string | null) => (language === 'ar' && ar ? ar : en)
  const items: Achievement[] = [
    ...certificates.map(c => ({
      key: `c-${c.certificate_id}`, kind: 'certificate' as const, title: c.track_title,
      subtitle: tf('profile.wins.score', { n: Math.round(c.score) }), date: c.issued_at, href: `/verify/${c.certificate_id}`,
    })),
    ...projects.filter(p => p.attempt?.status === 'completed').map(p => ({
      key: `p-${p.slug}`, kind: 'project' as const, title: local(p.title, p.title_ar),
      subtitle: t('profile.wins.projectDone'), date: p.attempt?.submitted_at ?? '', href: `/challenges/projects/${p.slug}`,
    })),
    ...courses.filter(c => c.status === 'completed' || c.progress >= 100).map(c => ({
      key: `k-${c.course_id}`, kind: 'course' as const, title: local(c.title, c.title_ar),
      subtitle: t('profile.wins.courseDone'), date: c.completed_at ?? '', href: c.href ?? `/courses/${c.slug}`,
    })),
  ].sort((a, b) => (b.date || '').localeCompare(a.date || '')).slice(0, 8)
  const pill = { certificate: 'border-emerald text-emerald', project: 'border-amber text-amber-text', course: 'border-dim text-dim' }

  return (
    <section className={cn(card, 'flex flex-col gap-4 p-[22px]')}>
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-[15px] font-semibold text-bright">{t('profile.wins.title')}</h2>
        <Link href="/certificates" className="text-sm text-amber-text hover:text-amber-text2">{t('profile.wins.all')}</Link>
      </div>
      {items.length === 0 ? (
        <p className="flex items-center gap-2 text-sm text-dim"><Award size={14} aria-hidden="true" />{t('profile.wins.empty')}</p>
      ) : (
        <ul className="grid gap-3 [grid-template-columns:repeat(auto-fill,minmax(240px,1fr))]">
          {items.map(item => {
            const body = (
              <>
                <div className="flex items-center justify-between gap-2">
                  <span className={cn('rounded-full border px-2 py-0.5 text-[11px]', pill[item.kind])}>{t(`profile.wins.${item.kind}`)}</span>
                  {item.date && <span className="font-mono text-[11px] text-ghost" dir="ltr">{item.date.slice(0, 7)}</span>}
                </div>
                <span dir="auto" className="font-display text-base font-bold text-bright">{item.title}</span>
                <span className="text-sm text-dim">{item.subtitle}</span>
              </>
            )
            return (
              <li key={item.key}>
                {item.href ? (
                  <Link href={item.href} className="flex h-full flex-col gap-2 rounded-[10px] border border-border bg-panel p-4 transition-colors hover:border-amber/40">{body}</Link>
                ) : (
                  <div className="flex h-full flex-col gap-2 rounded-[10px] border border-border bg-panel p-4">{body}</div>
                )}
              </li>
            )
          })}
        </ul>
      )}
    </section>
  )
}

// ─── Settings tab ─────────────────────────────────────────────────────────────
function SettingsView({ onDone }: { onDone: () => void }) {
  const { user } = useAuth()
  const { t } = useI18n()
  const { token, logout } = useAuthStore()
  const [form, setForm] = useState({
    full_name: user?.full_name ?? '',
    bio: user?.bio ?? '',
    github_url: user?.github_url ?? '',
    linkedin_url: user?.linkedin_url ?? '',
  })
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const [formError, setFormError] = useState('')
  const [verificationSent, setVerificationSent] = useState(false)
  const [resending, setResending] = useState(false)
  const [loggingOutAll, setLoggingOutAll] = useState(false)
  const [confirmingDelete, setConfirmingDelete] = useState(false)
  const [deleting, setDeleting] = useState(false)

  if (!user) return null

  async function save(event: React.FormEvent) {
    event.preventDefault()
    setSaving(true)
    setFormError('')
    try {
      const updated = await api.updateMe(form)
      // Refresh the cached user only: reusing setAuth's default TTL here
      // would silently extend the session on every profile save.
      if (token) useAuthStore.setState({ user: updated })
      setSaved(true)
      window.setTimeout(() => { setSaved(false); onDone() }, 900)
    } catch (err) {
      setFormError(getErrorMessage(err))
    }
    setSaving(false)
  }

  async function resend() {
    setResending(true)
    try {
      await api.resendVerification()
      setVerificationSent(true)
    } catch { /* rate limited or already verified */ }
    setResending(false)
  }

  async function logoutAll() {
    setLoggingOutAll(true)
    try {
      await api.logoutAllDevices()
    } finally {
      logout()
    }
  }

  async function deleteAccount() {
    setDeleting(true)
    try {
      await api.deleteAccount()
      logout()
    } catch {
      setDeleting(false)
    }
  }

  const row = 'flex min-h-11 items-center justify-between gap-4 border-b border-muted py-3.5 last:border-b-0'

  return (
    <form onSubmit={save} className="flex max-w-[760px] flex-col gap-5">
      <section className={cn(card, 'flex flex-col gap-4 p-[22px]')}>
        <h2 className="text-[15px] font-semibold text-bright">{t('profile.settings.personal')}</h2>
        <div className="grid gap-3.5 [grid-template-columns:repeat(auto-fit,minmax(240px,1fr))]">
          <Input label={t('profile.field.name')} dir="auto" value={form.full_name}
            onChange={e => setForm(p => ({ ...p, full_name: e.target.value }))} />
          <Input label={t('profile.field.email')} dir="ltr" value={user.email} readOnly />
          <Input label="GitHub" dir="ltr" placeholder="https://github.com/…" value={form.github_url}
            onChange={e => setForm(p => ({ ...p, github_url: e.target.value }))} />
          <Input label="LinkedIn" dir="ltr" placeholder="https://linkedin.com/in/…" value={form.linkedin_url}
            onChange={e => setForm(p => ({ ...p, linkedin_url: e.target.value }))} />
        </div>
        <label className="flex flex-col gap-1.5">
          <span className="text-xs text-dim">{t('profile.field.bio')}</span>
          <textarea
            dir="auto"
            className="min-h-20 w-full resize-none rounded-lg border border-border bg-panel px-3 py-2.5 text-base text-bright placeholder:text-ghost focus:border-amber/50 focus:outline-none md:text-sm"
            placeholder={t('profile.field.bioPlaceholder')}
            value={form.bio}
            onChange={e => setForm(p => ({ ...p, bio: e.target.value }))}
          />
        </label>
        {formError && <div role="alert" className="rounded border border-rose/20 bg-rose/10 px-3 py-2 text-xs text-rose">{formError}</div>}
      </section>

      <section className={cn(card, 'flex flex-col px-[22px] py-2')} aria-label={t('profile.settings.account')}>
        <div className={row}>
          <div className="flex flex-col gap-0.5">
            <span className="text-sm text-bright">{user.is_verified ? t('profile.verify.done') : t('profile.verify.pending')}</span>
            <span className="text-xs text-ghost" dir="ltr">{user.email}</span>
          </div>
          {user.is_verified ? (
            <CheckCircle size={18} className="text-emerald" aria-hidden="true" />
          ) : verificationSent ? (
            <span className="text-xs text-emerald">{t('profile.verify.sent')}</span>
          ) : (
            <Button type="button" variant="outline" size="sm" loading={resending} onClick={resend}>
              <Mail size={13} aria-hidden="true" /> {t('profile.verify.resend')}
            </Button>
          )}
        </div>
        <Link href="/profile/learning" className={cn(row, 'hover:text-bright')}>
          <div className="flex flex-col gap-0.5">
            <span className="text-sm text-bright">{t('profile.learningProfile')}</span>
            <span className="text-xs text-ghost">{t('profile.learning.hint')}</span>
          </div>
          <UserRound size={16} className="text-dim" aria-hidden="true" />
        </Link>
        <div className={row}>
          <div className="flex flex-col gap-0.5">
            <span className="text-sm text-bright">{t('profile.logoutAll')}</span>
            <span className="text-xs text-ghost">{t('profile.logoutAll.hint')}</span>
          </div>
          <Button type="button" variant="outline" size="sm" loading={loggingOutAll} onClick={logoutAll}>
            <LogOut size={13} aria-hidden="true" /> {t('profile.logoutAll')}
          </Button>
        </div>
        <div className={cn(row, 'flex-wrap')}>
          <div className="flex flex-col gap-0.5">
            <span className="text-sm text-rose">{t('profile.delete')}</span>
            <span className="text-xs text-ghost">{confirmingDelete ? t('profile.delete.confirm') : t('profile.delete.hint')}</span>
          </div>
          {confirmingDelete ? (
            <div className="flex gap-2">
              <Button type="button" variant="outline" size="sm" onClick={() => setConfirmingDelete(false)}>{t('profile.delete.cancel')}</Button>
              <button type="button" onClick={deleteAccount} disabled={deleting}
                className="min-h-9 rounded-lg bg-rose px-3 text-sm font-medium text-on-solid hover:bg-rose/90 disabled:opacity-50">
                {t('profile.delete')}
              </button>
            </div>
          ) : (
            <button type="button" onClick={() => setConfirmingDelete(true)}
              className="flex min-h-9 items-center gap-1.5 rounded-lg px-2 text-sm text-rose hover:bg-rose/10">
              <Trash2 size={13} aria-hidden="true" /> {t('profile.delete')}
            </button>
          )}
        </div>
      </section>

      <div className="flex flex-wrap justify-between gap-3">
        <button type="button" onClick={() => logout()}
          className="flex h-11 items-center rounded-lg border border-rose/40 px-[18px] text-sm text-rose hover:bg-rose/10">
          {t('profile.logout')}
        </button>
        <Button type="submit" className="h-11 px-[22px]" loading={saving} variant={saved ? 'ghost' : 'amber'}>
          {saved ? <><CheckCircle size={14} className="text-emerald" aria-hidden="true" /> {t('profile.saved')}</> : <><Save size={14} aria-hidden="true" /> {t('profile.save')}</>}
        </Button>
      </div>
    </form>
  )
}
