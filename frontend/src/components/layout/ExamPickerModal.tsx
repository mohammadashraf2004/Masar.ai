'use client'
import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useI18n } from '@/lib/i18n'
import { api } from '@/lib/api'
import { cn } from '@/lib/utils'
import { Spinner } from '@/components/ui/index'
import { ShieldCheck, X, Trophy, Clock, Star, CheckCircle, Lock } from 'lucide-react'

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
export function ExamPickerModal({ onClose }: { onClose: () => void }) {
  const { t } = useI18n()
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

        // Which exams a certificate was issued for, by the exam id the API sends with each
        // (a certificate without one, from an older API, marks nothing rather than everything).
        const certExamIds = new Set(
          certs.map((c) => c.exam_id).filter((id): id is number => typeof id === 'number'),
        )

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
        className="fixed inset-0 bg-scrim/80 backdrop-blur-sm z-40"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="bg-ink border border-border rounded-xl shadow-2xl w-full max-w-lg pointer-events-auto flex flex-col max-h-[80vh]">

          {/* Header */}
          <div className="flex items-center justify-between px-5 py-4 border-b border-border flex-shrink-0">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-md bg-amber/10 border border-amber/20 flex items-center justify-center">
                <ShieldCheck size={14} className="text-amber-text" />
              </div>
              <div>
                <h2 className="ui-card-title">Get Verified</h2>
                <p className="text-xs text-ghost">Choose a certification exam to take</p>
              </div>
            </div>
            <button
              type="button"
              onClick={onClose}
              aria-label={t('common.close')}
              className="w-11 h-11 lg:w-7 lg:h-7 rounded flex items-center justify-center text-ghost hover:text-bright hover:bg-surface transition-colors"
            >
              <X size={15} />
            </button>
          </div>

          {/* Body */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {loading && (
              <div className="flex flex-col items-center justify-center py-12 gap-3" role="status">
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
                  className="inline-block mt-4 text-xs text-amber-text hover:underline"
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
                    <span className="text-xs text-amber-text bg-amber/10 border border-amber/20 px-2 py-0.5 rounded-full">
                      Attempted
                    </span>
                  ) : (
                    <span className="text-xs text-sky bg-sky/10 border border-sky/20 px-2 py-0.5 rounded-full">
                      Available
                    </span>
                  )}
                </div>

                {/* Title */}
                <h3 className="ui-card-title mb-1">{exam.title}</h3>
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
                    <span className="flex items-center gap-1 text-xs text-amber-text font-mono ml-auto">
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
                    <span className="text-xs text-ghost ms-1">
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
