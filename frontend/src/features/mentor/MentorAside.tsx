'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { api, mentorV2 } from '@/lib/api'
import { Card } from '@/components/ui/index'
import { toThread, type Thread } from '@/hooks/useMentorChat'
import { useI18n, useMentorV2I18n, type MentorV2Key } from '@/lib/i18n'
import { formatShortDate } from '@/lib/mentor/format'
import { cn } from '@/lib/utils'
import type { LearnerModel, MentorSuggestion, SkillStatus } from './types'

const STATUS_TONE: Record<SkillStatus, string> = {
  mastered: 'border-emerald text-emerald',
  learning: 'border-amber text-amber-text',
  needs_review: 'border-rose text-rose',
}

/**
 * "What the mentor knows about you", from the server's learner model: the position, and each skill
 * with its status, confidence and the evidence behind it. The note under it is a promise the server
 * keeps: one mistake does not change a status. It refetches whenever `version` changes (a quiz answer).
 */
export function LearnerModelCard({ version }: { version: number }) {
  const { t, language } = useMentorV2I18n()
  const [model, setModel] = useState<LearnerModel | null>(null)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    let alive = true
    mentorV2.learner(language).then(
      (m) => { if (alive) { setModel(m); setFailed(false) } },
      () => { if (alive) setFailed(true) },
    )
    return () => { alive = false }
  }, [version, language])

  // Only what the server knows: an unknown track, course or lesson is left out, never filled in.
  const position = model ? [model.position.track, model.position.course, model.position.lesson].filter(Boolean) : []

  return (
    <Card className="flex flex-col gap-3.5 p-5" data-testid="learner-model" data-tour="mentor-learner">
      <h2 className="ui-card-title">{t('mentor.v2.learner.title')}</h2>
      {model && position.length > 0 && (
        <p dir="auto" className="flex flex-wrap items-center gap-1.5 font-mono text-xs text-dim">
          {position.map((part, i) => (
            <span key={`${i}-${part}`} className="inline-flex items-center gap-1.5">
              {i > 0 && <span aria-hidden="true">›</span>}
              <span className={i === position.length - 1 ? 'text-amber-text' : undefined}>{part}</span>
            </span>
          ))}
        </p>
      )}
      {model && model.skills.length === 0 && <p className="text-xs leading-relaxed text-ghost">{t('mentor.v2.learner.empty')}</p>}
      {!model && !failed && <p className="text-xs text-ghost">{t('mentor.v2.learner.loading')}</p>}
      {failed && <p role="alert" className="text-xs text-rose">{t('mentor.v2.failedNoCharge')}</p>}
      {model && (
        <ul className="flex flex-col gap-3.5">
          {model.skills.map((skill) => (
            <li key={skill.name} className="flex flex-col gap-1.5" data-skill={skill.name}>
              <div className="flex items-center gap-2">
                <span dir="ltr" className="min-w-0 flex-1 truncate text-caption font-medium text-bright">{skill.name}</span>
                <span data-status={skill.status} className={cn('whitespace-nowrap rounded-full border px-2 py-0.5 text-xs', STATUS_TONE[skill.status])}>
                  {t(`mentor.v2.status.${skill.status}` as MentorV2Key)}
                </span>
                <span dir="ltr" className="font-mono text-xs text-dim">{skill.confidence.toFixed(2)}</span>
              </div>
              <div className="progress-track h-1 w-full">
                <div className={cn('progress-fill', skill.status === 'needs_review' ? 'bg-rose' : skill.status === 'mastered' ? 'bg-emerald' : 'bg-amber')} style={{ width: `${Math.round(skill.confidence * 100)}%` }} />
              </div>
              {skill.evidence.map((line) => <p key={line} dir="auto" className="text-xs text-ghost">{line}</p>)}
            </li>
          ))}
        </ul>
      )}
      <p className="text-xs leading-relaxed text-ghost">{t('mentor.v2.learner.note')}</p>
    </Card>
  )
}

/** The mentor's one proactive suggestion (the server allows one every 24 hours). Starting or dismissing it is told to the server. */
export function SuggestionCard() {
  const { t, language } = useMentorV2I18n()
  const [suggestion, setSuggestion] = useState<MentorSuggestion | null>(null)

  useEffect(() => {
    let alive = true
    mentorV2.suggestion(language).then((s) => { if (alive) setSuggestion(s) }, () => {})
    return () => { alive = false }
  }, [language])

  if (!suggestion) return null

  const resolve = () => { void mentorV2.resolveSuggestion(suggestion.id); setSuggestion(null) }

  return (
    <Card data-testid="suggestion-card" className="flex flex-col gap-3 border-amber/30 p-5 [background-image:radial-gradient(90%_120%_at_0%_0%,rgb(var(--acc)/var(--acc-soft-a)),transparent_60%)]">
      <span dir="ltr" className="ui-eyebrow ui-eyebrow-accent font-mono">{t('mentor.v2.suggestion.label')}</span>
      <p dir="auto" className="text-sm leading-[1.7] text-bright">{suggestion.text}</p>
      <div className="flex flex-wrap gap-2">
        <Link
          href={suggestion.action.href}
          onClick={resolve}
          className="inline-flex min-h-[44px] items-center rounded-lg bg-amber px-3.5 text-[13px] font-semibold text-on-amber hover:bg-amber2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
        >
          {suggestion.action.label}
        </Link>
        <button
          type="button"
          onClick={resolve}
          className="min-h-[44px] rounded-lg border border-border px-3.5 text-[13px] text-bright hover:border-amber/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
        >
          {t('mentor.v2.suggestion.later')}
        </button>
      </div>
      <p className="text-xs text-ghost">{t('mentor.v2.suggestion.note')}</p>
    </Card>
  )
}

/** The existing conversation list, compact (40px rows). Earlier threads are read in place. */
export function PastChats({ onOpen }: { onOpen?: (thread: Thread) => void }) {
  const { t, language } = useI18n()
  const [threads, setThreads] = useState<Thread[]>([])
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    let alive = true
    api.getMentorSessions().then(
      (sessions) => {
        if (alive) setThreads(sessions.map(toThread).sort((a, b) => Date.parse(b.at) - Date.parse(a.at)))
      },
      () => {},
    ).finally(() => { if (alive) setLoaded(true) })
    return () => { alive = false }
  }, [])

  return (
    <Card className="p-5">
      <h2 className="ui-card-title mb-2">{t('mentor.threads')}</h2>
      {threads.length === 0 ? (
        loaded && <p className="py-2 text-[13px] text-ghost">{t('mentor.threads.empty')}</p>
      ) : (
        <ul>
          {threads.slice(0, 6).map((thread) => (
            <li key={thread.id} className="border-t border-border first:border-t-0">
              <button
                type="button"
                onClick={() => onOpen?.(thread)}
                className="flex h-10 w-full items-center justify-between gap-3 text-start text-[13px] text-soft transition-colors hover:text-bright focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring max-lg:min-h-[44px]"
              >
                <span dir="auto" className="min-w-0 flex-1 truncate">{thread.title || t('mentor.thread.untitled')}</span>
                <span className="shrink-0 text-xs text-ghost">{formatShortDate(thread.at, language)}</span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </Card>
  )
}
