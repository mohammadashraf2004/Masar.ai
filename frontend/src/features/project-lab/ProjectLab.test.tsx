import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useLanguageStore } from '@/lib/language'
import { useAuthStore } from '@/lib/store'
import { useAuthPrompt } from '@/components/auth/AuthPrompt'
import { router } from '@/test/nav'
import { LabProjectsSection } from './LabProjectsSection'
import { ProjectLab } from './ProjectLab'
import { ProjectLabPage, ProjectWorkspacePage } from './ProjectLabPage'
import { LAB_STRINGS } from './strings'
import type {
  LabArtifact, LabAttempt, LabCheckResult, LabCompletion, LabFile, LabProgress, LabProjectCard, LabProjectDetail, LabRunResult,
  LabSubmission, LabWorkspace,
} from './types'

vi.mock('@/lib/api', () => ({
  api: {
    getLabProjects: vi.fn(), getLabProject: vi.fn(), startLabProject: vi.fn(), getLabAttempt: vi.fn(),
    getLabWorkspace: vi.fn(), getLabFile: vi.fn(), saveLabFile: vi.fn(), resetLabFile: vi.fn(),
    runLabFile: vi.fn(), checkLabTask: vi.fn(), getLabArtifacts: vi.fn(), getLabArtifact: vi.fn(),
    getLabSubmission: vi.fn(), submitLabProject: vi.fn(), getLabCompletion: vi.fn(),
  },
}))
import { api } from '@/lib/api'
const mocked = vi.mocked(api)

const CARD: LabProjectCard = {
  slug: 'masar-commerce-analysis',
  title: 'Masar Commerce — Business Performance Analysis',
  title_ar: 'مسار كوميرس — تحليل أداء الأعمال',
  summary: 'Analyse a year of orders.', summary_ar: 'حلّل طلبات عام كامل.',
  difficulty: 'beginner', estimated_hours: 2,
  track: { slug: 'data-analyst', title: 'Data Analyst', title_ar: 'محلل بيانات' },
  milestone_count: 3, task_count: 3, attempt: null,
}

function progress(done: string[] = []): LabProgress {
  const slugs = [['introduction', 'state-the-objective'], ['inspect-the-data', 'profile-the-tables'], ['basic-kpis', 'headline-kpis']]
  return {
    status: done.length === 3 ? 'completed' : 'active',
    completed_tasks: done.length, total_tasks: 3, percent: Math.round((100 * done.length) / 3),
    current_task: slugs.map(s => s[1]).find(s => !done.includes(s)) ?? null,
    milestones: slugs.map(([m, task]) => ({ slug: m, completed_tasks: done.includes(task) ? 1 : 0, total_tasks: 1, percent: done.includes(task) ? 100 : 0 })),
    tasks: slugs.map(([m, task]) => ({
      slug: task, milestone: m, status: done.includes(task) ? 'completed' : 'not_started',
      check_count: done.includes(task) ? 1 : 0, last_outcome: done.includes(task) ? 'pass' : null, completed_at: null,
    })),
  }
}

const ATTEMPT: LabAttempt = {
  id: 41, status: 'active', started_at: '2026-10-06T10:00:00Z', project: { ...CARD, attempt: null },
  workspace_root: 'masar-commerce-analysis', progress: progress(),
  milestones: [
    { slug: 'introduction', title: 'Project Introduction', title_ar: 'مقدمة المشروع', tasks: [
      { slug: 'state-the-objective', title: 'State the objective', title_ar: 'حدّد هدف التحليل',
        instructions: 'Open **report.md**.', instructions_ar: 'افتح **report.md**.', hints: [], primary_file: 'report.md' },
    ] },
    { slug: 'inspect-the-data', title: 'Inspect the Data', title_ar: 'افحص البيانات', tasks: [
      { slug: 'profile-the-tables', title: 'Profile the tables', title_ar: 'استكشف الجداول',
        instructions: 'Set `row_counts`.', instructions_ar: 'اجعل `row_counts`.', hints: [{ en: 'Use len(df).', ar: 'استخدم len(df).' }],
        primary_file: 'analysis/inspect_data.py' },
    ] },
    { slug: 'basic-kpis', title: 'Calculate Basic KPIs', title_ar: 'احسب المؤشرات الأساسية', tasks: [
      { slug: 'headline-kpis', title: 'Headline KPIs', title_ar: 'المؤشرات الرئيسية',
        instructions: 'Fill in `kpis`.', instructions_ar: 'املأ `kpis`.', hints: [], primary_file: 'analysis/kpis.py' },
    ] },
  ],
}

