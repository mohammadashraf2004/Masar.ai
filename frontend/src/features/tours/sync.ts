import { api, type TourRecordApi } from '@/lib/api'
import { getRecord, saveRecord, type TourRecord, type TourStatus } from './records'
import { TOURS, type TourId } from './registry'

/**
 * Moves tour progress onto the account (docs/backend-requests.md §6), with `records.ts`'s
 * localStorage kept as the cache eligibility reads and the offline fallback.
 *
 * The wire status is a superset of the local one: `in_progress` has no local meaning yet —
 * nothing here ever writes it, and a remote record carrying it is treated as not seen, same
 * as no record at all, so it never blocks the tour from running.
 */

const TO_WIRE: Record<TourStatus, 'completed' | 'skipped'> = { done: 'completed', skipped: 'skipped' }
const FROM_WIRE: Partial<Record<TourRecordApi['status'], TourStatus>> = { completed: 'done', skipped: 'skipped' }

function fromWire(rec: TourRecordApi): TourRecord | null {
  const status = FROM_WIRE[rec.status]
  return status ? { status, version: rec.version, at: rec.at } : null
}

// ─── The retry queue ─────────────────────────────────────────────────────────

const QUEUE_KEY = 'masar.tours.queue'

interface QueueEntry { userId: number; tourId: string; status: TourStatus; version: number; at: string }

function readQueue(): QueueEntry[] {
  try {
    const parsed: unknown = JSON.parse(window.localStorage.getItem(QUEUE_KEY) ?? '[]')
    return Array.isArray(parsed) ? (parsed as QueueEntry[]) : []
  } catch {
    return []
  }
}

function writeQueue(queue: QueueEntry[]): void {
  try {
    window.localStorage.setItem(QUEUE_KEY, JSON.stringify(queue))
  } catch {
    // Storage is blocked or full: the write is simply retried again next load.
  }
}

function enqueue(entry: QueueEntry): void {
  const rest = readQueue().filter((e) => !(e.userId === entry.userId && e.tourId === entry.tourId))
  writeQueue([...rest, entry])
}

async function send(entry: QueueEntry): Promise<boolean> {
  try {
    await api.putTour(entry.tourId, { status: TO_WIRE[entry.status], version: entry.version, at: entry.at })
    return true
  } catch {
    return false
  }
}

/** Push one record up now; queued for the next load if the request fails. Callers that do
 *  not need to know when it lands (TourProvider) simply do not await it. */
export function pushRecord(userId: number, tourId: TourId, record: TourRecord): Promise<void> {
  const entry: QueueEntry = { userId, tourId, status: record.status, version: record.version, at: record.at }
  return send(entry).then((ok) => { if (!ok) enqueue(entry) })
}

/** Retry whatever failed to push last time, for this account only. Each write is tried in
 *  order and only kept in the queue if it fails again — a transient failure on one tour
 *  must not reorder the others. */
export async function retryQueue(userId: number): Promise<void> {
  const mine = readQueue().filter((e) => e.userId === userId)
  if (mine.length === 0) return
  const stillFailing: QueueEntry[] = []
  for (const entry of mine) {
    if (!(await send(entry))) stillFailing.push(entry)
  }
  const others = readQueue().filter((e) => e.userId !== userId)
  writeQueue([...others, ...stillFailing])
}

// ─── Writing ─────────────────────────────────────────────────────────────────

/** Write locally and push to the server immediately. The write is synchronous; the push is
 *  not something callers need to wait for, though the promise is there if a test wants to. */
export function saveAndSync(userId: number, tourId: TourId, rec: Omit<TourRecord, 'at'> & { at?: string }): Promise<void> {
  saveRecord(userId, tourId, rec)
  const saved = getRecord(userId, tourId)
  return saved ? pushRecord(userId, tourId, saved) : Promise.resolve()
}

// ─── Merging on login ────────────────────────────────────────────────────────

/**
 * Fetch every record the account has and merge it with what is local: whichever side's `at`
 * is newer wins. A local-only record, or one newer than the server's, is pushed up — this is
 * what carries an existing user's pre-migration localStorage onto their account the first
 * time they load the app after this feature ships.
 */
async function mergeFromServer(userId: number): Promise<void> {
  let remote: TourRecordApi[]
  try {
    remote = await api.getMyTours()
  } catch {
    return   // offline, or the request failed: localStorage is already the fallback
  }
  const remoteById = new Map(remote.map((r) => [r.tour_id, r]))
  const ids = Array.from(new Set<string>([...TOURS.map((t) => t.id), ...Array.from(remoteById.keys())]))
  for (const tourId of ids) {
    const id = tourId as TourId
    const local = getRecord(userId, id)
    const wire = remoteById.get(tourId)
    const fromServer = wire ? fromWire(wire) : null
    if (fromServer && (!local || fromServer.at >= local.at)) {
      const same = local && local.at === fromServer.at && local.status === fromServer.status && local.version === fromServer.version
      if (!same) saveRecord(userId, id, fromServer)
    } else if (local && (!wire || local.at > wire.at)) {
      pushRecord(userId, id, local)
    }
  }
}

const syncedThisSession = new Set<number>()

/** Called once per account per app load: flushes any queued retry, then merges with the
 *  server. Safe to call on every mount — the merge itself only runs once per session. */
export async function ensureSynced(userId: number): Promise<void> {
  await retryQueue(userId)
  if (syncedThisSession.has(userId)) return
  syncedThisSession.add(userId)
  await mergeFromServer(userId)
}

export function resetSyncedForTests(): void {
  syncedThisSession.clear()
}
