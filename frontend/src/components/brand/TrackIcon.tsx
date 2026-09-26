/**
 * The navigation icon for tracks (المسارات): the mark's two rails with the
 * marker drawn as a ring, in the same 1.8 line weight as the lucide icons
 * beside it. `MasarMark` itself is heavier (2.4, solid node) — right for a
 * tile, too loud in a row of line icons — so this is its outline cut.
 *
 * Symmetric, so like the mark it is never mirrored in right-to-left.
 */
export function TrackIcon({ size = 18, className }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.8}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      className={className}
    >
      <path d="M5 4V20" />
      <path d="M19 4V20" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  )
}
