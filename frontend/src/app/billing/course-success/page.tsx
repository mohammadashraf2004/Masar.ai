'use client'
import { Suspense, useEffect, useState } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { Check, Clock, XCircle } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import type { BillingOrder } from '@/types'

export default function CoursePaymentResultPage() {
  return <Suspense fallback={null}><CoursePaymentResult /></Suspense>
}

function CoursePaymentResult() {
  const { isLoading: authLoading } = useAuth()
  const params = useSearchParams()
  const orderId = Number(params.get('order_id'))
  const [order, setOrder] = useState<BillingOrder | null>(null)
  const [fetchFailed, setFailed] = useState(false)
  // A missing or malformed order id is known from the URL alone: no request, no effect.
  const badId = !Number.isInteger(orderId) || orderId <= 0
  const failed = fetchFailed || badId

  useEffect(() => {
    if (authLoading || badId) return
    let alive = true
    let timer: ReturnType<typeof setTimeout> | undefined
    let attempts = 0
    const load = async () => {
      try {
        const next = await api.getBillingOrder(orderId)
        if (!alive) return
        setOrder(next)
        attempts += 1
        if (next.status === 'pending' && attempts < 6) timer = setTimeout(load, 2000)
      } catch {
        if (alive) setFailed(true)
      }
    }
    void load()
    return () => { alive = false; if (timer) clearTimeout(timer) }
  }, [authLoading, orderId, badId])

  if (authLoading) return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>

  const paid = order?.status === 'paid'
  const pending = order?.status === 'pending'

  return (
    <AppShell>
      <PageHeader title="Course payment" contained />
      <PageBody>
        {!order && !failed && <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>}
        {failed && <Card className="mx-auto max-w-md p-8 text-center text-sm text-rose" role="alert">We could not find this order.</Card>}
        {order && (
          <Card className="mx-auto flex max-w-md flex-col items-center gap-4 p-8 text-center">
            {paid ? <Check size={34} className="text-emerald" /> : pending ? <Clock size={34} className="text-amber-text" /> : <XCircle size={34} className="text-rose" />}
            <h2 className="text-lg font-bold text-white">
              {paid ? 'Payment confirmed' : pending ? "We're confirming your payment" : 'Payment was not completed'}
            </h2>
            <p className="text-sm leading-relaxed text-dim">
              {paid ? 'Your course is now available.' : pending ? 'Payment received. The secure webhook confirmation may take a moment.' : 'No course access was granted.'}
            </p>
            <p className="text-sm font-medium text-bright" dir="auto">{order.course.title_ar || order.course.title}</p>
            {paid ? (
              <Link href={`/courses/${order.course.slug}`} className={buttonStyles({ size: 'lg' })}>Start Course</Link>
            ) : (
              <Link href={`/courses/${order.course.slug}`} className={buttonStyles({ variant: 'ghost' })}>Back to course</Link>
            )}
          </Card>
        )}
      </PageBody>
    </AppShell>
  )
}
