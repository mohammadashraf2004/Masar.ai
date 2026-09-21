import { readFileSync, readdirSync, statSync } from 'node:fs'
import { join, relative } from 'node:path'
import { describe, expect, it } from 'vitest'

/**
 * Static guards for the two ways a control most often ends up wrong.
 *
 * 1. Nesting. `<Link><Button/></Link>` is an <a> holding a <button>: two tab
 *    stops for one control, and a screen reader announces a button inside a
 *    link. Navigation is an <a> styled with `buttonStyles()`; an action is a
 *    <button>. Never both.
 * 2. A name. An icon-only <button> (a close "X") has no text, so without an
 *    `aria-label` a screen reader says only "button".
 *
 * jsdom cannot see either from the outside as reliably as the source can, so
 * this reads the source, the way direction-and-touch.test.ts does. The real
 * pages are checked in a browser.
 */
const SRC = join(__dirname, '..')

function sourceFiles(dir: string): string[] {
  return readdirSync(dir).flatMap((entry) => {
    const full = join(dir, entry)
    if (statSync(full).isDirectory()) return sourceFiles(full)
    return /\.tsx$/.test(entry) && !/\.test\.tsx$/.test(entry) ? [full] : []
  })
}

/** Blank comments out (same length, so line numbers survive): prose that
 *  mentions "<button>" is not markup. */
function stripComments(src: string): string {
  return src
    .replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ' '))
    .replace(/(^|[\s;{}(),])\/\/[^\n]*/g, (m, lead: string) => lead + ' '.repeat(m.length - lead.length))
}

/** Read one JSX tag starting at `i` (`src[i] === '<'`), skipping `>` inside
 *  attribute expressions such as `onClick={() => x}`. */
function readTag(src: string, i: number): { end: number; text: string; selfClosing: boolean } | null {
  let depth = 0
  let quote: string | null = null
  for (let j = i + 1; j < src.length; j++) {
    const c = src[j]
    if (quote) {
      if (c === quote && src[j - 1] !== '\\') quote = null
    } else if (depth > 0) {
      if (c === '{') depth++
      else if (c === '}') depth--
      else if (c === '"' || c === "'" || c === '`') {
        const q = c
        j++
        while (j < src.length && src[j] !== q) {
          if (src[j] === '\\') j++
          j++
        }
      }
    } else if (c === '{') depth = 1
    else if (c === '"' || c === "'") quote = c
    else if (c === '>') return { end: j + 1, text: src.slice(i, j + 1), selfClosing: src[j - 1] === '/' }
  }
  return null
}

const INTERACTIVE = new Set(['button', 'Button', 'a', 'Link', 'input', 'select', 'textarea', 'summary'])
const VOID = new Set(['input', 'img', 'br', 'hr'])

const lineOf = (src: string, index: number) => src.slice(0, index).split('\n').length

/** "<Button> inside <Link>" for every interactive element inside another. */
function nestedInteractive(source: string): string[] {
  const src = stripComments(source)
  const found: string[] = []
  const stack: { name: string; line: number }[] = []
  let i = 0
  while (i < src.length) {
    if (src[i] === '<' && i + 1 < src.length) {
      const closing = src[i + 1] === '/' ? /^<\/([A-Za-z][\w.]*)>/.exec(src.slice(i, i + 60)) : null
      if (closing) {
        const at = stack.map((s) => s.name).lastIndexOf(closing[1])
        if (at >= 0) stack.length = at
        i += closing[0].length
        continue
      }
      const prev = i > 0 ? src[i - 1] : ' '
      if (/[A-Za-z]/.test(src[i + 1]) && !/[\w]/.test(prev)) {
        const tag = readTag(src, i)
        if (tag) {
          const name = /^<([A-Za-z][\w.]*)/.exec(tag.text)![1]
          const line = lineOf(src, i)
          if (INTERACTIVE.has(name)) {
            const parent = stack.find((s) => INTERACTIVE.has(s.name))
            if (parent) found.push(`line ${line}: <${name}> inside <${parent.name}> (opened on line ${parent.line})`)
          }
          if (!tag.selfClosing && !VOID.has(name)) stack.push({ name, line })
          i = tag.end
          continue
        }
      }
    }
    i++
  }
  return found
}

