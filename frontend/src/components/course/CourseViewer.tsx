'use client'
import { useEffect, useState } from 'react'
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
import { localizedTitle, localizedDescription, localizedContent } from '@/lib/content-language'
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
  useAuth()
  const { t, tf, language } = useI18n()
  const [course, setCourse] = useState<ToolCourse | null>(null)
  const [enrollment, setEnrollment] = useState<ToolEnrollment | null>(null)
  const [activeTopic, setActiveTopic] = useState<ToolTopic | null>(null)
  const [activeTab, setActiveTab] = useState<'lesson' | 'exercise' | 'quiz' | 'project'>('lesson')
  const [loading, setLoading] = useState(true)
  const [enrolling, setEnrolling] = useState(false)

  useEffect(() => {
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
        setCourse(c)
        if (c.topics?.[0]) setActiveTopic(c.topics[0])
      } catch {}
      setLoading(false)
    }
    load()
  }, [slug, curriculum])

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

  return (
    <AppShell>
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

      <div className="flex-1 flex flex-col lg:flex-row lg:overflow-hidden min-w-0">
        {/* ── Topics sidebar (flat — no levels) ── */}
        <div className="w-full lg:w-60 xl:w-72 shrink-0 max-h-[40vh] lg:max-h-none overflow-y-auto border-b lg:border-b-0 lg:border-e border-border bg-ink py-4">
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
                    className={cn(
                      'w-full text-start px-3 py-2 rounded text-sm transition-all my-0.5',
                      active
                        ? 'bg-amber/10 text-amber-text border border-amber/20'
                        : 'text-dim hover:text-bright hover:bg-surface border border-transparent'
                    )}
                    onClick={() => setActiveTopic(topic)}
                  >
                    <div className="flex items-center gap-2">
                      <Circle size={8} className={active ? 'text-amber-text' : 'text-ghost'} />
                      <span dir="auto" className="flex-1">{localizedTitle(topic, language)}</span>
                    </div>
                    <div className="flex items-center gap-2 mt-1 ms-3.5">
                      <DifficultyBadge level={topic.difficulty} className="text-xs py-0" />
                      {topic.estimated_hours != null && <span className="text-lc-meta text-ghost">{tf('card.hours', { n: topic.estimated_hours })}</span>}
                    </div>
                  </button>
                )
              })}
            </div>
          )}
        </div>

        {/* ── Topic content ── */}
        {activeTopic ? (
          <div className="flex-1 min-w-0 flex flex-col lg:overflow-hidden">
            <div className="px-4 sm:px-6 lg:px-8 py-4 sm:py-5 border-b border-border shrink-0">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 dir="auto" className="font-display font-bold text-white text-xl mb-2">
                    {localizedTitle(activeTopic, language)}
                  </h2>
                  <div className="flex items-center gap-2 flex-wrap">
                    <DifficultyBadge level={activeTopic.difficulty} />
                    {activeTopic.estimated_hours != null && <Badge variant="ghost">{tf('course.estimatedHours', { n: activeTopic.estimated_hours })}</Badge>}
                    {activeTopic.skill_tags.map(tag => (
                      <Badge key={tag} variant="ghost">{tag}</Badge>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-1 mt-4 py-1 -my-1 overflow-x-auto">
                {[
                  { key: 'lesson', icon: BookOpen, label: t('course.lessons'), count: activeTopic.lessons.length },
                  { key: 'exercise', icon: Code, label: t('course.exercises'), count: activeTopic.exercises.length },
                  { key: 'quiz', icon: HelpCircle, label: t('course.quiz'), count: activeTopic.quizzes.length },
                  { key: 'project', icon: FolderKanban, label: t('course.project'), count: activeTopic.projects.length },
                ].map(({ key, icon: Icon, label, count }) => (
                  <button
                    key={key}
                    onClick={() => setActiveTab(key as typeof activeTab)}
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
            </div>

            <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6">
              {activeTab === 'lesson' && (
                <div className="space-y-4 max-w-3xl">
                  {activeTopic.lessons.length === 0 ? (
                    <p className="text-ghost text-sm">{t('course.noLessons')}</p>
                  ) : activeTopic.lessons.map((lesson, i) => (
                    <LessonCard key={lesson.id} lesson={lesson} index={i} topicId={activeTopic.id} />
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
                <div className="space-y-5 max-w-3xl">
                  {activeTopic.exercises.length === 0 ? (
                    <p className="text-ghost text-sm">{t('exercise.noneYet')}</p>
                  ) : activeTopic.exercises.map((ex, i) => ex.is_locked ? (
                    <LockedContent key={ex.id} courseSlug={ex.course_slug} />
                  ) : <ExerciseCard key={ex.id} exercise={ex} index={i} total={activeTopic.exercises.length} />)}
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
                <div className="space-y-5 max-w-3xl">
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

function LessonCard({ lesson, index, topicId }: {
  lesson: Lesson
  index: number
  topicId: number
}) {
  const { t, tf, language } = useI18n()
  const [expanded, setExpanded] = useState(index === 0)
  const [marking, setMarking] = useState(false)
  const [done, setDone] = useState(false)

  // The body the reader gets, and whether it is the language they asked for.
  // A lesson with no Arabic version still renders — in English, with a note
  // saying so, rather than an empty page.
  const body = localizedContent(lesson, language)

  if (lesson.is_locked) return <LockedContent courseSlug={lesson.course_slug} />

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
      <button
        className="w-full flex items-center gap-4 p-4 sm:p-5 text-start hover:bg-surface/50 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="w-7 h-7 rounded bg-amber/10 border border-amber/20 flex items-center justify-center shrink-0">
          <Play size={11} className="text-amber-text" />
        </div>
        <div className="flex-1 min-w-0">
          <p dir="auto" className="font-display font-bold text-bright text-lc-title">{localizedTitle(lesson, language)}</p>
          {lesson.estimated_minutes != null && <p className="text-lc-meta text-ghost mt-1">{tf('lesson.readTime', { n: lesson.estimated_minutes })}</p>}
        </div>
        {expanded
          ? <ChevronDown size={14} className="text-ghost shrink-0" />
          : <ChevronRight size={14} className="text-ghost shrink-0 rtl:rotate-180" />
        }
      </button>

      {expanded && (
        <div className="px-4 sm:px-6 pb-6 border-t border-border">
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
              dir={body.shownIn === 'ar' ? 'rtl' : 'ltr'}
            />
          </div>
          <div className="mt-4 pt-4 border-t border-border">
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

function LockedContent({ courseSlug }: { courseSlug?: string | null }) {
  return (
    <Card className="flex flex-col items-center gap-3 p-8 text-center">
      <Lock size={24} className="text-amber-text" aria-hidden="true" />
      <p className="text-sm font-medium text-bright">Purchase this course to unlock this content.</p>
      <Link href={courseSlug ? `/courses/${courseSlug}` : '/explore'} className={buttonStyles({ size: 'sm' })}>
        View course
      </Link>
    </Card>
  )
}
