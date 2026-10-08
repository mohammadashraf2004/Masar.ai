'use client'
import { useEffect, useRef, useState, type UIEvent } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Badge, DifficultyBadge, ProgressBar, Spinner } from '@/components/ui/index'
import { Button, buttonStyles } from '@/components/ui/Button'
import { QuizPanel } from '@/components/ui/QuizPanel'
import { ExerciseCard } from '@/components/ui/ExerciseCard'
import { ProjectCard } from '@/components/ui/ProjectCard'
import { ProjectSubmit } from '@/components/ui/ProjectSubmit'
import { api } from '@/lib/api'
import type { ToolCourse, ToolTopic, ToolEnrollment, Lesson } from '@/types'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { localizedTitle, localizedDescription, localizedBody } from '@/lib/content-language'
import { CourseVocabulary } from '@/components/ui/TechnicalTerm'
import { rolesForTerms } from '@/content/terminology'
import {
  ChevronDown, ChevronRight, BookOpen, Code, FolderKanban, HelpCircle,
  CheckCircle, Circle, Play, Layers, Briefcase, Info, Lock,
} from 'lucide-react'
import { MarkdownLesson } from '@/components/ui/MarkdownLesson'

/** A curriculum course has no tool enrollment: show its course enrollment in the same shape. */
function asEnrollment(course: ToolCourse, progressPct: number): ToolEnrollment {
  return {
    id: 0, tool_course_id: course.id, progress_pct: progressPct, enrolled_at: '',
    tool_course: { ...course, topic_count: course.topics.length },
  }
}

/**
 * The lesson viewer. A tool course (LangChain, Docker...) and a curriculum course
 * (`/courses/course-001/learn`) share it: same topics, lessons, exercises, quizzes
 * and projects. They differ only in what "enrolled" means. A curriculum course's
 * enrollment is the platform's own course enrollment (independent of any track),
 * the one the catalogue, readiness and recommendations read, so that is what is
 * shown and created here for it.
 */
