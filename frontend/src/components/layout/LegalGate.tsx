'use client'
import { useEffect, useId, useState } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { useAuthStore } from '@/lib/store'

/**
 * Asks a signed-in learner to accept the Terms and Privacy Policy when the
 * account has not accepted the versions now in force — every account that
 * predates them, and every account after a document changes materially.
 *
 * Whether acceptance is needed is the server's answer
 * (`user.requires_legal_acceptance`); nothing here compares version strings.
 * Acceptance is recorded by the server against the versions it is publishing,
 * so this dialog can only say "yes", never "yes to version X".
 *
 * A session that was signed in before this existed has no such field on its
 * stored user, so it is refreshed once from `/auth/me`. Nobody is ever marked as
 * having accepted on their behalf.
 */
export function LegalGate() {
  const { t } = useI18n()
  const user = useAuthStore((s) => s.user)
  const token = useAuthStore((s) => s.token)
  const logout = useAuthStore((s) => s.logout)
  const [agreed, setAgreed] = useState(false)
  const [saving, setSaving] = useState(false)
  const [failed, setFailed] = useState(false)
  const boxId = useId()

  const unknown = !!token && !!user && user.requires_legal_acceptance === undefined
  useEffect(() => {
    if (!unknown) return
    let alive = true
    ;(async () => {
      try {
        const fresh = await api.getMe()
        if (alive) useAuthStore.setState({ user: fresh })
      } catch {
        /* nothing to prompt about if the account cannot be read */
      }
    })()
    return () => {
      alive = false
    }
  }, [unknown])

  if (!token || user?.requires_legal_acceptance !== true) return null

  async function accept() {
    setSaving(true)
    setFailed(false)
    try {
      const updated = await api.acceptLegal()
      useAuthStore.setState({ user: updated })
    } catch {
      setFailed(true)
      setSaving(false)
    }
  }

  const link = 'text-amber underline underline-offset-2 hover:text-amber2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-amber'
  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-void/90 p-4 backdrop-blur-sm">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby={`${boxId}-title`}
        className="w-full max-w-md rounded-lg border border-border bg-panel p-6 shadow-2xl"
      >
        <h2 id={`${boxId}-title`} className="font-display text-lg font-bold text-white">{t('legal.update.title')}</h2>
        <p className="mt-2 text-sm leading-relaxed text-soft">{t('legal.update.body')}</p>

        <div className="mt-5 flex items-start gap-3">
          <input
            id={boxId}
            type="checkbox"
            checked={agreed}
            onChange={(e) => setAgreed(e.target.checked)}
            className="mt-0.5 h-5 w-5 shrink-0 cursor-pointer accent-amber focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber"
          />
          <label htmlFor={boxId} className="min-h-[44px] flex-1 cursor-pointer py-0.5 text-sm leading-relaxed text-soft">
            {t('legal.agree.prefix')}
            <Link href="/terms" target="_blank" rel="noopener noreferrer" className={link}>{t('legal.terms')}</Link>
            {t('legal.agree.and')}
            <Link href="/privacy" target="_blank" rel="noopener noreferrer" className={link}>{t('legal.privacy')}</Link>
            {t('legal.agree.suffix')}
          </label>
        </div>

        {failed && <p role="alert" className="mt-3 text-xs text-rose">{t('legal.update.error')}</p>}

        <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
          <button
            type="button"
            onClick={logout}
            className="min-h-[44px] rounded px-2 text-xs text-soft hover:text-bright focus-visible:outline focus-visible:outline-2 focus-visible:outline-amber lg:min-h-0"
          >
            {t('nav.signOut')}
          </button>
          <Button onClick={() => void accept()} disabled={!agreed} loading={saving}>
            {t('legal.update.cta')}
          </Button>
        </div>
      </div>
    </div>
  )
}
