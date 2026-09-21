'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { CourseCard } from '@/components/learning/CourseCard'
import { buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { localizedName } from '@/lib/learning'
import { useI18n } from '@/lib/i18n'
import type { CatalogCourseDetail } from '@/types'

/**
 * A course in the catalogue: why it matters (level, fields, skills, the career
 * goals it serves) and where to open its lessons. The lessons themselves stay on
 * their existing pages — the catalogue entry points at them, it never copies
 * them — so this page is the "front door" to a track level or tool course.
 */
export default function CoursePage() {
  const { isLoading: authLoading } = useAuth()
  const { slug } = useParams() as { slug: string }
  const { t, language } = useI18n()
  const [course, setCourse] = useState<CatalogCourseDetail | null>(null)
  const [state, setState] = useState<'loading' | 'ready' | 'missing'>('loading')

  useEffect(() => {
    if (authLoading) return
    api.getCatalogCourse(slug)
      .then((c) => {
        setCourse(c)
        setState('ready')
      })
      .catch(() => setState('missing'))
  }, [authLoading, slug])

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  return (
    <AppShell>
      <PageHeader title={course ? localizedName(course, language) : t('nav.explore')} />
      <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl space-y-4">
          {state === 'loading' && <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>}
          {state === 'missing' && (
            <Card className="p-8 text-center">
              <p className="mb-4 text-sm text-ghost">{t('card.notFound')}</p>
              <Link href="/explore" className={buttonStyles({ variant: 'ghost', size: 'sm' })}>{t('nav.explore')}</Link>
            </Card>
          )}
          {state === 'ready' && course && <CourseCard course={course} defaultOpen />}
        </div>
      </div>
    </AppShell>
  )
}
