import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { QuickOnboarding } from '@/components/learning/QuickOnboarding'
import { STRINGS } from '@/lib/i18n'
import { useLanguageStore } from '@/lib/language'
import { FIELDS } from '@/test/fixtures'

vi.mock('@/lib/api', () => ({ api: { saveMyLearningProfile: vi.fn() } }))
import { api } from '@/lib/api'

const onDone = vi.fn()
const onSkip = vi.fn()

beforeEach(() => {
  vi.mocked(api.saveMyLearningProfile).mockReset()
  vi.mocked(api.saveMyLearningProfile).mockResolvedValue({} as never)
  onDone.mockReset()
  onSkip.mockReset()
})

const setup = () => {
  render(<QuickOnboarding fields={FIELDS} onDone={onDone} onSkip={onSkip} />)
  return userEvent.setup()
}

describe('the short onboarding', () => {
  it('asks three short questions, one step at a time', async () => {
    const user = setup()
    expect(screen.getByText('Step 1 of 3')).toBeInTheDocument()
    expect(screen.getByText(STRINGS.en['qob.prog.q'])).toBeInTheDocument()
    await user.click(screen.getByRole('radio', { name: STRINGS.en['qob.prog.comfortable'] }))
    await user.click(screen.getByRole('button', { name: 'Next' }))
    expect(screen.getByText('Step 2 of 3')).toBeInTheDocument()
    await user.click(screen.getByRole('radio', { name: STRINGS.en['qob.ai.basics'] }))
    await user.click(screen.getByRole('button', { name: 'Next' }))
    expect(screen.getByText(STRINGS.en['qob.interests.q'])).toBeInTheDocument()
    // A career goal is never one of the questions: the only radios were the experience levels.
    expect(screen.queryAllByRole('radio')).toHaveLength(0)
  })

  it('cannot go on without an answer, and can go back', async () => {
    const user = setup()
    expect(screen.getByRole('button', { name: 'Next' })).toBeDisabled()
    await user.click(screen.getByRole('radio', { name: STRINGS.en['qob.prog.none'] }))
    await user.click(screen.getByRole('button', { name: 'Next' }))
    await user.click(screen.getByRole('button', { name: 'Back' }))
    expect(screen.getByRole('radio', { name: STRINGS.en['qob.prog.none'] })).toHaveAttribute('aria-checked', 'true')
  })

  it('saves the plain choices, and only those, then finishes', async () => {
    const user = setup()
    await user.click(screen.getByRole('radio', { name: STRINGS.en['qob.prog.basic'] }))
    await user.click(screen.getByRole('button', { name: 'Next' }))
    await user.click(screen.getByRole('radio', { name: STRINGS.en['qob.ai.projects'] }))
    await user.click(screen.getByRole('button', { name: 'Next' }))
    expect(screen.getByRole('button', { name: 'Finish' })).toBeDisabled()
    await user.click(screen.getByRole('checkbox', { name: /NLP/ }))
    await user.click(screen.getByRole('button', { name: 'Finish' }))
    expect(api.saveMyLearningProfile).toHaveBeenCalledWith({
      programming_experience: 'basic', ai_experience: 'projects', fields: ['nlp'],
    })
    expect(onDone).toHaveBeenCalledTimes(1)
  })

  it('shows an error and stays put when saving fails', async () => {
    vi.mocked(api.saveMyLearningProfile).mockRejectedValue(new Error('down'))
    const user = setup()
    await user.click(screen.getByRole('radio', { name: STRINGS.en['qob.prog.none'] }))
    await user.click(screen.getByRole('button', { name: 'Next' }))
    await user.click(screen.getByRole('radio', { name: STRINGS.en['qob.ai.none'] }))
    await user.click(screen.getByRole('button', { name: 'Next' }))
    await user.click(screen.getByRole('checkbox', { name: /NLP/ }))
    await user.click(screen.getByRole('button', { name: 'Finish' }))
    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.en['qob.saveError'])
    expect(onDone).not.toHaveBeenCalled()
  })

  it('can be skipped without saving anything', async () => {
    const user = setup()
    await user.click(screen.getByRole('button', { name: STRINGS.en['qob.skip'] }))
    expect(onSkip).toHaveBeenCalled()
    expect(api.saveMyLearningProfile).not.toHaveBeenCalled()
  })

  it('is in Arabic for an Arabic reader', () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    setup()
    expect(screen.getByText(STRINGS.ar['qob.prog.q'])).toBeInTheDocument()
    expect(screen.getByRole('radio', { name: STRINGS.ar['qob.prog.none'] })).toBeInTheDocument()
  })
})
