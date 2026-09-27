import { describe, expect, it } from 'vitest'
import { place, type Box } from './place'

// The overlay is the viewport; boxes here are the padded spotlight.
const W = 1440, H = 900, CH = 190, CW = 344

const box = (x: number, y: number, w: number, h: number): Box => ({ x, y, w, h })

describe('place: desktop', () => {
  it('goes below the target when there is room, its arrow on the top edge', () => {
    const r = box(500, 200, 200, 80)
    const p = place(r, W, H, CH, false)
    expect(p).toMatchObject({ side: 'top', cw: CW, top: 200 + 80 + 14 })
    // Centred on the target: the target's centre is x=600.
    expect(p.left).toBe(600 - CW / 2)
    expect(p.off).toBe(CW / 2)
  })

  it('goes above when there is no room below, its arrow on the bottom edge', () => {
    const r = box(500, 700, 200, 120)   // 900 - 820 - 14 - 12 = 54px below: too little
    const p = place(r, W, H, CH, false)
    expect(p).toMatchObject({ side: 'bottom', top: 700 - 14 - CH })
  })

  it('goes to the side with more room when neither above nor below fits', () => {
    // A short viewport, the target in the middle: no vertical room either way.
    const r = box(900, 100, 200, 40)
    const p = place(r, W, 260, CH, false)
    // 94px below and 74px above: neither holds the card. Left has 874px, right 314px: the left.
    expect(p).toMatchObject({ side: 'right', left: 900 - 14 - CW })
    const q = place(box(100, 100, 200, 40), W, 260, CH, false)
    expect(q).toMatchObject({ side: 'left', left: 300 + 14 })
  })

  it('tries the sides first for a target taller than 40% of the viewport', () => {
    const tall = box(20, 100, 200, H * 0.4 + 1)
    expect(place(tall, W, H, CH, false).side).toBe('left')     // beside it, not below
    const short = box(20, 100, 200, H * 0.4 - 1)
    expect(place(short, W, H, CH, false).side).toBe('top')      // below it, as usual
  })

  it("puts a placement: 'side' target's card beside it even when there is room below", () => {
    const nav = box(10, 300, 228, 56)
    const p = place(nav, W, H, CH, false, 'side')
    expect(p.side).toBe('left')
    expect(p.left).toBe(10 + 228 + 14)
    // Vertically centred on the target, clamped to the arrow's range.
    expect(p.top).toBe(300 + 28 - CH / 2)
    expect(p.off).toBe(CH / 2)
  })

  it('honours an explicit bottom / top preference', () => {
    const r = box(500, 400, 200, 80)
    expect(place(r, W, H, CH, false, 'top')).toMatchObject({ side: 'bottom', top: 400 - 14 - CH })
    expect(place(r, W, H, CH, false, 'bottom').side).toBe('top')
  })

  it('docks the card to the bottom with no arrow when nothing fits', () => {
    // Fills the viewport: no room on any side.
    const p = place(box(0, 0, W, H), W, H, CH, false)
    expect(p).toEqual({ left: 12, top: H - CH - 12, cw: CW, side: null })
  })

  it('keeps the card 12px inside the viewport, the arrow still on the target', () => {
    const atStart = place(box(4, 200, 60, 40), W, H, CH, false)
    expect(atStart.left).toBe(12)
    expect(atStart.off).toBe(22)   // the target's centre is 22px in from where the card starts
    const atEnd = place(box(W - 64, 200, 60, 40), W, H, CH, false)
    expect(atEnd.left).toBe(W - CW - 12)
    expect(atEnd.off).toBe(CW - 22)
  })

  it('never lets the arrow into the card\'s corners', () => {
    const p = place(box(4, 200, 20, 40), W, H, CH, false)
    expect(p.off).toBe(22)
    const q = place(box(W - 24, 200, 20, 40), W, H, CH, false)
    expect(q.off).toBe(CW - 22)
  })

  it('centres the card over a full dim when the target is missing', () => {
    expect(place(null, W, H, CH, false)).toEqual({ left: (W - CW) / 2, top: (H - CH) / 2, cw: CW, side: null })
  })

  it('shrinks the card on a viewport narrower than 344 + 24', () => {
    expect(place(null, 300, H, CH, false).cw).toBe(300 - 24)
  })
})

describe('place: mobile', () => {
  const MW = 390, MH = 844

  it('is as wide as the viewport less 12px a side', () => {
    const p = place(box(20, 100, 350, 120), MW, MH, CH, true)
    expect(p.cw).toBe(MW - 24)
    expect(p.left).toBe(12)
  })

  it('goes below, then above, and never beside', () => {
    expect(place(box(20, 100, 350, 120), MW, MH, CH, true).side).toBe('top')
    expect(place(box(20, 600, 350, 120), MW, MH, CH, true).side).toBe('bottom')
    // A tall target that would go beside on desktop still goes above or below here.
    const tall = place(box(20, 300, 350, MH * 0.5), MW, MH, CH, true, 'side')
    expect(tall).toMatchObject({ side: 'bottom', left: 12 })
  })

  it('docks when neither above nor below fits', () => {
    expect(place(box(0, 0, MW, MH), MW, MH, CH, true)).toEqual({ left: 12, top: MH - CH - 12, cw: MW - 24, side: null })
  })
})
