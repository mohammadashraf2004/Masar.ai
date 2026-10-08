import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { mentorV2 } from '@/lib/api'
import { HintLadder } from './HintLadder'
import { resetMentorMock } from './mock'
import type { MentorBlock } from './types'

const first: Extract<MentorBlock, { kind: 'hint' }> = { kind: 'hint', grounding: 'lesson', level: 1, label: 'Conceptual nudge', text: 'What decides which conversation resumes?' }

beforeEach(() => resetMentorMock())
afterEach(() => vi.restoreAllMocks())

describe('HintLadder', () => {
  it('starts at level 1 of 4 with the first dot wide', () => {
    render(<HintLadder exerciseId="9007" first={first} />)
    expect(screen.getByText('HINT')).toBeInTheDocument()
    expect(screen.getByText('Level 1 of 4')).toBeInTheDocument()
    const dots = screen.getAllByTestId('hint-dot')
    expect(dots.map((d) => d.className.includes('w-[18px]'))).toEqual([true, false, false, false])
  })

  it('stacks clearer hints, and offers the solution only at level 3', async () => {
    const hint = vi.spyOn(mentorV2, 'hint')
    render(<HintLadder exerciseId="9007" first={first} />)
    await userEvent.click(screen.getByRole('button', { name: 'A clearer hint' }))
    expect(await screen.findByTestId('hint-level-2')).toBeInTheDocument()
    expect(screen.getByTestId('hint-level-1')).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: 'A clearer hint' }))
    expect(await screen.findByTestId('hint-level-3')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'A clearer hint' })).toBeNull()
    expect(screen.getByRole('button', { name: 'Show the solution' })).toBeInTheDocument()
    expect(hint.mock.calls.map(([body]) => body.level)).toEqual([2, 3])
  })

  it('never asks for the solution until the learner confirms, and can back out', async () => {
    const hint = vi.spyOn(mentorV2, 'hint')
    render(<HintLadder exerciseId="9007" first={first} />)
    await userEvent.click(screen.getByRole('button', { name: 'A clearer hint' }))
    await screen.findByTestId('hint-level-2')
    await userEvent.click(screen.getByRole('button', { name: 'A clearer hint' }))
    await screen.findByTestId('hint-level-3')

    await userEvent.click(screen.getByRole('button', { name: 'Show the solution' }))
    const strip = screen.getByRole('alertdialog')
    expect(within(strip).getByText(/half reward \(\+20 instead of \+40\)/)).toBeInTheDocument()
    expect(hint.mock.calls.some(([body]) => body.level === 4)).toBe(false)

    await userEvent.click(within(strip).getByRole('button', { name: 'I will try myself' }))
    expect(screen.queryByRole('alertdialog')).toBeNull()
    expect(hint.mock.calls.some(([body]) => body.level === 4)).toBe(false)

    await userEvent.click(screen.getByRole('button', { name: 'Show the solution' }))
    await userEvent.click(within(screen.getByRole('alertdialog')).getByRole('button', { name: 'Show the solution' }))
    expect(await screen.findByTestId('hint-level-4')).toBeInTheDocument()
    expect(hint).toHaveBeenLastCalledWith(expect.objectContaining({ exerciseId: '9007', level: 4, confirm: true }), 'en')
    expect(screen.getByText('Level 4 of 4')).toBeInTheDocument()
  })

  it('reports each further reply, so the conversation keeps what it cost', async () => {
    const onReveal = vi.fn()
    render(<HintLadder exerciseId="9007" first={first} onReveal={onReveal} />)
    await userEvent.click(screen.getByRole('button', { name: 'A clearer hint' }))
    await screen.findByTestId('hint-level-2')
    expect(onReveal).toHaveBeenCalledWith(expect.objectContaining({ creditCost: 2 }))
  })

  it('says the provider failed and the charge was refunded, and keeps the ladder', async () => {
    vi.spyOn(mentorV2, 'hint').mockRejectedValueOnce(new Error('down'))
    render(<HintLadder exerciseId="9007" first={first} />)
    await userEvent.click(screen.getByRole('button', { name: 'A clearer hint' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Any charge was refunded')
    expect(screen.getByTestId('hint-level-1')).toBeInTheDocument()
  })
})
