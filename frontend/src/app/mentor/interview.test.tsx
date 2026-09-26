import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import MentorPage from '@/app/mentor/page'
import SetupPage from '@/app/mentor/interview/new/page'
import ReportPage from '@/app/mentor/interview/[id]/report/page'
import { STRINGS } from '@/lib/i18n'
import { buildSession, endSession, type AnswerScore, type InterviewSession, type QuestionRecord } from '@/lib/mentor/interview'
import { interviewStore } from '@/lib/mentor/interviewStore'
import { useLanguageStore } from '@/lib/language'
import { router, setParams, setSearch } from '@/test/nav'

// The mock interview: setup, the stage, and the report. The API, the camera, the microphone and
// the scorer are the seams; the rest is the real code.

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({
    user: { full_name: 'Amira Hassan', experience_level: 'intermediate', overall_readiness_score: 42 },
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
  api: { getMentorSessions: vi.fn(), chat: vi.fn(), newMentorSession: vi.fn(), getMockInterviewQuestion: vi.fn(), listTracks: vi.fn() },
}))
// Scoring without the 600 ms wait, and switchable off (as in a production build).
const scorer = vi.hoisted(() => ({ on: true }))
vi.mock('@/lib/mentor/scoring', async (importOriginal) => {
  const real = await importOriginal<typeof import('@/lib/mentor/scoring')>()
  return { ...real, getAnswerScorer: () => (scorer.on ? new real.MockAnswerScorer({ delayMs: 0 }) : null) }
})
import { api } from '@/lib/api'

const nextQuestion = vi.mocked(api.getMockInterviewQuestion)
const listTracks = vi.mocked(api.listTracks)

const httpError = (status: number, detail?: unknown) => ({ response: { status, data: { detail } } })
const q = (text: string, extra: Partial<{ question_type: 'theoretical' | 'coding'; hints: string[] }> = {}) => ({
  question: text, question_type: 'theoretical' as const, hints: [], ...extra,
})

function seed(over: Partial<InterviewSession> = {}, ended = false): InterviewSession {
  const s = { ...buildSession('iv1', { role: 'AI Developer', type: 'technical', language: 'en', durationMin: 30 }), totalQuestions: 2, ...over }
  interviewStore.save(ended ? endSession(s) : s)
  return s
}
const rec = (id: string, over: Partial<QuestionRecord> = {}): QuestionRecord => ({
  id, text: `Question ${id}`, qtype: 'theoretical', hints: [], answer: null, skipped: false, score: null, ...over,
})
const score = (a: number, s: number, c: number): AnswerScore => ({ accuracy: a, structure: s, clarity: c, note: { key: 'interview.note.solid' } })

async function renderStage() {
  setSearch('mode=interview')
  await act(async () => { render(<MentorPage />) })
}
const answerBox = () => screen.findByRole('textbox', { name: STRINGS.en['interview.answer.label'] })
const nextButton = () => screen.getByRole('button', { name: STRINGS.en['interview.next'] })

// ── camera and microphone stand-ins ─────────────────────────────────────
const stream = () => ({ getTracks: () => [{ stop: vi.fn() }] }) as unknown as MediaStream
function setMedia(getUserMedia: unknown) {
  Object.defineProperty(navigator, 'mediaDevices', { value: getUserMedia ? { getUserMedia } : undefined, configurable: true })
}
class FakeRecognition {
  static last: FakeRecognition | null = null
  lang = ''
  continuous = false
  interimResults = false
  onresult: ((e: unknown) => void) | null = null
  onerror: ((e: unknown) => void) | null = null
  onend: (() => void) | null = null
  start() { FakeRecognition.last = this }
  stop() { this.onend?.() }
  abort() {}
}

beforeEach(() => {
  Element.prototype.scrollTo = vi.fn()
  vi.mocked(api.getMentorSessions).mockResolvedValue([])
  listTracks.mockResolvedValue([
    { id: 1, slug: 'ai-developer', title: 'AI Developer', title_ar: 'مطوّر ذكاء اصطناعي', estimated_weeks: 12 },
    { id: 2, slug: 'data-analyst', title: 'Data Analyst', estimated_weeks: 8 },
  ])
  scorer.on = true
  setMedia(undefined)
})
afterEach(() => {
  vi.unstubAllEnvs()
  delete (window as { SpeechRecognition?: unknown }).SpeechRecognition
  FakeRecognition.last = null
})