/** Icon-only buttons that carry no accessible name. */
function unnamedIconButtons(source: string): string[] {
  const src = stripComments(source)
  const icons = new Set<string>()
  for (const m of Array.from(src.matchAll(/import\s*\{([^}]*)\}\s*from\s*['"]lucide-react['"]/g))) {
    m[1].split(',').forEach((n) => icons.add(n.trim().split(/\s+as\s+/).pop()!))
  }
  const found: string[] = []
  for (const m of Array.from(src.matchAll(/<(button|Button)\b/g))) {
    const tag = readTag(src, m.index!)
    if (!tag || tag.selfClosing) continue
    const close = src.indexOf(`</${m[1]}>`, tag.end)
    if (close < 0) continue
    const inner = src.slice(tag.end, close).trim()
    const only = /^<([A-Z][A-Za-z0-9]*)\b[^>]*\/>$/.exec(inner)
    if (only && icons.has(only[1]) && !/aria-label(ledby)?=/.test(tag.text)) {
      found.push(`line ${lineOf(src, m.index!)}: icon-only <${m[1]}> (${only[1]}) has no aria-label`)
    }
  }
  return found
}

const FILES = sourceFiles(SRC)
const rel = (f: string) => relative(SRC, f).replace(/\\/g, '/')

describe('the guards themselves', () => {
  it('scan the whole app, not nothing', () => {
    const names = FILES.map(rel)
    expect(names.length).toBeGreaterThan(60)
    expect(names).toEqual(expect.arrayContaining([
      'app/page.tsx', 'app/dashboard/page.tsx', 'app/tracks/page.tsx', 'app/exam/[examId]/page.tsx',
      'components/ui/Button.tsx', 'components/ui/Modal.tsx', 'components/layout/AppShell.tsx',
    ]))
  })

  it('see a button inside a link, however it is written', () => {
    expect(nestedInteractive(`<Link href="/x"><Button size="sm">Go</Button></Link>`)).toHaveLength(1)
    expect(nestedInteractive(`<Link href="/x">\n  <Button onClick={() => go()}>Go</Button>\n</Link>`)).toHaveLength(1)
    expect(nestedInteractive(`<a href="/x"><button type="button">Go</button></a>`)).toHaveLength(1)
    expect(nestedInteractive(`<button onClick={f}><a href="/x">Go</a></button>`)).toHaveLength(1)
  })

  it('accept the two correct shapes, and prose that only mentions the tags', () => {
    expect(nestedInteractive(`<Link href="/x" className={buttonStyles()}>Go</Link>`)).toEqual([])
    expect(nestedInteractive(`<Button onClick={f}>Go</Button>`)).toEqual([])
    expect(nestedInteractive(`{/* an <a> around a <button> is wrong */}\n<Link href="/x">Go</Link>`)).toEqual([])
    expect(nestedInteractive(`// <Link><Button/></Link>\n<Link href="/x">Go</Link>`)).toEqual([])
  })

  it('see an icon-only button with no name, and accept one that has it', () => {
    const head = `import { X } from 'lucide-react'\n`
    expect(unnamedIconButtons(head + `<button onClick={close}><X size={15} /></button>`)).toHaveLength(1)
    expect(unnamedIconButtons(head + `<button onClick={close} aria-label="Close"><X size={15} /></button>`)).toEqual([])
    // A button with text, or with a non-icon component child, is not icon-only.
    expect(unnamedIconButtons(head + `<button onClick={close}><X size={15} /> Close</button>`)).toEqual([])
    expect(unnamedIconButtons(head + `<button onClick={pick}><LearningLabel parts={p} /></button>`)).toEqual([])
  })
})

describe('interactive semantics across the app', () => {
  it('never puts one interactive element inside another', () => {
    const offenders = FILES.flatMap((f) => nestedInteractive(readFileSync(f, 'utf8')).map((m) => `${rel(f)} ${m}`))
    expect(offenders).toEqual([])
  })

  it('leaves the shared 2px keyboard focus ring alone (globals.css) instead of thinning it per component', () => {
    // A `focus-visible:outline-1` override turns the ring into a 1px line that all but
    // vanishes on the dark panels; that is why the global rule is a solid 2px.
    const offenders = FILES.filter((f) => /focus(-visible)?:outline-(1|0)/.test(stripComments(readFileSync(f, 'utf8')))).map(rel)
    expect(offenders).toEqual([])
  })

  it('gives every icon-only button an accessible name', () => {
    const offenders = FILES.flatMap((f) => unnamedIconButtons(readFileSync(f, 'utf8')).map((m) => `${rel(f)} ${m}`))
    expect(offenders).toEqual([])
  })
})
