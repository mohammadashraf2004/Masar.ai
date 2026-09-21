'use client'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { catalogCache } from './learningCatalogCache'
import type { CareerGoal, LearningField, LearningLevel } from '@/types'

export interface LearningCatalog {
  levels: LearningLevel[]
  fields: LearningField[]
  goals: CareerGoal[]
}

/**
 * The learning vocabulary — levels, fields, career goals — as the backend
 * serves it. Nothing about it is hard-coded in the interface: a field added on
 * the server shows up here, in onboarding, in Explore and in the filters.
 *
 * Held in a shared promise (see learningCatalogCache) so the screens that need
 * it in one session make a single fetch. A failure is not cached, so navigating
 * away and back retries instead of remembering the error.
 */
function load(): Promise<LearningCatalog> {
  let request = catalogCache.get()
  if (!request) {
    request = Promise.all([api.getLearningLevels(), api.getLearningFields(), api.getCareerGoals()])
      .then(([levels, fields, goals]) => ({ levels, fields, goals }))
      .catch((error) => {
        catalogCache.set(null)
        throw error
      })
    catalogCache.set(request)
  }
  return request
}

export function useLearningCatalog() {
  const [catalog, setCatalog] = useState<LearningCatalog | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    let cancelled = false
    load()
      .then((c) => !cancelled && setCatalog(c))
      .catch(() => !cancelled && setError(true))
    return () => {
      cancelled = true
    }
  }, [])

  return { catalog, error, loading: !catalog && !error }
}
