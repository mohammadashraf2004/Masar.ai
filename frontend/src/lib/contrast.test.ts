import { readFileSync } from 'node:fs'
import { join } from 'node:path'
import { describe, expect, it } from 'vitest'
import config from '../../tailwind.config'

// The palette is a set of CSS variables per theme in globals.css, and the Tailwind
// utility names (`text-ghost`, `bg-panel`…) are mapped onto them in
// tailwind.config.ts. This pins the result for BOTH themes: `text-ghost` alone is
// used ~360 times, so a token that slips under 4.5:1 is a regression in all of
// them, and a light theme that nobody checked is the likeliest place for one.
const css = readFileSync(join(__dirname, '../app/globals.css'), 'utf8')
const colors = (config.theme?.extend?.colors ?? {}) as Record<string, string>

type Tokens = Record<string, string>
const THEMES = {
  // `.prism-code` shares the dark block on purpose: code is always dark.
  dark: /:root,\s*\[data-theme="dark"\],\s*\.prism-code\s*\{([^}]*)\}/,
  light: /\[data-theme="light"\]\s*\{([^}]*)\}/,
} as const

/** `--name: value;` declarations of one theme block, comments removed. */
function readTokens(block: RegExp): Tokens {
  const body = css.match(block)?.[1]
  if (!body) throw new Error(`theme block not found: ${block}`)
  const tokens: Tokens = {}
  for (const m of Array.from(body.replace(/\/\*[\s\S]*?\*\//g, '').matchAll(/--([a-z0-9-]+):\s*([^;]+);/g))) {
    tokens[m[1]] = m[2].trim()
  }
  return tokens
}

const TOKENS = { dark: readTokens(THEMES.dark), light: readTokens(THEMES.light) }

/** `#rrggbb` for a variable holding `r g b` channels. */
function hexOf(theme: keyof typeof TOKENS, token: string): string {
  const raw = TOKENS[theme][token]
  const channels = raw?.match(/^(\d+)\s+(\d+)\s+(\d+)$/)
  if (!channels) throw new Error(`--${token} in the ${theme} theme is not an "r g b" triplet: ${raw}`)
  return '#' + [1, 2, 3].map(i => Number(channels[i]).toString(16).padStart(2, '0')).join('')
}

/** The theme token a Tailwind colour name is built on (`ghost` -> `faint`). */
function tokenOf(name: string): string {
  const value = colors[name]
  const token = typeof value === 'string' ? value.match(/var\(--([a-z0-9-]+)\)/)?.[1] : undefined
  if (!token) throw new Error(`tailwind colour "${name}" is not a theme token: ${value}`)
  return token
}

function luminance(hex: string): number {
  const n = hex.replace('#', '')
  const [r, g, b] = [0, 2, 4].map(i => parseInt(n.slice(i, i + 2), 16) / 255)
    .map(c => (c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)))
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

function ratio(fg: string, bg: string): number {
  const [a, b] = [luminance(fg), luminance(bg)].sort((x, y) => y - x)
  return (a + 0.05) / (b + 0.05)
}

function blend(fg: string, bg: string, alpha: number): string {
  const c = (h: string) => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16))
  const [f, b] = [c(fg), c(bg)]
  return '#' + f.map((v, i) => Math.round(v * alpha + b[i] * (1 - alpha)).toString(16).padStart(2, '0')).join('')
}

const TEXT = ['ghost', 'dim', 'soft', 'bright'] as const
// Every page/card/panel background text is set on. `border` and `muted` are
// hover/chip fills, checked separately below.
const SURFACES = ['void', 'ink', 'surface', 'panel'] as const

