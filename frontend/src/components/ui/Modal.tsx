'use client'
import { useEffect, useId, useRef, type ReactNode, type RefObject } from 'react'
import { X } from 'lucide-react'
import { useI18n } from '@/lib/i18n'
import { cn } from '@/lib/utils'

const FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'

interface ModalProps {
  /** The dialog's accessible name; drawn as its heading. */
  title: ReactNode
  /** Its accessible description; drawn under the heading. */
  description?: ReactNode
  /** Called for Escape and the close button - "dismiss", never "confirm". */
  onClose: () => void
  /** What takes focus when it opens (the primary action). The panel itself if omitted. */
  initialFocus?: RefObject<HTMLElement | null>
  /** A small mark beside the heading. */
  icon?: ReactNode
  /** Buttons, laid out by the modal so every dialog reads the same. */
  footer?: ReactNode
  className?: string
  children?: ReactNode
}

/**
 * A modal dialog: a real `role="dialog"` with an accessible name and
 * description, focus that moves in, stays in (Tab wraps) and returns to where it
 * was, Escape to dismiss, and content that scrolls inside the panel so a short
 * phone never pushes the close button out of reach.
 *
 * Nothing behind it is dismissed by clicking the backdrop: an announcement is
 * acknowledged by a deliberate choice, not by a stray tap.
 */
export function Modal({ title, description, onClose, initialFocus, icon, footer, className, children }: ModalProps) {
  const { t } = useI18n()
  const id = useId()
  const panel = useRef<HTMLDivElement>(null)
  // Read through a ref so the effect below runs once, not on every render of the caller.
  const close = useRef(onClose)
  useEffect(() => {
    close.current = onClose
  })

  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null
    const target = initialFocus?.current ?? panel.current
    target?.focus()

    function onKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        e.preventDefault()
        close.current()
        return
      }
      if (e.key !== 'Tab' || !panel.current) return
      const items = Array.from(panel.current.querySelectorAll<HTMLElement>(FOCUSABLE))
      if (items.length === 0) {
        e.preventDefault()
        return
      }
      const first = items[0]
      const last = items[items.length - 1]
      const active = document.activeElement
      if (e.shiftKey && (active === first || active === panel.current)) {
        e.preventDefault()
        last.focus()
      } else if (!e.shiftKey && active === last) {
        e.preventDefault()
        first.focus()
      } else if (!panel.current.contains(active)) {
        e.preventDefault()
        first.focus()
      }
    }
    document.addEventListener('keydown', onKeyDown)
    return () => {
      document.removeEventListener('keydown', onKeyDown)
      // Back to what the learner was on, if it is still there.
      if (previous && document.contains(previous)) previous.focus()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- runs once per mount by design
  }, [])

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-scrim/90 p-4 backdrop-blur-sm">
      <div
        ref={panel}
        role="dialog"
        aria-modal="true"
        aria-labelledby={`${id}-title`}
        aria-describedby={description ? `${id}-desc` : undefined}
        tabIndex={-1}
        className={cn(
          'relative max-h-[calc(100dvh-2rem)] w-full max-w-lg overflow-y-auto rounded-lg border border-border bg-panel p-5 shadow-2xl outline-none sm:p-6',
          className
        )}
      >
        <button
          type="button"
          onClick={onClose}
          aria-label={t('common.close')}
          className="absolute end-1.5 top-1.5 flex h-11 w-11 items-center justify-center rounded text-soft transition-colors hover:bg-surface hover:text-bright focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
        >
          <X size={18} aria-hidden="true" />
        </button>

        <div className="flex items-start gap-3 pe-9">
          {icon && (
            <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-amber/30 bg-amber/10 text-amber-text" aria-hidden="true">
              {icon}
            </span>
          )}
          <div className="min-w-0">
            <h2 id={`${id}-title`} className="ui-card-title">{title}</h2>
            {description && <p id={`${id}-desc`} className="ui-description mt-1">{description}</p>}
          </div>
        </div>

        {children && <div className="mt-5">{children}</div>}

        {footer && (
          <div className="mt-6 flex flex-col gap-2 sm:flex-row-reverse sm:justify-start">{footer}</div>
        )}
      </div>
    </div>
  )
}
