'use client'
import { useState } from 'react'
import { Check, Copy } from 'lucide-react'
import { useRefundI18n } from '@/lib/billing/refundI18n'

export function ReferenceNumber({ value, showHelp = false }: { value: string; showHelp?: boolean }) {
  const { t } = useRefundI18n()
  const [copied, setCopied] = useState(false)

  async function copy() {
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(value)
      } else {
        const field = document.createElement('textarea')
        field.value = value
        field.style.position = 'fixed'
        field.style.opacity = '0'
        document.body.appendChild(field)
        field.select()
        document.execCommand('copy')
        field.remove()
      }
      setCopied(true)
      window.setTimeout(() => setCopied(false), 1800)
    } catch {
      // Keep the reference selected/readable if the browser blocks clipboard
      // access; the button can be retried after clipboard permission changes.
    }
  }

  return (
    <div className="flex flex-col items-center gap-1.5">
      <div className="flex flex-wrap items-center justify-center gap-2">
        <span className="text-xs text-dim">{t('reference')}:</span>
        <span dir="ltr" className="font-mono text-sm font-semibold text-white">{value}</span>
        <button
          type="button"
          onClick={() => void copy()}
          className="inline-flex min-h-[36px] items-center gap-1 rounded-md border border-border px-2 text-xs text-soft hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
          aria-label={`${t('copy')} ${value}`}
        >
          {copied ? <Check size={13} aria-hidden="true" /> : <Copy size={13} aria-hidden="true" />}
          {copied ? t('copied') : t('copy')}
        </button>
      </div>
      {showHelp && <p className="text-xs leading-relaxed text-ghost">{t('keepReference')}</p>}
    </div>
  )
}