describe('the stage', () => {
  it('fetches the first question for the role, and shows the stage', async () => {
    nextQuestion.mockResolvedValueOnce(q('What is retrieval-augmented generation?', { hints: ['Think of an open-book exam'] }))
    seed()
    await renderStage()
    expect(await screen.findByRole('heading', { level: 2, name: 'What is retrieval-augmented generation?' })).toBeInTheDocument()
    expect(nextQuestion).toHaveBeenCalledWith('AI Developer technical concepts', 'intermediate', [])
    expect(screen.getByText('AI Developer')).toHaveAttribute('dir', 'ltr')
    expect(screen.getByText('Technical')).toBeInTheDocument()
    expect(screen.getByText('Question 1 of 2')).toBeInTheDocument()
    expect(screen.getByRole('timer')).toHaveAccessibleName(/of 30:00/)
    expect(screen.getByText(STRINGS.en['interview.interviewer'])).toBeInTheDocument()
    expect(screen.getByText(STRINGS.en['interview.you'])).toBeInTheDocument()
    expect(screen.getByText(STRINGS.en['interview.hints'])).toBeInTheDocument()
  })

  it('says Preparing while it fetches, and the interviewer halo breathes only then', async () => {
    let release!: (v: ReturnType<typeof q>) => void
    nextQuestion.mockReturnValueOnce(new Promise((res) => { release = res }))
    seed()
    await renderStage()
    expect(await screen.findByText(STRINGS.en['interview.loadingQuestion'])).toBeInTheDocument()
    expect(document.querySelector('[data-busy="true"] .animate-masarHalo')).not.toBeNull()
    await act(async () => { release(q('First?')) })
    expect(await screen.findByText('First?')).toBeInTheDocument()
    expect(document.querySelector('.animate-masarHalo')).toBeNull()
  })

  it('answers, scores the answer in the side panel, and asks the next with the earlier pair', async () => {
    nextQuestion.mockResolvedValueOnce(q('First?')).mockResolvedValueOnce(q('Second?'))
    const user = userEvent.setup()
    seed()
    await renderStage()
    expect(screen.getByText(STRINGS.en['interview.lastScore.none'])).toBeInTheDocument()
    expect(nextButton()).toBeDisabled()
    await user.type(await answerBox(), 'It retrieves documents first. Then it generates from them. We cut errors by 30 percent.')
    await user.click(nextButton())

    expect(await screen.findByText('Second?')).toBeInTheDocument()
    expect(screen.getByText('Question 2 of 2')).toBeInTheDocument()
    expect(nextQuestion).toHaveBeenLastCalledWith('AI Developer technical concepts', 'intermediate', [
      { question: 'First?', answer: 'It retrieves documents first. Then it generates from them. We cut errors by 30 percent.' },
    ])
    // The panel: a score out of 10, the three bars, and the note.
    await screen.findByText(STRINGS.en['interview.dim.accuracy'])
    expect(screen.getAllByRole('meter')).toHaveLength(3)
    expect(screen.getByText(STRINGS.en['interview.note.label'])).toBeInTheDocument()
    expect(screen.getByText(STRINGS.en['interview.mockScores'])).toBeInTheDocument()
    // The last question's button leads to the report.
    expect(screen.getByRole('button', { name: STRINGS.en['interview.finish'] })).toBeInTheDocument()
  })

  it('skipping records the question as skipped and moves on without scoring', async () => {
    nextQuestion.mockResolvedValueOnce(q('First?')).mockResolvedValueOnce(q('Second?'))
    const user = userEvent.setup()
    seed()
    await renderStage()
    await user.click(await screen.findByRole('button', { name: STRINGS.en['interview.skip'] }))
    expect(await screen.findByText('Second?')).toBeInTheDocument()
    expect(interviewStore.get('iv1')?.questions[0]).toMatchObject({ skipped: true, answer: '', score: null })
    expect(nextQuestion).toHaveBeenLastCalledWith(expect.any(String), 'intermediate', [{ question: 'First?', answer: '' }])
  })

  it('finishing the last question ends the interview once its score is in, and opens the report', async () => {
    const user = userEvent.setup()
    seed({ questions: [rec('a', { answer: 'done', score: score(7, 7, 7) }), rec('b')] })
    await renderStage()
    await user.type(await answerBox(), 'A decent answer with 3 points.')
    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.finish'] }))
    await waitFor(() => expect(router.push).toHaveBeenCalledWith('/mentor/interview/iv1/report'))
    const saved = interviewStore.get('iv1')!
    expect(saved.endedAt).not.toBeNull()
    expect(saved.questions[1].score).not.toBeNull()
    expect(nextQuestion).not.toHaveBeenCalled()
  })

  it('a reload resumes at the first unanswered question without asking for it again', async () => {
    seed({ questions: [rec('a', { answer: 'x' }), rec('b')] })
    await renderStage()
    expect(await screen.findByText('Question b')).toBeInTheDocument()
    expect(screen.getByText('Question 2 of 2')).toBeInTheDocument()
    expect(nextQuestion).not.toHaveBeenCalled()
  })

  it('offers the report when every question was answered but the interview never ended', async () => {
    const user = userEvent.setup()
    seed({ questions: [rec('a', { answer: 'x' }), rec('b', { answer: 'y' })] })
    await renderStage()
    await user.click(await screen.findByRole('button', { name: STRINGS.en['interview.finish'] }))
    await waitFor(() => expect(router.push).toHaveBeenCalledWith('/mentor/interview/iv1/report'))
    expect(interviewStore.get('iv1')?.endedAt).not.toBeNull()
  })

  it('a failed question can be retried, and an empty wallet offers the plans', async () => {
    nextQuestion.mockRejectedValueOnce(httpError(402, { error: 'insufficient_credits' })).mockResolvedValueOnce(q('Now it works?'))
    const user = userEvent.setup()
    seed()
    await renderStage()
    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.en['mentor.error.credits'])
    expect(within(screen.getByTestId('mentor-upsell')).getByRole('link')).toHaveAttribute('href', '/billing')
    await user.click(screen.getByRole('button', { name: STRINGS.en['common.retry'] }))
    expect(await screen.findByText('Now it works?')).toBeInTheDocument()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it('ending asks first, then ends with what was answered and opens the report', async () => {
    nextQuestion.mockResolvedValueOnce(q('First?'))
    const user = userEvent.setup()
    seed({ totalQuestions: 5 })
    await renderStage()
    await screen.findByText('First?')
    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.end'] }))
    const dialog = screen.getByRole('dialog', { name: STRINGS.en['interview.end.title'] })
    expect(within(dialog).getByText('You will see a report for the 0 questions answered so far.')).toBeInTheDocument()
    // The safe choice has the focus, and keeping going closes it without ending anything.
    expect(within(dialog).getByRole('button', { name: STRINGS.en['interview.end.cancel'] })).toHaveFocus()
    await user.click(within(dialog).getByRole('button', { name: STRINGS.en['interview.end.cancel'] }))
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(interviewStore.get('iv1')?.endedAt).toBeNull()

    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.end'] }))
    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.end.confirm'] }))
    await waitFor(() => expect(router.push).toHaveBeenCalledWith('/mentor/interview/iv1/report'))
    expect(interviewStore.get('iv1')?.endedAt).not.toBeNull()
  })

  it('with scoring off (a production build) says so and saves answers without scores', async () => {
    scorer.on = false
    nextQuestion.mockResolvedValueOnce(q('First?')).mockResolvedValueOnce(q('Second?'))
    const user = userEvent.setup()
    seed()
    await renderStage()
    expect(await screen.findByText(STRINGS.en['interview.scoresOff'])).toBeInTheDocument()
    await user.type(await answerBox(), 'An answer')
    await user.click(nextButton())
    await screen.findByText('Second?')
    expect(interviewStore.get('iv1')?.questions[0]).toMatchObject({ answer: 'An answer', score: null })
    expect(screen.queryByRole('meter')).not.toBeInTheDocument()
  })

  it('has an empty state, with the earlier interviews, when nothing is in progress', async () => {
    seed({ questions: [rec('a', { answer: 'x', score: score(8, 8, 8) })] }, true)
    await renderStage()
    expect(await screen.findByText(STRINGS.en['interview.none.title'])).toBeInTheDocument()
    const history = screen.getByRole('link', { name: /AI Developer/ })
    expect(history).toHaveAttribute('href', '/mentor/interview/iv1/report')
    expect(within(history).getByText('8')).toBeInTheDocument()
  })
})

describe('the camera on the stage', () => {
  async function stage() {
    nextQuestion.mockResolvedValue(q('First?'))
    seed()
    await renderStage()
    await screen.findByText('First?')
  }

  it('waits for a click before asking, then shows the live video', async () => {
    const getUserMedia = vi.fn().mockResolvedValue(stream())
    setMedia(getUserMedia)
    const user = userEvent.setup()
    await stage()
    expect(getUserMedia).not.toHaveBeenCalled()
    expect(screen.getByText(STRINGS.en['interview.cam.idle'])).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.check.cameraBtn'] }))
    expect(await screen.findByLabelText(STRINGS.en['interview.cam.tile'])).toBeInTheDocument()
    expect(getUserMedia).toHaveBeenCalledWith({ video: { facingMode: 'user' }, audio: false })
  })

  it('shows Waiting while the browser prompt is open', async () => {
    setMedia(vi.fn().mockReturnValue(new Promise(() => {})))
    const user = userEvent.setup()
    await stage()
    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.check.cameraBtn'] }))
    expect(await screen.findByText(STRINGS.en['interview.cam.pending'])).toBeInTheDocument()
  })

  it('denied: says how to fix it, offers to try again, and the interview still works', async () => {
    const getUserMedia = vi.fn().mockRejectedValueOnce({ name: 'NotAllowedError' }).mockResolvedValueOnce(stream())
    setMedia(getUserMedia)
    const user = userEvent.setup()
    await stage()
    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.check.cameraBtn'] }))
    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.en['interview.cam.denied'])
    await user.type(await answerBox(), 'Still able to type')
    expect(nextButton()).toBeEnabled()
    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.cam.retry'] }))
    expect(await screen.findByLabelText(STRINGS.en['interview.cam.tile'])).toBeInTheDocument()
  })

  it('no device: says so and offers no pointless retry', async () => {
    setMedia(vi.fn().mockRejectedValue({ name: 'NotFoundError' }))
    const user = userEvent.setup()
    await stage()
    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.check.cameraBtn'] }))
    expect(await screen.findByText(STRINGS.en['interview.cam.none'])).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: STRINGS.en['interview.cam.retry'] })).not.toBeInTheDocument()
  })

  it('a browser with no camera API says that, with no button', async () => {
    await stage()
    expect(screen.getByText(STRINGS.en['interview.cam.idle'])).toBeInTheDocument()
    // Asking is what discovers it: idle -> unsupported.
    await userEvent.setup().click(screen.getByRole('button', { name: STRINGS.en['interview.check.cameraBtn'] }))
    expect(await screen.findByText(STRINGS.en['interview.cam.unsupported'])).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: STRINGS.en['interview.check.cameraBtn'] })).not.toBeInTheDocument()
  })
})

