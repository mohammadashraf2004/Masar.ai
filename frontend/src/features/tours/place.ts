/**
 * Where the card goes. Pure geometry, in the coordinates of the overlay (the viewport).
 *
 * Desktop: below the target, then above, then the side with more room. Tall targets
 * (over 40% of the viewport) and steps marked `placement: 'side'` try the sides first.
 * The card stays 12px inside the viewport; when nothing fits it docks to the bottom
 * with no arrow; with no target it is centred.
 * Mobile: above or below only, and as wide as the viewport less 12px a side.
 */

export interface Box { x: number; y: number; w: number; h: number }

export type Side = 'top' | 'bottom' | 'left' | 'right'

export interface Placement {
  left: number
  top: number
  /** The card's width. */
  cw: number
  /** Which edge of the card the arrow sits on; null for no arrow. */
  side: Side | null
  /** How far along that edge the arrow's centre is. */
  off?: number
}

/** A preferred placement: a side of the target, or `side` for "either side". */
export type Preference = Side | 'side'

export function place(
  r: Box | null, W: number, H: number, ch: number, mobile: boolean, pref?: Preference,
): Placement {
  const gap = 14, M = 12, cw = mobile ? W - 2 * M : Math.min(344, W - 2 * M)
  const clamp = (v: number, a: number, b: number) => Math.max(a, Math.min(b, v))
  if (!r) return { left: (W - cw) / 2, top: (H - ch) / 2, cw, side: null }
  const sp = { bottom: H - (r.y + r.h) - gap - M, top: r.y - gap - M, left: r.x - gap - M, right: W - (r.x + r.w) - gap - M }
  const sides = (['left', 'right'] as const).slice().sort((a, b) => sp[b] - sp[a])
  let order: Side[] = mobile
    ? ['bottom', 'top']
    : (r.h > H * 0.4 || pref === 'side') ? [...sides, 'bottom', 'top'] : ['bottom', 'top', ...sides]
  if (pref && pref !== 'side' && !mobile) order = [pref, ...order.filter((o) => o !== pref)]
  const fits = (o: Side) => (o === 'bottom' || o === 'top') ? sp[o] >= ch : sp[o] >= cw
  const o = order.find(fits)
  const cx = r.x + r.w / 2, cy = r.y + r.h / 2
  if (o === 'bottom' || o === 'top') {
    const left = clamp(cx - cw / 2, M, W - cw - M)
    return { left, top: o === 'bottom' ? r.y + r.h + gap : r.y - gap - ch, cw, side: o === 'bottom' ? 'top' : 'bottom', off: clamp(cx - left, 22, cw - 22) }
  }
  if (o === 'left' || o === 'right') {
    const top = clamp(cy - ch / 2, M, H - ch - M)
    return { left: o === 'left' ? r.x - gap - cw : r.x + r.w + gap, top, cw, side: o === 'left' ? 'right' : 'left', off: clamp(cy - top, 22, ch - 22) }
  }
  return { left: M, top: H - ch - M, cw, side: null }
}
