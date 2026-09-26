import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import MentorPage from '@/app/mentor/page'
import { useLanguageStore } from '@/lib/language'
import { STRINGS } from '@/lib/i18n'
import { router, setSearch } from '@/test/nav'
import { WalletProvider } from '@/components/layout/WalletContext'

// The AI mentor page, chat mode. The API is the seam: every request goes through `api.*`, so what
// the page does with a success, a failure, a slow answer and a full quota is testable without a
// network or a model.

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({
    user: { full_name: 'Amira Hassan', experience_level: 'intermediate', overall_readiness_score: 42.4 },
    isAuthenticated: true,
    isLoading: false,
  }),
}))
vi.mock('@/components/layout/AppShell', async () => {
  const { createElement } = await import('react')
  return { AppShell: ({ children }: { children: React.ReactNode }) => createElement('div', null, children) }
})
vi.mock('@/components/layout/PageHeader', async () => {
  const { createElement, Fragment } = await import('react')
  return {
    PageHeader: ({ title, action }: { title: string; action?: React.ReactNode }) =>
      createElement(Fragment, null, createElement('h1', null, title), action),
  }
})
vi.mock('@/lib/api', () => ({
  api: {
    chat: vi.fn(),
    getMentorSessions: vi.fn(),
    newMentorSession: vi.fn(),
    getMockInterviewQuestion: vi.fn(),
    getWallet: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const chat = vi.mocked(api.chat)
const sessions = vi.mocked(api.getMentorSessions)
const newSession = vi.mocked(api.newMentorSession)
const getWallet = vi.mocked(api.getWallet)

const httpError = (status: number, detail?: unknown) => ({ response: { status, data: { detail } } })

function deferred<T>() {
  let resolve!: (v: T) => void
  const promise = new Promise<T>((res) => { resolve = res })
  return { promise, resolve }
}

const reply = (text: string, suggested_actions: string[] = []) => ({ session_id: 1, reply: text, suggested_actions })
const session = (id: number, title: string | undefined, messages: Array<[string, string]> = [], updated = '2026-09-20T10:00:00Z') => ({
  id,
  title,
  messages: messages.map(([role, content]) => ({ role: role as 'user' | 'assistant', content, timestamp: updated })),
  created_at: updated,
  updated_at: updated,
})

const box = () => screen.getByRole('textbox', { name: STRINGS.en['mentor.input.label'] })
const sendButton = () => screen.getByRole('button', { name: STRINGS.en['common.send'] })

async function renderChat() {
  await act(async () => { render(<WalletProvider><MentorPage /></WalletProvider>) })
}

async function ask(user: ReturnType<typeof userEvent.setup>, text: string) {
  await user.type(box(), text)
  await user.click(sendButton())
}

beforeEach(() => {
  Element.prototype.scrollTo = vi.fn()
  sessions.mockResolvedValue([])
  getWallet.mockResolvedValue({ credit_balance: 500 })
  newSession.mockResolvedValue(session(9, 'New Session') as never)
})
afterEach(() => vi.unstubAllEnvs())

describe('opening the mentor', () => {
  it('greets the learner, names what it knows, and offers an empty focusable box', async () => {
    await renderChat()
    expect(screen.getByRole('heading', { level: 1, name: STRINGS.en['nav.mentor'] })).toBeInTheDocument()
    expect(screen.getByText(/I'm your AI mentor/)).toBeInTheDocument()
    expect(box()).toHaveValue('')
    expect(chat).not.toHaveBeenCalled()
    // The context the API is really given, and no more.
    const known = within(screen.getByRole('heading', { name: STRINGS.en['mentor.known.title'] }).closest('div') as HTMLElement)
    expect(known.getByText('Intermediate')).toBeInTheDocument()
    expect(known.getByText('42%')).toBeInTheDocument()
    expect(known.getByText(STRINGS.en['mentor.known.note'])).toBeInTheDocument()
  })

  it('arrives on the latest conversation, as that is the one the API continues', async () => {
    sessions.mockResolvedValue([
      session(2, 'What is RAG?', [['user', 'What is RAG?'], ['assistant', 'Retrieval-augmented generation.']]),
      session(1, 'Older one', [['user', 'Older one'], ['assistant', 'Older answer']], '2026-09-10T10:00:00Z'),
    ])
    await renderChat()
    expect(await screen.findByText('Retrieval-augmented generation.')).toBeInTheDocument()
    expect(screen.queryByText('Older answer')).not.toBeInTheDocument()
  })

  it('does not send an empty or whitespace-only message', async () => {
    const user = userEvent.setup()
    await renderChat()
    expect(sendButton()).toBeDisabled()
    await user.type(box(), '   {Enter}')
    expect(chat).not.toHaveBeenCalled()
  })
})

describe('asking a question', () => {
  it('sends it with the reader’s language settings and shows the answer', async () => {
    chat.mockResolvedValue(reply('RAG retrieves documents first, then generates from them.', ['Quiz me']))
    const user = userEvent.setup()
    await renderChat()
    await ask(user, 'Explain RAG simply')
    expect(await screen.findByText(/retrieves documents first/)).toBeInTheDocument()
    expect(chat).toHaveBeenCalledWith('Explain RAG simply', undefined, { language: 'en', terminology_mode: 'arabic_first' })
    expect(box()).toHaveValue('')
  })

  it('shows the typing line while waiting and blocks a second send', async () => {
    const pending = deferred<ReturnType<typeof reply>>()
    chat.mockReturnValue(pending.promise)
    const user = userEvent.setup()
    await renderChat()
    await ask(user, 'Explain RAG simply')

    expect(await screen.findByText(STRINGS.en['mentor.typing'])).toBeInTheDocument()
    await user.type(box(), 'and another')
    expect(sendButton()).toBeDisabled()
    await user.keyboard('{Enter}')
    expect(chat).toHaveBeenCalledTimes(1)

    await act(async () => { pending.resolve(reply('Simply: look it up, then answer.')) })
    expect(await screen.findByText(/look it up, then answer/)).toBeInTheDocument()
    expect(screen.queryByText(STRINGS.en['mentor.typing'])).not.toBeInTheDocument()
  })

  it('sends with Enter, but not Shift+Enter', async () => {
    chat.mockResolvedValue(reply('ok'))
    const user = userEvent.setup()
    await renderChat()
    await user.type(box(), 'first{Shift>}{Enter}{/Shift}')
    expect(chat).not.toHaveBeenCalled()
    expect((box() as HTMLTextAreaElement).value).toBe('first\n')
    await user.type(box(), 'second{Enter}')
    await waitFor(() => expect(chat).toHaveBeenCalledTimes(1))
    expect(chat.mock.calls[0][0]).toBe('first\nsecond')
  })

  it('tapping a suggestion chip sends it', async () => {
    chat.mockResolvedValueOnce(reply('First answer', ['Quiz me on chunking'])).mockResolvedValueOnce(reply('Second answer'))
    const user = userEvent.setup()
    await renderChat()
    await ask(user, 'hello')
    await user.click(await screen.findByRole('button', { name: 'Quiz me on chunking' }))
    expect(await screen.findByText('Second answer')).toBeInTheDocument()
    expect(chat).toHaveBeenLastCalledWith('Quiz me on chunking', undefined, expect.anything())
  })

  it('a shortcut sends its prompt', async () => {
    chat.mockResolvedValue(reply('Here is a plan'))
    const user = userEvent.setup()
    await renderChat()
    await user.click(screen.getByRole('button', { name: new RegExp(STRINGS.en['mentor.shortcut1']) }))
    expect(await screen.findByText('Here is a plan')).toBeInTheDocument()
    expect(chat.mock.calls[0][0]).toBe(STRINGS.en['mentor.shortcut1'])
  })

  it('attached code goes in the message as a fenced block and shows as a code block', async () => {
    chat.mockResolvedValue(reply('Looks fine'))
    const user = userEvent.setup()
    await renderChat()
    await user.click(screen.getByRole('button', { name: STRINGS.en['mentor.attach'] }))
    await user.type(screen.getByLabelText(STRINGS.en['mentor.attach.label']), 'x = 1')
    await user.type(box(), 'Review this')
    await user.click(sendButton())
    await waitFor(() => expect(chat).toHaveBeenCalled())
    expect(chat.mock.calls[0][0]).toBe('Review this\n\n```\nx = 1\n```')
    const sent = screen.getByText('Review this').closest('[dir]') as HTMLElement
    expect(within(sent).getByText('x = 1').closest('pre')).toBeInTheDocument()
    expect(screen.queryByLabelText(STRINGS.en['mentor.attach.label'])).not.toBeInTheDocument()
  })
})

describe('code in a reply', () => {
  const answer = 'Use a loop:\n\n```python\nfor i in range(3):\n    print(i)\n```\n\nAnd an untagged one:\n\n```\nplain block\n```\n\nInline `len(x)` stays inline.'

  it('draws fenced code, tagged or not, as a dark left-to-right block, and inline code inline', async () => {
    chat.mockResolvedValue(reply(answer))
    const user = userEvent.setup()
    await renderChat()
    await ask(user, 'loop?')
    const tagged = (await screen.findByText(/for i in range/)).closest('pre') as HTMLElement
    expect(tagged.parentElement).toHaveAttribute('dir', 'ltr')
    expect(tagged.parentElement?.className).toContain('bg-[#0B0E14]')
    expect(tagged.textContent).toContain('print(i)')
    expect(screen.getByText('python')).toBeInTheDocument()
    // The untagged fence is a block too, not inline code.
    expect(screen.getByText('plain block').closest('pre')).toBeInTheDocument()
    expect(screen.getByText('len(x)').closest('pre')).toBeNull()
  })

  it('has a copy button per block that copies exactly the code', async () => {
    chat.mockResolvedValue(reply(answer))
    const user = userEvent.setup()
    await renderChat()
    await ask(user, 'loop?')
    await screen.findByText(/for i in range/)
    const copy = screen.getAllByRole('button', { name: new RegExp(STRINGS.en['mentor.copyCode']) })
    expect(copy).toHaveLength(2)
    await user.click(copy[0])
    expect(await navigator.clipboard.readText()).toBe('for i in range(3):\n    print(i)')
    expect(within(copy[0]).getByText(STRINGS.en['mentor.copied'])).toBeInTheDocument()
  })
})

describe('when the mentor fails', () => {
  it('says why, keeps what was typed for another try, and shows offline only when unreachable', async () => {
    chat.mockRejectedValueOnce(httpError(503, 'RuntimeError sk-LEAK api.openai.com'))
    const user = userEvent.setup()
    await renderChat()
    await ask(user, 'Explain RAG')
    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent(STRINGS.en['mentor.error.unavailable'])
    expect(document.body.textContent).not.toMatch(/sk-LEAK|RuntimeError|api\.openai\.com/)
    // Retrying works and the draft is still there.
    expect(box()).toHaveValue('Explain RAG')
    expect(screen.getByText(STRINGS.en['mentor.offline'])).toBeInTheDocument()
    chat.mockResolvedValueOnce(reply('Second try worked'))
    await user.click(sendButton())
    expect(await screen.findByText('Second try worked')).toBeInTheDocument()
    expect(screen.getByText(STRINGS.en['mentor.online'])).toBeInTheDocument()
  })

  it('an empty wallet (402) says so and offers the plans', async () => {
    chat.mockRejectedValueOnce(httpError(402, { error: 'insufficient_credits' }))
    const user = userEvent.setup()
    await renderChat()
    await ask(user, 'hi')
    expect(await screen.findByText(STRINGS.en['mentor.error.credits'])).toBeInTheDocument()
    const upsell = screen.getByTestId('mentor-upsell')
    expect(within(upsell).getByText(STRINGS.en['mentor.upsell.credits.title'])).toBeInTheDocument()
    expect(within(upsell).getByRole('link', { name: STRINGS.en['mentor.upsell.credits.cta'] })).toHaveAttribute('href', '/billing')
  })
})

describe('the Free plan quota', () => {
  it('shows what is left, counts each delivered message, and stops at the limit with an upsell to /billing', async () => {
    setSearch('mockQuotaUsed=19')
    chat.mockResolvedValue(reply('Last free answer'))
    const user = userEvent.setup()
    await renderChat()
    expect(screen.getByText('1 of 20 messages left today')).toBeInTheDocument()
    expect(screen.queryByTestId('mentor-upsell')).not.toBeInTheDocument()

    await ask(user, 'one more')
    expect(await screen.findByText('Last free answer')).toBeInTheDocument()
    const upsell = await screen.findByTestId('mentor-upsell')
    expect(within(upsell).getByText(STRINGS.en['mentor.upsell.quota.title'])).toBeInTheDocument()
    expect(within(upsell).getByRole('link', { name: STRINGS.en['mentor.upsell.cta'] })).toHaveAttribute('href', '/billing')
    expect(box()).toBeDisabled()
    expect(sendButton()).toBeDisabled()
  })

  it('opens already at the limit with ?mockQuotaUsed=20, and a shortcut cannot send', async () => {
    setSearch('mockQuotaUsed=20')
    const user = userEvent.setup()
    await renderChat()
    expect(await screen.findByTestId('mentor-upsell')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: new RegExp(STRINGS.en['mentor.shortcut2']) }))
    expect(chat).not.toHaveBeenCalled()
  })

  it('a failed message does not use up the allowance', async () => {
    setSearch('mockQuotaUsed=5')
    chat.mockRejectedValueOnce(httpError(500))
    const user = userEvent.setup()
    await renderChat()
    await ask(user, 'hi')
    await screen.findByRole('alert')
    expect(screen.getByText('15 of 20 messages left today')).toBeInTheDocument()
  })

  it('shows no quota at all in a production build, where there is no real quota to show', async () => {
    vi.stubEnv('NODE_ENV', 'production')
    setSearch('mockQuotaUsed=20')
    await renderChat()
    expect(screen.queryByTestId('mentor-upsell')).not.toBeInTheDocument()
    expect(screen.queryByText(/messages left today/)).not.toBeInTheDocument()
    expect(box()).toBeEnabled()
  })
})

describe('threads', () => {
  const list = () => [
    session(2, 'What is RAG?', [['user', 'What is RAG?'], ['assistant', 'Latest answer']]),
    session(1, 'New Session', [['user', 'Explain embeddings please'], ['assistant', 'Older answer']], '2026-09-10T10:00:00Z'),
  ]

  it('lists them with a title and a date; a "New Session" takes the first message as its title', async () => {
    sessions.mockResolvedValue(list())
    await renderChat()
    expect(await screen.findByRole('button', { name: /What is RAG\?/ })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Explain embeddings please/ })).toBeInTheDocument()
    expect(screen.getByText('10 September')).toBeInTheDocument()
  })

  it('opens an earlier one to read, says new messages go to the latest, and goes back', async () => {
    sessions.mockResolvedValue(list())
    const user = userEvent.setup()
    await renderChat()
    await user.click(await screen.findByRole('button', { name: /Explain embeddings please/ }))
    expect(screen.getByText('Older answer')).toBeInTheDocument()
    expect(screen.queryByText('Latest answer')).not.toBeInTheDocument()
    expect(screen.getByText(STRINGS.en['mentor.thread.viewing'])).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: STRINGS.en['mentor.thread.back'] }))
    expect(screen.getByText('Latest answer')).toBeInTheDocument()
    expect(screen.queryByText(STRINGS.en['mentor.thread.viewing'])).not.toBeInTheDocument()
  })

  it('a new conversation starts from the greeting', async () => {
    sessions.mockResolvedValue(list())
    const user = userEvent.setup()
    await renderChat()
    await screen.findByText('Latest answer')
    await user.click(screen.getByRole('button', { name: STRINGS.en['mentor.threads.new'] }))
    await waitFor(() => expect(newSession).toHaveBeenCalled())
    await waitFor(() => expect(screen.queryByText('Latest answer')).not.toBeInTheDocument())
    expect(screen.getByText(/I'm your AI mentor/)).toBeInTheDocument()
  })

  it('says so when there are none', async () => {
    await renderChat()
    expect(await screen.findByText(STRINGS.en['mentor.threads.empty'])).toBeInTheDocument()
  })
})

describe('the mode switch', () => {
  it('keeps the mode in the URL', async () => {
    const user = userEvent.setup()
    await renderChat()
    const group = screen.getByRole('group', { name: STRINGS.en['mentor.modes'] })
    expect(within(group).getByRole('button', { name: STRINGS.en['mentor.mode.chat'] })).toHaveAttribute('aria-pressed', 'true')
    await user.click(within(group).getByRole('button', { name: STRINGS.en['mentor.mode.interview'] }))
    expect(router.replace).toHaveBeenCalledWith('/mentor?mode=interview', { scroll: false })
  })

  it('?mode=interview shows the interview side, not the chat', async () => {
    setSearch('mode=interview')
    await renderChat()
    expect(screen.queryByRole('textbox', { name: STRINGS.en['mentor.input.label'] })).not.toBeInTheDocument()
    expect(await screen.findByText(STRINGS.en['interview.none.title'])).toBeInTheDocument()
    expect(screen.getAllByRole('link', { name: STRINGS.en['interview.report.new'] })[0]).toHaveAttribute('href', '/mentor/interview/new')
    expect(within(screen.getByRole('group', { name: STRINGS.en['mentor.modes'] })).getByRole('button', { name: STRINGS.en['mentor.mode.interview'] }))
      .toHaveAttribute('aria-pressed', 'true')
  })
})

describe('in Arabic', () => {
  beforeEach(() => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
  })

  it('asks the server to answer in Arabic and renders the answer right-to-left', async () => {
    chat.mockResolvedValue(reply('يسترجع المستندات أولاً ثم يولّد الإجابة.'))
    const user = userEvent.setup()
    await renderChat()
    await user.type(screen.getByRole('textbox', { name: STRINGS.ar['mentor.input.label'] }), 'ما هو RAG؟')
    await user.click(screen.getByRole('button', { name: STRINGS.ar['common.send'] }))
    const answer = await screen.findByText(/يسترجع المستندات/)
    expect(answer.closest('[dir]')).toHaveAttribute('dir', 'rtl')
    expect(chat).toHaveBeenCalledWith('ما هو RAG؟', undefined, { language: 'ar', terminology_mode: 'arabic_first' })
  })

  it('greets, labels and reports in Arabic, with code still left to right', async () => {
    chat.mockResolvedValueOnce(reply('جرّب:\n\n```python\nprint(1)\n```'))
    const user = userEvent.setup()
    await renderChat()
    expect(screen.getByText(/أنا مرشدك الذكي/)).toBeInTheDocument()
    await user.type(screen.getByRole('textbox', { name: STRINGS.ar['mentor.input.label'] }), 'س')
    await user.click(screen.getByRole('button', { name: STRINGS.ar['common.send'] }))
    expect((await screen.findByText('print(1)')).closest('[dir]')).toHaveAttribute('dir', 'ltr')
    chat.mockRejectedValueOnce(httpError(429))
    await user.type(screen.getByRole('textbox', { name: STRINGS.ar['mentor.input.label'] }), 'ص')
    await user.click(screen.getByRole('button', { name: STRINGS.ar['common.send'] }))
    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.ar['mentor.error.rateLimit'])
  })
})

