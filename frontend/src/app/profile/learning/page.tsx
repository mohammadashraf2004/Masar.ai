'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { useLearningCatalog } from '@/hooks/useLearningCatalog'
import { AppShell } from '@/components/layout/AppShell'
import { LegalFooter } from '@/components/layout/LegalFooter'
import { PageHeader } from '@/components/layout/PageHeader'
import { FieldPicker, GoalPicker, LevelPicker } from '@/components/learning/Pickers'
import { MySkillsSection } from '@/components/learning/MySkills'
import { Button } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'

/**
 * The learning profile as one editable page. It renders the same three pickers
 * onboarding does — the options come from the API and the wording is defined
 * once — and saving rebuilds the path on the server.
 */
export default function LearningProfilePage() {
  const { isLoading: authLoading } = useAuth()
  const { t } = useI18n()
  const { catalog, error } = useLearningCatalog()
  const [level, setLevel] = useState<string | null>(null)
  const [fields, setFields] = useState<string[]>([])
  const [goal, setGoal] = useState<string | null>(null)
  const [loaded, setLoaded] = useState(false)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState<'saved' | 'error' | null>(null)

  useEffect(() => {
    if (authLoading) return
    api.getMyLearningProfile()
      .then((p) => {
        setLevel(p.level?.slug ?? null)
        setFields(p.fields.map((f) => f.slug))
        setGoal(p.career_goal?.slug ?? null)
      })
      .catch(() => {})
      .finally(() => setLoaded(true))
  }, [authLoading])

  const complete = !!level && fields.length > 0 && !!goal

  async function save() {
    if (!complete) return
    setSaving(true)
    setMessage(null)
    try {
      await api.saveMyLearningProfile({ level, fields, career_goal: goal })
      await api.saveMyLearningPath({ regenerate: true })
      setMessage('saved')
    } catch {
      setMessage('error')
    }
    setSaving(false)
  }

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  const chosenLevel = catalog?.levels.find((l) => l.slug === level) ?? null

  return (
    <AppShell>
      <PageHeader title={t('plp.title')} subtitle={t('plp.subtitle')} />
      <div className="flex flex-1 flex-col overflow-y-auto px-4 pt-6 pb-[calc(1.25rem+env(safe-area-inset-bottom))] sm:px-6 lg:px-8">
        <div className="mx-auto w-full max-w-3xl space-y-6">
          {error ? (
            <p role="alert" className="text-sm text-rose">{t('onb.loadError')}</p>
          ) : !catalog || !loaded ? (
            <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>
          ) : (
            <>
              <MySkillsSection />
              <Card className="p-5">
                <h2 className="ui-card-title mb-1">{t('onb.level.title')}</h2>
                <p className="mb-4 text-xs text-soft">{t('onb.level.hint')}</p>
                <LevelPicker levels={catalog.levels} value={level} onChange={setLevel} />
              </Card>
              <Card className="p-5">
                <h2 className="ui-card-title mb-1">{t('onb.fields.title')}</h2>
                <p className="mb-4 text-xs text-soft">{t('onb.fields.hint')}</p>
                <FieldPicker fields={catalog.fields} value={fields} onChange={setFields} level={chosenLevel} />
              </Card>
              <Card className="p-5">
                <h2 className="ui-card-title mb-1">{t('onb.goal.title')}</h2>
                <p className="mb-4 text-xs text-soft">{t('onb.goal.hint')}</p>
                <GoalPicker goals={catalog.goals} value={goal} onChange={setGoal} />
              </Card>

              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <Button size="lg" onClick={() => void save()} loading={saving} disabled={!complete}>
                  {t('plp.save')}
                </Button>
                {message === 'saved' && (
                  <p role="status" className="text-sm text-emerald">
                    {t('plp.saved')}{' '}
                    <Link href="/learn/masar" className="underline">{t('learn.title')}</Link>
                  </p>
                )}
                {message === 'error' && <p role="alert" className="text-sm text-rose">{t('plp.saveError')}</p>}
              </div>
            </>
          )}
        </div>
        <LegalFooter className="mx-auto w-full max-w-3xl" />
      </div>
    </AppShell>
  )
}
