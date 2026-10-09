'use client'

import type { ReactNode } from 'react'
import { Flag, ListChecks, ListOrdered, Lightbulb, Target } from 'lucide-react'
import { MarkdownLesson } from '@/components/ui/MarkdownLesson'
import { useExerciseI18n, useI18n } from '@/lib/i18n'

/** The sections an exercise brief is authored in, in either language. A brief
 * opens with its goal, then `**Instructions**`, `**Expected output**` and an
 * optional `**Think about it**`; any other bold heading (acceptance criteria,
 * hints in older briefs) stays inside the section it appears in. */
const HEADINGS: Record<string, BriefPart> = {
  instructions: 'steps',
  'التعليمات': 'steps',
  'expected output': 'expected',
  'المخرَج المتوقع': 'expected',
  'المخرج المتوقع': 'expected',
  'think about it': 'reflect',
  'فكّر في الأمر': 'reflect',
  'فكر في الأمر': 'reflect',
}

type BriefPart = 'goal' | 'steps' | 'expected' | 'reflect'

export function splitBrief(markdown: string): Record<BriefPart, string> {
  const parts: Record<BriefPart, string[]> = { goal: [], steps: [], expected: [], reflect: [] }
  let current: BriefPart = 'goal'
  for (const line of markdown.split('\n')) {
    const heading = /^\*\*(.+?)\*\*\s*$/.exec(line.trim())
    const part = heading ? HEADINGS[heading[1].trim().toLowerCase()] ?? HEADINGS[heading[1].trim()] : undefined
    if (part) {
      current = part
      continue
    }
    parts[current].push(line)
  }
  return {
    goal: parts.goal.join('\n').trim(),
    steps: parts.steps.join('\n').trim(),
    expected: parts.expected.join('\n').trim(),
    reflect: parts.reflect.join('\n').trim(),
  }
}

/** One exercise brief as labelled sections: what you will achieve, the steps,
 * what to produce and an optional ungraded reflection. Works for guided code
 * exercises and written ones alike, so every exercise reads the same way. */
export function ExerciseBrief({ content, dir }: { content: string; dir: 'ltr' | 'rtl' }) {
  const tx = useExerciseI18n()
  const { t } = useI18n()
  const brief = splitBrief(content)
  // A brief without any recognised heading is shown whole, as before.
  if (!brief.steps && !brief.expected && !brief.reflect) {
    return (
      <div dir={dir}>
        <BriefSection icon={<ListChecks size={13} />} label={t('exercise.task')}>
          <MarkdownLesson content={content} dir={dir} compact />
        </BriefSection>
      </div>
    )
  }
  return (
    <div className="space-y-4" dir={dir}>
      {brief.goal && (
        <BriefSection icon={<Target size={13} />} label={tx.brief.goal}>
          <MarkdownLesson content={brief.goal} dir={dir} compact />
        </BriefSection>
      )}
      {brief.steps && (
        <BriefSection icon={<ListOrdered size={13} />} label={tx.brief.steps}>
          <MarkdownLesson content={brief.steps} dir={dir} compact />
        </BriefSection>
      )}
      {brief.expected && (
        <BriefSection icon={<Flag size={13} />} label={tx.brief.expected}>
          <MarkdownLesson content={brief.expected} dir={dir} compact />
        </BriefSection>
      )}
      {brief.reflect && (
        <BriefSection icon={<Lightbulb size={13} />} label={tx.brief.reflect} note={tx.brief.notGraded}>
          <MarkdownLesson content={brief.reflect} dir={dir} compact />
        </BriefSection>
      )}
    </div>
  )
}

function BriefSection({ icon, label, note, children }: { icon: ReactNode; label: string; note?: string; children: ReactNode }) {
  return (
    <section>
      <div className="mb-1.5 flex items-center gap-1.5 text-amber-text">
        {icon}
        <h3 className="text-lc-label font-medium uppercase tracking-wider">{label}</h3>
        {note && <span className="text-lc-label text-ghost">· {note}</span>}
      </div>
      {children}
    </section>
  )
}
