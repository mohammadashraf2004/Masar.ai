import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useLanguageStore } from '@/lib/language'
import type { ExerciseAttemptState, ExerciseFile, GradeResult } from '@/types'
import { CodeCell } from './CodeCell'

const FILES: ExerciseFile[] = [
  { name: 'main.py', content: 'scores = [3, 4, 5]\n# Step 1: add them up\ntotal = ___\n' },
]

function grade(overrides: Partial<GradeResult>): GradeResult {
  return {
    status: 'incorrect', passed: false, stdout: '', stderr: '', execution_time_ms: 2,
    tests_passed: 0, tests_total: 2,
    feedback: { code: 'TEST_FAILED', message: 'The total should be 12.', messages: { en: 'The total should be 12.' } },
    ...overrides,
  }
}

function state(overrides: Partial<ExerciseAttemptState>): ExerciseAttemptState {
  return {
    failed_checks: 0, passed: false, completed_independently: false,
    solution_viewed: false, solution_available: false, checks_until_solution: 3,
    ...overrides,
  }
}

function Guided({ onSubmit, onShowSolution, onLoadAttemptState }: {
  onSubmit?: (files: ExerciseFile[]) => Promise<GradeResult>
  onShowSolution?: () => Promise<string>
  onLoadAttemptState?: () => Promise<ExerciseAttemptState>
}) {
  return (
    <CodeCell
      exerciseId={41}
      files={FILES}
      runtime="Python 3.12"
      onRunTests={vi.fn()}
      onSubmit={onSubmit ?? vi.fn().mockResolvedValue(grade({}))}
      onShowSolution={onShowSolution}
      onLoadAttemptState={onLoadAttemptState}
      hint={'Python has a built-in that adds a list.\n\nIt is called `sum`.\n\nWrite `sum(scores)`.'}
    />
  )
}

beforeEach(() => {
  window.localStorage.clear()
  useLanguageStore.setState({ language: 'en', mode: 'arabic_first', annotateTerms: true })
})

