'use client'

import type { ReactNode } from 'react'
import { Award, BarChart3, CheckCircle2, FileCode2, FileText, NotebookPen } from 'lucide-react'
import { Card } from '@/components/ui/index'
import { useLabI18n } from './strings'
import type { LabCompletion } from './types'

const ARTIFACT_ICON = { report: FileText, chart: BarChart3, analysis: FileCode2, sql: FileCode2, notes: NotebookPen }

/** The Project Completed summary: tasks, milestones, validated skill areas and the learner's own
 *  artifacts (listed by name — contents stay private). Built from the frozen completion data that
 *  a later portfolio or certificate feature will reuse. */
export function CompletionSummary({ completion, action }: { completion: LabCompletion; action?: ReactNode }) {
  const { t, tf, pick, language } = useLabI18n()
  const date = completion.submitted_at
    ? new Intl.DateTimeFormat(language === 'ar' ? 'ar-EG' : 'en-GB', { day: 'numeric', month: 'long', year: 'numeric' })
      .format(new Date(completion.submitted_at))
    : null

  return (
    <Card className="space-y-5 border-emerald/30 p-5" data-testid="lab-completion">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="flex items-start gap-3">
          <Award size={22} aria-hidden="true" className="mt-0.5 shrink-0 text-emerald" />
          <div>
            <p className="text-xs font-semibold uppercase text-emerald">{t('lab.completion.status')}</p>
            <h2 className="ui-section-title">{pick(completion.project.title, completion.project.title_ar)}</h2>
            <p className="mt-1 text-sm text-soft">
              {tf('lab.completion.tasks', { done: completion.completed_tasks, total: completion.total_tasks })}
              {date && <> · {tf('lab.submit.submittedOn', { date })}</>}
            </p>
            {completion.project.role && (
              <p className="mt-0.5 text-xs text-ghost">{tf('lab.completion.role', { role: pick(completion.project.role, completion.project.role_ar) })}</p>
            )}
          </div>
        </div>
        {action}
      </div>

      <div className="grid grid-cols-1 gap-5 md:grid-cols-3">
        <section aria-labelledby="lab-completion-skills">
          <h3 id="lab-completion-skills" className="ui-card-title mb-2">{t('lab.submit.skills')}</h3>
          <ul className="flex flex-wrap gap-1.5">
            {completion.skills.map(skill => (
              <li key={skill.en} className="rounded-full border border-emerald/30 bg-emerald/5 px-2.5 py-0.5 text-xs text-soft">{pick(skill.en, skill.ar)}</li>
            ))}
          </ul>
        </section>
        <section aria-labelledby="lab-completion-milestones">
          <h3 id="lab-completion-milestones" className="ui-card-title mb-2">{t('lab.submit.milestones')}</h3>
          <ul className="space-y-1">
            {completion.milestones.map(milestone => (
              <li key={milestone.slug} className="flex items-center gap-1.5 text-xs text-soft">
                <CheckCircle2 size={13} aria-hidden="true" className={milestone.completed ? 'shrink-0 text-emerald' : 'shrink-0 text-ghost'} />
                {pick(milestone.title, milestone.title_ar)}
              </li>
            ))}
          </ul>
        </section>
        <section aria-labelledby="lab-completion-artifacts">
          <h3 id="lab-completion-artifacts" className="ui-card-title mb-2">{t('lab.submit.artifacts')}</h3>
          <ul className="space-y-1">
            {completion.artifacts.map(artifact => {
              const Icon = ARTIFACT_ICON[artifact.kind] ?? FileText
              return (
                <li key={artifact.path} className="flex min-w-0 items-center gap-1.5 text-xs text-soft">
                  <Icon size={13} aria-hidden="true" className="shrink-0 text-ghost" />
                  <span className="truncate font-mono" dir="ltr">{artifact.path}</span>
                </li>
              )
            })}
          </ul>
        </section>
      </div>
    </Card>
  )
}
