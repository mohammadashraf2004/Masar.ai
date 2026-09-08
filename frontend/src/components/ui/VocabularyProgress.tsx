'use client'
import { useEffect } from 'react'
import Link from 'next/link'
import { Check, Circle } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { ProgressBar } from '@/components/ui/index'
import { useVocabularyStore } from '@/lib/vocabulary'
import { TERM_LIST } from '@/content/terminology'

/**
 * "Your AI Vocabulary" — the employability half of the Arabic-first bet made
 * visible. Arabic gets the concept across; this tracks whether the student
 * can also *name* it the way the industry does.
 *
 * A term counts as learned once the student has answered something about it
 * or marked it from the glossary; merely reading a lesson only marks it
 * encountered.
 */
export function VocabularyProgress({
  className,
  limit = 8,
  showList = true,
}: {
  className?: string
  /** How many terms to list under the bar. */
  limit?: number
  showList?: boolean
}) {
  const { t } = useI18n()
  const learned = useVocabularyStore((s) => s.learned)
  const encountered = useVocabularyStore((s) => s.encountered)
  const load = useVocabularyStore((s) => s.load)

  useEffect(() => {
    load()
  }, [load])

  const total = TERM_LIST.length
  const learnedCount = learned.size
  const pct = total === 0 ? 0 : Math.round((learnedCount / total) * 100)

  // Learned first, then terms they've met but not mastered — that second
  // group is the actionable one.
  const ordered = [...TERM_LIST].sort((a, b) => {
    const score = (id: string) => (learned.has(id) ? 2 : encountered.has(id) ? 1 : 0)
    return score(b.id) - score(a.id) || a.en.localeCompare(b.en)
  })

  return (
    <div className={cn('rounded-lg bg-panel border border-border p-4', className)}>
      <div className="flex items-baseline justify-between gap-2 mb-2">
        <h3 className="text-sm font-medium text-bright">{t('term.glossaryTitle')}</h3>
        <span className="text-xs font-mono text-amber">{pct}%</span>
      </div>

      <ProgressBar value={pct} size="md" color={pct >= 80 ? 'emerald' : 'amber'} />

      <p className="text-xs text-ghost mt-2">
        <span className="font-mono text-soft">
          {learnedCount} / {total}
        </span>{' '}
        {t('term.progress')}
      </p>

      {showList && (
        <ul className="mt-3 space-y-1.5">
          {ordered.slice(0, limit).map((term) => {
            const isLearned = learned.has(term.id)
            return (
              <li key={term.id} className="flex items-center gap-2 text-xs">
                {isLearned ? (
                  <Check size={11} className="text-emerald shrink-0" />
                ) : (
                  <Circle size={9} className="text-ghost shrink-0" />
                )}
                <span className={cn(isLearned ? 'text-soft' : 'text-ghost')} dir="ltr">
                  {term.preferred}
                </span>
              </li>
            )
          })}
        </ul>
      )}

      <Link
        href="/glossary"
        className="inline-block mt-3 text-xs text-amber hover:text-amber2 transition-colors"
      >
        {t('nav.glossary')} →
      </Link>
    </div>
  )
}
