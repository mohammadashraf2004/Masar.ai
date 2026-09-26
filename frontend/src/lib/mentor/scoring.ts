import { mentorMocksEnabled } from '@/lib/mentor/mocks'
import type { AnswerScore, InterviewLanguage } from '@/lib/mentor/interview'

export interface ScoreRequest {
  question: string
  answer: string
  language: InterviewLanguage
}

/**
 * Something that reads an interview answer and scores it out of 10 on accuracy, structure and
 * clarity, with a note.
 *
 * The backend cannot do this: it writes questions and never sees the answer (see
 * docs/backend-requests.md). `MockAnswerScorer` stands in, and is off in a production build.
 */
export interface AnswerScorer {
  readonly isMock: boolean
  score(request: ScoreRequest): Promise<AnswerScore>
}

const clamp = (n: number) => Math.max(1, Math.min(9, Math.round(n)))

function words(text: string): string[] {
  return text.trim().split(/\s+/).filter(Boolean)
}

/**
 * NOT an evaluation. It looks at how long an answer is, how many sentences it has and whether it
 * mentions a number, and gives the same three scores for the same text every time. That is enough
 * to build and check the bars, the report and "retry weak questions"; it cannot tell a right
 * answer from a wrong one, and the screen says so wherever it shows these scores.
 */
export class MockAnswerScorer implements AnswerScorer {
  readonly isMock = true
  private readonly delayMs: number

  constructor({ delayMs = 600 }: { delayMs?: number } = {}) {
    this.delayMs = delayMs
  }

  async score({ answer }: ScoreRequest): Promise<AnswerScore> {
    if (this.delayMs > 0) await new Promise((resolve) => setTimeout(resolve, this.delayMs))
    const count = words(answer).length
    const sentences = answer.split(/[.!?؟\n]+/).filter((s) => s.trim()).length
    const hasNumber = /\d/.test(answer)

    const accuracy = clamp(3.5 + (Math.min(count, 60) / 60) * 4 + (hasNumber ? 1.5 : 0))
    const structure = clamp(3.5 + (Math.min(sentences, 4) / 4) * 4 + (count >= 25 ? 1 : 0))
    const clarity = clamp(count > 140 ? 6 : 4 + (Math.min(count, 20) / 20) * 4 + (count <= 90 ? 1 : 0))

    return {
      accuracy,
      structure,
      clarity,
      note: { key: count < 15 ? 'interview.note.short' : 'interview.note.solid' },
    }
  }
}

/** The scorer the interview uses, or `null` when there is none (no scores are shown then). */
export function getAnswerScorer(): AnswerScorer | null {
  return mentorMocksEnabled() ? new MockAnswerScorer() : null
}
