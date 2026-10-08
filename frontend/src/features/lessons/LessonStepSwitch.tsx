import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import type { LessonStep } from './useLessonScrollSteps'

/** The "١ المحتوى / ٢ التمرين" pill switch. Purely a controlled view — the
 *  scrolling and the IntersectionObserver that keeps `active` in sync with
 *  scroll position both live in `useLessonScrollSteps`. */
export function LessonStepSwitch({
  active,
  hasExercise,
  onSelect,
}: {
  active: LessonStep
  hasExercise: boolean
  onSelect: (step: LessonStep) => void
}) {
  const { t } = useI18n()
  if (!hasExercise) return null

  return (
    <div
      role="group"
      aria-label={t('lessons.navigation')}
      className="inline-flex max-w-full items-center gap-1 overflow-x-auto rounded-full border border-border bg-panel/90 p-1"
    >
      <Pill selected={active === 'content'} onClick={() => onSelect('content')}>
        {t('lessons.stepContent')}
      </Pill>
      <Pill selected={active === 'exercise'} onClick={() => onSelect('exercise')}>
        {t('lessons.stepExercise')}
      </Pill>
    </div>
  )
}

function Pill({ selected, onClick, children }: { selected: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={selected}
      className={cn(
        'h-9 shrink-0 rounded-full px-4 text-sm font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring',
        selected
          ? 'bg-amber-soft text-amber-text shadow-[inset_0_0_0_1px_rgb(var(--acc)/0.35)]'
          : 'text-dim hover:bg-surface hover:text-bright',
      )}
    >
      {children}
    </button>
  )
}
