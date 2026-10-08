'use client'

import { useEffect, useState } from 'react'
import { AlertTriangle, CheckCircle2, Circle, Clock, Scissors, ServerCrash, XCircle } from 'lucide-react'
import { Spinner } from '@/components/ui/index'
import { cn } from '@/lib/utils'
import { CsvTable } from './FileEditor'
import { useLabI18n, type LabStringKey } from './strings'
import type { LabArtifact, LabCheckResult, LabHint, LabRunResult } from './types'
import type { LabRequestError } from './useProjectLab'

export type LabPanelTab = 'output' | 'checks' | 'artifacts' | 'hints'
const TABS: LabPanelTab[] = ['output', 'checks', 'artifacts', 'hints']

function Pre({ children, tone = 'default' }: { children: string; tone?: 'default' | 'error' }) {
  return (
    <pre
      dir="ltr"
      className={cn(
        'max-h-72 overflow-auto whitespace-pre-wrap break-words rounded-lg border p-3 font-mono text-xs leading-5',
        tone === 'error' ? 'border-rose/30 bg-rose/5 text-rose' : 'border-border bg-void text-soft',
      )}
    >
      {children}
    </pre>
  )
}

function Notice({ children }: { children: string }) {
  return (
    <p role="note" className="flex items-start gap-2 rounded-md border border-amber/25 bg-amber/5 px-3 py-2 text-xs text-amber-text">
      <Scissors size={13} aria-hidden="true" className="mt-0.5 shrink-0" />
      <span>{children}</span>
    </p>
  )
}

function RequestFailed({ error }: { error: LabRequestError }) {
  const { t } = useLabI18n()
  return <p role="alert" className="text-sm text-rose">{t(error === 'busy' ? 'lab.request.busy' : 'lab.run.failed')}</p>
}

function RunView({ run, running, failed }: { run: LabRunResult | null; running: boolean; failed: LabRequestError }) {
  const { t, tf } = useLabI18n()
  if (running) return <p role="status" className="flex items-center gap-2 text-sm text-soft"><Spinner className="size-4" />{t('lab.action.running')}</p>
  if (failed) return <RequestFailed error={failed} />
  if (!run) return <p className="text-sm text-ghost">{t('lab.output.empty')}</p>
  const tone = {
    success: { icon: CheckCircle2, cls: 'text-emerald' },
    error: { icon: XCircle, cls: 'text-rose' },
    timeout: { icon: Clock, cls: 'text-amber-text' },
    infrastructure_error: { icon: ServerCrash, cls: 'text-amber-text' },
  }[run.status]
  const Icon = tone.icon
  return (
    <div className="space-y-3" data-testid="lab-run" data-status={run.status}>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className={cn('flex items-center gap-2 text-sm font-medium', tone.cls)} role="status">
          <Icon size={15} aria-hidden="true" />{t(`lab.run.${run.status}` as const)}
        </p>
        <span className="font-mono text-xs text-ghost" dir="ltr">
          <span dir="ltr">{run.path}</span> · {tf('lab.output.ms', { ms: String(run.execution_ms) })}
        </span>
      </div>
      {run.table && (
        <div className="flex max-h-80 flex-col overflow-hidden rounded-lg border border-border">
          <CsvTable path={run.path} table={run.table} />
        </div>
      )}
      {run.table?.truncated && <Notice>{t('lab.output.rowsTruncated')}</Notice>}
      {(run.stdout || (!run.stderr && run.status === 'success' && !run.table)) && (
        <div>
          <p className="mb-1 text-xs text-ghost">{t('lab.output.stdout')}</p>
          <Pre>{run.stdout || t('lab.output.noOutput')}</Pre>
        </div>
      )}
      {run.stdout_truncated && <Notice>{t('lab.output.stdoutTruncated')}</Notice>}
      {run.stderr && (
        <div>
          <p className="mb-1 text-xs text-ghost">{t('lab.output.stderr')}</p>
          <Pre tone={run.status === 'error' ? 'error' : 'default'}>{run.stderr}</Pre>
        </div>
      )}
      {run.stderr_truncated && <Notice>{t('lab.output.stderrTruncated')}</Notice>}
      {run.artifacts_truncated && <Notice>{t('lab.artifacts.truncated')}</Notice>}
    </div>
  )
}

