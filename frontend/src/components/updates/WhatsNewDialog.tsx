'use client'
import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { HelpCircle, ListChecks, Route, Sparkles, type LucideIcon } from 'lucide-react'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Modal } from '@/components/ui/Modal'
import { useAcknowledgeUpdate } from '@/hooks/useAcknowledgeUpdate'
import { api } from '@/lib/api'
import { useI18n, type StringKey } from '@/lib/i18n'
import { WHATS_NEW } from '@/lib/releases'

/** Where the button goes: the roadmap if there is one, otherwise the place to build it. */
type Destination = 'roadmap' | 'build'

const FEATURES: Array<{ icon: LucideIcon; title: StringKey; body: StringKey }> = [
  { icon: ListChecks, title: 'update.gap.title', body: 'update.gap.body' },
  { icon: HelpCircle, title: 'why.toggle', body: 'update.why.body' },
  { icon: Route, title: 'update.roadmap.title', body: 'update.roadmap.body' },
]

/**
 * "New in Masar" - shown once to an account that existed before the skill-gap
 * release, to say what changed and where to find it.
 *
 * It describes the features and sends the learner to them; it does not draw a
 * skill gap of its own. A learner with no roadmap has nothing to explore yet, so
 * the same words lead to building one instead. Whether it is shown at all is the
 * server's answer (`user.pending_updates`).
 *
 * Every way out - the button, "Maybe later", the close button, Escape -
 * acknowledges it, so it is not asked twice.
 */
export function WhatsNewDialog() {
  const { t } = useI18n()
  const acknowledge = useAcknowledgeUpdate(WHATS_NEW)
  const cta = useRef<HTMLAnchorElement>(null)
  const [destination, setDestination] = useState<Destination | null>(null)

  useEffect(() => {
    let alive = true
    ;(async () => {
      let next: Destination = 'roadmap'
      try {
        const profile = await api.getMyLearningProfile()
        if (profile.needs_onboarding) next = 'build'
        else if (!(await api.getMyLearningPath())) next = 'build'
      } catch {
        // The roadmap page decides for itself what to do about a learner without one.
      }
      if (alive) setDestination(next)
    })()
    return () => {
      alive = false
    }
  }, [])

  // Nothing is drawn until it is known where the button leads: no flash of the wrong one.
  if (!destination) return null
  const build = destination === 'build'

  return (
    <Modal
      title={t('update.title')}
      description={build ? t('update.leadBuild') : t('update.lead')}
      icon={<Sparkles size={18} />}
      onClose={acknowledge}
      initialFocus={cta}
      footer={
        <>
          <Link
            ref={cta}
            href={build ? '/onboarding/learning-profile' : '/learn'}
            onClick={acknowledge}
            className={buttonStyles({ className: 'w-full sm:w-auto' })}
          >
            {build ? t('card.empty.cta') : t('update.cta')}
          </Link>
          <Button variant="ghost" onClick={acknowledge} className="w-full sm:w-auto">{t('update.later')}</Button>
        </>
      }
    >
      <ul className="space-y-4">
        {FEATURES.map(({ icon: Icon, title, body }) => (
          <li key={title} className="flex items-start gap-3">
            <Icon size={16} aria-hidden="true" className="mt-0.5 shrink-0 text-amber" />
            <div className="min-w-0">
              <h3 className="text-sm font-semibold text-bright">{t(title)}</h3>
              <p className="mt-0.5 text-sm leading-relaxed text-soft">{t(body)}</p>
            </div>
          </li>
        ))}
      </ul>
    </Modal>
  )
}
