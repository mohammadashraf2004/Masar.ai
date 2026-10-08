/** Wire types for the Project Lab API (backend/app/views/project_lab.py). */

export type LabLanguage = 'python' | 'sql' | 'markdown' | 'csv' | 'text'

export interface LabTrackRef {
  slug: string
  title: string
  title_ar?: string | null
}

export interface LabAttemptRef {
  id: number
  status: 'active' | 'completed'
  percent: number
  completed_tasks: number
  total_tasks: number
  submitted_at?: string | null
}

export interface LabProjectCard {
  slug: string
  title: string
  title_ar?: string | null
  summary: string
  summary_ar?: string | null
  difficulty: string
  estimated_hours?: number | null
  track: LabTrackRef
  milestone_count: number
  task_count: number
  attempt: LabAttemptRef | null
}

export interface LabTaskSummary {
  slug: string
  title: string
  title_ar?: string | null
}

export interface LabHint {
  en: string
  ar?: string | null
}

export interface LabTaskDetail extends LabTaskSummary {
  instructions: string
  instructions_ar?: string | null
  hints: LabHint[]
  primary_file?: string | null
}

export interface LabMilestone<T = LabTaskDetail> {
  slug: string
  title: string
  title_ar?: string | null
  summary?: string | null
  summary_ar?: string | null
  tasks: T[]
}

/** Project Overview content (shown before starting). */
export interface LabProjectOverview {
  role?: string | null
  role_ar?: string | null
  scenario?: string | null
  scenario_ar?: string | null
  duration_hours?: number[] | null
  skills: LabHint[]
  deliverables: LabHint[]
}

export interface LabProjectDetail extends LabProjectCard {
  milestones: LabMilestone<LabTaskSummary>[]
  overview: LabProjectOverview
}

export type LabTaskStatus = 'not_started' | 'in_progress' | 'completed'
export type LabOutcome = 'pass' | 'fail' | 'error'

export interface LabTaskProgress {
  slug: string
  milestone: string
  status: LabTaskStatus
  check_count: number
  last_outcome: LabOutcome | null
  completed_at: string | null
}

export interface LabProgress {
  status: 'active' | 'completed'
  completed_tasks: number
  total_tasks: number
  percent: number
  current_task: string | null
  milestones: { slug: string; completed_tasks: number; total_tasks: number; percent: number }[]
  tasks: LabTaskProgress[]
}

export interface LabAttempt {
  id: number
  status: 'active' | 'completed'
  started_at: string
  submitted_at?: string | null
  project: LabProjectCard
  milestones: LabMilestone[]
  workspace_root: string
  progress: LabProgress
}

export interface LabWorkspaceEntry {
  path: string
  kind: 'file' | 'dir'
  language: LabLanguage | null
  editable: boolean
  size: number | null
  modified: boolean
}

export interface LabWorkspace {
  root: string
  entries: LabWorkspaceEntry[]
}

export interface LabTable {
  columns: string[]
  rows: (string | number | boolean | null)[][]
  row_count: number
  truncated: boolean
}

export interface LabFile {
  path: string
  language: LabLanguage
  editable: boolean
  content: string | null
  table: LabTable | null
}

export type LabRunStatus = 'success' | 'error' | 'timeout' | 'infrastructure_error'

export interface LabGeneratedFile {
  path: string
  size: number
  media_type: string | null
  encoding: 'base64' | 'text' | null
  content: string | null
}

export interface LabRunResult {
  path: string
  kind: 'python' | 'sql'
  status: LabRunStatus
  stdout: string
  stderr: string
  execution_ms: number
  generated_files: LabGeneratedFile[]
  table: LabTable | null
  error: { type: string; message: string; line: number | null } | null
  /** Output beyond the project's limit was cut (the text ends with a marker). */
  stdout_truncated?: boolean
  stderr_truncated?: boolean
  /** The run generated more files than are returned and kept. */
  artifacts_truncated?: boolean
}

export interface LabCheckItem {
  id: string
  passed: boolean
  /** Not run yet: it depends on the checks above passing first. */
  pending?: boolean
  label: string | null
  labels: Record<string, string> | null
  message: string | null
  messages: Record<string, string> | null
}

export interface LabCheckResult {
  task: string
  outcome: LabOutcome
  passed: boolean
  checks: LabCheckItem[]
  error: { kind: 'execution' | 'infrastructure'; message: string; messages: Record<string, string> } | null
  run: { status: string; stdout: string; stderr: string } | null
  newly_completed: boolean
  task_status: LabTaskStatus
  progress: LabProgress
}

/** A file the learner's code generated (charts), the latest version per path. */
export interface LabArtifact {
  path: string
  media_type: string
  encoding: 'base64' | 'text'
  size: number
  sha256: string
  updated_at: string
}

export interface LabArtifactContent extends LabArtifact {
  content: string
}

export interface LabSubmission {
  submitted_at: string | null
  ready: boolean
  percent: number
  completed_tasks: number
  total_tasks: number
  milestones: { slug: string; title: string; title_ar?: string | null; completed: boolean }[]
  skills: LabHint[]
  artifacts: { path: string; media_type: string; size: number }[]
}

/** Portfolio-ready completion data (frozen at final submission). Artifacts are listed by path only. */
export interface LabCompletion {
  schema_version: number
  project: {
    slug: string
    title: string
    title_ar?: string | null
    description: string
    description_ar?: string | null
    role?: string | null
    role_ar?: string | null
    difficulty: string
    duration_hours?: number[] | null
    track: LabTrackRef
  }
  status: 'in_progress' | 'ready' | 'completed'
  completed_tasks: number
  total_tasks: number
  percent: number
  completed_at: string | null
  submitted_at: string | null
  milestones: { slug: string; title: string; title_ar?: string | null; completed: boolean; completed_tasks: number; total_tasks: number }[]
  skills: LabHint[]
  deliverables: LabHint[]
  artifacts: { path: string; kind: 'report' | 'chart' | 'analysis' | 'sql' | 'notes'; media_type: string; size: number; updated_at: string | null }[]
}