function ChecksView({ check, checking, failed, taskTitle }: {
  check: LabCheckResult | null; checking: boolean; failed: LabRequestError; taskTitle: (slug: string) => string
}) {
  const { t, tf, language } = useLabI18n()
  if (checking) return <p role="status" className="flex items-center gap-2 text-sm text-soft"><Spinner className="size-4" />{t('lab.action.checking')}</p>
  if (failed) return <RequestFailed error={failed} />
  if (!check) return <p className="text-sm text-ghost">{t('lab.checks.empty')}</p>

  const passedCount = check.checks.filter(c => c.passed).length
  // A check waiting on the ones above has not failed; it is not counted yet.
  const evaluated = check.checks.filter(c => !c.pending).length
  let banner: { cls: string; text: string; icon: typeof CheckCircle2 }
  if (check.outcome === 'pass') {
    banner = { cls: 'border-emerald/30 bg-emerald/10 text-emerald', icon: CheckCircle2,
      text: t(check.newly_completed ? 'lab.checks.pass' : 'lab.checks.passAgain') }
  } else if (check.outcome === 'fail') {
    banner = { cls: 'border-amber/30 bg-amber/10 text-amber-text', icon: AlertTriangle,
      text: tf('lab.checks.fail', { passed: passedCount, total: evaluated }) }
  } else {
    banner = { cls: 'border-rose/30 bg-rose/10 text-rose', icon: check.error?.kind === 'infrastructure' ? ServerCrash : XCircle,
      text: t(check.error?.kind === 'infrastructure' ? 'lab.checks.error.infrastructure' : 'lab.checks.error.execution') }
  }
  const Icon = banner.icon
  const localized = (value: string | null, values: Record<string, string> | null) => values?.[language] ?? value

  return (
    <div className="space-y-3" data-testid="lab-check" data-outcome={check.outcome}>
      <p className="text-xs text-ghost">{tf('lab.checks.task', { task: taskTitle(check.task) })}</p>
      <div role="status" className={cn('flex items-start gap-2 rounded-lg border px-3 py-2.5 text-sm font-medium', banner.cls)}>
        <Icon size={16} aria-hidden="true" className="mt-0.5 shrink-0" />
        <span>{banner.text}</span>
      </div>
      {check.error && <p className="text-sm text-soft">{localized(check.error.message, check.error.messages)}</p>}
      {check.checks.length > 0 && (
        <ul className="space-y-2">
          {check.checks.map(item => (
            <li key={item.id} className="flex items-start gap-2 text-sm">
              {item.passed
                ? <CheckCircle2 size={15} className="mt-0.5 shrink-0 text-emerald" aria-label={t('lab.checks.passed')} role="img" />
                : item.pending
                  ? <Circle size={15} className="mt-0.5 shrink-0 text-ghost" aria-label={t('lab.checks.pending')} role="img" />
                  : <XCircle size={15} className="mt-0.5 shrink-0 text-rose" aria-label={t('lab.checks.failed')} role="img" />}
              <div className="min-w-0">
                <p className={item.passed || item.pending ? 'text-soft' : 'text-bright'}>{localized(item.label, item.labels) ?? item.id}</p>
                {!item.passed && item.message && (
                  <p className="mt-0.5 text-xs leading-relaxed text-ghost">{localized(item.message, item.messages)}</p>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
      {check.run?.stderr && <Pre tone="error">{check.run.stderr}</Pre>}
    </div>
  )
}

/** The attempt's saved artifacts — charts from any Run or Check, latest version of each. */
function ArtifactsView({ artifacts, artifactData, loadArtifact }: {
  artifacts: LabArtifact[]
  artifactData: Record<string, string>
  loadArtifact: (artifact: LabArtifact) => void
}) {
  const { t } = useLabI18n()
  useEffect(() => { for (const artifact of artifacts) loadArtifact(artifact) }, [artifacts, loadArtifact])
  if (artifacts.length === 0) return <p className="text-sm text-ghost">{t('lab.artifacts.empty')}</p>
  return (
    <ul className="space-y-4">
      {artifacts.map(artifact => {
        const src = artifactData[artifact.sha256]
        return (
          <li key={artifact.path} className="space-y-2">
            <p className="font-mono text-xs text-soft" dir="ltr">{artifact.path}</p>
            {artifact.encoding === 'base64' && src ? (
              // eslint-disable-next-line @next/next/no-img-element -- a data: URL of a chart this learner generated
              <img src={src} alt={artifact.path} className="max-w-full rounded-lg border border-border bg-white" />
            ) : artifact.encoding === 'base64' ? (
              <Spinner className="size-4" />
            ) : null}
          </li>
        )
      })}
    </ul>
  )
}

function HintsView({ hints }: { hints: LabHint[] }) {
  const { tf, t, pick } = useLabI18n()
  const [shown, setShown] = useState(0)
  if (hints.length === 0) return <p className="text-sm text-ghost">{t('lab.hints.empty')}</p>
  return (
    <div className="space-y-3">
      <p className="text-xs text-ghost">{t('lab.hints.intro')}</p>
      {hints.slice(0, shown).map((hint, index) => (
        <div key={index} role="note" className="rounded-lg border border-amber/20 bg-amber/5 p-3 text-sm text-soft">
          <p className="mb-1 text-xs font-semibold text-amber-text">{tf('lab.hints.label', { n: index + 1 })}</p>
          <p className="break-words">{pick(hint.en, hint.ar)}</p>
        </div>
      ))}
      {shown < hints.length && (
        <button type="button" onClick={() => setShown(count => count + 1)}
          className="min-h-[40px] rounded-md border border-border px-3 text-sm text-soft hover:border-amber/30 hover:text-bright lg:min-h-[34px]">
          {tf('lab.hints.show', { n: shown + 1 })}
        </button>
      )}
    </div>
  )
}

/** Run output, Check Step results, generated artifacts and hints. */
export function OutputPanel({
  tab, onTab, run, running, runFailed, check, checking, checkFailed, hints, hintsKey, taskTitle,
  artifacts, artifactData, loadArtifact,
}: {
  tab: LabPanelTab
  onTab: (tab: LabPanelTab) => void
  run: LabRunResult | null
  running: boolean
  runFailed: LabRequestError
  check: LabCheckResult | null
  checking: boolean
  checkFailed: LabRequestError
  hints: LabHint[]
  /** Resets the revealed hints when the task changes. */
  hintsKey: string
  taskTitle: (slug: string) => string
  artifacts: LabArtifact[]
  artifactData: Record<string, string>
  loadArtifact: (artifact: LabArtifact) => void
}) {
  const { t } = useLabI18n()
  const label: Record<LabPanelTab, LabStringKey> = {
    output: 'lab.panel.output', checks: 'lab.panel.checks', artifacts: 'lab.panel.artifacts', hints: 'lab.panel.hints',
  }
  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <div role="tablist" aria-label={t('lab.panel.output')} className="flex shrink-0 gap-1 overflow-x-auto border-b border-border px-2">
        {TABS.map(name => (
          <button
            key={name}
            type="button"
            role="tab"
            id={`lab-tab-${name}`}
            aria-selected={tab === name}
            aria-controls={`lab-tabpanel-${name}`}
            onClick={() => onTab(name)}
            className={cn(
              '-mb-px min-h-[44px] shrink-0 border-b-2 px-3 text-xs font-medium transition-colors lg:min-h-[38px]',
              tab === name ? 'border-amber text-amber-text' : 'border-transparent text-ghost hover:text-soft',
            )}
          >
            {t(label[name])}
            {name === 'artifacts' && artifacts.length > 0 && (
              <span className="ms-1.5 font-mono text-[10px] text-ghost">{artifacts.length}</span>
            )}
          </button>
        ))}
      </div>
      <div role="tabpanel" id={`lab-tabpanel-${tab}`} aria-labelledby={`lab-tab-${tab}`} className="min-h-0 flex-1 overflow-y-auto p-4">
        {tab === 'output' && <RunView run={run} running={running} failed={runFailed} />}
        {tab === 'checks' && <ChecksView check={check} checking={checking} failed={checkFailed} taskTitle={taskTitle} />}
        {tab === 'artifacts' && <ArtifactsView artifacts={artifacts} artifactData={artifactData} loadArtifact={loadArtifact} />}
        {tab === 'hints' && <HintsView key={hintsKey} hints={hints} />}
      </div>
    </div>
  )
}
