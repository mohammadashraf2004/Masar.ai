'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { ReferenceNumber } from '@/components/billing/ReferenceNumber'
import { RefundPolicySummary } from '@/components/billing/RefundPolicySummary'
import { api } from '@/lib/api'
import { useMoney } from '@/lib/billing/money'
import { useRefundI18n } from '@/lib/billing/refundI18n'
import type { RefundStatus, SubscriptionOrder } from '@/lib/billing/types'

const statusKey: Record<RefundStatus, 'notRequested' | 'requested' | 'underReview' | 'approved' | 'rejected' | 'processing' | 'refunded' | 'failed'> = {
  not_requested: 'notRequested', requested: 'requested', under_review: 'underReview',
  approved: 'approved', rejected: 'rejected', processing: 'processing', refunded: 'refunded', failed: 'failed',
}

export default function SubscriptionOrderPage() {
  const params = useParams<{ reference: string }>()
  const reference = decodeURIComponent(params.reference)
  const { language, t } = useRefundI18n()
  const [order, setOrder] = useState<SubscriptionOrder | null>(null)
  const [notFound, setNotFound] = useState(false)
  const [reason, setReason] = useState('')
  const [confirmed, setConfirmed] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(false)
  const { money } = useMoney(order?.currency ?? 'EGP')

  useEffect(() => {
    let active = true
    api.getSubscriptionOrder(reference)
      .then((value) => { if (active) setOrder(value) })
      .catch(() => { if (active) setNotFound(true) })
    return () => { active = false }
  }, [reference])

  async function submit() {
    if (!order || !confirmed || reason.trim().length < 5) return
    setSubmitting(true)
    setError(false)
    try {
      const updated = await api.requestSubscriptionRefund(order.reference_number, {
        reason: reason.trim(), confirmed: true, idempotency_key: crypto.randomUUID(),
      })
      setOrder(updated)
    } catch {
      setError(true)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AppShell>
      <PageHeader title={t('details')} subtitle={reference} contained />
      <PageBody className="space-y-5">
        {!order && !notFound && <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>}
        {notFound && <Card className="p-8 text-center text-sm text-dim">Order not found.</Card>}
        {order && (
          <>
            <Card className="space-y-5 p-5">
              <ReferenceNumber value={order.reference_number} showHelp />
              <dl className="grid gap-4 text-sm sm:grid-cols-2">
                <div><dt className="text-xs text-ghost">{t('paymentDate')}</dt><dd className="mt-1 text-soft">{new Date(order.paid_at ?? order.created_at).toLocaleString(language)}</dd></div>
                <div><dt className="text-xs text-ghost">{t('amount')}</dt><dd className="mt-1 font-mono text-soft">{money(order.amount / 100)}</dd></div>
                <div><dt className="text-xs text-ghost">{t('subscription')}</dt><dd className="mt-1 text-soft">{order.plan.toUpperCase()} · {order.billing_period}</dd></div>
                <div><dt className="text-xs text-ghost">{t('refundStatus')}</dt><dd className="mt-1 font-semibold text-soft">{t(statusKey[order.refund.status])}</dd></div>
              </dl>
            </Card>

            {order.refund.status !== 'not_requested' && (
              <Card className="p-5 text-center">
                <h2 className="text-base font-semibold text-white">
                  {order.refund.status === 'requested' || order.refund.status === 'under_review' ? t('received') : t(statusKey[order.refund.status])}
                </h2>
                <div className="mt-3"><ReferenceNumber value={order.reference_number} /></div>
                <p className="mt-2 text-sm text-dim">{t('refundStatus')}: {t(statusKey[order.refund.status])}</p>
              </Card>
            )}

            {order.refund_eligible && order.refund.status === 'not_requested' && (
              <Card className="space-y-4 p-5">
                <h2 className="text-base font-semibold text-white">{t('requestRefund')}</h2>
                <dl className="grid gap-2 rounded-lg bg-panel p-3 text-xs sm:grid-cols-2">
                  <div><dt className="text-ghost">{t('reference')}</dt><dd dir="ltr" className="font-mono text-soft">{order.reference_number}</dd></div>
                  <div><dt className="text-ghost">{t('paymentDate')}</dt><dd className="text-soft">{new Date(order.paid_at!).toLocaleDateString(language)}</dd></div>
                  <div><dt className="text-ghost">{t('amount')}</dt><dd className="font-mono text-soft">{money(order.amount / 100)}</dd></div>
                  <div><dt className="text-ghost">{t('subscription')}</dt><dd className="text-soft">{order.plan.toUpperCase()} · {order.billing_period}</dd></div>
                </dl>
                <RefundPolicySummary />
                <label className="block text-xs font-semibold text-soft">
                  {t('reason')}
                  <textarea
                    value={reason}
                    onChange={(event) => setReason(event.target.value)}
                    placeholder={t('reasonPlaceholder')}
                    maxLength={2000}
                    className="mt-2 min-h-28 w-full rounded-lg border border-border bg-surface p-3 text-sm font-normal text-white outline-none focus:border-amber"
                  />
                </label>
                <label className="flex items-start gap-2 text-xs leading-relaxed text-dim">
                  <input type="checkbox" checked={confirmed} onChange={(event) => setConfirmed(event.target.checked)} className="mt-0.5" />
                  <span>{t('confirm')}</span>
                </label>
                {error && <p role="alert" className="text-xs text-rose">{t('requestError')}</p>}
                <Button onClick={() => void submit()} loading={submitting} disabled={!confirmed || reason.trim().length < 5}>
                  {t('submit')}
                </Button>
              </Card>
            )}

            <RefundPolicySummary compact />
            <Link href="/billing/orders" className={buttonStyles({ variant: 'ghost' })}>{t('backToPayments')}</Link>
          </>
        )}
      </PageBody>
    </AppShell>
  )
}
