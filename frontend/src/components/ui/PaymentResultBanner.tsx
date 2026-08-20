'use client'
import { useEffect, useState, useRef } from 'react'
import { useSearchParams, useRouter, usePathname } from 'next/navigation'
import { api } from '@/lib/api'
import { CheckCircle, XCircle, Clock, X } from 'lucide-react'

// Mounted on the dashboard — where Paymob's checkout redirect now lands
// (?payment_ref=...). Deliberately does not trust anything in the URL
// itself; it only shows what our own authenticated status endpoint
// reports, which only reflects what the server-side webhook has
// actually confirmed.
export function PaymentResultBanner() {
  const params = useSearchParams()
  const router = useRouter()
  const pathname = usePathname()
  const ref = params.get('payment_ref') ?? ''
  const [status, setStatus] = useState<'pending' | 'confirmed' | 'failed' | null>(null)
  const [kind, setKind] = useState<'wallet_topup' | 'exam_payment' | null>(null)
  const attempts = useRef(0)

  useEffect(() => {
    if (!ref) return
    let cancelled = false
    setStatus('pending')

    async function poll() {
      try {
        const data = await api.getPaymentStatus(ref)
        if (cancelled) return
        setKind(data.kind)
        if (data.status === 'confirmed' || data.status === 'failed') {
          setStatus(data.status)
          return
        }
      } catch {
        // briefly possible if the webhook hasn't landed yet — keep polling
      }
      attempts.current += 1
      if (attempts.current < 15 && !cancelled) setTimeout(poll, 2000)
    }
    poll()
    return () => { cancelled = true }
  }, [ref])

  if (!ref || !status) return null

  const dismiss = () => router.replace(pathname)

  return (
    <div className={`mb-4 flex items-center gap-3 px-4 py-3 rounded-lg border ${
      status === 'confirmed' ? 'bg-emerald/5 border-emerald/20' :
      status === 'failed'    ? 'bg-rose/5 border-rose/20' :
                                'bg-amber/5 border-amber/20'
    }`}>
      {status === 'pending'   && <Clock size={16} className="text-amber flex-shrink-0" />}
      {status === 'confirmed' && <CheckCircle size={16} className="text-emerald flex-shrink-0" />}
      {status === 'failed'    && <XCircle size={16} className="text-rose flex-shrink-0" />}
      <p className="text-sm flex-1">
        {status === 'pending' && 'Confirming your payment… this usually takes a few seconds.'}
        {status === 'confirmed' && (kind === 'wallet_topup' ? 'Payment confirmed — your credits have been added.' : 'Payment confirmed — you now have access to the exam.')}
        {status === 'failed' && "Payment wasn't completed. No charge should apply — please try again."}
      </p>
      <button onClick={dismiss} className="text-ghost hover:text-soft flex-shrink-0">
        <X size={14} />
      </button>
    </div>
  )
}
