'use client'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Badge, Spinner, ProgressBar } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import {
  Zap, Lock, CheckCircle, Code2, Download,
  ChevronRight, AlertTriangle, Trophy, Star,
  Play, RotateCcw, X, Send, FileJson, Lightbulb, Loader2
} from 'lucide-react'

// ─── Types ────────────────────────────────────────────────────────────────────
interface Challenge {
  id: number
  title: string
  slug: string
  difficulty: string
  credit_cost: number
  passing_score: number
  description: string
  tags: string[]
  is_enrolled: boolean
  best_score: number | null
  status: string | null
}

interface ChallengeDetail extends Challenge {
  dataset_description: string
  dataset_filename: string
  dirty_dataset: any[]
  grading_rubric: { criterion: string; weight: number; description: string }[]
  hints: string[]
  max_attempts: number
  attempts_used: number
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
const DIFF_COLORS: Record<string, string> = {
  beginner:     'emerald',
  intermediate: 'amber',
  advanced:     'rose',
}

const STATUS_LABEL: Record<string, string> = {
  enrolled:  'In Progress',
  submitted: 'Submitted',
  graded:    'Graded',
  passed:    'Passed ✓',
  failed:    'Failed',
}

function DiffBadge({ diff }: { diff: string }) {
  const color = DIFF_COLORS[diff] ?? 'ghost'
  return <Badge variant={color as any} className="capitalize">{diff}</Badge>
}

// ─── Enroll Modal ─────────────────────────────────────────────────────────────
function EnrollModal({ challenge, onClose, onSuccess }: {
  challenge: Challenge; onClose: () => void; onSuccess: () => void
}) {
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState('')

  const handleEnroll = async () => {
    setLoading(true)
    setError('')
    try {
      await api.enrollChallenge(challenge.slug)
      onSuccess()
      onClose()
    } catch (e: any) {
      const detail = e?.response?.data?.detail
      if (typeof detail === 'object' && detail?.error === 'insufficient_credits') {
        setError(`Not enough credits. You need ${detail.credits_needed} but have ${detail.credits_available}. Buy more credits from the wallet.`)
      } else {
        setError(typeof detail === 'string' ? detail : 'Enrollment failed.')
      }
    }
    setLoading(false)
  }

  return (
    <>
      <div className="fixed inset-0 bg-void/80 backdrop-blur-sm z-40" onClick={onClose} />
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="bg-ink border border-border rounded-xl shadow-2xl w-full max-w-sm pointer-events-auto p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-bright">Unlock Challenge</h2>
            <button onClick={onClose} className="text-ghost hover:text-bright"><X size={15} /></button>
          </div>
          <p className="text-sm text-soft mb-4 leading-relaxed">{challenge.title}</p>
          <div className="flex items-center justify-between py-3 px-4 bg-surface border border-border rounded-lg mb-4">
            <span className="text-xs text-ghost">Cost</span>
            <span className="text-lg font-mono font-bold text-amber">{challenge.credit_cost} credits</span>
          </div>
          <ul className="space-y-1.5 mb-5">
            {['Access the full dirty dataset', 'Submit your cleaning pipeline', 'Get AI-graded feedback per rubric criterion', `Up to ${3} attempts`].map(item => (
              <li key={item} className="flex items-center gap-2 text-xs text-ghost">
                <CheckCircle size={11} className="text-emerald flex-shrink-0" /> {item}
              </li>
            ))}
          </ul>
          {error && (
            <div className="flex items-start gap-2 px-3 py-2.5 rounded-lg bg-rose/10 border border-rose/20 mb-4">
              <AlertTriangle size={12} className="text-rose flex-shrink-0 mt-0.5" />
              <p className="text-xs text-rose">{error}</p>
            </div>
          )}
          <Button className="w-full" onClick={handleEnroll} loading={loading}>
            <Zap size={13} /> Spend {challenge.credit_cost} Credits & Unlock
          </Button>
        </div>
      </div>
    </>
  )
}

// ─── Submit Modal ─────────────────────────────────────────────────────────────
function SubmitModal({ challenge, onClose, onSuccess }: {
  challenge: ChallengeDetail; onClose: () => void; onSuccess: (result: any) => void
}) {
  const [code, setCode]       = useState('')
  const [notes, setNotes]     = useState('')
  const [github, setGithub]   = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState('')

  const handleSubmit = async () => {
    if (!code.trim()) { setError('Please paste your solution code.'); return }
    setLoading(true)
    setError('')
    try {
      const result = await api.submitChallengeAttempt(challenge.slug, { solution_code: code, solution_notes: notes, github_url: github })
      onSuccess(result)
      onClose()
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? 'Submission failed.')
    }
    setLoading(false)
  }

