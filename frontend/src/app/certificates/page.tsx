'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Award, Download, ExternalLink, Link2 } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { CourseCertificate } from '@/components/certificates/CourseCertificate'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card, EmptyState, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { linkedInShareUrl, printCertificate, verifyUrlFor } from '@/lib/certificates'
import { cn } from '@/lib/utils'
import type { CertificateSummary } from '@/types'

type View =
  | { kind: 'loading' }
  | { kind: 'error' }
  | { kind: 'ready'; certificates: CertificateSummary[] }

/**
 * Certificates: the learner's issued certificates (handoff README §8), newest first.
 *
 * The certificate itself is English and left-to-right whatever the page language is;
 * everything around it - title, actions, the history list - follows the reader's
 * language. With none yet it says so and points at the tracks, where the exams are.
 */
export default function CertificatesPage() {
  const { isLoading: authLoading } = useAuth()
  const { t, tf, language } = useI18n()
  const [view, setView] = useState<View>({ kind: 'loading' })
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [copied, setCopied] = useState<'idle' | 'ok' | 'failed'>('idle')
  // Bumped by "try again" to re-run the load below.
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    if (authLoading) return
    let alive = true
    ;(async () => {
      try {
        const rows = await api.getMyCertificates()
        if (!alive) return
        // Newest first: the one just earned is the one shown.
        const certificates = [...rows].sort((a, b) => Date.parse(b.issued_at) - Date.parse(a.issued_at))
        setView({ kind: 'ready', certificates })
        setSelectedId(certificates[0]?.certificate_id ?? null)
      } catch {
        if (alive) setView({ kind: 'error' })
      }
    })()
    return () => {
      alive = false
    }
  }, [authLoading, attempt])

  function retry() {
    setView({ kind: 'loading' })
    setAttempt((n) => n + 1)
  }

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  const certificates = view.kind === 'ready' ? view.certificates : []
  const selected = certificates.find(c => c.certificate_id === selectedId) ?? certificates[0] ?? null
  const verifyUrl = selected ? verifyUrlFor(selected.certificate_id) : ''

  async function copyLink() {
    try {
      await navigator.clipboard.writeText(verifyUrl)
      setCopied('ok')
    } catch {
      setCopied('failed')
    }
  }

  const dateFor = (iso: string) =>
    new Date(iso).toLocaleDateString(language === 'ar' ? 'ar-u-nu-latn-ca-gregory' : 'en-GB', {
      day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC',
    })

  return (
    <AppShell>
      <PageHeader
        title={t('nav.certificates')}
        subtitle={t('cert.subtitle')}
        contained
        action={selected && (
          <div className="flex flex-wrap gap-2.5">
            <Button variant="ghost" onClick={() => void copyLink()}>
              <Link2 size={14} aria-hidden="true" /> {t('cert.copyLink')}
            </Button>
            <a
              href={linkedInShareUrl(verifyUrl)}
              target="_blank"
              rel="noopener noreferrer"
              className={buttonStyles({ variant: 'ghost' })}
            >
              <ExternalLink size={14} aria-hidden="true" /> {t('cert.linkedin')}
            </a>
            <Button onClick={printCertificate}>
              <Download size={14} aria-hidden="true" /> {t('cert.pdf')}
            </Button>
          </div>
        )}
      />

      <PageBody className="space-y-6">
        {view.kind === 'loading' && (
          <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>
        )}

        {view.kind === 'error' && (
          <Card className="p-8 text-center">
            <p role="alert" className="mb-4 text-sm text-rose">{t('cert.loadError')}</p>
            <Button variant="ghost" onClick={retry}>{t('common.retry')}</Button>
          </Card>
        )}

        {view.kind === 'ready' && certificates.length === 0 && (
          <Card>
            <EmptyState
              icon={<Award size={32} aria-hidden="true" />}
              title={t('cert.empty.title')}
              description={t('cert.empty.body')}
              action={<Link href="/tracks" className={buttonStyles()}>{t('cert.empty.cta')}</Link>}
            />
          </Card>
        )}

        {selected && (
          <>
            <CourseCertificate
              variant="exam"
              examScore={selected.score}
              recipient={selected.user_name}
              title={selected.track_title}
              certificateId={selected.certificate_id}
              issuedAt={selected.issued_at}
              verifyUrl={verifyUrl}
            />

            <div className="flex flex-col gap-1.5">
              <label htmlFor="verify-link" className="text-xs text-dim">{t('cert.linkLabel')}</label>
              <input
                id="verify-link"
                readOnly
                dir="ltr"
                value={verifyUrl}
                onFocus={e => e.currentTarget.select()}
                className="w-full rounded-lg border border-border bg-surface px-3 py-2.5 font-mono text-xs text-bright outline-none focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
              />
              {/* Announced when it changes, seen by everyone: the button gives no other sign it worked. */}
              <p role="status" className={cn('min-h-[1rem] text-xs', copied === 'failed' ? 'text-rose' : 'text-emerald')}>
                {copied === 'ok' ? t('cert.copied') : copied === 'failed' ? t('cert.copyFailed') : ''}
              </p>
            </div>

            <section aria-labelledby="cert-history" className="flex flex-col gap-2.5">
              <h2 id="cert-history" className="text-sm font-semibold text-white">{t('cert.history')}</h2>
              <ul aria-labelledby="cert-history" className="flex flex-col gap-2.5">
                {certificates.map(cert => {
                  const active = cert.certificate_id === selected.certificate_id
                  return (
                    <li key={cert.certificate_id}>
                      <button
                        type="button"
                        aria-current={active || undefined}
                        onClick={() => { setSelectedId(cert.certificate_id); setCopied('idle') }}
                        className={cn(
                          'flex w-full min-h-[44px] flex-wrap items-center gap-3.5 rounded-[10px] border bg-surface px-4 py-3.5 text-start transition-colors',
                          active ? 'border-amber' : 'border-border hover:border-muted',
                        )}
                      >
                        <span aria-hidden="true" className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-amber text-on-amber">
                          <Award size={18} />
                        </span>
                        <span className="flex min-w-[12rem] flex-1 flex-col gap-0.5">
                          <span dir="auto" className="font-display text-sm font-bold text-white">{cert.track_title}</span>
                          <span className="text-xs text-ghost">
                            {tf('cert.examMeta', { date: dateFor(cert.issued_at), id: cert.certificate_id.replace(/-/g, '').slice(0, 8).toUpperCase() })}
                          </span>
                        </span>
                        <span className="rounded-full border border-emerald px-2.5 py-0.5 text-xs text-emerald">{t('cert.issued')}</span>
                      </button>
                    </li>
                  )
                })}
              </ul>
            </section>
          </>
        )}
      </PageBody>
    </AppShell>
  )
}
