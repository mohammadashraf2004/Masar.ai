import { afterEach, describe, expect, it, vi } from 'vitest'

/** Fresh module instance each time, so its top-level placeholder check runs again. */
async function loadRegistry() {
  vi.resetModules()
  return import('./registry')
}

describe('the TOURS_RELEASED_AT placeholder warning', () => {
  afterEach(() => {
    vi.unstubAllEnvs()
  })

  it('warns once in a dev build while the placeholder date is still set', async () => {
    vi.stubEnv('NODE_ENV', 'development')
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})

    await loadRegistry()

    expect(warn).toHaveBeenCalledTimes(1)
    expect(warn.mock.calls[0][0]).toMatch(/TOURS_RELEASED_AT/)
  })

  it('stays silent outside a dev build', async () => {
    vi.stubEnv('NODE_ENV', 'test')
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})

    await loadRegistry()

    expect(warn).not.toHaveBeenCalled()
  })

  it('stays silent in production', async () => {
    vi.stubEnv('NODE_ENV', 'production')
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})

    await loadRegistry()

    expect(warn).not.toHaveBeenCalled()
  })
})