describe('the microphone on the stage', () => {
  it('is hidden where the browser has no speech recognition', async () => {
    nextQuestion.mockResolvedValue(q('First?'))
    seed()
    await renderStage()
    await screen.findByText('First?')
    expect(screen.queryByRole('button', { name: STRINGS.en['interview.mic.on'] })).not.toBeInTheDocument()
    expect(screen.getByPlaceholderText(STRINGS.en['interview.answer.placeholder'])).toBeInTheDocument()
  })

  it('toggles dictation into the answer box where it exists', async () => {
    ;(window as { SpeechRecognition?: unknown }).SpeechRecognition = FakeRecognition
    nextQuestion.mockResolvedValue(q('First?'))
    const user = userEvent.setup()
    seed({ language: 'ar' })
    await renderStage()
    const mic = await screen.findByRole('button', { name: STRINGS.en['interview.mic.on'] })
    expect(mic).toHaveAttribute('aria-pressed', 'false')
    await user.click(mic)
    expect(FakeRecognition.last?.lang).toBe('ar-SA')
    expect(screen.getByRole('button', { name: STRINGS.en['interview.mic.off'] })).toHaveAttribute('aria-pressed', 'true')
    act(() => FakeRecognition.last?.onresult?.({ resultIndex: 0, results: [{ isFinal: true, 0: { transcript: 'first phrase' } }] }))
    act(() => FakeRecognition.last?.onresult?.({ resultIndex: 0, results: [{ isFinal: true, 0: { transcript: 'second phrase' } }] }))
    expect(await answerBox()).toHaveValue('first phrase second phrase')
    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.mic.off'] }))
    expect(screen.getByRole('button', { name: STRINGS.en['interview.mic.on'] })).toHaveAttribute('aria-pressed', 'false')
  })

  it('says when the microphone is blocked, and typing still works', async () => {
    ;(window as { SpeechRecognition?: unknown }).SpeechRecognition = FakeRecognition
    nextQuestion.mockResolvedValue(q('First?'))
    const user = userEvent.setup()
    seed()
    await renderStage()
    await user.click(await screen.findByRole('button', { name: STRINGS.en['interview.mic.on'] }))
    act(() => FakeRecognition.last?.onerror?.({ error: 'not-allowed' }))
    expect(await screen.findByText(STRINGS.en['interview.mic.denied'])).toBeInTheDocument()
    await user.type(await answerBox(), 'typed')
    expect(nextButton()).toBeEnabled()
  })
})

