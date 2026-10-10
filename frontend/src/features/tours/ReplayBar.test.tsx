import { readFileSync } from 'node:fs'
import { join } from 'node:path'
import { describe, expect, it } from 'vitest'

const css = readFileSync(join(__dirname, '../../app/globals.css'), 'utf8')

describe('ReplayBar placement', () => {
  it('stays below the shell header instead of covering bottom-page composers', () => {
    const rule = css.match(/\.tour-replay\s*\{([^}]+)\}/)?.[1] ?? ''

    expect(rule).toContain('inset-block-start:')
    expect(rule).toContain('bottom: auto')
    expect(rule).not.toMatch(/bottom:\s*16px/)
  })
})
