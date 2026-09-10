'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Badge, ProgressBar, Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
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
  CheckCircle, Circle, Play, Layers, Briefcase, Info,
} from 'lucide-react'
import { MarkdownLesson } from '@/components/ui/MarkdownLesson'

export default function ToolCoursePage() {
  useAuth()
  const { t, language } = useI18n()
  const { slug } = useParams() as { slug: string }
  const [course, setCourse] = useState<ToolCourse | null>(null)
  const [enrollment, setEnrollment] = useState<ToolEnrollment | null>(null)
  const [activeTopic, setActiveTopic] = useState<ToolTopic | null>(null)
  const [activeTab, setActiveTab] = useState<'lesson' | 'exercise' | 'quiz' | 'project'>('lesson')
  const [loading, setLoading] = useState(true)
  const [enrolling, setEnrolling] = useState(false)

  useEffect(() => {
    async function load() {
      try {
        const [c, enrs] = await Promise.all([api.getToolCourse(slug), api.getMyToolEnrollments()])
        setCourse(c)
        const enr = enrs.find(e => e.tool_course.slug === slug)
        if (enr) setEnrollment(enr)
        if (c.topics?.[0]) setActiveTopic(c.topics[0])
      } catch {}
      setLoading(false)
    }
    load()
  }, [slug])

  async function handleEnroll() {
    if (!course) return
    setEnrolling(true)
    try {
      const enr = await api.enrollToolCourse(course.id)
      setEnrollment(enr)
    } catch {}
    setEnrolling(false)
  }

  if (loading) return (
    <AppShell>
      <div className="flex-1 flex items-center justify-center">
        <Spinner className="w-6 h-6" />
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
        <div className="w-full lg:w-72 shrink-0 max-h-[40vh] lg:max-h-none overflow-y-auto border-b lg:border-b-0 lg:border-e border-border bg-ink py-4">
          {course.topics.length === 0 ? (
            <div className="px-4 py-8 text-center">
              <Layers size={24} className="text-muted mx-auto mb-2" />
              <p className="text-xs text-ghost leading-relaxed">
                Content for {course.title} is being drafted. Check back soon.
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
                        ? 'bg-amber/10 text-amber border border-amber/20'
                        : 'text-dim hover:text-bright hover:bg-surface border border-transparent'
                    )}
                    onClick={() => setActiveTopic(topic)}
                  >
                    <div className="flex items-center gap-2">
                      <Circle size={8} className={active ? 'text-amber' : 'text-ghost'} />
                      <span className="flex-1">{localizedTitle(topic, language)}</span>
                    </div>
                    <div className="flex items-center gap-2 mt-1 ms-3.5">
                      <Badge variant={topic.difficulty} className="text-[10px] py-0">
                        {topic.difficulty}
                      </Badge>
                      <span className="text-xs text-ghost">{topic.estimated_hours}h</span>
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
                  <h2 className="font-display font-bold text-white text-base sm:text-lg mb-2">
                    {localizedTitle(activeTopic, language)}
                  </h2>
                  <div className="flex items-center gap-2 flex-wrap">
                    <Badge variant={activeTopic.difficulty}>{activeTopic.difficulty}</Badge>
                    <Badge variant="ghost">{activeTopic.estimated_hours}h {t('course.estimated')}</Badge>
                    {activeTopic.skill_tags.map(tag => (
                      <Badge key={tag} variant="ghost">{tag}</Badge>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-1 mt-4">
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
                      'flex items-center gap-2 px-4 py-2 rounded text-sm transition-all',
                      activeTab === key
                        ? 'bg-amber/10 text-amber border border-amber/20'
                        : 'text-ghost hover:text-soft border border-transparent'
                    )}
                  >
                    <Icon size={13} />
                    {label}
                    <span className={cn(
                      'text-xs px-1.5 py-0.5 rounded',
                      activeTab === key ? 'bg-amber/20 text-amber' : 'bg-muted text-ghost'
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
                  ) : activeTopic.exercises.map((ex, i) => (
                    <ExerciseCard
                      key={ex.id}
                      exercise={ex}
                      index={i}
                      total={activeTopic.exercises.length}
                    />
                  ))}
                </div>
              )}

              {activeTab === 'quiz' && (
                activeTopic.quizzes.length === 0 ? (
                  <p className="text-ghost text-sm">No quiz for this topic yet.</p>
                ) : (
                  <div className="space-y-8">
                    {activeTopic.quizzes.map(quiz => (
                      <QuizPanel key={quiz.id} quiz={quiz} />
                    ))}
                  </div>
                )
              )}

              {activeTab === 'project' && (
                <div className="space-y-5 max-w-3xl">
                  {activeTopic.projects.length === 0 ? (
                    <p className="text-ghost text-sm">{t('project.noneYet')}</p>
                  ) : activeTopic.projects.map(proj => (
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
              className="text-[11px] px-2 py-0.5 rounded border border-border bg-muted/40 text-dim"
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
              <span className="text-[11px] text-ghost font-mono">{matched.length}</span>
            </div>
            <p className="text-xs text-soft leading-relaxed mt-1" dir="rtl">{role.summaryAr}</p>
            <ul className="mt-2.5 space-y-1">
              {role.jdPhrases.slice(0, 2).map(phrase => (
                <li
                  key={phrase}
                  className="text-[11px] text-ghost leading-relaxed ps-2.5 border-s border-border"
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
  const { t, language } = useI18n()
  const [expanded, setExpanded] = useState(index === 0)
  const [marking, setMarking] = useState(false)
  const [done, setDone] = useState(false)

  // The body the reader gets, and whether it is the language they asked for.
  // A lesson with no Arabic version still renders — in English, with a note
  // saying so, rather than an empty page.
  const body = localizedContent(lesson, language)

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
        className="w-full flex items-center gap-4 p-5 text-start hover:bg-surface/50 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="w-7 h-7 rounded bg-amber/10 border border-amber/20 flex items-center justify-center shrink-0">
          <Play size={11} className="text-amber" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-medium text-bright text-sm">{localizedTitle(lesson, language)}</p>
          <p className="text-xs text-ghost mt-0.5">{lesson.estimated_minutes} min read</p>
        </div>
        {expanded
          ? <ChevronDown size={14} className="text-ghost shrink-0" />
          : <ChevronRight size={14} className="text-ghost shrink-0 rtl:rotate-180" />
        }
      </button>

      {expanded && (
        <div className="px-5 pb-6 border-t border-border">
          {body.isFallback && (
            <div className="mt-4 flex items-start gap-2 px-3 py-2 rounded-lg bg-sky/5 border border-sky/20">
              <Info size={13} className="text-sky shrink-0 mt-0.5" />
              <p className="text-xs text-soft leading-relaxed">{t('course.arabicUnavailable')}</p>
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