describe.each(['dark', 'light'] as const)('the %s theme', (theme) => {
  const hex = (name: string) => hexOf(theme, tokenOf(name))

  describe('text colour tokens', () => {
    it.each(TEXT.flatMap(t => SURFACES.map(s => [t, s] as const)))(
      '%s text has at least 4.5:1 on %s',
      (text, surface) => {
        expect(ratio(hex(text), hex(surface))).toBeGreaterThanOrEqual(4.5)
      },
    )

    it('keeps the hierarchy: ghost < dim < soft < bright, each a visible step on a panel', () => {
      const on = (t: string) => ratio(hex(t), hex('panel'))
      expect(on('ghost')).toBeLessThan(on('dim'))
      expect(on('dim')).toBeLessThan(on('soft'))
      expect(on('soft')).toBeLessThan(on('bright'))
      // ghost must stay visibly quieter than primary text
      expect(on('bright') - on('ghost')).toBeGreaterThan(6)
    })

    it.each(SURFACES)('heading text (white) has at least 7:1 on %s', (surface) => {
      expect(ratio(hex('white'), hex(surface))).toBeGreaterThanOrEqual(7)
    })

    it('keeps ghost readable on the border-coloured hover fill (large-text/UI minimum 3:1)', () => {
      expect(ratio(hex('ghost'), hex('border'))).toBeGreaterThanOrEqual(3)
    })
  })

  // Amber as TEXT is its own token (`amber-text`, and the brighter step
  // `amber-text2`), because the fill colour is under 2:1 on a light page.
  describe('amber text', () => {
    it.each((['amber-text', 'amber-text2'] as const).flatMap(t => SURFACES.map(s => [t, s] as const)))(
      '%s has at least 4.5:1 on %s',
      (text, surface) => {
        expect(ratio(hex(text), hex(surface))).toBeGreaterThanOrEqual(4.5)
      },
    )
  })

  // Status colours are used as text (`text-rose` errors, badges) on a 10% tint
  // of themselves laid over a surface, which is the darkest-contrast case. The
  // amber badge is `text-amber-text` on `bg-amber/10`, so it is that pair.
  describe('status text', () => {
    // [the text colour, the fill its 10% tint is made from]
    const cases = [
      ['rose', 'rose'], ['emerald', 'emerald'], ['sky', 'sky'], ['violet', 'violet'], ['amber-text', 'amber'],
    ] as const
    it.each(cases)('%s text has at least 4.5:1 on its own 10%% tint over a panel and a card', (text, tint) => {
      for (const surface of ['panel', 'surface'] as const) {
        const bg = blend(hex(tint), hex(surface), 0.1)
        expect(ratio(hex(text), bg), surface).toBeGreaterThanOrEqual(4.5)
      }
    })
  })

  describe('text on a solid fill', () => {
    it('on-amber on the amber fill has at least 7:1', () => {
      expect(ratio(hex('on-amber'), hex('amber'))).toBeGreaterThanOrEqual(7)
    })

    it.each(['emerald', 'rose'] as const)('on-solid on the %s fill has at least 4.5:1', (fill) => {
      expect(ratio(hex('on-solid'), hex(fill))).toBeGreaterThanOrEqual(4.5)
    })
  })

  // WCAG 1.4.11: the keyboard focus outline is a UI component and needs 3:1.
  describe('the keyboard focus ring', () => {
    it.each(SURFACES)('has at least 3:1 on %s', (surface) => {
      expect(ratio(hex('ring'), hex(surface))).toBeGreaterThanOrEqual(3)
    })
  })
})

describe('the two themes', () => {
  it('are actually different (a copied block would pass every check above)', () => {
    for (const name of ['void', 'surface', 'panel', 'bright', 'white', 'ghost']) {
      expect(hexOf('light', tokenOf(name)), name).not.toBe(hexOf('dark', tokenOf(name)))
    }
  })

  it('define the same tokens, so switching theme can never leave one undefined', () => {
    expect(Object.keys(TOKENS.light).sort()).toEqual(Object.keys(TOKENS.dark).sort())
  })

  it('back every Tailwind colour that points at a variable', () => {
    for (const [name, value] of Object.entries(colors)) {
      for (const m of Array.from(String(value).matchAll(/var\(--([a-z0-9-]+)\)/g))) {
        expect(TOKENS.dark, `${name} -> --${m[1]}`).toHaveProperty(m[1])
      }
    }
  })
})
