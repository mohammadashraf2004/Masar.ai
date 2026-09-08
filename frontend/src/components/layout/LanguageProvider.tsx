'use client'
import { useEffect } from 'react'
import { useLanguageStore, directionFor } from '@/lib/language'

/**
 * Keeps `<html lang>` / `<html dir>` in sync with the reader's preference.
 *
 * Done in an effect rather than server-side because the preference lives in
 * localStorage: the server has no way to know it, and reading it during
 * render would desynchronise hydration. The document starts in the
 * Arabic-first default (`lang="ar" dir="rtl"` in the root layout), so the
 * only readers who see a direction flip are the ones who chose English.
 */
export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const language = useLanguageStore((s) => s.language)

  useEffect(() => {
    const root = document.documentElement
    root.lang = language
    root.dir = directionFor(language)
  }, [language])

  return <>{children}</>
}