describe('what the mentor knows', () => {
  it('lists exactly the five things the API is given, then says the lesson and exercise are not sent', async () => {
    await renderChat()
    const card = screen.getByRole('heading', { name: STRINGS.en['mentor.known.title'] }).closest('div') as HTMLElement
    const rows = Array.from(card.querySelectorAll('dl > div')).map((row) => [row.querySelector('dt')?.textContent, row.querySelector('dd')?.textContent])
    expect(rows).toEqual([
      [STRINGS.en['mentor.known.name'], 'Amira Hassan'],
      [STRINGS.en['mentor.known.level'], 'Intermediate'],
      [STRINGS.en['mentor.known.readiness'], '42%'],
      [STRINGS.en['mentor.known.language'], 'English'],
      [STRINGS.en['mentor.known.terms'], 'Arabic First'],
    ])
    expect(within(card).getByText(STRINGS.en['mentor.known.note'])).toBeInTheDocument()
  })

  it('has shortcuts that ask for nothing the mentor cannot see', () => {
    for (const language of ['en', 'ar'] as const) {
      for (const key of ['mentor.shortcut1', 'mentor.shortcut2', 'mentor.shortcut3'] as const) {
        expect(STRINGS[language][key]).not.toMatch(/exercise|test|my code|تمريني|الاختبار|الكود/i)
      }
    }
  })
})

