'use client'
import { useState } from 'react'
import { MentorCodeBlock } from '@/components/mentor/MentorCodeBlock'
import { mentorV2 } from '@/lib/api'
import { useMentorV2I18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'
import { exerciseDraft } from './draft'
import { mentorV2Live } from './flag'
import type { MentorBlock, MentorMessageV2 } from './types'

type HintData = Extract<MentorBlock, { kind: 'hint' }>

/**
 * Progressive hints for an exercise: a nudge, a direction, detailed guidance, and only then the
 * solution. Levels 1-3 are mentor replies about the real exercise and the learner's current draft;
 * the solution (level 4) is the exercise's own reference solution, only ever requested after the
 * learner confirms - viewing it is recorded on the exercise. Without an exercise there is no ladder
 * to climb: the hint is shown on its own.
 */
export function HintLadder({
  exerciseId,
  first,
  onReveal,
}: {
  exerciseId: string
  first: HintData
  /** Each further reply, so the conversation can keep it (and the credits it cost). */
  onReveal?: (message: MentorMessageV2) => void
}) {
  const { t, tf, n, language } = useMentorV2I18n()
  const [levels, setLevels] = useState<HintData[]>([first])
  const [confirming, setConfirming] = useState(false)
  const [busy, setBusy] = useState(false)
  const [failed, setFailed] = useState(false)
  const current = levels[levels.length - 1].level

  async function reveal(level: 2 | 3 | 4, confirm = false) {
    setBusy(true)
    setFailed(false)
    try {
      const message = await mentorV2.hint({
        exerciseId, level, code: exerciseDraft(exerciseId), ...(confirm ? { confirm: true } : {}),
      }, language)
      const block = message.blocks.find((b): b is HintData => b.kind === 'hint')
      if (block) setLevels((prev) => [...prev, block])
      setConfirming(false)
      onReveal?.(message)
    } catch {
      setFailed(true)
    } finally {
      setBusy(false)
    }
  }

  const btn = 'min-h-[44px] rounded-lg border px-3.5 text-[13px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-40'

  return (
    <div className="flex flex-col gap-3" data-testid="hint-ladder">
      <div className="flex items-center gap-3">
        <span dir="ltr" className="ui-eyebrow ui-eyebrow-accent font-mono">{t('mentor.v2.hint.label')}</span>
        <span className="text-xs text-dim">{tf('mentor.v2.hint.level', { n: n(current) })}</span>
        <span aria-hidden="true" className="ms-auto flex items-center gap-1">
          {[1, 2, 3, 4].map((level) => (
            <span
              key={level}
              data-testid="hint-dot"
              className={cn('h-2 rounded-full transition-all', level === current ? 'w-[18px] bg-amber' : level < current ? 'w-2 bg-amber/60' : 'w-2 bg-muted')}
            />
          ))}
        </span>
      </div>

      {levels.map((hint) => (
        <div key={hint.level} className="flex flex-col gap-1.5 border-s-2 border-amber/50 ps-3" data-testid={`hint-level-${hint.level}`}>
          <span className="text-xs font-semibold text-amber-text">{hint.label}</span>
          <p dir="auto" className="text-sm leading-[1.75] text-bright">{hint.text}</p>
          {hint.code && <MentorCodeBlock code={hint.code} lang="python" />}
        </div>
      ))}

      {failed && <p role="alert" className="text-xs text-rose">{t('mentor.v2.failedNoCharge')}</p>}

      {exerciseId && current < 3 && (
        <button type="button" disabled={busy} onClick={() => void reveal((current + 1) as 2 | 3)} className={cn(btn, 'self-start border-border text-bright hover:border-amber/40')}>
          {t('mentor.v2.hint.clearer')}
        </button>
      )}

      {exerciseId && current === 3 && !confirming && (
        <button type="button" disabled={busy} onClick={() => setConfirming(true)} className={cn(btn, 'self-start border-border text-bright hover:border-amber/40')}>
          {t('mentor.v2.hint.showSolution')}
        </button>
      )}

      {confirming && (
        <div role="alertdialog" aria-label={t('mentor.v2.hint.showSolution')} className="flex flex-col gap-2.5 rounded-lg border border-amber p-3.5">
          <p className="text-[13px] leading-[1.7] text-bright">{t(mentorV2Live() ? 'mentor.v2.hint.confirmLive' : 'mentor.v2.hint.confirm')}</p>
          <div className="flex flex-wrap gap-2">
            <button type="button" disabled={busy} onClick={() => void reveal(4, true)} className={cn(btn, 'border-amber bg-amber font-semibold text-on-amber')}>
              {t('mentor.v2.hint.confirmYes')}
            </button>
            <button type="button" disabled={busy} onClick={() => setConfirming(false)} className={cn(btn, 'border-border text-bright')}>
              {t('mentor.v2.hint.confirmNo')}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
