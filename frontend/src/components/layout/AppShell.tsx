'use client'
import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { useAuthStore } from '@/lib/store'
import { useI18n } from '@/lib/i18n'
import type { StringKey } from '@/lib/i18n'
import { api } from '@/lib/api'
import { cn } from '@/lib/utils'
import { Spinner } from '@/components/ui/index'
import { LogoMark, Wordmark } from '@/components/layout/Logo'
import {
  LayoutDashboard, BookOpen, Brain,
  LogOut, ChevronRight, Zap, Users,
  ShieldCheck, X, Trophy, Clock, Star,
  CheckCircle, Lock, Flame, Wrench, BookMarked
} from 'lucide-react'

// Labels are i18n keys, not strings: the sidebar is the one piece of chrome
// on every page, so it has to follow the reader's language like the content
// does.
const NAV: Array<{ href: string; icon: React.ElementType; label: StringKey }> = [
  { href: '/dashboard',  icon: LayoutDashboard, label: 'nav.dashboard' },
  { href: '/tracks',     icon: BookOpen,        label: 'nav.tracks' },
  { href: '/tools',      icon: Wrench,          label: 'nav.tools' },
  { href: '/glossary',   icon: BookMarked,      label: 'nav.glossary' },
  { href: '/mentor',     icon: Brain,           label: 'nav.mentor' },
  { href: '/community',  icon: Users,           label: 'nav.community' },
  { href: '/challenges', icon: Flame,           label: 'nav.challenges' },
]

// ─── Types ────────────────────────────────────────────────────────────────────
interface ExamSummary {
  id: number
  title: string
  description: string
  duration_minutes: number
  total_points: number
  passing_score: number
  track: { name: string; slug: string; icon?: string }
  attempts_used?: number
  max_attempts?: number
  best_score?: number | null
  passed?: boolean
}

