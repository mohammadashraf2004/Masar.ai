export type Segment = { type: 'text'; text: string } | { type: 'code'; code: string; lang: string }

const FENCE = /```([\w+#.-]*)[^\S\n]*\n([\s\S]*?)```/g

/**
 * Splits a message the learner wrote into prose and fenced code, so the code can be drawn as a
 * code block and the prose left exactly as typed. (A mentor reply goes through a markdown
 * renderer instead; a learner's message must not, or a stray `*` or `#` would reformat it.)
 *
 * A fence that is never closed stays text.
 */
export function splitFences(text: string): Segment[] {
  const segments: Segment[] = []
  let last = 0
  for (const match of Array.from(text.matchAll(FENCE))) {
    const start = match.index ?? 0
    const before = text.slice(last, start).replace(/\n+$/, '')
    if (before.trim()) segments.push({ type: 'text', text: before })
    segments.push({ type: 'code', code: match[2].replace(/\n$/, ''), lang: match[1] })
    last = start + match[0].length
  }
  const rest = text.slice(last).replace(/^\n+/, '')
  if (rest.trim()) segments.push({ type: 'text', text: rest })
  return segments
}

/** The message that is sent: what was typed, then the attached code as a fenced block. */
export function withAttachment(text: string, code: string): string {
  const body = code.replace(/\s+$/, '')
  if (!body.trim()) return text
  const fenced = '```\n' + body + '\n```'
  return text.trim() ? `${text.trim()}\n\n${fenced}` : fenced
}
