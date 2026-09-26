'use client'
import { useId, useState } from 'react'
import Link from 'next/link'
import { ChevronDown, Circle, CircleDot } from 'lucide-react'
import { Badge, Card, Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { useSkillGaps } from '@/hooks/useSkillGaps'
import { useI18n } from '@/lib/i18n'
import { fieldLabel, skillLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { SkillGapGroup, SkillGapItem } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'
import { SkillGapSummary } from './SkillGapSummary'

/** How many "working toward" skills the compact profile view lists before it links to the roadmap. */
const PROFILE_LIMIT = 8

function GapSkill({ item }: { item: SkillGapItem }) {
  const { t } = useI18n()
  const ctx = useLabelContext()
  const partial = item.status === 'partially_covered'
  const Icon = partial ? CircleDot : Circle
  // Status is what a badge is for: "in progress" and "needed now". The rest is
  // context, so it is plain secondary text rather than another pill.
  const notes = [
    item.is_goal_required && t('gap.goalRequired'),
    item.course_count === 0 && t('gap.noCourse'),
    item.covered_by_completed && t('gap.completedHint'),
  ].filter(Boolean) as string[]
  const hasMeta = partial || item.is_immediate || notes.length > 0
  return (
    <li data-status={item.status} className="flex items-start gap-2 py-2 text-sm">
      <Icon size={15} aria-hidden="true" className={cn('mt-[3px] shrink-0', partial ? 'text-amber-text' : 'text-dim')} />
      <div className="flex min-w-0 flex-1 flex-wrap items-center gap-x-2.5 gap-y-1">
        <span className="min-w-0 break-words text-bright"><LearningLabel parts={skillLabel(item, ctx)} /></span>
        {hasMeta && (
          <span className="flex flex-wrap items-center gap-x-2 gap-y-1">
            {partial && <Badge variant="amber">{t('gap.status.partially_covered')}</Badge>}
            {item.is_immediate && <Badge variant="sky">{t('gap.immediate')}</Badge>}
            {notes.length > 0 && (
              <span className="text-xs text-soft">
                {notes.map((n, i) => (
                  <span key={n}>{i > 0 && <span aria-hidden="true">{' · '}</span>}{n}</span>
                ))}
              </span>
            )}
          </span>
        )}
      </div>
    </li>
  )
}

function GroupHeading({ group }: { group: SkillGapGroup }) {
  const { t } = useI18n()
  const ctx = useLabelContext()
  if (group.kind === 'tools') return <>{t('skills.group.tools')}</>
  if (group.kind === 'general' || !group.field) return <>{t('skills.group.general')}</>
  return <LearningLabel parts={fieldLabel(group.field, ctx, true)} />
}

/**
 * The per-field list of everything still to gain. Closed to begin with: on the
 * roadmap the summary answers "how far am I", and the roadmap itself is the
 * page's subject — the full list is one tap away rather than a screen of rows
 * pushing the stages out of view.
 */
function GapGroups({ groups, count }: { groups: SkillGapGroup[]; count: number }) {
  const { t, tf } = useI18n()
  const [open, setOpen] = useState(false)
  const listId = useId()
  return (
    <div className="mt-4 border-t border-border pt-1">
      <button
        type="button"
        aria-expanded={open}
        aria-controls={listId}
        onClick={() => setOpen((o) => !o)}
        className="inline-flex min-h-[44px] items-center gap-1.5 rounded text-xs font-medium text-amber-text hover:text-amber-text2 lg:min-h-[36px]"
      >
        {open ? t('gap.hide') : t('gap.show')}
        <span className="font-normal text-soft">({count})</span>
        <ChevronDown size={12} aria-hidden="true" className={cn('transition-transform', open && 'rotate-180')} />
      </button>
      {open && (
        <div id={listId} className="mt-2 space-y-5">
          {groups.map((group) => (
            <section key={group.key} aria-labelledby={`gap-group-${group.key}`}>
              <h3 id={`gap-group-${group.key}`} className="flex flex-wrap items-baseline justify-between gap-x-3 gap-y-0.5 text-xs font-medium uppercase tracking-widest text-soft">
                <span><GroupHeading group={group} /></span>
                <span className="font-normal normal-case tracking-normal">
                  {tf('gap.groupProgress', { known: group.known_count, total: group.total })}
                </span>
              </h3>
              <ul className="mt-1 divide-y divide-border/60">
                {group.skills.map((item) => <GapSkill key={item.slug} item={item} />)}
              </ul>
            </section>
          ))}
        </div>
      )}
    </div>
  )
}

interface SkillGapsPanelProps {
  /** `roadmap` lists every gap under its field; `profile` is the compact view for My Skills. */
  variant?: 'roadmap' | 'profile'
  /** Change it to ask the backend again (a rebuilt roadmap, a saved skill list). */
  reloadKey?: string | number
  className?: string
}

/**
 * The learner's skill gaps: a coverage summary and what is still to gain.
 *
 * Everything shown — which skills are relevant, whether each is known, in
 * progress or missing, how they group, the coverage percentage — is what
 * `GET /learning/my-skill-gaps` returned. This component fetches and draws it;
 * it is read-only by design, because the source of truth is the skill list the
 * learner declares (edited in My Skills), not this analysis of it.
 */
export function SkillGapsPanel({ variant = 'roadmap', reloadKey = 0, className }: SkillGapsPanelProps) {
  const { t, tf } = useI18n()
  const state = useSkillGaps(reloadKey)

  if (state.kind === 'loading') {
    return (
      <Card className={className ?? 'p-5'}>
        <div role="status" aria-label={t('common.loading')} className="flex justify-center py-3"><Spinner className="h-5 w-5" /></div>
      </Card>
    )
  }
  if (state.kind === 'error') {
    return (
      <Card className={className ?? 'p-5'}>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <p role="alert" className="text-sm text-rose">{t('gap.loadError')}</p>
          <Button variant="ghost" size="sm" onClick={state.retry}>{t('common.retry')}</Button>
        </div>
      </Card>
    )
  }
  if (state.kind === 'unavailable') {
    return (
      <Card className={className ?? 'p-5'}>
        <p className="text-sm text-soft">{t('gap.unavailable')}</p>
      </Card>
    )
  }

  const { gaps } = state
  const { summary } = gaps
  const stillToGain = [...gaps.partial, ...gaps.missing]

  const summaryBlock = (
    <SkillGapSummary
      known={summary.known}
      partial={summary.partial}
      missing={summary.missing}
      total={summary.required}
      coveragePct={summary.coverage_pct}
      immediate={summary.immediate}
    />
  )

  if (variant === 'profile') {
    const shown = stillToGain.slice(0, PROFILE_LIMIT)
    return (
      <div className={className}>
        {summaryBlock}
        {shown.length > 0 && (
          <section aria-labelledby="gap-working-toward" className="mt-4">
            <h3 id="gap-working-toward" className="mb-1 text-xs font-medium uppercase tracking-widest text-soft">
              {t('gap.workingToward')}
            </h3>
            <ul className="divide-y divide-border/60">
              {shown.map((item) => <GapSkill key={item.slug} item={item} />)}
            </ul>
            {stillToGain.length > shown.length && (
              <p className="mt-1 text-xs text-soft">
                {tf('gap.more', { n: stillToGain.length - shown.length })}{' '}
                <Link href="/learn/masar" className="text-amber-text underline">{t('gap.seeAll')}</Link>
              </p>
            )}
          </section>
        )}
        <p className="mt-3 text-xs leading-relaxed text-soft">{t('gap.note')}</p>
      </div>
    )
  }

  return (
    <Card className={className ?? 'p-5 sm:p-6'}>
      <div className="mb-3 flex flex-wrap items-center justify-between gap-x-4">
        <h2 className="text-sm font-semibold text-bright">{t('gap.title')}</h2>
        <Link href="/profile/learning" className="-my-3 inline-flex min-h-[44px] items-center text-xs font-medium text-amber-text hover:text-amber-text2 lg:my-0 lg:min-h-0">
          {t('mys.edit')}
        </Link>
      </div>
      {summaryBlock}
      {stillToGain.length === 0 ? (
        <p role="status" className="mt-4 text-sm text-emerald">{t('gap.allKnown')}</p>
      ) : (
        <GapGroups groups={gaps.groups.filter((g) => g.skills.length > 0)} count={stillToGain.length} />
      )}
      <p className="mt-4 text-xs leading-relaxed text-soft">{t('gap.note')}</p>
    </Card>
  )
}
