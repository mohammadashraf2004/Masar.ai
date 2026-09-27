import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useLanguageStore } from '@/lib/language'
import { Tour } from './Tour'
import { tourById, type TourDef } from './registry'
import { ONBOARDING_DESKTOP, Targets, mockLayout } from './tourTestKit'

const ONBOARDING = tourById('onboarding')
const MENTOR = tourById('mentor-interview')

function setup(tour: TourDef = ONBOARDING, extra: Partial<React.ComponentProps<typeof Tour>> = {}) {
  const onFinish = vi.fn()
  const ids = Array.from(new Set(tour.steps.map((s) => (typeof s.target === 'string' ? s.target : s.target.desktop))))
  const view = render(
    <>
      <Targets ids={ids} />
      <Tour tour={tour} steps={tour.steps} device="desktop" onFinish={onFinish} {...extra} />
    </>,
  )
  return { onFinish, ...view }
}

const card = () => screen.getByRole('dialog')
const title = () => screen.getByRole('heading', { level: 3 }).textContent
const counter = () => card().querySelector('[aria-live="polite"]')!.textContent
const button = (name: string) => screen.getByRole('button', { name })
/** The step changes after the text has faded out. */
const stepIs = (n: number) => waitFor(() => expect(counter()).toMatch(new RegExp('^' + n + ' ')))

beforeEach(() => {
  mockLayout()
})

describe('the card', () => {
  it('is a labelled modal dialog whose counter is a live region', () => {
    setup()
    expect(card()).toHaveAttribute('aria-modal', 'true')
    const heading = screen.getByRole('heading', { level: 3 })
    expect(card()).toHaveAttribute('aria-labelledby', heading.id)
    expect(card().querySelector('[aria-live="polite"]')).toHaveTextContent('1 of 4')
  })

  it('is drawn in a portal on the body, over the page', () => {
    const { container } = setup()
    expect(container.querySelector('[role="dialog"]')).toBeNull()
    expect(document.body.querySelector('.tour-layer > [role="dialog"]')).toBe(card())
  })

  it('takes focus, and gives it back when it goes', () => {
    const opener = document.createElement('button')
    document.body.appendChild(opener)
    opener.focus()
    const { unmount } = setup()
    expect(card()).toHaveFocus()
    unmount()
    expect(opener).toHaveFocus()
    opener.remove()
  })

  it('keeps Tab inside itself, wrapping at both ends and coming back from the page', () => {
    setup()
    fireEvent.click(button('Next'))
    // Now on step 2: Skip, Back, Next.
    return waitFor(() => expect(counter()).toMatch(/^2 /)).then(() => {
      const skip = button('Skip tour'), next = button('Next')
      next.focus()
      fireEvent.keyDown(document, { key: 'Tab' })
      expect(skip).toHaveFocus()
      fireEvent.keyDown(document, { key: 'Tab', shiftKey: true })
      expect(next).toHaveFocus()
      // Focus that has wandered onto the page is brought back.
      const outside = document.querySelector<HTMLElement>('[data-tour="path"]')!
      outside.tabIndex = 0
      outside.focus()
      fireEvent.keyDown(document, { key: 'Tab' })
      expect(card().contains(document.activeElement)).toBe(true)
    })
  })

  it('is 44px tall on every button', () => {
    setup()
    fireEvent.click(button('Next'))
    return waitFor(() => expect(counter()).toMatch(/^2 /)).then(() => {
      for (const b of Array.from(card().querySelectorAll('button'))) expect(b.className).toMatch(/min-h-\[44px\]/)
    })
  })
})

