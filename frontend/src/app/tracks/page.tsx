'use client'

import { useCallback, useEffect, useState } from 'react'
import { AppShell } from '@/components/layout/AppShell'
import { PageBody } from '@/components/layout/PageContainer'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { useAuthStore } from '@/lib/store'
import type { CareerTrackSummary } from '@/types'
import { TrackCard, TrackCardSkeleton } from '@/features/tracks/TrackCard'

export default function TracksPage() {
  const { t } = useI18n()
  const authLoading = !useAuthStore(state => state._hasHydrated)
  const [tracks, setTracks] = useState<CareerTrackSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    setError(false)
    try {
      setTracks(await api.listTracks())
    } catch {
      setError(true)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (authLoading) return
    const timer = window.setTimeout(() => { void load() }, 0)
    return () => window.clearTimeout(timer)
  }, [authLoading, load])

  return (
    <AppShell>
      <PageBody className="pt-1" footer={false}>
        <section className="flex flex-col gap-5 font-sans">
          <header className="flex flex-col gap-1.5">
            <h1 className="text-[26px] font-bold leading-tight text-white">{t('tracks.title')}</h1>
            <p className="max-w-4xl text-sm leading-[1.6] text-dim [text-wrap:pretty]">
              {t('tracks.subtitle')}
            </p>
          </header>

          {authLoading || loading ? (
            <div className="grid grid-cols-1 gap-4 min-[700px]:[grid-template-columns:repeat(auto-fill,minmax(320px,1fr))]" aria-label={t('tracks.loading')}>
              {Array.from({ length: 5 }, (_, index) => <TrackCardSkeleton key={index} />)}
            </div>
          ) : error ? (
            <div className="rounded-xl border border-border bg-surface p-8 text-center">
              <p className="mb-4 text-sm text-dim">{t('tracks.loadError')}</p>
              <button onClick={() => void load()} className="h-11 rounded-lg border border-amber px-5 text-sm font-semibold text-amber-text">{t('common.retry')}</button>
            </div>
          ) : tracks.length === 0 ? (
            <div className="rounded-xl border border-border bg-surface p-10 text-center text-sm text-dim">{t('tracks.empty')}</div>
          ) : (
            <div className="grid grid-cols-1 gap-4 min-[700px]:[grid-template-columns:repeat(auto-fill,minmax(320px,1fr))]">
              {tracks.map((track, index) => <TrackCard key={track.slug} track={track} index={index} />)}
            </div>
          )}
        </section>
      </PageBody>
    </AppShell>
  )
}
