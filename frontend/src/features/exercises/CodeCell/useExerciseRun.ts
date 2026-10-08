'use client'

import { useCallback, useState } from 'react'
import type { ExerciseFile, ExerciseRunResult, GradeResult } from '@/types'

export type ExerciseRunStatus = 'idle' | 'running' | 'done' | 'error'
export type ExerciseRunAction = 'tests' | 'submit'

export function useExerciseRun({
  onRunTests,
  onSubmit,
}: {
  onRunTests: (files: ExerciseFile[]) => Promise<ExerciseRunResult>
  onSubmit: (files: ExerciseFile[]) => Promise<GradeResult>
}) {
  const [status, setStatus] = useState<ExerciseRunStatus>('idle')
  const [action, setAction] = useState<ExerciseRunAction | null>(null)
  const [execution, setExecution] = useState<ExerciseRunResult | GradeResult | null>(null)
  const [grade, setGrade] = useState<GradeResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const runTests = useCallback(async (files: ExerciseFile[]) => {
    setStatus('running')
    setAction('tests')
    setError(null)
    try {
      const nextExecution = await onRunTests(files)
      setExecution(nextExecution)
      setGrade(null)
      setStatus('done')
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Could not run the tests.')
      setStatus('error')
    } finally {
      setAction(null)
    }
  }, [onRunTests])

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
      setStatus('done')
      return nextGrade
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Could not submit the exercise.')
      setStatus('error')
      return null
    } finally {
      setAction(null)
    }
  }, [onSubmit])

  return { status, action, execution, grade, error, runTests, submit }
}
