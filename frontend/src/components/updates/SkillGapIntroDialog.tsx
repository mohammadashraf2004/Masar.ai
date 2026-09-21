'use client'
import { useRef } from 'react'
import Link from 'next/link'
import { Target } from 'lucide-react'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Modal } from '@/components/ui/Modal'
import { useAcknowledgeUpdate } from '@/hooks/useAcknowledgeUpdate'
import { useSkillGaps } from '@/hooks/useSkillGaps'
import { useI18n } from '@/lib/i18n'
import { FIRST_ROADMAP_INTRO } from '@/lib/releases'

/**
 * "Your skill gap is ready" - the new learner's first meeting with the feature,
 * once their roadmap exists.
 *
 * It is an introduction and nothing more: the two numbers are the ones the
 * backend reported for this learner (`GET /learning/my-skill-gaps`), and the
 * button leads to the roadmap, where the analysis itself lives. It shows only
 * when there is something real to introduce - a roadmap, and skills measured
 * against it - so a learner who has not built one is never shown an empty
 * "skill gap". A learner with nothing left to gain is told that instead of "0
 * skills to gain".
 */
export function SkillGapIntroDialog() {
  const { t, tf, skillsToGain } = useI18n()
  const acknowledge = useAcknowledgeUpdate(FIRST_ROADMAP_INTRO)
  const cta = useRef<HTMLAnchorElement>(null)
  const state = useSkillGaps()

  if (state.kind !== 'ready' || state.gaps.summary.required === 0) return null
  const { summary, partial, missing } = state.gaps
  const toGain = partial.length + missing.length
  const done = toGain === 0

  return (
    <Modal
      title={t('intro.title')}
      description={done ? t('intro.leadDone') : t('intro.lead')}
      icon={<Target size={18} />}
      onClose={acknowledge}
      initialFocus={cta}
      footer={
        <>
          <Link
            ref={cta}
            href="/learn"
            onClick={acknowledge}
            className={buttonStyles({ className: 'w-full sm:w-auto' })}
          >
            {done ? t('intro.ctaDone') : t('intro.cta')}
          </Link>
          <Button variant="ghost" onClick={acknowledge} className="w-full sm:w-auto">{t('update.later')}</Button>
        </>
      }
    >
      {!done && (
        <div className="rounded-md border border-border bg-surface/40 px-4 py-3">
          <p className="font-display text-xl font-bold text-white">{skillsToGain(toGain)}</p>
          <p className="mt-1 text-sm text-soft">{tf('gap.coverageOf', { known: summary.known, total: summary.required })}</p>
        </div>
      )}
    </Modal>
  )
}
