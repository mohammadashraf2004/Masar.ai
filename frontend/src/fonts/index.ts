import localFont from 'next/font/local'

/**
 * Self-hosted product typefaces.
 *
 * These were loaded from fonts.googleapis.com until the CSP was tightened,
 * at which point `style-src 'self'` silently blocked the stylesheet and
 * `font-src 'self' data:` blocked the files — every face fell back to a
 * system font in production while looking correct in dev. Shipping the files
 * ourselves removes the third-party origin instead of re-opening the policy.
 *
 * Only the subsets the product actually renders are committed: `latin` for
 * the three Latin families, `arabic` for IBM Plex Sans Arabic — which never
 * sets Latin text here, because DM Sans is ahead of it in `--font-arabic`.
 * This matches the coverage the Google stylesheet was serving for the same
 * ranges, so nothing that rendered before renders differently now.
 */

// DM Sans, Syne and JetBrains Mono are variable fonts: Google served one
// file per subset for every weight we asked for, so each is declared once
// over the range the app uses rather than once per weight.

export const dmSans = localFont({
  src: [
    { path: './dm-sans-latin.woff2', weight: '300 600', style: 'normal' },
    { path: './dm-sans-latin-italic.woff2', weight: '400', style: 'italic' },
  ],
  variable: '--font-dm-sans',
  display: 'swap',
  // Must stay off. The generated fallback is a size-adjusted local Arial,
  // and `--font-arabic` lists DM Sans ahead of Plex Arabic — Arial ships
  // Arabic glyphs on Windows and macOS, so it would win the per-glyph
  // fallback and Arabic body text would silently render in Arial.
  adjustFontFallback: false,
})

export const plexArabic = localFont({
  src: [
    { path: './plex-arabic-300.woff2', weight: '300', style: 'normal' },
    { path: './plex-arabic-400.woff2', weight: '400', style: 'normal' },
    { path: './plex-arabic-500.woff2', weight: '500', style: 'normal' },
    { path: './plex-arabic-600.woff2', weight: '600', style: 'normal' },
    { path: './plex-arabic-700.woff2', weight: '700', style: 'normal' },
  ],
  variable: '--font-plex-arabic',
  display: 'swap',
  // Five static weights, ~220KB together. Preloading all of them on every
  // page costs more than the swap it would avoid; `display: swap` already
  // matches how these faces arrived over the Google stylesheet.
  preload: false,
})

export const syne = localFont({
  src: [{ path: './syne-latin.woff2', weight: '600 800', style: 'normal' }],
  variable: '--font-syne',
  display: 'swap',
})

export const jetbrainsMono = localFont({
  src: [{ path: './jetbrains-mono-latin.woff2', weight: '400 500', style: 'normal' }],
  variable: '--font-jetbrains',
  display: 'swap',
  // Code blocks only — nothing above the fold needs it.
  preload: false,
})

/** Every font variable, for the `<html>` element in the root layout. */
export const fontVariables = [
  dmSans.variable,
  plexArabic.variable,
  syne.variable,
  jetbrainsMono.variable,
].join(' ')
