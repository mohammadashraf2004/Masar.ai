'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { CheckCircle, XCircle } from 'lucide-react'
import axios from 'axios'
import { CourseCertificate } from '@/components/certificates/CourseCertificate'
import { Logo } from '@/components/layout/Logo'
import { LegalFooter } from '@/components/layout/LegalFooter'
import { buttonStyles } from '@/components/ui/Button'
import { Spinner } from '@/components/ui/index'
import { LanguageSwitcher } from '@/components/ui/LanguageSwitcher'
import { api } from '@/lib/api'
import { verifyUrlFor } from '@/lib/certificates'
import { useI18n } from '@/lib/i18n'
import type { CertificateSummary } from '@/types'

type View =
  | { kind: 'loading' }
  | { kind: 'found'; certificate: CertificateSummary }
  | { kind: 'missing' }
  | { kind: 'error' }

/**
 * The page a certificate's QR code and verification link open (handoff README §9).
 *
 * Public: an employer needs no account, so this sits outside the app shell and asks
 * for no sign-in. It answers one question - is this certificate real, and still valid -
 * and shows the certificate itself as the evidence.
 */
export default function VerifyCertificatePage() {
  const { id } = useParams() as { id: string }
  const { t } = useI18n()
  const [view, setView] = useState<View>({ kind: 'loading' })

  useEffect(() => {
    let alive = true
    api.verifyCertificate(id)
      .then(certificate => { if (alive) setView({ kind: 'found', certificate }) })
      .catch(err => {
        if (!alive) return
        setView(axios.isAxiosError(err) && err.response?.status === 404 ? { kind: 'missing' } : { kind: 'error' })
      })
    return () => { alive = false }
  }, [id])

  return (
    <div className="flex min-h-dvh flex-col bg-void px-4 pt-8 pb-[calc(1.25rem+env(safe-area-inset-bottom))] sm:px-6 lg:px-8">
      <div className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-8">
        <div className="flex items-center justify-between gap-3">
          <Link href="/" aria-label={t('cert.verify.home')}><Logo size={28} wordmarkClassName="text-sm" /></Link>
          <LanguageSwitcher />
        </div>

        <h1 className="font-display text-2xl font-bold text-white lg:text-[26px]">{t('cert.verify.title')}</h1>

        {view.kind === 'loading' && (
          <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>
        )}

        {view.kind === 'found' && (
          <>
            {view.certificate.is_valid ? (
              <p role="status" className="flex items-center gap-2 rounded-lg border border-emerald/20 bg-emerald/10 px-3 py-2.5 text-sm text-emerald">
                <CheckCircle size={16} aria-hidden="true" /> {t('cert.verify.valid')}
              </p>
            ) : (
              <p role="alert" className="flex items-center gap-2 rounded-lg border border-rose/20 bg-rose/10 px-3 py-2.5 text-sm text-rose">
                <XCircle size={16} aria-hidden="true" /> {t('cert.verify.revoked')}
              </p>
            )}
            <CourseCertificate
              variant="exam"
              examScore={view.certificate.score}
              recipient={view.certificate.user_name}
              title={view.certificate.track_title}
              certificateId={view.certificate.certificate_id}
              issuedAt={view.certificate.issued_at}
              verifyUrl={verifyUrlFor(view.certificate.certificate_id)}
            />
          </>
        )}

        {(view.kind === 'missing' || view.kind === 'error') && (
          <p role="alert" className="flex items-center gap-2 rounded-lg border border-rose/20 bg-rose/10 px-3 py-2.5 text-sm text-rose">
            <XCircle size={16} aria-hidden="true" />
            {view.kind === 'missing' ? t('cert.verify.notFound') : t('cert.verify.error')}
          </p>
        )}

        <Link href="/" className={buttonStyles({ variant: 'ghost', className: 'self-start' })}>{t('cert.verify.home')}</Link>
      </div>
      <LegalFooter className="mx-auto w-full max-w-5xl" />
    </div>
  )
}