  return (
    <>
      <div className="fixed inset-0 bg-void/80 backdrop-blur-sm z-40" onClick={onClose} />
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="bg-ink border border-border rounded-xl shadow-2xl w-full max-w-2xl pointer-events-auto flex flex-col max-h-[90vh]">
          <div className="flex items-center justify-between px-5 py-4 border-b border-border flex-shrink-0">
            <h2 className="text-sm font-semibold text-bright">Submit Solution — {challenge.title}</h2>
            <button onClick={onClose} className="text-ghost hover:text-bright"><X size={15} /></button>
          </div>
          <div className="flex-1 overflow-y-auto p-5 space-y-4">
            <div>
              <label className="text-xs font-medium text-soft uppercase tracking-widest block mb-1.5">Solution Code *</label>
              <textarea
                className="w-full bg-void border border-border rounded-lg text-sky-300 font-mono text-xs p-3 outline-none focus:border-amber/40 resize-none leading-relaxed"
                rows={14}
                placeholder="Paste your complete cleaning pipeline code here..."
                value={code}
                onChange={e => setCode(e.target.value)}
                style={{ fontFamily: 'var(--font-jetbrains), monospace' }}
              />
            </div>
            <div>
              <label className="text-xs font-medium text-soft uppercase tracking-widest block mb-1.5">Explanation / Notes</label>
              <textarea
                className="w-full bg-surface border border-border rounded-lg text-soft text-sm p-3 outline-none focus:border-amber/40 resize-none"
                rows={3}
                placeholder="Explain your approach, design decisions, and any trade-offs..."
                value={notes}
                onChange={e => setNotes(e.target.value)}
              />
            </div>
            <div>
              <label className="text-xs font-medium text-soft uppercase tracking-widest block mb-1.5">GitHub URL (optional)</label>
              <input
                className="w-full bg-surface border border-border rounded-lg px-3 py-2.5 text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50"
                placeholder="https://github.com/you/solution"
                value={github}
                onChange={e => setGithub(e.target.value)}
              />
            </div>
            {error && (
              <div className="flex items-start gap-2 px-3 py-2.5 rounded-lg bg-rose/10 border border-rose/20">
                <AlertTriangle size={12} className="text-rose flex-shrink-0 mt-0.5" />
                <p className="text-xs text-rose">{error}</p>
              </div>
            )}
          </div>
          <div className="px-5 py-4 border-t border-border flex-shrink-0">
            <Button className="w-full" onClick={handleSubmit} loading={loading}>
              {loading ? 'Grading with AI...' : <><Send size={13} /> Submit for AI Grading</>}
            </Button>
          </div>
        </div>
      </div>
    </>
  )
}

