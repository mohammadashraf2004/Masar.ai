import { readFileSync } from 'node:fs'
import { join } from 'node:path'
import { describe, expect, it } from 'vitest'

// jsdom cannot compute the cascade, so what is pinned is the rule itself. That it
// really wins over `focus:outline-none` and paints a 2px ring is checked in a real
// browser (login, register and every authenticated page's text fields).
const css = readFileSync(join(__dirname, '../app/globals.css'), 'utf8')

describe('the shared text-field focus ring', () => {
  const block = css.match(/:is\(\s*input:not\([^)]*\),\s*textarea,\s*select\s*\):focus-visible\s*\{([^}]*)\}/)

  it('exists, and covers text inputs, textareas and selects on :focus-visible', () => {
    expect(block).not.toBeNull()
  })

  // The colour is the --ring token — amber on the dark theme, a darker amber on
  // the light one (contrast.test.ts holds both to 3:1 against every surface).
  it('draws a solid 2px outline in the ring colour', () => {
    expect(block?.[1]).toMatch(/outline:\s*2px solid rgb\(var\(--ring\)\)/)
  })

  it('leaves checkboxes, radios and buttons to the general focus rule', () => {
    const excluded = css.match(/:is\(\s*input:not\(([^)]*)\)/)?.[1] ?? ''
    for (const type of ['checkbox', 'radio', 'button', 'submit', 'file', 'range']) {
      expect(excluded).toContain(`[type="${type}"]`)
    }
  })

  it('keeps the general 2px focus rule that every other control relies on', () => {
    expect(css).toMatch(/\*:focus-visible\s*\{\s*outline:\s*2px solid rgb\(var\(--ring\)\)/)
  })
})
