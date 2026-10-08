'use client'
import { X } from 'lucide-react'
import { useMentorV2I18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'

/**
 * What the mentor can see for the next message, as removable chips under the chat header: the
 * lesson, and the exercise's code. What is on is what the request carries as `context`; remove both
 * and the mentor answers in general. The default (the learner's last active lesson) is the
 * server's, so the labels come from the caller.
 */
export function ContextBar({
  lessonLabel,
  codeLabel,
  lessonOn,
  codeOn,
  onToggleLesson,
  onToggleCode,
  onRestore,
}: {
  lessonLabel: string | null
  codeLabel: string | null
  lessonOn: boolean
  codeOn: boolean
  onToggleLesson: (on: boolean) => void
  onToggleCode: (on: boolean) => void
  onRestore: () => void
}) {
  const { t, tf } = useMentorV2I18n()
  const showLesson = lessonOn && lessonLabel !== null
  const showCode = codeOn && codeLabel !== null
  const anyAvailable = lessonLabel !== null || codeLabel !== null
  const removed = (lessonLabel !== null && !lessonOn) || (codeLabel !== null && !codeOn)

  const chip = 'inline-flex min-h-[44px] max-w-full items-center gap-1.5 rounded-full border ps-3 pe-1 text-xs lg:min-h-[28px]'
  const remove = 'grid h-9 w-9 shrink-0 place-items-center rounded-full text-dim hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring lg:h-6 lg:w-6'

  return (
    <div data-testid="context-bar" className="flex flex-wrap items-center gap-x-2 gap-y-1.5 border-b border-border bg-panel px-[18px] py-2">
      <span className="text-xs text-dim">{t('mentor.v2.sees')}</span>

      {showLesson && (
        <span data-chip="lesson" className={cn(chip, 'border-amber bg-amber-soft text-amber-text')}>
          <span dir="auto" className="min-w-0 truncate">{lessonLabel}</span>
          <button type="button" aria-label={tf('mentor.v2.remove', { name: lessonLabel ?? '' })} onClick={() => onToggleLesson(false)} className={remove}>
            <X size={12} aria-hidden="true" />
          </button>
        </span>
      )}

      {showCode && (
        <span data-chip="code" dir="ltr" className={cn(chip, 'border-border bg-surface font-mono text-bright')}>
          <span className="min-w-0 truncate">{codeLabel}</span>
          <button type="button" aria-label={tf('mentor.v2.remove', { name: codeLabel ?? '' })} onClick={() => onToggleCode(false)} className={remove}>
            <X size={12} aria-hidden="true" />
          </button>
        </span>
      )}

      {!showLesson && !showCode && <span className="min-w-0 flex-1 text-xs text-ghost">{t('mentor.v2.nothingAttached')}</span>}

      {anyAvailable && removed && (
        <button
          type="button"
          onClick={onRestore}
          className="min-h-[44px] rounded-md px-2 text-xs font-medium text-amber-text hover:text-amber-text2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring lg:min-h-0 lg:py-1"
        >
          {t('mentor.v2.attach')}
        </button>
      )}
    </div>
  )
}