describe('CodeCell guided practice', () => {
  it('loads the starter with its blanks and step comments', async () => {
    render(<Guided />)
    expect(await screen.findByRole('textbox', { name: 'main.py' })).toHaveValue(FILES[0].content)
    expect(screen.getByRole('button', { name: 'Run Code' })).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Check Answer' })).toBeEnabled()
  })

  it('reveals hints one rung at a time and can hide them again', async () => {
    render(<Guided />)
    await userEvent.click(screen.getByRole('button', { name: 'Hint' }))
    const note = screen.getByRole('note')
    expect(note).toHaveTextContent('Hint 1 of 3')
    expect(note).toHaveTextContent('built-in that adds a list')
    expect(note).not.toHaveTextContent('sum(scores)')

    await userEvent.click(screen.getByRole('button', { name: 'Next hint' }))
    expect(screen.getByRole('note')).toHaveTextContent('Hint 2 of 3')
    await userEvent.click(screen.getByRole('button', { name: 'Next hint' }))
    expect(screen.getByRole('note')).toHaveTextContent('sum(scores)')
    expect(screen.queryByRole('button', { name: 'Next hint' })).toBeNull()

    await userEvent.click(screen.getByRole('button', { name: 'Hide hints' }))
    expect(screen.queryByRole('note')).toBeNull()
    expect(screen.getByRole('button', { name: 'Hint' })).toBeInTheDocument()
  })

  it('gives feedback, then a more specific hint, then the worked solution after three different answers', async () => {
    const onShowSolution = vi.fn().mockResolvedValue('total = sum(scores)')
    const onSubmit = vi.fn()
      .mockResolvedValueOnce(grade({ attempt: state({ failed_checks: 1, checks_until_solution: 2 }) }))
      .mockResolvedValueOnce(grade({ attempt: state({ failed_checks: 2, checks_until_solution: 1 }) }))
      .mockResolvedValueOnce(grade({ attempt: state({ failed_checks: 3, solution_available: true, checks_until_solution: 0 }) }))
    render(<Guided onSubmit={onSubmit} onShowSolution={onShowSolution} />)
    expect(screen.queryByRole('button', { name: 'Show Solution' })).toBeNull()
    expect(screen.getByText('3 different answers unlock the worked solution. Hints are open any time.')).toBeInTheDocument()

    // First wrong answer: feedback only.
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    expect(await screen.findByText('The total should be 12.')).toBeInTheDocument()
    expect(screen.queryByRole('note')).toBeNull()
    expect(screen.getByText('Two more different answers unlock the worked solution.')).toBeInTheDocument()

    // Second: the next, more specific hint opens by itself.
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    await screen.findByText('One more different answer unlocks the worked solution.')
    expect(screen.getByRole('note')).toHaveTextContent('Hint 2 of 3')
    expect(screen.getByRole('note')).not.toHaveTextContent('sum(scores)')

    // Third: the solution is offered (and the last hint).
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    await userEvent.click(await screen.findByRole('button', { name: 'Show Solution' }))
    expect(await screen.findByText('total = sum(scores)')).toBeInTheDocument()
    expect(onShowSolution).toHaveBeenCalledOnce()
  })

  it('restores solution access from the server after a reload', async () => {
    const onLoadAttemptState = vi.fn().mockResolvedValue(state({ failed_checks: 3, solution_available: true, checks_until_solution: 0 }))
    render(<Guided onShowSolution={vi.fn().mockResolvedValue('total = sum(scores)')} onLoadAttemptState={onLoadAttemptState} />)
    expect(await screen.findByRole('button', { name: 'Show Solution' })).toBeInTheDocument()
    expect(onLoadAttemptState).toHaveBeenCalledOnce()
  })

  it('says when a pass came after viewing the solution', async () => {
    render(<Guided
      onShowSolution={vi.fn().mockResolvedValue('total = sum(scores)')}
      onSubmit={vi.fn().mockResolvedValue(grade({
        status: 'correct', passed: true, tests_passed: 2,
        feedback: { code: 'CORRECT', message: 'Well done.', messages: {} },
        attempt: state({ passed: true, solution_viewed: true, solution_available: true, checks_until_solution: 0 }),
      }))}
    />)
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    expect(await screen.findByText(/Completed with help from the worked solution/)).toBeInTheDocument()
  })

  it.each([
    [grade({ feedback: { code: 'BLANKS_REMAINING', message: 'One blank (`___`) is still empty.', messages: {} } }), 'Blanks to fill', false],
    [grade({ status: 'syntax_error', feedback: { code: 'SYNTAX_ERROR', message: 'Python could not read your code.', messages: {} } }), 'Syntax error', false],
    [grade({ status: 'runtime_error', feedback: { code: 'RUNTIME_ERROR', message: 'Your code stopped with an error.', messages: {} } }), 'Runtime error', false],
    [grade({ status: 'timeout', feedback: { code: 'TIMEOUT', message: 'Your code took too long.', messages: {} } }), 'Time limit reached', false],
    [grade({ tests_passed: 1 }), 'Not quite yet', true],
  ])('names the kind of result (%#) and asks for another try', async (result, label, scored) => {
    render(<Guided onSubmit={vi.fn().mockResolvedValue(result)} />)
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    const card = (await screen.findByText(label)).closest('section') as HTMLElement
    expect(within(card).getByText(result.feedback.message)).toBeInTheDocument()
    expect(within(card).getByText('Fix this and check again. Your code is saved as you type.')).toBeInTheDocument()
    // A score only means something when the code actually ran to the checks.
    expect(within(card).queryByText(/\/ 2 tests/) !== null).toBe(scored)
  })

  it('celebrates a correct answer with its score and the success message', async () => {
    render(<Guided onSubmit={vi.fn().mockResolvedValue(grade({
      status: 'correct', passed: true, tests_passed: 2, tests_total: 2,
      feedback: { code: 'CORRECT', message: 'You added the scores with sum().', messages: {} },
    }))} />)
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    const card = (await screen.findByText('Correct')).closest('section') as HTMLElement
    expect(within(card).getByText('2 / 2 tests')).toBeInTheDocument()
    expect(within(card).getByText('You added the scores with sum().')).toBeInTheDocument()
    expect(within(card).queryByText(/check again/)).toBeNull()
  })

  it('shows partial credit as its own result with the checks that pass', async () => {
    render(<Guided onSubmit={vi.fn().mockResolvedValue(grade({ status: 'partial', tests_passed: 1 }))} />)
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    const card = (await screen.findByText('Partly correct')).closest('section') as HTMLElement
    expect(within(card).getByText('1 / 2 tests')).toBeInTheDocument()
    expect(within(card).getByText('Fix this and check again. Your code is saved as you type.')).toBeInTheDocument()
  })

  it.each([
    ['execution_error', 'The project runner is unavailable. Your answer was not graded and this attempt does not count.'],
    ['grading_error', 'This exercise cannot be checked right now because of a problem on our side.'],
  ] as const)('never presents a %s as a wrong answer', async (status, message) => {
    render(<Guided onSubmit={vi.fn().mockResolvedValue(grade({ status, feedback: { code: status.toUpperCase(), message, messages: {} } }))} />)
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    const card = (await screen.findByText('Not graded')).closest('section') as HTMLElement
    expect(within(card).getByText(message)).toBeInTheDocument()
    expect(within(card).getByText('This attempt was not counted. Try again in a moment.')).toBeInTheDocument()
    expect(within(card).queryByText(/check again/)).toBeNull()
    expect(within(card).queryByText(/tests/)).toBeNull()
  })

  it('names resource limits', async () => {
    render(<Guided onSubmit={vi.fn().mockResolvedValue(grade({ status: 'memory_limit', feedback: { code: 'MEMORY_LIMIT', message: 'Too much memory.', messages: {} } }))} />)
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    expect(await screen.findByText('Memory limit reached')).toBeInTheDocument()
  })

  it('marks a result stale once the code changes, and reset clears it', async () => {
    render(<Guided onSubmit={vi.fn().mockResolvedValue(grade({
      status: 'correct', passed: true, tests_passed: 2, tests_total: 2,
      feedback: { code: 'CORRECT', message: 'Well done.', messages: {} },
    }))} />)
    const stale = 'You have changed the code since this result. Check again to grade the new version.'
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    expect(await screen.findByText('Well done.')).toBeInTheDocument()
    expect(screen.queryByText(stale)).toBeNull()
    await userEvent.type(screen.getByRole('textbox', { name: 'main.py' }), '# edit')
    expect(screen.getByText(stale)).toBeInTheDocument()
    // The menu toggle and the menu item share the label; the item opens second.
    await userEvent.click(screen.getByRole('button', { name: 'Reset to starter code' }))
    const [, item] = screen.getAllByRole('button', { name: 'Reset to starter code' })
    await userEvent.click(item)
    expect(screen.queryByText('Well done.')).toBeNull()
    expect(screen.queryByText(stale)).toBeNull()
  })

  it.each([
    ['en', { response: { status: 429 } }, 'You are checking very quickly. Wait a few seconds, then try again.'],
    ['en', new Error('Network Error'), 'Could not reach the checker. Nothing was graded; try again in a moment.'],
    ['ar', { response: { status: 503 } }, 'تعذّر الوصول إلى أداة التحقق. لم يُقيَّم شيء؛ حاول مرة أخرى بعد قليل.'],
  ] as const)('explains a failed request in the interface language (%s)', async (language, cause, message) => {
    useLanguageStore.setState({ language })
    render(<Guided onSubmit={vi.fn().mockRejectedValue(cause)} />)
    await userEvent.click(screen.getByRole('button', { name: language === 'ar' ? 'تحقّق من الإجابة' : 'Check Answer' }))
    expect(await screen.findByRole('alert')).toHaveTextContent(message)
  })

  it('keeps the traceback of a checked answer behind Technical details', async () => {
    render(<Guided onSubmit={vi.fn().mockResolvedValue(grade({
      status: 'runtime_error', stderr: ['Traceback (most recent call last):', 'ZeroDivisionError: division by zero'].join('\n'),
      feedback: { code: 'RUNTIME_ERROR', message: 'Blank 2: divide must refuse a zero divisor.', messages: {} },
    }))} />)
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    await screen.findByText('Blank 2: divide must refuse a zero divisor.')
    const details = screen.getByText('Technical details').closest('details') as HTMLDetailsElement
    expect(details).not.toHaveAttribute('open')
    expect(within(details).getByText(/ZeroDivisionError/)).toBeInTheDocument()
  })

  it('speaks Arabic around unchanged code', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<Guided />)
    expect(await screen.findByRole('textbox', { name: 'main.py' })).toHaveValue(FILES[0].content)
    await userEvent.click(screen.getByRole('button', { name: 'تلميح' }))
    expect(screen.getByRole('note')).toHaveTextContent('تلميح 1 من 3')
    await userEvent.click(screen.getByRole('button', { name: 'التلميح التالي' }))
    expect(screen.getByRole('note')).toHaveTextContent('تلميح 2 من 3')
    await userEvent.click(screen.getByRole('button', { name: 'تحقّق من الإجابة' }))
    expect(await screen.findByText('ليست صحيحة بعد')).toBeInTheDocument()
  })
})
