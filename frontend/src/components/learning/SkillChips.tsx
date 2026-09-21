'use client'
import { skillLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { Skill } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'

const TONE = {
  neutral: 'border-border bg-surface text-soft',
  /** A skill the learner already has: the same sky as "Already know" on the roadmap. */
  known: 'border-sky/20 bg-sky/5 text-sky',
} as const

interface SkillChipsProps {
  skills: Skill[]
  tone?: keyof typeof TONE
  /** Show only the first `max` and end the list with "+N". */
  max?: number
  className?: string
}

/**
 * A wrapping row of skill names — the one way a course card, the catalogue and
 * "Why this course?" all draw a list of skills, so they cannot drift apart.
 */
export function SkillChips({ skills, tone = 'neutral', max, className }: SkillChipsProps) {
  const ctx = useLabelContext()
  const shown = max === undefined ? skills : skills.slice(0, max)
  const more = skills.length - shown.length
  return (
    <ul className={cn('flex flex-wrap gap-1.5', className)}>
      {shown.map((s) => (
        <li key={s.slug} className={cn('rounded border px-1.5 py-0.5 text-xs', TONE[tone])}>
          <LearningLabel parts={skillLabel(s, ctx)} />
        </li>
      ))}
      {more > 0 && <li className="px-1 py-0.5 text-xs text-dim">+{more}</li>}
    </ul>
  )
}
