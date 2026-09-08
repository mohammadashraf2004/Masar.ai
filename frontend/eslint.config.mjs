// ESLint 9 flat config.
//
// Replaces .eslintrc.json, which ESLint 9 no longer reads by default, and
// replaces `next lint`, which Next 16 removed in favour of invoking the
// ESLint CLI directly (see the "lint" script in package.json).
//
// eslint-config-next@16 ships native flat-config arrays, so these spread
// in directly — no FlatCompat shim required.
import nextCoreWebVitals from 'eslint-config-next/core-web-vitals'

export default [
  {
    ignores: [
      '.next/**',
      'node_modules/**',
      'next-env.d.ts',
      'public/**',
    ],
  },
  // Scope deliberately matches the pre-migration .eslintrc.json, which
  // extended only `next/core-web-vitals`. Adding
  // `eslint-config-next/typescript` here turns on the full
  // @typescript-eslint ruleset, which surfaces 34 pre-existing
  // `no-explicit-any` / `set-state-in-effect` findings across the app.
  // Those are worth fixing, but they are code quality rather than
  // security, and quietly widening the lint gate during a framework
  // migration would mean either a large unrelated diff or a pile of
  // suppressions. Tracked as a follow-up in GATE.md instead.
  ...nextCoreWebVitals,
  {
    rules: {
      // Surfaces every raw-HTML sink in review. There is exactly one in
      // this codebase (MarkdownLesson.tsx, Prism's own escaped output);
      // it carries an inline disable with the reasoning next to it, so a
      // NEW one shows up here rather than passing silently.
      'react/no-danger': 'warn',
      // The app is entirely App Router; this rule targets the pages/
      // directory convention and misfires here.
      '@next/next/no-html-link-for-pages': 'off',
    },
  },
]
