'use client'
import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import type { SkillOption } from '@/types'
import { SkillPicker } from './SkillPicker'

export interface SkillsQuery {
  goal: string
  level: string | null
  fields: string[]
}

interface SkillsStepProps {
  query: SkillsQuery
  value: string[]
  onChange: (slugs: string[]) => void
}

interface Loaded {
  key: string
  options: SkillOption[] | null // null = failed
}

/**
 * "Skills & Technologies I Know" for one goal, route and level.
 *
 * The list is fetched from the API — which derives it from the catalogue — and
 * never written into the interface. The result is tagged with the request it
 * answers (as the paths page does), so changing the goal or the fields reads as
 * loading until the new list lands, with no state to reset by hand.
 */
export function SkillsStep({ query, value, onChange }: SkillsStepProps) {
  const { t } = useI18n()
  const key = `${query.goal}|${query.level ?? ''}|${query.fields.join(',')}`
  const [loaded, setLoaded] = useState<Loaded | null>(null)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    let stale = false
    api
      .getSkillOptions({ career_goal: query.goal, level: query.level, field: query.fields })
      .then((options) => !stale && setLoaded({ key, options }))
      .catch(() => !stale && setLoaded({ key, options: null }))
    return () => {
      stale = true
    }
    // `key` covers goal, level and fields; `attempt` is the retry button.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, attempt])

  const current = loaded?.key === key ? loaded : null

  if (!current) {
    return (
      <div className="flex justify-center py-10" role="status" aria-label={t('common.loading')}>
        <Spinner className="h-5 w-5" />
      </div>
    )
  }

  if (current.options === null) {
    return (
      <div className="py-4 text-center">
        <p role="alert" className="mb-3 text-sm text-rose">{t('skills.loadError')}</p>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => {
            setLoaded(null)
            setAttempt((n) => n + 1)
          }}
        >
          {t('common.retry')}
        </Button>
      </div>
    )
  }

  if (current.options.length === 0) {
    return <p className="py-4 text-sm text-soft">{t('skills.empty')}</p>
  }

  return <SkillPicker options={current.options} value={value} onChange={onChange} />
}
