'use client'
import { STRINGS, useI18n, type StringKey } from '@/lib/i18n'
import { pick } from '@/lib/content-language'
import type { Recommendation } from '@/types'
import { CourseCard } from './CourseCard'

interface NamedParam {
  title: string
  title_ar?: string | null
}

/**
 * The sentence for a recommendation, in the reader's language. The server sends a
 * reason code plus the names it needs; this only chooses the wording. A code this
 * build does not know yet falls back to the server's own English sentence, so a
 * newer backend never shows a blank or a raw code.
 */
export function useReasonText() {
  const { tf, language } = useI18n()
  return (rec: Recommendation): string => {
    const key = `rec.${rec.reason_code}` as StringKey
    const p = rec.params
    const names = Array.isArray(p.courses)
      ? (p.courses as NamedParam[]).map((c) => pick(c.title, c.title_ar, language)).join(', ')
      : ''
    const goal = typeof p.goal_title === 'string' ? pick(p.goal_title, p.goal_title_ar as string | null, language) : ''
    if (!(key in STRINGS.en)) return rec.reason
    return tf(key, {
      percent: Number(p.percent ?? 0),
      count: Number(p.count ?? 0),
      goal,
      courses: names,
    })
  }
}

/** A grid of recommended courses, each with the reason it is suggested. */
export function RecommendationGrid({ items }: { items: Recommendation[] }) {
  const reasonText = useReasonText()
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
      {items.map((rec) => (
        <div key={rec.course.id} className="flex flex-col gap-2">
          <p className="rounded-md border border-border bg-panel px-3 py-2 text-xs text-soft" dir="auto">
            {reasonText(rec)}
          </p>
          <CourseCard course={rec.course} className="flex-1" />
        </div>
      ))}
    </div>
  )
}
