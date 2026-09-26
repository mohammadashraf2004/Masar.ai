'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { BadgeCheck, CircleDot } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n, type StringKey } from '@/lib/i18n'
import { skillLabel } from '@/lib/learning'
import type { LearningProfile, MySkills } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'
import { SkillGapsPanel } from './SkillGapsPanel'
import { SkillsStep } from './SkillsStep'

type Load =
  | { kind: 'loading' }
  | { kind: 'error' }
  | { kind: 'ready'; skills: MySkills; profile: LearningProfile }

/**
 * Profile → My Skills: what the learner knows and is learning, and a way to
 * change it.
 *
 * "Known" is what the learner said (or a course they finished taught them);
 * "Learning" is derived from courses they have started. Editing reopens the same
 * "Skills & Technologies I Know" picker onboarding uses, and saving asks the
 * server to rebuild the roadmap around the new list — what they have finished
 * stays finished, and the message says so.
 */
export function MySkillsSection() {
  const { t, tf } = useI18n()
  const ctx = useLabelContext()
  // Bumped after a save, so the coverage below is asked for again.
  const [saves, setSaves] = useState(0)
  const [load, setLoad] = useState<Load>({ kind: 'loading' })
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState<string[]>([])
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState<'saved' | 'savedNoPath' | 'error' | null>(null)

  // Bumped by "try again" to re-run the load below.
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    let alive = true
    ;(async () => {
      try {
        const [skills, profile] = await Promise.all([api.getMySkills(), api.getMyLearningProfile()])
        if (alive) setLoad({ kind: 'ready', skills, profile })
      } catch {
        if (alive) setLoad({ kind: 'error' })
      }
    })()
    return () => {
      alive = false
    }
  }, [attempt])

  if (load.kind === 'loading') {
    return (
      <Card className="p-5">
        <div className="flex justify-center py-4" role="status" aria-label={t('common.loading')}><Spinner className="h-5 w-5" /></div>
      </Card>
    )
  }
  if (load.kind === 'error') {
    return (
      <Card className="p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <p role="alert" className="text-sm text-rose">{t('mys.loadError')}</p>
          <Button variant="ghost" size="sm" onClick={() => { setLoad({ kind: 'loading' }); setAttempt((n) => n + 1) }}>
            {t('common.retry')}
          </Button>
        </div>
      </Card>
    )
  }

  const { skills, profile } = load
  const canEdit = !!profile.career_goal

  function startEditing() {
    // Only what the learner declared is theirs to edit; skills inferred from a
    // finished course are shown as known but are not part of this list.
    setDraft(skills.known.filter((k) => k.source === 'self_declared').map((k) => k.skill.slug))
    setMessage(null)
    setEditing(true)
  }

  async function save() {
    setSaving(true)
    setMessage(null)
    try {
      const saved = await api.saveMySkills(draft)
      setLoad({ kind: 'ready', skills: { known: saved.known, learning: saved.learning }, profile })
      setEditing(false)
      setSaves((n) => n + 1)
      setMessage(saved.roadmap_updated ? 'saved' : 'savedNoPath')
    } catch {
      setMessage('error')
    }
    setSaving(false)
  }

  return (
    <Card className="p-5 sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <h2 className="text-sm font-semibold text-bright">{t('mys.title')}</h2>
        {!editing && (
          <Button variant="ghost" size="sm" onClick={startEditing} disabled={!canEdit}>
            {t('mys.edit')}
          </Button>
        )}
      </div>
      {!canEdit && <p className="mt-2 text-xs text-soft">{t('mys.needGoal')}</p>}

      {editing && profile.career_goal ? (
        <div className="mt-4">
          <h3 className="text-sm font-semibold text-bright">{t('skills.heading')}</h3>
          <p className="mb-4 mt-1 text-xs text-soft">{t('skills.hint')}</p>
          <SkillsStep
            query={{
              goal: profile.career_goal.slug,
              level: profile.level?.slug ?? null,
              fields: profile.fields.map((f) => f.slug),
            }}
            value={draft}
            onChange={setDraft}
          />
          <div className="mt-5 flex flex-wrap gap-2">
            <Button size="sm" loading={saving} onClick={() => void save()}>{t('mys.save')}</Button>
            <Button size="sm" variant="ghost" disabled={saving} onClick={() => setEditing(false)}>{t('mys.cancel')}</Button>
          </div>
        </div>
      ) : (
        <div className="mt-4 grid gap-5 sm:grid-cols-2">
          <section aria-labelledby="mys-known">
            <h3 id="mys-known" className="mb-2 text-xs font-medium uppercase tracking-widest text-soft">{t('mys.known')}</h3>
            {skills.known.length === 0 ? (
              <p className="text-sm text-soft">{t('mys.none')}</p>
            ) : (
              <ul className="space-y-1.5">
                {skills.known.map((k) => (
                  <li key={k.skill.slug} className="flex items-start gap-2 text-sm text-bright">
                    <BadgeCheck size={15} className="mt-0.5 shrink-0 text-sky" aria-hidden="true" />
                    <span className="min-w-0">
                      <LearningLabel parts={skillLabel(k.skill, ctx)} />
                      {k.source !== 'self_declared' && (
                        <span className="ms-2 text-xs text-soft">
                          {t(`mys.source.${k.source}` as StringKey)}
                        </span>
                      )}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </section>
          <section aria-labelledby="mys-learning">
            <h3 id="mys-learning" className="mb-2 text-xs font-medium uppercase tracking-widest text-soft">{t('mys.learning')}</h3>
            {skills.learning.length === 0 ? (
              <p className="text-sm text-soft">{t('mys.noneLearning')}</p>
            ) : (
              <ul className="space-y-1.5">
                {skills.learning.map((s) => (
                  <li key={s.slug} className="flex items-start gap-2 text-sm text-bright">
                    <CircleDot size={15} className="mt-0.5 shrink-0 text-amber-text" aria-hidden="true" />
                    <LearningLabel parts={skillLabel(s, ctx)} />
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      )}

      {!editing && canEdit && (
        <div className="mt-6 border-t border-border pt-5">
          <p className="mb-3 text-xs text-soft">
            {tf('mys.declared', { n: skills.known.filter((k) => k.source === 'self_declared').length })}
          </p>
          <SkillGapsPanel variant="profile" reloadKey={saves} />
        </div>
      )}

      {message === 'saved' && (
        <p role="status" className="mt-4 text-sm text-emerald">
          {t('mys.saved')}{' '}
          <Link href="/learn/masar" className="underline">{t('mys.viewRoadmap')}</Link>
        </p>
      )}
      {message === 'savedNoPath' && <p role="status" className="mt-4 text-sm text-emerald">{t('mys.savedNoPath')}</p>}
      {message === 'error' && <p role="alert" className="mt-4 text-sm text-rose">{t('mys.saveError')}</p>}
    </Card>
  )
}
