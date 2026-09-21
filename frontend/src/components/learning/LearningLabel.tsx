'use client'
import { useI18n } from '@/lib/i18n'
import type { LabelParts } from '@/lib/learning'

/**
 * Renders a name the way the reader's language and terminology mode want it —
 * `NLP (معالجة اللغة الطبيعية)` in Arabic First, `NLP` in English Technical.
 *
 * Each run is wrapped in <bdi> with its own direction so an English term
 * inside an Arabic sentence (or the reverse) keeps its punctuation and word
 * order instead of being reshuffled by the surrounding text.
 */
export function LearningLabel({ parts, className }: { parts: LabelParts; className?: string }) {
  return (
    <span className={className}>
      <bdi dir={parts.primaryDir}>{parts.primary}</bdi>
      {parts.gloss && (
        <span className="text-soft font-normal">
          {' ('}
          <bdi dir="rtl">{parts.gloss}</bdi>
          {')'}
        </span>
      )}
    </span>
  )
}

/** The language and terminology mode, in the shape the label helpers take. */
export function useLabelContext() {
  const { language, mode } = useI18n()
  return { language, mode }
}
