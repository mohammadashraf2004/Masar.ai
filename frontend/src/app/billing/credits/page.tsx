'use client'
import { Suspense, useCallback, useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { Check, Clock3, Sparkles, X } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { useWallet } from '@/components/layout/WalletContext'
import { Button } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api, type CreditPurchase, type CreditPurchaseStatus } from '@/lib/api'
import { billingCatalog } from '@/lib/billing/catalog'
import { useMoney } from '@/lib/billing/money'
import { getPaymentProvider } from '@/lib/billing/payments'
import { formatAmount } from '@/lib/billing/pricing'
import type { BillingCatalog, CreditPack } from '@/lib/billing/types'
import { useI18n, type StringKey } from '@/lib/i18n'
import { cn } from '@/lib/utils'

export default function BuyCreditsPage() {
  return (
    <Suspense fallback={null}>
      <BuyCreditsInner />
    </Suspense>
  )
}

/** How often, and for how long, a just-paid order is re-read while the provider's webhook is awaited. */
const POLL_MS = 3000
const POLL_LIMIT = 20

const STATUS_KEYS: Record<CreditPurchaseStatus, StringKey> = {
  pending: 'credits.status.pending',
  expired: 'credits.status.expired',
  failed: 'credits.status.failed',
  paid: 'credits.status.paid',
  partially_refunded: 'credits.status.partially_refunded',
  refunded: 'credits.status.refunded',
  chargeback: 'credits.status.chargeback',
}

/**
 * Buy Credits: the four packs, the balance (bought credits apart from included ones) and the
 * purchase history. Prices and credit amounts come from the server's catalogue; paying opens
 * the provider's hosted checkout and credits arrive only when the provider's confirmed webhook
 * says so - the page returned to afterwards (`?reference=`) merely asks the server what happened.
 */
function BuyCreditsInner() {
  const { isLoading: authLoading } = useAuth()
  const { t } = useI18n()
  const reference = useSearchParams().get('reference') ?? ''

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  return (
    <AppShell>
      <PageHeader title={t('credits.title')} subtitle={t('credits.subtitle')} contained />
      <CreditsContent reference={reference} />
    </AppShell>
  )
}

