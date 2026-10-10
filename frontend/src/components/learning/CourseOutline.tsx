'use client'
import Link from 'next/link'
import { Clock } from 'lucide-react'
import { Badge, Card, DifficultyBadge, ProgressBar } from '@/components/ui/index'
import { pick } from '@/lib/content-language'
import { useI18n, type StringKey } from '@/lib/i18n'
import { fieldLabel, labelText, roleLabel, skillLabel, titleLabel } from '@/lib/learning'
import type { CatalogCourseDetail } from '@/types'
import { LearningLabel, useLabelContext } from './LearningLabel'
import { SkillChips } from './SkillChips'
import { GatedLink } from '@/components/auth/AuthPrompt'

const HEADING = 'mb-3 text-card-title font-semibold text-bright'

function normalizedCopy(value: string) {
  return value
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/[.!?؟]+$/, '')
    .toLocaleLowerCase()
}

/**
 * Everything the course page says about a course before its lessons: what it is
 * about, what it teaches, its modules and projects, what it builds on and which
 * roadmaps use it. Structure only: no lesson text is here or in the payload.
 */
export function CourseOutline({ course }: { course: CatalogCourseDetail }) {
  const { t, tf, language } = useI18n()
  const ctx = useLabelContext()

  const description = pick(course.description, course.description_ar, language)
  const rawObjectives = (language === 'ar' && course.learning_objectives_ar?.length
    ? course.learning_objectives_ar
    : course.learning_objectives) ?? []
  const descriptionKey = description ? normalizedCopy(description) : ''
  const seenObjectives = new Set<string>()
  const objectives = rawObjectives.filter((objective) => {
    const key = normalizedCopy(objective)
    if (!key || key === descriptionKey || seenObjectives.has(key)) return false
    seenObjectives.add(key)
    return true
  })
  const modules = course.modules ?? []
  const projects = course.projects ?? []
  const recommended = course.recommended_prerequisites ?? []
  const roadmaps = course.roadmaps ?? []

  return (
    <div className="space-y-4">
      <Card className="space-y-4 p-5">
        <div className="ui-caption flex flex-wrap items-center gap-2">
          <DifficultyBadge level={course.level.slug} />
          {course.estimated_hours > 0 && (
            <span className="inline-flex items-center gap-1">
              <Clock size={12} aria-hidden="true" />
              {tf('card.hours', { n: Math.round(course.estimated_hours) })}
            </span>
          )}
          {course.module_count ? <span>{tf('card.modules', { n: course.module_count })}</span> : null}
          {course.lesson_count ? <span>{tf('card.lessons', { n: course.lesson_count })}</span> : null}
          {course.fields.map((f) => (
            <span key={f.slug} className="rounded border border-border px-1.5 py-0.5">
              <LearningLabel parts={fieldLabel(f, ctx, true)} />
            </span>
          ))}
        </div>

        {description && (
          <div>
            <h2 className={HEADING}>{t('cp.about')}</h2>
            <p className="ui-body-copy" dir="auto">{description}</p>
          </div>
        )}

        {objectives.length > 0 && (
          <div>
            <h2 className={HEADING}>{t('card.objectives')}</h2>
            <ul className="list-disc space-y-1 ps-5 text-body-copy text-soft">
              {objectives.map((o) => <li key={o} dir="auto">{o}</li>)}
            </ul>
          </div>
        )}

        {course.skills.length > 0 && (
          <div>
            <h2 className={HEADING}>{t('card.skills')}</h2>
            <SkillChips skills={course.skills} />
          </div>
        )}
      </Card>

      {(course.prerequisites.length > 0 || recommended.length > 0 || course.assumes.length > 0) && (
        <Card className="space-y-3 p-5">
          <h2 className={HEADING}>{t('cp.prerequisites')}</h2>
          {course.prerequisites.length > 0 && (
            <div>
              <p className="mb-1 text-xs text-soft">{t('cp.required')}</p>
              <ul className="space-y-1 text-sm">
                {course.prerequisites.map((p) => (
                  <li key={p.slug}>
                    <Link href={`/courses/${p.slug}`} className="text-amber-text hover:text-amber-text2">
                      <LearningLabel parts={titleLabel(p, ctx)} />
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {recommended.length > 0 && (
            <div>
              <p className="mb-1 text-xs text-soft">{t('cp.alsoHelpful')}</p>
              <ul className="space-y-1 text-sm">
                {recommended.map((p) => (
                  <li key={p.slug}>
                    <Link href={`/courses/${p.slug}`} className="text-amber-text hover:text-amber-text2">
                      <LearningLabel parts={titleLabel(p, ctx)} />
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {course.assumes.length > 0 && (
            <p className="text-sm text-soft">
              {t('card.assumes')}: {course.assumes.map((s) => labelText(skillLabel(s, ctx))).join(', ')}
            </p>
          )}
        </Card>
      )}

      {modules.length > 0 ? (
        <Card className="p-5">
          <h2 className={HEADING}>{t('cp.modules')}</h2>
          <ol className="divide-y divide-border">
            {modules.map((m) => (
              <li key={m.id} className="py-3 first:pt-0 last:pb-0">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-bright" dir="auto">
                      <span className="text-soft">{m.order}. </span>
                      {pick(m.title, m.title_ar, language)}
                    </p>
                    <p className="mt-0.5 text-xs text-soft">
                      {tf('cp.moduleLessons', { n: m.lesson_count })}
                      {m.estimated_hours ? ` · ${tf('card.hours', { n: Math.round(m.estimated_hours) })}` : ''}
                    </p>
                  </div>
                  <div className="flex shrink-0 flex-col items-end gap-1.5">
                    {m.is_optional === true && (
                      <Badge variant="ghost">
                        {course.slug === 'course-016' ? t('course.optionalKubernetes') : t('course.optionalModule')}
                      </Badge>
                    )}
                    {m.status === 'completed' && <Badge variant="emerald">{t('enr.completed')}</Badge>}
                  </div>
                </div>
                {m.completion_pct != null && m.completion_pct > 0 && m.status !== 'completed' && (
                  <ProgressBar value={m.completion_pct} className="mt-2" />
                )}
                {/* The outline: lesson names, folded so a long module does not bury the
                    page. A lesson opens through sign-in for a visitor; for a learner the
                    lesson page and the server apply the course's own Free/Pro rules. */}
                {(m.lessons?.length ?? 0) > 0 && (
                  <details className="group mt-2">
                    <summary className="inline-flex min-h-[44px] cursor-pointer list-none items-center gap-1 text-xs text-soft hover:text-bright lg:min-h-0 [&::-webkit-details-marker]:hidden">
                      <span aria-hidden="true" className="inline-block transition-transform group-open:rotate-90 rtl:-scale-x-100">›</span>
                      {t('cp.lessonList')}
                    </summary>
                    <ol className="mt-1 space-y-0.5 ps-4">
                      {m.lessons!.map((lesson) => {
                        const title = pick(lesson.title, lesson.title_ar, language)
                        return (
                          <li key={lesson.id} className="text-sm" dir="auto">
                            {course.kind === 'tool_course' ? (
                              <GatedLink
                                href={`/courses/${course.slug}/lessons/${lesson.id}`}
                                className="inline-flex min-h-[44px] items-center text-soft hover:text-amber-text lg:min-h-0 lg:py-0.5"
                              >
                                {title}
                              </GatedLink>
                            ) : (
                              <span className="inline-flex min-h-[44px] items-center text-soft lg:min-h-0 lg:py-0.5">{title}</span>
                            )}
                          </li>
                        )
                      })}
                    </ol>
                  </details>
                )}
              </li>
            ))}
          </ol>
        </Card>
      ) : (
        !course.is_available && <Card className="p-5 text-sm text-soft">{t('cp.notPublished')}</Card>
      )}

      {projects.length > 0 && (
        <Card className="p-5">
          <h2 className={HEADING}>{t('cp.projects')}</h2>
          <ul className="space-y-2 text-sm">
            {projects.map((p) => (
              <li key={p.id} className="flex flex-wrap items-center gap-2">
                <span className="text-bright" dir="auto">{pick(p.title, p.title_ar, language)}</span>
                <Badge variant={p.kind === 'capstone' ? 'amber' : 'ghost'}>{t(`cp.project.${p.kind}` as StringKey)}</Badge>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {roadmaps.length > 0 && (
        <Card className="p-5">
          <h2 className={HEADING}>{t('cp.roadmaps')}</h2>
          <ul className="space-y-1.5 text-sm">
            {roadmaps.map((r) => (
              <li key={r.career_goal.slug} className="flex flex-wrap items-center gap-2">
                <Link href={`/roadmaps/${r.career_goal.slug}`} className="text-amber-text hover:text-amber-text2">
                  <LearningLabel parts={roleLabel(r.career_goal, ctx)} />
                </Link>
                <Badge variant={r.track_role === 'core' ? 'amber' : 'ghost'}>{t(`card.role.${r.track_role}` as StringKey)}</Badge>
              </li>
            ))}
          </ul>
          <p className="mt-3 text-xs text-soft">{t('cp.roadmaps.note')}</p>
        </Card>
      )}
    </div>
  )
}
