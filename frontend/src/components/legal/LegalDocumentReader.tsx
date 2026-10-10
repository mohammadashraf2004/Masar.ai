'use client'
import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import type { LegalDocument } from '@/types'

type Load = { key: string; doc: LegalDocument | null }

/**
 * One legal document, read in place — inside a dialog that must not send the
 * reader away to see what they are agreeing to.
 *
 * Same source as the public `/terms` and `/privacy` pages (the API, with its
 * version), so the text here is the text the account is recorded as accepting.
 * Follows the interface language.
 */
export function LegalDocumentReader({ kind, titleId }: { kind: 'terms' | 'privacy'; titleId?: string }) {
  const { t, tf, language } = useI18n()
  const key = `${kind}|${language}`
  const [load, setLoad] = useState<Load | null>(null)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    let stale = false
    api
      .getLegalDocument(kind, language)
      .then((doc) => !stale && setLoad({ key, doc }))
      .catch(() => !stale && setLoad({ key, doc: null }))
    return () => {
      stale = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, attempt])

  const current = load?.key === key ? load : null

  if (!current) {
    return (
      <div className="flex justify-center py-12" role="status" aria-label={t('common.loading')}>
        <Spinner className="h-6 w-6" />
      </div>
    )
  }

  if (!current.doc) {
    return (
      <div className="py-8 text-center">
        <p role="alert" className="mb-4 text-sm text-rose">{t('legal.loadError')}</p>
        <Button variant="ghost" onClick={() => { setLoad(null); setAttempt((n) => n + 1) }}>
          {t('common.retry')}
        </Button>
      </div>
    )
  }

  const doc = current.doc
  return (
    <article>
      <h3 id={titleId} className="ui-section-title">{doc.title}</h3>
      <p className="ui-caption mt-1">{tf('legal.version', { v: doc.version })}</p>
      <p className="mt-4 text-sm leading-relaxed text-soft">{doc.intro}</p>
      {doc.sections.map((section) => (
        <section key={section.heading} className="mt-5">
          <h4 className="mb-2 text-sm font-semibold text-bright">{section.heading}</h4>
          {section.body.map((paragraph, i) => (
            <p key={i} className="mb-3 text-sm leading-relaxed text-soft">{paragraph}</p>
          ))}
        </section>
      ))}
    </article>
  )
}
