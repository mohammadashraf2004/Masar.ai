'use client'
import { useEffect, useRef, useState } from 'react'
import { mentorV2 } from '@/lib/api'
import { useMentorV2I18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'
import type { MentorBlock, QuizAnswerResult } from './types'

type QuizData = Extract<MentorBlock, { kind: 'quiz' }>
type Lang = 'ar' | 'en'
type Shown = Pick<QuizData, 'question' | 'options'>

/**
 * A multiple-choice question in a mentor message. The answer is never in the block: picking an
 * option asks the server (`/mentor/quiz/answer`), and what comes back is feedback, not a key. A
 * wrong pick says the guiding question and offers "try again"; it never shows which option was
 * right. A right pick shows the confirmation and the skill's movement, in mono.
 *
 * The question follows the UI language. A block records the language it was written in (`lang`);
 * when the learner switches to another one, the same question is asked for again in the new
 * language (free, nothing recorded) and replaces the text in place. Option ids are the same in
 * every language, so a pick means the same thing either way. If the translation cannot be had,
 * the question stays as it was and still works.
 *
 * `renderFeedback` draws the server's feedback blocks (text and a small check question); the chat
 * and the lesson panel pass the same message renderer so feedback looks like any mentor reply.
 */
export function QuizBlock({
  block,
  onResult,
  renderFeedback,
}: {
  block: QuizData
  onResult?: (result: QuizAnswerResult) => void
  renderFeedback: (blocks: MentorBlock[]) => React.ReactNode
}) {
  const { t, language } = useMentorV2I18n()
  const [picked, setPicked] = useState<string | null>(null)
  const [result, setResult] = useState<QuizAnswerResult | null>(null)
  const [busy, setBusy] = useState(false)
  const [failed, setFailed] = useState(false)
  // The question in each language other than the block's own, as the server returned it.
  const [others, setOthers] = useState<Partial<Record<Lang, Shown>>>({})
  // The language the feedback on screen was written in.
  const answeredIn = useRef<Lang | null>(null)

  const needsOther = block.lang !== undefined && block.lang !== language
  const shown: Shown = (needsOther ? others[language] : undefined) ?? block

  useEffect(() => {
    if (!needsOther || others[language]) return
    let alive = true
    mentorV2.quiz(block.quizId, language).then(
      (fresh) => { if (alive) setOthers((prev) => ({ ...prev, [language]: { question: fresh.question, options: fresh.options } })) },
      () => { /* keep the question as it is: it is still answerable */ },
    )
    return () => { alive = false }
  }, [block.quizId, language, needsOther, others])

  // A wrong answer's feedback quotes the question. Once the language changes it would be a
  // sentence in one language about a question in another, so the learner is offered the retry.
  useEffect(() => {
    if (result && !result.correct && answeredIn.current !== language) {
      setPicked(null)
      setResult(null)
    }
  }, [language, result])

  async function pick(optionId: string) {
    if (busy || result) return
    setPicked(optionId)
    setBusy(true)
    setFailed(false)
    try {
      const answer = await mentorV2.answerQuiz({ quizId: block.quizId, optionId }, language)
      answeredIn.current = language
      setResult(answer)
      onResult?.(answer)
    } catch {
      setFailed(true)
      setPicked(null)
    } finally {
      setBusy(false)
    }
  }

  function retry() {
    setPicked(null)
    setResult(null)
  }

  return (
    <div className="flex flex-col gap-2.5" data-testid="quiz-block">
      <span dir="ltr" className="ui-eyebrow font-mono">{t('mentor.v2.quiz.label')}</span>
      <p dir="auto" className="text-sm font-medium leading-[1.7] text-white">{shown.question}</p>
      <ul role="radiogroup" aria-label={shown.question} className="flex flex-col gap-2">
        {shown.options.map((option, i) => {
          const isPicked = picked === option.id
          const right = isPicked && result?.correct === true
          const wrong = isPicked && result?.correct === false
          return (
            <li key={option.id}>
              <button
                type="button"
                role="radio"
                aria-checked={isPicked}
                disabled={busy || result !== null}
                onClick={() => void pick(option.id)}
                data-state={right ? 'right' : wrong ? 'wrong' : isPicked ? 'picked' : 'idle'}
                className={cn(
                  'flex min-h-[44px] w-full items-center gap-3 rounded-lg border px-3 py-2 text-start text-[13px] transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring',
                  right ? 'border-emerald bg-emerald/10 text-white'
                    : wrong ? 'border-rose bg-rose/10 text-white'
                    : isPicked ? 'border-amber bg-amber text-on-amber'
                    : 'border-border bg-surface text-bright hover:border-amber/40',
                )}
              >
                <span dir="ltr" aria-hidden="true" className="grid h-6 w-6 shrink-0 place-items-center rounded-md border border-border font-mono text-xs text-dim">
                  {String.fromCharCode(65 + i)}
                </span>
                <span dir="auto" className="min-w-0 flex-1">{option.text}</span>
              </button>
            </li>
          )
        })}
      </ul>

      {failed && <p role="alert" className="text-xs text-rose">{t('mentor.v2.failedNoCharge')}</p>}

      {result?.correct && (
        <div role="status" className="flex flex-col gap-1.5 text-sm text-bright">
          {renderFeedback(result.feedback)}
          {result.skillDelta && (
            <span dir="ltr" className="self-start font-mono text-xs text-emerald">
              {result.skillDelta.skill} {result.skillDelta.from} → {result.skillDelta.to}
            </span>
          )}
        </div>
      )}

      {result && !result.correct && (
        <div role="status" className="flex flex-col gap-2 rounded-lg border border-rose/40 bg-void p-3 text-sm text-bright">
          {renderFeedback(result.feedback)}
          <button
            type="button"
            onClick={retry}
            className="min-h-[44px] self-start rounded-lg border border-border px-3 text-[13px] text-bright hover:border-amber/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
          >
            {t('mentor.v2.quiz.retry')}
          </button>
        </div>
      )}
    </div>
  )
}
