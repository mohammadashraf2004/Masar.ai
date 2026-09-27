import { act, fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { AccountMenu } from '@/components/layout/AccountMenu'
import { router, setPathname } from '@/test/nav'
import { getRecord, saveRecord } from './records'
import { resetTourSession, setToursEnabled, tourRanThisSession } from './session'
import { TourProvider } from './TourProvider'
import { OLD_ACCOUNT, ONBOARDING_DESKTOP, ONBOARDING_MOBILE, Targets, mockLayout, signIn } from './tourTestKit'

/** Everything the mentor page (and, for the test's sake, a lesson) could be pointing at. */
const MENTOR_PAGE = ['interview-tab', 'credits', 'lang-switch', 'lesson-terms', 'mentor-lang']

const page = (ids: readonly string[], extra?: React.ReactNode) => (
  <TourProvider><Targets ids={ids} />{extra}</TourProvider>
)
const card = () => screen.queryByRole('dialog')
const title = () => screen.getByRole('heading', { level: 3 }).textContent
const counter = () => card()!.querySelector('[aria-live="polite"]')!.textContent
const button = (name: string) => screen.getByRole('button', { name })

/** Let the tour's timers run (under fake timers): the page settling, the text fading. */
const tick = (ms: number) => act(async () => { await vi.advanceTimersByTimeAsync(ms) })

const setWidth = (value: number) =>
  Object.defineProperty(window, 'innerWidth', { value, configurable: true, writable: true })

/** A fresh visit: a new tab, so a tour is allowed to run again. */
function newSession() {
  document.body.replaceChildren()
  resetTourSession()
}

beforeEach(() => {
  setToursEnabled(true)
  mockLayout()
  setPathname('/dashboard')
  signIn()
})

afterEach(() => {
  vi.useRealTimers()
  setWidth(1024)
})

describe('when a tour starts', () => {
  it('runs the onboarding for a new account on its first visit to home', () => {
    render(page(ONBOARDING_DESKTOP))
    expect(card()).not.toBeNull()
    expect(title()).toBe('Your path starts here')
    expect(counter()).toBe('1 of 4')
    expect(tourRanThisSession()).toBe(true)
  })

  it('starts nothing when tours are off', () => {
    setToursEnabled(false)
    render(page(ONBOARDING_DESKTOP))
    expect(card()).toBeNull()
  })

  it('starts nothing for an existing account on home', () => {
    signIn({ created_at: OLD_ACCOUNT })
    render(page(ONBOARDING_DESKTOP))
    expect(card()).toBeNull()
  })

  it('starts nothing on a page with no tour', () => {
    setPathname('/glossary')
    render(page(ONBOARDING_DESKTOP))
    expect(card()).toBeNull()
  })

  it('is never on a payment page', () => {
    setPathname('/billing')
    render(page(ONBOARDING_DESKTOP))
    expect(card()).toBeNull()
  })

  it('waits while another dialog is open, and starts when it closes', async () => {
    vi.useFakeTimers()
    const modal = <div role="dialog" aria-modal="true" aria-label="What's new">an announcement</div>
    const { rerender } = render(page(ONBOARDING_DESKTOP, modal))
    await tick(1500)
    expect(document.querySelector('[data-tour-card]')).toBeNull()
    expect(tourRanThisSession()).toBe(false)

    rerender(page(ONBOARDING_DESKTOP))
    await tick(500)
    expect(document.querySelector('[data-tour-card]')).not.toBeNull()
  })
})

describe('remembering', () => {
  it('saves { status, version, at } when the tour is finished', async () => {
    vi.useFakeTimers()
    render(page(ONBOARDING_DESKTOP))
    for (let n = 0; n < 3; n++) {
      fireEvent.click(button('Next'))
      await tick(200)
    }
    fireEvent.click(button('Get started'))
    expect(getRecord(7, 'onboarding')).toMatchObject({ status: 'done', version: 1 })
    expect(Number.isNaN(Date.parse(getRecord(7, 'onboarding')!.at))).toBe(false)
    expect(card()).toBeNull()
  })

  it('saves a skip as skipped', () => {
    render(page(ONBOARDING_DESKTOP))
    fireEvent.click(button('Skip tour'))
    expect(getRecord(7, 'onboarding')).toMatchObject({ status: 'skipped', version: 1 })
  })

  it('does not show it again, in this session or the next', () => {
    const first = render(page(ONBOARDING_DESKTOP))
    fireEvent.click(button('Skip tour'))
    first.unmount()

    render(page(ONBOARDING_DESKTOP))
    expect(card()).toBeNull()

    newSession()
    render(page(ONBOARDING_DESKTOP))
    expect(card()).toBeNull()
  })

  it('shows it again after a version bump', () => {
    saveRecord(7, 'onboarding', { status: 'done', version: 0 })    // seen an earlier version
    render(page(ONBOARDING_DESKTOP))
    expect(card()).not.toBeNull()
  })

  it('does not show it again for the current version', () => {
    saveRecord(7, 'onboarding', { status: 'done', version: 1 })
    render(page(ONBOARDING_DESKTOP))
    expect(card()).toBeNull()
  })
})

describe('the "New" tag', () => {
  it('is on a feature tour shown to an existing account', () => {
    signIn({ created_at: OLD_ACCOUNT })
    setPathname('/mentor')
    render(page(MENTOR_PAGE))
    expect(title()).toBe('New: mock interviews')
    expect(within(card()!).getByText('New')).toBeInTheDocument()
  })

  it('is not on it for a new signup', () => {
    setPathname('/mentor')
    render(page(MENTOR_PAGE))
    expect(title()).toBe('New: mock interviews')
    expect(within(card()!).queryByText('New')).toBeNull()
  })
})

describe('the order tours come in', () => {
  it('runs one tour a session: the onboarding first, and nothing else until the next visit', () => {
    const home = render(page(ONBOARDING_DESKTOP))
    expect(title()).toBe('Your path starts here')
    fireEvent.click(button('Skip tour'))
    home.unmount()

    // Same session, a page with tours of its own.
    setPathname('/mentor')
    const mentor = render(page(MENTOR_PAGE))
    expect(card()).toBeNull()
    mentor.unmount()

    // The next session: the mentor's own tour ...
    newSession()
    const second = render(page(MENTOR_PAGE))
    expect(title()).toBe('New: mock interviews')
    fireEvent.click(button('Skip tour'))
    second.unmount()

    // ... and the one after that, the language tour.
    newSession()
    render(page(MENTOR_PAGE))
    expect(title()).toBe('Arabic first, English anytime')
  })

  it('holds the language tour back until a new account has done the onboarding', () => {
    saveRecord(7, 'mentor-interview', { status: 'done', version: 1 })
    setPathname('/mentor')
    render(page(MENTOR_PAGE))
    expect(card()).toBeNull()
  })

  it('does not hold it back for an existing account, which is never given the onboarding', () => {
    signIn({ created_at: OLD_ACCOUNT })
    saveRecord(7, 'mentor-interview', { status: 'done', version: 1 })
    setPathname('/courses/langgraph/learn')
    render(page(MENTOR_PAGE))
    expect(title()).toBe('Arabic first, English anytime')
  })
})

describe('steps whose target is not there', () => {
  beforeEach(() => {
    signIn({ created_at: OLD_ACCOUNT })
    saveRecord(7, 'mentor-interview', { status: 'done', version: 1 })
    setPathname('/mentor')
    vi.useFakeTimers()
  })

  it('leaves the step out silently and counts the rest', async () => {
    // The mentor page has no lesson on it: of the language tour's three steps, two can be shown.
    render(page(['lang-switch', 'mentor-lang']))
    await tick(3500)
    expect(counter()).toBe('1 of 2')
    expect(title()).toBe('Arabic first, English anytime')
    fireEvent.click(button('Next'))
    await tick(200)
    expect(counter()).toBe('2 of 2')
    expect(title()).toBe('Choose how your mentor talks')
    expect(button('Got it')).toBeInTheDocument()
  })

  it('starts as soon as every target is there, without waiting out the settle time', () => {
    render(page(['lang-switch', 'lesson-terms', 'mentor-lang']))
    expect(counter()).toBe('1 of 3')
  })

  it('does not run at all when fewer than two steps remain, and records nothing', async () => {
    render(page(['mentor-lang']))
    await tick(10_000)
    expect(document.querySelector('[data-tour-card]')).toBeNull()
    expect(getRecord(7, 'language')).toBeUndefined()
    expect(tourRanThisSession()).toBe(false)
  })

  it('waits for a target that turns up late, and includes it', async () => {
    const view = render(page(['lang-switch', 'mentor-lang']))
    await tick(800)
    expect(document.querySelector('[data-tour-card]')).toBeNull()
    view.rerender(page(['lang-switch', 'lesson-terms', 'mentor-lang']))
    await tick(500)
    expect(counter()).toBe('1 of 3')
  })

  it('ignores a target that is in the page but not on screen (the other header\'s language switch)', async () => {
    mockLayout({ hidden: ['lang-switch'] })
    render(page(['lang-switch', 'lesson-terms', 'mentor-lang']))
    await tick(3500)
    expect(counter()).toBe('1 of 2')
    expect(title()).toBe('Explained in Arabic, named like the industry')
  })
})

describe('per-device targets', () => {
  it('points at the sidebar items on a desktop', () => {
    render(page(ONBOARDING_DESKTOP))
    expect(counter()).toBe('1 of 4')
  })

  it('points at the on-page elements on a phone', () => {
    setWidth(390)
    mockLayout({ width: 390, height: 844 })
    render(page(ONBOARDING_MOBILE))
    expect(counter()).toBe('1 of 4')
  })

  it('does not use the sidebar items on a phone, where there is no sidebar', async () => {
    vi.useFakeTimers()
    setWidth(390)
    mockLayout({ width: 390, height: 844 })
    render(page(ONBOARDING_DESKTOP))       // the sidebar's ids are in the page, but the phone wants other ones
    await tick(3500)
    expect(counter()).toBe('1 of 2')       // just path and learn
  })
})

describe('replaying', () => {
  const menu = () => screen.getByRole('button', { name: /Profile menu/ })
  const replay = () => {
    fireEvent.click(menu())
    fireEvent.click(within(screen.getByRole('group', { name: 'Help' })).getByRole('button', { name: 'Replay tour' }))
  }

  it('is in the Help menu, and plays the tour again even after it was seen', () => {
    saveRecord(7, 'onboarding', { status: 'done', version: 1 })
    render(page(ONBOARDING_DESKTOP, <AccountMenu />))
    expect(card()).toBeNull()
    replay()
    expect(title()).toBe('Your path starts here')
  })

  it('leaves what was saved alone: skipping a replay keeps a finished tour finished', () => {
    saveRecord(7, 'onboarding', { status: 'done', version: 1, at: '2026-09-28T10:00:00.000Z' })
    render(page(ONBOARDING_DESKTOP, <AccountMenu />))
    replay()
    fireEvent.click(button('Skip tour'))
    expect(getRecord(7, 'onboarding')).toEqual({ status: 'done', version: 1, at: '2026-09-28T10:00:00.000Z' })
  })

  it('replays the tour of the page it is opened on', () => {
    signIn({ created_at: OLD_ACCOUNT })
    saveRecord(7, 'mentor-interview', { status: 'done', version: 1 })
    setPathname('/mentor')
    render(page(['interview-tab', 'credits'], <AccountMenu />))
    expect(card()).toBeNull()
    replay()
    expect(title()).toBe('New: mock interviews')
  })

  it('goes to the tour\'s page first when its targets are on another', () => {
    setPathname('/glossary')
    const view = render(page([], <AccountMenu />))
    replay()
    expect(router.push).toHaveBeenCalledWith('/dashboard')
    expect(card()).toBeNull()

    // The next page mounts its own provider, which starts the tour.
    view.unmount()
    setPathname('/dashboard')
    saveRecord(7, 'onboarding', { status: 'done', version: 1 })
    render(page(ONBOARDING_DESKTOP))
    expect(title()).toBe('Your path starts here')
  })

  it('leaves a note after a tour ends, with a button to play it again', () => {
    render(page(ONBOARDING_DESKTOP))
    fireEvent.click(button('Skip tour'))
    const note = screen.getByRole('status')
    expect(note).toHaveTextContent('You can replay this tour anytime from Help.')
    fireEvent.click(within(note).getByRole('button', { name: 'Replay tour' }))
    expect(screen.queryByRole('status')).toBeNull()
    expect(title()).toBe('Your path starts here')
  })

  it('clears the note by itself after a while', async () => {
    vi.useFakeTimers()
    render(page(ONBOARDING_DESKTOP))
    fireEvent.click(button('Skip tour'))
    expect(screen.getByRole('status')).toBeInTheDocument()
    await tick(12_100)
    expect(screen.queryByRole('status')).toBeNull()
  })

  it('is not offered outside the app shell, where there is nothing to replay', () => {
    render(<AccountMenu />)
    fireEvent.click(menu())
    expect(screen.queryByRole('button', { name: 'Replay tour' })).toBeNull()
  })
})

describe('the language tour on a phone', () => {
  beforeEach(() => {
    signIn({ created_at: OLD_ACCOUNT })
    saveRecord(7, 'mentor-interview', { status: 'done', version: 1 })
    setPathname('/mentor')
    setWidth(390)
    mockLayout({ width: 390, height: 844 })
  })

  it('points at the menu button, in the phone\'s words, without opening the menu', async () => {
    vi.useFakeTimers()
    render(page(['menu-button', 'mentor-lang', 'lang-switch']))
    await tick(3500)
    expect(counter()).toBe('1 of 2')
    expect(title()).toBe('Arabic first, English anytime')
    expect(card()).toHaveTextContent('Switch the interface language from the menu anytime; your progress stays the same.')
    expect(document.querySelector('#mobile-menu')).toBeNull()
  })

  it('does not point at the header\'s switch, which a phone does not show', async () => {
    vi.useFakeTimers()
    render(page(['lang-switch', 'mentor-lang']))
    await tick(3500)
    // Only the mentor rows are there for it: one step is not a tour.
    expect(document.querySelector('[data-tour-card]')).toBeNull()
  })
})

describe('the language tour on a desktop', () => {
  it('says "here", not "from the menu"', async () => {
    vi.useFakeTimers()
    signIn({ created_at: OLD_ACCOUNT })
    saveRecord(7, 'mentor-interview', { status: 'done', version: 1 })
    setPathname('/mentor')
    render(page(['lang-switch', 'mentor-lang', 'menu-button']))
    await tick(3500)
    expect(card()).toHaveTextContent('Switch to English here anytime')
  })
})