describe('moving through the steps', () => {
  it('goes forward with Next and back with Back, the step counter following', async () => {
    setup()
    expect(title()).toBe('Your path starts here')
    fireEvent.click(button('Next'))
    await stepIs(2)
    expect(title()).toBe('Learn at your pace')
    fireEvent.click(button('Next'))
    await stepIs(3)
    expect(title()).toBe('Practice what you learn')
    fireEvent.click(button('Back'))
    await stepIs(2)
    expect(title()).toBe('Learn at your pace')
  })

  it('has no Back on the first step, and no Skip on the last', async () => {
    setup()
    expect(screen.queryByRole('button', { name: 'Back' })).toBeNull()
    expect(screen.getByRole('button', { name: 'Skip tour' })).toBeInTheDocument()
    for (let n = 2; n <= 4; n++) { fireEvent.click(button('Next')); await stepIs(n) }
    expect(screen.getByRole('button', { name: 'Back' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Skip tour' })).toBeNull()
  })

  it('skips from any step, reporting a skip', () => {
    const { onFinish } = setup()
    fireEvent.click(button('Skip tour'))
    expect(onFinish).toHaveBeenCalledExactlyOnceWith('skipped')
  })

  it('draws one pill per step, the current one wider', async () => {
    setup()
    const pills = () => Array.from(card().querySelectorAll<HTMLElement>('[aria-hidden="true"] > span')).map((p) => p.style.width)
    expect(pills()).toEqual(['18px', '6px', '6px', '6px'])
    fireEvent.click(button('Next'))
    await stepIs(2)
    expect(pills()).toEqual(['6px', '18px', '6px', '6px'])
  })

  it('fades the text for 140ms while the step changes underneath it', async () => {
    setup()
    const content = () => card().querySelector<HTMLElement>('.tour-content')!
    fireEvent.click(button('Next'))
    expect(content().style.opacity).toBe('0')
    expect(counter()).toMatch(/^1 /)
    await stepIs(2)
    expect(content().style.opacity).toBe('1')
  })

  it('changes at once for someone who asked for less motion', () => {
    window.matchMedia = ((q: string) => ({ matches: q.includes('reduce'), media: q })) as unknown as typeof window.matchMedia
    try {
      setup()
      fireEvent.click(button('Next'))
      expect(counter()).toMatch(/^2 /)
    } finally {
      // @ts-expect-error jsdom has no matchMedia; put it back as it was
      delete window.matchMedia
    }
  })
})

describe('the last step', () => {
  async function toLast(tour: TourDef) {
    const view = setup(tour)
    for (let n = 2; n <= tour.steps.length; n++) { fireEvent.click(button('Next')); await stepIs(n) }
    return view
  }

  it('reads "Get started" for the onboarding, and finishing reports done', async () => {
    const { onFinish } = await toLast(ONBOARDING)
    expect(screen.queryByRole('button', { name: 'Next' })).toBeNull()
    fireEvent.click(button('Get started'))
    expect(onFinish).toHaveBeenCalledExactlyOnceWith('done')
  })

  it('reads "Got it" for a feature tour', async () => {
    const { onFinish } = await toLast(MENTOR)
    expect(screen.queryByRole('button', { name: 'Get started' })).toBeNull()
    fireEvent.click(button('Got it'))
    expect(onFinish).toHaveBeenCalledExactlyOnceWith('done')
  })

  it('reads the same in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar' })
    const { onFinish } = setup(MENTOR)
    fireEvent.click(button('التالي'))
    await waitFor(() => expect(counter()).toMatch(/^٢ /))
    fireEvent.click(button('فهمت'))
    expect(onFinish).toHaveBeenCalledWith('done')
  })
})

