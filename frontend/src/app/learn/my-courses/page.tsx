'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { BookOpen } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { buttonStyles } from '@/components/ui/Button'
import { Badge, Card, ProgressBar, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { pick } from '@/lib/content-language'
import { useI18n, type StringKey } from '@/lib/i18n'
import type { MyCourse } from '@/types'

/**
 * The courses this learner is enrolled in, however they got there (a purchase, an
 * admin grant, or simply enrolling in a free course). Progress is the server's
 * live number; there is no track involved.
 */
export default function MyCoursesPage() {
  const { isLoading: authLoading } = useAuth()
  const { t, tf, language } = useI18n()
  const [courses, setCourses] = useState<MyCourse[]>([])
  const [state, setState] = useState<'loading' | 'ready' | 'error'>('loading')

  useEffect(() => {
    if (authLoading) return
    api.getMyCourses()
      .then((items) => { setCourses(items); setState('ready') })
      .catch(() => setState('error'))
  }, [authLoading])

  if (authLoading) return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>

  return (
    <AppShell>
      <PageHeader title={t('mc.title')} contained />
      <PageBody>
        {state === 'loading' && <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>}
        {state === 'error' && <Card className="p-8 text-center text-sm text-rose" role="alert">{t('mc.error')}</Card>}
        {state === 'ready' && courses.length === 0 && (
          <Card className="flex flex-col items-center gap-3 p-10 text-center">
            <BookOpen size={28} className="text-ghost" aria-hidden="true" />
            <p className="text-sm text-dim">{t('mc.empty')}</p>
            <Link href="/learn" className={buttonStyles({ variant: 'ghost' })}>{t('mc.browse')}</Link>
          </Card>
        )}
        {state === 'ready' && courses.length > 0 && (
          <div className="grid gap-4 md:grid-cols-2">
            {courses.map((course) => (
              <Card key={course.course_id} className="space-y-4 p-5">
                <div>
                  <h2 className="font-display font-bold text-white" dir="auto">{pick(course.title, course.title_ar, language)}</h2>
                  <p className="mt-1 flex flex-wrap items-center gap-2 text-xs text-ghost">
                    <Badge variant={course.status === 'completed' ? 'emerald' : 'ghost'}>
                      {course.status === 'completed'
                        ? t('enr.completed')
                        : course.status === 'paused' ? t('enr.paused') : t(`mc.source.${course.access_type}` as StringKey)}
                    </Badge>
                    {course.module_count ? <span>{tf('card.modules', { n: course.module_count })}</span> : null}
                  </p>
                </div>
                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs text-dim"><span>{t('mc.progress')}</span><span>{Math.round(course.progress)}%</span></div>
                  <ProgressBar value={course.progress} />
                </div>
                <div className="flex flex-wrap gap-2">
                  <Link href={course.href || `/courses/${course.slug}`} className={buttonStyles({ size: 'sm' })}>
                    {course.status === 'completed' ? t('enr.review') : t('curriculum.continue')}
                  </Link>
                  <Link href={`/courses/${course.slug}`} className={buttonStyles({ variant: 'ghost', size: 'sm' })}>
                    {t('mc.details')}
                  </Link>
                </div>
              </Card>
            ))}
          </div>
        )}
      </PageBody>
    </AppShell>
  )
}
