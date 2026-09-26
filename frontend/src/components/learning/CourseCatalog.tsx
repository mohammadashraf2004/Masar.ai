'use client'
import { useEffect, useState } from 'react'
import { useLearningCatalog } from '@/hooks/useLearningCatalog'
import { Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { fieldLabel, levelLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { CatalogCourse } from '@/types'
import { CourseCard } from './CourseCard'
import { LearningLabel, useLabelContext } from './LearningLabel'

function Chip({ pressed, onClick, children }: { pressed: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      aria-pressed={pressed}
      onClick={onClick}
      className={cn(
        'min-h-[44px] rounded-full border px-3.5 py-1.5 text-sm transition-colors lg:min-h-0',
        pressed
          ? 'border-amber/50 bg-amber/10 text-amber-text'
          : 'border-border bg-panel text-soft hover:border-muted hover:text-bright'
      )}
    >
      {children}
    </button>
  )
}

/**
 * Every published course, browsable on its own: the level and category chips are
 * the platform's own vocabulary (served by the API, never listed here) and
 * filtering happens on the server, so a category added there appears here. No
 * career track is involved: a learner who has picked none sees the same
 * catalogue as everyone else, with their own progress and readiness on each card.
 */
export function CourseCatalog() {
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  const { catalog, error } = useLearningCatalog()
  const [level, setLevel] = useState<string | null>(null)
  const [field, setField] = useState<string | null>(null)
  const [courses, setCourses] = useState<CatalogCourse[] | null>(null)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    let stale = false // a slower earlier answer must never overwrite a newer one
    api.listCatalogCourses({ level: level ? [level] : [], field: field ? [field] : [] })
      .then((rows) => {
        if (stale) return
        setCourses(rows)
        setFailed(false)
      })
      .catch(() => !stale && setFailed(true))
    return () => {
      stale = true
    }
  }, [level, field])

  // A category with no course at all would be a filter that can only return nothing.
  const categories = (catalog?.fields ?? []).filter((f) => f.course_count > 0)

  return (
    <div className="space-y-5">
      {catalog && !error && (
        <div className="space-y-3">
          <div role="group" aria-label={t('cat.filter.difficulty')} className="flex flex-wrap gap-2">
            <Chip pressed={level === null} onClick={() => setLevel(null)}>{t('cat.filter.all')}</Chip>
            {catalog.levels.map((l) => (
              <Chip key={l.slug} pressed={level === l.slug} onClick={() => setLevel(level === l.slug ? null : l.slug)}>
                <LearningLabel parts={levelLabel(l, ctx)} />
              </Chip>
            ))}
          </div>
          {categories.length > 0 && (
            <div role="group" aria-label={t('cat.filter.category')} className="flex flex-wrap gap-2">
              <Chip pressed={field === null} onClick={() => setField(null)}>{t('cat.filter.all')}</Chip>
              {categories.map((f) => (
                <Chip key={f.slug} pressed={field === f.slug} onClick={() => setField(field === f.slug ? null : f.slug)}>
                  <LearningLabel parts={fieldLabel(f, ctx, true)} />
                </Chip>
              ))}
            </div>
          )}
        </div>
      )}

      {failed || error ? (
        <p role="alert" className="text-sm text-rose">{t('cat.loadError')}</p>
      ) : !courses ? (
        <div className="flex justify-center py-10"><Spinner announce /></div>
      ) : (
        <>
          <p className="text-xs text-soft" aria-live="polite">{tf('cat.count', { n: courses.length })}</p>
          {courses.length === 0 ? (
            <p className="py-10 text-center text-sm text-ghost">{t('cat.empty')}</p>
          ) : (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
              {courses.map((c) => <CourseCard key={c.id} course={c} />)}
            </div>
          )}
        </>
      )}
    </div>
  )
}
