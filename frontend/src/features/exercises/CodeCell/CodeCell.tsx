'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import { Check, ChevronDown, Lightbulb, RotateCcw, X } from 'lucide-react'
import Link from 'next/link'
import { Spinner } from '@/components/ui/index'
import { cn } from '@/lib/utils'
import { useExerciseI18n, useMentorV2I18n } from '@/lib/i18n'
import type { ExerciseFile, ExerciseRunResult, GradeResult } from '@/types'
import { exerciseDraftKey } from '../draftKeys'
import { CodeEditor } from './CodeEditor'
import { codeCellColors } from './codeCellTheme'
import { useExerciseRun } from './useExerciseRun'

function starterVersion(content: string) {
  let hash = 2166136261
  for (let index = 0; index < content.length; index += 1) {
    hash ^= content.charCodeAt(index)
    hash = Math.imul(hash, 16777619)
  }
  return (hash >>> 0).toString(36)
}

function draftKey(exerciseId: string | number, file: ExerciseFile) {
  return exerciseDraftKey(exerciseId, file.name, starterVersion(file.content))
}

function legacyDraftKey(exerciseId: string | number, fileName: string) {
  return exerciseDraftKey(exerciseId, fileName)
}

export type CodeCellProps = {
  exerciseId: string | number
  files: ExerciseFile[]
  activeFile?: string
  runtime: string
  language?: string
  highlightLines?: number[]
  onChange?(name: string, content: string): void
  onRunTests(files: ExerciseFile[]): Promise<ExerciseRunResult>
  onSubmit(files: ExerciseFile[]): Promise<GradeResult>
  hint?: string | null
  onShowSolution?(): Promise<string>
  onPassed?(): void
  gradingAvailable?: boolean
  // [mentor-v2] where "ask for a review" goes (the mentor's code-review tab); omitted, the button is not shown
  reviewHref?: string
  // [/mentor-v2]
}

