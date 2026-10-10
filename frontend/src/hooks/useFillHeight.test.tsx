import { act, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { useFillHeight } from './useFillHeight'

function Probe({ min }: { min?: number }) {
  const [probeRef, height] = useFillHeight<HTMLDivElement>({ min })
  return (
    <div data-page-scroll>
      <div ref={probeRef} data-testid="probe">{height ?? 'unmeasured'}</div>
    </div>
  )
}

/** jsdom has no layout: the element starts `top` pixels down the page. */
function startAt(top: number) {
  vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({ top } as DOMRect)
}

function resizeTo(height: number) {
  Object.defineProperty(window, 'innerHeight', { configurable: true, value: height })
}

afterEach(() => { vi.restoreAllMocks(); resizeTo(768) })

describe('useFillHeight', () => {
  it('runs from where the element starts to the bottom of the window, less the gap', async () => {
    startAt(150)
    resizeTo(900)
    await act(async () => { render(<Probe />) })
    expect(screen.getByTestId('probe')).toHaveTextContent('730')
  })

  it('grows and shrinks with the window', async () => {
    startAt(150)
    resizeTo(900)
    await act(async () => { render(<Probe />) })
    await act(async () => { resizeTo(1400); window.dispatchEvent(new Event('resize')) })
    expect(screen.getByTestId('probe')).toHaveTextContent('1230')
    await act(async () => { resizeTo(700); window.dispatchEvent(new Event('resize')) })
    expect(screen.getByTestId('probe')).toHaveTextContent('530')
  })

  it('never goes under the minimum on a very short window', async () => {
    startAt(150)
    resizeTo(500)
    await act(async () => { render(<Probe min={420} />) })
    expect(screen.getByTestId('probe')).toHaveTextContent('420')
  })
})
