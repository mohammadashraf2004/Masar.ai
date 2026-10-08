import { highlight, languages } from 'prismjs/components/prism-core'
import 'prismjs/components/prism-clike'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-yaml'

export const codeCellColors = {
  background: '#0B0E14',
  chrome: '#0D1117',
  line: '#1E2535',
  text: '#C7D0DE',
  bright: '#E2E8F0',
  muted: '#5C6678',
  gutter: '#3A4456',
  amber: '#F59E0B',
} as const

export const codeEditorStyle = {
  fontFamily: 'var(--font-jetbrains), "JetBrains Mono", monospace',
  fontSize: 12.5,
  lineHeight: 1.75,
  minHeight: 190,
  minWidth: 'max-content',
  flex: '1 0 auto',
  color: codeCellColors.text,
  tabSize: 4,
} as const

/** Prism supplies token spans; this adds line highlights without changing layout.
 *
 * react-simple-code-editor overlays a transparent textarea on this HTML. The two
 * layers must therefore have identical line geometry. Making these spans block
 * elements while also retaining the source newlines creates two visual rows for
 * one source row and makes typed text appear on a neighbouring line.
 */
export function highlightedPython(code: string, highlightedLines: ReadonlySet<number>): string {
  return highlightedCode(code, 'python', highlightedLines)
}

function escapeHtml(code: string): string {
  return code.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
}

export function highlightedCode(
  code: string,
  language: string,
  highlightedLines: ReadonlySet<number>,
): string {
  const grammar = language === 'yaml' ? languages.yaml : language === 'python' ? languages.python : undefined
  const rendered = grammar ? highlight(code, grammar, language) : escapeHtml(code)
  return rendered
    .split('\n')
    .map((line, index) => {
      const highlighted = highlightedLines.has(index + 1)
      if (!highlighted) return line
      return `<span class="code-cell-line--highlighted" style="background:rgba(245,158,11,0.10);color:${codeCellColors.bright}">${line}</span>`
    })
    .join('\n')
}
