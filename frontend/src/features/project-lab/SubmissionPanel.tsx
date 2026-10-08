'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Award, CheckCircle2, ChevronDown, FileImage } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { cn } from '@/lib/utils'
import { useLabI18n } from './strings'
import type { LabSubmission } from './types'

/** Final submission: offered once every task has passed, then the summary of what was validated.
 *  Portfolio publishing and certificates are deliberately not part of this phase. */
export function SubmissionPanel({ submission, submitting, failed, onSubmit, summaryHref }: {
  submission: LabSubmission
  submitting: boolean
  failed: boolean
  onSubmit: () => void
  /** The project overview, which shows the full completion summary once submitted. */
  summaryHref?: string
}) {
  const { t, tf, pick, language } = useLabI18n()
  // Already submitted when the lab opened: a one-line summary that opens on demand, so the
  // milestones and instructions stay near the top. Submitting now opens it.
  const [expanded, setExpanded] = useState(!submission.submitted_at)
  if (!submission.ready) return null
  const submittedOn = submission.submitted_at
    ? new Intl.DateTimeFormat(language === 'ar' ? 'ar-EG' : 'en-GB', { day: 'numeric', month: 'long', year: 'numeric' })
      .format(new Date(submission.submitted_at))
    : null

  return (
    <section aria-labelledby="lab-submission-heading" data-testid="lab-submission"
      className="rounded-lg border border-emerald/30 bg-emerald/5 p-3">
      <h2 id="lab-submission-heading" className="flex items-center gap-2 text-sm font-semibold text-bright">
        <Award size={16} aria-hidden="true" className="shrink-0 text-emerald" />
        {submittedOn ? t('lab.submit.doneTitle') : t('lab.submit.title')}
      </h2>
      {submittedOn ? (
        <div className="mt-2 space-y-3 text-xs text-soft">
          <p>{tf('lab.submit.submittedOn', { date: submittedOn })} · {tf('lab.submit.overall', { percent: submission.percent })}</p>
          {summaryHref && (
            <Link href={summaryHref} className="inline-flex min-h-[36px] items-center text-xs font-medium text-emerald underline lg:min-h-0">
              {t('lab.submit.viewSummary')}
            </Link>
          )}
          <button type="button" aria-expanded={expanded} aria-controls="lab-submission-details"
            onClick={() => setExpanded(value => !value)}
            className="inline-flex min-h-[36px] items-center gap-1 rounded-md text-xs font-medium text-emerald hover:underline lg:min-h-0">
            {t(expanded ? 'lab.submit.hide' : 'lab.submit.show')}
            <ChevronDown size={13} aria-hidden="true" className={cn('transition-transform', expanded && 'rotate-180')} />
          </button>
          <div id="lab-submission-details" hidden={!expanded} className="space-y-3">
          <div>
            <p className="mb-1 font-semibold text-bright">{t('lab.submit.milestones')}</p>
            <ul className="space-y-0.5">
              {submission.milestones.map(milestone => (
                <li key={milestone.slug} className="flex items-center gap-1.5">
                  <CheckCircle2 size={12} aria-hidden="true" className="shrink-0 text-emerald" />
                  {pick(milestone.title, milestone.title_ar)}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p className="mb-1 font-semibold text-bright">{t('lab.submit.skills')}</p>
            <ul className="flex flex-wrap gap-1.5">
              {submission.skills.map(skill => (
                <li key={skill.en} className="rounded-full border border-border bg-surface px-2 py-0.5">{pick(skill.en, skill.ar)}</li>
              ))}
            </ul>
          </div>
          {submission.artifacts.length > 0 && (
            <div>
              <p className="mb-1 font-semibold text-bright">{t('lab.submit.artifacts')}</p>
              <ul className="space-y-0.5">
                {submission.artifacts.map(artifact => (
                  <li key={artifact.path} className="flex items-center gap-1.5 font-mono" dir="ltr">
                    <FileImage size={12} aria-hidden="true" className="shrink-0 text-ghost" />{artifact.path}
                  </li>
                ))}
              </ul>
            </div>
          )}
          </div>
        </div>
      ) : (
        <div className="mt-2 space-y-2">
          <p className="text-xs text-soft">{t('lab.submit.body')}</p>
          <Button size="sm" onClick={onSubmit} loading={submitting} disabled={submitting}>
            {submitting ? t('lab.submit.submitting') : t('lab.submit.button')}
          </Button>
          {failed && <p role="alert" className="text-xs text-rose">{t('lab.submit.failed')}</p>}
        </div>
      )}
    </section>
  )
}
