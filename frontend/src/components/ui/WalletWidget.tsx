'use client'
import { useState, useEffect, useCallback } from 'react'
import { api } from '@/lib/api'
import { Spinner } from '@/components/ui/index'
import {
  Zap, Plus, X, CheckCircle, Clock,
  ChevronRight, AlertTriangle, Banknote,
  ArrowDownLeft, ArrowUpRight, Gift
} from 'lucide-react'

// ─── Types ────────────────────────────────────────────────────────────────────
interface Wallet {
  credit_balance: number
  lifetime_purchased: number
  lifetime_spent: number
}

interface Package {
  id: number
  name: string
  credits: number
  egp_price: number
  bonus_credits: number
  is_popular: boolean
  description: string
}

interface Transaction {
  id: number
  transaction_type: string
  status: string
  credits: number
  egp_amount: number | null
  payment_method: string | null
  payment_ref: string | null
  description: string
  action_type: string | null
  balance_after: number
  created_at: string
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
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

function balanceColor(balance: number): string {
  if (balance >= 50)  return 'text-emerald'
  if (balance >= 20)  return 'text-amber'
  return 'text-rose'
}

// ─── Top-up Modal ─────────────────────────────────────────────────────────────
function TopUpModal({ onClose, onSuccess }: { onClose: () => void; onSuccess: () => void }) {
  const [packages, setPackages]     = useState<Package[]>([])
  const [selected, setSelected]     = useState<Package | null>(null)
  const [method, setMethod]         = useState<string>('')
  const [ref, setRef]               = useState('')
  const [loading, setLoading]       = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [done, setDone]             = useState(false)
  const [error, setError]           = useState('')
  const [showManual, setShowManual] = useState(false)
  const [payingVia, setPayingVia]   = useState<'card' | 'wallet' | null>(null)
  const [walletPhone, setWalletPhone] = useState('')

  useEffect(() => {
    api.getWalletPackages().then(pkgs => {
      setPackages(pkgs)
      setSelected(pkgs.find((p: Package) => p.is_popular) ?? pkgs[0])
      setLoading(false)
    })
  }, [])

  const handleSubmit = async () => {
    if (!selected || !method || !ref.trim()) {
      setError('Please select a package, payment method, and enter your reference number.')
      return
    }
    setSubmitting(true)
    setError('')
    try {
      await api.requestTopUp({ package_id: selected.id, payment_method: method, payment_ref: ref.trim() })
      setDone(true)
      setTimeout(() => { onSuccess(); onClose(); }, 2000)
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? 'Request failed. Please try again.')
    }
    setSubmitting(false)
  }

