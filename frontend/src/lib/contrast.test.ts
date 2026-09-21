import { describe, expect, it } from 'vitest'
import config from '../../tailwind.config'

// The app is dark-only, so the palette in tailwind.config.ts is the single
// source of truth for text contrast. This pins it: `text-ghost` alone is used
// ~360 times, so a token that slips under 4.5:1 is a regression in all of them.
const colors = (config.theme?.extend?.colors ?? {}) as Record<string, string>

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

describe('text colour tokens', () => {
  it.each(TEXT.flatMap(t => SURFACES.map(s => [t, s] as const)))(
    '%s text has at least 4.5:1 on %s',
    (text, surface) => {
      expect(ratio(colors[text], colors[surface])).toBeGreaterThanOrEqual(4.5)
    },
  )

  it('keeps the hierarchy: ghost < dim < soft < bright, each a visible step on a panel', () => {
    const on = (t: string) => ratio(colors[t], colors.panel)
    expect(on('ghost')).toBeLessThan(on('dim'))
    expect(on('dim')).toBeLessThan(on('soft'))
    expect(on('soft')).toBeLessThan(on('bright'))
    // ghost must stay visibly quieter than primary text
    expect(on('bright') - on('ghost')).toBeGreaterThan(6)
  })

  // Status colours are used as text (`text-rose` errors, badges) on a 10% tint
  // of themselves laid over a surface, which is the darkest-contrast case.
  it.each(['rose', 'amber', 'emerald', 'sky'] as const)(
    '%s text has at least 4.5:1 on its own 10%% tint over a panel',
    (name) => {
      const fg = colors[name]
      const tint = blend(fg, colors.panel, 0.1)
      expect(ratio(fg, tint)).toBeGreaterThanOrEqual(4.5)
    },
  )

  it('keeps ghost readable on the border-coloured hover fill (large-text/UI minimum 3:1)', () => {
    expect(ratio(colors.ghost, colors.border)).toBeGreaterThanOrEqual(3)
  })
})
