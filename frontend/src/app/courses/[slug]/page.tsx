'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { Check, Lock } from 'lucide-react'
import { useSession } from '@/hooks/useAuth'
import { useRequireAuth } from '@/components/auth/AuthPrompt'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { CourseEnroll } from '@/components/learning/CourseEnroll'
import { CourseOutline } from '@/components/learning/CourseOutline'
import { CourseReadiness } from '@/components/learning/CourseReadiness'
import { ReadinessCheck } from '@/components/learning/ReadinessCheck'
import { buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { localizedName } from '@/lib/learning'
import { useI18n } from '@/lib/i18n'
import type { CatalogCourseDetail, CourseAccess, ReadinessReport } from '@/types'

/**
 * One course, on its own. It is reached from the catalogue, a roadmap or a
 * recommendation, and needs none of them: any published course can be opened,
 * read about and enrolled in directly, with no track or career goal chosen.
 *
 * The page shows what the course is (outline), how ready this learner is for it
 * (advice, computed by the server from their own progress) and how to start. A paid
 * course also shows its price; the server, not this page, decides who has access.
 * The lessons stay on their existing pages: the catalogue entry points at them.
 */
export default function CoursePage() {
  // Public: anyone may read what a course is. Starting it needs an account, and
  // what a signed-in learner may open is the server's answer (Free/Pro, owned).
  const { isLoading: authLoading, isAuthenticated } = useSession()
  const requireAuth = useRequireAuth()
  const { slug } = useParams() as { slug: string }
  const { t, language } = useI18n()
  const [course, setCourse] = useState<CatalogCourseDetail | null>(null)
  const [state, setState] = useState<'loading' | 'ready' | 'missing'>('loading')
  const [access, setAccess] = useState<CourseAccess | null>(null)
  const [readiness, setReadiness] = useState<ReadinessReport | null>(null)
  const [checking, setChecking] = useState(false)

  useEffect(() => {
    if (authLoading) return
    api.getCatalogCourse(slug)
      .then(async (c) => {
        setCourse(c)
        if (!isAuthenticated) {
          // No account, no access or readiness to ask about.
          setState('ready')
          return
        }
        const ownership = await api.getCourseAccess(slug)
        setAccess(ownership)
        setState('ready')
        // Readiness is advice: a failure to load it must never hide the course.
        if (c.is_available) {
          try { setReadiness(await api.getCourseReadiness(slug)) } catch { setReadiness(null) }
        }
      })
      .catch(() => setState('missing'))
  }, [authLoading, isAuthenticated, slug])

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  const canLearn = !!course && access?.has_access === true
  const canPreview = !!course && (access?.free_lesson_count ?? 0) > 0

  return (
    <AppShell>
      <PageHeader title={course ? localizedName(course, language) : t('nav.explore')} dirAuto contained />
      <PageBody>
        {state === 'loading' && <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>}
        {state === 'missing' && (
          <Card className="space-y-3 p-8 text-center">
            <p className="text-sm text-soft">{t('card.notFound')}</p>
            <Link href="/explore" className={buttonStyles({ variant: 'ghost', size: 'sm' })}>{t('nav.explore')}</Link>
          </Card>
        )}
        {state === 'ready' && course && (
          <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_22rem]">
            <div className="min-w-0 lg:order-1"><CourseOutline course={course} /></div>

            <aside className="space-y-4 lg:order-2 lg:self-start">
              <Card className="space-y-4 p-5">
                {!isAuthenticated ? (
                  <>
                    <p className="text-sm text-bright">{t('gate.lessonsAfterSignIn')}</p>
                    <button
                      type="button"
                      onClick={() => requireAuth(`/courses/${slug}`)}
                      className={buttonStyles({ variant: 'amber', size: 'lg', className: 'w-full' })}
                    >
                      {t('gate.startLearning')}
                    </button>
                  </>
                ) : canLearn ? (
                  <p className="flex items-center gap-2 text-sm text-emerald">
                    <Check size={16} aria-hidden="true" />
                    {access?.reason === 'pro' ? t('course.proAccess') : t('course.owned')}
                  </p>
                ) : (
                  <>
                    <p className="text-sm text-bright">{t('course.freePreview')}</p>
                    {canPreview && (
                      <Link href={`/courses/${slug}/learn`} className={buttonStyles({ variant: 'ghost', size: 'lg' })}>
                        {t('course.startFreeLessons')}
                      </Link>
                    )}
                    <Link href="/billing" className={buttonStyles({ variant: 'amber', size: 'lg' })}>
                      <Lock size={15} aria-hidden="true" /> {t('course.upgradePro')}
                    </Link>
                  </>
                )}
              </Card>

              {canLearn && (
                <CourseEnroll
                  course={course}
                  readinessState={readiness?.state}
                  onEnrolled={(done) => setReadiness(done.readiness)}
                />
              )}

              {readiness && (
                <CourseReadiness report={readiness} onTakeCheck={checking ? undefined : () => setChecking(true)} />
              )}
              {checking && (
                <ReadinessCheck slug={slug} onResult={setReadiness} onClose={() => setChecking(false)} />
              )}
            </aside>
          </div>
        )}
      </PageBody>
    </AppShell>
  )
}
