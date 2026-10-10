'use client'

import { useCallback, useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { ArrowLeft, ArrowRight } from 'lucide-react'
import { AppShell } from '@/components/layout/AppShell'
import { PageBody } from '@/components/layout/PageContainer'
import { TrackWorkflowPath } from '@/components/learning/TrackWorkflowPath'
import { api } from '@/lib/api'
import { localizedDescription, localizedTitle } from '@/lib/content-language'
import { useI18n } from '@/lib/i18n'
import { useAuthStore } from '@/lib/store'
import { cn } from '@/lib/utils'
import type { CareerTrack, CareerTrackSummary } from '@/types'
import { normalizedTrack } from '@/features/tracks/TrackCard'

function DetailSkeleton({ label }: { label: string }) {
  return (
    <div className="animate-pulse space-y-4" aria-label={label}>
      <div className="h-11 rounded-xl bg-surface" />
      <div className="h-64 rounded-[14px] bg-surface" />
      <div className="h-[520px] rounded-xl bg-surface" />
    </div>
  )
}

export default function TrackDetailPage() {
  const { slug } = useParams() as { slug: string }
  const { t, language, dir } = useI18n()
  const authLoading = !useAuthStore(state => state._hasHydrated)
  const [track, setTrack] = useState<CareerTrack | null>(null)
  const [tabs, setTabs] = useState<CareerTrackSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    setError(false)
    try {
      const [detail, all] = await Promise.all([api.getTrack(slug), api.listTracks()])
      setTrack(detail)
      setTabs(all)
    } catch {
      setError(true)
    } finally {
      setLoading(false)
    }
  }, [slug])

  useEffect(() => {
    document.querySelector<HTMLElement>('[data-page-scroll]')?.scrollTo({ top: 0 })
    window.scrollTo({ top: 0 })
    if (authLoading) return
    const timer = window.setTimeout(() => { void load() }, 0)
    return () => window.clearTimeout(timer)
  }, [authLoading, load])

  const Back = dir === 'rtl' ? ArrowRight : ArrowLeft

  return (
    <AppShell>
      <PageBody footer={false}>
        {authLoading || loading ? <DetailSkeleton label={t('tracks.detailLoading')} /> : error || !track ? (
          <div className="rounded-xl border border-border bg-surface p-10 text-center">
            <p className="mb-4 text-sm text-dim">{t('tracks.detailError')}</p>
            <button onClick={() => void load()} className="h-11 rounded-lg border border-amber px-5 text-sm font-semibold text-amber-text">{t('common.retry')}</button>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex items-center gap-2">
              <Link href="/tracks" aria-label={t('tracks.back')} className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border border-border bg-surface text-bright hover:border-amber hover:text-amber-text">
                <Back size={17} aria-hidden="true" />
              </Link>
              <nav className="flex min-w-0 flex-1 gap-1 overflow-x-auto rounded-xl border border-border bg-surface p-1" aria-label={t('tracks.switcher')}>
                {tabs.map((tab) => (
                  <Link
                    key={tab.slug}
                    href={`/tracks/${tab.slug}`}
                    className={cn(
                      'shrink-0 rounded-lg px-4 py-2 font-display text-xs font-semibold whitespace-nowrap',
                      tab.slug === track.slug ? 'bg-amber text-on-amber' : 'text-dim hover:bg-panel hover:text-white',
                    )}
                  >{localizedTitle({ title: tab.title_en || tab.title, title_ar: tab.title_ar }, language)}</Link>
                ))}
              </nav>
            </div>
            <TrackHeader track={track} />
            <TrackWorkflowPath goal={track.slug} />
          </div>
        )}
      </PageBody>
    </AppShell>
  )
}

function TrackHeader({ track }: { track: CareerTrack }) {
  const { t, tf, language } = useI18n()
  const item = normalizedTrack(track)
  const title = localizedTitle({ title: item.title_en, title_ar: item.title_ar }, language)
  const description = localizedDescription(item, language)
  const progressLabel = item.status === 'done'
    ? t('tracks.progress.done')
    : item.status === 'current' ? t('tracks.progress.current') : t('tracks.progress.new')

  return (
    <section className={cn(
      'rounded-[14px] border bg-surface p-5 sm:p-7',
      item.status === 'current' ? 'border-amber shadow-[0_0_0_4px_rgb(var(--acc)/var(--acc-soft-a))]' : 'border-border',
    )}>
      <h1 dir="auto" className="ui-page-title">{title}</h1>
      <p dir="auto" className="ui-description mt-3 max-w-3xl">{description}</p>
      <div className="ui-caption mt-4 flex flex-wrap gap-x-2 gap-y-1">
        <span>{tf('tracks.courseCount', { n: item.course_count })}</span>
        <span>·</span>
        <span>{tf('tracks.hourCount', { n: item.hours })}</span>
      </div>
      <div className="mt-6 border-t border-border pt-4">
        <div className="mb-2 flex items-center justify-between text-caption">
          <span className="text-dim">{progressLabel}</span>
          <span dir="ltr" className="font-mono text-amber-text">{Math.round(item.progress)}%</span>
        </div>
        <div className="h-1 overflow-hidden rounded-sm bg-panel" role="progressbar" aria-valuenow={Math.round(item.progress)} aria-valuemin={0} aria-valuemax={100}>
          <div className={cn('h-full', item.status === 'done' ? 'bg-emerald' : 'bg-amber')} style={{ width: `${item.progress}%` }} />
        </div>
      </div>
    </section>
  )
}
