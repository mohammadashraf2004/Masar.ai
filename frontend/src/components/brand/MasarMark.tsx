/**
 * The Masar mark — "Waypoint": two rails and the learner as a node held
 * between them (مسار is a track). Drawn on a 24px grid with one stroke weight so
 * it survives 14px inside a 28px tile.
 *
 * The glyph only, in `currentColor`: the tile it usually sits in is
 * `LogoMark` (layout/Logo.tsx), and the bare glyph is also the tile-less
 * "mono" use — `text-amber-text` straight onto a dark surface.
 *
 * It is mirror-symmetric, so it reads the same in a right-to-left page. Never
 * add `rtl:rotate-180` to it.
 */
export function MasarMark({ size = 14, className, style }: { size?: number; className?: string; style?: React.CSSProperties }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2.4}
      aria-hidden="true"
      className={className}
      // For a size that is not in pixels (the certificate sizes everything in `cqw`);
      // CSS width and height beat the attributes above.
      style={style}
    >
      <path d="M4 3.5V20.5" />
      <path d="M20 3.5V20.5" />
      <circle cx="12" cy="12" r="4.5" fill="currentColor" stroke="none" />
    </svg>
  )
}
