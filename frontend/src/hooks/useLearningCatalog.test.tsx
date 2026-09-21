import { renderHook, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useLearningCatalog } from '@/hooks/useLearningCatalog'
import { CATALOG } from '@/test/fixtures'

vi.mock('@/lib/api', () => ({
  api: { getLearningLevels: vi.fn(), getLearningFields: vi.fn(), getCareerGoals: vi.fn() },
}))
import { api } from '@/lib/api'

beforeEach(() => {
  vi.mocked(api.getLearningLevels).mockResolvedValue(CATALOG.levels)
  vi.mocked(api.getLearningFields).mockResolvedValue(CATALOG.fields)
  vi.mocked(api.getCareerGoals).mockResolvedValue(CATALOG.goals)
})

describe('useLearningCatalog', () => {
  it('loads levels, fields and career goals from the API', async () => {
    const { result } = renderHook(() => useLearningCatalog())
    expect(result.current.loading).toBe(true)
    await waitFor(() => expect(result.current.catalog).not.toBeNull())
    expect(result.current.catalog?.fields.map((f) => f.slug)).toContain('multimodal')
    expect(result.current.loading).toBe(false)
  })

  it('shares one request between every screen that asks in a session', async () => {
    const a = renderHook(() => useLearningCatalog())
    const b = renderHook(() => useLearningCatalog())
    await waitFor(() => expect(a.result.current.catalog).not.toBeNull())
    await waitFor(() => expect(b.result.current.catalog).not.toBeNull())
    expect(api.getLearningFields).toHaveBeenCalledTimes(1)
  })

  it('reports a failure', async () => {
    vi.mocked(api.getLearningFields).mockRejectedValue(new Error('down'))
    const { result } = renderHook(() => useLearningCatalog())
    await waitFor(() => expect(result.current.error).toBe(true))
    expect(result.current.loading).toBe(false)
  })

  it('does not remember a failure — asking again retries', async () => {
    vi.mocked(api.getLearningFields).mockRejectedValueOnce(new Error('down'))
    const first = renderHook(() => useLearningCatalog())
    await waitFor(() => expect(first.result.current.error).toBe(true))

    const second = renderHook(() => useLearningCatalog())
    await waitFor(() => expect(second.result.current.catalog).not.toBeNull())
    expect(api.getLearningFields).toHaveBeenCalledTimes(2)
  })
})
