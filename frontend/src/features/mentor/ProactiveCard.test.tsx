import { act, render, screen, within } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import { useLanguageStore } from '@/lib/language'
import { ProactiveCard } from './MentorMessageView'
import { mockControl, mockProactive, resetMentorMock } from './mock'
import type { MentorMessageV2 } from './types'

function card(): MentorMessageV2 {
  mockControl.now = () => 0
  const message = mockProactive('en')
  if (!message) throw new Error('the mock proactive card was not offered')
  return message
}

beforeEach(() => {
  resetMentorMock()
  useLanguageStore.setState({ language: 'en' })
})

describe('ProactiveCard follows the UI language', () => {
  it('words the trigger from its code, in whichever language is active', async () => {
    render(<ProactiveCard message={card()} />)
    const view = screen.getByTestId('proactive-card')
    expect(within(view).getByText('You just finished a lesson')).toBeInTheDocument()

    await act(async () => { useLanguageStore.setState({ language: 'ar' }) })
    expect(within(view).getByText('أنهيت درساً للتو')).toBeInTheDocument()
    expect(within(view).queryByText('You just finished a lesson')).toBeNull()
  })

  it('shows the live server’s code as a sentence, not as lesson_completed', () => {
    render(<ProactiveCard message={{ ...card(), proactive: { trigger: 'lesson_completed' } }} />)
    expect(screen.queryByText('lesson_completed')).toBeNull()
  })

  it('shows a trigger this build does not know exactly as sent', () => {
    render(<ProactiveCard message={{ ...card(), proactive: { trigger: 'streak_broken' } }} />)
    expect(screen.getByText('streak_broken')).toBeInTheDocument()
  })

  it('re-asks its quiz question in the new language, so the whole card follows', async () => {
    render(<ProactiveCard message={card()} />) // an English quiz block
    expect(screen.getByText('What makes the agent resume the same conversation on a new call?')).toBeInTheDocument()

    await act(async () => { useLanguageStore.setState({ language: 'ar' }) })
    expect(await screen.findByText('ما الذي يجعل الوكيل يستأنف نفس المحادثة عند استدعاء جديد؟')).toBeInTheDocument()
  })
})
