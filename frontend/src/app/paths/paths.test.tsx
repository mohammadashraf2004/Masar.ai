import { beforeEach, describe, expect, it, vi } from 'vitest'
import { redirect } from 'next/navigation'
import LegacyPathsPage from '@/app/paths/page'
import LegacyPathPage from '@/app/paths/[slug]/page'

vi.mock('next/navigation', () => ({ redirect: vi.fn() }))

describe('legacy Paths redirects', () => {
  beforeEach(() => vi.mocked(redirect).mockClear())

  it('redirects /paths to Tracks', () => {
    LegacyPathsPage()
    expect(redirect).toHaveBeenCalledWith('/tracks')
  })

  it('keeps a reliable fixed-track slug', async () => {
    await LegacyPathPage({ params: Promise.resolve({ slug: 'ai-engineer' }) })
    expect(redirect).toHaveBeenCalledWith('/tracks/ai-engineer')
  })

  it('sends generated and unknown paths to the Tracks index', async () => {
    await LegacyPathPage({ params: Promise.resolve({ slug: 'custom' }) })
    expect(redirect).toHaveBeenCalledWith('/tracks')
  })
})