export function CodeCell({
  exerciseId,
  files,
  activeFile,
  runtime,
  language = 'python',
  highlightLines = [],
  onChange,
  onRunTests,
  onSubmit,
  onPassed,
  reviewHref,
  hint,
  onShowSolution,
  gradingAvailable = true,
}: CodeCellProps) {
  const tx = useExerciseI18n()
  const mentorTx = useMentorV2I18n()
  // Test fixtures are submitted to the runner but are intentionally private:
  // learners only see and edit solution files.
  const visibleFiles = useMemo(() => {
    const editable = files.filter(file => !file.readOnly)
    return editable.length > 0 ? editable : files
  }, [files])
  const starters = useMemo(() => new Map(files.map(file => [file.name, file])), [files])
  const [drafts, setDrafts] = useState<Record<string, string>>(() => Object.fromEntries(files.map(file => [file.name, file.content])))
  const [selected, setSelected] = useState(() => {
    if (activeFile && visibleFiles.some(file => file.name === activeFile)) return activeFile
    return visibleFiles[0]?.name ?? ''
  })
  const [menuOpen, setMenuOpen] = useState(false)
  const [hintOpen, setHintOpen] = useState(false)
  const [solution, setSolution] = useState<string | null>(null)
  const [solutionOpen, setSolutionOpen] = useState(false)
  const [solutionLoading, setSolutionLoading] = useState(false)
  const solutionRequest = useRef<Promise<string> | null>(null)
  const autoRevealDone = useRef(false)
  const activeExercise = useRef(exerciseId)
  const menuRef = useRef<HTMLDivElement>(null)
  const runner = useExerciseRun({ onRunTests, onSubmit })

  // A different exercise starts with no solution shown. Reset during render
  // (React's "adjust state when a prop changes"), not in an effect, so the
  // previous exercise's solution is never painted for the new one.
  const [solutionFor, setSolutionFor] = useState(exerciseId)
  if (solutionFor !== exerciseId) {
    setSolutionFor(exerciseId)
    setSolution(null)
    setSolutionOpen(false)
    setSolutionLoading(false)
  }

  useEffect(() => {
    // Restore after hydration so a browser-only draft cannot make the server
    // and first client render disagree.
    const timer = window.setTimeout(() => {
      setDrafts(Object.fromEntries(files.map(file => {
        // Starter-versioned keys prevent a draft from the old free-form
        // exercise from hiding a newly released fill-in-the-blank scaffold.
        const saved = window.localStorage.getItem(draftKey(exerciseId, file))
        return [file.name, saved ?? file.content]
      })))
    }, 0)
    return () => window.clearTimeout(timer)
  }, [exerciseId, files])

  useEffect(() => {
    if (!menuOpen) return
    const close = (event: MouseEvent) => {
      if (!menuRef.current?.contains(event.target as Node)) setMenuOpen(false)
    }
    document.addEventListener('mousedown', close)
    return () => document.removeEventListener('mousedown', close)
  }, [menuOpen])

  useEffect(() => {
    if (runner.status === 'done' && runner.grade?.passed) onPassed?.()
  }, [onPassed, runner.grade?.passed, runner.status])

  useEffect(() => {
    // Refs are not render state: keep them in step after commit.
    activeExercise.current = exerciseId
    solutionRequest.current = null
    autoRevealDone.current = false
  }, [exerciseId])

  const current = starters.get(selected) ?? visibleFiles[0]
  const currentFiles = () => files.map(file => ({ ...file, content: drafts[file.name] ?? file.content }))

  function update(content: string) {
    if (!current || current.readOnly) return
    setDrafts(previous => ({ ...previous, [current.name]: content }))
    window.localStorage.setItem(draftKey(exerciseId, current), content)
    // The mentor code-review tab still consumes the stable legacy key.
    window.localStorage.setItem(legacyDraftKey(exerciseId, current.name), content)
    onChange?.(current.name, content)
  }

  function reset() {
    const fresh = Object.fromEntries(files.map(file => [file.name, file.content]))
    setDrafts(fresh)
    files.forEach(file => {
      window.localStorage.removeItem(draftKey(exerciseId, file))
      window.localStorage.removeItem(legacyDraftKey(exerciseId, file.name))
    })
    files.forEach(file => onChange?.(file.name, file.content))
    setMenuOpen(false)
  }

  function handleKeyboard(event: React.KeyboardEvent) {
    if (!(event.metaKey || event.ctrlKey) || event.key !== 'Enter' || runner.status === 'running') return
    event.preventDefault()
    if (event.shiftKey) {
      if (gradingAvailable) void submitAndReveal()
    } else {
      void runner.runTests(currentFiles())
    }
  }

  // The first passing submission of an exercise opens its worked solution.
  // Done here, in the submit handler, not in an effect watching the runner:
  // the reveal belongs to this submission of this exercise, so a pass left
  // over from the previous exercise can never open the next one's solution.
  async function submitAndReveal() {
    const submittedFor = exerciseId
    const grade = await runner.submit(currentFiles())
    if (!grade?.passed || !onShowSolution || autoRevealDone.current || activeExercise.current !== submittedFor) return
    autoRevealDone.current = true
    if (solution !== null) {
      setSolutionOpen(true)
      return
    }
    setSolutionLoading(true)
    try {
      const request = solutionRequest.current ?? onShowSolution()
      solutionRequest.current = request
      const value = await request
      if (activeExercise.current !== submittedFor) return
      setSolution(value)
      setSolutionOpen(true)
    } catch {
      solutionRequest.current = null
    } finally {
      if (activeExercise.current === submittedFor) setSolutionLoading(false)
    }
  }

  async function toggleSolution() {
    if (solutionOpen) {
      setSolutionOpen(false)
      return
    }
    if (solution === null && onShowSolution) {
      setSolutionLoading(true)
      try {
        const request = solutionRequest.current ?? onShowSolution()
        solutionRequest.current = request
        setSolution(await request)
      } catch {
        solutionRequest.current = null
        return
      } finally {
        setSolutionLoading(false)
      }
    }
    setSolutionOpen(true)
  }

  if (!current) return null

  return (
    <div className="min-w-0 space-y-3" dir="ltr" onKeyDown={handleKeyboard}>
      <section
        className="min-w-0 overflow-hidden rounded-xl border"
        style={{ background: codeCellColors.background, borderColor: 'rgb(var(--line))' }}
      >
        <div className="flex h-[42px] min-w-0 items-stretch border-b border-[#1E2535] bg-[#0D1117]">
          <div role="tablist" aria-label="Exercise files" className="flex min-w-0 flex-1 overflow-x-auto">
            {visibleFiles.map(file => (
              <button
                type="button"
                role="tab"
                aria-selected={file.name === current.name}
                key={file.name}
                onClick={() => setSelected(file.name)}
                className={cn(
                  'relative shrink-0 px-3 py-1.5 font-mono text-xs',
                  file.name === current.name ? 'text-[#E2E8F0] after:absolute after:inset-x-0 after:bottom-0 after:h-0.5 after:bg-[#F59E0B]' : 'text-[#5C6678]',
                )}
              >
                {file.name}
              </button>
            ))}
          </div>
          <span className="ms-auto hidden shrink-0 items-center px-3 text-[11px] text-[#5C6678] sm:flex">{runtime}</span>
          <div ref={menuRef} className="relative flex shrink-0 items-center">
            <button
              type="button"
              aria-label={tx.reset}
              aria-expanded={menuOpen}
              onClick={() => setMenuOpen(open => !open)}
              className="flex h-full items-center px-3 text-[#5C6678] hover:text-[#E2E8F0]"
            >
              <ChevronDown size={15} />
            </button>
            {menuOpen && (
              <div className="absolute end-2 top-10 z-20 w-52 rounded-lg border border-[#1E2535] bg-[#0D1117] p-1 shadow-2xl">
                <button type="button" onClick={reset} className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-start text-xs text-[#E2E8F0] hover:bg-[#161C28]">
                  <RotateCcw size={13} /> {tx.reset}
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="max-w-full overflow-x-auto">
          <CodeEditor
            value={drafts[current.name] ?? current.content}
            onChange={update}
            readOnly={current.readOnly}
            highlightLines={current.name === 'agent.py' ? highlightLines : []}
            ariaLabel={`${current.name}${current.readOnly ? ' (read only)' : ''}`}
            language={language}
          />
        </div>

        <div className="flex flex-wrap justify-end gap-2 border-t border-[#1E2535] bg-[#0D1117] px-3 py-2.5 font-arabic text-[13px]">
          {/* [mentor-v2] */}
          {reviewHref && (
            <Link
              href={reviewHref}
              className="flex h-[38px] items-center justify-center rounded-[7px] border border-[#1E2535] px-4 text-[#E2E8F0] hover:border-[#F59E0B]"
            >
              {mentorTx.t('mentor.v2.review.request')}
            </Link>
          )}
          {/* [/mentor-v2] */}
          <button
            type="button"
            disabled={runner.status === 'running'}
            onClick={() => void runner.runTests(currentFiles())}
            className="flex h-[38px] items-center justify-center gap-2 rounded-[7px] border border-[#1E2535] px-4 text-[#E2E8F0] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {runner.action === 'tests' && <Spinner className="size-3.5" />} {tx.runTests}
          </button>
          <button
            type="button"
            disabled={runner.status === 'running' || !gradingAvailable}
            title={!gradingAvailable ? tx.gradingPending : undefined}
            onClick={() => void submitAndReveal()}
            className="flex h-[38px] items-center justify-center gap-2 rounded-[7px] bg-[#F59E0B] px-4 font-semibold text-[#080A0E] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {runner.action === 'submit' && <Spinner className="size-3.5" />} {tx.submit}
          </button>
        </div>
      </section>

      {!gradingAvailable && (
        <div role="note" className="rounded-xl border border-amber/30 bg-amber/5 p-4 text-sm leading-6 text-bright" dir="auto">
          {tx.gradingPending}
        </div>
      )}

      {runner.status === 'running' && (
        <div role="status" className="rounded-xl border border-[#1E2535] bg-[#0D1117] p-4 text-sm text-[#E2E8F0]">
          <span className="flex items-center gap-2"><Spinner className="size-4" />{tx.grading}</span>
        </div>
      )}
      {runner.status === 'error' && (
        <div role="alert" className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-300">{runner.error}</div>
      )}
      {runner.execution && (
        <section aria-label={tx.console} className="overflow-hidden rounded-xl border border-[#1E2535] bg-[#090D13] text-sm" dir="ltr">
          <div className="border-b border-[#1E2535] px-4 py-2 font-arabic text-xs text-[#A0AEC0]" dir="auto">{tx.console}</div>
          {(runner.execution.stdout || !runner.execution.stderr) && (
            <pre className="max-h-64 overflow-auto whitespace-pre-wrap p-4 font-mono text-xs leading-5 text-[#E2E8F0]">
              {runner.execution.stdout || tx.noOutput}
            </pre>
          )}
          {runner.execution.stderr && (
            <pre className="max-h-48 overflow-auto whitespace-pre-wrap border-t border-rose-500/20 p-4 font-mono text-xs leading-5 text-rose-300">{runner.execution.stderr}</pre>
          )}
        </section>
      )}
      {runner.status === 'done' && runner.grade && <GradeCard grade={runner.grade} labels={tx} />}
      {(hint || onShowSolution) && (
        <div className="flex flex-wrap items-center gap-2" dir="auto">
          {hint && <button type="button" onClick={() => setHintOpen(open => !open)} className="inline-flex min-h-9 items-center gap-2 rounded-lg border border-border px-3 text-sm text-bright"><Lightbulb size={14} />{tx.hint}</button>}
          {onShowSolution && (
            <button
              type="button"
              disabled={solutionLoading}
              aria-expanded={solutionOpen}
              onClick={() => void toggleSolution()}
              className="min-h-9 rounded-lg border border-border px-3 text-sm text-bright disabled:opacity-60"
            >
              {solutionOpen ? tx.hideSolution : tx.showSolution}
            </button>
          )}
        </div>
      )}
      {hintOpen && hint && <div role="note" className="rounded-xl border border-amber/30 bg-amber/5 p-4 text-sm text-bright" dir="auto">{hint}</div>}
      {solutionOpen && solution && (
        <section className="overflow-hidden rounded-xl border border-border bg-[#090D13]">
          <h4 className="border-b border-border px-4 py-2 text-sm font-semibold text-bright" dir="auto">{tx.completedSolution}</h4>
          <pre className="overflow-auto p-4 font-mono text-xs text-[#E2E8F0]" dir="ltr">{solution}</pre>
        </section>
      )}
    </div>
  )
}

function GradeCard({ grade, labels }: { grade: GradeResult; labels: ReturnType<typeof useExerciseI18n> }) {
  return (
    <section className="rounded-xl border border-[#1E2535] bg-[#0D1117] p-4 text-[#E2E8F0]" dir="auto">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs text-[#5C6678]">{labels.result}</p>
          <p className="font-mono text-lg font-semibold" dir="ltr">{grade.tests_passed} / {grade.tests_total} {labels.tests}</p>
        </div>
        <span className={cn('rounded-full px-2.5 py-1 text-xs font-semibold', grade.passed ? 'bg-emerald-500/15 text-emerald-300' : 'bg-rose-500/15 text-rose-300')}>
          {grade.passed ? labels.passed : labels.failed}
        </span>
      </div>
      <p className="mt-4 flex items-start gap-2 border-t border-[#1E2535] pt-3 text-sm leading-6 text-[#A0AEC0]">
        <span className={cn('mt-1 flex size-4 shrink-0 items-center justify-center rounded-full', grade.passed ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300')}>
          {grade.passed ? <Check size={10} /> : <X size={10} />}
        </span>
        {grade.feedback.message}
      </p>
    </section>
  )
}
