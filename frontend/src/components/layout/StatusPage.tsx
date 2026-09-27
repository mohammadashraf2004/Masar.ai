'use client'
import Link from 'next/link'
import { AppShell } from '@/components/layout/AppShell'
import { LegalFooter } from '@/components/layout/LegalFooter'
import { Button, buttonStyles } from '@/components/ui/Button'
import { useI18n, type StringKey } from '@/lib/i18n'
import { useAuthStore } from '@/lib/store'

/**
 * The page a dead end shows - a URL that is not there (404) or a page that threw
 * (500) - in the product's own voice instead of the framework's bare default.
 *
 * Signed in, it sits inside the app shell, so the sidebar is still there to leave by.
 * Signed out (or before the saved session has been read, which is the first render),
 * it is the bare `--bg` page: the shell needs an account and would have nothing to show.
 *
 * The big number is in `--faint`, in mono, decoration only: the heading carries the
 * meaning, so the number is hidden from assistive technology and always `ltr` (in an
 * Arabic page "404" is otherwise placed by the bidi rules like any other run of digits).
 */
export function StatusPage({
  code,
  title,
  body,
  onRetry,
}: {
  code: string
  title: StringKey
  body: StringKey
  /** Offered on an error page, where trying again can work; not on a 404, where it cannot. */
  onRetry?: () => void
}) {
  const { t } = useI18n()
  const signedIn = useAuthStore(s => s._hasHydrated && !!s.token)

  const content = (
    <div className="flex flex-1 flex-col overflow-y-auto px-4 pb-[calc(1.25rem+env(safe-area-inset-bottom))] sm:px-6 lg:px-8">
      <div className="flex flex-1 flex-col items-center justify-center gap-6 py-16 text-center">
        <p aria-hidden="true" dir="ltr" className="select-none font-mono text-[96px] font-medium leading-none text-ghost sm:text-[128px]">
          {code}
        </p>
        <div className="max-w-md space-y-2">
          <h1 className="font-display text-2xl font-bold text-white">{t(title)}</h1>
          <p className="text-sm leading-relaxed text-dim">{t(body)}</p>
        </div>
        <div className="flex flex-wrap justify-center gap-3">
          <Link href="/dashboard" className={buttonStyles()}>{t('err.dashboard')}</Link>
          <Link href="/tracks" className={buttonStyles({ variant: 'ghost' })}>{t('err.tracks')}</Link>
          {onRetry && <Button variant="ghost" onClick={onRetry}>{t('common.retry')}</Button>}
        </div>
      </div>
      <LegalFooter className="mx-auto w-full max-w-3xl" />
    </div>
  )

  return signedIn ? (
    <AppShell>{content}</AppShell>
  ) : (
    <div className="flex min-h-dvh flex-col bg-void">{content}</div>
  )
}