describe('setup', () => {
  async function renderSetup(search = '') {
    setSearch(search)
    await act(async () => { render(<SetupPage />) })
  }

  it('offers the roles, types, languages and lengths, and will not start without a role', async () => {
    await renderSetup()
    const roles = await screen.findByRole('group', { name: STRINGS.en['interview.role'] })
    expect(within(roles).getAllByRole('radio').map((r) => r.closest('label')?.textContent)).toEqual(['AI Developer', 'Data Analyst'])
    expect(within(screen.getByRole('group', { name: STRINGS.en['interview.type'] })).getAllByRole('radio')).toHaveLength(3)
    expect(within(screen.getByRole('group', { name: STRINGS.en['interview.duration'] })).getAllByRole('radio')).toHaveLength(3)
    expect(screen.getByText(STRINGS.en['interview.langNote'])).toBeInTheDocument()
    expect(screen.getByRole('button', { name: STRINGS.en['interview.start'] })).toBeDisabled()
  })

  it('shows what it costs and follows the length', async () => {
    const user = userEvent.setup()
    await renderSetup()
    await screen.findByRole('group', { name: STRINGS.en['interview.role'] })
    expect(screen.getByText('Cost: 15 credits (3 per question)')).toBeInTheDocument()
    expect(screen.getByText('5 questions')).toBeInTheDocument()
    await user.click(within(screen.getByRole('group', { name: STRINGS.en['interview.duration'] })).getByRole('radio', { name: '45 min' }))
    expect(screen.getByText('Cost: 24 credits (3 per question)')).toBeInTheDocument()
  })

  it('starts a saved interview with the choices, ending any earlier one that was still open', async () => {
    seed({ id: 'old' })
    const user = userEvent.setup()
    await renderSetup()
    expect(screen.getByText(STRINGS.en['interview.setup.inProgress'])).toBeInTheDocument()
    await user.click(await screen.findByRole('radio', { name: 'Data Analyst' }))
    await user.click(screen.getByRole('radio', { name: 'System design' }))
    await user.click(screen.getByRole('radio', { name: '15 min' }))
    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.start'] }))
    expect(router.push).toHaveBeenCalledWith('/mentor?mode=interview')
    const created = interviewStore.active()!
    expect(created).toMatchObject({ role: 'Data Analyst', type: 'system_design', durationMin: 15, totalQuestions: 3, questions: [] })
    expect(interviewStore.get('old')?.endedAt).not.toBeNull()
  })

  it('lists the roles in Arabic where there is an Arabic name, but keeps the English one as the role', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    const user = userEvent.setup()
    await renderSetup()
    await user.click(await screen.findByRole('radio', { name: 'مطوّر ذكاء اصطناعي' }))
    await user.click(screen.getByRole('button', { name: STRINGS.ar['interview.start'] }))
    expect(interviewStore.active()?.role).toBe('AI Developer')
  })

  it('says when the roles could not load and retries', async () => {
    listTracks.mockRejectedValueOnce(new Error('offline'))
    const user = userEvent.setup()
    await renderSetup()
    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.en['interview.tracks.error'])
    await user.click(screen.getByRole('button', { name: STRINGS.en['common.retry'] }))
    expect(await screen.findByRole('radio', { name: 'AI Developer' })).toBeInTheDocument()
  })

  it('retrying weak questions asks exactly those again, locked to the earlier settings, at no cost', async () => {
    seed(
      {
        role: 'Data Analyst', type: 'behavioral', durationMin: 45, totalQuestions: 3,
        questions: [
          rec('a', { answer: 'ok', score: score(9, 9, 9) }),
          rec('b', { answer: 'meh', score: score(3, 4, 4) }),
          rec('c', { skipped: true, answer: '' }),
        ],
      },
      true,
    )
    const user = userEvent.setup()
    await renderSetup('retry=iv1')
    expect(await screen.findByText('Retrying 2 weak questions from your last interview.')).toBeInTheDocument()
    expect(screen.getByText(STRINGS.en['interview.cost.retry'])).toBeInTheDocument()
    expect(screen.getByRole('radio', { name: 'Behavioral' })).toBeChecked()
    expect(screen.getByRole('radio', { name: 'Behavioral' })).toBeDisabled()
    await user.click(screen.getByRole('button', { name: STRINGS.en['interview.start'] }))
    const created = interviewStore.active()!
    expect(created.retryOf).toBe('iv1')
    expect(created.totalQuestions).toBe(2)
    expect(created.questions.map((x) => x.text)).toEqual(['Question b', 'Question c'])
    expect(created.questions.every((x) => x.answer === null && x.score === null && !x.skipped)).toBe(true)
  })

  describe('camera and microphone check', () => {
    it('camera: idle, then on', async () => {
      setMedia(vi.fn().mockResolvedValue(stream()))
      const user = userEvent.setup()
      await renderSetup()
      expect(screen.getByText(STRINGS.en['interview.check.optional'])).toBeInTheDocument()
      await user.click(screen.getByRole('button', { name: STRINGS.en['interview.check.cameraBtn'] }))
      expect(await screen.findByLabelText(STRINGS.en['interview.cam.tile'])).toBeInTheDocument()
    })

    it('camera: denied is explained and can be retried', async () => {
      setMedia(vi.fn().mockRejectedValue({ name: 'NotAllowedError' }))
      const user = userEvent.setup()
      await renderSetup()
      await user.click(screen.getByRole('button', { name: STRINGS.en['interview.check.cameraBtn'] }))
      expect(await screen.findByText(STRINGS.en['interview.cam.denied'])).toBeInTheDocument()
      expect(screen.getByRole('button', { name: STRINGS.en['interview.cam.retry'] })).toBeInTheDocument()
      // ...and the interview can still start without a camera.
      await user.click(await screen.findByRole('radio', { name: 'AI Developer' }))
      expect(screen.getByRole('button', { name: STRINGS.en['interview.start'] })).toBeEnabled()
    })

    it('the microphone row exists only with speech recognition, and reports each outcome', async () => {
      await renderSetup()
      expect(screen.queryByText(STRINGS.en['interview.check.mic'])).not.toBeInTheDocument()
    })

    it('microphone: working, and blocked', async () => {
      ;(window as { SpeechRecognition?: unknown }).SpeechRecognition = FakeRecognition
      const getUserMedia = vi.fn().mockResolvedValueOnce(stream()).mockRejectedValueOnce({ name: 'NotAllowedError' })
      setMedia(getUserMedia)
      const user = userEvent.setup()
      await renderSetup()
      expect(screen.getByText(STRINGS.en['interview.mic.idle'])).toBeInTheDocument()
      await user.click(screen.getByRole('button', { name: STRINGS.en['interview.check.micBtn'] }))
      expect(await screen.findByText(STRINGS.en['interview.mic.ok'])).toBeInTheDocument()
      await user.click(screen.getByRole('button', { name: STRINGS.en['interview.check.micBtn'] }))
      expect(await screen.findByText(STRINGS.en['interview.mic.denied'])).toBeInTheDocument()
    })
  })
})

