'use client'
import { Clock } from 'lucide-react'
import { Badge } from '@/components/ui/index'
import { pick } from '@/lib/content-language'
import { useI18n } from '@/lib/i18n'
import { iconFor } from '@/lib/learning-icons'
import { fieldLabel, labelText, levelLabel, roleLabel } from '@/lib/learning'
import type { CareerGoal, LearningField, LearningLevel } from '@/types'
import { ChoiceCard } from './ChoiceCard'
import { LearningLabel, useLabelContext } from './LearningLabel'

// The three questions of onboarding as reusable pieces. The onboarding flow,
// the learning-profile page and the Explore filters all render from these, so
// the options, their wording and their behaviour are defined once — and every
// option list comes from the API, never from this file.

export function LevelPicker({
  levels, value, onChange,
}: { levels: LearningLevel[]; value: string | null; onChange: (slug: string) => void }) {
  const { language } = useI18n()
  const ctx = useLabelContext()
  return (
    <div role="radiogroup" className="grid grid-cols-1 gap-3">
      {levels.map((level) => (
        <ChoiceCard
          key={level.slug}
          role="radio"
          selected={value === level.slug}
          onSelect={() => onChange(level.slug)}
          title={<LearningLabel parts={levelLabel(level, ctx)} />}
          description={pick(level.description, level.description_ar, language)}
        />
      ))}
    </div>
  )
}

export function FieldPicker({
  fields, value, onChange, level,
}: {
  fields: LearningField[]
  value: string[]
  onChange: (slugs: string[]) => void
  /** The level chosen earlier, so an advanced field can explain itself. */
  level?: LearningLevel | null
}) {
  const { t, tf, language } = useI18n()
  const ctx = useLabelContext()

  const toggle = (slug: string) =>
    onChange(value.includes(slug) ? value.filter((s) => s !== slug) : [...value, slug])

  // Chosen fields that start above the learner's level. Comparing two ranks the
  // server supplied is presentation; whether the route is built, and how, is
  // decided by the backend when the path is generated.
  const above = fields.filter(
    (f) => value.includes(f.slug) && f.min_level && level && level.rank < f.min_level.rank
  )

  return (
    <div>
      <div role="group" className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        {fields.map((field) => {
          const Icon = iconFor(field.icon)
          return (
            <ChoiceCard
              key={field.slug}
              role="checkbox"
              selected={value.includes(field.slug)}
              onSelect={() => toggle(field.slug)}
              icon={Icon}
              title={<LearningLabel parts={fieldLabel(field, ctx)} />}
              badge={field.is_advanced ? <Badge variant="advanced">{t('onb.fields.advanced')}</Badge> : undefined}
              description={pick(field.description, field.description_ar, language)}
              footer={
                field.available_course_count === 0 ? (
                  <span className="inline-flex items-center gap-1">
                    <Clock size={11} aria-hidden="true" />
                    {t('onb.fields.comingSoon')}
                  </span>
                ) : undefined
              }
            />
          )
        })}
      </div>

      {above.map((field) => (
        <p
          key={field.slug}
          role="note"
          className="mt-4 rounded-md border border-amber/30 bg-amber/5 px-3 py-2.5 text-xs leading-relaxed text-soft"
        >
          {tf('onb.fields.advancedNotice', {
            field: labelText(fieldLabel(field, ctx, true)),
            // The modalities it builds on, as the catalogue lists them.
            prerequisites: field.prerequisites.map((p) => labelText(fieldLabel(p, ctx, true))).join(' / '),
          })}
        </p>
      ))}
    </div>
  )
}

export function GoalPicker({
  goals, value, onChange,
}: { goals: CareerGoal[]; value: string | null; onChange: (slug: string) => void }) {
  const { language } = useI18n()
  const ctx = useLabelContext()
  return (
    <div role="radiogroup" className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      {goals.map((goal) => (
        <ChoiceCard
          key={goal.slug}
          role="radio"
          selected={value === goal.slug}
          onSelect={() => onChange(goal.slug)}
          icon={iconFor(goal.icon)}
          title={<LearningLabel parts={roleLabel(goal, ctx)} />}
          description={pick(goal.description, goal.description_ar, language)}
        />
      ))}
    </div>
  )
}