/** Below the shell, where the wallet is provided (a page cannot read the wallet outside AppShell). */
function CreditsContent({ reference }: { reference: string }) {
  const { t, tf, language } = useI18n()
  const { wallet, refresh } = useWallet()
  const provider = useMemo(() => getPaymentProvider(), [])

  const [catalog, setCatalog] = useState<BillingCatalog | null>(null)
  const [orders, setOrders] = useState<CreditPurchase[] | null>(null)
  const [loadFailed, setLoadFailed] = useState(false)
  const [selected, setSelected] = useState<string | null>(null)
  const [buying, setBuying] = useState(false)
  const [buyError, setBuyError] = useState<'unavailable' | 'busy' | null>(null)
  const [returned, setReturned] = useState<CreditPurchase | null>(null)
  const [checking, setChecking] = useState(Boolean(reference))
  const { money } = useMoney(catalog?.currency ?? 'EGP')

  const loadOrders = useCallback(async () => {
    try {
      setOrders(await api.getCreditPurchases())
    } catch {
      setOrders((prev) => prev ?? [])
    }
  }, [])

  useEffect(() => {
    let alive = true
    billingCatalog.load()
      .then((loaded) => {
        if (!alive) return
        setCatalog(loaded)
        const popular = loaded.packs.find((p) => p.popular) ?? loaded.packs[0]
        setSelected((prev) => prev ?? popular?.id ?? null)
      })
      .catch(() => { if (alive) setLoadFailed(true) })
    api.getCreditPurchases()
      .then((rows) => { if (alive) setOrders(rows) })
      .catch(() => { if (alive) setOrders((prev) => prev ?? []) })
    return () => { alive = false }
  }, [])

  // Coming back from the checkout: ask the server what happened to this order, until it settles.
  useEffect(() => {
    if (!reference) return
    let alive = true
    let tries = 0
    let timer: ReturnType<typeof setTimeout> | undefined
    const check = async () => {
      try {
        const status = await api.getPaymentStatus(reference)
        if (!alive) return
        if (status.order) setReturned(status.order)
        const settled = status.status !== 'pending'
        if (settled) {
          setChecking(false)
          await Promise.all([refresh(), loadOrders()])
          return
        }
      } catch {
        // fall through to try again
      }
      tries += 1
      if (!alive) return
      if (tries >= POLL_LIMIT) { setChecking(false); return }
      timer = setTimeout(check, POLL_MS)
    }
    void check()
    return () => { alive = false; if (timer) clearTimeout(timer) }
  }, [reference, refresh, loadOrders])

  async function buy() {
    if (!provider || !selected || buying) return
    setBuying(true)
    setBuyError(null)
    try {
      const result = await provider.pay({
        cart: { type: 'pack', id: selected }, cycle: 'monthly', method: 'card',
        amount: catalog?.packs.find((p) => p.id === selected)?.price ?? 0,
        currency: catalog?.currency ?? 'EGP', promoCode: null,
      })
      if (result.status === 'redirect') {
        window.location.assign(result.url)
        return
      }
      setBuyError('unavailable')
    } catch (err) {
      const status = (err as { response?: { status?: number } })?.response?.status
      setBuyError(status === 429 ? 'busy' : 'unavailable')
    }
    setBuying(false)
  }

  const balance = wallet?.credit_balance ?? null
  const purchased = wallet ? Math.min(wallet.purchased_credits ?? 0, wallet.credit_balance) : null
  const included = balance !== null && purchased !== null ? balance - purchased : null
  const chosen = catalog?.packs.find((p) => p.id === selected) ?? null
  const dateFmt = new Intl.DateTimeFormat(language === 'ar' ? 'ar-EG' : 'en-GB', { dateStyle: 'medium' })

  return (
      <PageBody className="space-y-5">
        {reference && <ReturnBanner order={returned} checking={checking} />}

        <Card className="grid gap-4 p-[22px] sm:grid-cols-3" data-testid="credits-balance">
          <div>
            <p className="text-xs text-dim">{t('credits.balance')}</p>
            <p className="mt-1 font-mono text-3xl font-semibold text-white">{balance === null ? '—' : formatAmount(balance)}</p>
          </div>
          <div>
            <p className="text-xs text-dim">{t('credits.purchased')}</p>
            <p className="mt-1 font-mono text-xl text-white">{purchased === null ? '—' : formatAmount(purchased)}</p>
            <p className="mt-1 text-xs leading-relaxed text-ghost">{t('credits.purchased.hint')}</p>
          </div>
          <div>
            <p className="text-xs text-dim">{t('credits.included')}</p>
            <p className="mt-1 font-mono text-xl text-white">{included === null ? '—' : formatAmount(included)}</p>
            <p className="mt-1 text-xs leading-relaxed text-ghost">{t('credits.included.hint')}</p>
          </div>
        </Card>

        <p className="flex items-start gap-2 text-[13px] leading-relaxed text-dim">
          <Sparkles size={14} aria-hidden="true" className="mt-0.5 shrink-0 text-amber-text" />
          {t('credits.explain')}
        </p>

        {!catalog && !loadFailed && <div className="flex justify-center py-12"><Spinner announce className="h-6 w-6" /></div>}
        {loadFailed && <p role="alert" className="text-sm text-rose">{t('billing.loadError')}</p>}

        {catalog && catalog.packs.length === 0 && (
          <p className="rounded-lg border border-dashed border-border px-4 py-6 text-center text-[13px] text-dim">
            {t('billing.packs.none')}
          </p>
        )}

        {catalog && catalog.packs.length > 0 && (
          <section aria-label={t('credits.packs')} className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
            {catalog.packs.map((pack) => (
              <PackCard
                key={pack.id} pack={pack} price={money(pack.price)}
                selected={pack.id === selected} onChoose={() => setSelected(pack.id)}
              />
            ))}
          </section>
        )}

        {catalog && chosen && (
          <Card className="flex flex-col gap-3 p-[22px] sm:flex-row sm:items-center sm:justify-between">
            <div className="min-w-0">
              <p className="text-sm font-semibold text-white">
                {tf('credits.summary', { credits: formatAmount(chosen.credits), price: money(chosen.price) })}
              </p>
              <p className="mt-1 text-xs text-dim">{t('credits.vat')}</p>
              {!provider && <p className="mt-2 text-xs text-amber-text">{t('billing.closed')}</p>}
              {provider?.isMock && <p className="mt-2 text-xs text-amber-text">{t('billing.mock')}</p>}
              {buyError && (
                <p role="alert" className="mt-2 text-xs text-rose">
                  {t(buyError === 'busy' ? 'credits.error.busy' : 'credits.error.unavailable')}
                </p>
              )}
            </div>
            <Button
              size="lg" className="w-full shrink-0 sm:w-auto" loading={buying}
              disabled={!provider || provider.isMock} onClick={() => void buy()}
            >
              {t('credits.buy')}
            </Button>
          </Card>
        )}

        <section aria-labelledby="credits-history" className="space-y-3">
          <h2 id="credits-history" className="text-base font-bold text-white">{t('credits.history')}</h2>
          {orders === null ? (
            <div className="flex justify-center py-6"><Spinner announce className="h-5 w-5" /></div>
          ) : orders.length === 0 ? (
            <p className="text-[13px] text-dim">{t('credits.history.empty')}</p>
          ) : (
            <ul data-testid="credits-history-list" className="divide-y divide-border overflow-hidden rounded-xl border border-border bg-surface">
              {orders.map((order) => (
                <li key={order.reference} className="flex flex-wrap items-center justify-between gap-x-4 gap-y-1 px-4 py-3">
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-white">
                      {order.package ?? t('credits.pack')} · {tf('credits.n', { n: formatAmount(order.credits) })}
                    </p>
                    <p className="text-xs text-dim">
                      {order.created_at ? dateFmt.format(new Date(order.created_at)) : ''}
                      {order.price !== null ? ` · ${money(order.price)}` : ''}
                      {order.credits_reversed > 0 ? ` · ${tf('credits.reversed', { n: formatAmount(order.credits_reversed) })}` : ''}
                    </p>
                  </div>
                  <StatusBadge status={order.status} label={t(STATUS_KEYS[order.status])} />
                </li>
              ))}
            </ul>
          )}
        </section>

        <p className="text-xs text-dim">
          <Link href="/billing" className="text-amber-text underline underline-offset-2">{t('credits.back')}</Link>
        </p>
      </PageBody>
  )
}

