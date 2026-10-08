'use client'

import { ListChecks } from 'lucide-react'
import { DifficultyBadge } from '@/components/ui/index'
import { MarkdownLesson } from '@/components/ui/MarkdownLesson'
import { pickText } from '@/lib/content-language'
import { useI18n } from '@/lib/i18n'
import { runExerciseTests, showExerciseSolution, submitExercise } from '@/lib/api'
// [mentor-v2]
import { mentorV2Enabled } from '@/features/mentor/flag'
// [/mentor-v2]
import type { Exercise } from '@/types'
import { CodeCell } from './CodeCell/CodeCell'
import { exerciseFiles, memorySaverImportLine } from './lessonExerciseFiles'

export function LessonCodeExercise({
  exercise,
  index,
  total,
  onPassed,
}: {
  exercise: Exercise
  index: number
  total: number
  onPassed: () => void
}) {
  const { t, language } = useI18n()
  const title = pickText(exercise.title, exercise.title_ar, language)
  const brief = pickText(exercise.description, exercise.description_ar, language)
  const files = exerciseFiles(exercise)
  const codeLanguage = exercise.language ?? 'python'
  const runtimes: Record<string, string> = {
    bash: 'Shell',
    dockerfile: 'Dockerfile',
    hcl: 'Terraform HCL',
    ini: 'Configuration',
    python: 'Python 3.12',
    sparql: 'SPARQL',
    sql: 'SQL',
    yaml: 'YAML',
  }
  const runtime = runtimes[codeLanguage] ?? codeLanguage
  const counter = total > 1 ? `${t('exercise.label')} ${index + 1} ${t('exercise.of')} ${total}` : t('exercise.label')

  return (
    <div className="min-w-0 space-y-4">
      <section className="overflow-hidden rounded-xl border border-border bg-panel">
        <div className="border-b border-border px-5 pb-3.5 pt-4">
          <div className="mb-1.5 flex items-start justify-between gap-3">
            <span className="font-mono text-lc-label uppercase tracking-wider text-ghost">{counter}</span>
            <DifficultyBadge level={exercise.difficulty} />
          </div>
          <h2 className="font-display text-base font-bold leading-snug text-bright" dir={title.shownIn === 'ar' ? 'rtl' : 'ltr'}>{title.text}</h2>
        </div>
        <div className="px-5 py-4">
          <div className="mb-2.5 flex items-center gap-1.5 text-amber-text">
            <ListChecks size={13} />
            <span className="text-lc-label font-medium uppercase tracking-wider">{t('exercise.task')}</span>
          </div>
          <MarkdownLesson content={brief.text} dir={brief.shownIn === 'ar' ? 'rtl' : 'ltr'} compact />
        </div>
      </section>

      <CodeCell
        key={exercise.id}
        exerciseId={exercise.id}
        files={files}
        runtime={runtime}
        language={codeLanguage}
        highlightLines={memorySaverImportLine(files)}
        onRunTests={currentFiles => runExerciseTests(exercise.id, currentFiles)}
        onSubmit={currentFiles => submitExercise(exercise.id, currentFiles)}
        onPassed={onPassed}
        gradingAvailable={exercise.grading_available !== false}
        hint={language === 'ar' ? exercise.hint_ar ?? exercise.hint : exercise.hint}
        onShowSolution={exercise.grading_available !== false ? () => showExerciseSolution(exercise.id) : undefined}
        // [mentor-v2]
        reviewHref={mentorV2Enabled() ? `/mentor?tab=review&exerciseId=${exercise.id}` : undefined}
        // [/mentor-v2]
      />
    </div>
  )
}