// ─── Challenge Card ───────────────────────────────────────────────────────────
function ChallengeCard({ ch, onSelect }: { ch: Challenge; onSelect: () => void }) {
  const statusColor = ch.status === 'passed' ? 'text-emerald' : ch.status === 'failed' ? 'text-rose' : 'text-amber'

  return (
    <Card glow className="p-5">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2 flex-wrap">
          <DiffBadge diff={ch.difficulty} />
          {ch.status && (
            <span className={`text-xs font-medium ${statusColor}`}>{STATUS_LABEL[ch.status] ?? ch.status}</span>
          )}
        </div>
        <div className="flex items-center gap-1.5 text-xs font-mono">
          <Zap size={11} className="text-amber" />
          <span className="text-amber font-bold">{ch.credit_cost}</span>
          <span className="text-ghost">credits</span>
        </div>
      </div>

      <h3 className="font-display font-bold text-bright text-base mb-2">{ch.title}</h3>
      <p className="text-xs text-ghost leading-relaxed mb-3 line-clamp-2">{ch.description}</p>

      <div className="flex flex-wrap gap-1.5 mb-4">
        {ch.tags.slice(0, 4).map(tag => (
          <span key={tag} className="text-xs px-2 py-0.5 rounded bg-surface border border-border text-ghost">{tag}</span>
        ))}
      </div>

      {ch.best_score !== null && (
        <div className="mb-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs text-ghost">Best score</span>
            <span className={`text-xs font-mono font-bold ${ch.best_score >= ch.passing_score ? 'text-emerald' : 'text-rose'}`}>
              {ch.best_score.toFixed(1)}%
            </span>
          </div>
          <ProgressBar value={ch.best_score} color={ch.best_score >= ch.passing_score ? 'emerald' : 'rose'} />
        </div>
      )}

      <Button
        className="w-full"
        variant={ch.is_enrolled ? 'outline' : 'amber'}
        size="sm"
        onClick={onSelect}
      >
        {ch.is_enrolled
          ? <><Play size={12} /> Open Challenge</>
          : <><Lock size={12} /> Unlock for {ch.credit_cost} credits</>
        }
      </Button>
    </Card>
  )
}

