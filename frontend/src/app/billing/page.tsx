'use client'
import { useEffect, useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useSession } from '@/hooks/useAuth'
import { useRequireAuth } from '@/components/auth/AuthPrompt'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { useCreditBalance } from '@/components/layout/WalletContext'
import { CheckoutCard, type OrderItem } from '@/components/billing/CheckoutCard'
import { OfferBanner, type PromoError } from '@/components/billing/OfferBanner'
import { PackTile } from '@/components/billing/PackTile'
import { PlanCard } from '@/components/billing/PlanCard'
import { RefundPolicySummary } from '@/components/billing/RefundPolicySummary'
import { AiAllowanceCard } from '@/components/billing/AiAllowanceCard'
import { PlanTerms } from '@/components/billing/PlanTerms'
import { Button } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { billingCatalog } from '@/lib/billing/catalog'
import { api } from '@/lib/api'
import { useMoney } from '@/lib/billing/money'
import { getPaymentProvider, type PaymentFailure } from '@/lib/billing/payments'
import { formatAmount, priceOrder, yearlySavingPercent } from '@/lib/billing/pricing'
import type { BillingCatalog, BillingCycle, CartItem, PaymentMethodId } from '@/lib/billing/types'
import { useI18n, type StringKey } from '@/lib/i18n'
import { cn } from '@/lib/utils'

type Promo = { code: string; percent: number }

/**
 * Plans and checkout (handoff README-new-pages, Task 11).
 *
 * The page is written against two seams and knows neither's implementation: the catalog
 * (`lib/billing/catalog`: plans, packs, the offer, promo codes) and a `PaymentProvider`
 * (`lib/billing/payments`). Today both are stand-ins, so the whole flow can be built and
 * checked without a gateway; see docs/backend-requests.md for what the real ones need.
 *
 * One item is ordered at a time: choosing a plan or a pack replaces what was chosen. Prices
 * are VAT-inclusive, so the order adds up to what is charged and no tax line is added.
 */