describe('the keyboard', () => {
  const press = (key: string) => fireEvent.keyDown(document.activeElement ?? document.body, { key })

  it('goes forward with → in English, back with ←, and skips on Escape', async () => {
    const { onFinish } = setup()
    press('ArrowRight')
    await stepIs(2)
    press('ArrowLeft')
    await stepIs(1)
    press('ArrowLeft')                       // nothing before the first step
    expect(counter()).toMatch(/^1 /)
    press('Escape')
    expect(onFinish).toHaveBeenCalledExactlyOnceWith('skipped')
  })

  it('goes forward with ← in Arabic, back with →', async () => {
    useLanguageStore.setState({ language: 'ar' })
    setup()
    press('ArrowLeft')
    await waitFor(() => expect(counter()).toMatch(/^٢ /))
    press('ArrowRight')
    await waitFor(() => expect(counter()).toMatch(/^١ /))
  })

  it('does not treat the other direction\'s forward key as forward', async () => {
    setup()
    press('ArrowRight')
    await stepIs(2)
    press('ArrowLeft')                       // in English this is back, not forward
    await stepIs(1)
  })

  it('goes forward on Enter, but leaves Enter on a focused button to the button', async () => {
    setup()
    press('Enter')
    await stepIs(2)
    // Enter on Back is Back's, not "next".
    button('Back').focus()
    fireEvent.keyDown(button('Back'), { key: 'Enter' })
    expect(counter()).toMatch(/^2 /)
  })

  it('finishes on the forward key at the last step', async () => {
    const { onFinish } = setup(MENTOR)
    press('ArrowRight')
    await stepIs(2)
    press('ArrowRight')
    expect(onFinish).toHaveBeenCalledExactlyOnceWith('done')
  })

  it('leaves the keys alone while someone types in the page behind', () => {
    const { onFinish } = setup()
    const input = document.createElement('input')
    document.body.appendChild(input)
    input.focus()
    fireEvent.keyDown(input, { key: 'ArrowRight' })
    fireEvent.keyDown(input, { key: 'Enter' })
    expect(counter()).toMatch(/^1 /)
    expect(onFinish).not.toHaveBeenCalled()
    input.remove()
  })
})

describe('the "New" tag', () => {
  it('is on a feature tour shown to an account that predates it', () => {
    setup(MENTOR, { showNew: true })
    expect(within(card()).getByText('New')).toBeInTheDocument()
  })

  it('is absent when it is not asked for, and never on the onboarding', () => {
    const { unmount } = setup(MENTOR, { showNew: false })
    expect(within(card()).queryByText('New')).toBeNull()
    unmount()
    setup(ONBOARDING, { showNew: true })
    expect(within(card()).queryByText('New')).toBeNull()
  })
})

describe('the strings', () => {
  it('are English, with the counter as "1 of 4"', () => {
    setup()
    expect(card()).toHaveTextContent('1 of 4')
    expect(card()).toHaveTextContent('Follow your personalized learning path and see what to learn next.')
    expect(card().closest('.tour-layer')).toHaveAttribute('dir', 'ltr')
  })

  it('are Arabic, right to left, with the counter in Arabic digits: "١ من ٤"', () => {
    useLanguageStore.setState({ language: 'ar' })
    setup()
    expect(counter()).toBe('١ من ٤')
    expect(title()).toBe('مسارك يبدأ من هنا')
    expect(card()).toHaveTextContent('اتّبع مسار التعلّم المخصّص لك، واعرف ما الذي تتعلّمه بعد ذلك.')
    expect(button('تخطّي الجولة')).toBeInTheDocument()
    expect(card().closest('.tour-layer')).toHaveAttribute('dir', 'rtl')
  })
})

