'use client'

import { useCallback, useState } from 'react'
import type { ExerciseFile, ExerciseRunResult, GradeResult } from '@/types'

export type ExerciseRunStatus = 'idle' | 'running' | 'done' | 'error'
export type ExerciseRunAction = 'tests' | 'submit'

/** The code a result belongs to, so the cell can tell when the learner has
 *  edited it since (a "Correct" must not appear to describe newer code). */
export function filesSignature(files: ExerciseFile[]) {
  return files.map(file => `${file.name}\u0000${file.content}`).join('\u0001')
}

export function useExerciseRun({
  onRunTests,
  onSubmit,
  describeError,
}: {
  onRunTests: (files: ExerciseFile[]) => Promise<ExerciseRunResult>
  onSubmit: (files: ExerciseFile[]) => Promise<GradeResult>
  /** Turns a failed request (busy, offline, signed out) into a message the
   *  learner can act on; without it the raw error message is shown. */
  describeError?: (cause: unknown, action: ExerciseRunAction) => string
}) {
  const [status, setStatus] = useState<ExerciseRunStatus>('idle')
  const [action, setAction] = useState<ExerciseRunAction | null>(null)
  const [execution, setExecution] = useState<ExerciseRunResult | GradeResult | null>(null)
  const [grade, setGrade] = useState<GradeResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [resultFor, setResultFor] = useState<string | null>(null)

  const failure = useCallback((cause: unknown, failed: ExerciseRunAction) => {
    if (describeError) return describeError(cause, failed)
    if (cause instanceof Error) return cause.message
    return failed === 'tests' ? 'Could not run the tests.' : 'Could not submit the exercise.'
  }, [describeError])

  const runTests = useCallback(async (files: ExerciseFile[]) => {
    setStatus('running')
    setAction('tests')
    setError(null)
    try {
      const nextExecution = await onRunTests(files)
      setExecution(nextExecution)
      setGrade(null)
      setResultFor(filesSignature(files))
      setStatus('done')
    } catch (cause) {
      setError(failure(cause, 'tests'))
      setStatus('error')
    } finally {
      setAction(null)
    }
  }, [onRunTests, failure])

  // Resolves with the grade (null when submitting failed), so the caller can
  // react to this submission in its own handler rather than in an effect.
  const submit = useCallback(async (files: ExerciseFile[]): Promise<GradeResult | null> => {
    setStatus('running')
    setAction('submit')
    setError(null)
    try {
      const nextGrade = await onSubmit(files)
      setGrade(nextGrade)
      setExecution(nextGrade)
      setResultFor(filesSignature(files))
      setStatus('done')
      return nextGrade
    } catch (cause) {
      setError(failure(cause, 'submit'))
      setStatus('error')
      return null
    } finally {
      setAction(null)
    }
  }, [onSubmit, failure])

  /** Forget the last result (for example after "Reset to starter code"). */
  const clear = useCallback(() => {
    setStatus('idle')
    setExecution(null)
    setGrade(null)
    setError(null)
    setResultFor(null)
  }, [])

  return { status, action, execution, grade, error, resultFor, runTests, submit, clear }
}
