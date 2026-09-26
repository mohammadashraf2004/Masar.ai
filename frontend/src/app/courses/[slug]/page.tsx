'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import axios from 'axios'
import { Check, Lock } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageBody } from '@/components/layout/PageContainer'
import { CourseEnroll } from '@/components/learning/CourseEnroll'
import { CourseOutline } from '@/components/learning/CourseOutline'
import { CourseReadiness } from '@/components/learning/CourseReadiness'
import { ReadinessCheck } from '@/components/learning/ReadinessCheck'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { localizedName } from '@/lib/learning'
import { useI18n, type StringKey } from '@/lib/i18n'
import type { CatalogCourseDetail, CourseAccess, CourseOffer, ReadinessReport } from '@/types'

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
  const { isLoading: authLoading } = useAuth()
  const { slug } = useParams() as { slug: string }
  const { t, language } = useI18n()
  const [course, setCourse] = useState<CatalogCourseDetail | null>(null)
  const [state, setState] = useState<'loading' | 'ready' | 'missing'>('loading')
  const [offer, setOffer] = useState<CourseOffer | null>(null)
  const [access, setAccess] = useState<CourseAccess | null>(null)
  const [readiness, setReadiness] = useState<ReadinessReport | null>(null)
  const [checking, setChecking] = useState(false)
  const [buying, setBuying] = useState(false)
  // A message key, not text, so the message follows the reader's language if it changes.
  const [checkoutError, setCheckoutError] = useState<StringKey | ''>('')

  useEffect(() => {
    if (authLoading) return
    api.getCatalogCourse(slug)
      .then(async (c) => {
        setCourse(c)
        const ownership = await api.getCourseAccess(slug)
        setAccess(ownership)
        if (!c.is_free && !ownership.has_access) {
          try { setOffer(await api.getCourseOffer(slug)) } catch { setOffer(null) }
        }
        setState('ready')
        // Readiness is advice: a failure to load it must never hide the course.
        if (c.is_available) {
          try { setReadiness(await api.getCourseReadiness(slug)) } catch { setReadiness(null) }
        }
      })
      .catch(() => setState('missing'))
  }, [authLoading, slug])

  async function buyCourse() {
    setBuying(true)
    setCheckoutError('')
    try {
      const checkout = await api.checkoutCourse(slug)
      window.location.assign(checkout.payment_url)
    } catch (error: unknown) {
      const detail = axios.isAxiosError(error) ? error.response?.data?.detail : null
      const code = typeof detail === 'object' && detail ? detail.code : null
      if (code === 'COURSE_ALREADY_OWNED') {
        setAccess({ has_access: true, reason: 'purchase', enrollment_id: null })
        setCheckoutError('course.err.owned')
      } else if (code === 'COURSE_OFFER_UNAVAILABLE') {
        setCheckoutError('course.err.unavailable')
      } else {
        setCheckoutError('course.err.checkout')
      }
    } finally {
      setBuying(false)
    }
  }

  const price = offer
    ? new Intl.NumberFormat('en-EG', { style: 'currency', currency: offer.currency }).format(offer.price_amount / 100)
    : null

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  const canLearn = !!course && (access?.has_access || course.is_free)

  return (
    <AppShell>
      <PageHeader title={course ? localizedName(course, language) : t('nav.explore')} dirAuto contained />
      <PageBody>
        {state === 'loading' && <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>}
        {state === 'missing' && (
          <Card className="space-y-3 p-8 text-center">
            <p className="text-sm text-soft">{t('card.notFound')}</p>
            <Link href="/learn" className={buttonStyles({ variant: 'ghost', size: 'sm' })}>{t('nav.learn')}</Link>
          </Card>
        )}
        {state === 'ready' && course && (
          <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_22rem]">
            <div className="min-w-0 lg:order-1"><CourseOutline course={course} /></div>

            <aside className="space-y-4 lg:order-2 lg:self-start">
              <Card className="space-y-4 p-5">
                {canLearn ? (
                  <p className="flex items-center gap-2 text-sm text-emerald">
                    <Check size={16} aria-hidden="true" />
                    {course.is_free ? t('course.freeAccess') : t('course.owned')}
                  </p>
                ) : (
                  <>
                    <div>
                      <p className="text-2xl font-bold text-white">{price ?? t('course.priceUnavailable')}</p>
                      {offer?.original_price_amount && offer.original_price_amount > offer.price_amount && (
                        <p className="text-sm text-ghost line-through">
                          {new Intl.NumberFormat('en-EG', { style: 'currency', currency: offer.currency }).format(offer.original_price_amount / 100)}
                        </p>
                      )}
                    </div>
                    <ul className="space-y-2 text-sm text-dim">
                      {(['course.benefit.lifetime', 'course.benefit.arabic', 'course.benefit.projects', 'course.benefit.mentor', 'course.benefit.certificate'] as const).map((benefit) => (
                        <li key={benefit} className="flex items-center gap-2"><Check size={14} aria-hidden="true" className="text-emerald" />{t(benefit)}</li>
                      ))}
                    </ul>
                    <Button size="lg" loading={buying} disabled={!offer} onClick={() => void buyCourse()}>
                      <Lock size={15} aria-hidden="true" /> {t('course.buy')}
                    </Button>
                  </>
                )}
                {checkoutError && <p role="alert" className="text-sm text-rose">{t(checkoutError)}</p>}
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
