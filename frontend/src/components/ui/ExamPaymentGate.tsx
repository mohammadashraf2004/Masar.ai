'use client'
import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { Spinner } from '@/components/ui/index'
import {
  ShieldCheck, X, CheckCircle, AlertTriangle,
  Zap, Banknote, Clock
} from 'lucide-react'
import { Button } from '@/components/ui/Button'

interface ExamPaymentGateProps {
  examId: number
  examTitle: string
  onPaid: () => void       // called when payment confirmed → start exam
  onClose: () => void
}

const PAYMENT_LABELS: Record<string, string> = {
  fawry:         'Fawry',
  instapay:      'InstaPay',
  vodafone_cash: 'Vodafone Cash',
}

const PAYMENT_ICONS: Record<string, string> = {
  fawry:         '🟡',
  instapay:      '🔵',
  vodafone_cash: '🔴',
}

const PAYMENT_INSTRUCTIONS: Record<string, (price: number) => string[]> = {
  fawry: (p) => [
    `Open the Fawry app or visit any Fawry outlet`,
    `Pay ${p} EGP using service code AI-CAREER-EXAM`,
    `Enter the receipt reference number below`,
  ],
  instapay: (p) => [
    `Open your bank's InstaPay service`,
    `Transfer ${p} EGP to payments@aicareer.eg`,
    `Use your registered email as the transfer note`,
    `Enter the transaction ID below`,
  ],
  vodafone_cash: (p) => [
    `Open Vodafone Cash app or dial *9#`,
    `Send ${p} EGP to 01XXXXXXXXX`,
    `Enter the confirmation code you receive below`,
  ],
}

