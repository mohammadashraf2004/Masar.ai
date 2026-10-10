'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import { Check, ChevronDown, Info, Lightbulb, RotateCcw, X } from 'lucide-react'
import { Spinner } from '@/components/ui/index'
import { cn } from '@/lib/utils'
import { useExerciseI18n } from '@/lib/i18n'
import type { ExerciseAttemptState, ExerciseFile, ExerciseRunResult, GradeResult } from '@/types'
import { exerciseDraftKey } from '../draftKeys'
import { CodeEditor } from './CodeEditor'
import { codeCellColors } from './codeCellTheme'
import { filesSignature, useExerciseRun } from './useExerciseRun'

type ExerciseLabels = ReturnType<typeof useExerciseI18n>

/** A failed request in words a learner can act on. Nothing was graded in
 *  any of these cases, so none of them may read like a wrong answer. */
export function describeRequestError(cause: unknown, labels: ExerciseLabels) {
  const response = (cause as { response?: { status?: number; data?: { detail?: unknown } } } | null)?.response
  if (!response) return labels.errors.unavailable
  if (response.status === 429) return labels.errors.busy
  if (response.status === 401) return labels.errors.session
  if (response.status === 409) return labels.errors.notGradable
  return labels.errors.unavailable
}

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
  /** The server's record of this learner's attempts; it decides when the
   *  worked solution may open, so the choice survives reloads and devices. */
  onLoadAttemptState?(): Promise<ExerciseAttemptState>
  onPassed?(): void
  gradingAvailable?: boolean
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
  hint,
  onShowSolution,
  onLoadAttemptState,
  gradingAvailable = true,
}: CodeCellProps) {
  const tx = useExerciseI18n()
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
  // Hints are a ladder: each paragraph of the authored hint is one rung,
  // revealed on request so the first nudge never gives the answer away.
  const hintSteps = useMemo(() => (hint ?? '').split(/\n\s*\n/).map(step => step.trim()).filter(Boolean), [hint])
  const [hintsShown, setHintsShown] = useState(0)
  // The worked solution opens after a pass or after several different wrong
  // answers. The server decides (and enforces it); this mirrors its record.
  const [attempt, setAttempt] = useState<ExerciseAttemptState | null>(null)
  const [solution, setSolution] = useState<string | null>(null)
  // A solution already fetched (after a pass) stays available to toggle.
  const solutionAvailable = (attempt?.solution_available ?? false) || solution !== null
  const [solutionOpen, setSolutionOpen] = useState(false)
  const [solutionLoading, setSolutionLoading] = useState(false)
  const solutionRequest = useRef<Promise<string> | null>(null)
  const autoRevealDone = useRef(false)
  const activeExercise = useRef(exerciseId)
  const menuRef = useRef<HTMLDivElement>(null)
  const runner = useExerciseRun({ onRunTests, onSubmit, describeError: cause => describeRequestError(cause, tx) })

  // A different exercise starts with no solution shown. Reset during render
  // (React's "adjust state when a prop changes"), not in an effect, so the
  // previous exercise's solution is never painted for the new one.
  const [solutionFor, setSolutionFor] = useState(exerciseId)
  if (solutionFor !== exerciseId) {
    setSolutionFor(exerciseId)
    setSolution(null)
    setSolutionOpen(false)
    setSolutionLoading(false)
    setHintsShown(0)
    setAttempt(null)
  }

  useEffect(() => {
    if (!onLoadAttemptState || !gradingAvailable) return
    let live = true
    void (async () => {
      try {
        const state = await onLoadAttemptState()
        if (live && state) setAttempt(state)
      } catch {
        // Unknown state keeps the solution locked; the server enforces it anyway.
      }
    })()
    return () => { live = false }
    // Once per exercise: the loader is a new closure on every render.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [exerciseId, gradingAvailable])

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
  // The shown result belongs to code the learner has since edited.
  const stale = runner.resultFor !== null && runner.resultFor !== filesSignature(currentFiles())

  function update(content: string) {
    if (!current || current.readOnly) return
    setDrafts(previous => ({ ...previous, [current.name]: content }))
    window.localStorage.setItem(draftKey(exerciseId, current), content)
    // The mentor (hints and chat context) still reads the stable legacy key.
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
    // The old result described code that is gone.
    runner.clear()
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
    const state = grade?.attempt
    if (state && activeExercise.current === submittedFor) {
      setAttempt(state)
      // From the second different wrong answer on, open one more (more
      // specific) hint for each attempt; the third also opens the solution.
      if (!grade.passed && state.failed_checks >= 2) {
        setHintsShown(shown => Math.max(shown, Math.min(state.failed_checks, hintSteps.length)))
      }
    }
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
                {file.label ?? file.name}
              </button>
            ))}
          </div>
          <span className="ms-auto hidden shrink-0 items-center px-3 text-xs text-[#5C6678] sm:flex">{runtime}</span>
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
            ariaLabel={`${current.label ?? current.name}${current.readOnly ? ' (read only)' : ''}`}
            language={language}
          />
        </div>

        <div className="flex flex-wrap justify-end gap-2 border-t border-[#1E2535] bg-[#0D1117] px-3 py-2.5 font-arabic text-[13px]">
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
          {runner.execution.stderr && (runner.grade && !runner.grade.passed && runner.grade.feedback.message ? (
            // After Check Answer the result card explains the failure; the raw
            // traceback stays one click away instead of in the learner's face.
            <details className="border-t border-rose-500/20">
              <summary className="cursor-pointer px-4 py-2 font-arabic text-xs text-[#A0AEC0]" dir="auto">{tx.technicalDetails}</summary>
              <pre className="max-h-48 overflow-auto whitespace-pre-wrap px-4 pb-4 font-mono text-xs leading-5 text-rose-300">{runner.execution.stderr}</pre>
            </details>
          ) : (
            <pre className="max-h-48 overflow-auto whitespace-pre-wrap border-t border-rose-500/20 p-4 font-mono text-xs leading-5 text-rose-300">{runner.execution.stderr}</pre>
          ))}
        </section>
      )}
      {runner.status === 'done' && runner.grade && <GradeCard grade={runner.grade} labels={tx} stale={stale} />}
      {runner.status === 'done' && runner.grade?.passed && attempt?.passed && !attempt.completed_independently && (
        <p className="text-xs text-ghost" dir="auto">{tx.passedWithSolution}</p>
      )}
      {(hintSteps.length > 0 || onShowSolution) && (
        <div className="flex flex-wrap items-center gap-2" dir="auto">
          {hintSteps.length > 0 && hintsShown === 0 && (
            <button type="button" onClick={() => setHintsShown(1)} className="inline-flex min-h-9 items-center gap-2 rounded-lg border border-border px-3 text-sm text-bright">
              <Lightbulb size={14} />{tx.hint}
            </button>
          )}
          {onShowSolution && solutionAvailable && (
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
          {onShowSolution && !solutionAvailable && gradingAvailable && (
            <span className="text-xs text-ghost">{tx.solutionLocked(attempt?.checks_until_solution ?? 3)}</span>
          )}
        </div>
      )}
      {hintsShown > 0 && (
        <div role="note" aria-live="polite" className="space-y-3 rounded-xl border border-amber/30 bg-amber/5 p-4 text-sm leading-6 text-bright" dir="auto">
          <ol className="space-y-2">
            {hintSteps.slice(0, hintsShown).map((step, index) => (
              <li key={index} className="flex gap-2">
                <Lightbulb size={14} className="mt-1 shrink-0 text-amber-text" />
                <span>
                  {hintSteps.length > 1 && (
                    <span className="me-1.5 text-xs font-semibold text-amber-text">{tx.hintCount(index + 1, hintSteps.length)}</span>
                  )}
                  {step}
                </span>
              </li>
            ))}
          </ol>
          <div className="flex flex-wrap gap-2">
            {hintsShown < hintSteps.length && (
              <button type="button" onClick={() => setHintsShown(count => count + 1)} className="min-h-9 rounded-lg border border-amber/40 px-3 text-sm text-bright">
                {tx.nextHint}
              </button>
            )}
            <button type="button" onClick={() => setHintsShown(0)} className="min-h-9 rounded-lg px-3 text-sm text-dim hover:text-bright">
              {tx.hideHints}
            </button>
          </div>
        </div>
      )}
      {solutionOpen && solution && (
        <section className="overflow-hidden rounded-xl border border-border bg-[#090D13]">
          <h4 className="border-b border-border px-4 py-2 text-sm font-semibold text-bright" dir="auto">{tx.completedSolution}</h4>
          <pre className="overflow-auto p-4 font-mono text-xs text-[#E2E8F0]" dir="ltr">{solution}</pre>
        </section>
      )}
    </div>
  )
}