const WORKSPACE: LabWorkspace = {
  root: 'masar-commerce-analysis',
  entries: [
    { path: 'README.md', kind: 'file', language: 'markdown', editable: false, size: 10, modified: false },
    { path: 'analysis', kind: 'dir', language: null, editable: false, size: null, modified: false },
    { path: 'analysis/inspect_data.py', kind: 'file', language: 'python', editable: true, size: 10, modified: false },
    { path: 'analysis/kpis.py', kind: 'file', language: 'python', editable: true, size: 10, modified: false },
    { path: 'charts', kind: 'dir', language: null, editable: false, size: null, modified: false },
    { path: 'data', kind: 'dir', language: null, editable: false, size: null, modified: false },
    { path: 'data/orders.csv', kind: 'file', language: 'csv', editable: false, size: 100, modified: false },
    { path: 'report.md', kind: 'file', language: 'markdown', editable: true, size: 10, modified: false },
    { path: 'sql', kind: 'dir', language: null, editable: false, size: null, modified: false },
    { path: 'sql/revenue_by_category.sql', kind: 'file', language: 'sql', editable: true, size: 10, modified: false },
  ],
}

const FILES: Record<string, LabFile> = {
  'report.md': { path: 'report.md', language: 'markdown', editable: true, content: '## Objective\n', table: null },
  'analysis/kpis.py': { path: 'analysis/kpis.py', language: 'python', editable: true, content: 'kpis = {}\n', table: null },
  'analysis/inspect_data.py': { path: 'analysis/inspect_data.py', language: 'python', editable: true, content: 'row_counts = {}\n', table: null },
  'data/orders.csv': {
    path: 'data/orders.csv', language: 'csv', editable: false, content: null,
    table: { columns: ['order_id', 'status'], rows: [['O00001', 'pending'], ['O00002', 'completed']], row_count: 2600, truncated: true },
  },
}

const RUN_OK: LabRunResult = {
  path: 'analysis/kpis.py', kind: 'python', status: 'success', stdout: "revenue: 6621483.5\n", stderr: '',
  execution_ms: 812, generated_files: [], table: null, error: null,
}

function check(outcome: LabCheckResult['outcome'], extra: Partial<LabCheckResult> = {}): LabCheckResult {
  return {
    task: 'state-the-objective', outcome, passed: outcome === 'pass', checks: [], error: null, run: null,
    newly_completed: outcome === 'pass', task_status: outcome === 'pass' ? 'completed' : 'in_progress',
    progress: progress(outcome === 'pass' ? ['state-the-objective'] : []), ...extra,
  }
}

beforeEach(() => {
  vi.clearAllMocks()
  // A signed-in learner; the signed-out overview is asserted on its own below.
  useAuthStore.setState({ token: 'tok', _hasHydrated: true })
  useAuthPrompt.setState({ open: false, next: null })
  mocked.getLabProjects.mockResolvedValue([CARD])
  mocked.getLabAttempt.mockResolvedValue(ATTEMPT)
  mocked.getLabWorkspace.mockResolvedValue(WORKSPACE)
  mocked.getLabFile.mockImplementation(async (_id: number, path: string) => FILES[path])
  mocked.saveLabFile.mockImplementation(async (_id: number, path: string, content: string) => ({ ...FILES[path], content }))
  mocked.getLabArtifacts.mockResolvedValue([])
})

async function renderLab() {
  render(<ProjectLab attemptId={41} />)
  return screen.findByRole('textbox', { name: /report\.md/ })
}

describe('Guided projects on the Challenges page', () => {
  it('shows the project card and opens the overview without starting anything', async () => {
    render(<LabProjectsSection />)
    const card = await screen.findByTestId('lab-project-card')
    expect(within(card).getByRole('heading', { name: CARD.title })).toBeInTheDocument()
    expect(within(card).getByText('Data Analyst')).toBeInTheDocument()
    expect(within(card).getByText(/3 milestones · 3 tasks/)).toHaveTextContent('3 milestones · 3 tasks · About 2 h')

    await userEvent.click(within(card).getByRole('button', { name: /View project/ }))
    expect(mocked.startLabProject).not.toHaveBeenCalled()
    expect(router.push).toHaveBeenCalledWith('/challenges/projects/masar-commerce-analysis')
  })

  it('continues a started project straight in the workspace', async () => {
    mocked.getLabProjects.mockResolvedValue([{ ...CARD, attempt: { id: 41, status: 'active', percent: 33, completed_tasks: 1, total_tasks: 3 } }])
    render(<LabProjectsSection />)
    const card = await screen.findByTestId('lab-project-card')
    expect(within(card).getByText('1 of 3 tasks complete')).toBeInTheDocument()
    await userEvent.click(within(card).getByRole('button', { name: /Continue project/ }))
    expect(mocked.startLabProject).not.toHaveBeenCalled()
    expect(router.push).toHaveBeenCalledWith('/challenges/projects/masar-commerce-analysis/workspace')
  })

  it('offers a submitted project as completed', async () => {
    mocked.getLabProjects.mockResolvedValue([{ ...CARD, attempt: { id: 41, status: 'completed', percent: 100, completed_tasks: 3, total_tasks: 3, submitted_at: '2026-10-06T12:00:00Z' } }])
    render(<LabProjectsSection />)
    const card = await screen.findByTestId('lab-project-card')
    await userEvent.click(within(card).getByRole('button', { name: /View Completed Project/ }))
    expect(router.push).toHaveBeenCalledWith('/challenges/projects/masar-commerce-analysis')
  })

  it('renders the card in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<LabProjectsSection />)
    const card = await screen.findByTestId('lab-project-card')
    expect(within(card).getByRole('heading', { name: 'مسار كوميرس — تحليل أداء الأعمال' })).toBeInTheDocument()
    expect(within(card).getByText('محلل بيانات')).toBeInTheDocument()
    expect(within(card).getByRole('button', { name: /اعرض المشروع/ })).toBeInTheDocument()
  })

  it('stays out of the way when there are no projects or the request fails', async () => {
    mocked.getLabProjects.mockRejectedValue(new Error('offline'))
    const { container } = render(<LabProjectsSection />)
    await act(async () => {})
    expect(container).toBeEmptyDOMElement()
  })
})

