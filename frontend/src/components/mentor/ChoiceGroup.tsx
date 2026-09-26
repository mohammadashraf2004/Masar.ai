'use client'
import { useId } from 'react'
import { cn } from '@/lib/utils'

export interface Choice<T extends string | number> {
  value: T
  label: string
}

/**
 * One choice out of a few, drawn as chips. They are real radio buttons (arrow keys move between
 * them, a group has one tab stop, a screen reader announces "2 of 3"), with the input visually
 * hidden and the chip its label; the ring shows on the chip when the input has keyboard focus.
 */
export function ChoiceGroup<T extends string | number>({
  legend,
  choices,
  value,
  onChange,
  disabled,
  dir,
}: {
  legend: string
  choices: readonly Choice<T>[]
  value: T | null
  onChange: (value: T) => void
  disabled?: boolean
  /** For labels in another script than the page (a role's English name in an Arabic page). */
  dir?: 'ltr' | 'rtl' | 'auto'
}) {
  const name = useId()
  return (
    <fieldset disabled={disabled} className="min-w-0">
      <legend className="mb-2 text-[13px] font-medium text-soft">{legend}</legend>
      <div className="flex flex-wrap gap-2">
        {choices.map((choice) => {
          const checked = choice.value === value
          return (
            <label
              key={String(choice.value)}
              className={cn(
                'flex min-h-[44px] cursor-pointer items-center rounded-full border px-4 py-2 text-[13px] transition-colors lg:min-h-9',
                'has-[:focus-visible]:outline has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-offset-2 has-[:focus-visible]:outline-ring',
                checked ? 'border-amber bg-amber-soft font-semibold text-white' : 'border-border text-dim hover:border-amber/40 hover:text-bright',
                disabled && 'cursor-not-allowed opacity-60',
              )}
            >
              <input
                type="radio"
                name={name}
                className="sr-only"
                checked={checked}
                onChange={() => onChange(choice.value)}
              />
              <span dir={dir}>{choice.label}</span>
            </label>
          )
        })}
      </div>
    </fieldset>
  )
}
