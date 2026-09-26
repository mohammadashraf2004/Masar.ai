import { cn } from '@/lib/utils'
import { MasarMark } from '@/components/brand/MasarMark'

/**
 * The Masar brand mark in its amber tile — the two-rail "Waypoint" glyph
 * (`components/brand/MasarMark`) at half the tile's size.
 *
 * Built from markup rather than loaded as a file so it inherits the palette
 * and stays crisp at 28px, the size it renders at in the sidebar. The glyph
 * takes `text-on-amber`, not `text-void`: `void` is the page background, which
 * is cream in the light theme, and cream on amber is unreadable.
 * `public/masar-mark.svg` is the same geometry with literal hex, for anything
 * outside the app (README, press, slide decks).
 */
export function LogoMark({
  size = 28,
  className,
  label = 'Masar',
}: {
  size?: number
  className?: string
  /** Pass null when a wordmark sits beside it, so it isn't read out twice. */
  label?: string | null
}) {
  return (
    <span
      // 6px radius on the 28px tile, 8px from the 32px one up.
      className={cn(
        'grid shrink-0 place-items-center bg-amber text-on-amber',
        size <= 28 ? 'rounded-md' : 'rounded-lg',
        className,
      )}
      style={{ width: size, height: size }}
      {...(label ? { role: 'img', 'aria-label': label } : { 'aria-hidden': true })}
    >
      <MasarMark size={Math.round(size / 2)} />
    </span>
  )
}

/**
 * The name in both scripts. Which one shows is decided by CSS off
 * `html[lang]` (see `.brand-en` / `.brand-ar` in globals.css) rather than by
 * reading the language store here: the preference lives in localStorage and
 * the server always renders the Arabic-first default, so a JS-side choice
 * would desynchronise hydration. Both spans are always in the DOM; only one
 * is displayed.
 *
 * This is one name in two scripts, not a translation — مسار and Masar are
 * the same word, which is why it is not in `lib/i18n`.
 */
export function Wordmark({ className }: { className?: string }) {
  return (
    <span className={cn('font-display font-bold text-bright tracking-tight', className)}>
      <span className="brand-en">Masar</span>
      <span className="brand-ar">مسار</span>
    </span>
  )
}

/**
 * The same name in the *other* script — Masar beside an Arabic reader's مسار,
 * مسار beside an English reader's Masar — for the sidebar lockup, where the
 * name in the reader's script leads and this sits at the far end, quiet.
 * Hidden from assistive technology: the name has already been read once.
 */
export function AltWordmark({ className }: { className?: string }) {
  return (
    <span aria-hidden="true" className={cn('font-display font-bold', className)}>
      <span className="brand-alt-en">Masar</span>
      <span className="brand-alt-ar">مسار</span>
    </span>
  )
}

export function Logo({
  size = 28,
  className,
  wordmarkClassName,
}: {
  size?: number
  className?: string
  wordmarkClassName?: string
}) {
  return (
    <div className={cn('flex items-center gap-2.5', className)}>
      <LogoMark size={size} label={null} />
      <Wordmark className={wordmarkClassName} />
    </div>
  )
}
