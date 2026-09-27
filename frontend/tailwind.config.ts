import type { Config } from 'tailwindcss'

/**
 * A colour that is a CSS variable, with Tailwind's opacity modifier still
 * working (`bg-amber/10`). The variables hold space-separated RGB channels and
 * are defined per theme in src/app/globals.css.
 */
const v = (token: string) => `rgb(var(--${token}) / <alpha-value>)`

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/features/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      // Every colour is a theme token (see the variables in globals.css), so one
      // class is dark or light with data-theme on <html>. The names are the ones
      // the code already used; the token behind each is on the right.
      colors: {
        // Surfaces
        void:    v('bg'),      // page
        ink:     v('side'),    // sidebar, menus
        surface: v('card'),    // cards, fields
        panel:   v('card2'),   // inset and active fills
        border:  v('line'),    // 1px hairlines
        // Not the handoff's "muted" (that is text, and is `dim` here): this is the
        // mid-tone the code already used for bar tracks, chip fills and hover borders.
        muted:   v('track'),
        // Text, quietest to loudest. ghost and dim are secondary text, so they
        // must clear 4.5:1 (WCAG AA) on every surface text sits on
        // (void/ink/surface/panel) in BOTH themes; see src/lib/contrast.test.ts.
        ghost:   v('faint'),
        dim:     v('mute'),
        soft:    v('soft'),
        bright:  v('text'),
        white:   v('head'),
        // Accent — amber. `amber` is for fills, borders and gradients, with
        // `on-amber` for text on top. Amber used AS TEXT is `amber-text`: it
        // darkens in the light theme, where the fill colour is under 2:1.
        // amber2 is the hover fill; amber-text2 the brighter text step.
        amber:         v('acc'),
        amber2:        v('acc-hover'),
        'amber-text':  v('acc-text'),
        'amber-text2': v('acc-text2'),
        'amber-soft':  'rgb(var(--acc) / var(--acc-soft-a))',
        'on-amber':    v('on-acc'),
        ring:          v('ring'),
        amberDim:'#92610A',
        // Status. Error text and the "advanced" badge sit on a rose/10 tint of a
        // panel; see src/lib/contrast.test.ts. `on-solid` is text on an
        // emerald/rose fill (dark on the dark theme's bright fills, white on the
        // light theme's deep ones).
        emerald: v('ok'),
        rose:    v('bad'),
        sky:     v('sky'),
        violet:  v('violet'),
        'on-solid': v('on-solid'),
        // Dimmed backdrop behind modals and the mobile menu; dark in both themes.
        scrim:   v('scrim'),
        // Certificate paper.
        cert:    v('cert'),
      },
      // The three stacks are assembled once, in globals.css (--font-body,
      // --font-display, --font-mono), so utilities and element selectors there
      // share them; each carries the Arabic fallback behind its Latin face.
      fontFamily: {
        sans:  ['var(--font-body)'],
        // The mono stack is `--font-mono` in globals.css. The note below is why
        // it is ordered the way it is.
        // 'JetBrains Mono Diagrams' goes FIRST, not after var(--font-jetbrains)
        // — its own unicode-range (see globals.css) means the browser skips
        // it instantly for every character outside that set, so it's safe
        // to lead with. It has to lead: var(--font-jetbrains) doesn't just
        // expand to JetBrains Mono, next/font/local appends its own
        // auto-generated metric-matched fallback ("jetbrainsMono Fallback",
        // local Arial, no unicode-range) right after it. Arial happens to
        // carry box-drawing glyphs too, at Arial's own width, and CSS font
        // fallback stops at the first face with ANY glyph for a character —
        // not the best-matched one — so with this face listed third, Arial
        // silently won every box-drawing/arrow character before this face
        // was ever consulted, which is exactly what the reported diagram
        // misalignment turned out to be (confirmed: the two self-hosted
        // JetBrains Mono files share identical glyph metrics — the bug was
        // never reaching them, not a metrics mismatch between them).
        mono:  ['var(--font-mono)'],
        display: ['var(--font-display)'],
      },
      // Course-content type scale. The values are CSS variables defined once
      // in globals.css (--lc-*), so the lesson body (element selectors there)
      // and the reader chrome around it (these utilities) cannot drift apart.
      fontSize: {
        'lc-title': ['var(--lc-title)', '1.3'],
        'lc-body':  ['var(--lc-body)', '1.75'],
        'lc-meta':  ['var(--lc-meta)', '1.5'],
        'lc-label': ['var(--lc-label)', '1.4'],
      },
      backgroundImage: {
        'grid-pattern': `
          linear-gradient(rgb(var(--line) / 0.6) 1px, transparent 1px),
          linear-gradient(90deg, rgb(var(--line) / 0.6) 1px, transparent 1px)
        `,
      },
      backgroundSize: {
        'grid': '40px 40px',
      },
      animation: {
        'fade-up':   'fadeUp 0.5s ease forwards',
        'fade-in':   'fadeIn 0.3s ease forwards',
        'pulse-slow':'pulse 3s ease-in-out infinite',
        'scan':      'scan 2s linear infinite',
        'glow':      'glow 2s ease-in-out infinite alternate',
        // The interviewer's halo, only while a question loads (handoff: 6px -> 18px, 1.2s).
        'masarHalo': 'masarHalo 1.2s ease-in-out infinite',
      },
      keyframes: {
        fadeUp:  { from: { opacity: '0', transform: 'translateY(16px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        fadeIn:  { from: { opacity: '0' }, to: { opacity: '1' } },
        scan:    { from: { transform: 'translateY(-100%)' }, to: { transform: 'translateY(100vh)' } },
        glow:    { from: { boxShadow: '0 0 4px #F59E0B40' }, to: { boxShadow: '0 0 16px #F59E0B80' } },
        masarHalo: {
          '0%, 100%': { boxShadow: '0 0 0 6px rgba(245,158,11,.10)' },
          '50%':      { boxShadow: '0 0 0 18px rgba(245,158,11,.22)' },
        },
      },
    },
  },
  plugins: [],
}
export default config
