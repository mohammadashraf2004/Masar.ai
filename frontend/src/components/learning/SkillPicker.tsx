'use client'
import { useId } from 'react'
import { Check } from 'lucide-react'
import { Badge } from '@/components/ui/index'
import { useI18n } from '@/lib/i18n'
import { fieldLabel, skillLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { FieldRef, SkillOption } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'

interface Group {
  key: string
  field: FieldRef | null
  kind: 'field' | 'tools' | 'general'
  options: SkillOption[]
}

/**
 * Sections for the picker, derived from what the server sent: a capability is
 * filed under the field most of its courses belong to, a tool goes under
 * "Tools & frameworks", and anything the route does not cover falls under
 * "General". The order is the server's (capabilities first, then tools); a group
 * appears at the position of its first member. Nothing here names a category.
 */
export function groupSkillOptions(options: SkillOption[]): Group[] {
  const groups: Group[] = []
  const at = new Map<string, Group>()
  for (const option of options) {
    const tool = option.kind === 'tool'
    const key = tool ? '@tools' : option.group ? `field:${option.group.slug}` : '@general'
    let group = at.get(key)
    if (!group) {
      group = {
        key,
        field: tool ? null : option.group ?? null,
        kind: tool ? 'tools' : option.group ? 'field' : 'general',
        options: [],
      }
      at.set(key, group)
      groups.push(group)
    }
    group.options.push(option)
  }
  return groups
}

interface SkillPickerProps {
  options: SkillOption[]
  value: string[]
  onChange: (slugs: string[]) => void
}

/**
 * "Skills & Technologies I Know": real checkboxes in labelled groups.
 *
 * Every option is a native `<input type="checkbox">` inside its `<label>`, so it
 * is a checkbox to assistive technology, toggles from the keyboard (Tab, Space)
 * and shows a focus ring; the whole row is the target and is at least 44px tall.
 * Selections the learner made earlier for skills this route does not list are
 * left alone by "Clear all" — they still count, they are just not on screen.
 */
export function SkillPicker({ options, value, onChange }: SkillPickerProps) {
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  const base = useId()
  const groups = groupSkillOptions(options)
  const visible = new Set(options.map((o) => o.slug))
  const chosenHere = value.filter((slug) => visible.has(slug)).length

  const toggle = (slug: string) =>
    onChange(value.includes(slug) ? value.filter((s) => s !== slug) : [...value, slug])

  return (
    <div>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
        <p className="text-xs text-soft" role="status" aria-live="polite">
          {tf('skills.selected', { n: chosenHere })}
        </p>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => onChange(Array.from(new Set([...value, ...options.map((o) => o.slug)])))}
            className="min-h-[44px] rounded-md border border-border px-3 text-xs text-soft transition-colors hover:border-muted hover:text-bright focus-visible:outline focus-visible:outline-2 focus-visible:outline-amber lg:min-h-0 lg:py-1.5"
          >
            {t('skills.selectAll')}
          </button>
          <button
            type="button"
            onClick={() => onChange(value.filter((s) => !visible.has(s)))}
            disabled={chosenHere === 0}
            className="min-h-[44px] rounded-md border border-border px-3 text-xs text-soft transition-colors hover:border-muted hover:text-bright focus-visible:outline focus-visible:outline-2 focus-visible:outline-amber disabled:opacity-40 lg:min-h-0 lg:py-1.5"
          >
            {t('skills.clear')}
          </button>
        </div>
      </div>

      <div className="space-y-6">
        {groups.map((group) => {
          const heading =
            group.kind === 'tools' ? t('skills.group.tools')
            : group.kind === 'general' ? t('skills.group.general')
            : null
          return (
            <fieldset key={group.key} className="min-w-0">
              <legend className="mb-2.5 text-xs font-medium uppercase tracking-widest text-soft">
                {heading ?? (group.field && <LearningLabel parts={fieldLabel(group.field, ctx, true)} />)}
              </legend>
              {group.kind === 'tools' && (
                <p className="mb-3 text-xs leading-relaxed text-soft">{t('skills.toolNote')}</p>
              )}
              <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                {group.options.map((option) => {
                  const selected = value.includes(option.slug)
                  const id = `${base}-${option.slug}`
                  return (
                    <label
                      key={option.slug}
                      htmlFor={id}
                      className={cn(
                        'flex min-h-[44px] cursor-pointer items-center gap-3 rounded-lg border px-3 py-2 transition-colors',
                        'has-[:focus-visible]:outline has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-offset-1 has-[:focus-visible]:outline-amber',
                        selected
                          ? 'border-amber/50 bg-amber/10 text-bright'
                          : 'border-border bg-panel text-soft hover:border-muted hover:text-bright'
                      )}
                    >
                      <input
                        id={id}
                        type="checkbox"
                        className="peer sr-only"
                        checked={selected}
                        onChange={() => toggle(option.slug)}
                      />
                      <span
                        aria-hidden="true"
                        className={cn(
                          'flex h-5 w-5 shrink-0 items-center justify-center rounded border transition-colors',
                          selected ? 'border-amber bg-amber text-void' : 'border-muted bg-surface'
                        )}
                      >
                        {selected && <Check size={13} strokeWidth={3} />}
                      </span>
                      <span className="min-w-0 flex-1 text-sm leading-snug">
                        <LearningLabel parts={skillLabel(option, ctx)} />
                      </span>
                      {option.is_required && <Badge variant="amber">{t('skills.required')}</Badge>}
                    </label>
                  )
                })}
              </div>
            </fieldset>
          )
        })}
      </div>
    </div>
  )
}
