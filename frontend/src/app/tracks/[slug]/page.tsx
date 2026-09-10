'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card } from '@/components/ui/index'
import { Badge } from '@/components/ui/index'
import { ProgressBar } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { QuizPanel } from '@/components/ui/QuizPanel'
import { ExerciseCard } from '@/components/ui/ExerciseCard'
import { ProjectCard as ProjectBrief } from '@/components/ui/ProjectCard'
import { ProjectSubmit } from '@/components/ui/ProjectSubmit'
import { api } from '@/lib/api'
import type { CareerTrack, Topic, Enrollment, Lesson, Project } from '@/types'
import { difficultyBg, cn, safeUrl } from '@/lib/utils'
import { isTrackComingSoon } from '@/lib/tracks'
import { useI18n } from '@/lib/i18n'
import {
  localizedTitle, localizedDescription, localizedContent,
} from '@/lib/content-language'
import {
  ChevronDown, ChevronRight, BookOpen, Code, FolderKanban,
  Lock, CheckCircle, Circle, ArrowRight, Play, HelpCircle
} from 'lucide-react'
import { MarkdownLesson } from '@/components/ui/MarkdownLesson'
import { CourseVocabulary } from '@/components/ui/TechnicalTerm'
import { Info } from 'lucide-react'

export default function TrackPage() {
  useAuth()
  const { t, language } = useI18n()
  const { slug } = useParams() as { slug: string }
  const [track, setTrack] = useState<CareerTrack | null>(null)
  const [enrollment, setEnrollment] = useState<Enrollment | null>(null)
  const [expandedLevel, setExpandedLevel] = useState<number>(0)
  const [activeTopic, setActiveTopic] = useState<Topic | null>(null)
  const [activeTab, setActiveTab] = useState<'lesson' | 'exercise' | 'quiz' | 'project'>('lesson')
  const [loading, setLoading] = useState(true)
  const [enrolling, setEnrolling] = useState(false)

  useEffect(() => {
    async function load() {
      try {
        const [t, enrs] = await Promise.all([api.getTrack(slug), api.getMyEnrollments()])
        setTrack(t)
        const enr = enrs.find(e => e.track.slug === slug)
        if (enr) setEnrollment(enr)
        // Auto-open first level and select first topic
        if (t.levels?.[0]?.topics?.[0]) {
          setActiveTopic(t.levels[0].topics[0])
        }
      } catch {}
      setLoading(false)
    }
    load()
  }, [slug])

  async function handleEnroll() {
    if (!track) return
    setEnrolling(true)
    try {
      const enr = await api.enroll(track.id)
      setEnrollment(enr)
    } catch {}
    setEnrolling(false)
  }

  if (loading) return (
    <AppShell>
      <div className="flex-1 flex items-center justify-center">
        <div className="w-6 h-6 border border-amber border-t-transparent rounded-full animate-spin" />
      </div>
    </AppShell>
  )

  if (!track) return (
    <AppShell>
      <div className="flex-1 flex items-center justify-center text-ghost">Track not found.</div>
    </AppShell>
  )

  return (
    <AppShell>
      <PageHeader
        title={localizedTitle(track, language)}
        subtitle={localizedDescription(track, language)}
        action={
          enrollment ? (
            <div className="flex items-center gap-2">
              <span className="text-xs text-emerald">{t('course.enrolled')}</span>
              <ProgressBar value={enrollment.completion_percentage} className="w-24" />
            </div>
          ) : isTrackComingSoon(track.slug) ? (
            // Reachable by URL even though the tracks list offers no way in,
            // so the CTA has to be gated here too — otherwise a stale link
            // enrols someone in a track with no lessons behind it.
            <Button size="sm" variant="ghost" disabled>
              {t('course.comingSoon')}
            </Button>
          ) : (
            <Button onClick={handleEnroll} loading={enrolling} size="sm">
              Enroll now
            </Button>
          )
        }
      />

      <div className="flex-1 flex flex-col lg:flex-row lg:overflow-hidden min-w-0">
        {/* ── Skill tree sidebar ── */}
        <div className="w-full lg:w-72 shrink-0 max-h-[45vh] lg:max-h-none overflow-y-auto border-b lg:border-b-0 lg:border-e border-border bg-ink py-4">
          {track.levels.map((level, li) => {
            const isOpen = expandedLevel === li
            return (
              <div key={level.id} className="mb-1">
                <button
                  className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-surface transition-colors group"
                  onClick={() => setExpandedLevel(isOpen ? -1 : li)}
                >
                  <div className="w-5 h-5 rounded bg-amber/10 border border-amber/20 flex items-center justify-center shrink-0">
                    <span className="text-xs font-mono text-amber">{li + 1}</span>
                  </div>
                  <span className="text-sm font-medium text-bright flex-1 text-start">
                    {localizedTitle(level, language)}
                  </span>
                  {isOpen
                    ? <ChevronDown size={13} className="text-ghost" />
                    : <ChevronRight size={13} className="text-ghost" />
                  }
                </button>

                {isOpen && (
                  <div className="ms-4 ps-4 border-s border-border mb-2">
                    {level.topics.map(topic => {
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
                            <Badge variant={topic.difficulty as 'beginner' | 'intermediate' | 'advanced'} className="text-[10px] py-0">
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
            )
          })}
        </div>

        {/* ── Topic content ── */}
        {activeTopic ? (
          <div className="flex-1 min-w-0 flex flex-col lg:overflow-hidden">
            {/* Topic header */}
            <div className="px-4 sm:px-6 lg:px-8 py-4 sm:py-5 border-b border-border shrink-0">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 className="font-display font-bold text-white text-base sm:text-lg mb-2">{activeTopic.title}</h2>
                  <div className="flex items-center gap-2 flex-wrap">
                    <Badge variant={activeTopic.difficulty as 'beginner' | 'intermediate' | 'advanced'}>
                      {activeTopic.difficulty}
                    </Badge>
                    <Badge variant="ghost">{activeTopic.estimated_hours}h estimated</Badge>
                    {activeTopic.skill_tags.map(tag => (
                      <Badge key={tag} variant="ghost">{tag}</Badge>
                    ))}
                  </div>
                </div>
              </div>

              {/* Content tabs */}
              <div className="flex items-center gap-1 mt-4 overflow-x-auto">
                {[
                  { key: 'lesson', icon: BookOpen, label: 'Lessons', count: activeTopic.lessons.length },
                  { key: 'exercise', icon: Code, label: 'Exercises', count: activeTopic.exercises.length },
                  { key: 'quiz', icon: HelpCircle, label: 'Quiz', count: activeTopic.quizzes.length },
                  { key: 'project', icon: FolderKanban, label: 'Projects', count: activeTopic.projects.length },
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

            {/* Content area */}
            <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6">
              {activeTab === 'lesson' && (
                <div className="space-y-4 max-w-3xl">
                  {activeTopic.lessons.length === 0 ? (
                    <p className="text-ghost text-sm">{t('course.noLessons')}</p>
                  ) : activeTopic.lessons.map((lesson, i) => (
                    <LessonCard key={lesson.id} lesson={lesson} index={i} />
                  ))}

                  {/* The English terminology this topic teaches, so the
                      student leaves able to name what they just learned. */}
                  <CourseVocabulary terms={activeTopic.technical_terms ?? []} className="pt-4" />
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
                <div className="space-y-4 max-w-3xl">
                  {activeTopic.projects.length === 0 ? (
                    <p className="text-ghost text-sm">No projects for this topic yet.</p>
                  ) : activeTopic.projects.map(proj => (
                    <ProjectCard key={proj.id} project={proj} />
                  ))}
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-ghost flex-col gap-2">
            <BookOpen size={32} className="text-muted" />
            <p className="text-sm">Select a topic from the left to start.</p>
          </div>
        )}
      </div>
    </AppShell>
  )
}

// ── Sub-components ──────────────────────────────────────────────────────────

function LessonCard({ lesson, index }: { lesson: Lesson; index: number }) {
  const { t, language } = useI18n()
  const [expanded, setExpanded] = useState(index === 0)

  // Same fallback rule as the tool-course reader: show the Arabic body when
  // it exists, otherwise the English original with a note.
  const body = localizedContent(lesson, language)

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
            <MarkdownLesson content={body.text} dir={body.shownIn === 'ar' ? 'rtl' : 'ltr'} />
          </div>
        </div>
      )}
    </Card>
  )
}

function ProjectCard({ project }: { project: Project }) {
  // Brief and submission are both shared with the tool-course reader now —
  // this page used to carry its own copy of each, and its own bugs in them.
  return <ProjectBrief project={project} footer={<ProjectSubmit project={project} />} />
}