export default function BillingPage() {
  // Public: plans, prices and what they include are for anyone to compare.
  // Starting a trial or paying needs an account (the server refuses it anyway).
  const { isLoading: authLoading } = useSession()
  const requireAuth = useRequireAuth()
  const { t, tf } = useI18n()
  const router = useRouter()
  const provider = useMemo(() => getPaymentProvider(), [])

  const [catalog, setCatalog] = useState<BillingCatalog | null>(null)
  const [loadFailed, setLoadFailed] = useState(false)
  const [attempt, setAttempt] = useState(0)

  const [cycle, setCycle] = useState<BillingCycle>('yearly')
  const [cart, setCart] = useState<CartItem>({ type: 'plan', id: 'pro' })
  const [promo, setPromo] = useState<Promo | null>(null)
  const [promoError, setPromoError] = useState<PromoError | null>(null)
  const [checkingPromo, setCheckingPromo] = useState(false)
  // What the provider takes is the provider's to say (`listMethods`), so the page holds no list of its
  // own; the first one it names is the one preselected until the reader picks another.
  const [methods, setMethods] = useState<readonly PaymentMethodId[]>([])
  const [chosenMethod, setChosenMethod] = useState<PaymentMethodId | null>(null)
  const [cardReady, setCardReady] = useState(false)
  const [processing, setProcessing] = useState(false)
  const [failure, setFailure] = useState<PaymentFailure | null>(null)

  const { money } = useMoney(catalog?.currency ?? 'EGP')

  useEffect(() => {
    let alive = true
    ;(async () => {
      try {
        const listed = provider ? await provider.listMethods() : []
        if (alive) setMethods(listed)
      } catch {
        if (alive) setMethods([])
      }
    })()
    return () => {
      alive = false
    }
  }, [provider])

  useEffect(() => {
    if (authLoading) return
    let alive = true
    ;(async () => {
      try {
        const loaded = await billingCatalog.load()
        if (alive) setCatalog(loaded)
      } catch {
        if (alive) setLoadFailed(true)
      }
    })()
    return () => {
      alive = false
    }
  }, [authLoading, attempt])

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  const method = chosenMethod && methods.includes(chosenMethod) ? chosenMethod : (methods[0] ?? null)
  const totals = catalog ? priceOrder(cart, cycle, catalog, promo) : null
  const saving = catalog ? yearlySavingPercent(catalog.plans) : 0

  function retry() {
    setLoadFailed(false)
    setAttempt((n) => n + 1)
  }

  // Any change to what is being bought clears the last failure: it was about the old order.
  function choose(item: CartItem) {
    setCart(item)
    setFailure(null)
  }

  async function togglePromo() {
    if (!catalog?.offer) return
    if (promo) {
      setPromo(null)
      return
    }
    setCheckingPromo(true)
    setPromoError(null)
    try {
      const result = await billingCatalog.validatePromo(catalog.offer.code)
      if (result.valid) setPromo({ code: result.code, percent: result.percent })
      else setPromoError(result.reason)
    } catch {
      setPromoError('unavailable')
    }
    setCheckingPromo(false)
  }

  async function pay() {
    if (!requireAuth('/billing')) return
    const startsTrial = Boolean(catalog?.trialEligible && cart.type === 'plan' && cart.id === 'pro')
    if (!catalog || !totals || processing || (!startsTrial && (!provider || !method))) return
    setProcessing(true)
    setFailure(null)
    try {
      if (startsTrial) {
        await api.startSubscriptionTrial('pro', cycle)
        router.push('/billing/orders?trial=started')
        return
      }
      if (!provider || !method) return
      const result = await provider.pay({
        cart, cycle, method, amount: totals.total, currency: catalog.currency, promoCode: promo?.code ?? null,
      })
      if (result.status === 'paid') {
        // Stays "processing" while the next page loads, so the button cannot be pressed twice.
        router.push(`/billing/success?invoice=${encodeURIComponent(result.invoiceId)}`)
        return
      }
      if (result.status === 'redirect') {
        window.location.assign(result.url)
        return
      }
      setFailure(result.reason)
    } catch {
      setFailure('unavailable')
    }
    setProcessing(false)
  }

  function orderItem(): OrderItem | null {
    if (!catalog) return null
    if (cart.type === 'plan') {
      const plan = catalog.plans.find((p) => p.id === cart.id)
      if (!plan) return null
      return {
        name: tf('billing.item.plan', {
          name: t(`billing.plan.${plan.id}.name` as StringKey),
          cycle: cycle === 'yearly' ? t('billing.yearly') : t('billing.monthly'),
        }),
        meta: catalog.trialEligible && plan.id === 'pro'
          ? t('billing.trial.summary')
          : cycle === 'yearly' ? tf('billing.item.planYearly', { price: money(plan.yearly) }) : t('billing.item.planMonthly'),
      }
    }
    const pack = catalog.packs.find((p) => p.id === cart.id)
    if (!pack) return null
    return {
      name: tf('billing.item.pack', { credits: formatAmount(pack.credits) }),
      meta: pack.bonus > 0 ? tf('billing.item.packBonus', { n: pack.bonus }) : t('billing.item.packPlain'),
    }
  }
  const item = orderItem()

  return (
    <AppShell>
      <PageHeader
        title={t('billing.title')}
        subtitle={t('billing.subtitle')}
        contained
        action={
          <div className="flex flex-wrap items-center gap-2.5">
            <div role="group" aria-label={t('billing.cycle')} className="flex gap-1 rounded-[10px] border border-border bg-surface p-1">
              {(['monthly', 'yearly'] as const).map((value) => (
                <button
                  key={value}
                  type="button"
                  aria-pressed={cycle === value}
                  onClick={() => setCycle(value)}
                  className={cn(
                    'min-h-[44px] rounded-[7px] border px-3.5 py-2 text-[13px] transition-colors lg:min-h-0',
                    'focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring',
                    cycle === value ? 'border-border bg-panel font-semibold text-white' : 'border-transparent text-dim hover:text-bright',
                  )}
                >
                  {t(value === 'yearly' ? 'billing.yearly' : 'billing.monthly')}
                </button>
              ))}
            </div>
            {saving > 0 && (
              <span className="rounded-full border border-emerald px-2.5 py-0.5 text-xs font-semibold text-emerald">
                {tf('billing.save', { n: saving })}
              </span>
            )}
          </div>
        }
      />

      <PageBody className="space-y-5">
        {!catalog && !loadFailed && <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>}

        {loadFailed && (
          <Card className="p-8 text-center">
            <p role="alert" className="mb-4 text-sm text-rose">{t('billing.loadError')}</p>
            <Button variant="ghost" onClick={retry}>{t('common.retry')}</Button>
          </Card>
        )}

        {catalog && totals && item && (
          <>
            {catalog.offer && (
              <OfferBanner
                offer={catalog.offer}
                applied={promo !== null}
                checking={checkingPromo}
                error={promoError}
                onToggle={() => void togglePromo()}
              />
            )}

            {catalog.currentPlan === 'pro' && <AiAllowanceCard />}

            <div className="grid gap-4 [grid-template-columns:repeat(auto-fit,minmax(260px,1fr))]">
              {catalog.plans.map((plan) => (
                <PlanCard
                  key={plan.id}
                  plan={plan}
                  cycle={cycle}
                  currency={catalog.currency}
                  selected={cart.type === 'plan' && cart.id === plan.id}
                  current={plan.id === catalog.currentPlan}
                  onChoose={() => choose({ type: 'plan', id: plan.id })}
                />
              ))}
            </div>

            <div className="flex flex-wrap items-start gap-5">
              <CreditPacks catalog={catalog} cart={cart} onChoose={choose} />
              <div className="min-w-0 flex-[1_1_340px]">
                <CheckoutCard
                  item={item}
                  totals={totals}
                  currency={catalog.currency}
                  promo={promo}
                  methods={methods}
                  method={method}
                  onMethod={setChosenMethod}
                  provider={provider}
                  cardReady={cardReady}
                  onCardReady={setCardReady}
                  processing={processing}
                  failure={failure}
                  onPay={() => void pay()}
                  trial={Boolean(catalog.trialEligible && cart.type === 'plan' && cart.id === 'pro')}
                />
              </div>
            </div>
            <PlanTerms />
            <RefundPolicySummary />
          </>
        )}
      </PageBody>
    </AppShell>
  )
}

