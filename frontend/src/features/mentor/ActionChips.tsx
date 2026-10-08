'use client'
import { useMentorV2I18n, type MentorV2Key } from '@/lib/i18n'
import { cn } from '@/lib/utils'
import type { MentorIntent } from './types'

/** The seven things the learner can ask for. A chosen one is sent as `intent`, and the server prefers it to its own guess. */
export const ACTIONS: { key: 'explain' | 'simplify' | 'hint' | 'socratic' | 'quiz' | 'practice' | 'review'; intent: MentorIntent }[] = [
  { key: 'explain', intent: 'EXPLAIN' },
  { key: 'simplify', intent: 'SIMPLIFY' },
  { key: 'hint', intent: 'HINT' },
  { key: 'socratic', intent: 'SOCRATIC' },
  { key: 'quiz', intent: 'QUIZ' },
  { key: 'practice', intent: 'PRACTICE' },
  { key: 'review', intent: 'REVIEW' },
]

/** The intents that can be sent with nothing typed: they act on what the mentor already sees. */
export const NEEDS_NO_TEXT: readonly MentorIntent[] = ['HINT', 'QUIZ', 'REVIEW']

export function placeholderKey(intent: MentorIntent | null): MentorV2Key {
  const found = ACTIONS.find((a) => a.intent === intent)
  return (found ? `mentor.v2.placeholder.${found.key}` : 'mentor.v2.placeholder.default') as MentorV2Key
}

export function ActionChips({
  selected,
  disabled,
  onSelect,
}: {
  selected: MentorIntent | null
  disabled?: boolean
  onSelect: (intent: MentorIntent | null) => void
}) {
  const { t } = useMentorV2I18n()
  return (
    <div
      role="group"
      aria-label={t('mentor.v2.actions.label')}
      className="flex gap-2 overflow-x-auto px-3.5 pb-2.5 pt-1 [scrollbar-width:none]"
    >
      {ACTIONS.map(({ key, intent }) => {
        const on = selected === intent
        return (
          <button
            key={key}
            type="button"
            aria-pressed={on}
            disabled={disabled}
            onClick={() => onSelect(on ? null : intent)}
            className={cn(
              'min-h-[40px] shrink-0 whitespace-nowrap rounded-full border px-3.5 text-xs transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-40 lg:min-h-[32px]',
              on ? 'border-amber bg-amber-soft font-semibold text-amber-text' : 'border-border text-dim hover:border-amber/40 hover:text-bright',
            )}
          >
            {t(`mentor.v2.actions.${key}` as MentorV2Key)}
          </button>
        )
      })}
    </div>
  )
}
