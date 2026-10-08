import { describe, expect, it } from 'vitest'
import { highlightedCode, highlightedPython } from './codeCellTheme'

describe('highlightedPython', () => {
  it('preserves one rendered row per source row', () => {
    const source = 'first = 1\nsecond = 2\n'
    const html = highlightedPython(source, new Set([1, 3]))

    // The editor is an exact overlay: source newlines alone define its rows.
    expect(html.split('\n')).toHaveLength(source.split('\n').length)
    expect(html).not.toMatch(/display\s*:\s*(?:block|inline-block)/i)
    expect(html).not.toContain('code-cell-line\"')

    const rendered = document.createElement('div')
    rendered.innerHTML = html
    expect(rendered.textContent).toBe(source)
  })

  it('escapes non-Python configuration text while preserving its rows', () => {
    const source = 'command: "value < other & next"\n'
    const html = highlightedCode(source, 'dockerfile', new Set())
    const rendered = document.createElement('div')
    rendered.innerHTML = html
    expect(rendered.textContent).toBe(source)
    expect(html.split('\n')).toHaveLength(source.split('\n').length)
  })
})
