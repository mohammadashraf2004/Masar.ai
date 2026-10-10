'use client'
import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import { Code, Send } from 'lucide-react'
import Link from 'next/link'
import { LogoMark } from '@/components/layout/Logo'
import { MentorMarkdown, UserMessageBody } from '@/components/mentor/MentorMarkdown'
import { QuotaUpsell } from '@/components/mentor/QuotaUpsell'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/index'
import type { useMentorChat } from '@/hooks/useMentorChat'
import { useI18n, type StringKey } from '@/lib/i18n'
import { useCreditBalance } from '@/components/layout/WalletContext'
import { MENTOR_MESSAGE_CREDITS, cannotAffordMessage } from '@/lib/mentor/credits'
import { withAttachment } from '@/lib/mentor/fences'
import { cn } from '@/lib/utils'

type Chat = ReturnType<typeof useMentorChat>

const MAX_COMPOSER_HEIGHT = 128

/**
 * The chat card (handoff Task 12a): header with the mentor's name and status, the messages, the
 * suggestion chips and the composer. The state is the page's (`useMentorChat`), because the side
 * column reads and drives the same conversation.
 */
export function ChatCard({ chat }: { chat: Chat }) {
  const { t, tf, dir } = useI18n()
  const [draft, setDraft] = useState('')
  const [attaching, setAttaching] = useState(false)
  const [attached, setAttached] = useState('')
  const log = useRef<HTMLDivElement>(null)
  const field = useRef<HTMLTextAreaElement>(null)

  const balance = useCreditBalance()
  // What is left after the messages sent since the balance was read; below one message's price, or
  // once the backend has said 402, the box gives way to the out-of-credits bar.
  const spent = chat.delivered * MENTOR_MESSAGE_CREDITS
  const broke = chat.creditsShort || cannotAffordMessage(balance, spent)
  const left = balance === null ? null : Math.max(0, balance - spent)
  const exhausted = chat.quotaStatus?.exhausted ?? false
  const blocked = chat.loading || exhausted
  const canSend = !blocked && (draft.trim() !== '' || attached.trim() !== '')

  // Auto-scroll to the newest message whenever one is added (or the typing line appears).
  useEffect(() => {
    log.current?.scrollTo({ top: log.current.scrollHeight })
  }, [chat.messages, chat.loading])

  // The composer grows with what is typed, up to a few lines, then scrolls.
  useLayoutEffect(() => {
    const el = field.current
    if (!el) return
    // Empty: back to the one-row height, whatever the placeholder would need if it wrapped.
    if (!draft) {
      el.style.height = ''
      return
    }
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, MAX_COMPOSER_HEIGHT)}px`
  }, [draft])

  async function submit(text: string, code = '') {
    const content = withAttachment(text, code)
    if (!content.trim() || blocked) return
    const sent = await chat.send(content)
    if (sent) {
      setDraft('')
      setAttached('')
      setAttaching(false)
    }
    field.current?.focus()
  }

  return (
    // Runs to the bottom of the screen: the page measures it (useFillHeight) and sets --mentor-chat-h.
    <Card className="flex h-[var(--mentor-chat-h,calc(100dvh-200px))] min-h-[420px] min-w-0 flex-col overflow-hidden p-0">
      <div className="flex items-center gap-3 border-b border-border px-[18px] py-3.5">
        <LogoMark size={34} label={null} />
        <div className="min-w-0 flex-1">
          <p className="text-sm font-semibold text-white">{t('mentor.name')}</p>
          {/* Says what the model is (and is not) told: level and readiness, not the lesson. */}
          <p className="text-xs leading-snug text-ghost">{t('mentor.header.sub')}</p>
        </div>
        <span className={cn('flex shrink-0 items-center gap-1.5 text-xs', chat.online ? 'text-emerald' : 'text-ghost')}>
          <span aria-hidden="true" className={cn('h-[7px] w-[7px] rounded-full', chat.online ? 'bg-emerald' : 'bg-ghost')} />
          {chat.online ? t('mentor.online') : t('mentor.offline')}
        </span>
      </div>

      {chat.viewing && (
        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 border-b border-border bg-panel px-[18px] py-2.5 text-xs text-dim">
          <span className="min-w-0 flex-[1_1_200px]">{t('mentor.thread.viewing')}</span>
          <button
            type="button"
            onClick={chat.backToLatest}
            className="min-h-[44px] font-medium text-amber-text underline underline-offset-2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring lg:min-h-0"
          >
            {t('mentor.thread.back')}
          </button>
        </div>
      )}

      <div
        ref={log}
        role="log"
        aria-label={t('mentor.log')}
        aria-live="polite"
        className="flex min-h-0 flex-1 flex-col gap-3.5 overflow-y-auto p-[18px]"
      >
        {chat.messages.map((message, i) => {
          const mine = message.role === 'user'
          return (
            <div
              key={`${message.timestamp}-${i}`}
              dir={mine ? 'auto' : dir}
              role={message.error ? 'alert' : undefined}
              className={cn(
                'min-w-0 max-w-[82%] rounded-xl px-3.5 py-3 text-sm leading-[1.75] [overflow-wrap:anywhere]',
                mine
                  ? 'self-end rounded-be-[4px] bg-amber-soft text-bright'
                  : cn('self-start rounded-bs-[4px] border bg-panel text-soft', message.error ? 'border-rose/40' : 'border-border'),
              )}
            >
              {mine ? (
                <UserMessageBody text={message.content} />
              ) : message.error ? (
                <p>{t(message.content as StringKey)}</p>
              ) : (
                <MentorMarkdown>{message.content}</MentorMarkdown>
              )}
            </div>
          )
        })}

        {chat.loading && (
          <div role="status" className="flex items-center gap-2 self-start text-[13px] text-ghost">
            <span aria-hidden="true" className="h-[7px] w-[7px] animate-pulse rounded-full bg-amber" />
            {t('mentor.typing')}
          </div>
        )}
      </div>

      {chat.suggestions.length > 0 && (
        <div role="group" aria-label={t('mentor.suggestions')} className="flex flex-wrap gap-2 px-[18px] pb-3">
          {chat.suggestions.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              disabled={blocked}
              onClick={() => void submit(suggestion)}
              className="min-h-[44px] rounded-full border border-border px-3 py-1.5 text-start text-xs text-dim transition-colors hover:border-amber/40 hover:text-bright focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-40 lg:min-h-0"
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}

      {exhausted && !broke && (
        <QuotaUpsell
          kind="quota"
          limit={chat.quotaStatus?.limit}
          className="mx-[18px] mb-3"
        />
      )}

      <div className="border-t border-border px-3.5 py-3">
        {broke ? (
          <QuotaUpsell kind="credits" />
        ) : (
          <>
        {attaching && (
          <div className="mb-2.5">
            <label htmlFor="mentor-attach" className="mb-1 block text-xs text-ghost">{t('mentor.attach.label')}</label>
            <textarea
              id="mentor-attach"
              dir="ltr"
              value={attached}
              onChange={(e) => setAttached(e.target.value)}
              placeholder={t('mentor.attach.placeholder')}
              rows={5}
              className="w-full resize-y rounded-lg border border-border bg-void px-3 py-2.5 text-start font-mono text-xs leading-[1.7] text-bright placeholder:text-ghost focus:border-amber/50 focus:outline-none"
            />
          </div>
        )}
        <form
          className="flex items-end gap-2.5"
          onSubmit={(e) => {
            e.preventDefault()
            void submit(draft, attached)
          }}
        >
          <button
            type="button"
            aria-pressed={attaching}
            aria-label={t('mentor.attach')}
            title={t('mentor.attach')}
            onClick={() => setAttaching((v) => !v)}
            className={cn(
              'flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring lg:h-10 lg:w-10',
              attaching ? 'border-amber/50 bg-amber-soft text-amber-text' : 'border-border text-dim hover:text-bright',
            )}
          >
            <Code size={16} aria-hidden="true" />
          </button>
          <textarea
            ref={field}
            dir="auto"
            rows={1}
            value={draft}
            disabled={exhausted}
            aria-label={t('mentor.input.label')}
            placeholder={t('mentor.placeholder')}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => {
              // Enter sends, Shift+Enter adds a line; Enter that confirms an IME choice does neither.
              if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
                e.preventDefault()
                void submit(draft, attached)
              }
            }}
            className="min-h-[64px] min-w-0 flex-1 resize-none sm:min-h-[44px] rounded-lg border border-border bg-void px-3.5 py-[11px] text-base leading-snug text-bright placeholder:text-ghost placeholder:text-sm focus:border-amber/50 focus:outline-none disabled:opacity-50 md:text-sm"
            style={{ direction: dir }}
          />
          <Button type="submit" disabled={!canSend} className="h-11 shrink-0 px-4 max-sm:w-11 max-sm:px-0 lg:h-11">
            <Send size={14} aria-hidden="true" className="rtl:-scale-x-100" />
            <span className="max-sm:sr-only">{t('common.send')}</span>
          </Button>
        </form>
        {(left !== null || (chat.quotaStatus && !exhausted)) && (
          <div data-tour="credits" className="mt-1 flex items-center justify-between gap-x-3 text-xs text-ghost">
            <span className="flex min-w-0 flex-1 flex-wrap gap-x-3">
              {left !== null && (
                <span data-testid="credit-line">{tf('mentor.credits.line', { n: left })}</span>
              )}
              {chat.quotaStatus && !exhausted && (
                <span>{tf('mentor.quota.left', { n: chat.quotaStatus.left, limit: chat.quotaStatus.limit })}</span>
              )}
            </span>
            {/* After the text, at the trailing end of the row; it mirrors with the page's direction. */}
            {left !== null && (
              <Link
                href="/billing"
                className="inline-flex min-h-[44px] shrink-0 items-center font-medium text-amber-text underline-offset-2 hover:text-amber-text2 hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring lg:min-h-0"
              >
                {t('mentor.credits.topup')}
              </Link>
            )}
          </div>
        )}
          </>
        )}
      </div>
    </Card>
  )
}
