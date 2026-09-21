import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import MentorPage from '@/app/mentor/page'
import { useLanguageStore } from '@/lib/language'
import { STRINGS } from '@/lib/i18n'

// The AI mentor page. The API is the seam: every request goes through
// `api.*`, so what the page does with a success, a failure, a slow answer and
// a second question is testable without a network or a model.

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: { full_name: 'Amira Hassan' }, isAuthenticated: true, isLoading: false }),
}))
vi.mock('@/components/layout/AppShell', async () => {
  const { createElement } = await import('react')
  return { AppShell: ({ children }: { children: React.ReactNode }) => createElement('div', null, children) }
})
vi.mock('@/components/layout/PageHeader', async () => {
  const { createElement } = await import('react')
  return { PageHeader: ({ title }: { title: string }) => createElement('h1', null, title) }
})
vi.mock('@/lib/api', () => ({
  api: { chat: vi.fn(), reviewCode: vi.fn(), analyzeSkillGap: vi.fn(), getMockInterviewQuestion: vi.fn() },
}))
import { api } from '@/lib/api'

const chat = vi.mocked(api.chat)

/** What axios rejects with for an HTTP error. */
const httpError = (status: number, detail?: unknown) => ({ response: { status, data: { detail } } })

/** A request the test resolves or rejects itself, to observe the in-flight state. */
function deferred<T>() {
  let resolve!: (v: T) => void
  let reject!: (e: unknown) => void
  const promise = new Promise<T>((res, rej) => { resolve = res; reject = rej })
  return { promise, resolve, reject }
}

const reply = (text: string, suggested_actions: string[] = []) => ({ session_id: 1, reply: text, suggested_actions })

const box = () => screen.getByPlaceholderText('Ask your mentor anything…')
const sendButton = () => screen.getByRole('button', { name: STRINGS.en['common.send'] })

async function ask(user: ReturnType<typeof userEvent.setup>, text: string) {
  await user.type(box(), text)
  await user.click(sendButton())
}

beforeEach(() => {
  // jsdom has no layout, so scrollTo does not exist on elements.
  Element.prototype.scrollTo = vi.fn()
})

describe('opening the mentor', () => {
  it('greets the learner and offers an empty, focusable question box', () => {
    render(<MentorPage />)
    expect(screen.getByText(/أنا مرشدك الذكي/)).toBeInTheDocument()
    expect(box()).toHaveValue('')
    // A placeholder is not a name: assistive technology needs a real label.
    expect(screen.getByRole('textbox', { name: STRINGS.en['mentor.input.label'] })).toBe(box())
    expect(sendButton()).toBeEnabled()
    expect(chat).not.toHaveBeenCalled()
  })

  it('does not send an empty or whitespace-only message', async () => {
    const user = userEvent.setup()
    render(<MentorPage />)
    await user.click(sendButton())
    await user.type(box(), '   ')
    await user.click(sendButton())
    expect(chat).not.toHaveBeenCalled()
  })
})

