'use client'
import type { ElementType, ReactNode } from 'react'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ChoiceCardProps {
  /** `radio` for pick-one groups, `checkbox` for pick-many. */
  role: 'radio' | 'checkbox'
  selected: boolean
  onSelect: () => void
  title: ReactNode
  description?: ReactNode
  /** A small tag beside the title, e.g. "Advanced". */
  badge?: ReactNode
  icon?: ElementType
  /** A line under the description, e.g. "Content coming soon". */
  footer?: ReactNode
  className?: string
}

/**
 * One selectable option. A real <button> with the matching ARIA role, so it is
 * reachable and operable from the keyboard and announced correctly, and its
 * whole surface is the target — comfortably over 44px tall on a phone.
 * Direction-safe: it uses logical (start/end) utilities only.
 */
export function ChoiceCard({
  role, selected, onSelect, title, description, badge, icon: Icon, footer, className,
}: ChoiceCardProps) {
  return (
    <button
      type="button"
      role={role}
      aria-checked={selected}
      onClick={onSelect}
      className={cn(
        'relative w-full text-start rounded-lg border p-4 pe-9 transition-all duration-150',
        selected
          ? 'bg-amber/10 border-amber/50 text-bright'
          : 'bg-panel border-border text-soft hover:border-muted hover:text-bright',
        className
      )}
    >
      {selected && <Check size={14} className="absolute top-3.5 end-3.5 text-amber-text" aria-hidden="true" />}
      <span className="flex items-start gap-3">
        {Icon && (
          <span
            className={cn(
              'mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-md border',
              selected ? 'border-amber/40 bg-amber/10 text-amber-text' : 'border-border bg-surface text-soft'
            )}
            aria-hidden="true"
          >
            <Icon size={15} />
          </span>
        )}
        <span className="min-w-0 flex-1">
          <span className="flex flex-wrap items-center gap-2">
            <span className="text-sm font-medium leading-snug">{title}</span>
            {badge}
          </span>
          {description && (
            <span className="mt-1 block text-xs leading-relaxed text-soft">{description}</span>
          )}
          {footer && <span className="mt-2 block text-xs text-dim">{footer}</span>}
        </span>
      </span>
    </button>
  )
}