describe('the report', () => {
  async function renderReport(id = 'iv1') {
    setParams({ id })
    await act(async () => { render(<ReportPage />) })
  }
  const scored = () =>
    seed(
      {
        totalQuestions: 3,
        questions: [
          rec('a', { answer: 'Strong answer', score: score(9, 8, 7) }),
          rec('b', { answer: 'Weak answer', score: score(3, 4, 5) }),
          rec('c', { skipped: true, answer: '' }),
        ],
      },
      true,
    )

  it('shows the overall score, the three averages, and every question with its scores', async () => {
    scored()
    await renderReport()
    // (9+8+7)/3 = 8, (3+4+5)/3 = 4 -> 6
    expect(await screen.findByTestId('overall-score')).toHaveTextContent('6')
    expect(screen.getByText('2 of 3 questions answered')).toBeInTheDocument()
    expect(screen.getByText('Question a')).toBeInTheDocument()
    expect(screen.getByText('Strong answer')).toBeInTheDocument()
    expect(screen.getAllByRole('meter').length).toBe(3 + 3 + 3)
    expect(screen.getByText(STRINGS.en['interview.report.skipped'])).toBeInTheDocument()
  })

  it('reads strengths and improvements off the scores, and lists the weak questions', async () => {
    scored()
    await renderReport()
    expect(await screen.findByText('Strongest: Technical accuracy (6/10 on average)')).toBeInTheDocument()
    expect(screen.getByText('Weakest: Clarity and brevity (6/10 on average)')).toBeInTheDocument()
    expect(screen.getByText(/Revisit this question: .*Question b/)).toBeInTheDocument()
    expect(screen.getByText(/Revisit this question: .*Question c/)).toBeInTheDocument()
    expect(screen.queryByText(/Revisit this question: .*Question a/)).not.toBeInTheDocument()
  })

  it('"retry weak questions" opens setup for this interview; "new interview" opens a fresh one', async () => {
    scored()
    await renderReport()
    expect(await screen.findByRole('link', { name: STRINGS.en['interview.report.retry'] })).toHaveAttribute('href', '/mentor/interview/new?retry=iv1')
    expect(screen.getByRole('link', { name: STRINGS.en['interview.report.new'] })).toHaveAttribute('href', '/mentor/interview/new')
    expect(screen.getByRole('link', { name: STRINGS.en['interview.report.back'] })).toHaveAttribute('href', '/mentor?mode=interview')
  })

  it('with nothing weak, says so instead of offering a retry', async () => {
    seed({ totalQuestions: 1, questions: [rec('a', { answer: 'Great', score: score(9, 9, 9) })] }, true)
    await renderReport()
    expect(await screen.findByText(STRINGS.en['interview.report.retryNone'])).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: STRINGS.en['interview.report.retry'] })).not.toBeInTheDocument()
  })

  it('with no scores (scoring off) says so and lists the questions and answers only', async () => {
    seed({ totalQuestions: 1, questions: [rec('a', { answer: 'My answer' })] }, true)
    await renderReport()
    expect(await screen.findByText(STRINGS.en['interview.report.noScores'])).toBeInTheDocument()
    expect(screen.queryByTestId('overall-score')).not.toBeInTheDocument()
    expect(screen.queryByRole('meter')).not.toBeInTheDocument()
    expect(screen.getByText('My answer')).toBeInTheDocument()
  })

  it('an interview this browser does not have says so', async () => {
    await renderReport('nope')
    expect(await screen.findByRole('alert')).toHaveTextContent(STRINGS.en['interview.report.notFound'])
  })

  it('reads in Arabic, with the role and the questions still readable', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    scored()
    await renderReport()
    expect(await screen.findByRole('heading', { name: STRINGS.ar['interview.report.title'] })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: STRINGS.ar['interview.report.retry'] })).toBeInTheDocument()
    expect(screen.getByTestId('overall-score').closest('[dir]')).toHaveAttribute('dir', 'ltr')
  })
})


