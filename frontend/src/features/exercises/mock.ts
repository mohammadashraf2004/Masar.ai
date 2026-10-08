import type { ExerciseFile, GradeResult, TestResult } from '@/types'

const wait = () => new Promise(resolve => setTimeout(resolve, 450))

function source(files: ExerciseFile[]) {
  return files.find(file => file.name === 'agent.py')?.content ?? files.find(file => !file.readOnly)?.content ?? ''
}

function balanced(code: string): boolean {
  const pairs: Record<string, string> = { ')': '(', ']': '[', '}': '{' }
  const stack: string[] = []
  for (const character of code) {
    if ('([{'.includes(character)) stack.push(character)
    if (character in pairs && stack.pop() !== pairs[character]) return false
  }
  return stack.length === 0
}

export async function mockRunExerciseTests(_id: string | number, files: ExerciseFile[]): Promise<TestResult[]> {
  await wait()
  const code = source(files)
  const isMemoryLesson = files.some(file => file.content.includes('MemorySaver'))
  if (!isMemoryLesson) {
    const executableLines = code.split('\n').filter(line => line.trim() && !line.trim().startsWith('#'))
    return [
      { name: 'Solution contains executable code', passed: executableLines.length > 0 },
      { name: 'Starter TODOs are completed', passed: !/(?:\bTODO\b|\bNotImplementedError\b|^\s*pass\s*$)/m.test(code) },
      { name: 'Code structure is complete', passed: balanced(code) },
    ]
  }
  return [
    { name: 'Imports MemorySaver', passed: /from\s+langgraph\.checkpoint\.memory\s+import\s+MemorySaver/.test(code) },
    { name: 'Compiles with a checkpointer', passed: /compile\s*\([^)]*checkpointer\s*=/.test(code) },
    { name: 'Uses a stable thread_id', passed: /thread_id/.test(code) && /configurable/.test(code) },
  ]
}

export async function mockSubmitExercise(id: string | number, files: ExerciseFile[]): Promise<GradeResult> {
  const tests = await mockRunExerciseTests(id, files)
  const ok = tests.filter(test => test.passed).length
  const passed = ok === tests.length
  return {
    status: passed ? 'correct' : 'incorrect',
    passed,
    stdout: '', stderr: '', execution_time_ms: 0,
    tests_passed: ok, tests_total: tests.length,
    failed_test: passed ? null : tests.find(test => !test.passed)?.name,
    feedback: {
      code: passed ? 'CORRECT' : 'TEST_FAILED',
      message: passed ? 'Correct!' : 'Review the first failed requirement.',
      messages: { en: passed ? 'Correct!' : 'Review the first failed requirement.' },
    },
  }
}
