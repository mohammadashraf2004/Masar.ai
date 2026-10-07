import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { getRecord, saveRecord } from './records'

vi.mock('@/lib/api', () => ({ api: { getMyTours: vi.fn(), putTour: vi.fn() } }))
import { api } from '@/lib/api'
import { ensureSynced, pushRecord, resetSyncedForTests, retryQueue, saveAndSync } from './sync'

const USER = 42
const now = () => new Date().toISOString()
const earlier = () => new Date(Date.now() - 60_000).toISOString()
const later = () => new Date(Date.now() + 60_000).toISOString()

beforeEach(() => {
  resetSyncedForTests()
  vi.mocked(api.getMyTours).mockResolvedValue([])
  vi.mocked(api.putTour).mockResolvedValue({ tour_id: 'onboarding', status: 'completed', version: 1, at: now() })
})

afterEach(() => {
  window.localStorage.clear()
})

// ─── Merging ────────────────────────────────────────────────────────────────

describe('merging on login', () => {
  it('takes the server record when there is nothing local', async () => {
    vi.mocked(api.getMyTours).mockResolvedValue([{ tour_id: 'onboarding', status: 'completed', version: 1, at: now() }])
    await ensureSynced(USER)
    expect(getRecord(USER, 'onboarding')).toMatchObject({ status: 'done', version: 1 })
  })

  it('takes the server record when it is newer than the local one', async () => {
    saveRecord(USER, 'onboarding', { status: 'skipped', version: 1, at: earlier() })
    vi.mocked(api.getMyTours).mockResolvedValue([{ tour_id: 'onboarding', status: 'completed', version: 1, at: later() }])
    await ensureSynced(USER)
    expect(getRecord(USER, 'onboarding')).toMatchObject({ status: 'done' })
  })

  it('keeps the local record, and pushes it up, when it is newer than the server\'s', async () => {
    saveRecord(USER, 'onboarding', { status: 'done', version: 1, at: later() })
    vi.mocked(api.getMyTours).mockResolvedValue([{ tour_id: 'onboarding', status: 'skipped', version: 1, at: earlier() }])
    await ensureSynced(USER)
    expect(getRecord(USER, 'onboarding')).toMatchObject({ status: 'done' })
    expect(api.putTour).toHaveBeenCalledWith('onboarding', expect.objectContaining({ status: 'completed' }))
  })

  it('copies the server\'s version even when it does not match the current one — eligibility decides what that means, not the merge', async () => {
    vi.mocked(api.getMyTours).mockResolvedValue([{ tour_id: 'onboarding', status: 'completed', version: 0, at: now() }])
    await ensureSynced(USER)
    expect(getRecord(USER, 'onboarding')).toMatchObject({ version: 0 })
  })

  it('treats an in_progress record as not seen — it is never written locally', async () => {
    vi.mocked(api.getMyTours).mockResolvedValue([{ tour_id: 'onboarding', status: 'in_progress', version: 1, at: now() }])
    await ensureSynced(USER)
    expect(getRecord(USER, 'onboarding')).toBeUndefined()
  })
})

// ─── Migrating an existing browser's local-only records ─────────────────────

describe('migrating local-only records', () => {
  it('pushes a record that only exists locally up to the server', async () => {
    saveRecord(USER, 'language', { status: 'done', version: 1, at: earlier() })
    vi.mocked(api.getMyTours).mockResolvedValue([])
    await ensureSynced(USER)
    expect(api.putTour).toHaveBeenCalledWith('language', expect.objectContaining({ status: 'completed', version: 1 }))
    expect(getRecord(USER, 'language')).toMatchObject({ status: 'done' })   // unchanged locally
  })

  it('only merges once per session — a second call makes no second fetch', async () => {
    await ensureSynced(USER)
    await ensureSynced(USER)
    expect(api.getMyTours).toHaveBeenCalledTimes(1)
  })
})

// ─── Offline / failure fallback ──────────────────────────────────────────────

describe('offline or a failed request', () => {
  it('leaves local records untouched when the fetch fails, and does not throw', async () => {
    saveRecord(USER, 'onboarding', { status: 'done', version: 1, at: now() })
    vi.mocked(api.getMyTours).mockRejectedValue(new Error('network error'))
    await expect(ensureSynced(USER)).resolves.toBeUndefined()
    expect(getRecord(USER, 'onboarding')).toMatchObject({ status: 'done' })
  })
})

// ─── The retry queue ──────────────────────────────────────────────────────────

describe('the retry queue', () => {
  it('queues a push that fails, and retries it on the next call', async () => {
    vi.mocked(api.putTour).mockRejectedValueOnce(new Error('network error'))
    await saveAndSync(USER, 'onboarding', { status: 'done', version: 1 })
    expect(api.putTour).toHaveBeenCalledTimes(1)

    vi.mocked(api.putTour).mockResolvedValue({ tour_id: 'onboarding', status: 'completed', version: 1, at: now() })
    await retryQueue(USER)
    expect(api.putTour).toHaveBeenCalledTimes(2)

    // A second retry has nothing left to send.
    await retryQueue(USER)
    expect(api.putTour).toHaveBeenCalledTimes(2)
  })

  it('drops a queued write once it succeeds, rather than resending it forever', async () => {
    vi.mocked(api.putTour).mockRejectedValueOnce(new Error('network error'))
    await pushRecord(USER, 'onboarding', { status: 'done', version: 1, at: now() })
    expect(api.putTour).toHaveBeenCalledTimes(1)

    vi.mocked(api.putTour).mockResolvedValue({ tour_id: 'onboarding', status: 'completed', version: 1, at: now() })
    await retryQueue(USER)
    await retryQueue(USER)
    expect(api.putTour).toHaveBeenCalledTimes(2)
  })

  it('does not retry another account\'s queued write', async () => {
    vi.mocked(api.putTour).mockRejectedValue(new Error('network error'))
    await pushRecord(USER, 'onboarding', { status: 'done', version: 1, at: now() })
    expect(api.putTour).toHaveBeenCalledTimes(1)

    await retryQueue(USER + 1)
    expect(api.putTour).toHaveBeenCalledTimes(1)   // not retried under the wrong account
  })
})

// ─── Writing ──────────────────────────────────────────────────────────────────

describe('saveAndSync', () => {
  it('writes locally before the network call is even sent', () => {
    saveAndSync(USER, 'onboarding', { status: 'skipped', version: 1 })
    expect(getRecord(USER, 'onboarding')).toMatchObject({ status: 'skipped', version: 1 })
  })

  it('sends the local status as the wire one', async () => {
    await saveAndSync(USER, 'onboarding', { status: 'done', version: 2 })
    expect(api.putTour).toHaveBeenCalledWith('onboarding', expect.objectContaining({ status: 'completed', version: 2 }))
  })
})
