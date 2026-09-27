'use client'
import { useEffect, useRef } from 'react'
import { createPortal } from 'react-dom'
import { useI18n } from '@/lib/i18n'

/** How long the note stays before it clears itself. */
const SHOWN_FOR_MS = 12_000

/**
 * What a tour leaves behind when it ends, finished or skipped: a note that it can be
 * played again from Help, with the button to do it now.
 */
export function ReplayBar({ onReplay, onDismiss }: { onReplay: () => void; onDismiss: () => void }) {
  const { t, dir } = useI18n()

  // The timer must not restart every time the caller renders.
  const dismiss = useRef(onDismiss)
  useEffect(() => { dismiss.current = onDismiss })
  useEffect(() => {
    const timer = setTimeout(() => dismiss.current(), SHOWN_FOR_MS)
    return () => clearTimeout(timer)
  }, [])

  if (typeof document === 'undefined') return null
  return createPortal(
    <div role="status" dir={dir} className="tour-replay">
      <span className="text-[13px]" style={{ color: 'var(--tt)' }}>{t('tour.done')}</span>
      <button
        type="button"
        onClick={onReplay}
        className="tour-ghost flex min-h-[44px] items-center rounded-lg px-3 text-[13px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
        style={{ border: '1px solid var(--tl)', color: 'var(--th)' }}
      >
        {t('tour.replay')}
      </button>
    </div>,
    document.body,
  )
}
