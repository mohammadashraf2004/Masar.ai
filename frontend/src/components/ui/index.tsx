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
        // The handoff's card: --card (surface) with a 1px hairline and a 12px radius. It was
        // --card2 (panel), which on the light theme is *darker* than the page rather than lifted.
        'bg-surface border border-border rounded-xl transition-all duration-200',
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
  intermediate: 'bg-amber/10 text-amber-text border-amber/20',
  advanced:     'bg-rose/10 text-rose border-rose/20',
  amber:        'bg-amber/10 text-amber-text border-amber/20',
  emerald:      'bg-emerald/10 text-emerald border-emerald/20',
  rose:         'bg-rose/10 text-rose border-rose/20',
  sky:          'bg-sky/10 text-sky border-sky/20',
  ghost:        'bg-muted/40 text-soft border-border',
}
export function Badge({ variant = 'ghost', className, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        // A pill (999px radius), the handoff's status shape.
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-caption font-medium border',
        badgeStyles[variant],
        className
      )}
      {...props}
    />
  )
}

/**
 * A difficulty level as the reader's language spells it: مبتدئ / متوسط / متقدم,
 * or Beginner / Intermediate / Advanced. The API sends the English slug, and the
 * slug is also what picks the colour, so it is never shown raw. A level this does
 * not know (the API adds one) is shown as sent, in a neutral badge, rather than
 * hidden or mistranslated.
 */
const LEVEL_SLUGS = ['beginner', 'intermediate', 'advanced'] as const
type LevelSlug = (typeof LEVEL_SLUGS)[number]
const isLevelSlug = (level: string): level is LevelSlug => (LEVEL_SLUGS as readonly string[]).includes(level)

export function DifficultyBadge({ level, ...props }: { level: string } & Omit<BadgeProps, 'variant' | 'children'>) {
  const { t } = useI18n()
  const known = isLevelSlug(level)
  return (
    <Badge variant={known ? level : 'ghost'} {...props}>
      {known ? t(`level.${level}`) : level}
    </Badge>
  )
}

// ─── Progress bar ─────────────────────────────────────────────────────────────
interface ProgressProps {
  value: number   // 0–100
  className?: string
  color?: 'amber' | 'emerald' | 'rose' | 'sky'
  size?: 'sm' | 'md'
}
// Solid fills, as the handoff draws them (track --line, fill --acc).
const progressColors = {
  amber:   'bg-amber',
  emerald: 'bg-emerald',
  rose:    'bg-rose',
  sky:     'bg-sky',
}
export function ProgressBar({ value, className, color = 'amber', size = 'sm' }: ProgressProps) {
  const clamped = Math.min(100, Math.max(0, value))
  // A finished bar is green whatever colour it was given: "done" reads the same everywhere.
  const tone = clamped >= 100 && color === 'amber' ? 'emerald' : color
  // 4px, or 6px for the hero card.
  return (
    <div className={cn('progress-track w-full', size === 'sm' ? 'h-1' : 'h-1.5', className)}>
      <div className={cn('progress-fill', progressColors[tone])} style={{ width: `${clamped}%` }} />
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
      <p className="ui-card-title mb-1">{title}</p>
      {description && <p className="ui-description max-w-xs">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}
