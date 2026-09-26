'use client'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { useTheme } from '@/hooks/useTheme'
import type { Theme } from '@/lib/theme'

/**
 * The light / dark switch: a pill of two options, the chosen one filled amber.
 *
 * Two buttons with `aria-pressed` rather than a single toggle button, because
 * what it says is a choice between two named things, and each option is
 * announced with its own name ("Dark, pressed") in either language. The pill
 * is compact from `lg` up (it sits in the 64px header); below that each half
 * gets the 44px touch target the rest of the app holds controls to.
 */
export function ThemeToggle({ className }: { className?: string }) {
  const { t } = useI18n()
  const { theme, setTheme } = useTheme()

  const options: Array<{ value: Theme; label: string }> = [
    { value: 'light', label: t('theme.light') },
    { value: 'dark', label: t('theme.dark') },
  ]

  return (
    <div
      role="group"
      aria-label={t('theme.label')}
      className={cn('flex gap-0.5 rounded-full border border-border bg-surface p-[3px]', className)}
    >
      {options.map(({ value, label }) => {
        const active = theme === value
        return (
          <button
            key={value}
            type="button"
            aria-pressed={active}
            onClick={() => setTheme(value)}
            className={cn(
              'inline-flex min-h-[44px] items-center justify-center rounded-full px-3 text-xs transition-colors lg:min-h-0 lg:py-1',
              active ? 'bg-amber font-semibold text-on-amber' : 'text-dim hover:text-bright',
            )}
          >
            {label}
          </button>
        )
      })}
    </div>
  )
}
