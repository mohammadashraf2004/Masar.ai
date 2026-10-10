import type { Exercise, ExerciseFile } from '@/types'

/** The editor file an exercise of each language is written in (and its draft is saved under). */
export const EXERCISE_FILE_NAMES: Record<string, string> = {
  bash: 'solution.sh',
  dockerfile: 'Dockerfile',
  hcl: 'main.tf',
  ini: 'openssl.cnf',
  python: 'agent.py',
  sparql: 'query.sparql',
  sql: 'query.sql',
  yaml: 'solution.yaml',
}

export function exerciseFileName(language?: string | null): string {
  return EXERCISE_FILE_NAMES[language ?? 'python'] ?? 'solution.txt'
}

const TITLE_STOPWORDS = new Set([
  'a', 'an', 'the', 'and', 'or', 'of', 'to', 'for', 'with', 'in', 'on', 'at', 'by', 'from', 'into',
  'your', 'its', 'using', 'use', 'vs', 'versus', 'against', 'so', 'that', 'it', 'is', 'are', 'as', 'how',
  'correctly', 'simple', 'basic', 'one', 'two', 'three',
])

/** A short Python file name from the exercise's English title
 *  ("Scale Training and Test Data Correctly" -> `scale_training_test.py`).
 *  Only a label: drafts stay keyed by the language's storage name. */
export function pythonFileLabel(title: string): string {
  const words = title.toLowerCase().split(/[^a-z0-9]+/).filter(word => word && !TITLE_STOPWORDS.has(word))
  const stem = words.slice(0, 3).join('_').replace(/^(\d)/, '_$1')
  return stem ? `${stem}.py` : 'main.py'
}

export function exerciseFiles(exercise: Exercise): ExerciseFile[] {
  const name = exerciseFileName(exercise.language)
  const label = (exercise.language ?? 'python') === 'python' ? pythonFileLabel(exercise.title) : undefined
  return [
    { name, label, content: exercise.starter_code ?? '# Write your solution here\n' },
  ]
}

export function memorySaverImportLine(files: ExerciseFile[]): number[] {
  const agent = files.find(file => file.name.endsWith('.py'))
  const index = agent?.content.split('\n').findIndex(line => line.includes('MemorySaver')) ?? -1
  return index >= 0 ? [index + 1] : []
}
