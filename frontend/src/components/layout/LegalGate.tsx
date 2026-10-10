'use client'
import { useEffect, useId, useRef, useState } from 'react'
import { ArrowLeft } from 'lucide-react'
import { LegalDocumentReader } from '@/components/legal/LegalDocumentReader'
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
 *
 * The Terms and Privacy links open the document inside this dialog rather than
 * in a new tab: in-app browsers (WhatsApp, Facebook, Instagram) ignore
 * `target="_blank"`, so a new-tab link did nothing there and the learner could
 * not read what they were asked to accept. A modified click (Ctrl/Cmd/middle)
 * still opens the public page, as any link would.
 */
export function LegalGate() {
  const { t } = useI18n()
  const user = useAuthStore((s) => s.user)
  const token = useAuthStore((s) => s.token)
  const logout = useAuthStore((s) => s.logout)
  const [agreed, setAgreed] = useState(false)
  const [saving, setSaving] = useState(false)
  const [failed, setFailed] = useState(false)
  const [reading, setReading] = useState<'terms' | 'privacy' | null>(null)
  // Which link opened the reader; it is re-created on the way back, so focus
  // goes to the new element through these refs.
  const opened = useRef<'terms' | 'privacy' | null>(null)
  const links = useRef<Record<'terms' | 'privacy', HTMLAnchorElement | null>>({ terms: null, privacy: null })
  const backRef = useRef<HTMLButtonElement | null>(null)
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

  // Move focus with the view: to Back when a document opens, and to the link
  // that opened it when the reader comes back.
  useEffect(() => {
    if (reading) backRef.current?.focus()
    else if (opened.current) links.current[opened.current]?.focus()
  }, [reading])

  if (!token || user?.requires_legal_acceptance !== true) return null

  function read(e: React.MouseEvent<HTMLAnchorElement>, kind: 'terms' | 'privacy') {
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return
    e.preventDefault()
    opened.current = kind
    setReading(kind)
  }

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

  const link = 'text-amber-text underline underline-offset-2 hover:text-amber-text2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring'
  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-scrim/90 p-4 backdrop-blur-sm">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby={reading ? `${boxId}-doc` : `${boxId}-title`}
        className={`flex max-h-[calc(100dvh-2rem)] w-full flex-col rounded-lg border border-border bg-panel p-6 shadow-2xl ${reading ? 'max-w-2xl' : 'max-w-md'}`}
      >
        {reading ? (
          <>
            <div className="-mx-6 -mt-2 mb-3 border-b border-border px-6 pb-2">
              <button
                ref={backRef}
                type="button"
                onClick={() => setReading(null)}
                className="-ms-2 inline-flex min-h-[44px] items-center gap-2 rounded px-2 text-sm text-soft hover:text-bright focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
              >
                <ArrowLeft size={16} className="rtl:rotate-180" aria-hidden="true" />
                {t('legal.back')}
              </button>
            </div>
            <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain pe-1">
              <LegalDocumentReader kind={reading} titleId={`${boxId}-doc`} />
            </div>
          </>
        ) : (
          <>
            <h2 id={`${boxId}-title`} className="ui-card-title">{t('legal.update.title')}</h2>
            <p className="mt-2 text-sm leading-relaxed text-soft">{t('legal.update.body')}</p>

            <div className="mt-5 flex items-start gap-3">
              <input
                id={boxId}
                type="checkbox"
                checked={agreed}
                onChange={(e) => setAgreed(e.target.checked)}
                className="mt-0.5 h-5 w-5 shrink-0 cursor-pointer accent-amber focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
              />
              <label htmlFor={boxId} className="min-h-[44px] flex-1 cursor-pointer py-0.5 text-sm leading-relaxed text-soft">
                {t('legal.agree.prefix')}
                <a ref={(el) => { links.current.terms = el }} href="/terms" onClick={(e) => read(e, 'terms')} className={link}>{t('legal.terms')}</a>
                {t('legal.agree.and')}
                <a ref={(el) => { links.current.privacy = el }} href="/privacy" onClick={(e) => read(e, 'privacy')} className={link}>{t('legal.privacy')}</a>
                {t('legal.agree.suffix')}
              </label>
            </div>

            {failed && <p role="alert" className="mt-3 text-xs text-rose">{t('legal.update.error')}</p>}

            <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
              <button
                type="button"
                onClick={logout}
                className="min-h-[44px] rounded px-2 text-xs text-soft hover:text-bright focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring lg:min-h-0"
              >
                {t('nav.signOut')}
              </button>
              <Button onClick={() => void accept()} disabled={!agreed} loading={saving}>
                {t('legal.update.cta')}
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
