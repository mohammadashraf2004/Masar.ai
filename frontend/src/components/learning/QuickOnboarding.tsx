'use client'
import { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n, type StringKey } from '@/lib/i18n'
import { fieldLabel } from '@/lib/learning'
import type { AiExperience, LearningField, ProgrammingExperience } from '@/types'
import { ChoiceCard } from './ChoiceCard'
import { LearningLabel, useLabelContext } from './LearningLabel'

const PROGRAMMING: ProgrammingExperience[] = ['none', 'basic', 'comfortable', 'professional']
const AI: AiExperience[] = ['none', 'basics', 'projects', 'applications']

interface QuickOnboardingProps {
  fields: LearningField[]
  onDone: () => void
  /** "Skip for now": leaves without saving anything. */
  onSkip: () => void
}

/**
 * The short first-time questions: how much programming, how much AI, and what the
 * learner wants to learn. Three steps, and no career track: the answers only help
 * the platform judge readiness and suggest where to start. They are sent to the
 * server as plain choices; nothing about the learner's level is computed here.
 */
export function QuickOnboarding({ fields, onDone, onSkip }: QuickOnboardingProps) {
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  const [step, setStep] = useState(0)
  const [programming, setProgramming] = useState<ProgrammingExperience | null>(null)
  const [ai, setAi] = useState<AiExperience | null>(null)
  const [interests, setInterests] = useState<string[]>([])
  const [saving, setSaving] = useState(false)
  const [failed, setFailed] = useState(false)

  const total = 3
  const canContinue = step === 0 ? programming !== null : step === 1 ? ai !== null : interests.length > 0
  // A field with no course at all cannot be an interest the platform can act on.
  const choices = fields.filter((f) => f.course_count > 0)

  async function finish() {
    setSaving(true)
    setFailed(false)
    try {
      await api.saveMyLearningProfile({
        programming_experience: programming,
        ai_experience: ai,
        fields: interests,
      })
      onDone()
    } catch {
      setFailed(true)
    }
    setSaving(false)
  }

  return (
    <Card className="mx-auto max-w-2xl space-y-6 p-6">
      <div>
        <h1 className="ui-page-title">{t('qob.title')}</h1>
        <p className="mt-1 text-sm text-soft">{t('qob.subtitle')}</p>
        <p className="mt-3 text-xs text-soft" aria-live="polite">{tf('qob.step', { n: step + 1, total })}</p>
      </div>

      {step === 0 && (
        <fieldset className="space-y-2">
          <legend className="mb-3 text-sm font-medium text-bright">{t('qob.prog.q')}</legend>
          <div role="radiogroup" aria-label={t('qob.prog.q')} className="space-y-2">
            {PROGRAMMING.map((value) => (
              <ChoiceCard
                key={value} role="radio" selected={programming === value}
                onSelect={() => setProgramming(value)} title={t(`qob.prog.${value}` as StringKey)}
              />
            ))}
          </div>
        </fieldset>
      )}

      {step === 1 && (
        <fieldset className="space-y-2">
          <legend className="mb-3 text-sm font-medium text-bright">{t('qob.ai.q')}</legend>
          <div role="radiogroup" aria-label={t('qob.ai.q')} className="space-y-2">
            {AI.map((value) => (
              <ChoiceCard
                key={value} role="radio" selected={ai === value}
                onSelect={() => setAi(value)} title={t(`qob.ai.${value}` as StringKey)}
              />
            ))}
          </div>
        </fieldset>
      )}

      {step === 2 && (
        <fieldset className="space-y-2">
          <legend className="mb-1 text-sm font-medium text-bright">{t('qob.interests.q')}</legend>
          <p className="mb-3 text-xs text-soft">{t('qob.interests.hint')}</p>
          <div role="group" aria-label={t('qob.interests.q')} className="grid gap-2 sm:grid-cols-2">
            {choices.map((f) => (
              <ChoiceCard
                key={f.slug} role="checkbox" selected={interests.includes(f.slug)}
                onSelect={() => setInterests((prev) => prev.includes(f.slug) ? prev.filter((s) => s !== f.slug) : [...prev, f.slug])}
                title={<LearningLabel parts={fieldLabel(f, ctx)} />}
              />
            ))}
          </div>
        </fieldset>
      )}

      {failed && <p role="alert" className="text-sm text-rose">{t('qob.saveError')}</p>}

      <div className="flex flex-wrap items-center justify-between gap-3">
        <button type="button" onClick={onSkip} className="min-h-[44px] text-xs text-soft underline hover:text-bright lg:min-h-0">
          {t('qob.skip')}
        </button>
        <div className="flex gap-2">
          {step > 0 && <Button variant="ghost" onClick={() => setStep(step - 1)}>{t('qob.back')}</Button>}
          {step < total - 1 ? (
            <Button disabled={!canContinue} onClick={() => setStep(step + 1)}>{t('qob.next')}</Button>
          ) : (
            <Button disabled={!canContinue} loading={saving} onClick={() => void finish()}>{t('qob.finish')}</Button>
          )}
        </div>
      </div>
    </Card>
  )
}