describe('cost, loading and the no-scoring state', () => {
  it('tags the stage with what each question costs', async () => {
    nextQuestion.mockResolvedValue(q('First?'))
    seed()
    await renderStage()
    expect(await screen.findByText('3 credits per question')).toBeInTheDocument()
  })

  it('a retry carries no cost tag, because it costs nothing', async () => {
    seed({ retryOf: 'earlier', questions: [rec('a'), rec('b')] })
    await renderStage()
    await screen.findByText('Question a')
    expect(screen.queryByText(/credits per question/)).not.toBeInTheDocument()
  })

  it('while a question loads, shows the loading text and the interviewer halo pulses (masarHalo)', async () => {
    let release!: (v: ReturnType<typeof q>) => void
    nextQuestion.mockReturnValueOnce(new Promise((res) => { release = res }))
    seed()
    await renderStage()
    expect(await screen.findByText(STRINGS.en['interview.loadingQuestion'])).toBeInTheDocument()
    expect(document.querySelector('.animate-masarHalo')).not.toBeNull()
    await act(async () => { release(q('Ready?')) })
    await screen.findByText('Ready?')
    expect(document.querySelector('.animate-masarHalo')).toBeNull()
  })

  it('with scoring off: a "scoring not available yet" card, a dash for history scores, and the device-only note', async () => {
    scorer.on = false
    seed({ id: 'past', questions: [rec('p', { answer: 'x' })], totalQuestions: 1 }, true)
    seed({ id: 'now' })
    nextQuestion.mockResolvedValue(q('First?'))
    await renderStage()
    const card = (await screen.findByRole('heading', { name: STRINGS.en['interview.scoresOff.title'] })).closest('div') as HTMLElement
    expect(within(card).getByText(STRINGS.en['interview.scoresOff'])).toBeInTheDocument()
    expect(screen.queryByText(STRINGS.en['interview.lastScore'])).not.toBeInTheDocument()
    const row = screen.getByRole('link', { name: /AI Developer/ })
    expect(within(row).getByText('—')).toBeInTheDocument()
    expect(within(row).getByText(STRINGS.en['interview.history.unscored'])).toHaveClass('sr-only')
    expect(screen.getByText(STRINGS.en['interview.history.local'])).toBeInTheDocument()
  })

  it('has the new strings in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    nextQuestion.mockResolvedValue(q('First?'))
    seed()
    await renderStage()
    expect(await screen.findByText(STRINGS.ar['interview.perQuestion'].replace('{n}', '3'))).toBeInTheDocument()
    expect(screen.getByText(STRINGS.ar['interview.history.local'])).toBeInTheDocument()
  })
})

