'use client'
import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ArrowLeft, ArrowRight, Send } from 'lucide-react'
import { LogoMark } from '@/components/layout/Logo'
import { useCreditBalance } from '@/components/layout/WalletContext'
import { MentorMarkdown } from '@/components/mentor/MentorMarkdown'
import { QuotaUpsell } from '@/components/mentor/QuotaUpsell'
import type { Thread } from '@/hooks/useMentorChat'
import { Card } from '@/components/ui/index'
import { useI18n, useMentorV2I18n } from '@/lib/i18n'
import { cannotAffordMessage } from '@/lib/mentor/credits'
import { cn } from '@/lib/utils'
import { ActionChips, NEEDS_NO_TEXT, placeholderKey } from './ActionChips'
import { ContextBar } from './ContextBar'
import { contextLabels, DEFAULT_CONTEXT } from './context'
import { LearnerModelCard, PastChats, SuggestionCard } from './MentorAside'
import { MentorBlocks, MentorMessageView, type MessageActions } from './MentorMessageView'
import type { MentorContextSelection } from './types'
import { useMentorV2 } from './useMentorV2'
import { mentorV2EndpointLive } from './flag'
import { mockCreditBalanceFromQuery } from './mock'

const MAX_COMPOSER_HEIGHT = 128

/**
 * The hub's chat (Mentor v2 §2a): a chat card with the context bar, the messages, the action chips
 * and the composer, beside the learner model, the suggestion and past chats. Below 900px the chat
 * is the whole screen, with its own top bar, and the aside is left to the other tabs.
 */