describe('the credit line and the out-of-credits bar', () => {
  it('says what a message costs and what is left, and counts down as messages are delivered', async () => {
    chat.mockResolvedValue(reply('ok'))
    const user = userEvent.setup()
    await renderChat()
    expect(await screen.findByTestId('credit-line')).toHaveTextContent('Each message costs 2 credits · 500 left')
    await ask(user, 'hello')
    await screen.findByText('ok')
    expect(screen.getByTestId('credit-line')).toHaveTextContent('498 left')
  })

  it('replaces the box with a bar linking to /billing when the balance cannot pay for a message', async () => {
    getWallet.mockResolvedValue({ credit_balance: 1 })
    await renderChat()
    const bar = await screen.findByTestId('mentor-upsell')
    expect(within(bar).getByText(STRINGS.en['mentor.upsell.credits.title'])).toBeInTheDocument()
    expect(within(bar).getByRole('link', { name: STRINGS.en['mentor.upsell.credits.cta'] })).toHaveAttribute('href', '/billing')
    expect(screen.queryByRole('textbox', { name: STRINGS.en['mentor.input.label'] })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: STRINGS.en['common.send'] })).not.toBeInTheDocument()
  })

  it('exactly one message of credit still has the box, and spending it brings the bar', async () => {
    getWallet.mockResolvedValue({ credit_balance: 2 })
    chat.mockResolvedValue(reply('last one'))
    const user = userEvent.setup()
    await renderChat()
    await screen.findByTestId('credit-line')
    await ask(user, 'hello')
    await screen.findByText('last one')
    await waitFor(() => expect(screen.queryByRole('textbox', { name: STRINGS.en['mentor.input.label'] })).not.toBeInTheDocument())
    expect(screen.getByTestId('mentor-upsell')).toBeInTheDocument()
  })

  it('a 402 swaps the box for the bar even when the balance looked fine', async () => {
    chat.mockRejectedValueOnce(httpError(402, { error: 'insufficient_credits' }))
    const user = userEvent.setup()
    await renderChat()
    await ask(user, 'hi')
    expect(await screen.findByTestId('mentor-upsell')).toBeInTheDocument()
    expect(screen.queryByRole('textbox', { name: STRINGS.en['mentor.input.label'] })).not.toBeInTheDocument()
    expect(screen.getByText(STRINGS.en['mentor.error.credits'])).toBeInTheDocument()
  })

  it('does not block, or show a made-up number, when the balance is not known', async () => {
    getWallet.mockRejectedValue(new Error('offline'))
    await renderChat()
    expect(box()).toBeEnabled()
    expect(screen.queryByTestId('credit-line')).not.toBeInTheDocument()
    expect(screen.queryByTestId('mentor-upsell')).not.toBeInTheDocument()
  })
})