describe('the interview loading state, from the handoff', () => {
  it('says "المُحاوِر يجهّز السؤال التالي…" in Arabic while the halo pulses, and only then', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first', annotateTerms: true })
    let release!: (v: ReturnType<typeof q>) => void
    nextQuestion.mockReturnValueOnce(new Promise((res) => { release = res }))
    seed()
    await renderStage()
    expect(await screen.findByText('المُحاوِر يجهّز السؤال التالي…')).toBeInTheDocument()
    expect(document.querySelectorAll('.animate-masarHalo')).toHaveLength(1)
    await act(async () => { release(q('First?')) })
    await screen.findByText('First?')
    expect(document.querySelector('.animate-masarHalo')).toBeNull()
    expect(screen.queryByText('المُحاوِر يجهّز السؤال التالي…')).not.toBeInTheDocument()
  })

  it('an empty wallet mid-interview names the interview price (3 a question), not the chat one', async () => {
    nextQuestion.mockRejectedValueOnce(httpError(402, { error: 'insufficient_credits' }))
    seed()
    await renderStage()
    const bar = await screen.findByTestId('mentor-upsell')
    expect(within(bar).getByText(STRINGS.en['interview.upsell.credits.body'])).toBeInTheDocument()
    expect(within(bar).getByRole('link', { name: STRINGS.en['mentor.upsell.credits.cta'] })).toHaveAttribute('href', '/billing')
  })
})
