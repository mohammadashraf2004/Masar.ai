'use client'
import { useEffect, useState } from 'react'
import { LogoMark } from '@/components/layout/Logo'
import { MentorBlocks } from '@/features/mentor/MentorMessageView'
import type { QuizAnswerResult } from '@/features/mentor/types'
import { mentorV2 } from '@/lib/api'
import { useMentorV2I18n } from '@/lib/i18n'

/**
 * Under a wrong quiz answer in a lesson: instead of just "wrong", the mentor's guiding question
 * (from `/mentor/quiz/answer`), with its mark and "Mentor · no credits". It never says which option
 * was right, and it renders nothing if the server has nothing to say.
 */
export function MentorQuizNote({ quizId, optionId }: { quizId: string; optionId: string }) {
  const { t, language } = useMentorV2I18n()
  const [result, setResult] = useState<QuizAnswerResult | null>(null)

  useEffect(() => {
    let alive = true
    mentorV2.answerQuiz({ quizId, optionId }, language).then((r) => { if (alive) setResult(r) }, () => {})
    return () => { alive = false }
  }, [quizId, optionId, language])

  if (!result || result.correct) return null

  return (
    <div data-testid="mentor-quiz-note" className="mt-3 flex gap-2.5 rounded-lg border border-border bg-panel p-3">
      <LogoMark size={26} label={null} className="mt-0.5" />
      <div className="flex min-w-0 flex-1 flex-col gap-2 text-[13px] leading-[1.7] text-bright">
        <MentorBlocks blocks={result.feedback} />
        <span className="text-[11px] text-ghost">{t('mentor.v2.quizNote')}</span>
      </div>
    </div>
  )
}
