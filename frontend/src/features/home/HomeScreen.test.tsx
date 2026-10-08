import { act, cleanup, render, screen, within } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { HomeScreen } from './HomeScreen'
import { homeMocksEnabled } from './flag'
import { arabicDigits } from './strings'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import type { User } from '@/types'

vi.mock('@/components/layout/AppShell', async () => {
  const { createElement } = await import('react')
  return { AppShell: ({ children }: { children: React.ReactNode }) => createElement('div', { 'data-testid': 'shell' }, children) }
})

async function renderHome() {
  await act(async () => { render(<HomeScreen />) })
  // The overview arrives through a dynamic import; the first one in a run is slower than a tick.
  await screen.findByRole('heading', { level: 1 })
}

beforeEach(() => {
  useAuthStore.setState({ token: 'tok', user: { full_name: 'Layan Al-Harbi' } as User, expiresAt: null, _hasHydrated: true })
  useLanguageStore.setState({ language: 'ar' })
  vi.useFakeTimers({ toFake: ['Date'] })
  vi.setSystemTime(new Date(2026, 9, 3, 20, 0, 0))
})
afterEach(() => {
  // Unmount before resetting the store, or the still-mounted screen re-renders outside act.
  cleanup()
  vi.useRealTimers()
  useLanguageStore.setState({ language: 'en' })
})

describe('Home, Arabic', () => {
  it('greets by name and says how far the exam is, in Arabic-Indic digits', async () => {
    await renderHome()
    expect(screen.getByRole('heading', { level: 1, name: 'مساء الخير، Layan' })).toBeInTheDocument()
    expect(screen.getByText(/أنت على بعد ٣ نقاط من أهلية اختبار RAG Engineer/)).toBeInTheDocument()
  })

  it('continues the lesson: Latin course name, copy digits, mono percentage, both buttons', async () => {
    await renderHome()
    const course = screen.getByText('LangGraph')
    expect(course).toHaveAttribute('dir', 'ltr')
    expect(screen.getByText('الدرس ٧ — Checkpointers وحفظ ذاكرة المحادثة')).toBeInTheDocument()
    expect(screen.getByText('الدرس ٧ من ١٢ · ١٨ دقيقة متبقية')).toBeInTheDocument()
    const pct = screen.getByText('62%')
    expect(pct.className).toContain('font-mono')
    expect(screen.getByRole('link', { name: 'متابعة الدرس' })).toHaveAttribute('href', '/courses/langgraph-agent-memory/lessons/7')
    expect(screen.getByRole('link', { name: 'خطة الدورة' })).toHaveAttribute('href', '/courses/langgraph-agent-memory')
  })

  it('shows the readiness score and the four skills with Latin digits', async () => {
    await renderHome()
    expect(screen.getByText('72')).toBeInTheDocument()
    expect(screen.getByText('/100')).toHaveAttribute('dir', 'ltr')
    const week = screen.getByText('هذا الأسبوع')
    expect(week).toHaveTextContent('+6 هذا الأسبوع')
    // The number is its own left-to-right island, so Arabic around it cannot turn "+6" into "6+".
    expect(within(week).getByText('+6')).toHaveAttribute('dir', 'ltr')
    for (const [name, value] of [['Retrieval و RAG', '80'], ['Agents', '64'], ['النشر و Serving', '58'], ['Evaluation', '49']]) {
      const row = screen.getByText(name).closest('li') as HTMLElement
      expect(within(row).getByText(value)).toBeInTheDocument()
    }
  })

  it('draws the track as five stages: two done, one in progress, two locked', async () => {
    await renderHome()
    expect(screen.getByText('٢ من ٥ مراحل')).toBeInTheDocument()
    const rows = Array.from(document.querySelectorAll('li[data-status]'))
    expect(rows.map((r) => r.getAttribute('data-status'))).toEqual(['done', 'done', 'now', 'lock', 'lock'])
    expect(within(rows[0] as HTMLElement).getByText('مكتمل')).toBeInTheDocument()
    const now = within(rows[2] as HTMLElement).getByText(/جارٍ/)
    expect(now).toHaveTextContent('جارٍ · 64%')
    expect(within(now).getByText('64%')).toHaveAttribute('dir', 'ltr')
    expect(within(rows[3] as HTMLElement).getByText('مقفل')).toBeInTheDocument()
    expect(within(rows[0] as HTMLElement).getByText('٦ دورات · ٣٢ ساعة')).toBeInTheDocument()
  })

  it('keeps the exam booking disabled until eligible, with the unmet requirement shown', async () => {
    await renderHome()
    expect(screen.getByText('RAG Engineer — Associate')).toHaveAttribute('dir', 'ltr')
    expect(screen.getByText('اختبار مراقَب بالكاميرا · ٩٠ دقيقة')).toBeInTheDocument()
    expect(screen.getByText('72/75')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'احجز موعداً بعد الأهلية' })).toBeDisabled()
  })

  it('shows the two stats and the mentor strip', async () => {
    await renderHome()
    expect(screen.getByText('سلسلة الأيام').nextElementSibling).toHaveTextContent('12')
    expect(screen.getByText('تمارين مقيّمة').nextElementSibling).toHaveTextContent('86')
    expect(screen.getByText(/درجاتك في Retrieval evaluation/)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'افتح المحادثة' })).toHaveAttribute('href', '/mentor')
  })

  it('keeps the walkthrough targets the onboarding tour points at', async () => {
    await renderHome()
    for (const id of ['learn', 'path', 'practice', 'mentor']) {
      expect(document.querySelector(`[data-tour="${id}"]`), id).not.toBeNull()
    }
  })

  it('says good morning before noon', async () => {
    vi.setSystemTime(new Date(2026, 9, 3, 8, 0, 0))
    await renderHome()
    expect(screen.getByRole('heading', { level: 1, name: 'صباح الخير، Layan' })).toBeInTheDocument()
  })
})

describe('Home, English', () => {
  it('uses Latin digits and English copy', async () => {
    useLanguageStore.setState({ language: 'en' })
    await renderHome()
    expect(screen.getByRole('heading', { level: 1, name: 'Good evening, Layan' })).toBeInTheDocument()
    expect(screen.getByText('Lesson 7 of 12 · 18 min left')).toBeInTheDocument()
    expect(screen.getByText('2 of 5 stages')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continue lesson' })).toBeInTheDocument()
  })
})

describe('helpers', () => {
  it('converts digits for copy only', () => {
    expect(arabicDigits('٧ من 12')).toBe('٧ من ١٢')
    expect(arabicDigits(2026)).toBe('٢٠٢٦')
  })

  it('shows mock data in dev or on a flagged build, never in a plain production build', () => {
    vi.stubEnv('NODE_ENV', 'production')
    vi.stubEnv('NEXT_PUBLIC_HOME_MOCKS', '')
    expect(homeMocksEnabled()).toBe(false)
    vi.stubEnv('NEXT_PUBLIC_HOME_MOCKS', '1')
    expect(homeMocksEnabled()).toBe(true)
    vi.stubEnv('NEXT_PUBLIC_HOME_MOCKS', '')
    vi.stubEnv('NODE_ENV', 'development')
    expect(homeMocksEnabled()).toBe(true)
    vi.stubEnv('NODE_ENV', 'test')
    expect(homeMocksEnabled()).toBe(false)
    vi.unstubAllEnvs()
  })
})
