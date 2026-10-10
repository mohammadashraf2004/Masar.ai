'use client'
import { Fragment, useState } from 'react'
import Link from 'next/link'
import { MentorCodeBlock } from '@/components/mentor/MentorCodeBlock'
import { MentorMarkdown } from '@/components/mentor/MentorMarkdown'
import { useMentorV2I18n, type MentorV2Key } from '@/lib/i18n'
import { cn } from '@/lib/utils'
import { HintLadder } from './HintLadder'
import { lessonHref } from './links'
import { QuizBlock } from './QuizBlock'
import type { MentorBlock, MentorMessageV2, QuizAnswerResult } from './types'

/** What the blocks of a message can do back to the conversation. */
export interface MessageActions {
  /** The exercise a hint ladder belongs to. */
  exerciseId?: string
  onQuizResult?: (result: QuizAnswerResult) => void
  /** The learner answered a "quick check" question inline. */
  onCheckAnswer?: (answer: string, question: string) => void
  /** A further hint was revealed. */
  onHintMessage?: (message: MentorMessageV2) => void
}

/** An LTR row of mono boxes with arrows: the focus is accented, a node after it is dashed (not reached yet). */
export function ConceptChain({ nodes, focus }: { nodes: string[]; focus: number }) {
  return (
    <div dir="ltr" role="list" className="flex flex-wrap items-center gap-1.5">
      {nodes.map((node, i) => (
        <Fragment key={node}>
          {i > 0 && <span aria-hidden="true" className="font-mono text-xs text-ghost">→</span>}
          <span
            role="listitem"
            aria-current={i === focus ? 'step' : undefined}
            data-state={i === focus ? 'focus' : i > focus ? 'future' : 'past'}
            className={cn(
              'rounded-md border px-2 py-1 font-mono text-xs',
              i === focus ? 'border-amber bg-amber-soft text-amber-text'
                : i > focus ? 'border-dashed border-border text-ghost'
                : 'border-border text-bright',
            )}
          >
            {node}
          </span>
        </Fragment>
      ))}
    </div>
  )
}

function CheckBlock({ question, onAnswer }: { question: string; onAnswer?: (answer: string, question: string) => void }) {
  const { t } = useMentorV2I18n()
  const [value, setValue] = useState('')
  const [sent, setSent] = useState(false)
  return (
    <form
      className="flex flex-col gap-2 rounded-lg border border-border bg-surface p-3"
      onSubmit={(e) => {
        e.preventDefault()
        if (!value.trim() || sent) return
        setSent(true)
        onAnswer?.(value.trim(), question)
      }}
    >
      <span className="text-xs font-semibold text-amber-text">{t('mentor.v2.check')}</span>
      <p dir="auto" className="text-sm leading-[1.7] text-white">{question}</p>
      <div className="flex gap-2">
        <input
          dir="auto"
          value={value}
          disabled={sent}
          onChange={(e) => setValue(e.target.value)}
          aria-label={question}
          placeholder={t('mentor.v2.answerPlaceholder')}
          className="min-h-[44px] min-w-0 flex-1 rounded-lg border border-border bg-void px-3 text-sm text-bright placeholder:text-ghost focus:border-amber/50 focus:outline-none disabled:opacity-60"
        />
        <button
          type="submit"
          disabled={sent || !value.trim()}
          className="min-h-[44px] rounded-lg border border-border px-3 text-[13px] text-bright hover:border-amber/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-40"
        >
          {t('mentor.v2.checkSend')}
        </button>
      </div>
    </form>
  )
}

/**
 * "From this lesson" (solid amber border) or "Extra concept · <lesson title>" (dashed), linking to
 * that lesson. The title, course and lesson id are the server's verified source - a reference the
 * model made up never reaches here - and the link is built by the app. A general answer has no pill.
 */
export function GroundingPill({ grounding, sourceLessonId, sourceCourseId, sourceTitle }: {
  grounding: 'lesson' | 'extra' | 'general'; sourceLessonId?: string; sourceCourseId?: string; sourceTitle?: string
}) {
  const { t, tf } = useMentorV2I18n()
  if (grounding === 'general') return null
  const href = grounding === 'extra' ? lessonHref(sourceCourseId, sourceLessonId) : null
  const label = grounding === 'lesson'
    ? t('mentor.v2.grounding.lesson')
    : sourceTitle
      ? tf('mentor.v2.grounding.extraTitle', { title: sourceTitle })
      // No verified title to name: say only that it is extra (never a database id as a number).
      : tf('mentor.v2.grounding.extra', { n: '' }).split('·')[0].trim()
  const className = cn(
    'inline-flex self-start rounded-full border px-2.5 py-0.5 text-xs',
    grounding === 'lesson' ? 'border-amber text-amber-text' : 'border-dashed border-ghost text-dim',
    href && 'hover:text-bright focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring',
  )
  if (href) {
    return (
      <Link href={href} data-grounding={grounding} dir="auto" className={className} title={t('mentor.v2.grounding.open')}>
        {label}
      </Link>
    )
  }
  return <span data-grounding={grounding} dir="auto" className={className}>{label}</span>
}