const DETAIL: LabProjectDetail = {
  ...CARD, difficulty: 'intermediate', milestones: ATTEMPT.milestones,
  overview: {
    role: 'Junior Data Analyst', role_ar: 'محلل بيانات مبتدئ',
    scenario: 'You have just joined Masar Commerce.', scenario_ar: 'انضممت للتو إلى مسار كوميرس.',
    duration_hours: [12, 18],
    skills: [{ en: 'SQL', ar: 'SQL' }, { en: 'Data Cleaning', ar: 'تنظيف البيانات' }],
    deliverables: [{ en: 'A final executive report', ar: 'تقرير تنفيذي نهائي' }],
  },
}

const COMPLETION: LabCompletion = {
  schema_version: 1,
  project: { slug: CARD.slug, title: CARD.title, title_ar: CARD.title_ar, description: CARD.summary, role: 'Junior Data Analyst',
    role_ar: 'محلل بيانات مبتدئ', difficulty: 'intermediate', duration_hours: [12, 18], track: CARD.track },
  status: 'completed', completed_tasks: 3, total_tasks: 3, percent: 100,
  completed_at: '2026-10-06T11:00:00Z', submitted_at: '2026-10-06T12:00:00Z',
  milestones: ATTEMPT.milestones.map(m => ({ slug: m.slug, title: m.title, title_ar: m.title_ar, completed: true, completed_tasks: 1, total_tasks: 1 })),
  skills: [{ en: 'SQL Business Analysis', ar: 'تحليل الأعمال باستخدام SQL' }],
  deliverables: DETAIL.overview.deliverables,
  artifacts: [
    { path: 'report.md', kind: 'report', media_type: 'text/plain', size: 900, updated_at: null },
    { path: 'charts/monthly_revenue.png', kind: 'chart', media_type: 'image/png', size: 4000, updated_at: null },
    { path: 'analysis/kpis.py', kind: 'analysis', media_type: 'text/plain', size: 300, updated_at: null },
  ],
}

