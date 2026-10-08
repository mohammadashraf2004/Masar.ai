'use client'
import Link from 'next/link'
import { X } from 'lucide-react'
import { LogoMark } from '@/components/layout/Logo'
import { MentorMessageView } from '@/features/mentor/MentorMessageView'
import { useI18n, useMentorV2I18n, type StringKey } from '@/lib/i18n'
import type { PanelExchange } from './useLessonMentor'

/**
 * The mentor beside the lesson: a side panel from the desktop width, a bottom sheet on a phone. Each
 * exchange shows the quoted selection (a `--card2` block with a 2px amber edge), then the mentor's
 * answer with its intent tag, grounding pill and an optional quick-check question.
 */
export function LessonMentorPanel({
  lessonNumber,
  courseId,
  lessonId,
  exchanges,
  loading,
  failed,
  onClose,
  onRetry,
  onFollowUp,
}: {
  lessonNumber: number
  courseId: string
  lessonId: string
  exchanges: PanelExchange[]
  loading: boolean
  /** Why the last question failed (the message to show), or null. */
  failed: StringKey | null
  onClose: () => void
  onRetry: () => void
  /** The learner answered a quick-check question in the panel. */
  onFollowUp: (answer: string) => void
}) {
  const { t, tf, n } = useMentorV2I18n()
  const { t: tMain } = useI18n()

  return (
    <aside
      aria-label={t('mentor.v2.panel.title')}
      data-testid="lesson-mentor-panel"
      // A 360px panel (280px at the least) docked at the end edge, below the header. It is fixed rather than a
      // third column of the lesson's row: that row is 1024px wide and already holds the article and the module
      // list, so in the flow the panel wrapped to the bottom of the page, below the fold. A phone gets a bottom sheet.
      className="fixed z-[60] flex w-[360px] min-w-[280px] max-w-[calc(100vw-2rem)] flex-col gap-3 rounded-xl border border-border bg-surface p-4 shadow-[0_8px_24px_rgba(0,0,0,.35)] end-4 top-20 bottom-4 max-[899px]:inset-x-0 max-[899px]:bottom-0 max-[899px]:end-auto max-[899px]:top-auto max-[899px]:max-h-[75dvh] max-[899px]:w-auto max-[899px]:min-w-0 max-[899px]:max-w-none max-[899px]:overflow-y-auto max-[899px]:rounded-b-none max-[899px]:pb-[max(1rem,env(safe-area-inset-bottom))]"
    >
      <header className="flex items-center gap-2.5">
        <LogoMark size={30} label={null} />
        <div className="min-w-0 flex-1">
          <p className="text-sm font-semibold text-white">{t('mentor.v2.panel.title')}</p>
          <p className="text-xs text-ghost">{tf('mentor.v2.panel.lesson', { n: n(lessonNumber) })}</p>
        </div>
        <button
          type="button"
          aria-label={t('mentor.v2.panel.close')}
          onClick={onClose}
          className="grid h-11 w-11 place-items-center rounded-lg text-dim hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
        >
          <X size={16} aria-hidden="true" />
        </button>
      </header>

      <div className="flex min-h-0 flex-1 flex-col gap-3 overflow-y-auto" aria-live="polite">
        {exchanges.map((exchange, i) => (
          <div key={i} className="flex flex-col gap-2.5">
            {exchange.quote && (
              <blockquote
                dir="auto"
                aria-label={t('mentor.v2.panel.quote')}
                className="rounded-lg border-s-2 border-amber bg-panel px-3 py-2 text-[13px] leading-[1.7] text-soft"
              >
                {exchange.quote}
              </blockquote>
            )}
            {exchange.reply
              ? <MentorMessageView message={exchange.reply} actions={{ onCheckAnswer: (answer) => onFollowUp(answer) }} />
              : <p role="status" className="text-[13px] text-ghost">{t('mentor.v2.typing')}</p>}
          </div>
        ))}

        {failed && !loading && (
          <div role="alert" className="flex flex-wrap items-center gap-3 rounded-xl border border-rose/40 bg-panel px-3 py-2.5 text-[13px] text-soft">
            <span>{tMain(failed)}</span>
            <button type="button" onClick={onRetry} className="min-h-[44px] rounded-lg border border-border px-3 text-bright hover:border-amber/40">{t('mentor.v2.retry')}</button>
          </div>
        )}
      </div>

      <Link href={`/mentor?courseId=${encodeURIComponent(courseId)}&lessonId=${encodeURIComponent(lessonId)}`} className="min-h-[44px] self-start py-3 text-xs font-medium text-amber-text underline-offset-2 hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring lg:min-h-0 lg:py-0">
        {t('mentor.v2.panel.open')}
      </Link>
    </aside>
  )
}