describe('asking a question', () => {
  it('sends the question with the reader’s language settings and shows the answer', async () => {
    chat.mockResolvedValue(reply('RAG retrieves documents first, then generates from them.', ['Quiz me']))
    const user = userEvent.setup()
    render(<MentorPage />)

    await ask(user, 'What is RAG?')

    expect(await screen.findByText(/RAG retrieves documents first/)).toBeInTheDocument()
    expect(chat).toHaveBeenCalledTimes(1)
    expect(chat).toHaveBeenCalledWith('What is RAG?', undefined, { language: 'en', terminology_mode: 'arabic_first' })
    // The question stays on screen, the box is emptied, follow-ups appear.
    expect(screen.getByText('What is RAG?')).toBeInTheDocument()
    expect(box()).toHaveValue('')
    expect(screen.getByRole('button', { name: 'Quiz me' })).toBeInTheDocument()
  })

  it('shows a busy state while waiting and blocks a second send', async () => {
    const pending = deferred<ReturnType<typeof reply>>()
    chat.mockReturnValue(pending.promise)
    const user = userEvent.setup()
    render(<MentorPage />)

    await ask(user, 'Explain RAG simply')

    // In flight: the button is disabled and marked busy, so neither a click
    // nor Enter can start a second request.
    await waitFor(() => expect(sendButton()).toBeDisabled())
    expect(sendButton()).toHaveAttribute('aria-busy', 'true')
    await user.type(box(), 'and another{Enter}')
    await user.click(sendButton())
    expect(chat).toHaveBeenCalledTimes(1)

    await act(async () => { pending.resolve(reply('Simply: look it up, then answer.')) })
    expect(await screen.findByText(/look it up, then answer/)).toBeInTheDocument()
    expect(sendButton()).toBeEnabled()
    expect(sendButton()).not.toHaveAttribute('aria-busy')
  })

  it('sends with Enter, but not Shift+Enter', async () => {
    chat.mockResolvedValue(reply('ok'))
    const user = userEvent.setup()
    render(<MentorPage />)

    await user.type(box(), 'first{Shift>}{Enter}{/Shift}')
    expect(chat).not.toHaveBeenCalled()
    await user.type(box(), '{Enter}')
    await waitFor(() => expect(chat).toHaveBeenCalledTimes(1))
  })

  it('keeps a multi-message conversation in order', async () => {
    chat.mockResolvedValueOnce(reply('It retrieves, then generates.'))
      .mockResolvedValueOnce(reply('Think of it as an open-book exam.'))
    const user = userEvent.setup()
    render(<MentorPage />)

    await ask(user, 'What is RAG?')
    await screen.findByText(/It retrieves, then generates/)
    await ask(user, 'Simpler please')
    await screen.findByText(/open-book exam/)

    const text = document.body.textContent ?? ''
    const order = ['What is RAG?', 'It retrieves, then generates.', 'Simpler please', 'open-book exam']
      .map(s => text.indexOf(s))
    expect(order.every(i => i >= 0)).toBe(true)
    expect([...order].sort((a, b) => a - b)).toEqual(order)
    expect(chat).toHaveBeenCalledTimes(2)
  })

  it('a follow-up chip fills the box for the learner to send', async () => {
    chat.mockResolvedValue(reply('ok', ['Ask me to quiz you']))
    const user = userEvent.setup()
    render(<MentorPage />)
    await ask(user, 'hi')
    await user.click(await screen.findByRole('button', { name: 'Ask me to quiz you' }))
    expect(box()).toHaveValue('Ask me to quiz you')
  })

  it('keeps the conversation when the learner opens another tool and comes back', async () => {
    chat.mockResolvedValue(reply('An answer that must survive.'))
    const user = userEvent.setup()
    render(<MentorPage />)
    await ask(user, 'What is RAG?')
    await screen.findByText(/must survive/)

    await user.click(screen.getByRole('button', { name: /Code review/ }))
    expect(screen.queryByText(/must survive/)).not.toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: /Mentor chat/ }))

    expect(screen.getByText(/must survive/)).toBeInTheDocument()
    expect(screen.getByText('What is RAG?')).toBeInTheDocument()
  })
})

describe('when the mentor fails', () => {
  it('says the mentor is unavailable, hands the question back, and is not stuck loading', async () => {
    chat.mockRejectedValue(httpError(503, 'The mentor is unavailable right now. Your credits were refunded.'))
    const user = userEvent.setup()
    render(<MentorPage />)

    await ask(user, 'What is RAG?')

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent(STRINGS.en['mentor.error.unavailable'])
    // The old text told every learner to "check your API configuration".
    expect(document.body.textContent).not.toMatch(/API configuration/i)
    // Not stuck: the button is live again and the question is back to resend.
    expect(sendButton()).toBeEnabled()
    expect(sendButton()).not.toHaveAttribute('aria-busy')
    expect(box()).toHaveValue('What is RAG?')
  })

  it('lets the learner retry and get an answer after a failure', async () => {
    chat.mockRejectedValueOnce(httpError(503)).mockResolvedValueOnce(reply('RAG: retrieve, then generate.'))
    const user = userEvent.setup()
    render(<MentorPage />)

    await ask(user, 'What is RAG?')
    await screen.findByRole('alert')

    await user.click(sendButton()) // the question was restored — one click
    expect(await screen.findByText(/RAG: retrieve, then generate/)).toBeInTheDocument()
    expect(chat).toHaveBeenCalledTimes(2)
    expect(chat).toHaveBeenLastCalledWith('What is RAG?', undefined, expect.anything())
  })

  it('does not overwrite something the learner has since started typing', async () => {
    const pending = deferred<ReturnType<typeof reply>>()
    chat.mockReturnValue(pending.promise)
    const user = userEvent.setup()
    render(<MentorPage />)

    await ask(user, 'first question')
    await user.type(box(), 'a different thought')
    await act(async () => { pending.reject(httpError(503)) })

    await screen.findByRole('alert')
    expect(box()).toHaveValue('a different thought')
  })

  it.each([
    ['an empty wallet', httpError(402, { error: 'insufficient_credits', message: 'You need 2 credits' }), 'mentor.error.credits'],
    ['an unverified email', httpError(403, { error: 'email_verification_required', message: 'Verify' }), 'mentor.error.verify'],
    ['a rate limit', httpError(429, 'slow down'), 'mentor.error.rateLimit'],
    ['an over-long message', httpError(422, [{ msg: 'too long' }]), 'mentor.error.invalid'],
    ['no connection', { code: 'ECONNABORTED', message: 'timeout of 30000ms exceeded' }, 'mentor.error.network'],
  ] as const)('tells the learner what to do about %s', async (_name, error, key) => {
    chat.mockRejectedValue(error)
    const user = userEvent.setup()
    render(<MentorPage />)

    await ask(user, 'hello')

    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.en[key])
  })

  it('never shows server text, even if a provider error slipped into the response', async () => {
    chat.mockRejectedValue(httpError(500, 'RuntimeError: Incorrect API key sk-LEAK-0123 at api.openai.com'))
    const user = userEvent.setup()
    render(<MentorPage />)

    await ask(user, 'hello')
    await screen.findByRole('alert')
    expect(document.body.textContent).not.toMatch(/sk-LEAK|RuntimeError|api\.openai\.com/)
  })
})