describe('switching language part-way through', () => {
  it('re-renders the card in the new language and direction without restarting', async () => {
    setup()
    fireEvent.click(button('Next'))
    await stepIs(2)
    expect(title()).toBe('Learn at your pace')

    act(() => { useLanguageStore.setState({ language: 'ar' }) })

    expect(title()).toBe('تعلّم بالسرعة التي تناسبك')       // the same step, in Arabic
    expect(counter()).toBe('٢ من ٤')                          // still step 2: not restarted
    expect(card().closest('.tour-layer')).toHaveAttribute('dir', 'rtl')
    expect(button('السابق')).toBeInTheDocument()

    act(() => { useLanguageStore.setState({ language: 'en' }) })
    expect(counter()).toBe('2 of 4')
    expect(card().closest('.tour-layer')).toHaveAttribute('dir', 'ltr')
  })

  it('places the card again for the new direction', async () => {
    // The nav rail swaps sides with the direction: at the start edge in each.
    mockLayout({
      rects: { 'nav-mentor': { x: 16, y: 300, w: 216, h: 44 } },
      rtlRects: { 'nav-mentor': { x: 1208, y: 300, w: 216, h: 44 } },
    })
    setup()
    for (let n = 2; n <= 4; n++) { fireEvent.click(button('Next')); await stepIs(n) }
    // Beside the item, on its far side: to its right in LTR.
    await waitFor(() => expect(card().style.left).toBe(`${16 - 6 + 216 + 12 + 14}px`))
    expect(card().querySelector<HTMLElement>('.tour-arrow')!.style.left).toBe('-7px')

    // What LanguageProvider does when the language changes.
    document.documentElement.dir = 'rtl'
    act(() => { useLanguageStore.setState({ language: 'ar' }) })

    // The item is now at the right edge, and the card goes to its left.
    await waitFor(() => expect(card().style.left).toBe(`${1208 - 6 - 14 - 344}px`))
    expect(card().querySelector<HTMLElement>('.tour-arrow')!.style.right).toBe('-7px')
    expect(counter()).toBe('٤ من ٤')
    document.documentElement.dir = ''
  })
})

describe('placement on the page', () => {
  it('sits below its target with the arrow on the target\'s centre', async () => {
    mockLayout({ rects: { path: { x: 100, y: 100, w: 200, h: 80 } } })
    setup()
    // The spotlight is the target plus 6px each side: x 94..306, y 94..186, centre x = 200.
    await waitFor(() => expect(card().style.top).toBe(`${186 + 14}px`))
    expect(card().style.width).toBe('344px')
    expect(card().style.left).toBe(`${200 - 172}px`)
    // 344/2 = 172 along the card: the arrow's own centre, so its left edge is 7px short of that.
    expect(card().querySelector<HTMLElement>('.tour-arrow')!.style.left).toBe(`${172 - 7}px`)
  })

  it('draws the ring round the target and the dim as its shadow', async () => {
    setup()
    const ring = () => document.querySelector<HTMLElement>('.tour-ring')!
    await waitFor(() => expect(ring().style.left).toBe('94px'))
    expect(ring().style.top).toBe('94px')
    expect(ring().style.width).toBe('212px')
    expect(ring().style.height).toBe('92px')
    expect(ring().style.borderRadius).toBe('12px')
    expect(ring().style.boxShadow).toContain('0 0 0 9999px var(--dim)')
    expect(ring().style.boxShadow).toContain('rgba(245,158,11,.20)')
    // The four blur panels leave the target itself uncovered.
    expect(document.querySelectorAll('.tour-blur')).toHaveLength(4)
  })

  it('goes full width on a phone', async () => {
    mockLayout({ width: 390, height: 844 })
    setup()
    await waitFor(() => expect(card().style.width).toBe('366px'))
  })

  it('is centred over a full dim when the target is not there', async () => {
    mockLayout({ hidden: ['path'] })
    setup()
    await waitFor(() => expect(card().style.opacity).toBe('1'), { timeout: 4000 })
    expect(card().style.left).toBe(`${(1440 - 344) / 2}px`)
    expect(parseFloat(document.querySelector<HTMLElement>('.tour-ring')!.style.borderRadius)).toBe(0)
    expect(card().querySelector<HTMLElement>('.tour-arrow')!.style.display).toBe('none')
  })

  it('stays inside the viewport whichever step it is on', async () => {
    setup()
    for (let n = 1; n <= 4; n++) {
      if (n > 1) { fireEvent.click(button('Next')); await stepIs(n) }
      await waitFor(() => expect(card().style.opacity).toBe('1'))
      const left = parseFloat(card().style.left), top = parseFloat(card().style.top)
      expect(left).toBeGreaterThanOrEqual(12)
      expect(left + 344).toBeLessThanOrEqual(1440 - 12)
      expect(top).toBeGreaterThanOrEqual(12)
    }
  })
})