/** What kind of result this is, so a learner can tell "Python could not read
 * it" from "it ran but the answer is wrong" at a glance - and from "we could
 * not grade it", which is never the learner's fault. */
export function gradeOutcome(grade: GradeResult, labels: ExerciseLabels) {
  if (grade.passed) return { label: labels.status.correct, scored: true, graded: true }
  if (grade.feedback.code === 'BLANKS_REMAINING') return { label: labels.status.blanks, scored: false, graded: true }
  switch (grade.status) {
    case 'incorrect': return { label: labels.status.incorrect, scored: true, graded: true }
    case 'partial': return { label: labels.status.partial, scored: true, graded: true }
    case 'syntax_error': return { label: labels.status.syntax, scored: false, graded: true }
    case 'runtime_error': return { label: labels.status.runtime, scored: false, graded: true }
    case 'timeout': return { label: labels.status.timeout, scored: false, graded: true }
    case 'memory_limit': return { label: labels.status.memory, scored: false, graded: true }
    case 'output_limit': return { label: labels.status.output, scored: false, graded: true }
    case 'forbidden_operation': return { label: labels.status.forbidden, scored: false, graded: true }
    case 'execution_error': case 'grading_error': return { label: labels.status.notGraded, scored: false, graded: false }
    default: return { label: labels.status.error, scored: false, graded: false }
  }
}

