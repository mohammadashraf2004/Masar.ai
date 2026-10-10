import Link from 'next/link'
import { Card } from '@/components/ui/index'
import { buttonStyles } from '@/components/ui/Button'
import { LessonCodeExercise } from '@/features/exercises/LessonCodeExercise'
import { ExerciseCard } from '@/components/ui/ExerciseCard'
import { useI18n } from '@/lib/i18n'
import type { Exercise } from '@/types'

type LessonExercisesProps = {
  courseSlug: string
  exercises: Exercise[]
  indexOffset?: number
  total?: number
  onPassed(exercise: Exercise): void
}

/** Exercises canonically owned by one lesson. The caller does the lesson-id
 * filtering; this component only renders the resulting interactive practice. */
export function LessonExercises({
  courseSlug,
  exercises,
  indexOffset = 0,
  total = exercises.length,
  onPassed,
}: LessonExercisesProps) {
  const { t } = useI18n()
  if (exercises.length === 0) return null

  return (
    <section aria-labelledby="lesson-practice-heading" className="max-w-[760px] space-y-5">
      <div className="space-y-1">
        <h2 id="lesson-practice-heading" className="ui-section-title">
          {t('lessons.practiceExercises')}
        </h2>
        <p className="ui-description">{t('lessons.practiceDescription')}</p>
      </div>

      {exercises.map((exercise, offset) => (
        exercise.is_locked ? (
          <Card key={exercise.id} className="space-y-3 p-8 text-center">
            <p className="text-sm font-medium text-bright">{t('lessons.purchaseToUnlock')}</p>
            <Link
              href={`/courses/${exercise.course_slug ?? courseSlug}`}
              className={buttonStyles({ variant: 'ghost', size: 'sm' })}
            >
              {t('nav.explore')}
            </Link>
          </Card>
        ) : (
          exercise.exercise_type === 'code' || exercise.starter_code ? (
            <LessonCodeExercise
              key={exercise.id}
              exercise={exercise}
              index={indexOffset + offset}
              total={total}
              onPassed={() => onPassed(exercise)}
            />
          ) : (
            <ExerciseCard
              key={exercise.id}
              exercise={exercise}
              index={indexOffset + offset}
              total={total}
              onResult={correct => { if (correct) onPassed(exercise) }}
            />
          )
        )
      ))}
    </section>
  )
}
