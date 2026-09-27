'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowRight } from 'lucide-react'
import { Card, ProgressBar } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { titleLabel } from '@/lib/learning'
import type { Recommendation, Recommendations } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'
import { useReasonText } from './RecommendationGrid'

const MAX_EACH = 3

function Row({ rec }: { rec: Recommendation }) {
  const ctx = useLabelContext()
  const reasonText = useReasonText()
  const progress = rec.course.enrollment?.progress_percentage
  return (
    <li className="py-3 first:pt-0 last:pb-0">
      <Link href={`/courses/${rec.course.slug}`} className="text-sm font-medium text-bright hover:text-amber-text">
        <LearningLabel parts={titleLabel(rec.course, ctx)} />
      </Link>
      <p className="mt-0.5 text-xs text-soft" dir="auto">{reasonText(rec)}</p>
      {progress !== undefined && progress > 0 && <ProgressBar value={progress} className="mt-2" />}
    </li>
  )
}

/**
 * A short "continue" and "recommended next" on the dashboard, from the same
 * server-side recommendations as Learn. It renders nothing when there is nothing
 * to say or the request fails: the dashboard never depends on it.
 */
export function LearningSuggestions() {
  const { t } = useI18n()
  const [recs, setRecs] = useState<Recommendations | null>(null)

  useEffect(() => {
    let alive = true
    api.getRecommendations().then((r) => alive && setRecs(r)).catch(() => {})
    return () => {
      alive = false
    }
  }, [])

  const groups = [
    { key: 'continue', title: t('hub.yourLearning'), items: (recs?.continue_learning ?? []).slice(0, MAX_EACH) },
    { key: 'next', title: t('hub.recommended'), items: (recs?.recommended_next ?? []).slice(0, MAX_EACH) },
  ].filter((g) => g.items.length > 0)
  if (groups.length === 0) return null

  return (
    <section aria-label={t('hub.title')} className="grid gap-4 md:grid-cols-2">
      {groups.map((g, i) => (
        // The first card is the walkthrough's "learn" step: what to continue, or for an account
        // with nothing under way yet, what to start.
        <Card key={g.key} data-tour={i === 0 ? 'learn' : undefined} className="p-5">
          <div className="mb-3 flex items-center justify-between gap-2">
            <h2 className="text-sm font-semibold text-bright">{g.title}</h2>
            <Link href="/learn" className="inline-flex items-center gap-1 text-xs text-amber-text hover:text-amber-text2">
              {t('nav.learn')} <ArrowRight size={11} className="rtl:rotate-180" aria-hidden="true" />
            </Link>
          </div>
          <ul className="divide-y divide-border">
            {g.items.map((rec) => <Row key={rec.course.id} rec={rec} />)}
          </ul>
        </Card>
      ))}
    </section>
  )
}
