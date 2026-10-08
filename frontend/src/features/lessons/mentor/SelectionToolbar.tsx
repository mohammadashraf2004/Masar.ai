'use client'
import { useEffect, useState, type RefObject } from 'react'
import { LogoMark } from '@/components/layout/Logo'
import type { MentorIntent } from '@/features/mentor/types'
import { useMentorV2I18n, type MentorV2Key } from '@/lib/i18n'

export const MIN_WORDS = 3

export const SELECTION_ACTIONS: { key: 'explain' | 'simplify' | 'example' | 'why' | 'quiz'; intent: MentorIntent }[] = [
  { key: 'explain', intent: 'EXPLAIN' },
  { key: 'simplify', intent: 'SIMPLIFY' },
  // "Give an example" is an explanation with an example; the server has no separate intent for it.
  { key: 'example', intent: 'EXPLAIN' },
  { key: 'why', intent: 'WHY' },
  { key: 'quiz', intent: 'QUIZ' },
]

export function wordCount(text: string): number {
  return text.trim().split(/\s+/).filter(Boolean).length
}

interface Anchor { text: string; top: number; left: number }

/**
 * The floating toolbar over selected lesson text. It appears only for a selection of three or more
 * words that lies inside the lesson article, above the selection; Esc or any scroll hides it.
 * The five actions send the selection (not the whole lesson) to the mentor with an explicit intent.
 */
export function SelectionToolbar({
  articleRef,
  onAsk,
}: {
  articleRef: RefObject<HTMLElement>
  onAsk: (intent: MentorIntent, selectedText: string, label: string) => void
}) {
  const { t } = useMentorV2I18n()
  const [anchor, setAnchor] = useState<Anchor | null>(null)

  useEffect(() => {
    function read() {
      const selection = window.getSelection()
      const article = articleRef.current
      if (!selection || selection.rangeCount === 0 || selection.isCollapsed || !article) return setAnchor(null)
      const range = selection.getRangeAt(0)
      // Only inside the article: a selection in the sidebar, the header or the exercise gets no toolbar.
      if (!article.contains(range.commonAncestorContainer)) return setAnchor(null)
      const text = selection.toString().trim()
      if (wordCount(text) < MIN_WORDS) return setAnchor(null)
      const rect = typeof range.getBoundingClientRect === 'function' ? range.getBoundingClientRect() : null
      const top = rect ? Math.max(8, rect.top - 52) : 8
      const left = rect ? Math.min(Math.max(rect.left + rect.width / 2, 160), window.innerWidth - 160) : window.innerWidth / 2
      setAnchor({ text, top, left })
    }
    const hide = () => setAnchor(null)
    const onKey = (event: KeyboardEvent) => { if (event.key === 'Escape') hide() }
    document.addEventListener('selectionchange', read)
    document.addEventListener('keydown', onKey)
    // Capture: the lesson scrolls inside its own container, and scroll events do not bubble.
    document.addEventListener('scroll', hide, true)
    return () => {
      document.removeEventListener('selectionchange', read)
      document.removeEventListener('keydown', onKey)
      document.removeEventListener('scroll', hide, true)
    }
  }, [articleRef])

  if (!anchor) return null

  return (
    <div
      role="toolbar"
      aria-label={t('mentor.v2.selection.label')}
      data-testid="selection-toolbar"
      // Pressing a button must not collapse the selection it is about.
      onMouseDown={(e) => e.preventDefault()}
      style={{ position: 'fixed', top: anchor.top, left: anchor.left, transform: 'translateX(-50%)' }}
      className="z-[70] flex max-w-[calc(100vw-16px)] items-center gap-1 overflow-x-auto rounded-[10px] bg-white p-1 shadow-[0_8px_24px_rgba(0,0,0,.35)]"
    >
      <span className="grid shrink-0 place-items-center px-1"><LogoMark size={30} label={null} /></span>
      {SELECTION_ACTIONS.map(({ key, intent }) => {
        const label = t(`mentor.v2.selection.${key}` as MentorV2Key)
        return (
          <button
            key={key}
            type="button"
            onClick={() => { onAsk(intent, anchor.text, label); setAnchor(null) }}
            className="min-h-[34px] shrink-0 whitespace-nowrap rounded-md px-2.5 text-[13px] text-void transition-colors hover:bg-amber hover:text-on-amber focus-visible:bg-amber focus-visible:text-on-amber focus-visible:outline-none"
          >
            {label}
          </button>
        )
      })}
    </div>
  )
}