function GradeCard({ grade, labels, stale }: { grade: GradeResult; labels: ExerciseLabels; stale: boolean }) {
  const outcome = gradeOutcome(grade, labels)
  return (
    <section
      aria-live="polite"
      className={cn(
        'rounded-xl border bg-[#0D1117] p-4 text-[#E2E8F0]',
        grade.passed ? 'border-emerald-500/40' : outcome.graded ? 'border-[#1E2535]' : 'border-amber-500/40',
        stale && 'opacity-80',
      )}
      dir="auto"
    >
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs text-[#5C6678]">{labels.result}</p>
          <p className="text-lg font-semibold">{outcome.label}</p>
        </div>
        {outcome.scored && grade.tests_total > 0 && (
          <span
            className={cn('rounded-full px-2.5 py-1 font-mono text-xs font-semibold', grade.passed ? 'bg-emerald-500/15 text-emerald-300' : 'bg-rose-500/15 text-rose-300')}
            dir="ltr"
          >
            {grade.tests_passed} / {grade.tests_total} {labels.tests}
          </span>
        )}
      </div>
      <p className="mt-4 flex items-start gap-2 border-t border-[#1E2535] pt-3 text-sm leading-6 text-[#CBD5E1]">
        <span className={cn(
          'mt-1 flex size-4 shrink-0 items-center justify-center rounded-full',
          grade.passed ? 'bg-emerald-500/20 text-emerald-300' : outcome.graded ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-300',
        )}>
          {grade.passed ? <Check size={10} /> : outcome.graded ? <X size={10} /> : <Info size={10} />}
        </span>
        <span className="whitespace-pre-line">{grade.feedback.message}</span>
      </p>
      {!grade.passed && (
        <p className="mt-2 ps-6 text-xs text-[#8B98AD]">{outcome.graded ? labels.tryAgain : labels.notCounted}</p>
      )}
      {stale && <p className="mt-2 ps-6 text-xs text-amber-300">{labels.stale}</p>}
    </section>
  )
}