export function ExamPaymentGate({ examId, examTitle, onPaid, onClose }: ExamPaymentGateProps) {
  const [price, setPrice]       = useState<number | null>(null)
  const [method, setMethod]     = useState('')
  const [ref, setRef]           = useState('')
  const [loading, setLoading]   = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [submitted, setSubmitted]   = useState(false)
  const [alreadyPaid, setAlreadyPaid] = useState(false)
  const [error, setError]       = useState('')
  const [showManual, setShowManual] = useState(false)
  const [payingVia, setPayingVia] = useState<'card' | 'wallet' | null>(null)
  const [walletPhone, setWalletPhone] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const [priceData, statusData] = await Promise.all([
          api.getExamPaymentPrice(),
          api.getExamPaymentStatus(examId),
        ])
        setPrice(priceData.egp_price)
        if (statusData.paid) {
          setAlreadyPaid(true)
        }
      } catch {}
      setLoading(false)
    }
    load()
  }, [examId])

  const handleSubmit = async () => {
    if (!method) { setError('Please select a payment method.'); return }
    if (!ref.trim()) { setError('Please enter your payment reference number.'); return }
    setSubmitting(true)
    setError('')
    try {
      await api.submitExamPayment({ exam_id: examId, payment_method: method, payment_ref: ref.trim() })
      setSubmitted(true)
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? 'Submission failed. Please try again.')
    }
    setSubmitting(false)
  }

  const handlePayNow = async (via: 'card' | 'wallet') => {
    if (via === 'wallet' && !walletPhone.trim()) {
      setError('Please enter the mobile number to charge.')
      return
    }
    setPayingVia(via)
    setError('')
    try {
      const { checkout_url } = await api.initExamPayment({
        exam_id: examId,
        method: via,
        phone_number: via === 'wallet' ? walletPhone.trim() : undefined,
      })
      window.location.href = checkout_url
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? 'Could not start checkout. Please try again.')
      setPayingVia(null)
    }
  }

  return (
    <>
      <div className="fixed inset-0 bg-void/80 backdrop-blur-sm z-40" onClick={onClose} />
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="bg-ink border border-border rounded-xl shadow-2xl w-full max-w-md pointer-events-auto flex flex-col max-h-[90vh]">

          {/* Header */}
          <div className="flex items-center justify-between px-5 py-4 border-b border-border flex-shrink-0">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-md bg-amber/10 border border-amber/20 flex items-center justify-center">
                <ShieldCheck size={14} className="text-amber" />
              </div>
              <div>
                <h2 className="text-sm font-semibold text-bright">Exam Access</h2>
                <p className="text-xs text-ghost truncate max-w-48">{examTitle}</p>
              </div>
            </div>
            <button onClick={onClose} className="w-11 h-11 lg:w-7 lg:h-7 rounded flex items-center justify-center text-ghost hover:text-bright hover:bg-surface transition-colors">
              <X size={15} />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-5 space-y-5">
            {loading ? (
              <div className="flex justify-center py-8"><Spinner className="w-5 h-5" /></div>

            ) : alreadyPaid ? (
              /* Already paid — can start */
              <div className="text-center py-6">
                <CheckCircle size={40} className="text-emerald mx-auto mb-4" />
                <p className="text-bright font-semibold mb-2">Payment Confirmed</p>
                <p className="text-xs text-ghost mb-6">Your payment for this exam has been verified. You can start the exam now.</p>
                <Button className="w-full" onClick={onPaid}>
                  <ShieldCheck size={13} /> Start Exam
                </Button>
              </div>

            ) : submitted ? (
              /* Submitted — waiting for confirmation */
              <div className="text-center py-6">
                <Clock size={40} className="text-amber mx-auto mb-4" />
                <p className="text-bright font-semibold mb-2">Payment Submitted</p>
                <p className="text-xs text-ghost leading-relaxed mb-2">
                  Your payment reference has been received. Exam access will be granted after confirmation — usually within <strong className="text-soft">1 hour</strong>.
                </p>
                <p className="text-xs text-ghost mb-6">
                  Check back later or contact support if it takes longer.
                </p>
                <Button variant="outline" className="w-full" onClick={onClose}>
                  Close
                </Button>
              </div>

            ) : (
              <>
                {/* Important notice */}
                <div className="flex items-start gap-2.5 px-4 py-3 bg-amber/5 border border-amber/20 rounded-lg">
                  <Banknote size={14} className="text-amber flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-xs font-semibold text-amber mb-0.5">EGP Payment Only</p>
                    <p className="text-xs text-ghost leading-relaxed">
                      Certification exams require a real EGP payment. Credits cannot be used. This ensures your certificate is a verified, paid credential.
                    </p>
                  </div>
                </div>

                {/* Price */}
                <div className="flex items-center justify-between py-3 px-4 bg-surface border border-border rounded-lg">
                  <span className="text-xs text-ghost">Exam fee</span>
                  <span className="text-2xl font-mono font-bold text-amber">{price} EGP</span>
                </div>

                {error && (
                  <div className="flex items-start gap-2 px-3 py-2.5 rounded-lg bg-rose/10 border border-rose/20">
                    <AlertTriangle size={12} className="text-rose flex-shrink-0 mt-0.5" />
                    <p className="text-xs text-rose">{error}</p>
                  </div>
                )}

                {/* Pay now — real Paymob checkout, instant confirmation */}
                <div className="space-y-2">
                  <Button className="w-full" onClick={() => handlePayNow('card')} loading={payingVia === 'card'} disabled={!!payingVia}>
                    💳 Pay {price} EGP by Card
                  </Button>
                  <div className="flex gap-2">
                    <input
                      className="flex-1 bg-surface border border-border rounded-lg px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 font-mono"
                      placeholder="01XXXXXXXXX"
                      value={walletPhone}
                      onChange={e => setWalletPhone(e.target.value)}
                    />
                    <Button variant="outline" onClick={() => handlePayNow('wallet')} loading={payingVia === 'wallet'} disabled={!!payingVia}>
                      📱 Pay by Wallet
                    </Button>
                  </div>
                  <p className="text-xs text-ghost text-center">
                    Secure checkout via Paymob · access granted automatically once paid
                  </p>
                </div>

                {/* Manual fallback (Fawry / InstaPay / bank transfer) */}
                <button
                  onClick={() => setShowManual(s => !s)}
                  className="text-xs text-ghost hover:text-soft underline decoration-dotted underline-offset-2 w-full text-center"
                >
                  {showManual ? 'Hide manual payment options' : 'Already paid via Fawry / InstaPay? Submit manually'}
                </button>

                {showManual && (
                  <>
                    <div>
                      <p className="text-xs text-ghost uppercase tracking-widest font-medium mb-2">Payment method</p>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                        {Object.entries(PAYMENT_LABELS).map(([key, label]) => (
                          <button
                            key={key}
                            onClick={() => setMethod(key)}
                            className={`py-3 rounded-lg border text-xs font-medium transition-all ${
                              method === key
                                ? 'bg-amber/10 border-amber/40 text-amber'
                                : 'bg-surface border-border text-ghost hover:text-soft hover:border-amber/20'
                            }`}
                          >
                            <div className="text-lg mb-0.5">{PAYMENT_ICONS[key]}</div>
                            {label}
                          </button>
                        ))}
                      </div>
                    </div>

                    {method && price && (
                      <div className="bg-surface border border-border rounded-lg p-4">
                        <p className="text-xs font-semibold text-bright mb-2.5">How to pay via {PAYMENT_LABELS[method]}:</p>
                        <ol className="space-y-2">
                          {PAYMENT_INSTRUCTIONS[method](price).map((step, i) => (
                            <li key={i} className="flex items-start gap-2 text-xs text-ghost">
                              <span className="w-4 h-4 rounded-full bg-amber/10 border border-amber/20 text-amber flex items-center justify-center text-xs font-mono flex-shrink-0">
                                {i + 1}
                              </span>
                              {step}
                            </li>
                          ))}
                        </ol>
                      </div>
                    )}

                    <div>
                      <label className="text-xs font-medium text-soft uppercase tracking-widest block mb-1.5">
                        Payment reference / transaction ID
                      </label>
                      <input
                        className="w-full bg-surface border border-border rounded-lg px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 font-mono"
                        placeholder="e.g. FWR-123456789"
                        value={ref}
                        onChange={e => setRef(e.target.value)}
                      />
                    </div>

                    <Button
                      className="w-full"
                      onClick={handleSubmit}
                      loading={submitting}
                      disabled={!method || !ref.trim()}
                    >
                      Submit Payment Reference
                    </Button>

                    <p className="text-xs text-ghost text-center">
                      Access granted after manual verification · usually within 1 hour
                    </p>
                  </>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </>
  )
}