import { describe, expect, it } from 'vitest'
import type { Exercise } from '@/types'
import { exerciseFileName, exerciseFiles, pythonFileLabel } from './lessonExerciseFiles'

const exercise = (overrides: Partial<Exercise>): Exercise => ({
  id: 5, title: 'Scale Training and Test Data Correctly', description: '', difficulty: 'beginner',
  skill_tested: [], exercise_type: 'code', language: 'python', starter_code: 'x = ___\n',
  ...overrides,
} as Exercise)

describe('exercise file names', () => {
  it('labels a Python file after its exercise', () => {
    expect(pythonFileLabel('Scale Training and Test Data Correctly')).toBe('scale_training_test.py')
    expect(pythonFileLabel('Build and Inspect a NumPy Data Pipeline')).toBe('build_inspect_numpy.py')
    expect(pythonFileLabel('3D Tensors')).toBe('_3d_tensors.py')
    expect(pythonFileLabel('The')).toBe('main.py')
  })

  it('keeps the storage name, so drafts saved under agent.py still load', () => {
    const [file] = exerciseFiles(exercise({}))
    // CodeCell keys every saved draft by `name`, never by the label, and the
    // mentor's code review reads drafts by the same language file name.
    expect(file).toMatchObject({ name: 'agent.py', label: 'scale_training_test.py' })
    expect(file.name).toBe(exerciseFileName('python'))
  })

  it('leaves configuration files under their conventional names', () => {
    const [file] = exerciseFiles(exercise({ language: 'dockerfile', title: 'Write a Dockerfile' }))
    expect(file).toMatchObject({ name: 'Dockerfile', label: undefined })
  })
})
