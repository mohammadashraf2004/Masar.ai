import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  THEME_INIT_SCRIPT, THEME_STORAGE_KEY, getTheme, isTheme, setTheme, subscribeTheme,
} from '@/lib/theme'

const root = document.documentElement

afterEach(() => {
  root.removeAttribute('data-theme')
  window.localStorage.clear()
})

describe('the no-flash script that runs in <head>', () => {
  // The script is the one piece of theme code that runs before anything else is
  // loaded, so it is executed here exactly as the browser will: as a bare string.
  const run = () => new Function(THEME_INIT_SCRIPT)()

  it('applies a saved light theme', () => {
    window.localStorage.setItem(THEME_STORAGE_KEY, 'light')
    run()
    expect(root).toHaveAttribute('data-theme', 'light')
  })

  it.each([['nothing saved', null], ['a saved dark theme', 'dark'], ['an unrecognised value', 'sepia']])(
    'leaves the document alone for %s (dark needs no attribute)',
    (_label, saved) => {
      if (saved !== null) window.localStorage.setItem(THEME_STORAGE_KEY, saved)
      run()
      expect(root).not.toHaveAttribute('data-theme')
    },
  )

  it('never throws when storage is blocked', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => { throw new Error('blocked') })
    expect(run).not.toThrow()
    expect(root).not.toHaveAttribute('data-theme')
  })
})

describe('setTheme / getTheme', () => {
  it('reads dark when nothing has been set', () => {
    expect(getTheme()).toBe('dark')
  })

  it('applies the theme to the document and remembers it', () => {
    setTheme('light')
    expect(getTheme()).toBe('light')
    expect(root).toHaveAttribute('data-theme', 'light')
    expect(window.localStorage.getItem(THEME_STORAGE_KEY)).toBe('light')

    setTheme('dark')
    expect(getTheme()).toBe('dark')
    expect(window.localStorage.getItem(THEME_STORAGE_KEY)).toBe('dark')
  })

  it('still applies for this visit when storage is blocked', () => {
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new Error('full') })
    expect(() => setTheme('light')).not.toThrow()
    expect(getTheme()).toBe('light')
  })

  it('tells subscribers, and stops telling them once they unsubscribe', () => {
    const listener = vi.fn()
    const unsubscribe = subscribeTheme(listener)
    setTheme('light')
    expect(listener).toHaveBeenCalledTimes(1)
    unsubscribe()
    setTheme('dark')
    expect(listener).toHaveBeenCalledTimes(1)
  })
})

describe('a change made in another tab', () => {
  const fromOtherTab = (key: string | null, newValue: string | null) =>
    window.dispatchEvent(new StorageEvent('storage', { key, newValue }))

  it('is followed, so two open tabs never disagree', () => {
    const listener = vi.fn()
    const unsubscribe = subscribeTheme(listener)
    fromOtherTab(THEME_STORAGE_KEY, 'light')
    expect(getTheme()).toBe('light')
    expect(listener).toHaveBeenCalledTimes(1)
    fromOtherTab(THEME_STORAGE_KEY, 'dark')
    expect(getTheme()).toBe('dark')
    unsubscribe()
  })

  it('ignores storage changes that are not the theme', () => {
    const listener = vi.fn()
    const unsubscribe = subscribeTheme(listener)
    fromOtherTab('language-prefs', 'light')
    expect(listener).not.toHaveBeenCalled()
    expect(root).not.toHaveAttribute('data-theme')
    unsubscribe()
  })
})

describe('isTheme', () => {
  it('accepts only the two themes', () => {
    expect(isTheme('dark')).toBe(true)
    expect(isTheme('light')).toBe(true)
    expect(isTheme('auto')).toBe(false)
    expect(isTheme(undefined)).toBe(false)
  })
})