// ─── Challenge Detail View ────────────────────────────────────────────────────
function ChallengeDetailView({ slug, onBack }: { slug: string; onBack: () => void }) {
  const [ch, setCh]           = useState<ChallengeDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [showEnroll, setShowEnroll] = useState(false)
  const [showSubmit, setShowSubmit] = useState(false)
  const [result, setResult]   = useState<any>(null)
  const [activeTab, setActiveTab] = useState<'dataset' | 'rubric' | 'hints'>('dataset')
  const [hintQuestion, setHintQuestion] = useState('')
  const [hintLoading, setHintLoading] = useState(false)
  const [hintError, setHintError] = useState('')
  const [aiHints, setAiHints] = useState<{hint:string;concept:string;next_step:string}[]>([])

  const load = async () => {
    setLoading(true)
    try { setCh(await api.getChallenge(slug)) } catch {}
    setLoading(false)
  }

  useEffect(() => { load() }, [slug])

  const askForHint = async () => {
    if (!hintQuestion.trim()) return
    setHintLoading(true)
    setHintError('')
    try {
      const result = await api.getChallengeHint(slug, {
        stuck_on: hintQuestion,
        previous_hints: aiHints.map(h => h.hint),
      })
      setAiHints(prev => [...prev, result])
      setHintQuestion('')
    } catch (e: any) {
      const detail = (e as any)?.response?.data?.detail
      if (typeof detail === 'object' && detail?.error === 'insufficient_credits') {
        setHintError('Not enough credits. Buy more from the wallet.')
      } else {
        setHintError(typeof detail === 'string' ? detail : 'Failed to get hint.')
      }
    }
    setHintLoading(false)
  }

  const downloadDataset = () => {
    if (!ch) return
    const blob = new Blob([JSON.stringify(ch.dirty_dataset, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = ch.dataset_filename
    a.click()
    URL.revokeObjectURL(url)
  }

  if (loading) return <div className="flex-1 flex items-center justify-center"><Spinner className="w-6 h-6" /></div>
  if (!ch) return null

  const canSubmit = ch.is_enrolled && ch.status === 'enrolled'
  const canRetry  = ch.is_enrolled && (ch.status === 'failed') && (ch.attempts_used < ch.max_attempts)

  return (
    <div className="flex-1 overflow-y-auto px-8 py-6">
      {showEnroll && <EnrollModal challenge={ch} onClose={() => setShowEnroll(false)} onSuccess={load} />}
      {showSubmit && <SubmitModal challenge={ch} onClose={() => setShowSubmit(false)} onSuccess={r => { setResult(r); load() }} />}

      <button onClick={onBack} className="flex items-center gap-1.5 text-xs text-ghost hover:text-soft mb-5 transition-colors">
        ← Back to challenges
      </button>

      <div className="max-w-4xl space-y-6">
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <DiffBadge diff={ch.difficulty} />
              <span className="text-xs text-ghost font-mono">{ch.credit_cost} credits to unlock</span>
              <span className="text-xs text-ghost">·</span>
              <span className="text-xs text-ghost">Pass: {ch.passing_score}%</span>
              <span className="text-xs text-ghost">·</span>
              <span className="text-xs text-ghost">{ch.attempts_used}/{ch.max_attempts} attempts used</span>
            </div>
            <h1 className="font-display font-bold text-bright text-2xl mb-2">{ch.title}</h1>
            <p className="text-sm text-ghost leading-relaxed max-w-2xl">{ch.description}</p>
          </div>
          <div className="flex-shrink-0 flex flex-col gap-2">
            {!ch.is_enrolled && (
              <Button onClick={() => setShowEnroll(true)}>
                <Lock size={13} /> Unlock — {ch.credit_cost} credits
              </Button>
            )}
            {canSubmit && (
              <Button onClick={() => setShowSubmit(true)}>
                <Send size={13} /> Submit Solution
              </Button>
            )}
            {canRetry && (
              <Button variant="outline" onClick={() => setShowEnroll(true)}>
                <RotateCcw size={13} /> Retry — {ch.credit_cost} credits
              </Button>
            )}
            {ch.status === 'passed' && (
              <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald/10 border border-emerald/20">
                <Trophy size={14} className="text-emerald" />
                <span className="text-xs font-semibold text-emerald">Passed!</span>
              </div>
            )}
          </div>
        </div>

        {/* Grading result */}
        {result && (
          <Card className={`p-5 ${result.passed ? 'border-emerald/20' : 'border-rose/20'}`}>
            <div className="flex items-center gap-3 mb-4">
              {result.passed
                ? <Trophy size={18} className="text-emerald" />
                : <AlertTriangle size={18} className="text-amber" />
              }
              <div>
                <p className={`font-semibold text-sm ${result.passed ? 'text-emerald' : 'text-amber'}`}>
                  {result.passed ? 'Challenge Passed!' : 'Not quite — keep improving'}
                </p>
                <p className="text-xs text-ghost">Score: <span className="font-mono font-bold">{result.score}%</span></p>
              </div>
            </div>
            <p className="text-xs text-ghost leading-relaxed mb-4">{result.overall_feedback}</p>
            <div className="space-y-2">
              {result.feedback?.map((f: any) => (
                <div key={f.criterion} className="flex items-center gap-3 text-xs">
                  <span className={`w-2 h-2 rounded-full flex-shrink-0 ${f.passed ? 'bg-emerald' : 'bg-rose'}`} />
                  <span className="text-soft w-40 flex-shrink-0">{f.criterion}</span>
                  <span className="font-mono text-amber w-12">{f.score}%</span>
                  <span className="text-ghost flex-1">{f.feedback}</span>
                </div>
              ))}
            </div>
          </Card>
        )}

        {/* Tabs */}
        <div>
          <div className="flex gap-1 mb-4 border-b border-border">
            {(['dataset', 'rubric', 'hints'] as const).map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2.5 text-xs font-medium capitalize transition-colors border-b-2 -mb-px ${
                  activeTab === tab
                    ? 'border-amber text-amber'
                    : 'border-transparent text-ghost hover:text-soft'
                }`}
              >
                {tab === 'dataset' ? 'Dataset' : tab === 'rubric' ? 'Grading Rubric' : 'Hints'}
              </button>
            ))}
          </div>

          {activeTab === 'dataset' && (
            <div>
              <Card className="p-4 mb-3">
                <p className="text-xs text-ghost leading-relaxed whitespace-pre-line">{ch.dataset_description}</p>
              </Card>
              {ch.is_enrolled ? (
                <>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs text-ghost">{ch.dirty_dataset.length} records</span>
                    <button
                      onClick={downloadDataset}
                      className="flex items-center gap-1.5 text-xs text-amber hover:text-amber/80 transition-colors"
                    >
                      <Download size={12} /> Download {ch.dataset_filename}
                    </button>
                  </div>
                  <Card className="overflow-hidden">
                    <div className="flex items-center gap-2 px-4 py-2 bg-ink border-b border-border">
                      <FileJson size={13} className="text-ghost" />
                      <span className="text-xs font-mono text-ghost">{ch.dataset_filename}</span>
                    </div>
                    <pre className="p-4 text-xs font-mono text-sky-300 overflow-x-auto max-h-80 leading-relaxed"
                      style={{ fontFamily: 'var(--font-jetbrains), monospace' }}>
                      {JSON.stringify(ch.dirty_dataset.slice(0, 5), null, 2)}
                      {ch.dirty_dataset.length > 5 && `\n\n// ... ${ch.dirty_dataset.length - 5} more records`}
                    </pre>
                  </Card>
                </>
              ) : (
                <Card className="p-8 text-center border-dashed">
                  <Lock size={24} className="text-ghost mx-auto mb-3" />
                  <p className="text-sm text-bright mb-1">Dataset locked</p>
                  <p className="text-xs text-ghost">Unlock this challenge to access the full dirty dataset.</p>
                </Card>
              )}
            </div>
          )}

          {activeTab === 'rubric' && (
            <div className="space-y-3">
              {ch.grading_rubric.map((r, i) => (
                <Card key={i} className="p-4 flex items-start gap-4">
                  <div className="w-12 h-12 rounded-lg bg-amber/10 border border-amber/20 flex items-center justify-center flex-shrink-0">
                    <span className="text-sm font-mono font-bold text-amber">{r.weight}%</span>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-bright mb-1">{r.criterion}</p>
                    <p className="text-xs text-ghost leading-relaxed">{r.description}</p>
                  </div>
                </Card>
              ))}
            </div>
          )}

          {activeTab === 'hints' && (
            ch.is_enrolled ? (
              <div className="space-y-4">
                {ch.hints.length > 0 && (
                  <div className="space-y-2">
                    {ch.hints.map((hint, i) => (
                      <Card key={i} className="p-4 flex items-start gap-3">
                        <span className="w-5 h-5 rounded bg-amber/10 border border-amber/20 flex items-center justify-center text-xs font-mono text-amber flex-shrink-0">{i + 1}</span>
                        <p className="text-sm text-soft leading-relaxed">{hint}</p>
                      </Card>
                    ))}
                  </div>
                )}
                <Card className="p-5">
                  <div className="flex items-center gap-2 mb-3">
                    <Lightbulb size={14} className="text-amber" />
                    <span className="text-xs font-semibold text-amber uppercase tracking-widest">Ask AI Mentor for a Hint</span>
                    <span className="text-xs text-ghost ml-auto">1 credit per hint</span>
                  </div>
                  <p className="text-xs text-ghost mb-3 leading-relaxed">
                    Describe what you're stuck on. The AI will guide you toward the answer without revealing the solution.
                  </p>
                  <textarea
                    className="w-full bg-surface border border-border rounded-lg px-3 py-2.5 text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 resize-none mb-3"
                    rows={3}
                    placeholder="e.g. I'm not sure how to handle Arabic month names in the date column..."
                    value={hintQuestion}
                    onChange={e => setHintQuestion(e.target.value)}
                  />
                  {hintError && (
                    <div className="flex items-center gap-2 px-3 py-2 rounded bg-rose/10 border border-rose/20 mb-3">
                      <AlertTriangle size={12} className="text-rose" />
                      <p className="text-xs text-rose">{hintError}</p>
                    </div>
                  )}
                  <Button size="sm" variant="outline" onClick={askForHint} disabled={hintLoading || !hintQuestion.trim()} className="w-full">
                    {hintLoading
                      ? <><Loader2 size={12} className="animate-spin" /> Thinking...</>
                      : <><Lightbulb size={12} /> Get AI Hint (1 credit)</>
                    }
                  </Button>
                  {aiHints.length > 0 && (
                    <div className="mt-4 space-y-3">
                      {aiHints.map((h, i) => (
                        <div key={i} className="bg-void border border-border rounded-lg p-4">
                          <p className="text-xs text-ghost mb-1 font-medium">Hint {i + 1}</p>
                          <p className="text-sm text-soft leading-relaxed mb-2">{h.hint}</p>
                          {h.concept && (
                            <div className="flex items-center gap-2 mt-2">
                              <span className="text-xs text-ghost">Look up:</span>
                              <code className="text-xs px-2 py-0.5 rounded bg-surface border border-border text-amber font-mono">{h.concept}</code>
                            </div>
                          )}
                          {h.next_step && (
                            <p className="text-xs text-ghost mt-2">
                              <span className="text-soft font-medium">Next step:</span> {h.next_step}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </Card>
              </div>
            ) : (
              <Card className="p-8 text-center border-dashed">
                <Lock size={24} className="text-ghost mx-auto mb-3" />
                <p className="text-xs text-ghost">Unlock challenge to view hints.</p>
              </Card>
            )
          )}
        </div>
      </div>
    </div>
  )
}

// ─── Main Page ────────────────────────────────────────────────────────────────
export default function ChallengesPage() {
  const [challenges, setChallenges] = useState<Challenge[]>([])
  const [loading, setLoading]       = useState(true)
  const [selectedSlug, setSelectedSlug] = useState<string | null>(null)
  const [filter, setFilter]         = useState<string>('all')

  const load = async () => {
    setLoading(true)
    try { setChallenges(await api.getChallenges()) } catch {}
    setLoading(false)
  }

  useEffect(() => { load() }, [])

  const filtered = filter === 'all'
    ? challenges
    : filter === 'enrolled'
    ? challenges.filter(c => c.is_enrolled)
    : challenges.filter(c => c.difficulty === filter)

  if (selectedSlug) {
    return (
      <AppShell>
        <ChallengeDetailView slug={selectedSlug} onBack={() => { setSelectedSlug(null); load() }} />
      </AppShell>
    )
  }

  return (
    <AppShell>
      <PageHeader
        title="Challenge Projects"
        subtitle="Unlock real-world dirty data challenges. Pay with credits, submit your pipeline, get AI-graded feedback."
      />
      <div className="flex-1 overflow-y-auto px-8 py-6">

        {/* Filter tabs */}
        <div className="flex items-center gap-2 mb-6 flex-wrap">
          {['all', 'enrolled', 'beginner', 'intermediate', 'advanced'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-all ${
                filter === f
                  ? 'bg-amber/10 border border-amber/30 text-amber'
                  : 'bg-surface border border-border text-ghost hover:text-soft'
              }`}
            >
              {f === 'all' ? 'All Challenges' : f === 'enrolled' ? 'My Challenges' : f}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="flex justify-center py-16"><Spinner className="w-6 h-6" /></div>
        ) : filtered.length === 0 ? (
          <Card className="p-12 text-center">
            <Code2 size={32} className="text-ghost mx-auto mb-3" />
            <p className="text-bright font-medium mb-1">No challenges found</p>
            <p className="text-xs text-ghost">Try a different filter.</p>
          </Card>
        ) : (
          <div className="grid grid-cols-3 gap-5">
            {filtered.map(ch => (
              <ChallengeCard key={ch.id} ch={ch} onSelect={() => setSelectedSlug(ch.slug)} />
            ))}
          </div>
        )}
      </div>
    </AppShell>
  )
}
