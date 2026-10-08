'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { api } from '@/lib/api'
import type {
  LabArtifact, LabAttempt, LabCheckResult, LabFile, LabRunResult, LabSubmission, LabWorkspace,
} from './types'

export type LabBusy = null | 'save' | 'run' | 'check' | 'reset' | 'submit'
/** Why a Run/Check request failed before producing a result. `busy`: the learner already has
 *  one running (another tab) — the server allows one execution at a time per learner. */
export type LabRequestError = null | 'network' | 'busy'

function requestError(error: unknown): LabRequestError {
  const response = (error as { response?: { status?: number; data?: { detail?: { code?: string } } } })?.response
  return response?.status === 409 && response.data?.detail?.code === 'EXECUTION_IN_PROGRESS' ? 'busy' : 'network'
}

/** Everything the Project Lab page does, independent of layout.
 *
 *  Edits live in `drafts` until saved. Run and Check Step always save every unsaved draft first,
 *  because the server executes the SAVED workspace — what the learner sees is what runs. */
export function useProjectLab(attemptId: number) {
  const [attempt, setAttempt] = useState<LabAttempt | null>(null)
  const [workspace, setWorkspace] = useState<LabWorkspace | null>(null)
  const [files, setFiles] = useState<Record<string, LabFile>>({})
  const [drafts, setDrafts] = useState<Record<string, string>>({})
  const [selectedPath, setSelectedPath] = useState<string | null>(null)
  const [selectedTask, setSelectedTask] = useState<string | null>(null)
  const [busy, setBusy] = useState<LabBusy>(null)
  const [run, setRun] = useState<LabRunResult | null>(null)
  const [runError, setRunError] = useState<LabRequestError>(null)
  const [check, setCheck] = useState<LabCheckResult | null>(null)
  const [checkError, setCheckError] = useState<LabRequestError>(null)
  const [saveError, setSaveError] = useState(false)
  const [artifacts, setArtifacts] = useState<LabArtifact[]>([])
  // Image data URLs keyed by sha256, so a chart that did not change is never fetched twice.
  const [artifactData, setArtifactData] = useState<Record<string, string>>({})
  const [submission, setSubmission] = useState<LabSubmission | null>(null)
  const [submitError, setSubmitError] = useState(false)
  const [loadState, setLoadState] = useState<'loading' | 'ready' | 'missing'>('loading')
  // Read through refs so the callbacks below keep a stable identity (the initial load depends on
  // `openFile`; re-creating it on every edit would reload the lab).
  const filesRef = useRef(files)
  const draftsRef = useRef(drafts)
  const artifactDataRef = useRef(artifactData)
  useEffect(() => {
    filesRef.current = files
    draftsRef.current = drafts
    artifactDataRef.current = artifactData
  })

  const openFile = useCallback(async (path: string) => {
    setSelectedPath(path)
    if (filesRef.current[path]) return
    try {
      const file = await api.getLabFile(attemptId, path)
      setFiles(previous => ({ ...previous, [path]: file }))
    } catch { /* the editor shows its empty state; choosing the file again retries */ }
  }, [attemptId])

  const refreshWorkspace = useCallback(async () => {
    try { setWorkspace(await api.getLabWorkspace(attemptId)) } catch { /* keep the previous tree */ }
  }, [attemptId])

  const refreshArtifacts = useCallback(async () => {
    try { setArtifacts(await api.getLabArtifacts(attemptId)) } catch { /* keep the previous list */ }
  }, [attemptId])

  /** The data URL of a saved image artifact (fetched once per version). */
  const loadArtifact = useCallback(async (artifact: LabArtifact) => {
    if (artifactDataRef.current[artifact.sha256] || artifact.encoding !== 'base64') return
    try {
      const full = await api.getLabArtifact(attemptId, artifact.path)
      setArtifactData(previous => ({ ...previous, [full.sha256]: `data:${full.media_type};base64,${full.content}` }))
    } catch { /* the preview shows the path without the image */ }
  }, [attemptId])

  const refreshSubmission = useCallback(async () => {
    try { setSubmission(await api.getLabSubmission(attemptId)) } catch { /* summary stays hidden */ }
  }, [attemptId])

  useEffect(() => {
    let cancelled = false
    void (async () => {
      try {
        const [nextAttempt, nextWorkspace] = await Promise.all([api.getLabAttempt(attemptId), api.getLabWorkspace(attemptId)])
        if (cancelled) return
        setAttempt(nextAttempt)
        setWorkspace(nextWorkspace)
        const current = nextAttempt.progress.current_task
          ?? nextAttempt.milestones[0]?.tasks[0]?.slug ?? null
        setSelectedTask(current)
        const task = nextAttempt.milestones.flatMap(m => m.tasks).find(t => t.slug === current)
        const first = task?.primary_file ?? nextWorkspace.entries.find(e => e.kind === 'file' && e.editable)?.path
        setLoadState('ready')
        void refreshArtifacts()
        if (nextAttempt.progress.completed_tasks === nextAttempt.progress.total_tasks) void refreshSubmission()
        if (first) await openFile(first)
      } catch {
        if (!cancelled) setLoadState('missing')
      }
    })()
    return () => { cancelled = true }
  }, [attemptId, openFile, refreshArtifacts, refreshSubmission])

  const dirtyPaths = Object.keys(drafts).filter(path => files[path] && drafts[path] !== files[path].content)

  const edit = useCallback((path: string, content: string) => {
    const file = filesRef.current[path]
    if (!file?.editable) return
    setSaveError(false)
    setDrafts(previous => ({ ...previous, [path]: content }))
  }, [])

  /** Save every unsaved draft. Returns false if any save failed (drafts are kept). */
  const saveAll = useCallback(async (): Promise<boolean> => {
    const pending = Object.entries(draftsRef.current).filter(([path, content]) => filesRef.current[path]?.content !== content)
    if (pending.length === 0) return true
    try {
      const saved = await Promise.all(pending.map(([path, content]) => api.saveLabFile(attemptId, path, content)))
      setFiles(previous => ({ ...previous, ...Object.fromEntries(saved.map(file => [file.path, file])) }))
      setDrafts(previous => {
        const next = { ...previous }
        for (const file of saved) if (next[file.path] === file.content) delete next[file.path]
        return next
      })
      void refreshWorkspace()
      return true
    } catch {
      setSaveError(true)
      return false
    }
  }, [attemptId, refreshWorkspace])

  const save = useCallback(async () => {
    setBusy('save')
    try { await saveAll() } finally { setBusy(null) }
  }, [saveAll])

  const runFile = useCallback(async (path: string) => {
    setBusy('run')
    setRunError(null)
    try {
      if (!(await saveAll())) return
      const result = await api.runLabFile(attemptId, path)
      setRun(result)
      if (result.generated_files.length > 0) void refreshArtifacts()
    } catch (error) {
      setRunError(requestError(error))
    } finally {
      setBusy(null)
    }
  }, [attemptId, saveAll, refreshArtifacts])

  const checkTask = useCallback(async (taskSlug: string) => {
    setBusy('check')
    setCheckError(null)
    try {
      if (!(await saveAll())) return
      const result = await api.checkLabTask(attemptId, taskSlug)
      setCheck(result)
      setAttempt(previous => previous ? { ...previous, status: result.progress.status, progress: result.progress } : previous)
      void refreshArtifacts()
      if (result.progress.completed_tasks === result.progress.total_tasks) void refreshSubmission()
    } catch (error) {
      setCheckError(requestError(error))
    } finally {
      setBusy(null)
    }
  }, [attemptId, saveAll, refreshArtifacts, refreshSubmission])

  const resetFile = useCallback(async (path: string) => {
    setBusy('reset')
    try {
      const file = await api.resetLabFile(attemptId, path)
      setFiles(previous => ({ ...previous, [path]: file }))
      setDrafts(previous => {
        const next = { ...previous }
        delete next[path]
        return next
      })
      void refreshWorkspace()
    } catch {
      setSaveError(true)
    } finally {
      setBusy(null)
    }
  }, [attemptId, refreshWorkspace])

  /** Final submission: only offered once every task has passed; repeating it is harmless. */
  const submit = useCallback(async () => {
    setBusy('submit')
    setSubmitError(false)
    try {
      const result = await api.submitLabProject(attemptId)
      setSubmission(result)
      setAttempt(previous => previous ? { ...previous, submitted_at: result.submitted_at } : previous)
    } catch {
      setSubmitError(true)
    } finally {
      setBusy(null)
    }
  }, [attemptId])

  return {
    attempt, workspace, files, drafts, dirtyPaths, selectedPath, selectedTask, setSelectedTask,
    busy, run, runError, check, checkError, saveError, loadState,
    artifacts, artifactData, loadArtifact, submission, submitError,
    openFile, edit, save, runFile, checkTask, resetFile, submit,
  }
}

export type ProjectLabState = ReturnType<typeof useProjectLab>
