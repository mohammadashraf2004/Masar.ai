'use client'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { HTMLAttributes } from 'react'

// ─── Card ────────────────────────────────────────────────────────────────────
interface CardProps extends HTMLAttributes<HTMLDivElement> {
  glow?: boolean
}
export function Card({ className, glow, ...props }: CardProps) {
  return (
    <div
      className={cn(
        'bg-panel border border-border rounded-lg transition-all duration-200',
        glow && 'hover:border-amber/20 hover:shadow-[0_0_24px_rgba(245,158,11,0.06)]',
        className
      )}
      {...props}
    />
  )
}

// ─── Badge ───────────────────────────────────────────────────────────────────
type BadgeVariant = 'beginner' | 'intermediate' | 'advanced' | 'amber' | 'emerald' | 'rose' | 'sky' | 'ghost'
interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant
}
const badgeStyles: Record<BadgeVariant, string> = {
  beginner:     'bg-emerald/10 text-emerald border-emerald/20',
  intermediate: 'bg-amber/10 text-amber border-amber/20',
  advanced:     'bg-rose/10 text-rose border-rose/20',
  amber:        'bg-amber/10 text-amber border-amber/20',
  emerald:      'bg-emerald/10 text-emerald border-emerald/20',
  rose:         'bg-rose/10 text-rose border-rose/20',
  sky:          'bg-sky/10 text-sky border-sky/20',
  ghost:        'bg-muted/40 text-soft border-border',
}
export function Badge({ variant = 'ghost', className, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border',
        badgeStyles[variant],
        className
      )}
      {...props}
    />
  )
}

// ─── Progress bar ─────────────────────────────────────────────────────────────
interface ProgressProps {
  value: number   // 0–100
  className?: string
  color?: 'amber' | 'emerald' | 'rose' | 'sky'
  size?: 'sm' | 'md'
}
const progressColors = {
  amber:   'from-amber to-amber2',
  emerald: 'from-emerald to-emerald/70',
  rose:    'from-rose to-rose/70',
  sky:     'from-sky to-sky/70',
}
export function ProgressBar({ value, className, color = 'amber', size = 'sm' }: ProgressProps) {
  return (
    <div className={cn('progress-track w-full', size === 'sm' ? 'h-1' : 'h-2', className)}>
      <div
        className={cn('progress-fill bg-gradient-to-r', progressColors[color])}
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  )
}

// ─── Spinner ──────────────────────────────────────────────────────────────────
/**
 * A spinner is decorative unless it is the *only* sign that something is loading.
 * Pass `announce` then: it becomes a polite live region reading "Loading…" (in
 * the reader's language), so a screen-reader user is told what is happening.
 * Leave it off when the spinner sits inside a control or region that already
 * says so (a button's own label, a wrapper with role="status"), otherwise the
 * same state is announced twice.
 */
export function Spinner({ className, announce }: { className?: string; announce?: boolean }) {
  const { t } = useI18n()
  return (
    <span
      role={announce ? 'status' : undefined}
      aria-hidden={announce ? undefined : true}
      className={cn(
        'inline-block w-4 h-4 border border-amber border-t-transparent rounded-full animate-spin',
        announce && 'relative',
        className
      )}
    >
      {announce && <span className="sr-only">{t('common.loading')}</span>}
    </span>
  )
}

// ─── Divider ─────────────────────────────────────────────────────────────────
export function Divider({ className }: { className?: string }) {
  return <div className={cn('border-t border-border', className)} />
}

// ─── Empty state ─────────────────────────────────────────────────────────────
export function EmptyState({ icon, title, description, action }: {
  icon?: React.ReactNode
  title: string
  description?: string
  action?: React.ReactNode
}) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      {icon && <div className="text-4xl mb-4 text-ghost">{icon}</div>}
      <p className="text-bright font-medium mb-1">{title}</p>
      {description && <p className="text-sm text-ghost max-w-xs">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}
