import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useLanguageStore } from '@/lib/language'
import type { ExerciseFile } from '@/types'
import { CodeCell } from './CodeCell'

const FILES: ExerciseFile[] = [
  { name: 'agent.py', content: 'from langgraph.checkpoint.memory import MemorySaver\n\ngraph = builder.compile()\n' },
  { name: 'tests.py', content: 'def test_agent():\n    assert True\n', readOnly: true },
]

beforeEach(() => {
  window.localStorage.clear()
  useLanguageStore.setState({ language: 'en', mode: 'arabic_first', annotateTerms: true })
})

describe('CodeCell', () => {
  it('keeps and restores drafts while hiding private test files', async () => {
    // An unversioned draft from the previous free-form starter must not hide
    // a newly published fill-in-the-blank scaffold.
    window.localStorage.setItem('exercise:anon:7:agent.py', 'stale = True\n')
    const first = render(<Cell />)

    const agent = await screen.findByRole('textbox', { name: 'agent.py' })
    await waitFor(() => expect(agent).toHaveValue(FILES[0].content))
    fireEvent.change(agent, { target: { value: 'edited = True\n' } })
    expect(window.localStorage.getItem('exercise:anon:7:agent.py')).toBe('edited = True\n')
    first.unmount()

    render(<Cell />)
    await waitFor(() => expect(screen.getByRole('textbox', { name: 'agent.py' })).toHaveValue('edited = True\n'))

    expect(screen.queryByRole('tab', { name: 'tests.py' })).toBeNull()
    expect(screen.queryByRole('textbox', { name: /tests\.py/ })).toBeNull()
    expect(screen.getByRole('textbox', { name: 'agent.py' })).toHaveValue('edited = True\n')
  })

  it('supports shortcuts and reset to starter code', async () => {
    const onRunTests = vi.fn().mockResolvedValue({ status: 'success', stdout: 'ok\n', stderr: '', execution_time_ms: 2 })
    const onSubmit = vi.fn().mockResolvedValue({ status: 'correct', passed: true, stdout: '', stderr: '', execution_time_ms: 3, tests_passed: 2, tests_total: 2, feedback: { code: 'CORRECT', message: 'Done', messages: { en: 'Done' } } })
    render(<Cell onRunTests={onRunTests} onSubmit={onSubmit} />)
    const editor = await screen.findByRole('textbox', { name: 'agent.py' })
    fireEvent.keyDown(editor, { key: 'Enter', ctrlKey: true })
    await waitFor(() => expect(onRunTests).toHaveBeenCalledOnce())
    expect(onRunTests.mock.calls[0][0].map((file: ExerciseFile) => file.name)).toEqual(['agent.py', 'tests.py'])
    fireEvent.keyDown(editor, { key: 'Enter', ctrlKey: true, shiftKey: true })
    await waitFor(() => expect(onSubmit).toHaveBeenCalledOnce())

    fireEvent.change(editor, { target: { value: 'changed\n' } })
    await userEvent.click(screen.getByRole('button', { name: 'Reset to starter code' }))
    await userEvent.click(screen.getAllByRole('button', { name: 'Reset to starter code' })[1])
    expect(screen.getByRole('textbox', { name: 'agent.py' })).toHaveValue(FILES[0].content)
    expect(window.localStorage.getItem('exercise:anon:7:agent.py')).toBeNull()
  })

  it('runs code without grading and renders stdout, syntax errors, and runtime errors in the console', async () => {
    const onRunTests = vi.fn()
      .mockResolvedValueOnce({ status: 'success', stdout: 'hello\n', stderr: '', execution_time_ms: 2 })
      .mockResolvedValueOnce({ status: 'syntax_error', stdout: '', stderr: 'SyntaxError: invalid syntax', execution_time_ms: 1 })
      .mockResolvedValueOnce({ status: 'runtime_error', stdout: '', stderr: 'RuntimeError: boom', execution_time_ms: 1 })
    const onSubmit = vi.fn()
    render(<Cell onRunTests={onRunTests} onSubmit={onSubmit} />)

    await userEvent.click(screen.getByRole('button', { name: 'Run Code' }))
    expect(await screen.findByText('hello')).toBeInTheDocument()
    expect(onSubmit).not.toHaveBeenCalled()

    await userEvent.click(screen.getByRole('button', { name: 'Run Code' }))
    expect(await screen.findByText('SyntaxError: invalid syntax')).toHaveClass('text-rose-300')

    await userEvent.click(screen.getByRole('button', { name: 'Run Code' }))
    expect(await screen.findByText('RuntimeError: boom')).toHaveClass('text-rose-300')
  })

  it('shows targeted grading feedback, hint, solution, and Arabic controls', async () => {
    useLanguageStore.setState({ language: 'ar' })
    const onSubmit = vi.fn().mockResolvedValue({
      status: 'incorrect', passed: false, stdout: '', stderr: '', execution_time_ms: 2,
      tests_passed: 1, tests_total: 4, failed_test: 'round_called',
      feedback: { code: 'REQUIRED_FUNCTION_MISSING', message: 'استخدم round() كما هو مطلوب.', test_id: 'round_called', messages: { en: 'Use round().', ar: 'استخدم round() كما هو مطلوب.' } },
      // The third different wrong answer: the server now allows the solution.
      attempt: {
        failed_checks: 3, passed: false, completed_independently: false,
        solution_viewed: false, solution_available: true, checks_until_solution: 0,
      },
    })
    const solution = vi.fn().mockResolvedValue('result = round(value, 2)')
    render(
      <CodeCell
        exerciseId={7} files={FILES} runtime="Python 3.12"
        onRunTests={vi.fn()} onSubmit={onSubmit}
        hint="استخدم round(value, digits)." onShowSolution={solution}
      />,
    )

    await userEvent.click(screen.getByRole('button', { name: 'تحقّق من الإجابة' }))
    expect(await screen.findByText('استخدم round() كما هو مطلوب.')).toBeInTheDocument()
    // Repeated wrong answers open the hint without being asked.
    expect(screen.getByRole('note')).toHaveTextContent('round(value, digits)')
    await userEvent.click(screen.getByRole('button', { name: 'عرض الحل' }))
    expect(await screen.findByText('result = round(value, 2)')).toBeInTheDocument()
    expect(solution).toHaveBeenCalledOnce()

    await userEvent.click(screen.getByRole('button', { name: 'إخفاء الحل' }))
    expect(screen.queryByText('result = round(value, 2)')).toBeNull()

    await userEvent.click(screen.getByRole('button', { name: 'عرض الحل' }))
    expect(screen.getByText('result = round(value, 2)')).toBeInTheDocument()
    expect(solution).toHaveBeenCalledOnce()
  })

  it('reveals the completed solution and explanation automatically after passing', async () => {
    const onSubmit = vi.fn().mockResolvedValue({
      status: 'correct', passed: true, stdout: '', stderr: '', execution_time_ms: 2,
      tests_passed: 4, tests_total: 4,
      feedback: { code: 'CORRECT', message: 'You completed the filtering expression.', messages: { en: 'You completed the filtering expression.' } },
    })
    const onShowSolution = vi.fn().mockResolvedValue('result = rows[rows["active"]]')
    render(
      <CodeCell
        exerciseId={8} files={FILES} runtime="Python 3.12"
        onRunTests={vi.fn()} onSubmit={onSubmit} onShowSolution={onShowSolution}
      />,
    )

    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    expect(await screen.findByText('You completed the filtering expression.')).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Completed solution' })).toBeInTheDocument()
    expect(screen.getByText('result = rows[rows["active"]]')).toBeInTheDocument()
    expect(onShowSolution).toHaveBeenCalledOnce()

    await userEvent.click(screen.getByRole('button', { name: 'Hide Solution' }))
    expect(screen.queryByText('result = rows[rows["active"]]')).toBeNull()
  })

  it('does not carry a revealed solution, or the pass that revealed it, to the next exercise', async () => {
    const onSubmit = vi.fn().mockResolvedValue({
      status: 'correct', passed: true, stdout: '', stderr: '', execution_time_ms: 2,
      tests_passed: 4, tests_total: 4,
      feedback: { code: 'CORRECT', message: 'Passed.', messages: { en: 'Passed.' } },
    })
    const firstSolution = vi.fn().mockResolvedValue('first = "solution"')
    const nextSolution = vi.fn().mockResolvedValue('next = "solution"')
    const { rerender } = render(
      <CodeCell exerciseId={8} files={FILES} runtime="Python 3.12"
        onRunTests={vi.fn()} onSubmit={onSubmit} onShowSolution={firstSolution} />,
    )
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    expect(await screen.findByText('first = "solution"')).toBeInTheDocument()

    rerender(
      <CodeCell exerciseId={9} files={FILES} runtime="Python 3.12"
        onRunTests={vi.fn()} onSubmit={onSubmit} onShowSolution={nextSolution} />,
    )
    await waitFor(() => expect(screen.queryByText('first = "solution"')).toBeNull())
    expect(screen.queryByRole('heading', { name: 'Completed solution' })).toBeNull()
    expect(nextSolution).not.toHaveBeenCalled()

    // Passing the new exercise reveals its own solution.
    await userEvent.click(screen.getByRole('button', { name: 'Check Answer' }))
    expect(await screen.findByText('next = "solution"')).toBeInTheDocument()
    expect(nextSolution).toHaveBeenCalledOnce()
  })

  it('allows running classified code while deterministic grading is pending', async () => {
    const onRunTests = vi.fn().mockResolvedValue({
      status: 'success', stdout: 'draft output\n', stderr: '', execution_time_ms: 2,
    })
    const onSubmit = vi.fn()
    render(<Cell onRunTests={onRunTests} onSubmit={onSubmit} gradingAvailable={false} />)

    expect(screen.getByRole('note')).toHaveTextContent('Deterministic grading')
    expect(screen.getByRole('button', { name: 'Check Answer' })).toBeDisabled()
    await userEvent.click(screen.getByRole('button', { name: 'Run Code' }))
    expect(await screen.findByText('draft output')).toBeInTheDocument()
    expect(onSubmit).not.toHaveBeenCalled()
  })
})

function Cell({
  onRunTests = vi.fn().mockResolvedValue({ status: 'success', stdout: '', stderr: '', execution_time_ms: 1 }),
  onSubmit = vi.fn().mockResolvedValue({ status: 'incorrect', passed: false, stdout: '', stderr: '', execution_time_ms: 1, tests_passed: 0, tests_total: 1, feedback: { code: 'TEST_FAILED', message: '', messages: {} } }),
  gradingAvailable = true,
}: {
  onRunTests?: (files: ExerciseFile[]) => Promise<import('@/types').ExerciseRunResult>
  onSubmit?: (files: ExerciseFile[]) => Promise<import('@/types').GradeResult>
  gradingAvailable?: boolean
}) {
  return (
    <CodeCell
      exerciseId={7}
      files={FILES}
      runtime="Python 3.12"
      highlightLines={[1]}
      onRunTests={onRunTests}
      onSubmit={onSubmit}
      gradingAvailable={gradingAvailable}
    />
  )
}
