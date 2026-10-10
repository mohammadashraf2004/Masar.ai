import type { ReactNode } from 'react'
import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import CommunityPage from '@/app/community/page'

// The page owns its own axios instance; `http` stands in for it.
const http = vi.hoisted(() => ({
  get: vi.fn(),
  post: vi.fn(),
  interceptors: { request: { use: vi.fn() }, response: { use: vi.fn() } },
}))
vi.mock('axios', () => ({ default: { create: () => http } }))

const auth = vi.hoisted(() => ({ isLoading: false }))
vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: true, isLoading: auth.isLoading }),
}))
vi.mock('@/components/layout/AppShell', () => ({ AppShell: ({ children }: { children: ReactNode }) => <>{children}</> }))

const author = { id: 1, full_name: 'Layan Al-Harbi', experience_level: 'beginner', overall_readiness_score: 40 }
const post = (id: number, title: string, post_type = 'discussion') => ({
  id, post_type, title, content: `${title} body`, tags: [], likes_count: 0, comments_count: 0,
  created_at: '2026-10-01T10:00:00Z', author, liked_by_me: false, comments: [],
})
const feed = (...posts: ReturnType<typeof post>[]) => ({ data: { posts, total: posts.length } })

function deferred<T>() {
  let resolve!: (value: T) => void
  let reject!: (reason: unknown) => void
  const promise = new Promise<T>((res, rej) => { resolve = res; reject = rej })
  return { promise, resolve, reject }
}

const feedCalls = () => http.get.mock.calls.filter(([url]) => url === '/community/feed')
const FIRST = { params: { page: '1', per_page: '20' } }
const PROBLEMS = { params: { page: '1', per_page: '20', post_type: 'problem' } }

beforeEach(() => {
  http.get.mockReset()
  http.post.mockReset()
  auth.isLoading = false
})

describe('Community feed', () => {
  it('shows a spinner, asks for the feed once, then lists the posts', async () => {
    const pending = deferred<ReturnType<typeof feed>>()
    http.get.mockReturnValue(pending.promise)
    render(<CommunityPage />)

    expect(screen.getByRole('status')).toBeInTheDocument()
    await act(async () => { pending.resolve(feed(post(1, 'How do I fine-tune?'), post(2, 'My first agent'))) })

    expect(await screen.findByText('How do I fine-tune?')).toBeInTheDocument()
    expect(screen.getByText('My first agent')).toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(feedCalls()).toEqual([['/community/feed', FIRST]])
  })

  it('does not ask for the feed until the session is known', async () => {
    auth.isLoading = true
    http.get.mockResolvedValue(feed(post(1, 'Signed-in feed')))
    const { rerender } = render(<CommunityPage />)

    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(http.get).not.toHaveBeenCalled()

    auth.isLoading = false
    rerender(<CommunityPage />)
    expect(await screen.findByText('Signed-in feed')).toBeInTheDocument()
    expect(feedCalls()).toHaveLength(1)
  })

  it('filters by post type, shows the spinner while it loads, and clears the filter again', async () => {
    const user = userEvent.setup()
    http.get.mockResolvedValueOnce(feed(post(1, 'Everything post')))
    render(<CommunityPage />)
    expect(await screen.findByText('Everything post')).toBeInTheDocument()

    const problems = deferred<ReturnType<typeof feed>>()
    http.get.mockReturnValueOnce(problems.promise)
    await user.click(screen.getByRole('button', { name: 'Problem' }))

    // The old posts give way to the spinner at once, not after the request settles.
    expect(screen.queryByText('Everything post')).not.toBeInTheDocument()
    expect(screen.getByRole('status')).toBeInTheDocument()
    await act(async () => { problems.resolve(feed(post(2, 'Stuck on CUDA', 'problem'))) })
    expect(await screen.findByText('Stuck on CUDA')).toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(feedCalls()[1]).toEqual(['/community/feed', PROBLEMS])

    http.get.mockResolvedValueOnce(feed(post(1, 'Everything post')))
    await user.click(screen.getByRole('button', { name: 'All' }))
    expect(await screen.findByText('Everything post')).toBeInTheDocument()
    expect(feedCalls()[2]).toEqual(['/community/feed', FIRST])
  })

  it('ignores a slow answer for a filter the learner has already left', async () => {
    const user = userEvent.setup()
    const everything = deferred<ReturnType<typeof feed>>()
    const problems = deferred<ReturnType<typeof feed>>()
    http.get.mockReturnValueOnce(everything.promise).mockReturnValueOnce(problems.promise)
    render(<CommunityPage />)

    await user.click(screen.getByRole('button', { name: 'Problem' }))
    await act(async () => { problems.resolve(feed(post(2, 'Stuck on CUDA', 'problem'))) })
    expect(await screen.findByText('Stuck on CUDA')).toBeInTheDocument()

    // The first request finally answers; it must not overwrite the filtered list.
    await act(async () => { everything.resolve(feed(post(1, 'Stale unfiltered post'))) })
    expect(screen.getByText('Stuck on CUDA')).toBeInTheDocument()
    expect(screen.queryByText('Stale unfiltered post')).not.toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('survives a failed load: the spinner stops, the empty state shows, and a filter still works', async () => {
    const user = userEvent.setup()
    http.get.mockRejectedValueOnce(new Error('network down'))
    render(<CommunityPage />)

    expect(await screen.findByText('No posts yet')).toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()

    http.get.mockResolvedValueOnce(feed(post(3, 'Back online', 'project')))
    await user.click(screen.getByRole('button', { name: 'Project' }))
    await waitFor(() => expect(screen.getByText('Back online')).toBeInTheDocument())
    expect(screen.queryByText('No posts yet')).not.toBeInTheDocument()
  })
})
