import { mentorMocksEnabled } from '@/lib/mentor/mocks'

/** What the design says the Free plan includes: "20 messages a day on Free, unlimited on Career". */
export const FREE_DAILY_LIMIT = 20

export interface QuotaStatus {
  limit: number
  used: number
  left: number
  exhausted: boolean
}

/**
 * A daily mentor-message allowance for the plan the account is on.
 *
 * The backend has credits (2 per message, a 402 when they run out) and no plan quota, so this
 * seam has no real implementation. `MockMentorQuota` counts in this browser; the real one will
 * be whatever the API reports (see docs/backend-requests.md).
 */
export interface MentorQuota {
  readonly isMock: boolean
  status(): QuotaStatus
  /** Counts one delivered message and returns the new status. */
  consume(): QuotaStatus
}

const KEY = 'masar:mock-mentor-quota:v1'

interface Options {
  limit?: number
  now?: () => Date
  storage?: Pick<Storage, 'getItem' | 'setItem'> | null
}

function statusOf(limit: number, used: number): QuotaStatus {
  const left = Math.max(0, limit - used)
  return { limit, used, left, exhausted: left === 0 }
}

/**
 * Counts messages per calendar day in localStorage. Not a limit anyone is held to: clearing the
 * browser's data resets it. It exists so the count, the low-quota state and the upsell can be
 * built and seen.
 */
export class MockMentorQuota implements MentorQuota {
  readonly isMock = true
  private readonly limit: number
  private readonly now: () => Date
  private readonly storage: Pick<Storage, 'getItem' | 'setItem'> | null

  constructor({ limit = FREE_DAILY_LIMIT, now = () => new Date(), storage }: Options = {}) {
    this.limit = limit
    this.now = now
    this.storage = storage === undefined ? browserStorage() : storage
  }

  private today() {
    const d = this.now()
    const pad = (n: number) => String(n).padStart(2, '0')
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
  }

  private read(): number {
    try {
      const raw = this.storage?.getItem(KEY)
      if (!raw) return 0
      const parsed = JSON.parse(raw) as { day?: unknown; used?: unknown }
      return parsed.day === this.today() && typeof parsed.used === 'number' ? parsed.used : 0
    } catch {
      return 0
    }
  }

  private write(used: number) {
    try {
      this.storage?.setItem(KEY, JSON.stringify({ day: this.today(), used }))
    } catch {
      // Private mode or blocked storage: the count just does not persist.
    }
  }

  status(): QuotaStatus {
    return statusOf(this.limit, this.read())
  }

  consume(): QuotaStatus {
    const used = this.read() + 1
    this.write(used)
    return statusOf(this.limit, used)
  }

  /** Sets today's count, for `?mockQuotaUsed=` (see `mockQuotaUsedFromUrl`). */
  setUsed(used: number) {
    this.write(Math.max(0, Math.floor(used)))
  }
}

function browserStorage(): Storage | null {
  try {
    return typeof window === 'undefined' ? null : window.localStorage
  } catch {
    return null
  }
}

/**
 * `?mockQuotaUsed=20` puts today's count at 20, so the "you have used today's messages" state can
 * be reached without sending 20 messages: the counterpart of billing's `?mockPayment=`.
 */
export function mockQuotaUsedFromUrl(search: string): number | null {
  const raw = new URLSearchParams(search).get('mockQuotaUsed')
  if (raw === null || !/^\d{1,4}$/.test(raw)) return null
  return Number(raw)
}

/** The quota the page counts against, or `null` when there is none to show. */
export function getMentorQuota(search = ''): MentorQuota | null {
  if (!mentorMocksEnabled()) return null
  const quota = new MockMentorQuota()
  const forced = mockQuotaUsedFromUrl(search)
  if (forced !== null) quota.setUsed(forced)
  return quota
}
