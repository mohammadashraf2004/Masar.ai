'use client'
import { Code2, ListChecks, PenLine } from 'lucide-react'
import { Badge } from '@/components/ui/index'
import { MarkdownLesson } from '@/components/ui/MarkdownLesson'
import { AnswerChat } from '@/components/ui/AnswerChat'
import { CodeBlock } from '@/components/ui/CodeBlock'
import { useI18n } from '@/lib/i18n'
import { pickText } from '@/lib/content-language'
import { cn } from '@/lib/utils'
import type { Exercise } from '@/types'

/**
 * One exercise, as a brief the student can actually follow.
 *
 * The problem this replaces: the description was rendered as
 * `<p>{ex.description}</p>`. Most briefs in the catalogue are structured
 * markdown — numbered steps, bullets, fenced snippets — and HTML collapses
 * every newline in a `<p>`, so a five-step task arrived as one run-on
 * sentence ("... before moving on to code: 1. Is LangChain an LLM? 2. What
 * is ..."). The steps were there; the shape was gone.
 *
 * So: the brief goes through the same markdown renderer the lessons use
 * (compact scale), and the card is split into labelled sections — what to
 * do, the starter code, where to answer — so the order of operations is
 * visible at a glance instead of inferred from a paragraph.
 *
 * Shared by the track and tool-course readers; they had identical copies of
 * the old markup, and identical bugs in it.
 */
export function ExerciseCard({
  exercise,
  index,
  total,
}: {
  exercise: Exercise
  /** Position in the topic, 0-based — rendered as "Exercise 2 of 4". */
  index?: number
  total?: number
}) {
  const { t, language } = useI18n()

  // Direction follows the text actually shown: an English brief stays LTR
  // even for an Arabic reader, because that is what is on screen.
  const brief = pickText(exercise.description, exercise.description_ar, language)
  const title = pickText(exercise.title, exercise.title_ar, language)

  const hasCode = Boolean(exercise.starter_code)
  const counter =
    index !== undefined && total !== undefined && total > 1
      ? `${t('exercise.label')} ${index + 1} ${t('exercise.of')} ${total}`
      : t('exercise.label')

  return (
    <div className="bg-panel border border-border rounded-lg overflow-hidden">
      {/* ── Header: what this is, how hard, what it tests ── */}
      <div className="px-5 pt-4 pb-3.5 border-b border-border">
        <div className="flex items-start justify-between gap-3 mb-1.5">
          <span className="text-[11px] font-mono text-ghost uppercase tracking-wider">
            {counter}
          </span>
          <Badge variant={exercise.difficulty}>{exercise.difficulty}</Badge>
        </div>

        <h3
          className="font-display font-bold text-bright text-base leading-snug"
          dir={title.shownIn === 'ar' ? 'rtl' : 'ltr'}
        >
          {title.text}
        </h3>

        {exercise.skill_tested.length > 0 && (
          <div className="flex items-center gap-1.5 flex-wrap mt-2.5">
            <span className="text-[11px] text-ghost">{t('exercise.skills')}:</span>
            {exercise.skill_tested.map((skill) => (
              <span
                key={skill}
                className="text-[10px] px-1.5 py-0.5 rounded border border-border bg-muted/40 text-dim font-mono"
                dir="ltr"
              >
                {skill}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* ── The task ── */}
      <Section icon={<ListChecks size={13} />} label={t('exercise.task')}>
        <MarkdownLesson
          content={brief.text}
          dir={brief.shownIn === 'ar' ? 'rtl' : 'ltr'}
          compact
        />
      </Section>

      {/* ── Starter code, if the exercise scaffolds one ── */}
      {hasCode && (
        <Section icon={<Code2 size={13} />} label={t('exercise.starterCode')}>
          <CodeBlock code={exercise.starter_code!} language="python" />
        </Section>
      )}

      {/* ── Where to answer ── */}
      <Section icon={<PenLine size={13} />} label={t('exercise.yourAnswer')} last>
        <AnswerChat
          target={{ kind: 'exercise', id: exercise.id }}
          isCode={hasCode}
          starterCode={exercise.starter_code}
        />
      </Section>
    </div>
  )
}

/** A labelled band inside the card. The label is what makes the order of
 *  operations readable — task, then scaffold, then answer. */
function Section({
  icon,
  label,
  children,
  last,
}: {
  icon: React.ReactNode
  label: string
  children: React.ReactNode
  last?: boolean
}) {
  return (
    <div className={cn('px-5 py-4', !last && 'border-b border-border')}>
      <div className="flex items-center gap-1.5 mb-2.5 text-amber">
        {icon}
        <span className="text-[11px] font-medium uppercase tracking-wider">{label}</span>
      </div>
      {children}
    </div>
  )
}
