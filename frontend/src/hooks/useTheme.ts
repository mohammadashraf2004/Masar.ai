'use client'
import { useSyncExternalStore } from 'react'
import { getTheme, setTheme, subscribeTheme, type Theme } from '@/lib/theme'

const SERVER_THEME: Theme = 'dark'

/**
 * The active theme and its setter.
 *
 * Read from the document, not from React state: the inline script in the root
 * layout has already set it by the time this runs, so the server snapshot
 * ('dark', which is what the server renders) is only used for hydration and the
 * client snapshot takes over immediately after, with no mismatch warning.
 */
export function useTheme(): { theme: Theme; setTheme: (theme: Theme) => void } {
  const theme = useSyncExternalStore(subscribeTheme, getTheme, () => SERVER_THEME)
  return { theme, setTheme }
}