// ─── Exam Picker Modal ────────────────────────────────────────────────────────
function ExamPickerModal({ onClose }: { onClose: () => void }) {
  const router = useRouter()
  const [exams, setExams] = useState<ExamSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        // Fetch my-attempts to enrich with past results
        const [attemptsData, certsData] = await Promise.allSettled([
          api.getMyAttempts(),
          api.getMyCertificates(),
        ])

        const attempts = attemptsData.status === 'fulfilled' ? attemptsData.value : []
        const certs    = certsData.status    === 'fulfilled' ? certsData.value    : []

        // Build a map of exam_id → best attempt info
        const attemptMap: Record<number, { best_score: number; passed: boolean; count: number }> = {}
        for (const a of attempts) {
          const eid = a.exam_id
          if (!attemptMap[eid]) attemptMap[eid] = { best_score: 0, passed: false, count: 0 }
          attemptMap[eid].count++
          if ((a.score ?? 0) > attemptMap[eid].best_score) attemptMap[eid].best_score = a.score ?? 0
          if (a.passed) attemptMap[eid].passed = true
        }

        const certExamIds = new Set(certs.map((c: any) => c.exam_id))

        // Fetch all exams across all enrolled tracks
        const enrollments = await api.getMyEnrollments()
        const examLists = await Promise.allSettled(
          enrollments.map((e: any) => api.getExamsForTrack(e.track.id))
        )

        const allExams: ExamSummary[] = []
        examLists.forEach((result, idx) => {
          if (result.status === 'fulfilled') {
            for (const exam of result.value) {
              const info = attemptMap[exam.id]
              allExams.push({
                ...exam,
                track: enrollments[idx].track,
                attempts_used: info?.count ?? 0,
                best_score: info?.best_score ?? null,
                passed: certExamIds.has(exam.id) || info?.passed || false,
              })
            }
          }
        })

        setExams(allExams)
      } catch (e: any) {
        setError('Could not load exams. Make sure you are enrolled in a track.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const handleStart = (examId: number) => {
    onClose()
    router.push(`/exam/${examId}`)
  }

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-void/80 backdrop-blur-sm z-40"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="bg-ink border border-border rounded-xl shadow-2xl w-full max-w-lg pointer-events-auto flex flex-col max-h-[80vh]">

          {/* Header */}
          <div className="flex items-center justify-between px-5 py-4 border-b border-border flex-shrink-0">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-md bg-amber/10 border border-amber/20 flex items-center justify-center">
                <ShieldCheck size={14} className="text-amber" />
              </div>
              <div>
                <h2 className="text-sm font-semibold text-bright">Get Verified</h2>
                <p className="text-xs text-ghost">Choose a certification exam to take</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="w-7 h-7 rounded flex items-center justify-center text-ghost hover:text-bright hover:bg-surface transition-colors"
            >
              <X size={15} />
            </button>
          </div>

          {/* Body */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {loading && (
              <div className="flex flex-col items-center justify-center py-12 gap-3">
                <Spinner className="w-5 h-5" />
                <p className="text-xs text-ghost">Loading available exams…</p>
              </div>
            )}

            {!loading && error && (
              <div className="py-10 text-center">
                <ShieldCheck size={28} className="text-ghost mx-auto mb-3" />
                <p className="text-sm text-bright mb-1">No exams available</p>
                <p className="text-xs text-ghost">{error}</p>
              </div>
            )}

            {!loading && !error && exams.length === 0 && (
              <div className="py-10 text-center">
                <Lock size={28} className="text-ghost mx-auto mb-3" />
                <p className="text-sm text-bright mb-1">No exams unlocked yet</p>
                <p className="text-xs text-ghost max-w-xs mx-auto">
                  Enroll in a career track and complete the curriculum to unlock certification exams.
                </p>
                <Link
                  href="/tracks"
                  onClick={onClose}
                  className="inline-block mt-4 text-xs text-amber hover:underline"
                >
                  Browse tracks →
                </Link>
              </div>
            )}

            {!loading && exams.map((exam) => (
              <div
                key={exam.id}
                className={cn(
                  'bg-surface border rounded-lg p-4 transition-all duration-150',
                  exam.passed
                    ? 'border-emerald/20 bg-emerald/5'
                    : 'border-border hover:border-amber/20'
                )}
              >
                {/* Track + status */}
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-1.5">
                    {exam.track.icon && <span className="text-sm">{exam.track.icon}</span>}
                    <span className="text-xs text-ghost">{exam.track.name}</span>
                  </div>
                  {exam.passed ? (
                    <span className="flex items-center gap-1 text-xs text-emerald bg-emerald/10 border border-emerald/20 px-2 py-0.5 rounded-full">
                      <CheckCircle size={10} />
                      Certified
                    </span>
                  ) : (exam.attempts_used ?? 0) > 0 ? (
                    <span className="text-xs text-amber bg-amber/10 border border-amber/20 px-2 py-0.5 rounded-full">
                      Attempted
                    </span>
                  ) : (
                    <span className="text-xs text-sky bg-sky/10 border border-sky/20 px-2 py-0.5 rounded-full">
                      Available
                    </span>
                  )}
                </div>

                {/* Title */}
                <h3 className="text-sm font-medium text-bright mb-1">{exam.title}</h3>
                <p className="text-xs text-ghost leading-relaxed mb-3 line-clamp-2">{exam.description}</p>

                {/* Meta row */}
                <div className="flex items-center gap-3 mb-3">
                  <span className="flex items-center gap-1 text-xs text-dim">
                    <Clock size={11} className="text-ghost" />
                    {exam.duration_minutes} min
                  </span>
                  <span className="flex items-center gap-1 text-xs text-dim">
                    <Trophy size={11} className="text-ghost" />
                    {exam.total_points} pts
                  </span>
                  <span className="flex items-center gap-1 text-xs text-dim">
                    <Star size={11} className="text-ghost" />
                    Pass: {exam.passing_score}+
                  </span>
                  {(exam.attempts_used ?? 0) > 0 && exam.best_score !== null && (
                    <span className="flex items-center gap-1 text-xs text-amber font-mono ml-auto">
                      Best: {exam.best_score}
                    </span>
                  )}
                </div>

                {/* Attempts */}
                {(exam.max_attempts ?? 3) > 0 && (
                  <div className="flex items-center gap-1.5 mb-3">
                    {Array.from({ length: exam.max_attempts ?? 3 }).map((_, i) => (
                      <span
                        key={i}
                        className={cn(
                          'w-2 h-2 rounded-full',
                          i < (exam.attempts_used ?? 0)
                            ? exam.passed ? 'bg-emerald' : 'bg-rose'
                            : 'bg-border'
                        )}
                      />
                    ))}
                    <span className="text-xs text-ghost ml-1">
                      {(exam.max_attempts ?? 3) - (exam.attempts_used ?? 0)} attempt{(exam.max_attempts ?? 3) - (exam.attempts_used ?? 0) !== 1 ? 's' : ''} left
                    </span>
                  </div>
                )}

                {/* CTA */}
                <button
                  onClick={() => handleStart(exam.id)}
                  disabled={exam.passed && (exam.attempts_used ?? 0) >= (exam.max_attempts ?? 3)}
                  className={cn(
                    'w-full py-2 rounded-lg text-xs font-semibold transition-all duration-150',
                    exam.passed
                      ? 'bg-emerald/10 border border-emerald/20 text-emerald hover:bg-emerald/20'
                      : (exam.attempts_used ?? 0) >= (exam.max_attempts ?? 3)
                      ? 'bg-surface border border-border text-ghost cursor-not-allowed'
                      : 'btn-amber'
                  )}
                >
                  {exam.passed
                    ? 'Retake Exam'
                    : (exam.attempts_used ?? 0) >= (exam.max_attempts ?? 3)
                    ? 'No attempts remaining'
                    : (exam.attempts_used ?? 0) > 0
                    ? 'Retry Exam'
                    : 'Start Exam'}
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}

// ─── AppShell ─────────────────────────────────────────────────────────────────
export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const { user, logout } = useAuthStore()
  const { t } = useI18n()
  const [showExamPicker, setShowExamPicker] = useState(false)

  return (
    <div className="flex h-screen bg-void overflow-hidden">

      {showExamPicker && <ExamPickerModal onClose={() => setShowExamPicker(false)} />}

      {/* ── Sidebar ── */}
      <aside className="w-56 shrink-0 flex flex-col bg-ink border-e border-border">

        {/* Brand */}
        <Link
          href="/dashboard"
          className="px-5 py-5 flex items-center gap-2.5 border-b border-border"
        >
          <LogoMark size={28} label={null} />
          <Wordmark className="text-sm" />
        </Link>

        {/* Readiness pill */}
        {user && (
          <div className="mx-3 mt-4 px-3 py-2 rounded bg-surface border border-border">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs text-ghost">{t('nav.readiness')}</span>
              <span className="text-xs font-mono text-amber">
                {user.overall_readiness_score.toFixed(0)}%
              </span>
            </div>
            <div className="h-1 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-amber to-amber2 rounded-full transition-all duration-700"
                style={{ width: `${user.overall_readiness_score}%` }}
              />
            </div>
          </div>
        )}

        {/* Nav */}
        <nav className="flex-1 px-3 mt-4 space-y-0.5">
          {NAV.map(({ href, icon: Icon, label }) => {
            const active = pathname === href || pathname.startsWith(href + '/')
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  'flex items-center gap-3 px-3 py-2.5 rounded text-sm transition-all duration-150 group',
                  active
                    ? 'bg-amber/10 text-amber border border-amber/20'
                    : 'text-dim hover:text-bright hover:bg-surface border border-transparent'
                )}
              >
                <Icon size={15} className={cn(active ? 'text-amber' : 'text-ghost group-hover:text-soft')} />
                <span className="flex-1">{t(label)}</span>
                {active && <ChevronRight size={12} className="text-amber/60 rtl:rotate-180" />}
              </Link>
            )
          })}
        </nav>

        {/* Quick actions */}
        <div className="mx-3 mb-3 px-3 py-2.5 rounded bg-surface border border-border">
          <div className="flex items-center gap-2 mb-1">
            <Zap size={12} className="text-amber" />
            <span className="text-xs text-amber font-medium">{t('nav.quickAction')}</span>
          </div>
          <Link href="/mentor" className="text-xs text-ghost hover:text-soft transition-colors">
            {t('nav.askMentor')} →
          </Link>
        </div>

        {/* ── Get Verified button ── */}
        <div className="mx-3 mb-3">
          <button
            onClick={() => setShowExamPicker(true)}
            className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded bg-amber/10 border border-amber/20 text-amber text-sm font-medium hover:bg-amber/20 hover:border-amber/40 transition-all duration-150 group"
          >
            <ShieldCheck size={15} className="flex-shrink-0" />
            <span className="flex-1 text-start">{t('nav.getVerified')}</span>
            <ChevronRight size={12} className="text-amber/50 group-hover:text-amber/80 transition-colors rtl:rotate-180" />
          </button>
        </div>

        {/* Sign out */}
        {user && (
          <div className="px-3 pb-4 border-t border-border pt-3">
            <button
              onClick={logout}
              className="w-full flex items-center gap-2 px-3 py-2 rounded text-xs text-ghost hover:text-rose hover:bg-rose/5 transition-colors"
            >
              <LogOut size={12} />
              {t('nav.signOut')}
            </button>
          </div>
        )}
      </aside>

      {/* ── Main content ── */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {children}
      </main>
    </div>
  )
}