/** Renders blocks in order. The same renderer draws a reply, a quiz's feedback and the lesson panel's answer. */
export function MentorBlocks({ blocks, actions = {} }: { blocks: MentorBlock[]; actions?: MessageActions }) {
  return (
    <>
      {blocks.map((block, i) => {
        switch (block.kind) {
          case 'text':
            return (
              <div key={i} className="flex flex-col gap-1.5">
                <GroundingPill grounding={block.grounding} sourceLessonId={block.sourceLessonId} sourceCourseId={block.sourceCourseId} sourceTitle={block.sourceTitle} />
                <div dir="auto"><MentorMarkdown>{block.text}</MentorMarkdown></div>
              </div>
            )
          case 'concept_chain':
            return <ConceptChain key={i} nodes={block.nodes} focus={block.focus} />
          case 'code':
            return <MentorCodeBlock key={i} code={block.code} lang={block.lang} />
          case 'hint':
            return <HintLadder key={i} exerciseId={actions.exerciseId ?? ''} first={block} onReveal={actions.onHintMessage} />
          case 'quiz':
            return (
              <QuizBlock
                key={i}
                block={block}
                onResult={actions.onQuizResult}
                renderFeedback={(feedback) => <MentorBlocks blocks={feedback} actions={actions} />}
              />
            )
          case 'check':
            return <CheckBlock key={i} question={block.question} onAnswer={actions.onCheckAnswer} />
        }
      })}
    </>
  )
}

function IntentTag({ intent }: { intent: string }) {
  return (
    <span dir="ltr" className="inline-flex self-start rounded-md border border-border bg-surface px-1.5 py-0.5 font-mono text-xs text-dim">
      {intent}
    </span>
  )
}

const TRIGGER_KEYS: Record<string, MentorV2Key | undefined> = {
  lesson_completed: 'mentor.v2.trigger.lesson_completed',
}

/**
 * A mentor message that opened itself (`proactive`): on the page background with a border, headed
 * "PROACTIVE · QUIZ", the trigger, and a pill that says it is free. No credit counter moves for it.
 */
export function ProactiveCard({ message, actions }: { message: MentorMessageV2; actions?: MessageActions }) {
  const { t } = useMentorV2I18n()
  // The server names the trigger by code; the words come from the active language, so the card
  // reads right after a language switch. A code this build does not know is shown as sent.
  const trigger = message.proactive?.trigger ?? ''
  const triggerKey = TRIGGER_KEYS[trigger]
  return (
    <div data-testid="proactive-card" className="flex w-full max-w-[88%] flex-col gap-3 self-start rounded-xl border border-border bg-void p-3.5">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
        <span dir="ltr" className="ui-eyebrow ui-eyebrow-accent font-mono">
          {t('mentor.v2.proactive')}{message.intent ? ` · ${message.intent}` : ''}
        </span>
        <span dir="auto" className="min-w-0 flex-1 text-xs text-dim">{triggerKey ? t(triggerKey) : trigger}</span>
        <span className="rounded-full border border-emerald px-2 py-0.5 text-xs text-emerald">{t('mentor.v2.proactiveFree')}</span>
      </div>
      <MentorBlocks blocks={message.blocks} actions={actions} />
    </div>
  )
}

/** One message of the v2 conversation. */
export function MentorMessageView({ message, actions }: { message: MentorMessageV2; actions?: MessageActions }) {
  const { t, tf } = useMentorV2I18n()
  if (message.proactive) return <ProactiveCard message={message} actions={actions} />

  if (message.role === 'learner') {
    const text = message.blocks.flatMap((b) => (b.kind === 'text' ? [b.text] : [])).join('\n')
    return (
      <div
        dir="auto"
        data-role="learner"
        className="min-w-0 max-w-[88%] self-end whitespace-pre-wrap rounded-xl rounded-be-[4px] bg-amber-soft px-3.5 py-3 text-sm leading-[1.75] text-bright [overflow-wrap:anywhere]"
      >
        {message.intent && <div className="mb-1.5"><IntentTag intent={message.intent} /></div>}
        {text}
      </div>
    )
  }

  return (
    <div
      data-role="mentor"
      className="flex min-w-0 max-w-[88%] flex-col gap-2.5 self-start rounded-xl rounded-bs-[4px] border border-border bg-panel px-3.5 py-3 text-sm leading-[1.75] text-soft [overflow-wrap:anywhere]"
    >
      {message.intent && <IntentTag intent={message.intent} />}
      <MentorBlocks blocks={message.blocks} actions={actions} />
      <span dir="ltr" className="self-end font-mono text-xs text-ghost" data-testid="message-cost">
        {message.creditCost === 0 ? t('mentor.v2.free') : tf('mentor.v2.spent', { n: message.creditCost })}
      </span>
    </div>
  )
}