describe('the thread list, latest first', () => {
  const older = session(1, 'New Session', [['user', 'Explain embeddings please'], ['assistant', 'Older answer']], '2026-09-10T10:00:00Z')
  const latest = session(2, 'What is RAG?', [['user', 'What is RAG?'], ['assistant', 'Latest answer']], '2026-09-20T10:00:00Z')
  const fresh = { ...session(3, 'New Session', []), updated_at: null, created_at: '2026-09-25T10:00:00Z' }

  it('is ordered by time whatever order the API answers in, and marks the latest as the open one', async () => {
    sessions.mockResolvedValue([older, latest] as never)
    await renderChat()
    const rows = await screen.findAllByRole('button', { name: /RAG\?|embeddings please/ })
    expect(rows[0].textContent).toContain('What is RAG?')
    expect(rows[1].textContent).toContain('Explain embeddings please')
    expect(rows[0]).toHaveAttribute('aria-current', 'true')
    expect(rows[1]).not.toHaveAttribute('aria-current')
  })

  it('never labels a thread "New Session": the first message does, or a neutral name when there is none', async () => {
    sessions.mockResolvedValue([fresh, latest, older] as never)
    await renderChat()
    await screen.findByRole('button', { name: /What is RAG\?/ })
    expect(document.body.textContent).not.toMatch(/New Session/)
    expect(screen.getByRole('button', { name: new RegExp(STRINGS.en['mentor.thread.untitled']) })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Explain embeddings please/ })).toBeInTheDocument()
  })

  it('sending from an older thread goes to the latest conversation, and the reader is taken back to it', async () => {
    sessions.mockResolvedValue([latest, older] as never)
    chat.mockResolvedValue(reply('Answer in the latest'))
    const user = userEvent.setup()
    await renderChat()
    await user.click(await screen.findByRole('button', { name: /Explain embeddings please/ }))
    expect(screen.getByText('Older answer')).toBeInTheDocument()
    expect(screen.getByText(STRINGS.en['mentor.thread.viewing'])).toBeInTheDocument()

    await ask(user, 'A new question')
    expect(await screen.findByText('Answer in the latest')).toBeInTheDocument()
    expect(screen.queryByText(STRINGS.en['mentor.thread.viewing'])).not.toBeInTheDocument()
    expect(screen.queryByText('Older answer')).not.toBeInTheDocument()
    expect(screen.getByText('Latest answer')).toBeInTheDocument()
    expect(screen.getByText('A new question')).toBeInTheDocument()
  })
})

