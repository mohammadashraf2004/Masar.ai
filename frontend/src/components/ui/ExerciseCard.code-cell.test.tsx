import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useLanguageStore } from '@/lib/language'
import type { Exercise } from '@/types'
import { ExerciseCard } from './ExerciseCard'

vi.mock('@/components/ui/AnswerChat', () => ({
  AnswerChat: () => <div data-testid="written-answer">Written answer</div>,
}))

vi.mock('@/lib/api', async importOriginal => {
  const actual = await importOriginal<typeof import('@/lib/api')>()
  return { ...actual, runExerciseTests: vi.fn(), submitExercise: vi.fn() }
})

const exercise = (overrides: Partial<Exercise> = {}): Exercise => ({
  id: 42,
  title: 'Complete the function',
  description: 'Replace the TODO with working Python.',
  difficulty: 'beginner',
  skill_tested: ['python'],
  ...overrides,
})

beforeEach(() => {
  useLanguageStore.setState({ language: 'en', mode: 'arabic_first', annotateTerms: true })
})

describe('ExerciseCard code-cell rollout', () => {
  it('uses CodeCell for coding exercises in every course reader', async () => {
    render(<ExerciseCard exercise={exercise({ starter_code: 'value = None  # TODO\n' })} />)
    expect(await screen.findByRole('textbox', { name: 'agent.py' })).toHaveValue('value = None  # TODO\n')
    expect(screen.queryByRole('tab', { name: 'tests.py' })).toBeNull()
    expect(screen.getByRole('button', { name: 'Run Code' })).toBeInTheDocument()
  })

  it('keeps the written-answer flow when an exercise has no starter code', () => {
    render(<ExerciseCard exercise={exercise()} />)
    expect(screen.getByTestId('written-answer')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Run Code' })).toBeNull()
  })

  it('gives canonical course exercises a blank code cell even without starter code', async () => {
    render(<ExerciseCard exercise={exercise()} forceCodeCell />)
    expect(await screen.findByRole('textbox', { name: 'agent.py' })).toHaveValue('# Write your solution here\n')
    expect(screen.queryByTestId('written-answer')).toBeNull()
  })

  it('uses the correct file name and runtime for configuration exercises', async () => {
    render(<ExerciseCard exercise={exercise({
      exercise_type: 'code',
      language: 'dockerfile',
      starter_code: '# TODO: write the Dockerfile\n',
    })} />)
    expect(await screen.findByRole('textbox', { name: 'Dockerfile' })).toHaveValue('# TODO: write the Dockerfile\n')
    expect(screen.getAllByText('Dockerfile').length).toBeGreaterThanOrEqual(2)
  })
})
