/**
 * Light / dark theme.
 *
 * The theme is the `data-theme` attribute on <html>; every colour in the app is
 * a CSS variable that attribute switches (see globals.css). Dark is the default
 * and is what the server renders, so an absent attribute means dark.
 *
 * The choice lives in localStorage — a device preference, like the language
 * store, that must survive a logout — and is applied by a tiny inline script in
 * the root layout before first paint, otherwise a reader who chose light would
 * see the dark page flash first. This module deliberately imports no React so
 * that layout (a server component) can use it; the hook is in hooks/useTheme.
 */
export type Theme = 'dark' | 'light'

export const THEME_STORAGE_KEY = 'masar-theme'

/**
 * Runs in <head>, before the body is parsed. It has to work with nothing else
 * loaded and must never throw (localStorage is unavailable in some private
 * modes), and it only ever sets `light`: dark needs no attribute.
 */
export const THEME_INIT_SCRIPT =
  `try{if(localStorage.getItem('${THEME_STORAGE_KEY}')==='light')document.documentElement.setAttribute('data-theme','light')}catch(e){}`

export function isTheme(value: unknown): value is Theme {
  return value === 'dark' || value === 'light'
}

/** The theme currently applied to the document. Browser only. */
export function getTheme(): Theme {
  return document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark'
}

const listeners = new Set<() => void>()
const notify = () => listeners.forEach((listener) => listener())

/** Apply and remember a theme, and tell everything that is showing it. */
export function setTheme(theme: Theme): void {
  document.documentElement.setAttribute('data-theme', theme)
  try {
    localStorage.setItem(THEME_STORAGE_KEY, theme)
  } catch {
    // Storage is blocked or full: the theme still applies for this visit.
  }
  notify()
}

/**
 * For useSyncExternalStore. Also follows a change made in another tab, so two
 * open tabs never show different themes.
 */
export function subscribeTheme(listener: () => void): () => void {
  listeners.add(listener)
  const onStorage = (event: StorageEvent) => {
    if (event.key !== THEME_STORAGE_KEY) return
    document.documentElement.setAttribute('data-theme', event.newValue === 'light' ? 'light' : 'dark')
    listener()
  }
  window.addEventListener('storage', onStorage)
  return () => {
    listeners.delete(listener)
    window.removeEventListener('storage', onStorage)
  }
}
