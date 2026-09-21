'use client'
import { Suspense, useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams, useRouter, useSearchParams } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { useLearningCatalog } from '@/hooks/useLearningCatalog'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { LearningLabel, useLabelContext } from '@/components/learning/LearningLabel'
import { AdvisoryList, MasarSummary, PathRoadmap } from '@/components/learning/PathRoadmap'
import { Button, buttonStyles } from '@/components/ui/Button'
import { Card, Spinner } from '@/components/ui/index'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { levelLabel } from '@/lib/learning'
import { cn } from '@/lib/utils'
import type { LearningPath } from '@/types'

type State = 'loading' | 'ready' | 'missing' | 'error'

/** The outcome of one request, tagged with the request it answers. Comparing
 *  the tag to the current request is what makes "loading" a derived value: after
 *  the level or fields change, the stored result no longer matches and the page
 *  reads as loading until the new answer lands — no state has to be reset. */
interface Outcome {
  key: string
  status: 'ready' | 'missing' | 'error'
  path?: LearningPath
}

/**
 * A path preview. Two kinds share this page: a predefined one
 * (`/paths/ai-engineer-computer-vision`) and a custom combination from Explore
 * (`/paths/custom?level=…&fields=…&goal=…`). Neither is saved — "Make this my
 * Masar" is the only thing that writes, and it goes through the same profile and
 * path calls onboarding does.
 */
function PathPreview() {
  const { isLoading: authLoading } = useAuth()
  const { slug } = useParams() as { slug: string }
  const search = useSearchParams()
  const router = useRouter()
  const { t } = useI18n()
  const ctx = useLabelContext()
  const { catalog } = useLearningCatalog()

  const custom = slug === 'custom'
  const [level, setLevel] = useState<string | null>(search.get('level'))
  const [outcome, setOutcome] = useState<Outcome | null>(null)
  const [saving, setSaving] = useState(false)
  const [saveFailed, setSaveFailed] = useState(false)
  const [hasPath, setHasPath] = useState(false)

  const fields = (search.get('fields') ?? '').split(',').filter(Boolean)
  const goal = search.get('goal')
  const fieldsKey = fields.join(',')

  // A custom combination needs its level and goal in the URL; without them
  // there is nothing to generate.
  const missingParams = custom && (!level || !goal)
  const key = `${slug}|${level}|${goal}|${fieldsKey}`
  const current = outcome?.key === key ? outcome : null
  const state: State = saveFailed ? 'error' : missingParams ? 'missing' : (current?.status ?? 'loading')
  const path = current?.path ?? null

  useEffect(() => {
    if (authLoading || missingParams) return
    let stale = false
    const request =
      custom && level && goal
        ? api.generateLearningPath({ level, fields: fieldsKey ? fieldsKey.split(',') : [], career_goal: goal })
        : api.getLearningPath(slug, level ?? undefined)
    request
      .then((p) => !stale && setOutcome({ key, status: 'ready', path: p }))
      .catch((err: { response?: { status?: number } }) => {
        if (!stale) setOutcome({ key, status: err?.response?.status === 404 ? 'missing' : 'error' })
      })
    return () => {
      stale = true
    }
  }, [authLoading, missingParams, custom, slug, level, goal, fieldsKey, key])

  useEffect(() => {
    if (authLoading) return
    api.getMyLearningProfile().then((p) => setHasPath(p.has_active_path)).catch(() => {})
  }, [authLoading])

  async function adopt() {
    if (!path) return
    setSaving(true)
    try {
      await api.saveMyLearningProfile({
        level: path.level.slug,
        // The fields the learner asked for — not the prerequisite routes the
        // backend added, which are the server's to add again next time.
        fields: path.fields.map((f) => f.slug),
        career_goal: path.career_goal.slug,
      })
      await api.saveMyLearningPath({ regenerate: true })
      router.push('/learn')
    } catch {
      setSaveFailed(true)
      setSaving(false)
    }
  }

  if (authLoading) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }

  return (
    <AppShell>
      <PageHeader title={t('paths.title')} />
      <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl space-y-6">
          {state === 'loading' && <div className="flex justify-center py-16"><Spinner announce className="h-6 w-6" /></div>}

          {state === 'missing' && (
            <Card className="p-8 text-center">
              <p className="mb-4 text-sm text-ghost">{t('paths.notFound')}</p>
              <Link href="/paths" className={buttonStyles({ variant: 'ghost', size: 'sm' })}>{t('paths.title')}</Link>
            </Card>
          )}

          {state === 'error' && (
            <Card className="p-8 text-center">
              <p role="alert" className="text-sm text-rose">{t('learn.loadError')}</p>
            </Card>
          )}

          {state === 'ready' && path && (
            <>
              {catalog && (
                <div role="radiogroup" aria-label={t('onb.summary.level')} className="flex flex-wrap gap-2">
                  {catalog.levels.map((l) => (
                    <button
                      key={l.slug}
                      type="button"
                      role="radio"
                      aria-checked={path.level.slug === l.slug}
                      onClick={() => setLevel(l.slug)}
                      className={cn(
                        'min-h-[44px] rounded-full border px-3.5 py-1.5 text-sm transition-colors lg:min-h-0',
                        path.level.slug === l.slug
                          ? 'border-amber/50 bg-amber/10 text-amber'
                          : 'border-border bg-panel text-soft hover:border-muted hover:text-bright'
                      )}
                    >
                      <LearningLabel parts={levelLabel(l, ctx)} />
                    </button>
                  ))}
                </div>
              )}

              <MasarSummary
                path={path}
                actions={
                  <Button size="sm" loading={saving} onClick={() => void adopt()}>
                    {t('paths.startWithThis')}
                  </Button>
                }
              />
              {hasPath && <p className="-mt-3 text-xs text-ghost">{t('paths.replacesCurrent')}</p>}
              <AdvisoryList path={path} catalogFields={catalog?.fields} />
              <PathRoadmap path={path} />
            </>
          )}
        </div>
      </div>
    </AppShell>
  )
}

export default function PathPreviewPage() {
  // useSearchParams needs a Suspense boundary for the page to prerender.
  return (
    <Suspense fallback={null}>
      <PathPreview />
    </Suspense>
  )
}
