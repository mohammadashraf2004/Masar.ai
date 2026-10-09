'use client'
import { useRef, useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, ArrowRight, CheckCircle } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { Card, Spinner } from '@/components/ui/index'
import { Button, buttonStyles } from '@/components/ui/Button'
import { LessonExercises } from './LessonExercises'
import { LessonBackLink } from './LessonBackLink'
import { MarkdownLesson } from '@/components/ui/MarkdownLesson'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { localizedTitle, localizedBody } from '@/lib/content-language'
import { cn } from '@/lib/utils'
import { useLessonPage } from './useLessonPage'
import { useLessonScrollSteps } from './useLessonScrollSteps'
import { LessonStepSwitch } from './LessonStepSwitch'
import { LessonAside } from './LessonAside'
// [mentor-v2]
import { mentorV2Enabled } from '@/features/mentor/flag'
import { LessonMentorLayer } from './mentor/LessonMentorLayer'
// [/mentor-v2]

export function LessonPage({ courseSlug, lessonParam }: { courseSlug: string; lessonParam: string }) {
  const { isLoading: authLoading, isAuthenticated } = useAuth()
  const { t, tf, language } = useI18n()
  const data = useLessonPage(courseSlug, lessonParam, !authLoading && isAuthenticated)
  const [completed, setCompleted] = useState(false)
  const [marking, setMarking] = useState(false)
  const [mentorPanelOpen, setMentorPanelOpen] = useState(false)
  const hasExercise = data.exercises.length > 0

  const { containerRef, dividerRef, active, scrollTo } = useLessonScrollSteps({ hasExercise })
  // [mentor-v2] the article the selection toolbar listens inside
  const articleRef = useRef<HTMLElement>(null)
  // [/mentor-v2]

  function handleExercisePassed(exerciseId: number, exerciseType?: string) {
    // Deterministic code submission records progress atomically on the
    // backend. The generic progress route deliberately refuses code ids.
    if (exerciseType === 'code') return
    if (data.topicId != null) {
      api.updateToolTopicProgress(data.topicId, { exercise_id: exerciseId }).catch(() => {})
    }
  }

  async function markComplete() {
    if (completed || data.isCompleted) return
    setMarking(true)
    try {
      if (data.topicId != null) {
        await api.updateToolTopicProgress(data.topicId, { lesson_id: data.lesson.id })
      }
      setCompleted(true)
    } finally {
      setMarking(false)
    }
  }

  if (data.state === 'loading') {
    return (
      <AppShell>
        <div className="flex flex-1 items-center justify-center"><Spinner announce className="h-6 w-6" /></div>
      </AppShell>
    )
  }

  if (data.state === 'missing') {
    return (
      <AppShell>
        <div className="flex flex-1 items-center justify-center p-6">
          <Card className="space-y-3 p-8 text-center">
            <p className="text-sm text-soft">{t('card.notFound')}</p>
            <Link href={`/courses/${courseSlug}`} className={buttonStyles({ variant: 'ghost', size: 'sm' })}>
              {t('nav.explore')}
            </Link>
          </Card>
        </div>
      </AppShell>
    )
  }

  const body = localizedBody(data.lesson, language)
  const title = localizedTitle(data.lesson, language)
  const previousHref = data.previousLessonId != null ? `/courses/${courseSlug}/lessons/${data.previousLessonId}` : null
  const nextHref = data.nextLessonId != null ? `/courses/${courseSlug}/lessons/${data.nextLessonId}` : null
  const lessonComplete = completed || data.isCompleted

  return (
    <AppShell>
      {/* [code-cell] min-h-0 lets this flex child use the full desktop viewport as its scrollport. */}
      <div
        ref={containerRef}
        data-testid="lesson-scroll-container"
        data-mentor-open={mentorPanelOpen || undefined}
        className={cn(
          // Below lg the window scrolls: `clip` (unlike `hidden`) does not make
          // this a scroll container, so the sticky step bar sticks to the viewport.
          'min-h-0 min-w-0 flex-1 px-4 py-6 max-lg:overflow-x-clip sm:px-6 lg:overflow-y-auto lg:overflow-x-hidden lg:px-8',
          hasExercise && 'lg:scroll-pt-28',
          mentorPanelOpen && 'min-[1280px]:pe-[392px]',
        )}
      >
        <div className="mx-auto max-w-5xl space-y-5">
          <LessonBackLink
            href={`/courses/${data.course.slug}`}
            label={localizedTitle({ title: data.course.title, title_ar: data.course.title_ar }, language)}
          />
          {/* [/code-cell] */}
          {/* ── Header ── */}
          <header className="space-y-2.5">
            <nav aria-label="breadcrumb" className="flex flex-wrap items-center gap-1.5 text-xs text-ghost" dir="auto">
              {data.track && (
                <>
                  <Link href={`/tracks/${data.track.slug}`} className="hover:text-bright">
                    {localizedTitle({ title: data.track.title, title_ar: data.track.title_ar }, language)}
                  </Link>
                  <span aria-hidden="true">/</span>
                </>
              )}
              <Link href={`/courses/${data.course.slug}`} className="hover:text-bright">
                {localizedTitle({ title: data.course.title, title_ar: data.course.title_ar }, language)}
              </Link>
              <span aria-hidden="true">/</span>
              <span className="text-amber-text">{tf('lessons.of', { n: data.lessonNumber, total: data.lessonTotal })}</span>
            </nav>

            <h1 dir="auto" className="font-display text-[28px] font-bold leading-[1.35] text-white">{title}</h1>

            <div className="flex flex-wrap items-center gap-2 text-xs text-dim" dir="auto">
              {data.lesson.estimated_minutes != null && <span>{tf('lesson.readTime', { n: Math.round(data.lesson.estimated_minutes) })}</span>}
              {hasExercise && (
                <>
                  <span aria-hidden="true">·</span>
                  <span>{t('lessons.gradedExercise')}</span>
                  <span aria-hidden="true">·</span>
                  <span className="font-mono text-amber-text" dir="ltr">{tf('lessons.credits', { n: data.credits })}</span>
                </>
              )}
            </div>
          </header>

          {hasExercise && (
            // A full-width opaque bar, not a floating pill: content (the code
            // editor included) scrolls beneath it instead of showing around it,
            // and the scroll container's scroll-padding keeps a focused line
            // or the caret below it.
            <div
              data-testid="lesson-step-switcher"
              className="sticky top-14 z-20 -mx-4 border-b border-border bg-void/95 px-4 py-1.5 backdrop-blur sm:-mx-6 sm:px-6 lg:top-0 lg:-mx-8 lg:px-8"
            >
              <LessonStepSwitch active={active} hasExercise={hasExercise} onSelect={scrollTo} />
            </div>
          )}

          {/* ── Body: article + module aside ── */}
          <div className="flex flex-wrap items-start gap-8">
            <article ref={articleRef} className="min-w-0 max-w-[760px] flex-[1_1_560px] space-y-[18px] text-[16px] leading-[1.95] text-bright [text-wrap:pretty]">
              {data.lesson.is_locked ? (
                <Card className="space-y-3 p-8 text-center">
                  <p className="text-sm font-medium text-bright">Purchase this course to unlock this content.</p>
                  <Link href={`/courses/${data.lesson.course_slug ?? courseSlug}`} className={buttonStyles({ variant: 'ghost', size: 'sm' })}>
                    {t('nav.explore')}
                  </Link>
                </Card>
              ) : (
                <MarkdownLesson content={body.text} blocks={body.blocks} dir={body.shownIn === 'ar' ? 'rtl' : 'ltr'} />
              )}
            </article>

            <LessonAside courseSlug={data.course.slug} lessons={data.moduleLessons} />
            {/* [mentor-v2] */}
            {mentorV2Enabled() && (
              <LessonMentorLayer
                // One mentor per lesson: moving to another lesson must not leave the previous
                // lesson's questions and answers in the panel under the new lesson's title.
                key={data.lesson.id}
                articleRef={articleRef}
                courseId={data.course.slug}
                lessonId={String(data.lesson.id)}
                lessonNumber={data.lessonNumber}
                onOpenChange={setMentorPanelOpen}
              />
            )}
            {/* [/mentor-v2] */}
          </div>

          {hasExercise && (
            <div className="flex justify-end border-t border-border pt-5">
              <Button size="sm" onClick={() => scrollTo('exercise')}>
                {t('lessons.nextExercise')}
                <ArrowRight size={14} className="rtl:rotate-180" aria-hidden="true" />
              </Button>
            </div>
          )}

          {/* ── Divider + exercise ── */}
          {hasExercise && (
            <>
              <div ref={dividerRef} className="flex items-center gap-3 pt-[18px]">
                <span className="h-px flex-1 bg-border" aria-hidden="true" />
              </div>

              <LessonExercises
                courseSlug={courseSlug}
                exercises={data.exercises}
                indexOffset={data.exerciseIndex}
                total={data.exerciseTotal}
                onPassed={exercise => handleExercisePassed(exercise.id, exercise.exercise_type)}
              />
            </>
          )}

          <nav
            aria-label={t('lessons.navigation')}
            className="flex flex-wrap items-center justify-between gap-3 border-t border-border pt-5"
          >
            <div className="min-w-0 flex-1">
              {previousHref && (
                <Link href={previousHref} className={buttonStyles({ variant: 'ghost', size: 'sm' })}>
                  <ArrowLeft size={14} className="rtl:rotate-180" aria-hidden="true" />
                  {t('lessons.previousLesson')}
                </Link>
              )}
            </div>

            {lessonComplete ? (
              <span className="inline-flex min-h-9 items-center gap-1.5 text-sm text-emerald">
                <CheckCircle size={15} aria-hidden="true" />
                {t('course.completed')}
              </span>
            ) : (
              <Button size="sm" variant="outline" loading={marking} onClick={() => void markComplete()}>
                {t('course.markComplete')}
              </Button>
            )}

            <div className="flex min-w-0 flex-1 justify-end">
              {nextHref && (
                <Link href={nextHref} className={buttonStyles({ size: 'sm' })}>
                  {t('lessons.nextLesson')}
                  <ArrowRight size={14} className="rtl:rotate-180" aria-hidden="true" />
                </Link>
              )}
            </div>
          </nav>
        </div>
      </div>
    </AppShell>
  )
}
