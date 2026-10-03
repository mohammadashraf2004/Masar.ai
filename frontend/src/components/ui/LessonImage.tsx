'use client'
import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { X, ZoomIn } from 'lucide-react'
import { resolveAssetUrl } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import type { ImageBlock } from '@/types'

/**
 * One figure of a lesson, rendered where the lesson's author placed it.
 *
 * The image sits on a light panel in both themes: these are diagrams and
 * screenshots drawn for a white page, and a transparent PNG with dark lines
 * would vanish on the dark theme. It scales down to the column and never
 * up (a small diagram stays small and centred), reserves its space from the
 * declared size so nothing jumps as it loads, and loads only when it is about
 * to be seen.
 *
 * Activating it opens a full-window view: on a desktop the figure is fitted to
 * the window, on a phone it takes the full width and scrolls, so a dense
 * diagram can be read and pinch-zoomed. Escape, the close button or a tap
 * outside the figure closes it and focus returns to the figure.
 *
 * The caption reads "Figure 4.2 — ..." when the course numbers its figures and
 * is the caption alone otherwise; the alt text is the description a screen
 * reader gets.
 */
export function LessonImage({ block }: { block: ImageBlock }) {
  const { t } = useI18n()
  const [open, setOpen] = useState(false)
  const [failed, setFailed] = useState(false)
  const trigger = useRef<HTMLButtonElement>(null)
  const src = resolveAssetUrl(block.url)
  const caption = [block.figure_number, block.caption].filter(Boolean).join(' — ')

  return (
    <figure className="lesson-figure" data-figure={block.asset_key}>
      {failed ? (
        <div
          role="img"
          aria-label={block.alt}
          className="mx-auto flex min-h-[8rem] max-w-full items-center justify-center rounded-lg border border-dashed border-border bg-surface px-4 py-6 text-center text-sm text-soft"
        >
          {t('lesson.figureUnavailable')}
        </div>
      ) : (
        <button
          ref={trigger}
          type="button"
          onClick={() => setOpen(true)}
          aria-haspopup="dialog"
          aria-label={`${t('lesson.figureZoom')}: ${block.alt}`}
          className="group relative mx-auto block min-h-[44px] w-fit max-w-full cursor-zoom-in rounded-lg border border-border bg-white p-2 sm:p-3"
        >
          {/* eslint-disable-next-line @next/next/no-img-element -- served by the API, not by next/image */}
          <img
            src={src}
            alt={block.alt}
            width={block.width ?? undefined}
            height={block.height ?? undefined}
            loading="lazy"
            decoding="async"
            onError={() => setFailed(true)}
            className="block h-auto max-w-full"
          />
          <span
            aria-hidden="true"
            className="pointer-events-none absolute end-3 top-3 flex h-8 w-8 items-center justify-center rounded-full bg-black/60 text-white opacity-100 transition-opacity sm:opacity-0 sm:group-hover:opacity-100 sm:group-focus-visible:opacity-100"
          >
            <ZoomIn size={16} />
          </span>
        </button>
      )}
      {caption && (
        <figcaption dir="auto" className="mx-auto mt-2 max-w-[var(--lc-measure)] text-center text-sm text-soft">
          {caption}
        </figcaption>
      )}
      {open && (
        <Lightbox src={src} alt={block.alt} caption={caption} onClose={() => setOpen(false)} returnFocus={trigger} />
      )}
    </figure>
  )
}

function Lightbox({ src, alt, caption, onClose, returnFocus }: {
  src: string
  alt: string
  caption: string
  onClose: () => void
  returnFocus: React.RefObject<HTMLButtonElement | null>
}) {
  const { t } = useI18n()
  const closeButton = useRef<HTMLButtonElement>(null)
  const close = useRef(onClose)
  useEffect(() => {
    close.current = onClose
  })

  useEffect(() => {
    const opener = returnFocus.current
    const scroll = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    closeButton.current?.focus()

    function onKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        e.preventDefault()
        close.current()
      } else if (e.key === 'Tab') {
        // The close button is the only control: keep focus on it.
        e.preventDefault()
        closeButton.current?.focus()
      }
    }
    document.addEventListener('keydown', onKeyDown)
    return () => {
      document.removeEventListener('keydown', onKeyDown)
      document.body.style.overflow = scroll
      if (opener && document.contains(opener)) opener.focus()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- once per open, by design
  }, [])

  return createPortal(
    <div
      role="dialog"
      aria-modal="true"
      aria-label={alt}
      className="fixed inset-0 z-[60] flex flex-col bg-scrim/90"
      onClick={onClose}
      data-testid="figure-lightbox"
    >
      <div className="flex shrink-0 justify-end p-2 sm:p-4">
        <button
          ref={closeButton}
          type="button"
          onClick={onClose}
          aria-label={t('common.close')}
          className="flex h-11 w-11 items-center justify-center rounded-full bg-black/60 text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
        >
          <X size={20} aria-hidden="true" />
        </button>
      </div>
      <div className="flex min-h-0 flex-1 items-start justify-center overflow-auto px-2 pb-4 sm:items-center sm:px-6">
        {/* eslint-disable-next-line @next/next/no-img-element -- served by the API, not by next/image */}
        <img
          src={src}
          alt={alt}
          onClick={(e) => e.stopPropagation()}
          className="h-auto w-full rounded bg-white object-contain sm:max-h-[85vh] sm:w-auto sm:max-w-[95vw]"
        />
      </div>
      {caption && (
        <p dir="auto" className="shrink-0 px-4 pb-4 text-center text-sm text-white/90">
          {caption}
        </p>
      )}
    </div>,
    document.body,
  )
}
