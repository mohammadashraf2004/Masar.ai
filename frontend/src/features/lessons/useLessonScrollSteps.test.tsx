import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useLessonScrollSteps } from './useLessonScrollSteps'

type Callback = (entries: Partial<IntersectionObserverEntry>[]) => void

let observedCallback: Callback | null = null
let observedOptions: IntersectionObserverInit | undefined
const disconnect = vi.fn()

beforeEach(() => {
  observedCallback = null
  observedOptions = undefined
  disconnect.mockClear()
  class FakeObserver {
    constructor(cb: Callback, options?: IntersectionObserverInit) { observedCallback = cb; observedOptions = options }
    observe = vi.fn()
    disconnect = disconnect
  }
  vi.stubGlobal('IntersectionObserver', FakeObserver)
})

function Harness({ hasExercise, onContentRead }: { hasExercise: boolean; onContentRead?: () => void }) {
  const { containerRef, dividerRef, active, scrollTo } = useLessonScrollSteps({ hasExercise, onContentRead })
  return (
    <div ref={containerRef} data-testid="container">
      <span data-testid="active">{active}</span>
      <button onClick={() => scrollTo('content')}>go-content</button>
      <button onClick={() => scrollTo('exercise')}>go-exercise</button>
      <div ref={dividerRef} data-testid="divider" />
    </div>
  )
}

describe('useLessonScrollSteps', () => {
  it('starts on the content step and does not observe when there is no exercise', () => {
    render(<Harness hasExercise={false} />)
    expect(screen.getByTestId('active')).toHaveTextContent('content')
    expect(observedCallback).toBeNull()
  })

  it('observes only a thin band at the container\'s top, not its full bounds', () => {
    // Regression guard: `threshold: 0` alone only reports enter/exit of the
    // container's FULL bounds, so once the divider is anywhere on screen it
    // stays "intersecting" for the rest of a scroll and the callback never
    // fires again as it settles near the top. `rootMargin` shrinking the
    // observed region to the top edge is what makes "intersecting" mean
    // "scrolled up near the top" and keeps firing as that band is crossed.
    render(<Harness hasExercise />)
    expect(observedOptions?.rootMargin).toBeTruthy()
    expect(observedOptions?.rootMargin).not.toBe('0px')
  })

  it('switches to the exercise step once the divider enters the top band, and fires onContentRead exactly once', () => {
    const onContentRead = vi.fn()
    render(<Harness hasExercise onContentRead={onContentRead} />)
    expect(observedCallback).not.toBeNull()

    act(() => { observedCallback?.([{ isIntersecting: true }]) })
    expect(screen.getByTestId('active')).toHaveTextContent('exercise')
    expect(onContentRead).toHaveBeenCalledTimes(1)

    // Scrolling back out of the top band, then into it again, must not re-fire the read event.
    act(() => { observedCallback?.([{ isIntersecting: false }]) })
    expect(screen.getByTestId('active')).toHaveTextContent('content')
    act(() => { observedCallback?.([{ isIntersecting: true }]) })
    expect(onContentRead).toHaveBeenCalledTimes(1)
  })

  it('the content pill scrolls the container itself to the top, not the window', async () => {
    const user = userEvent.setup()
    render(<Harness hasExercise />)
    const container = screen.getByTestId('container')
    container.scrollTo = vi.fn()

    await user.click(screen.getByText('go-content'))
    expect(container.scrollTo).toHaveBeenCalledWith({ top: 0, behavior: 'smooth' })
    expect(screen.getByTestId('active')).toHaveTextContent('content')
  })

  it('the exercise pill scrolls the container to the divider and marks content read', async () => {
    const onContentRead = vi.fn()
    const user = userEvent.setup()
    render(<Harness hasExercise onContentRead={onContentRead} />)
    const container = screen.getByTestId('container')
    const divider = screen.getByTestId('divider')
    container.scrollTo = vi.fn()
    container.getBoundingClientRect = () => ({ top: 0 } as DOMRect)
    divider.getBoundingClientRect = () => ({ top: 400 } as DOMRect)

    await user.click(screen.getByText('go-exercise'))
    // 400 - 64: the divider lands just below the sticky step bar.
    expect(container.scrollTo).toHaveBeenCalledWith({ top: 336, behavior: 'smooth' })
    expect(screen.getByTestId('active')).toHaveTextContent('exercise')
    expect(onContentRead).toHaveBeenCalledTimes(1)
  })

  it('below lg, where the window scrolls, it scrolls the window and observes the viewport', async () => {
    vi.stubGlobal('matchMedia', (query: string) => ({
      matches: false, media: query, addEventListener: vi.fn(), removeEventListener: vi.fn(),
    }))
    const scrollTo = vi.spyOn(window, 'scrollTo').mockImplementation(() => {})
    const user = userEvent.setup()
    render(<Harness hasExercise />)
    const container = screen.getByTestId('container')
    container.scrollTo = vi.fn()
    screen.getByTestId('divider').getBoundingClientRect = () => ({ top: 900 } as DOMRect)

    expect(observedOptions?.root).toBeNull()
    expect(document.documentElement.style.scrollPaddingTop).toBe('64px')
    await user.click(screen.getByText('go-exercise'))
    expect(scrollTo).toHaveBeenCalledWith({ top: 900 - 64, behavior: 'smooth' })
    expect(container.scrollTo).not.toHaveBeenCalled()
    scrollTo.mockRestore()
    vi.unstubAllGlobals()
  })
})
