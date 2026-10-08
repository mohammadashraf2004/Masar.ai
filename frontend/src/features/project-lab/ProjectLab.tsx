'use client'

import { useEffect, useRef, useState } from 'react'
import { Eye, PenLine, Play, RotateCcw, Save, ShieldCheck } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Modal } from '@/components/ui/Modal'
import { Spinner } from '@/components/ui/index'
import { cn } from '@/lib/utils'
import { FileEditor } from './FileEditor'
import { FileTree } from './FileTree'
import { labProjectHref } from './LabProjectsSection'
import { MarkdownPreview } from './MarkdownPreview'
import { OutputPanel, type LabPanelTab } from './OutputPanel'
import { SubmissionPanel } from './SubmissionPanel'
import { TaskPanel } from './TaskPanel'
import { useLabI18n } from './strings'
import { useProjectLab } from './useProjectLab'

type MobileView = 'task' | 'code' | 'output'

/** The Project Lab workspace for one attempt.
 *
 *  Very wide screens (1900px+): task | files + editor | output, side by side. On ordinary desktop
 *  screens the output panel moves under the editor, so the editor keeps a useful width after the
 *  app sidebar has taken its share of the viewport. Below lg the three areas become views behind
 *  a segmented control, one at a time at full width. Layout uses logical properties throughout,
 *  so the page mirrors in Arabic; code, file names and output stay LTR. */