describe('in Arabic', () => {
  beforeEach(() => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
  })

  it('asks the server to answer in Arabic and renders the answer right-to-left', async () => {
    chat.mockResolvedValue(reply('يسترجع المستندات أولاً ثم يولّد الإجابة.'))
    const user = userEvent.setup()
    render(<MentorPage />)

    await user.type(screen.getByPlaceholderText('Ask your mentor anything…'), 'ما هو RAG؟')
    await user.click(screen.getByRole('button', { name: STRINGS.ar['common.send'] }))

    const answer = await screen.findByText(/يسترجع المستندات/)
    expect(answer.closest('[dir]')).toHaveAttribute('dir', 'rtl')
    expect(chat).toHaveBeenCalledWith('ما هو RAG؟', undefined, { language: 'ar', terminology_mode: 'arabic_first' })
  })

  it('labels the message box in Arabic', () => {
    render(<MentorPage />)
    expect(screen.getByRole('textbox', { name: STRINGS.ar['mentor.input.label'] })).toBeInTheDocument()
  })

  it('reports failures in Arabic', async () => {
    chat.mockRejectedValue(httpError(503))
    const user = userEvent.setup()
    render(<MentorPage />)

    await user.type(screen.getByPlaceholderText('Ask your mentor anything…'), 'مرحبا')
    await user.click(screen.getByRole('button', { name: STRINGS.ar['common.send'] }))

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent(STRINGS.ar['mentor.error.unavailable'])
    expect(alert.querySelector('[dir]')).toHaveAttribute('dir', 'rtl')
    expect(alert.textContent).not.toContain(STRINGS.en['mentor.error.unavailable'])
  })
})

describe('the other mentor tools no longer fail silently', () => {
  it('code review', async () => {
    vi.mocked(api.reviewCode).mockRejectedValue(httpError(402, { error: 'insufficient_credits' }))
    const user = userEvent.setup()
    render(<MentorPage />)

    await user.click(screen.getByRole('button', { name: /Code review/ }))
    await user.type(screen.getByPlaceholderText('Paste your code here…'), 'print(1)')
    await user.click(screen.getByRole('button', { name: /Review code/ }))

    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.en['mentor.error.credits'])
    expect(screen.getByRole('button', { name: /Review code/ })).toBeEnabled()
  })

  it('skill gap', async () => {
    vi.mocked(api.analyzeSkillGap).mockRejectedValue(httpError(503))
    const user = userEvent.setup()
    render(<MentorPage />)

    await user.click(screen.getByRole('button', { name: /Skill gap/ }))
    await user.click(screen.getByRole('button', { name: /Analyze skill gap/ }))

    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.en['mentor.error.unavailable'])
    expect(screen.getByRole('button', { name: /Analyze skill gap/ })).toBeEnabled()
  })

  it('mock interview', async () => {
    vi.mocked(api.getMockInterviewQuestion).mockRejectedValue(httpError(403, { error: 'email_verification_required' }))
    const user = userEvent.setup()
    render(<MentorPage />)

    await user.click(screen.getByRole('button', { name: /Mock interview/ }))
    await user.click(screen.getByRole('button', { name: /Start interview/ }))

    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.en['mentor.error.verify'])
    expect(screen.getByRole('button', { name: /Start interview/ })).toBeEnabled()
  })

  it('an error does not follow the learner to another tool, and clears on the next try', async () => {
    vi.mocked(api.analyzeSkillGap).mockRejectedValueOnce(httpError(503)).mockResolvedValueOnce({
      target_role: 'AI Engineer', current_skills: [], missing_skills: [], recommended_roadmap: [],
      readiness_score: 55, summary: 'Getting there.',
    })
    const user = userEvent.setup()
    render(<MentorPage />)

    await user.click(screen.getByRole('button', { name: /Skill gap/ }))
    await user.click(screen.getByRole('button', { name: /Analyze skill gap/ }))
    await screen.findByRole('alert')

    await user.click(screen.getByRole('button', { name: /Code review/ }))
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: /Skill gap/ }))
    await user.click(screen.getByRole('button', { name: /Analyze skill gap/ }))
    expect(await screen.findByText(/Getting there/)).toBeInTheDocument()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    const region = screen.getByText(/Getting there/).closest('div') as HTMLElement
    expect(within(region).queryByText(STRINGS.en['mentor.error.unavailable'])).toBeNull()
  })
})
