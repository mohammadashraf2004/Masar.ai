import { cn } from '@/lib/utils'
import { ButtonHTMLAttributes, forwardRef } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'amber' | 'ghost' | 'danger' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'amber', size = 'md', loading, children, disabled, ...props }, ref) => {
    // `min-h-[44px]` below lg gives every button a comfortable touch target
    // without touching padding or type size, so the sm/md/lg hierarchy still
    // reads through width and font. From lg up it releases and the desktop
    // metrics are exactly what they were.
    const base = 'inline-flex items-center justify-center gap-2 rounded font-medium transition-all duration-150 min-h-[44px] lg:min-h-0 disabled:opacity-40 disabled:cursor-not-allowed focus-visible:outline focus-visible:outline-1 focus-visible:outline-amber'
    const variants = {
      amber: 'bg-amber text-void hover:bg-amber2 hover:shadow-[0_0_20px_rgba(245,158,11,0.3)]',
      ghost: 'bg-transparent border border-border text-soft hover:border-amber/30 hover:text-bright hover:bg-surface',
      danger: 'bg-rose/10 border border-rose/30 text-rose hover:bg-rose/20',
      outline: 'bg-transparent border border-amber/40 text-amber hover:bg-amber/10',
    }
    const sizes = {
      sm: 'px-3 py-1.5 text-xs',
      md: 'px-4 py-2 text-sm',
      lg: 'px-6 py-3 text-sm',
    }
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(base, variants[variant], sizes[size], className)}
        {...props}
      >
        {loading ? (
          <span className="w-4 h-4 border border-current border-t-transparent rounded-full animate-spin" />
        ) : children}
      </button>
    )
  }
)
Button.displayName = 'Button'