  const handlePayNow = async (via: 'card' | 'wallet') => {
    if (!selected) { setError('Please select a package first.'); return }
    if (via === 'wallet' && !walletPhone.trim()) {
      setError('Please enter the mobile number to charge.')
      return
    }
    setPayingVia(via)
    setError('')
    try {
      const { checkout_url } = await api.initWalletTopUp({
        package_id: selected.id,
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
                <Zap size={14} className="text-amber" />
              </div>
              <div>
                <h2 className="text-sm font-semibold text-bright">Buy Credits</h2>
                <p className="text-xs text-ghost">Pay in EGP via local payment methods</p>
              </div>
            </div>
            <button onClick={onClose} className="w-7 h-7 rounded flex items-center justify-center text-ghost hover:text-bright hover:bg-surface transition-colors">
              <X size={15} />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-5 space-y-5">
            {done ? (
              <div className="py-8 text-center">
                <CheckCircle size={36} className="text-emerald mx-auto mb-3" />
                <p className="text-bright font-semibold mb-1">Request Submitted!</p>
                <p className="text-xs text-ghost">Your credits will be added after payment confirmation.</p>
              </div>
            ) : loading ? (
              <div className="flex justify-center py-8"><Spinner className="w-5 h-5" /></div>
            ) : (
              <>
                {/* Packages */}
                <div>
                  <p className="text-xs text-ghost uppercase tracking-widest font-medium mb-2">Choose a package</p>
                  <div className="space-y-2">
                    {packages.map(pkg => {
                      const total = pkg.credits + pkg.bonus_credits
                      const isSelected = selected?.id === pkg.id
                      return (
                        <button
                          key={pkg.id}
                          onClick={() => setSelected(pkg)}
                          className={`w-full text-left p-3 rounded-lg border transition-all ${
                            isSelected
                              ? 'bg-amber/10 border-amber/40'
                              : 'bg-surface border-border hover:border-amber/20'
                          }`}
                        >
                          <div className="flex items-center justify-between mb-0.5">
                            <div className="flex items-center gap-2">
                              <span className="text-sm font-semibold text-bright">{pkg.name}</span>
                              {pkg.is_popular && (
                                <span className="text-xs px-1.5 py-0.5 rounded bg-amber/20 text-amber border border-amber/30 font-medium">Popular</span>
                              )}
                            </div>
                            <span className="text-sm font-mono font-bold text-amber">{pkg.egp_price.toFixed(0)} EGP</span>
                          </div>
                          <div className="flex items-center gap-3">
                            <span className="text-xs text-soft font-mono">{total} credits</span>
                            {pkg.bonus_credits > 0 && (
                              <span className="text-xs text-emerald">+{pkg.bonus_credits} bonus</span>
                            )}
                            <span className="text-xs text-ghost ml-auto">
                              ~{(pkg.egp_price / total * 100).toFixed(0)} pt/credit
                            </span>
                          </div>
                        </button>
                      )
                    })}
                  </div>
                </div>

                {error && (
                  <div className="flex items-start gap-2 px-3 py-2.5 rounded-lg bg-rose/10 border border-rose/20">
                    <AlertTriangle size={13} className="text-rose flex-shrink-0 mt-0.5" />
                    <p className="text-xs text-rose">{error}</p>
                  </div>
                )}

                {/* Pay now — real Paymob checkout, instant confirmation */}
                <div className="space-y-2">
                  <button
                    onClick={() => handlePayNow('card')}
                    disabled={!selected || !!payingVia}
                    className="w-full py-3 rounded-lg btn-amber text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  >
                    {payingVia === 'card' ? <Spinner className="w-4 h-4" /> : <>💳 Pay by Card</>}
                  </button>
                  <div className="flex gap-2">
                    <input
                      className="flex-1 bg-surface border border-border rounded-lg px-3 py-2.5 text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 font-mono"
                      placeholder="01XXXXXXXXX"
                      value={walletPhone}
                      onChange={e => setWalletPhone(e.target.value)}
                    />
                    <button
                      onClick={() => handlePayNow('wallet')}
                      disabled={!selected || !!payingVia}
                      className="px-4 py-2.5 rounded-lg border border-border text-xs font-medium text-soft hover:border-amber/30 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5"
                    >
                      {payingVia === 'wallet' ? <Spinner className="w-4 h-4" /> : <>📱 Pay by Wallet</>}
                    </button>
                  </div>
                  <p className="text-xs text-ghost text-center">
                    Secure checkout via Paymob · credits added automatically once paid
                  </p>
                </div>

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
                      <div className="grid grid-cols-3 gap-2">
                        {Object.entries(PAYMENT_LABELS).map(([key, label]) => (
                          <button
                            key={key}
                            onClick={() => setMethod(key)}
                            className={`py-2.5 rounded-lg border text-xs font-medium transition-all ${
                              method === key
                                ? 'bg-amber/10 border-amber/40 text-amber'
                                : 'bg-surface border-border text-ghost hover:text-soft hover:border-amber/20'
                            }`}
                          >
                            <div className="text-base mb-0.5">{PAYMENT_ICONS[key]}</div>
                            {label}
                          </button>
                        ))}
                      </div>
                    </div>

                    {method && selected && (
                      <div className="bg-surface border border-border rounded-lg p-3 text-xs text-ghost space-y-1">
                        <p className="text-bright font-medium mb-2">Payment instructions</p>
                        {method === 'fawry' && (
                          <>
                            <p>1. Open Fawry app or visit any Fawry outlet</p>
                            <p>2. Pay <span className="text-amber font-mono">{selected.egp_price} EGP</span> to service code <span className="text-amber font-mono">AI-CAREER</span></p>
                            <p>3. Enter the reference number you receive below</p>
                          </>
                        )}
                        {method === 'instapay' && (
                          <>
                            <p>1. Open your InstaPay app</p>
                            <p>2. Transfer <span className="text-amber font-mono">{selected.egp_price} EGP</span> to <span className="text-amber font-mono">payments@aicareer.eg</span></p>
                            <p>3. Use your phone number as the transfer note</p>
                            <p>4. Enter the transaction ID below</p>
                          </>
                        )}
                        {method === 'vodafone_cash' && (
                          <>
                            <p>1. Dial <span className="text-amber font-mono">*9*7*01XXXXXXXXX*{selected.egp_price.toFixed(0)}#</span></p>
                            <p>2. Or use the Vodafone Cash app to send to <span className="text-amber font-mono">01XXXXXXXXX</span></p>
                            <p>3. Enter the confirmation code you receive below</p>
                          </>
                        )}
                      </div>
                    )}

                    <div>
                      <label className="text-xs font-medium text-soft uppercase tracking-widest block mb-1.5">
                        Payment reference / transaction ID
                      </label>
                      <input
                        className="w-full bg-surface border border-border rounded-lg px-3 py-2.5 text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 font-mono"
                        placeholder="e.g. FWR-123456789"
                        value={ref}
                        onChange={e => setRef(e.target.value)}
                      />
                    </div>

                    <button
                      onClick={handleSubmit}
                      disabled={submitting || !selected || !method || !ref.trim()}
                      className="w-full py-3 rounded-lg btn-amber text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                      {submitting ? <Spinner className="w-4 h-4" /> : <><Zap size={14} /> Submit Top-Up Request</>}
                    </button>

                    <p className="text-xs text-ghost text-center">
                      Credits are added after manual verification (usually within 1 hour).
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

// ─── Transaction History Modal ────────────────────────────────────────────────
function TransactionModal({ onClose }: { onClose: () => void }) {
  const [txs, setTxs]       = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.getWalletTransactions().then(data => { setTxs(data); setLoading(false) })
  }, [])

  const typeIcon = (tx: Transaction) => {
    if (tx.transaction_type === 'topup' || tx.transaction_type === 'bonus') return <ArrowUpRight size={13} className="text-emerald" />
    if (tx.transaction_type === 'deduction') return <ArrowDownLeft size={13} className="text-rose" />
    return <Gift size={13} className="text-amber" />
  }

  return (
    <>
      <div className="fixed inset-0 bg-void/80 backdrop-blur-sm z-40" onClick={onClose} />
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="bg-ink border border-border rounded-xl shadow-2xl w-full max-w-md pointer-events-auto flex flex-col max-h-[80vh]">
          <div className="flex items-center justify-between px-5 py-4 border-b border-border flex-shrink-0">
            <h2 className="text-sm font-semibold text-bright">Transaction History</h2>
            <button onClick={onClose} className="w-7 h-7 rounded flex items-center justify-center text-ghost hover:text-bright hover:bg-surface transition-colors">
              <X size={15} />
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-4">
            {loading ? (
              <div className="flex justify-center py-8"><Spinner className="w-5 h-5" /></div>
            ) : txs.length === 0 ? (
              <p className="text-xs text-ghost text-center py-8">No transactions yet.</p>
            ) : (
              <div className="space-y-2">
                {txs.map(tx => (
                  <div key={tx.id} className="flex items-center gap-3 px-3 py-2.5 bg-surface border border-border rounded-lg">
                    <div className="w-7 h-7 rounded-md bg-void border border-border flex items-center justify-center flex-shrink-0">
                      {typeIcon(tx)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-medium text-bright truncate">{tx.description}</p>
                      <p className="text-xs text-ghost">{new Date(tx.created_at).toLocaleDateString('en-EG')}</p>
                    </div>
                    <div className="text-right flex-shrink-0">
                      <p className={`text-sm font-mono font-bold ${tx.credits > 0 ? 'text-emerald' : 'text-rose'}`}>
                        {tx.credits > 0 ? '+' : ''}{tx.credits}
                      </p>
                      <p className="text-xs text-ghost font-mono">{tx.balance_after} left</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

// ─── Wallet Widget (sidebar) ──────────────────────────────────────────────────
export function WalletWidget() {
  const [wallet, setWallet]       = useState<Wallet | null>(null)
  const [showTopUp, setShowTopUp] = useState(false)
  const [showHistory, setShowHistory] = useState(false)

  const loadWallet = useCallback(() => {
    api.getWallet().then(setWallet).catch(() => {})
  }, [])

  useEffect(() => { loadWallet() }, [loadWallet])

  if (!wallet) return null

  const low = wallet.credit_balance < 20

  return (
    <>
      {showTopUp    && <TopUpModal onClose={() => setShowTopUp(false)} onSuccess={loadWallet} />}
      {showHistory  && <TransactionModal onClose={() => setShowHistory(false)} />}

      <div className={`mx-3 mb-3 rounded-lg border p-3 ${low ? 'border-rose/30 bg-rose/5' : 'border-border bg-surface'}`}>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-1.5">
            <Zap size={12} className={low ? 'text-rose' : 'text-amber'} />
            <span className={`text-xs font-medium ${low ? 'text-rose' : 'text-amber'}`}>Credits</span>
          </div>
          <button
            onClick={() => setShowHistory(true)}
            className="text-xs text-ghost hover:text-soft transition-colors"
          >
            History
          </button>
        </div>

        <div className="flex items-center justify-between mb-2.5">
          <span className={`text-2xl font-mono font-bold ${balanceColor(wallet.credit_balance)}`}>
            {wallet.credit_balance}
          </span>
          {low && (
            <span className="flex items-center gap-1 text-xs text-rose">
              <AlertTriangle size={11} />
              Low balance
            </span>
          )}
        </div>

        <button
          onClick={() => setShowTopUp(true)}
          className="w-full flex items-center justify-center gap-1.5 py-1.5 rounded-lg btn-amber text-xs font-semibold"
        >
          <Plus size={12} />
          Buy Credits
        </button>
      </div>
    </>
  )
}