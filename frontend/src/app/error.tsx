'use client'
import { useEffect } from 'react'
import { StatusPage } from '@/components/layout/StatusPage'

/**
 * A page that threw while rendering. The root layout is still standing, so the
 * language and theme are too; only what the failed page drew is replaced.
 * (A failure in the root layout itself is `global-error.tsx`'s.)
 */
export default function ErrorPage({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => {
    // The digest is what ties this to the server-side log line for the same failure.
    console.error(error)
  }, [error])

  return <StatusPage code="500" title="err.server.title" body="err.server.body" onRetry={reset} />
}