export function MentorChat({ base = DEFAULT_CONTEXT }: { base?: MentorContextSelection }) {
  const { t, tf, n, language } = useMentorV2I18n()
  const { t: tOld, dir } = useI18n()
  const router = useRouter()
  const chat = useMentorV2({ base, proactive: true })
  const walletBalance = useCreditBalance()
  const mockBalance = mentorV2EndpointLive('message') ? null : mockCreditBalanceFromQuery()
  const balance = mockBalance ?? walletBalance
  const [draft, setDraft] = useState('')
  const [viewing, setViewing] = useState<Thread | null>(null)
  const log = useRef<HTMLDivElement>(null)
  const field = useRef<HTMLTextAreaElement>(null)

  const labels = contextLabels(base, language, n)
  const lessonLabel = base.lessonId ? labels.lesson : null
  const codeLabel = base.exerciseId ? labels.code : null
  const left = balance === null ? null : Math.max(0, balance - chat.spent)
  const broke = chat.creditsShort || cannotAffordMessage(balance, chat.spent)
  const canSend = !chat.loading && (draft.trim() !== '' || (chat.intent !== null && NEEDS_NO_TEXT.includes(chat.intent)))

  useEffect(() => {
    const el = log.current
    if (el) el.scrollTop = el.scrollHeight
  }, [chat.messages, chat.loading, chat.failure])

  useEffect(() => {
    const el = field.current
    if (!el) return
    if (!draft) { el.style.height = ''; return }
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, MAX_COMPOSER_HEIGHT)}px`
  }, [draft])

  async function submit() {
    if (!canSend) return
    const sent = await chat.send(draft)
    if (sent) setDraft('')
    field.current?.focus()
  }

  const actions: MessageActions = {
    exerciseId: base.exerciseId,
    onQuizResult: chat.onQuizResult,
    onCheckAnswer: (answer) => void chat.answerCheck(answer),
    onHintMessage: chat.append,
  }

  const Back = dir === 'rtl' ? ArrowRight : ArrowLeft

  return (
    <>
      {/* Mobile: the chat is the screen. */}
      <div className="flex min-w-0 flex-[2_1_520px] flex-col max-[899px]:fixed max-[899px]:inset-0 max-[899px]:z-[60] max-[899px]:bg-void" data-testid="mentor-chat">
        <header className="flex items-center gap-2.5 border-b border-border bg-ink px-3 pt-[env(safe-area-inset-top)] min-[900px]:hidden">
          <button
            type="button"
            aria-label={t('mentor.v2.mobile.back')}
            onClick={() => router.back()}
            className="grid h-11 w-11 shrink-0 place-items-center rounded-lg text-white hover:bg-panel focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
          >
            <Back size={18} aria-hidden="true" />
          </button>
          <div className="min-w-0 flex-1 py-2">
            <p className="text-sm font-semibold text-white">{t('mentor.v2.mobile.title')}</p>
            {lessonLabel && <p dir="auto" className="truncate text-[11px] text-ghost">{lessonLabel}</p>}
          </div>
          {left !== null && (
            <Link href="/billing" className="flex h-[34px] items-center gap-2 rounded-full border border-border bg-surface px-3 font-mono text-xs text-white">
              <span aria-hidden="true" className="h-[7px] w-[7px] rounded-full bg-amber" />{left}
            </Link>
          )}
        </header>

        <Card className="flex h-[calc(100dvh-200px)] min-h-[480px] min-w-0 flex-col overflow-hidden p-0 md:h-[640px] max-[899px]:h-auto max-[899px]:min-h-0 max-[899px]:flex-1 max-[899px]:rounded-none max-[899px]:border-0">
          <div className="flex items-center gap-3 border-b border-border px-[18px] py-3.5 max-[899px]:hidden">
            <LogoMark size={34} label={null} />
            <div className="min-w-0 flex-1">
              <p className="text-sm font-semibold text-white">{tOld('mentor.name')}</p>
              <p className="text-xs leading-snug text-ghost">{t('mentor.v2.subtitle')}</p>
            </div>
            <button
              type="button"
              onClick={() => { chat.newThread(); setViewing(null) }}
              disabled={chat.loading || chat.messages.length === 0}
              className="min-h-[36px] shrink-0 rounded-lg border border-border px-3 text-xs text-bright hover:border-amber/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-40"
            >
              {t('mentor.v2.newThread')}
            </button>
          </div>

          <ContextBar
            lessonLabel={lessonLabel}
            codeLabel={codeLabel}
            lessonOn={chat.lessonOn}
            codeOn={chat.codeOn}
            onToggleLesson={chat.setLessonOn}
            onToggleCode={chat.setCodeOn}
            onRestore={() => { chat.setLessonOn(true); chat.setCodeOn(true) }}
          />

          {viewing && (
            <div className="flex flex-wrap items-center gap-x-3 gap-y-1 border-b border-border bg-panel px-[18px] py-2.5 text-xs text-dim">
              <span className="min-w-0 flex-[1_1_200px]">{tOld('mentor.thread.viewing')}</span>
              <button type="button" onClick={() => setViewing(null)} className="min-h-[44px] font-medium text-amber-text underline underline-offset-2 lg:min-h-0">
                {tOld('mentor.thread.back')}
              </button>
            </div>
          )}

          <div
            ref={log}
            role="log"
            aria-label={t('mentor.v2.log')}
            aria-live="polite"
            className="flex min-h-0 flex-1 flex-col gap-3.5 overflow-y-auto p-[18px]"
          >
            {viewing ? (
              viewing.messages.map((m, i) => (
                <div
                  key={`${m.timestamp}-${i}`}
                  dir="auto"
                  className={cn(
                    'min-w-0 max-w-[88%] rounded-xl px-3.5 py-3 text-sm leading-[1.75] [overflow-wrap:anywhere]',
                    m.role === 'user' ? 'self-end rounded-be-[4px] bg-amber-soft text-bright' : 'self-start rounded-bs-[4px] border border-border bg-panel text-soft',
                  )}
                >
                  {m.blocks ? <MentorBlocks blocks={m.blocks} /> : <MentorMarkdown>{m.content}</MentorMarkdown>}
                </div>
              ))
            ) : (
              <>
                {chat.messages.length === 0 && <p className="m-auto max-w-xs text-center text-sm text-ghost">{t('mentor.v2.empty')}</p>}
                {chat.messages.map((message) => <MentorMessageView key={message.id} message={message} actions={actions} />)}
                {chat.failure && (
                  <div role="alert" className="flex flex-wrap items-center gap-3 self-start rounded-xl border border-rose/40 bg-panel px-3.5 py-3 text-sm text-soft">
                    <span>{tOld(chat.failure.errorKey)}</span>
                    <button type="button" onClick={() => void chat.retry()} className="min-h-[44px] rounded-lg border border-border px-3 text-[13px] text-bright hover:border-amber/40">
                      {t('mentor.v2.retry')}
                    </button>
                  </div>
                )}
                {chat.loading && (
                  <div role="status" className="flex items-center gap-2 self-start text-[13px] text-ghost">
                    <span aria-hidden="true" className="h-[7px] w-[7px] animate-pulse rounded-full bg-amber" />
                    {t('mentor.v2.typing')}
                  </div>
                )}
              </>
            )}
          </div>

          <div className="border-t border-border pt-2">
            {broke ? (
              <div className="px-3.5 pb-3"><QuotaUpsell kind="credits" /></div>
            ) : (
              <>
                <ActionChips selected={chat.intent} disabled={chat.loading || !!viewing} onSelect={chat.setIntent} />
                <form
                  className="flex items-end gap-2.5 px-3.5 pb-1 max-[899px]:pb-[max(0.25rem,env(safe-area-inset-bottom))]"
                  onSubmit={(e) => { e.preventDefault(); void submit() }}
                >
                  <textarea
                    ref={field}
                    dir="auto"
                    rows={1}
                    value={draft}
                    disabled={!!viewing}
                    aria-label={t(placeholderKey(chat.intent))}
                    placeholder={t(placeholderKey(chat.intent))}
                    onChange={(e) => setDraft(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); void submit() }
                    }}
                    className="min-h-[44px] min-w-0 flex-1 resize-none rounded-lg border border-border bg-void px-3.5 py-[11px] text-base leading-snug text-bright placeholder:text-ghost placeholder:text-sm focus:border-amber/50 focus:outline-none disabled:opacity-50 md:text-sm max-[899px]:rounded-full"
                  />
                  <button
                    type="submit"
                    disabled={!canSend}
                    aria-label={t('mentor.v2.send')}
                    className="grid h-11 shrink-0 place-items-center rounded-lg bg-amber px-4 text-[13px] font-semibold text-on-amber hover:bg-amber2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-40 max-[899px]:w-11 max-[899px]:rounded-full max-[899px]:px-0"
                  >
                    <Send size={14} aria-hidden="true" className="rtl:-scale-x-100 min-[900px]:hidden" />
                    <span className="max-[899px]:hidden">{t('mentor.v2.send')}</span>
                  </button>
                </form>
                <div data-tour="credits" className="flex flex-wrap items-center justify-between gap-x-3 px-3.5 pb-3 pt-1 text-xs text-ghost">
                  <span className="min-w-0 flex-1">{t('mentor.v2.cost')}</span>
                  {left !== null && <span dir="ltr" className="font-mono" data-testid="credit-line">{tf('mentor.v2.balance', { n: left })}</span>}
                </div>
              </>
            )}
          </div>
        </Card>
      </div>

      <div className="flex min-w-0 flex-[1_1_300px] flex-col gap-5 max-[899px]:hidden">
        <LearnerModelCard version={chat.learnerVersion} />
        <SuggestionCard />
        <PastChats onOpen={setViewing} />
      </div>
    </>
  )
}