export function CourseViewer({ slug, curriculum = false }: { slug: string; curriculum?: boolean }) {
  const { isLoading: authLoading, isAuthenticated } = useAuth()
  const { t, tf, language } = useI18n()
  const [course, setCourse] = useState<ToolCourse | null>(null)
  const [enrollment, setEnrollment] = useState<ToolEnrollment | null>(null)
  const [activeTopic, setActiveTopic] = useState<ToolTopic | null>(null)
  const [activeTab, setActiveTab] = useState<'lesson' | 'exercise' | 'quiz' | 'project'>('lesson')
  const [loading, setLoading] = useState(true)
  const [enrolling, setEnrolling] = useState(false)
  const [readerCompact, setReaderCompact] = useState(false)
  const pageScrollRef = useRef<HTMLDivElement>(null)
  const sectionSwitcherRef = useRef<HTMLDivElement>(null)
  const contentTopRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // The auth store is persisted and hydrates after the first client render.
    // Starting an authenticated curriculum request before that point sends no
    // bearer token; the 401 used to be swallowed below and the viewer stayed
    // permanently empty because hydration was not an effect dependency.
    if (authLoading || !isAuthenticated) return

    let cancelled = false
    async function load() {
      try {
        let c: ToolCourse
        if (curriculum) {
          const [loaded, progress] = await Promise.all([api.getToolCourse(slug), api.getCourseProgress(slug)])
          c = loaded
          if (progress.enrolled) setEnrollment(asEnrollment(c, progress.progress_percentage))
        } else {
          const [loaded, enrs] = await Promise.all([api.getToolCourse(slug), api.getMyToolEnrollments()])
          c = loaded
          const enr = enrs.find(e => e.tool_course.slug === slug)
          if (enr) setEnrollment(enr)
        }
        if (!cancelled) {
          setCourse(c)
          if (c.topics?.[0]) setActiveTopic(c.topics[0])
        }
      } catch {}
      if (!cancelled) setLoading(false)
    }
    load()
    return () => { cancelled = true }
  }, [slug, curriculum, authLoading, isAuthenticated])

  async function handleEnroll() {
    if (!course) return
    setEnrolling(true)
    try {
      if (curriculum) {
        const done = await api.enrollInCourse(slug)
        setEnrollment(asEnrollment(course, done.enrollment.progress_percentage))
      } else {
        setEnrollment(await api.enrollToolCourse(course.id))
      }
    } catch {}
    setEnrolling(false)
  }

  function handleReaderScroll(event: UIEvent<HTMLDivElement>) {
    const compact = event.currentTarget.scrollTop > 72
    setReaderCompact(previous => previous === compact ? previous : compact)
  }

  function selectTab(tab: typeof activeTab) {
    setActiveTab(tab)

    // Every section starts immediately below the sticky switcher. Without
    // resetting this page-owned scrollport, changing tabs near the end of a
    // long lesson can land halfway through (or below) the next section.
    requestAnimationFrame(() => {
      const root = pageScrollRef.current
      const content = contentTopRef.current
      if (!root || !content) return
      const switcherHeight = sectionSwitcherRef.current?.getBoundingClientRect().height ?? 0
      const top = root.scrollTop + content.getBoundingClientRect().top - root.getBoundingClientRect().top - switcherHeight
      root.scrollTo?.({ top, behavior: 'smooth' })
    })
  }

  if (loading) return (
    <AppShell>
      <div className="flex-1 flex items-center justify-center">
        <Spinner announce className="w-6 h-6" />
      </div>
    </AppShell>
  )

  if (!course) return (
    <AppShell>
      <div className="flex-1 flex items-center justify-center text-ghost">{t('course.notFound')}</div>
    </AppShell>
  )

  const sections = activeTopic ? [
    { key: 'lesson' as const, icon: BookOpen, label: t('course.lessons'), count: activeTopic.lessons.length },
    { key: 'exercise' as const, icon: Code, label: t('course.exercises'), count: activeTopic.exercises.length },
    { key: 'quiz' as const, icon: HelpCircle, label: t('course.quiz'), count: activeTopic.quizzes.length },
    { key: 'project' as const, icon: FolderKanban, label: t('course.project'), count: activeTopic.projects.length },
  ] : []
  const activeSectionIndex = sections.findIndex(section => section.key === activeTab)
  const nextSection = sections.slice(activeSectionIndex + 1).find(section => section.count > 0)
  const activeTopicIndex = activeTopic ? course.topics.findIndex(topic => topic.id === activeTopic.id) : -1
  const nextTopic = activeTopicIndex >= 0 ? course.topics[activeTopicIndex + 1] ?? null : null

  return (
    <AppShell>
      {/* [code-cell] One page-level scroller lets the course and topic headers
          move away. A nested lesson-only scroller left half the viewport fixed. */}
      <div
        ref={pageScrollRef}
        data-testid="course-page-scroll"
        className="min-h-0 min-w-0 flex-1 overflow-y-auto overflow-x-hidden"
        onScroll={handleReaderScroll}
      >
        <PageHeader
          title={`${course.icon ?? ''} ${localizedTitle(course, language)}`}
          subtitle={localizedDescription(course, language)}
          dirAuto
          action={
            enrollment ? (
              <div className="flex items-center gap-2">
                <span className="text-xs text-emerald">{t('course.enrolled')}</span>
                <ProgressBar value={enrollment.progress_pct} className="w-24" />
              </div>
            ) : (
              <Button onClick={handleEnroll} loading={enrolling} size="sm">
                {t('course.startLearning')}
              </Button>
            )
          }
        />

        <div className="flex min-w-0 flex-col lg:flex-row">
        {/* ── Topics sidebar (flat — no levels) ── */}
        <div
          data-testid="course-topic-rail"
          className={cn(
            'max-h-[40vh] w-full shrink-0 overflow-y-auto border-b border-border bg-ink py-4 transition-[width] duration-200 lg:sticky lg:top-0 lg:max-h-dvh lg:border-b-0 lg:border-e',
            readerCompact ? 'lg:w-20' : 'lg:w-56 xl:w-64',
          )}
        >
          {course.topics.length === 0 ? (
            <div className="px-4 py-8 text-center">
              <Layers size={24} className="text-muted mx-auto mb-2" />
              <p className="text-xs text-ghost leading-relaxed">
                {tf('course.drafting', { title: localizedTitle(course, language) })}
              </p>
            </div>
          ) : (
            <div className="px-2">
              {course.topics.map(topic => {
                const active = activeTopic?.id === topic.id
                return (
                  <button
                    key={topic.id}
                    aria-label={localizedTitle(topic, language)}
                    title={readerCompact ? localizedTitle(topic, language) : undefined}
                    className={cn(
                      'my-0.5 w-full rounded px-3 py-2 text-start text-sm transition-all',
                      readerCompact && 'lg:px-2',
                      active
                        ? 'bg-amber/10 text-amber-text border border-amber/20'
                        : 'text-dim hover:text-bright hover:bg-surface border border-transparent'
                    )}
                    onClick={() => {
                      setActiveTopic(topic)
                      selectTab('lesson')
                    }}
                  >
                    <div className={cn('flex items-center gap-2', readerCompact && 'lg:justify-center')}>
                      <Circle size={8} className={cn(active ? 'text-amber-text' : 'text-ghost', readerCompact && 'lg:hidden')} />
                      <span dir="auto" className={cn('flex-1', readerCompact && 'lg:sr-only')}>{localizedTitle(topic, language)}</span>
                      <span
                        aria-hidden="true"
                        className={cn(
                          'hidden size-8 items-center justify-center rounded-md border font-mono text-xs',
                          readerCompact && 'lg:inline-flex',
                          active ? 'border-amber/30 bg-amber/10 text-amber-text' : 'border-border text-dim',
                        )}
                      >
                        {topic.order}
                      </span>
                    </div>
                    <div className={cn('mt-1 ms-3.5 flex items-center gap-2', readerCompact && 'lg:hidden')}>
                      <DifficultyBadge level={topic.difficulty} className="text-xs py-0" />
                      {topic.estimated_hours != null && <span className="text-lc-meta text-ghost">{tf('card.hours', { n: Math.round(topic.estimated_hours) })}</span>}
                      {topic.is_optional === true && (
                        <Badge variant="ghost">
                          {course.slug === 'course-016' ? t('course.optionalKubernetes') : t('course.optionalModule')}
                        </Badge>
                      )}
                    </div>
                  </button>
                )
              })}
            </div>
          )}
        </div>

        {/* ── Topic content ── */}
        {activeTopic ? (
          <div className="flex min-w-0 flex-1 flex-col">
            <div className="shrink-0 border-b border-border px-4 py-4 sm:px-6 sm:py-5 lg:px-8">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 dir="auto" className="font-display font-bold text-white text-xl mb-2">
                    {localizedTitle(activeTopic, language)}
                  </h2>
                  <div className="flex items-center gap-2 flex-wrap">
                    <DifficultyBadge level={activeTopic.difficulty} />
                    {activeTopic.estimated_hours != null && <Badge variant="ghost">{tf('course.estimatedHours', { n: Math.round(activeTopic.estimated_hours) })}</Badge>}
                    {activeTopic.is_optional === true && (
                      <Badge variant="ghost">
                        {course.slug === 'course-016' ? t('course.optionalKubernetes') : t('course.optionalModule')}
                      </Badge>
                    )}
                    {activeTopic.skill_tags.map(tag => (
                      <Badge key={tag} variant="ghost">{tag}</Badge>
                    ))}
                  </div>
                </div>
              </div>

              </div>

            <div
              ref={sectionSwitcherRef}
              data-testid="course-section-switcher"
              className="sticky top-0 z-20 flex items-center gap-1 overflow-x-auto border-b border-border bg-void/95 px-4 py-2 shadow-[0_8px_20px_rgb(0_0_0/0.12)] backdrop-blur sm:px-6 lg:px-8"
            >
                {sections.map(({ key, icon: Icon, label, count }) => (
                  <button
                    key={key}
                    onClick={() => selectTab(key)}
                    aria-pressed={activeTab === key}
                    className={cn(
                      'flex shrink-0 items-center gap-2 whitespace-nowrap px-4 py-2 min-h-[44px] lg:min-h-0 rounded text-sm transition-all',
                      activeTab === key
                        ? 'bg-amber/10 text-amber-text border border-amber/20'
                        : 'text-ghost hover:text-soft border border-transparent'
                    )}
                  >
                    <Icon size={13} />
                    {label}
                    <span className={cn(
                      'text-xs px-1.5 py-0.5 rounded',
                      activeTab === key ? 'bg-amber/20 text-amber-text' : 'bg-muted text-ghost'
                    )}>
                      {count}
                    </span>
                  </button>
                ))}
            </div>

            <div
              ref={contentTopRef}
              data-testid="course-content-scroll"
              className="min-w-0 overflow-x-hidden px-4 py-6 sm:px-6 lg:px-8"
            >
              {activeTab === 'lesson' && (
                <div className="mx-auto w-full max-w-5xl space-y-4">
                  {activeTopic.lessons.length === 0 ? (
                    <p className="text-ghost text-sm">{t('course.noLessons')}</p>
                  ) : activeTopic.lessons.map((lesson, i) => (
                    <LessonCard
                      key={lesson.id}
                      lesson={lesson}
                      index={i}
                      topicId={activeTopic.id}
                      courseSlug={course.slug}
                    />
                  ))}

                  {/* The terminology this topic teaches, then the roles that
                      ask for it — Arabic explains the concept, the English
                      term is what a job description will say. */}
                  <CourseVocabulary
                    terms={[...(activeTopic.technical_terms ?? []), ...(course.technical_terms ?? [])]}
                    className="pt-4"
                  />
                  <JobRolePanel
                    terms={[...(activeTopic.technical_terms ?? []), ...(course.technical_terms ?? [])]}
                    industrySkills={course.industry_skills ?? []}
                  />
                </div>
              )}

              {activeTab === 'exercise' && (
                <div className="mx-auto w-full max-w-5xl space-y-5">
                  {activeTopic.exercises.length === 0 ? (
                    <p className="text-ghost text-sm">{t('exercise.noneYet')}</p>
                  ) : activeTopic.exercises.map((ex, i) => ex.is_locked ? (
                    <LockedContent key={ex.id} courseSlug={ex.course_slug} />
                  ) : (
                    <div key={ex.id}>
                      <ExerciseCard
                        exercise={ex}
                        index={i}
                        total={activeTopic.exercises.length}
                      />
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'quiz' && (
                activeTopic.quizzes.length === 0 ? (
                  <p className="text-ghost text-sm">No quiz for this topic yet.</p>
                ) : (
                  <div className="space-y-8">
                    {activeTopic.quizzes.map(quiz => quiz.is_locked ? (
                      <LockedContent key={quiz.id} courseSlug={quiz.course_slug} />
                    ) : <QuizPanel key={quiz.id} quiz={quiz} />)}
                  </div>
                )
              )}

              {activeTab === 'project' && (
                <div className="mx-auto w-full max-w-5xl space-y-5">
                  {activeTopic.projects.length === 0 ? (
                    <p className="text-ghost text-sm">{t('project.noneYet')}</p>
                  ) : activeTopic.projects.map(proj => proj.is_locked ? (
                    <LockedContent key={proj.id} courseSlug={proj.course_slug} />
                  ) : (
                    // Tool-course projects were display-only — no way to
                    // submit one, though the endpoint takes any project id
                    // regardless of which kind of topic it hangs off.
                    <ProjectCard
                      key={proj.id}
                      project={proj}
                      footer={<ProjectSubmit project={proj} />}
                    />
                  ))}
                </div>
              )}

              {nextSection && (
                <div className="mx-auto mt-8 flex w-full max-w-5xl justify-end border-t border-border pt-5">
                  <Button size="sm" onClick={() => selectTab(nextSection.key)}>
                    {tf('course.nextSection', { section: nextSection.label })}
                    <ChevronRight size={14} className="rtl:rotate-180" aria-hidden="true" />
                  </Button>
                </div>
              )}

              {!nextSection && nextTopic && (
                <div className="mx-auto mt-8 flex w-full max-w-5xl justify-end border-t border-border pt-5">
                  <Button
                    size="sm"
                    onClick={() => {
                      setActiveTopic(nextTopic)
                      selectTab('lesson')
                    }}
                  >
                    {tf('course.nextModule', { module: localizedTitle(nextTopic, language) })}
                    <ChevronRight size={14} className="rtl:rotate-180" aria-hidden="true" />
                  </Button>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-ghost flex-col gap-2">
            <BookOpen size={32} className="text-muted" />
            <p className="text-sm">
              {course.topics.length === 0 ? 'Content coming soon.' : 'Select a topic from the left to start.'}
            </p>
          </div>
        )}
        </div>
      </div>
      {/* [/code-cell] */}
    </AppShell>
  )
}

/** "Where you'll see this" — the terms this topic teaches, mapped to the
 *  roles whose job descriptions use them. The point of keeping terminology
 *  in English is employability, so the platform closes that loop explicitly
 *  rather than leaving the student to infer it. */
function JobRolePanel({ terms, industrySkills }: { terms: string[]; industrySkills: string[] }) {
  const { t } = useI18n()
  const roles = rolesForTerms(terms).slice(0, 3)
  if (roles.length === 0 && industrySkills.length === 0) return null

  return (
    <div className="pt-6">
      <div className="flex items-center gap-2 mb-3">
        <Briefcase size={14} className="text-sky" />
        <h3 className="text-sm font-medium text-bright">{t('term.seenIn')}</h3>
      </div>

      {industrySkills.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-3">
          {industrySkills.map(skill => (
            <span
              key={skill}
              className="text-lc-label px-2 py-0.5 rounded border border-border bg-muted/40 text-dim"
              dir="ltr"
            >
              {skill}
            </span>
          ))}
        </div>
      )}

      <div className="space-y-2.5">
        {roles.map(({ role, matched }) => (
          <Card key={role.id} className="p-4">
            <div className="flex items-baseline justify-between gap-2">
              <p className="font-display font-bold text-bright text-sm" dir="ltr">{role.title}</p>
              <span className="text-lc-label text-ghost font-mono">{matched.length}</span>
            </div>
            <p className="text-lc-meta text-soft mt-1" dir="rtl">{role.summaryAr}</p>
            <ul className="mt-2.5 space-y-1">
              {role.jdPhrases.slice(0, 2).map(phrase => (
                <li
                  key={phrase}
                  className="text-lc-meta text-ghost ps-2.5 border-s border-border"
                  dir="ltr"
                >
                  {phrase}
                </li>
              ))}
            </ul>
          </Card>
        ))}
      </div>
    </div>
  )
}

function LessonCard({ lesson, index, topicId, courseSlug }: {
  lesson: Lesson
  index: number
  topicId: number
  courseSlug: string
}) {
  const { t, tf, language } = useI18n()
  const [expanded, setExpanded] = useState(index === 0)
  const [marking, setMarking] = useState(false)
  const [done, setDone] = useState(false)

  // The body the reader gets, and whether it is the language they asked for.
  // A lesson with no Arabic version still renders — in English, with a note
  // saying so, rather than an empty page.
  const body = localizedBody(lesson, language)

  if (lesson.is_locked) {
    return (
      <LockedContent
        courseSlug={lesson.course_slug}
        title={localizedTitle(lesson, language)}
        detailHref={`/courses/${courseSlug}/lessons/${lesson.id}`}
      />
    )
  }

  async function markComplete() {
    setMarking(true)
    try {
      await api.updateToolTopicProgress(topicId, { lesson_id: lesson.id })
      setDone(true)
    } catch {}
    setMarking(false)
  }

  return (
    <Card className={cn('overflow-hidden transition-all', expanded ? 'border-amber/20' : '')}>
      <div className="flex items-center">
        <button
          className="flex min-w-0 flex-1 items-center gap-4 p-4 text-start transition-colors hover:bg-surface/50 sm:p-5"
          aria-expanded={expanded}
          aria-controls={`lesson-body-${lesson.id}`}
          onClick={() => setExpanded(!expanded)}
        >
          <div className="flex size-7 shrink-0 items-center justify-center rounded border border-amber/20 bg-amber/10">
            <Play size={11} className="text-amber-text" />
          </div>
          <div className="min-w-0 flex-1">
            <p dir="auto" className="font-display font-bold text-bright text-lc-title">{localizedTitle(lesson, language)}</p>
            {lesson.estimated_minutes != null && <p className="mt-1 text-lc-meta text-ghost">{tf('lesson.readTime', { n: Math.round(lesson.estimated_minutes) })}</p>}
          </div>
          {expanded
            ? <ChevronDown size={14} className="shrink-0 text-ghost" />
            : <ChevronRight size={14} className="shrink-0 text-ghost rtl:rotate-180" />
          }
        </button>
        <Link
          href={`/courses/${courseSlug}/lessons/${lesson.id}`}
          className={buttonStyles({ variant: 'outline', size: 'sm', className: 'me-3 shrink-0 sm:me-4' })}
        >
          {t('lessons.openLesson')}
        </Link>
      </div>

      {expanded && (
        <div id={`lesson-body-${lesson.id}`} className="border-t border-border px-4 pb-6 sm:px-6">
          {body.isFallback && (
            <div className="mt-4 flex items-start gap-2 px-3 py-2 rounded-lg bg-sky/5 border border-sky/20">
              <Info size={13} className="text-sky shrink-0 mt-0.5" />
              <p className="text-lc-meta text-soft">{t('course.arabicUnavailable')}</p>
            </div>
          )}
          <div className="mt-4">
            {/* Direction follows the text that is actually rendered, not the
                reader's preference: an English fallback body stays LTR. */}
            <MarkdownLesson
              content={body.text}
              blocks={body.blocks}
              dir={body.shownIn === 'ar' ? 'rtl' : 'ltr'}
            />
          </div>
          <div className="mt-4 flex flex-wrap items-center gap-3 border-t border-border pt-4">
            {done ? (
              <span className="flex items-center gap-1.5 text-xs text-emerald">
                <CheckCircle size={13} /> {t('course.completed')}
              </span>
            ) : (
              <Button size="sm" variant="outline" loading={marking} onClick={markComplete}>
                {t('course.markComplete')}
              </Button>
            )}
          </div>
        </div>
      )}
    </Card>
  )
}

function LockedContent({ courseSlug, title, detailHref }: {
  courseSlug?: string | null
  title?: string
  detailHref?: string
}) {
  const { t } = useI18n()
  return (
    <Card className="flex flex-col items-center gap-3 p-8 text-center">
      <Lock size={24} className="text-amber-text" aria-hidden="true" />
      {title && <p dir="auto" className="font-display text-sm font-bold text-bright">{title}</p>}
      <p className="text-sm font-medium text-bright">Purchase this course to unlock this content.</p>
      <div className="flex flex-wrap justify-center gap-2">
        {detailHref && (
          <Link href={detailHref} className={buttonStyles({ variant: 'outline', size: 'sm' })}>
            {t('lessons.openLesson')}
          </Link>
        )}
        <Link href={courseSlug ? `/courses/${courseSlug}` : '/explore'} className={buttonStyles({ size: 'sm' })}>
          View course
        </Link>
      </div>
    </Card>
  )
}
