import { cn } from '@/lib/utils'

/**
 * The Masar brand mark — two rails with a marker between them: a track
 * (مسار) and the reader's position along it.
 *
 * Drawn inline rather than loaded as a file so it inherits the Tailwind
 * palette and stays crisp at 28px, which is the size it actually renders at
 * in the sidebar. `public/masar-mark.svg` is the same geometry with literal
 * hex, for anything outside the app (README, press, slide decks).
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
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      className={cn('shrink-0', className)}
      {...(label ? { role: 'img', 'aria-label': label } : { 'aria-hidden': true })}
    >
      <rect width="64" height="64" rx="14" className="fill-amber" />
      <rect x="12" y="14" width="5" height="36" className="fill-void" />
      <rect x="47" y="14" width="5" height="36" className="fill-void" />
      <circle cx="32" cy="32" r="10" className="fill-void" />
    </svg>
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