describe('the handoff copy, in Arabic', () => {
  beforeEach(() => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
  })

  it('the header says what the mentor knows and that it does not see the lesson', async () => {
    await renderChat()
    expect(screen.getByText('يعرف مستواك وجاهزيتك · لا يرى درسك الحالي')).toBeInTheDocument()
  })

  it('the credit line reads "رصيدان لكل رسالة · المتبقّي N" with a top-up link to /billing', async () => {
    await renderChat()
    expect(await screen.findByTestId('credit-line')).toHaveTextContent('رصيدان لكل رسالة · المتبقّي 500')
    expect(screen.getByRole('link', { name: 'شحن الرصيد' })).toHaveAttribute('href', '/billing')
  })

  it('the out-of-credits bar has the title, body and button from the handoff, and links to /billing', async () => {
    getWallet.mockResolvedValue({ credit_balance: 0 })
    await renderChat()
    const bar = await screen.findByTestId('mentor-upsell')
    expect(within(bar).getByText('نفد رصيدك')).toBeInTheDocument()
    expect(within(bar).getByText('كل رسالة للمرشد تكلّف رصيدين. اشحن رصيدك أو رقِّ خطتك لتكمل المحادثة.')).toBeInTheDocument()
    expect(within(bar).getByRole('link', { name: 'اشحن الرصيد' })).toHaveAttribute('href', '/billing')
  })
})

describe('the credit line in English', () => {
  it('has a Top up link to /billing next to the price and balance', async () => {
    await renderChat()
    expect(await screen.findByRole('link', { name: STRINGS.en['mentor.credits.topup'] })).toHaveAttribute('href', '/billing')
  })
  it('says what the mentor does not see, in the header', async () => {
    await renderChat()
    expect(screen.getByText(STRINGS.en['mentor.header.sub'])).toBeInTheDocument()
  })
})

describe('the top-up link sits after the credit text, at the trailing end', () => {
  it.each(['en', 'ar'] as const)('in %s: text first, link second, in the DOM (so the row mirrors with the direction)', async (language) => {
    useLanguageStore.setState({ language, mode: 'arabic_first', annotateTerms: true })
    await renderChat()
    const line = await screen.findByTestId('credit-line')
    const link = screen.getByRole('link', { name: STRINGS[language]['mentor.credits.topup'] })
    expect(line.compareDocumentPosition(link) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
    // One row, spread to its two ends, on logical (not left/right) properties.
    const row = link.parentElement as HTMLElement
    expect(row.className).toContain('justify-between')
    expect(row.className).not.toMatch(/\b(pl|pr|ml|mr|text-left|text-right|flex-row-reverse)\b/)
  })
})
