import type { ReactNode } from 'react'
import { render, screen, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import ChallengesPage from '@/app/challenges/page'

vi.mock('@/components/layout/AppShell', () => ({ AppShell: ({ children }: { children: ReactNode }) => <>{children}</> }))
vi.mock('@/lib/api', () => ({ api: { getChallenges: vi.fn(), getLabProjects: vi.fn() } }))
import { api } from '@/lib/api'
import { useAuthStore } from '@/lib/store'

beforeEach(() => {
  // The signed-in page (the signed-out one is page.anonymous.test.tsx).
  useAuthStore.setState({ token: 'tok', user: null, expiresAt: null, _hasHydrated: true })
  vi.mocked(api.getChallenges).mockResolvedValue([{
    id: 1, title: 'Clean the Sales Ledger', slug: 'clean-sales', difficulty: 'beginner', credit_cost: 20,
    passing_score: 70, description: 'Dirty data.', tags: [], is_enrolled: false, best_score: null, status: null,
  }])
  vi.mocked(api.getLabProjects).mockResolvedValue([{
    slug: 'masar-commerce-analysis', title: 'Masar Commerce — Business Performance Analysis',
    title_ar: 'مسار كوميرس — تحليل أداء الأعمال', summary: 'Analyse a year of orders.', summary_ar: null,
    difficulty: 'beginner', estimated_hours: 2, track: { slug: 'data-analyst', title: 'Data Analyst', title_ar: null },
    milestone_count: 3, task_count: 3, attempt: null,
  }])
})

describe('Challenges page', () => {
  it('lists guided projects above the existing challenges, which are unchanged', async () => {
    render(<ChallengesPage />)
    const section = await screen.findByRole('region', { name: 'Guided projects' })
    expect(within(section).getByRole('heading', { name: 'Masar Commerce — Business Performance Analysis' })).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Clean the Sales Ledger' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Unlock for 20 credits/ })).toBeInTheDocument()
  })

  it('does not render an empty legacy challenge panel when only guided projects exist', async () => {
    vi.mocked(api.getChallenges).mockResolvedValue([])

    render(<ChallengesPage />)

    expect(await screen.findByRole('heading', { name: 'Masar Commerce — Business Performance Analysis' })).toBeInTheDocument()
    expect(screen.queryByText('No challenges found')).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'All Challenges' })).not.toBeInTheDocument()
  })
})
