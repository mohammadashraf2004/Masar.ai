'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { Card, Spinner } from '@/components/ui/index'
import { ReferenceNumber } from '@/components/billing/ReferenceNumber'
import { RefundPolicySummary } from '@/components/billing/RefundPolicySummary'
import { api } from '@/lib/api'
import { useAuth } from '@/hooks/useAuth'
import { useMoney } from '@/lib/billing/money'
import { useRefundI18n } from '@/lib/billing/refundI18n'
import type { RefundStatus, SubscriptionOrder } from '@/lib/billing/types'

const statusKey: Record<RefundStatus, Parameters<ReturnType<typeof useRefundI18n>['t']>[0]> = {
  not_requested: 'notRequested', requested: 'requested', under_review: 'underReview',
  approved: 'approved', rejected: 'rejected', processing: 'processing',
  refunded: 'refunded', failed: 'failed',
}

export default function BillingOrdersPage() {
  // The account's own orders: signed-out visitors are sent to sign in.
  useAuth()
  const { language, t } = useRefundI18n()
  const { money } = useMoney('EGP')
  const [orders, setOrders] = useState<SubscriptionOrder[] | null>(null)
  const [subscription, setSubscription] = useState<Awaited<ReturnType<typeof api.getMySubscription>> | null>(null)

  useEffect(() => {
    let active = true
    Promise.all([api.getSubscriptionOrders(), api.getMySubscription()])
      .then(([items, current]) => { if (active) { setOrders(items); setSubscription(current) } })
      .catch(() => { if (active) setOrders([]) })
    return () => { active = false }
  }, [])

  return (
    <AppShell>
      <PageHeader title={t('history')} subtitle={t('historySubtitle')} contained />
      <PageBody className="space-y-5">
        {subscription?.subscription && (
          <Card className="p-5">
            <h2 className="text-sm font-semibold text-white">{t('subscription')}</h2>
            <dl className="mt-3 grid gap-3 text-xs sm:grid-cols-3">
              <div><dt className="text-ghost">Plan</dt><dd className="mt-1 text-soft">{subscription.subscription.plan.toUpperCase()}</dd></div>
              <div><dt className="text-ghost">Status</dt><dd className="mt-1 text-soft">{subscription.subscription.status}</dd></div>
              <div><dt className="text-ghost">Current period ends</dt><dd className="mt-1 text-soft">{new Date(subscription.subscription.current_period_end).toLocaleDateString(language)}</dd></div>
            </dl>
            <p className="mt-3 text-xs text-dim">{t('cancellationNote')} {t('cancellation')}</p>
          </Card>
        )}

        {!orders && <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>}
        {orders?.length === 0 && <Card className="p-8 text-center text-sm text-dim">{t('noOrders')}</Card>}
        {orders?.map((order) => (
          <Card key={order.reference_number} className="p-5">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div className="space-y-2">
                <ReferenceNumber value={order.reference_number} />
                <p className="text-xs text-dim">
                  {order.plan.toUpperCase()} · {order.billing_period} · {money(order.amount / 100)}
                </p>
                <p className="text-xs text-ghost">
                  {t('paymentDate')}: {new Date(order.paid_at ?? order.created_at).toLocaleDateString(language)}
                </p>
              </div>
              <div className="text-end">
                <p className="text-xs text-ghost">{t('refundStatus')}</p>
                <p className="mt-1 text-sm font-semibold text-soft">{t(statusKey[order.refund.status])}</p>
                <Link
                  href={`/billing/orders/${encodeURIComponent(order.reference_number)}`}
                  className="mt-3 inline-flex min-h-[40px] items-center text-xs font-semibold text-amber-text hover:underline"
                >
                  {t('details')}
                </Link>
              </div>
            </div>
          </Card>
        ))}
        <RefundPolicySummary />
      </PageBody>
    </AppShell>
  )
}

