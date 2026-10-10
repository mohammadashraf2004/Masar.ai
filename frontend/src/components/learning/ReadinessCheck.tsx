'use client'
import { useEffect, useId, useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { pick } from '@/lib/content-language'
import { useI18n } from '@/lib/i18n'
import { skillLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { AssessmentResult, ReadinessAssessment, ReadinessReport } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'

interface ReadinessCheckProps {
  slug: string
  /** The learner's updated readiness, once the server has graded the answers. */
  onResult: (report: ReadinessReport) => void
  onClose: () => void
}

/**
 * The short readiness check: a handful of real questions from the courses this
 * one builds on. The answer key never reaches the browser; the learner sends
 * their choices and the server grades them and returns the new readiness. There
 * is no pass or fail, only "you know this" and "review this".
 */
export function ReadinessCheck({ slug, onResult, onClose }: ReadinessCheckProps) {
  const { t, tf, language } = useI18n()
  const ctx = useLabelContext()
  const groupId = useId()
  const [assessment, setAssessment] = useState<ReadinessAssessment | null>(null)
  const [answers, setAnswers] = useState<Record<string, number>>({})
  const [result, setResult] = useState<AssessmentResult | null>(null)
  const [loadFailed, setLoadFailed] = useState(false)
  const [submitFailed, setSubmitFailed] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    let alive = true
    api.getReadinessAssessment(slug)
      .then((a) => alive && setAssessment(a))
      .catch(() => alive && setLoadFailed(true))
    return () => {
      alive = false
    }
  }, [slug])

  async function submit() {
    setSubmitting(true)
    setSubmitFailed(false)
    try {
      const graded = await api.submitReadinessAssessment(slug, answers)
      setResult(graded)
      onResult(graded.readiness)
    } catch {
      setSubmitFailed(true)
    }
    setSubmitting(false)
  }

  const answered = Object.keys(answers).length
  const total = assessment?.question_count ?? 0

  return (
    <Card className="space-y-4 p-5" aria-label={t('rd.check.title')}>
      <h2 className="ui-card-title">{t('rd.check.title')}</h2>

      {loadFailed ? (
        <p role="alert" className="text-sm text-rose">{t('rd.check.loadError')}</p>
      ) : !assessment ? (
        <div className="flex justify-center py-6"><Spinner announce /></div>
      ) : result ? (
        <div className="space-y-3">
          <p className="text-sm text-bright">
            {t('rd.check.result')}: {tf('rd.check.score', { c: result.correct_count, n: result.question_count })}
          </p>
          {Object.keys(result.skill_results).length > 0 && (
            <div className="space-y-1">
              <p className="text-xs font-medium uppercase tracking-widest text-soft">{t('rd.check.bySkill')}</p>
              <ul className="space-y-1 text-sm text-soft">
                {[...result.readiness.strengths, ...result.readiness.gaps]
                  .filter((s) => s.skill.slug in result.skill_results)
                  .map((s) => (
                    <li key={s.skill.slug}>
                      <LearningLabel parts={skillLabel(s.skill, ctx)} /> — {Math.round(result.skill_results[s.skill.slug] * 100)}%
                    </li>
                  ))}
              </ul>
            </div>
          )}
          <Button variant="ghost" size="sm" onClick={onClose}>{t('rd.check.close')}</Button>
        </div>
      ) : assessment.questions.length === 0 ? (
        <>
          <p className="text-sm text-soft">{t('rd.check.unavailable')}</p>
          <Button variant="ghost" size="sm" onClick={onClose}>{t('rd.check.close')}</Button>
        </>
      ) : (
        <>
          <p className="text-xs text-soft">
            {tf('rd.check.intro', { n: assessment.question_count, m: assessment.estimated_minutes })}
          </p>
          <ol className="space-y-5">
            {assessment.questions.map((q, qi) => {
              const name = `${groupId}-${qi}`
              const options = language === 'ar' && q.options_ar?.length === q.options.length ? q.options_ar : q.options
              return (
                <li key={q.id}>
                  <fieldset>
                    <legend className="mb-2 text-sm text-bright" dir="auto">
                      {qi + 1}. {pick(q.question, q.question_ar, language)}
                    </legend>
                    <div className="space-y-1.5">
                      {options.map((option, oi) => {
                        const checked = answers[q.id] === oi
                        return (
                          <label
                            key={oi}
                            className={cn(
                              'flex min-h-[44px] cursor-pointer items-start gap-2 rounded-md border px-3 py-2 text-sm lg:min-h-0',
                              checked ? 'border-amber/50 bg-amber/10 text-bright' : 'border-border text-soft hover:border-muted'
                            )}
                          >
                            <input
                              type="radio"
                              name={name}
                              checked={checked}
                              onChange={() => setAnswers((prev) => ({ ...prev, [q.id]: oi }))}
                              className="mt-1"
                            />
                            <span dir="auto">{option}</span>
                          </label>
                        )
                      })}
                    </div>
                  </fieldset>
                </li>
              )
            })}
          </ol>
          {submitFailed && <p role="alert" className="text-sm text-rose">{t('rd.check.submitError')}</p>}
          <div className="flex flex-wrap items-center justify-between gap-3">
            <p className="text-xs text-soft" aria-live="polite">{tf('rd.check.answered', { a: answered, n: total })}</p>
            <div className="flex gap-2">
              <Button variant="ghost" size="sm" onClick={onClose}>{t('common.close')}</Button>
              <Button size="sm" loading={submitting} disabled={answered < total} onClick={() => void submit()}>
                {submitting ? t('rd.check.submitting') : t('rd.check.submit')}
              </Button>
            </div>
          </div>
        </>
      )}
    </Card>
  )
}
