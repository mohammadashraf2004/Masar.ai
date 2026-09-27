'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowRight, Compass } from 'lucide-react'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { courseHref, fieldLabel, roleLabel, labelText, titleLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { LearningPath, LearningProfile } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'

type View =
  | { kind: 'loading' }
  | { kind: 'error' }
  | { kind: 'empty'; profile: LearningProfile }
  | { kind: 'path'; path: LearningPath }

interface YourMasarCardProps {
  /** `dashboard` names both the current and the next course and offers the
   *  lessons; `home` is the compact version. */
  variant?: 'dashboard' | 'home'
  className?: string
}

/**
 * The learner's roadmap, in one card — the dashboard's headline and the home
 * screen's compact summary.
 *
 * Everything it shows is the server's: the percentage, the current and next
 * course, whether the roadmap is finished. It only decides which of four states
 * to draw:
 *   - loading  — a placeholder, so the page does not jump when it lands;
 *   - error    — said plainly, with a retry (a broken card is worse than none);
 *   - empty    — no roadmap yet (a new account, or one that predates the
 *                redesign): an invitation, never a redirect;
 *   - a roadmap.
 */
export function YourMasarCard({ variant = 'dashboard', className }: YourMasarCardProps) {
  const { t, tf, language, mode } = useI18n()
  const ctx = useLabelContext()
  const [view, setView] = useState<View>({ kind: 'loading' })
  // Bumped by "try again" to re-run the load below.
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    let alive = true
    ;(async () => {
      try {
        const profile = await api.getMyLearningProfile()
        if (!alive) return
        if (profile.needs_onboarding) {
          setView({ kind: 'empty', profile })
          return
        }
        const path = await api.getMyLearningPath()
        if (alive) setView(path ? { kind: 'path', path } : { kind: 'empty', profile })
      } catch {
        if (alive) setView({ kind: 'error' })
      }
    })()
    return () => {
      alive = false
    }
  }, [attempt])

  function retry() {
    setView({ kind: 'loading' })
    setAttempt((n) => n + 1)
  }

  if (view.kind === 'loading') {
    return (
      <Card className={cn('p-5', className)}>
        <div role="status" aria-label={t('common.loading')} className="animate-pulse space-y-3">
          <div className="h-3 w-24 rounded bg-muted/60" />
          <div className="h-5 w-56 rounded bg-muted/60" />
          <div className="h-2 w-full rounded bg-muted/40" />
        </div>
      </Card>
    )
  }

  if (view.kind === 'error') {
    return (
      <Card className={cn('p-5', className)}>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <p role="alert" className="text-sm text-rose">{t('card.loadError')}</p>
          <Button variant="ghost" size="sm" onClick={retry}>{t('common.retry')}</Button>
        </div>
      </Card>
    )
  }

  if (view.kind === 'empty') {
    const { profile } = view
    const carried =
      profile.source === 'migrated' && profile.career_goal
        ? labelText(roleLabel(profile.career_goal, { language, mode }))
        : null
    return (
      // A roadmap that has not started is still where the path begins: the walkthrough's first stop.
      <Card data-tour="path" className={cn('border-amber/30 bg-gradient-to-br from-amber/5 to-transparent p-5', className)}>
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="min-w-0 max-w-xl">
            <h2 className="flex items-center gap-2 text-sm font-semibold text-bright">
              <Compass size={15} className="text-amber-text" aria-hidden="true" />
              {t('card.empty.title')}
            </h2>
            <p className="mt-1 text-xs leading-relaxed text-soft">{t('card.empty.body')}</p>
            {carried && <p className="mt-1 text-xs text-soft">{tf('banner.onboard.carried', { goal: carried })}</p>}
          </div>
          <Link href={profile.needs_onboarding ? '/onboarding/learning-profile' : '/learn/masar'} className={buttonStyles({ size: 'sm' })}>
            {t('card.empty.cta')} <ArrowRight size={12} className="rtl:rotate-180" aria-hidden="true" />
          </Link>
        </div>
      </Card>
    )
  }

  const { path } = view
  const pct = Math.round(path.progress?.path_pct ?? 0)
  const { current_course: current, next_course: next } = path
  const home = variant === 'home'
  // How much the current course would add: the server's count, worded here.
  const gain = current?.why?.to_gain_count
  const gainText =
    gain === undefined ? null
    : gain === 0 ? t('card.nothingToGain')
    : gain === 1 ? t('card.skillToGain')
    : tf('card.skillsToGain', { n: gain })

  return (
    <Card glow data-tour="path" className={cn('p-5 sm:p-6', className)}>
      <p className="text-xs font-medium uppercase tracking-widest text-soft">
        {home ? t('card.masar') : t('card.roadmap')}
      </p>
      <h2 className="mt-1 font-display text-lg font-bold leading-snug text-white sm:text-xl">
        <LearningLabel parts={roleLabel(path.career_goal, ctx)} />
      </h2>
      {path.effective_fields.length > 0 && (
        <p className="mt-1 flex flex-wrap items-center gap-x-2 gap-y-1 text-sm text-soft">
          {path.effective_fields.map((f, i) => (
            <span key={f.slug} className="inline-flex items-center gap-2">
              {i > 0 && <span aria-hidden="true">·</span>}
              <LearningLabel parts={fieldLabel(f, ctx, true)} />
            </span>
          ))}
        </p>
      )}

      <div className="mt-5 flex items-center gap-3">
        <div
          role="progressbar"
          aria-label={t('card.progress')}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={pct}
          className="progress-track h-2 w-full flex-1"
        >
          <div className="progress-fill bg-gradient-to-r from-amber to-amber2" style={{ width: `${pct}%` }} />
        </div>
        <span className="font-mono text-xs text-amber-text" dir="ltr">{pct}%</span>
      </div>

      {current ? (
        <dl className="mt-5 space-y-1.5 text-sm">
          <div className="flex flex-wrap gap-x-2">
            <dt className="text-soft">{home ? t('card.learningNow') : `${t('card.current')}:`}</dt>
            <dd className="font-medium text-bright"><LearningLabel parts={titleLabel(current.course, ctx)} /></dd>
          </div>
          {next && (
            <div className="flex flex-wrap gap-x-2">
              <dt className="text-soft">{t('card.next')}:</dt>
              <dd className="text-bright"><LearningLabel parts={titleLabel(next.course, ctx)} /></dd>
            </div>
          )}
        </dl>
      ) : (
        path.is_complete && <p role="status" className="mt-5 text-sm text-emerald">{t('card.done')}</p>
      )}
      {current && gainText && <p className="mt-2 text-sm text-soft">{gainText}</p>}

      <div className="mt-5 flex flex-wrap gap-2">
        {home ? (
          <Link href="/learn/masar" className={buttonStyles({ size: 'sm' })}>
            {t('card.continueRoadmap')} <ArrowRight size={12} className="rtl:rotate-180" aria-hidden="true" />
          </Link>
        ) : (
          <>
            {current && (
              <Link href={courseHref(current)} className={buttonStyles({ size: 'sm' })}>
                {t('card.continue')} <ArrowRight size={12} className="rtl:rotate-180" aria-hidden="true" />
              </Link>
            )}
            <Link href="/learn/masar" className={buttonStyles({ size: 'sm', variant: current ? 'ghost' : 'amber' })}>
              {t('card.viewRoadmap')}
            </Link>
          </>
        )}
      </div>
    </Card>
  )
}
