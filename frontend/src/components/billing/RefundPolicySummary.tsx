import Link from 'next/link'
import { ShieldCheck } from 'lucide-react'
import { useRefundI18n } from '@/lib/billing/refundI18n'

export function RefundPolicySummary({ compact = false }: { compact?: boolean }) {
  const { t } = useRefundI18n()
  return (
    <aside className="rounded-xl border border-border bg-panel/60 p-4" aria-labelledby="refund-policy-title">
      <div className="flex items-start gap-3">
        <ShieldCheck size={18} className="mt-0.5 shrink-0 text-amber-text" aria-hidden="true" />
        <div>
          <h2 id="refund-policy-title" className="text-sm font-semibold text-white">{t('policyTitle')}</h2>
          {!compact && <p className="mt-1 text-xs leading-relaxed text-dim">{t('policyShort')}</p>}
          <p className="mt-1 text-xs leading-relaxed text-dim">{t('cancellation')}</p>
          <Link href="/refund-policy" className="mt-2 inline-flex text-xs font-semibold text-amber-text hover:underline">
            {t('readPolicy')}
          </Link>
        </div>
      </div>
    </aside>
  )
}
