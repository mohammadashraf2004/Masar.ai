import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import LearnPage from '@/app/learn/masar/page'
import { NEEDS_ONBOARDING, profile } from '@/test/fixtures'
import { router } from '@/test/nav'

vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ user: null, isAuthenticated: true, isLoading: false }),
  useGuest: () => {},
  useSession: () => ({ user: null, isAuthenticated: true, isLoading: false }), useNextParam: () => null,
}))
vi.mock('@/components/layout/AppShell', async () => {
  const { createElement } = await import('react')
  return { AppShell: ({ children }: { children: React.ReactNode }) => createElement('div', null, children) }
})
vi.mock('@/components/layout/PageHeader', async () => {
  const { createElement } = await import('react')
  return { PageHeader: ({ title }: { title: string }) => createElement('h1', null, title) }
})
vi.mock('@/components/learning/TrackWorkflowPath', () => ({
  TrackWorkflowPath: ({ goal }: { goal: string }) => <section><h2>Track Workflow</h2><span>{goal}</span></section>,
}))
vi.mock('@/lib/api', () => ({ api: { getMyLearningProfile: vi.fn() } }))
import { api } from '@/lib/api'

beforeEach(() => {
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile())
})

describe('Your Masar track workflow', () => {
  it('keeps Track Workflow and removes the old Your Learning Path UI and fetch', async () => {
    render(<LearnPage />)
    expect(await screen.findByRole('heading', { name: 'Track Workflow' })).toBeInTheDocument()
    expect(screen.getByText('ai-engineer')).toBeInTheDocument()
    expect(screen.queryByText('Your Learning Path')).not.toBeInTheDocument()
    expect(screen.queryByText('Your skill gaps')).not.toBeInTheDocument()
  })

  it('keeps valid profile and certificate actions', async () => {
    render(<LearnPage />)
    await screen.findByRole('heading', { name: 'Track Workflow' })
    expect(screen.getByRole('link', { name: /Edit my answers/ })).toHaveAttribute('href', '/profile/learning')
    expect(screen.getByRole('link', { name: /Certificates/ })).toHaveAttribute('href', '/certificates')
  })

  it('sends a learner who still needs onboarding to the profile flow', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    render(<LearnPage />)
    await waitFor(() => expect(router.replace).toHaveBeenCalledWith('/onboarding/learning-profile'))
    expect(screen.queryByRole('heading', { name: 'Track Workflow' })).not.toBeInTheDocument()
  })

  it('surfaces a load failure and retries', async () => {
    const user = userEvent.setup()
    vi.mocked(api.getMyLearningProfile).mockRejectedValueOnce(new Error('down'))
    render(<LearnPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load your Masar')
    await user.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByRole('heading', { name: 'Track Workflow' })).toBeInTheDocument()
  })
})
