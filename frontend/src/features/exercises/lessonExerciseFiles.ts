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

export function exerciseFiles(exercise: Exercise): ExerciseFile[] {
  const name = exerciseFileName(exercise.language)
  return [
    { name, content: exercise.starter_code ?? '# Write your solution here\n' },
  ]
}

export function memorySaverImportLine(files: ExerciseFile[]): number[] {
  const agent = files.find(file => file.name.endsWith('.py'))
  const index = agent?.content.split('\n').findIndex(line => line.includes('MemorySaver')) ?? -1
  return index >= 0 ? [index + 1] : []
}
