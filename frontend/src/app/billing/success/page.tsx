'use client'
import { Suspense, useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { Check } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { billingCatalog } from '@/lib/billing/catalog'
import { getPaymentProvider, type PaymentReceipt } from '@/lib/billing/payments'
import { formatAmount } from '@/lib/billing/pricing'
import type { BillingCatalog } from '@/lib/billing/types'
import { useI18n, type StringKey } from '@/lib/i18n'

type View = { kind: 'loading' } | { kind: 'none' } | { kind: 'paid'; receipt: PaymentReceipt; catalog: BillingCatalog }

export default function BillingSuccessPage() {
  return (
    <Suspense fallback={null}>
      <BillingSuccessInner />
    </Suspense>
  )
}

/**
 * Where a payment lands (`/billing/success?invoice=...`): after the provider confirms it,
 * whether by an in-page result, a gateway redirect or a webhook. It shows only what the
 * provider says that invoice was, never what the address claims, so a made-up link shows
 * "we could not find that payment" instead of a success.
 */
function BillingSuccessInner() {
  const { isLoading: authLoading } = useAuth()
  const { t, tf } = useI18n()
  const invoice = useSearchParams().get('invoice') ?? ''
  const provider = useMemo(() => getPaymentProvider(), [])
  const [view, setView] = useState<View>({ kind: 'loading' })

  useEffect(() => {
    if (authLoading) return
    let alive = true
    ;(async () => {
      try {
        const [receipt, catalog] = await Promise.all([
          provider && invoice ? provider.getReceipt(invoice) : Promise.resolve(null),
          billingCatalog.load(),
        ])
        if (alive) setView(receipt ? { kind: 'paid', receipt, catalog } : { kind: 'none' })
      } catch {
        if (alive) setView({ kind: 'none' })
      }
    })()
    return () => {
      alive = false
    }
  }, [authLoading, invoice, provider])

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  function message(receipt: PaymentReceipt, catalog: BillingCatalog): string {
    if (receipt.cart.type === 'plan') {
      return tf('billing.success.plan', {
        name: t(`billing.plan.${receipt.cart.id}.name` as StringKey),
        cycle: t(receipt.cycle === 'yearly' ? 'billing.yearly' : 'billing.monthly'),
      })
    }
    const packId = receipt.cart.id
    const pack = catalog.packs.find((p) => p.id === packId)
    return tf('billing.success.pack', { credits: formatAmount(pack ? pack.credits + pack.bonus : 0) })
  }

  return (
    <AppShell>
      <PageHeader title={t('billing.title')} contained />
      <PageBody>
        {view.kind === 'loading' && <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>}

        {view.kind === 'none' && (
          <Card className="mx-auto flex max-w-md flex-col items-center gap-4 p-8 text-center">
            <p role="alert" className="text-sm text-dim">{t('billing.success.none')}</p>
            <Link href="/billing" className={buttonStyles({ variant: 'ghost' })}>{t('billing.success.back')}</Link>
          </Card>
        )}

        {view.kind === 'paid' && (
          <Card className="mx-auto flex max-w-md flex-col items-center gap-3 px-6 py-10 text-center">
            <span aria-hidden="true" className="grid h-14 w-14 place-items-center rounded-full bg-amber text-on-amber">
              <Check size={26} strokeWidth={2.6} />
            </span>
            <h2 className="text-lg font-bold text-white">{t('billing.success.title')}</h2>
            <p className="text-[13px] leading-[1.7] text-dim">{message(view.receipt, view.catalog)}</p>
            <span dir="ltr" className="font-mono text-xs text-ghost">{view.receipt.invoiceId}</span>
            {provider?.isMock && <p className="text-xs leading-relaxed text-amber-text">{t('billing.mock')}</p>}
            <div className="mt-1.5 flex flex-wrap justify-center gap-2.5">
              <Link href="/dashboard" className={buttonStyles({ size: 'lg' })}>{t('billing.success.home')}</Link>
              <Button variant="ghost" size="lg" onClick={() => void provider?.downloadInvoice(view.receipt.invoiceId)}>
                {t('billing.success.download')}
              </Button>
            </div>
          </Card>
        )}
      </PageBody>
    </AppShell>
  )
}
