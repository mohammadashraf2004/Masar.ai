'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { Button } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { ReferenceNumber } from '@/components/billing/ReferenceNumber'
import { api } from '@/lib/api'
import { useAuth } from '@/hooks/useAuth'
import type { RefundStatus, SubscriptionOrder } from '@/lib/billing/types'

type AdminOrder = SubscriptionOrder & {
  id: number
  customer: { email: string; name: string }
  provider_transaction_id: string | null
  refund_admin_note?: string | null
}

type AdminRefundStatus = Exclude<RefundStatus, 'not_requested' | 'requested'>
const nextStatuses: Partial<Record<RefundStatus, AdminRefundStatus[]>> = {
  requested: ['under_review', 'rejected'],
  under_review: ['approved', 'rejected'],
  approved: ['processing', 'rejected'],
  processing: ['refunded', 'failed'],
  failed: ['processing', 'rejected'],
}

export default function AdminBillingPage() {
  const router = useRouter()
  const { user, isLoading } = useAuth()
  const [filters, setFilters] = useState({ reference_number: '', provider_transaction_id: '', customer: '', order_id: '' })
  const [orders, setOrders] = useState<AdminOrder[] | null>(null)
  const [selected, setSelected] = useState<AdminOrder | null>(null)
  const [nextStatus, setNextStatus] = useState<AdminRefundStatus>('under_review')
  const [note, setNote] = useState('')
  const [providerReference, setProviderReference] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    if (!isLoading && user?.role !== 'admin') router.replace('/')
  }, [isLoading, router, user])

  async function search() {
    setBusy(true)
    try {
      const rows = await api.adminSubscriptionOrders({
        reference_number: filters.reference_number || undefined,
        provider_transaction_id: filters.provider_transaction_id || undefined,
        customer: filters.customer || undefined,
        order_id: filters.order_id ? Number(filters.order_id) : undefined,
      })
      setOrders(rows)
    } finally {
      setBusy(false)
    }
  }

  async function open(reference: string) {
    const detail = await api.adminSubscriptionOrder(reference)
    setSelected(detail)
    const first = nextStatuses[detail.refund.status]?.[0]
    if (first) setNextStatus(first)
  }

  async function transition() {
    if (!selected) return
    setBusy(true)
    try {
      const updated = await api.adminTransitionRefund(selected.reference_number, {
        status: nextStatus,
        idempotency_key: crypto.randomUUID(),
        note: note || undefined,
        provider_reference: providerReference || undefined,
      })
      setSelected({ ...selected, ...updated })
      await search()
    } finally {
      setBusy(false)
    }
  }

  if (isLoading || user?.role !== 'admin') return <div className="grid min-h-dvh place-items-center bg-void"><Spinner announce /></div>

  return (
    <AppShell>
      <PageHeader title="Admin billing" subtitle="Search subscription payments and review the complete refund timeline." contained />
      <PageBody className="space-y-5">
        <Card className="grid gap-3 p-5 sm:grid-cols-2 lg:grid-cols-4">
          {([
            ['reference_number', 'Masar reference'], ['provider_transaction_id', 'Provider transaction'],
            ['customer', 'Customer email or name'], ['order_id', 'Order ID'],
          ] as const).map(([key, label]) => (
            <label key={key} className="text-xs text-dim">{label}
              <input
                value={filters[key]}
                onChange={(event) => setFilters((current) => ({ ...current, [key]: event.target.value }))}
                className="mt-1 block h-10 w-full rounded-lg border border-border bg-surface px-3 text-sm text-white outline-none focus:border-amber"
              />
            </label>
          ))}
          <Button onClick={() => void search()} loading={busy}>Search payments</Button>
        </Card>

        {orders?.map((order) => (
          <Card key={order.reference_number} className="flex flex-wrap items-center justify-between gap-3 p-4 hover:border-amber/50">
            <div><ReferenceNumber value={order.reference_number} /><p className="mt-1 text-xs text-ghost">{order.customer.email} · order {order.id}</p></div>
            <div className="text-end text-xs text-dim"><p>Payment: {order.status}</p><p>Refund: {order.refund.status}</p>
              <button type="button" onClick={() => void open(order.reference_number)} className="mt-2 min-h-9 font-semibold text-amber-text">Open details</button>
            </div>
          </Card>
        ))}

        {selected && (
          <Card className="space-y-5 p-5">
            <ReferenceNumber value={selected.reference_number} />
            <dl className="grid gap-3 text-xs sm:grid-cols-2 lg:grid-cols-4">
              <div><dt className="text-ghost">Customer</dt><dd className="text-soft">{selected.customer.email}</dd></div>
              <div><dt className="text-ghost">Order ID</dt><dd className="font-mono text-soft">{selected.id}</dd></div>
              <div><dt className="text-ghost">Provider transaction</dt><dd className="font-mono text-soft">{selected.provider_transaction_id ?? '—'}</dd></div>
              <div><dt className="text-ghost">Refund</dt><dd className="text-soft">{selected.refund.status}</dd></div>
            </dl>
            <div>
              <h2 className="text-sm font-semibold text-white">Payment and refund timeline</h2>
              <ol className="mt-3 space-y-2 border-s border-border ps-4">
                {selected.timeline?.map((event, index) => (
                  <li key={`${event.created_at}-${index}`} className="text-xs text-dim">
                    <span className="font-semibold text-soft">{event.type}: {event.status}</span> · {new Date(event.created_at).toLocaleString()}
                  </li>
                ))}
              </ol>
            </div>
            {selected.refund.status !== 'not_requested' && selected.refund.status !== 'refunded' && selected.refund.status !== 'rejected' && (
              <div className="grid gap-3 border-t border-border pt-4 sm:grid-cols-2">
                <label className="text-xs text-dim">Next status
                  <select value={nextStatus} onChange={(event) => setNextStatus(event.target.value as typeof nextStatus)} className="mt-1 block h-10 w-full rounded-lg border border-border bg-surface px-3 text-sm text-white">
                    {(nextStatuses[selected.refund.status] ?? []).map((value) => <option key={value}>{value}</option>)}
                  </select>
                </label>
                <label className="text-xs text-dim">Provider refund reference
                  <input value={providerReference} onChange={(event) => setProviderReference(event.target.value)} className="mt-1 block h-10 w-full rounded-lg border border-border bg-surface px-3 text-sm text-white" />
                </label>
                <label className="text-xs text-dim sm:col-span-2">Admin note
                  <textarea value={note} onChange={(event) => setNote(event.target.value)} className="mt-1 block min-h-20 w-full rounded-lg border border-border bg-surface p-3 text-sm text-white" />
                </label>
                <Button onClick={() => void transition()} loading={busy}>Record transition</Button>
              </div>
            )}
          </Card>
        )}
      </PageBody>
    </AppShell>
  )
}
