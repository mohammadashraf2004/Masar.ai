import { cn } from '@/lib/utils'
import { InputHTMLAttributes, forwardRef } from 'react'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  hint?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, hint, id, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-')
    // The message is tied to the field so it is read when the field is focused,
    // and is a live region so it is also read the moment it appears.
    const messageId = inputId ? `${inputId}-message` : undefined
    const described = (error || hint) && messageId ? messageId : undefined
    return (
      <div className="flex flex-col gap-1.5">
        {label && (
          <label htmlFor={inputId} className="ui-eyebrow">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          aria-invalid={error ? true : undefined}
          aria-describedby={described}
          className={cn(
            // 16px on mobile, 14px from md up. Mobile Safari zooms the whole
            // page when a focused field is under 16px and never zooms back
            // out; `text-base md:text-sm` is the standard way out of that
            // without changing how the field looks on a desktop.
            'w-full min-h-[44px] lg:min-h-0 bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost',
            'focus:outline-none focus:border-amber/50 focus:bg-panel transition-colors duration-150',
            error && 'border-rose/50 focus:border-rose/70',
            className
          )}
          {...props}
        />
        {error && <span id={messageId} role="alert" className="text-caption text-rose">{error}</span>}
        {hint && !error && <span id={messageId} className="ui-caption">{hint}</span>}
      </div>
    )
  }
)
Input.displayName = 'Input'
