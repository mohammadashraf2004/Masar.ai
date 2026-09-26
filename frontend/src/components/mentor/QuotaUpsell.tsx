'use client'
import Link from 'next/link'
import { Sparkles } from 'lucide-react'
import { buttonStyles } from '@/components/ui/Button'
import { useI18n } from '@/lib/i18n'

/**
 * The inline upsell (handoff Task 12a, backend notes): shown where the learner is blocked, not
 * in a dialog, and linking to /billing.
 *
 * - `quota`: the Free plan's daily message limit ("See plans & offers").
 * - `credits`: the wallet cannot pay for the next message, or the next interview question (the
 *   backend's 402). "Top up", and what it costs is that context's: 2 a message, 3 a question.
 */
export function QuotaUpsell({
  kind,
  context = 'chat',
  limit,
  className,
}: {
  kind: 'quota' | 'credits'
  context?: 'chat' | 'interview'
  limit?: number
  className?: string
}) {
  const { t, tf } = useI18n()
  const title = kind === 'quota' ? t('mentor.upsell.quota.title') : t('mentor.upsell.credits.title')
  const body =
    kind === 'quota'
      ? tf('mentor.upsell.quota.body', { limit: limit ?? 0 })
      : t(context === 'interview' ? 'interview.upsell.credits.body' : 'mentor.upsell.credits.body')
  const cta = kind === 'quota' ? t('mentor.upsell.cta') : t('mentor.upsell.credits.cta')
  return (
    <div
      role="status"
      data-testid="mentor-upsell"
      className={`flex flex-wrap items-center gap-3 rounded-lg border border-amber/30 bg-amber-soft p-3.5 ${className ?? ''}`}
    >
      <Sparkles size={16} aria-hidden="true" className="shrink-0 text-amber-text" />
      <div className="min-w-0 flex-[1_1_200px]">
        <p className="text-sm font-semibold text-white">{title}</p>
        <p className="text-[13px] leading-relaxed text-dim">{body}</p>
      </div>
      <Link href="/billing" className={buttonStyles({ size: 'sm' })}>{cta}</Link>
    </div>
  )
}
