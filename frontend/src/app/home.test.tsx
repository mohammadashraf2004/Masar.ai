import { render, screen, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import Home from '@/app/page'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import { NEEDS_ONBOARDING, path, profile } from '@/test/fixtures'
import { expectLinkStyledAsButton, expectMirroredArrow } from '@/test/interactive'
import type { User } from '@/types'

vi.mock('@/components/layout/AppShell', async () => {
  const { createElement } = await import('react')
  return { AppShell: ({ children }: { children: React.ReactNode }) => createElement('div', { 'data-testid': 'shell' }, children) }
})
vi.mock('@/components/layout/PageHeader', async () => {
  const { createElement } = await import('react')
  return { PageHeader: ({ title, wrapTitle }: { title: string; wrapTitle?: boolean }) =>
    createElement('h1', { 'data-wrap-title': wrapTitle ? 'true' : undefined }, title) }
})
vi.mock('@/lib/api', () => ({ api: { getMyLearningProfile: vi.fn(), getMyLearningPath: vi.fn() } }))
import { api } from '@/lib/api'

const signedIn = () =>
  useAuthStore.setState({ token: 'tok', user: { full_name: 'Amira Hassan' } as User, expiresAt: null, _hasHydrated: true })
const signedOut = () => useAuthStore.setState({ token: null, user: null, expiresAt: null, _hasHydrated: true })

beforeEach(() => {
  vi.mocked(api.getMyLearningProfile).mockResolvedValue(profile())
  vi.mocked(api.getMyLearningPath).mockResolvedValue(path())
  signedOut()
})

describe('home — a signed-in learner', () => {
  beforeEach(signedIn)

  it('greets them and shows the compact roadmap card', async () => {
    render(<Home />)
    expect(screen.getByRole('heading', { name: 'Welcome back, Amira' })).toBeInTheDocument()
    expect(await screen.findByText('Your Masar')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'AI Engineer' })).toBeInTheDocument()
    expect(screen.getByText('NLP & LLMs')).toBeInTheDocument()
    expect(screen.getByText('72%')).toBeInTheDocument()
    expect(screen.getByText("You're currently learning:").nextElementSibling).toHaveTextContent('LangChain')
    expect(screen.getByText('Next:').nextElementSibling).toHaveTextContent('RAG & Knowledge Systems')
    expect(screen.getByRole('link', { name: /Continue Roadmap/ })).toHaveAttribute('href', '/learn')
  })

  it('lets the greeting wrap onto two lines, as the dashboard greeting does, rather than cutting it off on a phone', async () => {
    render(<Home />)
    expect(screen.getByRole('heading', { name: 'Welcome back, Amira' })).toHaveAttribute('data-wrap-title', 'true')
    await screen.findByText('Your Masar')
  })

  it('does not show the marketing page', async () => {
    render(<Home />)
    await screen.findByText('Your Masar')
    expect(screen.queryByRole('link', { name: 'Create account' })).toBeNull()
    expect(screen.queryByText('Arabic-first lessons')).toBeNull()
  })

  it('invites them to build a roadmap when they have none', async () => {
    vi.mocked(api.getMyLearningProfile).mockResolvedValue(NEEDS_ONBOARDING)
    render(<Home />)
    expect(await screen.findByText('Build your personalized roadmap')).toBeInTheDocument()
    expect(screen.getByText('Tell us your goal and what you already know.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Build My Roadmap/ })).toHaveAttribute('href', '/onboarding/learning-profile')
  })

  it('keeps the way to the dashboard', async () => {
    render(<Home />)
    await screen.findByText('Your Masar')
    expect(screen.getByRole('link', { name: /Open dashboard/ })).toHaveAttribute('href', '/dashboard')
  })

  it('is written in Arabic for an Arabic reader', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    render(<Home />)
    expect(screen.getByRole('heading', { name: 'أهلاً بعودتك، Amira' })).toBeInTheDocument()
    expect(await screen.findByRole('link', { name: /واصل مسارك/ })).toHaveAttribute('href', '/learn')
  })

  it('shows an error state, not a broken card, when the roadmap cannot load', async () => {
    vi.mocked(api.getMyLearningProfile).mockRejectedValue(new Error('down'))
    render(<Home />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load your roadmap.')
  })
})

describe('home — a visitor who is not signed in', () => {
  it('sees the normal marketing page, not a roadmap', () => {
    render(<Home />)
    expect(screen.getByText('Arabic-first AI engineering')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Create account/ })).toHaveAttribute('href', '/auth/register')
    expect(screen.getAllByRole('link', { name: 'Sign in' })[0]).toHaveAttribute('href', '/auth/login')
    expect(screen.queryByText('Your Masar')).toBeNull()
    expect(screen.queryByText('Build your personalized roadmap')).toBeNull()
  })

  it('offers its two calls to action as links styled as buttons, not buttons inside links', () => {
    render(<Home />)
    const signUp = screen.getByRole('link', { name: /Create account/ })
    expectLinkStyledAsButton(signUp, '/auth/register')
    expectMirroredArrow(signUp)
    const signIn = screen.getAllByRole('link', { name: 'Sign in' }).find((a) => a.className.includes('min-h-[44px]') && a.className.includes('border'))!
    expectLinkStyledAsButton(signIn, '/auth/login')
    // and nothing on the page is a button pretending to navigate
    expect(screen.queryAllByRole('button').filter((b) => /Create account|Sign in/.test(b.textContent ?? ''))).toEqual([])
  })

  it('never asks the API for a roadmap', () => {
    render(<Home />)
    expect(api.getMyLearningProfile).not.toHaveBeenCalled()
    expect(api.getMyLearningPath).not.toHaveBeenCalled()
  })

  it('carries the Terms and Privacy links in its footer', () => {
    render(<Home />)
    const footer = screen.getByRole('contentinfo')
    expect(within(footer).getByRole('link', { name: 'Terms' })).toHaveAttribute('href', '/terms')
    expect(within(footer).getByRole('link', { name: 'Privacy' })).toHaveAttribute('href', '/privacy')
  })

  it('is written in Arabic for an Arabic reader', () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    render(<Home />)
    expect(screen.getByText('هندسة الذكاء الاصطناعي بالعربية أولاً')).toBeInTheDocument()
    expect(within(screen.getByRole('contentinfo')).getByRole('link', { name: 'الشروط' })).toHaveAttribute('href', '/terms')
  })
})

describe('home — before the session has loaded', () => {
  it('shows neither page: no flash of the sales page for a signed-in learner', () => {
    useAuthStore.setState({ token: 'tok', user: null, _hasHydrated: false })
    render(<Home />)
    expect(screen.queryByText('Arabic-first AI engineering')).toBeNull()
    expect(screen.queryByText('Your Masar')).toBeNull()
    expect(api.getMyLearningProfile).not.toHaveBeenCalled()
  })
})