describe('Project overview', () => {
  it('shows the capstone before starting, then starts it and opens the workspace', async () => {
    mocked.getLabProject.mockResolvedValue(DETAIL)
    mocked.startLabProject.mockResolvedValue({ attempt_id: 41, created: true })
    render(<ProjectLabPage slug="masar-commerce-analysis" />)
    const page = await screen.findByTestId('lab-overview')
    expect(within(page).getByRole('heading', { level: 1, name: CARD.title })).toBeInTheDocument()
    expect(within(page).getByText('Junior Data Analyst')).toBeInTheDocument()
    expect(within(page).getByText('Intermediate')).toBeInTheDocument()
    expect(within(page).getByText('12–18 hours')).toBeInTheDocument()
    expect(within(page).getByText('You have just joined Masar Commerce.')).toBeInTheDocument()
    expect(within(page).getByText('A final executive report')).toBeInTheDocument()
    expect(within(page).getByText('Data Cleaning')).toBeInTheDocument()
    expect(within(page).getByText('Run SQL on the company data')).toBeInTheDocument()
    const structure = within(page).getByRole('heading', { name: 'Project structure' }).closest('section') as HTMLElement
    expect(within(structure).getAllByRole('listitem')).toHaveLength(3)
    expect(page.textContent).not.toMatch(/validator|masar_commerce\./)
    await userEvent.click(within(page).getByRole('button', { name: 'Start Project' }))
    expect(mocked.startLabProject).toHaveBeenCalledWith('masar-commerce-analysis')
    await waitFor(() => expect(router.push).toHaveBeenCalledWith('/challenges/projects/masar-commerce-analysis/workspace'))
  })

  it('signed out, the overview is readable and Start asks them to sign in first', async () => {
    useAuthStore.setState({ token: null })
    mocked.getLabProject.mockResolvedValue(DETAIL)
    render(<ProjectLabPage slug="masar-commerce-analysis" />)
    const page = await screen.findByTestId('lab-overview')
    expect(within(page).getByText('Junior Data Analyst')).toBeInTheDocument()
    await userEvent.click(within(page).getByRole('button', { name: 'Sign in to start this project' }))
    expect(mocked.startLabProject).not.toHaveBeenCalled()
    expect(useAuthPrompt.getState()).toMatchObject({ open: true, next: '/challenges/projects/masar-commerce-analysis' })
  })

  it('offers Continue Project for a learner who has started', async () => {
    mocked.getLabProject.mockResolvedValue({ ...DETAIL, attempt: { id: 41, status: 'active', percent: 33, completed_tasks: 1, total_tasks: 3 } })
    render(<ProjectLabPage slug="masar-commerce-analysis" />)
    const link = await screen.findByRole('link', { name: 'Continue Project' })
    expect(link).toHaveAttribute('href', '/challenges/projects/masar-commerce-analysis/workspace')
    expect(screen.getByText('1 of 3 tasks')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Start Project' })).toBeNull()
  })

  it('shows the Project Completed summary for a submitted project', async () => {
    mocked.getLabProject.mockResolvedValue({ ...DETAIL, attempt: { id: 41, status: 'completed', percent: 100, completed_tasks: 3, total_tasks: 3, submitted_at: '2026-10-06T12:00:00Z' } })
    mocked.getLabCompletion.mockResolvedValue(COMPLETION)
    render(<ProjectLabPage slug="masar-commerce-analysis" />)
    const summary = await screen.findByTestId('lab-completion')
    expect(mocked.getLabCompletion).toHaveBeenCalledWith(41)
    expect(within(summary).getByText('Project Completed')).toBeInTheDocument()
    expect(within(summary).getByText(/3 \/ 3 tasks completed/)).toBeInTheDocument()
    expect(within(summary).getByText('SQL Business Analysis')).toBeInTheDocument()
    for (const path of ['report.md', 'charts/monthly_revenue.png', 'analysis/kpis.py']) {
      expect(within(summary).getByText(path)).toBeInTheDocument()
    }
    expect(within(summary).getByRole('link', { name: 'View Completed Project' }))
      .toHaveAttribute('href', '/challenges/projects/masar-commerce-analysis/workspace')
  })

  it('renders the overview and the completion summary in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar' })
    mocked.getLabProject.mockResolvedValue({ ...DETAIL, attempt: { id: 41, status: 'completed', percent: 100, completed_tasks: 3, total_tasks: 3, submitted_at: '2026-10-06T12:00:00Z' } })
    mocked.getLabCompletion.mockResolvedValue(COMPLETION)
    render(<ProjectLabPage slug="masar-commerce-analysis" />)
    const summary = await screen.findByTestId('lab-completion')
    expect(within(summary).getByText('اكتمل المشروع')).toBeInTheDocument()
    expect(within(summary).getByText('تحليل الأعمال باستخدام SQL')).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 1, name: CARD.title_ar as string })).toBeInTheDocument()
    expect(screen.getByText('انضممت للتو إلى مسار كوميرس.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'اعرض المشروع المكتمل' })).toBeInTheDocument()
  })

  it('sends a learner without an attempt from the workspace back to the overview', async () => {
    mocked.getLabProject.mockResolvedValue(DETAIL)
    render(<ProjectWorkspacePage slug="masar-commerce-analysis" />)
    await waitFor(() => expect(router.replace).toHaveBeenCalledWith('/challenges/projects/masar-commerce-analysis'))
    expect(mocked.getLabAttempt).not.toHaveBeenCalled()
  })

  it('opens the lab in the workspace for a started project, with a way back to the overview', async () => {
    mocked.getLabProject.mockResolvedValue({ ...DETAIL, attempt: { id: 41, status: 'active', percent: 0, completed_tasks: 0, total_tasks: 3 } })
    render(<ProjectWorkspacePage slug="masar-commerce-analysis" />)
    expect(await screen.findByRole('textbox', { name: /report\.md/ })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Project overview/ })).toHaveAttribute('href', '/challenges/projects/masar-commerce-analysis')
  })
})

