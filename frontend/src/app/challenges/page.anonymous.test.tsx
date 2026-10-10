import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import type { ReactNode } from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import ChallengesPage from '@/app/challenges/page'
import { AuthPromptDialog, useAuthPrompt } from '@/components/auth/AuthPrompt'
import { useAuthStore } from '@/lib/store'

// A signed-out visitor on the challenges page: the real hooks, no session.
vi.mock('next/navigation', () => ({
  useRouter: () => ({ replace: vi.fn(), push: vi.fn() }),
  usePathname: () => '/challenges',
}))
vi.mock('@/components/layout/AppShell', () => ({
  AppShell: ({ children }: { children: ReactNode }) => <>{children}<AuthPromptDialog /></>,
}))
vi.mock('@/features/project-lab/LabProjectsSection', () => ({ LabProjectsSection: () => null }))
vi.mock('@/lib/api', () => ({
  api: {
    getChallenges: vi.fn(),
    getChallenge: vi.fn(),
    getPublicChallenges: vi.fn(),
    enrollChallenge: vi.fn(),
  },
}))
import { api } from '@/lib/api'

const card = {
  id: 1, title: 'Clean the sales export', slug: 'clean-sales', difficulty: 'beginner', credit_cost: 25,
  passing_score: 70, max_attempts: 3, description: 'Deduplicate and normalise a messy export.', tags: ['pandas'],
}

beforeEach(() => {
  useAuthStore.setState({ token: null, user: null, expiresAt: null, _hasHydrated: true })
  useAuthPrompt.setState({ open: false, next: null })
  vi.mocked(api.getPublicChallenges).mockResolvedValue([card])
})
afterEach(() => window.history.replaceState({}, '', '/'))

describe('challenges for a signed-out visitor', () => {
  it('lists the public catalogue and never asks for the signed-in list or a challenge body', async () => {
    render(<ChallengesPage />)
    expect(await screen.findByText('Clean the sales export')).toBeInTheDocument()
    expect(api.getChallenges).not.toHaveBeenCalled()
    expect(screen.queryByRole('button', { name: 'My Challenges' })).toBeNull()
    expect(screen.queryByRole('button', { name: /Unlock for/ })).toBeNull()
    expect(screen.getByRole('button', { name: /View challenge/ })).toBeInTheDocument()
  })

  it('opens an overview from the card alone, and joining asks them to sign in', async () => {
    const u = userEvent.setup()
    render(<ChallengesPage />)
    await u.click(await screen.findByRole('button', { name: /View challenge/ }))
    expect(screen.getByRole('heading', { name: 'Clean the sales export' })).toBeInTheDocument()
    expect(screen.getByText(/The dataset, hints and submission open once you sign in/)).toBeInTheDocument()
    expect(api.getChallenge).not.toHaveBeenCalled()
    expect(api.enrollChallenge).not.toHaveBeenCalled()

    await u.click(screen.getByRole('button', { name: 'Sign in to join challenge' }))
    const dialog = screen.getByRole('dialog', { name: 'Sign in to continue learning' })
    expect(within(dialog).getByRole('link', { name: 'Sign in' }))
      .toHaveAttribute('href', '/auth/login?next=%2Fchallenges%3Fchallenge%3Dclean-sales')
  })

  it('opens the challenge named in the address (where sign-in sends them back)', async () => {
    window.history.replaceState({}, '', '/challenges?challenge=clean-sales')
    render(<ChallengesPage />)
    expect(await screen.findByRole('button', { name: 'Sign in to join challenge' })).toBeInTheDocument()
  })
})

describe('challenges once signed in', () => {
  it('opens the full challenge named in the address', async () => {
    useAuthStore.setState({ token: 'tok', user: { id: 1 } as never, expiresAt: null, _hasHydrated: true })
    window.history.replaceState({}, '', '/challenges?challenge=clean-sales')
    vi.mocked(api.getChallenges).mockResolvedValue([{ ...card, is_enrolled: false, best_score: null, status: null }])
    vi.mocked(api.getChallenge).mockResolvedValue({
      ...card, is_enrolled: false, best_score: null, status: null, dataset_description: '', dataset_filename: 'x.csv',
      dirty_dataset: [], grading_rubric: [], hints: [], attempts_used: 0,
    })
    render(<ChallengesPage />)
    expect(await screen.findByRole('button', { name: /Unlock — 25 credits/ })).toBeInTheDocument()
    expect(api.getChallenge).toHaveBeenCalledWith('clean-sales')
    expect(api.getPublicChallenges).not.toHaveBeenCalled()
  })
})