/** The credit packs, and the balance they add to. A child of the page so it sits inside the
 *  shell, where the wallet balance is provided. */
function CreditPacks({
  catalog, cart, onChoose,
}: {
  catalog: BillingCatalog
  cart: CartItem
  onChoose: (item: CartItem) => void
}) {
  const { t } = useI18n()
  const balance = useCreditBalance()
  return (
    <Card className="flex min-w-0 flex-[1.4_1_420px] flex-col gap-4 p-[22px]">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="flex flex-col gap-1">
          <h2 className="text-base font-bold text-white">{t('billing.packs.title')}</h2>
          <p className="text-[13px] leading-relaxed text-dim">{t('billing.packs.desc')}</p>
        </div>
        {balance !== null && (
          <span className="text-xs text-dim">
            {t('billing.packs.balance')} <span className="font-mono text-white">{formatAmount(balance)}</span>
          </span>
        )}
      </div>
      <div className="grid gap-3 [grid-template-columns:repeat(auto-fit,minmax(150px,1fr))]">
        {catalog.packs.map((pack) => (
          <PackTile
            key={pack.id}
            pack={pack}
            currency={catalog.currency}
            selected={cart.type === 'pack' && cart.id === pack.id}
            onChoose={() => onChoose({ type: 'pack', id: pack.id })}
          />
        ))}
      </div>
    </Card>
  )
}
