'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Logo } from '@/components/layout/Logo'
import { Button } from '@/components/ui/Button'
import { Spinner } from '@/components/ui/index'
import { LanguageSwitcher } from '@/components/ui/LanguageSwitcher'
import { LegalFooter } from '@/components/layout/LegalFooter'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import type { LegalDocument } from '@/types'

type Load = { key: string; doc: LegalDocument | null }

/**
 * A public page showing one legal document.
 *
 * The wording and its version both come from the API — this page holds neither —
 * so what a reader sees here is exactly what an account is recorded as
 * accepting. It follows the interface language; switching it fetches the other
 * language's text of the same version.
 */
export function LegalDocumentPage({ kind }: { kind: 'terms' | 'privacy' }) {
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

  return (
    <div className="flex min-h-dvh flex-col bg-void px-4 pt-8 pb-[calc(1.25rem+env(safe-area-inset-bottom))] sm:px-6">
      <div className="mx-auto mb-10 flex max-w-3xl items-center justify-between">
        <Link href="/" aria-label="Masar" className="inline-flex min-h-[44px] items-center lg:min-h-0"><Logo size={28} wordmarkClassName="text-sm" /></Link>
        <LanguageSwitcher />
      </div>

      <main className="mx-auto flex w-full max-w-3xl flex-1 flex-col">
        {!current && (
          <div className="flex justify-center py-24" role="status" aria-label={t('common.loading')}>
            <Spinner className="h-6 w-6" />
          </div>
        )}

        {current && !current.doc && (
          <div className="py-16 text-center">
            <p role="alert" className="mb-4 text-sm text-rose">{t('legal.loadError')}</p>
            <Button variant="ghost" onClick={() => { setLoad(null); setAttempt((n) => n + 1) }}>
              {t('common.retry')}
            </Button>
          </div>
        )}

        {current?.doc && (
          <article>
            <h1 className="font-display text-3xl font-bold text-white">{current.doc.title}</h1>
            <p className="mt-2 text-xs text-soft">{tf('legal.version', { v: current.doc.version })}</p>
            <p className="mt-6 text-sm leading-relaxed text-soft">{current.doc.intro}</p>
            {current.doc.sections.map((section) => (
              <section key={section.heading} className="mt-8">
                <h2 className="mb-2 text-base font-semibold text-bright">{section.heading}</h2>
                {section.body.map((paragraph, i) => (
                  <p key={i} className="mb-3 text-sm leading-relaxed text-soft">{paragraph}</p>
                ))}
              </section>
            ))}
          </article>
        )}

        <div className="mt-14 flex flex-wrap items-center gap-3">
          <Link href="/" className="inline-flex min-h-[44px] items-center text-xs text-soft hover:text-bright lg:min-h-0">
            {t('legal.back')}
          </Link>
        </div>
        <LegalFooter />
      </main>
    </div>
  )
}