function PackCard({
  pack, price, selected, onChoose,
}: { pack: CreditPack; price: string; selected: boolean; onChoose: () => void }) {
  const { t, tf } = useI18n()
  return (
    <button
      type="button"
      onClick={onChoose}
      aria-pressed={selected}
      className={cn(
        'relative flex min-h-[44px] flex-col gap-1 rounded-xl border p-5 text-start transition-colors',
        'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring',
        selected ? 'border-amber bg-amber-soft' : 'border-border bg-surface hover:border-muted',
        pack.popular && !selected && 'border-amber/40',
      )}
    >
      <span className="flex min-h-[22px] items-center justify-between gap-2">
        <span className="text-sm font-semibold text-white">{pack.name ?? t('credits.pack')}</span>
        {pack.popular && (
          <span className="rounded-full bg-amber px-2.5 py-0.5 text-[11px] font-semibold text-on-amber">{t('billing.popular')}</span>
        )}
      </span>
      <span className="mt-2 font-mono text-3xl font-medium text-white">{formatAmount(pack.credits)}</span>
      <span className="text-xs text-dim">{t('billing.packs.credits')}</span>
      <span className="mt-3 border-t border-border pt-3 text-base font-semibold text-amber-text">{price}</span>
      <span className="text-xs text-ghost">{tf('credits.perCredit', { n: (pack.price / pack.credits).toFixed(2) })}</span>
    </button>
  )
}

function StatusBadge({ status, label }: { status: CreditPurchaseStatus; label: string }) {
  const tone =
    status === 'paid' ? 'border-emerald text-emerald'
    : status === 'pending' ? 'border-amber/40 text-amber-text'
    : status === 'failed' || status === 'chargeback' ? 'border-rose/40 text-rose'
    : 'border-border text-dim'
  return <span className={cn('rounded-full border px-2.5 py-0.5 text-xs font-semibold', tone)}>{label}</span>
}

/** What happened to the order the shopper just came back from. Only the server's record decides. */
function ReturnBanner({ order, checking }: { order: CreditPurchase | null; checking: boolean }) {
  const { t, tf } = useI18n()
  const status = order?.status
  if (status === 'paid' || status === 'partially_refunded') {
    return (
      <Banner tone="ok" icon={<Check size={16} aria-hidden="true" />}>
        {tf('credits.return.paid', { credits: formatAmount(order?.credits ?? 0) })}
      </Banner>
    )
  }
  if (status === 'failed' || status === 'expired' || status === 'refunded' || status === 'chargeback') {
    return <Banner tone="bad" icon={<X size={16} aria-hidden="true" />}>{t('credits.return.failed')}</Banner>
  }
  if (checking || status === 'pending') {
    return <Banner tone="wait" icon={<Clock3 size={16} aria-hidden="true" />}>{t('credits.return.pending')}</Banner>
  }
  return <Banner tone="wait" icon={<Clock3 size={16} aria-hidden="true" />}>{t('credits.return.unknown')}</Banner>
}

function Banner({ tone, icon, children }: { tone: 'ok' | 'bad' | 'wait'; icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <div
      role={tone === 'bad' ? 'alert' : 'status'}
      className={cn(
        'flex items-start gap-2.5 rounded-xl border px-4 py-3 text-sm',
        tone === 'ok' && 'border-emerald/40 bg-emerald/10 text-emerald',
        tone === 'bad' && 'border-rose/30 bg-rose/10 text-rose',
        tone === 'wait' && 'border-amber/30 bg-amber/10 text-amber-text',
      )}
    >
      <span className="mt-0.5 shrink-0">{icon}</span>
      <span>{children}</span>
    </div>
  )
}
