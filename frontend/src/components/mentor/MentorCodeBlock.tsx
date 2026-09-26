'use client'
import { useEffect, useRef, useState } from 'react'
import { Check, Copy } from 'lucide-react'
import { useI18n } from '@/lib/i18n'

async function copyText(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text)
      return true
    }
  } catch {
    // Blocked by the page's permissions policy or a missing user gesture: try the old way.
  }
  try {
    const area = document.createElement('textarea')
    area.value = text
    area.setAttribute('readonly', '')
    area.style.position = 'fixed'
    area.style.opacity = '0'
    document.body.appendChild(area)
    area.select()
    const ok = document.execCommand('copy')
    document.body.removeChild(area)
    return ok
  } catch {
    return false
  }
}

/**
 * A code block in a mentor message (handoff Task 12a): always dark, left to right and scrolling
 * sideways, whatever the theme or the language of the sentence around it. The colours are the
 * handoff's own and are fixed on purpose, like the lesson code blocks: code is dark in both themes.
 */
export function MentorCodeBlock({ code, lang }: { code: string; lang?: string }) {
  const { t } = useI18n()
  const [copied, setCopied] = useState(false)
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(
    () => () => {
      if (timer.current) clearTimeout(timer.current)
    },
    [],
  )

  async function copy() {
    if (!(await copyText(code))) return
    setCopied(true)
    if (timer.current) clearTimeout(timer.current)
    timer.current = setTimeout(() => setCopied(false), 1600)
  }

  return (
    <div dir="ltr" className="my-2.5 overflow-hidden rounded-lg border border-[#1E2535] bg-[#0B0E14] text-start">
      <div className="flex min-h-[44px] items-center justify-between gap-3 border-b border-[#1E2535] ps-3.5 pe-1 lg:min-h-9">
        <span className="font-mono text-[11px] uppercase tracking-wide text-[#8E9BB0]">{lang || 'code'}</span>
        <button
          type="button"
          onClick={() => void copy()}
          className="inline-flex min-h-[44px] items-center gap-1.5 rounded-md px-3 text-xs text-[#C7D0DE] transition-colors hover:bg-[#161C28] hover:text-[#F7FAFC] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[#F59E0B] lg:min-h-8"
        >
          {copied ? <Check size={13} aria-hidden="true" /> : <Copy size={13} aria-hidden="true" />}
          {copied ? t('mentor.copied') : t('mentor.copy')}
          <span className="sr-only"> {t('mentor.copyCode')}</span>
        </button>
      </div>
      {/* tabIndex: a region that scrolls sideways has to be reachable from the keyboard. */}
      <pre tabIndex={0} className="!m-0 overflow-x-auto px-3.5 py-3 font-mono text-xs leading-[1.7] text-[#C7D0DE] focus-visible:outline focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-[#F59E0B]">
        <code>{code}</code>
      </pre>
      <span role="status" className="sr-only">{copied ? t('mentor.copied') : ''}</span>
    </div>
  )
}
