import Link from 'next/link'
import { buttonStyles } from '@/components/ui/Button'
import type { CareerTrackSummary, TrackCatalogueStatus } from '@/types'
import { useI18n } from '@/lib/i18n'
import { localizedDescription, localizedTitle } from '@/lib/content-language'
import { cn } from '@/lib/utils'

export function normalizedTrack(track: CareerTrackSummary) {
  const status = track.status ?? 'open'
  return {
    ...track,
    title_en: track.title_en || track.title,
    title_ar: track.title_ar || track.title,
    description: track.description || '',
    stack: track.stack ?? [],
    stage_count: track.stage_count ?? 0,
    course_count: track.course_count ?? 0,
    hours: track.hours ?? Math.round(track.estimated_weeks * 8),
    progress: Math.max(0, Math.min(100, track.progress ?? 0)),
    status,
    cta_href: track.cta_href || (status === 'done' ? '/certificates' : `/tracks/${track.slug}`),
  }
}

export function TrackCard({ track, index }: { track: CareerTrackSummary; index: number }) {
  const { t, tf, language } = useI18n()
  const item = normalizedTrack(track)
  const title = localizedTitle({ title: item.title_en, title_ar: item.title_ar }, language)
  const description = localizedDescription(item, language)
  return (
    <article
      className={cn(
        'relative flex min-h-[346px] flex-col gap-3.5 rounded-xl border bg-surface p-[22px]',
        item.status === 'current'
          ? 'border-amber shadow-[0_0_0_4px_rgb(var(--acc)/var(--acc-soft-a))]'
          : 'border-border',
      )}
      data-status={item.status}
    >
      <Link
        href={`/tracks/${item.slug}`}
        className="absolute inset-0 rounded-xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber"
        aria-label={tf('tracks.openLabel', { title })}
      />

      <div className="pointer-events-none flex items-center justify-between">
        <span dir="ltr" className="font-mono text-xs text-amber-text">{String(index + 1).padStart(2, '0')}</span>
        <span className={cn(
          'rounded-full border px-2.5 py-0.5 text-[11px] whitespace-nowrap',
          item.status === 'done' && 'border-emerald text-emerald',
          item.status === 'current' && 'border-amber text-amber-text',
          item.status === 'open' && 'border-border text-ghost',
        )}>{t(`tracks.status.${item.status}` as const)}</span>
      </div>

      <div className="pointer-events-none flex flex-col gap-1">
        <h2 dir="auto" className="font-display text-xl font-bold text-white">{title}</h2>
      </div>

      <p dir="auto" className="pointer-events-none text-[13px] leading-[1.7] text-dim [text-wrap:pretty]">{description}</p>

      <div dir="ltr" className="pointer-events-none flex flex-wrap justify-end gap-1.5">
        {item.stack.map((name) => (
          <span key={name} className="rounded border border-border px-2 py-[3px] font-mono text-[11px] text-bright">{name}</span>
        ))}
      </div>

      <footer className="pointer-events-none mt-auto flex flex-col gap-2.5 border-t border-border pt-3.5">
        <div className="flex justify-between gap-3 text-xs text-dim">
          <span>{tf('tracks.courseCount', { n: item.course_count })} · {tf('tracks.hourCount', { n: item.hours })}</span>
          <span dir="ltr" className="font-mono">{Math.round(item.progress)}%</span>
        </div>
        <div className="h-1 overflow-hidden rounded-sm bg-panel" aria-hidden="true">
          <div
            className={cn('h-full rounded-sm', item.status === 'done' ? 'bg-emerald' : 'bg-amber')}
            style={{ width: `${item.progress}%` }}
          />
        </div>
        <Link
          href={`/tracks/${item.slug}`}
          className={buttonStyles({
            variant: item.status === 'current' ? 'amber' : 'outline',
            className: 'pointer-events-auto relative z-10 w-full',
          })}
        >{t('tracks.explore')}</Link>
      </footer>
    </article>
  )
}

export function TrackCardSkeleton() {
  return (
    <div className="min-h-[346px] animate-pulse rounded-xl border border-border bg-surface p-[22px]" aria-hidden="true">
      <div className="mb-5 flex justify-between"><span className="h-4 w-8 rounded bg-panel" /><span className="h-5 w-16 rounded-full bg-panel" /></div>
      <div className="ms-auto mb-3 h-6 w-40 rounded bg-panel" />
      <div className="mb-5 h-4 w-24 rounded bg-panel" />
      <div className="space-y-2"><div className="h-3 w-full rounded bg-panel" /><div className="h-3 w-4/5 rounded bg-panel" /></div>
      <div className="mt-6 h-7 w-3/4 rounded bg-panel" />
      <div className="mt-8 border-t border-border pt-4"><div className="h-3 w-full rounded bg-panel" /><div className="mt-4 h-11 rounded-lg bg-panel" /></div>
    </div>
  )
}
