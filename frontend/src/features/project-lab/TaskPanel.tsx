'use client'

import { useState, type ReactNode } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { CheckCircle2, ChevronDown, Circle, CircleDot, FileCode2 } from 'lucide-react'
import { ProgressBar } from '@/components/ui/index'
import { cn } from '@/lib/utils'
import { useLabI18n } from './strings'
import type { LabAttempt, LabTaskStatus } from './types'

function StatusIcon({ status }: { status: LabTaskStatus }) {
  const { t } = useLabI18n()
  const label = t(`lab.task.status.${status}` as const)
  if (status === 'completed') return <CheckCircle2 size={16} className="shrink-0 text-emerald" aria-label={label} role="img" />
  if (status === 'in_progress') return <CircleDot size={16} className="shrink-0 text-amber-text" aria-label={label} role="img" />
  return <Circle size={16} className="shrink-0 text-ghost" aria-label={label} role="img" />
}

/** Project title, progress, milestone/task navigation and the selected task's instructions.
 *
 *  Ten milestones of three tasks would push the instructions far down the panel, so milestones
 *  collapse: the one holding the selected task is open, the others show their progress and open
 *  on demand. */
export function TaskPanel({ attempt, selectedTask, onSelectTask, onOpenFile, footer }: {
  attempt: LabAttempt
  selectedTask: string | null
  onSelectTask: (slug: string) => void
  onOpenFile: (path: string) => void
  /** Shown under the progress bar (the final submission panel). */
  footer?: ReactNode
}) {
  const { t, tf, pick } = useLabI18n()
  const { progress } = attempt
  const status = new Map(progress.tasks.map(task => [task.slug, task.status]))
  const counts = new Map(progress.milestones.map(m => [m.slug, m]))
  const task = attempt.milestones.flatMap(m => m.tasks).find(item => item.slug === selectedTask)
  const selectedMilestone = attempt.milestones.find(m => m.tasks.some(item => item.slug === selectedTask))?.slug
  // Only what the learner toggled is stored; otherwise the selected task's milestone is open.
  const [toggled, setToggled] = useState<Record<string, boolean>>({})
  const isOpen = (slug: string) => toggled[slug] ?? slug === selectedMilestone
  const toggle = (slug: string) => setToggled(previous => ({ ...previous, [slug]: !isOpen(slug) }))

  return (
    <div className="flex min-h-0 flex-col gap-5 overflow-y-auto p-4">
      <div>
        <p className="text-xs text-ghost">{pick(attempt.project.track.title, attempt.project.track.title_ar)}</p>
        <h1 className="mt-1 font-display text-lg font-bold leading-snug text-bright">
          {pick(attempt.project.title, attempt.project.title_ar)}
        </h1>
        <div className="mt-3">
          <div className="mb-1.5 flex items-center justify-between text-xs">
            <span className="text-ghost">{t('lab.progress')}</span>
            <span className="text-soft" data-testid="lab-progress">
              {tf('lab.progress.count', { done: progress.completed_tasks, total: progress.total_tasks })}
            </span>
          </div>
          <ProgressBar value={progress.percent} />
        </div>
        {footer && <div className="mt-3">{footer}</div>}
      </div>

      <nav aria-label={t('lab.milestones')}>
        <ol className="space-y-1">
          {attempt.milestones.map((milestone, index) => {
            const count = counts.get(milestone.slug)
            const expanded = isOpen(milestone.slug)
            const done = count ? count.completed_tasks === count.total_tasks && count.total_tasks > 0 : false
            const panelId = `lab-milestone-${milestone.slug}`
            return (
              <li key={milestone.slug}>
                <button
                  type="button"
                  aria-expanded={expanded}
                  aria-controls={panelId}
                  onClick={() => toggle(milestone.slug)}
                  className="flex min-h-[40px] w-full items-center gap-2 rounded-md px-2 text-start text-xs font-semibold text-soft hover:bg-surface hover:text-bright lg:min-h-[34px]"
                >
                  <span className={cn('font-mono', done ? 'text-emerald' : 'text-ghost')}>{index + 1}.</span>
                  <span className="min-w-0 flex-1">{pick(milestone.title, milestone.title_ar)}</span>
                  {count && (
                    <span className={cn('shrink-0 font-mono text-[11px] font-normal', done ? 'text-emerald' : 'text-ghost')}>
                      {tf('lab.milestone.count', { done: count.completed_tasks, total: count.total_tasks })}
                    </span>
                  )}
                  <ChevronDown size={14} aria-hidden="true"
                    className={cn('shrink-0 text-ghost transition-transform', expanded && 'rotate-180')} />
                </button>
                <ul id={panelId} hidden={!expanded} className="mb-2 mt-0.5 space-y-0.5 ps-3">
                  {milestone.tasks.map(item => (
                    <li key={item.slug}>
                      <button
                        type="button"
                        onClick={() => onSelectTask(item.slug)}
                        aria-current={item.slug === selectedTask ? 'step' : undefined}
                        className={cn(
                          'flex min-h-[40px] w-full items-center gap-2 rounded-md px-2 text-start text-sm transition-colors lg:min-h-[34px]',
                          item.slug === selectedTask ? 'bg-amber/10 text-bright' : 'text-soft hover:bg-surface hover:text-bright',
                        )}
                      >
                        <StatusIcon status={status.get(item.slug) ?? 'not_started'} />
                        <span className="min-w-0 flex-1">{pick(item.title, item.title_ar)}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              </li>
            )
          })}
        </ol>
      </nav>

      {task && (
        <section aria-labelledby="lab-task-heading" className="border-t border-border pt-4">
          <p className="text-[11px] font-semibold uppercase text-ghost">{t('lab.task.instructions')}</p>
          <h2 id="lab-task-heading" className="mt-1 text-base font-semibold text-bright">{pick(task.title, task.title_ar)}</h2>
          <div className="lab-markdown mt-3 space-y-3 text-sm leading-relaxed text-soft [&_code]:rounded [&_code]:bg-surface [&_code]:px-1 [&_code]:font-mono [&_code]:text-[0.85em] [&_code]:text-bright [&_li]:ms-5 [&_ol]:list-decimal [&_strong]:text-bright [&_table]:w-full [&_table]:text-xs [&_td]:border [&_td]:border-border [&_td]:p-1.5 [&_th]:border [&_th]:border-border [&_th]:p-1.5 [&_th]:text-start [&_ul]:list-disc">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                // Wide tables and code scroll inside the panel instead of widening it.
                table: ({ children }) => <div className="overflow-x-auto"><table>{children}</table></div>,
                pre: ({ children }) => <pre dir="ltr" className="overflow-x-auto rounded-lg bg-surface p-3 text-xs">{children}</pre>,
                code: ({ children }) => <code dir="ltr" className="break-words">{children}</code>,
              }}
            >
              {pick(task.instructions, task.instructions_ar)}
            </ReactMarkdown>
          </div>
          {task.primary_file && (
            <button
              type="button"
              onClick={() => onOpenFile(task.primary_file as string)}
              className="mt-4 inline-flex min-h-[40px] items-center gap-2 rounded-md border border-border px-3 text-xs text-soft hover:border-amber/30 hover:text-bright lg:min-h-[32px]"
            >
              <FileCode2 size={13} aria-hidden="true" />
              <span>{tf('lab.task.openFile', { file: task.primary_file })}</span>
            </button>
          )}
        </section>
      )}
    </div>
  )
}
