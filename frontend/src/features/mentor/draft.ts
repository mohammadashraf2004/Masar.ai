import { EXERCISE_FILE_NAMES, exerciseFileName } from '@/features/exercises/lessonExerciseFiles'

/**
 * What the learner has written in an exercise's editor, as the editor saved it in this browser
 * (CodeCell keeps the latest edit under `exercise:<id>:<file>`). Null when they have not edited
 * it: the caller then uses the starter, never a placeholder.
 */
export function exerciseDraft(exerciseId: string | number, language?: string | null): string | null {
  if (typeof window === 'undefined') return null
  const names = language ? [exerciseFileName(language)] : Object.keys(EXERCISE_FILE_NAMES).map((key) => EXERCISE_FILE_NAMES[key]).concat('solution.txt')
  try {
    for (const name of names) {
      const saved = window.localStorage.getItem(`exercise:${exerciseId}:${name}`)
      if (saved !== null) return saved
    }
  } catch { /* no storage */ }
  return null
}
