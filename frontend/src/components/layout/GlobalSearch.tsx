'use client'
import { useEffect, useId, useRef, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Search } from 'lucide-react'
import { api } from '@/lib/api'
import { cn } from '@/lib/utils'
import { useI18n, type StringKey } from '@/lib/i18n'
import { localizedTitle } from '@/lib/content-language'
import type { SearchHit } from '@/types'

// Two letters is the smallest query the server's term expansion can do
// anything useful with; the tools page uses the same floor.
const MIN_CHARS = 2
const MAX_HITS = 8
const DEBOUNCE_MS = 250

/**
 * The header's search: courses, tools and lessons, in either language.
 *
 * It asks the same endpoint the tools page does, which expands the query through
 * the terminology dictionary on the server — "التضمينات" finds the Embeddings
 * material — so there is nothing to match on the client. Results open in a list
 * below the field; the field is an ARIA combobox and the list a listbox, so the
 * keyboard (↑ ↓ Enter Esc) and a screen reader both get the whole interaction.
 * `Ctrl K` / `⌘ K` focuses it from anywhere.
 */
export function GlobalSearch({ className }: { className?: string }) {
  const { t, language } = useI18n()
  const router = useRouter()
  const listId = useId()
  const inputRef = useRef<HTMLInputElement>(null)
  const boxRef = useRef<HTMLDivElement>(null)

  const [query, setQuery] = useState('')
  // null until something has been asked, so "nothing yet" is not "no matches".
  const [hits, setHits] = useState<SearchHit[] | null>(null)
  const [pending, setPending] = useState(false)
  const [open, setOpen] = useState(false)
  const [active, setActive] = useState(-1)

  const trimmed = query.trim()
  const searchable = trimmed.length >= MIN_CHARS

  useEffect(() => {
    if (!searchable) return
    // An answer to an earlier query must not overwrite the answer to this one.
    let stale = false
    const handle = setTimeout(async () => {
      setPending(true)
      try {
        const result = await api.search(trimmed)
        if (stale) return
        setHits(result.hits.slice(0, MAX_HITS))
        setActive(-1)
      } catch {
        if (!stale) setHits([])
      }
      if (!stale) setPending(false)
    }, DEBOUNCE_MS)
    return () => {
      stale = true
      clearTimeout(handle)
    }
  }, [trimmed, searchable])

  // Ctrl K / ⌘ K from anywhere in the shell.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault()
        inputRef.current?.focus()
        inputRef.current?.select()
      }
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [])

  // A click anywhere else closes the list.
  useEffect(() => {
    if (!open) return
    const onMouseDown = (e: MouseEvent) => {
      if (boxRef.current && !boxRef.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener('mousedown', onMouseDown)
    return () => document.removeEventListener('mousedown', onMouseDown)
  }, [open])

  const showPanel = open && searchable
  const list = hits ?? []
  const hasList = showPanel && list.length > 0

  /** Close the list and empty the field, once a result has been chosen. */
  function finish() {
    setOpen(false)
    setQuery('')
    setHits(null)
    setActive(-1)
  }

  /** Enter on the highlighted result. (A click needs only `finish`: the link navigates.) */
  function go(hit: SearchHit) {
    finish()
    router.push(hit.href)
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      if (list.length === 0) return
      e.preventDefault()
      setOpen(true)
      const step = e.key === 'ArrowDown' ? 1 : -1
      setActive((i) => (i < 0 ? (step === 1 ? 0 : list.length - 1) : (i + step + list.length) % list.length))
    } else if (e.key === 'Enter') {
      if (hasList && active >= 0) {
        e.preventDefault()
        go(list[active])
      }
    } else if (e.key === 'Escape') {
      if (open) {
        e.stopPropagation()
        setOpen(false)
      }
    }
  }

  return (
    <div ref={boxRef} className={cn('relative', className)}>
      <Search
        size={15}
        aria-hidden="true"
        className="pointer-events-none absolute start-3 top-1/2 -translate-y-1/2 text-ghost"
      />
      <input
        ref={inputRef}
        value={query}
        onChange={(e) => { setQuery(e.target.value); setOpen(true) }}
        onFocus={() => setOpen(true)}
        onKeyDown={onKeyDown}
        role="combobox"
        aria-label={t('search.label')}
        aria-autocomplete="list"
        aria-expanded={hasList}
        aria-controls={hasList ? listId : undefined}
        aria-activedescendant={hasList && active >= 0 ? `${listId}-${active}` : undefined}
        autoComplete="off"
        enterKeyHint="search"
        placeholder={t('search.placeholder')}
        className="h-[38px] w-full rounded-lg border border-border bg-surface ps-9 pe-16 text-[13px] text-bright transition-colors placeholder:text-ghost focus:border-amber/50"
      />
      {!query && (
        // The shortcut is a hint for sighted keyboard users; it is not the field's name.
        // `dir="ltr"` is on the inner element, not the positioned one: a logical inset
        // (`end-2.5`) resolves against the element's OWN direction, so an ltr `kbd`
        // would be pinned to the physical right, on top of the icon, in an Arabic page.
        <span
          aria-hidden="true"
          className="pointer-events-none absolute end-2.5 top-1/2 -translate-y-1/2"
        >
          <kbd
            dir="ltr"
            className="rounded border border-border px-1.5 py-px font-mono text-[11px] text-ghost"
          >
            Ctrl K
          </kbd>
        </span>
      )}

      {showPanel && (
        <div className="absolute inset-x-0 top-full z-50 mt-2 max-h-[70vh] overflow-y-auto rounded-xl border border-border bg-ink shadow-2xl">
          {list.length === 0 && (
            <p role="status" className="px-4 py-3 text-xs text-ghost">
              {pending || hits === null ? t('search.searching') : t('search.none')}
            </p>
          )}
          {list.length > 0 && (
            <ul id={listId} role="listbox" aria-label={t('search.label')} className="py-1.5">
              {list.map((hit, i) => (
                <li key={`${hit.kind}-${hit.id}`} role="presentation">
                  <Link
                    id={`${listId}-${i}`}
                    role="option"
                    aria-selected={i === active}
                    href={hit.href}
                    onClick={finish}
                    onMouseEnter={() => setActive(i)}
                    className={cn(
                      'flex flex-col gap-0.5 px-4 py-2.5 transition-colors',
                      i === active ? 'bg-panel' : 'hover:bg-panel',
                    )}
                  >
                    <span className="flex items-center gap-2">
                      <span className="font-mono text-[10px] uppercase tracking-wider text-ghost">
                        {t(`search.kind.${hit.kind}` as StringKey)}
                      </span>
                      {hit.parent_title && <span className="truncate text-xs text-ghost">{hit.parent_title}</span>}
                    </span>
                    <span className="text-[13px] text-bright">{localizedTitle(hit, language) || hit.title}</span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}
