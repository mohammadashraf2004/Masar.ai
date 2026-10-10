import { cn } from '@/lib/utils'
import { ButtonHTMLAttributes, forwardRef } from 'react'

type ButtonVariant = 'amber' | 'ghost' | 'danger' | 'outline'
type ButtonSize = 'sm' | 'md' | 'lg'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: ButtonSize
  loading?: boolean
}

// `min-h-[44px]` below lg gives every button a comfortable touch target
// without touching padding or type size, so the sm/md/lg hierarchy still
// reads through width and font. From lg up it releases and the desktop
// metrics are exactly what they were.
const base = 'inline-flex items-center justify-center gap-2 rounded font-medium transition-all duration-150 min-h-[44px] lg:min-h-0 disabled:opacity-40 disabled:cursor-not-allowed focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring'
const variants: Record<ButtonVariant, string> = {
  // `on-amber`, not `void`: void is the page colour, which is cream in the light
  // theme; text on an amber fill stays near-black in both.
  amber: 'bg-amber text-on-amber hover:bg-amber2 hover:shadow-[0_0_20px_rgba(245,158,11,0.3)]',
  ghost: 'bg-transparent border border-border text-soft hover:border-amber/30 hover:text-bright hover:bg-surface',
  danger: 'bg-rose/10 border border-rose/30 text-rose hover:bg-rose/20',
  outline: 'bg-transparent border border-amber/40 text-amber-text hover:bg-amber/10',
}
const sizes: Record<ButtonSize, string> = {
  sm: 'px-3 py-1.5 text-caption',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-sm',
}

/**
 * The button look, for anything that has to be a link. A navigation is an
 * <a>: wrapping a <button> in one nests two interactive elements (two tab
 * stops, and a screen reader announces a button inside a link). Put these
 * classes on the <Link> instead.
 */
export function buttonStyles({ variant = 'amber', size = 'md', className }: { variant?: ButtonVariant; size?: ButtonSize; className?: string } = {}) {
  return cn(base, variants[variant], sizes[size], className)
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'amber', size = 'md', loading, children, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        aria-busy={loading || undefined}
        className={buttonStyles({ variant, size, className })}
        {...props}
      >
        {/* The label stays in the accessibility tree (visually hidden) while the
            spinner shows, so a busy button keeps its name rather than becoming an
            unnamed control. aria-busy carries the state; nothing is announced,
            because a disabled button holds no focus to announce it on. */}
        {loading ? (
          <>
            <span aria-hidden="true" className="w-4 h-4 border border-current border-t-transparent rounded-full animate-spin" />
            <span className="sr-only">{children}</span>
          </>
        ) : children}
      </button>
    )
  }
)
Button.displayName = 'Button'
