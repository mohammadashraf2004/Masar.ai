'use client'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { Card, Badge, Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { AnswerChat } from '@/components/ui/AnswerChat'
import { getErrorMessage } from '@/lib/utils'
import type { Quiz, QuizAttempt } from '@/types'
import { CheckCircle, XCircle, Trophy, RotateCcw, MessageSquare } from 'lucide-react'

interface QuizPanelProps {
  quiz: Quiz
}

export function QuizPanel({ quiz }: QuizPanelProps) {
  const [answers, setAnswers] = useState<Record<number, number>>({})
  const [result, setResult] = useState<QuizAttempt | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [loadingHistory, setLoadingHistory] = useState(true)
  const [bestPast, setBestPast] = useState<QuizAttempt | null>(null)

  const mcqIndices = quiz.questions
    .map((q, i) => ({ q, i }))
    .filter(({ q }) => (q.type ?? 'mcq') !== 'open')
    .map(({ i }) => i)
  const openIndices = quiz.questions
    .map((q, i) => ({ q, i }))
    .filter(({ q }) => q.type === 'open')
    .map(({ i }) => i)

  useEffect(() => {
    let cancelled = false
    api.getQuizAttempts(quiz.id).then(attempts => {
      if (cancelled) return
      if (attempts.length > 0) {
        const best = attempts.reduce((a, b) => (b.score > a.score ? b : a), attempts[0])
        setBestPast(best)
      }
      setLoadingHistory(false)
    }).catch(() => setLoadingHistory(false))
    return () => { cancelled = true }
  }, [quiz.id])

  async function handleSubmit() {
    setSubmitting(true)
    setError('')
    try {
      const answerPayload = Object.fromEntries(
        mcqIndices.map(i => [String(i), answers[i]]).filter(([, v]) => v !== undefined)
      ) as Record<string, number>
      const attempt = await api.submitQuiz(quiz.id, answerPayload)
      setResult(attempt)
      setBestPast(prev => (!prev || attempt.score > prev.score ? attempt : prev))
    } catch (err) {
      setError(getErrorMessage(err))
    }
    setSubmitting(false)
  }

  function retake() {
    setAnswers({})
    setResult(null)
  }

  const allMcqAnswered = mcqIndices.every(i => answers[i] !== undefined)

  return (
    <div className="space-y-4 max-w-3xl">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-medium text-bright">{quiz.title}</h3>
          <p className="text-xs text-ghost mt-0.5">
            {mcqIndices.length} multiple-choice{openIndices.length > 0 ? ` · ${openIndices.length} open-ended` : ''} · pass at {quiz.passing_score}%
          </p>
        </div>
        {!loadingHistory && bestPast && (
          <Badge variant={bestPast.passed ? 'emerald' : 'ghost'}>
            {bestPast.passed ? <CheckCircle size={11} className="mr-1" /> : null}
            Best: {Math.round(bestPast.score)}%
          </Badge>
        )}
      </div>

      {/* ── MCQ questions ── */}
      {mcqIndices.map(i => {
        const q = quiz.questions[i]
        const fb = result?.feedback?.[String(i)]
        const resolved = fb && !('skipped' in fb)
        return (
          <Card key={i} className="p-5">
            <p className="text-sm font-medium text-bright mb-3">
              {i + 1}. {q.question}
            </p>
            <div className="space-y-2">
              {(q.options ?? []).map((opt, oi) => {
                const selected = answers[i] === oi
                const showCorrectness = resolved && 'correct_answer' in fb
                const isCorrectOption = showCorrectness && fb.correct_answer === oi
                const isWrongSelected = showCorrectness && selected && !fb.correct
                return (
                  <button
                    key={oi}
                    disabled={!!result}
                    onClick={() => setAnswers(prev => ({ ...prev, [i]: oi }))}
                    className={`w-full text-left flex items-center gap-3 px-4 py-2.5 rounded-lg border text-sm transition-all ${
                      isCorrectOption
                        ? 'bg-emerald/10 border-emerald/40 text-emerald'
                        : isWrongSelected
                        ? 'bg-rose/10 border-rose/40 text-rose'
                        : selected
                        ? 'bg-amber/10 border-amber/40 text-amber'
                        : 'bg-surface border-border text-soft hover:border-amber/20'
                    } ${result ? 'cursor-default' : ''}`}
                  >
                    <span className={`w-4 h-4 rounded-full border-2 flex-shrink-0 flex items-center justify-center ${
                      selected || isCorrectOption ? 'border-current' : 'border-muted'
                    }`}>
                      {(selected || isCorrectOption) && <span className="w-2 h-2 rounded-full bg-current" />}
                    </span>
                    {opt}
                    {isCorrectOption && <CheckCircle size={13} className="ml-auto shrink-0" />}
                    {isWrongSelected && <XCircle size={13} className="ml-auto shrink-0" />}
                  </button>
                )
              })}
            </div>
            {resolved && 'explanation' in fb && fb.explanation && (
              <p className="text-xs text-ghost mt-3 pt-3 border-t border-border leading-relaxed">
                {fb.explanation}
              </p>
            )}
          </Card>
        )
      })}

      {mcqIndices.length > 0 && (
        <>
          {error && (
            <div className="px-3 py-2.5 rounded bg-rose/10 border border-rose/20 text-xs text-rose">{error}</div>
          )}
          {result ? (
            <Card className={`p-5 flex items-center gap-4 ${result.passed ? 'border-emerald/30' : 'border-amber/30'}`}>
              {result.passed ? <Trophy size={24} className="text-emerald shrink-0" /> : <XCircle size={24} className="text-amber shrink-0" />}
              <div className="flex-1">
                <p className="text-sm font-medium text-bright">
                  {result.passed ? 'Passed!' : 'Not quite — review and try again'}
                </p>
                <p className="text-xs text-ghost">Score: {Math.round(result.score)}% (need {quiz.passing_score}%)</p>
              </div>
              <Button size="sm" variant="outline" onClick={retake}>
                <RotateCcw size={12} /> Retake
              </Button>
            </Card>
          ) : (
            <Button onClick={handleSubmit} loading={submitting} disabled={!allMcqAnswered}>
              Submit Quiz
            </Button>
          )}
        </>
      )}

      {/* ── Open-ended questions ── */}
      {openIndices.map(i => {
        const q = quiz.questions[i]
        return (
          <Card key={i} className="p-5">
            <div className="flex items-start gap-2 mb-3">
              <MessageSquare size={14} className="text-amber shrink-0 mt-0.5" />
              <p className="text-sm font-medium text-bright">
                {i + 1}. {q.question}
              </p>
            </div>
            <AnswerChat target={{ kind: 'quiz_question', quizId: quiz.id, questionIndex: i }} />
          </Card>
        )
      })}

      {loadingHistory && mcqIndices.length === 0 && openIndices.length === 0 && (
        <div className="flex justify-center py-6"><Spinner className="w-5 h-5" /></div>
      )}
    </div>
  )
}