describe('Project lab', () => {
  it('renders the task, progress, file tree and the current task file', async () => {
    const editor = await renderLab()
    expect(screen.getByRole('heading', { level: 1, name: CARD.title })).toBeInTheDocument()
    expect(screen.getByTestId('lab-progress')).toHaveTextContent('0 of 3 tasks')
    expect(screen.getByRole('heading', { level: 2, name: 'State the objective' })).toBeInTheDocument()
    const files = screen.getByRole('navigation', { name: 'Files' })
    for (const name of ['kpis.py', 'orders.csv', 'revenue_by_category.sql', 'README.md']) {
      expect(within(files).getByRole('button', { name: new RegExp(name.replace('.', '\\.')) })).toBeInTheDocument()
    }
    expect(editor).toHaveValue('## Objective\n')
    expect(mocked.getLabFile).toHaveBeenCalledWith(41, 'report.md')
  })

  it('opens a file chosen in the tree', async () => {
    await renderLab()
    await userEvent.click(within(screen.getByRole('navigation', { name: 'Files' })).getByRole('button', { name: /kpis\.py/ }))
    expect(await screen.findByRole('textbox', { name: /analysis\/kpis\.py/ })).toHaveValue('kpis = {}\n')
    expect(screen.getByRole('button', { name: 'Run' })).toBeInTheDocument()
  })

  it('shows a dataset as a read-only table with no edit actions', async () => {
    await renderLab()
    const datasetButton = within(screen.getByRole('navigation', { name: 'Files' })).getByRole('button', { name: /orders\.csv/ })
    expect(within(datasetButton).getByLabelText('Read-only')).toBeInTheDocument()
    await userEvent.click(datasetButton)
    const table = await screen.findByRole('table', { name: 'data/orders.csv' })
    expect(within(table).getByRole('columnheader', { name: 'status' })).toBeInTheDocument()
    expect(screen.getByText('Showing 2 of 2600 rows')).toBeInTheDocument()
    expect(screen.queryByRole('textbox')).toBeNull()
    for (const name of ['Run', 'Save', 'Reset File']) expect(screen.queryByRole('button', { name })).toBeNull()
  })

  it('tracks edits and saves them', async () => {
    const editor = await renderLab()
    expect(screen.getByText('Saved')).toBeInTheDocument()
    fireEvent.change(editor, { target: { value: '## Objective\nMy goal.\n' } })
    expect(screen.getByText('Unsaved changes')).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: 'Save' }))
    expect(mocked.saveLabFile).toHaveBeenCalledWith(41, 'report.md', '## Objective\nMy goal.\n')
    await waitFor(() => expect(screen.getByText('Saved')).toBeInTheDocument())
  })

  it('saves before running and shows the run output', async () => {
    let resolveRun: (value: LabRunResult) => void = () => {}
    mocked.runLabFile.mockImplementation(() => new Promise(resolve => { resolveRun = resolve }))
    await renderLab()
    await userEvent.click(within(screen.getByRole('navigation', { name: 'Files' })).getByRole('button', { name: /kpis\.py/ }))
    const editor = await screen.findByRole('textbox', { name: /analysis\/kpis\.py/ })
    fireEvent.change(editor, { target: { value: 'kpis = {"revenue": 1}\n' } })
    await userEvent.click(screen.getByRole('button', { name: 'Run' }))

    expect(await screen.findByRole('button', { name: /Running/ })).toBeDisabled()
    expect(mocked.saveLabFile).toHaveBeenCalledWith(41, 'analysis/kpis.py', 'kpis = {"revenue": 1}\n')
    expect(mocked.saveLabFile.mock.invocationCallOrder[0]).toBeLessThan(mocked.runLabFile.mock.invocationCallOrder[0])
    await act(async () => resolveRun(RUN_OK))
    const result = await screen.findByTestId('lab-run')
    expect(result).toHaveAttribute('data-status', 'success')
    expect(within(result).getByText('Ran successfully')).toBeInTheDocument()
    expect(within(result).getByText(/revenue: 6621483.5/)).toBeInTheDocument()
  })

  it('distinguishes a code error from a platform failure', async () => {
    mocked.runLabFile.mockResolvedValueOnce({
      ...RUN_OK, status: 'error', stdout: '', stderr: 'Traceback (most recent call last):\nKeyError: \'x\'\n',
      error: { type: 'KeyError', message: "'x'", line: 2 },
    })
    await renderLab()
    await userEvent.click(within(screen.getByRole('navigation', { name: 'Files' })).getByRole('button', { name: /kpis\.py/ }))
    await screen.findByRole('textbox', { name: /analysis\/kpis\.py/ })
    await userEvent.click(screen.getByRole('button', { name: 'Run' }))
    let result = await screen.findByTestId('lab-run')
    expect(result).toHaveAttribute('data-status', 'error')
    expect(within(result).getByText('Your code stopped with an error')).toBeInTheDocument()
    expect(within(result).getByText(/KeyError/)).toBeInTheDocument()

    mocked.runLabFile.mockResolvedValueOnce({ ...RUN_OK, status: 'infrastructure_error', stdout: '', stderr: 'The project runner is busy.' })
    await userEvent.click(screen.getByRole('button', { name: 'Run' }))
    await waitFor(() => expect(screen.getByTestId('lab-run')).toHaveAttribute('data-status', 'infrastructure_error'))
    result = screen.getByTestId('lab-run')
    expect(within(result).getByText(/this is not a problem with your code/)).toBeInTheDocument()
  })

  it('shows a passing check and updates progress', async () => {
    mocked.checkLabTask.mockResolvedValue(check('pass', {
      checks: [{ id: 'section_written', passed: true, label: 'Written in your own words', labels: null, message: null, messages: null }],
    }))
    await renderLab()
    await userEvent.click(screen.getByRole('button', { name: 'Check Step' }))
    expect(mocked.checkLabTask).toHaveBeenCalledWith(41, 'state-the-objective')
    const result = await screen.findByTestId('lab-check')
    expect(result).toHaveAttribute('data-outcome', 'pass')
    expect(within(result).getByText('Step complete')).toBeInTheDocument()
    expect(within(result).getByText('Written in your own words')).toBeInTheDocument()
    expect(screen.getByTestId('lab-progress')).toHaveTextContent('1 of 3 tasks')
    expect(screen.getByRole('button', { name: /State the objective/ })).toContainElement(screen.getAllByRole('img', { name: 'Completed' })[0])
  })

  it('shows a check waiting on the ones above as pending, not failed', async () => {
    mocked.checkLabTask.mockResolvedValue(check('fail', {
      checks: [
        { id: 'revenue', passed: false, label: 'Revenue', labels: null, message: 'Use completed orders only.', messages: null },
        { id: 'computed_from_data', passed: false, pending: true, label: 'Calculated from the data', labels: null,
          message: 'This check runs once the checks above pass.', messages: null },
      ],
    }))
    await renderLab()
    await userEvent.click(screen.getByRole('button', { name: 'Check Step' }))
    const result = await screen.findByTestId('lab-check')
    expect(within(result).getByText('Not yet — 0 of 1 checks pass')).toBeInTheDocument()
    expect(within(result).getByRole('img', { name: 'Waiting for the checks above' })).toBeInTheDocument()
    expect(within(result).getAllByRole('img', { name: 'Not yet' })).toHaveLength(1)
  })

  it('shows a failing check with what to reconsider', async () => {
    mocked.checkLabTask.mockResolvedValue(check('fail', {
      task: 'headline-kpis',
      checks: [
        { id: 'kpis_defined', passed: true, label: 'kpis has the four keys', labels: null, message: null, messages: null },
        { id: 'aov', passed: false, label: 'Average order value', labels: null,
          message: 'Check which order statuses should contribute to revenue.', messages: null },
      ],
    }))
    await renderLab()
    await userEvent.click(screen.getByRole('button', { name: /Calculate Basic KPIs/ }))
    await userEvent.click(screen.getByRole('button', { name: /Headline KPIs/ }))
    await userEvent.click(screen.getByRole('button', { name: 'Check Step' }))
    expect(mocked.checkLabTask).toHaveBeenCalledWith(41, 'headline-kpis')
    const result = await screen.findByTestId('lab-check')
    expect(result).toHaveAttribute('data-outcome', 'fail')
    expect(within(result).getByText('Not yet — 1 of 2 checks pass')).toBeInTheDocument()
    expect(within(result).getByText('Check which order statuses should contribute to revenue.')).toBeInTheDocument()
    expect(screen.getByTestId('lab-progress')).toHaveTextContent('0 of 3 tasks')
  })

  it('shows an execution error from Check Step with the traceback', async () => {
    mocked.checkLabTask.mockResolvedValue(check('error', {
      error: { kind: 'execution', message: 'analysis/kpis.py stopped with an error.', messages: { en: 'analysis/kpis.py stopped with an error.', ar: 'توقف analysis/kpis.py بخطأ.' } },
      run: { status: 'error', stdout: '', stderr: 'ZeroDivisionError: division by zero' },
    }))
    await renderLab()
    await userEvent.click(screen.getByRole('button', { name: 'Check Step' }))
    const result = await screen.findByTestId('lab-check')
    expect(result).toHaveAttribute('data-outcome', 'error')
    expect(within(result).getByText('Your file could not run')).toBeInTheDocument()
    expect(within(result).getByText(/ZeroDivisionError/)).toBeInTheDocument()
  })

  it('asks before resetting a file, and resets only that file', async () => {
    mocked.resetLabFile.mockResolvedValue(FILES['report.md'])
    const editor = await renderLab()
    fireEvent.change(editor, { target: { value: 'my work' } })
    await userEvent.click(screen.getByRole('button', { name: 'Reset File' }))
    const dialog = await screen.findByRole('dialog', { name: 'Reset report.md?' })
    expect(within(dialog).getByRole('button', { name: 'Cancel' })).toHaveFocus()
    await userEvent.click(within(dialog).getByRole('button', { name: 'Cancel' }))
    expect(mocked.resetLabFile).not.toHaveBeenCalled()
    expect(editor).toHaveValue('my work')

    await userEvent.click(screen.getByRole('button', { name: 'Reset File' }))
    await userEvent.click(within(await screen.findByRole('dialog')).getByRole('button', { name: 'Reset file' }))
    expect(mocked.resetLabFile).toHaveBeenCalledWith(41, 'report.md')
    await waitFor(() => expect(screen.getByRole('textbox', { name: /report\.md/ })).toHaveValue('## Objective\n'))
  })

  it('reveals hints one at a time', async () => {
    await renderLab()
    await userEvent.click(screen.getByRole('button', { name: /Inspect the Data/ }))
    await userEvent.click(screen.getByRole('button', { name: /Profile the tables/ }))
    await userEvent.click(screen.getByRole('tab', { name: 'Hints' }))
    await userEvent.click(screen.getByRole('button', { name: 'Show hint 1' }))
    expect(screen.getByRole('note')).toHaveTextContent('Use len(df).')
  })

  it('collapses milestones other than the one holding the current task', async () => {
    await renderLab()
    const current = screen.getByRole('button', { name: /Project Introduction/ })
    const later = screen.getByRole('button', { name: /Calculate Basic KPIs/ })
    expect(current).toHaveAttribute('aria-expanded', 'true')
    expect(later).toHaveAttribute('aria-expanded', 'false')
    expect(later).toHaveTextContent('0/1')
    expect(screen.queryByRole('button', { name: /Headline KPIs/ })).toBeNull()
    await userEvent.click(later)
    expect(later).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('button', { name: /Headline KPIs/ })).toBeInTheDocument()
  })

  it('says when output was cut', async () => {
    mocked.runLabFile.mockResolvedValueOnce({ ...RUN_OK, stdout: 'x\n[output truncated]', stdout_truncated: true, stderr_truncated: false })
    await renderLab()
    await userEvent.click(within(screen.getByRole('navigation', { name: 'Files' })).getByRole('button', { name: /kpis\.py/ }))
    await screen.findByRole('textbox', { name: /analysis\/kpis\.py/ })
    await userEvent.click(screen.getByRole('button', { name: 'Run' }))
    const result = await screen.findByTestId('lab-run')
    expect(within(result).getByRole('note')).toHaveTextContent('Output was cut')
  })

  it('explains a refused concurrent run instead of a generic error', async () => {
    mocked.runLabFile.mockRejectedValueOnce({ response: { status: 409, data: { detail: { code: 'EXECUTION_IN_PROGRESS' } } } })
    await renderLab()
    await userEvent.click(within(screen.getByRole('navigation', { name: 'Files' })).getByRole('button', { name: /kpis\.py/ }))
    await screen.findByRole('textbox', { name: /analysis\/kpis\.py/ })
    await userEvent.click(screen.getByRole('button', { name: 'Run' }))
    expect(await screen.findByRole('alert')).toHaveTextContent(/Another Run or Check Step is still in progress/)
  })

  it('previews the report with the charts the learner generated, and never loads other images', async () => {
    const chart: LabArtifact = {
      path: 'charts/monthly_revenue.png', media_type: 'image/png', encoding: 'base64', size: 10,
      sha256: 'a'.repeat(64), updated_at: '2026-10-06T10:00:00Z',
    }
    mocked.getLabArtifacts.mockResolvedValue([chart])
    mocked.getLabArtifact.mockResolvedValue({ ...chart, content: 'iVBORw0KGgo=' })
    const original = FILES['report.md']
    FILES['report.md'] = {
      ...original,
      content: '# Regional and Time Trends\n\n![Monthly revenue](charts/monthly_revenue.png)\n\n'
        + '![Missing](charts/other.png)\n\n![Remote](https://example.com/x.png)\n',
    }
    try {
      await renderLab()
      await userEvent.click(screen.getByRole('button', { name: 'Preview' }))
      const preview = await screen.findByTestId('lab-markdown-preview')
      expect(within(preview).getByRole('heading', { name: 'Regional and Time Trends' })).toBeInTheDocument()
      const image = await within(preview).findByRole('img', { name: 'Monthly revenue' })
      expect(image).toHaveAttribute('src', 'data:image/png;base64,iVBORw0KGgo=')
      expect(within(preview).getByRole('img', { name: 'Missing' })).toHaveTextContent('charts/other.png has not been generated yet')
      expect(within(preview).getByRole('img', { name: 'Remote' })).toHaveTextContent('Only charts generated in this project')
      expect(preview.querySelector('img[src^="http"]')).toBeNull()
      expect(mocked.getLabArtifact).toHaveBeenCalledWith(41, 'charts/monthly_revenue.png')
      await userEvent.click(screen.getByRole('button', { name: 'Edit' }))
      expect(screen.getByRole('textbox', { name: /report\.md/ })).toBeInTheDocument()
    } finally {
      FILES['report.md'] = original
    }
  })

  it('offers the final submission once every task passes, then shows the summary', async () => {
    const all = ['state-the-objective', 'profile-the-tables', 'headline-kpis']
    const ready: LabSubmission = {
      submitted_at: null, ready: true, percent: 100, completed_tasks: 3, total_tasks: 3,
      milestones: ATTEMPT.milestones.map(m => ({ slug: m.slug, title: m.title, title_ar: m.title_ar, completed: true })),
      skills: [{ en: 'SQL joins and aggregation', ar: 'الربط والتجميع في SQL' }],
      artifacts: [{ path: 'charts/monthly_revenue.png', media_type: 'image/png', size: 10 }],
    }
    mocked.getLabSubmission.mockResolvedValue(ready)
    mocked.submitLabProject.mockResolvedValue({ ...ready, submitted_at: '2026-10-06T12:00:00Z' })
    mocked.checkLabTask.mockResolvedValue(check('pass', { task: 'headline-kpis', progress: progress(all) }))
    mocked.getLabAttempt.mockResolvedValue({ ...ATTEMPT, progress: progress(all.slice(0, 2)) })
    render(<ProjectLab attemptId={41} />)
    // The lab opens on the first unfinished task, and its file.
    expect(await screen.findByRole('textbox', { name: /analysis\/kpis\.py/ })).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 2, name: 'Headline KPIs' })).toBeInTheDocument()
    expect(screen.queryByTestId('lab-submission')).toBeNull()
    expect(mocked.getLabSubmission).not.toHaveBeenCalled()
    await userEvent.click(screen.getByRole('button', { name: 'Check Step' }))
    const panel = await screen.findByTestId('lab-submission')
    expect(within(panel).getByRole('heading', { name: 'Every task has passed' })).toBeInTheDocument()
    await userEvent.click(within(panel).getByRole('button', { name: 'Submit project' }))
    expect(mocked.submitLabProject).toHaveBeenCalledWith(41)
    expect(await within(panel).findByRole('heading', { name: 'Project submitted' })).toBeInTheDocument()
    expect(within(panel).getByText(/Submitted on 6 October 2026/)).toBeInTheDocument()
    expect(within(panel).getByText('Calculate Basic KPIs')).toBeInTheDocument()
    expect(within(panel).getByText('SQL joins and aggregation')).toBeInTheDocument()
    expect(within(panel).getByText('charts/monthly_revenue.png')).toBeInTheDocument()
  })

  it('shows the submission summary in Arabic for a submitted project', async () => {
    useLanguageStore.setState({ language: 'ar' })
    const all = ['state-the-objective', 'profile-the-tables', 'headline-kpis']
    mocked.getLabAttempt.mockResolvedValue({ ...ATTEMPT, status: 'completed', progress: progress(all) })
    mocked.getLabSubmission.mockResolvedValue({
      submitted_at: '2026-10-06T12:00:00Z', ready: true, percent: 100, completed_tasks: 3, total_tasks: 3,
      milestones: ATTEMPT.milestones.map(m => ({ slug: m.slug, title: m.title, title_ar: m.title_ar, completed: true })),
      skills: [{ en: 'SQL joins and aggregation', ar: 'الربط والتجميع في SQL' }], artifacts: [],
    })
    render(<ProjectLab attemptId={41} />)
    const panel = await screen.findByTestId('lab-submission')
    expect(within(panel).getByRole('heading', { name: 'تم تسليم المشروع' })).toBeInTheDocument()
    // Submitted earlier: the details stay folded until asked for.
    expect(within(panel).getByText('الربط والتجميع في SQL')).not.toBeVisible()
    await userEvent.click(within(panel).getByRole('button', { name: 'اعرض الملخص' }))
    expect(within(panel).getByText('الربط والتجميع في SQL')).toBeInTheDocument()
    expect(within(panel).getByText('احسب المؤشرات الأساسية')).toBeInTheDocument()
  })

  it('renders in Arabic, right to left, with code kept left to right', async () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<ProjectLab attemptId={41} />)
    const editor = await screen.findByRole('textbox', { name: /report\.md/ })
    expect(screen.getByRole('heading', { level: 1, name: CARD.title_ar as string })).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 2, name: 'حدّد هدف التحليل' })).toBeInTheDocument()
    for (const name of ['تشغيل', 'تحقق من الخطوة', 'إعادة الملف', 'حفظ']) {
      if (name === 'تشغيل') continue // report.md is not runnable
      expect(screen.getByRole('button', { name })).toBeInTheDocument()
    }
    expect(screen.getByTestId('lab-progress')).toHaveTextContent('المهام: ٠ من ٣')
    expect(editor.closest('[dir]')).toHaveAttribute('dir', 'ltr')
    expect(screen.getByRole('navigation', { name: 'الملفات' }).closest('[dir="rtl"]')).not.toBeNull()
  })
})

describe('Project lab strings', () => {
  it('has an Arabic string for every English one', () => {
    expect(Object.keys(LAB_STRINGS.ar).sort()).toEqual(Object.keys(LAB_STRINGS.en).sort())
    for (const value of Object.values(LAB_STRINGS.ar)) expect(value.trim()).not.toBe('')
  })
})
