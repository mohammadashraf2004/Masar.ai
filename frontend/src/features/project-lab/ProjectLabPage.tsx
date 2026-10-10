'use client'

import { useCallback, useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import {
  ArrowLeft, ArrowRight, BriefcaseBusiness, CheckCircle2, Clock, Code2, Database, FileCheck2, Lightbulb,
  ListChecks, Play, ShieldCheck, Terminal,
} from 'lucide-react'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Badge, Card, ProgressBar, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { useAuthStore } from '@/lib/store'
import { useRequireAuth } from '@/components/auth/AuthPrompt'
import { CompletionSummary } from './CompletionSummary'
import { labProjectHref } from './LabProjectsSection'
import { ProjectLab } from './ProjectLab'
import { useLabI18n } from './strings'
import type { LabCompletion, LabProjectDetail } from './types'

export function labWorkspaceHref(slug: string) {
  return `${labProjectHref(slug)}/workspace`
}

function useProject(slug: string) {
  const [project, setProject] = useState<LabProjectDetail | null>(null)
  const [state, setState] = useState<'loading' | 'ready' | 'missing'>('loading')
  const load = useCallback(async () => {
    try {
      setProject(await api.getLabProject(slug))
      setState('ready')
    } catch {
      setState('missing')
    }
  }, [slug])
  useEffect(() => { void (async () => { await load() })() }, [load])
  return { project, state }
}

function BackLink({ href, label }: { href: string; label: string }) {
  const { dir } = useLabI18n()
  const Back = dir === 'rtl' ? ArrowRight : ArrowLeft
  return (
    <Link href={href} className="inline-flex min-h-[44px] items-center gap-1.5 text-xs text-ghost hover:text-soft lg:min-h-0">
      <Back size={13} aria-hidden="true" /> {label}
    </Link>
  )
}

function Fact({ icon: Icon, label, value }: { icon: typeof Clock; label: string; value: string }) {
  return (
    <div className="flex items-start gap-2.5">
      <Icon size={16} aria-hidden="true" className="mt-0.5 shrink-0 text-amber-text" />
      <div className="min-w-0">
        <dt className="ui-eyebrow">{label}</dt>
        <dd className="text-sm text-bright">{value}</dd>
      </div>
    </div>
  )
}

/** /challenges/projects/[slug]: the Project Overview — what the capstone is, what the learner will
 *  produce and how the lab works — before (and between) working sessions. Visiting it never creates
 *  an attempt; Start does. For a submitted project it shows the completion summary. */
export function ProjectLabPage({ slug }: { slug: string }) {
  const { t, tf, pick, n } = useLabI18n()
  const router = useRouter()
  const { project, state } = useProject(slug)
  // The overview is public; starting a project needs an account.
  const signedIn = useAuthStore((s) => !!s.token)
  const requireAuth = useRequireAuth()
  const { t: tApp } = useI18n()
  const [starting, setStarting] = useState(false)
  const [startError, setStartError] = useState(false)
  const [completion, setCompletion] = useState<LabCompletion | null>(null)
  const attempt = project?.attempt ?? null
  const submitted = !!attempt?.submitted_at

  useEffect(() => {
    if (!attempt || !submitted) return
    let cancelled = false
    void (async () => {
      try {
        const data = await api.getLabCompletion(attempt.id)
        if (!cancelled) setCompletion(data)
      } catch { /* the overview still shows; the summary stays hidden */ }
    })()
    return () => { cancelled = true }
  }, [attempt, submitted])

  const start = async () => {
    if (!requireAuth(labProjectHref(slug))) return
    setStarting(true)
    setStartError(false)
    try {
      await api.startLabProject(slug)
      router.push(labWorkspaceHref(slug))
    } catch {
      setStartError(true)
      setStarting(false)
    }
  }

  if (state === 'loading') {
    return <div className="flex flex-1 items-center justify-center p-8"><Spinner announce className="size-6" /></div>
  }
  if (state === 'missing' || !project) {
    return (
      <div className="space-y-4 p-6">
        <BackLink href="/challenges" label={t('lab.back')} />
        <p role="alert" className="text-sm text-rose">{t('lab.missing')}</p>
      </div>
    )
  }

  const overview = project.overview
  const hours = overview.duration_hours?.length === 2
    ? tf('lab.overview.hoursRange', { min: overview.duration_hours[0], max: overview.duration_hours[1] })
    : project.estimated_hours ? tf('lab.card.hours', { n: project.estimated_hours }) : null
  const action = !attempt ? (
    <Button onClick={start} loading={starting} className="w-full sm:w-auto">
      <Play size={14} aria-hidden="true" />{signedIn ? t('lab.overview.start') : tApp('gate.startProject')}
    </Button>
  ) : (
    <Link href={labWorkspaceHref(slug)} className={buttonStyles({ className: 'w-full sm:w-auto' })}>
      {submitted ? <FileCheck2 size={14} aria-hidden="true" /> : <Play size={14} aria-hidden="true" />}
      {t(submitted ? 'lab.overview.viewCompleted' : 'lab.overview.continue')}
    </Link>
  )
  const environment: { icon: typeof Code2; key: Parameters<typeof t>[0] }[] = [
    { icon: Code2, key: 'lab.overview.env.edit' }, { icon: Terminal, key: 'lab.overview.env.python' },
    { icon: Database, key: 'lab.overview.env.sql' }, { icon: ListChecks, key: 'lab.overview.env.output' },
    { icon: ShieldCheck, key: 'lab.overview.env.check' }, { icon: Lightbulb, key: 'lab.overview.env.hints' },
  ]

  return (
    <div className="mx-auto w-full max-w-6xl space-y-6 px-4 py-6 sm:px-6 lg:px-8" data-testid="lab-overview">
      <BackLink href="/challenges" label={t('lab.back')} />

      <header className="space-y-3">
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="sky">{pick(project.track.title, project.track.title_ar)}</Badge>
          <Badge variant="emerald">{t('lab.card.free')}</Badge>
        </div>
        <p className="text-xs font-semibold uppercase text-amber-text">{t('lab.overview.kicker')}</p>
        <h1 className="ui-page-title">
          {pick(project.title, project.title_ar)}
        </h1>
        <p className="max-w-3xl text-sm leading-relaxed text-soft">{pick(project.summary, project.summary_ar)}</p>
      </header>

      {submitted && completion ? (
        <CompletionSummary completion={completion} action={action} />
      ) : (
        <Card className="space-y-4 p-5">
          <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {overview.role && <Fact icon={BriefcaseBusiness} label={t('lab.overview.role')} value={pick(overview.role, overview.role_ar)} />}
            <Fact icon={ShieldCheck} label={t('lab.overview.difficulty')} value={t(`lab.overview.level.${project.difficulty}` as Parameters<typeof t>[0]) ?? project.difficulty} />
            {hours && <Fact icon={Clock} label={t('lab.overview.duration')} value={hours} />}
            <Fact icon={ListChecks} label={t('lab.overview.structure')}
              value={tf('lab.card.milestones', { n: project.milestone_count, tasks: project.task_count })} />
          </dl>
          {attempt && !submitted && (
            <div>
              <div className="mb-1.5 flex items-center justify-between text-xs">
                <span className="text-ghost">{t('lab.progress')}</span>
                <span className="text-soft">{tf('lab.progress.count', { done: attempt.completed_tasks, total: attempt.total_tasks })}</span>
              </div>
              <ProgressBar value={attempt.percent} />
              {attempt.completed_tasks === attempt.total_tasks && attempt.total_tasks > 0 && (
                <p className="mt-2 text-xs text-emerald">{t('lab.overview.readyToSubmit')}</p>
              )}
            </div>
          )}
          <div className="flex flex-wrap items-center gap-3">
            {action}
            {!attempt && <p className="text-xs text-ghost">{t('lab.start.body')}</p>}
          </div>
          {startError && <p role="alert" className="text-xs text-rose">{t('lab.card.error')}</p>}
        </Card>
      )}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1.15fr)_minmax(0,1fr)]">
        <div className="space-y-6">
          {overview.scenario && (
            <section aria-labelledby="lab-scenario">
              <h2 id="lab-scenario" className="ui-card-title mb-2">{t('lab.overview.scenario')}</h2>
              <p className="text-sm leading-relaxed text-soft">{pick(overview.scenario, overview.scenario_ar)}</p>
            </section>
          )}
          {overview.deliverables.length > 0 && (
            <section aria-labelledby="lab-deliverables">
              <h2 id="lab-deliverables" className="ui-card-title mb-2">{t('lab.overview.deliverables')}</h2>
              <ul className="space-y-2">
                {overview.deliverables.map(item => (
                  <li key={item.en} className="flex items-start gap-2 text-sm text-soft">
                    <CheckCircle2 size={15} aria-hidden="true" className="mt-0.5 shrink-0 text-emerald" />
                    <span>{pick(item.en, item.ar)}</span>
                  </li>
                ))}
              </ul>
            </section>
          )}
          {overview.skills.length > 0 && (
            <section aria-labelledby="lab-skills">
              <h2 id="lab-skills" className="ui-card-title mb-2">{t('lab.overview.skills')}</h2>
              <ul className="flex flex-wrap gap-2">
                {overview.skills.map(item => (
                  <li key={item.en} className="rounded-full border border-border bg-surface px-3 py-1 text-xs text-soft">{pick(item.en, item.ar)}</li>
                ))}
              </ul>
            </section>
          )}
          <section aria-labelledby="lab-environment">
            <h2 id="lab-environment" className="ui-card-title mb-1">{t('lab.overview.environment')}</h2>
            <p className="mb-3 text-sm text-ghost">{t('lab.overview.environmentBody')}</p>
            <ul className="grid grid-cols-1 gap-2 sm:grid-cols-2">
              {environment.map(({ icon: Icon, key }) => (
                <li key={key} className="flex items-center gap-2 text-sm text-soft">
                  <Icon size={15} aria-hidden="true" className="shrink-0 text-amber-text" />{t(key)}
                </li>
              ))}
            </ul>
          </section>
        </div>

        <section aria-labelledby="lab-structure">
          <h2 id="lab-structure" className="ui-card-title mb-3">{t('lab.overview.milestones')}</h2>
          <ol className="space-y-2">
            {project.milestones.map((milestone, index) => (
              <li key={milestone.slug} className="flex gap-3 rounded-lg border border-border bg-surface p-3">
                <span className="flex size-7 shrink-0 items-center justify-center rounded-full bg-amber/10 font-mono text-xs text-amber-text">
                  {n(index + 1)}
                </span>
                <div className="min-w-0">
                  <p className="text-sm font-semibold text-bright">{pick(milestone.title, milestone.title_ar)}</p>
                  {milestone.summary && <p className="mt-0.5 text-xs leading-relaxed text-ghost">{pick(milestone.summary, milestone.summary_ar)}</p>}
                  <p className="mt-1 text-xs text-ghost">{tf('lab.overview.tasks', { n: milestone.tasks.length })}</p>
                </div>
              </li>
            ))}
          </ol>
        </section>
      </div>
    </div>
  )
}

/** /challenges/projects/[slug]/workspace: the lab itself. Without an attempt it sends the learner
 *  to the overview, where starting is an explicit choice. */
export function ProjectWorkspacePage({ slug }: { slug: string }) {
  const { t } = useLabI18n()
  const router = useRouter()
  const { project, state } = useProject(slug)

  useEffect(() => {
    if (state === 'ready' && project && !project.attempt) router.replace(labProjectHref(slug))
  }, [state, project, router, slug])

  if (state === 'loading' || (state === 'ready' && !project?.attempt)) {
    return <div className="flex flex-1 items-center justify-center p-8"><Spinner announce className="size-6" /></div>
  }
  if (state === 'missing' || !project?.attempt) {
    return (
      <div className="space-y-4 p-6">
        <BackLink href="/challenges" label={t('lab.back')} />
        <p role="alert" className="text-sm text-rose">{t('lab.missing')}</p>
      </div>
    )
  }
  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <div className="shrink-0 border-b border-border px-4 py-1">
        <BackLink href={labProjectHref(slug)} label={t('lab.overview.back')} />
      </div>
      <ProjectLab attemptId={project.attempt.id} />
    </div>
  )
}
