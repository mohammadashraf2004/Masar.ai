import Link from 'next/link'
import { Check } from 'lucide-react'
import { Card } from '@/components/ui/index'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { pick } from '@/lib/content-language'
import type { ModuleLessonRow } from './mockLesson'

/** Arabic-Indic digits for the row number, matching every other mono number
 *  in the reader (see `lesson.readTime` and the track pages). */
const ARABIC_DIGITS = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
function localizedNumber(n: number, language: string): string {
  const digits = String(n)
  return language === 'ar' ? digits.replace(/\d/g, d => ARABIC_DIGITS[Number(d)]) : digits
}

/** "دروس الوحدة" — the sticky module lesson list next to the article. Done
 *  rows link to their own lesson page; the current row is a highlighted
 *  non-link; locked rows render but are not clickable. */
export function LessonAside({ courseSlug, lessons }: { courseSlug: string; lessons: ModuleLessonRow[] }) {
  const { t, language } = useI18n()

  return (
    <aside className="w-full shrink-0 lg:sticky lg:top-16 lg:w-56 xl:w-60">
      <Card className="max-h-[calc(100dvh-6rem)] space-y-1 overflow-y-auto p-3">
      <p className="mb-2 text-lc-label font-semibold uppercase tracking-wider text-ghost">
        {t('lessons.moduleLessons')}
      </p>
      {lessons.map(row => {
        const title = pick(row.title, row.title_ar, language)
        const number = <span className="w-4 shrink-0 font-mono text-xs text-ghost" dir="ltr">{localizedNumber(row.order, language)}</span>

        if (row.status === 'locked') {
          return (
            <div
              key={row.id}
              className="flex items-center gap-2 rounded-lg px-2 py-2.5 text-sm text-ghost"
              aria-disabled="true"
            >
              {number}
              <span className="min-w-0 flex-1 truncate" dir="auto">{title}</span>
            </div>
          )
        }

        const isCurrent = row.status === 'current'
        return (
          <Link
            key={row.id}
            href={`/courses/${courseSlug}/lessons/${row.id}`}
            aria-current={isCurrent ? 'page' : undefined}
            className={cn(
              'flex items-center gap-2 rounded-lg px-2 py-2.5 text-sm transition-colors',
              isCurrent ? 'bg-amber-soft font-semibold text-amber-text' : 'text-bright hover:bg-surface',
            )}
          >
            {number}
            <span className="min-w-0 flex-1 truncate" dir="auto">{title}</span>
            {row.status === 'done' && <Check size={13} className="shrink-0 text-bright" aria-hidden="true" />}
            {isCurrent && <span className="size-1.5 shrink-0 rounded-full bg-amber-text" aria-hidden="true" />}
          </Link>
        )
      })}
      </Card>
    </aside>
  )
}
