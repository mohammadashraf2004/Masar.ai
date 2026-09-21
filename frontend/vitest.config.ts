import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vitest/config'

/**
 * Component and unit tests. jsdom gives a real DOM (roles, text, events) but no
 * layout engine, so anything that depends on measured layout — actual RTL
 * rendering, responsive breakpoints — is checked in a real browser instead; see
 * the note in src/test/setup.ts.
 */
export default defineConfig({
  // Next compiles JSX with its own toolchain; the tests need the automatic
  // runtime so components do not have to `import React`.
  esbuild: { jsx: 'automatic' },
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
    css: false,
    restoreMocks: true,
  },
})
