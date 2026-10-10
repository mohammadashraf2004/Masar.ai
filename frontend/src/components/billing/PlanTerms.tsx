import { Info } from 'lucide-react'
import { useI18n, type StringKey } from '@/lib/i18n'

const TERMS: StringKey[] = [
  'billing.terms.trial',
  'billing.terms.renewal',
  'billing.terms.cancel',
  'billing.terms.refund',
  'billing.terms.payment',
]

/** What a Pro subscription commits the learner to: trial, manual renewal, cancellation,
 *  refunds and who processes the payment - stated before they pay. */
export function PlanTerms() {
  const { t } = useI18n()
  return (
    <aside aria-labelledby="plan-terms-title" className="rounded-xl border border-border bg-panel/60 p-4">
      <div className="flex items-start gap-3">
        <Info size={18} aria-hidden="true" className="mt-0.5 shrink-0 text-amber-text" />
        <div>
          <h2 id="plan-terms-title" className="text-sm font-semibold text-white">{t('billing.terms.title')}</h2>
          <ul className="mt-1 list-disc space-y-1 ps-4 text-xs leading-relaxed text-dim">
            {TERMS.map((key) => <li key={key}>{t(key)}</li>)}
          </ul>
        </div>
      </div>
    </aside>
  )
}
