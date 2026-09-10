'use client'
import { useEffect, useRef, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import { MentorMessage, CodeReviewResult, SkillGapResult, InterviewQuestion } from '@/types'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import {
  Send, Brain, Code, Target, Mic2,
  Plus, RotateCcw, ChevronRight, AlertCircle
} from 'lucide-react'

type Tool = 'chat' | 'code-review' | 'skill-gap' | 'interview'

const TOOLS: { key: Tool; icon: typeof Brain; label: string; desc: string }[] = [
  { key: 'chat',        icon: Brain,    label: 'Mentor chat',   desc: 'Ask anything about your curriculum' },
  { key: 'code-review', icon: Code,     label: 'Code review',   desc: 'Paste code for AI feedback' },
  { key: 'skill-gap',   icon: Target,   label: 'Skill gap',     desc: 'Analyze your profile against a role' },
  { key: 'interview',   icon: Mic2,     label: 'Mock interview', desc: 'Practice with AI interview questions' },
]

export default function MentorPage() {
  useAuth()
  // Aliased: `language` on this page already means the code-review
  // language picker (python/js/...), which is a different axis entirely.
  const { language: uiLanguage, mode } = useI18n()
  const [tool, setTool] = useState<Tool>('chat')
  const [messages, setMessages] = useState<MentorMessage[]>([{
    role: 'assistant',
    // Greets in Arabic because that is the platform's default posture. Its
    // *answers* follow the same policy the lessons do — Arabic explanation,
    // English terminology, untouched code — enforced server-side from the
    // language settings sent with each message (see language_policy.py).
    content: 'أهلاً! أنا مرشدك الذكي. أقدر أشرح لك المفاهيم، وأختبرك فيها، وأراجع الكود بتاعك.\n\nعلى إيه شغّال دلوقتي؟',
    timestamp: new Date().toISOString(),
  }])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const chatRef = useRef<HTMLDivElement>(null)

  // Code review state
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [codeCtx, setCodeCtx] = useState('')
  const [codeReview, setCodeReview] = useState<CodeReviewResult | null>(null)
  const [reviewLoading, setReviewLoading] = useState(false)

  // Skill gap state
  const [cvText, setCvText] = useState('')
  const [targetRole, setTargetRole] = useState('AI Engineer')
  const [currentSkills, setCurrentSkills] = useState('')
  const [skillGap, setSkillGap] = useState<SkillGapResult | null>(null)
  const [gapLoading, setGapLoading] = useState(false)

  // Interview state
  const [interviewTopic, setInterviewTopic] = useState('Machine Learning concepts')
  const [interviewDiff, setInterviewDiff] = useState('intermediate')
  const [question, setQuestion] = useState<InterviewQuestion | null>(null)
  const [answer, setAnswer] = useState('')
  const [qa, setQa] = useState<Array<{ question: string; answer: string }>>([])
  const [interviewLoading, setInterviewLoading] = useState(false)

  useEffect(() => {
    chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, loading])

  async function sendMessage() {
    const text = input.trim()
    if (!text || loading) return
    setInput('')
    setSuggestions([])

    const userMsg: MentorMessage = { role: 'user', content: text, timestamp: new Date().toISOString() }
    setMessages(p => [...p, userMsg])
    setLoading(true)

    try {
      // The mentor answers in the reader's language and terminology mode —
      // the same policy the lessons follow, applied server-side.
      const res = await api.chat(text, undefined, {
        language: uiLanguage,
        terminology_mode: mode,
      })
      setMessages(p => [...p, { role: 'assistant', content: res.reply, timestamp: new Date().toISOString() }])
      setSuggestions(res.suggested_actions)
    } catch {
      setMessages(p => [...p, {
        role: 'assistant',
        content: '⚠️ Could not reach the mentor. Check your API configuration.',
        timestamp: new Date().toISOString(),
      }])
    }
    setLoading(false)
  }

  async function runCodeReview(e: React.FormEvent) {
    e.preventDefault()
    setReviewLoading(true)
    try {
      const r = await api.reviewCode(code, language, codeCtx || undefined)
      setCodeReview(r)
    } catch {}
    setReviewLoading(false)
  }

  async function runSkillGap(e: React.FormEvent) {
    e.preventDefault()
    setGapLoading(true)
    try {
      const r = await api.analyzeSkillGap({
        target_role: targetRole,
        current_skills: currentSkills.split(',').map(s => s.trim()).filter(Boolean),
        cv_text: cvText || undefined,
      })
      setSkillGap(r)
    } catch {}
    setGapLoading(false)
  }

  async function nextQuestion() {
    if (question && answer) {
      setQa(p => [...p, { question: question.question, answer }])
      setAnswer('')
    }
    setInterviewLoading(true)
    try {
      const q = await api.getMockInterviewQuestion(interviewTopic, interviewDiff, qa)
      setQuestion(q)
    } catch {}
    setInterviewLoading(false)
  }

  const severityColor = { low: 'text-emerald', medium: 'text-amber', high: 'text-rose' }
  const priorityColor = { medium: 'text-amber', high: 'text-rose', critical: 'text-rose' }

  return (
    <AppShell>
      <PageHeader title="AI Mentor" subtitle="Your personal AI career coach." />

      <div className="flex-1 flex flex-col lg:flex-row lg:overflow-hidden min-w-0">
        {/* ── Tool selector sidebar ── */}
        <div className="w-full lg:w-56 shrink-0 flex lg:block gap-2 lg:gap-0 lg:space-y-1 overflow-x-auto lg:overflow-x-visible border-b lg:border-b-0 lg:border-e border-border bg-ink px-3 py-3 lg:py-4">
          {TOOLS.map(({ key, icon: Icon, label, desc }) => (
            <button
              key={key}
              onClick={() => setTool(key)}
              className={cn(
                'w-40 shrink-0 lg:w-full text-start p-3 rounded border transition-all',
                tool === key
                  ? 'bg-amber/10 border-amber/20 text-amber'
                  : 'border-transparent text-dim hover:text-bright hover:bg-surface'
              )}
            >
              <div className="flex items-center gap-2 mb-1">
                <Icon size={13} className={tool === key ? 'text-amber' : 'text-ghost'} />
                <span className="text-sm font-medium">{label}</span>
              </div>
              <p className="text-xs leading-snug opacity-70 hidden lg:block">{desc}</p>
            </button>
          ))}
        </div>

        {/* ── Tool content ── */}
        <div className="flex-1 min-w-0 flex flex-col lg:overflow-hidden">

          {/* CHAT */}
          {tool === 'chat' && (
            <>
              <div ref={chatRef} className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6 space-y-4">
                {messages.map((msg, i) => (
                  <div key={i} className={cn('flex gap-2.5', msg.role === 'user' ? 'justify-end' : 'justify-start')}>
                    {msg.role === 'assistant' && (
                      <div className="w-6 h-6 rounded-full bg-amber/10 border border-amber/20 flex items-center justify-center mt-1 shrink-0">
                        <Brain size={11} className="text-amber" />
                      </div>
                    )}
                    <div className={cn(
                      'max-w-[85%] lg:max-w-[70%] min-w-0 [overflow-wrap:anywhere] px-4 py-3 rounded-xl text-sm',
                      msg.role === 'user'
                        ? 'bg-amber/10 border border-amber/20 text-bright rounded-br-sm'
                        : 'bg-surface border border-border text-soft rounded-bl-sm'
                    )}>
                      {msg.role === 'assistant' ? (
                        <div
                          className="prose-dark text-sm leading-relaxed"
                          dir={uiLanguage === 'ar' ? 'rtl' : 'ltr'}
                        >
                          <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                        </div>
                      ) : (
                        <p className="leading-relaxed">{msg.content}</p>
                      )}
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="flex items-start gap-2.5">
                    <div className="w-6 h-6 rounded-full bg-amber/10 border border-amber/20 flex items-center justify-center mt-1 shrink-0">
                      <Brain size={11} className="text-amber" />
                    </div>
                    <div className="bg-surface border border-border rounded-xl rounded-bl-sm px-4 py-3">
                      <div className="flex gap-1">
                        {[0, 150, 300].map(d => (
                          <span key={d} className="w-1.5 h-1.5 bg-amber/60 rounded-full animate-bounce"
                            style={{ animationDelay: `${d}ms` }} />
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Suggestions */}
              {suggestions.length > 0 && (
                <div className="px-4 sm:px-6 lg:px-8 pb-3 flex gap-2 flex-wrap">
                  {suggestions.map(s => (
                    <button key={s} onClick={() => setInput(s)}
                      className="px-3 py-1.5 rounded-full text-xs bg-surface border border-border text-dim hover:text-bright hover:border-amber/30 transition-colors">
                      {s}
                    </button>
                  ))}
                </div>
              )}

              {/* Quick prompts */}
              <div className="px-4 sm:px-6 lg:px-8 pb-3 flex gap-2 flex-wrap">
                {[
                  'Quiz me on PyTorch',
                  'Explain RAG simply',
                  'Review my training loop',
                  'Mock ML interview question',
                ].map(p => (
                  <button key={p} onClick={() => setInput(p)}
                    className="px-3 py-1.5 rounded-full text-xs bg-surface border border-border text-ghost hover:text-amber hover:border-amber/30 transition-colors">
                    {p}
                  </button>
                ))}
              </div>

              {/* Input */}
              <div className="px-4 sm:px-6 lg:px-8 pb-6 flex gap-3">
                <input
                  className="flex-1 bg-surface border border-border rounded-lg px-4 py-3 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 transition-colors"
                  placeholder="Ask your mentor anything…"
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                />
                <Button onClick={sendMessage} loading={loading} className="px-4">
                  <Send size={14} />
                </Button>
              </div>
            </>
          )}

          {/* CODE REVIEW */}
          {tool === 'code-review' && (
            <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6">
              <form onSubmit={runCodeReview} className="space-y-4 max-w-3xl">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs text-ghost uppercase tracking-wide mb-1.5 block">Language</label>
                    <select
                      className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright focus:outline-none focus:border-amber/50"
                      value={language}
                      onChange={e => setLanguage(e.target.value)}
                    >
                      {['python', 'javascript', 'typescript', 'bash', 'sql'].map(l => (
                        <option key={l} value={l}>{l}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="text-xs text-ghost uppercase tracking-wide mb-1.5 block">Context (optional)</label>
                    <input
                      className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50"
                      placeholder="What should this code do?"
                      value={codeCtx}
                      onChange={e => setCodeCtx(e.target.value)}
                    />
                  </div>
                </div>
                <div>
                  <label className="text-xs text-ghost uppercase tracking-wide mb-1.5 block">Your code</label>
                  <textarea
                    className="w-full bg-ink border border-border rounded px-4 py-3 text-base md:text-sm font-mono text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 resize-none"
                    rows={14}
                    placeholder="Paste your code here…"
                    value={code}
                    onChange={e => setCode(e.target.value)}
                    required
                  />
                </div>
                <Button type="submit" loading={reviewLoading}>
                  <Code size={13} /> Review code
                </Button>
              </form>

              {codeReview && (
                <div className="mt-6 max-w-3xl space-y-4">
                  <Card className="p-5">
                    <div className="flex items-center justify-between mb-4">
                      <span className="font-medium text-bright">Review result</span>
                      <div className="flex items-center gap-3">
                        <span className={cn('text-sm font-mono capitalize',
                          codeReview.overall_quality === 'excellent' ? 'text-emerald'
                          : codeReview.overall_quality === 'good' ? 'text-amber'
                          : 'text-rose'
                        )}>
                          {codeReview.overall_quality}
                        </span>
                        <span className="text-2xl font-display font-bold text-amber">{codeReview.score}</span>
                        <span className="text-ghost text-sm">/100</span>
                      </div>
                    </div>
                    <p className="text-sm text-soft leading-relaxed">{codeReview.summary}</p>
                  </Card>

                  {codeReview.issues.length > 0 && (
                    <Card className="p-5">
                      <h3 className="text-sm font-medium text-ghost uppercase tracking-wide mb-3">Issues</h3>
                      <div className="space-y-3">
                        {codeReview.issues.map((issue, i) => (
                          <div key={i} className="flex items-start gap-3 p-3 rounded bg-surface">
                            <AlertCircle size={13} className={severityColor[issue.severity] ?? 'text-amber'} />
                            <div>
                              <div className="flex items-center gap-2 mb-0.5">
                                <span className="text-xs font-medium text-bright">{issue.type}</span>
                                {issue.line && <span className="text-xs text-ghost">line {issue.line}</span>}
                                <span className={cn('text-xs', severityColor[issue.severity] ?? 'text-amber')}>
                                  {issue.severity}
                                </span>
                              </div>
                              <p className="text-xs text-soft">{issue.message}</p>
                              <p className="text-xs text-dim mt-0.5">→ {issue.suggestion}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </Card>
                  )}

                  {codeReview.strengths.length > 0 && (
                    <Card className="p-5">
                      <h3 className="text-sm font-medium text-ghost uppercase tracking-wide mb-3">Strengths</h3>
                      <ul className="space-y-1.5">
                        {codeReview.strengths.map((s, i) => (
                          <li key={i} className="text-sm text-soft flex items-start gap-2">
                            <span className="text-emerald mt-0.5">✓</span> {s}
                          </li>
                        ))}
                      </ul>
                    </Card>
                  )}
                </div>
              )}
            </div>
          )}

          {/* SKILL GAP */}
          {tool === 'skill-gap' && (
            <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6">
              <form onSubmit={runSkillGap} className="space-y-4 max-w-2xl">
                <div>
                  <label className="text-xs text-ghost uppercase tracking-wide mb-1.5 block">Target role</label>
                  <input
                    className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright focus:outline-none focus:border-amber/50"
                    value={targetRole}
                    onChange={e => setTargetRole(e.target.value)}
                  />
                </div>
                <div>
                  <label className="text-xs text-ghost uppercase tracking-wide mb-1.5 block">
                    Current skills (comma-separated)
                  </label>
                  <input
                    className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50"
                    placeholder="Python, NumPy, basic ML…"
                    value={currentSkills}
                    onChange={e => setCurrentSkills(e.target.value)}
                  />
                </div>
                <div>
                  <label className="text-xs text-ghost uppercase tracking-wide mb-1.5 block">
                    CV / resume text (optional)
                  </label>
                  <textarea
                    className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 min-h-28 resize-none"
                    placeholder="Paste your CV or LinkedIn summary…"
                    value={cvText}
                    onChange={e => setCvText(e.target.value)}
                  />
                </div>
                <Button type="submit" loading={gapLoading}>
                  <Target size={13} /> Analyze skill gap
                </Button>
              </form>

              {skillGap && (
                <div className="mt-6 max-w-2xl space-y-4">
                  <Card className="p-5">
                    <div className="flex items-center justify-between mb-3">
                      <span className="font-medium text-bright">Readiness for {skillGap.target_role}</span>
                      <span className={cn('text-2xl font-display font-bold',
                        skillGap.readiness_score >= 70 ? 'text-emerald'
                        : skillGap.readiness_score >= 40 ? 'text-amber'
                        : 'text-rose'
                      )}>
                        {skillGap.readiness_score}%
                      </span>
                    </div>
                    <p className="text-sm text-soft leading-relaxed">{skillGap.summary}</p>
                  </Card>

                  <Card className="p-5">
                    <h3 className="text-sm font-medium text-ghost uppercase tracking-wide mb-3">Missing skills</h3>
                    <div className="space-y-2">
                      {skillGap.missing_skills.map((s, i) => (
                        <div key={i} className="flex items-start gap-3 p-3 rounded bg-surface">
                          <span className={cn('text-xs font-mono mt-0.5 shrink-0', priorityColor[s.priority as 'medium' | 'high' | 'critical'])}>
                            {s.priority}
                          </span>
                          <div>
                            <p className="text-sm font-medium text-bright">{s.skill}</p>
                            <p className="text-xs text-ghost">{s.reason}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </Card>

                  <Card className="p-5">
                    <h3 className="text-sm font-medium text-ghost uppercase tracking-wide mb-3">Recommended roadmap</h3>
                    <ol className="space-y-2">
                      {skillGap.recommended_roadmap.map((step, i) => (
                        <li key={i} className="flex items-start gap-3 text-sm text-soft">
                          <span className="text-xs font-mono text-amber mt-0.5 shrink-0 w-5">{i + 1}.</span>
                          {step}
                        </li>
                      ))}
                    </ol>
                  </Card>
                </div>
              )}
            </div>
          )}

          {/* MOCK INTERVIEW */}
          {tool === 'interview' && (
            <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6 max-w-2xl">
              <div className="flex gap-4 mb-6">
                <div className="flex-1">
                  <label className="text-xs text-ghost uppercase tracking-wide mb-1.5 block">Topic</label>
                  <select
                    className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright focus:outline-none focus:border-amber/50"
                    value={interviewTopic}
                    onChange={e => setInterviewTopic(e.target.value)}
                  >
                    {['Machine Learning concepts', 'Deep Learning', 'Python', 'System design', 'Behavioral'].map(t => (
                      <option key={t} value={t}>{t}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-xs text-ghost uppercase tracking-wide mb-1.5 block">Difficulty</label>
                  <select
                    className="bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright focus:outline-none focus:border-amber/50"
                    value={interviewDiff}
                    onChange={e => setInterviewDiff(e.target.value)}
                  >
                    {['beginner', 'intermediate', 'advanced'].map(d => (
                      <option key={d} value={d}>{d}</option>
                    ))}
                  </select>
                </div>
              </div>

              {!question ? (
                <Button onClick={nextQuestion} loading={interviewLoading} size="lg">
                  <Mic2 size={14} /> Start interview
                </Button>
              ) : (
                <div className="space-y-4">
                  <Card className="p-5">
                    <div className="flex items-start gap-3 mb-3">
                      <span className="px-2 py-0.5 rounded bg-amber/10 border border-amber/20 text-xs text-amber font-mono shrink-0">
                        {question.question_type}
                      </span>
                    </div>
                    <p className="text-base text-bright leading-relaxed mb-4">{question.question}</p>
                    {question.hints.length > 0 && (
                      <details className="text-sm">
                        <summary className="text-ghost cursor-pointer hover:text-soft">Show hints</summary>
                        <ul className="mt-2 space-y-1 ps-3">
                          {question.hints.map((h, i) => (
                            <li key={i} className="text-dim text-xs">→ {h}</li>
                          ))}
                        </ul>
                      </details>
                    )}
                  </Card>

                  <div>
                    <label className="text-xs text-ghost uppercase tracking-wide mb-1.5 block">Your answer</label>
                    <textarea
                      className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 min-h-28 resize-none"
                      placeholder="Type your answer…"
                      value={answer}
                      onChange={e => setAnswer(e.target.value)}
                    />
                  </div>

                  <div className="flex gap-3">
                    <Button onClick={nextQuestion} loading={interviewLoading}>
                      <ChevronRight size={13} /> Next question
                    </Button>
                    <Button variant="ghost" onClick={() => { setQuestion(null); setQa([]); setAnswer('') }}>
                      <RotateCcw size={13} /> Restart
                    </Button>
                  </div>

                  {qa.length > 0 && (
                    <Card className="p-4">
                      <h3 className="text-xs font-medium text-ghost uppercase tracking-wide mb-3">
                        Session history ({qa.length} questions)
                      </h3>
                      <div className="space-y-3">
                        {qa.map((item, i) => (
                          <div key={i} className="text-xs">
                            <p className="text-soft font-medium mb-0.5">Q{i + 1}: {item.question}</p>
                            <p className="text-ghost ps-3 border-s border-border">{item.answer || '(no answer)'}</p>
                          </div>
                        ))}
                      </div>
                    </Card>
                  )}
                </div>
              )}
            </div>
          )}

        </div>
      </div>
    </AppShell>
  )
}