export function ProjectLab({ attemptId }: { attemptId: number }) {
  const lab = useProjectLab(attemptId)
  const { t, tf, pick, dir } = useLabI18n()
  const [panel, setPanel] = useState<LabPanelTab>('output')
  const [view, setView] = useState<MobileView>('code')
  const [confirmReset, setConfirmReset] = useState(false)
  // Markdown files open as text; the report can be read rendered, with its charts.
  const [preview, setPreview] = useState(false)
  const confirmRef = useRef<HTMLButtonElement>(null)

  const file = lab.selectedPath ? lab.files[lab.selectedPath] : undefined
  const value = file ? (lab.drafts[file.path] ?? file.content ?? '') : ''
  const dirty = file ? lab.dirtyPaths.includes(file.path) : false
  const runnable = !!file && file.editable && (file.language === 'python' || file.language === 'sql')
  const previewable = file?.language === 'markdown'
  const showPreview = previewable && preview
  const tasks = lab.attempt?.milestones.flatMap(m => m.tasks) ?? []
  const task = tasks.find(item => item.slug === lab.selectedTask)
  const busy = lab.busy !== null

  // Leaving with unsaved edits asks first (the browser's own prompt).
  useEffect(() => {
    if (lab.dirtyPaths.length === 0) return
    const warn = (event: BeforeUnloadEvent) => { event.preventDefault() }
    window.addEventListener('beforeunload', warn)
    return () => window.removeEventListener('beforeunload', warn)
  }, [lab.dirtyPaths.length])

  const run = () => {
    if (!file || !runnable) return
    setPanel('output')
    setView('output')
    void lab.runFile(file.path)
  }
  const check = () => {
    if (!task) return
    setPanel('checks')
    setView('output')
    void lab.checkTask(task.slug)
  }
  const onKeyDown = (event: React.KeyboardEvent) => {
    if (!(event.ctrlKey || event.metaKey) || busy) return
    if (event.key === 's') { event.preventDefault(); void lab.save() }
    if (event.key === 'Enter') { event.preventDefault(); run() }
  }

  if (lab.loadState === 'loading') {
    return <div className="flex flex-1 items-center justify-center p-8"><Spinner announce className="size-6" /></div>
  }
  if (lab.loadState === 'missing' || !lab.attempt || !lab.workspace) {
    return <p role="alert" className="p-8 text-sm text-rose">{t('lab.missing')}</p>
  }

  const status = lab.busy === 'save' ? t('lab.editor.saving')
    : lab.saveError ? t('lab.editor.saveFailed')
    : dirty ? t('lab.editor.unsaved') : t('lab.editor.saved')

  return (
    <div className="flex min-h-0 flex-1 flex-col" dir={dir} onKeyDown={onKeyDown}>
      <div role="tablist" aria-label={t('lab.view.label')} className="flex shrink-0 gap-1 border-b border-border p-2 lg:hidden">
        {(['task', 'code', 'output'] as const).map(name => (
          <button
            key={name}
            type="button"
            role="tab"
            aria-selected={view === name}
            onClick={() => setView(name)}
            className={cn(
              'min-h-[44px] flex-1 rounded-md text-sm font-medium',
              view === name ? 'bg-amber/10 text-amber-text' : 'text-ghost hover:text-soft',
            )}
          >
            {t(`lab.view.${name}` as const)}
          </button>
        ))}
      </div>

      <div className={cn(
        // grid-cols-1 = minmax(0, 1fr): below lg a wide result table must scroll inside its panel,
        // not stretch an implicit auto column (and the page) past the viewport.
        'grid min-h-0 flex-1 grid-cols-1',
        'lg:grid-cols-[minmax(280px,320px)_minmax(0,1fr)] lg:grid-rows-[minmax(0,2fr)_minmax(220px,1fr)]',
        'min-[1900px]:grid-cols-[minmax(300px,340px)_minmax(0,1fr)_minmax(340px,420px)] min-[1900px]:grid-rows-1',
      )}>
        <aside className={cn('min-h-0 min-w-0 flex-col border-border lg:row-span-2 lg:flex lg:border-e min-[1900px]:row-span-1', view === 'task' ? 'flex' : 'hidden')}>
          <TaskPanel
            attempt={lab.attempt}
            selectedTask={lab.selectedTask}
            onSelectTask={lab.setSelectedTask}
            onOpenFile={path => { void lab.openFile(path); setView('code') }}
            footer={lab.submission?.ready ? (
              <SubmissionPanel submission={lab.submission} submitting={lab.busy === 'submit'}
                failed={lab.submitError} onSubmit={() => void lab.submit()}
                summaryHref={labProjectHref(lab.attempt.project.slug)} />
            ) : null}
          />
        </aside>

        <section
          aria-label={t('lab.files')}
          className={cn('min-h-0 min-w-0 flex-col lg:col-start-2 lg:row-start-1 lg:flex', view === 'code' ? 'flex' : 'hidden')}
        >
          <div className="flex shrink-0 flex-wrap items-center gap-2 border-b border-border px-3 py-2">
            <p className="min-w-0 basis-full truncate font-mono text-xs text-soft sm:flex-1 sm:basis-auto" dir="ltr">{file?.path ?? ''}</p>
            {file?.editable && <span className={cn('text-xs', lab.saveError ? 'text-rose' : 'text-ghost')} role="status">{status}</span>}
            {previewable && (
              <Button size="sm" variant="ghost" onClick={() => setPreview(value => !value)} aria-pressed={showPreview}>
                {showPreview
                  ? <><PenLine size={13} aria-hidden="true" />{t('lab.editor.edit')}</>
                  : <><Eye size={13} aria-hidden="true" />{t('lab.editor.preview')}</>}
              </Button>
            )}
            {file?.editable && (
              <Button size="sm" variant="ghost" onClick={() => void lab.save()} disabled={busy || !dirty}>
                <Save size={13} aria-hidden="true" />{t('lab.action.save')}
              </Button>
            )}
            {file?.editable && (
              <Button size="sm" variant="ghost" onClick={() => setConfirmReset(true)} disabled={busy}>
                <RotateCcw size={13} aria-hidden="true" />{t('lab.action.reset')}
              </Button>
            )}
            {runnable && (
              <Button size="sm" variant="outline" onClick={run} disabled={busy} loading={lab.busy === 'run'}>
                <Play size={13} aria-hidden="true" />{lab.busy === 'run' ? t('lab.action.running') : t('lab.action.run')}
              </Button>
            )}
            <Button size="sm" onClick={check} disabled={busy || !task} loading={lab.busy === 'check'}>
              <ShieldCheck size={13} aria-hidden="true" />{lab.busy === 'check' ? t('lab.action.checking') : t('lab.action.check')}
            </Button>
          </div>

          <div className="grid min-h-0 flex-1 md:grid-cols-[220px_minmax(0,1fr)] xl:grid-cols-[240px_minmax(0,1fr)]">
            <div className="max-h-48 min-h-0 overflow-y-auto border-b border-border md:max-h-none md:border-b-0 md:border-e">
              <FileTree
                workspace={lab.workspace}
                selectedPath={lab.selectedPath}
                dirtyPaths={lab.dirtyPaths}
                onSelect={path => void lab.openFile(path)}
              />
            </div>
            <div className="flex min-h-[320px] min-w-0 flex-col bg-void">
              {file && showPreview ? (
                <MarkdownPreview markdown={value} artifacts={lab.artifacts} artifactData={lab.artifactData}
                  loadArtifact={lab.loadArtifact} />
              ) : file ? (
                <FileEditor key={file.path} file={file} value={value} onChange={content => lab.edit(file.path, content)} />
              ) : (
                <p className="p-6 text-sm text-ghost">{t('lab.editor.noFile')}</p>
              )}
            </div>
          </div>
        </section>

        <aside
          aria-label={t('lab.panel.output')}
          className={cn(
            'min-h-0 min-w-0 flex-col border-border lg:col-start-2 lg:row-start-2 lg:flex lg:border-t',
            'min-[1900px]:col-start-3 min-[1900px]:row-start-1 min-[1900px]:border-s min-[1900px]:border-t-0',
            view === 'output' ? 'flex' : 'hidden',
          )}
        >
          <OutputPanel
            tab={panel}
            onTab={setPanel}
            run={lab.run}
            running={lab.busy === 'run'}
            runFailed={lab.runError}
            check={lab.check}
            checking={lab.busy === 'check'}
            checkFailed={lab.checkError}
            hints={task?.hints ?? []}
            hintsKey={task?.slug ?? ''}
            taskTitle={slug => {
              const item = tasks.find(candidate => candidate.slug === slug)
              return item ? pick(item.title, item.title_ar) : slug
            }}
            artifacts={lab.artifacts}
            artifactData={lab.artifactData}
            loadArtifact={lab.loadArtifact}
          />
        </aside>
      </div>

      {confirmReset && file && (
        <Modal
          title={tf('lab.reset.title', { file: file.path })}
          description={t('lab.reset.body')}
          onClose={() => setConfirmReset(false)}
          initialFocus={confirmRef}
          icon={<RotateCcw size={16} aria-hidden="true" />}
          footer={(
            <>
              {/* Focus starts on Cancel: Enter must not destroy work by default. */}
              <Button ref={confirmRef} variant="ghost" onClick={() => setConfirmReset(false)}>{t('lab.reset.cancel')}</Button>
              <Button
                variant="danger"
                onClick={() => { setConfirmReset(false); void lab.resetFile(file.path) }}
              >
                {t('lab.reset.confirm')}
              </Button>
            </>
          )}
        />
      )}
    </div>
  )
}
