'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { CheckCircle2, FolderKanban, Play } from 'lucide-react'
import { Badge, Card, DifficultyBadge, ProgressBar } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import { useLabI18n } from './strings'
import type { LabProjectCard } from './types'

export function labProjectHref(slug: string) {
  return `/challenges/projects/${encodeURIComponent(slug)}`
}

function ProjectCardView({ project }: { project: LabProjectCard }) {
  const { t, tf, pick } = useLabI18n()
  const router = useRouter()
  const attempt = project.attempt
  const submitted = !!attempt?.submitted_at
  // New and finished projects open on the overview (starting is a choice made there); a project
  // in progress goes straight back to the workspace.
  const open = () => router.push(attempt && !submitted ? `${labProjectHref(project.slug)}/workspace` : labProjectHref(project.slug))
  const action = !attempt ? t('lab.card.view') : submitted ? t('lab.overview.viewCompleted') : t('lab.card.continue')
  return (
    <Card glow className="flex min-h-[280px] flex-col p-5 sm:p-6" data-testid="lab-project-card">
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <Badge variant="sky">{pick(project.track.title, project.track.title_ar)}</Badge>
        <DifficultyBadge level={project.difficulty} />
        <Badge variant="emerald">{t('lab.card.free')}</Badge>
      </div>
      <h3 className="mb-2 font-display text-lg font-bold leading-snug text-bright">{pick(project.title, project.title_ar)}</h3>
      <p className="mb-4 text-sm leading-relaxed text-ghost">{pick(project.summary, project.summary_ar)}</p>
      <p className="mb-4 text-xs text-soft">
        {tf('lab.card.milestones', { n: project.milestone_count, tasks: project.task_count })}
        {project.estimated_hours ? <> · {tf('lab.card.hours', { n: project.estimated_hours })}</> : null}
      </p>
      {attempt && (
        <div className="mb-4">
          <div className="mb-1 flex items-center justify-between text-xs">
            <span className="text-ghost">{tf('lab.card.progress', { done: attempt.completed_tasks, total: attempt.total_tasks })}</span>
            {attempt.status === 'completed' && (
              <span className="flex items-center gap-1 text-emerald"><CheckCircle2 size={12} aria-hidden="true" />{t('lab.card.completed')}</span>
            )}
          </div>
          <ProgressBar value={attempt.percent} />
        </div>
      )}
      <Button className="mt-auto w-full" size="sm" variant={attempt ? 'outline' : 'amber'} onClick={open}>
        <Play size={12} aria-hidden="true" /> {action}
      </Button>
    </Card>
  )
}

/** Challenges › Guided projects. Renders nothing when there are no projects (or the request
 *  fails), so the existing challenge list is never blocked by this section. */
export function LabProjectsSection() {
  const { t } = useLabI18n()
  const [projects, setProjects] = useState<LabProjectCard[]>([])

  useEffect(() => {
    let cancelled = false
    void (async () => {
      try {
        const data = await api.getLabProjects()
        if (!cancelled) setProjects(data)
      } catch { /* the section stays hidden */ }
    })()
    return () => { cancelled = true }
  }, [])

  if (projects.length === 0) return null
  return (
    <section aria-labelledby="lab-projects-heading" className="mb-10">
      <div className="mb-4 flex items-start gap-3">
        <FolderKanban size={18} aria-hidden="true" className="mt-0.5 shrink-0 text-amber-text" />
        <div>
          <h2 id="lab-projects-heading" className="font-display text-lg font-bold text-bright">{t('lab.section.title')}</h2>
          <p className="mt-1 text-sm text-ghost">{t('lab.section.subtitle')}</p>
        </div>
      </div>
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        {projects.map(project => <ProjectCardView key={project.slug} project={project} />)}
      </div>
    </section>
  )
}
