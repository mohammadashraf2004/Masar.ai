'use client'
import { useState } from 'react'
import { ArrowRight, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { fieldLabel, levelLabel, roleLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { LearningCatalog } from '@/hooks/useLearningCatalog'
import type { LearningPath } from '@/types'
import { FieldPicker, GoalPicker, LevelPicker } from './Pickers'
import { LearningLabel, useLabelContext } from './LearningLabel'
import { SkillsStep } from './SkillsStep'

const STEPS = 4

export interface OnboardingAnswers {
  level: string | null
  fields: string[]
  goal: string | null
  /** Skill slugs the learner says they already know. */
  skills: string[]
}

interface OnboardingFlowProps {
  catalog: LearningCatalog
  /** Answers to start from — a migrated learner's career goal, or a saved profile. */
  initial?: Partial<OnboardingAnswers>
  /** Called with the path the server built once the last step succeeds. */
  onDone: (path: LearningPath) => void
}

/**
 * Where am I? -> What interests me? -> Where do I want to go? -> What do I
 * already know? -> Build My Roadmap.
 *
 * The flow only collects answers. It does not decide what any of them means:
 * the last step saves the profile (with the skills the learner ticked) and asks
 * the server to build the path, and the server owns every rule about it — which
 * courses a known skill waives, which prerequisites remain, what is current. A
 * learner who picks an advanced field at a beginner level is told so and let
 * through — the route to it is the server's.
 */
export function OnboardingFlow({ catalog, initial, onDone }: OnboardingFlowProps) {
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  const [step, setStep] = useState(1)
  const [answers, setAnswers] = useState<OnboardingAnswers>({
    level: initial?.level ?? null,
    fields: initial?.fields ?? [],
    goal: initial?.goal ?? null,
    skills: initial?.skills ?? [],
  })
  const [building, setBuilding] = useState(false)
  const [error, setError] = useState(false)

  const level = catalog.levels.find((l) => l.slug === answers.level) ?? null
  const goal = catalog.goals.find((g) => g.slug === answers.goal) ?? null
  const chosenFields = catalog.fields.filter((f) => answers.fields.includes(f.slug))

  // Skills are optional: a learner who knows none of them, or is unsure, moves on.
  const ready =
    (step === 1 && !!answers.level) ||
    (step === 2 && answers.fields.length > 0) ||
    (step === 3 && !!answers.goal) ||
    step === 4
  const missing =
    step === 1 ? t('onb.needLevel') : step === 2 ? t('onb.needFields') : step === 3 ? t('onb.needGoal') : ''

  async function build() {
    if (!answers.level || !answers.goal || answers.fields.length === 0) return
    setBuilding(true)
    setError(false)
    try {
      await api.saveMyLearningProfile({
        level: answers.level,
        fields: answers.fields,
        career_goal: answers.goal,
        known_skills: answers.skills,
      })
      const path = await api.saveMyLearningPath({ regenerate: true })
      onDone(path)
    } catch {
      // The profile is saved before the path is built, so a failure here loses
      // nothing — the button simply tries the build again.
      setError(true)
      setBuilding(false)
    }
  }

  return (
    <div className="mx-auto w-full max-w-2xl">
      <div className="mb-6">
        <h1 className="font-display text-2xl font-bold text-white">{t('onb.title')}</h1>
        <p className="mt-1 text-sm text-soft">{t('onb.subtitle')}</p>
      </div>

      <div className="mb-5">
        <ol className="flex gap-1.5" aria-label={tf('onb.step', { n: step, total: STEPS })}>
          {Array.from({ length: STEPS }, (_, i) => (
            <li
              key={i}
              aria-current={i + 1 === step ? 'step' : undefined}
              className={cn(
                'h-1 flex-1 rounded-full transition-colors',
                i + 1 <= step ? 'bg-amber' : 'bg-muted'
              )}
            />
          ))}
        </ol>
        <p className="mt-2 text-xs text-soft">{tf('onb.step', { n: step, total: STEPS })}</p>
      </div>

      <Card className="p-5 sm:p-6">
        {step === 1 && (
          <section aria-labelledby="onb-h">
            <h2 id="onb-h" className="text-lg font-semibold text-bright">{t('onb.level.title')}</h2>
            <p className="mb-4 mt-1 text-sm text-soft">{t('onb.level.hint')}</p>
            <LevelPicker
              levels={catalog.levels}
              value={answers.level}
              onChange={(slug) => setAnswers((a) => ({ ...a, level: slug }))}
            />
          </section>
        )}

        {step === 2 && (
          <section aria-labelledby="onb-h">
            <h2 id="onb-h" className="text-lg font-semibold text-bright">{t('onb.fields.title')}</h2>
            <p className="mb-4 mt-1 text-sm text-soft">{t('onb.fields.hint')}</p>
            <FieldPicker
              fields={catalog.fields}
              value={answers.fields}
              level={level}
              onChange={(fields) => setAnswers((a) => ({ ...a, fields }))}
            />
          </section>
        )}

        {step === 3 && (
          <section aria-labelledby="onb-h">
            <h2 id="onb-h" className="text-lg font-semibold text-bright">{t('onb.goal.title')}</h2>
            <p className="mb-4 mt-1 text-sm text-soft">{t('onb.goal.hint')}</p>
            <GoalPicker
              goals={catalog.goals}
              value={answers.goal}
              onChange={(slug) => setAnswers((a) => ({ ...a, goal: slug }))}
            />
          </section>
        )}

        {step === 4 && answers.goal && (
          <section aria-labelledby="onb-h">
            <h2 id="onb-h" className="text-lg font-semibold text-bright">{t('skills.title')}</h2>
            <p className="mb-4 mt-1 text-sm text-soft">{t('skills.subtitle')}</p>
            <p className="mb-4 flex flex-wrap items-center gap-x-2 gap-y-1 rounded-lg border border-border bg-surface px-3 py-2.5 text-xs text-soft">
              {goal && <LearningLabel parts={roleLabel(goal, ctx)} className="text-bright" />}
              <span aria-hidden="true">·</span>
              {chosenFields.map((f, i) => (
                <span key={f.slug} className="inline-flex items-center gap-2">
                  {i > 0 && <span aria-hidden="true">+</span>}
                  <LearningLabel parts={fieldLabel(f, ctx, true)} />
                </span>
              ))}
              <span aria-hidden="true">·</span>
              {level && <LearningLabel parts={levelLabel(level, ctx)} />}
            </p>
            <h3 className="text-sm font-semibold text-bright">{t('skills.heading')}</h3>
            <p className="mb-4 mt-1 text-xs text-soft">{t('skills.hint')}</p>
            <SkillsStep
              query={{ goal: answers.goal, level: answers.level, fields: answers.fields }}
              value={answers.skills}
              onChange={(skills) => setAnswers((a) => ({ ...a, skills }))}
            />
            <p className="mt-5 text-xs text-soft">{t('skills.selfNote')}</p>
            {error && (
              <p role="alert" className="mt-4 rounded-md border border-rose/30 bg-rose/10 px-3 py-2.5 text-xs text-rose">
                {t('onb.build.error')}
              </p>
            )}
          </section>
        )}

        <div className="mt-6 flex flex-col-reverse gap-3 sm:flex-row sm:items-center sm:justify-between">
          {step > 1 ? (
            <Button variant="ghost" onClick={() => setStep((s) => s - 1)} disabled={building}>
              {t('onb.back')}
            </Button>
          ) : (
            <span />
          )}

          {step < STEPS ? (
            <div className="flex flex-col items-stretch gap-2 sm:items-end">
              <Button onClick={() => setStep((s) => s + 1)} disabled={!ready}>
                {t('onb.next')} <ArrowRight size={14} className="rtl:rotate-180" />
              </Button>
              {!ready && <p className="text-xs text-soft" aria-live="polite">{missing}</p>}
            </div>
          ) : (
            <Button size="lg" onClick={() => void build()} loading={building}>
              <Sparkles size={14} /> {building ? t('onb.build.building') : t('onb.build.cta')}
            </Button>
          )}
        </div>
      </Card>
    </div>
  )
}
