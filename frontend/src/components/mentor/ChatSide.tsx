'use client'
import { Plus } from 'lucide-react'
import { Card } from '@/components/ui/index'
import type { useMentorChat } from '@/hooks/useMentorChat'
import { useI18n, type StringKey } from '@/lib/i18n'
import { formatShortDate } from '@/lib/mentor/format'
import { cn } from '@/lib/utils'

type Chat = ReturnType<typeof useMentorChat>

const SHORTCUTS = ['mentor.shortcut1', 'mentor.shortcut2', 'mentor.shortcut3'] as const

/**
 * The chat mode's side column (handoff Task 12a): what the mentor is told about the learner,
 * three prompts that send on a tap, and earlier conversations.
 *
 * "What the mentor knows" lists what `/mentor/chat` is really given: the account's level and
 * readiness, and the language settings. It does not see the current lesson or exercise; the card
 * says so instead of showing a lesson the model was never told about.
 */
export function ChatSide({ chat, name, level, readiness }: { chat: Chat; name: string; level: string; readiness: number }) {
  const { t, language, mode } = useI18n()
  const blocked = chat.loading || (chat.quotaStatus?.exhausted ?? false)

  // Exactly what `/mentor/chat` is given about the learner: five things, and nothing else.
  const known: Array<{ label: StringKey; value: string; accent?: boolean; auto?: boolean }> = [
    { label: 'mentor.known.name', value: name, auto: true },
    { label: 'mentor.known.level', value: t(`level.${level}` as StringKey) },
    { label: 'mentor.known.readiness', value: `${readiness}%`, accent: true },
  ]
  // The two rows the learner controls; the language walkthrough points at them together.
  const chosen: typeof known = [
    { label: 'mentor.known.language', value: t(language === 'ar' ? 'lang.arabic' : 'lang.english') },
    { label: 'mentor.known.terms', value: t(`lang.mode.${mode}` as StringKey) },
  ]
  const row = (r: (typeof known)[number]) => (
    <div key={r.label} className="flex items-baseline justify-between gap-3">
      <dt className="text-dim">{t(r.label)}</dt>
      <dd dir={r.auto ? 'auto' : undefined} className={cn('min-w-0 truncate text-end font-medium', r.accent ? 'font-mono text-amber-text' : 'text-bright')}>{r.value}</dd>
    </div>
  )

  return (
    <div className="flex min-w-0 flex-[1_1_280px] flex-col gap-5">
      <Card className="p-5">
        <h2 className="mb-3 text-sm font-semibold text-white">{t('mentor.known.title')}</h2>
        <dl className="space-y-2.5 text-[13px]">
          {known.map(row)}
          <div data-tour="mentor-lang" className="space-y-2.5">{chosen.map(row)}</div>
        </dl>
        <p className="mt-3.5 text-xs leading-relaxed text-ghost">{t('mentor.known.note')}</p>
      </Card>

      <Card className="p-5">
        <h2 className="mb-3 text-sm font-semibold text-white">{t('mentor.shortcuts')}</h2>
        <ul className="space-y-2">
          {SHORTCUTS.map((key, i) => (
            <li key={key}>
              <button
                type="button"
                disabled={blocked}
                onClick={() => void chat.send(t(key))}
                className="flex min-h-[44px] w-full items-center gap-3 rounded-lg border border-border px-3 py-2 text-start text-[13px] text-soft transition-colors hover:border-amber/40 hover:text-bright focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-40"
              >
                <span dir="ltr" className="font-mono text-xs text-amber-text">{String(i + 1).padStart(2, '0')}</span>
                <span className="min-w-0 flex-1">{t(key)}</span>
              </button>
            </li>
          ))}
        </ul>
      </Card>

      <Card className="p-5">
        <div className="mb-2 flex items-center justify-between gap-3">
          <h2 className="text-sm font-semibold text-white">{t('mentor.threads')}</h2>
          <button
            type="button"
            onClick={() => void chat.newConversation()}
            disabled={chat.loading}
            className="inline-flex min-h-[44px] items-center gap-1.5 rounded-md px-2 text-xs font-medium text-amber-text hover:text-amber-text2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-40 lg:min-h-0 lg:py-1"
          >
            <Plus size={13} aria-hidden="true" />
            {t('mentor.threads.new')}
          </button>
        </div>
        {chat.threads.length === 0 ? (
          chat.threadsLoaded && <p className="py-2 text-[13px] text-ghost">{t('mentor.threads.empty')}</p>
        ) : (
          <ul>
            {chat.threads.map((thread) => (
              <li key={thread.id} className="border-t border-border first:border-t-0">
                <button
                  type="button"
                  onClick={() => chat.openThread(thread.id)}
                  aria-current={chat.activeThreadId === thread.id ? 'true' : undefined}
                  className={cn(
                    'flex min-h-[44px] w-full items-center justify-between gap-3 py-2 text-start text-[13px] transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring',
                    chat.activeThreadId === thread.id ? 'text-white' : 'text-soft hover:text-bright',
                  )}
                >
                  <span dir="auto" className="min-w-0 flex-1 truncate">{thread.title || t('mentor.thread.untitled')}</span>
                  <span className="shrink-0 text-xs text-ghost">{formatShortDate(thread.at, language)}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  )
}
