import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useLanguageStore } from '@/lib/language'
import type { Exercise } from '@/types'
import { LessonCodeExercise } from './LessonCodeExercise'

vi.mock('@/lib/api', async importOriginal => {
  const actual = await importOriginal<typeof import('@/lib/api')>()
  return {
    ...actual,
    runExerciseTests: vi.fn(),
    submitExercise: vi.fn(),
    showExerciseSolution: vi.fn(),
  }
})

beforeEach(() => {
  useLanguageStore.setState({ language: 'en', mode: 'arabic_first', annotateTerms: true })
})

describe('LessonCodeExercise', () => {
  it('renders pending shell exercises as editable cells without grading controls', async () => {
    const exercise: Exercise = {
      id: 73,
      title: 'Build a clean commit',
      description: 'Write the commands used to create the commit.',
      difficulty: 'beginner',
      skill_tested: ['git'],
      exercise_type: 'code_pending',
      language: 'bash',
      starter_code: '# TODO: enter the commands\n',
      grading_available: false,
    }

    render(
      <LessonCodeExercise
        exercise={exercise}
        index={0}
        total={1}
        onPassed={vi.fn()}
      />,
    )

    expect(await screen.findByRole('textbox', { name: 'solution.sh' })).toHaveValue('# TODO: enter the commands\n')
    expect(screen.getByText('Shell')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Submit Answer' })).toBeDisabled()
    expect(screen.queryByRole('button', { name: 'Show solution' })).toBeNull()
  })
})
