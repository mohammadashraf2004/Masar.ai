import type { LearningCatalog } from './useLearningCatalog'

/**
 * Where `useLearningCatalog` keeps its in-flight/finished request.
 *
 * Its own module, with no import of the API client, so the test setup can clear
 * it between tests without dragging the real client into the module graph
 * before a test file has had the chance to mock it.
 */
let pending: Promise<LearningCatalog> | null = null

export const catalogCache = {
  get: () => pending,
  set: (promise: Promise<LearningCatalog> | null) => {
    pending = promise
  },
}

/** Forget the cached catalogue (tests, and the "sign out" of a long session). */
export function resetLearningCatalogCache() {
  pending = null
}
