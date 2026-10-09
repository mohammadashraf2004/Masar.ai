'use client'
import { useEffect, useRef, useState } from 'react'
import { Check, Code2, Languages } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { useLanguageStore, TERMINOLOGY_MODES, type TerminologyMode } from '@/lib/language'

/**
 * The learner's control over the two language axes: which language the
 * explanations are in, and how much English terminology those explanations
 * carry (Industry Mode).
 *
 * Both are device preferences, applied instantly and everywhere — course
 * content, lesson prose, the AI mentor's replies. Code is deliberately
 * exempt, and the panel says so, because a student switching to "العربية"
 * needs to know their code samples are not about to be translated.
 */

const MODE_KEYS: Record<TerminologyMode, { label: `lang.mode.${TerminologyMode}`; hint: `lang.mode.${TerminologyMode}.hint` }> = {
  arabic_first: { label: 'lang.mode.arabic_first', hint: 'lang.mode.arabic_first.hint' },
  industry: { label: 'lang.mode.industry', hint: 'lang.mode.industry.hint' },
  english_technical: {
    label: 'lang.mode.english_technical',
    hint: 'lang.mode.english_technical.hint',
  },
}

export function LanguageSwitcher({
  className,
  placement = 'down',
  align = 'end',
}: {
  className?: string
  /** Which way the panel opens. `up` is for a trigger at the bottom of a
   *  scrolling menu, where a panel opening downward would be cut off. */
  placement?: 'down' | 'up'
  /** Which edge of the trigger the panel lines up with. `end` suits a trigger
   *  at the trailing edge of a header (the default); a trigger at the leading
   *  edge needs `start`, or the panel opens off-screen. */
  align?: 'start' | 'end'
}) {
  const { t, language, mode, annotateTerms } = useI18n()
  const setLanguage = useLanguageStore((s) => s.setLanguage)
  const setMode = useLanguageStore((s) => s.setMode)
  const setAnnotateTerms = useLanguageStore((s) => s.setAnnotateTerms)

  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!open) return
    const onClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(false)
    document.addEventListener('mousedown', onClick)
    document.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('mousedown', onClick)
      document.removeEventListener('keydown', onKey)
    }
  }, [open])

  return (
    <div className={cn('relative', className)} ref={ref}>
      <button
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        data-tour="lang-switch"
        title={t('lang.title')}
        className={cn(
          'flex min-h-[44px] items-center gap-1.5 px-2.5 py-1.5 rounded-lg border text-xs font-medium transition-all lg:min-h-0',
          open
            ? 'border-amber/40 bg-amber/10 text-amber-text'
            : 'border-border text-dim hover:text-bright hover:border-amber/20'
        )}
      >
        <Languages size={12} className="shrink-0" />
        <span>{language === 'ar' ? 'ع' : 'EN'}</span>
        <span className="text-ghost hidden md:inline">·</span>
        <span className="text-ghost hidden md:inline">{t(MODE_KEYS[mode].label)}</span>
      </button>

      {open && (
        <div
          className={cn(
            // Sized to the compact trigger: never narrower than it, and no
            // wider than the mode hints need to wrap onto two or three lines.
            'absolute w-60 min-w-full max-w-[calc(100vw-2rem)] bg-ink border border-border rounded-lg shadow-2xl z-50 overflow-hidden',
            align === 'start' ? 'start-0' : 'end-0',
            placement === 'up' ? 'bottom-full mb-1.5' : 'top-full mt-1.5',
          )}
        >
          {/* ── Explanation language ── */}
          <div className="px-3 pt-3 pb-2.5 border-b border-border">
            <p className="text-[11px] text-ghost mb-1.5">{t('lang.uiLanguage')}</p>
            <div className="flex gap-1.5">
              {(['ar', 'en'] as const).map((code) => (
                <button
                  key={code}
                  onClick={() => setLanguage(code)}
                  className={cn(
                    'flex-1 px-2 py-1.5 rounded-md border text-xs transition-colors',
                    language === code
                      ? 'border-amber/30 bg-amber/10 text-amber-text font-medium'
                      : 'border-border text-dim hover:text-bright'
                  )}
                >
                  {code === 'ar' ? t('lang.arabic') : t('lang.english')}
                </button>
              ))}
            </div>
          </div>

          {/* ── Industry Mode ladder ── */}
          <div className="px-3 pt-3 pb-2.5 border-b border-border">
            <p className="text-[11px] text-ghost mb-1.5">{t('lang.mode')}</p>
            <div className="space-y-1">
              {TERMINOLOGY_MODES.map((value) => {
                const active = mode === value
                return (
                  <button
                    key={value}
                    onClick={() => setMode(value)}
                    className={cn(
                      'w-full text-start px-2 py-1.5 rounded-md border transition-colors',
                      active
                        ? 'border-amber/30 bg-amber/10'
                        : 'border-transparent hover:bg-surface'
                    )}
                  >
                    <span className="flex items-center gap-1.5">
                      <span
                        className={cn(
                          'text-xs font-medium',
                          active ? 'text-amber-text' : 'text-soft'
                        )}
                      >
                        {t(MODE_KEYS[value].label)}
                      </span>
                      {active && <Check size={11} className="text-amber-text" />}
                    </span>
                    <span className="block text-[11px] text-ghost leading-snug mt-0.5">
                      {t(MODE_KEYS[value].hint)}
                    </span>
                  </button>
                )
              })}
            </div>
          </div>

          {/* ── Term highlighting ── */}
          <div className="px-3 py-2.5">
            <label className="flex items-start gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={annotateTerms}
                onChange={(e) => setAnnotateTerms(e.target.checked)}
                className="mt-0.5 accent-amber"
              />
              <span className="text-[11px] text-soft leading-snug">{t('lang.annotate')}</span>
            </label>
            <p className="flex items-start gap-1.5 mt-2 text-[11px] text-ghost leading-snug">
              <Code2 size={11} className="shrink-0 mt-0.5" />
              {t('lang.codeNote')}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
